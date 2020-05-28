# Using LLDB to bypass URLSession
#### Bypass overview
The goal of this bypass was to set a breakpoint at the start of `URLSession:didReceiveChallenge:completionHandler:` and override the `completionHandler`. Why?  This handler decided what to do with a `network request`.  

> completionHandler(NSURLSessionAuthChallengeCancelAuthenticationChallenge, NULL);

The above line of code is typically when an app has implemented `Certificate Pinning` and wanted to stop, after deciding it didn't trust the server.

#### The Needle
App's often used a `completionHandler` with Apple's `NSURLSession` on iOS and macOS.  The code would set an `enum` based on whether it trusted the server and connection:
```
typedef enum NSURLSessionAuthChallengeDisposition : NSInteger {
    ...
} NSURLSessionAuthChallengeDisposition;
```
Going for the jugulur would be finding this value and changing it, as below:

From: `NSURLSessionAuthChallengeCancelAuthenticationChallenge = 2 `

To: `NSURLSessionAuthChallengePerformDefaultHandling = 1`

I chose not to do this.  It was slow and error prone to find an integer value in `assembly code`. Especially when there was no obvious `Symbol` or `instruction` to leverage [ as we are assuming a stripped, release app ].

#### Tip
You could also drop the `(NSURLAuthenticationChallenge *)challenge` parameter.  However, a lot of code is likely to use that `challenge`.  Better to `substitute` the challenge with a host that is valid and not likely to trigger a `NSURLSessionAuthChallengeCancelAuthenticationChallenge`.

#### Bypass fail - NULL Stack Block
This bypass dropped the `Stack Block` with a NULL value.  

```
(lldb) breakpoint set --selector URLSession:didReceiveChallenge:completionHandler: -s objc_play
Breakpoint 2: where = objc_play`-[YDURLSessionDel URLSession:didReceiveChallenge:completionHandler:] at main.m:7, address = 0x0000000100001620
(lldb) c
```
At this point the Breakpoint fires.

You can then inspect every argument passed into the `Selector` (`URLSession:didReceiveChallenge:completionHandler:`).
```
(lldb) po $arg1
<YDURLSessionDel: 0x1005436c0>

(lldb) po $arg2
140735179686727

(lldb) po (char *)$arg2
"URLSession:didReceiveChallenge:completionHandler:"

(lldb) po (char *)$arg3
<__NSURLSessionLocal: 0x10325c480>

(lldb) po (char *)$arg4
<NSURLAuthenticationChallenge: 0x103270de0>

(lldb) po (char *)$arg5
<__NSStackBlock__: 0x700000776ba8>
 signature: "v24@?0q8@"NSURLCredential"16"
 invoke   : 0x7fff30e47a04 (/System/Library/Frameworks/CFNetwork.framework/Versions/A/CFNetwork`CFHTTPCookieStorageUnscheduleFromRunLoop)
 copy     : 0x7fff30d3b7ed (/System/Library/Frameworks/CFNetwork.framework/Versions/A/CFNetwork`CFURLCredentialStorageCopyAllCredentials)
 dispose  : 0x7fff30d3b825 (/System/Library/Frameworks/CFNetwork.framework/Versions/A/CFNetwork`CFURLCredentialStorageCopyAllCredentials)


(lldb) po $arg5 = NULL
<nil>
```
It crashed.  Why?  There was a `assembly` instruction to call a `Function Pointer` plus a certain amount of bytes.  This returned a bad instruction.
```
Thread 2: EXC_BAD_ACCESS (code=1, address=0x10)
```
Quite fun to see the instruction that caused the crash was `call   qword ptr [rcx + 0x10]`.  So `nulling $arg5` caused `rcx` to be `0`.


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
