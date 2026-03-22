---
name: diff-apply
description: "Apply generated diff files to the ace_engine repository (TypeScript/C++ hybrid codebase) with intelligent conflict resolution. Use when applying .diff or .patch files to ace_engine code, resolving merge conflicts while preserving original logic, or validating changes via compilation after patching. Target repo is ROOT/code/foundation/arkui/ace_engine in a repo manifest project."
---

# Diff Apply Skill

Apply diffs to ace_engine while preserving original logic and ensuring successful compilation.

## Directory Structure

```
ROOT/
└── code/
    ├── build.sh                          # Build script
    └── foundation/arkui/ace_engine/      # Working directory (run Claude here)
```

Working directory: `ROOT/code/foundation/arkui/ace_engine`
Build script location: `../../../build.sh` (relative to working directory)

## Workflow

1. **Analyze** — Read diff, identify affected files (.ts, .cpp, .h, .ets)
2. **Backup** — Copy affected files before modification
3. **Apply** — Apply diff, capture any rejects
4. **Resolve** — Fix conflicts per references/conflict-resolution.md
5. **Verify logic** — Ensure original behavior preserved
6. **Compile** — Run build, fix any errors

## Step 1: Analyze the Diff

```bash
# Preview what will change
cat your.diff | grep "^diff --git" | awk '{print $3}' | sed 's|^a/||'

# Check diff stats
diffstat your.diff 2>/dev/null || cat your.diff | grep -E "^\+|^-" | wc -l
```

Identify file types and assess risk:
- `.cpp`, `.h` files: High risk — careful with memory management, RAII patterns
- `.ts`, `.ets` files: Medium risk — watch for type changes, async patterns
- Build files: High risk — may break compilation

## Step 2: Backup Originals

```bash
BACKUP_DIR="/tmp/ace_backup_$(date +%s)"
mkdir -p "$BACKUP_DIR"

# For each file in diff (paths relative to ace_engine)
for f in $(cat your.diff | grep "^diff --git" | awk '{print $3}' | sed 's|^a/||'); do
  if [ -f "$f" ]; then
    mkdir -p "$BACKUP_DIR/$(dirname $f)"
    cp "$f" "$BACKUP_DIR/$f"
  fi
done
```

## Step 3: Apply Diff

```bash
# Already in ace_engine directory

# Try clean apply first
git apply --check /path/to/your.diff

# If clean:
git apply /path/to/your.diff

# If conflicts, apply with rejects:
git apply --reject --whitespace=fix /path/to/your.diff
# This creates .rej files for failed hunks
```

Alternative using patch:
```bash
patch -p1 --dry-run < /path/to/your.diff   # Test first
patch -p1 < /path/to/your.diff              # Apply
```

## Step 4: Resolve Conflicts

See **references/conflict-resolution.md** for detailed patterns.

Key principles:
- **Never delete** original error handling, logging, or validation
- **Preserve** memory management patterns in C++ (RAII, smart pointers)
- **Keep** type annotations in TypeScript
- **Merge carefully** when both sides modify the same function

For each `.rej` file:
1. Read the rejected hunk
2. Find the target location in the actual file
3. Manually integrate changes following conflict resolution rules
4. Delete the `.rej` file after resolution

## Step 5: Verify Logic Preservation

Before compiling, verify:
- [ ] No original functions deleted (unless explicitly intended)
- [ ] Error handling paths preserved
- [ ] Return types unchanged (or intentionally changed)
- [ ] No dangling references in C++ code
- [ ] Async/await patterns intact in TypeScript

## Step 6: Compile and Test

```bash
# Navigate to code directory and build
cd ../../..  # From ace_engine to ROOT/code

# Clean previous artifacts
find out -name "*.abc" | xargs rm

# Build
./build.sh --product-name rk3568 --build-target arkoala_abc

# Return to ace_engine
cd foundation/arkui/ace_engine
```

Or as a one-liner from ace_engine:
```bash
(cd ../../.. && find out -name "*.abc" | xargs rm && ./build.sh --product-name rk3568 --build-target arkoala_abc)
```

### If Compilation Fails

1. Read error message — identify file and line
2. Compare with backup — `diff "$BACKUP_DIR/file" "$REPO_DIR/file"`
3. Determine cause:
   - **Syntax error**: Likely bad conflict resolution
   - **Type error**: Check if diff changed interfaces
   - **Linker error**: Check C++ symbol visibility
4. Fix and rebuild

### Common Build Errors

| Error Pattern | Likely Cause | Fix |
|---------------|--------------|-----|
| `undefined reference` | Missing C++ symbol | Check header includes, symbol export |
| `TS2304: Cannot find name` | Missing TypeScript import | Add import statement |
| `TS2345: Argument type` | Type mismatch | Verify interface compatibility |
| `expected ';'` | Syntax from bad merge | Review conflict resolution |

## Quick Reference

```bash
# Full workflow from ace_engine directory (after backup)
git apply --reject --whitespace=fix /path/to/your.diff && \
find . -name "*.rej" -exec echo "CONFLICT: {}" \; && \
(cd ../../.. && find out -name "*.abc" | xargs rm && ./build.sh --product-name rk3568 --build-target arkoala_abc)
```