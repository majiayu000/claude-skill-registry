---
name: ffi-bindings
description: Create FFI bindings between Lean 4 and C code. Use when working with foreign functions, native libraries, Metal, or system APIs.
---

# FFI Bindings

Create Foreign Function Interface bindings between Lean 4 and C.

## Quick Start

1. Define opaque types for native handles
2. Declare extern functions in Lean
3. Implement C functions with proper memory management
4. Register external classes for garbage collection
5. Update build.sh for compilation

## Lean Side: Opaque Types

```lean
-- Define an opaque type backed by a native pointer
opaque WindowPointed : NonemptyType
def Window : Type := WindowPointed.type

instance : Nonempty Window := WindowPointed.property
```

## Lean Side: Extern Functions

```lean
-- Simple function
@[extern "lean_window_create"]
opaque Window.create : UInt32 → UInt32 → String → IO Window

-- Function returning a value
@[extern "lean_window_get_size"]
opaque Window.getSize : Window → IO (UInt32 × UInt32)

-- Function with no return value
@[extern "lean_window_close"]
opaque Window.close : Window → IO Unit

-- Pure function (no IO)
@[extern "lean_add_vectors"]
opaque Vec3.add : Vec3 → Vec3 → Vec3
```

## C Side: External Class Registration

```c
#include <lean/lean.h>

// Global class pointer (initialized once)
static lean_external_class* g_window_class = NULL;

// Destructor called when Lean GC collects the object
static void window_finalizer(void* ptr) {
    Window* window = (Window*)ptr;
    window_destroy(window);
}

// Initialize the class (call once at startup)
static void ensure_class_initialized() {
    if (g_window_class == NULL) {
        g_window_class = lean_register_external_class(
            window_finalizer,  // destructor
            NULL               // foreach (for nested lean objects)
        );
    }
}
```

## C Side: Creating Objects

```c
LEAN_EXPORT lean_obj_res lean_window_create(
    uint32_t width,
    uint32_t height,
    lean_obj_arg title_obj,
    lean_obj_arg world
) {
    ensure_class_initialized();

    // Extract string from Lean
    const char* title = lean_string_cstr(title_obj);

    // Create native object
    Window* window = window_new(width, height, title);

    // Wrap in Lean external object
    lean_object* result = lean_alloc_external(g_window_class, window);

    return lean_io_result_mk_ok(result);
}
```

## C Side: Extracting Native Pointers

```c
LEAN_EXPORT lean_obj_res lean_window_close(
    lean_obj_arg window_obj,
    lean_obj_arg world
) {
    // Extract native pointer
    Window* window = (Window*)lean_get_external_data(window_obj);

    window_close(window);

    return lean_io_result_mk_ok(lean_box(0));
}
```

## C Side: Returning Tuples

```c
LEAN_EXPORT lean_obj_res lean_window_get_size(
    lean_obj_arg window_obj,
    lean_obj_arg world
) {
    Window* window = (Window*)lean_get_external_data(window_obj);

    uint32_t w = window_get_width(window);
    uint32_t h = window_get_height(window);

    // Create tuple (UInt32 × UInt32)
    lean_object* pair = lean_alloc_ctor(0, 2, 0);
    lean_ctor_set(pair, 0, lean_box_uint32(w));
    lean_ctor_set(pair, 1, lean_box_uint32(h));

    return lean_io_result_mk_ok(pair);
}
```

## C Side: Working with Floats

```c
// Box a float for return
lean_object* boxed = lean_box_float(value);

// Unbox a float from argument
double value = lean_unbox_float(float_obj);

// Return Float × Float tuple
lean_object* pair = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(pair, 0, lean_box_float(x));
lean_ctor_set(pair, 1, lean_box_float(y));
```

## C Side: Working with Arrays

```c
// Create a Lean array
lean_object* arr = lean_mk_empty_array();
for (int i = 0; i < count; i++) {
    arr = lean_array_push(arr, lean_box_uint32(values[i]));
}

// Read from Lean array
size_t len = lean_array_size(arr);
for (size_t i = 0; i < len; i++) {
    lean_object* elem = lean_array_get_core(arr, i);
    uint32_t val = lean_unbox_uint32(elem);
}
```

## build.sh Template

```bash
#!/bin/bash
set -e

# Set compiler for FFI
export LEAN_CC=/usr/bin/clang

# For macOS frameworks
export LIBRARY_PATH="/opt/homebrew/lib:$LIBRARY_PATH"

# Build with Lake
lake build

# Or for Metal projects on macOS
# clang -c -o ffi.o ffi.c $(pkg-config --cflags lean4)
# clang -shared -o libffi.dylib ffi.o -framework Metal -framework Foundation
```

## Common Patterns

### Optional Values

```c
// Return none
return lean_io_result_mk_ok(lean_mk_option_none());

// Return some value
return lean_io_result_mk_ok(lean_mk_option_some(value));
```

### Error Handling

```c
// Return IO error
if (error) {
    lean_object* err = lean_mk_io_user_error(
        lean_mk_string("Error message")
    );
    return lean_io_result_mk_error(err);
}
```

## Projects Using FFI

Reference implementations:
- `graphics/afferent` - Metal GPU rendering
- `graphics/terminus` - Terminal I/O
- `data/quarry` - SQLite bindings
- `audio/fugue` - AudioToolbox
- `network/legate` - gRPC
