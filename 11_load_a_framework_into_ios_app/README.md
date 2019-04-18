## lldb - code injection - add and start a dynamic framework
Attaching to a process in the Simulator, loading a framework - that was not shipped in an app - and instantiating one of the framework's classes.

Ultimately, I wanted to inject the *hello_framework* and call *secret_objc_method*.
```
#import "hello_from_objc.h"
@implementation hello_from_objc

- (int) secret_objc_method {
    NSLog(@"Ran my ObjC method");
    return 42;
}
@end
```
#### Compile your Swift framework
In this example, I built a framework named *hello_framework*.  This contained both Objective-C and Swift code.

- Compiled for x86/64 only, at this stage.
- Build framework.  You don't need to run it.


#### Run you target app
Make sure xCode is not running.
Open the app you want to inspect, in the Simulator.
#### lldb attach via Terminal
```
// 'sample' is the app name
lldb attach -p `ps x|grep -i -m1 sample|awk '{print $1}'`

// check the path of your app
(lldb) pbundlepath
```
#### Check what is linked
```
(lldb) image list -b
[  0] DELETE_PROV_PROFILE_MACHINE
[  1] dyld
[  2] dyld_sim
[  3] Foundation
[  4] libobjc.A.dylib
[  5] libSystem.dylib
[  6] UIKit
```
Prove that the framework is not there.
```
(lldb) image list -b hello_framework
error: no modules found that match 'hello_framework'
```
#### Load dylib from Mac into device
Now load the process...
```
(lldb) process load /Users/PATH_TO_FRAMEWORK/hello_framework.framework/hello_framework
Loading "/Users/PATH_TO_FRAMEWORK/hello_framework.framework/hello_framework"...ok
Image 0 loaded.
```
Now test it has loaded...
```
(lldb) e id $my_hello = [hello_from_objc new]
(lldb) po $my_hello
<hello_from_objc: 0x600000013a80>
```
#### Closing thought...
The same would level of inspection would also be possible if somebody shipped a framework inside a production iOS app - but had not linked the framework - as the pictures below show.
