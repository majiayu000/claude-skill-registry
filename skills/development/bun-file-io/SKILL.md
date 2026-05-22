---
name: Bun File I/O
description: Use for Bun file I/O: Bun.file, Bun.write, streams, directories, glob patterns, metadata.
version: 1.0.0
---

# Bun File I/O

Bun provides fast, optimized file operations via `Bun.file()` and `Bun.write()`.

## Reading Files

### Bun.file()

```typescript
// Create file reference (lazy, doesn't read yet)
const file = Bun.file("./data.txt");

// File properties
console.log(file.size);        // Size in bytes
console.log(file.type);        // MIME type
console.log(file.name);        // File path
console.log(await file.exists()); // Boolean

// Read content
const text = await file.text();
const json = await file.json();
const buffer = await file.arrayBuffer();
const bytes = await file.bytes();   // Uint8Array
const stream = file.stream();       // ReadableStream
```

### Read Specific Types

```typescript
// JSON file
const config = await Bun.file("config.json").json();

// Text file
const content = await Bun.file("readme.md").text();

// Binary file
const binary = await Bun.file("image.png").arrayBuffer();

// With import attributes
import data from "./data.json" with { type: "json" };
import text from "./content.txt" with { type: "text" };
```

## Writing Files

### Bun.write()

```typescript
// Write string
await Bun.write("./output.txt", "Hello World");

// Write JSON
await Bun.write("./data.json", JSON.stringify({ key: "value" }, null, 2));

// Write binary
await Bun.write("./output.bin", new Uint8Array([1, 2, 3]));

// Write from Response
const response = await fetch("https://example.com/image.png");
await Bun.write("./image.png", response);

// Write from another file (efficient copy)
await Bun.write("./copy.txt", Bun.file("./original.txt"));

// Write with options
await Bun.write("./file.txt", "content", {
  mode: 0o644,  // Unix permissions
});
```

### Appending

```typescript
// Using Bun.file writer
const file = Bun.file("./log.txt");
const writer = file.writer();

writer.write("Line 1\n");
writer.write("Line 2\n");
await writer.flush();
writer.end();

// Or use node:fs
import { appendFile } from "node:fs/promises";
await appendFile("./log.txt", "New line\n");
```

## Streaming

### Read Stream

```typescript
const file = Bun.file("./large-file.txt");
const stream = file.stream();

const reader = stream.getReader();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  // Process chunk (Uint8Array)
  console.log(value);
}
```

### Write Stream

```typescript
const file = Bun.file("./output.txt");
const writer = file.writer();

for await (const chunk of dataSource) {
  writer.write(chunk);
}

await writer.end();
```

### Pipe Streams

```typescript
// File to file
const input = Bun.file("./input.txt");
const output = Bun.file("./output.txt");
await Bun.write(output, input);

// HTTP response to file
const response = await fetch(url);
await Bun.write("./download.zip", response);

// Process stream
const file = Bun.file("./data.txt");
const stream = file.stream();

const transformed = stream.pipeThrough(
  new TransformStream({
    transform(chunk, controller) {
      // Process chunk
      controller.enqueue(chunk.toUpperCase());
    },
  })
);
```

## Directory Operations

```typescript
import { readdir, mkdir, rmdir, stat } from "node:fs/promises";
import { existsSync, mkdirSync } from "node:fs";

// List directory
const files = await readdir("./src");
const filesWithTypes = await readdir("./src", { withFileTypes: true });

for (const entry of filesWithTypes) {
  if (entry.isDirectory()) {
    console.log(`Dir: ${entry.name}`);
  } else if (entry.isFile()) {
    console.log(`File: ${entry.name}`);
  }
}

// Create directory
await mkdir("./new-dir", { recursive: true });

// Remove directory
await rmdir("./old-dir", { recursive: true });

// Check if exists
const exists = existsSync("./path");
```

## Glob Patterns

```typescript
// Using Bun.Glob
const glob = new Bun.Glob("**/*.ts");

// Scan directory
for await (const file of glob.scan({ cwd: "./src" })) {
  console.log(file); // Relative paths
}

// Get all matches
const files = await Array.fromAsync(glob.scan("./src"));

// With options
const glob2 = new Bun.Glob("**/*.{ts,tsx}");
for await (const file of glob2.scan({
  cwd: "./src",
  dot: true,           // Include dotfiles
  absolute: true,      // Return absolute paths
  onlyFiles: true,     // Only files, not directories
})) {
  console.log(file);
}

// Test if path matches
const pattern = new Bun.Glob("*.ts");
pattern.match("file.ts");    // true
pattern.match("file.js");    // false
```

## File Metadata

```typescript
import { stat, lstat } from "node:fs/promises";

const stats = await stat("./file.txt");

console.log(stats.size);          // Size in bytes
console.log(stats.isFile());      // Is regular file
console.log(stats.isDirectory()); // Is directory
console.log(stats.isSymbolicLink()); // Is symlink
console.log(stats.mtime);         // Modified time
console.log(stats.ctime);         // Changed time
console.log(stats.atime);         // Access time
console.log(stats.mode);          // Permissions
```

## Path Operations

```typescript
import { join, dirname, basename, extname, resolve } from "node:path";

const filePath = "/home/user/project/src/index.ts";

join("a", "b", "c");           // "a/b/c"
dirname(filePath);             // "/home/user/project/src"
basename(filePath);            // "index.ts"
basename(filePath, ".ts");     // "index"
extname(filePath);             // ".ts"
resolve("./relative");         // Absolute path

// Bun-specific
import.meta.dir;   // Directory of current file
import.meta.file;  // Filename
import.meta.path;  // Full path
```

## Common Patterns

### Read JSON Config

```typescript
async function loadConfig<T>(path: string): Promise<T> {
  const file = Bun.file(path);
  if (!(await file.exists())) {
    throw new Error(`Config not found: ${path}`);
  }
  return file.json();
}

const config = await loadConfig<AppConfig>("./config.json");
```

### Copy Directory

```typescript
import { readdir, mkdir, stat } from "node:fs/promises";
import { join } from "node:path";

async function copyDir(src: string, dest: string) {
  await mkdir(dest, { recursive: true });

  for (const entry of await readdir(src, { withFileTypes: true })) {
    const srcPath = join(src, entry.name);
    const destPath = join(dest, entry.name);

    if (entry.isDirectory()) {
      await copyDir(srcPath, destPath);
    } else {
      await Bun.write(destPath, Bun.file(srcPath));
    }
  }
}
```

### Watch Files

```typescript
import { watch } from "node:fs";

watch("./src", { recursive: true }, (event, filename) => {
  console.log(`${event}: ${filename}`);
});

// Or with Bun's built-in (faster)
const watcher = Bun.spawn(["bun", "--watch", "src/index.ts"]);
```

### Temp Files

```typescript
import { mkdtemp } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";

// Create temp directory
const tempDir = await mkdtemp(join(tmpdir(), "app-"));
console.log(tempDir); // /tmp/app-xxxxx

// Write temp file
const tempFile = join(tempDir, "data.txt");
await Bun.write(tempFile, "temporary data");
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `ENOENT` | File not found | Check path, use exists() |
| `EACCES` | Permission denied | Check file permissions |
| `EISDIR` | Is a directory | Use readdir() for directories |
| `EEXIST` | Already exists | Use recursive: true for mkdir |

## When to Load References

Load `references/streams-advanced.md` when:
- Transform streams
- Compression streams
- Binary protocols

Load `references/performance.md` when:
- Large file handling
- Memory optimization
- Concurrent operations
