---
name: discovery
description: Module/command discovery, precedence order, collision detection, source tracking
disable-model-invocation: false
---

# Discovery Skill

This skill covers the discovery system in Invowk, which locates and aggregates commands from multiple sources with clear precedence rules and collision detection.

Use this skill when working on:
- `internal/discovery/` - Discovery and aggregation logic
- Module resolution and dependency handling
- Command collision detection and disambiguation
- Source tracking and precedence

---

## Discovery Precedence Order

The discovery system implements a **strict 4-level precedence hierarchy**:

| Priority | Source | Description |
|----------|--------|-------------|
| 1 (Highest) | Current Directory | `invkfile.cue` in the working directory |
| 2 | Local Modules | Sibling `*.invkmod` directories in current directory |
| 3 | User Commands | `~/.invowk/cmds/` with recursive search |
| 4 (Lowest) | Config Paths | Custom paths from config, searched recursively |

**Key Behavior:**
- Non-module sources (current dir, user dir, config paths): First source **shadows** later ones
- Module commands: **All included** with ambiguity flagging for transparent namespace

---

## File Discovery Algorithm

Discovery has two parallel tracks:

### Track A: Invkfile Discovery

```go
// Single-level check (current directory)
discoverInDir(dir)  // Looks for invkfile.cue OR invkfile

// Recursive search (user dir, config paths)
discoverInDirRecursive(dir)  // Uses filepath.WalkDir()
```

**File Priority:** `.cue` extension preferred over non-suffixed `invkfile`

### Track B: Module Discovery

```go
// Non-recursive - only immediate subdirectories
discoverModulesInDir(dir)
```

**Module Validation:**
- Uses `invkmod.IsModule()` to verify directory structure
- Skips reserved module name `"invkfile"` (reserved for canonical namespace)
- **Graceful degradation**: Invalid modules are silently skipped

---

## Source Tracking Types

### Source Enum

```go
const (
    SourceCurrentDir   Source = iota  // "current directory"
    SourceUserDir                     // "user commands (~/.invowk/cmds)"
    SourceConfigPath                  // "configured search path"
    SourceModule                      // "module" (from .invkmod)
)
```

### DiscoveredFile

Captures discovery metadata for each found file:

```go
type DiscoveredFile struct {
    Path     string           // Absolute path
    Source   Source           // Which source type
    Invkfile *invkfile.Invkfile  // Parsed content (lazy-loaded)
    Error    error            // Parse errors if applicable
    Module   *invkmod.Module  // Non-nil if from .invkmod
}
```

### CommandInfo

Output of command aggregation:

```go
type CommandInfo struct {
    Name        string  // Full name with prefix (e.g., "foo build")
    SimpleName  string  // Unprefixed name (e.g., "build")
    Source      Source
    SourceID    string  // "invkfile" or module short name
    ModuleID    string  // Full module ID (e.g., "io.invowk.sample")
    IsAmbiguous bool    // True if SimpleName conflicts across sources
    FilePath    string  // Absolute path to invkfile
    Command     *invkfile.Command
    Invkfile    *invkfile.Invkfile
}
```

---

## Command Aggregation & Collision Detection

The aggregation system uses a **two-phase process with transparent namespace**:

### Phase 1: Flatten & Index

```go
// Get all commands with proper namespacing
commands := invkfile.FlattenCommands()

// Modules have commands prefixed:
// Module "foo" with command "build" → "foo build"
```

### Phase 2: Conflict Analysis

The `DiscoveredCommandSet` provides:

| Field | Purpose |
|-------|---------|
| `Commands` | All discovered commands |
| `BySimpleName` | Index: simple name → all commands with that name |
| `AmbiguousNames` | Set of names that exist in >1 source |
| `BySource` | Groups commands by source ID |
| `SourceOrder` | Pre-sorted: "invkfile" first, then modules alphabetically |

### Precedence vs. Collision Handling

| Source Type | Behavior |
|-------------|----------|
| Non-module (current dir, user dir, config) | First source **WINS** (shadows later) |
| Module (sibling .invkmod directories) | **ALL included** with ambiguity flagging |

**IsAmbiguous Flag:** Set to `true` when a simple name conflicts across sources. This enables:
- **Transparent namespace** for unambiguous commands: `invowk cmd build`
- **Explicit disambiguation** for ambiguous ones: `invowk cmd @foo build`

---

## Module Dependency Handling

### Module Identity & Visibility

```go
type Module struct {
    Path    string          // Filesystem location
    Invkmod *invkmod.Invkmod  // Parsed metadata from invkmod.cue
}

// Module commands are automatically namespaced
// Module "foo" → commands like "foo build", "foo deploy"
```

### Module Collision Detection

When two modules have the same ID in different sources:

```go
type ModuleCollisionError struct {
    ModuleID string
    Sources  []string
}

// Validation
err := discovery.CheckModuleCollisions()
// Returns actionable guidance: "invowk module alias <source> <new-alias>"
```

**Module Aliases:** Configured in `config.ModuleAliases` map to disambiguate collisions.

### Command Scope Rules

Commands can only call:

1. Commands from the **same module**
2. Commands from **globally installed modules** (`~/.invowk/modules/`)
3. Commands from **first-level requirements** (direct dependencies in `invkmod.cue:requires`)

**CRITICAL:** Transitive dependencies are **NOT accessible**. Commands cannot call dependencies of dependencies. This enforces explicit, auditable dependency chains.

---

## Validation

### Command Tree Validation

`ValidateCommandTree()` enforces the **leaf-only args** rule:

```go
// A command cannot have both positional args AND subcommands
// Positional args would be unreachable if subcommands exist

type ArgsSubcommandConflictError struct {
    CommandPath []string  // Path to the conflicting command
    ArgNames    []string  // The args that conflict
}
```

---

## Usage Patterns

### Simple Command Execution

```go
disc := discovery.New(cfg)
commands, err := disc.DiscoverCommands()  // Flat list, sorted
```

### CLI Listing with Grouping

```go
cmdSet, err := disc.DiscoverCommandSet()

for _, sourceID := range cmdSet.SourceOrder {
    for _, cmd := range cmdSet.BySource[sourceID] {
        if cmd.IsAmbiguous {
            // Show with disambiguation prefix
        } else {
            // Show with transparent namespace
        }
    }
}
```

### Validation Before Execution

```go
commands, err := disc.DiscoverAndValidateCommands()  // Includes tree validation
```

### Get Specific Command

```go
cmdInfo, err := disc.GetCommand("foo build")
// Returns Command, Invkfile, Module metadata
```

---

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Combined file discovery + command aggregation | Tightly coupled; splitting would require large intermediate data structures |
| Non-module precedence shadows | User dir and config paths are fallback sources |
| Module commands all included | Modules in current dir are first-class and should all be visible |
| SimpleName-based collision detection | Enables transparent namespace while flagging attention for conflicts |
| Lazy parsing (LoadAll vs DiscoverAll) | Parsing deferred until needed; discovery is I/O only |
| Module aliases in config | Keeps discovery focused on filesystem; config handles naming |
| Graceful error handling | Invalid modules skipped; one bad module doesn't block others |

---

## File Organization

| File | Purpose |
|------|---------|
| `discovery.go` | Main discovery logic and public API |
| `command_set.go` | Command aggregation and collision detection |
| `validation.go` | Command tree validation |
| `source.go` | Source types and tracking |
| `doc.go` | Package documentation |

---

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Expecting transitive deps | Command can't call dep-of-dep | Add explicit first-level requirement |
| Forgetting disambiguation | "ambiguous command" error | Use `@source` prefix or `--from` flag |
| Args + subcommands together | ArgsSubcommandConflictError | Make args-only or subcommands-only |
| Testing non-module shadowing | Later source visible | Only first non-module source wins |
| Module with reserved name "invkfile" | Module silently skipped | Use different module name |
