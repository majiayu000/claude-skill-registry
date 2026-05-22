---
name: prompt-template-designer
description: |
  Design reusable prompt templates that encode domain-specific patterns for recurring AI tasks.
  Use when you've executed similar prompts 2+ times and need to capture the pattern as reusable
  intelligence. NOT for one-off prompts or generic "ask AI a question" patterns.
category: intelligence-design
version: "2.0.0"
dependencies: ["constitution:v6.0.1", "4-layer-teaching-method"]
---

# Prompt Template Designer

## Quick Start

```bash
# 1. Check if template-worthy
# Criteria: 2+ uses, 5+ decision points, domain-specific

# 2. Extract pattern
# Identify invariants (constants) vs variants (parameters)

# 3. Create template
# Use Intent → Constraints → Success Criteria structure
```

## Persona

Think like a patterns library designer extracting recurring prompt structures. Identify what varies (parameters) vs what stays constant (pattern), encode domain knowledge into constraints, and design templates that reduce cognitive load while maintaining quality.

## Analysis Questions

### 1. Recurrence Check
**"Have I used this pattern 2+ times?"**

| Scenario | Template? |
|----------|-----------|
| "Generate Git commit message" (daily) | YES |
| "Explain React hooks to new dev" (once) | NO |
| "Debug Bash permission error" (recurring) | YES |
| "Research specific API quirk" (unique) | NO |

**Principle**: Premature templating adds maintenance burden. Wait for second use.

### 2. Variation Analysis
**"What stays constant vs what changes?"**

| Type | What It Is | Examples |
|------|------------|----------|
| Invariants | Template structure | Intent verb, core constraints, output format |
| Variants | Parameters | File names, project context, thresholds |

### 3. Complexity Check
**"Does this have 5+ decision points?"**

**High-value template** (5+ decisions): Code review prompt (action verb, language, review focus, output format, severity levels, style guide, context, fixes vs identify)

**Low-value** (1-3 decisions): "Explain specific Git command" → just ask directly

### 4. Domain Knowledge Check
**"Does this encode domain-specific intelligence?"**

**High-value**: Team conventions, quality standards, project constraints
**Low-value**: Generic "ask AI a question" or "generate code"

### 5. Parameter Design
**"What parameters make this flexible but not vague?"**

| Pattern | Example |
|---------|---------|
| Enum | `{{ACTION_TYPE}}` - Values: [CREATE, DEBUG, REFACTOR] |
| Path | `{{TARGET_FILE}}` - Type: file_path |
| Text | `{{CHANGES_MADE}}` - Type: bullet_list |
| Composite | `{{ERROR_CONTEXT}}` - Required fields: error_message, file_location |

**Rule**: 3-7 parameters optimal. More → split into multiple templates.

## Principles

### Principle 1: Template When Recurs 2+

- **First use**: Write prompt directly
- **Second use**: Notice pattern, extract template
- **Third+ uses**: Use template, refine

### Principle 2: Parameters Over Hard-Coding

```
# Before (hard-coded)
DEBUG backup.sh with "Permission denied" error

# After (parameterized)
DEBUG {{SCRIPT_NAME}} with "{{ERROR_MESSAGE}}" error
```

### Principle 3: Document Success Patterns

Templates must include:
- When to use (trigger conditions)
- Why it works (pattern encoded)
- Example filled (concrete instantiation)
- Common mistakes (what to avoid)

### Principle 4: Version and Evolve

```markdown
### v2.0.0 (2025-11-18)
- BREAKING: Changed {{CHANGES}} to structured {{CHANGES_MADE}}
- Added "business value" requirement

### v1.0.0 (2025-10-15)
- Initial extraction from successful prompts
```

### Principle 5: Measure Effectiveness

| Metric | Target |
|--------|--------|
| Success rate | >85% |
| Time saved | Measurable |
| Iterations needed | <3 |
| Team adoption | >50% |

## Template Structure

```markdown
---
template_name: {{descriptive-name}}
category: {{create|debug|refactor|optimize|analyze|generate}}
domain: {{backend|frontend|devops|testing|documentation}}
version: {{semantic-version}}
success_rate: {{percentage}}
---

# {{Template Name}}

## When to Use
{{Trigger conditions}}

## Parameters
### {{PARAM_1}}
- **Type**: {{enum|path|text|composite}}
- **Example**: {{value}}
- **Required**: {{yes|no}}

## Template
\```
INTENT:
{{ACTION_VERB}} {{description with parameters}}

CONSTRAINTS:
- {{invariant constraint}}
- {{parameterized constraint using {{PARAM}}}}

SUCCESS CRITERIA:
- {{measurable criterion}}
\```

## Example (Filled)
{{Concrete instantiation}}

## Common Mistakes
- {{Anti-pattern and how to avoid}}
```

## Example: Git Commit Message Generator

```markdown
---
template_name: git-commit-message-conventional
category: generate
version: 2.0.0
success_rate: 95%
---

## Parameters
- **CHANGES_MADE**: List of changes (required)
- **JIRA_TICKET**: PROJ-NNNN format (required)
- **SCOPE**: [auth, api, ui, db, devops] (required)
- **TYPE**: [feat, fix, docs, refactor, test] (required)

## Template
\```
GENERATE Git commit message

CHANGES: {{CHANGES_MADE}}

CONSTRAINTS:
- Format: {{TYPE}}({{SCOPE}}): <description> [{{JIRA_TICKET}}]
- Subject: Imperative mood, <50 chars
- Body: Explain WHY (business value)

SUCCESS CRITERIA:
- Passes commitlint
- Teammate understands without reading diff
\```

## Example (Filled)
\```
feat(auth): add JWT refresh endpoint [PROJ-1234]

- Add /auth/refresh: improves mobile UX by eliminating re-logins
- Extend token to 24h: reduces authentication friction
\```

## Common Mistakes
- Forgetting Jira ticket
- Past tense ("Added") instead of imperative ("Add")
- Explaining WHAT instead of WHY
```

## Anti-Patterns

| Anti-Pattern | Symptom | Fix |
|--------------|---------|-----|
| Template Before Pattern | Creating for unused prompts | Use manually 2+ times first |
| Over-Parameterization | 15+ parameters | Aim for 3-7, split if more |
| Under-Parameterization | Only works for one scenario | Must apply to 3+ use cases |
| No Success Metrics | Never tracked quality | Track success rate, time saved |

## Quick Reference

**Template Creation Checklist**:
- [ ] Used pattern 2+ times?
- [ ] Identified constants vs variants?
- [ ] 5+ decision points?
- [ ] Parameters with examples?
- [ ] Filled example included?
- [ ] Success criteria defined?

**Parameter Design**:
- [ ] Descriptive names (not {{X}})?
- [ ] Type specified?
- [ ] Examples provided?
- [ ] Required/optional marked?

## Teaching Integration (L2 → L3)

**Transition signal**: Student has written similar prompts 2+ times with 85%+ success

**Teaching sequence**:
1. "You've done this before. What's similar?" (identify recurrence)
2. "What constraints appear in both?" (extract constants)
3. "What changed?" (parameterize variants)
4. "Let's formalize as reusable intelligence" (create template)

## If Verification Fails

1. Check recurrence: "Has this been used 2+ times?"
2. Check complexity: "Are there 5+ decision points?"
3. Check parameters: "3-7 well-designed parameters?"
4. **Stop and report** if template adds more cognitive load than it saves
