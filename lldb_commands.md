# LLDB Commands
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
##### Looks for a Debug Symbol
`(lldb)image lookup -r -n YDClass`
##### Looks for non-debug symbols:
`(lldb)image lookup -r -s YDClass`
##### Print text
```
(lldb) script print "Hello"
Hello
```
##### Breakpoints
```
// delete all breakpoints
breakpoint delete

breakpoint list

// Break on exact ObjC name
b "-[MyUser name:]"

// Regex Breakpoint
rb '\-\[UIViewController\ '
rb '\-\[YDUser(\(\w+\))?\ '
```



Breakpoint 7: no locations (pending).

##### STDOUT

If you use..

`lldb --wait-for`

`lldb -attach`

You are attaching **after** a decision on where to send `stdout` has been made.  

For example:

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
