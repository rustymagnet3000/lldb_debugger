## lldb - who is calling getEnv in my iOS app?
See how many times a C function is called when running an iOS app.  Some of the callers are unexpected.
```
breakpoint set -n getenv
breakpoint modify --auto-continue 1
breakpoint command add 1
  po (char *)$arg1
  DONE
continue
```
The most interesting line is `po (char *)$arg1`.  You are telling lldb how to cast $arg1.
