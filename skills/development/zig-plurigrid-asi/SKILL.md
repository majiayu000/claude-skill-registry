---
name: zig
description: "zig skill"
version: 1.0.0
---


# zig

Zig ecosystem for systems programming without hidden control flow.

## Atomic Skills

| Skill | Commands | Domain |
|-------|----------|--------|
| zig build | build system | Compile, link, cross-compile |
| zig test | testing | Run test blocks |
| zig fmt | formatter | Canonical formatting |
| zls | LSP | Autocomplete, diagnostics |

## Quick Start

```bash
# New project
mkdir myproject && cd myproject
zig init

# Build and run
zig build run

# Test
zig build test

# Format
zig fmt src/

# Cross-compile to WASM
zig build -Dtarget=wasm32-freestanding
```

## build.zig (0.15.2)

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

    const run_cmd = b.addRunArtifact(exe);
    run_cmd.step.dependOn(b.getInstallStep());

    const run_step = b.step("run", "Run the application");
    run_step.dependOn(&run_cmd.step);

    const tests = b.addTest(.{
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });

    const test_step = b.step("test", "Run unit tests");
    test_step.dependOn(&b.addRunArtifact(tests).step);
}
```

## Core Patterns

### Explicit Allocators

```zig
const std = @import("std");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    var list = std.ArrayList(u8).init(allocator);
    defer list.deinit();

    try list.appendSlice("hello");
}
```

### Error Handling

```zig
fn readFile(path: []const u8) ![]u8 {
    const file = try std.fs.cwd().openFile(path, .{});
    defer file.close();
    return file.readToEndAlloc(allocator, 1024 * 1024);
}

// Usage with catch
const data = readFile("config.txt") catch |err| {
    std.log.err("Failed: {}", .{err});
    return err;
};
```

### Comptime Metaprogramming

```zig
fn Vec(comptime T: type, comptime N: usize) type {
    return struct {
        data: [N]T,

        const Self = @This();

        pub fn dot(self: Self, other: Self) T {
            var sum: T = 0;
            inline for (0..N) |i| {
                sum += self.data[i] * other.data[i];
            }
            return sum;
        }
    };
}

const Vec3 = Vec(f32, 3);
```

### Defer/Errdefer

```zig
fn process() !void {
    const resource = try acquire();
    defer release(resource);  // Always runs

    const temp = try allocate();
    errdefer free(temp);  // Only on error

    try doWork(resource, temp);
    // temp ownership transferred, no errdefer needed
}
```

### C Interop

```zig
const c = @cImport({
    @cInclude("stdio.h");
    @cInclude("mylib.h");
});

pub fn main() void {
    _ = c.printf("Hello from C\n");
}
```

## Version Detection

```zig
// Feature detection over version checks
const has_new_api = @hasDecl(std, "Build");
const T = if (has_new_api) std.Build else std.build.Builder;
```

## Debug

```zig
std.debug.print("value: {any}\n", .{x});
std.log.info("structured: {}", .{data});
@breakpoint();  // Debugger trap
```

## Cross-Compile Targets

```bash
# List all targets
zig targets | jq '.native'

# Common targets
zig build -Dtarget=x86_64-linux-gnu
zig build -Dtarget=aarch64-macos
zig build -Dtarget=wasm32-wasi
zig build -Dtarget=thumb-none-eabi  # Embedded
```

## Related Skills

| Skill | Trit | Role |
|-------|------|------|
| zig-programming | -1 | 223 recipes, full docs |
| zls-integration | 0 | LSP features |
| **zig** | -1 | Ecosystem wrapper |

## GF(3) Triads

```
zig(-1) ⊗ zls-integration(0) ⊗ c-interop(+1) = 0 ✓
zig(-1) ⊗ acsets(0) ⊗ gay-mcp(+1) = 0 ✓  [Schema coloring]
zig(-1) ⊗ babashka(0) ⊗ duckdb-ies(+1) = 0 ✓  [Build analytics]
```

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule:

```
Trit: -1 (MINUS/Validator)
Home: Prof
Poly Op: ⊗
Kan Role: Ran (right Kan extension)
Color: #3B82F6 (blue)
```

### Why -1 (MINUS)?

Zig validates and constrains:
- No hidden allocations
- No hidden control flow
- No exceptions
- Explicit error handling
- Compile-time safety checks

The language itself is a **validator** — it refuses to compile unsafe patterns.

## Philosophy

> "Zig is not designed to make fancy high-level things.
> It's designed to make it easy to write correct low-level code."

- Explicit over implicit
- Compile-time over runtime
- No hidden control flow
- Allocator-aware by design
- C interop without FFI overhead