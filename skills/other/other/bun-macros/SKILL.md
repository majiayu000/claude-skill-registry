---
name: Bun Macros
description: Evaluate JavaScript at bundle time and inline results. Use when optimizing compile-time code generation, embedding files, inlining environment variables, or executing code during the bundling process.
version: 1.0.0
---

# Bun Macros

Bun macros run JavaScript at bundle time and inline the results into the output.

## Quick Start

```typescript
// src/config.ts (macro file)
export function getVersion() {
  return "1.0.0";
}

export function getBuildTime() {
  return new Date().toISOString();
}

// src/index.ts (consumer)
import { getVersion, getBuildTime } from "./config" with { type: "macro" };

// At bundle time, these become:
const version = "1.0.0";
const buildTime = "2024-01-15T12:00:00.000Z";
```

## Macro Syntax

```typescript
// Import with macro attribute
import { fn } from "./macro-file" with { type: "macro" };

// Call the macro (evaluated at build time)
const result = fn();
```

## Common Use Cases

### Environment Inlining

```typescript
// macros/env.ts
export function env(key: string): string {
  return process.env[key] ?? "";
}

// src/index.ts
import { env } from "./macros/env" with { type: "macro" };

const apiUrl = env("API_URL");
// Becomes: const apiUrl = "https://api.example.com";
```

### Git Information

```typescript
// macros/git.ts
export function gitCommit(): string {
  return Bun.spawnSync(["git", "rev-parse", "HEAD"])
    .stdout.toString().trim();
}

export function gitBranch(): string {
  return Bun.spawnSync(["git", "branch", "--show-current"])
    .stdout.toString().trim();
}

// src/index.ts
import { gitCommit, gitBranch } from "./macros/git" with { type: "macro" };

const BUILD_INFO = {
  commit: gitCommit(),
  branch: gitBranch(),
};
// Inlined at build time
```

### File Embedding

```typescript
// macros/embed.ts
export function embedFile(path: string): string {
  return Bun.file(path).text();
}

export function embedJSON(path: string): unknown {
  return Bun.file(path).json();
}

// src/index.ts
import { embedFile, embedJSON } from "./macros/embed" with { type: "macro" };

const license = embedFile("./LICENSE");
const config = embedJSON("./config.json");
```

### Build Constants

```typescript
// macros/constants.ts
export function isDev(): boolean {
  return process.env.NODE_ENV !== "production";
}

export function buildDate(): number {
  return Date.now();
}

export function randomId(): string {
  return Math.random().toString(36).slice(2);
}

// src/index.ts
import { isDev, buildDate, randomId } from "./macros/constants" with { type: "macro" };

if (isDev()) {
  console.log("Development mode");
}

const BUILD_ID = randomId();
```

### Directory Listing

```typescript
// macros/files.ts
import { readdirSync } from "fs";

export function listRoutes(): string[] {
  return readdirSync("./src/routes")
    .filter(f => f.endsWith(".tsx"))
    .map(f => f.replace(".tsx", ""));
}

// src/router.ts
import { listRoutes } from "./macros/files" with { type: "macro" };

const routes = listRoutes();
// Becomes: const routes = ["home", "about", "users"];
```

### Code Generation

```typescript
// macros/codegen.ts
export function generateTypes(schema: string): string {
  // Parse schema and generate types at build time
  const types = parseSchemaToTypes(schema);
  return types;
}

export function generateAPI(spec: string): string {
  const openapi = JSON.parse(Bun.file(spec).text());
  // Generate API client code
  return generateClientFromOpenAPI(openapi);
}
```

## Return Types

Macros can return:

```typescript
// Primitives
export function getString(): string { return "hello"; }
export function getNumber(): number { return 42; }
export function getBoolean(): boolean { return true; }
export function getNull(): null { return null; }

// Objects (serializable)
export function getObject(): object {
  return { key: "value", nested: { a: 1 } };
}

// Arrays
export function getArray(): string[] {
  return ["a", "b", "c"];
}

// Response (for bundler plugins)
export function getResponse(): Response {
  return new Response("content", {
    headers: { "Content-Type": "text/plain" },
  });
}
```

## Async Macros

```typescript
// macros/fetch.ts
export async function fetchSchema(): Promise<object> {
  const response = await fetch("https://api.example.com/schema.json");
  return response.json();
}

// src/index.ts
import { fetchSchema } from "./macros/fetch" with { type: "macro" };

const schema = await fetchSchema();
// Fetched at build time, inlined as object literal
```

## Parameters

```typescript
// macros/parameterized.ts
export function repeat(str: string, count: number): string {
  return str.repeat(count);
}

export function formatDate(format: string): string {
  return new Date().toLocaleDateString("en-US", {
    dateStyle: format as any,
  });
}

// src/index.ts
import { repeat, formatDate } from "./macros/parameterized" with { type: "macro" };

const separator = repeat("-", 20);
const date = formatDate("long");
```

## Conditional Code

```typescript
// macros/platform.ts
export function platform(): "node" | "bun" | "browser" {
  if (typeof Bun !== "undefined") return "bun";
  if (typeof process !== "undefined") return "node";
  return "browser";
}

// src/index.ts
import { platform } from "./macros/platform" with { type: "macro" };

if (platform() === "bun") {
  // This block is kept or removed at build time
  console.log("Running on Bun");
}
```

## Bundle-Only Execution

Macros ONLY run during bundling:

```bash
# Macros executed
bun build src/index.ts --outdir=dist

# Macros NOT executed (runtime)
bun run src/index.ts
```

## Error Handling

```typescript
// macros/safe.ts
export function requireEnv(key: string): string {
  const value = process.env[key];
  if (!value) {
    throw new Error(`Missing required env var: ${key}`);
  }
  return value;
}

// Build fails if env var missing
import { requireEnv } from "./macros/safe" with { type: "macro" };
const secret = requireEnv("API_SECRET");
```

## Debugging Macros

```typescript
// macros/debug.ts
export function debug(label: string, value: unknown): unknown {
  console.log(`[MACRO] ${label}:`, value);
  return value;
}

// See output during build
bun build src/index.ts --outdir=dist
// [MACRO] config: { ... }
```

## Best Practices

1. **Keep macros pure** - Avoid side effects
2. **Return serializable values** - Must be JSON-compatible
3. **Handle errors** - Throw meaningful errors for build failures
4. **Document dependencies** - Note what files/env vars are required
5. **Test separately** - Macros can be tested as regular functions

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Cannot find module` | Wrong import path | Check macro file location |
| `Not serializable` | Function/class returned | Return plain data |
| `Macro failed` | Runtime error in macro | Debug macro separately |
| `Not evaluated` | Missing `with { type: "macro" }` | Add import attribute |

## When to Load References

Load `references/advanced-patterns.md` when:
- Complex code generation
- Plugin integration
- Build pipelines
Retrieve and present patterns for custom macro implementations, integration examples with build systems, and advanced bundler plugin workflows.

Load `references/debugging.md` when:
- Macro not evaluating
- Unexpected output
- Performance issues
Retrieve debugging techniques, provide step-by-step diagnostics, and offer optimization strategies tied to the user's specific issue.
