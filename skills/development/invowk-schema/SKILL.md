---
name: invowk-schema
description: Schema guidelines for invkfile.cue and modules/*.invkmod, cross-platform runtime patterns, command implementations, capability checks, environment variables.
disable-model-invocation: false
---

# Invowk Schema Guidelines

Use this skill when:
- Editing the `invkfile.cue` root example file
- Working with sample modules in `modules/`
- Adding or modifying command/implementation structures
- Handling cross-platform runtime selection (native vs virtual runtimes on different platforms)

---

## Invkfile Examples

### Built-in Examples (`invkfile.cue` at project root)

- Always update the example file when invkfile definitions or features are added, modified, or removed.
- All commands should be idempotent and not cause any side effects on the host.
- No commands should be related to building invowk itself or manipulating any of its source code.
- Examples should range from simple (e.g., native "hello-world") to complex (e.g., container "hello-world" with `enable_host_ssh`).
- Examples should cover different features, such as:
  - Native vs. container execution.
  - Volume mounts for container execution.
  - Environment variables.
  - Host SSH access enabled vs. disabled.
  - Capabilities checks (with and without alternatives).
  - Tools checks (with and without alternatives).
  - Custom checks (with and without alternatives).
- Module metadata does not belong in invkfile examples; it lives in `invkmod.cue` for modules.

### Command Structure Validation

#### Leaf-Only Args Constraint

**Commands with positional arguments (`args`) cannot have subcommands.** This is enforced during command discovery and module validation.

Why: CLI parsers interpret positional arguments after a command name as potential subcommand names. If `deploy` has both `args: [{name: "env"}]` and a subcommand `deploy staging`, running `invowk cmd deploy prod` is ambiguous—is `prod` an argument or a subcommand name?

**Valid:**
```cue
// Leaf command with args (no subcommands)
cmds: [
    {name: "deploy", args: [{name: "env"}], ...}
]

// Parent command with subcommands (no args on parent)
cmds: [
    {name: "deploy"},           // No args here
    {name: "deploy staging"},   // Subcommand
    {name: "deploy prod"},      // Subcommand
]
```

**Invalid:**
```cue
cmds: [
    {name: "deploy", args: [{name: "env"}], ...},  // Has args
    {name: "deploy staging", ...}                   // Is a subcommand of deploy
]
// Error: command 'deploy' has both args and subcommands
```

This validation runs:
1. During `invowk cmd` execution (command discovery)
2. During `invowk module validate --deep`

### Cross-Platform Runtime Selection

**Bash scripts with native+virtual runtimes must use platform-specific implementations.**

**The problem:** The native runtime on Windows uses PowerShell (or `cmd`), which cannot parse bash syntax. When a command declares `runtimes: [{name: "native"}, {name: "virtual"}]`, the first runtime (native) becomes the default. This causes bash scripts to fail on Windows with PowerShell parser errors.

**The solution:** Split implementations by platform:
- **Linux/macOS**: Use `runtimes: [{name: "native"}, {name: "virtual"}]` with `platforms: [{name: "linux"}, {name: "macos"}]`
- **Windows**: Use `runtimes: [{name: "virtual"}]` with `platforms: [{name: "windows"}]` (virtual runtime uses `mvdan/sh`, a cross-platform POSIX shell)

**Valid (platform-specific implementations):**
```cue
implementations: [
    {
        script: """
            echo "Hello from bash"
            if [ -f /etc/os-release ]; then
                cat /etc/os-release
            fi
            """
        runtimes:  [{name: "native"}, {name: "virtual"}]
        platforms: [{name: "linux"}, {name: "macos"}]
    },
    {
        script: """
            echo "Hello from bash"
            if [ -f /etc/os-release ]; then
                cat /etc/os-release
            fi
            """
        runtimes:  [{name: "virtual"}]
        platforms: [{name: "windows"}]
    },
]
```

**Invalid (bash script without platform restriction):**
```cue
implementations: [
    {
        script: """
            echo "Hello from bash"
            if [ -f /etc/os-release ]; then
                cat /etc/os-release
            fi
            """
        runtimes: [{name: "native"}, {name: "virtual"}]
        // Missing platforms restriction - will fail on Windows!
    },
]
```

**When to apply this pattern:**
- Any command with bash/POSIX shell scripts
- That declares both native and virtual runtimes
- And should work on Windows

**Exceptions (no split needed):**
- Commands with `runtimes: [{name: "virtual"}]` only (already cross-platform)
- Commands with `runtimes: [{name: "native"}]` only and `platforms: [{name: "linux"}, {name: "macos"}]` (Linux/macOS only)
- Commands with PowerShell scripts intended for Windows

## Invkmod Modules

### Samples (`modules/` directory)

The `modules/` directory contains sample modules that serve as reference implementations and validation tests.

- A module is a `.invkmod` directory containing `invkmod.cue` (metadata) and `invkfile.cue` (commands).
- The invkmod schema lives in `pkg/invkmod/invkmod_schema.cue` and the invkfile schema in `pkg/invkfile/invkfile_schema.cue`.
- Always update sample modules when the invkmod schema, validation rules, or module behavior changes.
- Modules should demonstrate module-specific features (script file references, cross-platform paths, requirements).
- After module-related changes, run validation: `go run . module validate modules/<module-name>.invkmod --deep`.

### Current Sample Modules

- `io.invowk.sample.invkmod` - Minimal cross-platform module with a simple greeting command.

### Module Validation Checklist

When modifying module-related code, verify:
1. All modules in `modules/` pass validation: `go run . module validate modules/*.invkmod --deep`.
2. Module naming conventions and module ID matching are enforced.
3. `invkmod.cue` is required and parsed; `invkfile.cue` contains only commands.
4. Script path resolution works correctly (forward slashes, relative paths).
5. Nested module detection works correctly.
6. The `pkg/invkmod/` tests pass: `go test -v ./pkg/invkmod/...`.

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Stale sample modules | Validation fails after schema changes | Update modules in `modules/` after module-related changes |
| Missing platform restrictions | Bash scripts fail on Windows | Add platform-specific implementations for native+virtual runtimes |
| Args with subcommands | Discovery validation error | Commands with positional args cannot have subcommands |

For path handling in implementations, see `.claude/rules/windows.md`.
