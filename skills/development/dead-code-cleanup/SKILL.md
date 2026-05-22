---
name: dead-code-cleanup
description: Identify and safely remove dead code, deprecated code, and unused exports from codebase. Use when you need to clean up unused or obsolete code.
allowed-tools: Glob, Grep, Read, Edit, Bash(npm:*), Bash(pnpm:*), Bash(yarn:*), Bash(go:*), Bash(git status:*), Bash(tsc:*), Task
disable-model-invocation: true
---

# Dead Code Cleanup Command

## Purpose

Systematically identify and remove unused code while maintaining project integrity.

**Target Code**:

- Unused exports/functions/classes with no references
- Deprecated code without active migration plan
- Orphaned files (no imports from anywhere)
- Unreachable code paths

**Critical Constraint**: Project must build and pass all tests after cleanup.

---

## User Input

```text
$ARGUMENTS
```

**Interpretation**:

| Input                      | Action                                            |
| -------------------------- | ------------------------------------------------- |
| Empty                      | Analyze entire codebase                           |
| Path (e.g., `src/legacy/`) | Analyze specified directory                       |
| `--dry-run`                | Report only, no deletions                         |
| `--auto`                   | Delete HIGH confidence items without confirmation |

---

## Preservation Rules (NEVER DELETE)

### Absolute Preservation

| Category                  | Detection Method                              | Examples                       |
| ------------------------- | --------------------------------------------- | ------------------------------ |
| **Public API**            | `package.json` exports, `index.ts` re-exports | Library entry points           |
| **Planned Features**      | TODO/FIXME with ticket/issue                  | `// TODO(#123): implement`     |
| **Framework Conventions** | Path-based (pages/, app/, api/)               | Next.js routes, NestJS modules |
| **Test Infrastructure**   | Imported by `*.test.*`, `*.spec.*`            | Fixtures, mocks, test utils    |
| **Dynamic Imports**       | `import()`, `require()` patterns              | Lazy loading, code splitting   |
| **Build Dependencies**    | Referenced in package.json scripts            | Build tools, CLI scripts       |
| **External Contracts**    | GraphQL types, API schemas                    | Schema definitions             |

### Special Cases

**Exported but unused internally**:

- Public library → PRESERVE (external consumers unknown)
- Private app → Flag for review

**Deprecated with timeline**:

- Deadline NOT passed → PRESERVE
- Deadline passed + no usage → DELETE

---

## Analysis Workflow

### Phase 1: Context Gathering

**1.1 Detect Project Type**

```bash
# Framework detection
[ -f "next.config.js" ] && echo "Next.js"
[ -f "tsconfig.json" ] && echo "TypeScript"
[ -f "go.mod" ] && echo "Go"
```

**1.2 Identify Package Scope**

```bash
# Public library vs private app
grep '"private": false' package.json && echo "PUBLIC_LIBRARY"
```

**1.3 Map Public API Surface**

- Check `package.json` exports field
- Find `index.ts` re-exports
- List Go exported symbols (capital letter)

### Phase 2: Dead Code Detection

**2.1 Unused Exports**

For each export statement:

1. Search for import references across codebase
2. Check dynamic import patterns
3. Verify not in public API surface

**2.2 Deprecated Code**

```bash
grep -rn "@deprecated" --include="*.ts" --include="*.go"
grep -rn "DEPRECATED" --include="*.ts" --include="*.go"
```

Evaluate:

- Has migration deadline? Check if passed
- Has replacement? Check usage migrated
- No timeline? Flag for review

**2.3 Orphaned Files**

Files not imported anywhere:

- Exclude: entry points, config files, scripts
- Exclude: test files, type declarations
- Flag: utility files with no imports

**2.4 Unreachable Code**

- Code after return/throw
- Always-false conditions
- Dead switch cases

### Phase 3: Validation

**For each candidate**:

1. **Cross-reference check**: Search all possible import patterns
2. **String reference check**: Filename as string (dynamic loading)
3. **Comment reference check**: TODO/FIXME mentioning future use
4. **Preservation rule check**: Apply rules from above

**Confidence Classification**:

| Level  | Criteria                                      | Action                      |
| ------ | --------------------------------------------- | --------------------------- |
| HIGH   | No references, not preserved, clear dead code | Auto-delete (with `--auto`) |
| MEDIUM | No direct refs, but string/comment mentions   | Ask confirmation            |
| LOW    | Exported publicly, ambiguous usage            | Report only                 |

### Phase 4: Safe Deletion

**4.1 Pre-Deletion**

```bash
# Warn if uncommitted changes
git status --porcelain | grep -q . && echo "⚠️ Uncommitted changes exist"
```

**4.2 Incremental Deletion**

- Delete in batches (5-10 items)
- Verify after each batch
- Stop on first failure

**4.3 Post-Deletion Verification**

```bash
# Must pass after each batch
{build_command}  # npm run build / go build ./...
{test_command}   # npm test / go test ./...
{lint_command}   # npm run lint / golangci-lint run
```

**4.4 Rollback on Failure**

```bash
git checkout -- {failed_files}
```

---

## Output Format

### Progress Updates (During Analysis)

```markdown
🔍 Analyzing codebase...

**Project**: TypeScript (Next.js)
**Scope**: Entire codebase
**Mode**: Standard

---

## Context ✓

- Public API: 12 exports in src/index.ts
- Framework: Next.js (preserving pages/, app/, api/)
- Test utils: 5 shared utilities

## Detection Progress

- Scanning exports... (45/120)
- Checking deprecated markers...
```

### Final Report

```markdown
# 🧹 Dead Code Cleanup Report

**Generated**: {timestamp}
**Scope**: {analyzed_paths}

---

## 📊 Summary

| Category        | Count   | Lines       |
| --------------- | ------- | ----------- |
| Unused Exports  | {n}     | {lines}     |
| Deprecated Code | {n}     | {lines}     |
| Orphaned Files  | {n}     | {lines}     |
| **TOTAL**       | **{n}** | **{lines}** |

---

## 🔴 DELETED (HIGH Confidence)

### {file_path}:{line}

- **Type**: {function/class/variable}
- **Reason**: No references found
- **Verification**: Build ✓ Tests ✓

---

## 🟡 SKIPPED - Needs Review

### {file_path}:{line}

- **Type**: {function/class/variable}
- **Reason**: {why detected as dead}
- **Skip Reason**: {why preserved}
- **Action**: {recommended next step}

---

## 🟢 PRESERVED (Matched Rules)

### {file_path}:{line}

- **Rule**: {which preservation rule}
- **Detail**: {specifics}

---

## ⚠️ MANUAL REVIEW REQUIRED

Items requiring human decision:

1. **{file_path}:{line}**
   - Detected: {what was found}
   - Concern: {why uncertain}
   - Suggestion: {recommended action}

---

## ✅ Verification Results

- Build: {PASS/FAIL}
- Tests: {PASS/FAIL} ({passed}/{total})
- Lint: {PASS/FAIL}

---

## 📋 Next Steps

### Immediate

- [ ] Review {n} SKIPPED items
- [ ] Investigate {n} MANUAL REVIEW items

### Recommended

- [ ] Add deprecation notices before removing LOW confidence items
- [ ] Update documentation for removed APIs
- [ ] Configure lint rules to prevent future dead code

---

## 📝 Session Summary

- Analyzed: {total_files} files, {total_lines} lines
- Deleted: {deleted_count} items ({deleted_lines} lines)
- Skipped: {skipped_count} items (see reasons above)
- Preserved: {preserved_count} items (matched rules)
```

---

## Key Rules

### ✅ Must Do

- Run build + tests after EVERY deletion batch
- Document skip reasons for every preserved item
- Report all skipped items in final summary
- Preserve items matching preservation rules

### ❌ Must Not Do

- Delete without verification
- Ignore preservation rules
- Skip final report generation
- Batch too many deletions (max 10 per batch)

### 🛡️ Safety First

- When uncertain → SKIP and report
- When ambiguous → Ask user
- When build fails → Rollback immediately

---

## Execution Instructions

### Step 1: Parse Input

- Check for `--dry-run`, `--auto` flags
- Determine target path (default: entire codebase)

### Step 2: Safety Check

```bash
git status --porcelain
```

- Warn if uncommitted changes exist
- Suggest: "Consider committing or stashing changes first"

### Step 3: Context Gathering (Phase 1)

1. Detect project type and framework
2. Identify if public library
3. Map public API surface
4. List test infrastructure

### Step 4: Detection (Phase 2)

For TypeScript/JavaScript:

```bash
# Find exports
grep -rn "export \(function\|class\|const\|interface\|type\)" src/

# For each, check imports
grep -r "import.*{.*ExportName.*}" --exclude-dir=node_modules
```

For Go:

```bash
# Find exported symbols
grep -rn "^func [A-Z]" --include="*.go"
grep -rn "^type [A-Z]" --include="*.go"
```

### Step 5: Validation (Phase 3)

For each candidate:

1. Run cross-reference checks
2. Apply preservation rules
3. Classify confidence level

### Step 6: Action (Phase 4)

Based on mode:

- `--dry-run`: Generate report only
- `--auto`: Delete HIGH confidence, report rest
- Default: Ask confirmation for each deletion

### Step 7: Verification

After each batch:

```bash
# Detect package manager and run
npm run build && npm test
# OR
pnpm build && pnpm test
# OR
go build ./... && go test ./...
```

### Step 8: Final Report

Generate comprehensive report with:

- All deleted items
- All skipped items with reasons
- All preserved items with rules
- Manual review recommendations
- Verification results

**CRITICAL**: Always include skipped items in final report.

---

## Example Usage

```bash
# Report only (no deletions)
/dead-code-cleanup --dry-run

# Analyze specific directory
/dead-code-cleanup src/legacy/

# Auto-delete HIGH confidence items
/dead-code-cleanup --auto

# Default: interactive mode
/dead-code-cleanup
```

---

## Troubleshooting

### False Positives

**Symptom**: Code flagged but actually needed

**Check**:

- Dynamic imports with variables
- Framework lifecycle methods
- External consumer usage

### Build Failures

**Action**:

1. Rollback: `git checkout -- .`
2. Review failed item
3. Add to preservation rules if legitimate

### Missed Dead Code

**Solutions**:

- Check if matches preservation rules incorrectly
- Run with more aggressive grep patterns
- Manual verification
