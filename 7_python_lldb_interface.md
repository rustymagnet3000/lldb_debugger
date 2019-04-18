## Instantiate and read a Swift Class with lldb's Python interpreter
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
(String) firstName = "Derek"

(lldb) script print b
(Allocator.ASwiftClass) $R1 = 0x00006040002918a0 {
  eyeColor = 0x000060000066f040 {
    ObjectiveC.NSObject = {}
  }
  firstName = "Carlos"
  lastName = "Jackel"
}
```
