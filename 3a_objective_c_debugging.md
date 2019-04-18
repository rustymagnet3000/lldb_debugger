# Objective-C Playground
## Using lldb to understand Objective C
#### Initializing Classes
The following bit of code gets your age in seconds.   You validate the answer at https://www.epochconverter.com/.  This code shows:

- `alloc` gives pointer to new a object that needs to be initialized
- `alloc` and `init` the most common pattern in Objective-C
- `new` a shorthand way of writing `alloc` and `init`
- `initWithCalendarIdentifier` after `alloc` initialize with a custom `init` call

The following article suggests: `new = alloc + init`
https://stackoverflow.com/questions/11256228/what-is-the-difference-between-class-new-and-class-alloc-init-in-ios/11256311
```
#import <Foundation/Foundation.h>

int main(int argc, const char * argv[]) {
    @autoreleasepool {

        NSDate *today = [NSDate new];

        NSDateComponents *comps = [[NSDateComponents alloc]init];
        comps.day = 1;
        comps.year = 1999;
        comps.month = 1;
        comps.hour = 18;
        NSCalendar *g = [[NSCalendar alloc] initWithCalendarIdentifier:NSCalendarIdentifierGregorian];

        NSDate *mydob = [g dateFromComponents:comps];

        NSLog(@"Pointer to my dob: %p and today: %p", mydob, today);
        double time_alive = [today timeIntervalSinceDate: mydob];
        NSLog(@"I have been alive for this many seconds %.0f", time_alive);
    }
    return 0;
}

```
#### Classes
```
#import <Foundation/Foundation.h>

@interface Box:NSObject {
    double length;    // Length of a box
    double breadth;   // Breadth of a box
    double height;    // Height of a box
}

@property(nonatomic, readwrite) double height;  // Property
-(double) volume;
@end

@implementation Box

@synthesize height;

-(id)init {
    self = [super init];
    length = 1.0;
    breadth = 1.0;
    return self;
}

-(double) volume {
    return length*breadth*height;
}

@end

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        Box *box1 = [[Box alloc]init];    // Create box1 object of type Box

        double volume = 0.0;             // Store the volume of a box here

        // box 1 specification
        box1.height = 5.0;

        // volume of box 1
        volume = [box1 volume];
        NSLog(@"Volume of Box1 : %f", volume);
    }
    return 0;
}
```

##### Create a new Class Instance
```
(lldb) exp Box *$b = [Box new];

I could have easily written:
(lldb) exp Box *$a = [[Box alloc]init];

```
##### Print an initialised Class variable
```
(lldb) po $a->length
1
```
##### Print the Class pointer
```
(lldb) po $b
<Box: 0x100777d50>

(lldb) po (Box*)$b
<Box: 0x100777d50>
```
##### Set a Class variable
```
(lldb) exp $b->height = 20.0
(double) $8 = 20

(lldb) po $b->height
20
```
##### Access Instance Method
```
(lldb) po $b.volume
20
```
#### Invoke Instance Method with several parameters
I found some of the Objective-C syntax odd. Where is the major label in the below API?
```
- (void)getVersion:(int*)num1 minor:(int*)num2 patch:(int*)num3;

(lldb) e SampleClass *$sample = [[SampleClass alloc]init];
(lldb) po $sample
<SampleClass: 0x10040ae70>

(lldb) exp [$sample getVersion:&a minor:&b patch:&c];
```
#### NSString to NSData and back
```
(lldb) exp @import Foundation
(lldb) exp NSString* $str = @"hello string";
(lldb) po $str
hello string
(lldb) exp NSData* $data = [$str dataUsingEncoding:NSUTF8StringEncoding];
(lldb) po $data
<74657374 73747269 6e67>
(lldb) po (NSData*) $data
<74657374 73747269 6e67>

// just like in C, you have to encoded based on whether you had a null terminated string or not.
(lldb) exp NSString* $newStr = [[NSString alloc] initWithData:$data encoding:NSUTF8StringEncoding];
(lldb) po $newStr
hello string
```
#### Booleans
```
(lldb) expression BOOL $myflag = YES
(lldb) print $myflag
(BOOL) $myflag = NO
(lldb) expression $myflag = YES
(BOOL) $7 = YES
(lldb) print $myflag
(BOOL) $myflag = YES
```
#### Properties - save some code
To avoid specifying setter and getter functions, you can use @property in the Interface file and @synthesize in the implementation file.
```
#import <Foundation/Foundation.h>

@interface User : NSObject
{
    NSString *_firstName;
}
    @property (nonatomic, strong)NSString *firstName;
@end

@implementation User
    @synthesize firstName = _firstName;
@end

int main () {

    User *user = [[User alloc] init];
    user.firstName = @"Hook";
    NSLog(@"the captain is: %@", user.firstName);
    return 0;
}
```

#### Static Properties
```
@interface User : NSObject
    @property (class, nonatomic, assign, readonly) NSInteger userCount;
    @property (class, nonatomic, copy) NSUUID *identifier;
    + (void)resetIdentifier;
@end

@implementation User
    static NSUUID *_identifier = nil;
    static NSInteger _userCount = 0;

    + (NSInteger)userCount {
        return _userCount;
    }

    + (NSUUID *)identifier {
        if (_identifier == nil) {
            _identifier = [[NSUUID alloc] init];
        }
        return _identifier;
    }

    + (void)setIdentifier:(NSUUID *)newIdentifier {
        if (newIdentifier != _identifier) {
            _identifier = [newIdentifier copy];
        }
    }

    - (instancetype)init
    {
        self = [super init];
        if (self) {
            _userCount += 1;
        }
        return self;
    }

    + (void)resetIdentifier {
        _identifier = [[NSUUID alloc] init];
    }
@end

int main () {

    User *user;
    for (int i = 0; i < 3; i++) {
        user = [[User alloc] init];
        NSLog(@"User count: %ld",(long)User.userCount);
        NSLog(@"Identifier = %@",User.identifier);
    }

    [User resetIdentifier];
    NSLog(@"Identifier = %@",User.identifier);
    return 0;
}
```
