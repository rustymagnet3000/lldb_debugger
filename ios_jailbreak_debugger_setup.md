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

##### Electra Jailbreak
Electra shipped with a `debug-server`. Previous jailbreaks had lots of manual steps to get the correct `debug-server` onto the device.
![electra](images/2019/06/IMG_0069.png)


##### Electra app will not open
If you have a full Apple iOS developer license, you can code-sign `ad-hoc` apps to last one year. If the `Electra app` won't open, you can re-code sign the `ipa file`.  One way to achieve this:

 - Open `Cydia Impactor`
 - Select `\Device\InstallPackage`
 - Find the `Electra.ipa` file
 - When prompted by `Cydia Impactor` enter your Apple ID.
 - Do **NOT** enter your password.  Go to https://appleid.apple.com/ and generate a `APP-SPECIFIC PASSWORD`

Now `Electra` will work for another year.

##### Electra specifics
When you select `Tweaks`, Electra runs the `debug-server` from a different path:
```
// Tweaks enabled
/Developer/usr/bin/debugserver localhost:6666 -a 794

// Tweaks disabled
/usr/bin/debugserver localhost:6666 -a 794
```
##### Hijack the app, before it starts
`/Developer/usr/bin/debugserver localhost:6666 --waitfor my_app`
##### start lldb from Terminal on macOS
```
$ lldb
(lldb) process connect connect://localhost:6666
(lldb) thread list
```

##### Terminted due to Code Signing Error
If you selected "NO" to `tweaks` and use `lldb` against a `release` iOS app, the debugger will quickly crash, after attaching.  To get around this, you need to change the `entitlements` inside the app bundle.  Specifically: `<key>get-task-allow</key>`.

Instructions here:

https://gist.github.com/rustymagnet3000/605c333519cd265c7eac9d556f46dc75

The end state is:

```
security cms -D -i embedded.mobileprovision | grep -i -A 1 "get"
<key>get-task-allow</key>
	<true/>
```
##### References
```
https://github.com/dmayer/idb/wiki/How-to:-ssh-via-usb
https://kov4l3nko.github.io/blog/2018-05-25-my-experience-with-lldb-and-electra-jb/
```
