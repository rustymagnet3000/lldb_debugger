
## Thread Pause / Thread Exit
I have a C program that ran multiple threads.  

These threads were not tied together but they called the same function. Each started on a unique, background thread.  The threads started at roughly the same time.

### Output
```
Thread ID: dec:2264260 hex: 0x228cc4
Thread ID: dec:2264261 hex: 0x228cc5
shark: 0
jelly: 0
shark: 1
jelly: 1
shark: 2
jelly: 2
shark: 3
jelly: 3
shark: 4
jelly: 4
Program ended with exit code: 0
```
### Output
```


 (lldb) settings set thread-format "thread: #${thread.index}\t${thread.id%tid}\n{ ${module.file.basename}{`${function.name-with-args}\n"
 (lldb) thread list
 Process 3106 stopped
 thread: #1    0x1659a
 libsystem_kernel.dylib`__ulock_wait
 * thread: #2    0x165f7
 objc_playground_2`hello_world(voidptr=0x0000000100633f50)
 thread: #3    0x165f2
 libsystem_kernel.dylib`__workq_kernreturn
 thread: #4    0x165f4
 libsystem_kernel.dylib`__workq_kernreturn
 thread: #5    0x165f8
 objc_playground_2`hello_world(voidptr=0x0000000100634370)
 error: execution stopped with unexpected state.
 error: Execution was interrupted, reason: breakpoint 1.1.
 The process has been returned to the state before expression evaluation.
 jelly: 0
 jelly: 1
 jelly: 2
 jelly: 3
 jelly: 4

 // PATH 1
 (lldb) exp NSTimeInterval $blockThreadTimer = 0.5;
 (lldb) exp [NSThread sleepForTimeInterval:$blockThreadTimer];
 Thread ID: dec:76518 hex: 0x012ae6
 jelly: 0
 jelly: 1
 jelly: 2
 jelly: 3
 jelly: 4

  // PATH 2
 (lldb) exp [NSThread exit];
 Warning: hit breakpoint while running function, skipping commands and conditions to prevent recursion.error: Execution was interrupted, reason: breakpoint 3.1.
 The process has been returned to the state before expression evaluation.
 jelly: 0
 jelly: 1
 jelly: 2
 jelly: 3
 jelly: 4

 (lldb) c
 Process 3004 resuming
 Program ended with exit code: 0

```
