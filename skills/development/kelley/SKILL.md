---
name: kelley-zig-philosophy
description: Write Zig code in the style of Andrew Kelley, creator of Zig. Emphasizes simplicity, explicit behavior, compile-time metaprogramming, and being a better C. Use when writing systems code that prioritizes clarity and safety.
---

# Andrew Kelley Style Guide

## Overview

Andrew Kelley created Zig to address the shortcomings of C and C++ while maintaining their strengths. His philosophy centers on simplicity, explicitness, and leveraging compile-time computation to eliminate runtime overhead.

## Core Philosophy

> "Zig is not trying to be Rust. Zig is trying to be a better C."

> "The language should not have hidden control flow."

> "Communicate intent to the compiler and other programmers."

Kelley believes that complexity should be explicit and visible, not hidden behind abstractions that obscure what the code actually does.

## Design Principles

1. **No Hidden Control Flow**: What you see is what executes.

2. **No Hidden Allocations**: Memory operations are explicit.

3. **Compile-Time Over Runtime**: Move computation to compile time.

4. **Simplicity Over Features**: Small, orthogonal feature set.

## When Writing Code

### Always

- Use `comptime` to eliminate runtime overhead
- Make allocations explicit with allocator parameters
- Handle all error cases explicitly
- Prefer slices over pointers when possible
- Use `defer` for cleanup
- Document with `///` doc comments

### Never

- Hide control flow in operator overloads (Zig doesn't have them)
- Allocate implicitly—always pass allocators
- Ignore errors—handle or explicitly discard
- Use C-style null-terminated strings when slices work
- Rely on undefined behavior

### Prefer

- `comptime` over runtime generics
- Error unions over exceptions
- Slices over raw pointers
- `defer` over manual cleanup
- Explicit allocators over global state
- Packed structs for binary compatibility

## Code Patterns

### Compile-Time Computation

```zig
// comptime: evaluated at compile time, zero runtime cost
fn fibonacci(comptime n: u32) u32 {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// This is computed at compile time
const fib_10 = fibonacci(10);  // 55, no runtime computation

// Generic programming with comptime
fn max(comptime T: type, a: T, b: T) T {
    return if (a > b) a else b;
}

const result = max(i32, 5, 10);  // Type-safe, zero overhead


// Compile-time type reflection
fn printFields(comptime T: type) void {
    const fields = @typeInfo(T).Struct.fields;
    inline for (fields) |field| {
        @compileLog(field.name);
    }
}
```

### Error Handling

```zig
// Errors are values, not exceptions
const FileError = error{
    NotFound,
    PermissionDenied,
    Unexpected,
};

fn readFile(path: []const u8) FileError![]u8 {
    // Return error or success
    if (path.len == 0) {
        return error.NotFound;
    }
    // ... read file
    return data;
}

// Caller must handle errors explicitly
pub fn main() void {
    const data = readFile("config.txt") catch |err| {
        switch (err) {
            error.NotFound => std.debug.print("File not found\n", .{}),
            error.PermissionDenied => std.debug.print("Access denied\n", .{}),
            else => std.debug.print("Unexpected error\n", .{}),
        }
        return;
    };
    
    // Use data...
}

// try: shorthand for catch and return
fn processFile(path: []const u8) !void {
    const data = try readFile(path);  // Propagates error if any
    // Process data...
}

// errdefer: cleanup only on error
fn allocateAndProcess(allocator: Allocator) !*Resource {
    const resource = try allocator.create(Resource);
    errdefer allocator.destroy(resource);  // Only runs if error occurs
    
    try resource.init();  // If this fails, resource is freed
    return resource;
}
```

### Explicit Memory Management

```zig
const std = @import("std");
const Allocator = std.mem.Allocator;

// Always pass allocator explicitly
fn createBuffer(allocator: Allocator, size: usize) ![]u8 {
    return allocator.alloc(u8, size);
}

fn processData(allocator: Allocator, input: []const u8) ![]u8 {
    var result = try allocator.alloc(u8, input.len * 2);
    errdefer allocator.free(result);
    
    // Process...
    
    return result;
}

pub fn main() !void {
    // Choose your allocator
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    
    const allocator = gpa.allocator();
    
    const buffer = try createBuffer(allocator, 1024);
    defer allocator.free(buffer);
    
    // Use buffer...
}
```

### Defer and Cleanup

```zig
fn processFile(path: []const u8) !void {
    const file = try std.fs.cwd().openFile(path, .{});
    defer file.close();  // Always closes, even on error
    
    var buffer: [4096]u8 = undefined;
    const bytes_read = try file.read(&buffer);
    
    // Process buffer...
}

// Multiple defers execute in reverse order
fn complexOperation() !void {
    const a = try acquireResourceA();
    defer releaseResourceA(a);
    
    const b = try acquireResourceB();
    defer releaseResourceB(b);
    
    const c = try acquireResourceC();
    defer releaseResourceC(c);
    
    // On exit (success or error):
    // 1. releaseResourceC
    // 2. releaseResourceB
    // 3. releaseResourceA
}
```

### Slices Over Pointers

```zig
// Slices: pointer + length, safer than raw pointers
fn processBytes(data: []const u8) void {
    for (data) |byte| {
        // Safe iteration, bounds checked in debug
        std.debug.print("{x}", .{byte});
    }
}

// Slice operations
fn example() void {
    const array = [_]u8{ 1, 2, 3, 4, 5 };
    
    const slice = array[1..4];  // [2, 3, 4]
    const from_start = array[0..3];  // [1, 2, 3]
    const to_end = array[2..];  // [3, 4, 5]
    
    // Sentinel-terminated slices for C interop
    const c_string: [:0]const u8 = "hello";
}

// Convert between pointer types explicitly
fn pointerConversions(ptr: [*]u8, len: usize) void {
    const slice = ptr[0..len];  // Many-pointer to slice
    const single = &ptr[0];     // Many-pointer to single pointer
}
```

### Structs and Methods

```zig
const Point = struct {
    x: f32,
    y: f32,
    
    // Methods are just namespaced functions
    pub fn distance(self: Point, other: Point) f32 {
        const dx = self.x - other.x;
        const dy = self.y - other.y;
        return @sqrt(dx * dx + dy * dy);
    }
    
    pub fn zero() Point {
        return .{ .x = 0, .y = 0 };
    }
};

// Usage
const p1 = Point{ .x = 0, .y = 0 };
const p2 = Point{ .x = 3, .y = 4 };
const dist = p1.distance(p2);  // 5.0
const origin = Point.zero();
```

### Optionals and Null Safety

```zig
// Optional: T or null, explicit handling required
fn findUser(id: u32) ?User {
    if (id == 0) return null;
    return users[id];
}

pub fn main() void {
    // Must handle null case
    if (findUser(42)) |user| {
        std.debug.print("Found: {s}\n", .{user.name});
    } else {
        std.debug.print("User not found\n", .{});
    }
    
    // orelse: provide default
    const user = findUser(42) orelse User.anonymous();
    
    // .?: unwrap or undefined behavior (debug trap)
    const user = findUser(42).?;  // Crashes if null in debug
}
```

## Mental Model

Kelley approaches systems programming by asking:

1. **Can this run at compile time?** Use `comptime` to shift work
2. **Is control flow visible?** No hidden jumps or allocations
3. **Are errors handled?** Every error path must be addressed
4. **Is memory explicit?** Allocators passed, lifetimes clear
5. **Would a C programmer understand the output?** Zig maps to predictable machine code

## Signature Kelley Moves

- `comptime` for zero-cost generics
- Explicit allocator parameters everywhere
- `defer`/`errdefer` for cleanup
- Error unions instead of exceptions
- Slices instead of pointer arithmetic
- No operator overloading, no hidden behavior
