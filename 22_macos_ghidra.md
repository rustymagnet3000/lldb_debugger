# Patching a Binary on macOS with Ghidra

### Ghidra
Select `File` and `Export Program`.  

Do NOT select the `Export Tool` option.

### Export and Code Sign
Once exported, open `Terminal`:
```
chmod +x MyApp.bin

mv MyApp.bin /Applications/MyApp.App/Content/MacOS/MyApp

security find-identity -v -p codesigning

codesign --deep --force -s <mac Developer ID> MyApp.app

// RESULT -> MyApp.app: replacing existing signature
```

### Entitlements
If Code-signing fails, check the `entitlements`:
```
jtool --ent MyApp.app/Contents/MacOS/MyApp

codesign -d --entitlements :- MyApp.app/Contents/MacOS/MyApp
```
You can list and clear them:
```
xattr -lr MyApp.app

xattr -cr MyApp.app
```
If you get these errors:
```
EXC_CRASH (Code Signature Invalid)
// check you Code Signed the .app, with the --deep flag

LSOpenURLsWithRole() failed with error -10810
// check file has execute permissions
```
### Anti-Patching Detection
```
lldb -f MyApp.app

(lldb) run
Variant is NONAPPSTORE. Config is Release. Crash reporting (App Center) is enabled. Updating is enabled.
// I was still able to attach, when I removed all Entitlements to a Release build

Process ... exited with status = 173
// This was anti-patch Code Signing error
