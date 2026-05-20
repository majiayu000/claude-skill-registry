---
name: create-skill
description: >-
  Create new Standard Operating Procedure documents following project standards.
  Use when documenting new processes, workflows, or guidelines.
  Invoked by: "new process", "create sop", "document process", "new workflow",
  "create documentation", "new sop", "create skill".
---

# SOP Creation SOP

**Version**: 1.0.0
**Last Updated**: 2026-01-11
**Status**: Active

---

## Overview

### Purpose
This guide provides a standardized approach for creating new Standard Operating Procedure (SOP) documents. It ensures consistency across all process documentation, making SOPs easy to follow, maintain, and adapt into Claude Code skills.

### When to Use
**ALWAYS**: Creating new processes, documenting existing workflows, establishing guidelines, creating templates, defining procedures
**SKIP**: Quick notes, temporary documentation, one-off instructions

---

## YAML Frontmatter Reference

Every skill file (SKILL.md) must begin with YAML frontmatter. This section documents all available fields based on official Claude Code documentation.

### Available Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | No | Display name for the skill. Defaults to directory name. Lowercase letters, numbers, and hyphens only (max 64 characters). |
| `description` | Recommended | What the skill does and when to use it. Claude uses this to decide when to apply the skill. |
| `argument-hint` | No | Hint shown during autocomplete. Example: `[issue-number]` or `[filename] [format]`. |
| `disable-model-invocation` | No | Set to `true` to prevent Claude from automatically loading this skill. Default: `false`. |
| `user-invocable` | No | Set to `false` to hide from the `/` menu. Default: `true`. |
| `allowed-tools` | No | Tools Claude can use without asking permission when this skill is active. |
| `model` | No | Model to use when this skill is active. |
| `context` | No | Set to `fork` to run in a forked subagent context. Only use for isolated tasks. |
| `agent` | No | Which subagent type to use when `context: fork` is set. See Agent Types below. |
| `hooks` | No | Hooks scoped to this skill's lifecycle. |

### Agent Types (for `context: fork`)

When using `context: fork`, the `agent` field specifies which agent runs the skill:

**Built-in Agents:**
| Agent | Description |
|-------|-------------|
| `general-purpose` | Default agent with full tool access. Used if `agent` is omitted. |
| `Explore` | Read-only agent optimized for codebase exploration (Glob, Grep, Read). |
| `Plan` | Planning agent for designing implementation approaches. |

**Custom Agents:**
Reference any agent defined in `.claude/agents/` by path:
```yaml
agent: mobile/engineer    # Uses .claude/agents/mobile/engineer/AGENT.md
agent: backend/architect  # Uses .claude/agents/backend/architect/AGENT.md
```

### Important Notes

- **Only `description` is recommended**; all other fields are optional
- **`context: fork` runs the skill in isolation WITHOUT conversation context** - use sparingly and only for truly isolated tasks
- **`agent` only matters when `context: fork` is set** - it has no effect on inline skills
- **Most skills should NOT have `context` or `agent`** - they should run inline with full conversation context

### Example: Inline Skill (Most Common)

Most skills should run inline, maintaining conversation context:

```yaml
---
name: my-skill
description: >-
  What this skill does.
  Invoked by: "trigger phrase 1", "trigger phrase 2".
---
```

### Example: Forked/Isolated Skill (Use Sparingly)

Only use forked context for tasks that truly need isolation:

```yaml
---
name: heavy-analysis
description: Run deep analysis in isolation
context: fork
agent: Explore
allowed-tools: Read, Grep, Glob
---
```

### When to Use `context: fork`

**Use forked context when:**
- The task is completely self-contained and needs no prior context
- You want to run a long-running analysis without blocking the main conversation
- The task should not affect or be affected by the current conversation state

**Do NOT use forked context when:**
- The skill needs to reference previous conversation messages
- The skill modifies files that the user is actively working on
- The skill needs to ask follow-up questions or clarifications

---

## Quick Start

### Creating a New SOP

1. **Choose Location**: `/docs/processes/{category}/` where category is:
   - `development/` - Development workflows
   - `design/` - Design and research processes
   - `tests/` - Testing procedures
   - `code_review/` - Review processes
   - `troubleshooting/` - Diagnostic guides
   - `git/` - Version control processes

2. **Name the File**: Use snake_case with descriptive name
   ```
   {category}_{process_name}_process.md
   ```
   Examples: `code_review_process.md`, `testing_process.md`

3. **Use the Template**: Copy [SOP_TEMPLATE.md](SOP_TEMPLATE.md) and fill in sections

4. **Review Checklist**:
   - [ ] All placeholder text replaced
   - [ ] Metadata section complete
   - [ ] At least 2 phases defined
   - [ ] Quality checks added
   - [ ] Troubleshooting section populated
   - [ ] Related documents linked

---

## Process Workflow

### Flow Diagram
```
[Identify Need] --> [Choose Category & Name] --> [Copy Template]
       |
[Fill Metadata] --> [Define Phases] --> [Add Examples]
       |
[Add Troubleshooting] --> [Link Related Docs] --> [Review]
       |
[Publish] --> [Consider Skill Conversion]
```

### Phase Summary
| Phase | Objective | Deliverable | Duration |
|-------|-----------|-------------|----------|
| 1. Planning | Identify scope and structure | Outline with phases | 15-30 min |
| 2. Drafting | Write core content | Complete draft | 1-2 hours |
| 3. Review | Verify completeness | Finalized SOP | 30-60 min |
| **Total** | | | **2-4 hours** |

---

## Phase 1: Planning

**Objective**: Define the scope, structure, and key phases of the SOP
**Duration**: 15-30 minutes

### Step 1.1: Identify the Process

1. Answer these questions:
   - What problem does this process solve?
   - Who will use this process?
   - What is the expected outcome?
   - How often will it be used?

2. Define the scope:
   - What is covered by this SOP?
   - What is explicitly NOT covered?
   - What prerequisites exist?

### Step 1.2: Structure the Phases

1. Break the process into 2-5 logical phases
2. Each phase should:
   - Have a clear objective
   - Produce a deliverable
   - Have estimable duration
   - Be independently verifiable

### Deliverable
**Output**: Process outline with phases defined

**Quality Check**:
- [ ] Process has clear purpose
- [ ] Scope is well-defined
- [ ] 2-5 phases identified
- [ ] Each phase has clear output

---

## Phase 2: Drafting

**Objective**: Write the complete SOP content
**Duration**: 1-2 hours

### Step 2.1: Fill Metadata

```markdown
# [Process Name] Process Guide

**Version**: 1.0.0
**Last Updated**: YYYY-MM-DD
**Status**: Active
**Document Type**: Process Guide
**Project**: {Project Name}
```

### Step 2.2: Write Overview Section

Include:
- Purpose (2-3 sentences)
- Scope (Covered / NOT Covered)
- When to Use (ALWAYS / SKIP)
- Summary (2-3 paragraphs)

### Step 2.3: Write Phase Sections

For each phase:
```markdown
## Phase N: [Phase Name]

**Objective**: [Clear statement]
**Duration**: [Time estimate]

### Step N.1: [Step Name]
1. Action 1
2. Action 2

### Deliverable
**Output**: [What this phase produces]

**Quality Check**:
- [ ] Criterion 1
- [ ] Criterion 2
```

### Step 2.4: Add Supporting Sections

- Quick Reference (commands, file locations)
- Troubleshooting table
- Related Documentation links
- Changelog

### Deliverable
**Output**: Complete SOP draft

**Quality Check**:
- [ ] All sections filled
- [ ] No placeholder text remains
- [ ] Commands are correct
- [ ] Links are valid

---

## Phase 3: Review

**Objective**: Verify completeness and quality
**Duration**: 30-60 minutes

### Step 3.1: Self-Review

Use the SOP Quality Checklist:

**Structure**:
- [ ] Has YAML-like metadata header
- [ ] Has Overview section with Purpose, Scope, When to Use
- [ ] Has Process Workflow with diagram
- [ ] Has 2+ Phase sections
- [ ] Has Quick Reference section
- [ ] Has Troubleshooting section
- [ ] Has Related Documentation section
- [ ] Ends with "End of Document" marker

**Content**:
- [ ] Purpose is clear (answers "why")
- [ ] Scope is defined (covered / not covered)
- [ ] When to Use has ALWAYS and SKIP conditions
- [ ] Each phase has objective, steps, deliverable, quality check
- [ ] Commands are tested and correct
- [ ] File paths are accurate

**Style**:
- [ ] Uses consistent heading levels
- [ ] Uses markdown formatting correctly
- [ ] No spelling/grammar errors
- [ ] Action items use imperative verbs

### Step 3.2: Consider Skill Conversion

If this SOP should become a Claude Code skill:
1. Create skill in `.claude/skills/{skill-name}/`
2. Extract core workflow into SKILL.md
3. Use progressive disclosure for details
4. Add YAML frontmatter with triggers

### Deliverable
**Output**: Finalized, reviewed SOP

**Quality Check**:
- [ ] All checklist items pass
- [ ] Ready for publication
- [ ] Skill conversion assessed

---

## SOP Quality Checklist

### Required Sections

| Section | Required | Purpose |
|---------|----------|---------|
| Title + Metadata | Yes | Version, date, status |
| Overview | Yes | Purpose, scope, when to use |
| Process Workflow | Yes | Visual flow, phase summary |
| Phase 1-N | Yes | Step-by-step instructions |
| Quick Reference | Recommended | Commands, file locations |
| Troubleshooting | Recommended | Common issues and solutions |
| Related Documentation | Yes | Links to related SOPs |
| Changelog | Recommended | Version history |

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| SOP File | `{category}_{name}_process.md` | `code_review_process.md` |
| Skill Folder | `{prefix}-{name}` | `review-code` |
| Skill File | `SKILL.md` | `SKILL.md` |
| Template File | `{NAME}_TEMPLATE.md` | `SOP_TEMPLATE.md` |

### Status Values

| Status | Meaning |
|--------|---------|
| Draft | In development, not ready for use |
| Active | Current, approved for use |
| Deprecated | Being phased out, use alternative |
| Archived | Historical reference only |

---

## Quick Reference

### File Locations

| Type | Location |
|------|----------|
| Process SOPs | `/docs/processes/{category}/` |
| Setup Docs | `/docs/SETUP_*.md` |
| Reference Docs | `/docs/*.md` |
| Skills | `/.claude/skills/` |

### Template Location

Full SOP template: [SOP_TEMPLATE.md](SOP_TEMPLATE.md)

### Skill Names (New Convention)

| Name | Domain | Location |
|------|--------|----------|
| `create-skill` | Meta/documentation | shared/ |
| `dev-feature` | Development workflows | shared/ |
| `design-research` | Design/research | shared/ |
| `git-pr` | Git operations | shared/ |
| `setup-dev` | Environment setup | {domain}/ |
| `setup-env` | Environment variables | {domain}/ |
| `test` | Testing | {domain}/ |
| `review-code` | Code review | {domain}/ |
| `deploy` | Deployment | {domain}/ |
| `help` | Troubleshooting | {domain}/ |

---

## Troubleshooting

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Template not found** | Can't locate SOP_TEMPLATE.md | Check `.claude/skills/shared/create-skill/SOP_TEMPLATE.md` |
| **Unclear scope** | Process covers too much | Break into multiple SOPs |
| **Too detailed** | SOP over 500 lines | Use progressive disclosure with linked files |
| **Missing examples** | Users struggle to follow | Add concrete examples for each phase |
| **Outdated content** | Process has changed | Update SOP and increment version |

### When to Escalate
- Process spans multiple teams
- Requires external tool integration
- Conflicts with existing SOPs

---

## Related Skills

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `/dev-feature` | Feature development workflow | Creating feature documentation |
| `/design-research` | Research and design process | Researching before documenting |

> **Note**: Skill paths (`/skill-name`) work after deployment. In the template repo, skills are in domain folders.

---

**End of SOP**
