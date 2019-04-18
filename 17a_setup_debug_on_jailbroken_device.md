## Setup lldb on Jailbroken device
##### macOS - install iProxy
`brew install usbmuxd`
##### for lldb over USB access..
`iproxy 6666 6666 &`       
##### For SSH over USB access...
`iproxy 2222 22 &`        
##### the final TTD list...
- [x] `ssh -p 2222 root@localhost`   // SSH onto jailbroken device
- [x] `ps -ax | grep -i my_app` //  get your process ID 
- [x] `debugserver localhost:6666 -a my_app` // invoke lldb

##### Electra Jailbreak specifics
Electra ships with an lldb debug server. That is great news.  Previously there were a lot of steps to get the correct debug server onto your jailbroken device.

Note -> a specific path to access the pre-shipped lldb debugserver:

`/Developer/usr/bin/debugserver localhost:6666 -a 4133`
##### Hijack the app, before it starts
`/Developer/usr/bin/debugserver localhost:6666 --waitfor my_app`
##### start lldb from Terminal on macOS
```
$ lldb

(lldb) platform select remote-ios
 Platform: remote-ios
 Connected: no
  SDK Path: "/Users/Library/Developer/Xcode/iOS DeviceSupport/11.4 (15F79)"
  ....
  ....
  ....
 SDK Roots: [ 4] "/Users/Library/Developer/Xcode/iOS DeviceSupport/11.2.6 (15D100)"
 SDK Roots: [ 5] "/Users/Library/Developer/Xcode/iOS DeviceSupport/11.1 (15B93)"
 
(lldb) process connect connect://localhost:6666
(lldb) help methods // smoke test
```
##### References
```
https://github.com/dmayer/idb/wiki/How-to:-ssh-via-usb
https://kov4l3nko.github.io/blog/2018-05-25-my-experience-with-lldb-and-electra-jb/
```

