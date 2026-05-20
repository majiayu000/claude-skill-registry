---
name: zig-guide
description: |
  Zig language guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Zig files (.zig), build.zig, or when the user mentions Zig.
  Provides comptime patterns, allocator conventions, C interop guidelines,
  and testing standards specific to this project's coding standards.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: language
  language: zig
  extensions: ".zig"
---

# Zig Guide

> Applies to: Zig 0.13+, Systems Programming, CLIs, Embedded, Game Engines, C/C++ Replacement

## Core Principles

1. **Explicit Over Implicit**: No hidden control flow, no hidden allocations, no operator overloading, no implicit conversions
2. **Allocator Passing**: Every function that allocates receives an `std.mem.Allocator` as a parameter; never use a global allocator
3. **Errors Are Values**: Use error unions (`!`) with `try`, `catch`, and `errdefer`; never silently discard errors
4. **Comptime Over Runtime**: Move computation to compile time with `comptime`; use it for generics, validation, and code generation
5. **Safety With Escape Hatches**: Keep runtime safety enabled by default; disable only in measured hot paths with a justifying comment

## Guardrails

### Code Style

- Run `zig fmt` before every commit (non-negotiable)
- `camelCase` functions/variables, `PascalCase` types/structs/enums, `SCREAMING_SNAKE_CASE` module constants
- Prefer `snake_case` for file names (`my_module.zig`)
- Discard unused values explicitly: `_ = value;` (no `_` prefix naming)
- Prefer `const` over `var` everywhere; mutability requires justification
- All public declarations (`pub fn`, `pub const`) must have a doc comment (`///`)

### Memory and Allocators

- Every function that heap-allocates must accept an `std.mem.Allocator` parameter
- Always pair `alloc`/`free` with `defer` or `errdefer` at the call site
- Use `std.heap.ArenaAllocator` for batch allocations freed together
- Use `std.heap.GeneralPurposeAllocator` in debug builds (detects leaks, double-free)
- Never store an allocator in a struct unless the struct owns long-lived memory
- Prefer stack allocation (`var buf: [256]u8 = undefined;`) for small, bounded buffers
- Slices (`[]T`, `[]const T`) over raw pointers (`[*]T`) whenever possible

### Error Handling

- Return error unions (`!T`) for all fallible operations
- Use `try` to propagate; use `catch` only where you can handle or log meaningfully
- Use `errdefer` to clean up resources on error paths
- Define domain-specific error sets; avoid `anyerror` except at top-level boundaries
- Never ignore errors: `_ = fallibleFn();` is forbidden outside tests

```zig
const ConfigError = error{ FileNotFound, InvalidFormat, MissingField };

fn loadConfig(allocator: std.mem.Allocator, path: []const u8) ConfigError!Config {
    const file = std.fs.cwd().openFile(path, .{}) catch return error.FileNotFound;
    defer file.close();
    // parse and return ...
}
```

### Comptime

- Use `comptime` parameters for generics instead of runtime polymorphism
- Use `@typeInfo` and `@Type` for type introspection at compile time
- Use `@compileError` to produce clear messages for invalid type combinations
- Prefer `inline for` only when the loop count is comptime-known and small

```zig
fn max(comptime T: type, a: T, b: T) T {
    return if (a > b) a else b;
}

fn ensureUnsigned(comptime T: type) void {
    if (@typeInfo(T) != .int or @typeInfo(T).int.signedness == .signed)
        @compileError("expected unsigned integer type");
}
```

### Safety

- Keep runtime safety enabled in debug and test builds
- Validate all external inputs (file I/O, network, FFI boundaries)
- Use `std.math.add` / `std.math.mul` for checked arithmetic; sentinel slices (`[:0]const u8`) for C strings
- Avoid `@ptrCast` and `@intFromPtr` unless interfacing with C; justify each use

## Key Patterns

### Optionals

```zig
fn findUser(users: []const User, id: u64) ?*const User {
    for (users) |*user| {
        if (user.id == id) return user;
    }
    return null;
}

const user = findUser(users, 42) orelse return error.UserNotFound;

if (findUser(users, 42)) |u| {
    std.debug.print("Found: {s}\n", .{u.name});
}
```

### Defer and Errdefer

```zig
fn createConnection(allocator: std.mem.Allocator, host: []const u8) !*Connection {
    const conn = try allocator.create(Connection);
    errdefer allocator.destroy(conn); // only runs on error return

    conn.* = .{ .socket = try std.net.tcpConnectToHost(allocator, host, 8080), .allocator = allocator };
    errdefer conn.socket.close();

    try conn.performHandshake();
    return conn;
}
```

### Slices vs Arrays

```zig
const fixed: [4]u8 = .{ 1, 2, 3, 4 };          // fixed-size array (stack)
const c_str: [:0]const u8 = "hello";             // sentinel-terminated (C compat)

fn sum(values: []const u32) u64 {                // slice (preferred for params)
    var total: u64 = 0;
    for (values) |v| total += v;
    return total;
}
```

### Packed and Extern Structs

```zig
const StatusRegister = packed struct {
    carry: u1, zero: u1, irq_disable: u1, decimal: u1,
    brk: u1, _reserved: u1, overflow: u1, negative: u1,
};
const CFileHeader = extern struct { magic: u32, version: u16, flags: u16, size: u64 };
```

## Testing

```zig
const testing = @import("std").testing;

test "add returns correct sum" {
    try testing.expectEqual(@as(i32, 5), add(2, 3));
}

test "string list detects leaks via testing allocator" {
    var list = StringList.init(testing.allocator); // leak detection built-in
    defer list.deinit();
    try list.add("hello");
    try testing.expectEqual(@as(usize, 1), list.items.items.len);
}

test "readFileContents returns error for missing file" {
    try testing.expectError(error.FileNotFound, readFileContents(testing.allocator, "/nonexistent"));
}
```

### Testing Standards

- Test names describe behavior: `test "user creation fails with empty name"`
- Unit tests live in `test` blocks inside the same `.zig` file
- Integration tests go in `tests/` directory
- Use `std.testing.allocator` -- it detects memory leaks automatically
- Key assertions: `expectEqual`, `expectError`, `expectEqualStrings`, `expectEqualSlices`
- Coverage target: >80% for library code, >60% for application code

## Tooling

```bash
zig build              # Build (uses build.zig)
zig build test         # Run all tests
zig build run          # Build and run
zig fmt src/           # Format all source files
zig test src/main.zig  # Test a single file
zig build -Doptimize=ReleaseSafe   # Optimized with safety
zig build -Doptimize=ReleaseFast   # Maximum performance
```

See patterns.md for a build.zig template.

## C Interop

- Use `@cImport` / `@cInclude` for C headers (not manual extern declarations)
- Use `[*c]T` only at FFI boundary; convert to `[]T` or `?*T` immediately
- Use `std.mem.span` to convert `[*:0]const u8` (C string) to Zig slice
- Always call `exe.linkLibC()` in build.zig when using libc
- Validate all values received from C before using in safe Zig code

## References

For full implementation examples, see:

- [references/patterns.md](references/patterns.md) -- Arena allocator, GPA leak detection, comptime generics, comptime interface validation, C library wrapper (SQLite), sentinel string conversion, tagged union state machines, errdefer chains, build.zig template

## External References

- [Zig Language Reference](https://ziglang.org/documentation/master/)
- [Zig Standard Library Docs](https://ziglang.org/documentation/master/std/)
- [Zig Learn](https://ziglearn.org/)
- [Zig by Example](https://zig-by-example.github.io/)
- [Zig Cookbook](https://cookbook.ziglang.cc/)
