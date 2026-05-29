---
name: external-review
description: |
  External AI code review using Codex or Gemini.
  Reads project.yaml to determine which provider to use for frontend vs backend tasks.
  Includes hallucination detection to avoid blindly applying AI suggestions.
---

# External AI Review

## Overview

This skill provides external AI code review using Codex (OpenAI) or Gemini (Google). The provider is configured per task type (frontend/backend) in `project.yaml`.

## Prerequisites

- Codex CLI installed and authenticated (if using Codex)
- Gemini CLI installed and authenticated (if using Gemini)
- `superspec/project.yaml` configured with review settings

## Configuration

Check `superspec/project.yaml` for review settings:

```yaml
review:
  enabled: true/false              # Master switch

  frontend:
    provider: gemini               # gemini | codex | none
    model: gemini-3-pro-preview

  backend:
    provider: codex                # codex | gemini | none
    model: gpt-5.2-codex
```

## When to Use

After completing implementation (TDD cycle), if `review.enabled: true`:

1. Determine task type: `[FRONTEND]` or `[BACKEND]`
2. Read the corresponding provider config
3. If provider is not `none`, execute external review

## Review Process

### Step 1: Check Configuration

```markdown
1. Read superspec/project.yaml
2. Check if review.enabled is true
3. If false → Skip external review entirely
4. If true → Continue to Step 2
```

### Step 2: Determine Task Type

**Frontend indicators:**
- File extensions: `.tsx`, `.jsx`, `.vue`, `.css`, `.scss`, `.html`, `.svelte`
- Keywords: UI, component, page, view, form, modal, button, style, layout
- Directories: `components/`, `pages/`, `views/`, `styles/`

**Backend indicators:**
- File extensions: `.ts` (non-component), `.js` (non-component), `.py`, `.go`, `.rs`
- Keywords: API, service, controller, repository, database, auth, middleware
- Directories: `api/`, `services/`, `controllers/`, `lib/`, `utils/`

### Step 3: Execute External Review

**For Frontend tasks (provider: gemini):**

```bash
uv run ~/.claude/skills/gemini/scripts/gemini.py \
  -m gemini-3-pro-preview \
  -p "Review this frontend code for:
1. UI/UX best practices
2. Accessibility (a11y)
3. Component structure
4. CSS/styling issues
5. Performance concerns

Code to review:
$(cat [file_path])

Provide specific, actionable feedback."
```

**For Backend tasks (provider: codex):**

```bash
uv run ~/.claude/skills/codex/scripts/codex.py \
  "Review this backend code for:
1. Security vulnerabilities
2. Error handling
3. Performance issues
4. Code architecture
5. Type safety

Files: @[file_path]

Provide specific, actionable feedback." \
  gpt-5.2-codex
```

### Step 4: Hallucination Check (CRITICAL!)

**Before applying ANY suggestion from external AI, you MUST verify:**

```markdown
🔍 HALLUCINATION CHECK

For each suggestion from [Codex/Gemini]:

□ File exists?
  - Verify the file path mentioned actually exists
  - AI may reference non-existent files

□ Function/class exists?
  - Check if the mentioned symbol exists in codebase
  - AI may suggest changes to non-existent code

□ Makes sense in context?
  - Does the suggestion align with project architecture?
  - Does it match the existing code patterns?

□ Not already implemented?
  - AI may suggest something that's already done
  - Check before making duplicate changes

VERDICT:
- ✅ Validated: Apply the suggestion
- ❌ Hallucination: Ignore and document
- ⚠️ Partial: Apply with modifications
```

### Step 5: Apply Validated Fixes

Only apply suggestions that passed hallucination check:

```markdown
## Applied Changes

### From [Codex/Gemini] Review:

1. ✅ [Suggestion 1] - Applied
   - File: [path]
   - Change: [description]

2. ❌ [Suggestion 2] - Rejected (hallucination)
   - Reason: [file doesn't exist / function not found / etc.]

3. ⚠️ [Suggestion 3] - Partially applied
   - Original suggestion: [...]
   - Modified to: [...]
   - Reason: [...]
```

### Step 6: Re-submit if Needed

If significant changes were made, consider re-submitting for another review round:

```markdown
Review Loop:
1. Submit code → Get feedback
2. Hallucination check → Filter suggestions
3. Apply valid fixes
4. If major changes made → Re-submit (max 2 iterations)
5. Mark review complete
```

## TODO Structure (when external review enabled)

```markdown
--- EXTERNAL AI REVIEW ---
- [ ] Check review config (superspec/project.yaml)
- [ ] Determine task type (frontend/backend)
- [ ] Submit to [provider] for review
- [ ] Receive and document feedback
- [ ] Hallucination check for each suggestion
- [ ] Apply validated fixes only
- [ ] Re-submit if major changes (optional, max 2x)
- [ ] Document final review results
```

## Provider Comparison

| Aspect | Codex | Gemini |
|--------|-------|--------|
| **Best for** | Backend, logic, architecture | Frontend, UI/UX, design |
| **File reference** | `@file` syntax | Pass content via prompt |
| **Session resume** | Yes (SESSION_ID) | No |
| **Model** | gpt-5.2-codex | gemini-3-pro-preview |

## Common Hallucinations to Watch

| Type | Example | How to Detect |
|------|---------|---------------|
| **Ghost files** | "In src/utils/helpers.ts..." | Check if file exists |
| **Phantom functions** | "The validateUser() function..." | Search codebase |
| **Wrong imports** | "Import from @/lib/auth" | Verify import path |
| **Outdated patterns** | Suggests deprecated API | Check current version |
| **Context confusion** | Mixes up similar projects | Verify project context |

## Red Flags - NEVER Do

| Don't | Why |
|-------|-----|
| **Blindly apply all suggestions** | Hallucinations will break code |
| **Skip hallucination check** | AI confidently suggests wrong things |
| **Apply without testing** | Changes may not compile/run |
| **Ignore provider config** | User chose specific AI for reason |
| **Loop indefinitely** | Max 2 re-submission rounds |

## Integration with Phase Protocol

When using with `phase-protocol`:

```markdown
--- IMPLEMENTATION TASKS ---
- [ ] Task 1 (TDD)
- [ ] Task 2 (TDD)

--- EXTERNAL REVIEW (if enabled) ---
- [ ] External AI Review (this skill)

--- EXIT GATE ---
- [ ] Update tasks.md
- [ ] Git commit
```

## Quick Reference

```
1. Check config: review.enabled?
2. Task type: frontend or backend?
3. Get provider: review.[type].provider
4. Execute: Codex or Gemini
5. CHECK FOR HALLUCINATIONS!
6. Apply only validated suggestions
7. Re-submit if needed (max 2x)
```
