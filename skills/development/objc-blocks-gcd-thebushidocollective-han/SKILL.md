---
name: Objective-C Blocks and GCD
description: Use when blocks (closures) and Grand Central Dispatch in Objective-C for concurrent programming including block syntax, capture semantics, dispatch queues, dispatch groups, and patterns for thread-safe asynchronous code.
allowed-tools: []
---

# Objective-C Blocks and GCD

## Introduction

Blocks are Objective-C's closure implementation, providing anonymous functions
that capture surrounding context. Grand Central Dispatch (GCD) is Apple's
low-level API for managing concurrent operations using dispatch queues rather
than threads directly.

Blocks enable functional programming patterns, callbacks, and clean asynchronous
API design. GCD simplifies concurrency by abstracting thread management into
queues that automatically distribute work across available CPU cores. Together,
they form the foundation for modern Objective-C concurrent programming.

This skill covers block syntax and semantics, capture behavior, GCD queues and
dispatch functions, synchronization primitives, and patterns for safe concurrent
code.

## Block Syntax and Usage

Blocks are first-class objects that encapsulate code and can capture variables
from their defining scope.

```objectivec
// Basic block syntax
void (^simpleBlock)(void) = ^{
    NSLog(@"Hello from block");
};
simpleBlock(); // Call block

// Block with parameters
int (^addBlock)(int, int) = ^(int a, int b) {
    return a + b;
};
int result = addBlock(5, 3); // 8

// Block with return type
NSString *(^greetBlock)(NSString *) = ^NSString *(NSString *name) {
    return [NSString stringWithFormat:@"Hello, %@", name];
};
NSString *greeting = greetBlock(@"Alice");

// Blocks as method parameters
- (void)fetchDataWithCompletion:
    (void (^)(NSData *data, NSError *error))completion {
    dispatch_async(dispatch_get_global_queue(
        DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
        // Simulate network call
        NSData *data = [@"response" dataUsingEncoding:NSUTF8StringEncoding];

        dispatch_async(dispatch_get_main_queue(), ^{
            if (completion) {
                completion(data, nil);
            }
        });
    });
}

// Using block-based API
- (void)loadData {
    [self fetchDataWithCompletion:^(NSData *data, NSError *error) {
        if (error) {
            NSLog(@"Error: %@", error);
        } else {
            NSLog(@"Data: %@", data);
        }
    }];
}

// Typedef for block types
typedef void (^CompletionBlock)(BOOL success);
typedef void (^DataBlock)(NSData *data, NSError *error);
typedef NSString *(^TransformBlock)(NSString *input);

- (void)performOperationWithCompletion:(CompletionBlock)completion {
    // Async operation
    dispatch_async(dispatch_get_global_queue(
        DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
        // Work
        BOOL success = YES;

        dispatch_async(dispatch_get_main_queue(), ^{
            if (completion) {
                completion(success);
            }
        });
    });
}

// Blocks in collections
NSArray *blocks = @[
    ^{ NSLog(@"Block 1"); },
    ^{ NSLog(@"Block 2"); },
    ^{ NSLog(@"Block 3"); }
];

for (void (^block)(void) in blocks) {
    block();
}

// Block properties
@interface AsyncOperation : NSObject
@property (nonatomic, copy) CompletionBlock completion;
@property (nonatomic, copy) DataBlock dataHandler;
@end

@implementation AsyncOperation
@end
```

Blocks must be copied when stored in properties or collections to move them from
stack to heap storage.

## Block Capture Semantics

Blocks capture variables from their defining scope, with different behaviors for
different storage types and qualifiers.

```objectivec
// Capturing local variables
void captureExample(void) {
    NSInteger x = 10;

    void (^block)(void) = ^{
        NSLog(@"x = %ld", (long)x); // Captures value of x
    };

    x = 20;
    block(); // Prints "x = 10" (captured at block creation)
}

// __block qualifier for mutable capture
void mutableCaptureExample(void) {
    __block NSInteger counter = 0;

    void (^incrementBlock)(void) = ^{
        counter++; // Can modify counter
    };

    incrementBlock();
    incrementBlock();
    NSLog(@"Counter: %ld", (long)counter); // 2
}

// Capturing self in methods
@interface Counter : NSObject
@property (nonatomic, assign) NSInteger count;
- (void)incrementAsync;
@end

@implementation Counter

- (void)incrementAsync {
    // Strong capture of self
    dispatch_async(dispatch_get_global_queue(
        DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
        self.count++; // Captures self strongly
    });
}

@end

// Weak-strong dance for self
@interface ViewController : UIViewController
@property (nonatomic, strong) NSTimer *timer;
@end

@implementation ViewController

- (void)startTimer {
    __weak typeof(self) weakSelf = self;

    self.timer = [NSTimer scheduledTimerWithTimeInterval:1.0
                                                 repeats:YES
                                                   block:^(NSTimer *timer) {
        __strong typeof(weakSelf) strongSelf = weakSelf;
        if (!strongSelf) return;

        // Safe to use strongSelf
        [strongSelf updateUI];
    }];
}

- (void)updateUI {
    NSLog(@"Updating UI");
}

- (void)dealloc {
    [self.timer invalidate];
}

@end

// Capturing objects vs primitives
void objectCaptureExample(void) {
    NSMutableString *string = [NSMutableString stringWithString:@"Hello"];

    void (^block)(void) = ^{
        [string appendString:@" World"]; // Can mutate object
        NSLog(@"%@", string);
    };

    block(); // Prints "Hello World"
}

// Block retain cycles
@interface NetworkManager : NSObject
@property (nonatomic, copy) void (^completion)(NSData *data);
@end

@implementation NetworkManager

- (void)fetchData {
    __weak typeof(self) weakSelf = self;

    self.completion = ^(NSData *data) {
        __strong typeof(weakSelf) strongSelf = weakSelf;
        if (!strongSelf) return;

        [strongSelf processData:data];
    };
}

- (void)processData:(NSData *)data {
    NSLog(@"Processing: %@", data);
}

@end

// Capturing __block objects
void blockObjectExample(void) {
    __block NSMutableArray *array = [NSMutableArray array];

    void (^addBlock)(id) = ^(id object) {
        [array addObject:object]; // Can mutate and reassign
    };

    addBlock(@"Item 1");
    addBlock(@"Item 2");

    array = [NSMutableArray array]; // Can reassign
}
```

Use `__weak` to avoid retain cycles when capturing self, and `__block` to allow
mutation of captured variables.

## Dispatch Queues

GCD uses dispatch queues to manage concurrent execution, with serial queues
executing tasks sequentially and concurrent queues executing them in parallel.

```objectivec
// Main queue (serial, main thread)
dispatch_async(dispatch_get_main_queue(), ^{
    // Update UI
    NSLog(@"On main thread");
});

// Global concurrent queues
dispatch_queue_t highPriorityQueue = dispatch_get_global_queue(
    DISPATCH_QUEUE_PRIORITY_HIGH, 0);
dispatch_queue_t defaultQueue = dispatch_get_global_queue(
    DISPATCH_QUEUE_PRIORITY_DEFAULT, 0);
dispatch_queue_t lowPriorityQueue = dispatch_get_global_queue(
    DISPATCH_QUEUE_PRIORITY_LOW, 0);
dispatch_queue_t backgroundQueue = dispatch_get_global_queue(
    DISPATCH_QUEUE_PRIORITY_BACKGROUND, 0);

// Async execution on global queue
dispatch_async(defaultQueue, ^{
    // Background work
    NSLog(@"Background work");

    dispatch_async(dispatch_get_main_queue(), ^{
        // Update UI on main queue
        NSLog(@"UI update");
    });
});

// Custom serial queue
dispatch_queue_t serialQueue = dispatch_queue_create("com.example.serial", DISPATCH_QUEUE_SERIAL);

dispatch_async(serialQueue, ^{
    NSLog(@"Task 1");
});

dispatch_async(serialQueue, ^{
    NSLog(@"Task 2");
});

// Custom concurrent queue
dispatch_queue_t concurrentQueue = dispatch_queue_create(
    "com.example.concurrent", DISPATCH_QUEUE_CONCURRENT);

dispatch_async(concurrentQueue, ^{
    NSLog(@"Concurrent task 1");
});

dispatch_async(concurrentQueue, ^{
    NSLog(@"Concurrent task 2");
});

// Synchronous dispatch (blocks until complete)
__block NSString *result;
dispatch_sync(serialQueue, ^{
    result = @"Computed value";
});
NSLog(@"Result: %@", result);

// Dispatch after (delayed execution)
dispatch_after(dispatch_time(DISPATCH_TIME_NOW, 2 * NSEC_PER_SEC),
               dispatch_get_main_queue(), ^{
    NSLog(@"Executed after 2 seconds");
});

// Dispatch once (thread-safe singleton)
+ (instancetype)sharedInstance {
    static id sharedInstance = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        sharedInstance = [[self alloc] init];
    });
    return sharedInstance;
}

// Quality of service (iOS 8+)
dispatch_queue_t userInitiatedQueue = dispatch_get_global_queue(
    QOS_CLASS_USER_INITIATED, 0);
dispatch_queue_t utilityQueue = dispatch_get_global_queue(QOS_CLASS_UTILITY, 0);

dispatch_async(userInitiatedQueue, ^{
    // User-initiated work (high priority)
});
```

Use main queue for UI updates, global queues for background work, and custom
queues for synchronization and ordered execution.

## Dispatch Groups

Dispatch groups coordinate multiple async operations, notifying when all tasks
complete.

```objectivec
// Basic dispatch group
dispatch_group_t group = dispatch_group_create();
dispatch_queue_t queue = dispatch_get_global_queue(
    DISPATCH_QUEUE_PRIORITY_DEFAULT, 0);

dispatch_group_async(group, queue, ^{
    NSLog(@"Task 1");
});

dispatch_group_async(group, queue, ^{
    NSLog(@"Task 2");
});

dispatch_group_async(group, queue, ^{
    NSLog(@"Task 3");
});

dispatch_group_notify(group, dispatch_get_main_queue(), ^{
    NSLog(@"All tasks complete");
});

// Waiting for group completion
dispatch_group_wait(group, DISPATCH_TIME_FOREVER);
NSLog(@"After wait");

// Manual enter/leave
dispatch_group_t manualGroup = dispatch_group_create();

dispatch_group_enter(manualGroup);
[self fetchDataWithCompletion:^(NSData *data, NSError *error) {
    NSLog(@"Data fetched");
    dispatch_group_leave(manualGroup);
}];

dispatch_group_enter(manualGroup);
[self fetchImageWithCompletion:^(UIImage *image, NSError *error) {
    NSLog(@"Image fetched");
    dispatch_group_leave(manualGroup);
}];

dispatch_group_notify(manualGroup, dispatch_get_main_queue(), ^{
    NSLog(@"All fetches complete");
});

// Practical example: loading multiple resources
- (void)loadAllResources {
    dispatch_group_t resourceGroup = dispatch_group_create();
    __block NSData *userData = nil;
    __block NSData *settingsData = nil;
    __block UIImage *profileImage = nil;

    dispatch_group_enter(resourceGroup);
    [self fetchUserDataWithCompletion:^(NSData *data) {
        userData = data;
        dispatch_group_leave(resourceGroup);
    }];

    dispatch_group_enter(resourceGroup);
    [self fetchSettingsWithCompletion:^(NSData *data) {
        settingsData = data;
        dispatch_group_leave(resourceGroup);
    }];

    dispatch_group_enter(resourceGroup);
    [self fetchProfileImageWithCompletion:^(UIImage *image) {
        profileImage = image;
        dispatch_group_leave(resourceGroup);
    }];

    dispatch_group_notify(resourceGroup, dispatch_get_main_queue(), ^{
        // All resources loaded
        [self updateUIWithUser:userData settings:settingsData image:profileImage];
    });
}

- (void)fetchUserDataWithCompletion:(void (^)(NSData *))completion {
    dispatch_async(dispatch_get_global_queue(
        DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
        if (completion) completion([NSData data]);
    });
}

- (void)fetchSettingsWithCompletion:(void (^)(NSData *))completion {
    dispatch_async(dispatch_get_global_queue(
        DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
        if (completion) completion([NSData data]);
    });
}

- (void)fetchProfileImageWithCompletion:(void (^)(UIImage *))completion {
    dispatch_async(dispatch_get_global_queue(
        DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
        if (completion) completion([[UIImage alloc] init]);
    });
}

- (void)updateUIWithUser:(NSData *)user settings:(NSData *)settings
                   image:(UIImage *)image {
    NSLog(@"Updating UI with all resources");
}
```

Dispatch groups are essential for coordinating multiple async operations and
ensuring all complete before proceeding.

## Dispatch Barriers and Synchronization

Barriers provide synchronized access to shared resources in concurrent queues.

```objectivec
// Dispatch barrier for reader-writer pattern
@interface ThreadSafeCache : NSObject
@property (nonatomic, strong) dispatch_queue_t concurrentQueue;
@property (nonatomic, strong) NSMutableDictionary *cache;
@end

@implementation ThreadSafeCache

- (instancetype)init {
    self = [super init];
    if (self) {
        self.concurrentQueue = dispatch_queue_create(
            "com.example.cache",
            DISPATCH_QUEUE_CONCURRENT
        );
        self.cache = [NSMutableDictionary dictionary];
    }
    return self;
}

// Multiple readers allowed
- (id)objectForKey:(NSString *)key {
    __block id object;
    dispatch_sync(self.concurrentQueue, ^{
        object = self.cache[key];
    });
    return object;
}

// Exclusive writer with barrier
- (void)setObject:(id)object forKey:(NSString *)key {
    dispatch_barrier_async(self.concurrentQueue, ^{
        self.cache[key] = object;
    });
}

// Synchronous barrier write
- (void)setObjectSync:(id)object forKey:(NSString *)key {
    dispatch_barrier_sync(self.concurrentQueue, ^{
        self.cache[key] = object;
    });
}

@end

// Semaphores for limiting concurrency
- (void)downloadImagesWithLimit:(NSArray<NSURL *> *)urls {
    dispatch_semaphore_t semaphore = dispatch_semaphore_create(3);
    // Max 3 concurrent
    dispatch_queue_t queue = dispatch_get_global_queue(
        DISPATCH_QUEUE_PRIORITY_DEFAULT, 0);

    for (NSURL *url in urls) {
        dispatch_async(queue, ^{
            dispatch_semaphore_wait(semaphore, DISPATCH_TIME_FOREVER);

            // Download image
            NSLog(@"Downloading: %@", url);
            [NSThread sleepForTimeInterval:1.0]; // Simulate download

            dispatch_semaphore_signal(semaphore);
        });
    }
}

// Dispatch apply for parallel loops
- (void)processItems:(NSArray *)items {
    dispatch_apply(items.count, dispatch_get_global_queue(
        DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^(size_t index) {
        id item = items[index];
        NSLog(@"Processing item %zu: %@", index, item);
        // Process item in parallel
    });
}

// Mutex alternative with dispatch_sync
@interface Counter2 : NSObject
@property (nonatomic, strong) dispatch_queue_t syncQueue;
@property (nonatomic, assign) NSInteger count;
@end

@implementation Counter2

- (instancetype)init {
    self = [super init];
    if (self) {
        self.syncQueue = dispatch_queue_create("com.example.counter", DISPATCH_QUEUE_SERIAL);
        self.count = 0;
    }
    return self;
}

- (void)increment {
    dispatch_sync(self.syncQueue, ^{
        self.count++;
    });
}

- (NSInteger)currentCount {
    __block NSInteger value;
    dispatch_sync(self.syncQueue, ^{
        value = self.count;
    });
    return value;
}

@end
```

Barriers ensure exclusive write access while allowing concurrent reads, ideal
for thread-safe caches and data structures.

## Block-Based APIs

Modern Cocoa APIs extensively use blocks for callbacks, providing cleaner
alternatives to delegate patterns.

```objectivec
// NSURLSession with blocks
- (void)fetchURL:(NSURL *)url {
    NSURLSession *session = [NSURLSession sharedSession];

    NSURLSessionDataTask *task = [session dataTaskWithURL:url
        completionHandler:^(NSData *data, NSURLResponse *response,
                            NSError *error) {
        if (error) {
            NSLog(@"Error: %@", error);
            return;
        }

        dispatch_async(dispatch_get_main_queue(), ^{
            // Process data on main thread
            NSLog(@"Data received: %@", data);
        });
    }];

    [task resume];
}

// UIView animations with blocks
- (void)animateView:(UIView *)view {
    [UIView animateWithDuration:0.3
                     animations:^{
        view.alpha = 0.0;
        view.transform = CGAffineTransformMakeScale(0.5, 0.5);
    } completion:^(BOOL finished) {
        if (finished) {
            [view removeFromSuperview];
        }
    }];
}

// NSNotificationCenter with blocks
- (void)observeNotifications {
    id observer = [[NSNotificationCenter defaultCenter]
        addObserverForName:UIApplicationDidEnterBackgroundNotification
                    object:nil
                     queue:[NSOperationQueue mainQueue]
                usingBlock:^(NSNotification *note) {
        NSLog(@"App entered background");
    }];

    // Store observer to remove later
}

// Custom block-based API
typedef void (^ProgressBlock)(CGFloat progress);
typedef void (^CompletionBlock2)(BOOL success, NSError *error);

@interface Downloader : NSObject
- (void)downloadFile:(NSURL *)url
            progress:(ProgressBlock)progress
          completion:(CompletionBlock2)completion;
@end

@implementation Downloader

- (void)downloadFile:(NSURL *)url
            progress:(ProgressBlock)progress
          completion:(CompletionBlock2)completion {
    dispatch_async(dispatch_get_global_queue(
        DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
        // Simulate download with progress
        for (NSInteger i = 0; i <= 100; i += 10) {
            [NSThread sleepForTimeInterval:0.1];

            dispatch_async(dispatch_get_main_queue(), ^{
                if (progress) {
                    progress(i / 100.0);
                }
            });
        }

        dispatch_async(dispatch_get_main_queue(), ^{
            if (completion) {
                completion(YES, nil);
            }
        });
    });
}

@end

// Using custom block API
- (void)downloadExample {
    Downloader *downloader = [[Downloader alloc] init];
    NSURL *url = [NSURL URLWithString:@"https://example.com/file.zip"];

    [downloader downloadFile:url
                    progress:^(CGFloat progress) {
        NSLog(@"Progress: %.0f%%", progress * 100);
    } completion:^(BOOL success, NSError *error) {
        if (success) {
            NSLog(@"Download complete");
        } else {
            NSLog(@"Download failed: %@", error);
        }
    }];
}
```

Block-based APIs provide inline callback handling without the boilerplate of
delegation or notification observers.

## Best Practices

1. **Copy blocks when storing in properties** to move them from stack to heap
   and prevent crashes from dangling pointers

2. **Use weak-strong dance for self capture** in blocks stored as properties to
   break retain cycles

3. **Dispatch UI updates to main queue** using dispatch_async to ensure
   thread-safe UI modifications

4. **Prefer dispatch groups over nested callbacks** to coordinate multiple async
   operations cleanly

5. **Use dispatch barriers for reader-writer patterns** to allow concurrent
   reads while ensuring exclusive writes

6. **Create custom queues for synchronization** rather than using global queues
   to avoid contention and priority issues

7. **Check for nil before calling blocks** to prevent crashes from unimplemented
   optional block parameters

8. **Use dispatch_once for thread-safe singletons** to ensure exactly-once
   initialization without locks

9. **Limit concurrency with semaphores** when accessing rate-limited resources
   like network connections

10. **Profile with Instruments** to identify queue contention, thread explosion,
    and performance bottlenecks

## Common Pitfalls

1. **Creating retain cycles with strong self capture** in blocks stored as
   properties causes memory leaks

2. **Not copying blocks when storing them** leads to crashes when stack-allocated
   blocks go out of scope

3. **Using dispatch_sync on current queue** causes deadlock; never sync dispatch
   to the queue you're on

4. **Forgetting to dispatch to main queue** for UI updates causes crashes or
   undefined behavior

5. **Overusing dispatch_sync** blocks threads unnecessarily; prefer async
   dispatch for better performance

6. **Not balancing dispatch_group_enter/leave** causes group notifications to
   never fire or fire prematurely

7. **Accessing mutable state without synchronization** from multiple queues
   causes race conditions and data corruption

8. **Creating too many custom queues** wastes resources; reuse queues where
   appropriate

9. **Using global queues for barriers** doesn't work as barriers require custom
   concurrent queues

10. **Blocking in weak-strong dance** without nil check can cause crashes if
    weakSelf becomes nil during execution

## When to Use This Skill

Use blocks and GCD when building iOS, macOS, watchOS, or tvOS applications that
require asynchronous operations, concurrent processing, or callback-based APIs.

Apply dispatch queues for background processing, network calls, file I/O, or any
operation that shouldn't block the main thread.

Employ dispatch groups when coordinating multiple async operations that must all
complete before proceeding, like loading multiple resources.

Leverage dispatch barriers for thread-safe data structures that support
concurrent reads and exclusive writes.

Use block-based APIs when designing modern Objective-C interfaces that provide
inline callback handling without delegate boilerplate.

## Resources

- [Blocks Programming Topics](<https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/Blocks/>)
- [Concurrency Programming Guide](<https://developer.apple.com/library/archive/documentation/General/Conceptual/ConcurrencyProgrammingGuide/>)
- [Grand Central Dispatch Tutorial](<https://www.raywenderlich.com/5370-grand-central-dispatch-tutorial-for-swift-4-part-1-2>)
- [Dispatch Framework Documentation](<https://developer.apple.com/documentation/dispatch>)
- [NSHipster on Blocks](<https://nshipster.com/blocks/>)
