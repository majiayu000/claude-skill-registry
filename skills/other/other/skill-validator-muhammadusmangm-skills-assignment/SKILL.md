---
name: skill-validator
description: |
  Validates skills against production-level criteria with 9-category scoring.
  This skill should be used when reviewing, auditing, or improving skills to
  ensure quality standards. Evaluates structure, content, user interaction,
  documentation, domain standards, technical robustness, maintainability,
  zero-shot implementation, and reusability. Returns actionable validation
  report with scores and improvement recommendations.
---

# Skill Validator

Validate any skill against production-level quality criteria.

## Validation Workflow

### Phase 1: Gather Context

1. **Read the skill's SKILL.md** completely
2. **Identify skill type** from frontmatter description:
   - Builder skill (creates artifacts)
   - Guide skill (provides instructions)
   - Automation skill (executes workflows)
   - Analyzer skill (extracts insights)
   - Validator skill (enforces quality)
   - Hybrid skill (combination of above)
3. **Read all reference files** in `references/` directory
4. **Check for assets/scripts** directories
5. **Note frontmatter fields** (`name`, `description`, `allowed-tools`, `model`)

### Phase 2: Apply Criteria

Evaluate against **9 criteria categories**. Each criterion scores 0-3:
- **0**: Missing/Absent
- **1**: Present but inadequate
- **2**: Adequate implementation
- **3**: Excellent implementation

---

## Criteria Categories

### 1. Structure & Anatomy (Weight: 12%)

| Criterion | What to Check |
|-----------|---------------|
| **SKILL.md exists** | Root file present |
| **Line count** | <500 lines (context is precious) |
| **Frontmatter complete** | `name` and `description` present in YAML |
| **Name constraints** | Lowercase, numbers, hyphens only; ≤64 chars; matches directory |
| **Description format** | [What] + [When] format; ≤1024 chars |
| **Description style** | Third-person: "This skill should be used when..." |
| **No extraneous files** | No README.md, CHANGELOG.md, LICENSE in skill dir |
| **Progressive disclosure** | Details in `references/`, not bloated SKILL.md |
| **Asset organization** | Templates in `assets/`, scripts in `scripts/` |
| **Large file guidance** | If references >10k words, grep patterns in SKILL.md |

**Fail condition**: Missing SKILL.md or >800 lines = automatic fail

### 2. Content Quality (Weight: 15%)

| Criterion | What to Check |
|-----------|---------------|
| **Conciseness** | No verbose explanations, context is public good |
| **Imperative form** | Instructions use "Do X" not "You should do X" |
| **Appropriate freedom** | Constraints where needed, flexibility where safe |
| **Scope clarity** | Clear what skill does AND does not do |
| **No hallucination risk** | No instructions that encourage making up info |
| **Output specification** | Clear expected outputs defined |

### 3. User Interaction (Weight: 12%)

| Criterion | What to Check |
|-----------|---------------|
| **Clarification triggers** | Asks questions before acting on ambiguity |
| **Required vs optional** | Distinguishes must-know from nice-to-know |
| **Graceful handling** | What to do when user doesn't answer |
| **No over-asking** | Doesn't ask obvious or inferrable questions |
| **Question pacing** | Avoids too many questions in single message |
| **Context awareness** | Uses available context before asking |

**Key pattern to look for**:
```markdown
## Required Clarifications
1. Question about X
2. Question about Y

## Optional Clarifications
3. Question about Z (if relevant)

Note: Avoid asking too many questions in a single message.
```

### 4. Documentation & References (Weight: 10%)

| Criterion | What to Check |
|-----------|---------------|
| **Source URLs** | Official documentation links provided |
| **Reference files** | Complex details in `references/` not main file |
| **Fetch guidance** | Instructions to fetch docs for unlisted patterns |
| **Version awareness** | Notes about checking for latest patterns |
| **Example coverage** | Good/bad examples for key patterns |

**Key pattern to look for**:
```markdown
| Resource | URL | Use For |
|----------|-----|---------|
| Official Docs | https://... | Complex cases |
```

### 5. Domain Standards (Weight: 10%)

| Criterion | What to Check |
|-----------|---------------|
| **Best practices** | Follows domain conventions (e.g., WCAG, OWASP) |
| **Enforcement mechanism** | Checklists, validation steps, must-verify items |
| **Anti-patterns** | Lists what NOT to do |
| **Quality gates** | Output checklist before delivery |

**Key pattern to look for**:
```markdown
### Must Follow
- [ ] Requirement 1
- [ ] Requirement 2

### Must Avoid
- Antipattern 1
- Antipattern 2
```

### 6. Technical Robustness (Weight: 8%)

| Criterion | What to Check |
|-----------|---------------|
| **Error handling** | Guidance for failure scenarios |
| **Security considerations** | Input validation, secrets handling if relevant |
| **Dependencies** | External tools/APIs documented |
| **Edge cases** | Common edge cases addressed |
| **Testability** | Can outputs be verified? |

### 7. Maintainability (Weight: 8%)

| Criterion | What to Check |
|-----------|---------------|
| **Modularity** | References are self-contained topics |
| **Update path** | Easy to update when standards change |
| **No hardcoded values** | Uses placeholders/variables where appropriate |
| **Clear organization** | Logical section ordering |

### 8. Zero-Shot Implementation (Weight: 12%)

Skills should enable single-interaction implementation with embedded expertise.

| Criterion | What to Check |
|-----------|---------------|
| **Before Implementation section** | Context gathering guidance present |
| **Codebase context** | Guidance to scan existing structure/patterns |
| **Conversation context** | Uses discussed requirements/decisions |
| **Embedded expertise** | Domain knowledge in `references/`, not runtime discovery |
| **User-only questions** | Only asks for USER requirements, not domain knowledge |

**Key pattern to look for**:
```markdown
## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing structure, patterns, conventions |
| **Conversation** | User's specific requirements |
| **Skill References** | Domain patterns from `references/` |
| **User Guidelines** | Project-specific conventions |
```

**Red flag**: Skill instructs to "research" or "discover" domain knowledge at runtime instead of embedding it.

### 9. Reusability (Weight: 13%)

Skills should handle variations, not single requirements.

| Criterion | What to Check |
|-----------|---------------|
| **Handles variations** | Not hardcoded to single use case |
| **Variable elements** | Clarifications capture what VARIES |
| **Constant patterns** | Domain best practices encoded as constants |
| **Not requirement-specific** | Avoids hardcoded data, tools, configs |
| **Abstraction level** | Appropriate generalization for domain |

**Good example**:
```markdown
"Create visualizations - adaptable to data shape, chart type, library"
```

**Bad example (too specific)**:
```markdown
"Create bar chart with sales data using Recharts"
```

**Key check**: Does the skill work for multiple use cases within its domain?

---

## Type-Specific Validation

After scoring general criteria, verify type-specific requirements:

| Type | Must Have |
|------|-----------|
| **Builder** | Clarifications, Output Spec, Domain Standards, Output Checklist |
| **Guide** | Workflow Steps, Examples (Good/Bad), Official Docs links |
| **Automation** | Scripts in `scripts/`, Dependencies, Error Handling, I/O Spec |
| **Analyzer** | Analysis Scope, Evaluation Criteria, Output Format, Synthesis |
| **Validator** | Quality Criteria, Scoring Rubric, Thresholds, Remediation |

**Scoring**: Deduct 10 points if type-specific requirements missing for identified type.

---

## Scoring Guide

### Category Scores

Calculate each category score:
```
Category Score = (Sum of criterion scores) / (Max possible) * 100
```

### Overall Score

```
Overall = Σ(Category Score × Weight)
```

### Rating Thresholds

| Score | Rating | Meaning |
|-------|--------|---------|
| 90-100 | **Production** | Ready for wide use |
| 75-89 | **Good** | Minor improvements needed |
| 60-74 | **Adequate** | Functional but needs work |
| 40-59 | **Developing** | Significant gaps |
| 0-39 | **Incomplete** | Major rework required |

---

## Output Format

Generate validation report:

```markdown
# Skill Validation Report: [skill-name]

**Rating**: [Production/Good/Adequate/Developing/Incomplete]
**Overall Score**: [X]/100

## Summary
[2-3 sentence assessment]

## Category Scores

| Category | Score | Weight | Weighted |
|----------|-------|--------|----------|
| Structure & Anatomy | X/100 | 12% | X |
| Content Quality | X/100 | 15% | X |
| User Interaction | X/100 | 12% | X |
| Documentation | X/100 | 10% | X |
| Domain Standards | X/100 | 10% | X |
| Technical Robustness | X/100 | 8% | X |
| Maintainability | X/100 | 8% | X |
| Zero-Shot Implementation | X/100 | 12% | X |
| Reusability | X/100 | 13% | X |
| **Type-Specific Deduction** | -X | - | -X |

## Critical Issues (if any)
- [Issue requiring immediate fix]

## Improvement Recommendations
1. **High Priority**: [Specific action]
2. **Medium Priority**: [Specific action]
3. **Low Priority**: [Specific action]

## Strengths
- [What skill does well]
```

---

## Quick Validation Checklist

For rapid assessment, check these critical items:

### Structure & Frontmatter
- [ ] SKILL.md <500 lines
- [ ] Frontmatter: name (≤64 chars, lowercase, hyphens) + description (≤1024 chars)
- [ ] Description uses third-person style ("This skill should be used when...")
- [ ] No README.md/CHANGELOG.md in skill directory

### Content & Interaction
- [ ] Has clarification questions (Required vs Optional)
- [ ] Has output specification
- [ ] Has official documentation links

### Zero-Shot & Reusability
- [ ] Has "Before Implementation" section (context gathering)
- [ ] Domain expertise embedded in `references/` (not runtime discovery)
- [ ] Handles variations (not requirement-specific)

### Type-Specific (check based on skill type)
- [ ] Builder: Clarifications + Output Spec + Standards + Checklist
- [ ] Guide: Workflow + Examples + Docs
- [ ] Automation: Scripts + Dependencies + Error Handling
- [ ] Analyzer: Scope + Criteria + Output Format
- [ ] Validator: Criteria + Scoring + Thresholds + Remediation

**If 10+ checked**: Likely Production (90+)
**If 7-9 checked**: Likely Good (75-89)
**If 5-6 checked**: Likely Adequate (60-74)
**If <5 checked**: Needs significant work

---

## Reference Files

| File | When to Read |
|------|--------------|
| `references/detailed-criteria.md` | Deep evaluation of specific criterion |
| `references/scoring-examples.md` | Example validations for calibration |
| `references/improvement-patterns.md` | Common fixes for common issues |

---

## Usage Examples

### Validate a skill
```
Validate the chatgpt-widget-creator skill against production criteria
```

### Quick audit
```
Quick validation check on mcp-builder skill
```

### Focused review
```
Check if skill-creator skill has proper user interaction patterns
```
