---
name: zig-project
description: Modern Zig project architecture guide. Use when creating Zig projects (systems programming, CLI tools, game dev, high-performance services). Covers explicit allocators, comptime, error handling, and build system.
---
# Zig Project Architecture

## Core Principles

- **No hidden behavior** — No hidden allocations, no hidden control flow, no macros
- **Explicit allocators** — Pass allocator as parameter, never use global allocator
- **Comptime over macros** — Use comptime for generics and metaprogramming
- **Error unions** — Use `!T` for explicit error handling, avoid `anyerror`
- **defer/errdefer** — Resource cleanup at scope exit
- **No backwards compatibility** — Delete, don't deprecate. Change directly
- **LiteLLM for LLM APIs** — Use LiteLLM proxy for all LLM integrations

---

## No Backwards Compatibility

> **Delete unused code. Change directly. No compatibility layers.**

```zig
// ❌ BAD: Deprecated function kept around
/// Deprecated: Use newFunction instead
pub fn oldFunction() void {
    @compileLog("oldFunction is deprecated");
    newFunction();
}

// ❌ BAD: Alias for renamed functions
pub const old_name = new_name; // "for backwards compatibility"

// ❌ BAD: Unused parameters
fn process(_: *const Config, data: []const u8) !void {
    _ = data;
}

// ✅ GOOD: Just delete and update all usages
pub fn newFunction() void {
    // ...
}

// ✅ GOOD: Remove unused parameters entirely
fn process(data: []const u8) !void {
    // ...
}
```

---

## LiteLLM for LLM APIs

> **Use LiteLLM proxy. Don't call provider APIs directly.**

```zig
const std = @import("std");
const http = std.http;

pub const LLMClient = struct {
    allocator: std.mem.Allocator,
    base_url: []const u8,
    api_key: []const u8,

    pub fn init(allocator: std.mem.Allocator, base_url: []const u8, api_key: []const u8) LLMClient {
        return .{
            .allocator = allocator,
            .base_url = base_url,  // "http://localhost:4000"
            .api_key = api_key,
        };
    }

    pub fn complete(self: *LLMClient, prompt: []const u8, model: []const u8) ![]u8 {
        // Use OpenAI-compatible API through LiteLLM proxy
        var client = http.Client{ .allocator = self.allocator };
        defer client.deinit();

        // Build request to LiteLLM proxy...
        _ = prompt;
        _ = model;
        return "";
    }
};
```

---

## Quick Start

### 1. Initialize Project

```bash
# Create new project
mkdir myapp && cd myapp
zig init

# Or create executable project
zig init-exe

# Or create library project
zig init-lib
```

### 2. Project Structure

```
myapp/
├── build.zig           # Build configuration (in Zig)
├── build.zig.zon       # Package manifest (dependencies)
├── src/
│   ├── main.zig        # Entry point (for exe)
│   ├── root.zig        # Library root (for lib)
│   └── lib/            # Internal modules
│       └── utils.zig
├── tests/              # Integration tests (optional)
└── lib/                # Vendored dependencies
```

### 3. Core Files

**build.zig.zon** (Package Manifest)
```zig
.{
    .name = "myapp",
    .version = "0.1.0",
    .dependencies = .{
        // .some_dep = .{
        //     .url = "https://github.com/...",
        //     .hash = "...",
        // },
    },
    .paths = .{
        "build.zig",
        "build.zig.zon",
        "src",
    },
}
```

**build.zig** (Build Script)
```zig
const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    const exe = b.addExecutable(.{
        .name = "myapp",
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });

    b.installArtifact(exe);

    // Run step
    const run_cmd = b.addRunArtifact(exe);
    run_cmd.step.dependOn(b.getInstallStep());
    const run_step = b.step("run", "Run the application");
    run_step.dependOn(&run_cmd.step);

    // Test step
    const unit_tests = b.addTest(.{
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });
    const run_unit_tests = b.addRunArtifact(unit_tests);
    const test_step = b.step("test", "Run unit tests");
    test_step.dependOn(&run_unit_tests.step);
}
```

---

## Explicit Allocator Pattern

### Core Principle

Every function that allocates must receive an allocator parameter.

```zig
const std = @import("std");

// ❌ BAD: Hidden allocation (don't do this)
var global_allocator: std.mem.Allocator = undefined;
fn badAlloc() ![]u8 {
    return global_allocator.alloc(u8, 100);
}

// ✅ GOOD: Explicit allocator
fn goodAlloc(allocator: std.mem.Allocator) ![]u8 {
    return allocator.alloc(u8, 100);
}
```

### Common Allocators

```zig
const std = @import("std");

pub fn main() !void {
    // General purpose (with safety checks in debug)
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    // Arena (bulk alloc/dealloc)
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const arena_alloc = arena.allocator();

    // Fixed buffer (no heap)
    var buffer: [1024]u8 = undefined;
    var fba = std.heap.FixedBufferAllocator.init(&buffer);
    const fixed_alloc = fba.allocator();

    // Page allocator (direct OS calls)
    const page_alloc = std.heap.page_allocator;

    _ = allocator;
    _ = arena_alloc;
    _ = fixed_alloc;
    _ = page_alloc;
}
```

### Arena Pattern (Request-Scoped)

```zig
fn handleRequest(permanent_allocator: std.mem.Allocator) !void {
    // Create arena for this request
    var arena = std.heap.ArenaAllocator.init(permanent_allocator);
    defer arena.deinit();  // Free ALL request memory at once

    const allocator = arena.allocator();

    // All allocations use arena - no individual frees needed
    const data = try fetchData(allocator);
    const processed = try processData(allocator, data);
    try sendResponse(processed);

    // arena.deinit() frees everything
}
```

---

## Error Handling

### Error Unions

```zig
const std = @import("std");

// Define specific error set
const FileError = error{
    NotFound,
    AccessDenied,
    OutOfMemory,
    EndOfStream,
};

// Return error union
fn readFile(allocator: std.mem.Allocator, path: []const u8) FileError![]u8 {
    const file = std.fs.cwd().openFile(path, .{}) catch |err| {
        return switch (err) {
            error.FileNotFound => FileError.NotFound,
            error.AccessDenied => FileError.AccessDenied,
            else => FileError.NotFound,
        };
    };
    defer file.close();

    return file.readToEndAlloc(allocator, 1024 * 1024) catch FileError.OutOfMemory;
}
```

### try / catch / errdefer

```zig
fn processFile(allocator: std.mem.Allocator, path: []const u8) !void {
    // try: propagate error up
    const data = try readFile(allocator, path);
    errdefer allocator.free(data);  // cleanup on error

    // catch: handle error locally
    const parsed = parseData(data) catch |err| {
        std.log.err("Parse failed: {}", .{err});
        return err;
    };

    try saveResult(parsed);
}
```

### Error Formatting

```zig
fn example() !void {
    doSomething() catch |err| {
        std.log.err("Operation failed: {s}", .{@errorName(err)});
        return err;
    };
}
```

---

## Comptime (Compile-Time Execution)

### Generic Functions

```zig
fn max(comptime T: type, a: T, b: T) T {
    return if (a > b) a else b;
}

// Usage
const result = max(i32, 10, 20);  // Returns 20
const float_result = max(f64, 1.5, 2.5);  // Returns 2.5
```

### Generic Data Structures

```zig
pub fn ArrayList(comptime T: type) type {
    return struct {
        const Self = @This();

        items: []T,
        capacity: usize,
        allocator: std.mem.Allocator,

        pub fn init(allocator: std.mem.Allocator) Self {
            return .{
                .items = &[_]T{},
                .capacity = 0,
                .allocator = allocator,
            };
        }

        pub fn deinit(self: *Self) void {
            if (self.capacity > 0) {
                self.allocator.free(self.items.ptr[0..self.capacity]);
            }
        }

        pub fn append(self: *Self, item: T) !void {
            // Implementation...
            _ = item;
        }
    };
}

// Usage
var list = ArrayList(u32).init(allocator);
defer list.deinit();
```

### Compile-Time Validation

```zig
fn validateConfig(comptime config: Config) void {
    if (config.buffer_size == 0) {
        @compileError("buffer_size must be > 0");
    }
    if (config.buffer_size > 1024 * 1024) {
        @compileError("buffer_size too large");
    }
}
```

---

## Testing

### Inline Tests

```zig
const std = @import("std");
const testing = std.testing;

fn add(a: i32, b: i32) i32 {
    return a + b;
}

test "add positive numbers" {
    try testing.expectEqual(@as(i32, 5), add(2, 3));
}

test "add negative numbers" {
    try testing.expectEqual(@as(i32, -1), add(1, -2));
}
```

### Testing with Allocator

```zig
test "allocation test" {
    // Use testing allocator for leak detection
    const allocator = testing.allocator;

    const data = try allocator.alloc(u8, 100);
    defer allocator.free(data);

    try testing.expect(data.len == 100);
}
```

### Testing Errors

```zig
test "expect error" {
    const result = failingFunction();
    try testing.expectError(error.SomeError, result);
}

test "expect no error" {
    const result = try successFunction();
    try testing.expect(result > 0);
}
```

### Run Tests

```bash
# Run all tests
zig build test

# Run tests with output
zig test src/main.zig

# Run specific test
zig test src/main.zig --test-filter "add positive"
```

---

## Common Commands

```bash
# Build
zig build                    # Debug build
zig build -Doptimize=ReleaseFast  # Release build

# Run
zig build run               # Build and run

# Test
zig build test              # Run tests

# Format
zig fmt src/                # Format code

# Cross-compile
zig build -Dtarget=x86_64-linux-gnu
zig build -Dtarget=aarch64-macos
zig build -Dtarget=x86_64-windows

# Use as C compiler
zig cc -o output input.c
zig c++ -o output input.cpp
```

---


## Extended Reference

Detailed material starting at `## Checklist` has been moved to [`reference/extended.md`](reference/extended.md) to keep this skill concise. Load that reference when the task requires the moved examples, command catalogs, checklists, platform details, or implementation templates.
