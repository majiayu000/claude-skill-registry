# Example: Worker Skill (context: fork)

This example shows a skill that runs in an isolated context using `context: fork`. This is the recommended pattern for auditors, validators, and any worker that needs unbiased judgment.

---

## File Structure

```
skills/validate-skill/
└── SKILL.md
```

---

## Complete SKILL.md

```markdown
---
name: validate-skill
description: "Validates skills against quality standards. Use when reviewing skill quality, checking frontmatter completeness, or verifying naming conventions. Not for code linting or type checking."
context: fork    # CRITICAL: Runs in isolated context
agent: Explore   # Read-only tools only, cannot modify files
---

# Skill Validator

You are a skill quality auditor. Your role is to validate skills against the thecattoolkit_v3 quality standards.

## Your Constraints

<critical_constraint>
You are running in an ISOLATED context (context: fork).

You CANNOT see:
- The parent conversation history
- Previous implementation attempts

This isolation ensures UNBIASED validation.
</critical_constraint>

## Validation Checklist

For each skill reviewed, check:

### Frontmatter
- [ ] `name` present and valid (max 64 chars, lowercase, hyphens only)
- [ ] `description` present, non-spoiling
- [ ] `description` includes "Use when" clause
- [ ] `description` includes "Not for" clause

### Naming
- [ ] Uses gerund form or clear noun phrase
- [ ] Lowercase only, hyphens as separators
- [ ] Not reserved words (anthropic, claude)
- [ ] Not vague names (helper, utils, worker)

### Description Quality
- [ ] Third person perspective
- [ ] Non-spoiling (doesn't reveal body content)
- [ ] Clear trigger conditions
- [ ] Clear exclusions

### Content
- [ ] Core knowledge in SKILL.md
- [ ] No time-sensitive information
- [ ] Fully qualified MCP tool names (if used)

## Output Format

Return a structured report:

```yaml
overall: PASS|FAIL
checks:
  frontmatter:
    name: PASS|FAIL
    description: PASS|FAIL
    use_when: PASS|FAIL
    not_for: PASS|FAIL
  naming:
    gerund_form: PASS|FAIL
    lowercase: PASS|FAIL
    not_vague: PASS|FAIL
  description_quality:
    third_person: PASS|FAIL
    non_spoiling: PASS|FAIL
    clear_triggers: PASS|FAIL
issues:
  - "Specific issue description"
  - "Another issue"
suggestions:
  - "Improvement suggestion"
```

## Examples

### Passing Skill

```yaml
---
name: processing-pdfs
description: "Extracts text from PDF files. Use when working with PDF documents or need text extraction. Not for image-based PDFs."
---
```

**Result**: All checks PASS

### Failing Skill

```yaml
---
name: helper
description: "This skill helps you with various tasks by providing useful functionality when you need it."
---
```

**Result**:
- `naming.not_vague`: FAIL (name is vague)
- `description_quality.non_spoiling`: FAIL (spoils that it "helps with various tasks")
- `description_quality.use_when`: FAIL (no clear "Use when" clause)

## What You Cannot Do

- ❌ Modify files (you're an Explore agent, read-only)
- ❌ See why the skill was created (isolated context)
- ❌ Be influenced by previous attempts (no history)
- ❌ Make excuses (objective validation only)

## What You Must Do

- ✅ Validate against checklist
- ✅ Return structured report
- ✅ Be objective and unbiased
- ✅ Report specific issues
```

---

## Breakdown and Explanation

### Key Frontmatter Fields

```yaml
---
context: fork    # CRITICAL: Creates isolated context
agent: Explore   # Read-only, cannot modify files
---
```

**Why `context: fork`**:
- Creates isolated "clean room" for validation
- Auditor sees only the draft, not implementation history
- Ensures unbiased judgment

**Why `agent: Explore`**:
- Explore agent has read-only tools
- Cannot accidentally modify files during validation
- Focuses on analysis, not implementation

### The critical_constraint Section

```markdown
<critical_constraint>
You are running in an ISOLATED context...
This isolation ensures UNBIASED validation.
</critical_constraint>
```

**Purpose**: Explicitly remind the agent (and readers) why isolation matters.

### Structured Output

```yaml
overall: PASS|FAIL
checks:
  frontmatter: {...}
  naming: {...}
issues: [...]
suggestions: [...]
```

**Benefits**:
- Machine-readable for automated processing
- Clear pass/fail for each category
- Specific issues for fixes
- Suggestions for improvements

---

## How It Works

### Without context: fork (Biased)

```
Main → "Create a skill"
    → Attempt 1: Creates skill with vague name
    → Inline Auditor: "Hmm, close enough, let me be lenient"
    → Result: BIASED validation, poor quality
```

### With context: fork (Unbiased)

```
Main → "Create a skill"
    → Attempt 1: Creates skill with vague name
    → Skill(validate-skill, context: fork)
        → Sees ONLY the draft file
        → Has NO knowledge of attempts
        → Returns: "naming.not_vague: FAIL"
    → Result: UNBIASED validation, high quality
```

---

## When to Use context: fork

| Use Case | Why Fork |
|:---------|:---------|
| **Auditors/Validators** | Unbiased judgment |
| **Linters** | Clean context, no history pollution |
| **Security Scanners** | Isolated from trusted code |
| **Reviewers** | Objective assessment |

### When NOT to Use context: fork

| Use Case | Why Shared |
|:---------|:-----------|
| **Expertise injection** | Want agent to see conversation history |
| **Continuation** | Building on previous work |
| **Context-dependent tasks** | Need history to function correctly |

---

## Agent Types for Workers

| Agent | Tools | Use For |
|:------|:------|:--------|
| **Explore** | Read-only | Analysis, validation, research |
| **Plan** | Read-only | Planning, architecture design |
| **general-purpose** | All tools | Implementation, execution |

**For validators**: Use `Explore` (read-only)
**For implementers**: Use `general-purpose` (can modify files)

---

## Complete Example: Manager Pattern

This worker skill is typically used within the Manager Pattern:

```
Main → Skill(skill-manager)
       → TaskList tracking
       → Task(create-skill)
           → Returns: skill draft
       → Skill(validate-skill, context: fork)
           → Returns: PASS/FAIL + issues
       → If FAIL: Retry Task(create-skill)
       → If PASS: Return to Main
```

---

## Comparison: Worker Skill vs Loadout Agent

| Aspect | Worker Skill | Loadout Agent |
|:-------|:-------------|:---------------|
| **File location** | `.claude/skills/worker/SKILL.md` | `.claude/agents/worker.md` |
| `skills:` field | Not supported | Supported |
| **Identity** | Ephemeral (task-specific) | Persistent (persona) |
| **Best for** | One-off isolated tasks | Consistent multi-skill workers |

---

## Quick Reference

### Worker Skill Template

```yaml
---
name: my-worker
description: "What it does. Use when {trigger conditions}. Not for {exclusions}."
context: fork
agent: Explore  # or Plan, general-purpose
---

# Worker Instructions

<critical_constraint>
You are running in ISOLATED context.
You CANNOT see parent conversation history.
This ensures UNBIASED execution.
</critical_constraint>

## Your Task
[Specific instructions]

## Output Format
[Structured output specification]
```

---

## Next Steps

After understanding worker skills:

1. Review `loadout-agent.md` for multi-skill bundling
2. See `quality-gate.md` for validation patterns
3. Reference `02_PATTERNS.md` for Manager Pattern details
