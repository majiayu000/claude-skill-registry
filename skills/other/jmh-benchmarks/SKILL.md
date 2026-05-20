---
name: jmh-benchmarks
description: Expert guidance for writing Java microbenchmarks using JMH (Java Microbenchmark Harness). Use this skill when writing performance benchmarks, measuring method execution time, comparing algorithm implementations, profiling code performance, or debugging benchmark issues. Trigger keywords include "jmh", "benchmark", "microbenchmark", "performance test", "@Benchmark", "throughput", "warmup", "blackhole", "measure performance".
---

# JMH Benchmarks

JMH is the official OpenJDK harness for building reliable Java microbenchmarks. It handles warmup, JIT compilation, dead code elimination, and statistical analysis automatically.

## Project Setup

Generate a new benchmark project using the Maven archetype:

```bash
mvn archetype:generate \
  -DinteractiveMode=false \
  -DarchetypeGroupId=org.openjdk.jmh \
  -DarchetypeArtifactId=jmh-java-benchmark-archetype \
  -DgroupId=org.example \
  -DartifactId=my-benchmarks \
  -Dversion=1.0-SNAPSHOT
```

Build and run:

```bash
mvn clean verify
java -jar target/benchmarks.jar
```

## Basic Benchmark

```java
import org.openjdk.jmh.annotations.*;
import java.util.concurrent.TimeUnit;

@State(Scope.Thread)
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.NANOSECONDS)
@Warmup(iterations = 5, time = 1)
@Measurement(iterations = 5, time = 1)
@Fork(1)
public class MyBenchmark {

    private String data;

    @Setup
    public void setup() {
        data = "test-data";
    }

    @Benchmark
    public int measureLength() {
        return data.length();
    }
}
```

## Benchmark Modes

| Mode                  | Description                                       |
| --------------------- | ------------------------------------------------- |
| `Mode.Throughput`     | Operations per second (default)                   |
| `Mode.AverageTime`    | Average time per operation                        |
| `Mode.SampleTime`     | Samples execution time distribution (percentiles) |
| `Mode.SingleShotTime` | Single invocation time (cold start)               |
| `Mode.All`            | Run all modes                                     |

```java
@BenchmarkMode({Mode.Throughput, Mode.AverageTime})
```

## State Scopes

| Scope             | Description                                     |
| ----------------- | ----------------------------------------------- |
| `Scope.Thread`    | One instance per thread (no contention)         |
| `Scope.Benchmark` | Shared across all threads (contention possible) |
| `Scope.Group`     | Shared within thread group                      |

```java
@State(Scope.Thread)
public class MyState {
    // Non-final fields for computation inputs
    public int x = 42;
}
```

## Setup and Teardown

```java
@State(Scope.Thread)
public class MyBenchmark {

    private List<String> data;

    @Setup(Level.Trial)      // Once per benchmark run
    public void setupTrial() { }

    @Setup(Level.Iteration)  // Before each iteration
    public void setupIteration() { }

    @Setup(Level.Invocation) // Before each method call (expensive!)
    public void setupInvocation() { }

    @TearDown(Level.Trial)
    public void tearDown() { }
}
```

## Critical Pitfalls

### Dead Code Elimination

The JVM eliminates code whose results are unused. Always return or consume results:

```java
// WRONG: Result unused, JVM eliminates the call
@Benchmark
public void wrong() {
    compute(x);
}

// CORRECT: Return the result
@Benchmark
public int correct() {
    return compute(x);
}
```

### Multiple Results: Use Blackhole

When a method produces multiple values, use `Blackhole` to consume them:

```java
@Benchmark
public void multipleResults(Blackhole bh) {
    bh.consume(compute(x));
    bh.consume(compute(y));
}
```

### Constant Folding

Never use `final` fields or literal values as inputs. The JVM precomputes results for predictable inputs:

```java
@State(Scope.Thread)
public class MyState {
    // WRONG: final enables constant folding
    public final int x = 42;

    // CORRECT: non-final prevents optimisation
    public int x = 42;
}

@Benchmark
public int wrong() {
    return compute(42);  // Literal folded at compile time
}

@Benchmark
public int correct(MyState state) {
    return compute(state.x);  // Runtime value
}
```

### Manual Loops

Never write manual loops. JMH handles iteration and loop optimisations distort results:

```java
// WRONG: Loop unrolling distorts measurements
@Benchmark
public int wrong() {
    int sum = 0;
    for (int i = 0; i < 1000; i++) {
        sum += compute(i);
    }
    return sum;
}

// CORRECT: Single operation, let JMH iterate
@Benchmark
public int correct(MyState state) {
    return compute(state.i);
}
```

## Parameterised Benchmarks

Test across multiple configurations:

```java
@State(Scope.Benchmark)
public class ParamBenchmark {

    @Param({"10", "100", "1000"})
    public int size;

    @Param({"ArrayList", "LinkedList"})
    public String listType;

    private List<Integer> list;

    @Setup
    public void setup() {
        list = listType.equals("ArrayList")
            ? new ArrayList<>()
            : new LinkedList<>();
        for (int i = 0; i < size; i++) {
            list.add(i);
        }
    }

    @Benchmark
    public int iterate() {
        int sum = 0;
        for (int x : list) sum += x;
        return sum;
    }
}
```

Override parameters from command line:

```bash
java -jar benchmarks.jar -p size=50,500 -p listType=ArrayList
```

## Common Annotations

```java
@Warmup(iterations = 5, time = 1, timeUnit = TimeUnit.SECONDS)
@Measurement(iterations = 10, time = 2, timeUnit = TimeUnit.SECONDS)
@Fork(value = 2, jvmArgs = {"-Xms2G", "-Xmx2G"})
@Threads(4)
@Timeout(time = 30, timeUnit = TimeUnit.SECONDS)
```

## Programmatic Execution

Run benchmarks from code (useful for IDE integration):

```java
public static void main(String[] args) throws Exception {
    Options opt = new OptionsBuilder()
        .include(MyBenchmark.class.getSimpleName())
        .forks(1)
        .warmupIterations(3)
        .measurementIterations(5)
        .mode(Mode.AverageTime)
        .timeUnit(TimeUnit.NANOSECONDS)
        .build();

    new Runner(opt).run();
}
```

## Command Line Options

```bash
# List available benchmarks
java -jar benchmarks.jar -l

# Run specific benchmark
java -jar benchmarks.jar MyBenchmark

# Configure execution
java -jar benchmarks.jar -f 2 -wi 5 -i 10 -t 4

# Output formats
java -jar benchmarks.jar -rf json -rff results.json
java -jar benchmarks.jar -rf csv -rff results.csv

# Profilers
java -jar benchmarks.jar -prof gc
java -jar benchmarks.jar -prof stack
java -jar benchmarks.jar -prof perfasm  # Linux only

# Help
java -jar benchmarks.jar -h
```

## Maven Dependencies

For adding to an existing project (archetype preferred for new projects):

```xml
<dependencies>
    <dependency>
        <groupId>org.openjdk.jmh</groupId>
        <artifactId>jmh-core</artifactId>
        <version>1.37</version>
    </dependency>
    <dependency>
        <groupId>org.openjdk.jmh</groupId>
        <artifactId>jmh-generator-annprocess</artifactId>
        <version>1.37</version>
        <scope>provided</scope>
    </dependency>
</dependencies>
```

Configure the annotation processor in the compiler plugin:

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <configuration>
        <annotationProcessorPaths>
            <path>
                <groupId>org.openjdk.jmh</groupId>
                <artifactId>jmh-generator-annprocess</artifactId>
                <version>1.37</version>
            </path>
        </annotationProcessorPaths>
    </configuration>
</plugin>
```

## Resources

- [JMH Repository](https://github.com/openjdk/jmh)
- [Official Samples](https://github.com/openjdk/jmh/tree/master/jmh-samples/src/main/java/org/openjdk/jmh/samples)
