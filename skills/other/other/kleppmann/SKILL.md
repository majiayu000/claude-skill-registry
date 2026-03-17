---
name: kleppmann-data-intensive
description: Design distributed systems in the style of Martin Kleppmann, author of "Designing Data-Intensive Applications". Emphasizes understanding data systems deeply, making informed trade-offs, and building reliable data infrastructure. Use when designing databases, streaming systems, or data pipelines.
---

# Martin Kleppmann Style Guide

## Overview

Martin Kleppmann is the author of "Designing Data-Intensive Applications" (DDIA), one of the most influential books on distributed systems and databases. He excels at explaining complex concepts clearly and helping engineers make informed architectural decisions.

## Core Philosophy

> "Reliability means making systems work correctly, even when faults occur."

> "The goal of consistency models is to provide a abstraction for application developers."

> "There's no such thing as a 'best' database—only trade-offs."

Kleppmann believes in understanding systems deeply, not just using them. Every architectural choice is a trade-off; understand what you're trading.

## Design Principles

1. **Understand the Trade-offs**: CAP, PACELC, latency vs consistency.

2. **Design for Failure**: Partial failure is the norm in distributed systems.

3. **Data Outlives Code**: Schema design and data models matter enormously.

4. **Exactly-Once Is Hard**: Understand idempotency and at-least-once semantics.

## When Writing Code

### Always

- Understand the consistency guarantees your system provides
- Design for idempotency where possible
- Think about data evolution and schema changes
- Consider exactly-once vs at-least-once semantics
- Know your data access patterns before choosing storage
- Plan for failure recovery

### Never

- Assume "eventual consistency" without understanding what it means
- Ignore the differences between isolation levels
- Couple tightly without considering failure modes
- Treat distributed transactions as a silver bullet

### Prefer

- Idempotent operations
- Append-only data structures
- Event sourcing for audit trails
- Change data capture over dual writes
- Log-based message brokers over traditional ones

## Code Patterns

### Consistency Models Illustrated

```python
# Understanding consistency models through code

class LinearizableStore:
    """
    Linearizability: operations appear atomic and instantaneous.
    Strongest consistency - single copy illusion.
    """
    def __init__(self):
        self._lock = threading.Lock()
        self._data = {}
    
    def write(self, key, value):
        with self._lock:
            self._data[key] = value
    
    def read(self, key):
        with self._lock:
            return self._data.get(key)
    
    def compare_and_set(self, key, expected, new_value):
        with self._lock:
            if self._data.get(key) == expected:
                self._data[key] = new_value
                return True
            return False


class CausallyConsistentStore:
    """
    Causal consistency: respects happens-before relationship.
    Weaker than linearizable, but allows more concurrency.
    """
    def __init__(self, node_id):
        self.node_id = node_id
        self.data = {}
        self.vector_clock = defaultdict(int)
    
    def write(self, key, value, dependencies=None):
        # Update our clock
        self.vector_clock[self.node_id] += 1
        
        # Merge dependencies
        if dependencies:
            for node, time in dependencies.items():
                self.vector_clock[node] = max(self.vector_clock[node], time)
        
        self.data[key] = {
            'value': value,
            'clock': dict(self.vector_clock)
        }
        
        return dict(self.vector_clock)
    
    def read(self, key):
        if key in self.data:
            return self.data[key]['value'], self.data[key]['clock']
        return None, dict(self.vector_clock)
```

### Event Sourcing

```python
# Event sourcing: store events, derive state

from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class Event:
    event_type: str
    data: dict
    timestamp: datetime
    version: int

class EventStore:
    def __init__(self):
        self.events: List[Event] = []
        self.version = 0
    
    def append(self, event_type: str, data: dict):
        self.version += 1
        event = Event(
            event_type=event_type,
            data=data,
            timestamp=datetime.now(),
            version=self.version
        )
        self.events.append(event)
        return event
    
    def get_events(self, from_version=0):
        return [e for e in self.events if e.version > from_version]


class BankAccount:
    """Aggregate rebuilt from events"""
    
    def __init__(self, account_id: str, event_store: EventStore):
        self.account_id = account_id
        self.event_store = event_store
        self.balance = 0
        self._rebuild_state()
    
    def _rebuild_state(self):
        """Derive current state from event history"""
        for event in self.event_store.events:
            self._apply(event)
    
    def _apply(self, event: Event):
        if event.event_type == 'deposited':
            self.balance += event.data['amount']
        elif event.event_type == 'withdrawn':
            self.balance -= event.data['amount']
    
    def deposit(self, amount: float):
        event = self.event_store.append('deposited', {
            'account_id': self.account_id,
            'amount': amount
        })
        self._apply(event)
    
    def withdraw(self, amount: float):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        event = self.event_store.append('withdrawn', {
            'account_id': self.account_id,
            'amount': amount
        })
        self._apply(event)

# Benefits:
# 1. Complete audit trail
# 2. Time travel (state at any point)
# 3. Event replay for debugging
# 4. Easy to add new projections
```

### Idempotency Keys

```python
# Idempotency: safe retries without duplicate effects

import uuid
import hashlib

class IdempotentProcessor:
    def __init__(self):
        self.processed_keys = {}  # key -> result
        self.expiry_seconds = 3600
    
    def process(self, idempotency_key: str, operation):
        """
        Execute operation exactly once for a given key.
        Retries with same key return cached result.
        """
        # Check if already processed
        if idempotency_key in self.processed_keys:
            return self.processed_keys[idempotency_key]
        
        # Execute operation
        try:
            result = operation()
            self.processed_keys[idempotency_key] = {
                'status': 'success',
                'result': result
            }
            return self.processed_keys[idempotency_key]
        except Exception as e:
            # Don't cache failures (allow retry)
            raise
    
    @staticmethod
    def generate_key(*args):
        """Generate deterministic idempotency key"""
        content = '|'.join(str(arg) for arg in args)
        return hashlib.sha256(content.encode()).hexdigest()


# Usage:
processor = IdempotentProcessor()

def create_payment(user_id, amount, idempotency_key):
    def do_payment():
        # Actually create the payment
        return {'payment_id': str(uuid.uuid4()), 'amount': amount}
    
    return processor.process(idempotency_key, do_payment)

# Client can safely retry:
key = IdempotentProcessor.generate_key(user_id, amount, request_id)
result1 = create_payment(user_id, 100, key)
result2 = create_payment(user_id, 100, key)  # Same result, no duplicate payment
```

### Change Data Capture

```python
# CDC: capture database changes as a stream

from typing import Callable, List
from enum import Enum
from dataclasses import dataclass

class OperationType(Enum):
    INSERT = 'insert'
    UPDATE = 'update'
    DELETE = 'delete'

@dataclass
class ChangeEvent:
    table: str
    operation: OperationType
    key: dict
    before: dict  # For update/delete
    after: dict   # For insert/update
    timestamp: float
    sequence: int

class CDCProducer:
    """Publish changes from database write-ahead log"""
    
    def __init__(self, publisher):
        self.publisher = publisher
        self.sequence = 0
    
    def capture_insert(self, table: str, key: dict, data: dict):
        self.sequence += 1
        event = ChangeEvent(
            table=table,
            operation=OperationType.INSERT,
            key=key,
            before=None,
            after=data,
            timestamp=time.time(),
            sequence=self.sequence
        )
        self.publisher.publish(event)
    
    def capture_update(self, table: str, key: dict, before: dict, after: dict):
        self.sequence += 1
        event = ChangeEvent(
            table=table,
            operation=OperationType.UPDATE,
            key=key,
            before=before,
            after=after,
            timestamp=time.time(),
            sequence=self.sequence
        )
        self.publisher.publish(event)


class CDCConsumer:
    """Consume changes and maintain derived view"""
    
    def __init__(self):
        self.handlers: dict[str, List[Callable]] = {}
        self.last_sequence = 0
    
    def register(self, table: str, handler: Callable):
        if table not in self.handlers:
            self.handlers[table] = []
        self.handlers[table].append(handler)
    
    def process(self, event: ChangeEvent):
        # Ensure ordering
        if event.sequence <= self.last_sequence:
            return  # Already processed
        
        if event.table in self.handlers:
            for handler in self.handlers[event.table]:
                handler(event)
        
        self.last_sequence = event.sequence

# Usage: maintain search index from database changes
def update_search_index(event: ChangeEvent):
    if event.operation == OperationType.DELETE:
        search_index.delete(event.key)
    else:
        search_index.index(event.key, event.after)

consumer.register('products', update_search_index)
```

### Stream Processing

```python
# Stream processing patterns

from collections import defaultdict
from typing import Iterator, TypeVar, Callable

T = TypeVar('T')

class StreamProcessor:
    """Stateful stream processing"""
    
    def __init__(self):
        self.state = {}
    
    def process(self, stream: Iterator[T], handler: Callable[[T, dict], None]):
        """Process stream with access to state"""
        for record in stream:
            handler(record, self.state)
            yield self.state.copy()


def windowed_count(window_size_seconds: int):
    """Tumbling window aggregation"""
    def handler(event, state):
        window_start = (event['timestamp'] // window_size_seconds) * window_size_seconds
        key = (event['key'], window_start)
        
        if key not in state:
            state[key] = {'count': 0, 'window_start': window_start}
        state[key]['count'] += 1
        
        # Emit completed windows
        current_window = (time.time() // window_size_seconds) * window_size_seconds
        completed = [k for k in state if k[1] < current_window - window_size_seconds]
        for k in completed:
            emit(state.pop(k))
    
    return handler


def exactly_once_processing(processor, checkpointer):
    """
    Exactly-once semantics via:
    1. Idempotent writes
    2. Transactional checkpointing
    """
    def process_with_guarantees(records):
        for record in records:
            # Get last checkpoint
            last_offset = checkpointer.get_offset()
            
            if record.offset <= last_offset:
                continue  # Already processed
            
            # Process and checkpoint atomically
            with transaction():
                result = processor.process(record)
                checkpointer.save_offset(record.offset)
            
            yield result
    
    return process_with_guarantees
```

## Mental Model

Kleppmann approaches data systems by asking:

1. **What are the consistency requirements?** Linearizable, serializable, eventual?
2. **What are the access patterns?** Read-heavy, write-heavy, mixed?
3. **How do we handle failures?** Retries, idempotency, compensation?
4. **How does data evolve?** Schema changes, backward compatibility?
5. **What happens at the edges?** Network partitions, slow nodes?

## Signature Kleppmann Moves

- Event sourcing for auditability
- Idempotency keys for safe retries
- CDC over dual writes
- Understanding isolation levels deeply
- Log-based messaging for durability
- Making trade-offs explicit
