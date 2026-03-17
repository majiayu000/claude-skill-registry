---
name: parking-lot
description: Fast, non-poisoning synchronization primitives
---

# parking-lot

Fast, compact synchronization primitives that replace `std::sync`. Use when you need:
- Smaller memory footprint (1 byte for Mutex, 1 byte for RwLock)
- No lock poisoning (simpler error handling)
- Better performance under contention
- Fair locking options
- Optional deadlock detection

## Key Types

### Mutex<T>
Mutual exclusion lock. 1 byte overhead vs 40+ bytes for std.

```rust
use parking_lot::Mutex;

// Create - can be const-initialized (unlike std::sync::Mutex)
static GLOBAL: Mutex<Vec<String>> = Mutex::new(Vec::new());

// Or at runtime
let lock = Mutex::new(42);

// Lock - no .unwrap() needed (no poisoning!)
let mut guard = lock.lock();
*guard += 1;
// Guard auto-drops, releasing lock
```

### RwLock<T>
Reader-writer lock. Multiple readers OR one writer.

```rust
use parking_lot::RwLock;

let lock = RwLock::new(HashMap::new());

// Multiple readers allowed
let data = lock.read();
println!("{:?}", data.get("key"));

// Single writer (exclusive)
let mut data = lock.write();
data.insert("key", "value");
```

### Condvar
Condition variable for thread coordination.

```rust
use parking_lot::{Mutex, Condvar};

let pair = (Mutex::new(false), Condvar::new());
let (lock, cvar) = &pair;

// Waiting thread
let mut ready = lock.lock();
while !*ready {
    cvar.wait(&mut ready);
}

// Signaling thread
*lock.lock() = true;
cvar.notify_one();
```

### Once
One-time initialization (like std::sync::Once).

```rust
use parking_lot::Once;

static INIT: Once = Once::new();

INIT.call_once(|| {
    // Expensive initialization - runs exactly once
});
```

### ReentrantMutex<T>
Can be locked multiple times by the same thread.

```rust
use parking_lot::ReentrantMutex;

let lock = ReentrantMutex::new(42);
let guard1 = lock.lock();
let guard2 = lock.lock(); // OK - same thread
```

### FairMutex<T>
FIFO ordering for lock acquisition.

```rust
use parking_lot::FairMutex;

let lock = FairMutex::new(data);
// Threads acquire in the order they requested
```

## Usage in script-kit-gpui

### Shared Session State (main.rs)
```rust
use parking_lot::Mutex as ParkingMutex;

/// Wrapper to hold a script session that can be shared across async boundaries
/// Uses parking_lot::Mutex which doesn't poison on panic, avoiding .unwrap() calls
type SharedSession = Arc<ParkingMutex<Option<executor::ScriptSession>>>;
```

**Why**: ScriptSession is held across async boundaries and thread panics. Non-poisoning Mutex means no error handling bloat - just `.lock()` directly.

### HUD Manager (hud_manager.rs)
```rust
use parking_lot::Mutex;

static HUD_MANAGER: OnceLock<Arc<Mutex<HudManagerState>>> = OnceLock::new();

fn get_hud_manager() -> &'static Arc<Mutex<HudManagerState>> {
    HUD_MANAGER.get_or_init(|| Arc::new(Mutex::new(HudManagerState::new())))
}

// Usage - clean, no .unwrap()
let state = manager.lock();
let slot = state.first_free_slot();
```

**Why**: Global singleton pattern. No poisoning = cleaner access patterns.

### Frontmost App Tracker (frontmost_app_tracker.rs)
```rust
use parking_lot::RwLock;

static TRACKER_STATE: LazyLock<RwLock<TrackerState>> =
    LazyLock::new(|| RwLock::new(TrackerState::default()));

// Read access (frequent)
pub fn get_last_real_app() -> Option<TrackedApp> {
    TRACKER_STATE.read().last_real_app.clone()
}

// Write access (rare)
let mut state = TRACKER_STATE.write();
state.last_real_app = Some(tracked.clone());
```

**Why**: RwLock for read-heavy workload. App tracking is read frequently (every keystroke) but written rarely (app switch).

## vs std::sync

| Feature | parking_lot | std::sync |
|---------|-------------|-----------|
| Mutex size | 1 byte | 40+ bytes |
| RwLock size | 1 byte | 48+ bytes |
| Lock poisoning | No | Yes |
| const new() | Yes | Unstable |
| Fair locking | FairMutex | No |
| Deadlock detection | Optional | No |
| try_lock_for() | Yes | No |
| Upgradable reads | Yes | No |

### No Poisoning - Why It Matters

```rust
// std::sync - must handle poison
let guard = mutex.lock().unwrap(); // or expect()
// If any thread panicked while holding, this panics

// parking_lot - no poison to handle
let guard = mutex.lock(); // That's it
// If a thread panicked, lock is simply released
```

**Philosophy**: Lock poisoning "protects" against corrupted state, but in practice:
1. Most panics don't corrupt shared state
2. You usually want to crash anyway if state is corrupted
3. The `.unwrap()` noise obscures real logic

## Lock Patterns

### RAII Guards
All locks return guards that release on drop:

```rust
fn process(data: &Mutex<Data>) {
    let guard = data.lock();
    // guard.some_method()
} // Lock released here, even if we panic
```

### Try Lock (Non-blocking)
```rust
if let Some(guard) = mutex.try_lock() {
    // Got the lock
} else {
    // Lock held by someone else
}
```

### Timed Lock
```rust
use std::time::Duration;

if let Some(guard) = mutex.try_lock_for(Duration::from_millis(100)) {
    // Got lock within timeout
} else {
    // Timed out
}
```

### Mapped Guards
Access a field within locked data:

```rust
use parking_lot::{Mutex, MutexGuard, MappedMutexGuard};

struct Container { items: Vec<String> }

let mutex = Mutex::new(Container { items: vec![] });
let guard = mutex.lock();

// Map to just the items field
let items: MappedMutexGuard<Vec<String>> = 
    MutexGuard::map(guard, |c| &mut c.items);
```

### RwLock Upgradable Reads
```rust
// Start with read access
let read_guard = rwlock.upgradable_read();

// Decide we need to write
if needs_update(&*read_guard) {
    // Upgrade to write (may block)
    let mut write_guard = RwLockUpgradableReadGuard::upgrade(read_guard);
    *write_guard = new_value;
}
```

### Arc<Mutex<T>> with ArcMutexGuard
```rust
use parking_lot::{Mutex, ArcMutexGuard};
use std::sync::Arc;

let mutex = Arc::new(Mutex::new(42));

// Lock through Arc - guard has 'static lifetime
let guard: ArcMutexGuard<i32> = Mutex::lock_arc(&mutex);
// Can send guard to other threads!
```

## Deadlock Detection

Enable in Cargo.toml:
```toml
[dependencies]
parking_lot = { version = "0.12", features = ["deadlock_detection"] }
```

Then in debug builds:
```rust
use parking_lot::deadlock;
use std::thread;
use std::time::Duration;

// Start detector thread (usually in main)
thread::spawn(|| {
    loop {
        thread::sleep(Duration::from_secs(10));
        let deadlocks = deadlock::check_deadlock();
        if deadlocks.is_empty() {
            continue;
        }
        eprintln!("{} deadlocks detected!", deadlocks.len());
        for (i, threads) in deadlocks.iter().enumerate() {
            for t in threads {
                eprintln!("Deadlock #{}: Thread {:?}", i, t.thread_id());
                eprintln!("{:?}", t.backtrace());
            }
        }
    }
});
```

**Note**: Deadlock detection has runtime overhead. Use only in debug/test.

## Anti-patterns

### Holding Locks Across Await Points
```rust
// BAD - lock held across .await
async fn bad(mutex: &Mutex<Data>) {
    let guard = mutex.lock();
    some_async_op().await; // Other tasks blocked!
    // ...
}

// GOOD - release before await
async fn good(mutex: &Mutex<Data>) {
    let data = {
        let guard = mutex.lock();
        guard.clone() // Clone what you need
    }; // Lock released
    some_async_op().await;
    // Use data...
}
```

### Lock Ordering Violations (Deadlock Risk)
```rust
// Thread 1: lock A then B
// Thread 2: lock B then A
// = Potential deadlock!

// GOOD - consistent order everywhere
fn operation(a: &Mutex<A>, b: &Mutex<B>) {
    let _a = a.lock();
    let _b = b.lock(); // Always A before B
}
```

### Exposing MutexGuard in Return Types
```rust
// BAD - leaks lock duration to caller
fn get_data(&self) -> MutexGuard<Data> {
    self.data.lock()
}

// GOOD - return owned data
fn get_data(&self) -> Data {
    self.data.lock().clone()
}
```

### Forgetting Clone is Expensive
```rust
// If Data is large, cloning defeats the purpose
fn expensive(mutex: &Mutex<LargeData>) {
    let cloned = mutex.lock().clone(); // Copies megabytes
}

// Consider borrowing patterns or Arc<LargeData>
```

### Using Mutex When RwLock is Better
```rust
// If reads >> writes, RwLock allows parallelism
// Mutex serializes all access, even reads
let config = RwLock::new(Config::load()); // Reads are parallel
```

## Best Practices

1. **Prefer `parking_lot` over `std::sync`** for new code
2. **Use `RwLock` for read-heavy data** (config, caches)
3. **Use `Mutex` for write-heavy or small critical sections**
4. **Keep critical sections small** - do heavy work outside the lock
5. **Document lock ordering** if you have multiple locks
6. **Enable deadlock detection** in tests
7. **Alias to avoid confusion**: `use parking_lot::Mutex as ParkingMutex;`

## Common Cargo.toml Setup

```toml
[dependencies]
parking_lot = "0.12"

# Optional: deadlock detection for debug builds
[target.'cfg(debug_assertions)'.dependencies]
parking_lot = { version = "0.12", features = ["deadlock_detection"] }
```
