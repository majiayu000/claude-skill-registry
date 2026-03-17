---
name: unity-debugging
description: Diagnose compile errors and runtime issues using logs and headless runs
---

# Unity Debugging Skill

Diagnose and resolve Unity errors without a GUI.

> **See also**: [Shared Conventions](../shared/CONVENTIONS.md) | [Safety Guidelines](../shared/SAFETY.md)

## Purpose

Troubleshoot compile errors, runtime exceptions, and build failures using logs and headless tools.

## Log Locations (Linux)

```
~/.config/unity3d/Editor.log           # Editor log
~/.config/unity3d/Editor-prev.log      # Previous session
~/.config/unity3d/Player.log           # Player/build log
~/workspace/_artifacts/build.log        # CI build logs (custom)
/tmp/                                   # Temp logs from -logFile
```

## Compile-Only Check

Run a headless "compile only" pass to check for errors:

```bash
unity -quit -batchmode -nographics \
  -projectPath /path/to/project \
  -logFile compile.log

# Check exit code
echo $?  # 0 = success, non-zero = errors
```

## Run Tests Headless

```bash
unity -quit -batchmode -nographics \
  -projectPath /path/to/project \
  -runTests \
  -testPlatform EditMode \
  -testResults results.xml \
  -logFile test.log
```

## Triage Ladder

Work through issues in this order:

### 1. Compile Errors (CS errors)

```bash
grep "error CS" build.log | sort | uniq
```

Common patterns:
- `CS0246` - Type not found (missing using, asmdef reference)
- `CS1061` - Method not found (API change, typo)
- `CS0103` - Name doesn't exist (scope issue)

### 2. Missing Assembly References

```bash
grep -i "assembly.*not found\|asmdef" build.log
```

Fix: Check `.asmdef` files reference required assemblies.

### 3. Scripting Define Symbols / Platform Issues

```bash
grep -i "define\|platform\|#if\|conditional" build.log
```

Check `ProjectSettings/ProjectSettings.asset` for:
- `scriptingDefineSymbols`
- `scriptingBackend`

### 4. Package Resolution

```bash
grep -i "package\|manifest\|resolve" build.log
```

Check `Packages/manifest.json` for:
- Version conflicts
- Missing packages
- Registry issues

## Filtering Log Noise

### Extract Only Errors

```bash
grep -E "error CS[0-9]+|Error:|Exception:|FAILED" build.log
```

### Extract Exceptions

```bash
grep -A 5 "Exception:" build.log
```

### Common Exception Types

| Exception | Likely Cause |
|-----------|--------------|
| `NullReferenceException` | Unassigned reference, destroyed object |
| `MissingReferenceException` | Serialized reference to deleted asset |
| `MissingComponentException` | GetComponent on missing component |
| `TypeLoadException` | Assembly/DLL load failure |
| `FileNotFoundException` | Missing asset or DLL |

## Debugging Workflow

### Step 1: Get the Log

```bash
# Find latest log
ls -lt ~/.config/unity3d/*.log | head -5

# Or run compile check
unity -quit -batchmode -nographics \
  -projectPath ~/workspace/project \
  -logFile ~/workspace/_artifacts/debug.log
```

### Step 2: Summarize Issues

```bash
# Count error types
grep "error CS" debug.log | cut -d: -f1 | sort | uniq -c | sort -rn
```

### Step 3: Identify Root Cause

Start with first error - later errors often cascade from earlier ones.

```bash
# Get first 5 errors with context
grep -n -m 5 "error CS" debug.log
```

### Step 4: Fix and Verify

After making fixes:
```bash
unity -quit -batchmode -nographics \
  -projectPath ~/workspace/project \
  -logFile ~/workspace/_artifacts/verify.log

echo "Exit code: $?"
grep -c "error CS" verify.log
```

## Common Fixes

### Missing Type (CS0246)

```csharp
// Add missing using
using UnityEngine.UI;

// Or fix asmdef reference
// Edit YourAssembly.asmdef to include Unity.UI
```

### Null Reference Prevention

```csharp
// Before
_component.DoThing();

// After
if (_component != null)
    _component.DoThing();

// Or use null-conditional
_component?.DoThing();
```

### Serialization Issue

```csharp
// Field not serializing? Check:
[SerializeField] private MyType _field;  // Needs SerializeField for private

// Or make public (not recommended)
public MyType field;
```

## Policies

- Start with compile errors before runtime issues
- Fix first error first - cascading errors are common
- Always verify fix with another compile pass
- Document root cause for recurring issues
