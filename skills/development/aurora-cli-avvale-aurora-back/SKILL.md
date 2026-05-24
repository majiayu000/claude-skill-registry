---
name: aurora-cli
description: >
  Run Aurora CLI commands to generate/regenerate modules, add packages, or create projects.
  Trigger: When user asks to regenerate code, load module, add package, or create new Aurora project.
license: MIT
metadata:
  author: aurora
  version: "1.0"
  auto_invoke: "Regenerating modules, adding packages, Aurora CLI operations"
---

## When to Use

- User asks to "regenerate", "load", or "generate" a module
- User wants to add a package (oauth, auditing, etc.)
- User needs to create a new Aurora project
- After YAML schema changes that require code regeneration
- User mentions "aurora cli" or "aurora load"

---

## Critical Patterns

### Command Structure

| Action | Command | When to Use |
|--------|---------|-------------|
| Regenerate module | `aurora load back module -n=<bc>/<module>` | After YAML changes |
| Force regenerate | `aurora load back module -n=<bc>/<module> -f` | Override hash protection |
| With tests | `aurora load back module -n=<bc>/<module> -t` | Generate e2e tests |
| Add package | `aurora add back <package>` | Install preconfigured package |
| New project | `aurora new back <name>` | Create new project (rare) |

### Hash Protection System

Aurora tracks file modifications via hash. Files with custom changes are **protected by default**:
- Without `-f`: Modified files are preserved
- With `-f`: All files are overwritten (use with caution)

---

## Execution Flow

### 1. Identify Action
Ask the user what they want to do:
1. **Generate/Regenerate module** - Regenerate code from existing YAML
2. **Add package** - Install preconfigured package (auditing, oauth, etc.)
3. **Create project** - Create new Aurora project (rare)

### 2. Gather Information

**For Generate/Regenerate Module:**
1. Ask which bounded context and module to regenerate
2. ONLY if you can't identify them, list available YAMLs in `cliter/` using Glob
3. Ask about flags:
   - `--force` (overwrite existing files)
   - `--tests` (generate e2e tests)
   - `--verbose` (detailed output)

**For Add Package:**
1. Run `aurora add back` to show available packages
2. Ask which package to install
3. Ask if `--force` is needed

**For Create Project:**
1. Ask for project name
2. Confirm before executing

### 3. Execute Command

```bash
# Regenerate module
aurora load back module -n=<bounded-context>/<module> [-f] [-t] [-v]

# Add package
aurora add back <package> [-f]

# Create project
aurora new back <app-name>
```

### 4. Report Results

```
Command executed successfully
aurora load back module -n=tesla/model -ft

Regenerated Files:
  - src/@api/tesla/model/controllers/...
  - src/@app/tesla/model/domain/...

Preserved Files (modified hash):
  - src/@app/tesla/model/application/create/create-model.command-handler.ts
  (These files have custom modifications and were not overwritten)

Summary:
  - X files regenerated
  - Y files preserved
```

---

## Commands

```bash
# Regenerate module from YAML
aurora load back module -n=tesla/model

# Regenerate with force + tests
aurora load back module -n=tesla/model -ft

# Add package
aurora add back oauth

# Show available packages
aurora add back

# Create new project
aurora new back my-project
```

---

## Flags

| Flag | Description |
|------|-------------|
| `-f, --force` | Overwrite existing files (even with modified hash) |
| `-t, --tests` | Generate e2e test files |
| `-v, --verbose` | Show detailed CLI output |

---

## Error Handling

| Error | Solution |
|-------|----------|
| CLI not found | Report that Aurora CLI is not installed |
| YAML not found | Report expected path and suggest creating it |
| Permission error | Report and suggest solutions |
| Execution error | Show complete error output |

---

## Related Skills

This skill works with:
- **aurora-project-structure**: Understand project structure and locate generated files
- **aurora-cqrs**: Understand CQRS components that will be regenerated
- **conventional-commits**: Create commits after successful regeneration

---

## Resources

- **YAML Definitions**: `cliter/[package]/[module].aurora.yaml`
- **Lock Files**: `cliter/[package]/[module]-lock.json`
- **Generated Code**: `src/@api/` and `src/@app/`
