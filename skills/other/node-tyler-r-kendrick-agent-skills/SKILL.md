---
name: node
description: |
  Use when building applications with Node.js, the most widely deployed JavaScript/TypeScript runtime. Covers the event loop, module system (CommonJS and ESM), core modules (fs, path, http, crypto, streams, worker_threads, child_process), async patterns, diagnostics, error handling, security, native addons, and TypeScript integration.
  USE FOR: Node.js server-side development, HTTP servers and APIs, file system operations, streams and data processing, worker threads and parallelism, child process management, Node.js module system (CJS/ESM), event loop and async patterns, Node.js diagnostics and profiling, native addon development, Node.js TypeScript configuration, package.json exports field, Node.js 18/20/22+ features
  DO NOT USE FOR: Deno-specific features or Deno Deploy (use deno), Bun-specific APIs, frontend-only browser code, Express/Fastify/NestJS framework details (use the respective package skills), package manager comparison (use package-management)
license: MIT
metadata:
  displayName: "Node.js"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "Node.js Documentation"
    url: "https://nodejs.org"
  - title: "Node.js GitHub Repository"
    url: "https://github.com/nodejs/node"
  - title: "Node.js API Documentation"
    url: "https://nodejs.org/docs/latest/api/"
---

# Node.js

## Overview

Node.js is the original and most widely deployed server-side JavaScript runtime. Built on the V8 engine, it uses an event-driven, non-blocking I/O model that makes it well suited for data-intensive real-time applications. Node.js has the largest ecosystem of any runtime via npm, with millions of packages, and is supported by virtually every cloud provider, CI/CD platform, and hosting service.

Node.js runs JavaScript natively and supports TypeScript through transpilation tools (`tsx`, `ts-node`, `swc`, `esbuild`) or, starting with Node 22+, experimental built-in type stripping via `--experimental-strip-types`.

## Node.js Version Landscape

| Version | Status | Key Features |
|---------|--------|-------------|
| **18 LTS** | Maintenance LTS (EOL April 2025) | Global `fetch`, Web Streams API, `node --test` runner, `--watch` mode, `node:` prefix for builtins, `Blob` and `BroadcastChannel` globals, V8 10.2 |
| **20 LTS** | Active LTS | Stable `node --test` runner, stable permission model (`--experimental-permission`), `--env-file` flag, stable `import.meta.resolve`, single executable apps (SEA), V8 11.3, `URL.canParse()`, stable `globalThis.navigator` |
| **22 LTS** | Active LTS | `--experimental-strip-types` (TypeScript support), `require()` for ESM modules (`--experimental-require-module`), WebSocket client (`WebSocket` global), stable `glob` and `matchesGlob` on `fs`, V8 12.4, `node --run` for package.json scripts, Maglev compiler |
| **23+** | Current | `--experimental-transform-types` (enum/namespace support), unflagged `require()` of ESM (23.0+), stable `--experimental-strip-types` progression, V8 updates |

### Choosing a Version

- **For production:** Use the latest Active LTS release (currently Node 22 LTS or Node 20 LTS).
- **Even-numbered releases** become LTS and receive 30 months of support.
- **Odd-numbered releases** are Current (latest features) with a shorter support window.
- Use `nvm`, `fnm`, `volta`, or `mise` to manage multiple Node.js versions per project.

## Module System

Node.js supports two module systems: CommonJS (CJS) and ECMAScript Modules (ESM). Understanding when and how to use each is critical for modern Node.js development.

### CommonJS (CJS)

```javascript
// Exporting
module.exports = { greet };
module.exports.greet = function greet(name) {
  return `Hello, ${name}!`;
};
exports.greet = greet; // shorthand (do NOT reassign exports itself)

// Importing
const { greet } = require("./utils");
const fs = require("node:fs");
const lodash = require("lodash");
```

**Characteristics:**
- Synchronous `require()` -- modules are loaded and executed immediately.
- `module.exports` is the single exported value.
- `__dirname` and `__filename` are available.
- Circular dependencies are handled by returning partial exports.
- Default in files with `.cjs` extension or when `package.json` has no `"type"` field or `"type": "commonjs"`.

### ECMAScript Modules (ESM)

```typescript
// Exporting
export function greet(name: string): string {
  return `Hello, ${name}!`;
}
export default class UserService { /* ... */ }

// Importing
import { greet } from "./utils.js"; // note: .js extension required
import UserService from "./user-service.js";
import { readFile } from "node:fs/promises";
import lodash from "lodash";

// Dynamic import (works in both CJS and ESM)
const { default: chalk } = await import("chalk");

// Import metadata
console.log(import.meta.url);      // file:///path/to/module.js
console.log(import.meta.dirname);   // /path/to (Node 21+)
console.log(import.meta.filename);  // /path/to/module.js (Node 21+)
const resolved = import.meta.resolve("./other.js"); // resolved URL
```

**Characteristics:**
- Asynchronous module loading and evaluation.
- Static `import`/`export` syntax enables tree shaking.
- File extensions are mandatory in relative imports (`.js`, `.mjs`, `.ts` with loaders).
- No `__dirname` or `__filename` -- use `import.meta.dirname` (Node 21+) or `import.meta.url` with `fileURLToPath`.
- Default in files with `.mjs` extension or when `package.json` has `"type": "module"`.
- Top-level `await` is supported.

### package.json `type` Field

```jsonc
{
  "type": "module"  // Treat .js files as ESM
  // or
  "type": "commonjs" // Treat .js files as CJS (default if omitted)
}
```

| File Extension | `"type": "module"` | `"type": "commonjs"` (or omitted) |
|----------------|--------------------|------------------------------------|
| `.js` | ESM | CJS |
| `.mjs` | ESM | ESM |
| `.cjs` | CJS | CJS |
| `.ts` (with loader) | ESM | CJS |
| `.mts` (with loader) | ESM | ESM |
| `.cts` (with loader) | CJS | CJS |

### Conditional Exports (package.json `exports` Field)

The `exports` field in `package.json` defines the public API of a package and supports conditional resolution for different environments.

```jsonc
{
  "name": "my-library",
  "type": "module",
  "exports": {
    // Main entry point
    ".": {
      "types": "./dist/index.d.ts",       // TypeScript types (must be first)
      "import": "./dist/index.mjs",        // ESM entry
      "require": "./dist/index.cjs",       // CJS entry
      "default": "./dist/index.mjs"        // Fallback
    },
    // Subpath export
    "./utils": {
      "types": "./dist/utils.d.ts",
      "import": "./dist/utils.mjs",
      "require": "./dist/utils.cjs"
    },
    // Subpath pattern (wildcard)
    "./components/*": {
      "types": "./dist/components/*.d.ts",
      "import": "./dist/components/*.mjs",
      "require": "./dist/components/*.cjs"
    },
    // Restrict access -- block deep imports
    "./internal/*": null,
    // package.json self-reference
    "./package.json": "./package.json"
  },
  // Fallback for older Node.js (pre-exports support)
  "main": "./dist/index.cjs",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.ts"
}
```

**Condition ordering matters.** Node.js uses the first matching condition. Always place `"types"` first (for TypeScript), then `"import"`, then `"require"`, then `"default"`.

Additional conditions:

| Condition | Description |
|-----------|-------------|
| `"node"` | Node.js environment |
| `"browser"` | Browser bundlers (webpack, Vite) |
| `"development"` | Development mode |
| `"production"` | Production mode |
| `"node-addons"` | Native addon support required |
| `"edge-light"` | Edge runtime (Vercel Edge, Cloudflare) |

### Interoperability Between CJS and ESM

```typescript
// ESM can import CJS modules directly
import cjsModule from "./legacy-module.cjs";

// CJS can import ESM modules via dynamic import
const esmModule = await import("./modern-module.mjs");

// Node 22+ with --experimental-require-module: CJS can require() ESM
// Node 23+: require() of ESM is unflagged for synchronous ESM graphs
const esmModule = require("./modern-module.mjs");
```

## Event Loop and Async Patterns

### Event Loop Phases

The Node.js event loop processes callbacks in a specific order across multiple phases:

```
   ┌───────────────────────────┐
┌─>│         timers            │  setTimeout, setInterval callbacks
│  └──────────┬────────────────┘
│  ┌──────────┴────────────────┐
│  │     pending callbacks     │  I/O callbacks deferred from previous cycle
│  └──────────┬────────────────┘
│  ┌──────────┴────────────────┐
│  │       idle, prepare       │  Internal use only
│  └──────────┬────────────────┘
│  ┌──────────┴────────────────┐
│  │         poll              │  Retrieve new I/O events; execute I/O callbacks
│  └──────────┬────────────────┘
│  ┌──────────┴────────────────┐
│  │         check             │  setImmediate callbacks
│  └──────────┬────────────────┘
│  ┌──────────┴────────────────┐
│  │    close callbacks        │  socket.on('close', ...) etc.
│  └──────────┘────────────────┘
```

### Microtasks vs Macrotasks

```typescript
// Microtasks execute between every event loop phase transition
// and after every macrotask
console.log("1: synchronous");

// Macrotask (timer phase)
setTimeout(() => console.log("5: setTimeout"), 0);

// Macrotask (check phase)
setImmediate(() => console.log("6: setImmediate"));

// Microtask (next tick queue -- highest priority microtask)
process.nextTick(() => console.log("3: nextTick"));

// Microtask (promise queue -- after nextTick)
Promise.resolve().then(() => console.log("4: Promise.then"));

console.log("2: synchronous");

// Output: 1, 2, 3, 4, 5, 6 (5 and 6 order may vary at top level)
```

**Execution priority:**
1. Synchronous code
2. `process.nextTick()` callbacks (microtask queue)
3. Promise callbacks (microtask queue)
4. Timer callbacks (`setTimeout`, `setInterval`)
5. I/O callbacks
6. `setImmediate()` callbacks
7. Close callbacks

### Async/Await Patterns

```typescript
import { readFile, writeFile } from "node:fs/promises";
import { setTimeout as delay } from "node:timers/promises";

// Sequential execution
async function processFiles(paths: string[]): Promise<string[]> {
  const results: string[] = [];
  for (const path of paths) {
    const content = await readFile(path, "utf-8");
    results.push(content.toUpperCase());
  }
  return results;
}

// Parallel execution
async function processFilesParallel(paths: string[]): Promise<string[]> {
  const promises = paths.map((path) => readFile(path, "utf-8"));
  const contents = await Promise.all(promises);
  return contents.map((c) => c.toUpperCase());
}

// Controlled concurrency
async function processWithLimit(
  items: string[],
  concurrency: number,
  fn: (item: string) => Promise<void>
): Promise<void> {
  const executing = new Set<Promise<void>>();
  for (const item of items) {
    const p = fn(item).then(() => executing.delete(p));
    executing.add(p);
    if (executing.size >= concurrency) {
      await Promise.race(executing);
    }
  }
  await Promise.all(executing);
}

// Promise.allSettled -- wait for all, even if some fail
const results = await Promise.allSettled([
  fetch("https://api1.example.com"),
  fetch("https://api2.example.com"),
  fetch("https://api3.example.com"),
]);
for (const result of results) {
  if (result.status === "fulfilled") {
    console.log("Success:", result.value.status);
  } else {
    console.error("Failed:", result.reason);
  }
}

// Timeout with AbortController
async function fetchWithTimeout(
  url: string,
  timeoutMs: number
): Promise<Response> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(url, { signal: controller.signal });
    return response;
  } finally {
    clearTimeout(timeout);
  }
}

// AbortSignal.timeout (Node 18+)
const response = await fetch("https://api.example.com/data", {
  signal: AbortSignal.timeout(5000), // 5 second timeout
});

// Timers/promises
await delay(1000); // sleep for 1 second
```

## Core Modules

### File System (`node:fs/promises`)

```typescript
import {
  readFile, writeFile, appendFile,
  mkdir, rm, readdir, rename, copyFile, stat, access,
  watch, glob,
} from "node:fs/promises";
import { constants } from "node:fs";
import { join } from "node:path";

// Read file
const content = await readFile("./config.json", "utf-8");
const config = JSON.parse(content);

// Write file
await writeFile("./output.txt", "Hello, World!", "utf-8");

// Append to file
await appendFile("./log.txt", `${new Date().toISOString()} - Entry\n`);

// Create directory recursively
await mkdir("./output/reports/2024", { recursive: true });

// Remove directory recursively
await rm("./temp", { recursive: true, force: true });

// List directory contents
const entries = await readdir("./src", { withFileTypes: true });
for (const entry of entries) {
  if (entry.isDirectory()) {
    console.log(`DIR:  ${entry.name}`);
  } else if (entry.isFile()) {
    console.log(`FILE: ${entry.name}`);
  }
}

// Recursive directory listing (Node 18.17+)
const allFiles = await readdir("./src", { recursive: true });

// Copy file
await copyFile("./source.txt", "./destination.txt");

// Rename / move
await rename("./old-name.txt", "./new-name.txt");

// File stats
const info = await stat("./file.txt");
console.log(info.size);        // bytes
console.log(info.mtime);       // modification time
console.log(info.isFile());    // true
console.log(info.isDirectory()); // false

// Check file access
try {
  await access("./file.txt", constants.R_OK | constants.W_OK);
  console.log("File is readable and writable");
} catch {
  console.log("File is not accessible");
}

// Watch for file changes (Node 18+, recursive on macOS/Windows)
const watcher = watch("./src", { recursive: true });
for await (const event of watcher) {
  console.log(`${event.eventType}: ${event.filename}`);
}

// Glob (Node 22+)
for await (const entry of glob("**/*.ts")) {
  console.log(entry);
}
```

### Path (`node:path`)

```typescript
import path from "node:path";

path.join("/users", "alice", "documents", "file.txt");
// => "/users/alice/documents/file.txt"

path.resolve("./src", "../dist", "index.js");
// => "/absolute/path/to/dist/index.js"

path.basename("/users/alice/photo.png");      // "photo.png"
path.basename("/users/alice/photo.png", ".png"); // "photo"
path.extname("file.tar.gz");                  // ".gz"
path.dirname("/users/alice/photo.png");        // "/users/alice"

path.parse("/users/alice/photo.png");
// { root: "/", dir: "/users/alice", base: "photo.png", ext: ".png", name: "photo" }

path.format({ dir: "/users/alice", name: "photo", ext: ".png" });
// => "/users/alice/photo.png"

path.isAbsolute("/usr/local"); // true
path.isAbsolute("./src");     // false

path.relative("/users/alice", "/users/bob/docs");
// => "../bob/docs"

path.normalize("/users/alice/../bob/./docs");
// => "/users/bob/docs"

// Platform-specific separator
path.sep;     // "/" on POSIX, "\\" on Windows
path.delimiter; // ":" on POSIX, ";" on Windows
```

### HTTP Server

```typescript
import { createServer, IncomingMessage, ServerResponse } from "node:http";
import { createServer as createHttpsServer } from "node:https";
import { readFileSync } from "node:fs";

// Basic HTTP server
const server = createServer(
  (req: IncomingMessage, res: ServerResponse) => {
    const url = new URL(req.url!, `http://${req.headers.host}`);

    if (req.method === "GET" && url.pathname === "/") {
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ message: "Hello, World!" }));
      return;
    }

    if (req.method === "POST" && url.pathname === "/api/data") {
      let body = "";
      req.on("data", (chunk) => (body += chunk));
      req.on("end", () => {
        const data = JSON.parse(body);
        res.writeHead(201, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ received: data }));
      });
      return;
    }

    res.writeHead(404);
    res.end("Not Found");
  }
);

server.listen(3000, () => {
  console.log("Server running on http://localhost:3000");
});

// Graceful shutdown
process.on("SIGTERM", () => {
  server.close(() => {
    console.log("Server closed");
    process.exit(0);
  });
});
```

```typescript
// HTTP/2 server
import http2 from "node:http2";
import { readFileSync } from "node:fs";

const h2server = http2.createSecureServer({
  key: readFileSync("./server.key"),
  cert: readFileSync("./server.crt"),
});

h2server.on("stream", (stream, headers) => {
  stream.respond({
    ":status": 200,
    "content-type": "application/json",
  });
  stream.end(JSON.stringify({ protocol: "h2" }));
});

h2server.listen(8443);
```

### Crypto (`node:crypto`)

```typescript
import {
  randomBytes, randomUUID, createHash, createHmac,
  scrypt, timingSafeEqual,
  createCipheriv, createDecipheriv,
  generateKeyPairSync, publicEncrypt, privateDecrypt,
} from "node:crypto";

// Random values
const uuid = randomUUID();                          // "550e8400-e29b-..."
const token = randomBytes(32).toString("hex");      // 64-char hex string
const urlSafeToken = randomBytes(32).toString("base64url");

// Hashing
const hash = createHash("sha256")
  .update("Hello, World!")
  .digest("hex");

// Streaming hash (for large files)
import { createReadStream } from "node:fs";
const fileHash = createHash("sha256");
const stream = createReadStream("./large-file.bin");
stream.pipe(fileHash);
stream.on("end", () => {
  console.log("SHA-256:", fileHash.digest("hex"));
});

// HMAC
const hmac = createHmac("sha256", "secret-key")
  .update("message")
  .digest("hex");

// Password hashing with scrypt
import { promisify } from "node:util";
const scryptAsync = promisify(scrypt);

async function hashPassword(password: string): Promise<string> {
  const salt = randomBytes(16).toString("hex");
  const derivedKey = (await scryptAsync(password, salt, 64)) as Buffer;
  return `${salt}:${derivedKey.toString("hex")}`;
}

async function verifyPassword(
  password: string,
  stored: string
): Promise<boolean> {
  const [salt, hash] = stored.split(":");
  const derivedKey = (await scryptAsync(password, salt, 64)) as Buffer;
  const hashBuffer = Buffer.from(hash, "hex");
  return timingSafeEqual(derivedKey, hashBuffer);
}

// AES-256-GCM encryption
function encrypt(text: string, key: Buffer): { iv: string; encrypted: string; tag: string } {
  const iv = randomBytes(16);
  const cipher = createCipheriv("aes-256-gcm", key, iv);
  let encrypted = cipher.update(text, "utf-8", "hex");
  encrypted += cipher.final("hex");
  const tag = cipher.getAuthTag().toString("hex");
  return { iv: iv.toString("hex"), encrypted, tag };
}

function decrypt(data: { iv: string; encrypted: string; tag: string }, key: Buffer): string {
  const decipher = createDecipheriv(
    "aes-256-gcm",
    key,
    Buffer.from(data.iv, "hex")
  );
  decipher.setAuthTag(Buffer.from(data.tag, "hex"));
  let decrypted = decipher.update(data.encrypted, "hex", "utf-8");
  decrypted += decipher.final("utf-8");
  return decrypted;
}

// RSA key pair generation
const { publicKey, privateKey } = generateKeyPairSync("rsa", {
  modulusLength: 2048,
  publicKeyEncoding: { type: "spki", format: "pem" },
  privateKeyEncoding: { type: "pkcs8", format: "pem" },
});
```

### Streams API

Node.js streams are the foundational abstraction for handling flowing data efficiently without buffering entire payloads in memory.

```typescript
import { Readable, Writable, Transform, Duplex, pipeline } from "node:stream";
import { pipeline as pipelineAsync } from "node:stream/promises";
import { createReadStream, createWriteStream } from "node:fs";
import { createGzip, createGunzip } from "node:zlib";

// Readable stream
const readable = new Readable({
  read() {
    this.push("Hello ");
    this.push("World");
    this.push(null); // signals end of stream
  },
});

// Writable stream
const writable = new Writable({
  write(chunk, encoding, callback) {
    console.log("Received:", chunk.toString());
    callback();
  },
});

// Transform stream (read + transform + write)
const uppercase = new Transform({
  transform(chunk, encoding, callback) {
    callback(null, chunk.toString().toUpperCase());
  },
});

// Pipeline (recommended way to compose streams)
await pipelineAsync(
  createReadStream("./input.txt"),
  createGzip(),
  createWriteStream("./output.txt.gz")
);

// Pipeline with error handling (callback style)
pipeline(
  createReadStream("./input.txt"),
  uppercase,
  createWriteStream("./output.txt"),
  (err) => {
    if (err) console.error("Pipeline failed:", err);
    else console.log("Pipeline succeeded");
  }
);

// Async iteration over readable streams
const fileStream = createReadStream("./data.txt", "utf-8");
for await (const chunk of fileStream) {
  process.stdout.write(chunk);
}

// Object mode streams
const objectReadable = new Readable({
  objectMode: true,
  read() {
    this.push({ id: 1, name: "Alice" });
    this.push({ id: 2, name: "Bob" });
    this.push(null);
  },
});

const filter = new Transform({
  objectMode: true,
  transform(user, encoding, callback) {
    if (user.id > 1) {
      callback(null, user);
    } else {
      callback(); // skip this object
    }
  },
});

// Duplex stream (independent read and write sides)
const duplex = new Duplex({
  read(size) {
    this.push("data from read side");
    this.push(null);
  },
  write(chunk, encoding, callback) {
    console.log("Write side received:", chunk.toString());
    callback();
  },
});

// Web Streams interop (Node 18+)
import { Readable as WebReadable } from "node:stream/web";

const nodeStream = createReadStream("./file.txt");
const webStream = Readable.toWeb(nodeStream);
// Convert back: Readable.fromWeb(webStream)
```

### Worker Threads

Worker threads enable true parallel computation by running JavaScript in separate V8 isolates with their own event loops, while sharing memory via `SharedArrayBuffer`.

```typescript
// main.ts
import {
  Worker, isMainThread, parentPort, workerData, MessageChannel
} from "node:worker_threads";
import { cpus } from "node:os";

if (isMainThread) {
  // Main thread -- spawn workers
  const numCPUs = cpus().length;

  function runWorker(data: unknown): Promise<unknown> {
    return new Promise((resolve, reject) => {
      const worker = new Worker(new URL(import.meta.url), {
        workerData: data,
      });
      worker.on("message", resolve);
      worker.on("error", reject);
      worker.on("exit", (code) => {
        if (code !== 0)
          reject(new Error(`Worker exited with code ${code}`));
      });
    });
  }

  // Run computation across all CPUs
  const tasks = Array.from({ length: numCPUs }, (_, i) => ({
    start: i * 1_000_000,
    end: (i + 1) * 1_000_000,
  }));
  const results = await Promise.all(tasks.map(runWorker));
  console.log("Results:", results);
} else {
  // Worker thread
  const { start, end } = workerData as { start: number; end: number };
  let sum = 0;
  for (let i = start; i < end; i++) {
    sum += i;
  }
  parentPort!.postMessage(sum);
}
```

```typescript
// SharedArrayBuffer for shared memory
import { Worker, isMainThread } from "node:worker_threads";

if (isMainThread) {
  const shared = new SharedArrayBuffer(4);
  const array = new Int32Array(shared);
  array[0] = 0;

  const worker = new Worker(new URL(import.meta.url), {
    workerData: shared,
  });

  worker.on("exit", () => {
    console.log("Final value:", array[0]); // Modified by worker
  });
} else {
  const { workerData } = await import("node:worker_threads");
  const array = new Int32Array(workerData);
  Atomics.add(array, 0, 42);
}
```

```typescript
// MessageChannel for direct worker-to-worker communication
import { Worker, MessageChannel } from "node:worker_threads";

const { port1, port2 } = new MessageChannel();

const workerA = new Worker("./worker-a.js");
const workerB = new Worker("./worker-b.js");

// Transfer ports to workers (zero-copy transfer)
workerA.postMessage({ port: port1 }, [port1]);
workerB.postMessage({ port: port2 }, [port2]);
```

### Child Processes

```typescript
import {
  spawn, exec, execFile, fork
} from "node:child_process";
import { execSync, spawnSync } from "node:child_process";
import { promisify } from "node:util";

const execAsync = promisify(exec);
const execFileAsync = promisify(execFile);

// spawn -- streaming I/O, best for long-running processes
const child = spawn("ls", ["-la", "./src"], { cwd: process.cwd() });
child.stdout.on("data", (data) => console.log(`stdout: ${data}`));
child.stderr.on("data", (data) => console.error(`stderr: ${data}`));
child.on("close", (code) => console.log(`exit code: ${code}`));

// exec -- buffered output, runs in shell, good for short commands
const { stdout, stderr } = await execAsync("git log --oneline -5");
console.log(stdout);

// execFile -- like exec but without shell (safer, faster)
const { stdout: version } = await execFileAsync("node", ["--version"]);
console.log(version.trim());

// fork -- spawn a Node.js child process with IPC channel
const forked = fork("./worker.js");
forked.send({ type: "start", data: [1, 2, 3] });
forked.on("message", (msg) => {
  console.log("Received from child:", msg);
});

// Synchronous variants (block the event loop -- use sparingly)
const result = execSync("echo hello", { encoding: "utf-8" });
const spawnResult = spawnSync("node", ["--version"]);
console.log(spawnResult.stdout.toString().trim());

// spawn with shell and piping
const grep = spawn("grep", ["-r", "TODO", "./src"], {
  stdio: ["ignore", "pipe", "pipe"],
});

// AbortController with child processes
const controller = new AbortController();
const abortableChild = spawn("sleep", ["60"], { signal: controller.signal });
setTimeout(() => controller.abort(), 5000); // kill after 5 seconds
```

### Events (`node:events`)

```typescript
import { EventEmitter, on, once } from "node:events";

// Basic EventEmitter
class TaskQueue extends EventEmitter {
  private queue: string[] = [];

  add(task: string): void {
    this.queue.push(task);
    this.emit("added", task);
  }

  process(): void {
    while (this.queue.length > 0) {
      const task = this.queue.shift()!;
      this.emit("processing", task);
      // ... process task ...
      this.emit("completed", task);
    }
    this.emit("drained");
  }
}

const queue = new TaskQueue();
queue.on("added", (task) => console.log(`Task added: ${task}`));
queue.on("completed", (task) => console.log(`Task done: ${task}`));
queue.once("drained", () => console.log("All tasks complete"));

queue.add("build");
queue.add("test");
queue.process();

// Async iteration over events (Node 16+)
const eventStream = on(queue, "added");
for await (const [task] of eventStream) {
  console.log(`Received: ${task}`);
  if (task === "stop") break;
}

// Wait for a single event
const [task] = await once(queue, "added");

// Set max listeners (default is 10, warns on leak)
queue.setMaxListeners(20);

// Typed EventEmitter (TypeScript pattern)
interface AppEvents {
  start: [port: number];
  request: [method: string, url: string];
  error: [error: Error];
  close: [];
}

class TypedEmitter extends EventEmitter {
  emit<K extends keyof AppEvents>(event: K, ...args: AppEvents[K]): boolean {
    return super.emit(event, ...args);
  }
  on<K extends keyof AppEvents>(
    event: K,
    listener: (...args: AppEvents[K]) => void
  ): this {
    return super.on(event, listener);
  }
}
```

### URL and Net

```typescript
import { URL, URLSearchParams } from "node:url";

const url = new URL("https://example.com:8080/path?q=search#section");
console.log(url.hostname);     // "example.com"
console.log(url.port);         // "8080"
console.log(url.pathname);     // "/path"
console.log(url.searchParams.get("q")); // "search"
console.log(url.hash);         // "#section"

// Modify URL
url.searchParams.set("page", "2");
url.searchParams.append("sort", "name");
console.log(url.toString());

// fileURLToPath (ESM helper)
import { fileURLToPath } from "node:url";
const __filename = fileURLToPath(import.meta.url);
const __dirname = fileURLToPath(new URL(".", import.meta.url));
```

```typescript
// TCP server
import { createServer, Socket } from "node:net";

const tcpServer = createServer((socket: Socket) => {
  socket.write("Welcome!\n");
  socket.on("data", (data) => {
    socket.write(`Echo: ${data}`);
  });
  socket.on("end", () => console.log("Client disconnected"));
});
tcpServer.listen(9000);

// TCP client
import { connect } from "node:net";
const client = connect({ port: 9000, host: "localhost" }, () => {
  client.write("Hello, server!");
});
client.on("data", (data) => console.log(data.toString()));
```

### OS, Util, and Performance

```typescript
import os from "node:os";

os.cpus();           // CPU info array
os.cpus().length;    // Number of CPU cores
os.totalmem();       // Total memory in bytes
os.freemem();        // Free memory in bytes
os.platform();       // "linux", "darwin", "win32"
os.arch();           // "x64", "arm64"
os.hostname();       // Machine hostname
os.homedir();        // User home directory
os.tmpdir();         // Temp directory path
os.networkInterfaces(); // Network interface details
os.uptime();         // System uptime in seconds
os.type();           // "Linux", "Darwin", "Windows_NT"
```

```typescript
import { promisify, inspect, types, styleText } from "node:util";
import { gunzip } from "node:zlib";

// Promisify callback-based functions
const gunzipAsync = promisify(gunzip);

// Deep inspect objects
const obj = { nested: { deep: { value: 42 } } };
console.log(inspect(obj, { depth: null, colors: true }));

// Type checking utilities
types.isPromise(Promise.resolve()); // true
types.isDate(new Date());           // true
types.isRegExp(/test/);             // true
types.isAsyncFunction(async () => {}); // true

// styleText (Node 20.12+) -- terminal styling
console.log(styleText("red", "Error occurred"));
console.log(styleText("bold", "Important"));
```

```typescript
// Performance hooks
import {
  performance,
  PerformanceObserver,
} from "node:perf_hooks";

// Measure operation duration
performance.mark("start");
// ... expensive operation ...
performance.mark("end");
performance.measure("operation", "start", "end");

// Observe performance entries
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    console.log(`${entry.name}: ${entry.duration.toFixed(2)}ms`);
  }
});
observer.observe({ entryTypes: ["measure"] });

// Histogram for high-resolution timing
import { createHistogram } from "node:perf_hooks";
const histogram = createHistogram();
const start = performance.now();
// ... operation ...
histogram.record(Math.round((performance.now() - start) * 1e6)); // nanoseconds
console.log(`p50: ${histogram.percentile(50)}ns, p99: ${histogram.percentile(99)}ns`);
```

### Cluster

```typescript
import cluster from "node:cluster";
import { createServer } from "node:http";
import { cpus } from "node:os";

const numCPUs = cpus().length;

if (cluster.isPrimary) {
  console.log(`Primary ${process.pid} is running`);

  // Fork workers
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }

  cluster.on("exit", (worker, code, signal) => {
    console.log(`Worker ${worker.process.pid} died (${signal || code})`);
    // Restart worker
    cluster.fork();
  });

  // Send messages to workers
  for (const id in cluster.workers) {
    cluster.workers[id]!.send({ type: "config", data: { port: 3000 } });
  }
} else {
  // Workers share the TCP connection
  createServer((req, res) => {
    res.writeHead(200);
    res.end(`Handled by worker ${process.pid}\n`);
  }).listen(3000);

  process.on("message", (msg) => {
    console.log(`Worker ${process.pid} received:`, msg);
  });

  console.log(`Worker ${process.pid} started`);
}
```

### Diagnostics Channel

```typescript
import diagnostics_channel from "node:diagnostics_channel";

// Create a channel
const channel = diagnostics_channel.channel("app:requests");

// Subscribe to events
channel.subscribe((message: unknown) => {
  const { method, url, duration } = message as {
    method: string;
    url: string;
    duration: number;
  };
  console.log(`${method} ${url} - ${duration}ms`);
});

// Publish events
function handleRequest(method: string, url: string): void {
  const start = performance.now();
  // ... handle request ...
  channel.publish({
    method,
    url,
    duration: performance.now() - start,
  });
}

// TracingChannel (Node 19.9+) -- structured tracing
const tracingChannel = diagnostics_channel.tracingChannel("app:db");

tracingChannel.subscribe({
  start(message) { console.log("Query started:", message); },
  end(message) { console.log("Query ended:", message); },
  error(message) { console.error("Query failed:", message); },
  asyncStart(message) { console.log("Async phase started"); },
  asyncEnd(message) { console.log("Async phase ended"); },
});

// Trace a function call
tracingChannel.traceSync(
  () => {
    // synchronous work
  },
  { query: "SELECT * FROM users" }
);
```

## Error Handling

### Uncaught Exceptions and Unhandled Rejections

```typescript
// Catch unhandled promise rejections (should always be registered)
process.on("unhandledRejection", (reason, promise) => {
  console.error("Unhandled Rejection at:", promise, "reason:", reason);
  // Log to monitoring service, then shut down gracefully
  process.exit(1);
});

// Catch uncaught exceptions (last resort)
process.on("uncaughtException", (error, origin) => {
  console.error("Uncaught Exception:", error);
  console.error("Origin:", origin);
  // IMPORTANT: the process is in an undefined state after uncaughtException.
  // Always exit after logging.
  process.exit(1);
});

// uncaughtExceptionMonitor -- observe without overriding default behavior
process.on("uncaughtExceptionMonitor", (error, origin) => {
  // Log to monitoring service without preventing default crash behavior
  monitoringService.report(error, origin);
});

// Warning handler
process.on("warning", (warning) => {
  console.warn("Warning:", warning.name, warning.message);
});
```

### Error Patterns

```typescript
// Custom error classes
class AppError extends Error {
  constructor(
    message: string,
    public statusCode: number = 500,
    public code: string = "INTERNAL_ERROR",
    public isOperational: boolean = true
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, 404, "NOT_FOUND");
  }
}

class ValidationError extends AppError {
  constructor(
    message: string,
    public fields: Record<string, string>
  ) {
    super(message, 400, "VALIDATION_ERROR");
  }
}

// Error.captureStackTrace -- create cleaner stack traces
function createError(message: string): Error {
  const error = new Error(message);
  Error.captureStackTrace(error, createError); // omits createError from stack
  return error;
}

// Operational vs programmer errors
function isOperationalError(error: unknown): boolean {
  if (error instanceof AppError) return error.isOperational;
  return false;
}

// Global error handler pattern
process.on("uncaughtException", (error) => {
  if (isOperationalError(error)) {
    console.error("Operational error:", error.message);
    // Log and continue (if safe)
  } else {
    console.error("Programmer error -- crashing:", error);
    process.exit(1);
  }
});
```

### Async Error Handling Patterns

```typescript
// Try/catch with async/await
async function fetchUser(id: string): Promise<User> {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) {
      throw new AppError(`User fetch failed: ${response.status}`, response.status);
    }
    return await response.json();
  } catch (error) {
    if (error instanceof AppError) throw error;
    throw new AppError("Network error fetching user", 503);
  }
}

// Result type pattern (avoid throwing)
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

async function safeReadFile(path: string): Promise<Result<string>> {
  try {
    const content = await readFile(path, "utf-8");
    return { ok: true, value: content };
  } catch (error) {
    return { ok: false, error: error as Error };
  }
}

const result = await safeReadFile("./config.json");
if (result.ok) {
  console.log(result.value);
} else {
  console.error("Failed:", result.error.message);
}
```

## Environment Variables

```typescript
// Access environment variables
const port = process.env.PORT || "3000";
const nodeEnv = process.env.NODE_ENV || "development";
const databaseUrl = process.env.DATABASE_URL;

// Check for required variables
function requireEnv(name: string): string {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}

const apiKey = requireEnv("API_KEY");
```

```bash
# --env-file flag (Node 20.6+)
node --env-file=.env server.js
node --env-file=.env --env-file=.env.local server.js

# Multiple env files (later files override earlier ones)
node --env-file=.env --env-file=.env.production server.js
```

```ini
# .env file format (supported by --env-file)
PORT=3000
DATABASE_URL=postgres://localhost:5432/mydb
API_KEY=sk-abc123
NODE_ENV=development
# Comments are supported
MULTILINE="line1\nline2"
```

## TypeScript Support

### Experimental Type Stripping (Node 22+)

```bash
# Run TypeScript directly (strips types, no emit, no type checking)
node --experimental-strip-types app.ts

# With enums and namespaces (Node 23+)
node --experimental-transform-types app.ts
```

**Limitations of `--experimental-strip-types`:**
- Only strips types; does not perform type checking (use `tsc --noEmit` separately).
- Does not support TypeScript-specific emit features (enums, namespaces, decorators) without `--experimental-transform-types`.
- Does not support `paths` in tsconfig (use subpath imports in package.json instead).
- File extensions must be `.ts`, not `.tsx` (JSX requires a transform).

### tsx (Recommended for Development)

```bash
# Install
npm install -D tsx

# Run TypeScript files
npx tsx app.ts

# Watch mode
npx tsx watch app.ts

# Use as Node.js loader
node --import tsx app.ts
```

```jsonc
// package.json
{
  "scripts": {
    "dev": "tsx watch src/server.ts",
    "start": "node dist/server.js",
    "build": "tsc"
  }
}
```

### ts-node

```bash
# Install
npm install -D ts-node typescript

# Run
npx ts-node app.ts

# With ESM
node --loader ts-node/esm app.ts
```

```jsonc
// tsconfig.json for ts-node with ESM
{
  "compilerOptions": {
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "target": "ES2022",
    "esModuleInterop": true,
    "strict": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "ts-node": {
    "esm": true,
    "transpileOnly": true
  }
}
```

### Recommended tsconfig.json for Node.js

```jsonc
// Node 20+ recommended tsconfig
{
  "compilerOptions": {
    // Language and environment
    "target": "ES2022",
    "lib": ["ES2023"],
    "module": "NodeNext",
    "moduleResolution": "NodeNext",

    // Strictness
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true,

    // Output
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,

    // Interop
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true,

    // Skip type checking node_modules
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

## Diagnostics and Debugging

### Inspector (--inspect)

```bash
# Start with debugger listening
node --inspect server.js          # Listen on 127.0.0.1:9229
node --inspect=0.0.0.0:9229 server.js # Listen on all interfaces
node --inspect-brk server.js      # Break on first line

# Debug TypeScript with tsx
node --inspect --import tsx src/server.ts
```

Open `chrome://inspect` in Chrome, or connect from VS Code with a launch configuration:

```jsonc
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Debug TypeScript",
      "runtimeExecutable": "tsx",
      "args": ["${workspaceFolder}/src/server.ts"],
      "sourceMaps": true,
      "console": "integratedTerminal"
    }
  ]
}
```

### Async Hooks

```typescript
import { AsyncLocalStorage, AsyncResource } from "node:async_hooks";

// AsyncLocalStorage -- request-scoped context (recommended pattern)
const requestContext = new AsyncLocalStorage<{
  requestId: string;
  userId?: string;
}>();

function handleRequest(req: IncomingMessage, res: ServerResponse): void {
  const requestId = crypto.randomUUID();
  requestContext.run({ requestId }, () => {
    // All async operations within this callback share the context
    processRequest(req, res);
  });
}

function getRequestId(): string | undefined {
  return requestContext.getStore()?.requestId;
}

// Use in logging
function log(message: string): void {
  const store = requestContext.getStore();
  console.log(`[${store?.requestId ?? "no-ctx"}] ${message}`);
}
```

### Heap Snapshots and Profiling

```bash
# Generate heap snapshot on signal
kill -USR2 <pid>

# Generate heap snapshot programmatically
node --heapsnapshot-signal=SIGUSR2 server.js

# CPU profiling
node --prof server.js
node --prof-process isolate-*.log > profile.txt

# Heap snapshot from code
```

```typescript
import v8 from "node:v8";
import { writeFileSync } from "node:fs";

// Write heap snapshot
const snapshotPath = v8.writeHeapSnapshot();
console.log(`Heap snapshot written to: ${snapshotPath}`);

// Heap statistics
const stats = v8.getHeapStatistics();
console.log(`Heap used: ${(stats.used_heap_size / 1024 / 1024).toFixed(1)} MB`);
console.log(`Heap limit: ${(stats.heap_size_limit / 1024 / 1024).toFixed(1)} MB`);
```

## Security

### Experimental Permission Model (Node 20+)

```bash
# File system permissions
node --experimental-permission --allow-fs-read=/app/config --allow-fs-write=/app/logs server.js

# Network and child process permissions
node --experimental-permission \
  --allow-fs-read=* \
  --allow-child-process \
  server.js

# No permissions (maximally restricted)
node --experimental-permission server.js
```

```typescript
// Check permissions at runtime
import { permission } from "node:process";

if (permission.has("fs.read", "/etc/passwd")) {
  console.log("Has read access to /etc/passwd");
}

if (!permission.has("child")) {
  console.log("Cannot spawn child processes");
}
```

### Security Best Practices

```typescript
// Validate and sanitize all external input
import { URL } from "node:url";

function validateUrl(input: string): URL {
  const url = new URL(input);
  if (!["http:", "https:"].includes(url.protocol)) {
    throw new Error("Only HTTP(S) URLs are allowed");
  }
  return url;
}

// Prevent path traversal
import { resolve, normalize } from "node:path";

function safePath(baseDir: string, userPath: string): string {
  const resolved = resolve(baseDir, userPath);
  const normalized = normalize(resolved);
  if (!normalized.startsWith(resolve(baseDir))) {
    throw new Error("Path traversal detected");
  }
  return normalized;
}

// Use timing-safe comparison for secrets
import { timingSafeEqual, createHmac } from "node:crypto";

function verifySignature(payload: string, signature: string, secret: string): boolean {
  const expected = createHmac("sha256", secret).update(payload).digest("hex");
  if (signature.length !== expected.length) return false;
  return timingSafeEqual(Buffer.from(signature), Buffer.from(expected));
}
```

## Native Addons

### N-API (Node-API)

N-API is the stable C/C++ API for building native addons that are ABI-stable across Node.js versions.

```javascript
// binding.gyp
{
  "targets": [
    {
      "target_name": "addon",
      "sources": ["src/addon.c"],
      "include_dirs": ["<!@(node -p \"require('node-addon-api').include\")"],
      "defines": ["NAPI_DISABLE_CPP_EXCEPTIONS"]
    }
  ]
}
```

```bash
# Build with node-gyp
npm install -g node-gyp
node-gyp configure
node-gyp build

# Use prebuild for precompiled binaries
npm install prebuild prebuild-install
npx prebuild -t 18.0.0 -t 20.0.0 -t 22.0.0
```

```typescript
// Using a native addon
const addon = require("./build/Release/addon.node");
// Or with N-API node-addon-api (C++ wrapper):
// const addon = require("bindings")("addon");

const result = addon.heavyComputation(data);
```

**When to use native addons:**
- CPU-intensive computation that cannot be efficiently parallelized with worker threads.
- Wrapping existing C/C++ libraries (e.g., image processing, cryptography, machine learning).
- Low-level system access not available through Node.js APIs.

**Prefer alternatives when possible:**
- WebAssembly (WASM) for portable native performance without compilation per platform.
- Worker threads for CPU parallelism within JavaScript.
- Child processes for calling external binaries.

## Single Executable Applications (Node 20+)

Node.js can bundle an application into a single executable binary that includes the Node.js runtime.

```jsonc
// sea-config.json
{
  "main": "./dist/app.js",
  "output": "./dist/sea-prep.blob",
  "disableExperimentalSEAWarning": true,
  "useSnapshot": false,
  "useCodeCache": true
}
```

```bash
# 1. Bundle your application (single file)
npx esbuild src/app.ts --bundle --platform=node --outfile=dist/app.js

# 2. Generate the SEA preparation blob
node --experimental-sea-config sea-config.json

# 3. Copy the Node.js binary
cp $(command -v node) ./myapp

# 4. Inject the blob (macOS/Linux)
npx postject ./myapp NODE_SEA_BLOB dist/sea-prep.blob \
  --sentinel-fuse NODE_SEA_FUSE_fce680ab2cc467b6e072b8b5df1996b2

# 5. Run the standalone binary
./myapp
```

## package.json Exports Field Patterns

### Self-Referencing

```jsonc
{
  "name": "my-package",
  "exports": {
    ".": "./src/index.js"
  }
}
```

```typescript
// Within the same package, import via package name
import { helper } from "my-package"; // resolves to ./src/index.js
```

### Subpath Imports (Private Imports)

```jsonc
{
  "imports": {
    "#db": {
      "production": "./src/db/production.js",
      "default": "./src/db/development.js"
    },
    "#utils/*": "./src/utils/*.js"
  }
}
```

```typescript
// Import using the # prefix (private, not exposed to consumers)
import { connect } from "#db";
import { formatDate } from "#utils/date";
```

## Best Practices

1. **Use the latest Active LTS version** for production. Enable automatic security updates or have a process to apply them promptly.

2. **Use ESM for new projects.** Set `"type": "module"` in `package.json`. Use `.mjs`/`.cjs` extensions only when mixing module systems within a single package.

3. **Use `node:` prefix for built-in modules.** Write `import fs from "node:fs/promises"` instead of `import fs from "fs"` to make it unambiguous that you are importing a built-in.

4. **Use `fs/promises` instead of callback-based `fs`.** The promise-based API integrates naturally with async/await and avoids callback hell.

5. **Use `stream/promises` pipeline** for composing streams. Always handle backpressure by using `pipeline()` instead of manual `.pipe()` chains.

6. **Use `AbortController` for cancellation.** Pass `AbortSignal` to fetch, child processes, streams, and timers to enable clean cancellation.

7. **Always handle `unhandledRejection`** and `uncaughtException`. Log the error, flush metrics, and exit the process. Do not attempt to continue running after `uncaughtException`.

8. **Use `AsyncLocalStorage`** for request-scoped context (request IDs, user context, tracing spans) instead of passing context through every function argument.

9. **Use worker threads for CPU-intensive work.** The main event loop should only handle I/O coordination. Offload heavy computation to worker threads.

10. **Use `--env-file`** (Node 20.6+) instead of the `dotenv` package for loading environment variables from `.env` files.

11. **Configure the `exports` field** in `package.json` for any published package. Include `"types"` conditions for TypeScript consumers and both `"import"` and `"require"` conditions for dual CJS/ESM support.

12. **Use `tsx` for development** and `tsc` (or a bundler) for production builds. Do not use `ts-node` in production due to startup overhead.

13. **Enable `--experimental-permission`** in Node 20+ for defense-in-depth in production environments where the application should not access arbitrary file system paths or spawn processes.

14. **Use `diagnostics_channel`** for lightweight instrumentation and observability. It has near-zero overhead when no subscribers are registered.

15. **Prefer `node --test`** for simple test suites that do not need a full framework. For complex projects, use Vitest or Jest with proper TypeScript support.

16. **Use `process.exit()` sparingly.** Prefer graceful shutdown by closing servers, database connections, and flushing logs before exiting. Listen for `SIGTERM` and `SIGINT`.

17. **Set `"engines"` in package.json** to declare the minimum Node.js version:
    ```jsonc
    { "engines": { "node": ">=20.0.0" } }
    ```

18. **Profile before optimizing.** Use `--inspect`, `--prof`, heap snapshots, and `perf_hooks` to identify actual bottlenecks rather than guessing.
