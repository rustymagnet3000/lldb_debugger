## useful lldb aliases
#### scripts
```
command alias yd_reload_lldbinit command source ~/.lldbinit
command script import /usr/local/opt/chisel/libexec/fblldb.py   // https://github.com/facebook/chisel
command script import ~/lldb_commands/dslldb.py                 // https://github.com/DerekSelander/LLDB
```

#### extend your commands
```
command alias -h "Run a command in the UNIX shell." -- yd_shell platform shell
command alias -h "add: <search_term> -m module" yd_lookup lookup -X (?i)
command alias yd_dump image dump symtab -m C_Playground
```
#### Beautify
```
command alias yd_thread_beautify settings set thread-format "thread: #${thread.index}\t${thread.id%tid}\n"
command alias yd_register_beautify register read -f d
```
#### lldb context
```
command alias yd_smoke exp let $z = 5
command alias yd_swift settings set target.language swift
command alias yd_objc settings set target.language objc
command alias yd_c settings set target.language c
command alias yd_stack_vars frame variable --no-args
```
#### lldb over USB
```
command alias yd_attach process connect connect://localhost:6666
```
