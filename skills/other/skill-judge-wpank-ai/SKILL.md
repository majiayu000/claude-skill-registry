---
name: skill-judge
model: standard
description: Evaluate Agent Skill quality against official specifications. Use when reviewing SKILL.md files, auditing skill packages, improving skill design, or checking if a skill follows best practices. Provides 8-dimension scoring (120 points) with actionable improvements. Triggers on review skill, evaluate skill, audit skill, improve skill, skill quality, SKILL.md review.
---

# Skill Judge

Evaluate Agent Skills against official specifications and patterns derived from 17+ official examples.

## WHAT This Skill Does

Scores skills across 8 dimensions (120 points total) and provides specific, actionable improvement suggestions.

## WHEN To Use

- Reviewing/auditing a SKILL.md file
- Improving an existing skill's design
- Checking if a skill follows best practices
- Before publishing a skill to the ecosystem

**KEYWORDS**: review skill, evaluate skill, audit skill, skill quality, SKILL.md


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install skill-judge
```


---

## Core Philosophy

### The Core Formula

> **Good Skill = Expert-only Knowledge − What Claude Already Knows**

A Skill's value = its **knowledge delta** — the gap between what it provides and what the model already knows.

| Type | Definition | Treatment |
|------|------------|-----------|
| **Expert** | Claude genuinely doesn't know this | Must keep — this is the Skill's value |
| **Activation** | Claude knows but may not think of | Keep if brief — serves as reminder |
| **Redundant** | Claude definitely knows this | Delete — wastes tokens |

**Good Skill ratio:** >70% Expert, <20% Activation, <10% Redundant

---

## Evaluation Dimensions (120 points)

### D1: Knowledge Delta (20 pts) — THE CORE DIMENSION

Does the Skill add genuine expert knowledge?

| Score | Criteria |
|-------|----------|
| 0-5 | Explains basics Claude knows (tutorials, standard library usage) |
| 6-10 | Mixed: some expert knowledge diluted by obvious content |
| 11-15 | Mostly expert knowledge with minimal redundancy |
| 16-20 | Pure knowledge delta — every paragraph earns its tokens |

**Red flags** (instant ≤5): "What is [basic concept]", step-by-step tutorials, generic best practices

**Green flags** (high delta): Decision trees, non-obvious trade-offs, edge cases from experience, "NEVER do X because [non-obvious reason]"

---

### D2: Mindset + Procedures (15 pts)

Does the Skill transfer expert thinking patterns AND domain-specific procedures?

| Score | Criteria |
|-------|----------|
| 0-3 | Only generic procedures Claude already knows |
| 4-7 | Has domain procedures but lacks thinking frameworks |
| 8-11 | Good balance: thinking patterns + domain-specific workflows |
| 12-15 | Expert-level: shapes thinking AND provides procedures Claude wouldn't know |

**Valuable thinking patterns:** "Before [action], ask yourself: Purpose? Constraints? Differentiation?"

**Valuable procedures:** Domain-specific sequences, non-obvious ordering, critical steps easy to miss

**Redundant procedures:** Generic file operations, standard programming patterns

---

### D3: Anti-Pattern Quality (15 pts)

Does the Skill have effective NEVER lists?

| Score | Criteria |
|-------|----------|
| 0-3 | No anti-patterns mentioned |
| 4-7 | Generic warnings ("avoid errors", "be careful") |
| 8-11 | Specific NEVER list with some reasoning |
| 12-15 | Expert-grade anti-patterns with WHY — things only experience teaches |

**Test:** Would an expert read the anti-pattern list and say "yes, I learned this the hard way"?

---

### D4: Specification Compliance — Especially Description (15 pts)

**The description is THE MOST IMPORTANT field.** It's the only thing the agent sees before deciding to load the skill.

| Score | Criteria |
|-------|----------|
| 0-5 | Missing frontmatter or invalid format |
| 6-10 | Has frontmatter but description is vague or incomplete |
| 11-13 | Valid frontmatter, description has WHAT but weak on WHEN |
| 14-15 | Perfect: comprehensive description with WHAT, WHEN, and trigger keywords |

**Description must answer:**
1. **WHAT**: What does this Skill do?
2. **WHEN**: In what situations should it be used?
3. **KEYWORDS**: What terms should trigger this Skill?

**Poor:** "Helps with document tasks"  
**Good:** "Create, edit, and analyze .docx files. Use when working with Word documents, tracked changes, or professional document formatting."

---

### D5: Progressive Disclosure (15 pts)

Does the Skill implement proper content layering?

| Layer | Content | Size |
|-------|---------|------|
| 1: Metadata | name + description | ~100 tokens |
| 2: SKILL.md | Guidelines, decision trees | < 500 lines ideal |
| 3: Resources | scripts/, references/, assets/ | No limit |

| Score | Criteria |
|-------|----------|
| 0-5 | Everything dumped in SKILL.md (>500 lines, no structure) |
| 6-10 | Has references but unclear when to load them |
| 11-13 | Good layering with MANDATORY triggers present |
| 14-15 | Perfect: decision trees + explicit triggers + "Do NOT Load" guidance |

**Good trigger:** "**MANDATORY - READ ENTIRE FILE**: Before proceeding, you MUST read [`docx-js.md`](docx-js.md)"

**Bad trigger:** Just listing references at the end without loading guidance

---

### D6: Freedom Calibration (15 pts)

Is specificity appropriate for the task's fragility?

| Task Type | Should Have | Why |
|-----------|-------------|-----|
| Creative/Design | High freedom | Multiple valid approaches |
| Code review | Medium freedom | Principles exist but judgment required |
| File format operations | Low freedom | One wrong byte corrupts file |

| Score | Criteria |
|-------|----------|
| 0-5 | Severely mismatched (rigid scripts for creative, vague for fragile) |
| 6-10 | Partially appropriate |
| 11-13 | Good calibration for most scenarios |
| 14-15 | Perfect freedom calibration throughout |

**Test:** "If Agent makes a mistake, what's the consequence?" High consequence → Low freedom

---

### D7: Pattern Recognition (10 pts)

Does the Skill follow an established pattern?

| Pattern | ~Lines | When to Use |
|---------|--------|-------------|
| **Mindset** | ~50 | Creative tasks requiring taste |
| **Navigation** | ~30 | Multiple distinct scenarios (routes to sub-files) |
| **Philosophy** | ~150 | Art/creation requiring originality |
| **Process** | ~200 | Complex multi-step projects |
| **Tool** | ~300 | Precise operations on specific formats |

| Score | Criteria |
|-------|----------|
| 0-3 | No recognizable pattern, chaotic structure |
| 4-6 | Partially follows a pattern with significant deviations |
| 7-8 | Clear pattern with minor deviations |
| 9-10 | Masterful application of appropriate pattern |

---

### D8: Practical Usability (15 pts)

Can an Agent actually use this Skill effectively?

| Score | Criteria |
|-------|----------|
| 0-5 | Confusing, incomplete, or untested guidance |
| 6-10 | Usable but with noticeable gaps |
| 11-13 | Clear guidance for common cases |
| 14-15 | Comprehensive: edge cases, error handling, decision trees |

**Check for:** Decision trees for multi-path scenarios, working code examples, error handling/fallbacks, edge cases covered

---

## NEVER Do When Evaluating

- Give high scores just because it "looks professional"
- Ignore token waste — every redundant paragraph = deduction
- Let length impress you — 43-line Skill can outperform 500-line Skill
- Skip mentally testing the decision trees
- Forgive explaining basics with "provides helpful context"
- Overlook missing anti-patterns
- Undervalue the description field — poor description = skill never gets used
- Put "when to use" info only in the body (agent only sees description before loading)

---

## Evaluation Protocol

### Step 1: Knowledge Delta Scan

Read SKILL.md and mark each section:
- **[E] Expert**: Claude doesn't know this — value-add
- **[A] Activation**: Claude knows but reminder useful — acceptable
- **[R] Redundant**: Claude knows this — should delete

Calculate ratio: E:A:R (target >70:20:10)

### Step 2: Structure Analysis

```
[ ] Valid frontmatter (name ≤64 chars, comprehensive description)
[ ] Total lines in SKILL.md
[ ] Reference files and sizes
[ ] Pattern identification (Mindset/Navigation/Philosophy/Process/Tool)
[ ] Loading triggers present (if references exist)
```

### Step 3: Score Each Dimension

For each dimension: find evidence, assign score, note improvements if < max

### Step 4: Calculate Total & Grade

| Grade | Percentage | Meaning |
|-------|------------|---------|
| A | 90%+ (108+) | Excellent — production-ready |
| B | 80-89% (96-107) | Good — minor improvements needed |
| C | 70-79% (84-95) | Adequate — clear improvement path |
| D | 60-69% (72-83) | Below Average — significant issues |
| F | <60% (<72) | Poor — needs fundamental redesign |

### Step 5: Generate Report

```markdown
# Skill Evaluation Report: [Skill Name]

## Summary
- **Total Score**: X/120 (X%)
- **Grade**: [A/B/C/D/F]
- **Pattern**: [Mindset/Navigation/Philosophy/Process/Tool]
- **Knowledge Ratio**: E:A:R = X:Y:Z
- **Verdict**: [One sentence]

## Dimension Scores
| Dimension | Score | Max | Notes |
|-----------|-------|-----|-------|
| D1: Knowledge Delta | X | 20 | |
| D2: Mindset + Procedures | X | 15 | |
| D3: Anti-Pattern Quality | X | 15 | |
| D4: Specification Compliance | X | 15 | |
| D5: Progressive Disclosure | X | 15 | |
| D6: Freedom Calibration | X | 15 | |
| D7: Pattern Recognition | X | 10 | |
| D8: Practical Usability | X | 15 | |

## Critical Issues
[Must-fix problems]

## Top 3 Improvements
1. [Highest impact with specific guidance]
2. [Second priority]
3. [Third priority]
```

---

## Common Failure Patterns

| Pattern | Symptom | Fix |
|---------|---------|-----|
| **Tutorial** | Explains what X is, basic library usage | Delete basics. Focus on expert decisions. |
| **Dump** | 800+ lines, everything included | Core in SKILL.md (<300), details in references/ |
| **Orphan References** | References exist but never loaded | Add "MANDATORY - READ" at decision points |
| **Checkbox Procedure** | Step 1, Step 2... mechanical | Transform to "Before doing X, ask yourself..." |
| **Vague Warning** | "Be careful", "avoid errors" | Specific NEVER list with concrete examples |
| **Invisible Skill** | Great content, rarely activated | Fix description: WHAT + WHEN + KEYWORDS |
| **Wrong Location** | "When to use" in body, not description | Move triggers to description field |
| **Over-Engineered** | README, CHANGELOG, CONTRIBUTING | Delete. Only what Agent needs for the task. |

---

## The Meta-Question

> **"Would an expert in this domain say: 'Yes, this captures knowledge that took me years to learn'?"**

If yes → genuine value. If no → compressing what Claude already knows.

The best Skills are **compressed expert brains** — 10 years of experience in 50 lines.
