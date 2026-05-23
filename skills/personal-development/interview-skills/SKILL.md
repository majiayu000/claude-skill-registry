---
name: interview-skills
description: Frameworks for technical interviews and salary negotiation. Use for behavioral interview prep (STAR method), technical interview communication, offer evaluation, and compensation negotiation strategies.
allowed-tools: Read, Glob, Grep
---

# Interview Skills

This skill provides frameworks for excelling in technical interviews and negotiating job offers effectively.

## When to Use This Skill

- Preparing for behavioral interview questions
- Practicing the STAR method for storytelling
- Planning how to communicate during technical interviews
- Evaluating a job offer
- Preparing to negotiate salary or compensation
- Deciding whether to accept or counter an offer

## Core Frameworks

### STAR Method for Behavioral Questions

Structure answers to behavioral questions ("Tell me about a time when...") using STAR:

| Component | % of Answer | Purpose |
| --------- | ----------- | ------- |
| **S**ituation | 10% | Set the context |
| **T**ask | 10% | Your specific responsibility |
| **A**ction | 60% | What you did (the meat) |
| **R**esult | 20% | Outcomes with metrics |

**Example Structure:**

```text
"Tell me about a time you resolved a conflict on your team."

SITUATION (10%): "On my last project, two senior engineers disagreed
about the database architecture - one wanted PostgreSQL, the other MongoDB."

TASK (10%): "As the tech lead, I needed to help them reach a decision
that the whole team could support without damaging their relationship."

ACTION (60%): "First, I scheduled a meeting where each could present
their case with specific criteria: performance requirements, team expertise,
and maintenance burden. Then I created a decision matrix we could score together.
When scores were close, I facilitated a discussion about what mattered most
for THIS project specifically. I made sure both felt heard by summarizing
their key points before moving on."

RESULT (20%): "We chose PostgreSQL based on the team's existing expertise.
Both engineers felt the process was fair - one even said it was the best
technical decision process he'd experienced. The project launched on time
and we haven't had database issues in 18 months."
```

**Full reference with 5 example stories:** `references/star-method.md`

### Technical Interview Communication

Beyond coding ability, how you communicate matters:

#### Think Aloud

- Verbalize your thought process constantly
- "I'm thinking about using a hash map here because..."
- "Let me consider the edge cases..."
- Silence is your enemy - interviewers can't evaluate what they can't hear

#### Ask Clarifying Questions (First 5-10 Minutes)

- Input format and constraints
- Expected output
- Edge cases and error handling
- Performance requirements
- Example inputs/outputs

#### Drive the Conversation

- Don't wait to be led
- Propose your approach before coding
- Explain trade-offs proactively
- Check in: "Does this approach make sense before I implement?"

#### Handle "I Don't Know" Honestly

- "I haven't worked with that technology, but here's how I'd approach learning it..."
- "I'm not sure about the exact syntax, but the concept is..."
- Never pretend to know something you don't

### Salary Negotiation Framework

Negotiation is expected and professional. Most offers have room to negotiate.

#### Before Negotiating

1. **Research market rates**
   - levels.fyi for tech companies
   - Glassdoor for ranges
   - Blind for crowdsourced data
   - Talk to people in similar roles

2. **Know your BATNA**
   - Best Alternative To Negotiated Agreement
   - Your leverage depends on alternatives
   - Never negotiate from desperation

3. **Wait for the formal offer**
   - Don't discuss numbers until you have a written offer
   - "I'd prefer to discuss compensation once we're both sure about fit"

#### Negotiation Tactics

| Tactic | Example |
| ------ | ------- |
| Use email | Written negotiation is documented and thoughtful |
| State a range | "$150K-$160K based on my research" |
| Cite specifics | "Based on levels.fyi data for this role..." |
| Negotiate holistically | Salary, equity, sign-on, PTO, remote work |
| Express enthusiasm | "I'm excited about this role" + negotiation |

**Full reference with scripts and tactics:** `references/salary-negotiation.md`

### Handling Lowball Offers

When an offer is below expectations:

1. **Don't react emotionally** - Stay professional
2. **Defer response** - "Let me think about that and get back to you"
3. **Gather data** - Research what the role should pay
4. **Counter with evidence** - Not just "I want more"
5. **Be willing to walk** - Sometimes offers can't be fixed

## Story Bank Strategy

Prepare 3-5 versatile stories that can answer multiple question types:

| Story Theme | Can Answer Questions About |
| ----------- | -------------------------- |
| Technical challenge | Problem-solving, learning, complexity |
| Team conflict | Conflict resolution, communication, leadership |
| Project under pressure | Stress, prioritization, delivery |
| Mistake/failure | Learning, humility, growth |
| Cross-team collaboration | Influence, stakeholder management |

Each story should include:

- Quantified results where possible
- Your specific actions (not team actions)
- What you learned
- What you'd do differently

## Related Resources

- `references/star-method.md` - Full STAR examples for common questions
- `references/salary-negotiation.md` - Detailed negotiation tactics and scripts
- `/soft-skills:prep-interview` command - Structure your interview stories
- `professional-communication` skill - General communication frameworks

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
