---
name: stonebraker-database-architecture
description: Design databases in the style of Michael Stonebraker, Turing Award winner and creator of Ingres, Postgres, VoltDB, and Vertica. Emphasizes clean architecture, separation of OLTP/OLAP, and building systems that last decades. Use when designing database internals, storage engines, or making fundamental architectural decisions.
---

# Michael Stonebraker Style Guide

## Overview

Michael Stonebraker is a Turing Award winner (2014) who has created more influential database systems than anyone in history: Ingres, Postgres, VoltDB, Vertica, C-Store, H-Store, and SciDB. His work spans five decades and continues to shape how we think about data management.

## Core Philosophy

> "One size fits all is a thing of the past."

> "The database market is fragmenting. Different workloads need different architectures."

> "If you want performance, you have to know your workload."

Stonebraker believes that specialized databases will always outperform general-purpose ones. The era of the monolithic RDBMS serving all needs is over.

## Design Principles

1. **Workload-Specific Design**: OLTP, OLAP, streaming, and scientific data need different architectures.

2. **Main Memory is the New Disk**: Design for RAM-resident data; disk is for durability, not performance.

3. **Shared-Nothing Scales**: Horizontal partitioning beats shared-disk for scalability.

4. **The Log is the Database**: Write-ahead logging is fundamental; the log can be the source of truth.

5. **Clean Abstractions Endure**: Postgres has lasted 30+ years because of its extensible, clean design.

## When Writing Database Code

### Always

- Design for a specific workload first, generalize later
- Separate storage engine from query processing
- Make the common case fast, even at cost to edge cases
- Build extensibility points (types, operators, indexes, languages)
- Use write-ahead logging for durability
- Consider column vs row storage based on access patterns

### Never

- Assume one architecture fits all workloads
- Ignore the memory hierarchy (L1 → L2 → L3 → RAM → SSD → HDD)
- Mix OLTP and OLAP in the same engine without thought
- Underestimate the cost of disk I/O
- Build without considering concurrency control from day one

### Prefer

- Specialized engines over general-purpose compromises
- Main-memory optimized structures for OLTP
- Columnar storage for analytics
- Shared-nothing over shared-disk
- Deterministic execution for replication

## Code Patterns

### Separation of Concerns (Postgres Architecture)

```
┌─────────────────────────────────────────────────┐
│                  SQL Interface                   │
├─────────────────────────────────────────────────┤
│    Parser → Analyzer → Rewriter → Planner       │
├─────────────────────────────────────────────────┤
│              Executor (Volcano Model)            │
├─────────────────────────────────────────────────┤
│  Access Methods   │  Buffer Manager  │  WAL     │
├───────────────────┼──────────────────┼──────────┤
│              Storage Manager                     │
└─────────────────────────────────────────────────┘
```

### OLTP vs OLAP Design

```python
# OLTP: Row-oriented, point queries, high concurrency
class OLTPStorage:
    """
    Stonebraker's H-Store/VoltDB principles:
    - Main-memory resident
    - Single-threaded partitions (no locking!)
    - Stored procedures, not ad-hoc SQL
    - Deterministic execution for replication
    """
    def __init__(self, num_partitions):
        self.partitions = [Partition() for _ in range(num_partitions)]
    
    def execute(self, txn):
        partition = self.route(txn)
        # Single-threaded: no locks needed!
        return partition.execute(txn)
    
    def route(self, txn):
        # Partition by primary key
        return self.partitions[hash(txn.key) % len(self.partitions)]


# OLAP: Column-oriented, full scans, compression
class OLAPStorage:
    """
    Stonebraker's C-Store/Vertica principles:
    - Column-at-a-time processing
    - Heavy compression (RLE, dictionary, delta)
    - Projection-based storage (materialized views)
    - Read-optimized store + write-optimized store
    """
    def __init__(self):
        self.columns = {}  # column_name -> compressed array
        self.write_store = []  # Recent writes (row-oriented)
    
    def scan(self, column_name, predicate):
        # Operate on compressed data when possible
        col = self.columns[column_name]
        return col.scan_with_predicate(predicate)
    
    def aggregate(self, column_name, agg_func):
        # Vectorized execution on columnar data
        col = self.columns[column_name]
        return agg_func(col.decompress_batch())
```

### Write-Ahead Logging

```python
class WriteAheadLog:
    """
    Fundamental durability mechanism.
    The log IS the database; tables are just a cache.
    """
    def __init__(self, log_path):
        self.log_file = open(log_path, 'ab')
        self.lsn = 0  # Log Sequence Number
    
    def append(self, record):
        """Write-ahead: log before modifying data pages."""
        self.lsn += 1
        entry = LogEntry(
            lsn=self.lsn,
            timestamp=time.time(),
            record=record
        )
        self.log_file.write(entry.serialize())
        self.log_file.flush()
        os.fsync(self.log_file.fileno())  # Force to disk
        return self.lsn
    
    def recover(self):
        """Replay log to reconstruct state after crash."""
        for entry in self.read_all_entries():
            self.apply(entry)
```

### Extensible Type System (Postgres Model)

```sql
-- Stonebraker's key insight: let users define their own types
-- This is why Postgres supports JSON, arrays, PostGIS, etc.

CREATE TYPE complex AS (
    re double precision,
    im double precision
);

CREATE FUNCTION complex_add(complex, complex) RETURNS complex AS $$
    SELECT ROW($1.re + $2.re, $1.im + $2.im)::complex;
$$ LANGUAGE SQL IMMUTABLE;

CREATE OPERATOR + (
    leftarg = complex,
    rightarg = complex,
    function = complex_add,
    commutator = +
);

-- Now you can: SELECT (1.0, 2.0)::complex + (3.0, 4.0)::complex;
```

### Partition-Based Concurrency

```python
class PartitionedDatabase:
    """
    H-Store insight: if each partition is single-threaded,
    you eliminate locking overhead entirely.
    """
    def __init__(self, num_partitions):
        self.partitions = []
        for i in range(num_partitions):
            # Each partition runs in its own thread
            p = Partition(id=i)
            p.start()
            self.partitions.append(p)
    
    def execute_single_partition(self, txn):
        """Fast path: no coordination needed."""
        p = self.get_partition(txn.partition_key)
        return p.execute(txn)
    
    def execute_multi_partition(self, txn):
        """Slow path: requires coordination."""
        # Two-phase commit across partitions
        partitions = self.get_involved_partitions(txn)
        
        # Phase 1: Prepare
        votes = [p.prepare(txn) for p in partitions]
        if all(votes):
            # Phase 2: Commit
            for p in partitions:
                p.commit(txn)
        else:
            for p in partitions:
                p.abort(txn)
```

## Mental Model

Stonebraker approaches database design by asking:

1. **What is the workload?** OLTP, OLAP, streaming, scientific?
2. **Where is the data?** Memory, SSD, disk, distributed?
3. **What is the access pattern?** Point queries, range scans, full table scans?
4. **What consistency is required?** ACID, eventual, something in between?
5. **How will it scale?** Vertical, horizontal, both?

Then design the architecture specifically for those answers.

## Signature Stonebraker Moves

- Specialized engines over general-purpose
- Column stores for analytics, row stores for transactions
- Main-memory optimization for OLTP
- Shared-nothing architecture for scale
- Extensible type systems
- Clean separation between components
- Write-ahead logging as the foundation

## Key Papers

- "The Design of Postgres" (1986)
- "C-Store: A Column-oriented DBMS" (2005)
- "H-Store: A High-Performance, Distributed Main Memory Transaction Processing System" (2008)
- "The End of an Architectural Era" (2007)
- "One Size Fits All: An Idea Whose Time Has Come and Gone" (2005)
