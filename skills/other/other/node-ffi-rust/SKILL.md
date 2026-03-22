---
name: node-ffi-rust
description: Build high-performance native modules for Node.js using Rust and N-API via napi-rs. Use when optimizing compute-intensive operations, integrating system libraries, or requiring native performance without blocking the event loop.
license: MIT
compatibility: Requires Node.js 14+, Rust 1.56+, and platform-specific build tools (gcc/clang for Linux/macOS, MSVC for Windows)
metadata:
  author: langchain-fastapi-production
  version: "1.0"
---

# Node.js FFI Rust Skill

Build native extensions for Node.js using Rust with N-API bindings via napi-rs.

## When to Use

- **CPU-intensive operations**: Crypto, compression, math, image processing
- **System integration**: OS-level operations, hardware access
- **Large data processing**: Batch operations on buffers/arrays
- **Legacy libraries**: Wrap existing Rust/C libraries
- **Event loop safety**: Offload blocking work without freezing the server

## Quick Start

### 1. Create Project

```bash
cargo new --lib my-native-module
cd my-native-module
```

### 2. Add napi-rs

```toml
[package]
name = "my_native_module"
version = "0.1.0"
edition = "2021"

[dependencies]
napi = { version = "2", features = ["napi8"] }
napi-derive = "2"

[lib]
crate-type = ["cdylib"]
```

### 3. Write Rust Function

```rust
use napi_derive::napi;

#[napi]
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[napi]
pub fn process_buffer(data: Vec<u8>) -> Vec<u8> {
    data.iter().map(|b| b.wrapping_add(1)).collect()
}
```

### 4. Build

```bash
npm install -g @napi-rs/cli
napi build --release
```

### 5. Use in Node.js

```js
const { add, processBuffer } = require('./index.node');

console.log(add(2, 3));           // 5
console.log(processBuffer([1,2,3])); // [2,3,4]
```

## Architecture

```
JS → V8 → N-API → Rust → N-API → V8 → JS
```

Rust runs at native speed. N-API handles type conversion and memory safety.

## Performance Considerations

### Boundary Overhead
- **Cost**: 100-300 nanoseconds per call
- **Dominates**: Tiny functions called repeatedly
- **Solution**: Batch operations

### Serialization Cost
- **JSON**: Very expensive (parse/stringify)
- **TypedArray**: Zero-copy (direct memory mapping)
- **Buffers**: Efficient (single allocation)

### Rule of Thumb
**If work per call > boundary cost → native wins**

## Critical Edge Cases

See [references/EDGE_CASES.md](references/EDGE_CASES.md) for:
- Panic safety (catch_unwind required)
- Event loop blocking (use napi::Task)
- Buffer ownership (references vs copies)
- Async callbacks (thread safety)
- Cross-platform builds (prebuilt binaries)
- Struct layout (repr(C) for ABI stability)

## Best Practices

1. **Use napi-rs** — Safer than raw N-API, better DX
2. **Design around buffers** — TypedArray/Buffer, not JS objects
3. **Batch operations** — Process entire datasets, not row-by-row
4. **Avoid event loop blocking** — Use `napi::Task` for CPU work
5. **Wrap panics** — `std::panic::catch_unwind()` always
6. **Reuse buffers** — Minimize allocations
7. **Version APIs** — Struct layouts are ABI contracts

## Optimization Checklist

- [ ] Minimize JS ↔ Rust calls
- [ ] Avoid JSON serialization
- [ ] Use TypedArray/Buffer
- [ ] Batch operations
- [ ] No event loop blocking
- [ ] Panics wrapped safely
- [ ] Boundary overhead benchmarked
- [ ] Prebuilt binaries available
- [ ] No JS references held across threads
- [ ] Buffers reused where possible

## Example: Batch Array Processing

**Rust** (`src/lib.rs`):
```rust
use napi_derive::napi;

#[napi]
pub fn sum_array(data: Vec<u32>) -> u32 {
    data.iter().sum()
}

#[napi]
pub fn process_batch(data: Vec<u8>, key: u8) -> Vec<u8> {
    data.iter().map(|b| b ^ key).collect()
}
```

**Node.js** (`index.js`):
```js
const { sumArray, processBatch } = require('./index.node');

const data = new Uint32Array([1, 2, 3, 4, 5]);
console.log(sumArray(Array.from(data))); // 15

const buffer = Buffer.from([72, 101, 108, 108, 111]);
console.log(processBatch(buffer, 42)); // XOR encrypted
```

This avoids 5 separate JS→Rust calls and processes data once.

## Mental Model

Think of FFI as a **toll booth between two countries**.

- **Many tiny cars** (frequent small calls) → toll booth dominates
- **One giant truck** (batch operation) → efficient trip

This predicts nearly every FFI performance problem.

## See Also

- [Complete SDK Reference](references/COMPLETE_SDK_REFERENCE.md)
- [Rust Documentation](https://doc.rust-lang.org/)
- [napi-rs Docs](https://napi.rs/)
- [Node.js N-API](https://nodejs.org/api/n_api.html)
