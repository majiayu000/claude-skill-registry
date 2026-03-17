---
name: user-interview
description: "Requirements elicitation through structured interviewing. Use when: (1) User provides vague, ambiguous, or incomplete requirements, (2) Clarification is needed before building features or writing code, (3) User says 'build X' without specifying behavior, edge cases, or constraints, (4) Translating stakeholder requests into PRDs, specs, or user stories. Triggers on phrases like 'make it better', 'add a feature', 'fix this', 'I need something that...', or any request lacking concrete acceptance criteria."
---

# User Interview Skill

Transform vague requirements into actionable specifications through structured questioning.

## Core Principles

**Past behavior over future intentions.** Never ask "Would you use X?" — ask "Tell me about the last time you tried to solve this." Ground every discussion in concrete past experiences.

**Problems over solutions.** When users describe solutions ("add a dropdown"), redirect to problems: "What problem does that solve?" and "What would that enable you to do?"

**Specifics over generalities.** When users speak abstractly ("it's frustrating"), immediately anchor: "Can you give me a specific example?" or "When did that last happen?"

**One question at a time.** Never overwhelm with multiple questions. Ask the most important question, wait for the answer, then follow up.

## Interview Flow

### Phase 1: Context Discovery

Start broad, understand the landscape:

```
- "What are you trying to accomplish?"
- "Walk me through what happens today when you [do this task]."
- "What triggered this request? What happened recently?"
```

### Phase 2: Problem Validation

Confirm the problem exists and matters:

```
- "How are you solving this today?"
- "What's the hardest part about that?"
- "What have you already tried?"
- "How much time/money does this cost you?"
```

### Phase 3: Constraint Mapping

Identify boundaries and requirements:

```
- "Who else uses this? Who else is affected?"
- "What would a successful outcome look like?"
- "What would make this a failure?"
- "Are there any technical/business/time constraints I should know about?"
- "What's definitely out of scope?"
```

### Phase 4: Edge Case Exploration

Surface hidden complexity:

```
- "What happens when [X goes wrong]?"
- "What's the most unusual case you've encountered?"
- "Are there exceptions to how this normally works?"
- "What happens if [user does unexpected thing]?"
```

### Phase 5: Priority Clarification

Distinguish must-haves from nice-to-haves:

```
- "If you could only have one thing, what would it be?"
- "What would you cut if we had half the time?"
- "Is this blocking something else?"
```

## Probing Techniques

Use these when responses are vague or incomplete:

| Technique | When to Use | Example |
|-----------|-------------|---------|
| Echo probe | Encourage elaboration | "It felt 'clunky'?" |
| Specificity probe | Vague statement | "Can you give me a specific example?" |
| Contrast probe | Unclear criteria | "What would good vs bad look like?" |
| Why probe | Surface motivation | "Why is that important?" |
| Consequence probe | Understand impact | "What happens if we don't do this?" |

**Five Whys**: For root cause analysis, ask "Why?" iteratively (usually 3-5 times) until you reach the underlying need.

## Validation Signals

**Real interest** manifests as:
- Time commitment (willing to discuss further, bring others)
- Existing workarounds (already trying to solve it)
- Quantifiable pain (can estimate time/money lost)
- Urgency indicators (deadlines, blocking issues)

**Warning signs** of unclear requirements:
- "Make it better/faster/easier" without measurable criteria
- "Like [competitor] but different" without specifying how
- Different stakeholders interpret the requirement differently
- Cannot write acceptance criteria
- Requirements describe HOW instead of WHAT

## Output: Translating to Specs

When you have sufficient clarity, produce the appropriate artifact or hand off to a downstream workflow:

**User Stories** - For discrete implementable units:
```
As a [user type], I want to [action] so that [benefit].

Acceptance Criteria:
- Given [context], when [action], then [result]
- Given [context], when [action], then [result]
```

**Technical Spec** - For implementation-focused requirements. See `references/tech-spec-template.md`

**PRD Handoff** - For formal PRDs, use the `workflow-create-prd` skill using the insights gathered here.

## Completeness Checklist

Before generating output, verify:

- [ ] Core problem is validated (not just assumed)
- [ ] Success criteria are measurable
- [ ] Edge cases identified
- [ ] Scope boundaries explicit (in AND out)
- [ ] User/actor types identified
- [ ] Constraints documented (technical, business, time)
- [ ] Priorities clear (must-have vs nice-to-have)
- [ ] No conflicting requirements remain unresolved

## What NOT to Do

- **Don't ask leading questions**: "Wouldn't it be great if...?" biases responses
- **Don't suggest solutions**: Let users describe problems first
- **Don't accept first answer**: Probe deeper, especially on "why"
- **Don't ask hypotheticals**: "Would you use X?" yields unreliable data
- **Don't ask multiple questions at once**: One question, one answer
- **Don't assume shared understanding**: Clarify ambiguous terms

## Quick Reference by Situation

| Situation | Start With |
|-----------|------------|
| "Build me X" | "What problem does X solve for you?" |
| "Make it better" | "Better in what way? What's not working now?" |
| "Like [competitor]" | "What specifically about [competitor] do you want?" |
| "It's broken" | "Walk me through what happened." |
| "Add a feature" | "What would that feature let you do that you can't do now?" |
| User describes solution | "Interesting—what problem are you trying to solve?" |
| User can't articulate | "Can you show me how you do this today?" |

## References

- `references/tech-spec-template.md` - Technical specification template
- `references/question-bank.md` - Extended question library by category
- `references/failure-modes.md` - Common requirements gathering failures and how to avoid them

## Integration with Workflows

This skill is upstream of the `workflow-create-prd` skill. Once the interview is complete and requirements are clarified:
- Suggest using `workflow-create-prd` to formalize the requirements into a structured PRD.
- Use the `Technical Spec` template for implementation-focused requirements when a full PRD is not necessary.
