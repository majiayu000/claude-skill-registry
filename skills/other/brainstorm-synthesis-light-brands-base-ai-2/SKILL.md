---
name: brainstorm-synthesis
# prettier-ignore
description: "Use when facing hard architectural decisions, multiple valid approaches exist, need diverse perspectives before committing, or want M-of-N synthesis on complex problems"
version: 1.0.0
category: planning
triggers:
  - "brainstorm synthesis"
  - "f-thread"
  - "multiple perspectives"
  - "architectural decision"
  - "synthesize approaches"
  - "best of N"
  - "M of N"
  - "hard decision"
  - "compare approaches"
---

<objective>
Launch N agents with the same problem from different perspectives. Each returns an
approach with trade-offs. Synthesize the best unified solution from their collective
insights.

This is the F-thread (fusion) pattern: multiple independent analyses converge into one
superior answer. Use it when the decision is hard enough that diverse viewpoints add
value. </objective>

<when-to-use>
Architectural decisions with multiple valid approaches. Complex problems where no single
perspective captures the full picture. High-stakes choices where missing a consideration
is costly. Design decisions in /autotask deep mode.

Skip for straightforward implementations, well-established patterns, or decisions where
one approach is obviously correct. </when-to-use>

<agent-perspectives>
Select 3-5 perspectives that illuminate different facets of the problem:

**Standard perspectives:**

- Pragmatist: Simplest solution that works, minimize complexity
- Architect: Long-term maintainability, extensibility, patterns
- Performance: Efficiency, scalability, resource usage
- Security: Attack surface, data protection, access control
- User-focused: UX impact, developer experience, API ergonomics

**Domain-specific perspectives** (add based on problem):

- Data engineer: For data pipeline decisions
- DevOps: For deployment and infrastructure choices
- Testing: For testability and verification concerns
- Integration: For API and system boundary decisions

Choose perspectives that will genuinely disagree. Similar viewpoints waste the pattern's
value. The goal is productive tension that surfaces trade-offs. </agent-perspectives>

<execution>
Frame a clear problem statement that includes the decision to be made, relevant
constraints, and success criteria.

Launch agents in parallel using the Task tool. Each agent receives:

- The problem statement
- Their assigned perspective
- Instructions to return: recommended approach, key trade-offs, complexity estimate,
  risks

Wait for all agents to complete. Agents work independently without seeing each other's
responses.

Synthesize by identifying where agents agree (high-confidence elements), where they
disagree (trade-off zones), and which perspective's concerns are most relevant given
actual constraints.

Produce a unified recommendation that incorporates the strongest elements from multiple
approaches while maintaining coherence. </execution>

<synthesis-patterns>
**Consensus elements**: When 3+ agents recommend the same approach for a component, that
approach has high confidence. Include it in the final recommendation.

**Trade-off resolution**: When agents disagree, evaluate based on actual project
constraints. The pragmatist might win for a prototype; the architect for a core system.

**Risk integration**: Incorporate security and performance concerns as constraints on
the chosen approach rather than alternative approaches.

**Complexity calibration**: If most agents flag high complexity, the problem may need
decomposition before a single solution emerges. </synthesis-patterns>

<output-format>
Present the synthesized recommendation:

**Recommended Approach**: Clear description of the unified solution

**Why This Approach**: Key factors that made this the best choice

**Integrated Trade-offs**:

- [Trade-off 1]: How the solution handles it
- [Trade-off 2]: How the solution handles it

**Perspectives Incorporated**:

- From Pragmatist: [element included]
- From Architect: [element included]
- From Security: [constraint applied]

**Complexity**: [Low | Medium | High] with brief justification

**Dissenting Views**: Any perspective whose core concern wasn't fully addressed, and why
the trade-off was acceptable </output-format>

<integration-with-autotask>
When called from /autotask in deep mode, brainstorm-synthesis runs during the planning
phase for significant architectural decisions.

Return a concise recommendation that autotask can incorporate into the plan. The full
synthesis rationale goes into the design decisions section of the eventual PR.

Signal when the decision is too close to call - some choices genuinely need human input.
Don't force a recommendation when perspectives are evenly split on important factors.
</integration-with-autotask>

<key-principles>
Diverse perspectives create value. Homogeneous viewpoints waste the pattern.

Synthesis beats voting. Don't just pick the most popular approach - integrate the
strongest elements from multiple perspectives.

Productive disagreement is the point. When agents agree completely, the problem probably
didn't need this pattern.

Know when to escalate. Some decisions genuinely need human judgment. Synthesize what you
can, flag what you can't. </key-principles>
