# LLDB Commands
##### Launch
`lldb attach -p ps x|grep -i -m1 sample|awk '{print $1}'` // 'sample' is app name
##### Where am I?
`frame info`
##### Which Thread am I on?
`thread list`
##### Disassemble by address
`disas -s 0x00001620`
##### Disassemble by function name
`disas -n Foo.Bar`
##### Import lldb script
`command source <file_path>/lldb_script.txt`
##### Import Python script
`command script import <file_path>/lldb_python.py`
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
##### Print text
`script print "Hello"`
##### Registers (x86_64)
Argument  | Register | Alias  
--|---|--
Return  | RAX  | $rax
First  | RDI  | $arg1
Second  | RSI  | $arg2
Third  |  RDX |  $arg3
Fourth  | RCX  | $arg4  
Fifth  | R8  |  $arg5
Sixth  | R9  |  $arg6

Usage: `po $arg2`

##### Create NSString
`exp NSString *$myMethod = NSStringFromSelector(_cmd)`
##### Get Selector
`po NSSelectorFromString($meth)`

## Breakpoints
##### Delete all breakpoints
`b delete`
##### List
`b list`
##### Breakpoint on Address ( gdb syntax )
`b *0x1000016ce`
##### Breakpoint on Address with name (lldb syntax )
`br s -a 0x1000016ce -N fooName`
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
##### Watchpoint
```
watchpoint set variable completionHandler
watchpoint set expression -- $esi
help watchpoint set
help watchpoint set variable
watchpoint list
watch del 1
```
##### lldb iOS Simulators
Avoid using xCode if you are using the Python Debugger:
```
- Kill xcode
- Run iOS app in the simulator
- run a `ps -ax` to find your PID
- `$ lldb -p <PID>`
```
## Advanced
##### Logging
`settings set target.process.extra-startup-command QSetLogging:bitmask=LOG_ALL;`
##### Watch Packets ( caution )
`log enable gdb-remote packets`
##### Custom prompt
`settings set prompt \-\>`
##### Print with NSLog
`exp (void)NSLog(@"😀foobar woobar");`  // on a real iOS device, you don't need to `caflush` for this to appear in `console.app`
## STDOUT
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
