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

#### TabBar
```
po [[UIWindow keyWindow] rootViewController]
e id $rootvc = (id)0x7fb9ce868200
expression -lobjc -O -- [`$rootvc` _shortMethodDescription]
expression (void)[$rootvc setSelectedIndex:1]
caflush
expression (void)[$rootvc setSelectedIndex:0]
caflush

(lldb) po [$rootvc selectedViewController]
<tinyDormant.YDJediVC: 0x7fb9cd613a80>

(lldb) po [$rootvc viewControllers]
<__NSArrayM 0x600001038810>(
<tinyDormant.YDJediVC: 0x7fb9cd613a80>,
<tinyDormant.YDMandalorianVC: 0x7fb9cd41f1c0>
)
```
#### Part 1 : UITabBarController add a tab
```
(lldb) po [[UIWindow keyWindow] rootViewController]
<UITabBarController: 0x7fdf0f036000>

(lldb) e id $tbc = (id)0x7fdf0f036000

(lldb) po $tbc
<UITabBarController: 0x7fdf0f036000>

(lldb) po [$tbc description]
<UITabBarController: 0x7fdf0f036000>

// METHOD 1
(lldb) e Class $sithVcClass = (Class) objc_getClass("tinyDormant.YDSithVC")
(lldb) e id $sithvc = (id)[$sithVcClass new]
(lldb) po $sithvc
<tinyDormant.YDSithVC: 0x7fb9cd426880>

// METHOD 2
e id $newClass = (id)class_createInstance($sithVcClass, 100);


(lldb) po [$tbc viewControllers]
<__NSArrayM 0x6000029fc930>(
<tinyDormant.YDJediVC: 0x7fdf0ef194e0>,
<tinyDormant.YDMandalorianVC: 0x7fdf0ed23c50>
)

// Create mutable array
(lldb) e NSMutableArray *$listofvcontrollers = (NSMutableArray *)[$tbc viewControllers]

// Add and Delete and View Controller from the array
(lldb) po [$listofvcontrollers addObject:$sithvc]
(lldb) po [$listofvcontrollers removeObjectAtIndex:0]

// Print the array
(lldb) po $listofvcontrollers
<__NSArrayM 0x600001c32580>(
<tinyDormant.YDMandalorianVC: 0x7fa476e15c40>,
<tinyDormant.YDSithVC: 0x7fa476d033d0>
)

(lldb) po [$tbc setViewControllers:$listofvcontrollers]
 nil
```
#### Part 2 : UITabBarController beautify
```
 (lldb) search UITabBar
 <UITabBar: 0x7fa476e16be0; frame = (0 618; 375 49); autoresize = W+TM; gestureRecognizers = <NSArray: 0x60000082b690>; layer = <CALayer: 0x600000678b40>>

 (lldb) e id $tabs = (id)0x7fa476e16be0

 (lldb) po [$tabs items]
 <__NSArrayI 0x600000826580>(
 <UITabBarItem: 0x7fae2f6164c0>,
 <UITabBarItem: 0x7fae2f6195a0>,
 <UITabBarItem: 0x7fae2f502380> selected
 )

 (lldb) e int $sithIndex = [$listofvcontrollers indexOfObject:$sithvc]
 (lldb) po $sithIndex
 2

 (lldb) po [[[$tabs items] objectAtIndex:$sithIndex] setBadgeValue:@"99"];

 (lldb) e UIImage *$sithimage = [UIImage imageNamed:@"approval"];
 (lldb) e [[[$tabs items] objectAtIndex:$sithIndex] setImage:$sithimage]
  nil
 (lldb) caflush
```
#### Part 3 : UITabBarController add tint color
```
(lldb) po [$tabs barTintColor]
 nil
 (lldb) e (void)[$tabs setBarTintColor: [UIColor lightGrayColor]]
0x0000000108ea9e30

(lldb) caflush

(lldb) e (void)[$tabs setBarTintColor: [UIColor greenColor]]
(lldb) caflush
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

(lldb) e (void)[$rootvc pushViewController:$vc animated:YES]
(lldb) caflush
```

**WARNING** - careful with copy and paste of text into lldb. I spent hours trying to work out why one the above commands was not working.

#### References
```
https://www.objc.io/issues/19-debugging/lldb-debugging/
```
