# Breakpoints & Registers
## Finding a Swift secret inside an ARM register
#### Goal
With a debugger - in this example lldb - I wanted to stop at at the start of a function call and inspect the secrets.  I went into this exercise with the following mapping of where to find my secrets.

Parameter  | Simulator (x86/64) |  Physical (arm64)
--|---|--
return  | rax  |  x0
first  | rdi  |  x5
second  | rsi |  x4
third  |  rdx |  x3
#### Findings
Instead of using my table, it was better to use lldb helper names `$arg1` (object instance) `arg2` (selector) and `$arg3` (first value passed of interest into the selector) instead of the names of register on each chip type.

#### Swift code
```
func read_my_registers(password: String, salt: String, random: Int) -> String {
    print("[+] password: \(password)")
    print("[+] salt: \(salt)")
    print("[+] random number: \(random)")
    return "a returned secret string"
}

let randomString = NSUUID().uuidString          // call into file system for random string
let diceRoll = Int(arc4random_uniform(6) + 1)   // legacy C API used by Swift < 4.1

let lyft = LyftClass(mickey: "wild west")
lyft.read_my_registers(password: "ewoks love a password", salt: randomString, random: diceRoll)

```
#### Debugger - simulator
I started the app with a breakpoint before the U.I. code started to run.
```
(lldb) frame info
frame #0: 0x000000010c3d096e rusty_nails`AppDelegate.application. AppDelegate.swift:13

(lldb) rb read_my_registers         // regex breakpoint
Breakpoint 2: where = rusty_nails`rusty_nails.LyftClass.read_my_registers

(lldb) c
Process 15338 resuming

(lldb) po $rdi
error: <EXPR>:3:1: error: use of unresolved identifier '$rdi'
$rdi

(lldb) settings set target.language objc
Wow.  This was a painful lesson.  Wonder why `po $rx` never works?  
“First, registers are not available in the Swift LLDB debugging context. ”
https://github.com/DerekSelander/LLDB

(lldb) po $rdi
4393530128

(lldb) po (char*) $rdi
"ewoks love a password"
```
#### Debugger - real device
Started the same breakpoint on a real iPhone 7 device.
```
(lldb) po (char*) $x0
"ewoks love a password"
[+] Why is the Return register used at the start of a function?

(lldb)  po (char*) $x3
"AA565D14-2467-4454-ABF0-778A0C3BAE7C"
[+] I was expecting this value to be x2?

(lldb) po (char*) $x5
AA565D14-2467-4454-ABF0-778A0C3BAE7C
[+] Interesting that this is the same as previous value without quotes

(lldb) po (int) $x6
4999
[+] Not sure why this is duplicated inside of registers?

(lldb) po (int) $x8
4999
```

## Breakpoints that auto-continue
```
(lldb) b CCCryptorCreate
Breakpoint 1: where = libcommonCrypto.dylib`CCCryptorCreate, address = 0x000000011047e1b7

(lldb) breakpoint modify --auto-continue true 1
(lldb) br list
Current breakpoints:
1: name = 'CCCryptorCreate', locations = 1, resolved = 1, hit count = 0 Options: enabled auto-continue 
  1.1: where = libcommonCrypto.dylib`CCCryptorCreate, address = 0x000000011047e1b7, resolved, hit count = 0 

then to add some commands I used..

(lldb) breakpoint command add -s python 1
Enter your Python command(s). Type 'DONE' to end.
    print "Hit this breakpoint!"
    DONE

```
## Use breakpoint to print a string inside Code
The Swift Class I want to expect is below:
```
class hello_class {    
    func get_version() -> String {
        return "1.1.1.1.3"
    }
}
```
Connect lldb to your iOS app.  

#### Health-check - run the function with lldb
Check you can create a class instance and all the function.

```
(lldb) image lookup -rn hello_class

(lldb) expression let $hello = hello_class()

(lldb) po $hello
<hello_class: 0x60000001cbd0>

(lldb) po $hello.get_version()
"1.1.1.1.3"
```

#### Place regex breakpoint (iOS Simulator ONLY)
```
(lldb) rb hello_class.get_version
(lldb) continue
```
When the breakpoint hits...
```
(lldb) frame info
(lldb) finish
(lldb) register read $rax
(lldb) memory read <address in the $rax register>
```
You may notice that the returned string was not from the `Data` section.  It was part of the Text segment of the app.
```
(lldb) section my_app

[0x00000000000000-0x00000100000000] 0x0100000000 MY_APP`__PAGEZERO
[0x0000010fac0000-0x0000010fac5000] 0x0000005000 MY_APP`__TEXT
[0x0000010fac5000-0x0000010fac7000] 0x0000002000 MY_APP`__DATA
[0x0000010fac7000-0x0000010fad2000] 0x000000b000 MY_APP`__LINKEDIT
```
If you move the `version` variable and place it as a global variable, it is still inside the `Code` segment of the app.

