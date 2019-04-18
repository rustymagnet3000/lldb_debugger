## Invoke Swift Code with lldb
```
class lyftClass {

    static let request_number = 1
    static let uri = "https://my.url/"
    let app_version = "app_99"

    func facebook() -> Int {
        return 96
    }

    static func google() -> Int {
        return 42
    }
}
```

#### Invoking code from a Framework or the main application ?
If you are invoking code from a Swift dynamic framework, make sure to tell lldb about the Framework.  Below is why...
```
(lldb) exp let $a = RustyAppInfo()
error: <EXPR>:3:10: error: use of unresolved identifier 'RustyAppInfo'
let $a = RustyAppInfo()
       ^~~~~~~~~~~~

(lldb) expr -- import rusty_nails
(lldb) exp let $a = RustyAppInfo()
// success. now you have a class instant.
```
lldb knew I was trying to write swift code. In an iOS app, where you have Swift and Objective-C code, I always find it useful to type:

`(lldb) settings set target.language swift`
#### Connect to app via lldb
I liked to put a breakpoint on the the AppDelegate class.  If you let the app load, the context of Swift is automagically lost by lldb.
#### Print your class
```
(lldb) po lyftClass()
<lyftClass: 0x60c000051dc0>
```
#### Create a class instance
`expression let $lyft = rusty.lyftClass()`
#### Invoke a function from instant class
`po $lyft.app_version()`       
#### Try and print a Class member
```
po $lyft.request_number
error: <EXPR>:3:1: error: static member 'uri' cannot be used on instance of type 'lyftClass'
```
This fails as it is a Static class member and not accessible to the instantiated class.
#### Print a Class member
```
(lldb) po lyftClass.uri
"https://my.url/"
```
#### Print Class function member
```
(lldb) po lyftClass.google()
42
```
## Invoke Swift Class with Initializers
```
class lyftClass {

    static let url = "https://my.url/"
    let version = "app_99.0"
    let mickey: String
    let mouse: Int

    init(mickey: String, mouse: Int) {
        self.mickey = mickey
        self.mouse = mouse
    }

    convenience init(mickey: String){
        self.init(mickey: mickey, mouse: 100)
    }

    func facebook_string() -> String {
        return "jibber jabber"
    }

    static func google_int() -> Int {
        return 42
    }
}
```
#### Create a class instance
```
(lldb) expression let $a = lyftClass()
error: <EXPR>:3:10: error: cannot invoke initializer for type 'lyftClass' with no arguments

<EXPR>:3:10: note: overloads for 'lyftClass' exist with these partially matching parameter lists: (mickey: String, mouse: Int), (mickey: String)
let $a = lyftClass()
```
#### Invoke a function from instant class
```
(lldb) expression let $b = lyftClass(mickey: "zer", mouse: 500)
(lldb) po $b
<lyftClass: 0x60c000284470>

(lldb) po $b.mickey
"zer"

(lldb) po $b.mouse
500   
```
#### Create Class with convenience initializer
```
(lldb) expression let $a = lyftClass(mickey: "wow")
(lldb) po $a
<lyftClass: 0x60000009b580>
(lldb) po $a.mickey
"wow"
(lldb) po $a.mouse
100
```

