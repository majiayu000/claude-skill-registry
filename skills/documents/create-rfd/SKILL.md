---
name: create-rfd
description: |
  Request for Discussion (RFD) creation workflow. Use when exploring technical options,
  building consensus on architecture decisions, or documenting design rationale before
  implementation begins. Creates structured documents that capture problem context,
  evaluate alternatives, and preserve decision-making rationale.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: workflow
---

# Skill: Create RFD (Request for Discussion)

## Overview

RFDs (Requests for Discussion) capture ideas, explore options, and document decisions before implementation. Inspired by IETF's RFC tradition, they enable sharing incomplete ideas early for better outcomes.

**Core Principles:**
- Share early, refine together
- Document options, not just decisions
- Capture context for future readers
- Build consensus before implementation

**Philosophy**: "Ideas should be timely rather than polished." — Oxide Computer Company, RFD 1

## When to Use This Skill

| Scenario | Use RFD | Use PRD |
|----------|---------|---------|
| "Should we use Redis or PostgreSQL for sessions?" | ✅ | |
| "Build session management with Redis" | | ✅ |
| "Exploring authentication approaches" | ✅ | |
| "Implement OAuth with Google and GitHub" | | ✅ |
| "Should we adopt a new framework?" | ✅ | |
| Multiple valid options, need discussion | ✅ | |
| Requirements clear, need implementation plan | | ✅ |

**Key Distinction:**
- **RFD** = "Why" and "What options" (explore, discuss, decide)
- **PRD** = "What" and "How" (plan, implement, deliver)

**Typical Flow:**
```
Idea → RFD (explore options) → Decision → PRD (define implementation) → Tasks → Code
```

## RFD States (Lifecycle)

```
Prediscussion → Ideation → Discussion → Published → Committed
                    ↓           ↓
                    └─────→ Abandoned
```

| State | Description | Location |
|-------|-------------|----------|
| **Prediscussion** | Very early, author still forming idea | `.claude/rfd/` |
| **Ideation** | Ready for informal feedback, not finalized | `.claude/rfd/` |
| **Discussion** | Open for team discussion, seeking consensus | `docs/rfd/` |
| **Published** | Decision made, documented for reference | `docs/rfd/` |
| **Committed** | Implemented, part of the codebase | `docs/rfd/` |
| **Abandoned** | Proposal rejected or superseded | `docs/rfd/` |

## Process Overview

### 1. Receive Topic

User describes what they want to explore or decide:
- "I'm considering whether to use GraphQL or REST for the API"
- "We need to decide on a caching strategy"
- "Exploring options for real-time updates"
- "Should we migrate from Express to Fastify?"

### 2. Check Context

Before asking questions:
1. **Read `CLAUDE.md`** for tech stack and constraints
2. **Check `rfd-index.yaml`** for related existing RFDs
3. **Scan codebase** for existing implementations
4. **Review `CLAUDE.md`** for established conventions

### 3. Ask Discovery Questions

**IMPORTANT**: Ask clarifying questions to understand the problem space. Provide numbered options for easy responses.

**Core Questions** (adapt based on topic):

**Problem/Goal:**
- What problem are you trying to solve?
- What outcome do you want to achieve?

**Constraints:**
- What constraints exist? (technical, team, timeline, budget)
- Any hard requirements that eliminate options?

**Stakeholders:**
- Who needs to weigh in on this decision?
- Is this a solo decision or team consensus needed?

**Timeline:**
- When does this decision need to be made?
- Is this urgent or can it wait for more research?

**Options Awareness:**
- Have you already considered some options?
- Are there approaches you've ruled out?

**Success Criteria:**
- How will you know if the decision was good?
- What would success look like?

**Reversibility:**
- How hard would it be to change this decision later?
- Is this a one-way door or two-way door?

### 4. Research Options

Based on user answers:
1. Identify 2-4 viable options
2. Research each option (existing patterns, industry practices)
3. Document pros and cons for each
4. Note any options considered and rejected (with reasons)

### 5. Generate RFD

Create RFD using the template structure (see below).

**Target Audience**: Team members and future developers (clear, explicit, no jargon)

### 6. Determine Initial State

| If... | Initial State | Location |
|-------|---------------|----------|
| Very rough idea, author still thinking | Prediscussion | `.claude/rfd/` |
| Ready for informal feedback | Ideation | `.claude/rfd/` |
| Ready for team discussion | Discussion | `docs/rfd/` |

**Default**: Start in **Ideation** state.

### 7. Save and Update Index

1. **Get next RFD number** from `rfd-index.yaml` (`next_number` field)
2. **Create RFD file** in appropriate location based on state
3. **Update `rfd-index.yaml`**:
   - Add new entry to `rfds` array
   - Increment `next_number`
4. **Inform user** of file location and next steps

## RFD Template Structure

```markdown
---
rfd: NNNN
title: Short Descriptive Title
authors:
  - name: Author Name
state: Ideation
labels: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
discussion: null
related_prd: null
---

# RFD NNNN: Short Descriptive Title

## Summary

One paragraph (2-4 sentences) describing the proposal or question.

## Problem Statement

What problem does this address? Why is it important? What happens if we do nothing?

## Background

Context that readers need to understand this proposal. Include:
- Current state of the system
- Why this topic is being raised now
- Any previous attempts or related decisions

## Options Considered

### Option A: [Name]

Description of this approach.

**Pros:**
- Benefit 1
- Benefit 2

**Cons:**
- Drawback 1
- Drawback 2

**Effort**: Low / Medium / High

### Option B: [Name]

Description of this approach.

**Pros:**
- Benefit 1

**Cons:**
- Drawback 1

**Effort**: Low / Medium / High

### Rejected Options

Options that were considered but eliminated early:

- **[Option X]**: Rejected because [reason]
- **[Option Y]**: Not viable due to [constraint]

## Proposal

**Recommended option**: [Option A/B/C]

**Rationale**: [Why this option is recommended]

If no recommendation yet (seeking input):
> This RFD is seeking feedback. No recommendation has been made yet.

## Implementation Considerations

High-level implementation notes if the proposal is accepted:
- Key technical considerations
- Migration needs (if any)
- Dependencies or prerequisites

## Security Considerations

Any security implications of this decision:
- New attack surfaces
- Data handling changes
- Authentication/authorization impacts

## Compatibility

- **Breaking changes**: [Yes/No, and what breaks]
- **Migration path**: [How to transition]
- **Backwards compatibility**: [What's preserved]

## Open Questions

Questions that need answers before deciding:

1. [Question 1]?
2. [Question 2]?
3. [Question 3]?

## References

- Related RFDs: [links]
- External resources: [links]
- Related PRDs: [links if applicable]
```

## Output Format

**File Location** (based on state):
- Prediscussion/Ideation: `.claude/rfd/NNNN-rfd-topic-slug.md`
- Discussion/Published/Committed: `docs/rfd/NNNN.md`

**Naming Convention:**
- Private: `NNNN-rfd-topic-slug.md` (e.g., `0042-rfd-api-caching.md`)
- Public: `NNNN.md` (e.g., `0042.md`)

**Index Update**: Add entry to `rfd-index.yaml`

## State Transitions

### Promoting an RFD

**Ideation → Discussion:**
1. Update state in frontmatter to "Discussion"
2. Move file from `.claude/rfd/` to `docs/rfd/`
3. Rename to `NNNN.md` format
4. Create GitHub discussion (optional)
5. Update `rfd-index.yaml` with new path and discussion link

**Discussion → Published:**
1. Update state in frontmatter to "Published"
2. Ensure "Proposal" section has final decision
3. Remove or answer all "Open Questions"
4. Update `rfd-index.yaml`
5. Can now create PRD if implementation needed

**Published → Committed:**
1. Update state in frontmatter to "Committed"
2. Add links to implementation PRs/commits in References
3. Update `rfd-index.yaml`

### Abandoning an RFD

1. Update state in frontmatter to "Abandoned"
2. Add note at top explaining why:
   > **Note**: This RFD was abandoned on [date] because [reason].
3. Keep file for historical reference (do not delete)
4. Update `rfd-index.yaml`

### Commands for State Transitions

User can request:
- "Promote RFD 0042 to Discussion"
- "Mark RFD 0042 as Published - we're going with Option A"
- "Abandon RFD 0042 - no longer relevant"
- "Mark RFD 0042 as Committed - implementation complete"

## Linking RFD to PRD

When an RFD decision leads to implementation:

1. **RFD side**: Add to frontmatter: `related_prd: 0005-prd-feature-name.md`
2. **PRD side**: Add to frontmatter: `source_rfd: 0042`
3. **Cross-reference**: Add RFD link to PRD's "Technical Considerations" section

**Workflow:**
```
1. Complete RFD, state = Published
2. Use .claude/skills/create-prd/SKILL.md
3. PRD references RFD decision
4. When PRD implementation complete, mark RFD as Committed
```

## Embedded Mode (Suggest Only)

### When AI Should Suggest Creating an RFD

During regular development, suggest an RFD when:

1. **User asks comparison question**: "Should we use X or Y?"
2. **AI discusses multiple approaches**: Presenting 2+ options with pros/cons
3. **Architectural decision point**: Choice that affects system design
4. **Significant deviation**: Proposing change from existing patterns
5. **Future reference valuable**: Decision others would want to understand

### Suggestion Format

```
I notice we're discussing multiple approaches for [topic]. Would you like me
to create an RFD to formally document these options? This will help:

- Capture the pros/cons of each approach
- Document our decision rationale
- Provide context for future developers

Shall I create RFD [next_number]: [suggested title]?
```

### If User Confirms

1. Follow the standard RFD creation process
2. Start in **Ideation** state (in `.claude/rfd/`)
3. Include context from current discussion
4. Present completed RFD for review

### If User Declines

Continue with the conversation normally. The discussion itself provides some documentation via conversation history.

## Tips for Good RFDs

### Content Quality

- **Be honest about tradeoffs**: Every option has cons
- **Include rejected options**: Future readers need to know what was considered
- **Quantify when possible**: "50ms vs 200ms" beats "faster vs slower"
- **Link to evidence**: External resources, benchmarks, case studies

### Process Quality

- **Share early**: Don't polish in isolation
- **Keep scope focused**: One decision per RFD
- **Update as you learn**: RFDs can evolve during discussion
- **Close the loop**: Move to Published/Committed/Abandoned

### Common Mistakes

- ❌ Only documenting the chosen option (document all considered)
- ❌ Waiting until decision is made to write (write to facilitate decision)
- ❌ Scope creep (multiple decisions in one RFD)
- ❌ Abandoning without explanation (always note why)
- ❌ Never updating state (stale "Discussion" RFDs)

## When NOT to Use RFD

Skip RFD for:

- **Obvious decisions**: Only one viable option
- **Small scope**: Won't affect others, easily reversible
- **Already decided**: Discussion already happened elsewhere
- **Implementation details**: HOW not WHAT (use PRD instead)
- **Urgent fixes**: Document post-hoc if needed

## Related Workflows

| Workflow | Relationship |
|----------|--------------|
| **create-prd** | Creates implementation plan after RFD decision |
| **document-work** | Can identify mini-RFDs worth promoting |
| **generate-tasks** | Breaks down PRD (which may reference RFD) |

## Instructions for AI

### DO:

1. ✅ **Ask discovery questions** (understand problem space)
2. ✅ **Research multiple options** (even if user suggests one)
3. ✅ **Document rejected options** (with reasons)
4. ✅ **Reference existing context** (project.md, patterns.md, other RFDs)
5. ✅ **Suggest RFDs during discussions** (embedded mode)

### DO NOT:

1. ❌ **Start implementation** (RFD is for discussion, not action)
2. ❌ **Force a recommendation** (seeking input is valid)
3. ❌ **Skip the index update** (rfd-index.yaml must be current)

### After RFD Created:

1. Save to appropriate location based on state
2. Update `rfd-index.yaml`
3. Inform user of file location
4. Suggest next steps:
   - Review and refine
   - Promote to Discussion when ready
   - Or: "Create PRD from RFD NNNN" when decision is made

---

**Remember**: RFDs capture the "why" behind decisions. A year from now, someone will read this and understand not just what was decided, but why other options were rejected. That context is invaluable.

## Additional Resources

For detailed examples, full state machine documentation, and verbose instructions, see:
- **references/process.md** — Complete process guide with examples
