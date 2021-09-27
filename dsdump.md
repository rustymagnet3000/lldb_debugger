# dsdump

[Source](https://derekselander.github.io/dsdump/#apples_mach-o_file_format)
```bash
➜dsdump
Version: Beta 6 Built: (22:00:50, Dec  8 2019) dsdump [option..] <mach-o-file>
```

```swift
import UIKit
class ViewController : UIViewController {
  var meh: Int = 4
  override func viewDidLoad() {
    super.viewDidLoad()
    print("yayyyyy")
  }
  func swiftFunc() { }
}
```

swiftc weird.swift -sdk `xcrun --show-sdk-path  -sdk iphoneos` -target arm64-apple-ios99.99.99.9

```bash
jtool -l weird
LC 08: LC_LOAD_DYLINKER      	/usr/lib/dyld
LC 09: LC_UUID               	UUID: 66282AD3-03D8-336E-A5C9-48305CA88CED
LC 10: LC_BUILD_VERSION      	Build Version:           Platform: iOS 99.99.99
```

```bash
➜dsdump  --swift weird --verbose=4 --defined --color
 class weird.ViewController : UIViewController /System/Library/Frameworks/UIKit.framework/UIKit {

	// Properties
	var meh : Int

	// ObjC -> Swift bridged methods
	0x10000755c  @objc ViewController.viewDidLoad()
	0x100007914  @objc ViewController.init(nibName:bundle:)
	0x100007bb0  @objc ViewController.init(coder:)

	// Swift methods
	0x100007188  func ViewController.meh.getter // getter 
	0x10000721c  func ViewController.meh.setter // setter 
	0x1000072dc  func ViewController.meh.modify // modifyCoroutine 
	0x1000075a4  func ViewController.swiftFunc() // method 

➜strip weird
➜dsdump  --swift weird --verbose=4 --defined --color
 class weird.ViewController : UIViewController /System/Library/Frameworks/UIKit.framework/UIKit {

	// Properties
	var meh : Int

	// ObjC -> Swift bridged methods
	0x10000755c  @objc ViewController.viewDidLoad <stripped>
	0x100007914  @objc ViewController.initWithNibName:bundle: <stripped>
	0x100007bb0  @objc ViewController.initWithCoder: <stripped>

	// Swift methods
	0x100007188  func <stripped> // getter 
	0x10000721c  func <stripped> // setter 
	0x1000072dc  func <stripped> // modifyCoroutine 
	0x1000075a4  func <stripped> // method 
 }

  }
```