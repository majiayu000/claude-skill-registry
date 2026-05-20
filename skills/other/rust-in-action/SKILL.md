---
name: rust-in-action
description: >
  Write and review Rust code using systems programming concepts from "Rust in Action"
  by Tim McNamara. Covers language foundations, ownership and borrowing, smart pointers,
  data representation (bits, endianness, floats), memory (stack/heap/virtual), file I/O,
  networking (TCP/HTTP), concurrency (threads/closures), and OS-level programming.
  Use when writing systems-level Rust, working with binary data, raw pointers, file formats,
  network protocols, or low-level memory. Trigger on: "Rust", "systems programming",
  "smart pointers", "endianness", "bit manipulation", "TCP", "raw pointers", "serde",
  "borrow checker", "ownership", "concurrency", "kernel", ".rs files", "cargo".
---

# Rust in Action Skill

Apply the systems programming practices from Tim McNamara's "Rust in Action" to review existing code and write new Rust. This skill operates in two modes: **Review Mode** (analyze code for violations of Rust idioms and systems programming correctness) and **Write Mode** (produce safe, idiomatic, systems-capable Rust from scratch).

The key differentiator of this book: Rust is taught through real systems — a CPU simulator, key-value store, NTP client, raw TCP stack, and OS kernel. Practices focus on correctness at the hardware boundary, not just language syntax.

## Reference Files

- `practices-catalog.md` — Before/after examples for ownership, smart pointers, bit ops, I/O, networking, concurrency, error wrapping, and state machines

## How to Use This Skill

**Before responding**, read `practices-catalog.md` for the topic at hand. For ownership/borrowing issues read the ownership section. For systems/binary data read the data section. For a full review, read all sections.

---

## Mode 1: Code Review

When the user asks you to **review** Rust code, follow this process:

### Step 1: Identify the Domain
Determine whether the code is application-level, systems-level (binary data, I/O, networking, memory), or concurrent. The review focus shifts accordingly.

### Step 2: Analyze the Code

Check these areas in order of severity:

1. **Ownership & Borrowing** (Ch 4): Unnecessary `.clone()`? Value moved when a borrow would suffice? Use references where full ownership is not required.
2. **Smart Pointer Choice** (Ch 6): Is the right pointer type used? `Box<T>` for heap, `Rc<T>` for single-thread shared, `Arc<T>` for multi-thread shared, `RefCell<T>` for interior mutability (single-thread), `Mutex<T>` for interior mutability (multi-thread). `Cow<T>` when data is usually read but occasionally mutated.
3. **Error Handling** (Ch 3, 8): `.unwrap()` or `.expect()` where `?` belongs? For library code, define a custom error type that wraps downstream errors via `From` impl. Never leak internal error types across the public API boundary.
4. **Binary Data & Endianness** (Ch 5, 7): Are integer byte representations explicit? Use `to_le_bytes()` / `from_le_bytes()` / `to_be_bytes()`. Validate with checksums when writing binary formats. Use `serde` + `bincode` for structured serialization.
5. **Memory** (Ch 6): Is `unsafe` minimized? Raw pointer use must be bounded by a safe abstraction. Stack vs heap allocation: prefer stack; use `Box` only when size is unknown at compile time or you need heap lifetime.
6. **File & I/O** (Ch 7): Use `BufReader`/`BufWriter` for large files. Handle `ENOENT`, `EPERM`, `ENOSPC` distinctly — don't collapse I/O errors to strings. Use `std::fs::Path` for type-safe path handling.
7. **Networking** (Ch 8): TCP state is implicit in OS — model explicit state machines with enums. Use trait objects (`Box<dyn Trait>`) only when heterogeneous runtime dispatch is needed. Prefer `impl Trait` for static dispatch.
8. **Concurrency** (Ch 10): Closures passed to threads must be `'static` or use `move`. Shared mutable state needs `Arc<Mutex<T>>`. Use channels for message passing over shared state. Thread pool patterns over spawning one thread per task.
9. **Time** (Ch 9): Don't use `std::time::SystemTime` for elapsed measurement — it can go backwards. Use `std::time::Instant` for durations. For network time, NTP requires epoch conversion (NTP epoch: 1900 vs Unix: 1970 — offset 70 years = 2_208_988_800 seconds).
10. **Idioms**: Iterator adapters over manual loops. `for item in &collection` not `for i in 0..collection.len()`. `if let`/`while let` for single-variant matching. Exhaustive `match` — no silent wildcard arms.

### Step 3: Report Findings
For each issue, report:
- **Chapter reference** (e.g., "Ch 6: Smart Pointers")
- **Location** in the code
- **What's wrong** (the anti-pattern)
- **How to fix it** (the idiomatic / systems-correct approach)
- **Priority**: Critical (safety/UB/data corruption), Important (idiom/correctness), Suggestion (polish)

### Step 4: Provide Fixed Code
Offer a corrected version with comments explaining each change.

---

## Mode 2: Writing New Code

When the user asks you to **write** new Rust code, apply these core principles:

### Language Foundations (Ch 2)

1. **Use cargo, not rustc directly** (Ch 2). `cargo new`, `cargo build`, `cargo test`, `cargo doc`. Add third-party crates via `Cargo.toml` — never manually link.

2. **Prefer integer types that match the domain** (Ch 2). Use `u8` for bytes, `u16`/`u32`/`u64` for protocol fields sized to spec, `i64` for timestamps. Avoid default `usize` for domain values.

3. **Use `loop` for retry/event loops; `while` for condition-driven; `for` for iteration** (Ch 2). Never use `loop { if cond { break } }` where `while cond {}` is clearer.

### Compound Types & Traits (Ch 3)

4. **Model domain state with enums, not stringly-typed flags** (Ch 3). Enums with data (`enum Packet { Ack(u32), Data(Vec<u8>) }`) replace boolean + optional pairs and make invalid states unrepresentable.

5. **Implement `new()` as the canonical constructor** (Ch 3). `impl MyStruct { pub fn new(...) -> Self { ... } }`. Use `Default` for zero-value construction.

6. **Implement `std::fmt::Display` for user-facing output, `Debug` via derive** (Ch 3). Derive `Debug`; hand-implement `Display`. Never use `{:?}` in user-facing messages.

7. **Use `pub(crate)` to limit visibility to the crate; keep internals private** (Ch 3). Public API surface should be minimal and intentional.

8. **Document public items with `///` rustdoc comments** (Ch 3). Include examples in doc comments — `cargo test` runs them.

### Ownership, Borrowing & Smart Pointers (Ch 4, 6)

9. **Use references where full ownership is not required** (Ch 4). Pass `&T` for read, `&mut T` for write. Only transfer ownership when the callee must own (e.g., storing in a struct).

10. **Choose smart pointers by use case** (Ch 6):
    - `Box<T>` — heap allocation, single owner, unknown size at compile time
    - `Rc<T>` — shared ownership, single-threaded
    - `Arc<T>` — shared ownership, multi-threaded
    - `Cell<T>` — interior mutability for `Copy` types, single-threaded
    - `RefCell<T>` — interior mutability for non-`Copy`, single-threaded, runtime borrow checks
    - `Cow<'a, T>` — clone-on-write, avoids allocation when data is only read
    - `Arc<Mutex<T>>` — shared mutable state across threads

11. **Never use `Rc` across thread boundaries** (Ch 6). The compiler enforces this — `Rc` is not `Send`. Use `Arc` instead.

12. **Minimize `unsafe` blocks; wrap them in safe abstractions** (Ch 6). Raw pointers (`*const T`, `*mut T`) must be bounded within a module or function that upholds safety invariants. Document the safety contract with `// SAFETY:` comments.

### Data Representation (Ch 5)

13. **Be explicit about endianness in binary protocols** (Ch 5, 7). Use `u32::to_le_bytes()`, `u32::from_be_bytes()` etc. Never assume native endianness when writing to disk or network.

14. **Use bit operations to inspect and build packed data** (Ch 5). AND (`&`) to isolate bits, OR (`|`) to set bits, shift (`<<`, `>>`) to position. Use named constants for masks: `const SIGN_BIT: u32 = 0x8000_0000`.

15. **Validate binary data with checksums** (Ch 7). For key-value stores and file formats, store a CRC or hash alongside data. Verify on read before trusting.

### Files & Storage (Ch 7)

16. **Use `BufReader`/`BufWriter` for file I/O** (Ch 7). Raw `File::read()` makes a syscall per call. `BufReader` batches reads into user-space buffer.

17. **Use `serde` + `bincode` for binary serialization** (Ch 7). Add `#[derive(Serialize, Deserialize)]`; let `bincode::serialize`/`deserialize` handle encoding. Use `serde_json` for human-readable formats.

18. **Use `std::path::Path` and `PathBuf` for file paths** (Ch 7). Never build paths with string concatenation. Use `path.join()`, `path.extension()`, `path.file_name()`.

### Networking (Ch 8)

19. **Model protocol state explicitly with enums** (Ch 8). A TCP connection has states (SYN_SENT, ESTABLISHED, CLOSE_WAIT, etc.). Encode them as enum variants — the compiler enforces valid transitions.

20. **Wrap library errors in a domain error type** (Ch 8). When a function calls multiple libraries (network + I/O + parse), define an enum that wraps each. Implement `From<LibError> for DomainError` so `?` converts automatically.

21. **Use trait objects only for heterogeneous runtime dispatch** (Ch 8). `Vec<Box<dyn Animal>>` is correct when you have a mixed collection. For a single concrete type, `impl Trait` is zero-cost.

### Concurrency (Ch 10)

22. **Use `move` closures when passing to threads** (Ch 10). `thread::spawn(move || { ... })` transfers ownership of captured variables into the thread. This is required when the closure outlives the current stack frame.

23. **Use `Arc::clone()` explicitly, not `.clone()` on a value** (Ch 10). `Arc::clone(&ptr)` is idiomatic — it's cheap (increments a reference count). Avoid `.clone()` on the inner value.

24. **Use channels for work distribution; `Arc<Mutex<T>>` for shared state** (Ch 10). Channels (`std::sync::mpsc`) are simpler and safer. Use shared state only when channels don't fit (e.g., result collection).

25. **Use thread pools over raw `thread::spawn` per task** (Ch 10). Spawning one thread per request doesn't scale. Use `rayon`, `tokio`, or a manual pool with a bounded queue.

### Time (Ch 9)

26. **Use `Instant` for elapsed time, `SystemTime` for wall clock** (Ch 9). `SystemTime` can go backwards (NTP adjustments, leap seconds). `Instant` is monotonic.

27. **Apply the NTP epoch offset when working with network time** (Ch 9). NTP timestamps count seconds from 1900-01-01; Unix timestamps count from 1970-01-01. Offset: `2_208_988_800u64` seconds.

---

## Smart Pointer Selection Guide (Ch 6)

```
Is the data shared across threads?
├── Yes → Arc<T> (read-only) or Arc<Mutex<T>> (mutable)
└── No
    ├── Shared (multiple owners, single thread)?
    │   └── Rc<T> (read-only) or Rc<RefCell<T>> (mutable)
    └── Single owner
        ├── Size unknown at compile time / recursive type?
        │   └── Box<T>
        ├── Usually read, occasionally cloned/modified?
        │   └── Cow<'a, T>
        └── Interior mutability needed?
            ├── Copy type → Cell<T>
            └── Non-Copy → RefCell<T>
```

---

## Code Structure Templates

### Binary Protocol Field (Ch 5, 7)
```rust
/// Parse a 4-byte big-endian u32 from a byte buffer at offset.
fn read_u32_be(buf: &[u8], offset: usize) -> Result<u32, ParseError> {
    buf.get(offset..offset + 4)
        .ok_or(ParseError::UnexpectedEof)
        .map(|b| u32::from_be_bytes(b.try_into().unwrap()))
}

const FLAGS_MASK: u8 = 0b0000_1111;  // isolate lower 4 bits
fn extract_flags(byte: u8) -> u8 {
    byte & FLAGS_MASK
}
```

### Library Error Type (Ch 8)
```rust
#[derive(Debug)]
pub enum AppError {
    Io(std::io::Error),
    Network(std::net::AddrParseError),
    Parse(String),
}

impl std::fmt::Display for AppError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            AppError::Io(e)      => write!(f, "I/O error: {e}"),
            AppError::Network(e) => write!(f, "network error: {e}"),
            AppError::Parse(msg) => write!(f, "parse error: {msg}"),
        }
    }
}

impl std::error::Error for AppError {}
impl From<std::io::Error> for AppError {
    fn from(e: std::io::Error) -> Self { AppError::Io(e) }
}
impl From<std::net::AddrParseError> for AppError {
    fn from(e: std::net::AddrParseError) -> Self { AppError::Network(e) }
}
```

### State Machine with Enum (Ch 8)
```rust
#[derive(Debug, Clone, PartialEq)]
enum ConnectionState {
    Idle,
    Connecting { addr: std::net::SocketAddr },
    Connected { stream: std::net::TcpStream },
    Closed,
}

impl ConnectionState {
    fn connect(addr: std::net::SocketAddr) -> Result<Self, AppError> {
        let stream = std::net::TcpStream::connect(addr)?;
        Ok(ConnectionState::Connected { stream })
    }
}
```

### Thread Pool Pattern (Ch 10)
```rust
use std::sync::{Arc, Mutex};
use std::sync::mpsc;
use std::thread;

type Job = Box<dyn FnOnce() + Send + 'static>;

struct ThreadPool {
    sender: mpsc::Sender<Job>,
}

impl ThreadPool {
    fn new(size: usize) -> Self {
        let (sender, receiver) = mpsc::channel::<Job>();
        let receiver = Arc::new(Mutex::new(receiver));

        for _ in 0..size {
            let rx = Arc::clone(&receiver);
            thread::spawn(move || loop {
                let job = rx.lock().expect("mutex poisoned").recv();
                match job {
                    Ok(f) => f(),
                    Err(_) => break, // channel closed
                }
            });
        }
        ThreadPool { sender }
    }

    fn execute(&self, f: impl FnOnce() + Send + 'static) {
        self.sender.send(Box::new(f)).expect("thread pool closed");
    }
}
```

---

## Priority of Practices by Impact

### Critical (Safety, Correctness, UB)
- Ch 4: Borrow, don't clone — never move when a reference suffices
- Ch 6: Choose the right smart pointer — `Rc` is not thread-safe; don't share across threads
- Ch 6: Wrap `unsafe` in safe abstractions — document safety contracts with `// SAFETY:`
- Ch 5/7: Explicit endianness — wrong byte order silently corrupts binary data
- Ch 9: Use `Instant` for elapsed time — `SystemTime` can go backwards

### Important (Idiom & Maintainability)
- Ch 3: Domain enums over stringly-typed state — invalid states should not compile
- Ch 8: Wrap downstream errors in a domain error type with `From` impls
- Ch 8: `impl Trait` over `dyn Trait` when types are homogeneous
- Ch 10: `move` closures for threads — required when closure outlives the stack frame
- Ch 10: `Arc::clone()` idiom — makes cheap pointer clone explicit

### Suggestions (Systems Polish)
- Ch 2: Size integer types to the protocol spec — `u8` for bytes, `u16` for ports
- Ch 5: Named bit-mask constants — `const SIGN_BIT: u32 = 0x8000_0000`
- Ch 7: `BufReader`/`BufWriter` for all file I/O — syscall batching
- Ch 7: Checksums on binary writes — detect corruption on read
- Ch 9: NTP epoch offset constant — `const NTP_UNIX_OFFSET: u64 = 2_208_988_800`
