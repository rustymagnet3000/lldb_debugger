
## Thread Pause / Thread Exit
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


 (lldb) exp NSTimeInterval $blockThreadTimer = 2
 (lldb) exp [NSThread sleepForTimeInterval:$blockThreadTimer]
 (lldb) c
 Process 49868 resuming
 [+]Tiger Shark: thread ID: 0x14a075
 [+]Lemon Shark: thread ID: 0x14a07a
 Tiger Shark: 0
 Tiger Shark: 1
 Tiger Shark: 2
 Tiger Shark: 3
 Tiger Shark: 4
 Lemon Shark: 5
 Lemon Shark: 6
 Lemon Shark: 7
 Lemon Shark: 8
 Lemon Shark: 9

```
