# LLDB Commands
### Getting started
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
##### Read five instructions after address
`memory read --format instruction --count 5 0x10463d970`
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

### Advanced
### lldb command line ( no XCode )
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
### STDOUT
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
