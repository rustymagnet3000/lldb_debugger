# 🍪 NSHTTPCookie Thief 🍪
#### Debug App on Simulator without xCode
```
xcrun --sdk iphonesimulator lldb --attach-name tinyDormant --wait-for

(lldb) cont
// Visit page with Cookies

(lldb) process interrupt

(lldb) search WKHTTPCookieStore
<WKHTTPCookieStore: 0x600001f5d300>
```
#### Search with Debugger for Cookie setter
```
(lldb) image lookup -n "+[NSHTTPCookie cookiesWithResponseHeaderFields:forURL:]"
(lldb) image lookup -rn cookiesWithResponseHeaderFields
```
#### Why are no Addresses found?
The addresses are there but they are inside the `WebKit` module.
https://webkit.org/debugging-webkit/

![webkit_processes](/4b_NSHTTPCookie_thief/webkit_overview.png)

#### Switch debugger to WebKit process
```
ps -ax | grep -i WebKit.Networking
 2170 ??         0:00.27 /System/Library/Frameworks/WebKit.framework/XPCServices/com.apple.WebKit.Networking.xpc/com.apple.WebKit.Networking

 (lldb) b +[NSHTTPCookie cookiesWithResponseHeaderFields:forURL:]
 ```
Bingo.  First time!
#### Easier ways to find Cookies
In Safari inspector you can view the Cookies inside a WKWebView Cookie store.  You enable `Developer` mode in Safari and the following setting on your iOS device.

![](/4b_NSHTTPCookie_thief/safari_cookie_inspector.png)

All you need to access this code is:

![settings](/4b_NSHTTPCookie_thief/setting.PNG)
