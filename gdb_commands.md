# GDB
#### Better Cheat-Sheets
```
https://github.com/AnasAboureada/Penetration-Testing-Study-Notes/blob/master/cheatSheets/Cheatsheet_GDB.txt
https://www.exploit-db.com/papers/13205
https://sourceware.org/gdb/onlinedocs/gdb/Symbols.html
https://darkdust.net/files/GDB%20Cheat%20Sheet.pdf
```
#### Setup gdb + gef
```
https://gef.readthedocs.io/en/master/#setup
```
#### Set and Show Variable
```
set $foo = 3
set $str = "hello world"
set disassembly-flavor intel
set environment LD_PRELOAD=./mylib.so

show environment
show environment PATH
```
#### Print
```
gef➤  print "foobar"
$1 = "foobar"

gef➤  print $1
$2 = "foobar"

(gdb) p/x $foo
$1 = 0x3

(gdb) p $foo
$2 = 3

(gdb) p 5+5
$5 = 0xa

(gdb) p $bar = "hello"
$3 = "hello"

(gdb) p/x $bar
$4 = {0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x0}

(gdb) p $bar
$5 = "hello"
```
#### Breakpoints and Stepping
```
b *start_level
b *start_level + 24
b atoi
b _ZN8password11checkLengthEi

// break if Register ( Second Argument: RSI ) set to 6
break if $rsi == 6

// break if
break passwordcheck if 0 == 0

// Run debugger commands on Breakpoint 1
command 1
Type commands for breakpoint(s) 1, one per line.
End with a line saying just "end".
>print "fluffy foobar"
>end

gef➤ info breakpoints
gef➤ delete breakpoints
gef> nexti 3     /* run next 3 instructions */
```
#### Malloc
```
gef> p (int)malloc(6)
$7 = 0xb7ffd020
```
#### Structs
```
(gdb) ptype /o struct locals
```
#### Buffer filling
Useful when trying to overfill a buffer with `gets` / `strcpy` or an `environment variable`
```
// Bash
$ python -c 'print "A"*(80) + "\x44\x05\x01\x00"' | ./stack-four
$ cat ~/128chars | ./stack-five

// inside gdb
gef> r <<< AAAA
gef> r < ~/payload        <- read in file ( for gets() )
gef> r <<< $(python -c 'print "A"*80 + "\x44\x05\x01\x00"')
(gdb) run $(python -c 'print "\x90" * 132 + "\xff\xfe\xfd\x98"')
```

#### Sections
```
Display executable sections
(gdb) main info sec
Exec file:
    `/root/vuln', file type elf32-i386.
    0x080480f4->0x08048107 at 0x000000f4: .interp ALLOC LOAD READONLY DATA HAS_CONTENTS
    0x08048108->0x08048128 at 0x00000108: .note.ABI-tag ALLOC LOAD READONLY DATA HAS_CONTENTS
    0x08048128->0x080482c4 at 0x00000128: .hash ALLOC LOAD READONLY DATA HAS_CONTENTS
    0x080482c4->0x080486c4 at 0x000002c4: .dynsym ALLOC LOAD READONLY DATA HAS_CONTENTS
```
#### Disassemble
```
(gdb) disassemble main
(gdb) disas start_level
```
#### Where am I?
```
gef> where            
#0  0x0001058c in start_level ()
#1  0x41414140 in ?? ()

//  Instruction
gef> x/i $pc
=> 0x105fc <main+32>:	bl	0x10454 <getenv@plt>

gef> x/2i $pc
=> 0x105fc <main+32>:	bl	0x10454 <getenv@plt>
   0x10600 <main+36>:	str	r0, [r11, #-8]

gef> whatis 0x000106d8
type = int

gef> whatis "hello"
type = char [6]

Set environment variables
(gdb) set env PATH=`perl -e 'print "A" x 65'`
```
#### Shared Libraries
```
info sharedlibrary
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

gef> x/s *((char **)environ)
0xfffefed4:	"LS_COLORS="
```
#### Registers
```
info registers
```
#### Memory
```
gef> x/100wx $sp-200     // check overflowed Stack

gef> x/24x $sp          // read hex address from Stack pointer

gef> x/2w $sp        <--- print from stack pointer
0xfffefd00:	0xfffefd84	0x00000001	0x00000011	0xf77f0288

gef> x/wx 0xfffefd84        <--- print memory address
0xfffefd84:	0xfffefe8e

gef> x/s 0xfffefe8e         <-- string
0xfffefe8e:	"/opt/phoenix/arm/stack-two"

gef> find $sp, +96,0x000105bc           // find Return address on Stack
0xfffefd64
1 pattern found.
```
#### Calculate Sizes
```
gef> p 0xfffefd74 - 0xfffefd20
$9 = 0x54

gef> p/u 0x54
$10 = 84

gef> p/u 0xfffefd74 - 0xfffefd20
$11 = 84
```
#### GEF commands
```
gef> shellcode search linux arm
gef> shellcode get 698
[+] Downloading shellcode id=698
[+] Shellcode written to '/tmp/sc-fd1r2cvr.txt'

gef> vmmap
Start      End        Offset     Perm Path
0x00010000 0x00011000 0x00000000 r-x /opt/phoenix/arm/stack-four
0x00020000 0x00021000 0x00000000 rwx /opt/phoenix/arm/stack-four
0xf7752000 0xf77df000 0x00000000 r-x /opt/phoenix/arm-linux-musleabihf/lib/libc.so
0xf77ee000 0xf77ef000 0x0008c000 rwx /opt/phoenix/arm-linux-musleabihf/lib/libc.so
0xf77ef000 0xf77f1000 0x00000000 rwx
0xfffcf000 0xffff0000 0x00000000 rwx [stack]
0xffff0000 0xffff1000 0x00000000 r-x [vectors]



gef> check
checkpoint  checksec    
gef> checksec
[+] checksec for '/opt/phoenix/arm/stack-four'
Canary                        : No
NX                            : No
PIE                           : No
Fortify                       : No
RelRO                         : No


gef> xinfo 0xfffcf000
────────────────────────────── xinfo: 0xfffcf000 ──────────────────────────────
Page: 0xfffcf000  →  0xffff0000 (size=0x21000)
Permissions: rwx
Pathname: [stack]
Offset (from page): 0x0
Inode: 0
```
#### Shell
```
gef> shell
$ <shell command>
$ exit
```
#### Cool commands
```
Follow process forking
(gdb) set follow-fork-mode {parent, child, ask}

$) gdb version
GNU gdb (Ubuntu 8.1-0ubuntu3) 8.1.0.20180409-git
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
