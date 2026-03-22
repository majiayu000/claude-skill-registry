---
name: analyze-wast
description: Analyze WebAssembly test (WAST) files to debug compilation issues and create regression tests. Use when the user asks to debug or analyze WAST test failures, investigate compilation bugs in wasmoon, or when encountering test failures in spec/*.wast files. Triggers include "analyze wast", "debug wast", "wast bug", or references to specific .wast test files.
---

# Analyze WAST

Debug WebAssembly test files by reproducing issues, analyzing compilation stages, and creating regression tests.

## Workflow

### 1. Reproduce the Issue

Run the test to observe failures:

```bash
./install.sh

./wasmoon test <wast_file_path>
```

If user provides only a filename (e.g., "elem.wast"), automatically prefix with `spec/`.

Record:
- Failed assertion line numbers
- Error messages
- Expected vs actual behavior

### 2. Analyze Compilation Stages

Use the explore command to examine IR, VCode, and machine code:

```bash
./wasmoon explore <wast_file_path> --stage ir vcode mc
```

**Available stages:**
- `ir` - Intermediate Representation (SSA form)
- `vcode` - Virtual code (platform-independent)
- `mc` - Machine code (ARM64 assembly)

**What to check:**
- IR: Verify WebAssembly instructions translate correctly
- VCode: Check instruction selection matches expected patterns
- MC: Verify generated assembly is correct

### 3. Isolate the Root Cause

Create a minimal test case:

1. Extract the failing WAST module to a standalone `.wat` file
2. Test with both JIT and interpreter:
   ```bash
   ./wasmoon test <file>.wast          # JIT mode
   ./wasmoon test --no-jit <file>.wast # Interpreter mode
   ```
3. If only JIT fails, the bug is in compilation; if both fail, it's in the executor

Locate relevant code:
- Use Glob to find implementation files (e.g., `**/*lowering*.mbt`)
- Use Grep to search for instruction handlers
- Read source code in vcode/lower/, ir/translator/, executor/

### 4. Create Regression Test

Write a MoonBit test in `testsuite/` to prevent regressions:

```moonbit
test "descriptive_test_name" {
  let source =
    #|(module
    #|  (func (export "test") (result i32)
    #|    i32.const 42
    #|  )
    #|)
  let result = compare_jit_interp(source, "test", [])
  inspect(result, content="matched")
}
```

**Key points:**
- Use `#|` for multiline WAT source
- `compare_jit_interp(source, func_name, args)` runs both JIT and interpreter
- `inspect(result, content="matched")` verifies they produce the same output
- For arguments, use `[I32(value)]`, `[I64(value)]`, `[F32(value)]`, `[F64(value)]`

**Test file naming:**
- Use descriptive names: `<feature>_test.mbt`
- Examples: `conversions_test.mbt`, `call_indirect_test.mbt`

Run the test:
```bash
moon test -p testsuite -f <test_file>.mbt
```

### 5. Debug with LLDB (if needed)

For segfaults or unexplained crashes:

```bash
lldb -- ./wasmoon test <file>.wast
(lldb) run
# After crash:
(lldb) bt  # View backtrace
```

## Command Reference

```bash
# Build and install
moon build && ./install.sh

# Run WAST test
./wasmoon test spec/<file>.wast

# View compilation stages
./wasmoon explore <file>.wat --stage ir vcode mc

# Test with interpreter
./wasmoon test --no-jit <file>.wast

# Run single MoonBit test
moon test -p testsuite -f <test>.mbt

# Debug with LLDB
lldb -- ./wasmoon test <file>.wast
```

## Presentation

Explain findings to the user, including:
- Root cause of the bug
- Which component has the issue (translator, lowering, codegen, etc.)
- Suggested fix approach
- Impact assessment