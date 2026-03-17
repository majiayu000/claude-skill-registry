---
name: "north-star"
description: "Project vision alignment, mission definition, and quality standards — the guiding goal that shapes every decision"
---

# North Star — Ambitious Project Vision

**Domain**: Project vision, mission alignment, goal setting, quality standards
**Trigger**: Project initialization, vision discussions, "what are we building?", purpose alignment
**Updated**: 2026-02-26

---

## What This Skill Does

Every project needs a North Star — an ambitious, clear, inspiring goal that guides every decision. This skill helps define, document, and maintain that vision across projects.

A North Star is not:
- A feature list
- A deadline
- A metric to optimize
- A tagline for marketing

A North Star IS:
- A commitment that shapes every decision
- A filter for "should we build this?"
- A standard that demands excellence
- A vision worth pursuing even when it's hard

---

## The Active Context Plug

Add these fields to your project's `.github/copilot-instructions.md` Active Context:

```markdown
## Active Context
...existing fields...
North Star: [Your ambitious vision statement]
Guidelines: Read [path/to/NORTH-STAR.md] — defines what "[key phrase]" means in practice
```

**Example** (Alex Master):
```markdown
North Star: Create the most advanced and trusted AI partner for any job
Guidelines: Read alex_docs/NORTH-STAR.md — defines what "most advanced and trusted AI partner" means in practice
```

---

## North Star Templates

### Template 1: NASA-Quality Default (Recommended for Heirs)

```markdown
# North Star: [Project Name]

**Author**: [Name]
**Date**: [ISO Date]
**Version**: 1.0

---

## Mission Statement

Build software that earns trust through:
- **Reliability**: When it says something works, it works
- **Correctness**: No silent failures, no hidden bugs
- **Transparency**: Honest about limitations and uncertainties
- **Quality**: NASA Power of 10 principles where they apply

## Quality Standards

This project follows NASA/JPL-inspired coding standards:

| Rule | Standard | Status |
|------|----------|:------:|
| R1 | Restrict control flow to simple constructs | ☐ |
| R2 | All loops must have fixed upper bounds | ☐ |
| R3 | No dynamic memory after initialization | ☐ |
| R4 | Functions ≤60 lines | ☐ |
| R5 | Assertion density ≥2 per function | ☐ |
| R6 | Declare variables at smallest scope | ☐ |
| R7 | Check return values of non-void functions | ☐ |
| R8 | Limit preprocessor use (N/A for TypeScript) | N/A |
| R9 | Restrict pointer use (safe navigation) | ☐ |
| R10 | Compile with all warnings enabled | ☐ |

## Core Principles

| Principle | Meaning | Daily Application |
|-----------|---------|-------------------|
| **KISS** | Keep It Simple, Stupid | Choose the simplest solution that works. Complexity is the enemy of reliability. |
| **DRY** | Don't Repeat Yourself | One source of truth. If you copy-paste, you create drift. |
| **Quality-First** | No shortcuts that incur debt | Every shortcut becomes a landmine. Build right, or don't build yet. |
| **Research-Before-Code** | Understand before implementing | 30 minutes of research saves 3 hours of debugging. |

## Definition of Done (DoD)

A feature is **done** when ALL boxes are checked:

### Code Quality
- [ ] Compiles with zero errors and zero warnings
- [ ] Follows KISS — simplest solution that works
- [ ] Follows DRY — no duplicated logic
- [ ] Functions ≤60 lines (NASA R4)
- [ ] Variables declared at smallest scope (NASA R6)

### Testing & Verification
- [ ] Unit tests for logic-heavy functions
- [ ] Integration test or manual verification for workflows
- [ ] Edge cases explicitly handled (not ignored)
- [ ] Error paths tested — not just happy path

### Documentation
- [ ] Code comments explain *why*, not *what*
- [ ] README/changelog updated if user-facing
- [ ] API contracts documented (if applicable)

### Review & Safety
- [ ] Self-reviewed with this checklist
- [ ] Code-reviewed by peer (or AI adversarial review)
- [ ] No TODOs left unflagged in tracker
- [ ] No secrets, no PII, no hardcoded paths

### Error Handling
- [ ] All errors surface — no silent failures
- [ ] User-friendly error messages where applicable
- [ ] Recovery path exists for transient failures

## What This Means Daily

When making decisions, ask:
1. Does this increase or decrease reliability?
2. Would I trust this code in a critical system?
3. Am I cutting corners that will cost us later?
4. Is this the simplest solution that could work?

If the answer to any of these is unfavorable — stop and reconsider.
```

### Template 2: Product Vision

```markdown
# North Star: [Product Name]

**Author**: [Name]
**Date**: [ISO Date]

---

## The Vision

[One sentence that captures the ambitious goal]

## What Each Word Means

### [Key Word 1]
- What it means...
- What it doesn't mean...
- How we'll know we've achieved it...

### [Key Word 2]
- What it means...
- What it doesn't mean...
- How we'll know we've achieved it...

## What This Demands

To achieve this vision, we must:
1. [Commitment 1]
2. [Commitment 2]
3. [Commitment 3]

## Daily Filter

Before building anything, ask:
- Does this serve the vision?
- Is this the best use of our limited time?
- Will users care about this in a year?

If no — defer it. If yes — build it excellently.
```

### Template 3: Research Project

```markdown
# North Star: [Research Question]

**Principal Investigator**: [Name]
**Date**: [ISO Date]

---

## Research Question

[The central question this project seeks to answer]

## Why It Matters

[2-3 sentences on significance and impact]

## Success Criteria

This research succeeds if:
1. [Measurable outcome 1]
2. [Measurable outcome 2]
3. [Knowledge contribution]

## Integrity Standards

- All data collection follows [IRB/ethics protocol]
- All analysis will be reproducible
- Negative results will be reported honestly
- Limitations will be acknowledged explicitly

## Publication Commitment

Target venues: [Journals/Conferences]
Timeline: [Realistic dates]
Open access: [Yes/No and why]
```

---

## Creating Your North Star

### Step 1: Define the Ambition

Ask yourself:
- What would make this project legendary, not just successful?
- What standard would make me proud to show this to experts?
- What commitment would I want written on the project's tombstone?

Write one sentence. Make it ambitious but achievable.

### Step 2: Break Down the Words

For each key word in your North Star:
- What does it mean in this context?
- What does it NOT mean?
- How will you know you've achieved it?

### Step 3: Define Daily Implications

A North Star that doesn't affect daily decisions is just decoration.
- What does this mean when choosing between features?
- What does this mean when under time pressure?
- What does this mean when something "mostly works"?

### Step 4: Document and Integrate

1. Create `NORTH-STAR.md` in your project's docs folder
2. Add the Active Context plug to `copilot-instructions.md`
3. Reference the North Star in your README
4. Review alignment during retrospectives

---

## Integration with Alex Architecture

When Alex sees the `North Star:` field in Active Context, it:
1. Reads the North Star as a guiding principle for all suggestions
2. Filters recommendations through the North Star commitment
3. Flags when a proposed change might compromise the vision
4. References the Guidelines document when explaining decisions

**Heir projects**: Initialize with the NASA-Quality Default template, then customize.

---

## Common Anti-Patterns

### ❌ Feature List Disguised as Vision
```
North Star: Build user auth, dashboard, API, and mobile app
```
This is a backlog, not a vision. Try: "Enable secure, seamless access to data from any device."

### ❌ Metric Without Meaning
```
North Star: Achieve 99.9% uptime
```
Metrics are constraints, not purpose. Try: "Build infrastructure users can depend on without thinking about it."

### ❌ Marketing Speak
```
North Star: Synergize innovative solutions for next-gen experiences
```
If it could mean anything, it means nothing. Be specific. Be concrete. Be honest.

### ❌ Too Modest
```
North Star: Build a working product
```
Where's the ambition? What makes this project worth doing? Reach further.

---

## Resources

- [NASA/JPL Power of 10 Rules](https://en.wikipedia.org/wiki/The_Power_of_10:_Rules_for_Developing_Safety-Critical_Code)
- [Alex's North Star document](https://github.com/fabioc-aloha/Alex_Plug_In/blob/main/alex_docs/NORTH-STAR.md) — Alex's North Star in practice
- [NASA Code Standards Analysis](https://github.com/fabioc-aloha/Alex_Plug_In/blob/main/alex_docs/research/NASA-CODE-STANDARDS-ANALYSIS.md) — How Alex implements NASA standards

---

## Connections

- **research-first-development** — North Star shapes what to research before building
- **code-review** — Reviews should check North Star alignment
- **architecture-health** — Health includes vision alignment
- **self-actualization** — Regular assessment of North Star adherence
- **release-process** — Releases should serve the North Star
