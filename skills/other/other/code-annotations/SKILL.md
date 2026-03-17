---
name: code-annotations
description: Code annotation requirements for pikru. Use when writing or porting Rust functions from C code. All ported functions must have cref comments.
---

# Code Annotations

All Rust functions ported from C must be annotated with a cref comment:

```rust
// cref: c_function_name
fn rust_function() { ... }
```

## Purpose

The `// cref:` comments create a traceable link between the Rust implementation and the original C function it was ported from. This helps:

- Future maintainers understand the origin of the code
- Cross-reference behavior between C and Rust implementations
- Debug discrepancies between the two implementations
