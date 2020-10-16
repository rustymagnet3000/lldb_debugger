
<!-- TOC depthFrom:2 depthTo:3 withLinks:1 updateOnSave:1 orderedList:0 -->

	- [Getting started](#getting-started)
	- [Disassemble](#disassemble)
	- [Registers](#registers)
	- [Print](#print)
	- [Breakpoints](#breakpoints)
	- [Memory](#memory)
	- [Watchpoint](#watchpoint)
	- [Settings](#settings)
	- [Scripts](#scripts)
	- [Aliases](#aliases)
	- [lldb and Objective-C Blocks](#lldb-and-objective-c-blocks)
	- [lldb with C code](#lldb-with-c-code)
	- [Advanced](#advanced)
	- [stdout](#stdout)

<!-- /TOC -->

### Getting started
##### Check versions ( python, lldb )
`script import sys; print(sys.version)`
##### Launch
`lldb attach -p ps x|grep -i -m1 sample|awk '{print $1}'` // 'sample' is app name
##### Import lldb script
`command source <file_path>/lldb_script.txt`
##### Import Python script
`command script import <file_path>/lldb_python.py`
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
```
(lldb) search -r 0x0000000100610570
__NSURLSessionLocal * [0x0000000100614d20] + 0x28
```
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
```
command alias yd_attach process connect connect://localhost:6666
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
