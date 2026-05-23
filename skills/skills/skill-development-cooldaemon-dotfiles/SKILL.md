---
name: skill-development
description: Guidelines for creating Claude Code skills. Use when creating new skills, reviewing skill structure, or improving existing skills. Based on Anthropic's official skill development guide.
durability: encoded-preference
---

# Skill Development Guidelines

## Before You Start

Define 2-3 concrete use cases before writing:
1. What does a user want to accomplish?
2. What multi-step workflows does this require?
3. What domain knowledge should be embedded?

> **Scale awareness**: This repo has 30+ active skills. Every new skill adds ~100 tokens of description scanning to every prompt. Before creating a new skill, check if an existing skill can be extended instead.

### Skill Categories

| Category | Use Case | Key Techniques |
|----------|----------|----------------|
| Document & Asset Creation | Consistent output (docs, code, designs) | Templates, style guides, quality checklists |
| Workflow Automation | Multi-step processes | Step ordering, validation gates, iterative loops |
| MCP Enhancement | Workflow guidance for tools | Coordinates MCP calls, embeds domain expertise |

See `references/workflow-patterns.md` for 5 common skill patterns.

### Skill Durability

Skills also differ in how long they remain useful:

| Class | Definition | Examples | Maintenance |
|-------|-----------|----------|-------------|
| Encoded Preference | Encodes team/org workflow decisions | coding-style, git-workflow, api-design-patterns | Durable — update when team decisions change |
| Capability Uplift | Compensates for model limitations | Specific API patterns, workaround techniques | Ephemeral — deprecate when base model improves |

Most skills in this repo are **Encoded Preference** (global conventions). See [Skill Lifecycle](#skill-lifecycle) for when to deprecate Capability Uplift skills. See `references/workflow-patterns.md` for the Encoded Preference vs Capability Uplift distinction in detail.

## Folder Structure

```
skill-name/           # kebab-case required
├── SKILL.md          # Required (uppercase, exact)
├── references/       # Detailed docs (on-demand loading)
├── scripts/          # Executable scripts
└── assets/           # Templates, fonts, icons
```

**Critical Rules**:
- SKILL.md must be exactly `SKILL.md` (case-sensitive)
- Folder name: kebab-case, no spaces, no capitals
- NO README.md inside skill folder (use references/)

## YAML Frontmatter

### Required Fields

```yaml
---
name: skill-name      # kebab-case, matches folder
description: "..."    # Controls when skill triggers
---
```

### Optional Fields

```yaml
license: MIT
compatibility: Requires Python 3.10+
metadata:
  author: Your Name
  version: 1.0.0
  mcp-server: server-name
```

See `references/yaml-reference.md` for complete field documentation.

### Security Restrictions

**Forbidden in frontmatter**:
- XML angle brackets (< >) - injection risk
- "claude" or "anthropic" in name (reserved)

## Description Field (CRITICAL)

Structure: `[What it does] + [When to use it] + [Key capabilities]`

```yaml
# BAD: Too vague
description: "Creates documents"

# BAD: Missing triggers
description: "Sophisticated multi-page documentation systems"

# GOOD: Complete formula
description: "Creates Word documents with tracked changes for legal review. Use when user asks for contracts, legal documents, or revision-tracked content."

# GOOD: With negative trigger
description: "Advanced data analysis for CSV files. Use for statistical modeling, regression. Do NOT use for simple data exploration."
```

Include:
- What the skill does
- Trigger phrases/scenarios (what users actually say)
- File types if relevant
- Negative triggers when needed (Do NOT use for...)

### Description Analysis

With 30+ skills loaded, false positives (skill triggers when it shouldn't) waste context, and false negatives (skill doesn't trigger when needed) lose value. Analyze descriptions systematically:

**False Positive Check**: List 5 prompts from adjacent domains. Does your skill trigger? If yes, add negative triggers.

**False Negative Check**: List 5 paraphrased prompts for your skill. Would the description match? If not, add trigger phrases.

**Overlap Check**: Search existing skill descriptions for keyword collisions. If two skills trigger on the same prompt, either:
- Narrow one with negative triggers
- Merge if they cover the same domain

## Content Guidelines

### Litmus Test

> "If Claude did NOT read this SKILL, would its output quality drop?"
> - **Yes** --> keep the content
> - **No** --> remove it (Claude already knows this)

### DO Include

- **Policies/directions**: What to do, what approach to take
- **Anti-patterns**: What to avoid — but ONLY if they pass the Litmus Test above. If Claude would avoid the pattern without reading the skill, do not include it.
- **Domain knowledge**: Information requiring lookup
- **Output formats**: Expected structure when not obvious
- **Review categories**: Platform-agnostic area names that anchor coverage (see Review Categories Pattern below)

### DO NOT Include

- Standard library commands (Claude knows these)
- Basic language syntax
- General programming concepts
- Things you could find in any tutorial
- **Scope mismatch**: Platform-specific content in a skill whose agent targets all platforms (e.g., React checklist in a general performance-reviewer). Platform-specific content is correct when the skill's scope matches its agent's scope
- **Context-dependent severity thresholds**: The same pattern (e.g., O(n^2)) can be CRITICAL or harmless depending on data size and context -- do not hardcode severity in cross-platform skills

### Simplification Safety Checklist

When removing content from skills, verify:

- [ ] **WRONG/CORRECT code contrasts**: Keep for style-consistency skills (coding-style, etc.) — without concrete examples, judgment drifts across runs
- [ ] **Cross-skill references**: "See `makefile-first`" or "See `/tdd`" sections connect skill dependencies — removing them breaks agent routing
- [ ] **Reference file targets**: If text says "See references/X.md", verify X.md actually contains the promised content
- [ ] **Agent dependencies**: Check `skills:` frontmatter in all agents that load this skill — don't remove content they depend on
- [ ] **Coverage targets**: Language-specific metrics encode genuinely different policies — do not consolidate even if they look similar

### Calibration Examples

| Pattern | Verdict | Why |
|---------|---------|-----|
| "Run pytest for tests. Use -v for verbose." | Remove | Standard command Claude knows |
| "React rules in a general perf skill" | Remove | Scope mismatch with agent target |
| "React rules in react-patterns skill" | Keep | Scope matches agent scope |
| "Use pytest with fixtures in conftest.py" | Keep | Policy direction, not tutorial |
| Review categories (area names, no items) | Keep | Platform-agnostic anchors |

### Review Categories Pattern

Review-oriented skills and agents need anchors to ensure reproducible coverage across runs. Without any structure, Claude's non-deterministic output means reviews can vary -- one run checks caching, the next skips it entirely.

**Solution: Use categories, not checklist items.**

| Approach | Example | Problem |
|----------|---------|---------|
| No structure | (empty) | Non-deterministic coverage across runs |
| Specific checklist | "No O(n^2) on unbounded collections" | Fine in platform-scoped skill; causes bias in cross-platform agent |
| **Categories** | "Algorithmic complexity" | Platform-agnostic anchor; Claude applies specific knowledge per platform |

Categories go in the **agent** (not a skill) when they define how the agent structures its review workflow. Categories go in a **skill** when they define shared principles multiple agents reference.

## Progressive Disclosure

Skills load in three levels to save context:

| Level | Content | Loaded When |
|-------|---------|-------------|
| 1 | Name + description | Always (~100 tokens) |
| 2 | Full SKILL.md | Skill triggered |
| 3 | references/, scripts/ | On demand |

**Front-load important rules** - Claude pays more attention to content at the top.

## Size Guidelines

| Component | Guideline |
|-----------|-----------|
| SKILL.md | Under 500 lines, ~5000 words |
| Detailed docs | Move to references/ |
| Large examples | Move to references/ or scripts/ |

## Testing Your Skill

See `references/troubleshooting.md` for common issues (trigger failures, instructions not followed).

### Iteration Signals

| Signal | Meaning | Fix |
|--------|---------|-----|
| Never triggers | Description too vague | Add specific phrases |
| Triggers for unrelated | Description too broad | Add negative triggers |
| Wrong behavior | Instructions unclear | Add explicit steps |

See `references/troubleshooting.md` for common issues.

### Structured Evals

For systematic skill quality measurement, see `references/eval-patterns.md`.

## Skill Lifecycle

### When to Deprecate

Review skills when:
- A new model release may have learned the skill's techniques natively
- The skill's pass rate in evals drops below the no-skill baseline
- Team conventions change, making the skill's policies outdated

### Deprecation Process

1. Run the skill's eval prompts WITHOUT the skill loaded
2. Compare output quality against WITH-skill results
3. If no-skill output is equivalent or better: delete the skill folder
4. Update any agents that referenced it in `skills:` frontmatter

## Checklist

### Before Creating
- [ ] Identified 2-3 concrete use cases
- [ ] Is this knowledge Claude doesn't have?
- [ ] Would I explain this repeatedly without a skill?

### During Development
- [ ] Folder name in kebab-case
- [ ] SKILL.md exists (exact spelling)
- [ ] Frontmatter has `---` delimiters
- [ ] Name field: kebab-case, no spaces
- [ ] Description includes WHAT and WHEN
- [ ] No XML tags anywhere
- [ ] Under 500 lines
- [ ] Anti-patterns included only if they pass the Litmus Test (Claude wouldn't know without the skill)
- [ ] Library-specific: verify with context7 if APIs may have changed. Differences from Claude's knowledge → write in SKILL.md

### Before Release
- [ ] Tested triggering on obvious tasks
- [ ] Tested triggering on paraphrased requests
- [ ] Verified doesn't trigger on unrelated topics
- [ ] Functional tests pass

### Ongoing Maintenance
- [ ] Classified as Encoded Preference or Capability Uplift
- [ ] Description analyzed for false positives/negatives against adjacent skills
- [ ] Capability Uplift skills: reassessed after model updates
