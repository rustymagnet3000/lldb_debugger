# 🍪 NSHTTPCookie Thief 🍪
##### Install, attach and debug iOS app on real device from command line
`ios-deploy -d -W -b <DerivedDatapath to app build>/Debug-iphoneos/tinyDormant.app`

##### Attach to iOS Simulator app from command line
`xcrun --sdk iphonesimulator lldb --attach-name tinyDormant --wait-for`

##### Why are no image lookups, Breakpoints or Traces firing, with WKWebView?
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
##### Find Cookies in Memory with Frida script "observeSomething" and WKWebView
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
After WKWebView object has instantiated, `Child` webkit processes spawn:
```
 1820  0:00.28 /var/containers/Bundle/Application/<app id>/tinyDormant.app/tinyDormant
 1822  0:00.52 /System/Library/Frameworks/WebKit.framework/XPCServices/com.apple.WebKit.Networking.xpc/com.apple.W
 1823  0:01.27 /System/Library/Frameworks/WebKit.framework/XPCServices/com.apple.WebKit.WebContent.xpc/com.apple.W
 1824  0:00.03 /System/Library/Frameworks/WebKit.framework/XPCServices/com.apple.WebKit.Databases.xpc/com.apple.We
```

##### WebKit.Networking
This process updates the web pages and persists them on the device inside the app's sandbox.

`frida -l access.js -U -p 1822`

You can see the cached web pages here:
`/var/mobile/Containers/Data/Application/<GUID>/Library/Caches/WebKit/NetworkCache/Version 11/Blobs`

Alternatively get the cookies from this child process:
```
frida-trace -m "*[NSHTTPCookie initWithProperties:]" -p 1822
```
##### WebKit.Databases
`frida -l access.js -U -p 1824`

```
[iPhone::PID::1824]-> exit[SNPS] They are searching for: /var/mobile/Containers/Data/Application/4A42C020-6684-4727-9E14-D5CD4C37A7FA/Library/WebKit/WebsiteData/IndexedDB/https_uk.news.yahoo.com_0/article-server

Process is checking: /var/mobile/Containers/Data/Application/4A42C020-6684-4727-9E14-D5CD4C37A7FA/Library/WebKit/WebsiteData
Process is checking: /var/mobile/Containers/Data/Application/4A42C020-6684-4727-9E14-D5CD4C37A7FA/Library/WebKit/WebsiteData/IndexedDB
Process is checking: /var/mobile/Containers/Data/Application/4A42C020-6684-4727-9E14-D5CD4C37A7FA/Library/WebKit/WebsiteData/IndexedDB/https_uk.news.yahoo.com_0
Process is checking: /var/mobile/Containers/Data/Application/4A42C020-6684-4727-9E14-D5CD4C37A7FA/Library/WebKit/WebsiteData/IndexedDB/https_uk.news.yahoo.com_0/article-server
Process is checking: /var/mobile/Containers/Data/Application/4A42C020-6684-4727-9E14-D5CD4C37A7FA/Library/WebKit/WebsiteData/IndexedDB/https_uk.news.yahoo.com_0/article-server/IndexedDB.sqlite3-shm
```


### Easier ways to find Cookies
In Safari inspector - with a debuggable iOS app - you can view the Cookies inside a WKWebView Cookie store.  I had to download `Safari Technology Preview` from https://developer.apple.com/safari/download/ to get the `Cookies`, `network` and `Storage` tab.

You enable `Developer` mode in Safari and the following setting on your iOS device.

![](/4b_NSHTTPCookie_thief/safari_cookie_inspector.png)

All you need to access this code is:

![settings](/4b_NSHTTPCookie_thief/setting.PNG)
