---
name: Concurrency and Throughput
description: Comprehensive guide to concurrency models, throughput optimization, worker pools, task queues, and scaling strategies for high-performance applications
---

# Concurrency and Throughput

## Concurrency vs Parallelism

### Definitions

**Concurrency:**
- **Structure**: Dealing with many things at once
- **Example**: Single chef switching between multiple dishes
- **Implementation**: Event loop, async/await, coroutines

**Parallelism:**
- **Execution**: Doing many things at once
- **Example**: Multiple chefs each cooking a dish
- **Implementation**: Multiple threads, processes, CPU cores

### Visual Representation

```
Concurrency (Single Core):
Time →
CPU: [Task A][Task B][Task A][Task C][Task B][Task A]
     (Context switching between tasks)

Parallelism (Multi-Core):
Time →
CPU 1: [Task A][Task A][Task A][Task A]
CPU 2: [Task B][Task B][Task B][Task B]
CPU 3: [Task C][Task C][Task C][Task C]
     (Tasks running simultaneously)
```

---

## Throughput vs Latency

### Definitions

**Throughput:**
- **Measure**: Requests per second (RPS)
- **Goal**: Maximize total work done
- **Example**: 1000 requests/second

**Latency:**
- **Measure**: Time per request (milliseconds)
- **Goal**: Minimize time for single request
- **Example**: 50ms per request

### Trade-off

Often inverse relationship:
- **High Throughput**: May increase latency (batching, queuing)
- **Low Latency**: May reduce throughput (immediate processing)

**Example:**
```
Scenario 1: Low Latency
- Process each request immediately
- Latency: 10ms
- Throughput: 100 req/s

Scenario 2: High Throughput
- Batch 10 requests together
- Latency: 50ms (includes wait time)
- Throughput: 500 req/s
```

---

## Node.js Concurrency Model

### 1. Single-Threaded Event Loop

**How it Works:**
```
┌───────────────────────────┐
│        Event Loop         │
│                           │
│  ┌─────────────────────┐  │
│  │  Call Stack         │  │
│  └─────────────────────┘  │
│  ┌─────────────────────┐  │
│  │  Callback Queue     │  │
│  └─────────────────────┘  │
│  ┌─────────────────────┐  │
│  │  Microtask Queue    │  │
│  └─────────────────────┘  │
└───────────────────────────┘
```

**Characteristics:**
- Single JavaScript thread
- Non-blocking I/O
- Event-driven architecture

**Example:**
```javascript
console.log('1');

setTimeout(() => console.log('2'), 0);

Promise.resolve().then(() => console.log('3'));

console.log('4');

// Output: 1, 4, 3, 2
// (Synchronous → Microtasks → Macrotasks)
```

### 2. Non-Blocking I/O

**Bad (Blocking):**
```javascript
const fs = require('fs');

// Blocks event loop!
const data = fs.readFileSync('large-file.txt');
console.log(data);
```

**Good (Non-Blocking):**
```javascript
const fs = require('fs').promises;

// Doesn't block event loop
const data = await fs.readFile('large-file.txt');
console.log(data);
```

### 3. Worker Threads (CPU-Intensive Tasks)

**Use Case:** CPU-intensive operations (image processing, encryption)

```javascript
const { Worker } = require('worker_threads');

function runWorker(data) {
  return new Promise((resolve, reject) => {
    const worker = new Worker('./worker.js', {
      workerData: data
    });
    
    worker.on('message', resolve);
    worker.on('error', reject);
    worker.on('exit', (code) => {
      if (code !== 0) {
        reject(new Error(`Worker stopped with exit code ${code}`));
      }
    });
  });
}

// Usage
const result = await runWorker({ input: 'data' });
```

**worker.js:**
```javascript
const { parentPort, workerData } = require('worker_threads');

// CPU-intensive work
function processData(data) {
  // Heavy computation
  let result = 0;
  for (let i = 0; i < 1000000000; i++) {
    result += i;
  }
  return result;
}

const result = processData(workerData);
parentPort.postMessage(result);
```

### 4. Cluster Mode (Multiple Processes)

**Use Case:** Utilize all CPU cores

```javascript
const cluster = require('cluster');
const http = require('http');
const numCPUs = require('os').cpus().length;

if (cluster.isMaster) {
  console.log(`Master ${process.pid} is running`);
  
  // Fork workers
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }
  
  cluster.on('exit', (worker, code, signal) => {
    console.log(`Worker ${worker.process.pid} died`);
    cluster.fork(); // Restart worker
  });
} else {
  // Workers share TCP connection
  http.createServer((req, res) => {
    res.writeHead(200);
    res.end('Hello World\n');
  }).listen(8000);
  
  console.log(`Worker ${process.pid} started`);
}
```

---

## Python Concurrency

### 1. asyncio (Async/Await)

**Use Case:** I/O-bound tasks (network requests, database queries)

```python
import asyncio
import aiohttp

async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    urls = ['http://example.com' for _ in range(10)]
    
    # Run concurrently
    tasks = [fetch_url(url) for url in urls]
    results = await asyncio.gather(*tasks)
    
    return results

# Run
asyncio.run(main())
```

### 2. Threading (I/O-Bound Tasks)

**Use Case:** I/O-bound tasks with libraries that don't support asyncio

```python
import threading
import requests

def fetch_url(url):
    response = requests.get(url)
    return response.text

# Create threads
threads = []
results = []

for i in range(10):
    thread = threading.Thread(target=lambda: results.append(fetch_url('http://example.com')))
    threads.append(thread)
    thread.start()

# Wait for all threads
for thread in threads:
    thread.join()

print(f"Fetched {len(results)} URLs")
```

### 3. Multiprocessing (CPU-Bound Tasks)

**Use Case:** CPU-intensive operations (data processing, ML training)

```python
from multiprocessing import Pool

def process_data(data):
    # CPU-intensive work
    result = sum(i ** 2 for i in range(1000000))
    return result

if __name__ == '__main__':
    with Pool(processes=4) as pool:
        results = pool.map(process_data, range(10))
    
    print(results)
```

### 4. GIL (Global Interpreter Lock) Limitations

**Problem:**
- Only one thread executes Python bytecode at a time
- Threading doesn't help for CPU-bound tasks

**Solution:**
- Use `multiprocessing` for CPU-bound tasks
- Use `asyncio` or `threading` for I/O-bound tasks

**Example:**
```python
# BAD: Threading for CPU-bound (GIL limits performance)
import threading

def cpu_intensive():
    return sum(i ** 2 for i in range(10000000))

threads = [threading.Thread(target=cpu_intensive) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()
# Slower than single-threaded due to GIL!

# GOOD: Multiprocessing for CPU-bound
from multiprocessing import Pool

with Pool(4) as pool:
    results = pool.map(lambda _: sum(i ** 2 for i in range(10000000)), range(4))
# Actually uses 4 cores!
```

---

## Concurrency Patterns

### 1. Worker Pools (Fixed Number of Workers)

**Use Case:** Limit concurrency to prevent resource exhaustion

**Node.js:**
```javascript
class WorkerPool {
  constructor(maxWorkers = 10) {
    this.maxWorkers = maxWorkers;
    this.activeWorkers = 0;
    this.queue = [];
  }
  
  async execute(task) {
    // Wait if pool is full
    while (this.activeWorkers >= this.maxWorkers) {
      await new Promise(resolve => this.queue.push(resolve));
    }
    
    this.activeWorkers++;
    
    try {
      return await task();
    } finally {
      this.activeWorkers--;
      
      // Process next task in queue
      const next = this.queue.shift();
      if (next) next();
    }
  }
}

// Usage
const pool = new WorkerPool(5);

const tasks = Array.from({ length: 100 }, (_, i) => 
  () => fetch(`https://api.example.com/item/${i}`)
);

const results = await Promise.all(
  tasks.map(task => pool.execute(task))
);
```

**Python:**
```python
import asyncio
from asyncio import Semaphore

async def worker_pool(tasks, max_workers=10):
    semaphore = Semaphore(max_workers)
    
    async def execute(task):
        async with semaphore:
            return await task()
    
    return await asyncio.gather(*[execute(task) for task in tasks])

# Usage
tasks = [lambda: fetch_url(f'https://api.example.com/item/{i}') for i in range(100)]
results = await worker_pool(tasks, max_workers=5)
```

### 2. Task Queues (Redis Queue, Celery, Bull)

**Use Case:** Decouple request from processing, handle background jobs

**Architecture:**
```
Client → API → Queue → Worker → Database
                 ↓
              (Redis)
```

**Benefits:**
- Asynchronous processing
- Retry failed jobs
- Priority queues
- Rate limiting

### 3. Rate Limiting (Control Concurrency)

**Use Case:** Prevent overwhelming external APIs or databases

**Node.js (Bottleneck):**
```javascript
const Bottleneck = require('bottleneck');

const limiter = new Bottleneck({
  maxConcurrent: 5,  // Max 5 concurrent requests
  minTime: 200       // Min 200ms between requests
});

// Wrap API calls
const fetchWithLimit = limiter.wrap(async (url) => {
  const response = await fetch(url);
  return response.json();
});

// Usage
const results = await Promise.all(
  urls.map(url => fetchWithLimit(url))
);
```

**Python (aiolimiter):**
```python
from aiolimiter import AsyncLimiter
import asyncio

limiter = AsyncLimiter(max_rate=10, time_period=1)  # 10 req/s

async def fetch_with_limit(url):
    async with limiter:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()

# Usage
results = await asyncio.gather(*[fetch_with_limit(url) for url in urls])
```

### 4. Backpressure (Slow Down When Overwhelmed)

**Use Case:** Prevent memory exhaustion from fast producers

**Node.js (Streams):**
```javascript
const { Transform } = require('stream');

const processStream = new Transform({
  highWaterMark: 10,  // Buffer size
  
  async transform(chunk, encoding, callback) {
    // Process data
    const result = await processData(chunk);
    
    // Backpressure: Pause if buffer full
    if (!this.push(result)) {
      console.log('Backpressure: Pausing...');
    }
    
    callback();
  }
});

inputStream
  .pipe(processStream)
  .pipe(outputStream);
```

---

## Queue-Based Architecture

### Benefits

1. **Decouple Request from Processing**
   - API responds immediately
   - Processing happens asynchronously

2. **Handle Traffic Spikes**
   - Queue absorbs burst traffic
   - Workers process at steady rate

3. **Retry Failed Jobs**
   - Automatic retry with exponential backoff
   - Dead letter queue for permanent failures

4. **Priority Queues**
   - Process important jobs first
   - Multiple queues with different priorities

### Architecture

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌──────────┐
│  Client │ --> │   API   │ --> │  Queue  │ --> │  Worker  │
└─────────┘     └─────────┘     └─────────┘     └──────────┘
                     │               │                │
                     │               │                ↓
                     │               │           ┌──────────┐
                     │               │           │ Database │
                     │               │           └──────────┘
                     ↓               ↓
                Response         (Redis/RabbitMQ)
```

---

## Task Queue Systems

### 1. Node.js: Bull (Redis-Based)

**Installation:**
```bash
npm install bull
```

**Producer (Add Jobs):**
```javascript
const Queue = require('bull');

const emailQueue = new Queue('email', {
  redis: { host: 'localhost', port: 6379 }
});

// Add job to queue
await emailQueue.add('send-welcome', {
  to: 'user@example.com',
  subject: 'Welcome!',
  body: 'Thanks for signing up'
}, {
  attempts: 3,           // Retry 3 times
  backoff: {
    type: 'exponential',
    delay: 2000          // 2s, 4s, 8s
  },
  priority: 1            // Higher = more important
});

console.log('Email job queued');
```

**Consumer (Process Jobs):**
```javascript
const Queue = require('bull');

const emailQueue = new Queue('email', {
  redis: { host: 'localhost', port: 6379 }
});

// Process jobs
emailQueue.process('send-welcome', async (job) => {
  const { to, subject, body } = job.data;
  
  console.log(`Sending email to ${to}...`);
  await sendEmail(to, subject, body);
  
  return { sent: true };
});

// Handle completed jobs
emailQueue.on('completed', (job, result) => {
  console.log(`Job ${job.id} completed:`, result);
});

// Handle failed jobs
emailQueue.on('failed', (job, err) => {
  console.error(`Job ${job.id} failed:`, err);
});
```

### 2. Python: Celery (RabbitMQ/Redis)

**Installation:**
```bash
pip install celery redis
```

**celery_app.py:**
```python
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task(bind=True, max_retries=3)
def send_email(self, to, subject, body):
    try:
        print(f'Sending email to {to}...')
        # Send email logic
        return {'sent': True}
    except Exception as exc:
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)
```

**Producer:**
```python
from celery_app import send_email

# Add job to queue
result = send_email.delay('user@example.com', 'Welcome!', 'Thanks for signing up')
print(f'Job queued: {result.id}')
```

**Worker:**
```bash
celery -A celery_app worker --loglevel=info
```

### 3. BullMQ (Modern Bull Alternative)

**Features:**
- Better performance
- Better TypeScript support
- More features (rate limiting, job scheduling)

**Usage:**
```javascript
const { Queue, Worker } = require('bullmq');

const queue = new Queue('email', {
  connection: { host: 'localhost', port: 6379 }
});

// Add job
await queue.add('send-welcome', { to: 'user@example.com' });

// Process jobs
const worker = new Worker('email', async (job) => {
  console.log(`Processing job ${job.id}`);
  await sendEmail(job.data.to);
}, {
  connection: { host: 'localhost', port: 6379 },
  concurrency: 5  // Process 5 jobs concurrently
});
```

---

## Worker Pool Sizing

### I/O-Bound Tasks

**Rule:** More workers than CPU cores

**Reasoning:**
- Workers spend most time waiting for I/O
- Can handle many concurrent requests

**Example:**
```javascript
// 4 CPU cores, but 20 workers (I/O-bound)
const pool = new WorkerPool(20);
```

### CPU-Bound Tasks

**Rule:** Workers = CPU cores

**Reasoning:**
- More workers = more context switching overhead
- No benefit from more workers than cores

**Example:**
```javascript
const numCPUs = require('os').cpus().length;
const pool = new WorkerPool(numCPUs); // 4 workers for 4 cores
```

### Mixed Workload

**Rule:** Separate pools for each type

**Example:**
```javascript
const ioPool = new WorkerPool(20);    // I/O-bound tasks
const cpuPool = new WorkerPool(4);    // CPU-bound tasks

// Route tasks to appropriate pool
if (task.type === 'io') {
  await ioPool.execute(task);
} else {
  await cpuPool.execute(task);
}
```

---

## Connection Pooling

### 1. Database Connection Pooling

**Why:**
- Creating connections is expensive (100-500ms)
- Reuse connections for better performance

**PostgreSQL (Prisma):**
```javascript
const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient({
  datasources: {
    db: {
      url: 'postgresql://user:pass@localhost:5432/db?connection_limit=20'
    }
  }
});
```

**PostgreSQL (pg):**
```javascript
const { Pool } = require('pg');

const pool = new Pool({
  host: 'localhost',
  port: 5432,
  database: 'mydb',
  user: 'user',
  password: 'password',
  max: 20,              // Max connections
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000
});

// Usage
const result = await pool.query('SELECT * FROM users WHERE id = $1', [123]);
```

**Python (SQLAlchemy):**
```python
from sqlalchemy import create_engine

engine = create_engine(
    'postgresql://user:pass@localhost:5432/db',
    pool_size=20,           # Max connections
    max_overflow=10,        # Extra connections if pool full
    pool_timeout=30,        # Wait 30s for connection
    pool_recycle=3600       # Recycle connections after 1h
)
```

### 2. HTTP Connection Pooling (Keep-Alive)

**Node.js (axios):**
```javascript
const axios = require('axios');
const http = require('http');
const https = require('https');

const httpAgent = new http.Agent({ keepAlive: true, maxSockets: 50 });
const httpsAgent = new https.Agent({ keepAlive: true, maxSockets: 50 });

const client = axios.create({
  httpAgent,
  httpsAgent
});

// Reuses connections
await client.get('https://api.example.com/data');
```

**Python (requests):**
```python
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()

# Connection pooling
adapter = HTTPAdapter(
    pool_connections=10,
    pool_maxsize=50,
    max_retries=Retry(total=3, backoff_factor=0.3)
)

session.mount('http://', adapter)
session.mount('https://', adapter)

# Reuses connections
response = session.get('https://api.example.com/data')
```

### 3. Redis Connection Pooling

**Node.js (ioredis):**
```javascript
const Redis = require('ioredis');

const redis = new Redis({
  host: 'localhost',
  port: 6379,
  maxRetriesPerRequest: 3,
  lazyConnect: true,
  // Connection pool managed automatically
});
```

---

## Async/Await Patterns

### 1. Promise.all() for Parallel Execution

**Sequential (Slow):**
```javascript
const user = await getUser(1);      // 100ms
const posts = await getPosts(1);    // 100ms
const comments = await getComments(1); // 100ms
// Total: 300ms
```

**Parallel (Fast):**
```javascript
const [user, posts, comments] = await Promise.all([
  getUser(1),
  getPosts(1),
  getComments(1)
]);
// Total: 100ms (all run concurrently)
```

### 2. Promise.allSettled() for Error Handling

**Problem with Promise.all():**
```javascript
// If one fails, all fail
const results = await Promise.all([
  fetch('https://api1.com'),
  fetch('https://api2.com'),  // Fails!
  fetch('https://api3.com')
]);
// Throws error, loses results from api1 and api3
```

**Solution with Promise.allSettled():**
```javascript
const results = await Promise.allSettled([
  fetch('https://api1.com'),
  fetch('https://api2.com'),  // Fails
  fetch('https://api3.com')
]);

// All results available
results.forEach((result, i) => {
  if (result.status === 'fulfilled') {
    console.log(`API ${i + 1} succeeded:`, result.value);
  } else {
    console.error(`API ${i + 1} failed:`, result.reason);
  }
});
```

### 3. Avoid Async Overhead for Sync Operations

**Bad:**
```javascript
// Unnecessary async overhead
async function add(a, b) {
  return a + b;
}

const result = await add(1, 2);
```

**Good:**
```javascript
// Synchronous (no overhead)
function add(a, b) {
  return a + b;
}

const result = add(1, 2);
```

---

## Batching Strategies

### 1. Batch API Requests

**Sequential (Slow):**
```javascript
for (const id of userIds) {
  const user = await fetch(`https://api.example.com/users/${id}`);
  users.push(user);
}
// 100 users = 100 requests
```

**Batched (Fast):**
```javascript
// Single request with all IDs
const users = await fetch('https://api.example.com/users/batch', {
  method: 'POST',
  body: JSON.stringify({ ids: userIds })
});
// 100 users = 1 request
```

### 2. Batch Database Writes

**Sequential (Slow):**
```javascript
for (const user of users) {
  await db.users.create({ data: user });
}
// 100 users = 100 queries
```

**Batched (Fast):**
```javascript
await db.users.createMany({ data: users });
// 100 users = 1 query
```

### 3. Debouncing/Throttling

**Debouncing (Wait for Pause):**
```javascript
let timeout;

function debounce(func, delay) {
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), delay);
  };
}

// Usage: Only search after user stops typing for 300ms
const debouncedSearch = debounce(search, 300);
input.addEventListener('input', (e) => debouncedSearch(e.target.value));
```

**Throttling (Limit Rate):**
```javascript
let lastRun = 0;

function throttle(func, limit) {
  return (...args) => {
    const now = Date.now();
    if (now - lastRun >= limit) {
      func(...args);
      lastRun = now;
    }
  };
}

// Usage: Only update scroll position every 100ms
const throttledScroll = throttle(updateScrollPosition, 100);
window.addEventListener('scroll', throttledScroll);
```

### 4. DataLoader Pattern (GraphQL)

**Problem: N+1 Queries**
```javascript
// Resolver called for each user
const posts = users.map(user => getPosts(user.id));
// 100 users = 100 queries
```

**Solution: DataLoader**
```javascript
const DataLoader = require('dataloader');

const postLoader = new DataLoader(async (userIds) => {
  // Batch query
  const posts = await db.posts.findMany({
    where: { userId: { in: userIds } }
  });
  
  // Group by userId
  return userIds.map(id => posts.filter(post => post.userId === id));
});

// Usage (automatically batched)
const posts = await Promise.all(users.map(user => postLoader.load(user.id)));
// 100 users = 1 query
```

---

## Streaming for Large Datasets

### 1. Stream Processing (Not Loading All in Memory)

**Bad (Loads All in Memory):**
```javascript
const users = await db.users.findMany(); // 1 million users!
for (const user of users) {
  await processUser(user);
}
// Memory: 1GB+
```

**Good (Streams):**
```javascript
const { Readable } = require('stream');

const userStream = Readable.from(db.users.findManyStream());

userStream.on('data', async (user) => {
  await processUser(user);
});

userStream.on('end', () => {
  console.log('Done processing users');
});
// Memory: ~10MB
```

### 2. Backpressure Handling

**Problem:**
```javascript
// Producer faster than consumer
for (let i = 0; i < 1000000; i++) {
  stream.write(data); // Fills memory!
}
```

**Solution:**
```javascript
for (let i = 0; i < 1000000; i++) {
  const canContinue = stream.write(data);
  
  if (!canContinue) {
    // Wait for drain event
    await new Promise(resolve => stream.once('drain', resolve));
  }
}
```

### 3. Node.js Streams

**Example: Process Large CSV**
```javascript
const fs = require('fs');
const csv = require('csv-parser');

fs.createReadStream('large-file.csv')
  .pipe(csv())
  .on('data', (row) => {
    // Process each row
    processRow(row);
  })
  .on('end', () => {
    console.log('CSV processed');
  });
```

### 4. Python Generators/Iterators

**Example: Process Large File**
```python
def read_large_file(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            yield line.strip()

# Process line by line (low memory)
for line in read_large_file('large-file.txt'):
    process_line(line)
```

---

## Load Balancing

### 1. Round-Robin

**How it Works:**
- Distribute requests evenly across servers
- Server 1 → Server 2 → Server 3 → Server 1 → ...

**Pros:**
- Simple
- Even distribution

**Cons:**
- Doesn't consider server load

### 2. Least Connections

**How it Works:**
- Send request to server with fewest active connections

**Pros:**
- Better for long-running requests
- Adapts to server load

**Cons:**
- More complex

### 3. Consistent Hashing

**How it Works:**
- Hash request (e.g., user ID) to determine server
- Same user always goes to same server

**Pros:**
- Sticky sessions (useful for caching)
- Minimal redistribution when adding/removing servers

**Cons:**
- Uneven distribution possible

**Implementation:**
```javascript
const HashRing = require('hashring');

const ring = new HashRing([
  'server1:3000',
  'server2:3000',
  'server3:3000'
]);

// Get server for user
const server = ring.get(`user:${userId}`);
console.log(`Route user ${userId} to ${server}`);
```

### 4. Sticky Sessions (When Needed)

**Use Case:** Session data stored in server memory

**Implementation (Nginx):**
```nginx
upstream backend {
  ip_hash;  # Sticky sessions based on IP
  server server1:3000;
  server server2:3000;
  server server3:3000;
}
```

---

## Horizontal Scaling

### 1. Stateless Services (Can Add More Instances)

**Stateless (Good):**
```javascript
// No shared state
app.get('/api/users/:id', async (req, res) => {
  const user = await db.users.findUnique({ where: { id: req.params.id } });
  res.json(user);
});

// Can scale to 100 instances
```

**Stateful (Bad):**
```javascript
// Shared state in memory
const cache = new Map();

app.get('/api/users/:id', async (req, res) => {
  if (cache.has(req.params.id)) {
    return res.json(cache.get(req.params.id));
  }
  
  const user = await db.users.findUnique({ where: { id: req.params.id } });
  cache.set(req.params.id, user);
  res.json(user);
});

// Can't scale (cache not shared across instances)
```

**Solution: Use Redis for Shared State**
```javascript
app.get('/api/users/:id', async (req, res) => {
  const cached = await redis.get(`user:${req.params.id}`);
  if (cached) return res.json(JSON.parse(cached));
  
  const user = await db.users.findUnique({ where: { id: req.params.id } });
  await redis.setex(`user:${req.params.id}`, 3600, JSON.stringify(user));
  res.json(user);
});

// Can scale (Redis shared across instances)
```

### 2. Distributed Task Queues

**See "Task Queue Systems" section above**

### 3. Shared Nothing Architecture

**Principles:**
- No shared state between instances
- Each instance independent
- Communicate via message queues or APIs

**Benefits:**
- Easy to scale horizontally
- No single point of failure
- Better fault tolerance

---

## Measuring Concurrency

### 1. Concurrent Requests (Active at One Time)

**Metric:** Number of requests being processed simultaneously

**Monitoring:**
```javascript
let activeRequests = 0;

app.use((req, res, next) => {
  activeRequests++;
  
  res.on('finish', () => {
    activeRequests--;
  });
  
  next();
});

// Expose metric
app.get('/metrics', (req, res) => {
  res.json({ activeRequests });
});
```

### 2. Queue Depth

**Metric:** Number of jobs waiting in queue

**Monitoring (Bull):**
```javascript
const waiting = await queue.getWaitingCount();
const active = await queue.getActiveCount();
const failed = await queue.getFailedCount();

console.log(`Queue depth: ${waiting}, Active: ${active}, Failed: ${failed}`);
```

### 3. Worker Utilization

**Metric:** Percentage of time workers are busy

**Formula:**
```
Utilization = (Active Workers / Total Workers) × 100%
```

**Goal:** 70-80% (not 100%, leave headroom for spikes)

### 4. P95/P99 Latency Under Load

**Metric:** 95th/99th percentile latency

**Monitoring:**
```javascript
const latencies = [];

app.use((req, res, next) => {
  const start = Date.now();
  
  res.on('finish', () => {
    latencies.push(Date.now() - start);
  });
  
  next();
});

// Calculate P95
function getP95() {
  const sorted = latencies.sort((a, b) => a - b);
  const index = Math.floor(sorted.length * 0.95);
  return sorted[index];
}
```

---

## Benchmarking Tools

### 1. Apache Bench (ab)

```bash
# 1000 requests, 10 concurrent
ab -n 1000 -c 10 http://localhost:3000/api/users
```

### 2. wrk

```bash
# 10 threads, 100 connections, 30 seconds
wrk -t10 -c100 -d30s http://localhost:3000/api/users
```

### 3. wrk2

```bash
# Constant throughput: 1000 req/s
wrk2 -t10 -c100 -d30s -R1000 http://localhost:3000/api/users
```

### 4. k6

```javascript
// script.js
import http from 'k6/http';

export let options = {
  vus: 100,        // 100 virtual users
  duration: '30s'
};

export default function() {
  http.get('http://localhost:3000/api/users');
}
```

```bash
k6 run script.js
```

### 5. autocannon (Node.js)

```bash
# 50 connections, 60 seconds
autocannon -c 50 -d 60 http://localhost:3000/api/users
```

---

## Concurrency Anti-Patterns

### 1. Blocking the Event Loop (Node.js)

**Bad:**
```javascript
app.get('/api/compute', (req, res) => {
  // Blocks event loop for 5 seconds!
  let result = 0;
  for (let i = 0; i < 5000000000; i++) {
    result += i;
  }
  res.json({ result });
});
```

**Good:**
```javascript
app.get('/api/compute', async (req, res) => {
  // Offload to worker thread
  const result = await runWorker({ iterations: 5000000000 });
  res.json({ result });
});
```

### 2. Unbounded Concurrency (Resource Exhaustion)

**Bad:**
```javascript
// No limit on concurrent requests
const results = await Promise.all(
  urls.map(url => fetch(url))
);
// 10,000 URLs = 10,000 concurrent requests!
```

**Good:**
```javascript
// Limit to 10 concurrent requests
const pool = new WorkerPool(10);
const results = await Promise.all(
  urls.map(url => pool.execute(() => fetch(url)))
);
```

### 3. Race Conditions

**Bad:**
```javascript
let counter = 0;

async function increment() {
  const current = counter;
  await delay(10);
  counter = current + 1;
}

// Race condition!
await Promise.all([increment(), increment()]);
console.log(counter); // Expected: 2, Actual: 1
```

**Good:**
```javascript
// Use atomic operations (Redis INCR)
await redis.incr('counter');
await redis.incr('counter');
const counter = await redis.get('counter');
console.log(counter); // 2 (correct)
```

### 4. Deadlocks

**Bad:**
```javascript
// Lock A then Lock B
async function task1() {
  await lockA.acquire();
  await lockB.acquire();
  // Work
  lockB.release();
  lockA.release();
}

// Lock B then Lock A (deadlock!)
async function task2() {
  await lockB.acquire();
  await lockA.acquire();
  // Work
  lockA.release();
  lockB.release();
}
```

**Good:**
```javascript
// Always acquire locks in same order
async function task1() {
  await lockA.acquire();
  await lockB.acquire();
  // Work
  lockB.release();
  lockA.release();
}

async function task2() {
  await lockA.acquire(); // Same order!
  await lockB.acquire();
  // Work
  lockB.release();
  lockA.release();
}
```

---

## Real-World Scenarios

### Scenario 1: High-Throughput API

**Requirements:**
- Handle 10,000 req/s
- P95 latency < 100ms

**Solution:**
```javascript
// 1. Cluster mode (use all CPU cores)
const cluster = require('cluster');
const numCPUs = require('os').cpus().length;

if (cluster.isMaster) {
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }
} else {
  // 2. Connection pooling
  const prisma = new PrismaClient({
    datasources: {
      db: { url: 'postgresql://...?connection_limit=20' }
    }
  });
  
  // 3. Caching
  const redis = new Redis();
  
  app.get('/api/users/:id', async (req, res) => {
    // Check cache
    const cached = await redis.get(`user:${req.params.id}`);
    if (cached) return res.json(JSON.parse(cached));
    
    // Query database
    const user = await prisma.user.findUnique({ where: { id: req.params.id } });
    
    // Cache result
    await redis.setex(`user:${req.params.id}`, 3600, JSON.stringify(user));
    
    res.json(user);
  });
  
  app.listen(3000);
}
```

### Scenario 2: Batch Job Processing

**Requirements:**
- Process 1 million records
- Complete within 1 hour

**Solution:**
```javascript
const { Queue, Worker } = require('bullmq');

// Producer: Add jobs to queue
const queue = new Queue('process-records');

const records = await db.records.findMany({ take: 1000000 });

for (const record of records) {
  await queue.add('process', { recordId: record.id });
}

// Consumer: Process jobs in parallel
const worker = new Worker('process-records', async (job) => {
  const record = await db.records.findUnique({ where: { id: job.data.recordId } });
  await processRecord(record);
}, {
  concurrency: 100  // 100 concurrent workers
});

// 1,000,000 records / 100 workers / 3600s = ~3 records/s per worker
```

### Scenario 3: WebSocket Connections

**Requirements:**
- Support 100,000 concurrent WebSocket connections

**Solution:**
```javascript
const cluster = require('cluster');
const numCPUs = require('os').cpus().length;
const Redis = require('ioredis');
const { Server } = require('socket.io');
const { createAdapter } = require('@socket.io/redis-adapter');

if (cluster.isMaster) {
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }
} else {
  const io = new Server(3000);
  
  // Redis adapter for multi-instance support
  const pubClient = new Redis();
  const subClient = pubClient.duplicate();
  io.adapter(createAdapter(pubClient, subClient));
  
  io.on('connection', (socket) => {
    console.log(`Client connected: ${socket.id}`);
    
    socket.on('message', (data) => {
      // Broadcast to all clients (across all instances)
      io.emit('message', data);
    });
  });
}

// 100,000 connections / 8 cores = 12,500 per instance
```

### Scenario 4: File Processing Pipeline

**Requirements:**
- Process uploaded files asynchronously
- Support multiple file types (images, videos, PDFs)

**Solution:**
```javascript
const { Queue, Worker } = require('bullmq');

// Upload endpoint
app.post('/api/upload', upload.single('file'), async (req, res) => {
  const fileId = await saveFile(req.file);
  
  // Add to queue based on file type
  const queueName = getQueueForFileType(req.file.mimetype);
  await queues[queueName].add('process', { fileId });
  
  res.json({ fileId, status: 'processing' });
});

// Separate workers for each file type
const imageWorker = new Worker('images', processImage, { concurrency: 10 });
const videoWorker = new Worker('videos', processVideo, { concurrency: 5 });
const pdfWorker = new Worker('pdfs', processPDF, { concurrency: 20 });
```

---

## Implementation Examples

### Worker Pool in Node.js

```javascript
class WorkerPool {
  constructor(maxWorkers = 10) {
    this.maxWorkers = maxWorkers;
    this.activeWorkers = 0;
    this.queue = [];
  }
  
  async execute(task) {
    while (this.activeWorkers >= this.maxWorkers) {
      await new Promise(resolve => this.queue.push(resolve));
    }
    
    this.activeWorkers++;
    
    try {
      return await task();
    } finally {
      this.activeWorkers--;
      const next = this.queue.shift();
      if (next) next();
    }
  }
}

module.exports = WorkerPool;
```

### Celery Task Queue in Python

```python
# celery_app.py
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def process_data(data_id):
    # Process data
    data = fetch_data(data_id)
    result = expensive_computation(data)
    save_result(result)
    return result

# producer.py
from celery_app import process_data

# Add job to queue
result = process_data.delay(123)
print(f'Job queued: {result.id}')

# worker.sh
celery -A celery_app worker --loglevel=info --concurrency=10
```

### Connection Pooling Configuration

**PostgreSQL (Prisma):**
```javascript
const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient({
  datasources: {
    db: {
      url: 'postgresql://user:pass@localhost:5432/db?connection_limit=20&pool_timeout=20'
    }
  }
});
```

**Redis (ioredis):**
```javascript
const Redis = require('ioredis');

const redis = new Redis({
  host: 'localhost',
  port: 6379,
  maxRetriesPerRequest: 3,
  enableReadyCheck: true,
  lazyConnect: true
});
```

---

## Summary

### Quick Reference

**Concurrency vs Parallelism:**
- Concurrency: Structure (dealing with many things)
- Parallelism: Execution (doing many things)

**Node.js:**
- Event loop (single-threaded)
- Worker threads (CPU-intensive)
- Cluster mode (multi-process)

**Python:**
- asyncio (I/O-bound)
- Threading (I/O-bound, GIL limited)
- Multiprocessing (CPU-bound)

**Patterns:**
- Worker pools (limit concurrency)
- Task queues (async processing)
- Rate limiting (control rate)
- Backpressure (slow down when overwhelmed)

**Worker Pool Sizing:**
- I/O-bound: More workers than cores
- CPU-bound: Workers = cores
- Mixed: Separate pools

**Tools:**
- Bull/BullMQ (Node.js task queue)
- Celery (Python task queue)
- ab, wrk, k6 (benchmarking)

**Anti-Patterns:**
- Blocking event loop
- Unbounded concurrency
- Race conditions
- Deadlocks

**Key Metrics:**
- Concurrent requests
- Queue depth
- Worker utilization (70-80%)
- P95/P99 latency
