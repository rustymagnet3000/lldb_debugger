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
