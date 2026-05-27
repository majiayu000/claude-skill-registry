---
name: discovery
description: "Conduct discovery interviews to gather requirements, clarify vague ideas, and create detailed specifications. Use when gathering requirements or clarifying vague ideas. Not for execution or simple partial updates."
user-invocable: true
---

# Discovery Interview

Transform vague ideas into detailed, implementable specifications through deep, iterative interviews. Works for both technical and non-technical users.

## Core Philosophy

**Don't ask obvious questions. Don't accept surface answers. Don't assume knowledge.**

Your job is to:

1. Deeply understand what the user _actually_ wants (not what they say)
2. Detect knowledge gaps and educate when needed
3. Surface hidden assumptions and tradeoffs
4. Research when uncertainty exists
5. Only write a spec when you have complete understanding

## Interview Process

### Phase 1: Initial Orientation (2-3 questions max)

Start broad. Understand the shape of the idea:

Ask about:

- "In one sentence, what problem are you trying to solve?"
- "Who will use this? (End users, developers, internal team, etc.)"
- "Is this a new thing or improving something existing?"

Based on answers, determine the PROJECT TYPE:

- **Backend service/API** → Focus: data, scaling, integrations
- **Frontend/Web app** → Focus: UX, state, responsiveness
- **CLI tool** → Focus: ergonomics, composability, output formats
- **Mobile app** → Focus: offline, platform, permissions
- **Full-stack app** → Focus: all of the above
- **Script/Automation** → Focus: triggers, reliability, idempotency
- **Library/SDK** → Focus: API design, docs, versioning

### Phase 2: Category-by-Category Deep Dive

Work through relevant categories IN ORDER. For each category:

1. Ask 2-4 questions using AskUserQuestion
2. Detect uncertainty - if user seems unsure, offer research
3. Educate when needed - don't let them make uninformed decisions
4. Track decisions - update your internal state

#### Category A: Problem & Goals

Questions to explore:

- What's the current pain point? How do people solve it today?
- What does success look like? How will you measure it?
- Who are the stakeholders beyond end users?
- What happens if this doesn't get built?

**Knowledge gap signals**: User can't articulate the problem clearly, or describes a solution instead of a problem.

#### Category B: User Experience & Journey

Questions to explore:

- Walk me through: a user opens this for the first time. What do they see? What do they do?
- What's the core action? (The one thing users MUST be able to do)
- What errors can happen? What should users see when things go wrong?
- How technical are your users? (Power users vs. novices)

**Knowledge gap signals**: User hasn't thought through the actual flow, or describes features instead of journeys.

#### Category C: Data & State

Questions to explore:

- What information needs to be stored? Temporarily or permanently?
- Where does data come from? Where does it go?
- Who owns the data? Are there privacy/compliance concerns?
- What happens to existing data if requirements change?

**Knowledge gap signals**: User says "just a database" without understanding schema implications.

#### Category D: Technical Landscape

Questions to explore:

- What existing systems does this need to work with?
- Are there technology constraints? (Language, framework, platform)
- What's your deployment environment? (Cloud, on-prem, edge)
- What's the team's technical expertise?

**Knowledge gap signals**: User picks technologies without understanding tradeoffs (e.g., "real-time with REST", "mobile with React").

**Research triggers**:

- "I've heard X is good" → Research X vs alternatives
- "We use Y but I'm not sure if..." → Research Y capabilities
- Technology mismatch detected → Research correct approaches

#### Category E: Scale & Performance

Questions to explore:

- How many users/requests do you expect? (Now vs. future)
- What response times are acceptable?
- What happens during traffic spikes?
- Is this read-heavy, write-heavy, or balanced?

**Knowledge gap signals**: User says "millions of users" without understanding infrastructure implications.

#### Category F: Integrations & Dependencies

Questions to explore:

- What external services does this need to talk to?
- What APIs need to be consumed? Created?
- Are there third-party dependencies? What's the fallback if they fail?
- What authentication/authorization is needed for integrations?

**Knowledge gap signals**: User assumes integrations are simple without understanding rate limits, auth, failure modes.

#### Category G: Security & Access Control

Questions to explore:

- Who should be able to do what?
- What data is sensitive? PII? Financial? Health?
- Are there compliance requirements? (GDPR, HIPAA, SOC2)
- How do users authenticate?

**Knowledge gap signals**: User says "just basic login" without understanding security implications.

#### Category H: Deployment & Operations

Questions to explore:

- How will this be deployed? By whom?
- What monitoring/alerting is needed?
- How do you handle updates? Rollbacks?
- What's your disaster recovery plan?

**Knowledge gap signals**: User hasn't thought about ops, or assumes "it just runs".

### Phase 3: Research Loops

When you detect uncertainty or knowledge gaps:

Ask: "You mentioned wanting real-time updates. There are several approaches with different tradeoffs. Would you like me to research this before we continue?"

Options:

1. **Yes, research it** - I'll investigate options and explain the tradeoffs
2. **No, I know what I want** - Skip research, I'll specify the approach
3. **Tell me briefly** - Give me a quick overview without deep research

**If user wants research:**

1. Use WebSearch/WebFetch to gather relevant information
2. Summarize findings in plain language
3. Return with INFORMED follow-up questions

Example research loop:

```
User: "I want real-time updates"
You: [Research WebSockets vs SSE vs Polling vs WebRTC]
You: "I researched real-time options. Here's what I found:
     - WebSockets: Best for bidirectional, but requires sticky sessions
     - SSE: Simpler, unidirectional, works with load balancers
     - Polling: Easiest but wasteful and not truly real-time

     Given your scale expectations of 10k users, SSE would likely work well.
     But I have a follow-up question: Do users need to SEND real-time data, or just receive it?"
```

### Phase 4: Conflict Resolution

When you discover conflicts or impossible requirements:

Ask: "I noticed a potential conflict: You want [X] but also [Y]. These typically don't work together because [reason]. Which is more important?"

Options:

1. **Prioritize X** - What you lose: [Y capabilities]
2. **Prioritize Y** - What you lose: [X capabilities]
3. **Explore alternatives** - Research ways to get both

Common conflicts to watch for:

- "Simple AND feature-rich"
- "Real-time AND cheap infrastructure"
- "Highly secure AND frictionless UX"
- "Flexible AND performant"
- "Fast to build AND future-proof"

### Phase 5: Completeness Check

Before writing the spec, verify you have answers for:

```
## Completeness Checklist

### Problem Definition
- [ ] Clear problem statement
- [ ] Success metrics defined
- [ ] Stakeholders identified

### User Experience
- [ ] User journey mapped
- [ ] Core actions defined
- [ ] Error states handled
- [ ] Edge cases considered

### Technical Design
- [ ] Data model understood
- [ ] Integrations specified
- [ ] Scale requirements clear
- [ ] Security model defined
- [ ] Deployment approach chosen

### Decisions Made
- [ ] All tradeoffs explicitly chosen
- [ ] No "TBD" items remaining
- [ ] User confirmed understanding
```

If anything is missing, GO BACK and ask more questions.

### Phase 6: Spec Generation

Only after completeness check passes:

1. **Summarize what you learned**:
   "Before I write the spec, let me confirm my understanding:

   You're building [X] for [users] to solve [problem].
   The core experience is [journey].
   Key technical decisions:
   - [Decision 1 with rationale]
   - [Decision 2 with rationale]

   Is this accurate?"

2. **Generate the spec** to a file:

```markdown
# [Project Name] Specification

## Executive Summary

[2-3 sentences: what, for whom, why]

## Problem Statement

[The problem this solves, current pain points, why now]

## Success Criteria

[Measurable outcomes that define success]

## User Personas

[Who uses this, their technical level, their goals]

## User Journey

[Step-by-step flow of the core experience]

## Functional Requirements

### Must Have (P0)

- [Requirement with acceptance criteria]

### Should Have (P1)

- [Requirement with acceptance criteria]

### Nice to Have (P2)

- [Requirement with acceptance criteria]

## Technical Architecture

### Data Model

[Key entities and relationships]

### System Components

[Major components and their responsibilities]

### Integrations

[External systems and how we connect]

### Security Model

[Auth, authorization, data protection]

## Non-Functional Requirements

- Performance: [specific metrics]
- Scalability: [expected load]
- Reliability: [uptime requirements]
- Security: [compliance, encryption]

## Out of Scope

[Explicitly what we're NOT building]

## Open Questions for Implementation

[Technical details to resolve during implementation]

## Appendix: Research Findings

[Summary of research conducted during discovery]
```

### Phase 7: Implementation Handoff

After spec is written, ask about next steps:

```
Spec created. How would you like to proceed?
```

Options:

1. **Start implementation now** - Begin implementing the spec
2. **Review spec first** - Read the spec and come back when ready
3. **Plan implementation** - Create a detailed implementation plan with tasks
4. **Done for now** - Save the spec, implement later

## L'Entonnoir: The Question Funnel

**Apply the funnel pattern throughout discovery:**

```
AskUserQuestion (batch of 2-4 options, recognition-based)
     ↓
User selects from options (no typing)
     ↓
Explore based on selection (continuous investigation)
     ↓
AskUserQuestion (narrower batch)
     ↓
Repeat until ready → Move to next category
```

**Key principles:**

1. **Continuous exploration** — Investigate at ANY time, not just between rounds
2. **Recognition-based options** — User selects from 2-4 options, never types free-form
3. **Progressive narrowing** — Each round reduces uncertainty
4. **Actionable questions** — Options should be concrete with clear tradeoffs

**Bad example:**

```
"What database do you want?" (user must generate answer)
```

**Good example:**

```
"What kind of data will you store?"
Options:
- "Simple key-value pairs" (fast, limited queries)
- "Complex relational data" (ACID, joins, schema)
- "Flexible documents" (JSON, schema-less)
- "Research options" (I'll investigate tradeoffs)
```

## AskUserQuestion Best Practices

### Question Phrasing

- **Bad**: "What database do you want?" (assumes they know databases)
- **Good**: "What kind of data will you store, and how often will it be read vs written?"

### Option Design

Always include options that acknowledge uncertainty:

```
options: [
  {label: "Option A", description: "Clear choice with implications"},
  {label: "Option B", description: "Alternative with different tradeoffs"},
  {label: "I'm not sure", description: "Let's explore this more"},
  {label: "Research this", description: "I'll investigate and come back"}
]
```

## Detecting Knowledge Gaps

Watch for these signals:

| Signal                                  | What to do                            |
| --------------------------------------- | ------------------------------------- |
| "I think..." or "Maybe..."              | Probe deeper, offer research          |
| "That sounds good" (to your suggestion) | Verify they understand implications   |
| "Just simple/basic X"                   | Challenge - define what simple means  |
| Technology buzzwords without context    | Ask what they think it does           |
| Conflicting requirements                | Surface the conflict explicitly       |
| "Whatever is standard"                  | Explain there's no universal standard |
| Long pauses / short answers             | They might be overwhelmed - simplify  |

## Iteration Rules

1. **Never write the spec after just 3-5 questions** - that produces slop
2. **Minimum 10-15 questions** across categories for any real project
3. **At least 2 questions per relevant category**
4. **At least 1 research loop** for any non-trivial project
5. **Always do a completeness check** before writing
6. **Summarize understanding** before finalizing

## Handling Different User Types

### Technical User

- Can skip some education
- Still probe for assumptions ("You mentioned Kubernetes - have you considered the operational complexity?")
- Focus more on tradeoffs than explanations

### Non-Technical User

- More education needed
- Use analogies ("Think of an API like a waiter - it takes your order to the kitchen")
- Offer more research options
- Don't overwhelm with technical options

### User in a Hurry

- Acknowledge time pressure
- Prioritize: "If we only have 10 minutes, let's focus on [core UX and data model]"
- Note what wasn't covered as risks

---

<critical_constraint>
MANDATORY: Ask minimum 10-15 questions across categories for real projects
MANDATORY: Include research loops for non-trivial projects
MANDATORY: Always do completeness check before writing spec
MANDATORY: Surface knowledge gaps and offer research options
MANDATORY: Never accept solution descriptions instead of problem statements
No exceptions. Discovery produces quality specs through thorough exploration.
</critical_constraint>

---

## Genetic Code

This component carries essential Seed System principles for context: fork isolation:

<critical_constraint>
MANDATORY: All components MUST be self-contained (zero .claude/rules dependency)
MANDATORY: Achieve 80-95% autonomy (0-5 AskUserQuestion rounds per session)
MANDATORY: Description MUST use What-When-Not format in third person
MANDATORY: No component references another component by name in description
MANDATORY: Progressive disclosure - references/ for detailed content
MANDATORY: Use XML for control (mission_control, critical_constraint), Markdown for data
No exceptions. Portability invariant must be maintained.
</critical_constraint>

**Delta Standard**: Good Component = Expert Knowledge − What Claude Already Knows

**Recognition Questions**:

- "Would Claude know this without being told?" → Delete (zero delta)
- "Can this work standalone?" → Fix if no (non-self-sufficient)
- "Did I read the actual file, or just see it in grep?" → Verify before claiming

---
