---
name: Objective-C ARC Patterns
description: Use when automatic Reference Counting in Objective-C including strong/weak references, retain cycles, ownership qualifiers, bridging with Core Foundation, and patterns for memory-safe code without manual retain/release.
allowed-tools: []
---

# Objective-C ARC Patterns

## Introduction

Automatic Reference Counting (ARC) is Objective-C's memory management system
that automatically inserts retain and release calls at compile time. ARC
eliminates most manual memory management while providing deterministic memory
behavior and preventing common memory bugs like use-after-free and double-free.

Unlike garbage collection, ARC provides immediate deallocation when reference
counts reach zero, making it suitable for resource-constrained environments like
iOS. Understanding ARC's ownership rules, qualifiers, and patterns is essential
for writing memory-safe Objective-C code and avoiding retain cycles.

This skill covers strong and weak references, ownership qualifiers, retain
cycles, Core Foundation bridging, and best practices for ARC-based memory
management.

## Strong and Weak References

Strong references maintain ownership of objects and prevent deallocation, while
weak references observe objects without preventing deallocation.

```objectivec
// Strong references (default)
@interface Person : NSObject
@property (nonatomic, strong) NSString *name;
@property (nonatomic, strong) NSArray *friends;
@property (nonatomic, strong) UIImage *photo;
@end

@implementation Person
@end

// Weak references
@interface ViewController : UIViewController
@property (nonatomic, weak) id<ViewControllerDelegate> delegate;
@property (nonatomic, weak) IBOutlet UILabel *nameLabel;
@end

@implementation ViewController
@end

@protocol ViewControllerDelegate <NSObject>
- (void)viewControllerDidFinish:(ViewController *)controller;
@end

// Using strong and weak
void strongWeakExample(void) {
    Person *person = [[Person alloc] init];
    person.name = @"Alice"; // Strong reference to NSString

    __weak Person *weakPerson = person; // Weak reference
    NSLog(@"Weak person: %@", weakPerson.name);

    person = nil; // Person deallocated
    NSLog(@"After nil: %@", weakPerson); // weakPerson is now nil
}

// Unowned references (unsafe_unretained)
@interface NodeOld : NSObject
@property (nonatomic, unsafe_unretained) NodeOld *parent;
@property (nonatomic, strong) NSArray<NodeOld *> *children;
@end

@implementation NodeOld
@end

// Weak vs unowned
@interface CommentOld : NSObject
@property (nonatomic, strong) NSString *text;
@property (nonatomic, weak) PostOld *post; // Weak: can be nil
@end

@interface PostOld : NSObject
@property (nonatomic, strong) NSArray<CommentOld *> *comments;
@end

@implementation CommentOld
@end

@implementation PostOld
@end

// Strong captures in blocks
void blockCaptureExample(void) {
    Person *person = [[Person alloc] init];
    person.name = @"Bob";

    // Strong capture
    void (^strongBlock)(void) = ^{
        NSLog(@"%@", person.name); // Captures person strongly
    };

    // Weak capture to avoid retain cycle
    __weak Person *weakPerson = person;
    void (^weakBlock)(void) = ^{
        NSLog(@"%@", weakPerson.name); // Captures weakly
    };

    strongBlock();
    weakBlock();
}
```

Strong references increment retain count, while weak references are
automatically set to nil when the object deallocates, preventing dangling
pointers.

## Retain Cycles and Breaking Them

Retain cycles occur when objects hold strong references to each other, preventing
deallocation. Breaking cycles requires weak or unowned references.

```objectivec
// Retain cycle example
@interface Parent : NSObject
@property (nonatomic, strong) NSArray<Child *> *children;
@end

@interface Child : NSObject
@property (nonatomic, weak) Parent *parent; // Weak to break cycle
@property (nonatomic, strong) NSString *name;
@end

@implementation Parent
- (void)dealloc {
    NSLog(@"Parent deallocated");
}
@end

@implementation Child
- (void)dealloc {
    NSLog(@"Child deallocated");
}
@end

void noCycleExample(void) {
    Parent *parent = [[Parent alloc] init];
    Child *child = [[Child alloc] init];
    child.name = @"Alice";
    child.parent = parent; // Weak reference

    parent.children = @[child]; // Strong reference
    // When parent goes out of scope, both deallocate
}

// Delegate pattern without cycles
@protocol DataSourceDelegate <NSObject>
- (void)dataSourceDidUpdate:(id)source;
@end

@interface DataSource : NSObject
@property (nonatomic, weak) id<DataSourceDelegate> delegate;
- (void)fetchData;
@end

@implementation DataSource
- (void)fetchData {
    // Fetch data
    [self.delegate dataSourceDidUpdate:self];
}

- (void)dealloc {
    NSLog(@"DataSource deallocated");
}
@end

// Block retain cycles
@interface NetworkManager : NSObject
@property (nonatomic, strong) NSString *baseURL;
- (void)fetchDataWithCompletion:(void (^)(NSData *data))completion;
@end

@implementation NetworkManager
- (void)fetchDataWithCompletion:(void (^)(NSData *))completion {
    // Simulate async work
    dispatch_async(dispatch_get_global_queue(
        DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
        NSData *data = [@"response" dataUsingEncoding:NSUTF8StringEncoding];
        dispatch_async(dispatch_get_main_queue(), ^{
            completion(data);
        });
    });
}

- (void)dealloc {
    NSLog(@"NetworkManager deallocated");
}
@end

// Avoiding block cycles with weak-strong dance
@interface ViewController2 : UIViewController
@property (nonatomic, strong) NetworkManager *networkManager;
@end

@implementation ViewController2
- (void)loadData {
    __weak typeof(self) weakSelf = self;
    [self.networkManager fetchDataWithCompletion:^(NSData *data) {
        __strong typeof(weakSelf) strongSelf = weakSelf;
        if (!strongSelf) return;

        // Use strongSelf safely
        NSLog(@"Data loaded: %@", strongSelf.view);
    }];
}

- (void)dealloc {
    NSLog(@"ViewController2 deallocated");
}
@end

// Observer pattern cycles
@interface Observable : NSObject
@property (nonatomic, strong) NSMutableArray *observers;
- (void)addObserver:(id)observer;
- (void)removeObserver:(id)observer;
- (void)notifyObservers;
@end

@implementation Observable
- (instancetype)init {
    self = [super init];
    if (self) {
        _observers = [NSMutableArray array];
    }
    return self;
}

- (void)addObserver:(id)observer {
    // Use NSPointerArray for weak references
    [self.observers addObject:[NSValue valueWithPointer:(__bridge void *)observer]];
}

- (void)removeObserver:(id)observer {
    [self.observers removeObject:[NSValue valueWithPointer:(__bridge void *)observer]];
}

- (void)notifyObservers {
    for (NSValue *value in self.observers) {
        id observer = (__bridge id)(void *)[value pointerValue];
        if (observer) {
            // Notify observer
        }
    }
}
@end
```

Always use weak references for delegates, parent pointers, and observers to
break retain cycles. Use the weak-strong dance in blocks for safe self access.

## Ownership Qualifiers

ARC provides ownership qualifiers that explicitly control memory management
behavior for variables and properties.

```objectivec
// Property ownership qualifiers
@interface Container : NSObject

// Strong: default for object pointers
@property (nonatomic, strong) id strongProperty;

// Weak: doesn't prevent deallocation
@property (nonatomic, weak) id weakProperty;

// Copy: creates a copy of the object
@property (nonatomic, copy) NSString *name;
@property (nonatomic, copy) NSArray *items;

// Assign: for non-object types
@property (nonatomic, assign) NSInteger count;
@property (nonatomic, assign) CGFloat value;

// Unsafe_unretained: weak without nil-ing
@property (nonatomic, unsafe_unretained) id unsafeProperty;

@end

@implementation Container
@end

// Variable qualifiers
void qualifierExamples(void) {
    // __strong: default qualifier
    __strong NSString *strongString = @"Hello";

    // __weak: weak reference
    __weak NSString *weakString = strongString;

    // __unsafe_unretained: unmanaged weak
    __unsafe_unretained NSString *unsafeString = strongString;

    // __autoreleasing: for out parameters
    NSError * __autoreleasing error;
}

// Copy property behavior
@interface Message : NSObject
@property (nonatomic, copy) NSString *text;
@property (nonatomic, copy) NSArray *recipients;
@end

@implementation Message
@end

void copyPropertyExample(void) {
    Message *message = [[Message alloc] init];

    NSMutableString *mutableText = [NSMutableString stringWithString:@"Hello"];
    message.text = mutableText; // Copy made

    [mutableText appendString:@" World"];
    NSLog(@"Message text: %@", message.text); // Still "Hello"
    NSLog(@"Mutable text: %@", mutableText); // "Hello World"
}

// Autoreleasing parameters
BOOL loadData(NSData **outData, NSError **outError) {
    if (outData) {
        *outData = [@"data" dataUsingEncoding:NSUTF8StringEncoding];
    }
    return YES;
}

void autoreleaseExample(void) {
    NSData *data;
    NSError *error;

    if (loadData(&data, &error)) {
        NSLog(@"Loaded: %@", data);
    } else {
        NSLog(@"Error: %@", error);
    }
}

// Property attribute combinations
@interface ConfiguredObject : NSObject

// Read-only strong
@property (nonatomic, strong, readonly) NSString *identifier;

// Read-write copy
@property (nonatomic, copy, readwrite) NSString *name;

// Weak nullable
@property (nonatomic, weak, nullable) id<NSObject> delegate;

// Strong nonnull
@property (nonatomic, strong, nonnull) NSArray *items;

@end

@implementation ConfiguredObject
@end
```

Choose `copy` for properties that accept mutable types like NSMutableString or
NSMutableArray to prevent unexpected mutations.

## Core Foundation Bridging

Core Foundation objects require explicit memory management and bridging to work
correctly with ARC-managed Objective-C objects.

```objectivec
// Toll-free bridging with __bridge
void bridgingExample(void) {
    NSString *nsString = @"Hello";

    // Bridge to CF without transfer
    CFStringRef cfString = (__bridge CFStringRef)nsString;
    // nsString retains ownership

    // Bridge back to NS
    NSString *nsString2 = (__bridge NSString *)cfString;
}

// Transferring ownership to CF
void bridgeRetainExample(void) {
    NSString *nsString = @"Hello";

    // Transfer ownership to CF
    CFStringRef cfString = (__bridge_retained CFStringRef)nsString;
    // Must manually CFRelease

    // Use cfString
    CFIndex length = CFStringGetLength(cfString);
    NSLog(@"Length: %ld", (long)length);

    // Release manually
    CFRelease(cfString);
}

// Transferring ownership from CF
void bridgeTransferExample(void) {
    // Create CF object (owned)
    CFMutableStringRef cfString = CFStringCreateMutable(NULL, 0);
    CFStringAppend(cfString, CFSTR("Hello"));

    // Transfer to ARC
    NSMutableString *nsString = (__bridge_transfer NSMutableString *)cfString;
    // ARC now owns, no CFRelease needed

    [nsString appendString:@" World"];
    NSLog(@"%@", nsString);
}

// Working with CF collections
void cfCollectionExample(void) {
    // Create CF array
    CFArrayRef cfArray = CFArrayCreate(
        NULL,
        (const void *[]){@"A", @"B", @"C"},
        3,
        &kCFTypeArrayCallBacks
    );

    // Bridge to NSArray
    NSArray *nsArray = (__bridge_transfer NSArray *)cfArray;
    NSLog(@"Array: %@", nsArray);
}

// CF property lists
void cfPropertyListExample(void) {
    NSDictionary *dict = @{@"key": @"value"};

    // Convert to CF
    CFPropertyListRef plist = (__bridge_retained CFPropertyListRef)dict;

    // Write to file
    CFURLRef url = (__bridge CFURLRef)[NSURL fileURLWithPath:@"/tmp/test.plist"];
    CFPropertyListWrite(plist, url, kCFPropertyListXMLFormat_v1_0, 0, NULL);

    CFRelease(plist);
}

// Handling CF callbacks
void myCFArrayApplierFunction(const void *value, void *context) {
    NSString *string = (__bridge NSString *)value;
    NSLog(@"Value: %@", string);
}

void cfCallbackExample(void) {
    CFArrayRef cfArray = (__bridge CFArrayRef)@[@"A", @"B", @"C"];

    CFArrayApplyFunction(
        cfArray,
        CFRangeMake(0, CFArrayGetCount(cfArray)),
        myCFArrayApplierFunction,
        NULL
    );
}
```

Use `__bridge` for temporary bridging, `__bridge_retained` when transferring to
CF, and `__bridge_transfer` when transferring from CF to ARC.

## ARC and C Structures

When mixing ARC objects with C structures, explicit memory management is
required for object pointers in structures.

```objectivec
// Struct with object pointers
typedef struct {
    __unsafe_unretained NSString *name;
    NSInteger age;
} PersonStruct;

void structExample(void) {
    PersonStruct person;
    person.name = @"Alice"; // Must use __unsafe_unretained
    person.age = 30;

    NSLog(@"Person: %@, %ld", person.name, (long)person.age);
}

// Better: Use Objective-C class instead
@interface PersonData : NSObject
@property (nonatomic, strong) NSString *name;
@property (nonatomic, assign) NSInteger age;
@end

@implementation PersonData
@end

// Struct with manual memory management
typedef struct PersonStructManual {
    CFStringRef name; // Use CF types for retained ownership
    NSInteger age;
} PersonStructManual;

PersonStructManual createPerson(NSString *name, NSInteger age) {
    PersonStructManual person;
    person.name = CFBridgingRetain(name); // Retain manually
    person.age = age;
    return person;
}

void releasePerson(PersonStructManual person) {
    CFRelease(person.name); // Release manually
}

void manualStructExample(void) {
    PersonStructManual person = createPerson(@"Bob", 25);
    // Use person
    releasePerson(person);
}

// Arrays of objects in structs
typedef struct {
    __unsafe_unretained NSArray *items;
    NSInteger count;
} ContainerStruct;

// Alternative: Use pointer to object
typedef struct {
    void *items; // Bridge to NSArray when needed
    NSInteger count;
} ContainerStructPointer;

void pointerStructExample(void) {
    NSArray *array = @[@1, @2, @3];

    ContainerStructPointer container;
    container.items = (__bridge void *)array;
    container.count = array.count;

    // Retrieve
    NSArray *retrieved = (__bridge NSArray *)container.items;
    NSLog(@"Items: %@", retrieved);
}
```

Avoid storing ARC-managed objects in C structures. Use Objective-C classes or
CF types with manual management instead.

## Autorelease Pools

Autorelease pools manage temporary objects created by convenience methods and
prevent memory buildup in loops.

```objectivec
// Implicit autorelease pool in main
int main(int argc, char *argv[]) {
    @autoreleasepool {
        return UIApplicationMain(argc, argv, nil,
            NSStringFromClass([AppDelegate class]));
    }
}

// Explicit autorelease pools in loops
void processLargeDataset(void) {
    NSArray *items = /* large array */;

    for (id item in items) {
        @autoreleasepool {
            // Temporary objects released each iteration
            NSString *processed = [item description];
            NSData *data = [processed dataUsingEncoding:NSUTF8StringEncoding];
            // data and processed released at end of iteration
        }
    }
}

// Without autorelease pool (memory builds up)
void inefficientLoop(void) {
    for (NSInteger i = 0; i < 1000000; i++) {
        NSString *string = [NSString stringWithFormat:@"Number %ld", (long)i];
        // string not released until end of outer pool
    }
}

// With autorelease pool (memory released each iteration)
void efficientLoop(void) {
    for (NSInteger i = 0; i < 1000000; i++) {
        @autoreleasepool {
            NSString *string = [NSString stringWithFormat:@"Number %ld", (long)i];
            // string released at end of each iteration
        }
    }
}

// Nested autorelease pools
void nestedPools(void) {
    @autoreleasepool {
        NSString *outer = @"outer";

        @autoreleasepool {
            NSString *inner = [NSString stringWithFormat:@"%@ inner", outer];
            // inner released when inner pool drains
        }

        // outer released when outer pool drains
    }
}

// Background thread pools
void backgroundWork(void) {
    dispatch_async(dispatch_get_global_queue(
        DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
        @autoreleasepool {
            // Background work
            NSString *result = [NSString stringWithFormat:@"Result"];
            NSLog(@"%@", result);
        }
    });
}
```

Use explicit autorelease pools in tight loops that create many temporary objects
to prevent memory growth between autorelease pool drains.

## Best Practices

1. **Use weak for delegates and parent references** to break retain cycles in
   common delegation and hierarchical patterns

2. **Apply weak-strong dance in blocks** when capturing self to prevent cycles
   while ensuring safe access during execution

3. **Choose copy for mutable type properties** like NSString and NSArray to
   prevent unexpected mutations by callers

4. **Annotate nullability explicitly** with nullable/nonnull to improve API
   clarity and Swift interoperability

5. **Use autorelease pools in loops** that create temporary objects to prevent
   memory buildup in long-running iterations

6. **Bridge CF types explicitly** with appropriate qualifiers to manage
   ownership transfer between ARC and manual reference counting

7. **Avoid storing objects in C structs** as ARC cannot manage them; use
   Objective-C classes or CF types instead

8. **Check for nil after weak references** as they can become nil at any time
   when the referenced object deallocates

9. **Use NSPointerArray for weak collections** when maintaining collections of
   observers or delegates to prevent cycles

10. **Profile with Instruments** to detect retain cycles, memory leaks, and
    excessive autoreleased object creation

## Common Pitfalls

1. **Creating retain cycles with strong delegates** causes memory leaks; always
   use weak for delegate properties

2. **Capturing self strongly in blocks** without weak creates cycles when blocks
   are stored in properties

3. **Forgetting strong reference in weak-strong dance** allows self to
   deallocate during block execution

4. **Using strong for parent pointers** creates bidirectional strong references
   and prevents deallocation

5. **Not using copy for NSString properties** allows callers to pass mutable
   strings and modify them later

6. **Bridging CF types incorrectly** causes over-releases or leaks depending on
   ownership transfer direction

7. **Storing ARC objects in C structures** leads to premature deallocation or
   crashes as ARC cannot track them

8. **Creating NSTimer without invalidation** retains target strongly and
   prevents deallocation until invalidated

9. **Missing autorelease pools in tight loops** causes memory growth and
   potential crashes from memory pressure

10. **Using unsafe_unretained instead of weak** creates dangling pointers that
    crash when accessed after deallocation

## When to Use This Skill

Use ARC patterns when writing Objective-C code for iOS, macOS, watchOS, or tvOS
to ensure memory-safe applications without manual retain/release calls.

Apply weak references and the weak-strong dance when implementing delegates,
observers, or callbacks that could create retain cycles.

Employ proper bridging when interfacing with Core Foundation, Core Graphics, or
other C-based frameworks that use manual reference counting.

Leverage autorelease pools when processing large datasets, importing data, or
performing other operations that create many temporary objects in loops.

Use appropriate ownership qualifiers when designing public APIs to clearly
communicate memory management expectations to clients.

## Resources

- [Transitioning to ARC Release Notes](<https://developer.apple.com/library/archive/releasenotes/ObjectiveC/RN-TransitioningToARC/>)
- [Advanced Memory Management Programming Guide](<https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/MemoryMgmt/>)
- [Working with Objective-C](<https://developer.apple.com/library/archive/documentation/Swift/Conceptual/BuildingCocoaApps/WorkingWithCocoaDataTypes.html>)
- [Instruments User Guide](<https://developer.apple.com/library/archive/documentation/DeveloperTools/Conceptual/InstrumentsUserGuide/>)
- [Core Foundation Design Concepts](<https://developer.apple.com/library/archive/documentation/CoreFoundation/Conceptual/CFDesignConcepts/>)
