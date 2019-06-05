# Desymbolicate an iOS App
#### Inspiration from Apple
https://developer.apple.com/library/archive/technotes/tn2151/_index.html#//apple_ref/doc/uid/DTS40008184-CH1-SYMBOLICATEWITHXCODE

#### Steps to get a dsym file
- Build the iOS app for Archive
- Extract the MyApp.xcarchive
- Inside that file, you will find your dSYM files.
- To do this manually, inspect the `Package Contents`.

#### Get your device crash log
Pull the `.crash` file off a device.  I normally use xCode for this.

#### The manual method
```
atos -arch arm64 -o TheElements.app.dSYM/Contents/Resources/DWARF/TheElements -l 0x1000e4000 0x00000001000effdc

0x1000e4000 = address of app image
0x00000001000effdc = is the stripped name of the symbol you want to turn into a readable name
```

#### The pro method
In xCode 9, the file you want is here:
`/Applications/Xcode.app/Contents/SharedFrameworks/DVTFoundation.framework/Versions/A/Resources/symbolicatecrash `

#### Print to Terminal the logs
```
export DEVELOPER_DIR="/Applications/Xcode.app/Contents/Developer"
./symbolicatecrash -v crash_log_20_9_2018.crash myapp.app.dSYM
```

#### Achieve same without specifying the dsym file
`./symbolicatecrash  crash_log_20_9_2018.crash > /yourPath/crash1_symbolicated.crash`

