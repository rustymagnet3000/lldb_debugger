## lldb & rootless

I first heard of Apple's *System Integrity Protection* (Rootless?) back in 2015.  

A great short summary of why this doesn't work..

```
$ sudo lldb -n Finder
(lldb) process attach —name "Finder"
```
Can be found here: https://developer.apple.com/library/archive/documentation/Security/Conceptual/System_Integrity_Protection_Guide/RuntimeProtections/RuntimeProtections.html

You need to turn off Rootless.
