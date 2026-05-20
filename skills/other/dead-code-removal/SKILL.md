---
name: dead-code-removal
description: "Dead code removal via parallel scanning, reference verification, batch execution, and atomic commits. You are the ORCHESTRATOR — you scan, verify, batch, then delegate ALL removals."
---

# Dead Code Removal

Dead code removal via massively parallel scanning and execution. You are the ORCHESTRATOR — you scan, verify, batch, then execute all removals with atomic commits.

**Rules:**
- **Reference verification is law.** Verify with grep/language tools before ANY removal decision.
- **Never remove entry points.** Main entry files, test files, config files — off-limits.

**False-positive guards — NEVER mark as dead:**
- Symbols in entry point files or barrel `index` re-exports
- Symbols referenced in test files (tests are valid consumers)
- Symbols with `@public` / `@api` doc tags
- Hook factories (`createXXXHook`), tool factories (`createXXXTool`), plugin definitions
- Command templates, skill definitions, config objects
- Symbols in package exports

---

## PHASE 1: SCAN — Find Dead Code Candidates

Run ALL of these in parallel:

**Compiler/linter strict mode (primary scanner — run FIRST):**
```bash
# TypeScript
npx tsc --noEmit --noUnusedLocals --noUnusedParameters 2>&1

# Python
vulture src/ --min-confidence 80

# Go
staticcheck -checks U1000 ./...
```
This gives you the definitive list of unused locals, imports, parameters, and types with exact file:line locations.

**Orphaned file detection (run simultaneously):**
Find files in src/ NOT imported by any other file. Check all import statements.
EXCLUDE: index files, test files, entry points, markdown, config files.
Return: file paths.

**Unused export detection (run simultaneously):**
Find exported functions/types/constants that are never imported by other files.
Cross-reference: for each export, grep the symbol name across src/ — if it only appears in its own file, it's a candidate.
EXCLUDE: entry point exports, test files.
Return: file path, line, symbol name, export type.

Collect all results into a master candidate list.

---

## PHASE 2: VERIFY — Reference Confirmation (Zero False Positives)

For EACH candidate from Phase 1:

```bash
# Search for all references (excluding the declaration itself)
grep -rn "symbolName" src/ --include="*.ts" | grep -v "declaration_file.ts"

# Or use language-specific tools:
#   TypeScript: ts-prune, ts-unused-exports
#   Python: vulture --min-confidence 80
#   Go: staticcheck -checks U1000

# 0 references = CONFIRMED dead
# 1+ references = NOT dead, drop from list
```

Also apply the false-positive guards above. Produce a confirmed list:

```
| # | File | Symbol | Type | Action |
|---|------|--------|------|--------|
| 1 | src/foo.ts:42 | unusedFunc | function | REMOVE |
| 2 | src/bar.ts:10 | OldType | type | REMOVE |
| 3 | src/baz.ts:7 | ctx | parameter | PREFIX _ |
```

**Action types:**
- `REMOVE` — delete the symbol/import/file entirely
- `PREFIX _` — unused function parameter required by signature → rename to `_paramName`

If ZERO confirmed: report "No dead code found" and STOP.

---

## PHASE 3: BATCH — Group by File for Conflict-Free Parallelism

**Goal: maximize parallel execution with ZERO conflicts.**

1. Group confirmed dead code items by FILE PATH
2. All items in the SAME file go to the SAME batch (prevents two agents editing the same file)
3. If a dead FILE (entire file deletion) exists, it's its own batch
4. Target 5-15 batches. If fewer than 5 items total, use 1 batch per item.

**Example batching:**
```
Batch A: [src/hooks/foo/hook.ts — 3 unused imports]
Batch B: [src/features/bar/manager.ts — 2 unused constants, 1 dead function]
Batch C: [src/tools/baz/tool.ts — 1 unused param, src/tools/baz/types.ts — 1 unused type]
Batch D: [src/dead-file.ts — entire file deletion]
```

Files in the same directory CAN be batched together (they won't conflict as long as no two agents edit the same file). Maximize batch count for parallelism.

---

## PHASE 4: EXECUTE — Apply Removals

For EACH batch:

### Protocol

1. Read each file to understand exact syntax at the target lines
2. Re-verify with grep that the symbol is still dead (another batch may have changed things)
3. Apply the change:
   - Unused import (only symbol in line): remove entire import line
   - Unused import (one of many): remove only that symbol from the import list
   - Unused constant/function/type: remove the declaration. Clean up trailing blank lines.
   - Unused parameter: prefix with `_` (do NOT remove — required by signature)
   - Dead file: delete with `rm`
4. After ALL edits in this batch, run the type checker / build
5. If build fails: `git checkout -- [files]` and report failure
6. If build passes: stage ONLY your files and commit:
   `git add [your-specific-files] && git commit -m "refactor: remove dead code from [brief file list]"`
7. Report what you removed and the commit hash

### Critical Rules
- Stage ONLY your batch's files (`git add [specific files]`). NEVER `git add -A` — other batches may be running in parallel.
- If build fails after your edits, REVERT all changes and report. Do not attempt to fix.
- Pre-existing test failures in other files are expected. Only the type checker / build matters for your batch.

---

## PHASE 5: FINAL VERIFICATION

After ALL batches complete:

```bash
# Language-specific type check (must pass)
npx tsc --noEmit          # TypeScript
mypy src/                  # Python
go vet ./...               # Go

# Tests (note any NEW failures vs pre-existing)
npm test
pytest

# Build (must pass)
npm run build
```

Produce summary:

```markdown
## Dead Code Removal Complete

### Removed
| # | Symbol | File | Type | Commit |
|---|--------|------|------|--------|
| 1 | unusedFunc | src/foo.ts | function | abc1234 |

### Skipped (verification failed)
| # | Symbol | File | Reason |
|---|--------|------|--------|

### Verification
- Type check: PASS/FAIL
- Tests: X passing, Y failing (Z pre-existing)
- Build: PASS/FAIL
- Total removed: N symbols across M files
- Total commits: K atomic commits
```

---

## SCOPE CONTROL

If a specific scope is provided, narrow the scan:
- File path → only that file
- Directory → only that directory
- Symbol name → only that symbol
- `all` or empty → full project scan (default)

## ABORT CONDITIONS

STOP and report if:
- More than 50 candidates found (ask user to narrow scope or confirm proceeding)
- Build breaks and cannot be fixed by reverting

**Inspired by:** [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode) remove-deadcode command
