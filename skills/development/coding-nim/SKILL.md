---
name: coding-nim
cluster: coding
description: "Nim 2.x: macros, templates, compile-time, memory ARC/ORC, FFI, Nimble, systems programming"
tags: ["nim","systems","coding"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "nim macro template compile-time memory nimble arc orc ffi"
---

# coding-nim

## Purpose
This skill equips the AI to handle Nim 2.x programming tasks, focusing on advanced features like macros, templates, compile-time execution, memory management (ARC/ORC), FFI for interoperability, Nimble for package handling, and systems programming. Use it to generate, debug, and optimize Nim code efficiently.

## When to Use
Apply this skill for systems-level programming needing low-level control, such as embedded systems, performance-critical apps, or when integrating with C/C++ via FFI. Use it for projects requiring compile-time metaprogramming (e.g., via macros) or automatic memory management with ARC/ORC to avoid manual garbage collection.

## Key Capabilities
- Macros for code generation: Define reusable code transformations at compile-time.
- Templates for type-safe string-based metaprogramming.
- Compile-time execution: Run code during compilation using `static` blocks.
- Memory management: Switch between ARC (automatic reference counting) and ORC (optional reference counting) via compiler flags.
- FFI: Call external libraries (e.g., C functions) without wrappers.
- Nimble: Manage dependencies and build projects like a package manager.
- Systems programming: Direct hardware access, concurrency, and cross-platform compilation.

## Usage Patterns
To accomplish tasks, structure Nim code with modules and use the compiler for builds. For macros, define them in a separate proc and invoke at compile-time. When writing FFI code, use the `importc` pragma for C functions. For memory management, specify `--gc:arc` or `--gc:orc` flags during compilation. Always test code with `nim check` before full builds to catch errors early. Integrate templates for generic functions to reduce boilerplate.

## Common Commands/API
Use the Nim compiler (`nim`) for core operations. Compile a file: `nim c --verbosity:0 -r main.nim` (flags: `-r` for run, `--verbosity:0` for minimal output). For Nimble, install packages: `nimble install somepkg`. Define a macro:  
```nim
macro doubleIt(x: expr): stmt =  
  result = quote do: `x` * 2
```
Call it as `echo doubleIt(5)`. For FFI, import C: `proc printf(format: cstring; args: varargs[pointer]) {.importc: "printf", header: "<stdio.h>".}`. Config format: Use `nim.cfg` for settings, e.g., `gcc.exe = "gcc"` to specify compiler. Environment variables: Set `$NIMBLE_DIR` for package cache.

## Integration Notes
Integrate Nim with other languages via FFI; for C++, use `importcpp`. To embed in a project, compile Nim code to a shared library: `nim c --app:lib -d:release mylib.nim`. For CI/CD, use GitHub Actions with: `run: nim c --opt:speed file.nim`. If auth is needed (e.g., for Nimble registry), set env vars like `$NIMBLE_TOKEN` for private repos. Link against external libs: Add `--passL:-lssl` for OpenSSL. Ensure path configurations match, e.g., add `path = "/path/to/headers"` in `nim.cfg`.

## Error Handling
In Nim, use try-except blocks for runtime errors:  
```nim
try:  
  raise newException(ValueError, "Invalid input")  
except ValueError:  
  echo "Handled error: ", getCurrentExceptionMsg()
```
For compile-time errors, enable detailed output with `nim c --verbosity:2 file.nim`. Check for memory issues by switching to ORC: `nim c --gc:orc file.nim`. Parse compiler output for specifics; common flags include `--warnings:on` to catch undeclared vars. Log errors with `echo` or a logging library like `chronicles`.

## Concrete Usage Examples
1. **Define and use a macro for code generation**: To create a loop macro, write:  
```nim
macro forEach(items: seq, body: stmt): stmt =  
  result = quote do: for item in `items`: `body`
```
Use it as: `forEach(@[1, 2, 3], echo item)`. This generates efficient loops at compile-time.
   
2. **Use FFI to call a C function**: Import and call a C printf:  
```nim
proc cPrintf(format: cstring) {.importc: "printf", header: "<stdio.h>".}  
cPrintf("%s\n", "Hello from Nim")
```
Compile with `nim c --passC:-I/usr/include file.nim` to link C headers, enabling seamless integration.

## Graph Relationships
- Related to cluster: coding
- Connected via tags: nim (direct link to language-specific skills), systems (links to low-level programming tools), coding (broad connections to other coding skills like coding-python or coding-c)
