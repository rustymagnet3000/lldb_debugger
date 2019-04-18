# Debugger Playground

### 0. Pro lldb tips
`lldb` was Apple's debugger of choice. This article contained references to good lldb articles and a few tips to make debugging simpler.

### 1. Code Lifting
This article was written to show xCode and a debugger working together to:
- [x] extract a dynamic framework from an iOS app
- [x] build a new app and invoke the Objective-C code

### 2. Dormant code
This article was written to show:
- [x] Code can be invoked, even if it was not reference in code or by a header file
- [x] Why shipping _dormant code_ was a bad idea
- [x] Why tiny xCode _Build Settings_ matter, when _stripping symbols_ and _dead-code_

### 3. Objective-C and lldb playground
Learning Objective-C through the eyes of a debugger.

### 4. 🍪 WKWebView Cookie Thief 🍪
Once I opened a WKWebView rendered page inside an iOS app, I wanted my debugger (`lldb`) to print all cookies inside the `WKWebView cookie store`.

### 5. Facebook's Chisel commands
This was a fun set of python lldb scrupt to re-use. All about the U.I.

### 6. iOS create a fake ViewController
I wanted to create a new UIViewController and load it over the top of the screen that was loaded.  This was a workout.  It jumped between Objective-C and Swift context for the debugger.
```
e id $vc = [UIViewController new]
(lldb) po $vc
<UIViewController: 0x1067116e0>
```
### 7. Python lldb interface
This code create a Swift Class with lldb's Python interpreter and read the memory.

### 8. lldb aliases
You won't get far in an iOS / macOS debugging without adding command aliases. These are shorthand commands for your lldb commands.

### 9. Strings in memory
Find a hidden string with lldb Debugger.  This uses three lldb commands `section`, `memory find`, `memory read` to find a string inside a _stripped, release app_.

### 10. Swift code
If you  invoked code from a Swift dynamic framework, you hit a lot of traps.  This article was to explain how to avoid traps.

### 11. Code injection
Loaded a framework - that was not shipped in an app - and instantiate one of the framework's classes.

### 12. Debugger language context
In iOS, an app maybe written in Swift but a lot of the objects still had Objective-C base classes.  This article helps explain the error and fix it.

### Breakpoints & Registers
I wanted to stop at at the start of a function call and inspect the secrets.
