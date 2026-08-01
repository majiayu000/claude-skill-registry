---
name: uloop-compile
description: 'Compile Unity project via uloop CLI. Use when you need to: (1) Verify
  C# code compiles successfully after editing scripts, (2) Check for compile errors
  or warnings, (3) Validate script changes before'
---

---
name: uloop-compile
description: Compile Unity project via uloop CLI. Use when you need to: (1) Verify C# code compiles successfully after editing scripts, (2) Check for compile errors or warnings, (3) Validate script changes before running tests.
---

# uloop compile

Execute Unity project compilation.

## Usage

```bash
uloop compile [--force-recompile]
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `--force-recompile` | boolean | Force full recompilation (triggers Domain Reload) |

## Examples

```bash
# Check compilation
uloop compile

# Force full recompilation
uloop compile --force-recompile
```

## Output

Returns JSON:
- `Success`: boolean
- `ErrorCount`: number
- `WarningCount`: number

## Troubleshooting

If CLI hangs or shows "Unity is busy" errors after compilation, stale lock files may be preventing connection. Run the following to clean them up:

```bash
uloop fix
```

This removes any leftover lock files (`compiling.lock`, `domainreload.lock`, `serverstarting.lock`) from the Unity project's Temp directory.
