---
name: coding-systems
cluster: coding
description: "Systems meta-skill: Rust + Nim + Go + C for low-level, memory safety, FFI, performance-critical code"
tags: ["systems","low-level","performance","coding"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "systems programming low level memory performance ffi os c rust nim go"
---

# coding-systems

## Purpose
This skill equips the AI to handle systems programming using Rust, Nim, Go, and C, focusing on low-level operations, memory safety, FFI (Foreign Function Interface), and performance-critical code. It combines these languages for tasks like OS development, embedded systems, and high-throughput applications.

## When to Use
Use this skill for scenarios requiring direct hardware access, memory management, or inter-language calls, such as writing kernel modules, optimizing network servers, or integrating C libraries into modern languages. Avoid for high-level web apps; prefer when performance bottlenecks demand low-level control.

## Key Capabilities
- **Rust**: Enforces memory safety via ownership and borrowing; supports FFI with C using `extern "C"` blocks.
- **Nim**: Offers metaprogramming and FFI via `importc` pragma; compiles to C for performance.
- **Go**: Provides concurrency with goroutines and channels; uses cgo for FFI to C libraries.
- **C**: Enables raw memory manipulation and OS interactions; use for performance-critical kernels.
- Specific features: Rust's `unsafe` blocks for pointer arithmetic; Go's `sync` package for thread-safe operations; Nim's templates for code generation; C's `mmap` for direct memory mapping.

## Usage Patterns
To accomplish tasks, structure code with language-specific patterns: Use Rust for safe wrappers around C code; employ Go for scalable concurrent systems; leverage Nim for rapid prototyping of C-like code; fall back to C for hardware-level optimizations. For FFI, always define interfaces first (e.g., in C headers), then bind in target languages. Pattern: Import C headers in Rust via `#[link(name = "libc")]`; in Go, use `// #cgo LDFLAGS: -lmylib` for linking.

## Common Commands/API
- **Rust**: Build with `cargo build --release` for optimized binaries; use `std::ffi::c_void` for FFI pointers. API example: `extern "C" fn add(a: i32, b: i32) -> i32 { a + b }`
- **Nim**: Compile with `nim c --cc:gcc -d:release myfile.nim`; FFI via `proc add(a: cint, b: cint): cint {.importc: "add", header: "myheader.h".}`
- **Nim code snippet**:
  ```nim
  proc add(a: cint, b: cint): cint {.importc.}
  echo add(1, 2)  # Calls external C function
  ```
- **Go**: Run `go build -o myapp` with cgo; API: `import "C"` for FFI. Example: `C.add(C.int(1), C.int(2))`
- **Go code snippet**:
  ```go
  import "C"
  func main() { println(int(C.add(1, 2))) }
  ```
- **C**: Compile with `gcc -O3 -o myprog myfile.c` for optimizations; use `#include <sys/mman.h>` for OS APIs.
- Config formats: Use Cargo.toml for Rust dependencies (e.g., `[dependencies] libc = "0.2"`); Go's go.mod for modules; Nim's .nimble for packages.

## Integration Notes
Integrate by linking languages via FFI: For Rust-C, set `build.rs` to generate bindings with bindgen; in Go, use cgo directives like `// #include "myheader.h"`. If API keys are needed (e.g., for external tools), set env vars like `$RUST_ANALYZER_API_KEY`. For cross-language projects, use CMake for unified builds: Add `add_subdirectory(rust_project)` in CMakeLists.txt. Always handle ABI compatibility; e.g., ensure C functions use `__attribute__((visibility("default")))` for export.

## Error Handling
In Rust, use `Result<T, E>` for fallible operations; check with `match` or `?`. For Nim, use exceptions with `try/except`; e.g., `try: raise newException(ValueError, "Error") except: echo "Handled"`. Go errors return as second values; check with `if err != nil { return err }`. C uses errno; wrap with custom error codes. General pattern: Propagate errors up the call stack and log with details, e.g., in Rust: `fn safe_add(a: i32) -> Result<i32, String> { if a < 0 { Err("Negative input".to_string()) } else { Ok(a + 1) } }`.

## Concrete Usage Examples
1. **FFI Wrapper for C Library in Rust**: To call a C function for memory allocation, first define the interface: Use `extern "C" { fn malloc(size: usize) -> *mut u8; }`. Then, in code: `let ptr = unsafe { malloc(1024) }; if ptr.is_null() { panic!("Allocation failed"); }`. This pattern ensures safe memory handling in performance-critical apps.
2. **Concurrent Performance Task in Go**: For a high-throughput server, use goroutines: `go func() { for i := 0; i < 100; i++ { fmt.Println(i) } }(); runtime.Gosched()`. Integrate with C via cgo for low-level I/O, e.g., to read from a file descriptor, ensuring non-blocking operations for real-time systems.

## Graph Relationships
- Cluster: Related to "coding" cluster for general programming skills.
- Tags: Connected via "systems", "low-level", "performance", "coding" to other skills like "ffi-handling" or "memory-management".
- Embedding: Links to skills with similar vectors, such as "os-programming" based on "systems programming low level memory performance ffi os c rust nim go".
