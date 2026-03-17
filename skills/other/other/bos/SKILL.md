---
name: bos-concurrency-rust
description: Write Rust code in the style of Mara Bos, Rust library team lead and author of "Rust Atomics and Locks." Emphasizes low-level concurrency, atomics, and understanding the memory model. Use when writing concurrent or lock-free code.
---

# Mara Bos Style Guide

## Overview

Mara Bos is the Rust library team lead and author of "Rust Atomics and Locks." She maintains core synchronization primitives in the standard library. Her expertise: making concurrent code correct, efficient, and understandable.

## Core Philosophy

> "Concurrency bugs are hard to find. Make them impossible instead."

> "Understand the memory model before using atomics."

Bos believes that **concurrent code must be provably correct**. Understanding happens-before relationships and memory ordering is essential, not optional.

## Design Principles

1. **Correctness First**: A fast but incorrect concurrent algorithm is worthless.

2. **Understand Ordering**: Every atomic operation needs the right memory ordering.

3. **Minimize Shared State**: Less sharing means fewer bugs.

4. **Prefer High-Level Abstractions**: Use channels and mutexes before atomics.

## When Writing Code

### Always

- Use the highest-level abstraction that works (channels > mutexes > atomics)
- Document the synchronization strategy for concurrent code
- Test concurrent code with tools like Miri and loom
- Understand why each memory ordering is chosen
- Consider what happens if operations interleave

### Never

- Use `Ordering::Relaxed` without understanding the implications
- Assume operations happen in source code order
- Write lock-free code without formal reasoning
- Ignore potential data races in unsafe code

### Prefer

- `Mutex<T>` over manual locking
- `crossbeam` channels over `std::sync::mpsc`
- `parking_lot` for high-performance locking
- `Ordering::SeqCst` when unsure (then optimize if needed)

## Code Patterns

### The Ordering Hierarchy

```rust
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};

// RELAXED: No synchronization, only atomicity
// Use for: Counters where exact order doesn't matter
static COUNTER: AtomicUsize = AtomicUsize::new(0);

fn increment() {
    COUNTER.fetch_add(1, Ordering::Relaxed);
}

// ACQUIRE/RELEASE: Synchronize between threads
// Use for: Protecting non-atomic data, implementing locks
static READY: AtomicBool = AtomicBool::new(false);
static mut DATA: u64 = 0;

fn producer() {
    unsafe { DATA = 42; }
    READY.store(true, Ordering::Release);  // Release DATA
}

fn consumer() {
    while !READY.load(Ordering::Acquire) {}  // Acquire DATA
    unsafe { println!("{}", DATA); }  // Safe: synchronized
}

// SEQ_CST: Total ordering across all threads
// Use for: When you need a global order of operations
static FLAG_A: AtomicBool = AtomicBool::new(false);
static FLAG_B: AtomicBool = AtomicBool::new(false);

// With SeqCst, all threads agree on the order of operations
```

### Implementing a Spinlock

```rust
use std::sync::atomic::{AtomicBool, Ordering};
use std::cell::UnsafeCell;
use std::ops::{Deref, DerefMut};

pub struct SpinLock<T> {
    locked: AtomicBool,
    data: UnsafeCell<T>,
}

// SAFETY: SpinLock provides synchronization
unsafe impl<T: Send> Send for SpinLock<T> {}
unsafe impl<T: Send> Sync for SpinLock<T> {}

impl<T> SpinLock<T> {
    pub const fn new(data: T) -> Self {
        SpinLock {
            locked: AtomicBool::new(false),
            data: UnsafeCell::new(data),
        }
    }

    pub fn lock(&self) -> SpinLockGuard<'_, T> {
        // Spin until we acquire the lock
        while self.locked
            .compare_exchange_weak(
                false,              // Expected: unlocked
                true,               // Desired: locked
                Ordering::Acquire,  // Success: acquire the data
                Ordering::Relaxed,  // Failure: just retry
            )
            .is_err()
        {
            // Hint to the CPU that we're spinning
            std::hint::spin_loop();
        }
        
        SpinLockGuard { lock: self }
    }
}

pub struct SpinLockGuard<'a, T> {
    lock: &'a SpinLock<T>,
}

impl<T> Deref for SpinLockGuard<'_, T> {
    type Target = T;
    
    fn deref(&self) -> &T {
        // SAFETY: We hold the lock
        unsafe { &*self.lock.data.get() }
    }
}

impl<T> DerefMut for SpinLockGuard<'_, T> {
    fn deref_mut(&mut self) -> &mut T {
        // SAFETY: We hold the lock exclusively
        unsafe { &mut *self.lock.data.get() }
    }
}

impl<T> Drop for SpinLockGuard<'_, T> {
    fn drop(&mut self) {
        self.lock.locked.store(false, Ordering::Release);
    }
}
```

### Arc and Weak for Shared Ownership

```rust
use std::sync::{Arc, Weak};

struct Node {
    value: i32,
    // Strong reference to children (owns them)
    children: Vec<Arc<Node>>,
    // Weak reference to parent (doesn't own)
    parent: Weak<Node>,
}

fn create_tree() -> Arc<Node> {
    let root = Arc::new(Node {
        value: 1,
        children: Vec::new(),
        parent: Weak::new(),
    });
    
    let child = Arc::new(Node {
        value: 2,
        children: Vec::new(),
        parent: Arc::downgrade(&root),  // Weak reference
    });
    
    // To add child to root, we'd need interior mutability
    // (this example is simplified)
    
    root
}

fn traverse_up(node: &Node) {
    if let Some(parent) = node.parent.upgrade() {
        println!("Parent value: {}", parent.value);
        traverse_up(&parent);
    }
}
```

### Channel Patterns

```rust
use std::sync::mpsc;
use std::thread;

// Basic channel usage
fn producer_consumer() {
    let (tx, rx) = mpsc::channel();
    
    // Producer thread
    thread::spawn(move || {
        for i in 0..10 {
            tx.send(i).unwrap();
        }
    });
    
    // Consumer in main thread
    for received in rx {
        println!("Got: {}", received);
    }
}

// Multiple producers
fn multi_producer() {
    let (tx, rx) = mpsc::channel();
    
    for i in 0..4 {
        let tx_clone = tx.clone();
        thread::spawn(move || {
            tx_clone.send(format!("from thread {}", i)).unwrap();
        });
    }
    
    drop(tx);  // Drop original so rx knows when to stop
    
    for msg in rx {
        println!("{}", msg);
    }
}

// Bounded channel (backpressure)
fn bounded_channel() {
    let (tx, rx) = mpsc::sync_channel(10);  // Buffer of 10
    
    thread::spawn(move || {
        for i in 0..100 {
            tx.send(i).unwrap();  // Blocks if buffer full
        }
    });
}
```

### Testing Concurrent Code

```rust
// Use loom for exhaustive concurrency testing
#[cfg(test)]
mod tests {
    use loom::sync::atomic::{AtomicUsize, Ordering};
    use loom::thread;

    #[test]
    fn test_concurrent_increment() {
        loom::model(|| {
            let counter = AtomicUsize::new(0);
            
            let counter1 = &counter;
            let counter2 = &counter;
            
            let t1 = thread::spawn(move || {
                counter1.fetch_add(1, Ordering::SeqCst);
            });
            
            let t2 = thread::spawn(move || {
                counter2.fetch_add(1, Ordering::SeqCst);
            });
            
            t1.join().unwrap();
            t2.join().unwrap();
            
            assert_eq!(counter.load(Ordering::SeqCst), 2);
        });
    }
}
```

## Mental Model

Bos thinks about concurrency as:

1. **What is shared?** Identify all shared state.
2. **What orderings can occur?** Consider all interleavings.
3. **What synchronization is needed?** Ensure happens-before.
4. **Can I prove correctness?** If not, simplify.

## Memory Ordering Cheat Sheet

| Ordering | Use Case |
|----------|----------|
| `Relaxed` | Counters, statistics (no sync needed) |
| `Acquire` | Load that precedes accessing protected data |
| `Release` | Store that follows modifying protected data |
| `AcqRel` | Read-modify-write that does both |
| `SeqCst` | When you need global ordering (default choice) |

