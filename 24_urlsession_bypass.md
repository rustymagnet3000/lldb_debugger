# Using LLDB to bypass Certificate Pinning with URLSession
#### Bypass overview
_"Do I trust the server,  before sending data?"_.  You will often find that question in iOS and Android app code.  It refers to `certificate pinning`.

The below script overwrites the answer to that question.  The bypass requires a debugger (`lldb`) a scripting language (`python`) and writing values in memory (`registers`).

#### Result
```
(lldb) br s -a 0x1000013ae -N fooName
Breakpoint 2: where = objc_play`-[YDURLSessionDel URLSession:didReceiveChallenge:completionHandler:] + 334 at main.m:19:5, address = 0x00000001000013ae

(lldb) c
Process 48838 resuming
🍭Start
🍭Challenged on: www.google.com
🍭Cert chain length: 3

(lldb) yd_bypass_urlsession       // run custom Python LLDB script

[*]URLSession trust bypass started
[*]Original of NSURLSessionAuthChallengeDisposition: (unsigned long) rsi = 0x0000000000000002
[!]NSURLSessionAuthChallengeDisposition set to Cancel.
[*]PATCHING result: pass
🍭 HTTP Response Code: 200
🍭 finish
```
#### Background
App's often used a `completionHandler` with Apple's `NSURLSession` on iOS and macOS when deciding whether to start a `network request`.  

> completionHandler(NSURLSessionAuthChallengeCancelAuthenticationChallenge, NULL);

The above line of code is typical of an app that has implemented `Certificate Pinning` and has decided to stop the network request from being sent.  

#### Find the Needle in the Haystack
If you ingested the executable file into a disassembler like **Hopper**, you could find the `assembly instruction` to patch out the answer.  

Hopper had a really nice pseudo code flow of: `URLSession:didReceiveChallenge:completionHandler:`:
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
Sure enough, if you set a `breakpoint` on this `instruction`:
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

What is the `2` value in the second register (`arg2`)?  If a server and connection was trusted or not, the result was often this value:
 ```
typedef NS_ENUM(NSInteger, NSURLSessionAuthChallengeDisposition) {
   NSURLSessionAuthChallengeUseCredential = 0,                                       /* Use the specified credential, which may be nil */
   NSURLSessionAuthChallengePerformDefaultHandling = 1,                              /* Default handling for the challenge - as if this delegate were not implemented; the credential parameter is ignored. */
   NSURLSessionAuthChallengeCancelAuthenticationChallenge = 2,                       /* The entire request will be canceled; the credential parameter is ignored. */
   NSURLSessionAuthChallengeRejectProtectionSpace = 3,                               /* This challenge is rejected and the next authentication protection space should be tried; the credential parameter is ignored. */
}
```

#### Breakpoint and script
Most of the effort and skill was placing a breakpoint.
```
(lldb) br s -a 0x1000013ae -N fooName
```
You could then - now you have named the breakpoint - add instructions to the breakpoint OR you could invoke a Python script from the command line.

I choose to invoke my own Python script so it was simple to re-use this code on other apps. The main lines of the script were:
```
frame = exe_ctx.frame
disposition = frame.FindRegister("rsi")
if disposition.unsigned == 2:
     print "[!]NSURLSessionAuthChallengeDisposition set to Cancel."
     result = frame.registers[0].GetChildMemberWithName('rsi').SetValueFromCString("0x1", error)
     messages = {None: 'error', True: 'pass', False: 'fail'}
     print ("[*]PATCHING result: " + messages[result])
```
The trick was `frame = exe_ctx.frame`.  If you didn't have this context - from https://lldb.llvm.org/use/python-reference.html - you would get stuck for hours / days.

The full bypass code: https://github.com/rustymagnet3000/reverse_engineer_ios_with_debugger/blob/master/15_python_lldb_scripts/yd_pythonlldb_scripts.py

#### Try, try and try again
Like most bypass code, I tried multiple ideas.  I removed the details of failed ones for brevity.  If you care, essentially they were:

 - Set `completionHandler` to NULL
 - Overwrite the instruction with no operation ( a `NOP instruction` )
 - Passing a `NULL Objective-C block`
 - Passing a fake `Objective-C block`
 - Drop the `(NSURLAuthenticationChallenge *)challenge` ( failed as a lot of code depends on this challenge)

#### Source
```
@interface YDURLSessionDel : NSObject <NSURLSessionDelegate>
@end

@implementation YDURLSessionDel
- (void)URLSession:(NSURLSession *)session didReceiveChallenge:(NSURLAuthenticationChallenge *)challenge completionHandler:(void (^)(NSURLSessionAuthChallengeDisposition, NSURLCredential * _Nullable))completionHandler{

    SecTrustRef trust = [[challenge protectionSpace] serverTrust];
    NSLog(@"🍭Challenged on: %@", [[challenge protectionSpace] host]);
    NSLog(@"🍭Cert chain length: %ld", (long)SecTrustGetCertificateCount(trust));

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
        NSLog(@"🍭 @property waitsForConnectivity default: %hhd", config.waitsForConnectivity);
        config.waitsForConnectivity = YES;

        NSURLSession *session = [NSURLSession sessionWithConfiguration:config delegate:del delegateQueue:nil];
        NSLog(@"🍭 start");
        NSURLSessionDataTask *task = [session dataTaskWithRequest: request
                                                completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {

                                    if (error) {
                                        if(error.code == -999)
                                            NSLog(@"🍭 Bypass failed. Connection: %@ ( %ld)", [error localizedDescription], (long)error.code);
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
