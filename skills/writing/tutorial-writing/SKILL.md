---
name: tutorial-writing
description: Generate comprehensive implementation tutorial documents with deep background, context, rationale, and step-by-step milestones. Use when the user wants to learn by building—creating detailed guides instead of making direct code changes. Triggers on requests like "create a tutorial for", "implementation guide", "teach me how to implement", or explicit /tutorial invocation.
---

# Implementation Tutorial Generator

Generate exhaustive, educational implementation guides that go far beyond typical planning output. The goal is to enable a "tutorial doc + build-it-yourself" workflow where the developer stays connected to the work and learns by implementing.

## Philosophy

This skill exists because reviewing large AI-generated PRs often feels like "ugh"—you're disconnected from the work, rubber-stamping changes you don't fully understand. The alternative:

1. **AI researches deeply** and produces a comprehensive tutorial document
2. **Human implements** following the guide, staying connected to decisions
3. **Result**: Faster than pure manual work, but you understand what you built

The output is a markdown document, NOT code changes. You are teaching, not doing.

## Workflow

### Step 1: Gather Requirements

Before doing any research, ask the user:
- What feature or change do you want to implement?
- Where should I save the tutorial document? (Suggest a path like `private/tutorials/` or the project's docs folder)

### Step 2: Deep Codebase Research

Spend significant time exploring the codebase. This is NOT optional—the tutorial must be grounded in the actual code, not abstract principles. Research:

- **Architecture**: How is the project structured? What are the key directories and their purposes?
- **Patterns**: What conventions does this codebase follow? How are similar features implemented?
- **Related Code**: Find 2-3 existing implementations most similar to what we're building. Study them in depth.
- **Dependencies**: What libraries/frameworks are used? What APIs are available?
- **Testing**: How does this project test features? What testing utilities exist?
- **Types**: What TypeScript types or schemas are relevant?

Reference specific files and line numbers. The tutorial should feel like it was written by someone who knows this codebase intimately.

### Step 3: Generate the Tutorial Document

Write a comprehensive markdown document following this structure:

---

## Tutorial Document Structure

```markdown
# [Feature Name] Implementation Guide

> A step-by-step tutorial for implementing [feature] in [project name].
> Estimated implementation time: [X milestones, ~Y hours of focused work]

## Overview

[2-3 paragraphs explaining what we're building and why. Include the user-facing value and technical motivation. This should excite the reader about what they'll learn.]

## Background & Context

[Deep dive into the surrounding systems. Teach the reader about:
- How the relevant parts of the codebase work today
- Historical context if relevant (why things are the way they are)
- Key abstractions they need to understand
- Reference specific files: "The current implementation lives in `src/features/auth/` (see especially `auth-provider.tsx:45-120`)"]

## Technical Landscape

[Map out the territory:
- Relevant existing components/modules
- Data flow and state management patterns used here
- API contracts and type definitions
- External dependencies involved
- Constraints and gotchas to be aware of]

## Design Rationale

[Explain the approach we're taking and WHY:
- What alternatives were considered?
- Why is this approach better for THIS codebase?
- What tradeoffs are we making?
- How does this align with project conventions?]

## Implementation Milestones

[The core of the tutorial. Each milestone should be:
- Small enough to complete in one sitting
- Verifiable—you can SEE it works before moving on
- Buildable—each milestone builds on the previous]

### Milestone 1: [Foundation/Setup]

**Objective**: [What we're accomplishing]

**Why this first**: [Rationale for ordering]

**Files to create/modify**:
- `path/to/file.ts` - [what changes and why]
- `path/to/other.ts` - [what changes and why]

**Implementation approach**:
[Detailed explanation of WHAT to build, not copy-paste code. Describe:
- The structure and key functions needed
- How it connects to existing code
- Patterns to follow from similar implementations
- Edge cases to handle]

**Verification**:
- [ ] [Specific test to run or behavior to observe]
- [ ] [Another verification step]

**Checkpoint**: After this milestone, you should be able to [specific observable behavior].

---

### Milestone 2: [Core Functionality]

[Same structure as above...]

---

### Milestone 3: [Integration]

[Same structure...]

---

### Milestone N: [Polish & Edge Cases]

[Final milestone often handles:
- Error states and edge cases
- Loading states and UX polish
- Documentation and types cleanup]

## Testing Strategy

[How to thoroughly test this feature:
- Unit test approach and key test cases
- Integration test considerations
- Manual testing checklist
- Edge cases that MUST be tested]

## Risks & Mitigations

[What could go wrong?
- Technical risks (performance, compatibility, etc.)
- UX risks (confusing behavior, accessibility issues)
- Maintenance risks (technical debt, future conflicts)
- How to mitigate or monitor each]

## Going Further

[Optional extensions beyond the core implementation:
- Nice-to-have improvements
- Future enhancements to consider
- Related features this enables]

## References

[Specific pointers for the implementer:
- Key files: `path/to/file.ts:123` - description
- Related PRs or issues if known
- External documentation links
- Similar implementations in the codebase to reference]
```

---

## Quality Standards

The tutorial must:

1. **Be exhaustive**: Go deeper than typical plan mode output. If it takes 30+ minutes to generate, that's fine—the user is trading AI time for their own learning.

2. **Teach, don't just instruct**: Explain WHY at every step. The reader should understand the system better after reading, not just know what to type.

3. **Reference real code**: Every claim about "how the codebase works" should point to specific files and line numbers. No hand-waving.

4. **Enable independence**: After reading the tutorial, the developer should be able to implement WITHOUT coming back to ask more questions.

5. **Verify at each step**: Every milestone must have concrete verification. No "now the feature should work"—specify HOW to verify.

6. **Go beyond the obvious**: The tutorial can extend beyond where a typical PR would stop. Suggest polish, tests, documentation—even if the user might skip some of it.

## Output Behavior

1. Ask for output path before starting (suggest reasonable default)
2. Write the complete tutorial to the specified path
3. Summarize what was created and suggest how to proceed

## Example Invocations

```
/tutorial Add dark mode support to the component library

/tutorial Implement real-time notifications using WebSockets

/tutorial Refactor the data fetching layer to use React Query

/tutorial Add comprehensive error boundaries throughout the app
```

## Remember

You are not generating code. You are generating a TEACHING DOCUMENT. The human will write the code themselves, using your guide. This keeps them connected to the work, helps them learn the codebase, and produces better outcomes than reviewing AI-generated PRs.

Take your time. Be thorough. The user explicitly wants depth over speed.
