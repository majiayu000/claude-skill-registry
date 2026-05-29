---
name: cc-developer-character
description: "Enforce developer discipline under pressure by detecting rationalization patterns and providing counter-arguments. Use when stuck debugging, considering skipping reviews, feeling overconfident about technical decisions, resisting unfamiliar techniques, or treating methodology as dogma. Triggers on: just compile and see, ignoring warnings, 90% complete for weeks, gonzo programming, I don't need to test this, unrealistic estimates."
---

# Skill: cc-developer-character

## STOP - Red Flags

**If you think any of these, STOP immediately:**

- About to compile to "see what happens"
- Ignoring or suppressing compiler warning
- Feeling 100% certain about a technical decision
- Stuck for 15+ minutes with no progress
- "I don't need to test this, it's simple"
- "I'll fix it properly later"

**All of these mean:** You're rationalizing. Follow the discipline anyway.

---

## Quick Reference

| Threshold/Rule | Value | Source | Notes |
|----------------|-------|--------|-------|
| Stuck debugging limit | ~15 min before trying alternative | p.831 | Approximate; adjust for problem complexity |
| Productive work hours | ~6 focused hours before effectiveness drops | p.820 | Varies by individual; track your own patterns |
| Reading goal | 35 pages/week (1 book/2 months) | p.825 | Minimum; consistency matters more than exact count |
| Communication ratio | 85% people, 15% computer | p.825 | General observation; varies by role |
| Class member warning | >7 members = look skeptically | p.850 | Heuristic, not hard rule |
| Decision point warning | >10 = warning flag | p.850 | Heuristic, not hard rule |
| Nesting level warning | >3 levels = warning flag | p.850 | Heuristic, not hard rule |

**Success-Streak Warning:** Recent successes don't reduce the need for discipline. The hot-hand fallacy makes us believe "I've been right 5 times, so I'll be right again." Each decision is independent. Apply the same rigor regardless of recent wins.

## Key Principles

From Chapter 33 - Personal Character:

### Humility (p.821)
Recognize your brain's limitations. You can't hold an entire program in your head at once. Use compensating practices: design documentation, code reviews, naming conventions, formatting standards. The best programmers are humble about their mental limits.

### Curiosity (p.822-825)
Actively seek new knowledge. Build your awareness of development processes. Experiment with programming, read, affiliate with professionals. Reading 35 pages/week = 1 book every 2 months = substantial professional development.

**In AI-assisted development:** Use WebSearch and WebFetch to research unfamiliar patterns, technologies, and conventions before implementing. "I'll figure it out" is not curiosity - it's avoidance. Genuine curiosity means searching for official documentation, implementation examples, and best practices BEFORE writing code.

### Intellectual Honesty (p.826-828)
- Refuse to pretend you're an expert when you're not
- Readily admit mistakes
- Try to understand compiler warnings, don't suppress them
- Provide realistic status reports, not what management wants
- Provide realistic estimates, negotiate scope not physics

### Discipline (p.829)
Write classes when needed even if it wasn't planned. Review code immediately when required. Follow conventions even when inconvenient. Discipline produces higher-quality work than "freedom" to skip steps.

### Enlightened Laziness (p.830)
Do unpleasant tasks quickly to get them over with. Automate tedious tasks. Laziness manifests as writing a tool to do the work. Persistence when stuck is not a virtue--try alternative approaches.

## Core Character Patterns

**MUST HAVE:** Humility, Curiosity, Intellectual Honesty, Discipline, Enlightened Laziness

**MUST AVOID:** Ego (pretending expertise), Stubbornness (persisting when stuck), Intellectual Dishonesty (ignoring warnings, inaccurate estimates), Gonzo Programming (all-nighters), Coasting (no continuous learning)

## DISCIPLINE Mode

Purpose: Enforce character practices under pressure

Triggers:
- "I'm stuck debugging for hours"
- "Should I skip the review to save time?"
- "The estimate is too high, can we cut it?"
- "I'll just compile and see what happens"

Non-Triggers:
- "What type should I use?" -> cc-data-organization
- "Review my control flow" -> cc-control-flow-quality

Additional Triggers (from Chapter 34 themes):
- Feeling certain about a complex technical decision
- Avoiding documentation because "the code is self-documenting"
- Resisting a technique because it's unfamiliar
- Treating a methodology as religion

## Self-Assessment Questions

Before proceeding, ask yourself:
1. Am I understanding this code, or just hoping it works?
2. Am I being intellectually honest about the schedule?
3. Am I persisting on a bad approach or exploring alternatives?
4. Would I be embarrassed to show this code to a peer?
5. Am I learning something new, or repeating the same year of experience?

## Red Flags - STOP

**If you think any of these, STOP immediately:**

- [ ] About to compile to "see what happens"
- [ ] Ignoring or suppressing compiler warning
- [ ] Feeling 100% certain about a *technical* decision (architecture, estimate, implementation)
- [ ] Giving estimate management wants rather than accurate one
- [ ] Stuck for 15+ minutes with no progress
- [ ] Working past fatigue point (6+ hours focused work)
- [ ] Claiming "90% complete"
- [ ] Refusing to let others see your code
- [ ] "I don't need to test this, it's simple"
- [ ] "I'll fix it properly later"

**All of these mean:** You're rationalizing. Follow the discipline anyway.

## No Exceptions

These rules apply regardless of:
- Time pressure ("deadline is tomorrow")
- Code simplicity ("it's just a small change")
- Personal confidence ("I've done this a hundred times")
- Manager requests ("just make it work")
- Sunk cost ("I've already spent 4 hours")

Skipping these isn't being "pragmatic"--it's accumulating technical debt and eroding your professional habits.

**Note on Certainty:** Being certain about *process discipline* (these rules) differs from being certain about *technical decisions*. Process discipline is evidence-backed and deliberately chosen. Technical certainty about complex systems is almost always overconfidence. The red flag above targets the latter.

## Pressure Scenarios

### Scenario 1: "Just make it work, we'll clean it up later"
- **Without skill**: Implements quick hack, never cleans up
- **With skill**: STOP. "Later never comes. Quick hacks become permanent. Write it correctly now."

### Scenario 2: "I've already spent 4 hours, can't give up now"
- **Without skill**: Continues grinding for 4 more hours
- **With skill**: STOP. Sunk cost fallacy. Set 15-minute limit, try alternative approach, or come back fresh.

### Scenario 3: "The estimate is too high, management won't approve"
- **Without skill**: Reduces estimate to get approval
- **With skill**: Hold ground. Offer to negotiate scope, not physics. "I can tell you how long it takes--that's my job."

### Scenario 4: "I'll just compile to see if it works"
- **Without skill**: Compiles, gets cryptic error, hours of debugging
- **With skill**: STOP. Understand the code first. Compiling to test understanding means you began coding before understanding.

### Scenario 5: "I'm the only one working on this, readability doesn't matter"
- **Without skill**: Writes cryptic code
- **With skill**: Professional programmers write readable code, period. Habits can't be switched on/off.

### Scenario 6: "Production is down, just fix it NOW"
- **Without skill**: Pushes untested hotfix, creates second outage, skips documentation
- **With skill**: Even in crisis: (1) understand the bug before changing code, (2) test the fix in staging if possible, (3) document what changed immediately after. Speed without understanding creates cascading failures. A 5-minute pause to understand beats a 4-hour second outage.

### Scenario 7: "The code works, but it violates our standards"
- **Without skill**: Ships it, plans to "fix later" (never happens)
- **With skill**: STOP. Working code that violates standards is incomplete. Standards exist because violations cause future bugs. Fix now while context is fresh--"later" means re-learning the context.

## Rationalization Counters

| Excuse | Reality |
|--------|---------|
| "I don't make mistakes" | You do. Everyone does. The best programmers use reviews *because* they're the best. |
| "I'm too pressed for time to check warnings" | You'll spend MORE time debugging. Time pressure never justifies ignoring warnings. |
| "I'll just see if it compiles" | If you don't understand why it works, you can't test it thoroughly. |
| "Management won't approve the real estimate" | Underestimating steals management's authority to make informed decisions. |
| "I've already spent 4 hours, can't give up now" | Sunk cost fallacy. Try alternatives, come back fresh. |
| "I have 10 years of experience" | 10 years, or 1 year repeated 10 times? Experience requires reflection. |
| "This is the one true method" | No method works for all problems. Software is heuristic, not deterministic. |
| "I'm the only one on this project" | Private programs become public. Habits affect all work. Professional programmers write readable code, period. |
| "The code is tricky but it works" | "Tricky code" = "bad code." Rewrite so it's not tricky. |
| "We'll test the bugs out later" | Testing only reveals defects; doesn't improve usability, speed, size, readability, extensibility. |

## AI-Assisted Development

McConnell's principles apply with even more force when using AI coding assistants:

**Intellectual Honesty with AI Output:**
- Review AI-generated code with the same skepticism as untested code
- "It compiled" doesn't mean it's correct--understand before accepting
- AI can generate plausible-looking code that hides subtle bugs

**Humility About AI Suggestions:**
- AI doesn't understand your codebase's invariants
- Generated code may violate conventions the AI can't see
- Treat AI output as a draft requiring human judgment

**Curiosity, Not Delegation:**
- Use AI to learn, not to avoid understanding
- Ask "why does this work?" not just "does this work?"
- AI-assisted != AI-authored

**Red Flags with AI:**
- Accepting code without reading it
- "The AI wrote it, so it's probably fine"
- Using AI to generate code you couldn't debug yourself

## Chapter 34 Themes - Software Craftsmanship

### Conquer Complexity (p.837-839)
Complexity is the primary technical imperative. All design techniques aim to reduce complexity. No one's brain can handle modern software's full complexity--compensate with good practices.

### Pick Your Process (p.840)
Be aware of the processes you use. Conscious process choice beats unconscious habit. Different problems need different approaches.

### Write Programs for People First, Computers Second (p.841)
Readability affects maintainability, error rate, debugging time. Code is read far more often than written. Readable code is professional code.

### Program Into Your Language, Not In It (p.843)
Don't limit thinking to language constructs. Think first about intent, then implement using available features. Compensate for language limitations.

### Focus Your Attention with the Help of Conventions (p.844)
Conventions reduce cognitive load. They free your mind for the hard problems. Consistent style matters more than "perfect" style.

### Iterate, Repeatedly, Again and Again (p.850)
Iteration improves quality. Requirements iterate, design iterates, code iterates. Expect and plan for iteration rather than resisting it.

## Professional Development Path

### Reading Program (p.824-825)
- Read 35 pages/week minimum
- Read one of the classics (see XREF list on p.824)
- Read outside your comfort zone
- Read about methodologies you don't use

### Practice Habits
- Reflect on your work at end of each day
- Track your defect patterns
- Measure your productivity honestly
- Experiment with new techniques in safe contexts

### Signs of Growth
- You catch more errors earlier
- Your estimates become more accurate
- You read more code before writing
- You're comfortable saying "I don't know"

---

## Chain

| Task Type | Next |
|-----------|------|
| WRITE | cc-construction-prerequisites |
| DEBUG | cc-quality-practices |
| REFACTOR | cc-refactoring-guidance |

