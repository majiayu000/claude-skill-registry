---
name: beazley-deep-python
description: Write Python code in the style of David Beazley, author of Python Cookbook. Emphasizes generators, coroutines, metaprogramming, and understanding Python's internals. Use when writing advanced Python that requires deep language mastery.
---

# David Beazley Style Guide

## Overview

David Beazley is the author of "Python Cookbook" and "Python Essential Reference," and a legendary instructor who teaches advanced Python. His specialty: generators, coroutines, concurrency, and metaprogramming—the deep magic of Python.

## Core Philosophy

> "Generators are the most powerful feature in Python."

> "Understanding how things work is more important than knowing how to use them."

> "Python is deeper than you think."

Beazley believes in **understanding Python's machinery**, not just its surface API. This understanding unlocks powerful patterns.

## Design Principles

1. **Generators for Everything**: Data pipelines, coroutines, state machines—generators are the answer.

2. **Understand the Protocol**: Before using a feature, understand the protocol it implements.

3. **Metaprogramming with Purpose**: Metaclasses and decorators are tools, not toys.

4. **Concurrency Done Right**: Understand the GIL, use async appropriately, know when threads help.

## When Writing Code

### Always

- Use generators for large data processing
- Understand what `yield` actually does
- Know the difference between iterators and iterables
- Use `contextlib` for simple context managers
- Profile before optimizing

### Never

- Load entire files into memory when streaming works
- Use threads for CPU-bound work in Python
- Create metaclasses without clear justification
- Ignore the GIL when reasoning about concurrency

### Prefer

- Generator pipelines over nested loops
- `yield from` over manual iteration
- `async`/`await` over callbacks
- `concurrent.futures` over raw threading

## Code Patterns

### Generator Pipelines

```python
# Process large files without loading into memory

def read_lines(filename):
    """Generate lines from a file."""
    with open(filename) as f:
        for line in f:
            yield line.strip()


def filter_comments(lines):
    """Filter out comment lines."""
    for line in lines:
        if not line.startswith('#'):
            yield line


def parse_records(lines):
    """Parse CSV-like records."""
    for line in lines:
        yield line.split(',')


def filter_by_field(records, field_index, value):
    """Filter records by field value."""
    for record in records:
        if record[field_index] == value:
            yield record


# Compose the pipeline
def process_log(filename, status):
    lines = read_lines(filename)
    lines = filter_comments(lines)
    records = parse_records(lines)
    records = filter_by_field(records, 2, status)
    return records


# Memory-efficient: only one line in memory at a time
for record in process_log('huge.log', 'ERROR'):
    print(record)
```

### Generator-Based State Machines

```python
def tcp_server():
    """A coroutine-based state machine."""
    while True:
        # Wait for connection
        client = yield 'WAITING'
        print(f'Connected: {client}')
        
        # Handle requests
        while True:
            request = yield 'CONNECTED'
            if request == 'QUIT':
                print(f'Client {client} disconnected')
                break
            response = process(request)
            yield response


# Drive the state machine
server = tcp_server()
next(server)  # Initialize, returns 'WAITING'
server.send('client-1')  # Connect, returns 'CONNECTED'
result = server.send('GET /data')  # Process request
server.send('QUIT')  # Disconnect
```

### Yield From for Delegation

```python
# Flatten nested structures with yield from

def flatten(items):
    """Recursively flatten nested iterables."""
    for item in items:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)  # Delegate to sub-generator
        else:
            yield item


nested = [1, [2, [3, 4], 5], 6, [7, 8]]
list(flatten(nested))  # [1, 2, 3, 4, 5, 6, 7, 8]


# Yield from for coroutine delegation
def subtask():
    for i in range(3):
        result = yield f'subtask-{i}'
        print(f'subtask received: {result}')


def main_task():
    print('Starting main task')
    yield from subtask()  # Delegate entirely
    print('Subtask complete')
    yield 'done'
```

### Context Managers with contextlib

```python
from contextlib import contextmanager, ExitStack

@contextmanager
def timer(name):
    """Time a block of code."""
    import time
    start = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start
        print(f'{name}: {elapsed:.3f}s')


@contextmanager
def temporary_attribute(obj, name, value):
    """Temporarily set an attribute."""
    old_value = getattr(obj, name, None)
    setattr(obj, name, value)
    try:
        yield
    finally:
        if old_value is None:
            delattr(obj, name)
        else:
            setattr(obj, name, old_value)


# Combining multiple context managers
@contextmanager
def managed_resources(*managers):
    """Combine multiple context managers."""
    with ExitStack() as stack:
        resources = [stack.enter_context(m) for m in managers]
        yield resources
```

### Metaprogramming: Descriptors and Metaclasses

```python
# Type-checking descriptor
class Typed:
    expected_type = object
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f'{self.name} must be {self.expected_type.__name__}')
        instance.__dict__[self.name] = value


class Integer(Typed):
    expected_type = int


class String(Typed):
    expected_type = str


# Metaclass for automatic slot generation
class SlotsMeta(type):
    def __new__(mcs, name, bases, namespace):
        # Collect all Typed descriptors
        slots = [key for key, value in namespace.items() 
                 if isinstance(value, Typed)]
        namespace['__slots__'] = slots
        return super().__new__(mcs, name, bases, namespace)


class Record(metaclass=SlotsMeta):
    name = String()
    age = Integer()
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
```

### Async/Await Patterns

```python
import asyncio

async def fetch_url(session, url):
    """Fetch a single URL."""
    async with session.get(url) as response:
        return await response.text()


async def fetch_all(urls, max_concurrent=10):
    """Fetch multiple URLs with concurrency limit."""
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def fetch_with_limit(session, url):
        async with semaphore:
            return await fetch_url(session, url)
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_with_limit(session, url) for url in urls]
        return await asyncio.gather(*tasks)


# Producer-consumer with async queues
async def producer(queue):
    for i in range(10):
        await queue.put(i)
        await asyncio.sleep(0.1)
    await queue.put(None)  # Sentinel


async def consumer(queue, name):
    while True:
        item = await queue.get()
        if item is None:
            queue.put_nowait(None)  # Pass sentinel on
            break
        print(f'{name} processing {item}')
        await asyncio.sleep(0.2)


async def main():
    queue = asyncio.Queue()
    await asyncio.gather(
        producer(queue),
        consumer(queue, 'A'),
        consumer(queue, 'B'),
    )
```

## Mental Model

Beazley approaches Python by understanding mechanisms:

1. **What protocol does this implement?** (Iterator? Context manager? Descriptor?)
2. **What does the interpreter actually do?** (How does `for` use `__iter__`?)
3. **Can this be lazy?** (Generator instead of list?)
4. **What's the memory profile?** (Stream vs. materialize?)

## Key Insights

- `yield` transforms a function into a **factory for iterators**
- Context managers are about **resource lifecycle**, not just `try/finally`
- Metaclasses control **class creation**, not instance creation
- The GIL means **threads don't parallelize CPU work**
- `async`/`await` is about **cooperative multitasking**, not true parallelism

