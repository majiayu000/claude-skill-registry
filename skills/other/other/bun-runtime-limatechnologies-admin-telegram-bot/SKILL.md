---
name: bun-runtime
description: Bun runtime patterns and best practices. Package management, bundling, testing, scripts. Use when working with Bun as the JavaScript runtime.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Bun Runtime - Fast JavaScript Runtime

## Purpose

Expert guidance for Bun:

- **Package Management** - Fast installation
- **Bundling** - Built-in bundler
- **Testing** - Vitest-compatible runner
- **Scripts** - Task runner
- **APIs** - Bun-specific features

---

## Package Management

### Install Dependencies

```bash
# Install all dependencies
bun install

# Add dependency
bun add zod mongoose

# Add dev dependency
bun add -D typescript @types/node

# Add exact version
bun add react@18.2.0

# Add from GitHub
bun add github:user/repo

# Remove dependency
bun remove lodash

# Update dependencies
bun update

# Update specific package
bun update react
```

### bunfig.toml

```toml
# bunfig.toml
[install]
# Disable postinstall scripts for security
ignorescripts = true

# Registry configuration
registry = "https://registry.npmjs.org"

# Install settings
frozen-lockfile = true

[run]
# Shell for scripts
shell = "bash"
```

---

## Script Commands

### package.json Scripts

```json
{
	"scripts": {
		"dev": "bun run --hot src/index.ts",
		"start": "bun run src/index.ts",
		"build": "bun build src/index.ts --outdir dist",
		"typecheck": "bunx tsc --noEmit",
		"lint": "bunx eslint . --ext .ts,.tsx",
		"lint:fix": "bunx eslint . --ext .ts,.tsx --fix",
		"test": "bun test",
		"test:watch": "bun test --watch",
		"test:coverage": "bun test --coverage"
	}
}
```

### Running Scripts

```bash
# Run script
bun run dev
bun run build

# Shorthand (without "run")
bun dev
bun build

# Run TypeScript directly
bun run src/index.ts

# Hot reload
bun run --hot src/index.ts

# Watch mode
bun run --watch src/index.ts
```

---

## Bundling

### Basic Bundle

```bash
# Bundle for browser
bun build ./src/index.ts --outdir ./dist

# Minify
bun build ./src/index.ts --outdir ./dist --minify

# Source maps
bun build ./src/index.ts --outdir ./dist --sourcemap

# Target
bun build ./src/index.ts --outdir ./dist --target=browser
bun build ./src/index.ts --outdir ./dist --target=node
bun build ./src/index.ts --outdir ./dist --target=bun
```

### Build API

```typescript
// build.ts
const result = await Bun.build({
	entrypoints: ['./src/index.ts'],
	outdir: './dist',
	target: 'browser',
	minify: true,
	sourcemap: 'external',
	splitting: true,
	format: 'esm',
	define: {
		'process.env.NODE_ENV': '"production"',
	},
	external: ['react', 'react-dom'],
});

if (!result.success) {
	console.error('Build failed:');
	for (const log of result.logs) {
		console.error(log);
	}
	process.exit(1);
}
```

---

## Testing (Vitest-compatible)

### Test Configuration

```typescript
// bunfig.toml
[test];
preload = ['./tests/setup.ts'];
coverage = true;
```

### Test File

```typescript
// tests/example.test.ts
import { describe, test, expect, beforeEach, afterEach } from 'bun:test';

describe('Feature', () => {
	beforeEach(() => {
		// Setup
	});

	afterEach(() => {
		// Cleanup
	});

	test('should work correctly', () => {
		const result = 1 + 1;
		expect(result).toBe(2);
	});

	test('async operations', async () => {
		const data = await fetchData();
		expect(data).toBeDefined();
	});
});
```

### Mocking

```typescript
import { mock, spyOn } from 'bun:test';

// Mock function
const mockFn = mock((x: number) => x * 2);
mockFn(5);
expect(mockFn).toHaveBeenCalledWith(5);
expect(mockFn).toHaveReturnedWith(10);

// Spy on existing function
const spy = spyOn(console, 'log');
console.log('test');
expect(spy).toHaveBeenCalledWith('test');
```

---

## Bun APIs

### File System

```typescript
// Read file
const text = await Bun.file('path/to/file.txt').text();
const json = await Bun.file('path/to/file.json').json();
const buffer = await Bun.file('path/to/file.bin').arrayBuffer();

// Write file
await Bun.write('output.txt', 'Hello, World!');
await Bun.write('output.json', JSON.stringify({ hello: 'world' }));

// File info
const file = Bun.file('file.txt');
console.log(file.size);
console.log(file.type);
```

### HTTP Server

```typescript
// Simple server
Bun.serve({
	port: 3000,
	fetch(request) {
		const url = new URL(request.url);

		if (url.pathname === '/api/hello') {
			return Response.json({ message: 'Hello!' });
		}

		return new Response('Not Found', { status: 404 });
	},
});

// With WebSocket
Bun.serve({
	port: 3000,
	fetch(request, server) {
		if (server.upgrade(request)) {
			return;
		}
		return new Response('Upgrade failed', { status: 500 });
	},
	websocket: {
		open(ws) {
			console.log('Client connected');
		},
		message(ws, message) {
			ws.send(`Echo: ${message}`);
		},
		close(ws) {
			console.log('Client disconnected');
		},
	},
});
```

### Subprocess

```typescript
// Run command
const result = Bun.spawn(['echo', 'Hello']);
await result.exited;

// Capture output
const proc = Bun.spawn(['git', 'status'], {
	stdout: 'pipe',
});
const output = await new Response(proc.stdout).text();

// With stdin
const proc = Bun.spawn(['cat'], {
	stdin: 'pipe',
	stdout: 'pipe',
});
proc.stdin.write('Hello from stdin!');
proc.stdin.end();
```

### Password Hashing

```typescript
// Hash password
const hash = await Bun.password.hash('my-password', {
	algorithm: 'bcrypt',
	cost: 10,
});

// Verify password
const isValid = await Bun.password.verify('my-password', hash);
```

### Environment Variables

```typescript
// Access env vars
const apiKey = Bun.env['API_KEY'];
const nodeEnv = Bun.env['NODE_ENV'] ?? 'development';

// Set env vars
Bun.env['CUSTOM_VAR'] = 'value';
```

---

## Performance Tips

### Use Native APIs

```typescript
// Prefer Bun APIs over Node.js equivalents

// File reading
// Node.js way (slower)
import { readFile } from 'fs/promises';
const content = await readFile('file.txt', 'utf-8');

// Bun way (faster)
const content = await Bun.file('file.txt').text();
```

### Import Optimization

```typescript
// Use namespace imports for tree-shaking
import * as z from 'zod';

// Avoid dynamic imports in hot paths
// Bad:
async function validate(data: unknown) {
	const { z } = await import('zod');
	return z.object({}).parse(data);
}

// Good:
import { z } from 'zod';
function validate(data: unknown) {
	return z.object({}).parse(data);
}
```

### Bundle for Production

```bash
# Compile to single executable
bun build --compile ./src/index.ts --outfile myapp

# Run compiled binary
./myapp
```

---

## Docker Integration

```dockerfile
# Use Bun official image
FROM oven/bun:1-alpine AS base

# Install dependencies
FROM base AS deps
WORKDIR /app
COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile

# Build
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN bun run build

# Runtime
FROM base AS runner
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./

EXPOSE 3000
CMD ["bun", "run", "dist/index.js"]
```

---

## Agent Integration

This skill is used by:

- **bun-runtime-expert** agent
- **quality-checker** for running tests
- **build-error-fixer** for build issues
- **dockerfile-optimizer** for Docker builds

---

## FORBIDDEN

1. **`npm` commands** - Use `bun` instead
2. **Node.js fs when Bun.file works** - Use native APIs
3. **Ignoring lockfile** - Always use `--frozen-lockfile` in CI
4. **Skipping typecheck** - Run `bunx tsc --noEmit`

---

## Version

- **v1.0.0** - Initial implementation based on Bun 1.x patterns
