---
name: af-brainstorm-ideas
description: Guide collaborative brainstorming sessions that produce structured documents for Discovery. Use when starting a new product idea, running ideation workshops, or preparing concept documents for AgentFlow import.

# AgentFlow documentation fields
title: Ideation Expertise
created: 2026-02-25
updated: 2026-02-25
last_checked: 2026-02-25
tags: [skill, expertise, ideation, brainstorming, discovery, pre-discovery]
parent: ../README.md
related:
  - ../af-discover-scope/SKILL.md
  - ../../templates/ideation-document.md
  - ../../docs/guides/discovery-guide.md
---

# Ideation Expertise

## Purpose

Ideation is the creative, divergent-thinking phase that happens **before** Discovery. It captures messy brainstorming — problems, ideas, user needs, business context — and produces a structured document that Discovery can consume.

**Key principle:** Ideation is **tool-agnostic**. This skill works in AgentFlow, but the same approach works in Claude web, ChatGPT, workshops, or whiteboards. The output format is what matters, not the tool.

## Portable Skill

This skill is designed to be **portable**. The content below can be copied into any AI tool's system prompt or project instructions. Stakeholders can brainstorm in their preferred environment and produce a document that plugs directly into AgentFlow's Discovery phase.

---

## Ideation Guide

### What Ideation IS

- Exploring problems, opportunities, and ideas
- Capturing domain knowledge from stakeholders
- Describing user workflows, screens, and interactions
- Articulating business context and strategic alignment
- Identifying constraints, risks, and open questions

### What Ideation is NOT

- Making technical decisions (architecture, data models, APIs)
- Selecting technology stacks or frameworks
- Designing database schemas or system integrations
- Committing to implementation approaches

### The Precision Boundary

Ideation can be **highly precise** about the problem space and user experience. It must **stay silent** on technical implementation.

| Topic | Precision Level | Rationale |
|-------|----------------|-----------|
| Problems and pain points | High | Stakeholders are the domain experts |
| User personas and journeys | High | Domain knowledge, no code needed |
| Screens and interactions | High | Wireframe-level descriptions welcome |
| Business rules and logic | High | "Invoices must be approved within 30 days" |
| Success metrics | High | Measurable targets the business cares about |
| Feature ideas and priority | Medium | Directional (must-have vs nice-to-have) |
| Known constraints | Capture as context | "We already use Salesforce" is a constraint, not a decision |
| Data models and entities | Excluded | Discovery builds these with codebase context |
| API design | Excluded | Discovery + Refinement territory |
| Architecture and tech stack | Excluded | Requires codebase and infrastructure context |
| Database schema | Excluded | Refinement and Delivery territory |

**If the conversation drifts toward implementation:** Redirect with: "That's a great question for Discovery, where we'll have full codebase context. For now, let's capture what the user needs to accomplish."

### Guiding Questions

Use these themes to structure brainstorming. Not all questions apply to every project — use what's relevant.

#### Theme 1: Problem Space
- What problem are we solving? Who has this problem?
- How is this problem being solved today? What's broken about that?
- What happens if we don't solve this? What's the cost of inaction?
- How urgent is this? Is there a deadline or trigger event?

#### Theme 2: Opportunity Space
- What's the opportunity if we solve this well?
- Who benefits most? (Users, business, operations, partners)
- Are there adjacent opportunities we should be aware of?
- What does success look like in 6 months? 2 years?

#### Theme 3: User Space
- Who are the users? What are their roles and skill levels?
- Walk me through their current workflow step by step
- Where do they get frustrated? Where do they lose time?
- What would their ideal experience look like?
- Are there different user types with different needs?

#### Theme 4: Business Context
- Why is the business investing in this now?
- How does this align with company strategy or vision?
- What are the business constraints (budget, timeline, resources)?
- Are there compliance, regulatory, or legal requirements?
- What business metrics should this move?

#### Theme 5: Ideas and Features
- What are the key capabilities users need?
- Which of these are must-haves vs nice-to-haves?
- Are there existing products or competitors we can learn from?
- What's the smallest useful version of this?
- What screens or workflows do you envision?

#### Theme 6: Risks and Unknowns
- What could go wrong?
- What don't we know yet that we need to find out?
- Are there dependencies on other teams, systems, or decisions?
- What assumptions are we making that could be wrong?

### Versioning

Ideation often happens in multiple rounds as thinking evolves. Each round should:

1. **Increment the version** in the document frontmatter (v1, v2, v3...)
2. **Add a changelog entry** noting what changed and why
3. **Not delete previous thinking** — mark superseded ideas as such rather than removing them

When Discovery receives multiple versions, it examines the **delta** — what changed, what was refined, what was dropped — to understand the evolution of thinking.

### Output Format

Ideation produces an **Ideation Document** using the template at `.claude/templates/ideation-document.md`. The template has:

- YAML frontmatter (version, date, participants, status)
- Structured sections that map to Discovery's context questions
- A changelog for tracking version evolution

The document should be placed at `docs/context/ideation-document.md` in the project's specs worktree (or handed off as a standalone file if brainstorming happened outside AgentFlow).

---

## Using This Skill Outside AgentFlow

### In Claude Web or Claude Projects

Copy the "Ideation Guide" section above into your project instructions. Then start a conversation:

> "I want to brainstorm a new product idea. Guide me through the ideation process and produce a structured ideation document at the end."

The AI will use the guiding questions and precision boundaries to run a structured brainstorming session. At the end, ask it to format the output using the Ideation Document template.

### In ChatGPT or Other AI Tools

Copy the "Ideation Guide" section into the system prompt or custom instructions. The guiding questions and boundaries work with any capable AI.

### In Workshops or Meetings

Use the 6 themes as a facilitation framework:
1. **Problem Space** (20 min) — What's broken?
2. **Opportunity Space** (15 min) — What's possible?
3. **User Space** (20 min) — Who benefits and how?
4. **Business Context** (15 min) — Why now? Why us?
5. **Ideas and Features** (20 min) — What could we build?
6. **Risks and Unknowns** (10 min) — What could go wrong?

After the workshop, consolidate notes into the Ideation Document template.

### Importing Into AgentFlow

Once you have an ideation document (from any source):

1. Place it at `docs/context/ideation-document.md` in the project's specs worktree
2. If you have business context documents (vision statements, strategy docs, market research), place them in `docs/context/` as well
3. When Discovery starts, it will automatically detect and consume these documents
4. Discovery pre-populates its 4 context questions from what it finds, then fills gaps

---

## Integration with Discovery

### How Discovery Consumes Ideation Documents

When the Discovery process skill detects documents in `docs/context/`:

1. **Ideation documents** → Extract problems, ideas, personas, business rules, constraints
2. **Business context documents** → Extract strategic alignment, success criteria, business drivers
3. **Multiple versions** → Summarize the delta: what changed, what was refined, what was dropped
4. **Pre-populate Q1-Q4** → Map ideation content to Discovery's 4 mandatory questions
5. **Identify gaps** → Tell the user: "Based on your ideation document, here's what I already know and what I still need to ask about"

### Mapping to Discovery Questions

| Ideation Section | Maps to Discovery Question |
|-----------------|---------------------------|
| Problem Space | Q1: Business Driver |
| User Space | Q2: User Context |
| Known Constraints | Q3: Technical Constraints |
| Success Metrics | Q4: Success Criteria |
| Business Context | Q1 + Q4 enrichment |
| Ideas and Features | Informs entity model and feature decomposition |
| Risks and Unknowns | Informs ADRs and research needs |

### What Discovery Adds

Even with a rich ideation document, Discovery still:
- Validates and deepens the problem understanding
- Performs technical analysis (codebase, infrastructure, integrations)
- Builds the entity model and identifies the central entity
- Makes architecture decisions (ADRs) with full technical context
- Selects the tech stack (modules) based on constraints
- Creates Linear features and milestones
- Produces the 7 mandatory Discovery deliverables

Ideation accelerates Discovery by providing rich domain context. It doesn't replace Discovery's technical analysis.

---

## AI Guardrails

When running ideation as an AI session, enforce these boundaries:

```
YOU ARE facilitating an ideation session. Your role:

DO:
- Ask probing questions about problems, users, and business context
- Encourage divergent thinking — explore multiple directions
- Capture ideas without judging feasibility
- Describe user workflows and screens in detail
- Note business rules, constraints, and success metrics
- Flag assumptions and unknowns
- Use domain language (users, workflows, screens, rules)

DO NOT:
- Propose data models, database schemas, or entity relationships
- Suggest API designs, endpoints, or system architecture
- Recommend specific technologies, frameworks, or libraries
- Make infrastructure or deployment decisions
- Use technical language (tables, endpoints, schemas, microservices)
- Commit to implementation approaches

WHEN IMPLEMENTATION TOPICS ARISE:
- Capture them as "Known Constraints" if they're real constraints
  (e.g., "we use Salesforce" → constraint)
- Redirect to Discovery if they're decisions
  (e.g., "should we use GraphQL?" → "Discovery will evaluate that with full codebase context")
```

---

## Common Pitfalls

1. **Over-structuring too early** — Ideation is messy. Don't force premature organization. Capture ideas freely, structure later.

2. **Technical rabbit holes** — Stakeholders may naturally discuss technology. Capture constraints, redirect decisions.

3. **Skipping business context** — Without the "why", Discovery can't prioritize effectively. Always capture strategic alignment.

4. **Single-round thinking** — Ideation often improves with reflection. Encourage multiple rounds. Each version captures evolved thinking.

5. **Losing the messy bits** — Superseded ideas still have value. Mark them as dropped rather than deleting — Discovery may want to understand why.

6. **Too much precision too soon** — Wireframe-level screen descriptions are fine. Pixel-perfect mockups are premature. Keep it at the "what the user sees and does" level.
