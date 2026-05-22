---
name: systems-programming
description: Systems programming from memory management through networking. Covers memory models (stack vs heap, manual allocation, garbage collection, ownership/borrowing), concurrency (threads, mutexes, channels, async/await, actor model, data races vs race conditions), operating system concepts (processes, virtual memory, page tables, system calls, file descriptors, signals), compilation (lexing, parsing, code generation, linking, static vs dynamic libraries), networking fundamentals (TCP/IP, sockets, HTTP, DNS, TLS), and the hardware-software boundary (caches, cache lines, false sharing, memory-mapped I/O). Use when working with low-level code, diagnosing system-level bugs, understanding performance characteristics, or bridging between high-level languages and machine behavior.
type: skill
category: coding
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/coding/systems-programming/SKILL.md
superseded_by: null
---
# Systems Programming

Systems programming is programming where the machine's physical constraints -- memory, concurrency, I/O bandwidth, latency -- are not abstractions but design parameters. A web application can ignore cache lines; an operating system kernel cannot. This skill catalogs the concepts that distinguish systems programming from application programming, with emphasis on the mental models needed to reason about programs that interact directly with hardware and operating system primitives.

**Agent affinity:** hopper (compilers, language implementation, systems), turing (computability, machine models)

**Concept IDs:** code-abstraction, code-code-organization, code-debugging-strategies

## Part 1 -- Memory Management

### Stack vs Heap

**Stack.** LIFO allocation. Each function call pushes a frame; return pops it. Allocation and deallocation are free (pointer arithmetic). Size is bounded (typically 1-8 MB per thread). Perfect for local variables with known lifetimes.

**Heap.** Dynamic allocation. Memory is requested explicitly (malloc/new/Box::new) and freed explicitly or by a garbage collector. Slower than stack (allocator must find free space, manage fragmentation). Necessary for data whose size or lifetime is not known at compile time.

**The fundamental tradeoff.** Stack allocation is fast but inflexible (fixed size, LIFO lifetime). Heap allocation is flexible but slow (allocation overhead, fragmentation, potential leaks).

### Manual Memory Management (C)

**malloc/free.** The programmer requests memory and is responsible for returning it. Every malloc must have a corresponding free. Failure modes:

- **Memory leak:** malloc without free. Memory grows until the process is killed.
- **Use-after-free:** Accessing memory that has been freed. Undefined behavior -- the memory may have been reused.
- **Double free:** Freeing memory twice. Corrupts the allocator's data structures.
- **Buffer overflow:** Writing beyond allocated bounds. The most exploited vulnerability class in computing history.

### Garbage Collection

**Mark-and-sweep.** Starting from root references (stack, globals), mark all reachable objects. Sweep (free) unmarked objects. Simple but causes pause times proportional to heap size.

**Generational GC.** Observation: most objects die young. Divide the heap into generations (young, old). Collect the young generation frequently (fast, small) and the old generation rarely (slow, large). Used by JVM, .NET, V8.

**Reference counting.** Track the number of references to each object. Free when count reaches zero. Immediate reclamation but cannot collect cycles (A references B, B references A, nobody else references either). Python uses reference counting plus a cycle detector.

**Tradeoffs.** GC eliminates use-after-free and double-free. It introduces unpredictable pause times and higher memory usage (objects may survive longer than necessary). Real-time systems and game engines often avoid GC.

### Ownership and Borrowing (Rust)

Rust's ownership system eliminates both manual memory bugs and GC overhead:

- **Ownership:** Every value has exactly one owner. When the owner goes out of scope, the value is dropped (freed).
- **Move semantics:** Assigning a value to a new variable moves ownership. The old variable is no longer valid.
- **Borrowing:** References (&T for shared, &mut T for exclusive) allow temporary access without taking ownership. The borrow checker enforces at compile time: either one &mut or any number of & at any given time.
- **Lifetimes:** Annotations that tell the compiler how long a reference is valid. Prevents dangling references at compile time.

This system achieves memory safety without runtime cost. The price is compile-time complexity -- the borrow checker rejects programs that are correct but cannot be proven safe by its rules.

## Part 2 -- Concurrency

### Threads

A thread is an independent sequence of execution within a process. Threads share the process's address space (heap, globals, file descriptors) but have independent stacks and program counters.

**Creating threads.** POSIX pthreads (C), std::thread (C++/Rust), threading module (Python), Web Workers (JavaScript, no shared memory).

**The problem.** Shared mutable state + concurrent access = data races. A data race occurs when two threads access the same memory location, at least one writes, and there is no synchronization between them. The result is undefined behavior.

### Synchronization Primitives

**Mutex (mutual exclusion).** A lock that ensures only one thread can access a critical section at a time. Lock before accessing shared state, unlock after. Deadlock occurs when two threads each hold a lock the other needs.

**Read-write lock.** Multiple readers OR one writer. Better throughput than mutex when reads dominate.

**Condition variable.** Allows a thread to sleep until a condition is signaled by another thread. Used with a mutex to avoid busy-waiting.

**Semaphore.** A counter that controls access to a finite pool of resources. P (wait/decrement) and V (signal/increment). Mutex is a semaphore with count 1.

**Atomic operations.** Lock-free read-modify-write operations (compare-and-swap, fetch-and-add). Used for counters, flags, and lock-free data structures. Require understanding of memory ordering (relaxed, acquire, release, sequentially consistent).

### Channels (Message Passing)

Instead of sharing state, threads communicate by sending messages through channels. The sender puts a message in; the receiver takes it out. No shared mutable state, no data races.

**Go's philosophy:** "Do not communicate by sharing memory; share memory by communicating." Channels are first-class in Go, Rust, and Erlang.

**Bounded vs unbounded.** A bounded channel blocks the sender when full (backpressure). An unbounded channel never blocks but can consume unlimited memory.

### Async/Await

**Problem.** Threads are expensive (1 MB stack each, OS scheduling overhead). A web server handling 10,000 concurrent connections cannot afford 10,000 threads.

**Solution.** Cooperative multitasking. An async function yields control when it waits for I/O. A runtime (event loop, executor) multiplexes many async tasks onto a small number of threads.

**Mental model.** Async code looks sequential but executes concurrently. Each `await` is a potential suspension point. The task resumes when the awaited operation completes.

**Languages.** JavaScript (single-threaded event loop), Python (asyncio), Rust (tokio, async-std), C# (Task-based).

### The Actor Model

**Principle.** Each actor is an independent entity with its own state and mailbox. Actors communicate exclusively by sending messages. No shared state, no locks.

**Implementations.** Erlang/OTP (the original), Akka (JVM), Actix (Rust).

**When to use.** Distributed systems, fault-tolerant systems, systems with many independent entities (IoT, game servers, telecom switches). Erlang's "let it crash" philosophy -- actors fail independently and are restarted by supervisors.

### Data Race vs Race Condition

**Data race:** Two threads access the same memory, at least one writes, no synchronization. Undefined behavior. Prevented by Rust's type system, thread sanitizers (TSan), or correct use of synchronization.

**Race condition:** The program's correctness depends on the timing of operations, even if each individual access is synchronized. Example: check-then-act (if file exists, then open file -- another process may delete it between check and act). Harder to detect and fix.

## Part 3 -- Operating System Concepts

### Processes and Virtual Memory

A process is an instance of a running program. Each process has its own virtual address space -- an illusion that it has the entire memory to itself. The OS and hardware (MMU) translate virtual addresses to physical addresses via page tables.

**Page fault.** When a process accesses a virtual page that is not in physical memory, the OS loads it from disk (swap) or allocates a new page. Minor faults (page is in cache but not mapped) are fast. Major faults (page must be read from disk) are slow (milliseconds).

### System Calls

The boundary between user space and kernel space. A system call transfers control to the OS kernel to perform privileged operations: read/write files, create processes, allocate memory, send network packets.

**Common system calls.** open, read, write, close (files), fork, exec, wait (processes), socket, bind, listen, accept (networking), mmap, munmap (memory mapping), ioctl (device control).

**Cost.** System calls are expensive (context switch to kernel mode and back). Batch operations when possible. Use buffered I/O (stdio, BufReader) to reduce system call frequency.

### File Descriptors

In Unix, everything is a file. A file descriptor is a small integer that identifies an open file, socket, pipe, or device. stdin=0, stdout=1, stderr=2. The kernel maintains a file descriptor table per process.

**Resource limits.** Each process has a maximum number of open file descriptors (default 1024 on many systems, configurable). A server handling many connections may exhaust this limit.

### Signals

Asynchronous notifications sent to a process. SIGINT (Ctrl+C), SIGTERM (graceful shutdown request), SIGKILL (forced termination, cannot be caught), SIGSEGV (segmentation fault -- invalid memory access), SIGPIPE (write to a broken pipe).

**Signal safety.** Signal handlers run asynchronously, interrupting the normal flow. Only async-signal-safe functions (a restricted subset) may be called inside a signal handler. Setting a flag and returning is the safest pattern.

## Part 4 -- Compilation and Linking

### The Compilation Pipeline

```
Source code -> Lexer -> Tokens -> Parser -> AST -> Semantic Analysis ->
  IR (Intermediate Representation) -> Optimizer -> Code Generator -> Object Code ->
  Linker -> Executable
```

**Lexer (tokenizer).** Converts a character stream into a token stream. Identifies keywords, identifiers, literals, operators.

**Parser.** Converts the token stream into an Abstract Syntax Tree (AST). Enforces grammar rules. Reports syntax errors.

**Semantic analysis.** Type checking, name resolution, scope verification. Reports type errors and undeclared variables.

**Code generation.** Converts the AST (or IR) into machine code or bytecode.

**Optimization.** Transforms the IR to improve performance: dead code elimination, constant folding, loop unrolling, inlining, vectorization. LLVM provides a shared optimization framework used by Rust, Swift, and Clang.

### Static vs Dynamic Linking

**Static linking.** Library code is copied into the executable at link time. Produces a self-contained binary. Larger file size but no runtime dependency on shared libraries.

**Dynamic linking.** Library code is loaded at runtime from shared libraries (.so, .dll, .dylib). Smaller executables, shared memory across processes, but introduces dependency management (DLL hell, library version conflicts).

## Part 5 -- Networking Fundamentals

### The TCP/IP Stack

| Layer | Protocol | Function |
|---|---|---|
| Application | HTTP, DNS, SMTP | Application-level communication |
| Transport | TCP, UDP | Reliable (TCP) or unreliable (UDP) data transfer |
| Network | IP | Addressing and routing |
| Link | Ethernet, Wi-Fi | Physical data transmission |

### Sockets

A socket is an endpoint for network communication. The server binds to an address, listens, and accepts connections. The client connects to the server's address.

**TCP sockets.** Reliable, ordered byte stream. Connection-oriented (three-way handshake). Used for HTTP, database connections, file transfer.

**UDP sockets.** Unreliable, unordered datagrams. Connectionless. Used for DNS queries, video streaming, gaming (where latency matters more than reliability).

### HTTP

**Request-response protocol.** Client sends a request (method, path, headers, body). Server sends a response (status code, headers, body).

**Methods.** GET (retrieve), POST (create), PUT (replace), PATCH (partial update), DELETE (remove). Idempotent methods (GET, PUT, DELETE) can be retried safely.

**HTTP/2.** Multiplexing (multiple requests over one connection), header compression, server push. **HTTP/3.** QUIC (UDP-based transport), eliminates head-of-line blocking.

### DNS

**Domain Name System.** Translates human-readable names (example.com) to IP addresses. Hierarchical: root servers -> TLD servers (.com, .org) -> authoritative servers. Responses are cached at multiple levels (browser, OS, ISP).

### TLS

**Transport Layer Security.** Encrypts communication between client and server. TLS handshake establishes a shared secret via asymmetric cryptography (RSA or ECDHE). Subsequent data is encrypted with symmetric cryptography (AES). Certificates verify server identity.

## Part 6 -- The Hardware-Software Boundary

### CPU Caches

Modern CPUs have three cache levels (L1, L2, L3) between the core and main memory. L1 is fastest and smallest (32-64 KB), L3 is slowest and largest (8-64 MB).

**Cache line.** The unit of data transfer between cache and memory. Typically 64 bytes. Accessing one byte loads the entire cache line. Sequential access patterns exploit spatial locality; random access patterns defeat it.

**False sharing.** Two threads write to different variables that happen to share a cache line. The cache line bounces between cores (cache coherence protocol), destroying performance despite no logical data sharing. Fix: pad data to cache line boundaries.

### Memory-Mapped I/O

**mmap.** Maps a file or device into the process's virtual address space. Reads and writes to the mapped region are translated to file I/O by the OS. Efficient for large files (no copy into user-space buffers), enables shared memory between processes.

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Ignoring cache effects | 100x performance difference between cache hit and miss | Profile, use sequential access patterns |
| Deadlock from lock ordering | Thread A holds lock 1, wants lock 2; Thread B holds lock 2, wants lock 1 | Always acquire locks in the same global order |
| Blocking in async context | Blocks the entire runtime thread, starving other tasks | Use async versions of I/O operations |
| Fork without exec in multi-threaded program | Child inherits parent's mutex state, may deadlock | Use posix_spawn or fork+exec only |
| Unbounded channel growth | Producer faster than consumer, memory grows without limit | Use bounded channels with backpressure |
| Ignoring EINTR | System call interrupted by signal, returns error | Retry on EINTR |
| Not handling partial reads/writes | read() and write() may transfer fewer bytes than requested | Loop until all bytes are transferred |

## Cross-References

- **hopper agent:** Compiler design, language implementation, systems debugging.
- **turing agent:** Theoretical machine models that systems programming makes concrete.
- **dijkstra agent:** Structured concurrency, semaphore design, THE operating system.
- **knuth agent:** Low-level algorithm analysis, cache-aware algorithms.
- **algorithms-data-structures skill:** Algorithm selection depends on system-level characteristics (cache behavior, allocation cost).
- **debugging-testing skill:** Systems debugging techniques (gdb, rr, perf, strace).

## References

- Tanenbaum, A. S. & Bos, H. (2014). *Modern Operating Systems*. 4th edition. Pearson.
- Bryant, R. E. & O'Hallaron, D. R. (2015). *Computer Systems: A Programmer's Perspective*. 3rd edition. Pearson.
- Klabnik, S. & Nichols, C. (2023). *The Rust Programming Language*. 2nd edition. No Starch Press.
- Stevens, W. R. & Rago, S. A. (2013). *Advanced Programming in the UNIX Environment*. 3rd edition. Addison-Wesley.
- Kerrisk, M. (2010). *The Linux Programming Interface*. No Starch Press.
- Drepper, U. (2007). "What Every Programmer Should Know About Memory." Red Hat.
- Hopper, G. M. (1952). "The Education of a Computer." *Proceedings of the ACM National Conference*.
