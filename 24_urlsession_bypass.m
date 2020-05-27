
(lldb) breakpoint set --selector URLSession:didReceiveChallenge:completionHandler: -s objc_play
Breakpoint 2: where = objc_play`-[YDURLSessionDel URLSession:didReceiveChallenge:completionHandler:] at main.m:7, address = 0x0000000100001620
(lldb) c

///// BREAKPOINT FIRES

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

This crashes, when it tries to call the function later on.
