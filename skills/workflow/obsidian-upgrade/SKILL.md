---
name: obsidian-upgrade
description: Upgrade Obsidian wikis to latest format. Handles structure migration (phases/tasks → workstreams/specs), comment format upgrades (adding emoji prefixes), and LWW source-of-truth model. Use when user mentions "upgrade wiki", "migrate wiki", "update wiki format", or has old-format comments.
---

# Obsidian Upgrade

Audit and upgrade Obsidian wikis to the current format.

## Canonical Spec (Single Source of Truth)

**The canonical spec is `skills/obsidian-plan-wiki/SKILL.md` and its `references/` folder.**

This upgrade skill does NOT enumerate requirements. It points agents at the canonical spec and tells them to diff against it. When the canonical spec changes, this skill automatically upgrades to match.

## When to Use

- User mentions "upgrade wiki", "migrate wiki", "update wiki format"
- Wiki has old-format comments, outdated docs, or legacy structure

## Upgrade Strategy

**Launch parallel subtask agents** to audit each area. Each agent reads the canonical spec first, then diffs the existing wiki against it.

```
// Launch in parallel - each reads canonical spec then audits one area
Task(subagent_type: "general-purpose", prompt: "Audit AGENTS.md against canonical spec...")
Task(subagent_type: "general-purpose", prompt: "Audit comment format against canonical spec...")
Task(subagent_type: "general-purpose", prompt: "Audit directory structure against canonical spec...")
Task(subagent_type: "general-purpose", prompt: "Audit reference files against canonical spec...")
Task(subagent_type: "general-purpose", prompt: "Audit wiki links...")
```

Collect all findings, then present one unified upgrade plan.

---

## 1. AGENTS.md Audit (CRITICAL)

**Most important check.** Outdated agent instructions cause wrong output.

```
Task(
  subagent_type: "general-purpose",
  prompt: "Audit docs/AGENTS.md against canonical spec.

  FIRST: Read the canonical spec completely:
  - skills/obsidian-plan-wiki/SKILL.md (entire file, especially AGENTS.md Template section)
  - ALL files in skills/obsidian-plan-wiki/references/

  THEN: Read docs/AGENTS.md completely.

  DIFF: Report every difference between existing AGENTS.md and the canonical template.
  For each difference:
  - Line number in existing file
  - What exists (quote exactly)
  - What canonical spec requires
  - Whether it's missing, outdated, or wrong

  The canonical spec is the authority. If it says something should exist, check for it.
  "
)
```

---

## 2. Comment Format Audit

```
Task(
  subagent_type: "general-purpose",
  prompt: "Audit all Obsidian comments in docs/ directory.

  FIRST: Read skills/obsidian-plan-wiki/SKILL.md section on Task Tracking with Obsidian Comments.
  Read skills/obsidian-plan-wiki/references/obsidian-open-questions-system.md if it exists.

  THEN: Find EVERY file with %% comments in docs/.

  DIFF: For each comment, check if it matches the canonical format.
  Report each violation with:
  - File path and line number
  - Current comment (quote exactly)
  - What canonical spec requires
  - Proposed fix
  "
)
```

---

## 3. Structure Audit

```
Task(
  subagent_type: "general-purpose",
  prompt: "Audit wiki directory structure in docs/.

  FIRST: Read skills/obsidian-plan-wiki/SKILL.md section on Directory Structure.

  THEN: List actual structure of docs/ directory.

  DIFF: Report differences between actual structure and canonical structure.
  Note any legacy patterns that don't match the current spec.
  "
)
```

---

## 4. Reference Files Audit

```
Task(
  subagent_type: "general-purpose",
  prompt: "Audit reference files in docs/reference/.

  FIRST: List all files in skills/obsidian-plan-wiki/references/

  THEN: Check if corresponding files exist in docs/reference/

  DIFF: For each canonical reference file:
  - If missing in docs/reference/: note as missing
  - If exists: diff content and report differences
  "
)
```

---

## 5. Broken Links Audit

```
Task(
  subagent_type: "general-purpose",
  prompt: "Audit all wiki links in docs/ directory.

  For every [[wiki-link]] found:
  1. Check if target file exists
  2. Check if anchor (#section) exists in target
  3. Check for unclosed links

  Report each broken link with file, line, and issue.
  "
)
```

---

## Upgrade Plan Format

Collect all subtask findings into one plan:

```markdown
## Upgrade Plan: [Wiki Name]

### 1. AGENTS.md Fixes (CRITICAL)
| Line | Current | Canonical Requires | Action |
|------|---------|-------------------|--------|
| ... | ... | ... | ... |

### 2. Comment Upgrades
| File | Line | Current | Canonical Format |
|------|------|---------|------------------|
| ... | ... | ... | ... |

### 3. Structure Changes
| Current | Canonical |
|---------|-----------|
| ... | ... |

### 4. Reference Files
| File | Status |
|------|--------|
| ... | missing/outdated/ok |

### 5. Broken Links
| File | Line | Link | Issue |
|------|------|------|-------|
| ... | ... | ... | ... |

### Summary
- AGENTS.md: X fixes (CRITICAL)
- Comments: Y upgrades
- Structure: Z changes
- Reference files: N missing/outdated
- Links: M broken

Approve? (y/n)
```

---

## Execution Order

1. **Structure first** (affects all paths)
2. **CLAUDE.md pointer** (quick fix)
3. **AGENTS.md documentation** (so spec is correct)
4. **Reference files** (copy from canonical if missing)
5. **Comments** (now they match the spec)
6. **Validate links** (after all moves)
7. **Report results**

---

## Validation

After upgrades, verify:

```
Task(
  subagent_type: "general-purpose",
  prompt: "Validate wiki upgrade.

  Read: skills/obsidian-plan-wiki/SKILL.md and all references/

  Then verify docs/ matches the canonical spec:
  - AGENTS.md matches template
  - Comments match format
  - Structure matches spec
  - Reference files present
  - No broken links

  Report pass/fail for each with evidence.
  "
)
```
