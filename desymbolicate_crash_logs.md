# Desymbolicate a crash log from an iOS App

## Inspiration from Apple

<https://developer.apple.com/library/archive/technotes/tn2151/_index.html#//apple_ref/doc/uid/DTS40008184-CH1-SYMBOLICATEWITHXCODE>

## Steps to get a dSYM file

- Build the iOS app for Archive
- Extract the MyApp.xcarchive
- Inside that file, you will find your dSYM files.
- To do this manually, inspect the `Package Contents`.

## Get your device crash log

Pull the `.crash` file off a device.  I normally use Xcode for this.

## The manual method

```bash
# 0x1000e4000 = address of app image
# 0x00000001000effdc = the stripped name of the symbol you want to turn into a readable name
atos -arch arm64 -o TheElements.app.dSYM/Contents/Resources/DWARF/TheElements -l 0x1000e4000 0x00000001000effdc
```

## The pro method

In Xcode 9, the file you want is here:

`/Applications/Xcode.app/Contents/SharedFrameworks/DVTFoundation.framework/Versions/A/Resources/symbolicatecrash`

## Print to Terminal the logs

```bash
export DEVELOPER_DIR="/Applications/Xcode.app/Contents/Developer"
./symbolicatecrash -v crash_log_20_9_2018.crash myapp.app.dSYM
```

## Achieve same without specifying the dSYM file

```bash
./symbolicatecrash crash_log_20_9_2018.crash > /yourPath/crash1_symbolicated.crash
```
