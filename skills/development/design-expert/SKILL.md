---
name: design-expert
version: 1.0.0
description: Expert-level system design, architecture patterns, scalability, and distributed systems
category: design
tags: [system-design, architecture, scalability, distributed-systems, patterns]
allowed-tools:
  - Read
  - Write
  - Edit
---

# System Design Expert

Expert guidance for system design, software architecture, scalability patterns, and distributed systems.

## Core Concepts

### Architecture Patterns
- Microservices vs Monolithic
- Event-driven architecture
- CQRS and Event Sourcing
- Layered architecture
- Hexagonal architecture
- Service-oriented architecture (SOA)

### Scalability
- Horizontal vs vertical scaling
- Load balancing strategies
- Caching layers
- Database sharding
- Read replicas
- CDN usage

### Distributed Systems
- CAP theorem
- Consistency models
- Distributed consensus (Raft, Paxos)
- Message queues
- Service discovery
- Circuit breakers

## Design Patterns

```python
# Singleton Pattern
class DatabaseConnection:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.connection = self._create_connection()

# Factory Pattern
class ShapeFactory:
    @staticmethod
    def create_shape(shape_type: str):
        if shape_type == "circle":
            return Circle()
        elif shape_type == "square":
            return Square()
        raise ValueError(f"Unknown shape: {shape_type}")

# Observer Pattern
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def notify(self, event):
        for observer in self._observers:
            observer.update(event)

# Strategy Pattern
class PaymentStrategy:
    def pay(self, amount): pass

class CreditCardPayment(PaymentStrategy):
    def pay(self, amount):
        return f"Paid ${amount} via credit card"

class PayPalPayment(PaymentStrategy):
    def pay(self, amount):
        return f"Paid ${amount} via PayPal"
```

## Scalability Patterns

```python
# Circuit Breaker Pattern
from enum import Enum
import time

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED

    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise e

    def on_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

# Rate Limiter
from collections import deque
import time

class RateLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = deque()

    def allow_request(self, user_id):
        now = time.time()

        # Remove old requests outside window
        while self.requests and self.requests[0][1] < now - self.window_seconds:
            self.requests.popleft()

        # Check if under limit
        user_requests = sum(1 for uid, _ in self.requests if uid == user_id)

        if user_requests < self.max_requests:
            self.requests.append((user_id, now))
            return True

        return False
```

## Caching Strategy

```python
from functools import wraps
import hashlib
import json

class CacheStrategy:
    """Implement caching patterns"""

    def __init__(self, cache_backend):
        self.cache = cache_backend

    def cache_aside(self, key, fetch_func, ttl=3600):
        """Cache-aside (lazy loading)"""
        data = self.cache.get(key)

        if data is None:
            data = fetch_func()
            self.cache.set(key, data, ttl)

        return data

    def write_through(self, key, data, persist_func):
        """Write-through caching"""
        self.cache.set(key, data)
        persist_func(data)

    def write_behind(self, key, data, queue):
        """Write-behind (write-back) caching"""
        self.cache.set(key, data)
        queue.enqueue(lambda: self.persist(key, data))

def memoize(ttl=3600):
    """Memoization decorator"""
    cache = {}

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = hashlib.md5(
                json.dumps((args, kwargs), sort_keys=True).encode()
            ).hexdigest()

            if key in cache:
                cached_value, timestamp = cache[key]
                if time.time() - timestamp < ttl:
                    return cached_value

            result = func(*args, **kwargs)
            cache[key] = (result, time.time())
            return result

        return wrapper
    return decorator
```

## Database Patterns

```python
# Database Sharding
class ShardRouter:
    def __init__(self, num_shards):
        self.num_shards = num_shards
        self.shards = [f"shard_{i}" for i in range(num_shards)]

    def get_shard(self, key):
        """Route to shard based on key"""
        shard_id = hash(key) % self.num_shards
        return self.shards[shard_id]

# Read Replica Pattern
class DatabaseRouter:
    def __init__(self, primary, replicas):
        self.primary = primary
        self.replicas = replicas
        self.current_replica = 0

    def execute_write(self, query):
        """All writes go to primary"""
        return self.primary.execute(query)

    def execute_read(self, query):
        """Reads from replicas (round-robin)"""
        replica = self.replicas[self.current_replica]
        self.current_replica = (self.current_replica + 1) % len(self.replicas)
        return replica.execute(query)
```

## Load Balancing

```python
from typing import List
import random

class LoadBalancer:
    """Implement load balancing algorithms"""

    def __init__(self, servers: List[str]):
        self.servers = servers
        self.current = 0

    def round_robin(self):
        """Round-robin load balancing"""
        server = self.servers[self.current]
        self.current = (self.current + 1) % len(self.servers)
        return server

    def least_connections(self, connections_per_server):
        """Least connections algorithm"""
        return min(connections_per_server.items(), key=lambda x: x[1])[0]

    def random_selection(self):
        """Random server selection"""
        return random.choice(self.servers)

    def weighted_round_robin(self, weights):
        """Weighted round-robin"""
        total_weight = sum(weights.values())
        r = random.randint(1, total_weight)

        cumulative = 0
        for server, weight in weights.items():
            cumulative += weight
            if r <= cumulative:
                return server
```

## Best Practices

### Design Principles
- SOLID principles
- DRY (Don't Repeat Yourself)
- KISS (Keep It Simple, Stupid)
- YAGNI (You Aren't Gonna Need It)
- Separation of concerns
- Fail fast
- Design for failure

### Scalability
- Plan for growth early
- Use horizontal scaling
- Implement caching strategically
- Async where possible
- Database optimization
- Monitor everything
- Load test regularly

### Architecture
- Start with monolith, split when needed
- Define clear boundaries
- Use APIs for communication
- Version APIs properly
- Document architecture decisions
- Review regularly
- Keep it simple

## Anti-Patterns

❌ Premature optimization
❌ Over-engineering
❌ No monitoring
❌ Tight coupling
❌ God objects/classes
❌ No error handling
❌ Ignoring security

## Resources

- System Design Primer: https://github.com/donnemartin/system-design-primer
- Martin Fowler's Architecture: https://martinfowler.com/architecture/
- AWS Architecture: https://aws.amazon.com/architecture/
- Microservices.io: https://microservices.io/
