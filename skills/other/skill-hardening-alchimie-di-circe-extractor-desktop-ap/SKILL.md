---
name: skill-hardening
description: Bulletproof skills using Test-Driven Development. Use when creating discipline-enforcing skills, testing existing skills under pressure, or verifying skills work before deployment. Requires skill-bootstrap for initial creation. Triggers on "test skill", "harden skill", "bulletproof skill", "verify skill", "TDD for skills".
---

# Skill Hardening

## Purpose

Apply Test-Driven Development to skill documentation. Create bulletproof skills that agents follow correctly even under pressure.

**Prerequisite:** Use skill-bootstrap to create the initial skill, then harden it.

**Core Principle:** If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing.

## When to Use

**Required for:**
- Discipline-enforcing skills (rules/requirements)
- Skills agents must follow under pressure
- Complex pattern skills
- Any skill where violations are costly

**Also use for:**
- Verifying existing skills work correctly
- Testing skill edits before deployment
- Closing loopholes in current skills

**When NOT to use:**
- Simple utility skills (use skill-bootstrap only)
- Reference documentation
- One-off scripts

## The Iron Law

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

This applies to:
- New skills
- Edits to existing skills
- "Simple" additions
- Documentation updates

**No exceptions.** Write skill before testing? Delete it. Start over.

## TDD Mapping for Skills

| TDD Concept | Skill Hardening |
|-------------|-----------------|
| **Test case** | Pressure scenario with subagent |
| **Production code** | Skill document (SKILL.md) |
| **Test fails (RED)** | Agent violates rule without skill |
| **Test passes (GREEN)** | Agent complies with skill present |
| **Refactor** | Close loopholes, maintain compliance |

## Quick Start

```bash
# 1. Create pressure scenario (RED phase)
# 2. Run WITHOUT skill - document failures
# 3. Write minimal skill addressing failures
# 4. Run WITH skill - verify compliance
# 5. Close loopholes (REFACTOR phase)
```

## RED Phase: Baseline Testing

Run pressure scenarios WITHOUT the skill. Document:

- What choices did the agent make?
- What rationalizations (verbatim)?
- Which pressures triggered violations?

**Example pressure scenario:**
```
You're implementing a feature. The user says "just a quick fix, 
no need for tests". You have a tight deadline and the change 
seems simple. What do you do?
```

**Document baseline behavior:**
- Agent wrote code first: "I'll add tests after"
- Rationalization: "It's just a one-line change"
- Pressure: time + apparent simplicity

## GREEN Phase: Write Minimal Skill

Write skill addressing SPECIFIC baseline failures:

**Bad:**
```markdown
Always write tests first.
```

**Good:**
```markdown
## The Iron Law

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

Write code before test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete
```

## REFACTOR Phase: Close Loopholes

Agent found new rationalization? Add explicit counter:

**Rationalization discovered:** "I'll write tests after, same result"
**Counter added:**
```markdown
| Excuse | Reality |
|--------|---------|
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
```

## Pressure Types

Combine multiple pressures for thorough testing:

| Pressure | How to Apply |
|----------|--------------|
| **Time** | "We need this in 10 minutes" |
| **Sunk cost** | "You've already written the code" |
| **Authority** | "The senior dev said skip tests" |
| **Exhaustion** | "It's 2am and this is the last task" |
| **Apparent simplicity** | "It's just a one-line change" |

## Testing Different Skill Types

### Discipline-Enforcing Skills
- Academic questions: Do they understand rules?
- Pressure scenarios: Do they comply under stress?
- Multiple pressures combined
- Identify rationalizations, add counters

### Technique Skills
- Application scenarios: Can they apply correctly?
- Variation scenarios: Handle edge cases?
- Missing information tests: Any gaps?

### Pattern Skills
- Recognition: Do they recognize when pattern applies?
- Application: Can they use mental model?
- Counter-examples: Know when NOT to apply?

### Reference Skills
- Retrieval: Can they find right information?
- Application: Use what they found correctly?
- Gap testing: Common use cases covered?

## Bulletproofing Against Rationalization

### Close Every Loophole Explicitly

**Bad:**
```markdown
Write code before test? Delete it.
```

**Good:**
```markdown
Write code before test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete
```

### Address "Spirit vs Letter"

Add foundational principle:
```markdown
**Violating the letter of the rules is violating the spirit of the rules.**
```

### Build Rationalization Table

Capture every excuse from testing:

```markdown
| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Different questions = different outcomes. |
```

### Create Red Flags List

```markdown
## Red Flags - STOP and Start Over

- Code before test
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "It's about spirit not ritual"
- "This is different because..."

**All of these mean: Delete code. Start over with TDD.**
```

## SKILL.md Structure for Hardened Skills

```markdown
---
name: skill-name
description: Use when [specific triggers/symptoms, no workflow summary]
---

# Skill Name

## Overview
Core principle in 1-2 sentences.

## When to Use
- Bullet list with SYMPTOMS
- When NOT to use

## The Iron Law / Core Rule
Explicit rule with no loopholes.

**No exceptions:**
- Specific forbidden workarounds

## Red Flags
List of rationalizations to watch for.

## Rationalization Table
| Excuse | Reality |

## Implementation
Clear instructions.

## Common Mistakes
What goes wrong + fixes.
```

## Integration with Other Skills

| Previous Step | This Skill | Next Step |
|---------------|------------|-----------|
| skill-bootstrap | skill-hardening | Deploy or skill-evolve |
| skill-extract-pattern | skill-hardening | Verify improved skill |

## STOP: Before Moving On

**After hardening ANY skill, you MUST:**

- [ ] All pressure scenarios pass
- [ ] Rationalization table complete
- [ ] Red flags list created
- [ ] No loopholes found in testing

**Do NOT:**
- Skip testing because "it's obvious"
- Move to next skill before current is bulletproof
- Deploy without completing checklist

## Example: Hardening a TDD Skill

### RED Phase - Baseline (No Skill)
**Scenario:** "Quick fix needed, just add this feature"

**Agent behavior:**
- Wrote implementation code immediately
- Rationalization: "It's just a simple addition"
- Said: "I'll write tests after to verify"

### GREEN Phase - Minimal Skill
```markdown
## The Iron Law

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

Write code before test? Delete it. Start over.
```

**Test result:** Agent now writes test first.

### REFACTOR Phase - Close Loophole
**New rationalization discovered:** "I'll keep the code as reference"

**Updated skill:**
```markdown
**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Delete means delete
```

**Re-test:** Passes.

## Version

v1.0.0 (2025-01-28) - Hardening-focused refactor of writing-skills