# Code Lifting from an iOS app
This article was written to show:
- [x] a framework can be ripped out of an iOS app
- [x] you can invoke Objective-C code without even importing the Modules

#### Find the target app
I found an app that was using a phone number validator.  This was publicly available from:
https://github.com/iziz/libPhoneNumber-iOS

#### Extract the App
I downloaded the app via the AppStore and then extracted it from a jailbroken device.

#### Extract the Framwork
Inside the app bundle, copy the entire `libPhoneNumber-iOS` framework.  Ignore the fact the Framwork is codesigned.  xCode will resign the Framework later, when you create a fresh app.
#### Xcode
Create a new hello world project and drag in your lifted Framework.

The "lifted" code inside an iOS app was thinned.  Don't try and run this on a simulator.  Run the app in debug mode and connect `lldb`.

#### Dump the classes
```
[+] script to dump classes from: https://github.com/DerekSelander/LLDB

dclass -m libPhoneNumber_iOS

Dumping classes
************************************************************
NBPhoneNumberUtil
NBPhoneNumberDesc

```
#### attach lldb
```
(lldb) exp id $a = [NBPhoneNumberUtil new]
(lldb) po $a
<NBPhoneNumberUtil: 0x1c1c6b580>

(lldb) expression -lobjc -O -- [$a _shortMethodDescription]
// dumps all available Class, Properties and Instance Methods

(lldb) exp NSString *$b = @"497666777000"
(lldb) exp NSString *$nn = nil
(lldb) exp NSNumber *$cc = (NSNumber *)[$a extractCountryCode:$b nationalNumber:&$nn]
// using the github page, find how to invoke a method via Objective C, then apply it via lldb

(lldb) p $cc
(__NSCFNumber *) $cc = 0xb0000000000002c3 (long)49
(lldb) p $nn
(__NSCFString *) $nn = 0x00000001c4227be0 @"7666777000"
```
