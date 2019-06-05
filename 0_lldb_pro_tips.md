# Pro lldb tips
#### Launch
`lldb attach -p ps x|grep -i -m1 sample|awk '{print $1}'` // 'sample' is the app name
#### Import lldb script
`command source <file_path>/lldb_script.txt`
#### Import Python script
`command script import <file_path>/lldb_python.py`
#### Lookup
```
// This works on a stripped, release app...
(lldb) lookup -X (?i)address -m my_app
```
#### lldb iOS Simulators
Avoid using xCode if you are using the Python Debugger
- Kill xcode
- Run iOS app in the simulator
- run a `ps -ax` to find your PID
- `$ lldb -p <PID>`

### LLDB References
#### Inspiration
https://github.com/DerekSelander/LLDB
#### Multi-line lldb commands
https://swifting.io/blog/2016/02/19/6-basic-lldb-tips/
#### lldb cheatsheet
https://www.nesono.com/sites/default/files/lldb%20cheat%20sheet.pdf
#### some lldb commands
https://gist.github.com/ryanchang/a2f738f0c3cc6fbd71fa
#### great lldb overview
https://www.bignerdranch.com/blog/xcode-breakpoint-wizardry/
#### more lldb info
https://www.objc.io/issues/19-debugging/lldb-debugging/
#### lldb | python References
https://lldb.llvm.org/python-reference.html
#### ptrace References
Tonnes of articles on ptrace's wide API and a surprisingly large amount on using ptrace as a defence mechanism for iOS apps.
#### useful debugger blogs
https://www.unvanquished.net/\~modi/code/include/x86\_64-linux-gnu/sys/ptrace.h.html 
http://www.vantagepoint.sg/blog/89-more-android-anti-debugging-fun
#### ptrace enum values
http://www.secretmango.com/jimb/Whitepapers/ptrace/ptrace.html
#### anti-debug code samples
https://gist.github.com/joswr1ght/fb8c9f4f3f9a2feebf7f https://www.theiphonewiki.com/wiki/Bugging\_Debuggers
