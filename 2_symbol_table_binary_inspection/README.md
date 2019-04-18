# The life of a biscuit
## Using the Symbol table to inspect a binary  
This article was written to show:
- [x] Code can be invoked, even if it is not reference in code or by a header file
- [x] Why shipping "dormant code" is a bad idea
- [x] Why tiny xCode Build Settings for stripping symbols and dead-code matter


#### C code
The reference project has two c files: `biscuit.c` and `main.c`
```
#include "biscuit.h"

int biscuit(void){
    return 96;
}
```
```
#include <stdio.h>
#include <stdbool.h>
/**** No reference to  biscuit header file ****/

bool marshmallow(void){
    return true;
}

int main() {
    bool result = false;
    result = marshmallow();
    return 0;
}
```

#### Release build with optimization￼

In Xcode, turn on Optimization to the max setting in your Release mode.

> Tip ->   CMD+C over an xCode Build Setting gives the compiler flag being set

Now set it a Release build with no debug options selected.
￼
