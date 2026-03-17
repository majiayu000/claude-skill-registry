---
name: Bun Shell
description: Bun shell scripting with Bun.$, Bun.spawn, subprocess management. Use for shell commands, template literals, or command execution.
---

# Bun Shell

Bun provides powerful shell scripting capabilities with template literals and spawn APIs.

## Bun.$ (Shell Template)

### Basic Usage

```typescript
import { $ } from "bun";

// Run command
await $`echo "Hello World"`;

// Get output
const result = await $`ls -la`.text();
console.log(result);

// JSON output
const pkg = await $`cat package.json`.json();
console.log(pkg.name);
```

### Variable Interpolation

```typescript
import { $ } from "bun";

const name = "world";
const dir = "./src";

// Safe interpolation (escaped)
await $`echo "Hello ${name}"`;
await $`ls ${dir}`;

// Array expansion
const files = ["a.txt", "b.txt", "c.txt"];
await $`touch ${files}`;
```

### Piping

```typescript
import { $ } from "bun";

// Pipe commands
const result = await $`cat file.txt | grep "pattern" | wc -l`.text();

// Chain with JavaScript
const files = await $`ls -la`.text();
const lines = files.split("\n").filter(line => line.includes(".ts"));
```

### Error Handling

```typescript
import { $ } from "bun";

// Throws on non-zero exit
try {
  await $`exit 1`;
} catch (err) {
  console.log(err.exitCode); // 1
  console.log(err.stderr);
}

// Quiet mode (no throw)
const result = await $`exit 1`.quiet();
console.log(result.exitCode); // 1

// Check exit code
const { exitCode } = await $`grep pattern file.txt`.quiet();
if (exitCode !== 0) {
  console.log("Pattern not found");
}
```

### Output Types

```typescript
import { $ } from "bun";

// Text
const text = await $`echo hello`.text();

// JSON
const json = await $`cat data.json`.json();

// Lines
const lines = await $`ls`.lines();

// Blob
const blob = await $`cat image.png`.blob();

// ArrayBuffer
const buffer = await $`cat binary.dat`.arrayBuffer();
```

### Environment Variables

```typescript
import { $ } from "bun";

// Set env for command
await $`echo $MY_VAR`.env({ MY_VAR: "value" });

// Access current env
$.env.MY_VAR = "value";
await $`echo $MY_VAR`;

// Clear env
await $`env`.env({});
```

### Working Directory

```typescript
import { $ } from "bun";

// Change directory for command
await $`pwd`.cwd("/tmp");

// Or globally
$.cwd("/tmp");
await $`pwd`;
```

## Bun.spawn

### Basic Spawn

```typescript
const proc = Bun.spawn(["echo", "Hello World"]);
const output = await new Response(proc.stdout).text();
console.log(output); // "Hello World\n"
```

### With Options

```typescript
const proc = Bun.spawn(["node", "script.js"], {
  cwd: "./project",
  env: {
    NODE_ENV: "production",
    ...process.env,
  },
  stdin: "pipe",
  stdout: "pipe",
  stderr: "pipe",
});

// Write to stdin
proc.stdin.write("input data\n");
proc.stdin.end();

// Read stdout
const output = await new Response(proc.stdout).text();
const errors = await new Response(proc.stderr).text();

// Wait for exit
const exitCode = await proc.exited;
```

### Stdio Options

```typescript
// Inherit (use parent's stdio)
Bun.spawn(["ls"], { stdio: ["inherit", "inherit", "inherit"] });

// Pipe (capture output)
Bun.spawn(["ls"], { stdin: "pipe", stdout: "pipe", stderr: "pipe" });

// Null (ignore)
Bun.spawn(["ls"], { stdout: null, stderr: null });

// File (redirect to file)
Bun.spawn(["ls"], {
  stdout: Bun.file("output.txt"),
  stderr: Bun.file("errors.txt"),
});
```

### Streaming Output

```typescript
const proc = Bun.spawn(["tail", "-f", "log.txt"], {
  stdout: "pipe",
});

const reader = proc.stdout.getReader();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  console.log(new TextDecoder().decode(value));
}
```

## Bun.spawnSync

```typescript
// Synchronous execution
const result = Bun.spawnSync(["ls", "-la"]);

console.log(result.exitCode);
console.log(result.stdout.toString());
console.log(result.stderr.toString());
console.log(result.success); // exitCode === 0
```

## Shell Scripts

### Shebang Scripts

```typescript
#!/usr/bin/env bun
import { $ } from "bun";

// Script logic
const branch = await $`git branch --show-current`.text();
console.log(`Current branch: ${branch.trim()}`);

await $`npm test`;
await $`npm run build`;
```

```bash
chmod +x script.ts
./script.ts
```

### Complex Script

```typescript
#!/usr/bin/env bun
import { $ } from "bun";

async function deploy() {
  console.log("🚀 Starting deployment...");

  // Check for uncommitted changes
  const status = await $`git status --porcelain`.text();
  if (status.trim()) {
    console.error("❌ Uncommitted changes found!");
    process.exit(1);
  }

  // Run tests
  console.log("🧪 Running tests...");
  await $`bun test`;

  // Build
  console.log("🏗️ Building...");
  await $`bun run build`;

  // Deploy
  console.log("📦 Deploying...");
  await $`rsync -avz ./dist/ server:/app/`;

  console.log("✅ Deployment complete!");
}

deploy().catch((err) => {
  console.error("❌ Deployment failed:", err);
  process.exit(1);
});
```

### Parallel Commands

```typescript
import { $ } from "bun";

// Run in parallel
await Promise.all([
  $`npm run lint`,
  $`npm run typecheck`,
  $`npm run test`,
]);

// Or with spawn
const procs = [
  Bun.spawn(["npm", "run", "lint"]),
  Bun.spawn(["npm", "run", "typecheck"]),
  Bun.spawn(["npm", "run", "test"]),
];

await Promise.all(procs.map(p => p.exited));
```

## Interactive Commands

```typescript
import { $ } from "bun";

// Pass through stdin
const proc = Bun.spawn(["node"], {
  stdin: "inherit",
  stdout: "inherit",
  stderr: "inherit",
});

await proc.exited;
```

## Process Management

```typescript
const proc = Bun.spawn(["long-running-process"]);

// Kill process
proc.kill(); // SIGTERM
proc.kill("SIGKILL"); // Force kill

// Check if running
console.log(proc.killed);

// Get PID
console.log(proc.pid);

// Wait with timeout
const timeout = setTimeout(() => proc.kill(), 5000);
await proc.exited;
clearTimeout(timeout);
```

## Common Patterns

### Run npm/bun scripts

```typescript
import { $ } from "bun";

await $`bun run build`;
await $`bun test`;
await $`bunx tsc --noEmit`;
```

### Git Operations

```typescript
import { $ } from "bun";

const branch = await $`git branch --show-current`.text();
const commit = await $`git rev-parse HEAD`.text();
const status = await $`git status --short`.text();

if (status) {
  await $`git add -A`;
  await $`git commit -m "Auto commit"`;
}
```

### File Operations

```typescript
import { $ } from "bun";

// Find files
const files = await $`find . -name "*.ts"`.lines();

// Search content
const matches = await $`grep -r "TODO" src/`.text();

// Archive
await $`tar -czf backup.tar.gz ./data`;
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Command not found` | Not in PATH | Use absolute path |
| `Permission denied` | Not executable | chmod +x |
| `Exit code 1` | Command failed | Check stderr |
| `EPIPE` | Broken pipe | Handle process exit |

## When to Load References

Load `references/advanced-scripting.md` when:
- Complex pipelines
- Process groups
- Signal handling

Load `references/cross-platform.md` when:
- Windows compatibility
- Path handling
- Shell differences
