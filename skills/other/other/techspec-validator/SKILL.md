---
name: techspec-validator
description: Phase 2.5 — Automatic TechSpec validation after generation. Verifies file paths exist, checks interface consistency, detects breaking changes, validates new dependencies, and verifies PRD→TechSpec coverage. Generates techspec-validation.md in the state directory.
---

# TechSpec Validator

Runs **automatically as Phase 2.5**, between TechSpec generation and Tasks generation.
Purpose: catch implementation impossibilities before they become broken tasks.

## Position in flow

```
[PRD Validation]
      ↓
TechSpec generation
      ↓
[TechSpec Validation]  ← THIS SKILL
      ↓
Tasks generation
```

## Entry conditions

- `techspec.md` must exist in `tasks/prd-{slug}/` (run TechSpec generation first)
- `prd.md` must exist for coverage matrix validation
- Generates `techspec-validation.md` and saves to `.claude/feature-state/{slug}/`
- Load if already exists (resume flow)
- Can be forced with `--revalidate`

---

## Validation 1: File Paths and Imports

For every file path, import, and module reference mentioned in the TechSpec:

### What to check
- Explicit paths: `"add method to lib/firebase-admin.ts"` → Glob for `**/firebase-admin.ts`
- Import statements: `"import from @/components/shared/Button"` → Glob for `**/Button.{ts,tsx,swift,rs,py,go}`
- Directory references: `"create file in src/api/users/"` → verify parent directory exists

### Search commands

```bash
# Check file existence:
ls -la "{exact-path}" 2>/dev/null

# Search for file by name:
find . -name "{filename}" -not -path "*/node_modules/*" 2>/dev/null | head -5

# Or with glob patterns:
# Glob: **/{filename}.{ts,tsx,swift}
```

### Classification
- **File found** → ✅ Pass
- **Parent directory found but file missing** → ⚠️ Warning: "File will be created (parent dir exists)"
- **Neither file nor parent found** → ❌ Blocker: "Path does not exist in codebase"

---

## Validation 2: Interface and Type Consistency

Compare types and field names proposed in the TechSpec Data Model against the codebase:

### Naming consistency check

Extract field names from TechSpec Data Model section and grep for same concepts in codebase:

```bash
# Example: TechSpec proposes { userId: string }
# Check what the codebase actually uses:
grep -r "userId\|uid\b" . --include="*.ts" --include="*.swift" -l | head -10
```

| TechSpec term | Codebase term | Action |
|--------------|---------------|--------|
| Same | Same | ✅ Pass |
| Different (e.g., `userId` vs `uid`) | Inconsistent | ⚠️ Warning with suggested alignment |
| New type, no codebase match | New entity | ⚠️ Note: "New type will be introduced" |

### Type existence check
For each type/interface mentioned (e.g., `UserProfile`, `TrainerConnection`):

```bash
grep -r "interface {TypeName}\|type {TypeName}\|struct {TypeName}\|class {TypeName}" . \
  --include="*.ts" --include="*.swift" --include="*.rs" --include="*.go" -l
```

- Found → ✅ Pass
- Not found → ⚠️ Warning: "Type does not exist yet — will be created"

---

## Validation 3: Breaking Change Detection

Scan TechSpec for changes to **existing** functions, APIs, schemas, or types.

### Breaking change patterns to detect

| Pattern in TechSpec | Detection |
|--------------------|-----------|
| "change X field to Y" | Field rename → ❌ Blocker |
| "remove X field" | Field removal → ❌ Blocker |
| "update function signature of X" | API change → ❌ Blocker |
| "change return type of X" | Type change → ❌ Blocker |
| "rename X to Y" | Rename → ❌ Blocker |
| "deprecate X" | Deprecation → ⚠️ Warning |
| "add optional field X" | Additive change → ✅ Pass |
| "add new endpoint" | New addition → ✅ Pass |

### Breaking change requirement

For each detected breaking change, the TechSpec **must** include a migration plan:

```
TechSpec says: "rename uid to userId in User collection"
Check: Is there a Migration section or migration steps?
  → Yes: ✅ Breaking change documented
  → No:  ❌ Blocker: "Breaking change requires migration plan in TechSpec"
```

Keywords that indicate a migration plan is present: `migration`, `migrate`, `backward compatible`, `deprecation period`, `data migration`.

---

## Validation 4: New External Dependencies

Scan TechSpec for new library/package references not currently in the project:

### Detection

Extract library names from TechSpec (mentions of `npm install`, `pip install`, `cargo add`, `import X from 'Y'` for unknown Y).

For each new dependency:

```bash
# Node.js:
cat package.json | grep "{library-name}"

# Rust:
cat Cargo.toml | grep "{library-name}"

# Python:
cat requirements.txt | grep "{library-name}"

# Swift:
cat Package.swift | grep "{library-name}"
```

### Classification
- **Already in project** → ✅ Pass
- **Not in project, well-known library** → ⚠️ Warning: "New dependency: {name}. Requires installation."
- **Not in project, unknown/niche library** → ❌ Blocker: "Unknown dependency requires explicit approval"

When flagging new dependencies, note:
- Approximate bundle size if known (for frontend libs)
- License type if known (MIT, Apache, GPL, etc.)
- Whether it's dev-only or production dependency

---

## Validation 5: Internal Consistency

Check that sections of the TechSpec are internally consistent:

### Data Model ↔ Component Design
- Fields mentioned in Component Design match fields defined in Data Model
- If Component Design references a field not in Data Model → ⚠️ Warning

### API Changes ↔ Data Model
- API response shapes reflect the Data Model
- New fields returned by API exist in Data Model
- If mismatch → ⚠️ Warning with specific field names

### Error Handling ↔ Component Design
- Every external call in Component Design should have a corresponding failure mode in Error Handling
- If an external call has no error handling → ⚠️ Warning

---

## Validation 6: PRD → TechSpec Coverage

Cross-reference every functional requirement in `prd.md` with the TechSpec:

### Coverage check

For each functional requirement (FR) in the PRD:

1. Extract the FR text
2. Search TechSpec for implementation coverage (by keyword match)
3. Mark as covered or missing

### Coverage matrix output

```markdown
| PRD Requirement | TechSpec Section | Status |
|-----------------|------------------|--------|
| FR-1: User can connect with trainer | Component Design §2 — ConnectionService | ✅ Covered |
| FR-2: Connection stored in Firestore | Data Model §1 — connections collection | ✅ Covered |
| FR-3: Trainer sees connected students list | — | ❌ Missing |
```

### Missing coverage = Blocker

If any functional requirement has no corresponding TechSpec coverage:
- ❌ Blocker: "FR-{N}: '{requirement text}' has no technical implementation in TechSpec"

---

## Behavior

| Finding type | Effect |
|--------------|--------|
| ✅ Pass | Continue silently |
| ⚠️ Warning | Present to user, ask if they want to fix before continuing. Can be dismissed. |
| ❌ Blocker | **Stop the flow**. User must correct before Tasks generation. |

### User interaction for blockers

```
❌ TechSpec Validation Failed — cannot proceed to Tasks generation

Blocker 1: Import path not found: @/components/shared/Button
  The component does not exist at this path. Options:
  A) Create the component first (add to TechSpec as a new task)
  B) Update the import path if it exists elsewhere

Blocker 2: Breaking change in GET /api/users — response shape changed
  No migration plan found in TechSpec.
  → Add a Migration section describing backward compatibility or migration steps.

Blocker 3: FR-3 from PRD ("Trainer sees connected students") has no TechSpec coverage
  → Add implementation for this requirement to TechSpec.

Would you like me to update the TechSpec to address these? [Yes / Let me fix manually / Show full report]
```

### User interaction for warnings only

```
⚠️ TechSpec Validation — warnings found (non-blocking)

• Naming inconsistency: TechSpec uses userId, codebase uses uid everywhere
  → Consider aligning to uid for consistency
• New dependency: react-pdf not in package.json (requires npm install react-pdf)
• TrainerProfile type not found — will be created as new type

Continue to Tasks generation? [Yes, continue / Let me address these first]
```

---

## Output: techspec-validation.md

Save to `.claude/feature-state/{slug}/techspec-validation.md`:

```markdown
## TechSpec Validation Report

Generated: {timestamp}
TechSpec: tasks/prd-{slug}/techspec.md

### ✅ Passed
- All file paths verified in codebase
- No breaking changes detected
- All PRD requirements have technical coverage
- No new external dependencies

### ⚠️ Warnings (non-blocking)
- Naming inconsistency: TechSpec uses userId, codebase uses uid everywhere
  → Align to uid for consistency
- New dependency: react-pdf not in package.json

### ❌ Blockers (must fix before Tasks generation)
- Import path not found: @/components/shared/Button
- FR-3 from PRD has no technical implementation in TechSpec
- Breaking change in /api/users — no migration plan

### File Path Check
| Path | Found? | Notes |
|------|--------|-------|
| lib/firebase-admin.ts | ✅ | — |
| @/components/shared/Button | ❌ | File not found |
| src/api/users/ (directory) | ✅ | New file will be created here |

### Coverage Matrix
| PRD Requirement | TechSpec Section | Status |
|-----------------|------------------|--------|
| FR-1: User can connect | Component Design §2 | ✅ Covered |
| FR-2: Store in Firestore | Data Model §1 | ✅ Covered |
| FR-3: Trainer list | — | ❌ Missing |

### Breaking Changes
| Change | Type | Migration Plan? |
|--------|------|-----------------|
| Rename uid→userId in User | ❌ Breaking | ❌ Missing |

### New Dependencies
| Library | In Project? | Size | License |
|---------|-------------|------|---------|
| react-pdf | ❌ No | ~200kb | MIT |

### Verdict
BLOCKED — fix 3 blocker(s) before proceeding to Tasks generation.
```

---

## Integration with tasks generation

When `techspec-validation.md` exists and has no blockers, tasks generation reads it for context:
- Use File Path Check to know which paths are confirmed vs new
- Use Coverage Matrix to ensure every FR has at least one task
- Flag any new dependencies as setup tasks at the beginning of the task list
