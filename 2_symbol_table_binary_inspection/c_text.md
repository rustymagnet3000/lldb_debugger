

#### Strip Dead Code at the Linker phase
Now, try and run the same functions.
```
(lldb) po marshmallow()
error: use of undeclared identifier 'marshmallow'
(lldb) po biscuit()
error: use of undeclared identifier 'biscuit'
```
But that is not a complete solution.  If you dump the symbol table, items are still “friendly” to read.
