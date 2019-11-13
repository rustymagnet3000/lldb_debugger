# 🍪 WKWebView Cookie Thief 🍪
Once I opened a WKWebView rendered page inside an iOS app, I wanted to use lldb to print all cookies inside the WKWebView cookie store. But once you scratch the surface, you found a lot of data structures underneath the following simple code:
```
webView.configuration.websiteDataStore.httpCookieStore.getAllCookies { cookies in
            for cookie in cookies {
                print("\(cookie.name) is set to \(cookie.value)")
            }
        }
```
To mimic this code inside lldb you could find every single variable in that `closure` call _webview_, _configuration_, etc or you could look search for the _WKWebsiteDataStore_ on the `heap` and then grab the associated _WKHTTPCookieStore_.
#### A Swift Cookie Thief
But a quicker way is to find the `WKHTTPCookieStore` object on the `Heap`.
```
(lldb) settings set target.language swift
(lldb) exp import WebKit
(lldb) search WKHTTPCookieStore
<WKHTTPCookieStore: 0x2803db2c0>

(lldb) expr let $a = unsafeBitCast(0x2803db2c0, to: WKHTTPCookieStore.self)

(lldb) exp $a.getAllCookies{cookies in NSLog("🍪🍪 Cookie Thief 🍪🍪"); for cookie in cookies { NSLog("🍪 %@", cookie) }}
```
#### The results
```
[<NSHTTPCookie
	version:1
	name:s_fid
	value:0B1EE86304D66ECC-1F86181ADC4A3A3B
	expiresDate:'2023-11-21 10:26:50 +0000'
	created:'2018-11-21 10:26:50 +0000'
	sessionOnly:FALSE
	domain:.apple.com
	partition:none
	sameSite:none
	path:/
	isSecure:FALSE
 path:"/" isSecure:FALSE>, <NSHTTPCookie
	version:1
	name:s_vi
	value:[CS]v1|2DFA9449052E39D6-60002D4B40001F9C[CE]
	expiresDate:'2020-11-20 10:26:50 +0000'
	created:'2018-11-21 10:26:50 +0000'
	sessionOnly:FALSE
	domain:.apple.com
	partition:none
	sameSite:none
	path:/
	isSecure:FALSE
 path:"/" isSecure:FALSE>, <NSHTTPCookie
	version:1
```
#### Warning
This works on a physical iOS device.  But you don't see anything?  

- [x] Odd behaviour with simulators.
- [x] A release app sends STDOUT to syslogs (open `Console.app`)
- [x] `NSlog` and `printf` only print to lldb output when you are connected in a debug build.
- [x] I had to type `(lldb) continue` before the logs were sent.

#### Practice with Expression
```
(lldb) expr let $a = unsafeBitCast(0x2803db2c0, to: WKHTTPCookieStore.self)

(lldb) expression
Enter expressions, then terminate with an empty line to evaluate:
1 func $printSomething(a: WKHTTPCookieStore) {
2 print(a)
3 }
4
(lldb) exp $printSomething(a: $p)
<WKHTTPCookieStore: 0x2803db2c0>
```
#### An Objective-C Cookie Thief
Using an Objective-C `Block` was even nicer.
```
search WKHTTPCookieStore
expression id $alien = (id)0x283e9b020

(lldb) po [$alien description]
<WKHTTPCookieStore: 0x1d40db4a0>

(lldb) po [$alien debugDescription]
<WKHTTPCookieStore: 0x1d40db4a0>
```
##### Create the Block
```
(lldb) expression
Enter expressions, then terminate with an empty line to evaluate:
  1: void(^$cookieThief)(NSArray<NSHTTPCookie *> * _Nonnull) = ^(NSArray<NSHTTPCookie *> * _Nonnull cookies){
  2: NSLog(@"🍪🍪 Cookie Thief 🍪🍪");
  3: for(int i = 0; i < cookies.count; i++)
  4: NSLog(@"🍪 %@",cookies[i]);
  5: };
```
##### Invoke the Block
```
exp (void)[$alien getAllCookies:$cookieThief]
continue  // to watch the output in Console.app
```
##### Condensed expression
```
(lldb) exp (void)[$alien getAllCookies:^(NSArray<NSHTTPCookie *> * _Nonnull cookies) {NSLog(@"All cookies %@",cookies);}];
```
##### References
https://www.codeproject.com/Articles/1181358/Debugging-with-Xcode

https://www.mikeash.com/pyblog/friday-qa-2014-08-29-swift-memory-dumping.html

https://stackoverflow.com/questions/29441418/lldb-swift-casting-raw-address-into-usable-type

https://github.com/chenyongMAC/learn-infos/blob/56490a7951f2b82a665716abcae30a92fcab656c/hybrid/WKWebView-iOS11.md
