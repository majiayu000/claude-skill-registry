---
name: bug-fix-brief
description: Generates a structured Bug Fix Brief (BFB) to document issue corrections. Includes root cause analysis, repro steps, fix options, and fix checklist. Use when user asks to create a BFB, document a bug fix, or generate a bug correction document.
allowed-tools: Read, Write, AskUserQuestion, Glob
---

# Bug Fix Brief (BFB)

## Overview

This skill generates a Bug Fix Brief (BFB): a structured document in `docs/bfb/` that uniformly captures every bug fix with root cause, repro steps, fix options, and checklist.

## When to Use

- User asks to create a BFB
- User wants to document a bug fix in a structured way
- After identifying the root cause of a bug and before implementing the fix

**Trigger:** "create BFB", "document bug", "bug fix brief", "document fix"

## Instructions

### Phase 1: Gather Information

Check existing numbering:
```bash
ls docs/bfb/ 2>/dev/null || echo "Directory does not exist"
```

Ask the user for:
- BFB number (or propose next sequential)
- Concise title (3-5 words, kebab-case)
- Issue link (e.g. #1287)
- Environment (Prod/Stg/Dev) + version
- Observed vs expected behavior
- File/function/line of the cause

### Phase 2: Generate Template

Complete the full BFB template:

```markdown
## BFB-XXX: [Title]

**Reference:** [Issue link]
**Environment:** [Env] `vX.Y.Z`
**Date:** YYYY-MM-DD

---

### 1. Bug
- **Observed:** [wrong behavior]
- **Expected:** [correct behavior]

### 2. Repro
```
1. ...
2. ...
→ [error/output]
```

### 3. Cause
`path/file.ext` — `function()` @ line N
[Why it happens, max 3 lines]

### 4. Decision
| Option | Fix | Choice |
|--------|-----|--------|
| A | [desc] | ✅/❌ |
| B | [desc] | ✅/❌ |

**Rationale:** [why]

### 5. Fix
- [ ] [change 1]
- [ ] [test]
- [ ] [verify repro]

### 6. Notes
[recurring patterns, links, warnings]
```

### Phase 3: Ask Confirmation

Show the generated BFB and ask with AskUserQuestion:
- "Create the BFB"
- "Edit before creating"
- "Cancel"

### Phase 4: Write to Disk

Only after approval:
```bash
mkdir -p docs/bfb
```

Write to `docs/bfb/BFB-XXX-title.md`

## Examples

**Input:** "create BFB for login email null crash"

**Final output:**
```markdown
## BFB-042: Login crash with null email

**Reference:** #1287
**Environment:** Prod `v2.4.1`
**Date:** 2026-05-02

---

### 1. Bug
- **Observed:** App crashes if email field is empty
- **Expected:** Error message "Email required"

### 2. Repro
```
1. Open login screen
2. Tap "Login" without entering email
→ NullPointerException @ AuthManager.kt:34
```

### 3. Cause
`AuthManager.kt` — `validateEmail()` @ line 34
Missing null check on email.trim()

### 4. Decision
| Option | Fix | Choice |
|--------|-----|--------|
| A | Add safe call `?.` | ✅ |
| B | Refactor with Result type | ❌ |

**Rationale:** Option A is minimal, zero impact.

### 5. Fix
- [ ] Add `email?.trim()?.isNotEmpty() == true`
- [ ] Test `validateEmail_null_returnsFalse()`
- [ ] Verify repro

### 6. Notes
- Check other forms for missing null checks
```

## Best Practices

1. **Sequential numbering**: BFB-001, BFB-002, no gaps
2. **Concise title**: 3-5 words, kebab-case in filename
3. **Root cause**: exact file, function, line
4. **2+ fix options**: with pros/cons and rationale
5. **Verifiable checklist**: each item must be testable

## Constraints and Warnings

- **Confirmation required**: Always ask before writing
- **Max 3 lines for cause**: Stay concise
- **Directory `docs/bfb/`**: Create if it does not exist