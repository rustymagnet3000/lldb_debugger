#### Attach debugger
```
(lldb) process attach --wait-for -n C_Playground
----- run the app & lldb connects, as I have disabled Rootless on my macOS -----

`C_Playground was compiled with optimization - stepping may behave oddly; variables may not be available.`
```

#### Symbol Table
```
(lldb) image dump symtab -m C_Playground

/*** edited for brevity ****/
Symtab, file = /C_Playground, num_symbols = 9:

Index   UserID DSX Type            File Address/Value Load Address       Size               Flags      Name
------- ------ --- --------------- ------------------ ------------------ ------------------ ---------- ----------------------------------
[    0]      0 D   SourceFile      0x0000000000000000                    Sibling -> [    4] 0x00640000 main.c
[    1]      2 D   ObjectFile      0x000000005b51eb47                    0x0000000000000000 0x00660001 /main.o
[    2]      4 D   Code            0x0000000100000f80 0x0000000100000f80 0x0000000000000010 0x001e0000 marshmallow
[    3]      8 D   Code            0x0000000100000f90 0x0000000100000f90 0x0000000000000008 0x001e0000 main
[    4]     12 D   SourceFile      0x0000000000000000                    Sibling -> [    7]   0x00640000 /biscuit.c
[    5]     14 D   ObjectFile      0x000000005b51d825                    0x0000000000000000 0x00660001 /biscuit.o
[    6]     16 D   Code            0x0000000100000fa0 0x0000000100000fa0 0x000000000000000b 0x001e0000 biscuit
```
#### Summary
A Release scheme with Optimization is not enough to harden your app.
```

(lldb) po marshmallow()
true
(lldb) po biscuit()
96
```
