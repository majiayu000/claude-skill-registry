---
name: pavlo-database-performance
description: Optimize databases in the style of Andy Pavlo, CMU professor and database performance expert. Emphasizes understanding internals, benchmarking rigorously, and making informed architectural choices. Use when tuning query performance, designing storage engines, or evaluating database technologies.
---

# Andy Pavlo Style Guide

## Overview

Andy Pavlo is a professor at Carnegie Mellon University, leading researcher in database systems, and creator of the Database of Databases (dbdb.io). He is known for rigorous benchmarking, deep understanding of database internals, and bridging academic research with practical systems.

## Core Philosophy

> "There's no magic in databases. It's all just data structures and algorithms."

> "Benchmarks lie. Understand what you're measuring."

> "The best optimization is the one you don't have to make because you chose the right architecture."

Pavlo believes in understanding systems deeply, measuring rigorously, and making decisions based on data rather than marketing claims.

## Design Principles

1. **Know Your Hardware**: CPU cache lines, memory bandwidth, SSD latencies—they all matter.

2. **Measure, Don't Guess**: Microbenchmarks lie; end-to-end benchmarks reveal truth.

3. **Query Compilation > Interpretation**: Modern CPUs reward tight, compiled code.

4. **Vectorization Wins**: Process batches of tuples, not one at a time.

5. **Memory is Bandwidth**: In-memory DBs are often memory-bandwidth bound, not compute bound.

## When Writing Database Code

### Always

- Profile before optimizing
- Understand the memory hierarchy impact on your data structures
- Use vectorized execution for analytical queries
- Consider cache-conscious data layouts
- Benchmark with realistic workloads and data sizes
- Know the difference between OLTP and OLAP optimization strategies

### Never

- Trust vendor benchmarks without reproduction
- Optimize without measuring
- Ignore the buffer pool / caching behavior
- Assume indexes are always the answer
- Forget about CPU branch prediction and cache misses

### Prefer

- Compiled queries over interpreted
- Vectorized over tuple-at-a-time
- Column stores for analytical workloads
- Covering indexes to avoid heap fetches
- Batched I/O over random I/O

## Code Patterns

### Vectorized Execution

```cpp
// Tuple-at-a-time (slow - function call overhead per row)
for (auto& tuple : table) {
    if (predicate(tuple)) {
        result.push_back(project(tuple));
    }
}

// Vectorized execution (fast - process batches)
class VectorizedScan {
    static constexpr size_t BATCH_SIZE = 1024;
    
    void execute(Table& table, std::vector<Tuple>& result) {
        std::array<Tuple, BATCH_SIZE> batch;
        std::array<bool, BATCH_SIZE> selection;
        
        for (size_t offset = 0; offset < table.size(); offset += BATCH_SIZE) {
            size_t count = table.read_batch(offset, batch);
            
            // Evaluate predicate on entire batch
            evaluate_predicate(batch, count, selection);
            
            // Project selected tuples
            for (size_t i = 0; i < count; i++) {
                if (selection[i]) {
                    result.push_back(project(batch[i]));
                }
            }
        }
    }
};
```

### Query Compilation

```cpp
// Interpreted execution (slow)
class InterpretedExecutor {
    Value execute(const Expr& expr, const Tuple& tuple) {
        switch (expr.type) {
            case ADD:
                return execute(expr.left, tuple) + execute(expr.right, tuple);
            case COLUMN:
                return tuple.get(expr.column_id);
            // ... many more cases, many branches
        }
    }
};

// Compiled execution (fast - generate native code)
class CompiledQuery {
    // Generate LLVM IR or C++ code for the query
    // Compile once, execute many times with no interpretation overhead
    
    std::function<void(Tuple*, Result*)> compile(const Query& q) {
        // Example: SELECT a + b FROM t WHERE c > 10
        // Generates something like:
        return [](Tuple* t, Result* r) {
            if (t->c > 10) {
                r->emit(t->a + t->b);
            }
        };
    }
};
```

### Cache-Conscious Data Structures

```cpp
// Cache-unfriendly: pointer chasing
struct Node {
    int key;
    Node* left;
    Node* right;
};

// Cache-friendly: B+ tree with high fan-out
template<typename K, typename V, size_t FAN_OUT = 256>
class BPlusTreeNode {
    // Pack keys contiguously for cache-friendly binary search
    std::array<K, FAN_OUT - 1> keys;
    
    // Separate array for children/values
    union {
        std::array<BPlusTreeNode*, FAN_OUT> children;
        std::array<V, FAN_OUT - 1> values;
    };
    
    bool is_leaf;
    size_t num_keys;
    
    // Binary search stays in cache
    size_t find_key(K key) {
        return std::lower_bound(
            keys.begin(), 
            keys.begin() + num_keys, 
            key
        ) - keys.begin();
    }
};
```

### Proper Benchmarking

```python
class DatabaseBenchmark:
    """
    Pavlo's benchmarking principles:
    1. Warm up the cache
    2. Run multiple iterations
    3. Report percentiles, not just averages
    4. Measure what matters (end-to-end latency)
    """
    
    def __init__(self, db, workload):
        self.db = db
        self.workload = workload
        self.results = []
    
    def run(self, warmup_iters=100, measure_iters=1000):
        # Warmup phase - populate caches, trigger JIT
        for _ in range(warmup_iters):
            self.workload.execute(self.db)
        
        # Measurement phase
        for _ in range(measure_iters):
            start = time.perf_counter_ns()
            self.workload.execute(self.db)
            elapsed = time.perf_counter_ns() - start
            self.results.append(elapsed)
        
        return self.analyze()
    
    def analyze(self):
        results = sorted(self.results)
        return {
            'p50': results[len(results) // 2],
            'p99': results[int(len(results) * 0.99)],
            'p999': results[int(len(results) * 0.999)],
            'mean': sum(results) / len(results),
            'min': results[0],
            'max': results[-1],
        }
```

### Index Selection

```sql
-- Pavlo's index selection principles:

-- 1. Leading columns matter most
-- Good: queries filter on (a) or (a, b) or (a, b, c)
CREATE INDEX idx_abc ON t(a, b, c);

-- 2. Covering indexes avoid heap fetches
-- If query only needs a, b, d - include d in index
CREATE INDEX idx_abc_covering ON t(a, b, c) INCLUDE (d);

-- 3. Consider index-only scans for aggregations
-- This index can answer: SELECT COUNT(*) FROM t WHERE status = 'active'
CREATE INDEX idx_status ON t(status);

-- 4. Partial indexes for skewed data
-- Only index rows where is_active = true (if most rows are false)
CREATE INDEX idx_active_users ON users(email) WHERE is_active = true;

-- 5. Expression indexes for computed predicates
CREATE INDEX idx_lower_email ON users(LOWER(email));
```

### Understanding Buffer Pool Behavior

```python
class BufferPoolAnalysis:
    """
    Most "slow query" issues are buffer pool issues.
    """
    
    def diagnose_slow_query(self, query, db):
        # Check buffer pool hit ratio
        stats_before = db.get_buffer_stats()
        db.execute(query)
        stats_after = db.get_buffer_stats()
        
        reads = stats_after['disk_reads'] - stats_before['disk_reads']
        hits = stats_after['buffer_hits'] - stats_before['buffer_hits']
        
        hit_ratio = hits / (hits + reads) if (hits + reads) > 0 else 1.0
        
        if hit_ratio < 0.99:
            print(f"WARNING: Buffer hit ratio {hit_ratio:.2%}")
            print("Consider: larger buffer pool, better indexes, or query rewrite")
        
        if reads > 1000:
            print(f"WARNING: {reads} disk reads - check for sequential scan")
        
        return {
            'disk_reads': reads,
            'buffer_hits': hits,
            'hit_ratio': hit_ratio
        }
```

## Mental Model

Pavlo approaches database optimization by asking:

1. **What does EXPLAIN show?** Understand the query plan first
2. **Where is time spent?** I/O, CPU, network, locks?
3. **What's the data distribution?** Skew kills assumptions
4. **Is caching working?** Buffer pool, OS page cache, CPU cache
5. **Am I measuring correctly?** Warm cache, realistic data, percentiles

## Signature Pavlo Moves

- Rigorous benchmarking with proper methodology
- Understanding hardware characteristics
- Vectorized execution for analytics
- Query compilation for OLTP
- Cache-conscious data structure design
- EXPLAIN ANALYZE before optimizing
- Skepticism of vendor claims

## Key Resources

- CMU Database Systems course (15-445/645)
- Database of Databases (dbdb.io)
- "What's New with NewSQL?" (2016)
- "Self-Driving Database Management Systems" (2017)
- CMU Database Group YouTube channel
