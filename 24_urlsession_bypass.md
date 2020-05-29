# Using LLDB to bypass URLSession
#### Bypass overview
The goal of this bypass was to set a breakpoint at the start of `URLSession:didReceiveChallenge:completionHandler:` and override the `completionHandler`.

Why?  App's often used a `completionHandler` with Apple's `NSURLSession` on iOS and macOS when deciding whether to start a `network request`.  

> completionHandler(NSURLSessionAuthChallengeCancelAuthenticationChallenge, NULL);

The above line of code is typical of an app that has implemented `Certificate Pinning`.  The app is asking _"do I trust the server,  before sending data?"_.

#### The Needle
 The code would set an `enum` based on whether it trusted the server and connection:
 ```
 typedef NS_ENUM(NSInteger, NSURLSessionAuthChallengeDisposition) {
     NSURLSessionAuthChallengeUseCredential = 0,                                       /* Use the specified credential, which may be nil */
     NSURLSessionAuthChallengePerformDefaultHandling = 1,                              /* Default handling for the challenge - as if this delegate were not implemented; the credential parameter is ignored. */
     NSURLSessionAuthChallengeCancelAuthenticationChallenge = 2,                       /* The entire request will be canceled; the credential parameter is ignored. */
     NSURLSessionAuthChallengeRejectProtectionSpace = 3,                               /* This challenge is rejected and the next authentication protection space should be tried; the credential parameter is ignored. */
 }
```
It was slow and error prone to find a small integer value in `assembly code`, unless you could place an excellent breakpoint.  It would be great if we just could watch for a `Register` value changing to something we did not like.  Then we could

https://reverse.put.as/2019/11/19/how-to-make-lldb-a-real-debugger/

There was no obvious `Symbol` or `instruction` to leverage [ as we are assuming a stripped, release app ] as you will read.

#### Alternative tip
You could also drop the `(NSURLAuthenticationChallenge *)challenge` parameter.  But that would probably cause unexpected behavior, as code would rely on the `challenge` to extract the `Certificate Chain` from the server.  If you really don't want to attack the `NSURLSessionAuthChallengeDisposition`, you could `substitute` the `challenge` with a host that is valid.

#### Bypass fail - NULL Stack Block
This bypass dropped the `Stack Block` with a NULL value.  

```
(lldb) breakpoint set --selector URLSession:didReceiveChallenge:completionHandler: -s objc_play
Breakpoint 2: where = objc_play`-[YDURLSessionDel URLSession:didReceiveChallenge:completionHandler:] at main.m:7, address = 0x0000000100001620
(lldb) c
```
At this point the Breakpoint fires.

You can then inspect every argument passed into the `Selector` (`URLSession:didReceiveChallenge:completionHandler:`):
```
(lldb) po $arg1
<YDURLSessionDel: 0x1005436c0>

(lldb) po (char *)$arg2
"URLSession:didReceiveChallenge:completionHandler:"
```
Or, a more efficient way:
```
(lldb) frame variable
(YDURLSessionDel *) self = 0x0000000102845fa0
(SEL) _cmd = "URLSession:didReceiveChallenge:completionHandler:"
(__NSURLSessionLocal *) session = 0x0000000100605f50
(NSURLAuthenticationChallenge *) challenge = 0x000000010285cbe0
(void (^)(NSURLSessionAuthChallengeDisposition, NSURLCredential *)) completionHandler = 0x00007fff30e47a04
(SecTrustRef) trust = 0x000000010285b510
```
Where is the Completion Handling pointing?
```
(lldb) image lookup -a 0x00007fff30e47a04
      Address: CFNetwork[0x00000000001e0a04] (CFNetwork.__TEXT.__text + 1964164)
      Summary: CFNetwork`___lldb_unnamed_symbol10036$$CFNetwork
```
Well, another way to get a clue what is:
```
(lldb) po $arg5     // if you stop at the Method entry
<__NSStackBlock__: 0x70000598cba8>
 signature: "v24@?0q8@"NSURLCredential"16"
 invoke   : 0x7fff30e47a04 (/System/Library/Frameworks/CFNetwork.framework/Versions/A/CFNetwork`CFHTTPCookieStorageUnscheduleFromRunLoop)
 copy     : 0x7fff30d3b7ed (/System/Library/Frameworks/CFNetwork.framework/Versions/A/CFNetwork`CFURLCredentialStorageCopyAllCredentials)
 dispose  : 0x7fff30d3b825 (/System/Library/Frameworks/CFNetwork.framework/Versions/A/CFNetwork`CFURLCredentialStorageCopyAllCredentials)
```
Now we can see this code points `CFNetwork.CFHTTPCookieStorageUnscheduleFromRunLoop`.  

If you read Apple [documentation](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/Blocks/Articles/bxVariables.html#//apple_ref/doc/uid/TP40007502-CH6-SW1) on this, you can see it copies a whole chain of code onto the `Stack`, it just starts with `Cookie` related code.

> When you copy a block, any references to other blocks from within that block are copied if necessary—an entire tree may be copied (from the top). If you have block variables and you reference a block from within the block, that block will be copied.

Let's try and remove the `Completion Handler`!
```
(lldb) po $arg5 = NULL
(lldb) c
```
It crashed.  Why?
```
Thread 2: EXC_BAD_ACCESS (code=1, address=0x10)
```
The instruction that caused the crash was `call   qword ptr [rcx + 0x10]`.  So `nulling` caused `rcx` to be `0`.  The result, a bad address.

#### Bypass fail - a fake Block
```
lldb) breakpoint set --selector URLSession:didReceiveChallenge:completionHandler: -s objc_play

(lldb) exp
1 void (^$simpleBlock)(void) = ^{NSLog(@"hello from a block!");};
(lldb) p $simpleBlock
(void (^)()) $simpleBlock = 0x00000001041ff300

// at start of the function
(lldb) po $arg5 = 0x00000001041ff300
4364169984
```
Sure enough, the same crash AFTER my fake block ran.
#### Hopper Disassembler
If you use the `pseudo-code mode` in Hopper, it attempted to understand the code flow of: `URLSession:didReceiveChallenge:completionHandler:`:
```
/* @class YDURLSessionDel */
-(void)URLSession:(void *)arg2 didReceiveChallenge:(void *)arg3 completionHandler:(void *)arg4 {
    var_30 = [[arg3 protectionSpace] serverTrust];
    [[arg3 protectionSpace] host];
    NSLog(cfstring___m__);
    SecTrustGetCertificateCount(var_30);
    NSLog(cfstring___m__);
    (*(arg4 + 0x10))(arg4, 0x2, 0x0, arg4);
    return;
}
```
We care about the line: `(*(arg4 + 0x10))(arg4, 0x2, 0x0, arg4);`.

In assembly, that is this instruction:
```
0x1000016ce <+174>: call   qword ptr [rcx + 0x10]
```
Sure enough, if you set a `breakpoint` on this `opcode`:
```
(lldb) po $arg1
<__NSStackBlock__: 0x7000050deba8>
 signature: "v24@?0q8@"NSURLCredential"16"
 invoke   : 0x7fff30e47a04 (/System/Library/Frameworks/CFNetwork.framework/Versions/A/CFNetwork`CFHTTPCookieStorageUnscheduleFromRunLoop)
 copy     : 0x7fff30d3b7ed (/System/Library/Frameworks/CFNetwork.framework/Versions/A/CFNetwork`CFURLCredentialStorageCopyAllCredentials)
 dispose  : 0x7fff30d3b825 (/System/Library/Frameworks/CFNetwork.framework/Versions/A/CFNetwork`CFURLCredentialStorageCopyAllCredentials)

(lldb) po $arg2
2

(lldb) po $arg3
<nil>

(lldb) po $arg4
<__NSStackBlock__: 0x7000050deba8>
 signature: "v24@?0q8@"NSURLCredential"16"
 invoke   : 0x7fff30e47a04 (/System/Library/Frameworks/CFNetwork.framework/Versions/A/CFNetwork`CFHTTPCookieStorageUnscheduleFromRunLoop)
 copy     : 0x7fff30d3b7ed (/System/Library/Frameworks/CFNetwork.framework/Versions/A/CFNetwork`CFURLCredentialStorageCopyAllCredentials)
 dispose  : 0x7fff30d3b825 (/System/Library/Frameworks/CFNetwork.framework/Versions/A/CFNetwork`CFURLCredentialStorageCopyAllCredentials)
```

#### Bypass fail - NOP instruction
In Hopper, the instruction that passes the values we care about was here:
```
call       qword [rcx+0x10]
```
This `opcode` passes the `NSURLSessionAuthChallengeDisposition` into an `ObjC Block`, as we saw earlier:

 `(*(arg4 + 0x10))(arg4, 0x2, 0x0, arg4);`

`0x2` is the `Cancel challenge` option, `0x0` is because we are not passing in `Credentials` from the server.

If you `step` with a debugger,  this `call` stepped to an unnamed `Symbol` inside of `/System/Library/Frameworks/CFNetwork.framework`.

If you select `Modify/NOP Region` on this `instruction` it will change the call to:
```
nop        dword [rax]
```
Then select `File/Produce New Executable` and drop the `Code Signature` when prompted. As this is macOS, it will still run without a valid `Code Signature`.  If this was `iOS` we would have to go and resign everything [ which is no big deal ].

The app runs with interesting results.  A single retry. Then the app never returns.
```
🍭 start
🍭	Challenged on: www.google.com
🍭	Cert chain length: 3
// 10 seconds later
🍭	Challenged on: www.google.com
🍭	Cert chain length: 3
```
That means the we just patched out the code actually completes the request.  We created a fake `Timeout`.  Nice.

Visually, I imagined a pretty switch statement inside of some `CFNetwork` code that said, _"if I trust this `NSURLSessionAuthChallengeDisposition` then send the request"_.

#### Source
```
#import <Foundation/Foundation.h>

@interface YDURLSessionDel : NSObject <NSURLSessionDelegate>
@end

@implementation YDURLSessionDel
- (void)URLSession:(NSURLSession *)session didReceiveChallenge:(NSURLAuthenticationChallenge *)challenge completionHandler:(void (^)(NSURLSessionAuthChallengeDisposition, NSURLCredential * _Nullable))completionHandler{

    SecTrustRef trust = [[challenge protectionSpace] serverTrust];
    NSLog(@"🍭\tChallenged on: %@", [[challenge protectionSpace] host]);
    NSLog(@"🍭\tCert chain length: %ld", (long)SecTrustGetCertificateCount(trust));

    completionHandler(NSURLSessionAuthChallengeCancelAuthenticationChallenge, NULL);
}
@end

int main(void) {
    @autoreleasepool {

        dispatch_semaphore_t semaphore = dispatch_semaphore_create(0);
        NSURL *url = [NSURL URLWithString:@"https://www.google.com"];
        YDURLSessionDel *del = [[YDURLSessionDel alloc] init];
        NSURLRequest *request = [NSURLRequest requestWithURL:url];

        NSURLSessionConfiguration *config = [NSURLSessionConfiguration defaultSessionConfiguration];
        NSURLSession *session = [NSURLSession sessionWithConfiguration:config delegate:del delegateQueue:nil];
        NSLog(@"🍭 start");
        NSURLSessionDataTask *task = [session dataTaskWithRequest: request
                                                completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
                                    if (!data) {
                                        NSLog(@"🍭 %@", error);
                                    }

                                    if ([response isKindOfClass:[NSHTTPURLResponse class]]) {
                                        NSLog(@"🍭 HTTP Response Code: %ld", (long)[(NSHTTPURLResponse *)response statusCode]);
                                    }
                                    dispatch_semaphore_signal(semaphore);
                            }];
        [task resume];
        dispatch_semaphore_wait(semaphore, DISPATCH_TIME_FOREVER);
        NSLog(@"🍭 finish");

    }
    return 0;
}
```
