# lldb - C playground
#### Warm-up
Create a malloc char array, copy with strcpy, and free.

```
(lldb) e char *$str = (char *)malloc(8)
(lldb) e (void)strcpy($str, "munkeys")
(lldb) e $str[1] = 'o'
(lldb) p $str
(char *) $str = 0x00000001c0010460 "monkeys"
```
#### Find
(lldb) section
```
[0x00000000000000-0x00000100000000] 0x0100000000 my_app`__PAGEZERO
[0x0000010440c000-0x00000104ca0000] 0x0000894000 my_app`__TEXT
[0x00000104ca0000-0x00000104d90000] 0x00000f0000 my_app`__DATA
[0x00000104d90000-0x00000104e30000] 0x00000a0000 my_app`__LINKEDIT
```
#### Examine
```
(lldb) malloc_info --type 0x1c0010480
[+][+][+][+] The string is in the heap!  [+][+][+][+]

(lldb) memory read 0x00000001c0010460
```
#### Free
```
(lldb) e (void)free($str)
```
#### Print Bool
```
(lldb) po (bool) result
<object returned empty description>

(lldb) p result
(bool) $2 = true

(lldb) p/x result
(bool) $0 = 0x01

(lldb) exp result = false
(bool) $1 = false

(lldb) p/x result
(bool) $2 = 0x00

(lldb) p/t result
(bool) $4 = 0b00000000

(lldb) exp result = true
(bool) $5 = true

(lldb) p/t result
(bool) $6 = 0b00000001
```
#### Print Char Array
```
(lldb) po (char*) message
"AAAA"

(lldb) po message
"AAAA"

(lldb) p message
(char *) $5 = 0x0000000100000fa9 "AAAA"

(lldb) p *message
(char) $1 = 'A'
```
#### Struct initialize
```
(lldb) expr struct YD_MENU_ITEMS $menu = {.menu_option = "a", .description = "all items"};

(lldb) expr struct VERSION_INFO $b
error: typedef 'VERSION_INFO' cannot be referenced with a struct specifier

(lldb) expr VERSION_INFO $b
(lldb) p $b
(VERSION_INFO) $b = (Major = 0, Minor = 0, Build = 0)
```
#### Enum initialize
```
(lldb) expr PAS_RESULT $a
(lldb) po $a
<nil>
(lldb) p $a
(PAS_RESULT) $a = 0
(lldb) exp $a = 2
(PAS_RESULT) $0 = 2
```
#### Cast return types
The flexibility of `void *` is a great tool.  If you don't know how to cast the return handle, you can just point it to the garbage.
```
(lldb) exp (void*) getCurrentVersion(&$b);
(void *) $2 = 0x0000000000000000
(lldb) p $b
(VERSION_INFO) $b = (Major = 4, Minor = 6, Build = 13)
```

#### Banana Skins
Make sure you add the `$` sign before a variable. Else you will hit:

`error: warning: got name from symbols: b`


#### Stacking Smashing
Even with an almost empty C Playground, it was confusing to look at arm assembler instructions with the default C settings in xCode.  

xCode , by default, added stack protections.  These only appeared in you asm code when you had a Type that was a Char array of a Struct with a Char member.

See the picture for where to turn off Stack Smashing protections.

```
OTHER_CFLAGS = -fno-stack-protector
```
#### Reference
This gist is inspired by a great article:

https://www.objc.io/issues/19-debugging/lldb-debugging/

