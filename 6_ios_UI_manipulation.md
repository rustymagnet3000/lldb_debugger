## lldb - playing with screens
#### lldb - print all View Controllers connected to current hierarchy
`(lldb) po [[[UIWindow keyWindow] rootViewController] _printHierarchy]`

#### lldb - Recursive description of current view
`po [[[UIApplication sharedApplication] keyWindow] recursiveDescription]`

#### UILabel change text
Find the ID of the UIlabel after running the `recursiveDescription` command above.
```
(lldb) e id $myLabel = (id)0x104ec9370

(lldb) po $myLabel
<MyApp.CustomUILabel: 0x104ec9370; baseClass = UILabel; frame = (0 0; 287 21); text = 'Boring default text...'; opaque = NO; autoresize = RM+BM; userInteractionEnabled = NO; layer = <_UILabelLayer: 0x1d4291b70>>

(lldb) po [$myLabel superview]
<UIStackView: 0x104ec8f70; frame = (56 0; 287 88); opaque = NO; autoresize = RM+BM; layer = <CATransformLayer: 0x1d443a620>>

(lldb) p (int)[$myLabel setText:@"Bye World"]
Nothing will happen.  You need to refresh the screen or continue the app.

(lldb) e (void)[CATransaction flush]
```
#### Change background Color
```
(lldb) e id $myView2 = (id)0x104f474e0
(lldb)  v
<UIView: 0x104f474e0; frame = (0 0; 375 603); autoresize = RM+BM; layer = <CALayer: 0x1d0239c20>>
(lldb) e (void)[$myView2 setBackgroundColor:[UIColor blueColor]]

(lldb) caflush
// this is the Chisel alias for e (void)[CATransaction flush]
```

#### Push a new ViewController
```
(lldb) po [[UIWindow keyWindow] rootViewController]
<UINavigationController: 0x105074a00>

(lldb) e id $rootvc = (id)0x105074a00
(lldb) po $rootvc
<UINavigationController: 0x105074a00>

(lldb) e id $vc = [UIViewController new]
(lldb) po $vc
<UIViewController: 0x1067116e0>

(lldb) expression (void)[$rootvc pushViewController:$vc animated:YES]
(lldb) caflush
```

**WARNING** - careful with copy and paste of text into lldb. I spent hours trying to work out why one the above commands was not working.

#### References
```
https://www.objc.io/issues/19-debugging/lldb-debugging/
```
