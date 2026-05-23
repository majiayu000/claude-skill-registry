---
name: cue
description: CUE schema patterns for *.cue files, 3-step parsing flow, validation matrix, error formatting. Use when editing invkfile_schema.cue, invkmod_schema.cue, config_schema.cue, or working with cueutil parsing.
disable-model-invocation: false
---

# CUE Schema Patterns

Use this skill when:
- Working with CUE schema files (`*.cue`)
- Modifying parse functions in `pkg/invkfile/`, `pkg/invkmod/`, or `internal/config/`
- Adding new CUE definitions or corresponding Go struct fields
- Debugging CUE validation errors

---

## Schema Locations

- `pkg/invkfile/invkfile_schema.cue` defines invkfile structure.
- `pkg/invkmod/invkmod_schema.cue` defines invkmod structure.
- `internal/config/config_schema.cue` defines config.

## Schema Compilation Pattern (3-Step Flow)

All CUE parsing in Invowk follows a consistent 3-step pattern:

```go
// Step 1: Compile the schema (embedded via //go:embed)
ctx := cuecontext.New()
schemaValue := ctx.CompileString(embeddedSchema)
if schemaValue.Err() != nil {
    return nil, fmt.Errorf("internal error: failed to compile schema: %w", schemaValue.Err())
}

// Step 2: Compile user data and unify with schema
userValue := ctx.CompileBytes(data, cue.Filename(path))
if userValue.Err() != nil {
    return nil, formatCUEError(userValue.Err(), path)
}

schema := schemaValue.LookupPath(cue.ParsePath("#DefinitionName"))
unified := schema.Unify(userValue)
if err := unified.Validate(cue.Concrete(true)); err != nil {
    return nil, formatCUEError(err, path)
}

// Step 3: Decode to Go struct
var result GoStructType
if err := unified.Decode(&result); err != nil {
    return nil, formatCUEError(err, path)
}
```

**Key Points**:
- Schema is embedded via `//go:embed` for single-binary distribution
- Use `LookupPath()` to get the root definition (e.g., `#Invkfile`, `#Config`)
- Use `Validate(cue.Concrete(true))` to ensure all values are concrete
- Use `cue.Concrete(false)` for config files where some fields may be optional
- Always use `Decode()` for type-safe extraction (see Decode Usage Rules below)

**Reference Implementations**:
- `pkg/invkfile/parse.go:ParseBytes()` - Invkfile parsing
- `pkg/invkmod/invkmod.go:ParseInvkmodBytes()` - Invkmod parsing
- `internal/config/config.go:loadCUEIntoViper()` - Config loading

## Validation Responsibility Matrix

Validation is split between CUE and Go based on what each can handle:

### CUE Handles (Declarative, Schema-Level)

| Validation Type | CUE Construct | Example |
|-----------------|---------------|---------|
| Type checking | Native | `name: string` |
| Field format (regex) | `=~` | `name: =~"^[a-zA-Z][a-zA-Z0-9_-]*$"` |
| Enum values | Disjunction | `"native" \| "virtual" \| "container"` |
| Length limits | `strings.MaxRunes()` | `& strings.MaxRunes(256)` |
| Range constraints | Expressions | `>=0 & <=65535` |
| Required fields | No `?` suffix | `name: string` (required) |
| Optional fields | `?` suffix | `description?: string` (optional) |
| Closed structs | `close({})` | Rejects unknown fields |
| Mutual exclusivity | XOR constraints | See runtime config patterns |
| Non-empty lists | Pattern | `[_, ...]` (at least one) |

### Go Handles (Dynamic, Runtime-Level)

| Validation Type | Why Go-Only | Example |
|-----------------|-------------|---------|
| ReDoS prevention | CUE cannot analyze regex complexity | `ValidateRegexPattern()` |
| File existence | Requires filesystem access | `os.Stat()` |
| Path traversal | Cross-platform normalization | `filepath.Clean()` checks |
| Cross-field logic | Conditional requirements | Runtime-specific fields |
| Command hierarchy | Requires tree analysis | Leaf-only args constraint |
| Length limits (defense-in-depth) | Some limits enforced in Go too | `MaxNameLength` checks |

### Justification Comments

All Go-only validations MUST include a `[GO-ONLY]` comment explaining why:

```go
// ValidateRegexPattern validates a user-provided regex pattern for safety.
// [GO-ONLY] ReDoS (Regular Expression Denial of Service) prevention MUST be in Go.
// CUE cannot analyze regex complexity or detect catastrophic backtracking patterns.
func ValidateRegexPattern(pattern string) error { ... }
```

```go
// validateEnvFilePath validates an env file path for security.
// [GO-ONLY] Path traversal prevention and cross-platform path handling require Go.
// CUE cannot perform filesystem operations or cross-platform path normalization.
func validateEnvFilePath(path string) error { ... }
```

## Decode Usage Rules

**ALWAYS use `value.Decode(&goStruct)` for type-safe extraction.**

### Correct Pattern

```go
var invkfile Invkfile
if err := unified.Decode(&invkfile); err != nil {
    return nil, formatCUEError(err, path)
}
```

### Why Not Manual Extraction?

Manual extraction methods (`String()`, `Int64()`, `Bool()`) are error-prone:
- No compile-time type checking
- Requires manual error handling for each field
- Easy to forget optional field handling
- Doesn't leverage CUE's type system

**Exception**: Manual extraction is acceptable only for truly dynamic scenarios (e.g., extracting arbitrary user-defined keys). Document such cases.

## Field Naming Convention

CUE uses `snake_case`, Go uses `PascalCase`. The JSON tag bridges them:

```cue
// CUE Schema (snake_case)
#Config: close({
    container_engine: #ContainerEngine
    search_paths:     [...string]
    default_runtime:  #RuntimeType
})
```

```go
// Go Struct (PascalCase with JSON tags)
type Config struct {
    ContainerEngine ContainerEngine `json:"container_engine"`
    SearchPaths     []string        `json:"search_paths"`
    DefaultRuntime  RuntimeMode     `json:"default_runtime"`
}
```

**Rule**: Every CUE field name MUST have a matching JSON tag in the corresponding Go struct.

**Verification**: Schema sync tests (in `*_sync_test.go` files) catch mismatches at CI time.

## Error Formatting Requirements

All CUE errors MUST include JSON path prefixes for clear error messages:

### Error Format

```
<file-path>: <json-path>: <message>
```

Examples:
```
invkfile.cue: cmds[0].implementations[2].script: value exceeds maximum length
config.cue: container.auto_provision.enabled: expected bool, got string
```

### Implementation Pattern

Use the `formatCUEError()` helper (available in each package):

```go
import "cuelang.org/go/cue/errors"

func formatCUEError(err error, filePath string) error {
    if err == nil {
        return nil
    }

    cueErrors := errors.Errors(err)
    if len(cueErrors) == 0 {
        return fmt.Errorf("%s: %w", filePath, err)
    }

    var lines []string
    for _, e := range cueErrors {
        path := errors.Path(e)
        pathStr := formatPath(path)  // Convert ["cmds", "0", "script"] to "cmds[0].script"
        msg := e.Error()

        if pathStr != "" {
            lines = append(lines, fmt.Sprintf("%s: %s", pathStr, msg))
        } else {
            lines = append(lines, msg)
        }
    }

    if len(lines) == 1 {
        return fmt.Errorf("%s: %s", filePath, lines[0])
    }
    return fmt.Errorf("%s: validation failed:\n  %s", filePath, strings.Join(lines, "\n  "))
}
```

**Important**: Import `cuelang.org/go/cue/errors`, NOT the standard library `errors`. Only CUE's error package provides `Errors()` and `Path()` functions.

## CUE Library Version Pinning

### Current Version

CUE is pinned in `go.mod`:

```
cuelang.org/go v0.15.3
```

### Upgrade Process

When upgrading the CUE library version:

1. **Review Changelog**: Check for breaking changes in the CUE release notes
2. **Run Full Test Suite**: `make test` including all schema sync tests
3. **Check API Deprecations**: Search for deprecated function usage
4. **Verify Error Formats**: Manually test that error messages still include paths
5. **Update Documentation**: If CUE behavior changes, update this rules file
6. **Test Cross-Platform**: Run CI on all platforms (Linux, macOS, Windows)

### Known CUE Limitations

- **No Encode API**: CUE can decode Go structs but has no production-ready encoder
- **No Code Generation**: `gengotypes` is experimental; we use sync tests instead
- **Context is Stateful**: Create a new `cuecontext.New()` for each parse operation

## Rules

- All CUE structs must be closed (use `close({ ... })`) so unknown fields cause validation errors.
- When adding new CUE struct fields or definitions, always include appropriate validation constraints (e.g., `strings.MaxRunes()`, regex patterns with `=~`, range constraints like `>=0 & <=255`) - not just type declarations. This ensures defense-in-depth validation.
- Schema sync tests MUST exist for every Go struct that corresponds to a CUE definition.
- Go-only validations MUST have `[GO-ONLY]` comments explaining why CUE cannot handle them.

## Schema Sync Tests

Sync tests verify Go struct JSON tags match CUE schema field names at CI time. They catch misalignments before they cause silent parsing failures.

**Test Files**:
- `pkg/invkfile/sync_test.go` - Invkfile, Command, Implementation, etc.
- `pkg/invkmod/sync_test.go` - Invkmod, ModuleRequirement
- `internal/config/sync_test.go` - Config, VirtualShellConfig, UIConfig, etc.

**Pattern**:
```go
func TestStructNameSchemaSync(t *testing.T) {
    schema, _ := getCUESchema(t)
    cueFields := extractCUEFields(t, lookupDefinition(t, schema, "#DefinitionName"))
    goFields := extractGoJSONTags(t, reflect.TypeFor[GoStructType]())

    assertFieldsSync(t, "StructName", cueFields, goFields)
}
```

**When to Add Sync Tests**:
- Adding a new CUE definition with a corresponding Go struct
- Adding new fields to existing CUE/Go types
- Renaming fields (test will fail until both are updated)

## Common Pitfalls

### Unclosed CUE Structs

**Problem**: Open structs allow arbitrary unknown fields, bypassing validation.

```cue
// WRONG: Open struct - unknown fields silently accepted
#Config: {
    name: string
}

// CORRECT: Closed struct - unknown fields rejected
#Config: close({
    name: string
})
```

### Redundant Validation

**Problem**: Same validation in both CUE and Go creates maintenance burden.

**Rule**: Validation lives in ONE place. CUE handles format/type validation. Go handles security/filesystem/cross-field logic.

**Anti-Pattern**:
```go
// WRONG: Duplicates CUE regex validation
if !regexp.MustCompile(`^[a-zA-Z][a-zA-Z0-9_-]*$`).MatchString(name) {
    return fmt.Errorf("invalid name format")
}
```

**Correct Pattern**:
```go
// CORRECT: CUE handles format; Go handles length (defense-in-depth)
// [GO-ONLY] Length limit not in CUE for simplicity; checked here for defense-in-depth.
if len(name) > MaxNameLength {
    return fmt.Errorf("name too long (%d chars, max %d)", len(name), MaxNameLength)
}
```

### Missing JSON Tags

**Problem**: Go struct field without JSON tag won't be populated by `Decode()`.

**Symptom**: Field is always zero value despite being in CUE file.

**Fix**: Add JSON tag matching the CUE field name:
```go
type Config struct {
    SearchPaths []string `json:"search_paths"`  // Matches CUE field
    CachePath   string   // No JSON tag - will be empty!
}
```

### Wrong Error Import

**Problem**: Using standard library `errors` instead of CUE's error package.

```go
// WRONG: Standard library - no Path() function
import "errors"

// CORRECT: CUE error package with path extraction
import "cuelang.org/go/cue/errors"
```

### Stale Schema Sync Tests

**Problem**: Sync test exclusions become outdated after refactoring.

**Fix**: After any CUE/Go struct changes, run `make test` and verify sync tests pass. Remove obsolete exclusions.
