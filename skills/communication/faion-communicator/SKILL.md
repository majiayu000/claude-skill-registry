---
name: faion-communicator
description: "Communication: stakeholder dialogue, Mom Test, conflict resolution, feedback, storytelling."
user-invocable: false
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Faion Communicator

**Communication: User's language.**

Universal communication skill for effective dialogue with stakeholders, customers, team members, and decision-makers. From requirements gathering to selling ideas.

---

## Decision Tree: Quick Routing

| If you need... | Use | File |
|----------------|-----|------|
| **Customer validation** | The Mom Test | [mom-test](mom-test.md) |
| **Requirements gathering** | Stakeholder Communication | [stakeholder-communication](stakeholder-communication.md) |
| **Deep understanding** | Active Listening (RASA) | [active-listening](active-listening.md) |
| **Resolve conflict** | Thomas-Kilmann, NVC | [conflict-resolution](conflict-resolution.md) |
| **Give feedback** | SBI, Radical Candor | [feedback](feedback.md) |
| **Receive feedback** | Listen, clarify, thank | [feedback](feedback.md) |
| **Pitch to executives** | Pyramid Principle, SCQA | [selling-ideas](selling-ideas.md) + [business-storytelling](business-storytelling.md) |
| **Technical persuasion** | Evidence-based | [selling-ideas](selling-ideas.md) |
| **Sales context** | SPIN Selling, Challenger | [selling-ideas](selling-ideas.md) |
| **Performance issues** | Crucial Conversations | [difficult-conversations](difficult-conversations.md) |
| **Deliver bad news** | Direct, empathetic | [difficult-conversations](difficult-conversations.md) |
| **Negotiate contract** | BATNA, Principled | [negotiation](negotiation.md) |
| **Generate ideas (group)** | Classic, 6-3-5, Round Robin | [brainstorming-ideation](brainstorming-ideation.md) |
| **Generate ideas (solo)** | SCAMPER, Mind Mapping | [brainstorming-ideation](brainstorming-ideation.md) |

**By stakeholder:**
- Customers → mom-test | Executives → selling-ideas + business-storytelling
- Team → feedback | Peers → conflict-resolution | External → stakeholder-communication

**Common sequences:**
- Customer discovery: mom-test → active-listening → stakeholder-communication
- Difficult feedback: feedback → difficult-conversations → active-listening
- Proposal/pitch: selling-ideas → business-storytelling → negotiation

---

## Overview

This skill provides communication methodologies for:
- **Stakeholder Dialogue** - Interview, brainstorm, clarify, validate
- **Customer Validation** - The Mom Test, discovery interviews
- **Conflict Resolution** - Thomas-Kilmann modes, NVC
- **Feedback** - SBI, Radical Candor, receiving feedback
- **Selling Ideas** - SPIN, Challenger, pitching techniques
- **Storytelling** - Pyramid Principle, SCQA, Pixar
- **Negotiation** - Principled negotiation, persuasion
- **Difficult Conversations** - Crucial conversations framework
- **Brainstorming** - SCAMPER, Mind Mapping, 6-3-5, facilitation

---

## Context Discovery

### Auto-Investigation

| Signal | Check For | Why |
|--------|-----------|-----|
| Meeting notes | Interview transcripts, stakeholder feedback | Communication patterns |
| User research docs | Customer validation notes | Mom Test usage |
| Pitch decks | Presentation structure (SCQA, Pyramid) | Storytelling approach |
| Feedback documents | SBI format, 1-on-1 notes | Feedback culture |
| Conflict logs | Issue resolution patterns | Conflict style |

### Discovery Questions

```yaml
questions:
  - question: "What's your communication goal?"
    options:
      - label: "Gather requirements"
        description: "Use active-listening, stakeholder-communication"
      - label: "Validate business idea"
        description: "Use mom-test"
      - label: "Resolve conflict"
        description: "Use conflict-resolution, difficult-conversations"
      - label: "Give/receive feedback"
        description: "Use feedback (SBI, Radical Candor)"
      - label: "Pitch or persuade"
        description: "Use selling-ideas, business-storytelling"

  - question: "Who is your audience?"
    options:
      - label: "Customers/users"
        description: "Favor mom-test, active-listening"
      - label: "Executives/stakeholders"
        description: "Favor selling-ideas, business-storytelling"
      - label: "Team members"
        description: "Favor feedback, conflict-resolution"
      - label: "External partners"
        description: "Favor negotiation, stakeholder-communication"

  - question: "What's the context?"
    options:
      - label: "Discovery/research phase"
        description: "Use mom-test, active-listening"
      - label: "Decision-making"
        description: "Use selling-ideas, negotiation"
      - label: "Performance/sensitive topic"
        description: "Use difficult-conversations, feedback"
      - label: "Idea generation"
        description: "Use brainstorming-ideation"
```

---

## When to Use

| Situation | Methodology |
|-----------|-------------|
| Gathering requirements | active-listening, stakeholder-communication |
| Validating business ideas | mom-test |
| Team disagreements | conflict-resolution |
| Performance reviews | feedback |
| Pitching to stakeholders | selling-ideas |
| Presentations | business-storytelling |
| Contract discussions | negotiation |
| Sensitive topics | difficult-conversations |
| Generating ideas | brainstorming-ideation |

---

## All Methodologies (10)

| Name | Key Frameworks | File |
|------|----------------|------|
| Active Listening | RASA, Empathic Listening, Reflective | [active-listening](active-listening.md) |
| The Mom Test | Rob Fitzpatrick's validation | [mom-test](mom-test.md) |
| Stakeholder Communication | Interview, Brainstorm, Clarify, Validate, Socratic | [stakeholder-communication](stakeholder-communication.md) |
| Conflict Resolution | Thomas-Kilmann, NVC | [conflict-resolution](conflict-resolution.md) |
| Giving & Receiving Feedback | SBI, SBII, Radical Candor, EEC | [feedback](feedback.md) |
| Selling Ideas | SPIN Selling, Challenger Sale, Elevator Pitch | [selling-ideas](selling-ideas.md) |
| Business Storytelling | Pyramid Principle, SCQA, Pixar Framework | [business-storytelling](business-storytelling.md) |
| Negotiation & Persuasion | Principled Negotiation, BATNA, Cialdini's 6 | [negotiation](negotiation.md) |
| Difficult Conversations | Crucial Conversations, DESC Script | [difficult-conversations](difficult-conversations.md) |
| Brainstorming & Ideation | SCAMPER, Mind Mapping, 6-3-5, Reverse | [brainstorming-ideation](brainstorming-ideation.md) |

---

## Quick Reference

### Active Listening: RASA
```
Receive → Appreciate → Summarize → Ask
```

### The Mom Test: 3 Rules
1. Talk about their life, not your idea
2. Ask about past specifics, not future hypotheticals
3. Talk less, listen more

### Thomas-Kilmann: 5 Modes
```
Competing | Collaborating | Compromising | Avoiding | Accommodating
```

### Radical Candor: 2 Dimensions
```
Care Personally + Challenge Directly = Radical Candor
```

### SPIN: 4 Question Types
```
Situation → Problem → Implication → Need-Payoff
```

### Pyramid Principle: Structure
```
Lead with answer → Support with arguments → Base with evidence
```

### Brainstorming: Osborn's 4 Rules
1. Defer judgment
2. Go for quantity
3. Encourage wild ideas
4. Build on others' ideas

---

## Integration with Faion Network

### Used by Skills

| Skill | Uses Methodologies |
|-------|-------------------|
| faion-business-analyst | active-listening, stakeholder-communication, conflict-resolution, brainstorming-ideation |
| faion-product-manager | mom-test, selling-ideas, business-storytelling, brainstorming-ideation |
| faion-project-manager | conflict-resolution, feedback, negotiation |
| faion-researcher | mom-test, stakeholder-communication, brainstorming-ideation |
| faion-marketing-manager | selling-ideas, business-storytelling |
| faion-ux-ui-designer | active-listening, stakeholder-communication, brainstorming-ideation |

### Interactive Mode (faion-net)

When faion-net runs in Interactive mode, use these methodologies:

```python
# For requirements gathering
Apply: active-listening + stakeholder-communication

# For idea validation
Apply: mom-test

# For presenting proposals
Apply: selling-ideas + business-storytelling

# For disagreements
Apply: conflict-resolution

# For idea generation
Apply: brainstorming-ideation
```

---

## References

**Research sources:**
- [The Mom Test by Rob Fitzpatrick](https://tianpan.co/blog/2025-04-29-the-mom-test)
- [Thomas-Kilmann Conflict Model](https://www.mtdtraining.com/blog/thomas-kilmann-conflict-management-model.htm)
- [SBI Feedback Model](https://www.ccl.org/articles/leading-effectively-articles/closing-the-gap-between-intent-vs-impact-sbii/)
- [Radical Candor by Kim Scott](https://www.radicalcandor.com/blog/give-feedback-playbook)
- [SPIN Selling by Neil Rackham](https://www.gong.io/blog/spin-selling)
- [Challenger Sale by Dixon & Adamson](https://challengerinc.com/what-is-challenger-sales-methodology/)
- [Pyramid Principle by Barbara Minto](https://productmindset.substack.com/p/2836-mckinseys-pyramid-framework)
- [SCQA Framework](https://www.theanalystacademy.com/powerpoint-storytelling/)
- [Pixar Storytelling Framework](https://www.causevox.com/blog/pixar-pitch-framework/)
- [Crucial Conversations by Patterson et al.](https://cruciallearning.com/crucial-conversations-book/)
- [SCAMPER by Bob Eberle](https://www.mindtools.com/a88wtia/scamper)

---

*Faion Communicator v2.0.0*
*10 Methodologies | From Requirements to Negotiation*
