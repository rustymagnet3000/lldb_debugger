#### Strip Symbols
Turn off the `strip dead code` to prove the next step.

```
$ rabin2 -I C_Playground | grep -E 'arch|stripped'
arch     x86
stripped false      // before applying
￼
$ rabin2 -I C_Playground | grep -E 'arch|stripped'
arch     x86
stripped true       // after applying
```

#### Inspect the Symbol Table
```
(lldb) image dump symtab -m C_Playground

               Debug symbol
               |Synthetic symbol
               ||Externally Visible
               |||
Index   UserID DSX Type            File Address/Value Load Address       Size               Flags      Name
------- ------ --- --------------- ------------------ ------------------ ------------------ ---------- ----------------------------------
[    0]      0   X Data            0x0000000100000000 0x0000000102cd1000 0x0000000000000f80 0x000f0010 _mh_execute_header
[    1]      1   X Undefined       0x0000000000000000                    0x0000000000000000 0x00010100 dyld_stub_binder
[    2]      2  S  Code            0x0000000100000f80 0x0000000102cd1f80 0x0000000000000010 0x00000000 ___lldb_unnamed_symbol1$$C_Playground
[    3]      3  S  Code            0x0000000100000f90 0x0000000102cd1f90 0x0000000000000010 0x00000000 ___lldb_unnamed_symbol2$$C_Playground
[    4]      4  S  Code            0x0000000100000fa0 0x0000000102cd1fa0 0x000000000000000b 0x00000000 ___lldb_unnamed_symbol3$$C_Playground
```
#### Is that enough?
```
(lldb) po marshmallow()
true

(lldb) po biscuit()
96

(lldb) rb biscuit
Breakpoint 1: where = C_Playground`biscuit at biscuit.c:3, address = 0x0000000100000fa0
```

#### Find your functions in the Upside Down
```
$ r2 C_Playground
[0x100000f90]> is
[Symbols]
vaddr=0x100000000 paddr=0x00000000 ord=000 fwd=NONE sz=0 bind=GLOBAL type=FUNC name=__mh_execute_header
vaddr=0x100000f80 paddr=0x00000f80 ord=001 fwd=NONE sz=0 bind=LOCAL type=FUNC name=func.100000f80
vaddr=0x100000f90 paddr=0x00000f90 ord=002 fwd=NONE sz=0 bind=LOCAL type=FUNC name=func.100000f90
vaddr=0x100000fa0 paddr=0x00000fa0 ord=003 fwd=NONE sz=0 bind=LOCAL type=FUNC name=func.100000fa0

4 symbols

[0x100000f90]> s 0x100000fa0
[0x100000fa0]> pdf
/ (fcn) sym.func.100000fa0 11 					// you have found Biscuit!!
|   sym.func.100000fa0 ();
|           0x100000fa0      55             push rbp
|           0x100000fa1      4889e5         mov rbp, rsp
|           0x100000fa4      b860000000     mov eax, 0x60              ; ‘`’. // 60 in hex is 96 in decminal
|           0x100000fa9      5d             pop rbp
\           0x100000faa      c3             ret

```
#### Summary
Conclusion, the biscuit method is still available, via the Symbol table.  It doesn’t matter ..
 - The header file #include "biscuit.h" is never referenced.
 - There is no public API listed in the .h file to this function

You have the symbol.  You can call it, with a release build.  So you require a combination of Security Controls like `strip dead code` AND `strip symbols` to harden the app.  A `Release` build is not enough.
