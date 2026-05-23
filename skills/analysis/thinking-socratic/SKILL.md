---
name: thinking-socratic
description: Systematic questioning framework to deepen understanding, challenge assumptions, and uncover hidden beliefs. Use for requirements gathering, debugging, coaching, and critical analysis.
---

# Socratic Questioning

## Overview
The Socratic Method, developed by the ancient Greek philosopher Socrates, uses systematic questioning to stimulate critical thinking and illuminate ideas. Rather than providing answers, it draws out knowledge by challenging assumptions and exploring implications.

**Core Principle:** Questions are more powerful than answers. The right question reveals what we don't know we don't know.

## When to Use
- Requirements gathering (understanding what stakeholders really need)
- Debugging (tracing assumptions to find root causes)
- Code review (understanding design decisions)
- Coaching and mentoring (helping others reach insights)
- Self-reflection (examining your own beliefs)
- Evaluating proposals or designs
- When someone says "obvious" or "everyone knows"

Decision flow:
```
Understanding seems shallow? → yes → APPLY SOCRATIC QUESTIONING
Assumptions unexamined?     → yes → APPLY SOCRATIC QUESTIONING
Root cause unclear?         → yes → APPLY SOCRATIC QUESTIONING
```

## The Six Types of Socratic Questions

### 1. Clarification Questions
**Purpose:** Ensure clear understanding of the claim or concept

| Question | Use When |
|----------|----------|
| "What do you mean by X?" | Term is ambiguous |
| "Can you give me an example?" | Concept is abstract |
| "How does this relate to Y?" | Connection unclear |
| "Can you rephrase that?" | Statement is confusing |
| "What is the main point?" | Discussion is scattered |

**Example:**
> "The system needs to be fast."
> → "What do you mean by 'fast'? What latency is acceptable?"
> → "Fast for whom? End users? Batch processes?"

### 2. Assumption-Probing Questions
**Purpose:** Expose underlying beliefs that may be unexamined

| Question | Use When |
|----------|----------|
| "What are we assuming here?" | Conclusion seems too quick |
| "Is this always true?" | Generalization made |
| "What if that assumption is wrong?" | Testing robustness |
| "Why do we believe this?" | Basis unclear |
| "What would have to change for this to be false?" | Finding conditions |

**Example:**
> "We need microservices for scale."
> → "What are we assuming about our scale requirements?"
> → "Is it always true that microservices scale better?"
> → "What if a modular monolith could meet our needs?"

### 3. Reason & Evidence Questions
**Purpose:** Examine the support for a claim

| Question | Use When |
|----------|----------|
| "What evidence supports this?" | Claim is asserted |
| "How do we know this?" | Source unclear |
| "Are there other explanations?" | Causation assumed |
| "What would prove this wrong?" | Testing falsifiability |
| "Is this evidence sufficient?" | Conclusion seems strong |

**Example:**
> "Users don't want feature X."
> → "What evidence do we have for this?"
> → "How many users did we ask? How were they selected?"
> → "Could there be other explanations for the feedback?"

### 4. Perspective & Viewpoint Questions
**Purpose:** Consider alternative angles and stakeholders

| Question | Use When |
|----------|----------|
| "How would X see this?" | Single perspective dominates |
| "What's the opposite view?" | No alternatives considered |
| "Who disagrees, and why?" | Consensus seems too easy |
| "What are we not seeing?" | Blind spots suspected |
| "How does this look from [role]?" | Stakeholder impact unclear |

**Example:**
> "This API design is intuitive."
> → "How would a new developer view this?"
> → "What would someone from a different language background expect?"
> → "Who might find this confusing, and why?"

### 5. Implication & Consequence Questions
**Purpose:** Explore downstream effects and logical conclusions

| Question | Use When |
|----------|----------|
| "What follows from this?" | Implications unexplored |
| "If this is true, what else must be true?" | Testing consistency |
| "What are the consequences?" | Impact unclear |
| "How does this affect X?" | Ripple effects not considered |
| "What are the second-order effects?" | Only immediate effects seen |

**Example:**
> "We'll add this field to the API response."
> → "What follows from adding this field?"
> → "How does this affect clients that don't need it?"
> → "What are the implications for backward compatibility?"

### 6. Questions About the Question
**Purpose:** Reflect on the inquiry itself; meta-level examination

| Question | Use When |
|----------|----------|
| "Why is this question important?" | Purpose unclear |
| "What would answering this tell us?" | Value of question unclear |
| "Is this the right question?" | May be missing the point |
| "What question should we be asking?" | Reframing needed |
| "Why are we asking this now?" | Timing or priority unclear |

**Example:**
> "Which database should we use?"
> → "Why is this question important right now?"
> → "What would answering this tell us that we don't know?"
> → "Is the real question about database, or about data modeling?"

## Application Patterns

### For Requirements Gathering
```
Stakeholder: "We need a dashboard."
Clarification: "What decisions will the dashboard help you make?"
Assumptions: "What are we assuming about who will use this?"
Evidence: "What data shows this is the highest priority?"
Perspective: "How do different user roles need different views?"
Implications: "If we build this, what won't we build?"
Meta: "Is a dashboard the best solution, or is there another approach?"
```

### For Debugging
```
Report: "The system is slow."
Clarification: "Which operations are slow? How slow?"
Assumptions: "What are we assuming about where the bottleneck is?"
Evidence: "What metrics/traces support this?"
Perspective: "Is it slow for all users or specific patterns?"
Implications: "If we fix this, what else might change?"
Meta: "Is 'slow' the right frame? Could it be 'inconsistent'?"
```

### For Design Review
```
Proposal: "We should use event sourcing."
Clarification: "What do you mean by event sourcing in this context?"
Assumptions: "What are we assuming about our query patterns?"
Evidence: "What evidence suggests this fits our use case?"
Perspective: "How would ops view this? New team members?"
Implications: "What are the consequences for debugging? Storage?"
Meta: "Is the real question about event sourcing or auditability?"
```

## Facilitation Tips
- **Genuine curiosity**: Ask because you want to understand, not to trap
- **Follow the thread**: Let answers guide next questions
- **Comfortable silence**: Allow time for reflection
- **Non-judgmental tone**: Questions should feel safe
- **Build on answers**: "That's interesting. Can you say more about..."
- **Admit ignorance**: "I don't understand. Help me see..."

## Verification Checklist
- [ ] Used questions from at least 3 of the 6 categories
- [ ] Probed assumptions underlying the topic
- [ ] Explored at least one alternative perspective
- [ ] Examined implications and consequences
- [ ] Reached deeper understanding than starting point
- [ ] Documented key insights from questioning

## Key Meta-Questions
- "What do I think I know, and how do I know it?"
- "What question am I not asking?"
- "What would change my mind about this?"
- "Who knows more about this than I do?"
- "What's the question behind the question?"

## Socrates' Reminder
"I know that I know nothing."

The goal is not to prove others wrong but to discover truth together. The best questions reveal what everyone—including the questioner—doesn't yet understand.
