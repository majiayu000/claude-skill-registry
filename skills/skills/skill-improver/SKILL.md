---
name: skill-improver
description: Research and improve Claude skills with current best practices. Triggers on requests to improve skills, update skills, research best practices for skills, enhance skill quality, or modernize existing skills.
allowed-tools: WebSearch, Read, Edit, Write, Glob, Task
---

# Skill Improver

Research current best practices and improve existing Claude skills.

## Process Overview

1. Identify target skill and its domain
2. Research current best practices (web search)
3. Analyze existing skill against best practices
4. Generate improvement recommendations
5. Apply improvements (if requested)

## Step 1: Identify Target

Locate the skill to improve:

```bash
# Find skill location
ls -la .claude/skills/<skill-name>/
```

Read SKILL.md and all references to understand current implementation.

## Step 2: Research Best Practices

Use subagents (Task tool) to parallelize research across multiple topics:

```
Spawn parallel research agents for:
1. "<domain> best practices 2026"
2. "<domain> common mistakes to avoid"
3. "Claude AI <domain> techniques" (if applicable)
```

Each subagent should return:
- Key findings with sources
- Actionable recommendations

Focus areas:
- Industry standards and conventions
- Common pitfalls and how to avoid them
- Performance optimizations
- Security considerations (if relevant)
- Token efficiency for LLM skills

## Step 3: Analyze Skill

Compare existing skill against:

| Aspect | Check |
|--------|-------|
| **Clarity** | Instructions unambiguous? |
| **Completeness** | All use cases covered? |
| **Efficiency** | Minimal tokens for max utility? |
| **Accuracy** | Reflects current best practices? |
| **Triggers** | Description covers all valid triggers? |
| **Structure** | Follows skill-creator guidelines? |

## Step 4: Generate Recommendations

Create improvement report:

```markdown
## Skill Improvement Report: <skill-name>

### Summary
- Current state assessment
- Key findings from research

### Recommendations

#### High Priority
1. [Issue]: [Recommended fix]

#### Medium Priority
1. [Issue]: [Recommended fix]

#### Low Priority / Nice-to-Have
1. [Suggestion]

### Best Practices Found
- [Practice 1]: [Source]
- [Practice 2]: [Source]
```

## Step 5: Apply Improvements

If user approves changes:

1. Edit SKILL.md with improvements
2. Update/add references if needed
3. Update scripts if applicable
4. Validate with `scripts/validate_skill.py`

## Guidelines

- **Preserve intent** - Improvements should enhance, not change skill purpose
- **Cite sources** - Link to best practice sources when recommending changes
- **Prioritize impact** - Focus on changes that meaningfully improve skill quality
- **Maintain conciseness** - Don't bloat skills with unnecessary content
- **Test triggers** - Ensure description still triggers appropriately after changes

See `references/research-strategies.md` for search query templates and source evaluation guidelines.
