# Jailbreak Bypass
With a debugger connected to your iOS app you can easily read and modify Register values.  

Lately, I have been targetting the `setter` and `getter` of Objective-C code.  So when you set or get a value, you automate the manipulation.

## Practice
To finding a method to inspect and modify, you have to good starter commands:
```
(lldb) image lookup -n debugger_challenge.YD_Home_VC.secret_return_value
(lldb) image lookup -rn secret_return_value
```
##### place a  breakpoint
Try a regex breakpoint:
```
(lldb) rb secret_return_value
```
This places the breakpoint at the start of the function.  The breakpoint can also tell you the return type for the function.  We are dealing with an Integer in this function.
##### place a  better breakpoint
Try a regex breakpoint limited to a single dynamic library:
```
(lldb) rb secret_return_value -s hello_framework
```
##### find your register value
```
(lldb) register read // read value inside of $rax
(lldb) dis
(lldb) finish
(lldb) register read
(lldb) register write $rax 0x2e  // put the value 46 in register
```
I was using the xCode Simulator hence I look for the `x86/64` register called `rax`.  This register is called the `r0` register on a physical iOS device.

## Jailbreak Bypass
##### Find the Jailbreak setter
The below steps demonstrate a bypass of Jailbreak checks that run immediately when you launch the app.

##### Connect debugger
Set your iOS debugserver to wait for the app to be opened.

```
ssh onto Jailbroken devices

Install the app on JB device

root# /Developer/usr/bin/debugserver localhost:6666 -v DEBUG=1 -waitfor MYAPP   // on JB device ssh session

OPEN THE APP now the debugserver is waiting for a connection

$) LLDB_SDK=ios lldb // from macOS machine

(lldb) process connect connect://localhost:6666
```
##### Find the target
```
(lldb) lookup jail
****************************************************
2 hits in: MYAPP
****************************************************
-[RSADeviceInfo jailBreak]
-[RSADeviceInfo setJailBreak:]
```
##### Attack the Setter
```
(lldb) b -[RSADeviceInfo setJailBreak:]
Breakpoint 2: where = MYAPP`-[RSADeviceInfo setJailBreak:], address = 0x00000001033fe1fc

(lldb) c
Process 1874 resuming
Process 1874 stopped
* thread #1, queue = 'com.apple.main-thread', stop reason = breakpoint 1.1 2.1
    frame #0: 0x00000001033fe1fc MYAPP` -[RSADeviceInfo setJailBreak:]


(lldb) p (char *) $arg2
(char *) $2 = 0x00000001034bb104 "setJailBreak:"

(lldb) p (char *) $arg3
(char *) $4 = 0x0000000000000005 <no value available>

(lldb) p (int) $arg3
(int) $5 = 5. // this is the value

register write $arg3 0 // put the value 0 (clean?) in the setter
```
##### Attack the getter
Kill the app and start the whole process of connecting again.
```
(lldb) b -[RSADeviceInfo jailBreak]
Breakpoint 1: where = MYAPP`-[RSADeviceInfo jailBreak], address = 0x0000000100b821ec

Process 1957 stopped

(lldb) step until the return register is set $x0 on a physical iOS device

    frame #0: 0x0000000100b821f8 MYAPP` -[RSADeviceInfo jailBreak]  + 12
MYAPP`-[RSADeviceInfo jailBreak]:
->  0x100b821f8 <+12>: ret

(lldb) po (int) $x0
5

(lldb) register write $x0 0

(lldb) p (int) $x0
0
```
🐝🐝 Success 🐝🐝.  

The `getter` example is a little more work; you have to place the `breakpoint`, `step` until it sets the `return register` and then modify the return value.  All of that can be automated.

I prefer changing the `Setter` as this is normally a one-time only call.
## References
Read more about the different ARM and x86 Registers here: https://azeria-labs.com/arm-data-types-and-registers-part-2/

