---
name: bun-ffi-native-binding
description: Build high-performance native modules for JavaScript using Bun's FFI (Foreign Function Interface) with Zig or C. Use when optimizing hot paths, integrating system libraries, or requiring native performance for compute-intensive operations.
license: MIT
compatibility: Requires Bun 1.0+, Zig compiler (for Zig bindings), or C compiler (for C FFI)
metadata:
  author: langchain-fastapi-production
  version: "1.0"
---

# Bun FFI Native Binding Skill

Build native extensions for JavaScript using Bun's tight integration with Zig and C via FFI.

## When to Use

- **Hot paths**: Compute-intensive operations (crypto, compression, math)
- **System integration**: Direct OS/hardware access
- **Large data processing**: Batch operations on arrays/buffers
- **Legacy libraries**: Wrap existing C/Zig libraries

## Two Approaches

### 1. Zig Bindgen (Recommended)

Zig functions compiled directly into Bun with zero-overhead bindings.

**Setup:**
```bash
bun add -d @zig/build
```

**Zig function** (`src/math.zig`):
```zig
const std = @import("std");
const jsc = @import("jsc");

pub fn add(global: *jsc.JSGlobalObject, a: i32, b: i32) !i32 {
    return std.math.add(i32, a, b) catch {
        return global.throwPretty("Integer overflow", .{});
    };
}
```

**Binding declaration** (`src/bindings.ts`):
```ts
import { t, fn } from "bindgen";

export const add = fn({
  args: { global: t.globalObject, a: t.i32, b: t.i32 },
  ret: t.i32
});
```

**Usage** (`index.ts`):
```ts
import { add } from "bun:math";
console.log(add(2, 3)); // 5
```

### 2. C FFI (Dynamic Loading)

Load C libraries at runtime without compilation.

**C function** (`lib.c`):
```c
int add(int a, int b) {
    return a + b;
}
```

**Compile:**
```bash
gcc -shared -fPIC -o lib.so lib.c
```

**Load in Bun** (`index.ts`):
```ts
import { dlopen, FFIType } from "bun:ffi";

const lib = dlopen("./lib.so", {
  add: { args: [FFIType.i32, FFIType.i32], returns: FFIType.i32 }
});

console.log(lib.symbols.add(2, 3)); // 5
```

## Performance Considerations

### Bridge Cost
- **Overhead**: 10-100 nanoseconds per call
- **Dominates**: Tiny functions called repeatedly
- **Solution**: Batch operations

### Data Conversion
- **Overhead**: Proportional to payload size
- **Dominates**: Complex object marshaling
- **Solution**: Use typed arrays, avoid JSON

### Rule of Thumb
**If work per call > bridge cost → native wins**

## Critical Edge Cases

See [references/EDGE_CASES.md](references/EDGE_CASES.md) for:
- Exception boundaries (panics crash runtime)
- Memory ownership (who frees allocations?)
- Struct alignment (layout assumptions)
- GC interaction (pinning references)
- Thread safety (event loop constraints)
- ABI compatibility (C calling convention)

## Best Practices

1. **Minimize boundary crossings** — batch processing in native code
2. **Use typed arrays** — zero-copy buffer mapping
3. **Avoid per-call allocation** — reuse buffers
4. **Binary formats** — faster than JSON serialization
5. **Stable APIs** — version struct layouts
6. **Error handling** — convert panics to JS exceptions

## Optimization Checklist

- [ ] Minimize JS → native calls
- [ ] Avoid JSON across boundary
- [ ] Use typed arrays/buffers
- [ ] Batch processing in native
- [ ] Convert errors to JS exceptions
- [ ] No Zig panics escape to JS
- [ ] No global mutable state
- [ ] Benchmark boundary latency
- [ ] No per-call memory allocation
- [ ] Thread safety verified

## Example: Batch Array Processing

**Zig** (`src/process.zig`):
```zig
pub fn processArray(global: *jsc.JSGlobalObject, ptr: [*]u32, len: usize) !u32 {
    var sum: u32 = 0;
    for (0..len) |i| {
        sum +|= ptr[i];
    }
    return sum;
}
```

**JS** (`index.ts`):
```ts
const data = new Uint32Array([1, 2, 3, 4, 5]);
const sum = processArray(data.buffer, data.length);
```

This avoids 5 separate JS→native calls and marshals data once.

## See Also

- [Complete SDK Reference](references/COMPLETE_SDK_REFERENCE.md)
- [Zig Documentation](https://ziglang.org/documentation/)
- [Bun FFI Docs](https://bun.sh/docs/ffi)
