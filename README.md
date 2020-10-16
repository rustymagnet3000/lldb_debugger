# The LLDB Debugger
<!-- TOC depthFrom:3 depthTo:3 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Getting started](#getting-started)
- [Disassemble](#disassemble)
- [Registers](#registers)
- [Print](#print)
- [Breakpoints](#breakpoints)
- [Memory](#memory)
- [Scripting](#scripting)
- [Watchpoint](#watchpoint)
- [Settings](#settings)
- [Scripts](#scripts)
- [Aliases](#aliases)
- [Objective C](#objective-c)
- [lldb and Objective-C Blocks](#lldb-and-objective-c-blocks)
- [lldb with C code](#lldb-with-c-code)
- [Advanced](#advanced)
- [stdout](#stdout)
- [lldb - playing with screens](#lldb-playing-with-screens)
- [Facebook's Chisel](#facebooks-chisel)
- [Thread Pause / Thread Exit](#thread-pause-thread-exit)
- [Output](#output)
- [help lldb by setting the language](#help-lldb-by-setting-the-language)
- [lldb & rootless](#lldb-rootless)

<!-- /TOC -->

### Getting started
##### Frame
`frame info`
##### Thread
`thread list`
##### Brief list of attached Libraries
`image list -b`
##### Sections of all loaded code
`image dump sections`
##### Sections of a Module
`image dump sections myApp`
##### Symbols of a Module
`image dump symtab myApp`
##### Symbols of all loaded code (BAD IDEA)
`image dump symtab`
##### Lookup options:
`help image lookup`
##### Lookup a Debug Symbol
`image lookup -r -n YDClass`
##### Lookup non-debug symbols:
`image lookup -r -s YDClass`
##### Lookup Address:
`image lookup -a 0x1000016a0`
##### Search for Object on Heap:
`search -r 0x0000000100610570`


### Disassemble
##### By address
`disas -s 0x00001620`
##### By function name
`disas -n Foo.Bar`
##### By ObjC method
`disas -n "+[YDFileChecker asmSyscallFunction:]"`

### Registers
Argument  | Register | x86_64  | arm64
--|---|--|--
Return  | -  | RAX | -
First  | arg1 | RDI | x0
Second  | arg2 | c | x1
Third  |  arg3| RDX |  x2
Fourth  | arg4 | RCX  | x3
Fifth  | arg5 | R8  | x4
Sixth  | arg6 |  R9 | x5
Syscalls  | - | syscall  | x16

### Print
##### Register
`po $arg2`
##### Hex to Decimal
`p/d 0x1a        // (int) $2 = 26`
##### Create char *
`po char *$new`
##### Check for substring in a register
`po $new = (char *) strnstr((char *)$rsi, "Info.plist", (int)strlen((char *) $rsi))`
##### Create NSString
`exp NSString *$myMethod = NSStringFromSelector(_cmd)`
##### Get Selector
`po NSSelectorFromString($meth)`

### Breakpoints
##### Getting the options
`help breakpoint set`
#####  Options to add script to Breakpoint
`help break command add`
##### Delete all breakpoints
`b delete`
##### List
`b list`
##### Breakpoint on symbol name
`b syscall`
##### Breakpoint on fullname
`breakpoint set -F access`
##### Breakpoint on fullname in a single Module
`breakpoint set -F access -s libsystem_kernel.dylib`
##### Breakpoint on Name and give the breakpoint a name
`b -n task_get_exception_ports -N fooName --auto-continue true`
##### Breakpoint on Address ( gdb syntax )
`b *0x1000016ce`
##### Breakpoint on ObjC Class Method
`b "+[YDFileChecker foobar:]"`
##### Breakpoint on Function, name the breakpoint and set condition
`br set -b "+[YDFileChecker foobar:]" -N fooName  -c "$arg1 == 0x33"`
##### Breakpoint on Address with name (lldb syntax )
`br s -a 0x1000016ce -N fooName`
##### Break on Register value ( SVC calls )
`b set -N fooName --auto-continue true -c $x16==26`
##### Break on Register holding Info.plist substring
`br s -n syscall -c '(char *) strnstr((char *)$rsi, "Info.plist", (int)strlen((char *) $rsi)) != NULL'`
##### Breakpoint on Selector
`breakpoint set --selector URLSession:didReceiveChallenge:completionHandler:`
##### Breakpoint on Selector in Module
`breakpoint set --selector blah:blah: -s playModule`
##### Regex Breakpoint on Selector ( good for Swift )
`rb Foo.handleBarChallenge -s playModule -N fooName`
##### Breakpoint naming
`breakpoint set --selector blah:blah: -s objc_play -N fooName`
##### Breakpoint condition
`br mod -c $arg2 == "URLSession:didReceiveChallenge:completionHandler:" fooName`
##### Break on exact ObjC Method
`b "-[MyUser name:]"`
##### Breakpoint on completionHandler
`b -[YDURLSessionDel URLSession:didReceiveChallenge:completionHandler:]`
#####  Regex Breakpoint
`rb '\-\[UIViewController\ '`
`rb '\-\[YDUser(\(\w+\))?\ '`
`breakpoint set --func-regex=. --shlib=objc_play`

#####  Python script when Breakpoint fires
```
(lldb) breakpoint command add -s python fooName
Enter your Python command(s). Type 'DONE' to end.
    print("[!]found it")
    DONE
```
##### Callback to Python function when Breakpoint hits
```
(lldb) breakpoint command add -F ydscripts.YDHelloWorld fooName
```
#####  Add & continue Python script when Breakpoint fires
```
(lldb) breakpoint command add -s python fooName
    print lldb.frame.register["rsi"].value
    lldb.frame.register["rsi"].value = "1"
    print("[*]new value set.")
    thread = frame.GetThread()
    process = thread.GetProcess()
    process.Continue()
    DONE
```
#####  Breakpoint all code inside a function
```
(lldb) script
>>> for a in range(0x1000016bc, 0x1000016d1):
... 	lldb.target.BreakpointCreateByAddress(a)
```

### Memory

##### Read the string that is pointed to by a char* pointer
`memory read 0x00007fff36d99fb5`
##### Read five instructions after address
`memory read --format instruction --count 5 0x10463d970`
##### Get start and end of search
```
(lldb) section
[0x0000010462c000-0x00000107744000] 0x0003118000 MyApp`__TEXT
[0x00000107744000-0x00000107d48000] 0x0000604000 MyApp`__DATA
/* removed sections for brevity */
```
##### Find String in memory range
`mem find -s "youtube" -- 0x00000107744000 0x00000107d48000`
##### Read 100 bytes from address
`memory read -c100 0x10793362c`

### Scripting
```
//See how many times a C function is called when running an iOS app.

breakpoint set -n getenv
breakpoint modify --auto-continue 1
breakpoint command add 1
  po (char *)$arg1								// telling lldb how to cast $arg1
  DONE
continue
```


### Watchpoint
##### Help
`help watchpoint set`
##### watchpoint list
`watchpoint list`
##### watchpoint delete
`watch del 1`
##### watchpoint on Global variable
`watchpoint set variable file_exists`
##### Once it stops
`po file_exists = NO`
##### watchpoint on frame variable
`watchpoint set variable completionHandler`
##### watchpoint on address in function
`watchpoint set expression -w write -- "+[YDFileChecker checkFileExists]" + 32`
##### watchpoint on register
`watchpoint set expression -- $arg1`
##### watchpoint on register
`watchpoint set expression -w read_write -- $arg1`
##### Delete some watchpoints, if you see this error
`error: sending gdb watchpoint packet failed`

### Settings
##### show target.run-args
`settings show target.run-args`
##### show target.env-vars
`settings show target.env-vars`
##### Add setting to lldbinit file
`echo "settings set target.x86-disassembly-flavor intel" >> ~/.lldbinit`
##### Logging
`settings set target.process.extra-startup-command QSetLogging:bitmask=LOG_ALL;`


### Scripts
```
command alias yd_reload_lldbinit command source ~/.lldbinit
command script import /usr/local/opt/chisel/libexec/fblldb.py   // https://github.com/facebook/chisel
command script import ~/lldb_commands/dslldb.py                 // https://github.com/DerekSelander/LLDB
```
### Aliases
##### extend your commands
```
command alias -h "Run a command in the UNIX shell." -- yd_shell platform shell
command alias -h "add: <search_term> -m module" yd_lookup lookup -X (?i)
command alias yd_dump image dump symtab -m C_Playground
```
##### Beautify
```
settings show thread-format
command alias yd_thread_beautify settings set thread-format "thread: #${thread.index}\t${thread.id%tid}\n{ ${module.file.basename}{`${function.name-with-args}\n"
command alias yd_register_beautify register read -f d
```
##### lldb context
```
command alias yd_smoke exp let $z = 5
command alias yd_swift settings set target.language swift
command alias yd_objc settings set target.language objc
command alias yd_c settings set target.language c
command alias yd_stack_vars frame variable --no-args
```
##### lldb over USB
`command alias yd_attach process connect connect://localhost:6666`


### Objective C
#### Initializing Classes
The following bit of code gets your age in seconds.   You validate the answer at https://www.epochconverter.com/.  This code shows:

- `alloc` gives pointer to new a object that needs to be initialized
- `alloc` and `init` the most common pattern in Objective-C
- `new` a shorthand way of writing `alloc` and `init`
- `initWithCalendarIdentifier` after `alloc` initialize with a custom `init` call

The following article suggests: `new = alloc + init`
https://stackoverflow.com/questions/11256228/what-is-the-difference-between-class-new-and-class-alloc-init-in-ios/11256311
```
#import <Foundation/Foundation.h>

int main(int argc, const char * argv[]) {
    @autoreleasepool {

        NSDate *today = [NSDate new];

        NSDateComponents *comps = [[NSDateComponents alloc]init];
        comps.day = 1;
        comps.year = 1999;
        comps.month = 1;
        comps.hour = 18;
        NSCalendar *g = [[NSCalendar alloc] initWithCalendarIdentifier:NSCalendarIdentifierGregorian];

        NSDate *mydob = [g dateFromComponents:comps];

        NSLog(@"Pointer to my dob: %p and today: %p", mydob, today);
        double time_alive = [today timeIntervalSinceDate: mydob];
        NSLog(@"I have been alive for this many seconds %.0f", time_alive);
    }
    return 0;
}

```
#### Classes
```
#import <Foundation/Foundation.h>

@interface Box:NSObject {
    double length;    // Length of a box
    double breadth;   // Breadth of a box
    double height;    // Height of a box
}

@property(nonatomic, readwrite) double height;  // Property
-(double) volume;
@end

@implementation Box

@synthesize height;

-(id)init {
    self = [super init];
    length = 1.0;
    breadth = 1.0;
    return self;
}

-(double) volume {
    return length*breadth*height;
}

@end

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        Box *box1 = [[Box alloc]init];    // Create box1 object of type Box

        double volume = 0.0;             // Store the volume of a box here

        // box 1 specification
        box1.height = 5.0;

        // volume of box 1
        volume = [box1 volume];
        NSLog(@"Volume of Box1 : %f", volume);
    }
    return 0;
}
```

##### Create a new Class Instance
```
(lldb) exp Box *$b = [Box new];

I could have easily written:
(lldb) exp Box *$a = [[Box alloc]init];

```
##### Print an initialised Class variable
```
(lldb) po $a->length
1
```
##### Print the Class pointer
```
(lldb) po $b
<Box: 0x100777d50>

(lldb) po (Box*)$b
<Box: 0x100777d50>
```
##### Set a Class variable
```
(lldb) exp $b->height = 20.0
(double) $8 = 20

(lldb) po $b->height
20
```
##### Access Instance Method
```
(lldb) po $b.volume
20
```
#### Invoke Instance Method with several parameters
I found some of the Objective-C syntax odd. Where is the major label in the below API?
```
- (void)getVersion:(int*)num1 minor:(int*)num2 patch:(int*)num3;

(lldb) e SampleClass *$sample = [[SampleClass alloc]init];
(lldb) po $sample
<SampleClass: 0x10040ae70>

(lldb) exp [$sample getVersion:&a minor:&b patch:&c];
```
#### NSString to NSData and back
```
(lldb) exp @import Foundation
(lldb) exp NSString* $str = @"hello string";
(lldb) po $str
hello string
(lldb) exp NSData* $data = [$str dataUsingEncoding:NSUTF8StringEncoding];
(lldb) po $data
<74657374 73747269 6e67>
(lldb) po (NSData*) $data
<74657374 73747269 6e67>

// just like in C, you have to encoded based on whether you had a null terminated string or not.
(lldb) exp NSString* $newStr = [[NSString alloc] initWithData:$data encoding:NSUTF8StringEncoding];
(lldb) po $newStr
hello string
```
#### Booleans
```
(lldb) expression BOOL $myflag = YES
(lldb) print $myflag
(BOOL) $myflag = NO
(lldb) expression $myflag = YES
(BOOL) $7 = YES
(lldb) print $myflag
(BOOL) $myflag = YES
```
#### Properties - save some code
To avoid specifying setter and getter functions, you can use @property in the Interface file and @synthesize in the implementation file.
```
#import <Foundation/Foundation.h>

@interface User : NSObject
{
    NSString *_firstName;
}
    @property (nonatomic, strong)NSString *firstName;
@end

@implementation User
    @synthesize firstName = _firstName;
@end

int main () {

    User *user = [[User alloc] init];
    user.firstName = @"Hook";
    NSLog(@"the captain is: %@", user.firstName);
    return 0;
}
```

#### Static Properties
```
@interface User : NSObject
    @property (class, nonatomic, assign, readonly) NSInteger userCount;
    @property (class, nonatomic, copy) NSUUID *identifier;
    + (void)resetIdentifier;
@end

@implementation User
    static NSUUID *_identifier = nil;
    static NSInteger _userCount = 0;

    + (NSInteger)userCount {
        return _userCount;
    }

    + (NSUUID *)identifier {
        if (_identifier == nil) {
            _identifier = [[NSUUID alloc] init];
        }
        return _identifier;
    }

    + (void)setIdentifier:(NSUUID *)newIdentifier {
        if (newIdentifier != _identifier) {
            _identifier = [newIdentifier copy];
        }
    }

    - (instancetype)init
    {
        self = [super init];
        if (self) {
            _userCount += 1;
        }
        return self;
    }

    + (void)resetIdentifier {
        _identifier = [[NSUUID alloc] init];
    }
@end

int main () {

    User *user;
    for (int i = 0; i < 3; i++) {
        user = [[User alloc] init];
        NSLog(@"User count: %ld",(long)User.userCount);
        NSLog(@"Identifier = %@",User.identifier);
    }

    [User resetIdentifier];
    NSLog(@"Identifier = %@",User.identifier);
    return 0;
}
```


### lldb and Objective-C Blocks
##### lldb "Hello World" Block
```
(lldb) exp
1 void (^$simpleBlock)(void) = ^{
2 NSLog(@"hello from a block!");
3 };
4

(lldb) po $simpleBlock()
[1136:66563] hello from a block!
```
##### While Loop inside a Block
```
(lldb) expression
1 void (^$helloWhile)(int) =
2 ^(int a) {
3 while(a <10) {
4 printf("Hello %d\n", a);
5 a++;
6 }};

(lldb) po $helloWhile(2)
Hello 2
Hello 3
Hello 4
......
```
##### Add two numbers with a Block
```
(lldb) expression
1 int (^$add)(int, int) =
2 ^(int a, int b) { return a+b; }

(lldb) p $add(3,4)
(int) $0 = 7

(lldb) po $add
0x0000000101424110

(lldb) p $add
(int (^)(int, int)) $add = 0x0000000101424110
```

##### Void Block
```
po void (^$fakeBlock)(int, NSURLCredential * _Nullable) =^(int a, NSURLCredential *b) {NSLog(@"hello. Original enum was set to %d", a);}

po $fakeBlock(2,0)
```
##### Use Global Dispatch Block
```
(lldb) expression
1 dispatch_sync(dispatch_get_global_queue(0,0),
         ^(){ printf("Hello world\n"); });
```
##### Calling the Block with a Name
```
A more complicated example that gives the Block a name so it can be called like a function.

(lldb) exp
1 double (^$multiplyTwoValues)(double, double) =
2 ^(double firstValue, double secondValue) {
3 return firstValue * secondValue;
4 };
5

(lldb) po $multiplyTwoValues(2,4)
8


(lldb) exp double $result
(lldb) p $result
(double) $result = 0
(lldb) exp $result = $multiplyTwoValues(2,4)
(double) $1 = 8
(lldb) po $result
8
```

##### Get the syntax
```
(lldb) expression
Enter expressions, then terminate with an empty line to evaluate:
1 void(^$remover)(id, NSUInteger, BOOL *) = ^(id string, NSUInteger i,BOOL *stop){
2 NSLog(@"ID: %lu String: %@", (unsigned long)i, string);
3 };
4

(lldb) p $remover
(void (^)(id, NSUInteger, BOOL *)) $remover = 0x00000001021a4110

(lldb) exp [oldStrings enumerateObjectsUsingBlock:$remover]

ID: 0 String: odd
ID: 1 String: raygun
ID: 2 String: whoop whoop
3 String: doctor pants
```

### lldb with C code
##### malloc / strcpy
Create a malloc char array, copy with strcpy, and free.
```
(lldb) e char *$str = (char *)malloc(8)
(lldb) e (void)strcpy($str, "munkeys")
(lldb) e $str[1] = 'o'
(lldb) p $str
(char *) $str = 0x00000001c0010460 "monkeys"
```
##### Warm-up - getenv
```
(lldb) e const char *$home = NULL
(lldb) p *$home
error: Couldn't apply expression side effects : Couldn't dematerialize a result variable: couldn't read its memory
(lldb) e $home = getenv("HOME")
(const char *) $3 = 0x00007ffeefbff8d2 "/Users/foobar"
(lldb) po $home
"/Users/foobar"
(lldb) p $home
(const char *) $home = 0x00007ffeefbff8d2 "/Users/foobar"
```
##### Examine
```
(lldb) malloc_info --type 0x1c0010480
[+][+][+][+] The string is in the heap!  [+][+][+][+]

(lldb) memory read 0x00000001c0010460
```
##### Free
```
(lldb) e (void)free($str)
```
##### Print Bool
```
(lldb) po (bool) result
<object returned empty description>

(lldb) p result
(bool) $2 = true

(lldb) p/x result
(bool) $0 = 0x01

(lldb) exp result = false
(bool) $1 = false

(lldb) p/x result
(bool) $2 = 0x00

(lldb) p/t result
(bool) $4 = 0b00000000

(lldb) exp result = true
(bool) $5 = true

(lldb) p/t result
(bool) $6 = 0b00000001
```
##### Print Char Array
```
(lldb) po (char*) message
"AAAA"

(lldb) po message
"AAAA"

(lldb) p message
(char *) $5 = 0x0000000100000fa9 "AAAA"

(lldb) p *message
(char) $1 = 'A'
```
##### Struct initialize
```
(lldb) expr struct YD_MENU_ITEMS $menu = {.menu_option = "a", .description = "all items"};

(lldb) expr struct VERSION_INFO $b
error: typedef 'VERSION_INFO' cannot be referenced with a struct specifier

(lldb) expr VERSION_INFO $b
(lldb) p $b
(VERSION_INFO) $b = (Major = 0, Minor = 0, Build = 0)
```
##### Enum initialize
```
(lldb) expr PAS_RESULT $a
(lldb) po $a
<nil>
(lldb) p $a
(PAS_RESULT) $a = 0
(lldb) exp $a = 2
(PAS_RESULT) $0 = 2
```
##### Cast return types
The flexibility of `void *` is a great tool.  If you don't know how to cast the return handle, you can just point it to the garbage.
```
(lldb) exp (void*) getCurrentVersion(&$b);
(void *) $2 = 0x0000000000000000
(lldb) p $b
(VERSION_INFO) $b = (Major = 4, Minor = 6, Build = 13)
```

##### Banana Skins
Make sure you add the `$` sign before a variable. Else you will hit:

`error: warning: got name from symbols: b`


### Advanced
##### Check versions ( python, lldb )
`script import sys; print(sys.version)`
##### Launch
`lldb attach -p ps x|grep -i -m1 sample|awk '{print $1}'` // 'sample' is app name
##### Import lldb script
`command source <file_path>/lldb_script.txt`
##### Import Python script
`command script import <file_path>/lldb_python.py`

##### lldb command line ( no XCode )
```
- Kill xcode
- Run iOS app in the simulator
- run a `ps -ax` to find your PID
- `$ lldb -p <PID>`
```
##### Watch Packets ( caution )
`log enable gdb-remote packets`
##### Custom prompt
`settings set prompt \-\>`
##### Print with NSLog
`exp (void)NSLog(@"😀foobar woobar");`  // on a real iOS device, you don't need to `caflush` for this to appear in `console.app`


### stdout
If you use `lldb --wait-for` or `lldb -attach` you are attaching **after** a decision on where to send `stdout` was made.  For example:

```
// NSLog only sent to Console.app when you attach

./objc_playground_2
ps -ax
lldb -p 3668

(lldb) exp @import Foundation
(lldb) exp (void)NSLog(@"hello");
(lldb) c
Process 3668 resuming
< you can see the output to NSLog when you open console.app >
```
But you can control `stdout`.
```
$) lldb
(lldb) target create my_playground
(lldb) process launch
(lldb) exp @import Foundation
(lldb) exp (void)NSLog(@"hello");
2018-12-13 10:14:09.638801+0000 objc_playground_2[2776:61771] hello
```

### lldb - playing with screens
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
#### Part 3 : UINavigationBar add Right-Sided Button
```
(lldb) search UINavigationBar
(lldb) e id $nc = (id)0x113d960e0
(lldb) po [$nc setBarTintColor: [UIColor greenColor]]
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
#### Advanced : Wiring a more complicated U.I.
 - [ ] Find a UITabBarController in memory
 - [ ] Create a new UINavigationController
 - [ ] Create a new UIViewController
 - [ ] Connect the UIViewController to the UINavigationController
 - [ ] Create a new array of UINavigationControllers
 - [ ] Check the View Hierarchy to ensure it is wired correctly

```
 (lldb) search UITabBarController
 <UITabBarController: 0x7fa3b0029600>

 (lldb) search UINavigationController
 <UINavigationController: 0x7fa3b0813600>

 (lldb) po id $nc = [[UINavigationController alloc] initWithRootViewController:$sithvc]
 (lldb) po $nc
 <UINavigationController: 0x7fa3af80a000>

 (lldb) search UINavigationController
 <UINavigationController: 0x7fa3af81a200>

 <UINavigationController: 0x7fa3b0813600>

 (lldb) po [$nc2 viewControllers]
 <__NSSingleObjectArrayI 0x600002005570>(
 <tinyDormant.YDSithVC: 0x7fa3af704430>
 )

 (lldb) e Class $sithVcClass = (Class) objc_getClass("tinyDormant.YDSithVC")
 (lldb) e id $sithvc = (id)[$sithVcClass new]
 (lldb) po $sithvc
 <tinyDormant.YDSithVC: 0x7fa3af704430>

// NOW I NEED TO ADD IT...

 (lldb) po [[UIWindow keyWindow] rootViewController]
<UITabBarController: 0x7fa3b0029600>

(lldb) e id $tbc = (id)0x7fa3b0029600
(lldb) po $tbc
<UITabBarController: 0x7fa3b0029600>

(lldb) e NSMutableArray *$listofvcontrollers = (NSMutableArray *)[$tbc viewControllers]

(lldb) po $listofvcontrollers
 <__NSArrayM 0x600002cb89f0>(
 <tinyDormant.YDJediVC: 0x7fa3af727240>,
 <UINavigationController: 0x7fa3b0813600>
 )

(lldb) po [$listofvcontrollers addObject:$nc]

 (lldb) po $listofvcontrollers
<__NSArrayM 0x600002cb89f0>(
<tinyDormant.YDJediVC: 0x7fa3af727240>,
<UINavigationController: 0x7fa3b0813600>,
<UINavigationController: 0x7fa3af80a000>
)

(lldb) po [$tbc setViewControllers:$listofvcontrollers]

(lldb) search UITabBar
<UITabBar: 0x7fa476e16be0; frame = (0 618; 375 49); autoresize = W+TM; gestureRecognizers = <NSArray: 0x60000082b690>; layer = <CALayer: 0x600000678b40>>

(lldb) e id $tabs = (id)0x7fa476e16be0
(lldb) e UIImage *$sithimage = [UIImage imageNamed:@"UIBarButtonSystemItemFastForward"]
(lldb) e (void)[[[$tabs items] objectAtIndex:$sithIndex] setImage:$sithimage]
 nil

(lldb) caflush
```
**WARNING** - careful with copy and paste of text into lldb. I spent hours trying to work out why one the above commands was not working.



### Facebook's Chisel
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

### Thread Pause / Thread Exit
```
Thread ID: dec:2264260 hex: 0x228cc4
Thread ID: dec:2264261 hex: 0x228cc5
shark: 0
jelly: 0
shark: 1
jelly: 1
shark: 2
jelly: 2
shark: 3
jelly: 3
shark: 4
jelly: 4
Program ended with exit code: 0
```
### Output
```
 (lldb) settings set thread-format "thread: #${thread.index}\t${thread.id%tid}\n{ ${module.file.basename}{`${function.name-with-args}\n"
 (lldb) thread list
 Process 3106 stopped
 thread: #1    0x1659a
 libsystem_kernel.dylib`__ulock_wait
 * thread: #2    0x165f7
 objc_playground_2`hello_world(voidptr=0x0000000100633f50)
 thread: #3    0x165f2
 libsystem_kernel.dylib`__workq_kernreturn
 thread: #4    0x165f4
 libsystem_kernel.dylib`__workq_kernreturn
 thread: #5    0x165f8
 objc_playground_2`hello_world(voidptr=0x0000000100634370)


 (lldb) exp NSTimeInterval $blockThreadTimer = 2
 (lldb) exp [NSThread sleepForTimeInterval:$blockThreadTimer]
 (lldb) c
 Process 49868 resuming
 [+]Tiger Shark: thread ID: 0x14a075
 [+]Lemon Shark: thread ID: 0x14a07a
 Tiger Shark: 0
 Tiger Shark: 1
 Tiger Shark: 2
 Tiger Shark: 3
 Tiger Shark: 4
 Lemon Shark: 5
 Lemon Shark: 6
 Lemon Shark: 7
 Lemon Shark: 8
 Lemon Shark: 9

```

### help lldb by setting the language
##### I hit this error too many times!
```
(lldb) e id $my_hello = [hello_from_objc new]

error: <EXPR>:3:3: error: consecutive statements on a line must be separated by ';'
id $my_hello = [hello_from_objc new]
  ^
  ;
```
##### Tell lldb you are using Objective-C
`(lldb) expression -l objective-c -o -- id $my_hello = [hello_from_objc new]`
##### print all instance methods available to you..
`expression -lobjc -O -- [$my _shortMethodDescription]`
##### Set the expression language to Swift explicitly:
`(lldb) expression -l swift -o -- let $myHello = HelloClass()`
##### Set the expression language to Swift and call a function
(lldb) expression -l swift -o -- $myHello.hello()
##### Swift:
`(lldb) settings set target.language swift`


### lldb & rootless

Apple's *[System Integrity Protection][5909c6c8]*

  [5909c6c8]: https://developer.apple.com/library/archive/documentation/Security/Conceptual/System_Integrity_Protection_Guide/RuntimeProtections/RuntimeProtections.html "sip"

```
$ sudo lldb -n Finder
(lldb) process attach —name "Finder"
/* fails if you don't disable Rootless */
```
