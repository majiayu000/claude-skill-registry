---
name: cpp
description: Comprehensive C/C++ programming reference covering everything from C11-C23 and C++11-C++23, system programming, CUDA GPU computing, debugging tools, Rust interop, and advanced topics. Use for: C/C++ questions, modern language features, RAII/memory management, templates/generics, CUDA programming, system programming, debugging/profiling, performance optimization, cross-platform development, build systems, assembly, shell scripting, and any C/C++/CUDA development tasks.
---

# C/C++ Comprehensive Cheat Sheets (/cpp)

Complete C/C++ development reference combining local documentation with live examples from cppcheatsheet.com, covering everything from basic syntax to advanced GPU programming and system-level development.

## How It Works

When you ask C/C++ questions, I will:
1. **Fetch live examples** from https://cppcheatsheet.com/
2. **Enhance with local docs** if in the cppcheatsheet repository
3. **Provide current, comprehensive answers** from the best available sources

## Coverage Areas

### Modern C Programming (C11-C23)
**Core Language:** Syntax, types, memory management, preprocessor macros
**GNU Extensions:** Compiler-specific features and optimizations
**Build Systems:** Makefiles, compilation, linking
**Assembly:** X86 assembly integration and inline assembly

### Modern C++ Programming (C++11-C++23)
**Core Features:** RAII, templates, STL containers, iterators, algorithms
**Modern Standards:** Move semantics, constexpr, lambdas, concepts, coroutines, modules
**Memory Management:** Smart pointers, resource management, optimization (RVO)
**Build Systems:** CMake, package management, cross-platform builds

### System Programming
**Process Management:** POSIX processes, signals, process communication
**File Systems:** File I/O, directory operations, filesystem monitoring
**Networking:** Sockets, protocols, network programming patterns
**Threading:** Multithreading, synchronization, parallel programming
**IPC:** Inter-process communication, shared memory, message queues

### CUDA Programming
**GPU Computing:** CUDA kernels, memory hierarchy, performance optimization
**Advanced CUDA:** libcu++, Thrust library, cooperative groups
**Multi-GPU:** GPU-GPU communication, hardware topology, NVSHMEM
**Async Programming:** CUDA pipelines, memory visibility, asynchronous execution

### Debugging & Profiling
**Debug Tools:** GDB debugging, Valgrind memory analysis, sanitizers
**Performance:** Perf profiling, tracing, performance optimization
**GPU Debugging:** Nsight Systems, CUDA debugging and profiling

### System Tools & Automation
**Shell Scripting:** Bash programming, system administration
**System Tools:** OS utilities, networking tools, hardware inspection
**Service Management:** Systemd, process management, system monitoring

### Cross-Language Development
**Rust Interop:** Rust for C++ developers, FFI, memory safety comparison
**Language Bridging:** C/C++ integration, foreign function interfaces

### Advanced Topics
**Blog Content:** Deep-dive articles, RDMA networking, GPU-initiated communication
**Low-Level Programming:** Hardware interfaces, performance tuning
**Architecture:** System design, scalable applications

## References

For detailed information, I can access:
- **[Structure](references/structure.md)** - Complete topic-to-URL reference map
- **[Guidelines](references/guidelines.md)** - Code quality and best practices

## Quick Examples

### C/C++ Core
- "Modern C++23 features with examples" → Latest language standards
- "RAII and smart pointer patterns" → Memory management best practices
- "Template metaprogramming techniques" → Advanced generic programming

### System Programming
- "POSIX socket programming examples" → Network programming patterns
- "Multithreading with std::thread and synchronization" → Concurrent programming
- "Signal handling and process management" → System-level programming

### CUDA & GPU Programming
- "CUDA kernel optimization techniques" → GPU performance programming
- "Multi-GPU communication with NVSHMEM" → Distributed GPU computing
- "CUDA memory hierarchy and optimization" → Memory-efficient GPU code

### Debugging & Tools
- "GDB debugging C++ applications" → Interactive debugging techniques
- "Valgrind memory leak detection" → Memory analysis and debugging
- "Performance profiling with perf" → System performance analysis

### Build & Development
- "CMake cross-platform build systems" → Modern C++ project setup
- "Makefile patterns and best practices" → C build automation
- "Cross-compilation and toolchain setup" → Multi-platform development