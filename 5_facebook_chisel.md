# Facebook's Chisel and beyond
##### Read all Objects on a screen
```
(lldb) pviews
```
##### Change a Swift View border
```
(lldb) pvc
<UINavigationController 0x7fa47905fa00>, state: appeared, view: <UILayoutContainerView 0x7fa47862e9c0>
   | <DELETE_PROV_PROFILE_MACHINE.ydHomeVC 0x7fa47861dcc0>, state: appeared, view: <UIView 0x7fa4786327a0>
(lldb) expr -l objc -- @import UIKit
(lldb) border -c red -w 1.0 0x7fa4786327a0
(lldb) border -c red -w 5.0 0x7fa4786327a0
```
##### Find View Controller (fvc)
```
(lldb) fvc --view=0x7fc2c4410970
Found the owning view controller.
<MYAPP.ydHomeVC: 0x7fc2c443d850>
```
##### hide a View
```
(lldb) pvc
The current UIViewController that you want to hide…
<UIViewController 0x1067116e0>, state: appearing, view: <UIView 0x10b707740>

lldb) hide 0x10b707740
```
##### Show a hidden ViewControlller
```
var $window: UIWindow?
$window = UIWindow(frame: UIScreen.main.bounds)
let $mainViewController = ydHiddenVC()
window?.rootViewController = $mainViewController
$window?.makeKeyAndVisible()

https://medium.com/@Dougly/a-uiviewcontroller-and-uiviews-without-storyboard-swift-3-543096e78f2
```
##### UILabel fun
```
<UIButtonLabel: 0x7f826bd2b090; frame = (0 3; 56 20.5); text = 'Submit'; opaque = NO; userInteractionEnabled = NO; layer = <_UILabelLayer: 0x600003dc3ed0>>
   |    |    |    |    | <UILabel: 0x7f826be15710; frame = (148.5 12; 78.5 20.5); text = 'Feedback';

(lldb) mask 0x7f826bd2b090
(lldb) unmask 0x7f826bd2b090
(lldb) border -c yellow -w 2.0 0x7f826be15710
(lldb) border 0x7f826be15710
```
##### Cast from Swift to Objective-C object
```
<UILabel: 0x7f826bd2e8c0; frame = (33 10.5; 302 20); text = 'General feedback'; userInteractionEnabled = NO; layer = <_UILabelLayer: 0x600003db0e10>>
(lldb) expression id $alien = (id)0x7f826bd2e8c0  // UILabel Object was created in Swift but you need access in Objective-C
(lldb) po $alien
<UILabel: 0x7f826bd2e8c0; frame = (33 10.5; 302 20); text = 'General feedback'; userInteractionEnabled = NO; layer = <_UILabelLayer: 0x600003db0e10>>
(lldb) exp (void*)[$alien setText:@"odd"]
(void *) $11 = 0x0000000107116010
You won’t see anything until you..

(lldb) caflush

(lldb) po $alien
<UILabel: 0x7fd0b36444a0; frame = (172 12; 31 20.5); text = 'odd'; userInteractionEnabled = NO; layer = <_UILabelLayer: 0x6000031c8820>>
```

##### Demangle Swift ViewController Names
```
(lldb) search UIView -m myFramework      // observe the de-mangled Swift name
<myFramework.PageViewController: 0x7f826bf0c980>

(lldb) search UIViewController -m myFramework    // Great for Swift
_TtC8myFramework18PageViewController * [0x00007f826bf0c980]

(lldb) search -r 0x7f826bf0c980       // Now get all references to ViewController
```

