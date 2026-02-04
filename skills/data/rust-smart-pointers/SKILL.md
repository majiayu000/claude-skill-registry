---
name: rust-smart-pointers
description: Smart pointer patterns for Rust (Arc, Rc, RefCell, Cell, OnceLock, Mutex)
---

# rust-smart-pointers

Smart pointers in Rust provide automatic memory management and enable patterns that aren't possible with regular references. They're essential for GPUI applications where ownership crosses async boundaries, callbacks need shared state, and global singletons require thread-safe access.

## Ownership Fundamentals

Rust's ownership rules:
1. Each value has exactly one owner
2. When the owner goes out of scope, the value is dropped
3. References cannot outlive the data they point to

Smart pointers bypass these constraints when needed, at the cost of runtime overhead.

## Box<T> - Heap Allocation

`Box<T>` puts data on the heap instead of the stack. Use when:
- You have a type whose size can't be known at compile time
- You want to transfer ownership without copying large data
- You need a trait object (`Box<dyn Trait>`)

```rust
// Recursive types require Box
enum List {
    Cons(i32, Box<List>),
    Nil,
}

// Trait objects for dynamic dispatch
pub type OnClickCallback = Box<dyn Fn(&ClickEvent, &mut Window, &mut App) + 'static>;
pub type KeyEventCallback = Box<dyn Fn(KeyEvent) + Send + Sync + 'static>;

// Large data transfer without stack copying
fn process_data(data: Box<[u8; 1024 * 1024]>) { /* ... */ }
```

### script-kit-gpui patterns

```rust
// Trait objects for callbacks (one-shot or stored)
pub type OnHoverCallback = Box<dyn Fn(usize, bool) + 'static>;
pub type StreamCallback = Box<dyn Fn(String) + Send + Sync>;

// Dynamic dispatch for platform abstraction
let mut watcher: Box<dyn Watcher> = Box::new(recommended_watcher(/* ... */));
pub fn get_tokens(variant: DesignVariant) -> Box<dyn DesignTokens>;
```

## Rc<T> vs Arc<T> - Reference Counting

Both enable multiple ownership. `Rc` is single-threaded, `Arc` is thread-safe.

### Rc<T> - Single-threaded reference counting

```rust
use std::rc::Rc;

let data = Rc::new(ExpensiveData::new());
let clone1 = Rc::clone(&data);  // Cheap - just increments counter
let clone2 = Rc::clone(&data);

println!("count = {}", Rc::strong_count(&data)); // 3
```

**Use Rc when:**
- Multiple parts of single-threaded code need the same data
- Data doesn't cross thread boundaries (not `Send`)
- You want minimal overhead (no atomic operations)

### Arc<T> - Atomic reference counting

```rust
use std::sync::Arc;
use std::thread;

let data = Arc::new(vec![1, 2, 3]);
for _ in 0..3 {
    let data = Arc::clone(&data);
    thread::spawn(move || {
        println!("{:?}", data);  // Each thread has its own Arc
    });
}
```

**Use Arc when:**
- Data must be shared across threads
- Callbacks need access from async contexts
- Global state needs multiple accessors

### script-kit-gpui patterns

```rust
// GPUI callbacks are often multi-threaded, so Arc is preferred
pub type HotkeyHandler = Arc<dyn Fn() + Send + Sync>;
pub type ActionCallback = Arc<dyn Fn(String) + Send + Sync>;
pub type SubmitCallback = Arc<dyn Fn(String, Option<String>) + Send + Sync>;

// Arc for shared data in render closures (cheap clone during re-render)
cached_grouped_items: Arc<[GroupedListItem]>,
cached_grouped_flat_results: Arc<[scripts::SearchResult]>,

// Arc<Script> to avoid cloning entire Script struct during filtering
pub fn fuzzy_search_scripts(scripts: &[Arc<Script>], query: &str) -> Vec<ScriptMatch>;

// Shared images across multiple list items
clipboard_image_cache: std::collections::HashMap<String, Arc<gpui::RenderImage>>,
```

### Rc in script-kit-gpui (UI components)

```rust
// Rc for single-threaded UI callbacks (GPUI render is single-threaded)
on_primary_click: Option<Rc<FooterClickCallback>>,
on_secondary_click: Option<Rc<FooterClickCallback>>,
on_click: Option<Rc<OnClickCallback>>,
pub callback: Rc<ToastActionCallback>,
```

**Key insight:** Use `Rc` for UI callbacks that never leave the main thread, `Arc` for anything that might cross async/thread boundaries.

## RefCell<T> vs Cell<T> - Interior Mutability

Both allow mutation through shared references. Use when you need to mutate data that's behind an immutable reference.

### Cell<T> - Copy types only

```rust
use std::cell::Cell;

let value = Cell::new(5);
value.set(10);  // No borrow needed
let x = value.get();  // Returns a copy
```

**Limitations:** Only works with `Copy` types (integers, bools, etc.)

### RefCell<T> - Runtime borrow checking

```rust
use std::cell::RefCell;

let data = RefCell::new(vec![1, 2, 3]);

// Immutable borrow
println!("{:?}", data.borrow());

// Mutable borrow
data.borrow_mut().push(4);

// PANICS if borrowed mutably while already borrowed!
let r1 = data.borrow();
let r2 = data.borrow_mut();  // PANIC: already borrowed
```

**Use when:**
- You need interior mutability in single-threaded code
- Ownership patterns make compile-time borrowing impossible
- You're sure borrows won't overlap (or use `try_borrow`)

### script-kit-gpui usage

RefCell is rare in script-kit-gpui because most shared state crosses thread boundaries. The codebase prefers `Mutex` for interior mutability.

## Mutex<T> vs RwLock<T> - Thread-Safe Interior Mutability

### Mutex<T> - Exclusive access

```rust
use std::sync::Mutex;

let data = Mutex::new(vec![1, 2, 3]);

// Lock, mutate, auto-unlock when guard drops
{
    let mut guard = data.lock().unwrap();
    guard.push(4);
}  // Lock released here

// Poisoning: if a thread panics while holding the lock,
// subsequent lock() calls return Err (the mutex is "poisoned")
```

### RwLock<T> - Multiple readers OR single writer

```rust
use std::sync::RwLock;

let data = RwLock::new(vec![1, 2, 3]);

// Multiple readers allowed simultaneously
let r1 = data.read().unwrap();
let r2 = data.read().unwrap();  // OK!

// Writers get exclusive access
drop(r1); drop(r2);
let mut w = data.write().unwrap();
w.push(4);
```

**Use RwLock when:** Reads vastly outnumber writes.

### parking_lot alternatives

script-kit-gpui uses `parking_lot::Mutex` in some places:

```rust
use parking_lot::Mutex as ParkingMutex;

// Benefits over std::sync::Mutex:
// 1. Never poisons on panic
// 2. Smaller size (1 byte vs word-sized)
// 3. Slightly faster

type SharedSession = Arc<ParkingMutex<Option<executor::ScriptSession>>>;
```

### script-kit-gpui patterns

```rust
// Thread-safe mutable state for callbacks
pending_path_action: Arc<Mutex<Option<PathInfo>>>,
close_path_actions: Arc<Mutex<bool>>,
path_actions_showing: Arc<Mutex<bool>>,

// Scheduler with thread-safe script list
pub struct Scheduler {
    scripts: Arc<Mutex<Vec<ScheduledScript>>>,
    running: Arc<Mutex<bool>>,
}

// RwLock for read-heavy hotkey routes
static HOTKEY_ROUTES: OnceLock<RwLock<HotkeyRoutes>> = OnceLock::new();

// Process manager with RwLock for frequent reads
pub struct ProcessManager {
    active_processes: RwLock<HashMap<u32, ProcessInfo>>,
}
```

## OnceLock / LazyLock - Lazy Initialization

### OnceLock - Initialize once, read forever

```rust
use std::sync::OnceLock;

static CONFIG: OnceLock<Config> = OnceLock::new();

fn get_config() -> &'static Config {
    CONFIG.get_or_init(|| {
        // Expensive initialization runs exactly once
        Config::load_from_file()
    })
}
```

### LazyLock - Lazy with closure

```rust
use std::sync::LazyLock;

// Initialization closure is part of the type
static REGEX: LazyLock<Regex> = LazyLock::new(|| {
    Regex::new(r"^https?://").unwrap()
});
```

### script-kit-gpui patterns (OnceLock is dominant)

```rust
// Global singletons with OnceLock<Mutex<T>>
static WINDOW_MANAGER: OnceLock<Mutex<WindowManager>> = OnceLock::new();
static HUD_MANAGER: OnceLock<Arc<Mutex<HudManagerState>>> = OnceLock::new();
static HOTKEY_ROUTES: OnceLock<RwLock<HotkeyRoutes>> = OnceLock::new();

// Database connections
static AI_DB: OnceLock<Arc<Mutex<Connection>>> = OnceLock::new();
static NOTES_DB: OnceLock<Arc<Mutex<Connection>>> = OnceLock::new();
static DB_CONNECTION: OnceLock<Arc<Mutex<Connection>>> = OnceLock::new();

// Async channels
static HOTKEY_CHANNEL: OnceLock<(Sender<()>, Receiver<()>)> = OnceLock::new();

// SDK extraction flag
static SDK_EXTRACTED: OnceLock<Option<PathBuf>> = OnceLock::new();

// LazyLock for regex patterns
static URL_REGEX: LazyLock<Regex> = LazyLock::new(|| {
    Regex::new(r"^(https?://|file://)[^\s]+$").expect("Invalid URL regex")
});
```

**Pattern:** `OnceLock<Mutex<T>>` is the standard pattern for global mutable singletons.

## Combining Smart Pointers

### Arc<Mutex<T>> - Shared mutable state across threads

The most common pattern for thread-safe shared state:

```rust
// Multiple threads can clone the Arc and lock the Mutex
let state = Arc::new(Mutex::new(AppState::new()));

let state_clone = Arc::clone(&state);
thread::spawn(move || {
    let mut guard = state_clone.lock().unwrap();
    guard.update();
});
```

### Arc<RwLock<T>> - Read-heavy shared state

```rust
static SPACE_MANAGER: RwLock<Option<Arc<dyn SpaceManager>>> = RwLock::new(None);
```

### Rc<RefCell<T>> - Single-threaded shared mutable state

```rust
// Not used in script-kit-gpui (prefers Arc<Mutex<T>>)
let data = Rc::new(RefCell::new(Vec::new()));
let clone = Rc::clone(&data);
clone.borrow_mut().push(1);
```

### script-kit-gpui combining patterns

```rust
// The canonical pattern: OnceLock + Arc + Mutex
static HUD_MANAGER: OnceLock<Arc<Mutex<HudManagerState>>> = OnceLock::new();

fn get_hud_manager() -> &'static Arc<Mutex<HudManagerState>> {
    HUD_MANAGER.get_or_init(|| Arc::new(Mutex::new(HudManagerState::default())))
}

// OnceLock + Mutex (when Arc not needed)
static WINDOW_MANAGER: OnceLock<Mutex<WindowManager>> = OnceLock::new();

fn get_manager() -> &'static Mutex<WindowManager> {
    WINDOW_MANAGER.get_or_init(|| Mutex::new(WindowManager::new()))
}

// Arc<[T]> for immutable shared slices (cheap clone in render)
cached_grouped_items: Arc<[GroupedListItem]>,
```

## Anti-patterns and Common Mistakes

### 1. Deadlocks from nested locks

```rust
// DEADLOCK: Locking same mutex twice
let data = Arc::new(Mutex::new(0));
let guard1 = data.lock().unwrap();
let guard2 = data.lock().unwrap();  // Blocks forever!

// FIX: Drop the first guard before re-locking
let data = Arc::new(Mutex::new(0));
{
    let guard = data.lock().unwrap();
    // use guard
}  // guard dropped
{
    let guard = data.lock().unwrap();  // OK
}
```

### 2. Holding locks across await points

```rust
// BAD: Lock held across .await
async fn bad_example(data: Arc<Mutex<Vec<u8>>>) {
    let mut guard = data.lock().unwrap();
    do_async_work().await;  // Lock held during await!
    guard.push(1);
}

// GOOD: Lock, copy, unlock, then await
async fn good_example(data: Arc<Mutex<Vec<u8>>>) {
    let value = {
        let guard = data.lock().unwrap();
        guard.clone()  // Copy the data
    };  // Lock released
    do_async_work().await;
    data.lock().unwrap().push(1);
}
```

### 3. RefCell borrow panics

```rust
// PANIC: Overlapping borrows
let data = RefCell::new(vec![1, 2, 3]);
let r = data.borrow();
data.borrow_mut().push(4);  // PANIC!

// FIX: Use try_borrow_mut or ensure no overlap
let data = RefCell::new(vec![1, 2, 3]);
if let Ok(mut r) = data.try_borrow_mut() {
    r.push(4);
}
```

### 4. Unnecessary Arc cloning

```rust
// BAD: Clone Arc when you could borrow
fn process(data: Arc<Vec<u8>>) {
    for item in data.iter() {  // OK, but Arc clone was unnecessary
        println!("{}", item);
    }
}

// GOOD: Borrow when you don't need ownership
fn process(data: &[u8]) {
    for item in data.iter() {
        println!("{}", item);
    }
}

// BUT: Arc clone IS needed for closures that outlive the call
let data = Arc::new(vec![1, 2, 3]);
let data_clone = Arc::clone(&data);  // Necessary for move
button.on_click(move || {
    println!("{:?}", data_clone);
});
```

### 5. Using Rc when Arc is needed

```rust
// COMPILE ERROR: Rc is not Send
let data = Rc::new(vec![1, 2, 3]);
thread::spawn(move || {  // ERROR: Rc<Vec<i32>> cannot be sent between threads
    println!("{:?}", data);
});

// FIX: Use Arc for cross-thread sharing
let data = Arc::new(vec![1, 2, 3]);
thread::spawn(move || {
    println!("{:?}", data);  // OK
});
```

### 6. Mutex poisoning surprises

```rust
// Panic in one thread poisons the mutex
let data = Arc::new(Mutex::new(vec![]));
let d = Arc::clone(&data);
thread::spawn(move || {
    let _guard = d.lock().unwrap();
    panic!("oops");  // Mutex is now poisoned
}).join().ok();

// Subsequent locks return Err
let result = data.lock();  // Err(PoisonError)

// Options:
// 1. Use parking_lot::Mutex (never poisons)
// 2. Use into_inner() to recover: result.unwrap_or_else(|e| e.into_inner())
```

## Decision Tree

```
Need heap allocation for unsized/recursive type?
  YES -> Box<T>
  NO  -> Continue

Need multiple owners?
  NO  -> Use regular ownership or references
  YES -> Continue

Will data cross thread boundaries?
  NO  -> Rc<T> (single-threaded)
  YES -> Arc<T> (thread-safe)

Need interior mutability?
  NO  -> You're done with Rc/Arc
  YES -> Continue

Is it single-threaded?
  YES -> RefCell<T> (with Rc) or Cell<T> for Copy types
  NO  -> Continue

Is it read-heavy?
  YES -> RwLock<T>
  NO  -> Mutex<T>

Need lazy initialization?
  YES -> OnceLock<T> or LazyLock<T>

Common combinations:
- Arc<Mutex<T>> - shared mutable state across threads
- OnceLock<Mutex<T>> - global singleton
- OnceLock<Arc<Mutex<T>>> - global singleton that's also cloneable
- Arc<[T]> - shared immutable slice (cheap clone)
```

## Quick Reference

| Type | Thread-safe | Multiple owners | Mutable | Use case |
|------|-------------|-----------------|---------|----------|
| `Box<T>` | Yes* | No | Yes (if owned) | Heap allocation, trait objects |
| `Rc<T>` | No | Yes | No | Single-threaded sharing |
| `Arc<T>` | Yes | Yes | No | Multi-threaded sharing |
| `Cell<T>` | No | N/A | Yes | Interior mut for Copy types |
| `RefCell<T>` | No | N/A | Yes | Interior mut, runtime borrow check |
| `Mutex<T>` | Yes | N/A | Yes | Thread-safe interior mut |
| `RwLock<T>` | Yes | N/A | Yes | Read-heavy thread-safe mut |
| `OnceLock<T>` | Yes | N/A | No (after init) | One-time initialization |
| `LazyLock<T>` | Yes | N/A | No (after init) | Lazy one-time init with closure |

*Box is Send + Sync if T is Send + Sync
