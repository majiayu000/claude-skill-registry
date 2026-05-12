---
name: 145-refactoring-high-performance-java-memory-allocation
description: Use when you need to improve Java memory behavior in hot paths — including allocation reduction, primitive data choices, escape analysis, collection sizing, data layout, and deduplication patterns.
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

- Example 1: Reuse Temporary Objects in Confined Hot Paths
- Example 2: Prefer Primitives over Wrappers
- Example 3: Write Escape-Analysis-Friendly Code
- Example 4: Avoid Boxed Streams in Tight Hot Paths
- Example 5: Pre-Size Collections When Capacity Is Known
- Example 6: Reuse Expensive Objects with Thread Confinement
- Example 7: Use Flyweight Cache for Repeated Immutable Objects
- Example 8: Use Mutable In-Place Updates When Safe
- Example 9: Pool Expensive Objects Only When Justified
- Example 10: Pack Multiple Small Values into Primitives
- Example 11: Use Mutable Builder Reuse in Internal Pipelines
- Example 12: Prefer Flat Arrays (SoA) over Object Arrays in Batch Workloads
- Example 13: Use Open Addressing for Specialized Hot-Key Aggregation
- Example 14: Escape Analysis Deep Dive: Core Escape Conditions
- Example 15: Field Assignment Escape vs Local Non-Escape
- Example 16: Method-Call Escape vs Non-Retaining Method Call
- Example 17: Iterator Anonymous Class Escape
- Example 18: StringBuilder Escape vs `toString` Non-Escape
- Example 19: Boxed List Escape vs Primitive Array
- Example 20: Vector Intermediate Escape Chain vs In-Place Mutation
- Example 21: Lambda Return/List Capture Deep Dive
- Example 22: Record-Specific Escape Analysis Discussion
- Example 23: Exception Object Escape vs Throw Immediately
- Example 24: Scalar Replacement: TempData Object vs Locals
- Example 25: JVM Escape Analysis Verification Flags and Demo
- Example 26: Use Columnar Layouts for Analytical Access Patterns
- Example 27: Use Symbol Interning via IDs

### Example 1: Reuse Temporary Objects in Confined Hot Paths

Title: Avoid repeated temporary allocations in hot calls
Description: Reuse mutable helpers only when they are confined to a single thread (e.g. instance per worker, or `ThreadLocal`). Pre-size the buffer to skip early growth.

**Good example:**

```java
/** Caller-confined: one instance per thread/worker; not thread-safe. */
final class CoordinateFormatter {
    private final StringBuilder sb = new StringBuilder(32); // pre-sized

    String format(double x, double y) {
        sb.setLength(0);
        sb.append('(').append(x).append(", ").append(y).append(')');
        return sb.toString();
    }
}
```

**Bad example:**

```java
final class AllocatingFormatter {
    String format(double x, double y) {
        StringBuilder sb = new StringBuilder(); // new buffer + grow per call
        sb.append('(').append(x).append(", ").append(y).append(')');
        return sb.toString();
    }
}
```

### Example 2: Prefer Primitives over Wrappers

Title: Reduce boxing churn and GC pressure
Description: Wrapper types in tight numeric loops cause hidden boxing on each `+=`, plus pointer chasing that hurts cache locality. Use `int[]`/`long[]` and primitive locals instead.

**Good example:**

```java
final class PrimitiveAccumulator {
    int sumValues(int[] numbers) {
        int sum = 0;
        for (int n : numbers) {
            sum += n;
        }
        return sum;
    }
}
```

**Bad example:**

```java
import java.util.List;

final class BoxingAccumulator {
    int sumValues(List<Integer> numbers) {
        Integer sum = 0; // wrapper churn
        for (Integer n : numbers) {
            sum += n;
        }
        return sum;
    }
}
```

### Example 3: Write Escape-Analysis-Friendly Code

Title: Keep temporary objects local and non-escaping
Description: Helper objects that never leave the method are candidates for scalar replacement (no heap allocation). Returning, storing in a field, or publishing to another thread defeats it.

**Good example:**

```java
import java.util.List;

final class LocalComputation {
    /**
     * The Iterator allocated by `for-each` is fully consumed inside this method
     * and never escapes; HotSpot can typically scalar-replace it.
     */
    int firstIndexOf(List<String> items, String target) {
        int idx = 0;
        for (String s : items) {
            if (s.equals(target)) {
                return idx;
            }
            idx++;
        }
        return -1;
    }
}
```

**Bad example:**

```java
import java.util.Iterator;
import java.util.List;

final class EscapingComputation {
    /** The Iterator escapes to the caller and cannot be scalar-replaced. */
    Iterator<String> openIterator(List<String> items) {
        return items.iterator();
    }
}
```

### Example 4: Avoid Boxed Streams in Tight Hot Paths

Title: Prefer primitive loops when profiling shows stream/boxing overhead
Description: Streams are great for readability off the hot path. In frequently executed numeric code, a primitive `for` loop avoids `Spliterator`/pipeline overhead and any `Integer` boxing introduced by `boxed()` or `Stream<Integer>`.

**Good example:**

```java
import java.util.List;

final class LoopSquares {
    /** Single unbox per element, no Spliterator, no pipeline. */
    long sumSquares(List<Integer> values) {
        long sum = 0;
        for (int v : values) {
            sum += (long) v * v;
        }
        return sum;
    }
}
```

**Bad example:**

```java
import java.util.List;

final class BoxedStreamSquares {
    /** `Stream<Integer>` traversal boxes/unboxes every element. */
    long sumSquares(List<Integer> values) {
        return values.stream()
                .mapToLong(v -> (long) v * v) // unbox via Integer::intValue per element
                .sum();
    }
}
```

### Example 5: Pre-Size Collections When Capacity Is Known

Title: Avoid repeated rehash and array-grow churn
Description: `HashMap` rehashes (and `ArrayList` reallocates) as elements are added past their threshold. When the final size is known or bounded, sizing the collection up front removes those internal allocations.

**Good example:**

```java
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

final class PreSizedCollections {
    Map<String, Integer> indexBy(List<String> keys) {
        // load factor 0.75 -> capacity = ceil(size / 0.75) + 1
        Map<String, Integer> index = new HashMap<>(keys.size() * 4 / 3 + 1);
        int i = 0;
        for (String k : keys) {
            index.put(k, i++);
        }
        return index;
    }

    List<String> copyOf(List<String> source) {
        List<String> out = new ArrayList<>(source.size());
        out.addAll(source);
        return out;
    }
}
```

**Bad example:**

```java
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

final class GrowingCollections {
    Map<String, Integer> indexBy(List<String> keys) {
        Map<String, Integer> index = new HashMap<>(); // default 16; rehashes as it grows
        int i = 0;
        for (String k : keys) {
            index.put(k, i++);
        }
        return index;
    }

    List<String> copyOf(List<String> source) {
        List<String> out = new ArrayList<>(); // default 10; grows by 1.5x repeatedly
        out.addAll(source);
        return out;
    }
}
```

### Example 6: Reuse Expensive Objects with Thread Confinement

Title: Avoid creating `MessageDigest` per request
Description: `MessageDigest.getInstance(...)` is relatively expensive and can become visible under heavy request volume. Reuse a digest instance per thread (`ThreadLocal`) or per worker object and call `reset()` between uses.

**Good example:**

```java
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.HexFormat;

final class DigestService {
    private static final ThreadLocal<MessageDigest> SHA256 =
            ThreadLocal.withInitial(() -> {
                try {
                    return MessageDigest.getInstance("SHA-256");
                } catch (NoSuchAlgorithmException e) {
                    throw new IllegalStateException(e);
                }
            });

    String hashHex(byte[] payload) {
        MessageDigest md = SHA256.get();
        md.reset();
        byte[] out = md.digest(payload);
        return HexFormat.of().formatHex(out);
    }
}
```

**Bad example:**

```java
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.HexFormat;

final class AllocatingDigestService {
    String hashHex(byte[] payload) throws NoSuchAlgorithmException {
        MessageDigest md = MessageDigest.getInstance("SHA-256"); // new instance per call
        byte[] out = md.digest(payload);
        return HexFormat.of().formatHex(out);
    }
}
```

### Example 7: Use Flyweight Cache for Repeated Immutable Objects

Title: Deduplicate objects created from the same key
Description: If the same immutable object is loaded repeatedly by key (e.g., texture/config/schema), cache it with `computeIfAbsent` to avoid duplicate allocations and repeated initialization work.

**Good example:**

```java
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

final class TextureCache {
    private final Map<String, Texture> cache = new ConcurrentHashMap<>();

    Texture loadTexture(String path) {
        return cache.computeIfAbsent(path, Texture::new);
    }

    static final class Texture {
        private final String path;
        Texture(String path) { this.path = path; }
        String path() { return path; }
    }
}
```

**Bad example:**

```java
final class TextureLoader {
    Texture loadTexture(String path) {
        return new Texture(path); // allocates duplicate immutable objects repeatedly
    }

    static final class Texture {
        private final String path;
        Texture(String path) { this.path = path; }
    }
}
```

### Example 8: Use Mutable In-Place Updates When Safe

Title: Reuse existing object instances in internal hot loops
Description: In internal performance-sensitive code paths, mutating a caller-owned mutable object can remove repeated result allocations. Use this only with clear ownership/thread-safety boundaries.

**Good example:**

```java
import java.util.Calendar;
import java.util.Date;

final class DateCalculator {
    private final Calendar cal = Calendar.getInstance();

    /** Caller owns `date`; method mutates in place to avoid allocating a new Date. */
    void addDaysInPlace(Date date, int days) {
        cal.setTime(date);
        cal.add(Calendar.DAY_OF_MONTH, days);
        date.setTime(cal.getTimeInMillis());
    }
}
```

**Bad example:**

```java
import java.util.Calendar;
import java.util.Date;

final class AllocatingDateCalculator {
    Date addDays(Date date, int days) {
        Calendar cal = Calendar.getInstance(); // allocates per call
        cal.setTime(date);
        cal.add(Calendar.DAY_OF_MONTH, days);
        return cal.getTime(); // creates new Date object
    }
}
```

### Example 9: Pool Expensive Objects Only When Justified

Title: Borrow-return pattern for costly resources
Description: Object pools add complexity and should be used for expensive-to-create objects with measurable lifecycle overhead.

**Good example:**

```java
import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;

final class ConnectionPool {
    private final Queue<Connection> pool = new ConcurrentLinkedQueue<>();
    private final int maxSize = 16;

    Connection borrow(String url) {
        Connection c = pool.poll();
        return c != null ? c : new Connection(url);
    }

    void release(Connection c) {
        if (pool.size() < maxSize) {
            c.reset();
            pool.offer(c);
        }
    }

    static final class Connection {
        private final String url;
        Connection(String url) { this.url = url; }
        void reset() {}
    }
}
```

**Bad example:**

```java
final class ConnectionFactory {
    Connection open(String url) {
        return new Connection(url); // expensive object recreated every call
    }

    static final class Connection {
        Connection(String url) {}
    }
}
```

### Example 10: Pack Multiple Small Values into Primitives

Title: Avoid tiny wrapper objects for hot-path data transport
Description: For compact value sets (e.g., RGB, pair of ints), bit-packing into `int`/`long` can remove allocations and improve memory locality.

**Good example:**

```java
final class ColorCodec {
    int packArgb(int r, int g, int b) {
        return (0xFF << 24) | (r << 16) | (g << 8) | b;
    }

    int red(int argb)   { return (argb >>> 16) & 0xFF; }
    int green(int argb) { return (argb >>> 8) & 0xFF; }
    int blue(int argb)  { return argb & 0xFF; }
}
```

**Bad example:**

```java
final class Color {
    int r, g, b;
}

final class ColorFactory {
    Color pixel(int r, int g, int b) {
        Color c = new Color(); // allocation per pixel
        c.r = r; c.g = g; c.b = b;
        return c;
    }
}
```

### Example 11: Use Mutable Builder Reuse in Internal Pipelines

Title: Accumulate state once, avoid repeated immutable copies
Description: For internal assembly flows, reusing a mutable builder object avoids repeated deep-copy allocation patterns.

**Good example:**

```java
import java.util.ArrayList;
import java.util.List;

final class QueryBuilder {
    private final List<String> filters = new ArrayList<>();

    QueryBuilder addFilter(String field, String value) {
        filters.add(field + "=" + value);
        return this;
    }

    Query build() { return new Query(List.copyOf(filters)); }
    void reset() { filters.clear(); }

    record Query(List<String> filters) {}
}
```

**Bad example:**

```java
import java.util.ArrayList;
import java.util.List;

final class AllocatingQueryChain {
    Query addFilter(Query query, String filter) {
        List<String> copy = new ArrayList<>(query.filters()); // copy each step
        copy.add(filter);
        return new Query(copy);
    }

    record Query(List<String> filters) {}
}
```

### Example 12: Prefer Flat Arrays (SoA) over Object Arrays in Batch Workloads

Title: Improve locality and avoid per-element object churn
Description: Structure-of-Arrays keeps columns contiguous and avoids object header/pointer overhead common in object-per-element layouts.

**Good example:**

```java
final class ParticleSystemSoA {
    double[] x, y, z;
    double[] vx, vy, vz;
    boolean[] active;
    int size;

    void step() {
        for (int i = 0; i < size; i++) {
            if (active[i]) {
                x[i] += vx[i];
                y[i] += vy[i];
                z[i] += vz[i];
            }
        }
    }
}
```

**Bad example:**

```java
final class ParticleSystemAoS {
    Particle[] particles;

    void step() {
        for (Particle p : particles) {
            if (p.active) {
                p.x += p.vx;
                p.y += p.vy;
                p.z += p.vz;
            }
        }
    }

    static final class Particle {
        double x, y, z, vx, vy, vz;
        boolean active;
    }
}
```

### Example 13: Use Open Addressing for Specialized Hot-Key Aggregation

Title: Avoid boxing and object-heavy maps in extreme hot loops
Description: For highly specialized workloads (e.g., fixed-shape aggregations), open-addressing tables can outperform generic `HashMap` by reducing allocations and pointer indirection.

**Good example:**

```java
import java.util.Arrays;

final class StatsTable {
    private static final int SIZE = 1 << 14;
    private static final int MASK = SIZE - 1;
    private final long[] keys = new long[SIZE];
    private final int[] counts = new int[SIZE];
    private final long[] sums = new long[SIZE];

    void add(long hash, int value) {
        int idx = (int) hash & MASK;
        while (keys[idx] != 0 && keys[idx] != hash) {
            idx = (idx + 1) & MASK;
        }
        if (keys[idx] == 0) keys[idx] = hash;
        counts[idx]++;
        sums[idx] += value;
    }
}
```

**Bad example:**

```java
import java.util.HashMap;
import java.util.Map;

final class StandardStats {
    private final Map<String, Stats> map = new HashMap<>();

    void add(String key, int value) {
        map.computeIfAbsent(key, k -> new Stats()).add(value);
    }

    static final class Stats {
        int count; long sum;
        void add(int v) { count++; sum += v; }
    }
}
```

### Example 14: Escape Analysis Deep Dive: Core Escape Conditions

Title: Group the four conditions that force heap allocation
Description: An object is considered escaping (and less likely to be scalar-replaced) when: 1) it is returned from the method, 2) it is assigned to a field, 3) it is passed to code that may retain it, 4) it is captured by a lambda/anonymous class that outlives the scope.

**Good example:**

```java
final class NoEscapeSummary {
    int compute(int x, int y) {
        Point p = new Point(x, y); // local helper
        return p.x * p.x + p.y * p.y; // p does not escape this method
    }

    static final class Point {
        final int x, y;
        Point(int x, int y) { this.x = x; this.y = y; }
    }
}
```

**Bad example:**

```java
final class EscapeSummary {
    private Point last;

    Point compute(int x, int y) {
        Point p = new Point(x, y);
        last = p;      // escapes via field assignment
        return p;      // escapes via return
    }

    static final class Point {
        final int x, y;
        Point(int x, int y) { this.x = x; this.y = y; }
    }
}
```

### Example 15: Field Assignment Escape vs Local Non-Escape

Title: Contrast `EscapeExample` and `NoEscapeExample` style
Description: 

**Good example:**

```java
final class NoEscapeExample {
    int calculateDistance(int x1, int y1, int x2, int y2) {
        Point p1 = new Point(x1, y1);
        Point p2 = new Point(x2, y2);
        int dx = p2.x - p1.x;
        int dy = p2.y - p1.y;
        return dx * dx + dy * dy;
    }

    static final class Point {
        final int x, y;
        Point(int x, int y) { this.x = x; this.y = y; }
    }
}
```

**Bad example:**

```java
final class EscapeExample {
    private Point lastPoint;

    Point calculatePoint(int x, int y) {
        Point p = new Point(x * 2, y * 2);
        lastPoint = p;  // escapes to object field
        return p;       // escapes to caller
    }

    static final class Point {
        final int x, y;
        Point(int x, int y) { this.x = x; this.y = y; }
    }
}
```

### Example 16: Method-Call Escape vs Non-Retaining Method Call

Title: Passing local objects is safe only if callees do not retain them
Description: 

**Good example:**

```java
final class NoMethodEscape {
    int processPoint(int x, int y) {
        Point p = new Point(x, y);
        return lengthSquared(p); // callee only reads p
    }

    private int lengthSquared(Point p) {
        return p.x * p.x + p.y * p.y;
    }

    static final class Point {
        final int x, y;
        Point(int x, int y) { this.x = x; this.y = y; }
    }
}
```

**Bad example:**

```java
import java.util.ArrayList;
import java.util.List;

final class MethodEscape {
    private final List<Point> points = new ArrayList<>();

    void addPoint(int x, int y) {
        Point p = new Point(x, y);
        points.add(p); // escapes via retained collection
    }

    static final class Point {
        final int x, y;
        Point(int x, int y) { this.x = x; this.y = y; }
    }
}
```

### Example 17: Iterator Anonymous Class Escape

Title: Returning iterator objects forces escaping state
Description: 

**Good example:**

```java
import java.util.List;

final class NoIteratorEscape {
    void processItems(List<String> items) {
        for (int i = 0; i < items.size(); i++) {
            consume(items.get(i));
        }
    }

    private void consume(String s) {}
}
```

**Bad example:**

```java
import java.util.Iterator;
import java.util.List;

final class IteratorEscape {
    Iterator<String> getIterator(List<String> items) {
        return new Iterator<>() {
            int index = 0;
            @Override public boolean hasNext() { return index < items.size(); }
            @Override public String next() { return items.get(index++); }
        }; // anonymous iterator escapes
    }
}
```

### Example 18: StringBuilder Escape vs `toString` Non-Escape

Title: Return final String, not mutable builder objects
Description: 

**Good example:**

```java
final class StringBuilderNoEscape {
    String buildString(String a, String b) {
        StringBuilder sb = new StringBuilder();
        sb.append(a).append(' ').append(b);
        return sb.toString(); // builder stays local
    }
}
```

**Bad example:**

```java
final class StringBuilderEscape {
    StringBuilder buildString(String a, String b) {
        StringBuilder sb = new StringBuilder();
        sb.append(a).append(' ').append(b);
        return sb; // mutable helper escapes
    }
}
```

### Example 19: Boxed List Escape vs Primitive Array

Title: Avoid wrapper-object escape through collections when possible
Description: 

**Good example:**

```java
final class PrimitiveSquares {
    int[] calculateSquares(int[] numbers) {
        int[] out = new int[numbers.length];
        for (int i = 0; i < numbers.length; i++) {
            out[i] = numbers[i] * numbers[i];
        }
        return out;
    }
}
```

**Bad example:**

```java
import java.util.ArrayList;
import java.util.List;

final class BoxingEscape {
    List<Integer> calculateSquares(int[] numbers) {
        List<Integer> out = new ArrayList<>();
        for (int n : numbers) {
            out.add(n * n); // boxed Integer escapes via list
        }
        return out;
    }
}
```

### Example 20: Vector Intermediate Escape Chain vs In-Place Mutation

Title: Avoid transient object chains in numeric kernels
Description: 

**Good example:**

```java
final class Vector3Mutable {
    double x, y, z;
    void set(Vector3Mutable o) { x = o.x; y = o.y; z = o.z; }
    void addInPlace(Vector3Mutable o) { x += o.x; y += o.y; z += o.z; }
    void mulInPlace(double s) { x *= s; y *= s; z *= s; }
}

final class PhysicsNoEscape {
    private final Vector3Mutable temp1 = new Vector3Mutable();
    private final Vector3Mutable temp2 = new Vector3Mutable();

    void calculateForce(Vector3Mutable v, double m, Vector3Mutable a, Vector3Mutable out) {
        temp1.set(v); temp1.mulInPlace(m);
        temp2.set(a); temp2.mulInPlace(m);
        out.set(temp1); out.addInPlace(temp2);
    }
}
```

**Bad example:**

```java
final class Vector3 {
    final double x, y, z;
    Vector3(double x, double y, double z) { this.x = x; this.y = y; this.z = z; }
    Vector3 add(Vector3 o) { return new Vector3(x + o.x, y + o.y, z + o.z); }
    Vector3 mul(double s) { return new Vector3(x * s, y * s, z * s); }
}

final class PhysicsEscape {
    Vector3 calculateForce(Vector3 v, double m, Vector3 a) {
        Vector3 momentum = v.mul(m);
        Vector3 force = momentum.add(a.mul(m));
        return force; // chain creates transient escaping objects
    }
}
```

### Example 21: Lambda Return/List Capture Deep Dive

Title: Returning/capturing lambdas creates escaping closures
Description: 

**Good example:**

```java
import java.util.List;

final class NoLambdaEscape {
    void executeTasks(List<String> messages) {
        for (String msg : messages) {
            process(msg);
        }
    }

    private void process(String msg) {}
}
```

**Bad example:**

```java
import java.util.ArrayList;
import java.util.List;

final class LambdaEscape {
    List<Runnable> createTasks(List<String> messages) {
        List<Runnable> tasks = new ArrayList<>();
        for (String msg : messages) {
            tasks.add(() -> System.out.println(msg)); // captured lambda escapes in list
        }
        return tasks;
    }
}
```

### Example 22: Record-Specific Escape Analysis Discussion

Title: Records help value semantics but can still escape like classes
Description: 

**Good example:**

```java
record Person(String name, int age) {}

final class PersonService {
    String formatPerson(String name, int age) {
        Person p = new Person(name, age); // local use, candidate for scalar replacement
        return p.name() + ":" + p.age();
    }
}
```

**Bad example:**

```java
record Person(String name, int age) {}

final class PersonFactory {
    Person create(String name, int age) {
        return new Person(name, age); // escapes by return
    }
}
```

### Example 23: Exception Object Escape vs Throw Immediately

Title: Do not allocate and return exception objects as data
Description: 

**Good example:**

```java
final class ExceptionNoEscape {
    void validate(String input) {
        if (input == null) throw new IllegalArgumentException("Input is null");
        if (input.isEmpty()) throw new IllegalArgumentException("Input is empty");
    }

    boolean isValid(String input) {
        return input != null && !input.isEmpty();
    }
}
```

**Bad example:**

```java
final class ExceptionEscape {
    Exception validateAndCreateException(String input) {
        if (input == null) return new IllegalArgumentException("Input is null");
        if (input.isEmpty()) return new IllegalArgumentException("Input is empty");
        return null; // exception objects escape as return values
    }
}
```

### Example 24: Scalar Replacement: TempData Object vs Locals

Title: Prefer primitive locals when helper object adds no semantic value
Description: 

**Good example:**

```java
final class ScalarReplacement {
    double calculate(double[] values) {
        double sum = 0;
        int count = values.length;
        for (double v : values) sum += v;
        return sum / count;
    }
}
```

**Bad example:**

```java
final class ComplexCalculation {
    static final class TempData {
        double sum;
        int count;
    }

    TempData calculate(double[] values) {
        TempData d = new TempData();
        d.count = values.length;
        for (double v : values) d.sum += v;
        return d; // object escapes to caller
    }
}
```

### Example 25: JVM Escape Analysis Verification Flags and Demo

Title: Use diagnostic JVM options and paired methods to compare behavior
Description: Use JVM diagnostics in controlled environments when investigating EA behavior: -XX:+PrintEscapeAnalysis -XX:+DoEscapeAnalysis (default enabled) -XX:-DoEscapeAnalysis (for comparison only)

**Good example:**

```java
final class EscapeAnalysisTest {
    static final class Point {
        final int x, y;
        Point(int x, int y) { this.x = x; this.y = y; }
    }

    // likely NoEscape candidate
    static int testNoEscape() {
        Point p = new Point(3, 4);
        return p.x * p.x + p.y * p.y;
    }

    // GlobalEscape by return
    static Point testEscape() {
        return new Point(3, 4);
    }
}
```

**Bad example:**

```java
final class EscapeBlindChanges {
    int compute(int x, int y) {
        // Assumes stack allocation without checking runtime behavior or benchmarks
        return new Point(x, y).x + y;
    }

    static final class Point {
        final int x, y;
        Point(int x, int y) { this.x = x; this.y = y; }
    }
}
```

### Example 26: Use Columnar Layouts for Analytical Access Patterns

Title: Read only needed columns; improve cache locality
Description: Row-oriented object collections are convenient but expensive for scan-heavy analytics. Columnar arrays improve sequential access and reduce object indirection.

**Good example:**

```java
final class ColumnarTrades {
    private long[] timestamps;
    private int[] symbolIds;
    private double[] prices;
    private long[] volumes;
    private int size;

    double averagePrice(int symbolId) {
        double sum = 0;
        int count = 0;
        for (int i = 0; i < size; i++) {
            if (symbolIds[i] == symbolId) {
                sum += prices[i];
                count++;
            }
        }
        return count == 0 ? 0.0 : sum / count;
    }
}
```

**Bad example:**

```java
import java.util.ArrayList;
import java.util.List;

final class RowOrientedTrades {
    static final class Trade {
        long timestamp;
        String symbol;
        double price;
        long volume;
    }

    private final List<Trade> trades = new ArrayList<>();

    double averagePrice(String symbol) {
        double sum = 0;
        int count = 0;
        for (Trade t : trades) {
            if (t.symbol.equals(symbol)) {
                sum += t.price;
                count++;
            }
        }
        return count == 0 ? 0.0 : sum / count;
    }
}
```

### Example 27: Use Symbol Interning via IDs

Title: Deduplicate repeated strings and compare ints instead
Description: Replace repeated symbol strings with integer IDs to reduce memory and speed lookups/comparisons in hot paths.

**Good example:**

```java
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

final class SymbolInterning {
    private final Map<String, Integer> symbolToId = new ConcurrentHashMap<>();
    private final List<String> idToSymbol = new ArrayList<>();
    private final AtomicInteger nextId = new AtomicInteger();

    int intern(String symbol) {
        return symbolToId.computeIfAbsent(symbol, s -> {
            int id = nextId.getAndIncrement();
            idToSymbol.add(s);
            return id;
        });
    }
}
```

**Bad example:**

```java
import java.util.ArrayList;
import java.util.List;

final class DuplicatedStrings {
    static final class Trade { String symbol; double price; }
    private final List<Trade> trades = new ArrayList<>();

    void add(String symbol, double price) {
        Trade t = new Trade();
        t.symbol = symbol; // repeated string references everywhere
        t.price = price;
        trades.add(t);
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