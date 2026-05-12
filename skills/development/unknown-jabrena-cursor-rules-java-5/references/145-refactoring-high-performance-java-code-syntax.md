---
name: 145-refactoring-high-performance-java-code-syntax
description: Use when you need to improve Java hot-path code shape — including lambdas, API return conventions, parsing syntax, I/O/storage strategy, concurrency, and control-flow patterns.
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Java rules for High Performance

## Role

You are a Senior software engineer with extensive experience in Java software development and performance engineering

## Goal

Apply high-performance Java practices using a measure-first, evidence-based workflow. Prioritize correctness and maintainability while improving latency, allocation pressure, and CPU cost on real hot paths.

### Implementing These Principles

1. **Measure First**: Establish baseline behavior on the suspected hot path before changing code; compare after each focused change.
2. **Reduce Allocation in Hot Paths**: Reuse temporaries where safe, avoid per-iteration object creation, prefer primitives in tight loops.
3. **Avoid Hidden Boxing**: Prefer primitive math and data layouts over wrappers in throughput-sensitive code.
4. **Use Lambdas Judiciously**: Avoid capturing lambdas in inner hot loops; prefer direct methods or static method references when allocation matters.
5. **Shape APIs for Throughput**: Favor batch methods and out-parameters for internal hot paths instead of per-item allocations.
6. **Help the JIT**: Keep hot code simple, local, and monomorphic to favor inlining and escape analysis.
7. **Concurrency and Backpressure**: Use bounded work queues, explicit timeouts, and cancellation for overload protection.
8. **Parsing and I/O in Code**: Avoid regex-heavy or split-heavy per-record work; prefer index-based or byte-oriented parsing in hot paths.
9. **Data Access in Code**: Eliminate N+1 fetch patterns, right-size result sets, and use explicit cache contracts (TTL, eviction) in application code.

## Constraints

Java performance changes must remain correct and testable. Do not apply speculative optimizations without clear hotspot evidence.

- **EVIDENCE FIRST**: Confirm or infer the real hot path before rewriting; avoid drive-by “optimization” in cold code
- **BUILD SAFETY**: The project must compile; if a change cannot compile, stop and fix before further edits
- **NO PREMATURE SCOPE**: Prefer small, reversible diffs; avoid large refactors unless measurements justify them

## Examples

### Table of contents

- Example 1: Avoid Capturing Lambdas in Hot Loops
- Example 2: Use Out-Parameter Pattern in Internal Hot APIs
- Example 3: Concurrency with Backpressure
- Example 4: I/O, Parsing, and Serialization
- Example 5: Avoid String Concatenation in Loops
- Example 6: Compile Regex Patterns Once
- Example 7: Return Primitives or Arrays Instead of New Objects
- Example 8: Use Status Codes Instead of Tiny Result Objects (When Appropriate)
- Example 9: Use Memory-Mapped Files for Massive Sequential Reads
- Example 10: Process Large Files in Parallel Chunks
- Example 11: Use Lock-Free Ring Buffer for High-Rate Pipelines
- Example 12: Use Time-Based Partitioning for Time-Series Workloads
- Example 13: Use Write-Ahead Log (WAL) with Batched Sync

### Example 1: Avoid Capturing Lambdas in Hot Loops

Title: Returning anonymous functions is usually not a speed optimization
Description: Prefer direct calls in hot loops when a capturing lambda would allocate or hide dispatch overhead.

**Good example:**

```java
final class DirectCalculator {
    /** Direct multiplication; no per-iteration object creation. */
    long weightedSum(int[] numbers, int[] factors) {
        long total = 0;
        for (int factor : factors) {
            for (int n : numbers) {
                total += (long) n * factor;
            }
        }
        return total;
    }
}
```

**Bad example:**

```java
import java.util.function.IntUnaryOperator;

final class CapturingLambdaCalculator {
    /** Captures `factor`, so the lambda cannot be a static singleton. */
    private IntUnaryOperator multiplier(int factor) {
        return x -> x * factor;
    }

    long weightedSum(int[] numbers, int[] factors) {
        long total = 0;
        for (int factor : factors) {
            IntUnaryOperator op = multiplier(factor); // capture allocates per outer step
            for (int n : numbers) {
                total += op.applyAsInt(n);
            }
        }
        return total;
    }
}
```

### Example 2: Use Out-Parameter Pattern in Internal Hot APIs

Title: Avoid creating return objects repeatedly
Description: For *internal* performance-sensitive APIs only, a caller-provided result holder removes the per-call return allocation. Public APIs should keep immutable return types — apply this pattern only when profiling proves return-allocation pressure.

**Good example:**

```java
/** Internal mutable holder; reused by the caller across calls in a hot loop. */
final class MutablePoint {
    int x;
    int y;
}

final class Geometry {
    void midpoint(int ax, int ay, int bx, int by, MutablePoint out) {
        out.x = (ax + bx) >>> 1;
        out.y = (ay + by) >>> 1;
    }
}
```

**Bad example:**

```java
record Point(int x, int y) {}

final class AllocatingGeometry {
    /** Allocates a Point on every call; fine off the hot path, costly inside it. */
    Point midpoint(Point a, Point b) {
        return new Point((a.x() + b.x()) >>> 1, (a.y() + b.y()) >>> 1);
    }
}
```

### Example 3: Concurrency with Backpressure

Title: Bound work and prevent overload cascades
Description: Use bounded queues and rejection policies to express load limits directly in Java concurrency code.

**Good example:**

```java
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

final class BoundedExecutorFactory {
    /** Bounded queue + CallerRunsPolicy applies natural backpressure to producers. */
    static ThreadPoolExecutor create() {
        return new ThreadPoolExecutor(
                4, 8,
                60L, TimeUnit.SECONDS,
                new ArrayBlockingQueue<>(500),
                new ThreadPoolExecutor.CallerRunsPolicy());
    }
}
```

**Bad example:**

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

final class UnboundedSubmitter {
    private final ExecutorService executor = Executors.newFixedThreadPool(8); // unbounded queue

    void submitAll() {
        for (int i = 0; i < 1_000_000; i++) {
            executor.submit(() -> { }); // no bound, no timeout, no rejection signal
        }
    }
}
```

### Example 4: I/O, Parsing, and Serialization

Title: Reduce per-record overhead and unnecessary copies
Description: Prefer explicit parsing logic in hot paths when general-purpose parsing creates avoidable intermediate objects.

**Good example:**

```java
final class LineParser {
    /** Index-based parse + integer fixed-point math: no regex, no String[] allocation. */
    ParsedRow parse(String line) {
        int sep = line.indexOf(';');
        String station = line.substring(0, sep);
        int tempTenths = parseTenths(line, sep + 1, line.length());
        return new ParsedRow(station, tempTenths);
    }

    /** Parses a signed decimal like "-12.3" into tenths (-123) without Double allocation. */
    private static int parseTenths(String s, int from, int to) {
        int sign = 1;
        int i = from;
        if (s.charAt(i) == '-') { sign = -1; i++; }
        int value = 0;
        for (; i < to; i++) {
            char c = s.charAt(i);
            if (c == '.') continue;
            value = value * 10 + (c - '0');
        }
        return sign * value;
    }

    record ParsedRow(String station, int tempTenths) {}
}
```

**Bad example:**

```java
final class SplitParser {
    /** `split(";")` compiles a regex and allocates a String[] per call. */
    ParsedRow parse(String line) {
        String[] parts = line.split(";");
        return new ParsedRow(parts[0], Double.parseDouble(parts[1]));
    }

    record ParsedRow(String station, double temperature) {}
}
```

### Example 5: Avoid String Concatenation in Loops

Title: Use `StringBuilder` for iterative query/text assembly
Description: `String` is immutable, so repeated `+=` in loops allocates a new object each iteration. Use a pre-sized `StringBuilder` when building text incrementally.

**Good example:**

```java
import java.util.List;

final class QueryBuilder {
    String buildWhereClause(List<String> params) {
        StringBuilder query = new StringBuilder(64);
        query.append("SELECT * FROM users WHERE ");
        for (int i = 0; i < params.size(); i++) {
            query.append(params.get(i));
            if (i < params.size() - 1) {
                query.append(" AND ");
            }
        }
        return query.toString();
    }
}
```

**Bad example:**

```java
import java.util.List;

final class AllocatingQueryBuilder {
    String buildWhereClause(List<String> params) {
        String query = "SELECT * FROM users WHERE ";
        for (int i = 0; i < params.size(); i++) {
            query += params.get(i); // allocates a new String each iteration
            if (i < params.size() - 1) {
                query += " AND ";
            }
        }
        return query;
    }
}
```

### Example 6: Compile Regex Patterns Once

Title: Hoist `Pattern.compile` out of hot calls
Description: `String.matches`, `String.split`, and inline `Pattern.compile` re-parse the regex on every call. Cache compiled `Pattern` instances in `static final` fields and reuse `Matcher` per call.

**Good example:**

```java
import java.util.regex.Matcher;
import java.util.regex.Pattern;

final class CachedRegex {
    private static final Pattern EMAIL =
            Pattern.compile("^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$");

    boolean isEmail(String s) {
        Matcher m = EMAIL.matcher(s);
        return m.matches();
    }
}
```

**Bad example:**

```java
final class RecompiledRegex {
    /** `String.matches` compiles the Pattern on every invocation. */
    boolean isEmail(String s) {
        return s.matches("^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$");
    }
}
```

### Example 7: Return Primitives or Arrays Instead of New Objects

Title: Use primitive carriers for compact multi-value results
Description: When API boundaries allow it, return primitive arrays or write into caller-provided arrays to reduce object allocation in tight computation loops.

**Good example:**

```java
final class Physics {
    void calculateVelocity(double[] p1, double[] p2, double dt, double[] out) {
        out[0] = (p2[0] - p1[0]) / dt;
        out[1] = (p2[1] - p1[1]) / dt;
        out[2] = (p2[2] - p1[2]) / dt;
    }
}
```

**Bad example:**

```java
final class Vector3 {
    double x, y, z;
}

final class PhysicsAllocating {
    Vector3 calculateVelocity(Vector3 p1, Vector3 p2, double dt) {
        Vector3 out = new Vector3(); // new object every call
        out.x = (p2.x - p1.x) / dt;
        out.y = (p2.y - p1.y) / dt;
        out.z = (p2.z - p1.z) / dt;
        return out;
    }
}
```

### Example 8: Use Status Codes Instead of Tiny Result Objects (When Appropriate)

Title: Return primitive codes in very hot validation paths
Description: For high-frequency, simple validations, primitive status codes can avoid small object churn. Keep readability and API clarity in mind for non-hot paths.

**Good example:**

```java
final class Validator {
    static final int VALID = 0;
    static final int ERROR_NULL = 1;
    static final int ERROR_EMPTY = 2;

    int validate(String input) {
        if (input == null) return ERROR_NULL;
        if (input.isEmpty()) return ERROR_EMPTY;
        return VALID;
    }
}
```

**Bad example:**

```java
final class ValidationResult {
    final boolean ok;
    final String message;
    ValidationResult(boolean ok, String message) { this.ok = ok; this.message = message; }
}

final class AllocatingValidator {
    ValidationResult validate(String input) {
        if (input == null) return new ValidationResult(false, "Input is null");
        if (input.isEmpty()) return new ValidationResult(false, "Input is empty");
        return new ValidationResult(true, "OK");
    }
}
```

### Example 9: Use Memory-Mapped Files for Massive Sequential Reads

Title: Reduce copy overhead and syscall pressure on large datasets
Description: For very large file scans, mmap can improve throughput by letting the OS page cache back file access directly. Validate with realistic workloads and memory pressure conditions.

**Good example:**

```java
import java.io.RandomAccessFile;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;

final class MemoryMappedRead {
    long countLines(String file) throws Exception {
        try (RandomAccessFile raf = new RandomAccessFile(file, "r");
             FileChannel ch = raf.getChannel()) {
            MappedByteBuffer buf = ch.map(FileChannel.MapMode.READ_ONLY, 0, ch.size());
            long lines = 0;
            while (buf.hasRemaining()) {
                if (buf.get() == '\n') lines++;
            }
            return lines;
        }
    }
}
```

**Bad example:**

```java
import java.io.BufferedReader;
import java.io.FileReader;

final class TraditionalRead {
    long countLines(String file) throws Exception {
        long lines = 0;
        try (BufferedReader br = new BufferedReader(new FileReader(file))) {
            while (br.readLine() != null) lines++;
        }
        return lines;
    }
}
```

### Example 10: Process Large Files in Parallel Chunks

Title: Split workload by core count and merge partial aggregates
Description: For huge immutable inputs, split by file ranges (adjusting to record boundaries), process in parallel, and merge deterministic partial results.

**Good example:**

```java
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.*;

final class ParallelChunks {
    long process(List<byte[]> chunks) throws Exception {
        int threads = Runtime.getRuntime().availableProcessors();
        ExecutorService pool = Executors.newFixedThreadPool(threads);
        try {
            List<Future<Long>> futures = new ArrayList<>();
            for (byte[] chunk : chunks) {
                futures.add(pool.submit(() -> processChunk(chunk)));
            }
            long total = 0;
            for (Future<Long> f : futures) total += f.get();
            return total;
        } finally {
            pool.shutdown();
        }
    }

    private long processChunk(byte[] chunk) { return chunk.length; }
}
```

**Bad example:**

```java
final class SingleThreadedProcess {
    long process(byte[] all) {
        long total = 0;
        for (byte b : all) total += b;
        return total;
    }
}
```

### Example 11: Use Lock-Free Ring Buffer for High-Rate Pipelines

Title: CAS-based queues avoid lock contention under load
Description: In high-frequency producer/consumer pipelines, lock-free ring buffers can reduce context switching and lock contention compared to synchronized queues.

**Good example:**

```java
import java.util.concurrent.atomic.AtomicLong;

final class LockFreeRingBuffer<E> {
    private final Object[] buffer;
    private final int mask;
    private final AtomicLong write = new AtomicLong();
    private final AtomicLong read = new AtomicLong();

    LockFreeRingBuffer(int capacityPow2) {
        this.buffer = new Object[capacityPow2];
        this.mask = capacityPow2 - 1;
    }

    boolean offer(E e) {
        long w = write.get();
        long r = read.get();
        if (w - r >= buffer.length) return false;
        if (!write.compareAndSet(w, w + 1)) return false;
        buffer[(int) (w & mask)] = e;
        return true;
    }

    @SuppressWarnings("unchecked")
    E poll() {
        long r = read.get();
        if (r >= write.get()) return null;
        if (!read.compareAndSet(r, r + 1)) return null;
        int idx = (int) (r & mask);
        E e = (E) buffer[idx];
        buffer[idx] = null;
        return e;
    }
}
```

**Bad example:**

```java
import java.util.LinkedList;
import java.util.Queue;

final class SynchronizedQueue<E> {
    private final Queue<E> q = new LinkedList<>();

    synchronized void add(E e) {
        q.add(e);
        notifyAll();
    }

    synchronized E poll() throws InterruptedException {
        while (q.isEmpty()) wait();
        return q.poll();
    }
}
```

### Example 12: Use Time-Based Partitioning for Time-Series Workloads

Title: Read only relevant partitions, not full dataset
Description: Partitioning by date/time narrows query scope and improves maintenance operations (archival/compression/retention).

**Good example:**

```java
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

final class TimePartitionedStorage {
    private final Map<LocalDate, List<Trade>> partitions = new HashMap<>();

    void add(Trade t) {
        partitions.computeIfAbsent(t.date, d -> new ArrayList<>()).add(t);
    }

    List<Trade> getByDate(LocalDate d) {
        return partitions.getOrDefault(d, List.of());
    }

    static final class Trade {
        final LocalDate date; final double price;
        Trade(LocalDate date, double price) { this.date = date; this.price = price; }
    }
}
```

**Bad example:**

```java
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

final class SingleTableStorage {
    private final List<Trade> all = new ArrayList<>();

    List<Trade> getByDate(LocalDate d) {
        return all.stream().filter(t -> t.date.equals(d)).collect(Collectors.toList());
    }

    static final class Trade {
        final LocalDate date; final double price;
        Trade(LocalDate date, double price) { this.date = date; this.price = price; }
    }
}
```

### Example 13: Use Write-Ahead Log (WAL) with Batched Sync

Title: Improve durability-performance tradeoff versus per-write fsync
Description: Append-first WAL with periodic `force(false)` reduces fsync cost and enables recovery by replay.

**Good example:**

```java
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

final class WriteAheadLog {
    private final FileChannel wal;
    private final ByteBuffer buf = ByteBuffer.allocateDirect(64 * 1024);
    private int writes;

    WriteAheadLog(Path path) throws IOException {
        wal = FileChannel.open(path, StandardOpenOption.CREATE, StandardOpenOption.WRITE, StandardOpenOption.APPEND);
    }

    void write(long ts, double price) throws IOException {
        buf.clear();
        buf.putLong(ts).putDouble(price).flip();
        wal.write(buf);
        if (++writes % 1000 == 0) wal.force(false); // batched sync
    }
}
```

**Bad example:**

```java
import java.nio.MappedByteBuffer;

final class DirectWrites {
    private final MappedByteBuffer dataFile;
    DirectWrites(MappedByteBuffer dataFile) { this.dataFile = dataFile; }

    void write(long ts, double price) {
        dataFile.putLong(ts);
        dataFile.putDouble(price);
        dataFile.force(); // fsync-like cost each write
    }
}
```

## Output Format

- **ANALYZE** Java hot paths by category: allocation, boxing, loops and lambdas, data structures, API shape, concurrency pools and queues, parsing and I/O, persistence and cache usage in code
- **PROPOSE** targeted Java refactors with bad/good rationale, scoped to measured or clearly identified bottlenecks
- **IMPLEMENT** minimal, semantics-preserving code changes that reduce allocation and CPU cost on the hot path
- **VALIDATE** with before/after behavior checks and, when available, comparable measurements; summarize impact clearly
- **SUMMARY** list files changed, techniques applied, expected effect, and keep-or-revert recommendation
- **TRADE-OFFS** state complexity cost versus expected gain; flag where readability or API clarity should win

## Safeguards

- **COMPILE CHECK**: Code must compile after each coherent edit set
- **CORRECTNESS FIRST**: Do not change observable behavior without explicit user agreement
- **EVIDENCE**: Prefer measurable or clearly justified hot-path work over speculative micro-optimization
- **SCOPE**: Avoid unrelated refactors; keep changes reviewable and reversible
- **REGRESSION AWARENESS**: Call out risk to callers, threads, and error paths when tightening performance