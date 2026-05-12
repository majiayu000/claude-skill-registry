---
name: 145-refactoring-high-performance-java-cpu
description: Use when you need to improve Java CPU hot paths — including bit-level parsing, zero-copy/direct buffers, branchless arithmetic, loop unrolling, Unsafe caution, and SIMD/vectorization patterns.
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

- Example 1: Use SWAR-Style Delimiter Search in Byte Parsing
- Example 2: Use Branchless Arithmetic in Hot Paths (When Proven)
- Example 3: Avoid `sun.misc.Unsafe` Unless There Is Hard Evidence
- Example 4: Use Manual Loop Unrolling Sparingly
- Example 5: Use Zero-Copy and Direct Buffers for Large Transfers
- Example 6: Use Panama Vector API for Numeric Kernels

### Example 1: Use SWAR-Style Delimiter Search in Byte Parsing

Title: Scan multiple bytes per iteration when parsing hot streams
Description: SWAR (SIMD Within A Register) can speed delimiter detection by evaluating 8 bytes at once. Keep a simpler fallback implementation for maintainability and tests.

**Good example:**

```java
final class SWARSearch {
    private static final long SEMI = 0x3B3B3B3B3B3B3B3BL; // ';'

    int findSemicolon(long[] words, int startWord) {
        for (int i = startWord; i < words.length; i++) {
            long x = words[i] ^ SEMI;
            long m = (x - 0x0101010101010101L) & ~x & 0x8080808080808080L;
            if (m != 0) return i * 8 + (Long.numberOfTrailingZeros(m) >>> 3);
        }
        return -1;
    }
}
```

**Bad example:**

```java
final class ByteByByteSearch {
    int findSemicolon(byte[] data, int start) {
        for (int i = start; i < data.length; i++) {
            if (data[i] == ';') return i;
        }
        return -1;
    }
}
```

### Example 2: Use Branchless Arithmetic in Hot Paths (When Proven)

Title: Reduce branch misprediction costs for tiny numeric kernels
Description: Branchless code can help in highly predictable inner loops, but can hurt readability. Apply only with profiling evidence.

**Good example:**

```java
final class BranchlessMath {
    int abs(int x) {
        int mask = x >> 31;
        return (x + mask) ^ mask;
    }

    int max(int a, int b) {
        int diff = a - b;
        int sign = diff >> 31;
        return a - (diff & sign);
    }
}
```

**Bad example:**

```java
final class BranchyMath {
    int abs(int x) { return x < 0 ? -x : x; }
    int max(int a, int b) { return a > b ? a : b; }
}
```

### Example 3: Avoid `sun.misc.Unsafe` Unless There Is Hard Evidence

Title: Prefer safe code or supported APIs before unsafe memory access
Description: `Unsafe` can improve low-level throughput but increases portability and safety risk. Use only for proven bottlenecks and isolate behind well-tested abstractions.

**Good example:**

```java
final class SafeArraySum {
    long sum(byte[] data) {
        long s = 0;
        for (byte b : data) s += b;
        return s;
    }
}
```

**Bad example:**

```java
import sun.misc.Unsafe;
import java.lang.reflect.Field;

final class UnsafeArraySum {
    private static final Unsafe U;
    private static final long BASE;
    static {
        try {
            Field f = Unsafe.class.getDeclaredField("theUnsafe");
            f.setAccessible(true);
            U = (Unsafe) f.get(null);
            BASE = U.arrayBaseOffset(byte[].class);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    long sum(byte[] data) {
        long s = 0;
        for (int i = 0; i < data.length; i++) s += U.getByte(data, BASE + i);
        return s;
    }
}
```

### Example 4: Use Manual Loop Unrolling Sparingly

Title: Trade readability for throughput only in proven kernels
Description: Manual unrolling can reduce loop overhead and improve ILP on tight arithmetic kernels. Keep it localized and benchmarked.

**Good example:**

```java
final class UnrolledSum {
    int sum(int[] a) {
        int s0 = 0, s1 = 0, s2 = 0, s3 = 0;
        int i = 0, n = a.length - 3;
        for (; i < n; i += 4) {
            s0 += a[i];
            s1 += a[i + 1];
            s2 += a[i + 2];
            s3 += a[i + 3];
        }
        for (; i < a.length; i++) s0 += a[i];
        return s0 + s1 + s2 + s3;
    }
}
```

**Bad example:**

```java
final class SimpleSum {
    int sum(int[] a) {
        int s = 0;
        for (int i = 0; i < a.length; i++) s += a[i];
        return s;
    }
}
```

### Example 5: Use Zero-Copy and Direct Buffers for Large Transfers

Title: Reduce userspace copies with `transferTo` and direct buffers
Description: For large file/network transfers, `FileChannel.transferTo(...)` and direct buffers can reduce copy overhead and improve throughput.

**Good example:**

```java
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.channels.SocketChannel;

final class ZeroCopyTransfer {
    private final ByteBuffer direct = ByteBuffer.allocateDirect(8192);

    void send(FileChannel file, SocketChannel socket) throws IOException {
        long pos = 0;
        long size = file.size();
        while (pos < size) {
            pos += file.transferTo(pos, size - pos, socket);
        }
    }
}
```

**Bad example:**

```java
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.channels.SocketChannel;
import java.nio.charset.StandardCharsets;

final class MultipleCopyTransfer {
    void send(SocketChannel socket, String payload) throws IOException {
        byte[] bytes = payload.getBytes(StandardCharsets.UTF_8);
        ByteBuffer heap = ByteBuffer.allocate(bytes.length);
        heap.put(bytes);
        heap.flip();
        socket.write(heap);
    }
}
```

### Example 6: Use Panama Vector API for Numeric Kernels

Title: Vectorize arithmetic-heavy loops when available
Description: For hot numeric loops, the Vector API can exploit hardware SIMD and reduce per-element instruction overhead. Keep scalar fallback paths.

**Good example:**

```java
import jdk.incubator.vector.DoubleVector;
import jdk.incubator.vector.VectorOperators;
import jdk.incubator.vector.VectorSpecies;

final class VectorizedReturns {
    private static final VectorSpecies<Double> SPECIES = DoubleVector.SPECIES_PREFERRED;

    void calc(double[] prices, double[] returns) {
        int i = 1;
        int limit = SPECIES.loopBound(prices.length - 1);
        for (; i < limit; i += SPECIES.length()) {
            DoubleVector p = DoubleVector.fromArray(SPECIES, prices, i);
            DoubleVector prev = DoubleVector.fromArray(SPECIES, prices, i - 1);
            p.sub(prev).div(prev).intoArray(returns, i);
        }
        for (; i < prices.length; i++) {
            returns[i] = (prices[i] - prices[i - 1]) / prices[i - 1];
        }
    }
}
```

**Bad example:**

```java
final class ScalarReturns {
    void calc(double[] prices, double[] returns) {
        for (int i = 1; i < prices.length; i++) {
            returns[i] = (prices[i] - prices[i - 1]) / prices[i - 1];
        }
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