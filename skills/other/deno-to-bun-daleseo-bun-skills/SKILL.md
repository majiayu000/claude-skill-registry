---
name: deno-to-bun
description: Migrate Deno projects to Bun with API compatibility analysis. Use when converting Deno.* APIs to Bun equivalents, migrating from Deno Deploy, or updating permissions model and import maps.
compatibility: Requires Bun 1.0+
allowed-tools: ["Bash", "Read", "Grep", "Write"]
metadata:
  author: daleseo
  category: bun-runtime
  tags: [bun, migration, deno, deno-to-bun, compatibility, apis]
---

# Deno to Bun Migration

You are assisting with migrating an existing Deno project to Bun. This involves converting Deno APIs, updating configurations, and adapting to Bun's runtime model.

## Quick Reference

For detailed patterns, see:
- **API Mapping**: [api-mapping.md](references/api-mapping.md) - Deno.* to Bun equivalents
- **Permissions**: [permissions.md](references/permissions.md) - Permission model differences

## Migration Workflow

### 1. Pre-Migration Analysis

**Check if Bun is installed:**
```bash
bun --version
```

**Analyze current Deno project:**
```bash
# Check Deno version
deno --version

# Check for deno.json/deno.jsonc
ls -la | grep -E "deno.json|deno.jsonc"

# List permissions used
grep -r "deno run" .
```

Read `deno.json` or `deno.jsonc` to understand the project configuration.

### 2. API Compatibility Analysis

**Common Deno APIs and their Bun equivalents:**

#### File System
```typescript
// Deno
const text = await Deno.readTextFile("file.txt");
await Deno.writeTextFile("file.txt", "content");

// Bun
const text = await Bun.file("file.txt").text();
await Bun.write("file.txt", "content");
```

#### HTTP Server
```typescript
// Deno
Deno.serve({ port: 3000 }, (req) => {
  return new Response("Hello");
});

// Bun
Bun.serve({
  port: 3000,
  fetch(req) {
    return new Response("Hello");
  },
});
```

#### Environment Variables
```typescript
// Deno
const value = Deno.env.get("KEY");

// Bun (same as Node.js)
const value = process.env.KEY;
```

#### Reading JSON
```typescript
// Deno
const data = await Deno.readTextFile("data.json");
const json = JSON.parse(data);

// Bun
const json = await Bun.file("data.json").json();
```

For complete API mapping, see [api-mapping.md](references/api-mapping.md).

### 3. Configuration Migration

**Convert deno.json to package.json and bunfig.toml:**

**deno.json:**
```json
{
  "tasks": {
    "dev": "deno run --allow-net --allow-read main.ts",
    "test": "deno test"
  },
  "imports": {
    "oak": "https://deno.land/x/oak@v12.6.1/mod.ts"
  },
  "compilerOptions": {
    "lib": ["deno.window"]
  }
}
```

**package.json (Bun):**
```json
{
  "name": "my-bun-project",
  "type": "module",
  "scripts": {
    "dev": "bun run --hot main.ts",
    "test": "bun test"
  },
  "dependencies": {
    "hono": "^3.0.0"
  }
}
```

**bunfig.toml:**
```toml
[test]
preload = ["./tests/setup.ts"]
```

### 4. Import Map Conversion

**Deno imports:**
```typescript
// Deno - URL imports
import { serve } from "https://deno.land/std@0.200.0/http/server.ts";
import { oak } from "https://deno.land/x/oak@v12.6.1/mod.ts";
```

**Bun imports:**
```typescript
// Bun - npm packages
import { Hono } from "hono";
// Or for std library equivalents, use npm packages
```

**Common replacements:**
- `deno.land/std/http` → `hono` or native `Bun.serve`
- `deno.land/x/oak` → `hono` or `express`
- `deno.land/std/testing` → `bun:test`
- `deno.land/std/path` → Node.js `path` module

### 5. Permission Model Changes

**Deno permissions:**
```bash
deno run --allow-read --allow-write --allow-net main.ts
```

**Bun (no permission system):**
```bash
bun run main.ts  # Full system access by default
```

**Security implications:**
- Bun has no permission system like Deno
- Review code for security concerns
- Use environment variables for sensitive operations
- Consider running in containers for isolation

For detailed permission migration, see [permissions.md](references/permissions.md).

### 6. Update File Extensions and Imports

**Deno allows extension-less imports:**
```typescript
// Deno
import { helper } from "./utils";  // Resolves to utils.ts
```

**Bun requires extensions:**
```typescript
// Bun
import { helper } from "./utils.ts";  // Explicit extension
```

### 7. Testing Migration

**Deno test:**
```typescript
import { assertEquals } from "https://deno.land/std/testing/asserts.ts";

Deno.test("example", () => {
  assertEquals(1 + 1, 2);
});
```

**Bun test:**
```typescript
import { test, expect } from "bun:test";

test("example", () => {
  expect(1 + 1).toBe(2);
});
```

### 8. Update package.json

Create or update `package.json`:

```json
{
  "name": "migrated-from-deno",
  "type": "module",
  "scripts": {
    "dev": "bun run --hot main.ts",
    "start": "bun run main.ts",
    "test": "bun test"
  },
  "dependencies": {
    "hono": "^3.0.0"
  }
}
```

### 9. Install Dependencies

```bash
# Remove deno.lock if present
rm deno.lock

# Install Bun dependencies
bun install
```

### 10. Update TypeScript Configuration

Create `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "types": ["bun-types"],
    "lib": ["ES2022"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "allowImportingTsExtensions": true,
    "noEmit": true
  }
}
```

## Common Migration Patterns

### HTTP Server

**Deno:**
```typescript
Deno.serve({ port: 3000 }, (req) => {
  const url = new URL(req.url);

  if (url.pathname === "/") {
    return new Response("Hello");
  }

  return new Response("Not found", { status: 404 });
});
```

**Bun:**
```typescript
Bun.serve({
  port: 3000,
  fetch(req) {
    const url = new URL(req.url);

    if (url.pathname === "/") {
      return new Response("Hello");
    }

    return new Response("Not found", { status: 404 });
  },
});
```

### File Operations

**Deno:**
```typescript
const file = await Deno.open("file.txt");
const decoder = new TextDecoder();
const content = decoder.decode(await Deno.readAll(file));
file.close();
```

**Bun:**
```typescript
const content = await Bun.file("file.txt").text();
```

### Environment Variables

**Deno:**
```typescript
const apiKey = Deno.env.get("API_KEY");
Deno.env.set("NEW_VAR", "value");
```

**Bun:**
```typescript
const apiKey = process.env.API_KEY;
process.env.NEW_VAR = "value";  // Note: Setting at runtime doesn't persist
```

### Command Execution

**Deno:**
```typescript
const command = new Deno.Command("ls", {
  args: ["-la"],
});
const { stdout } = await command.output();
```

**Bun:**
```typescript
import { $ } from "bun";

const output = await $`ls -la`.text();
```

## Verification Steps

Run these commands to verify migration:

```bash
# 1. Install dependencies
bun install

# 2. Type check
bun run --bun tsc --noEmit

# 3. Run tests
bun test

# 4. Try development server
bun run dev

# 5. Test production build (if applicable)
bun run build
```

## Migration Checklist

Present this checklist to the user:

- [ ] Bun installed and verified
- [ ] Deno APIs mapped to Bun equivalents
- [ ] deno.json converted to package.json
- [ ] Import maps converted to npm dependencies
- [ ] URL imports replaced with npm packages
- [ ] File extensions added to imports
- [ ] Permission flags removed (security reviewed)
- [ ] Test framework migrated to bun:test
- [ ] TypeScript configuration created
- [ ] Dependencies installed with `bun install`
- [ ] Tests passing with `bun test`
- [ ] Application runs successfully
- [ ] Documentation updated

## Known Differences

### Deno Features Not in Bun

1. **Permission System**: Bun has full system access
2. **URL Imports**: Must use npm packages or local files
3. **Deno Deploy**: Use Docker or other deployment (see bun-deploy skill)
4. **Deno Namespace**: No `Deno.*` APIs (use Bun/Node equivalents)
5. **Built-in Formatter/Linter**: Use separate tools (Biome, ESLint, Prettier)

### Bun Advantages Over Deno

1. **npm Ecosystem**: Full access to npm packages
2. **Performance**: Faster startup and execution
3. **Package Manager**: Built-in package manager (3x faster than npm)
4. **Native Bundler**: Built-in bundler and transpiler
5. **Jest Compatibility**: Familiar testing API

## Completion

Once migration is complete, provide summary:
- ✅ Migration status (success/partial/issues)
- ✅ List of changes made
- ✅ API conversions performed
- ✅ Any remaining manual steps
- ✅ Links to Bun documentation for ongoing development

## Next Steps

Suggest to the user:
1. Review security implications (no permission system)
2. Update CI/CD pipelines for Bun
3. Consider containerization (bun-deploy skill)
4. Optimize with Bun-specific features
5. Update team documentation
