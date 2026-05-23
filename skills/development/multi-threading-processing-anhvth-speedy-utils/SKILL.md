---
name: 'multi-threading-processing'
description: 'Comprehensive guide for using multi-threading and multi-processing in Python, including when to choose each approach, best practices, and practical examples using the speedy_utils library.'
---

# Multi-Threading and Multi-Processing Guide

This skill provides comprehensive guidance for implementing concurrent and parallel processing in Python applications. It covers when to use multi-threading vs multi-processing, best practices, performance considerations, and practical examples using the `speedy_utils` library's multi-worker implementations.

## When to Use Multi-Threading vs Multi-Processing

### Multi-Threading (Use for I/O-bound tasks)

**Best for:**
- Network requests (HTTP, database queries, API calls)
- File I/O operations (reading/writing files)
- GUI applications that need to remain responsive
- Tasks waiting for external resources

**When to choose threading:**
```python
# I/O-bound example: Downloading multiple files
import requests
from speedy_utils import multi_thread

def download_file(url):
    response = requests.get(url)
    return len(response.content)

urls = ['https://example.com/file1', 'https://example.com/file2']
results = multi_thread(download_file, urls, workers=10)
```

### Multi-Processing (Use for CPU-bound tasks)

**Best for:**
- CPU-intensive computations (mathematical calculations, data processing)
- Image/video processing
- Machine learning model training/inference
- Scientific computing

**When to choose processing:**
```python
# CPU-bound example: Heavy computation
from speedy_utils import multi_process

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

numbers = list(range(30, 35))
results = multi_process(fibonacci, numbers, workers=4)
```

### Key Decision Factors

| Factor | Multi-Threading | Multi-Processing |
|--------|----------------|------------------|
| **GIL Impact** | Limited by GIL | Bypasses GIL |
| **Memory** | Shared memory | Separate memory spaces |
| **Communication** | Easy (shared variables) | Complex (pickling required) |
| **Overhead** | Low | High (process creation) |
| **Scalability** | Limited by cores | Scales with cores |
| **Debugging** | Easier | More complex |

## Best Practices

### 1. Choose the Right Backend

The `speedy_utils` library provides multiple backends:

```python
from speedy_utils import multi_process

# For I/O-bound tasks
results = multi_process(func, items, backend='threadpool')

# For CPU-bound tasks
results = multi_process(func, items, backend='mp')  # multiprocessing

# For distributed computing (if Ray available)
results = multi_process(func, items, backend='ray')
```

### 2. Optimize Worker Count

```python
import os
from speedy_utils import multi_thread

# For threading: Use more workers than CPU cores
cpu_count = os.cpu_count() or 4
thread_workers = cpu_count * 2  # Good starting point

# For processing: Match CPU cores (or slightly less)
process_workers = max(1, cpu_count - 1)

results = multi_thread(func, items, workers=thread_workers)
```

### 3. Handle Errors Gracefully

```python
# Continue processing even if some tasks fail
results = multi_thread(
    func,
    items,
    stop_on_error=False,  # Don't abort on first error
    workers=4
)

# Check for None values (failed tasks)
successful_results = [r for r in results if r is not None]
failed_count = results.count(None)
```

### 4. Use Batching for Small Tasks

```python
# For many small tasks, batch them to reduce overhead
def process_batch(items):
    return [item * 2 for item in items]

results = multi_thread(
    process_batch,
    items,
    batch=10,  # Process 10 items per task
    workers=4
)
```

### 5. Monitor and Clean Up Resources

```python
from speedy_utils import kill_all_thread, cleanup_phantom_workers

# Force cleanup of stuck threads/processes
killed_threads = kill_all_thread()
killed_processes = cleanup_phantom_workers()
```

## Performance Considerations

### Memory Usage

**Threading:** Shared memory, lower overhead
```python
# Threads share memory - efficient for large datasets
large_data = load_large_dataset()
results = multi_thread(process_item, large_data, workers=8)
```

**Processing:** Separate memory spaces, higher overhead
```python
# Each process gets a copy - use for CPU-bound work
results = multi_process(cpu_intensive_func, data, workers=4)
```

### Communication Between Workers

**Threading:** Easy communication
```python
shared_results = []
lock = threading.Lock()

def thread_safe_append(item):
    with lock:
        shared_results.append(process_item(item))

multi_thread(thread_safe_append, items, workers=4)
```

**Processing:** Requires serialization
```python
# Use return values or shared storage
def process_and_return(item):
    result = heavy_computation(item)
    return result  # Pickled and sent back

results = multi_process(process_and_return, items, workers=4)
```

## Common Patterns and Examples

### Pattern 1: Parallel Data Processing

```python
from speedy_utils import multi_thread
import pandas as pd

def process_dataframe_chunk(chunk):
    # Process a chunk of data
    return chunk['value'].sum()

# Split large dataframe into chunks
df = pd.read_csv('large_file.csv')
chunks = [df[i:i+1000] for i in range(0, len(df), 1000)]

results = multi_thread(process_dataframe_chunk, chunks, workers=8)
total = sum(results)
```

### Pattern 2: Concurrent API Calls

```python
import aiohttp
from speedy_utils import multi_thread

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

def fetch_multiple_urls(urls):
    async def main():
        async with aiohttp.ClientSession() as session:
            tasks = [fetch_url(session, url) for url in urls]
            return await asyncio.gather(*tasks)

    return asyncio.run(main())

results = multi_thread(fetch_multiple_urls, [urls], workers=1)  # Single async task
```

### Pattern 3: CPU-Intensive Computation

```python
from speedy_utils import multi_process
from PIL import Image
import numpy as np

def process_image(image_path):
    img = Image.open(image_path)
    # Heavy image processing
    processed = np.array(img) ** 2  # Example computation
    return processed.mean()

image_paths = ['image1.jpg', 'image2.jpg', ...]
results = multi_process(process_image, image_paths, workers=4)
```

## Error Handling and Debugging

### Custom Exception Handling

```python
from speedy_utils import multi_thread

def risky_operation(x):
    if x == 42:
        raise ValueError(f"Bad input: {x}")
    return x * 2

# Catch and handle errors
try:
    results = multi_thread(risky_operation, range(100), stop_on_error=True)
except Exception as e:
    print(f"Processing failed: {e}")
    # Handle error appropriately
```

### Logging and Monitoring

```python
import logging
from speedy_utils import multi_thread

logging.basicConfig(level=logging.INFO)

def monitored_task(item):
    logging.info(f"Processing item: {item}")
    result = process_item(item)
    logging.info(f"Completed item: {item}")
    return result

results = multi_thread(monitored_task, items, workers=4)
```

## Integration with Other Libraries

### With tqdm for Progress Bars

```python
from speedy_utils import multi_thread

def slow_task(x):
    time.sleep(0.1)  # Simulate work
    return x ** 2

# Automatic progress bar
results = multi_thread(slow_task, range(100), progress=True)
```

### With Ray for Distributed Computing

```python
from speedy_utils import multi_process

# Automatically uses Ray if available
results = multi_process(
    heavy_computation,
    large_dataset,
    backend='ray',
    workers=16  # Can exceed local cores
)
```

### With Pandas

```python
import pandas as pd
from speedy_utils import multi_thread

def process_row(row):
    # Process a single row
    return row['value'] * 2

df = pd.read_csv('data.csv')

# Process rows in parallel
results = multi_thread(process_row, df.to_dict('records'), workers=8)
processed_df = pd.DataFrame(results)
```

## Performance Benchmarking

### Compare Different Approaches

```python
import time
from speedy_utils import multi_thread, multi_process

def benchmark_func(x):
    # Some computation
    return sum(i**2 for i in range(x))

data = list(range(100, 200))

# Benchmark threading
start = time.time()
thread_results = multi_thread(benchmark_func, data, workers=8, progress=False)
thread_time = time.time() - start

# Benchmark processing
start = time.time()
process_results = multi_process(benchmark_func, data, workers=4, progress=False, backend='safe')
process_time = time.time() - start

# Benchmark sequential
start = time.time()
sequential_results = [benchmark_func(x) for x in data]
sequential_time = time.time() - start

print(f"Threading: {thread_time:.2f}s")
print(f"Processing: {process_time:.2f}s")
print(f"Sequential: {sequential_time:.2f}s")
```

## Troubleshooting Common Issues

### 1. GIL Limitations

**Problem:** Python's GIL prevents true parallel execution in threads for CPU-bound tasks.

**Solution:** Use multi-processing for CPU-bound work.

### 2. Pickle Errors

**Problem:** Functions/objects can't be pickled for inter-process communication.

**Solution:** Define functions at module level, avoid lambdas.

```python
# Good: Module-level function
def process_item(x):
    return x * 2

# Bad: Lambda
lambda x: x * 2  # Can't be pickled
```

### 3. Memory Issues

**Problem:** Large datasets copied to each process.

**Solution:** Use threading for large data, or lazy loading.

### 4. Deadlocks

**Problem:** Threads/processes waiting indefinitely.

**Solution:** Use timeouts and proper cleanup.

```python
results = multi_thread(
    func,
    items,
    timeout=300,  # 5 minute timeout
    workers=4
)
```

## Advanced Topics

### Custom Worker Pools

```python
from concurrent.futures import ThreadPoolExecutor
from speedy_utils.multi_worker.thread import _track_executor_threads

def custom_processing(items, workers=4):
    with ThreadPoolExecutor(max_workers=workers) as executor:
        _track_executor_threads(executor)  # Track for cleanup
        futures = [executor.submit(func, item) for item in items]
        return [f.result() for f in futures]
```

### Async Integration

```python
import asyncio
from speedy_utils import multi_thread

async def async_task(x):
    await asyncio.sleep(0.1)
    return x * 2

def run_async_tasks(items):
    async def main():
        return await asyncio.gather(*[async_task(x) for x in items])

    return asyncio.run(main())

# Run multiple async batches in parallel
batches = [items[i:i+10] for i in range(0, len(items), 10)]
results = multi_thread(run_async_tasks, batches, workers=4)
```

## References

This skill leverages the `speedy_utils` library's multi-worker implementations:

- `speedy_utils.multi_thread()` - Advanced threading with batching, progress bars, and error handling
- `speedy_utils.multi_process()` - Multi-processing with multiple backends (Ray, multiprocessing, threading)
- `speedy_utils.kill_all_thread()` - Emergency thread cleanup
- `speedy_utils.cleanup_phantom_workers()` - Process cleanup utilities

See the library's test files for additional examples and edge cases.