# 🍪 NSHTTPCookie Thief 🍪
##### Debug App on Simulator without xCode
```
xcrun --sdk iphonesimulator lldb --attach-name tinyDormant --wait-for

(lldb) cont
// Visit page with Cookies

(lldb) process interrupt

(lldb) search WKHTTPCookieStore
<WKHTTPCookieStore: 0x600001f5d300>
```
##### Search with Debugger for Cookie setter
```
(lldb) image lookup -n "+[NSHTTPCookie cookiesWithResponseHeaderFields:forURL:]"
(lldb) image lookup -rn cookiesWithResponseHeaderFields
```
##### Why are no Breakpoints or Traces firing?
```
(lldb) b +[NSHTTPCookie cookiesWithResponseHeaderFields:forURL:]

frida-trace -m "*[NSHTTPCookie initWithProperties:]" -p $mypid
```
Read this:
https://webkit.org/debugging-webkit/

Your app process doesn't see the calls to `NSHTTPCookie` as they are being made inside a child process.

![webkit_processes](/4b_NSHTTPCookie_thief/webkit_overview.png)

### Find the Cookies
##### Stop WKWebView loading
Breakpoint after WKWebView instantiated or before:
```
self.webView.load(myRequest)
```
##### Get the correct Child Process ID
After WKWebView has instantiated the `Child` webkit processes have spawned.

```
mypid=$(ps -ax | grep -i WebKit.WebContent | grep -i Xcode | awk '{print $1}')

echo $mypid
1761

```
##### Set the Trace
```
frida-trace -m "*[NSHTTPCookie initWithProperties:]" -p 229
```
##### Continue Debugger
Now `continue` the main app process.

Bingo.  First time!

### Easier ways to find Cookies
In Safari inspector - with a debuggable iOS app - you can view the Cookies inside a WKWebView Cookie store.  You enable `Developer` mode in Safari and the following setting on your iOS device.

![](/4b_NSHTTPCookie_thief/safari_cookie_inspector.png)

All you need to access this code is:

![settings](/4b_NSHTTPCookie_thief/setting.PNG)
