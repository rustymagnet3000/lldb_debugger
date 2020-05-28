# lldb and Objective-C Blocks
##### lldb "Hello World" Block
```
(lldb) exp
1 void (^$simpleBlock)(void) = ^{
2 NSLog(@"hello from a block!");
3 };
4

(lldb) po $simpleBlock()
[1136:66563] hello from a block!
```
##### While Loop inside a Block
```
(lldb) expression
1 void (^$helloWhile)(int) =
2 ^(int a) {
3 while(a <10) {
4 printf("Hello %d\n", a);
5 a++;
6 }};

(lldb) po $helloWhile(2)
Hello 2
Hello 3
Hello 4
......
```
##### Add two numbers with a Block
```
(lldb) expression
1 int (^$add)(int, int) =
2 ^(int a, int b) { return a+b; }

(lldb) p $add(3,4)
(int) $0 = 7

(lldb) po $add
0x0000000101424110

(lldb) p $add
(int (^)(int, int)) $add = 0x0000000101424110
```
##### Use Global Dispatch Block
```
(lldb) expression
1 dispatch_sync(dispatch_get_global_queue(0,0),
         ^(){ printf("Hello world\n"); });
```
##### Calling the Block with a Name
```
A more complicated example that gives the Block a name so it can be called like a function.

(lldb) exp
1 double (^$multiplyTwoValues)(double, double) =
2 ^(double firstValue, double secondValue) {
3 return firstValue * secondValue;
4 };
5

(lldb) po $multiplyTwoValues(2,4)
8


(lldb) exp double $result
(lldb) p $result
(double) $result = 0
(lldb) exp $result = $multiplyTwoValues(2,4)
(double) $1 = 8
(lldb) po $result
8
```

##### Get the syntax
```
(lldb) expression
Enter expressions, then terminate with an empty line to evaluate:
1 void(^$remover)(id, NSUInteger, BOOL *) = ^(id string, NSUInteger i,BOOL *stop){
2 NSLog(@"ID: %lu String: %@", (unsigned long)i, string);
3 };
4

(lldb) p $remover
(void (^)(id, NSUInteger, BOOL *)) $remover = 0x00000001021a4110

(lldb) exp [oldStrings enumerateObjectsUsingBlock:$remover]

ID: 0 String: odd
ID: 1 String: raygun
ID: 2 String: whoop whoop
3 String: doctor pants
```

### References
Some examples are from Apple.  Modified to work with lldb.
https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/WorkingwithBlocks/WorkingwithBlocks.html

The better reference was the WWDC `Debugging Tips and Tricks Xcode 8 edition Session 417` download.
