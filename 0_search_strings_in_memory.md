# Needle in a haystack
### Find a hidden string with lldb Debugger
I wrote the following for some cheap SO points:

`https://stackoverflow.com/questions/24431619/find-a-string-memory-using-lldb/51495522#51495522`

This uses three lldb commands `section`, `memory find`, `memory read` to find a string inside a **stripped, release app**.

### Debugger commands
```
(lldb) section
[0x0000010462c000-0x00000107744000] 0x0003118000 MyApp`__TEXT
[0x00000107744000-0x00000107d48000] 0x0000604000 MyApp`__DATA
/* removed sections for brevity */

(lldb) mem find -s "youtube" -- 0x00000107744000 0x00000107d48000
data found at location: 0x10793362c
0x10793362c: 79 6f 75 74 75 62 65 2e 63 6f 6d 2f 65 6d 62 65  youtube.com/embe


(lldb) memory read -c100 0x10793362c
0x10793362c: 79 6f 75 74 75 62 65 2e 63 6f 6d 2f 65 6d 62 65  youtube.com/embe
0x10793363c: 64 2f 58 46 67 45 59 75 35 71 66 36 38 3f 61 75  d/XFgccu5qf68?a
```
