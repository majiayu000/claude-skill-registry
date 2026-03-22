---
name: book-writing
version: 1.0.0
description: "This skill should be used when the user asks to 'document a project', 'write project documentation', 'create a technical book', 'generate docs', 'document this codebase', or wants documentation that reads like a book. Provides pedagogical principles, narrative structure techniques, tone adaptation for different audiences, and quality criteria for engaging technical writing."
---

# Book-Style Documentation Writing

Create project documentation that reads like a well-written book — engaging, progressive, and pedagogical — not a dry reference manual.

## Core Philosophy

Great documentation tells a story. Every project exists because someone had a problem worth solving. Start there. Build understanding layer by layer, the way a good teacher would — context before details, "why" before "how", concrete before abstract.

## Pedagogical Principles

### 1. Progressive Complexity

Structure content so each section builds on the previous one. Never reference concepts that haven't been introduced yet. A reader who starts at chapter 1 should never feel lost.

**Pattern:** Context → Concept → Example → Implication → Next concept

### 2. Narrative Hooks

Every chapter and section needs a reason to keep reading. Open with a question, a problem, or a scenario the reader recognizes. "You've probably dealt with..." or "Imagine you need to..." draws readers in.

### 3. The "Why" Before the "How"

Never explain implementation without first explaining motivation. Before showing how the authentication system works, explain why it exists, what threats it addresses, what would happen without it.

### 4. Concrete Before Abstract

Show a real example first, then extract the pattern. Don't start with "the system uses a publish-subscribe architecture" — start with "when a user places an order, three things happen simultaneously..."

### 5. Guided Tours, Not Maps

Instead of listing all 47 API endpoints, walk the reader through the 3 most important user journeys. They'll understand the architecture through experience, not enumeration.

## Tone Adaptation

### Developer Audience

- Use precise technical terminology without over-explaining basics
- Include code snippets, file paths, command examples
- Reference patterns they'll recognize (MVC, pub-sub, middleware chains)
- Be direct — developers appreciate efficiency
- Include "gotchas" and non-obvious behavior

### Stakeholder Audience

- Lead with business impact, not implementation
- Use analogies to explain technical concepts
- Focus on capabilities, constraints, and trade-offs
- Include diagrams and visual explanations
- Frame technical decisions as business decisions

### Adaptive (Both)

- Write in layers: narrative overview first, technical depth in expandable sections or appendices
- Use sidebars for technical deep-dives that developers want but stakeholders can skip
- Always provide a "what this means in practice" translation

## Documentation Workflow

### Phase 1: Scan

Read `phases/01-scan.md` — automated codebase analysis produces a project map.

### Phase 2: Interview

Read `phases/02-interview.md` — gated questionnaire collects all decisions before writing begins.

### Phase 3: Write

Read `phases/03-write.md` — parallel chapter writing using subagents.

### Phase 4: Review

Read `phases/04-review.md` — pedagogical quality review with auto-rewrite.

### Phase 5: Produce

Read `phases/05-produce.md` — media generation (audio, slides) via NotebookLM.

**IMPORTANT**: Read ONE phase file at a time. Complete ALL steps before reading the next.

## Structural Patterns (Not Templates)

Every project is different. The scanner agent proposes a custom outline. These patterns guide structure decisions:

### The Origin Story Pattern
For projects with interesting history or motivation. Start with the problem, walk through the journey of solving it.

### The Guided Tour Pattern
For complex systems. Take the reader on a walk through the system, following a request from entry to completion.

### The Building Blocks Pattern
For modular projects. Introduce each component independently, then show how they connect.

### The Problem-Solution Pattern
For tools and utilities. Each chapter presents a problem the tool solves, then shows how.

### The Onboarding Pattern
For projects where getting started is the priority. Hands-on first, architecture later.

### The Decision Record Pattern
For projects with non-obvious architecture choices. Each chapter presents a requirement, the options considered, trade-offs, and the final decision with its consequences. See `references/chapter-patterns.md` for full details.

## Quality Criteria

The pedagogy-reviewer agent uses these criteria:

1. **Engagement** — Would someone choose to keep reading? Are there narrative hooks?
2. **Progressive complexity** — Does each section build on the last? No forward references?
3. **Context before detail** — Is the "why" always before the "how"?
4. **Concrete examples** — Are abstract concepts grounded in real scenarios?
5. **Appropriate tone** — Does it match the target audience?
6. **Completeness** — Are all major aspects of the project covered?
7. **Navigability** — Can readers find what they need? Clear headings, logical flow?

## Additional Resources

### Reference Files

- **`references/writing-techniques.md`** — Detailed techniques for engaging technical prose
- **`references/chapter-patterns.md`** — Extended structural patterns with examples

### Phase Files

- **`phases/01-scan.md`** — Codebase scanning procedure
- **`phases/02-interview.md`** — User questionnaire (gated)
- **`phases/03-write.md`** — Parallel chapter writing with subagents
- **`phases/04-review.md`** — Pedagogical review and auto-rewrite
- **`phases/05-produce.md`** — Media production via NotebookLM
