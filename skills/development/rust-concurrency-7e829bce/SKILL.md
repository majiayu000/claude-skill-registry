---
name: rust-concurrency
description: Master Rust concurrency - threads, channels, and parallel iterators
sasmp_version: "1.3.0"
bonded_agent: rust-async-agent
bond_type: SECONDARY_BOND
version: "1.0.0"
---

# Rust Concurrency Skill

Master thread-based concurrency: threads, channels, synchronization, and parallel processing.

## Quick Start

### Threads

```rust
use std::thread;

let handle = thread::spawn(|| {
    println!("Hello from thread!");
    42
});

let result = handle.join().unwrap();
```

### Channels

```rust
use std::sync::mpsc;

let (tx, rx) = mpsc::channel();

thread::spawn(move || {
    tx.send("message").unwrap();
});

println!("Got: {}", rx.recv().unwrap());
```

### Mutex

```rust
use std::sync::{Arc, Mutex};

let counter = Arc::new(Mutex::new(0));
let mut handles = vec![];

for _ in 0..10 {
    let counter = Arc::clone(&counter);
    handles.push(thread::spawn(move || {
        *counter.lock().unwrap() += 1;
    }));
}

for h in handles { h.join().unwrap(); }
```

## Parallel Iterators (Rayon)

```rust
use rayon::prelude::*;

let sum: i32 = (0..1000)
    .into_par_iter()
    .map(|x| x * 2)
    .sum();
```

### Parallel Operations

```rust
// Parallel map
let results: Vec<_> = data.par_iter()
    .map(|x| expensive(x))
    .collect();

// Parallel sort
data.par_sort();
```

## Synchronization

### RwLock

```rust
use std::sync::RwLock;

let data = RwLock::new(vec![]);

// Multiple readers
let read = data.read().unwrap();

// Single writer
let mut write = data.write().unwrap();
```

### Atomics

```rust
use std::sync::atomic::{AtomicUsize, Ordering};

let counter = AtomicUsize::new(0);
counter.fetch_add(1, Ordering::SeqCst);
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Deadlock | Lock in same order |
| Data race | Use Arc<Mutex<T>> |
| Slow parallel | Increase work per thread |

## Resources

- [Rust Book Ch.16](https://doc.rust-lang.org/book/ch16-00-concurrency.html)
- [Rayon](https://docs.rs/rayon)
