---
name: skill-creation
description: How to create new agent skills for this project. Use when proposing a new skill, documenting repeated patterns, or formalizing domain knowledge. Keywords: skill, SKILL.md, agent, create skill, new skill, meta.
compatibility: Antigravity, Claude Code, Cursor
metadata:
  version: "1.0"
  project: "stepleague"
---

# Skill Creation Skill

> **Meta-skill**: This skill explains how to create other skills.

---

## ⚠️ CRITICAL: Approval Required

**New skills MUST be created with filename `SKILL.draft.md` and require user approval before activation.**

### Pending vs Active Skills

| Filename | Meaning |
|----------|---------|
| `SKILL.draft.md` | Pending - NOT active, awaiting approval |
| `SKILL.md` | Active - approved and in use |

**Why this works**: Skill systems only recognize `SKILL.md` files. A file named `SKILL.draft.md` is ignored by agents, so the skill doesn't activate until renamed.

### Approval Workflow

1. **Create** the skill folder with `SKILL.draft.md`
2. **Notify user**: "Created draft skill `skill-name`, please review"
3. **User reviews** and approves (or requests changes)
4. **Upon approval**: Rename `SKILL.draft.md` → `SKILL.md`

```powershell
# Example: Approve a pending skill
Rename-Item ".agent\skills\my-skill\SKILL.draft.md" "SKILL.md"
```

---

## When to Create a Skill

Create a new skill when:

| Trigger | Example |
|---------|---------|
| Pattern appears 3+ times | Same API pattern in multiple routes |
| Domain knowledge is complex | Integration with external service |
| Instructions are frequently repeated | "Always do X when working with Y" |
| User explicitly requests it | "Make a skill for..." |

**Do NOT create a skill for:**
- One-off tasks
- Simple rules already in AGENTS.md
- Temporary workarounds

---

## Skill Structure

### Minimum Required

```
.agent/skills/
└── skill-name/
    └── SKILL.md  # Required
```

### With Optional Directories

```
.agent/skills/
└── skill-name/
    ├── SKILL.md           # Required - main instructions
    ├── scripts/           # Optional - executable scripts
    ├── references/        # Optional - detailed docs
    └── assets/            # Optional - templates, data files
```

---

## SKILL.md Format

### YAML Frontmatter (Required)

```yaml
---
name: skill-name              # 1-64 chars, lowercase, hyphens only
description: >                # 1-1024 chars
  What this skill does and WHEN to use it.
  Include trigger keywords for agent matching.
  Keywords: keyword1, keyword2, keyword3.
compatibility: Antigravity, Claude Code, Cursor
metadata:
  version: "1.0"
  project: "stepleague"
---
```

### Naming Rules

| Rule | Example |
|------|---------|
| Lowercase only | `api-handler` not `API-Handler` |
| Hyphens for spaces | `form-components` not `form_components` |
| 1-64 characters | Keep it short |
| Match folder name | Folder `api-handler/` → `name: api-handler` |
| No consecutive hyphens | `api-handler` not `api--handler` |

### Body Content (Markdown)

Structure the body with:

1. **Title** - `# Skill Name`
2. **Overview** - What this skill covers
3. **Critical Rules** - Most important points (use ⚠️)
4. **Patterns/Examples** - Code examples with ✅/❌
5. **Real Codebase Examples** - ⭐ See below
6. **Related Skills** - Cross-references

---

## ⭐ Best Practices for Quality Skills (CRITICAL)

### 1. Include Real Codebase Examples

**Don't just write abstract patterns.** Find actual code from the project that demonstrates the pattern.

```markdown
### Pattern 1: useSearchParams Loops (REAL EXAMPLE)

**File:** `src/hooks/useFilterPersistence.ts`

**Problem:** This was causing infinite loops on /league/[id]/leaderboard...

```typescript
// ✅ CORRECT - Hydrate-once pattern (useFilterPersistence.ts lines 77-110)
const hasHydratedRef = useRef(false);
// ... actual code from project
```
```

**How to find examples:**
1. Search codebase with `grep_search` for pattern keywords
2. View commits that fixed the issue
3. Check conversations where the pattern was applied

### 2. Use Scripts for Automation

If a skill involves repeatable tasks, add helper scripts:

```
.agent/skills/skill-name/
├── SKILL.md
└── scripts/
    ├── check-violations.sh    # Find pattern violations
    ├── generate-template.js   # Generate boilerplate
    └── README.md              # Script documentation
```

**Script Example (design-system/scripts/find-hardcoded-colors.sh):**

```bash
#!/bin/bash
# Find hardcoded Tailwind color classes in codebase
echo "Finding potential violations..."
grep -rn "bg-slate\|bg-gray\|text-slate\|text-gray" src/ --include="*.tsx"
grep -rn "border-zinc\|bg-zinc" src/ --include="*.tsx"
```

### 3. Link to Specific Files and Lines

```markdown
**File:** [`useFilterPersistence.ts`](file:///src/hooks/useFilterPersistence.ts#L77-L110)

See [submit-steps/page.tsx lines 78-82](file:///src/app/(dashboard)/submit-steps/page.tsx#L78-L82) for the fix.
```

### 4. Include Debugging Checklists

```markdown
## Debugging Checklist

When you hit [issue]:

- [ ] Check for [common cause 1]
- [ ] Check for [common cause 2]
- [ ] Try [diagnostic step]
```

### 5. Document Project-Specific Issues

```markdown
## Project-Specific Issues

| File | Issue | Fix Applied |
|------|-------|-------------|
| `useFilterPersistence` | useSearchParams loop | Hydrate-once pattern |
| `submit-steps/page.tsx` | adminLeagues loop | useMemo for array |
```

## Description Best Practices

The `description` field is crucial - it's how agents decide to activate the skill.

### Include Trigger Keywords

```yaml
# ❌ BAD: Vague
description: Helps with forms

# ✅ GOOD: Specific + Keywords
description: >
  StepLeague reusable form components with accessibility.
  Use when creating forms, inputs, selects, checkboxes.
  Keywords: form, input, FormInput, FormSelect, accessibility.
```

### Describe WHEN to Use

```yaml
description: >
  [WHAT it does]. Use when [TRIGGER CONDITIONS].
  Keywords: [relevant terms].
```

---

## Project Context References

When creating skills for this project, reference these files:

| File | Purpose |
|------|---------|
| [AGENTS.md](../../../AGENTS.md) | Master context - check if pattern exists |
| [CLAUDE.md](../../../CLAUDE.md) | Claude Code context |
| [THEME_SYSTEM.md](../../../docs/THEME_SYSTEM.md) | Design/styling patterns |
| [FORM_SYSTEM.md](../../../docs/FORM_SYSTEM.md) | Form component docs |
| [docs/prds/](../../../docs/prds/) | PRD templates and examples |

### Existing Skills to Reference

| Skill | For |
|-------|-----|
| `architecture-philosophy` | Core design principles |
| `api-handler` | API route patterns |
| `supabase-patterns` | Database/auth patterns |
| `design-system` | UI/styling patterns |
| `error-handling` | Error patterns |
| `form-components` | Form patterns |
| `prd-creation` | PRD writing |
| `project-updates` | Documentation updates |

---

## Creating a New Skill - Step by Step

### 1. Check if Skill is Needed

Before creating:
- [ ] Is this pattern used 3+ times?
- [ ] Is it complex enough to warrant a skill?
- [ ] Is it NOT already covered in AGENTS.md?
- [ ] Is it NOT already covered by an existing skill?

### 2. Create the Folder and Draft File

```
.agent/skills/new-skill-name/SKILL.draft.md   ← Draft, not SKILL.md!
```

```yaml
---
name: new-skill-name
description: [WHAT + WHEN + Keywords]
compatibility: Antigravity, Claude Code, Cursor
metadata:
  version: "1.0"
  project: "stepleague"
---

# New Skill Name

## Overview

[What this skill covers]

## Critical Rules

[Most important points]

## Patterns

[Examples with ✅/❌]

## Related Skills

- `related-skill` - Why it's related
```

### 4. Notify User for Approval

After creating:
```
Created draft skill `new-skill-name` in `.agent/skills/new-skill-name/SKILL.draft.md`.
Please review and approve. To activate: rename to SKILL.md
```

### 5. Upon Approval - Activate

Rename `SKILL.draft.md` → `SKILL.md`:

```powershell
Rename-Item ".agent\skills\new-skill-name\SKILL.draft.md" "SKILL.md"
```

---

## Checklist for New Skills

- [ ] Created in `.agent/skills/skill-name/SKILL.draft.md` ← Draft file!
- [ ] Name follows rules (lowercase, hyphens, 1-64 chars)
- [ ] Description includes trigger keywords
- [ ] References relevant project files
- [ ] Cross-references related skills
- [ ] User notified for approval
- [ ] **Renamed to `SKILL.md` only after approval**

---

## Related Skills

- `architecture-philosophy` - Principles for when to modularize
- `project-updates` - How to update docs after changes
