---
name: Builtin Developer
description: Guides development of AILANG builtin functions. Use when user wants to add a builtin function, register new builtins, or understand the builtin system. Reduces development time from 7.5h to 2.5h (-67%).
---

# Builtin Developer

Add new builtin functions to AILANG using the modern registry system (M-DX1).

## Quick Start

**Development time: ~2.5 hours** (down from 7.5h with legacy system)

**Most common workflow:**
1. Register builtin with metadata (~30 min)
2. Write hermetic tests (~1 hour)
3. Validate and inspect (~30 min)
4. Runtime auto-wires (already done!)

## When to Use This Skill

Invoke this skill when:
- User wants to add a new builtin function
- User asks about builtin registration process
- User needs to understand the builtin system
- User wants to validate or inspect builtins
- User asks "how do I add a builtin?"

## System Overview

**Status**: 🎉 **M-DX1 COMPLETE (Oct 2025)** - 52 builtins migrated, fully documented

**Key Benefits:**
- **67% faster**: 2.5h instead of 7.5h
- **1 file instead of 4**: Single-point registration
- **71% less code**: Type Builder DSL reduces boilerplate
- **Automatic wiring**: Registry connects to runtime/link
- **Hermetic tests**: MockEffContext with HTTP/FS mocking

**Components:**
- **Central Registry** (`internal/builtins/spec.go`) - Single registration point
- **Type Builder DSL** (`internal/types/builder.go`) - Fluent type construction
- **Test Harness** (`internal/effects/testctx/`) - Hermetic testing helpers
- **CLI Commands** - Validation and inspection tools

## Available Scripts

### `scripts/validate_builtins.sh`
Validate all builtins in the registry.

**Usage:**
```bash
.claude/skills/builtin-developer/scripts/validate_builtins.sh
```

**What it checks:**
- All builtins are registered
- Proper metadata structure
- Type signatures valid
- Test coverage exists

### `scripts/check_builtin_health.sh`
Run ailang doctor and list commands.

**Usage:**
```bash
.claude/skills/builtin-developer/scripts/check_builtin_health.sh
```

## Workflow

### Step 1: Register the Builtin (~30 min)

**Create or edit module file** (e.g., `internal/builtins/string.go`):

```go
// internal/builtins/string.go
func init() {
    registerMyBuiltin()
}

func registerMyBuiltin() {
    RegisterEffectBuiltin(BuiltinSpec{
        Module:  "std/string",
        Name:    "_str_reverse",
        NumArgs: 1,
        IsPure:  true,        // or false with Effect: "IO"
        Type:    makeReverseType,
        Impl:    strReverseImpl,
        Metadata: &BuiltinMetadata{
            Description: "Reverse a string (Unicode-aware)",
            Params: []ParamDoc{
                {Name: "s", Description: "String to reverse"},
            },
            Returns: "Reversed string",
            Examples: []Example{
                {Code: `_str_reverse("hello")`, Description: "Returns \"olleh\""},
            },
            Since:     "v0.3.15",
            Stability: StabilityStable,
            Tags:      []string{"string", "reverse", "unicode"},
            Category:  "string",
        },
    })
}

func makeReverseType() types.Type {
    T := types.NewBuilder()
    return T.Func(T.String()).Returns(T.String())
}

func strReverseImpl(ctx *effects.EffContext, args []eval.Value) (eval.Value, error) {
    str := args[0].(*eval.StringValue).Value
    runes := []rune(str)
    for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
        runes[i], runes[j] = runes[j], runes[i]
    }
    return &eval.StringValue{Value: string(runes)}, nil
}
```

**Key points:**
- Use `RegisterEffectBuiltin()` in `init()`
- Use Type Builder DSL for type construction
- Include complete metadata (description, params, examples, tags)
- Set `IsPure: true` for pure functions, or `Effect: "IO"` for effects

**See:** [resources/type_builder_examples.md](resources/type_builder_examples.md) for type patterns

### Step 2: Write Hermetic Tests (~1 hour)

**Add tests in** `internal/builtins/register_test.go`:

```go
func TestStrReverse(t *testing.T) {
    ctx := testctx.NewMockEffContext()

    tests := []struct {
        input    string
        expected string
    }{
        {"hello", "olleh"},
        {"", ""},
        {"🎉", "🎉"},
    }

    for _, tt := range tests {
        result, err := strReverseImpl(ctx, []eval.Value{
            testctx.MakeString(tt.input),
        })
        assert.NoError(t, err)
        assert.Equal(t, tt.expected, testctx.GetString(result))
    }
}
```

**Test Harness helpers:**
- `testctx.NewMockEffContext()` - Create test context
- `testctx.MakeString()`, `MakeInt()`, `MakeRecord()` - Create test values
- `testctx.GetString()`, `GetInt()`, `GetRecord()` - Extract values

**For HTTP/FS effects:**
```go
ctx := testctx.NewMockEffContext()
ctx.GrantAll("Net")  // Grant Net capability
ctx.SetHTTPClient(server.Client())  // Use test server
```

**See:** [resources/testing_patterns.md](resources/testing_patterns.md) for more examples

### Step 3: Validate and Inspect (~30 min)

**Run validation:**
```bash
# Validate all builtins
ailang doctor builtins

# List all builtins by module
ailang builtins list --by-module

# Check for orphaned builtins (migration safety)
ailang builtins check-migration
```

**Run tests:**
```bash
# Test specific builtin
go test -v internal/builtins -run TestStrReverse

# Test all builtins
make test
```

**Test in REPL:**
```bash
ailang repl
> :type _str_reverse
string -> string

> _str_reverse("hello")
"olleh" : string
```

### Step 4: Runtime Wiring (Automatic!)

No manual wiring needed! The registry automatically:
- ✅ Registers with evaluator (`internal/eval`)
- ✅ Adds to type environment (`internal/types`)
- ✅ Links to runtime (`internal/runtime`)
- ✅ Generates module interface (`internal/link`)

**Feature flag removed in v0.3.10** - New registry is now the default.

## Key Components

### Central Registry

**Location:** `internal/builtins/spec.go`

**Features:**
- Single registration point with `RegisterEffectBuiltin()`
- Compile-time validation (arity, types, impl, effects)
- Freeze-safe (no registration after init)
- 52 builtins migrated

### Type Builder DSL

**Location:** `internal/types/builder.go`

**Reduces type construction from 35 lines → 10 lines (-71%)**

**Available methods:**
```go
T := types.NewBuilder()

// Primitive types
T.String()
T.Int()
T.Float()
T.Bool()
T.Unit()

// Complex types
T.List(elementType)
T.Record(fields...)
T.Tuple(types...)
T.Con("TypeName")
T.Var("α")

// Function types
T.Func(arg1, arg2, ...).Returns(returnType).Effects("IO", "FS")

// Type applications
T.App("Result", okType, errType)
```

**See:** [resources/type_builder_examples.md](resources/type_builder_examples.md)

### Test Harness

**Location:** `internal/effects/testctx/`

**Value constructors:**
- `MakeString(s string)` → StringValue
- `MakeInt(i int)` → IntValue
- `MakeFloat(f float64)` → FloatValue
- `MakeBool(b bool)` → BoolValue
- `MakeList([]Value)` → ListValue
- `MakeRecord(map[string]Value)` → RecordValue

**Value extractors:**
- `GetString(Value)` → string
- `GetInt(Value)` → int
- `GetFloat(Value)` → float64
- `GetBool(Value)` → bool
- `GetList(Value)` → []Value
- `GetRecord(Value)` → map[string]Value

**Effect mocking:**
- `ctx.GrantAll(effect)` - Grant capabilities
- `ctx.SetHTTPClient(client)` - Mock HTTP
- `ctx.SetFS(fs)` - Mock filesystem

### Validation & Inspection

**Commands:**
```bash
ailang doctor builtins              # Health checks
ailang builtins list                # List all builtins
ailang builtins list --by-module    # Group by module
ailang builtins list --by-effect    # Group by effect
ailang builtins check-migration     # Check for orphaned builtins
```

**6 validation rules:**
1. Type function exists and valid
2. Implementation function exists
3. Arity matches NumArgs
4. Effect consistency (IsPure vs Effect field)
5. Module name valid
6. Metadata complete

## Metrics

**Development time:**
| Task | Before | After | Savings |
|------|--------|-------|---------|
| Files to edit | 4 | 1 | -75% |
| Type construction | 35 LOC | 10 LOC | -71% |
| Total time | 7.5h | 2.5h | -67% |
| Test setup | ~50 LOC | ~15 LOC | -70% |

## Resources

### Detailed Examples

**For type patterns:**
- [resources/type_builder_examples.md](resources/type_builder_examples.md) - All type patterns

**For testing patterns:**
- [resources/testing_patterns.md](resources/testing_patterns.md) - Hermetic test examples

**For comprehensive guide:**
- [M-DX1-FINAL-SUMMARY.md](../../../M-DX1-FINAL-SUMMARY.md) - Complete M-DX1 summary
- `design_docs/planned/easier-ailang-dev.md` - Design rationale
- `CHANGELOG.md` (v0.3.10+) - Version history

### File Locations

**Builtin files by module:**
- `internal/builtins/string.go` - String functions (9 builtins)
- `internal/builtins/math.go` - Math functions (37 builtins)
- `internal/builtins/io.go` - IO functions (3 builtins)
- `internal/builtins/net.go` - Network functions (1 builtin)
- `internal/builtins/show.go` - Show typeclass (1 builtin)
- `internal/builtins/json_decode.go` - JSON decoding (1 builtin)

**Test files:**
- `internal/builtins/*_test.go` - Builtin tests
- `internal/effects/testctx/*_test.go` - Test harness tests

## Common Patterns

### Pattern 0: "Zero-Arg" Builtins (M-DX10 Unit-Argument Model)

**⚠️ AILANG has no true nullary functions!** All functions that appear to take no arguments must take a `unit` parameter.

```go
// ✅ CORRECT - Unit-argument model
RegisterEffectBuiltin(BuiltinSpec{
    Module:  "std/sharedmem",
    Name:    "_sharedmem_keys",
    NumArgs: 1,  // Takes unit parameter!
    Effect:  "SharedMem",
    Type: func() types.Type {
        T := types.NewBuilder()
        return T.Func(T.Unit()).Returns(T.List(T.String())).Effects("SharedMem")
    },
    Impl: func(ctx *effects.EffContext, args []eval.Value) (eval.Value, error) {
        // args[0] is unit, ignored (validates arity)
        keys := ctx.SharedMem.Cache.Keys()
        // ...
    },
})

// ❌ WRONG - True nullary (causes "arity mismatch: 0 vs 1")
RegisterEffectBuiltin(BuiltinSpec{
    Name:    "_sharedmem_keys",
    NumArgs: 0,  // BUG!
})
```

**Stdlib wrapper:**
```ailang
export func keys(u: unit) -> list[string] ! {SharedMem} {
    _sharedmem_keys(u)
}
-- Or expression body:
export func now() -> int ! {Clock} = _clock_now()
```

**Go tests must pass unit:**
```go
// ✅ Correct
result, err := impl(ctx, []eval.Value{&eval.UnitValue{}})

// ❌ Wrong - causes arity mismatch
result, err := impl(ctx, []eval.Value{})
```

**Reference:** [M-DX10 design doc](../../../design_docs/implemented/v0_4_6/m-dx10-nullary-function-calls.md)

### Pattern 1: Pure String Function

```go
RegisterEffectBuiltin(BuiltinSpec{
    Module:  "std/string",
    Name:    "_str_len",
    NumArgs: 1,
    IsPure:  true,
    Type: func() types.Type {
        T := types.NewBuilder()
        return T.Func(T.String()).Returns(T.Int())
    },
    Impl: func(ctx *effects.EffContext, args []eval.Value) (eval.Value, error) {
        s := args[0].(*eval.StringValue).Value
        return &eval.IntValue{Value: len([]rune(s))}, nil
    },
})
```

### Pattern 2: Effect Function with HTTP

```go
RegisterEffectBuiltin(BuiltinSpec{
    Module:  "std/net",
    Name:    "_net_httpRequest",
    NumArgs: 4,
    Effect:  "Net",
    Type:    makeHTTPRequestType,
    Impl:    effects.NetHTTPRequest,  // Uses ctx.GetHTTPClient()
})
```

### Pattern 3: Complex Record Types

**See:** [resources/type_builder_examples.md](resources/type_builder_examples.md) for full example with nested records.

## Progressive Disclosure

This skill loads information progressively:

1. **Always loaded**: This SKILL.md file (workflow overview)
2. **Execute as needed**: Scripts in `scripts/` (validation)
3. **Load on demand**: Detailed type examples in `resources/`

## Notes

- No feature flag needed (default since v0.3.10)
- Registry auto-wires to all subsystems
- Test harness prevents network/FS side effects
- Metadata enables future tooling (docs, LSP)
- Type Builder DSL is type-safe at compile time
