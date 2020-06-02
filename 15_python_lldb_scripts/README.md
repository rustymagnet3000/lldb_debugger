## Using Python to write LLDB scripts
### Warm-up
```
// Great auto-continue breakpoint to print which method is executing
script print (lldb.frame)

(lldb) script lldb.target
<lldb.SBTarget; proxy of <Swig Object of type 'lldb::SBTarget *' at 0x14867a360> >

(lldb) print lldb.frame.registers
(lldb) script help(lldb.process)
(lldb) script help(lldb.frame)
(lldb) script lldb.debugger.HandleCommand("frame info")

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

### Well placed Breakpoint
```
>>> print lldb.frame
frame #0: 0x000000010fe033eb tinyDormant`YDMandalorianVC.viewDidLoad(self=0x00007f893b245fa0) at mandalorianVC.swift:8:15


>>> print lldb.frame.get_all_variables()
(tinyDormant.YDJediVC) self = 0x00007fc2421187b0 {
  UIKit.UIViewController = {
    UIKit.UIResponder = {
      ObjectiveC.NSObject = {}
    }
  }
  secret_number = (_value = 10)
  secret_string = "foobar"
  secret_nsstring = 0xfe1420463360b96a "ewok"
}

>>> print lldb.frame.GetFunctionName()
tinyDormant.YDJediVC.viewDidLoad() -> ()
```

### Instantiate and read ObjC Class
```
>>> options.SetLanguage(lldb.eLanguageTypeObjC)


// you don't need print, but you won't get usable feedback if you don't use it
>>> print lldb.frame.EvaluateExpression('[MispelledByDesign new]')
 = <could not resolve type>

>>> a = lldb.frame.EvaluateExpression('[UIViewController new]')

>>> print a
(UIViewController *) $1 = 0x00007fab33c12140

>>> print a.description
<UIViewController: 0x7fab33c12140>
```
### Instantiate and read a Swift Class
```
(lldb) script
>>> options = lldb.SBExpressionOptions()
>>> options.SetLanguage(lldb.eLanguageTypeSwift)
>>> options.SetCoerceResultToId()
>>> e -lswift -O -- ASwiftClass()
error: <EXPR>:3:1: error: use of unresolved identifier 'ASwiftClass'
ASwiftClass()
^~~~~~~~~~~

(lldb) e -lswift -- import Allocator
(lldb) e -lswift -O -- ASwiftClass()
<ASwiftClass: 0x60000029cd40>

>>> b = lldb.target.EvaluateExpression('ASwiftClass()', options)
>>> print b.GetValueForExpressionPath('firstName')
No value

>>> script print b.GetValueForExpressionPath('.firstName')
firstName = "Carlos"

(lldb) script print b
(Allocator.ASwiftClass) $R1 = 0x00006040002918a0 {
eyeColor = 0x000060000066f040 {
ObjectiveC.NSObject = {}
}
firstName = "Carlos"
lastName = "Jackel"
}

>>> mynumber = lldb.frame.FindVariable("i")
>>> mynumber.GetValue()
'42'
```



### Troubleshooting
If you hit `unable to execute script function` you are probably hitting what is reported here:

http://ryanipete.com/blog/lldb/python/how_to_create_a_custom_lldb_command_pt_1/

Make sure your `madman.py` filename matches the name in this code:
```
debugger.HandleCommand('command script add -f madman.GetBundleIdentifier yd_bundle_id')
```
### References
https://github.com/theocalmes/lldbpy
https://lldb.llvm.org/use/python.html
https://aijaz.net/2017/01/11/lldb-python/index.html
https://hub.packtpub.com/lldb-and-command-line/
