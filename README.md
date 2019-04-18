# Debugger Playground

### 0. Strings in memory
Find a hidden string with lldb Debugger.  This uses three lldb commands `section`, `memory find`, `memory read` to find a string inside a _stripped, release app_.

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
Once I opened a WKWebView rendered page inside an iOS app, I wanted to use lldb to print all cookies inside the WKWebView cookie store. But once you scratch the surface, you found a lot of data structures underneath the following simple code:

### 5. Facebook's Chisel commands
This was a fun set of python lldb scrupt to re-use. All about the U.I.
