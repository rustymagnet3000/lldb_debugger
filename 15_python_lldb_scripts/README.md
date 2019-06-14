## Using Python to write LLDB scripts
#### Warm-up routine
```
(lldb) script lldb.target
<lldb.SBTarget; proxy of <Swig Object of type 'lldb::SBTarget *' at 0x14867a360> >

(lldb) script print lldb.target
SampleApp-Swift

(lldb) script print lldb.thread
thread #1: tid = 0x67f3e, 0x0000000108005244 SampleApp-Swift`main at AppDelegate.swift:14, queue = 'com.apple.main-thread', stop reason = breakpoint 1.4

(lldb) script print lldb.process
SBProcess: pid = 16218, state = stopped, threads = 1, executable = SampleApp-Swift

(lldb) script help(lldb.SBDebugger)

(lldb) script // drops you into the embedded python interpreter
>>> 2+3
5

>>> print lldb.debugger.GetVersionString()
lldb-902.0.79.2
  Swift-4.1

>>> help(lldb.debugger.GetSelectedTarget)

>>> print lldb.debugger.GetSelectedTarget()
SampleApp-Swift
```

## Instantiate and read a Swift Class
```
(lldb) script options = lldb.SBExpressionOptions()
(lldb) script options.SetLanguage(lldb.eLanguageTypeSwift)
(lldb) script options.SetCoerceResultToId()
(lldb) e -lswift -O -- ASwiftClass()
error: <EXPR>:3:1: error: use of unresolved identifier 'ASwiftClass'
ASwiftClass()
^~~~~~~~~~~

(lldb) e -lswift -- import Allocator
(lldb) e -lswift -O -- ASwiftClass()
<ASwiftClass: 0x60000029cd40>
```
Now you can try...
```
(lldb) script b = lldb.target.EvaluateExpression('ASwiftClass()', options)
(lldb) script print b.GetValueForExpressionPath('firstName')
No value
(lldb) script print b.GetValueForExpressionPath('.firstName')
(String) firstName = "Carlos"

(lldb) script print b
(Allocator.ASwiftClass) $R1 = 0x00006040002918a0 {
eyeColor = 0x000060000066f040 {
ObjectiveC.NSObject = {}
}
firstName = "Carlos"
lastName = "Jackel"
}
```


#### References
https://lldb.llvm.org/python-reference.html

https://hub.packtpub.com/lldb-and-command-line/
