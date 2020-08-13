# 🍪 NSHTTPCookie Thief 🍪
##### Install, attach and debug iOS app on real device from command line
`ios-deploy -d -W -b <DerivedDatapath to app build>/Debug-iphoneos/tinyDormant.app`

##### Attach to iOS Simulator app from command line
`xcrun --sdk iphonesimulator lldb --attach-name tinyDormant --wait-for`

##### Why are no image lookups, Breakpoints or Traces firing?
```
(lldb) image lookup -n "+[NSHTTPCookie cookiesWithResponseHeaderFields:forURL:]"
(lldb) image lookup -rn cookiesWithResponseHeaderFields

(lldb) b +[NSHTTPCookie cookiesWithResponseHeaderFields:forURL:]

frida-trace -m "*[NSHTTPCookie initWithProperties:]" -p $mypid
```
Read this:
https://webkit.org/debugging-webkit/

Your app process doesn't see the calls to `NSHTTPCookie` as they are being made inside a child process.

![webkit_processes](/4b_NSHTTPCookie_thief/webkit_overview.png)

## Find Cookies
##### Find Cookies in Memory with Frida scrip "observeSomething"
This works on a real device & iOS Simulator.

```
$) ps -ax | grep -i WebKit.Networking
29163 ??         <longPath>/.../com.apple.WebKit.Networking

$) frida --codeshare mrmacete/objc-method-observer -p 29163

[PID::29163]-> %resume                           
[PID::29163]-> observeSomething('*[* cookiesWithResponseHeaderFields:forURL:]');
 ```
 Results:
 ```
+[NSHTTPCookie cookiesWithResponseHeaderFields:forURL:]
 cookiesWithResponseHeaderFields: {
     "Set-Cookie" = "EuConsent=<removed for brevity>; path=/; expires=Sat, 16 Nov 2019 14:51:01 GMT;";
 } (__NSSingleEntryDictionaryI)
 forURL: https://uk.yahoo.com/?p=us&guccounter=1 (NSURL)

 RET: (
     "<NSHTTPCookie
 	version:0
 	name:EuConsent
 	value:<removed for brevity>
 	expiresDate:'2019-11-16 14:51:01 +0000'
 	created:'2019-11-15 14:51:01 +0000'
 	sessionOnly:FALSE
 	domain:yahoo.com
 	partition:none
 	sameSite:none
 	path:/
 	isSecure:FALSE
  path:"/" isSecure:FALSE>"
 )
```


##### Check if WKWebView Cookies are persisted
```
(lldbinit) search WKWebsiteDataStore

<WKWebsiteDataStore: 0x1c8057cd0>

(lldbinit) expression id $wkdatastore = (id)0x1c8057cd0
(lldbinit) po [$wkdatastore description]
<WKWebsiteDataStore: 0x1c8057cd0>

(lldbinit) po [$wkdatastore isPersistent]
0x0000000000000001
```
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
In Safari inspector - with a debuggable iOS app - you can view the Cookies inside a WKWebView Cookie store.  I had to download `Safari Technology Preview` from https://developer.apple.com/safari/download/ to get the `Cookies`, `network` and `Storage` tab.

You enable `Developer` mode in Safari and the following setting on your iOS device.

![](/4b_NSHTTPCookie_thief/safari_cookie_inspector.png)

All you need to access this code is:

![settings](/4b_NSHTTPCookie_thief/setting.PNG)
