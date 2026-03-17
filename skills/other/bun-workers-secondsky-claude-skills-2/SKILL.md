---
name: Bun Workers
description: Use for Web Workers in Bun, worker_threads, parallel processing, and background tasks.
version: 1.0.0
---

# Bun Workers

Bun supports Web Workers and Node.js worker_threads for parallel execution.

## Web Workers

### Basic Usage

```typescript
// main.ts
const worker = new Worker(new URL("./worker.ts", import.meta.url));

worker.postMessage({ type: "start", data: [1, 2, 3, 4, 5] });

worker.onmessage = (event) => {
  console.log("Result:", event.data);
};

worker.onerror = (error) => {
  console.error("Worker error:", error.message);
};

// worker.ts
self.onmessage = (event) => {
  const { type, data } = event.data;

  if (type === "start") {
    const result = data.map((x) => x * 2);
    self.postMessage(result);
  }
};
```

### Worker with URL

```typescript
// Import from file path
const worker = new Worker(new URL("./worker.ts", import.meta.url));

// Or with blob URL
const code = `
  self.onmessage = (e) => {
    self.postMessage(e.data * 2);
  };
`;
const blob = new Blob([code], { type: "application/javascript" });
const worker = new Worker(URL.createObjectURL(blob));
```

### Transferable Objects

```typescript
// main.ts
const buffer = new ArrayBuffer(1024 * 1024); // 1MB
const view = new Uint8Array(buffer);
view.fill(42);

// Transfer ownership (zero-copy)
worker.postMessage({ buffer }, [buffer]);
// buffer is now detached (empty)

// worker.ts
self.onmessage = (event) => {
  const { buffer } = event.data;
  const view = new Uint8Array(buffer);
  // Process buffer...

  // Transfer back
  self.postMessage({ buffer }, [buffer]);
};
```

### Shared Memory

```typescript
// main.ts
const shared = new SharedArrayBuffer(1024);
const view = new Int32Array(shared);

worker.postMessage({ shared });

// Both main and worker can access
Atomics.add(view, 0, 1);

// worker.ts
self.onmessage = (event) => {
  const { shared } = event.data;
  const view = new Int32Array(shared);

  // Atomic operations for thread safety
  Atomics.add(view, 0, 1);
  Atomics.notify(view, 0);
};
```

## Node.js worker_threads

```typescript
// main.ts
import { Worker, isMainThread, parentPort, workerData } from "worker_threads";

if (isMainThread) {
  const worker = new Worker(import.meta.filename, {
    workerData: { numbers: [1, 2, 3, 4, 5] },
  });

  worker.on("message", (result) => {
    console.log("Result:", result);
  });

  worker.on("error", (err) => {
    console.error("Error:", err);
  });

  worker.on("exit", (code) => {
    console.log("Worker exited with code:", code);
  });
} else {
  // Worker code
  const { numbers } = workerData;
  const sum = numbers.reduce((a, b) => a + b, 0);
  parentPort?.postMessage(sum);
}
```

### Worker Pool

```typescript
// worker-pool.ts
import { Worker } from "worker_threads";

class WorkerPool {
  private workers: Worker[] = [];
  private queue: Array<{
    task: any;
    resolve: (value: any) => void;
    reject: (err: Error) => void;
  }> = [];
  private activeWorkers = new Set<Worker>();

  constructor(
    private workerPath: string,
    private poolSize: number
  ) {
    for (let i = 0; i < poolSize; i++) {
      this.addWorker();
    }
  }

  private addWorker() {
    const worker = new Worker(this.workerPath);

    worker.on("message", (result) => {
      this.activeWorkers.delete(worker);
      this.processQueue();
    });

    worker.on("error", (err) => {
      this.activeWorkers.delete(worker);
      console.error("Worker error:", err);
    });

    this.workers.push(worker);
  }

  async execute(task: any): Promise<any> {
    return new Promise((resolve, reject) => {
      this.queue.push({ task, resolve, reject });
      this.processQueue();
    });
  }

  private processQueue() {
    for (const worker of this.workers) {
      if (!this.activeWorkers.has(worker) && this.queue.length > 0) {
        const { task, resolve, reject } = this.queue.shift()!;
        this.activeWorkers.add(worker);

        worker.once("message", resolve);
        worker.once("error", reject);
        worker.postMessage(task);
      }
    }
  }

  terminate() {
    this.workers.forEach((w) => w.terminate());
  }
}

// Usage
const pool = new WorkerPool("./worker.ts", 4);
const results = await Promise.all([
  pool.execute({ task: 1 }),
  pool.execute({ task: 2 }),
  pool.execute({ task: 3 }),
]);
pool.terminate();
```

## Patterns

### CPU-Intensive Tasks

```typescript
// main.ts
const worker = new Worker(new URL("./cpu-worker.ts", import.meta.url));

// Process large dataset
const data = Array.from({ length: 1000000 }, () => Math.random());

worker.postMessage({ type: "process", data });

worker.onmessage = (event) => {
  if (event.data.type === "progress") {
    console.log(`Progress: ${event.data.percent}%`);
  } else if (event.data.type === "result") {
    console.log("Done:", event.data.result);
  }
};

// cpu-worker.ts
self.onmessage = (event) => {
  const { type, data } = event.data;

  if (type === "process") {
    const chunkSize = 10000;
    let result = 0;

    for (let i = 0; i < data.length; i++) {
      result += Math.sqrt(data[i]);

      // Report progress
      if (i % chunkSize === 0) {
        self.postMessage({
          type: "progress",
          percent: Math.round((i / data.length) * 100),
        });
      }
    }

    self.postMessage({ type: "result", result });
  }
};
```

### Parallel Map

```typescript
async function parallelMap<T, R>(
  items: T[],
  fn: string, // Function name in worker
  workerUrl: URL,
  concurrency = 4
): Promise<R[]> {
  const results: R[] = new Array(items.length);
  const workers: Worker[] = [];

  // Create workers
  for (let i = 0; i < concurrency; i++) {
    workers.push(new Worker(workerUrl));
  }

  // Process items
  let nextIndex = 0;
  const processNext = (worker: Worker): Promise<void> => {
    return new Promise((resolve) => {
      if (nextIndex >= items.length) {
        resolve();
        return;
      }

      const index = nextIndex++;
      worker.postMessage({ fn, item: items[index], index });

      worker.onmessage = (event) => {
        results[event.data.index] = event.data.result;
        processNext(worker).then(resolve);
      };
    });
  };

  await Promise.all(workers.map(processNext));

  workers.forEach((w) => w.terminate());
  return results;
}
```

### Message Channel

```typescript
// Create channel for worker-to-worker communication
const channel = new MessageChannel();

const worker1 = new Worker(new URL("./worker1.ts", import.meta.url));
const worker2 = new Worker(new URL("./worker2.ts", import.meta.url));

// Give each worker a port
worker1.postMessage({ port: channel.port1 }, [channel.port1]);
worker2.postMessage({ port: channel.port2 }, [channel.port2]);

// worker1.ts
let port: MessagePort;
self.onmessage = (event) => {
  if (event.data.port) {
    port = event.data.port;
    port.onmessage = (e) => console.log("From worker2:", e.data);
    port.postMessage("Hello from worker1!");
  }
};
```

## Error Handling

```typescript
const worker = new Worker(new URL("./worker.ts", import.meta.url));

worker.onerror = (error) => {
  console.error("Uncaught error in worker:", error.message);
  error.preventDefault(); // Prevent bubbling
};

worker.onmessageerror = (event) => {
  console.error("Message deserialization failed");
};

// In worker
self.onerror = (error) => {
  self.postMessage({ type: "error", message: error.message });
};
```

## Termination

```typescript
const worker = new Worker(new URL("./worker.ts", import.meta.url));

// Request graceful shutdown
worker.postMessage({ type: "shutdown" });

// Force terminate after timeout
setTimeout(() => {
  worker.terminate();
}, 5000);

// In worker
self.onmessage = (event) => {
  if (event.data.type === "shutdown") {
    // Cleanup
    self.close();
  }
};
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Worker not found` | Wrong URL | Check worker file path |
| `Cannot serialize` | Non-transferable data | Use transferable objects |
| `DataCloneError` | Functions/DOM in message | Send only serializable data |
| `Worker terminated` | Premature terminate | Check termination logic |

## When to Load References

Load `references/optimization.md` when:
- Worker pool tuning
- Memory management
- Performance profiling

Load `references/patterns.md` when:
- Complex coordination
- Backpressure handling
- Error recovery
