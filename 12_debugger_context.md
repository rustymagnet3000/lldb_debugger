## Make sure lldb knows your language of choice

#### I hit this error too many times!
Why was I getting this error?
```
(lldb) e id $my_hello = [hello_from_objc new]

error: <EXPR>:3:3: error: consecutive statements on a line must be separated by ';'
id $my_hello = [hello_from_objc new]
  ^
  ;
```
#### Tell lldb you are using Objective-C
Whether lldb knows you are in the Swift or Objective-C context seems to be everything.
  
```
(lldb) expression -l objective-c -o -- id $my_hello = [hello_from_objc new]
```
Now print all instance methods available to you..

```
expression -lobjc -O -- [$my _shortMethodDescription]
```
Now invoke an Objective-C method.  Notice, you cannot use the Swift '.' notation.
```
po (int)[$my secret_objc_method]
```
If you get an error
```
error: unknown type name 'let'
error: use of undeclared identifier 'HelloClass'
```
then set the expression language to Swift explicitly:
```
(lldb) expression -l swift -o -- let $myHello = HelloClass()

(lldb) expression -l swift -o -- $myHello.hello()
```
Or you can change the lldb language context back to Objective-C or Swift:

`(lldb) settings set target.language swift`
