---
name: cleanTypes
description: TypeScript type best practices - proper typing patterns, avoiding type complexity, meaningful type annotations
---

# TypeScript Type Best Practices

## 1. Implicit is Better Than Explicit

**Rule:** If TypeScript can infer the type, don't annotate it.

TypeScript has powerful type inference. Let the compiler do the work.

### Remove Return Type Annotations

**Bad:**
```typescript
const extractExtension = (filename: string): string =>
  filename.replace(/.*symlink/, '')

function isSymlink(filePath: string): boolean {
  try {
    return fs.lstatSync(filePath).isSymbolicLink()
  } catch {
    return false
  }
}

function buildSymlinkPlan(): SymlinkPlan[] {
  return symlinkFiles.map(src => ({ from: src, to: transformPath(src) }))
}
```

**Good:**
```typescript
const extractExtension = (filename: string) =>
  filename.replace(/.*symlink/, '')

function isSymlink(filePath: string) {
  try {
    return fs.lstatSync(filePath).isSymbolicLink()
  } catch {
    return false
  }
}

function buildSymlinkPlan() {
  return symlinkFiles.map(src => ({ from: src, to: transformPath(src) }))
}
```

**Why:**
- `.replace()` returns `string` - TypeScript knows this
- `return true/false` is clearly `boolean`
- `.map()` with object literal - TypeScript infers the array type

### Use .map() Instead of Imperative Loops

**Bad:**
```typescript
function buildSymlinkPlan(): SymlinkPlan[] {
  const plan: SymlinkPlan[] = []

  for (const src of symlinkFiles) {
    plan.push({ from: src, to: transformPath(src) })
  }

  return plan
}
```

**Good:**
```typescript
function buildSymlinkPlan() {
  return symlinkFiles.map(src => ({ from: src, to: transformPath(src) }))
}
```

**Why:**
- No need for explicit array type annotation
- No need for return type annotation
- More declarative, less noise
- Compiler infers everything correctly

### Remove Variable Type Annotations

**Bad:**
```typescript
interface Logger {
  info: (msg: string) => void
  success: (msg: string) => void
  warn: (msg: string) => void
  error: (msg: string) => void
}

const log: Logger = {
  info: createLogFunction('info'),
  success: createLogFunction('success'),
  warn: createLogFunction('warn'),
  error: createLogFunction('error')
}
```

**Good:**
```typescript
const log = {
  info: createLogFunction('info'),
  success: createLogFunction('success'),
  warn: createLogFunction('warn'),
  error: createLogFunction('error')
}
```

**Why:**
- TypeScript infers the shape from the object literal
- If you remove the annotation and the interface becomes unused, delete it
- Less noise, same type safety

### When to Keep Type Annotations

**Do annotate:**
1. **Function parameters** - Always annotate (TypeScript can't infer these)
2. **At the source** - Type variables early in the chain to help inference flow
3. **Public APIs** - Types are documentation for exported functions
4. **When inference fails** - If compiler infers `any`, you MUST declare explicitly

**Example - Type at the source to enable inference:**
```typescript
// Bad: No type annotation, chain can't infer properly
function findFiles(rootDir: string) {
  const output = execSync(`find . -name '*.txt'`, { cwd: rootDir, encoding: 'utf-8' })
  return output.trim().split('\n').filter(line => line.length > 0)
}
// Compiler may not infer that output is string, causing downstream issues

// Good: Type the source variable, inference flows through the chain
function findFiles(rootDir: string) {
  const output: string = execSync(`find . -name '*.txt'`, { cwd: rootDir, encoding: 'utf-8' })
  return output.trim().split('\n').filter(line => line.length > 0)
}
// Now .trim() knows it's working with string, .split() returns string[], etc.
```

**Don't annotate:**
1. **Obvious return types** - String methods, boolean literals, void functions
2. **Intermediate transformations** - Once you've typed the source, let inference flow
3. **Collection operations** - `.map()`, `.filter()` preserve and transform types correctly

### Benefits

- **Less code** - Fewer type annotations to write and maintain
- **Easier refactoring** - Change implementation, types update automatically
- **Better signal-to-noise** - Annotations that remain are truly meaningful
- **Finds dead code** - Unused interfaces become obvious when you stop annotating

## 2. Type Aliases for Busy Function Signatures

**Rule:** Only use type aliases when the function signature gets "busy" with type noise.

### Simple Signatures - Keep Inline

**Good:**
```typescript
function isSymlink(filePath: string) {
  return fs.lstatSync(filePath).isSymbolicLink()
}

function findSymlinkFiles(rootDir: string): string[] {
  const output = execSync('find . -name "*.txt"', { cwd: rootDir })
  return output.trim().split('\n')
}
```

These are clean - minimal noise, easy to read.

### Busy Signatures - Use Type Alias

**Bad:**
```typescript
function processFiles(
  rootDir: string,
  filter: (file: string, stats: fs.Stats) => boolean,
  transform: (content: string, path: string) => Promise<string>,
  onError: (error: Error, file: string) => void
): Promise<ProcessResult[]> {
  // implementation
}
```

**Good:**
```typescript
type FileFilter = (file: string, stats: fs.Stats) => boolean
type FileTransform = (content: string, path: string) => Promise<string>
type ErrorHandler = (error: Error, file: string) => void
type ProcessFiles = (
  rootDir: string,
  filter: FileFilter,
  transform: FileTransform,
  onError: ErrorHandler
) => Promise<ProcessResult[]>

const processFiles: ProcessFiles = (rootDir, filter, transform, onError) => {
  // implementation
}
```

**Why:** The signature is now scannable - you see the parameter names clearly, and can check the type alias definitions separately if needed.

### When to Use Type Aliases

**Use type aliases when:**
- Function has 4+ parameters
- Parameters have complex types (callbacks, generic types)
- The same signature is used multiple times
- The inline signature makes the function definition hard to scan

**Don't use type aliases when:**
- Function has 1-3 simple parameters
- Types are obvious (string, number, boolean)
- Compiler can infer the return type
- The inline signature is still readable

## 3. Accept Nullable Types, Handle Explicitly

**Rule:** Accept `T | null` in your type signatures, handle the null case explicitly with clear failure semantics.

**Bad:**
```typescript
// Filter nulls early, pass only valid values
function buildPlan() {
  return files.map(transformPath).filter(path => path !== null)
}

function executePlan(plan: string[]) {
  // Silent assumption: all paths are valid
  return plan.map(path => createLink(path))
}
```

**Good:**
```typescript
// Accept nullable type, handle explicitly
function buildPlan() {
  return files.map(file => ({
    from: file,
    to: transformPath(file) // Returns string | null
  }))
}

function executePlan(plan: Array<{from: string, to: string | null}>) {
  return plan.map(({ from, to }) => safeLink(from, to))
}

function safeLink(src: string, dest: string | null) {
  if (!dest) {
    // Explicit failure with error result
    return { from: src, to: '<unparseable>', success: false }
  }
  // Continue with valid dest
}
```

**Why:**
- **Explicit over silent** - Failures are visible in results, not hidden by filtering
- **Push responsibility down** - Let `safeLink` decide what to do with nulls (it's about safety!)
- **Better error tracking** - You can count and report failures, not silently skip them

## 4. Export Discipline

**Rule:** Only export what's actually used by other modules. Everything else is internal implementation.

**Bad:**
```typescript
// links.ts
export { setupSymlinks, buildSymlinkPlan, safeLink, transformPath }
export type { SymlinkPlan, LinkResult }
```

Check if these are imported anywhere:
```bash
$ rg "import.*buildSymlinkPlan"
# No results

$ rg "import.*safeLink"
# No results
```

**Good:**
```typescript
// links.ts - Only export the public API
export { setupSymlinks }
export type { LinkResult }  // Used by consumers
```

**Why:**
- **Clear API surface** - What's exported is your public interface
- **Easier refactoring** - Internal functions can be renamed/removed freely
- **Finds dead code** - Unused exports highlight unnecessary abstractions

**Process:**
1. After writing a module, search for usages: `rg "import.*functionName"`
2. Remove exports that have zero imports
3. Keep only: (a) main public API functions, (b) types used by consumers

## References

- TypeScript Handbook: https://www.typescriptlang.org/docs/handbook/
- Effective TypeScript by Dan Vanderkam
