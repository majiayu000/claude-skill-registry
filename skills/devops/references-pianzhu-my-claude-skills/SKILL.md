---
name: references
description: '> Inherits: All rules from rules-universal.md'
---

# Skill Audit Rules

> **Inherits**: All rules from `rules-universal.md`
> **Execution Required**: Execute each check table below. Verify directory structure, frontmatter, scripts, and references.

## Table of Contents

- [Overview](#overview)
- [Skill Directory Validation](#skill-directory-validation)
- [SKILL.md Validation](#skillmd-validation)
- [Scripts Audit](#scripts-audit)
- [References Audit](#references-audit)
- [Design Principles](#design-principles)
- [Common Issues](#common-issues)

---

## Overview

**A skill is any directory containing a `SKILL.md` file.**

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter: name, description (required)
│   └── Markdown body: instructions (required)
├── scripts/      - Executable code (runtime, NO size limit)
├── references/   - Documentation (on-demand, no official limit)
├── assets/       - Output resources (not loaded)
└── [custom]/     - Any other directories
```

**CRITICAL**: Audit ALL files in skill directory by their type.

---

## Skill Directory Validation

| Check | Rule | Severity |
|-------|------|----------|
| SKILL.md exists | Required in skill root | Fatal |
| File named exactly `SKILL.md` | Case-sensitive | Fatal |
| Directory structure | scripts/, references/, assets/ if used | Info |
| No extraneous files | No README.md, CHANGELOG.md | Warning |
| All references accessible | Files exist and readable | Severe |
| Reference depth | One level deep (no nested references) | Warning |

### Full Directory Audit

Audit ALL files in skill directory by type. Report: "Total files: N, Audited: N"

---

## SKILL.md Validation

### Frontmatter

| Field | Rule | Severity |
|-------|------|----------|
| name | Required, ≤64 characters (character count, not bytes) | Severe |
| name | Lowercase letters, numbers, hyphens only | Warning |
| description | Required, ≤1024 characters (character count, not bytes; ≤500 recommended) | Severe |
| description | Must include trigger conditions | Severe |
| allowed-tools | Valid tool names, comma-separated | Warning |

### Description Quality

**Good pattern:**
```yaml
description: This skill should be used when the user asks to "specific phrase", "another phrase", mentions "keyword", or discusses topic-area.
```

**Must include:**
- Specific trigger phrases
- Keywords that indicate relevance
- Topic areas covered

**Should NOT include:**
- Implementation details
- Technical specifications
- Information belonging in body

### Body Validation

| Range | Status | Severity |
|-------|--------|----------|
| ≤500 lines | Ideal | - |
| 500-625 (≤25% over) | Acceptable | - |
| >625 lines | Should optimize | Warning |

**When body too long, check in order:**
1. Contains explanations AI knows? → Delete
2. Lengthy text vs concise examples? → Simplify
3. Repeated information? → Deduplicate
4. Excessive constraints for flexible tasks? → Simplify
5. Still too long? → Split to references/

---

## Scripts Audit

**IMPORTANT: Scripts are runtime-executed, NOT loaded into context. NO line count limits.**

| File Type | Loaded to Context | Line Limit |
|-----------|-------------------|------------|
| SKILL.md body | Yes | <500 lines (official) |
| references/*.md | Yes (on demand) | **No limit** |
| scripts/*.py | **No** (runtime) | **No limit** |
| scripts/*.sh | **No** (runtime) | **No limit** |

### Script Integrity Verification

**CRITICAL**: For composite systems, verify script integrity with source code.

#### Step 1: Identify Script Locations

| Priority | Location |
|----------|----------|
| 1 | Explicitly declared paths |
| 2 | `skills/<skill-name>/scripts/` |
| 3 | Relative paths in SKILL.md |
| 4 | Shared script directories |

#### Step 2: Declaration vs Reality Check

| Check | Requirement | Severity |
|-------|-------------|----------|
| Declared exists | All declared scripts exist | Severe |
| Undeclared scripts | Document or justify | Info |
| Function merge | Check if merged into other scripts | - |

**Function Merge Check** (Critical):
- If declared script doesn't exist, **read other scripts' source code**
- Check if declared function is implemented elsewhere
- **Result**: Not a missing issue if merged (document update needed)

#### Step 3: Script Type Classification

| Type | Purpose | Should Document? |
|------|---------|------------------|
| **Runtime** | Called during skill execution | Yes (required) |
| **Dev tools** | Development/debugging only | No (don't list) |
| **Internal helpers** | Imported by other scripts | Optional |

#### Step 4: Description Consistency

| Check | Requirement | Severity |
|-------|-------------|----------|
| Description matches code | Read source, verify function | Severe |
| Major functions documented | All exported functions | Warning |
| Brief but accurate | Not misleading | Warning |

#### Step 5: Dependency Verification

| Check | Requirement | Severity |
|-------|-------------|----------|
| Import targets exist | All imported modules exist | Fatal |
| External packages | Listed in requirements | Severe |
| Circular imports | None | Severe |

### Shell Scripts

```bash
#!/bin/bash
set -euo pipefail  # Required

# Error handling
trap 'echo "Error on line $LINENO"' ERR

# Main logic
```

| Check | Rule | Severity |
|-------|------|----------|
| Shebang line | `#!/bin/bash` or `#!/usr/bin/env bash` | Warning |
| Error handling | `set -euo pipefail` | Warning |
| Variable quoting | All variables quoted | Warning |
| Exit codes | Appropriate codes | Info |

### Python Scripts

```python
#!/usr/bin/env python3
"""Script description."""

import sys

def main():
    try:
        # Main logic
        pass
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

| Check | Rule | Severity |
|-------|------|----------|
| Shebang | `#!/usr/bin/env python3` | Warning |
| Error handling | try/except for critical ops | Warning |
| Specific exceptions | No bare `except:` | Warning |
| No hardcoded secrets | Use environment variables | Severe |
| Path traversal | Sanitize file paths | Severe |

### Script Should NOT Check

- File length/line count (NO limit)
- TOC requirement (not needed for code)
- Style preferences (design choice)

---

## References Audit

**Purpose**: Documentation loaded on-demand

> **Official guidance**: "Keep individual reference files focused. Agents load these on demand, so smaller files mean less use of context." — No official line limit.

### Size Evaluation (Content-Based)

**No hardcoded limit.** Evaluate based on content nature:

| Question | If Yes |
|----------|--------|
| Does content have indivisible integrity? | Do not flag size |
| Would splitting cause functional risk? | Do not flag size |
| Is there obvious redundancy? | Suggest trimming |
| Can content be split without impact? | Suggest splitting |

### Requirements

| Check | Rule | Severity |
|-------|------|----------|
| Referenced in SKILL.md | Clear "when to read" instructions | Warning |
| No duplication | Not duplicated in SKILL.md body | Info |
| TOC for large files | Files >100 lines have TOC | Info |
| One level deep | No nested references | Warning |

### "When to Read" Pattern

**Good:**
```markdown
## Reference Files

Read `references/api-spec.md` when:
- User asks about API endpoints
- Generating API-related code

Read `references/error-codes.md` when:
- Encountering error codes
- User reports specific errors
```

**Bad:**
```markdown
See references/ for more information.
```

---

## Design Principles

### Universality & Portability

| Check | Rule | Severity |
|-------|------|----------|
| No hardcoded language content | Use variables/templates | Warning |
| No environment-specific paths | Use relative paths or config | Severe |
| Configurable behavior | Key behaviors configurable | Info |

### AI Executor Awareness

> **Full details**: See `methodology-core.md` → AI Capability Model
> **Full LLM checks**: See `rules-universal.md` → LLM Prompting Best Practices
> **Multi-phase checks**: See `type-prompt.md` → Conversational/Multi-Phase Prompt Rules

| Check | Rule | Severity |
|-------|------|----------|
| Avoid over-specification | Don't specify what AI can infer | Warning |
| Use semantic labels | Semantic placeholders vs hardcoded strings | Warning |
| Trust AI judgment | Guidelines over rigid rules | Info |
| Verbosity constraints | Explicit output length limits | Warning |
| Scope boundaries | Clear prohibition constraints | Warning |
| Tool preference | Prefer tools over internal knowledge | Warning |
| Agentic updates | Brief updates at major phases (if agentic) | Warning |
| Long-context outline | For >10k tokens: outline, restatement | Warning |
| Constraint centralization | If multi-phase: critical rules in ≤3 locations | Severe |
| Stop condition strength | If multi-phase: strong stop language at phase gates | Severe |
| Prohibition language | Strong language for critical constraints | Warning |

### When Hardcoding is Acceptable

**Do NOT flag:**
- License/copyright notices
- Brand names
- Technical specifications
- Code examples (syntax, not content)
- Regex for technical patterns

**DO flag:**
- User-facing messages
- Error messages shown to users
- Output templates with fixed language
- UI labels

---

## Common Issues

### Should Flag

| Issue | Severity |
|-------|----------|
| File not named `SKILL.md` | Fatal |
| Missing name/description | Fatal/Severe |
| name >64 chars, description >1024 chars | Severe |
| Description missing trigger conditions | Severe |
| Trigger conditions in body instead of description | Warning |
| Body >625 lines without optimization | Warning |
| References not mentioned in SKILL.md | Warning |
| Deep reference nesting (>1 level) | Warning |
| Script without error handling | Warning |
| Hardcoded paths in scripts | Severe |

### Should NOT Flag

| Pattern | Reason |
|---------|--------|
| Body 500-625 lines | Acceptable range |
| Using references/ | Good practice |
| Optional fields missing | Optional |
| Style variations | Design choice |
| Script file length | No limit for scripts |
| License headers | Intentional |
