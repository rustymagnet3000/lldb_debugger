# GDB
#### Set and Print Variable
```
(gdb) set $foo = 3

(gdb) p/x $foo
$1 = 0x3

(gdb) p $foo
$2 = 3

(gdb) p $bar = "hello"
$3 = "hello"

(gdb) p/x $bar
$4 = {0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x0}

(gdb) p $bar
$5 = "hello"
```
#### Malloc
```
gef> p (int)malloc(6)
$7 = 0xb7ffd020
```

#### Locations of system calls
```
gef> x/x strcpy
0xffffb7f72050 <strcpy>:	0xf3
gef> x/x system
0xffffb7f9fee4 <system>:	0xff
gef> x/x printf
0xffffb7faafa4 <printf>:	0xff
```
#### Set and Print Variable
```
gef> p getenv ("PATH")
'getenv' has unknown return type; cast the call to its declared return type

gef> p (char *) getenv ("PATH")
$8 = 0xffffffffffa2 "/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games"

// https://sourceware.org/gdb/onlinedocs/gdb/Calling.html
(gdb) p ((char * (*) (const char *)) getenv) ("PATH")

gef> set env FooBarEnvVariables=`perl -e 'print "A" x 65'`
```

#### Cool commands
```
Set environment variables
(gdb) set env PATH=`perl -e 'print "A" x 65'`

Follow process forking
(gdb) set follow-fork-mode {parent, child, ask}

```
#### Setup on macOS
```
https://timnash.co.uk/getting-gdb-to-semi-reliably-work-on-mojave-macos/

// NO `brew install gdb`
// NO `set startup-with-shell enable` inside of ~/.gdbinit

Create an Entitlements file

Create a Signing Certificate in KeyChain

codesign --entitlements gdb.xml -fs gdbcert /usr/local/bin/gdb
```

#### References
```
https://www.exploit-db.com/papers/13205
```
