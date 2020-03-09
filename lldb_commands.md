# LLDB Commands
##### Brief list of attached Libraries
`image list -b`
##### Sections of all loaded code
`image dump sections`
##### Sections of a Module
`image dump sections myApp`
##### Symbols of a Module
`image dump symtab myApp`
##### Symbols of all loaded code
`image dump symtab`
##### Print text
```
(lldb) script print "Hello"
Hello
```
#### Breakpoints
```
// delete all breakpoints
breakpoint delete

breakpoint list

// Break on exact ObjC name
b "-[MyUser name:]"

// Regex Breakpoint
(lldb) rb '\-\[UIViewController\ '
```
