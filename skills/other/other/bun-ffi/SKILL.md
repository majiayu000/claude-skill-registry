---
name: Bun FFI
description: This skill should be used when the user asks about "bun:ffi", "foreign function interface", "calling C from Bun", "native libraries", "dlopen", "shared libraries", "calling native code", or integrating C/C++ libraries with Bun.
version: 1.0.0
---

# Bun FFI

Bun's FFI allows calling native C/C++ libraries from JavaScript.

## Quick Start

```typescript
import { dlopen, suffix, FFIType } from "bun:ffi";

// Load library
const lib = dlopen(`libc.${suffix}`, {
  printf: {
    args: [FFIType.cstring],
    returns: FFIType.int,
  },
});

// Call function
lib.symbols.printf("Hello from C!\n");
```

## Loading Libraries

### Platform-Specific Paths

```typescript
import { dlopen, suffix } from "bun:ffi";

// suffix is: "dylib" (macOS), "so" (Linux), "dll" (Windows)

// System library
const libc = dlopen(`libc.${suffix}`, { ... });

// Custom library
const myLib = dlopen(`./libmylib.${suffix}`, { ... });

// Absolute path
const sqlite = dlopen("/usr/lib/libsqlite3.so", { ... });
```

### Cross-Platform Loading

```typescript
function getLibPath(name: string): string {
  const platform = process.platform;
  const paths = {
    darwin: `/usr/local/lib/lib${name}.dylib`,
    linux: `/usr/lib/lib${name}.so`,
    win32: `C:\\Windows\\System32\\${name}.dll`,
  };
  return paths[platform] || paths.linux;
}

const lib = dlopen(getLibPath("mylib"), { ... });
```

## FFI Types

```typescript
import { FFIType } from "bun:ffi";

const types = {
  // Integers
  i8: FFIType.i8,        // int8_t
  i16: FFIType.i16,      // int16_t
  i32: FFIType.i32,      // int32_t / int
  i64: FFIType.i64,      // int64_t / long long

  // Unsigned integers
  u8: FFIType.u8,        // uint8_t
  u16: FFIType.u16,      // uint16_t
  u32: FFIType.u32,      // uint32_t
  u64: FFIType.u64,      // uint64_t

  // Floats
  f32: FFIType.f32,      // float
  f64: FFIType.f64,      // double

  // Pointers
  ptr: FFIType.ptr,      // void*
  cstring: FFIType.cstring, // const char*

  // Other
  bool: FFIType.bool,    // bool
  void: FFIType.void,    // void
};
```

## Function Definitions

```typescript
import { dlopen, FFIType, ptr, CString } from "bun:ffi";

const lib = dlopen("./libmath.so", {
  // Simple function
  add: {
    args: [FFIType.i32, FFIType.i32],
    returns: FFIType.i32,
  },

  // String function
  greet: {
    args: [FFIType.cstring],
    returns: FFIType.cstring,
  },

  // Pointer function
  allocate: {
    args: [FFIType.u64],
    returns: FFIType.ptr,
  },

  // Void function
  log_message: {
    args: [FFIType.cstring],
    returns: FFIType.void,
  },

  // No args
  get_version: {
    args: [],
    returns: FFIType.cstring,
  },
});

// Call functions
const sum = lib.symbols.add(1, 2); // 3
const message = lib.symbols.greet(ptr(Buffer.from("World\0")));
```

## Working with Strings

```typescript
import { dlopen, FFIType, ptr, CString } from "bun:ffi";

// Passing strings to C
const str = Buffer.from("Hello\0"); // Must be null-terminated
lib.symbols.print_string(ptr(str));

// Receiving strings from C
const result = lib.symbols.get_string();
const jsString = new CString(result); // Convert to JS string
console.log(jsString.toString());
```

## Working with Pointers

```typescript
import { dlopen, FFIType, ptr, toArrayBuffer } from "bun:ffi";

const lib = dlopen("./libdata.so", {
  create_buffer: {
    args: [FFIType.u64],
    returns: FFIType.ptr,
  },
  fill_buffer: {
    args: [FFIType.ptr, FFIType.u8, FFIType.u64],
    returns: FFIType.void,
  },
  free_buffer: {
    args: [FFIType.ptr],
    returns: FFIType.void,
  },
});

// Allocate buffer
const size = 1024;
const bufPtr = lib.symbols.create_buffer(size);

// Fill buffer
lib.symbols.fill_buffer(bufPtr, 0xff, size);

// Read buffer as ArrayBuffer
const arrayBuffer = toArrayBuffer(bufPtr, 0, size);
const view = new Uint8Array(arrayBuffer);
console.log(view); // [255, 255, 255, ...]

// Free buffer
lib.symbols.free_buffer(bufPtr);
```

## Structs

```typescript
import { dlopen, FFIType, ptr } from "bun:ffi";

// C struct:
// struct Point { int32_t x; int32_t y; };

const lib = dlopen("./libgeom.so", {
  create_point: {
    args: [FFIType.i32, FFIType.i32],
    returns: FFIType.ptr, // Returns Point*
  },
  get_distance: {
    args: [FFIType.ptr, FFIType.ptr],
    returns: FFIType.f64,
  },
});

// Create struct manually
const point = new ArrayBuffer(8); // 2 x int32
const view = new DataView(point);
view.setInt32(0, 10, true); // x = 10
view.setInt32(4, 20, true); // y = 20

// Pass to C
lib.symbols.get_distance(ptr(point), ptr(point));
```

## Callbacks

```typescript
import { dlopen, FFIType, callback } from "bun:ffi";

const lib = dlopen("./libsort.so", {
  sort_array: {
    args: [FFIType.ptr, FFIType.u64, FFIType.ptr], // callback
    returns: FFIType.void,
  },
});

// Create callback
const compareCallback = callback(
  {
    args: [FFIType.ptr, FFIType.ptr],
    returns: FFIType.i32,
  },
  (a, b) => {
    const aVal = new DataView(toArrayBuffer(a, 0, 4)).getInt32(0, true);
    const bVal = new DataView(toArrayBuffer(b, 0, 4)).getInt32(0, true);
    return aVal - bVal;
  }
);

// Use callback
lib.symbols.sort_array(arrayPtr, length, compareCallback.ptr);

// Close callback when done
compareCallback.close();
```

## Example: SQLite

```typescript
import { dlopen, FFIType, ptr, CString } from "bun:ffi";

const sqlite = dlopen("libsqlite3.dylib", {
  sqlite3_open: {
    args: [FFIType.cstring, FFIType.ptr],
    returns: FFIType.i32,
  },
  sqlite3_exec: {
    args: [FFIType.ptr, FFIType.cstring, FFIType.ptr, FFIType.ptr, FFIType.ptr],
    returns: FFIType.i32,
  },
  sqlite3_close: {
    args: [FFIType.ptr],
    returns: FFIType.i32,
  },
});

// Open database
const dbPtrArray = new BigInt64Array(1);
const dbPath = Buffer.from("test.db\0");
sqlite.symbols.sqlite3_open(ptr(dbPath), ptr(dbPtrArray));
const db = dbPtrArray[0];

// Execute query
const sql = Buffer.from("CREATE TABLE test (id INTEGER);\0");
sqlite.symbols.sqlite3_exec(db, ptr(sql), null, null, null);

// Close
sqlite.symbols.sqlite3_close(db);
```

## Memory Management

```typescript
// Manual allocation
const buffer = new ArrayBuffer(1024);
const pointer = ptr(buffer);

// Buffer stays valid as long as ArrayBuffer exists
// JavaScript GC will clean up ArrayBuffer

// For C-allocated memory, call C's free function
lib.symbols.free(cPointer);
```

## Thread Safety

```typescript
// FFI calls are synchronous and block the main thread
// For long-running operations, use Web Workers:

// worker.ts
import { dlopen } from "bun:ffi";
const lib = dlopen(...);

self.onmessage = (e) => {
  const result = lib.symbols.expensive_operation(e.data);
  self.postMessage(result);
};
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Library not found` | Wrong path | Check library path |
| `Symbol not found` | Wrong function name | Check function export |
| `Type mismatch` | Wrong FFI types | Match C types exactly |
| `Segmentation fault` | Memory error | Check pointer validity |

## When to Load References

Load `references/type-mappings.md` when:
- Complex type conversions
- Struct layouts
- Union types

Load `references/performance.md` when:
- Optimizing FFI calls
- Batching operations
- Memory pooling
