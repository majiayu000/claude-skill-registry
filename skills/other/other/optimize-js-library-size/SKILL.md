---
name: optimize-js-library-size
description: Optimize JavaScript library size
disable-model-invocation: true
---

Reduce the size of this JavaScript library.

# Goals

- Reduce the minified and gzipped/brotli minified size
- NEVER reduce minified size at the expense of gzipped/brotli minified size
- ALWAYS preserve the public API surface
- Focus on large structural changes instead of small wins

# Workflow

1. Read and understand the library structure
2. Run relevant tests and note which ones already fail (do NOT fix them)
3. Measure size
4. Optimize
5. Rebuild
6. Measure size and compare: if size didn't improve, then revert and go back to
   step 4
7. Run relevant tests: if tests are newly failing, then revert and go back to
   step 4
8. Repeat from step 4

# Tools

- Ensure `terser` is configured:

  ```js
  {
    // Assume modern JavaScript
    ecma: 2020,
    module: true,
    toplevel: true,
    // Run multiple times
    compress: {
      passes: 3,
    },
    // Mangle underscore prefixed properties
    mangle: {
      properties: {
        regex: `^_[^_]+`,
      },
    },
  }
  ```

- Use `node` to measure size:

  ```bash
  node --input-type=module << 'EOF'
    import { readFileSync } from 'fs'
    import { gzipSync, brotliCompressSync } from 'zlib'
    const raw = readFileSync('REPLACE_ME.js', 'utf8')
    const minified = Buffer.from(raw.replace(/^\/\/# sourceMappingURL=[^\n]+$/m, '').trimEnd())
    console.log(`Minified: ${minified.length} | Gzipped: ${gzipSync(minified).length} | Brotli: ${brotliCompressSync(minified).length}`)
  EOF
  ```

# Techniques

## High-level

- Delete dead code
- Unify repeated or similar logic
- Simplify complex logic without changing behavior
- Extract repeated code to variables or functions

## Low-level

- Mangle internal objects using private class fields or underscore prefixed
  properties
- Replace internal classes with closures returning objects
- Inline single-use functions that don't add clarity
- Restructure single-use functions that add clarity to be inlinable by `terser`
- Replace `function`s with arrow functions
- Replace `switch` with `if` and `else`
- Replace `===`/`!==` with `==`/`!=` when it doesn't change behavior
- Replace strict checks with truthy/falsy checks when it doesn't change behavior

These aren't exhaustive. Reason from first principles when none fits cleanly.
