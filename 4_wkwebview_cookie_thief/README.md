# 🍪 WKWebView Cookie Thief 🍪
I wanted to use lldb to print all cookies inside a WKWebView cookie store. I wanted my debugger to mimic the following code:
```
webView.configuration.websiteDataStore.httpCookieStore.getAllCookies { cookies in
            for cookie in cookies {
                print("\(cookie.name) is set to \(cookie.value)")
            }
        }
```
#### A Swift Cookie Thief
Find the `WKHTTPCookieStore` object on the `Heap`.
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
- [x] If you are using a Release / App Store app, `Get-TaskAllow=false` will stop lldb.
- [x] `NSlog` and `printf` only appear to print to lldb output when you are connected in a debug build.
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
expression id $a = (id)0x283e9b020

(lldb) po [$a description]
<WKHTTPCookieStore: 0x1d40db4a0>
```
##### Create the Block
```
(lldb) expression
Enter expressions, then terminate with an empty line to evaluate:
  1: void(^$cookieThief)(NSArray<NSHTTPCookie *> * _Nonnull) = ^(NSArray<NSHTTPCookie *> * _Nonnull cookies){
  2: NSLog(@"[*] Cookie Thief ");
  3: for(int i = 0; i < cookies.count; i++)
  4: NSLog(@"\t%@",cookies[i]);
  5: };
```
##### Invoke the Block
```
exp (void)[$a getAllCookies:$cookieThief]
cont              // to watch the output in Console.app
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
