## useful lldb aliases
#### scripts
```
command alias yd_reload_lldbinit command source ~/.lldbinit
command script import /usr/local/opt/chisel/libexec/fblldb.py   // https://github.com/facebook/chisel
command script import ~/lldb_commands/dslldb.py                 // https://github.com/DerekSelander/LLDB
```
#### lldb context
```
command alias yd_smoke exp let $z = 5
command alias yd_swift settings set target.language swift
command alias yd_objc settings set target.language objc
command alias yd_c settings set target.language c
```
#### lldb over USB
```
command alias yd_attach process connect connect://localhost:6666
```
#### extend your commands
```
command alias -h "Run a command in the UNIX shell." -- shell platform shell
command alias -h "add: <search_term> -m module" yd_lookup lookup -X (?i)
command alias yd_dump image dump symtab -m C_Playground
```
