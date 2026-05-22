---
name: documentation-standards
description: This skill should be used when the user asks about "documentation templates", "doc structure", "README format", "API documentation format", "how to write tutorials", "documentation checklist", or when the documentation-writer agent needs templates and workflows for specific documentation types. Provides Diataxis-based templates, checklists, and examples for 7 documentation types.
---

# Documentation Standards

Templates, workflows, and checklists for creating documentation following Diataxis principles.

## When to Use This Skill

Use when:

- Creating any type of documentation
- Need template for specific doc type
- Want checklist to verify doc completeness
- documentation-writer agent needs HOW guidance

## Diataxis Framework Quick Reference

| Quadrant | Purpose | Audience | Focus |
|----------|---------|----------|-------|
| **Tutorial** | Learning | Beginners | Hand-holding, confidence building |
| **How-to** | Goal completion | Practitioners | Steps to achieve specific goal |
| **Reference** | Information | Any level | Exhaustive, accurate lookup |
| **Explanation** | Understanding | Curious users | WHY, context, decisions |

## Documentation Types Overview

| Type | Diataxis | When to Use | Guidelines | Template |
|------|----------|-------------|------------|----------|
| README (root) | How-to | Project entry point | `references/readme-guidelines.md` | `examples/readme-root-template.md` |
| README (module) | Reference + How-to | Module documentation | `references/readme-guidelines.md` | `examples/readme-module-template.md` |
| Quick Start | How-to | Fast path to working | `references/quickstart-guidelines.md` | `examples/quickstart-template.md` |
| CONTRIBUTING | How-to | Guide contributors | `references/contributing-guidelines.md` | `examples/contributing-template.md` |
| API docs | Reference | Endpoint documentation | `references/api-docs-guidelines.md` | `examples/api-docs-template.md` |
| Tutorial | Tutorial | Onboarding, learning | `references/tutorial-guidelines.md` | `examples/tutorial-template.md` |
| How-to guide | How-to | Specific task completion | `references/howto-guidelines.md` | `examples/howto-template.md` |
| Reference | Reference | Exhaustive information | `references/reference-guidelines.md` | `examples/reference-docs-template.md` |
| Explanation/ADR | Explanation | Architecture decisions | `references/adr-guidelines.md` | `examples/explanation-adr-template.md` |

## Quick Decision Tree

```
What does the reader need?
├─ Learn something new → Tutorial
├─ Accomplish a specific task → How-to
├─ Look up information → Reference
└─ Understand why/context → Explanation
```

## Type Summaries and Checklists

### Type 1: README (Root Project)

**Diataxis:** How-to (goal: get project running)

**Required Sections:**

1. Title + One-liner
2. Quick Start (fastest path to working)
3. Installation (step-by-step)
4. Usage (basic examples)
5. License

**Checklist:**

- [ ] Can someone get running in <5 minutes?
- [ ] Prerequisites clearly stated (checklist format)?
- [ ] Installation steps verified to work?
- [ ] Basic usage example included?

**Guidelines:** `references/readme-guidelines.md`
**Template:** `examples/readme-root-template.md`

---

### Quick Start Guide

**Diataxis:** How-to (goal: get running FAST)

**When to Create:** If README Quick Start section > 10 lines

**Required Sections:**

1. Time estimate upfront (with emoji title)
2. Prerequisites (checklist format with `- [ ]`)
3. Steps with time per section and expected output
4. Verification that it works
5. Troubleshooting (top 2-3 issues)
6. "Need Help?" section with resources

**Checklist:**

- [ ] Time-boxed (stated upfront)?
- [ ] Every command copy-paste ready?
- [ ] Expected output shown for each step?
- [ ] Ends with verifiable working state?
- [ ] "Need Help?" section instead of "Next Steps"?

**Guidelines:** `references/quickstart-guidelines.md`
**Template:** `examples/quickstart-template.md`

---

### CONTRIBUTING.md

**Diataxis:** How-to (goal: enable contributions)

**Required Sections:**

1. How to Contribute (overview)
2. Reporting Bugs
3. Development Setup (with time estimate)
4. Pull Request Process
5. Code of Conduct (or link)

**Checklist:**

- [ ] Welcoming tone?
- [ ] Setup instructions tested?
- [ ] PR process clear?
- [ ] Response timeline mentioned?

**Guidelines:** `references/contributing-guidelines.md`
**Template:** `examples/contributing-template.md`

---

### Type 2: README (Module/Library)

**Diataxis:** Reference + How-to hybrid

**Required Sections:**

1. Purpose - What problem does this module solve?
2. API - Functions/classes exported
3. Usage Examples - Common use cases
4. Dependencies - What this module depends on

**Checklist:**

- [ ] Purpose clearly stated?
- [ ] All exports documented?
- [ ] Examples for main use cases?

**Guidelines:** `references/readme-guidelines.md`
**Template:** `examples/readme-module-template.md`

---

### Type 3: API Documentation

**Diataxis:** Reference (exhaustive, accurate)

**Required Sections:**

1. Endpoint - Method + Path
2. Authentication - Requirements
3. Request - Headers, params, body
4. Response - Success + all error cases
5. Examples - curl/code

**Checklist:**

- [ ] All parameters documented with types?
- [ ] All response codes covered?
- [ ] Request/response examples provided?
- [ ] Authentication requirements stated?

**Guidelines:** `references/api-docs-guidelines.md`
**Template:** `examples/api-docs-template.md`

---

### Type 4: Tutorial

**Diataxis:** Tutorial (learning-oriented)

**Core Principles:**

- Hand-holding: Every step explicit
- Confidence building: Small wins frequently
- Beginner-friendly: Assume nothing

**Required Sections:**

1. What you'll learn - Clear outcomes
2. Time estimate - Total and per section
3. Prerequisites - Checklist format
4. Steps - Numbered, explicit with checkpoints
5. Verification - How to know it worked
6. Troubleshooting - Common issues
7. Need Help? - Resources and next steps

**Checklist:**

- [ ] Can a complete beginner follow?
- [ ] Each step has verification?
- [ ] No assumed knowledge?
- [ ] Time estimates included?

**Guidelines:** `references/tutorial-guidelines.md`
**Template:** `examples/tutorial-template.md`

---

### Type 5: How-to Guide

**Diataxis:** How-to (goal-oriented)

**Core Principles:**

- Goal-focused: Solve specific problem
- Assumes knowledge: Reader knows basics
- Concise: Minimum steps to goal

**Required Sections:**

1. Goal - What reader will accomplish
2. Prerequisites - Required knowledge/setup
3. Steps - Direct path to goal
4. Troubleshooting - Common issues

**Checklist:**

- [ ] Goal clearly stated?
- [ ] Steps minimal but complete?
- [ ] No unnecessary explanation?

**Guidelines:** `references/howto-guidelines.md`
**Template:** `examples/howto-template.md`

---

### Type 6: Reference Documentation

**Diataxis:** Reference (information-oriented)

**Core Principles:**

- Exhaustive: All options documented
- Accurate: 100% correct, verified against code
- Consistent: Same format throughout

**Required Sections:**

1. Overview - What this covers
2. Index/TOC - Navigation
3. Entries - Consistent format per item
4. Cross-references - Links to related

**Checklist:**

- [ ] Every option/parameter documented?
- [ ] Format consistent throughout?
- [ ] Verified against actual code?
- [ ] Types/defaults specified?

**Guidelines:** `references/reference-guidelines.md`
**Template:** `examples/reference-docs-template.md`

---

### Type 7: Explanation / ADR

**Diataxis:** Explanation (understanding-oriented)

**Core Principles:**

- WHY-focused: Context and reasoning
- Long half-life: Stays relevant over time
- Contextual: Background and history

**Required Sections (ADR Format):**

1. Title - Decision being documented
2. Status - Proposed/Accepted/Deprecated
3. Context - Why decision was needed
4. Decision - What was decided
5. Alternatives - Options considered with pros/cons
6. Consequences - Trade-offs (positive AND negative)

**Checklist:**

- [ ] Context explains WHY decision was needed?
- [ ] Alternatives considered documented?
- [ ] Trade-offs clearly stated?
- [ ] Consequences (good AND bad) listed?

**Guidelines:** `references/adr-guidelines.md`
**Template:** `examples/explanation-adr-template.md`

---

## Process: Choosing the Right Type

### Step 1: Identify the Reader

Who is blocked without this doc?

- **New user** → Tutorial or README
- **Developer doing task** → How-to
- **Developer looking up info** → Reference
- **Anyone asking "why"** → Explanation

### Step 2: Identify the Need

What do they need?

- **Learn** → Tutorial
- **Do** → How-to
- **Know** → Reference
- **Understand** → Explanation

### Step 3: Get Guidelines and Template

1. Consult the guidelines file for rules and tips
2. Use the template file as a starting point

### Step 4: Verify

Use the checklist for that doc type.

## Anti-Patterns

- **Super-documents:** Mixing all types in one doc
- **Tutorial as Reference:** Exhaustive details in learning context
- **Reference without verification:** Claims not traced to code
- **Explanation without context:** WHY without background
- **How-to with too much explanation:** Should be direct
- **"Next Steps" instead of "Need Help?":** Less actionable

## File Structure

```
documentation-standards/
├── SKILL.md                    # This file - overview and checklists
├── references/                 # Guidelines and rules for each doc type
│   ├── quickstart-guidelines.md
│   ├── contributing-guidelines.md
│   ├── readme-guidelines.md
│   ├── api-docs-guidelines.md
│   ├── tutorial-guidelines.md
│   ├── howto-guidelines.md
│   ├── reference-guidelines.md
│   └── adr-guidelines.md
└── examples/                   # Concrete templates and working samples
    ├── quickstart-template.md
    ├── contributing-template.md
    ├── readme-root-template.md
    ├── readme-module-template.md
    ├── api-docs-template.md
    ├── tutorial-template.md
    ├── howto-template.md
    ├── reference-docs-template.md
    ├── explanation-adr-template.md
    ├── good-readme.md          # Working example
    ├── good-api-doc.md         # Working example
    └── good-adr.md             # Working example
```

---

*All documentation should be accurate, minimal, and serve a single Diataxis purpose.*
