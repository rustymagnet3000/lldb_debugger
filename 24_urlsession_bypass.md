# Using LLDB to bypass URLSession
#### Bypass overview
The goal of this bypass was to set a breakpoint and override the `completionHandler` that decided what to do with a `network request`.  This `completionHandler` was widely used with Apple's `NSURLSession` on iOS and macOS.

> completionHandler(NSURLSessionAuthChallengeCancelAuthenticationChallenge, NULL);

An alternative bypass would be to stop on this `Enum` from Apple:
```
typedef enum NSURLSessionAuthChallengeDisposition : NSInteger {
    ...
} NSURLSessionAuthChallengeDisposition;
```
The value is passed into a `Stack Block`.  It is slow to find an integer value in `assembly code` when you don't have an obvious Symbol or instruction to use.

If you follow this bypass, you change a value from `NSURLSessionAuthChallengeCancelAuthenticationChallenge = 2 ` to `NSURLSessionAuthChallengePerformDefaultHandling = 1`.

#### Tip
You could also drop the `(NSURLAuthenticationChallenge *)challenge` parameter.  However, a lot of code is likely to use that `challenge`.  better to `substitute` a challenge that will be valid instead of dropping the original `challenge`.

#### Bypass fail
This bypass replace a `Function Pointer` with a NULL value.  

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
