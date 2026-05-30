---
name: dacp-interpreter
description: "Load, validate, and use DACP bundles as structured execution context. Detects .bundle/ companion directories, validates integrity (manifest schema, fidelity, provenance), loads typed data, and builds ExecutionContext for receiving agents. Scripts are NEVER auto-executed. Use when processing incoming DACP bundles, interpreting .bundle/ directories alongside .msg files, validating bundle integrity, or building execution context from bundle payloads."
---

# DACP Interpreter

Scripts in bundles are **review-only references** — the interpreter NEVER auto-executes any script (SAFE-01).

## Summary

The DACP Interpreter handles receiving-side bundle processing. When a `.bundle/` directory appears alongside a `.msg` file, the interpreter detects, validates, loads, and integrates the bundle into a structured `ExecutionContext`.

### Fidelity Level Guide

| Level | Contents | What to Do |
|-------|----------|------------|
| 0 | Intent markdown only | Read intent.md, proceed with instructions |
| 1 | Intent + structured data | Access `typedData` for structured parameters |
| 2 | Intent + data + schemas | Validate your understanding against schemas |
| 3 | Intent + data + code | Review scripts, decide whether to execute or reference |
| 4 | Intent + data + code + tests | Verify with provided test fixtures before proceeding |

### Interpretation Pipeline

```
DETECT -> VALIDATE -> LOAD -> INTEGRATE
  |          |         |         |
  |          |         |         +-- buildExecutionContext()
  |          |         +-- loadBundle()
  |          +-- validateBundle()
  +-- Check for .bundle/ directory
```

## Workflow

### Step 1: Detect Bundle Companion

Look for a `.bundle/` directory alongside the `.msg` file. If found, prefer the bundle over raw `.msg` content.

### Step 2: Validate Bundle

Call `validateBundle(bundlePath)` to check:
   - `.complete` marker exists (atomicity guarantee)
   - `manifest.json` parses and validates against Zod schema
   - Fidelity level matches actual directory contents
   - All referenced data and code files exist on disk
   - Size limits respected (50KB data, 10KB per script, 100KB total)
   - Data payloads validate against referenced JSON schemas
   - All scripts have provenance (source skill attribution)

### Step 3: Load Bundle

Call `loadBundle(bundlePath)` to get a typed `LoadedBundle` with:
   - Parsed manifest object
   - Raw intent markdown
   - JSON data payloads as typed objects
   - Schema definitions
   - Script content loaded for review

### Step 4: Build Execution Context

Call `buildExecutionContext(loadedBundle)` to get:
   - `intentSummary` -- what the sender wants done
   - `intentMarkdown` -- full instructions
   - `typedData` -- structured parameters you can use directly
   - `scriptReferences` -- scripts to review (NOT execute blindly)
   - `assemblyRationale` -- why the bundle was composed this way

### Step 5: Review Scripts Before Use

For each script in `scriptReferences`:
   - Read the script content
   - Understand what it does
   - Decide: execute it, reference its logic, or skip it
   - NEVER execute without reviewing first

### Step 6: Report Outcome

After completing the work, report the handoff outcome (intent alignment, rework needed, verification status) for drift tracking.

## Error Handling

### Invalid Bundles

If `validateBundle()` returns `valid: false`:
- Check if a `.msg` fallback file exists alongside the bundle
- If yes: fall back to `.msg` content (backward compatibility)
- If no: report the validation errors and request a re-send

### Provenance Failures

Scripts without a valid `source_skill` in the manifest are rejected. This ensures
every executable artifact traces back to a known, versioned skill. If provenance
validation fails:
- Do NOT use the script
- Report which scripts failed provenance
- Request a corrected bundle from the sender

## References

- `src/interpreter/validator.ts` -- bundle validation pipeline
- `src/interpreter/loader.ts` -- bundle loading into typed structures
- `src/interpreter/context-builder.ts` -- execution context assembly
- `src/interpreter/provenance-guard.ts` -- deep provenance validation
- `src/interpreter/types.ts` -- type definitions (LoadedBundle, ExecutionContext, etc.)
- `src/dacp/types.ts` -- DACP type system (BundleManifest, FidelityLevel, etc.)
