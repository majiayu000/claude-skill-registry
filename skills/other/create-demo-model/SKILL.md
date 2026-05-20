---
name: create-demo-model
description: Create a Diff Studio demo model TS file and register it in the package, using equations from an IVP file. Use this skill when the user wants to create a demo model from an IVP file, mentions "demo model", "IVP file", "Diff Studio demo", or asks to convert an .ivp file into a demo.
argument-hint: <ivp-file-path> [png-file-path]
---

# Create Demo Model from IVP File

Create a Diff Studio demo model using equations extracted from the IVP file, and register it in the package.

## Input Parsing

The user provides arguments in this format:

```
<ivp-file-path> [png-file-path]
```

- `ivp-file-path` (required) — path to the `.ivp` file
- `png-file-path` (optional) — path to the `.png` preview image

If `ivp-file-path` is missing, ask the user to provide it.

## Workflow

### Step 1 - Validate inputs

Verify that `ivp-file-path` exists and has a `.ivp` extension.
If `png-file-path` is provided, verify it exists and has a `.png` extension.
If validation fails, report the issue and stop.

### Step 2 - Run the generator

Run the conversion script from the skill directory:

```bash
python3 .claude/skills/create-demo-model/scripts/ivp-to-demo.py <ivp-file-path> [png-file-path]
```

If the script exits with a non-zero code, show stderr to the user and stop.
