---
name: scope-project
description: Adversarial project planning workflow. Explores the problem space, drafts tickets in batches, then pits a planner against an implementer to find gaps. Creates well-specified, batch-tagged tickets upstream only after the implementer signs off.
model: opus
---

# Scope Project - Adversarial Project Planning

Thoroughly plans an entire project through exploration, iterative ticket drafting, and adversarial review. A planner drafts tickets; an implementer challenges them. Only when the implementer is satisfied that every ticket could be implemented without unanswered questions do the tickets go upstream.

**This skill does NOT write code.** It explores, questions, plans, and creates tickets.

## Philosophy

**Planning is cheaper than rework.** A gap discovered during planning costs minutes to fix. The same gap discovered during implementation costs hours — and may cascade into other tickets. Invest heavily in planning quality.

**Adversarial review catches what self-review misses.** The planner has blind spots — assumptions baked into the plan that seem obvious but aren't. An implementer reviewing with "could I actually build this?" eyes will find gaps the planner can't see.

**Convergence is the goal, not perfection.** The planner and implementer iterate until the implementer is satisfied, not until every conceivable edge case is documented. Use judgment about when tickets are "good enough" — detailed enough to implement without guessing, but not so verbose they become novels.

**Batch structure is a planning decision.** Tickets go upstream already tagged with their batch assignment. The batch structure should reflect real implementation dependencies, not arbitrary grouping.

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────┐
│                  SCOPE PROJECT WORKFLOW                       │
├──────────────────────────────────────────────────────────────┤
│  1. Project discovery (dialogue with user)                   │
│  2. Codebase exploration                                     │
│  3. Draft project plan (present to user for approval)        │
│  4. Create .tickets/ staging directory                       │
│  5. Draft tickets (subagent per ticket)                      │
│  6. Adversarial review loop:                                 │
│     ├─ Implementer reviews all tickets                       │
│     ├─ Planner addresses feedback                            │
│     ├─ Repeat until implementer signs off                    │
│     └─ Escalate to human if stalemated                       │
│  7. Present final tickets to user                            │
│  8. Cut tickets upstream (subagent per ticket)               │
│  9. Clean up .tickets/ directory                             │
└──────────────────────────────────────────────────────────────┘
```

## Workflow Details

### 1. Project Discovery

**Understand what the user wants to build.** This is a dialogue — ask probing questions to get a precise picture of the project.

**Questions to explore:**
- What is the project's goal? What problem does it solve?
- What's the scope? What's explicitly out of scope?
- Are there existing systems this interacts with?
- What are the constraints? (Timeline, technology, compatibility)
- Are there natural phases or batches? What depends on what?
- What does "done" look like for the whole project?

**Push back on vagueness.** If the user says "add authentication," ask: what kind? OAuth? JWT? Session-based? What providers? What permissions model? The goal is precision.

**Output:** Clear, shared understanding of the project and its boundaries.

### 2. Codebase Exploration

**Explore the codebase to understand context.** Use exploration agents and tools to map out:

- Current architecture and conventions
- Code areas that will be affected
- Existing patterns to follow or extend
- Integration points and constraints
- Third-party dependencies involved

**For third-party dependencies:**
- Use WebFetch to read API documentation
- Clone relevant repositories to `/tmp` for examination if needed
- Understand integration points and constraints

**Output:** Comprehensive understanding of the codebase as it relates to the project.

### 3. Draft Project Plan

Synthesize the discovery and exploration into a structured project plan.

**The plan should include:**

**Project summary:**
- Goal and scope (1-2 paragraphs)
- Key technical decisions and rationale

**Batch structure:**
- How many batches, and what's the ordering rationale
- Dependencies between batches
- What each batch delivers (a coherent increment)

**Ticket inventory:**
- List of tickets per batch (title + one-line summary)
- Dependencies between tickets (within and across batches)
- Estimated scope per ticket (qualitative: small / medium / large)

**Risk areas:**
- Tickets that seem underspecified
- Cross-cutting concerns that span multiple tickets
- Integration risks between batches

**Present the plan to the user for approval.** This is the primary human checkpoint — the user should agree with the project structure, batch grouping, and ticket inventory before detailed ticket drafting begins.

**Wait for user approval before proceeding.** The user may adjust batches, add/remove tickets, reorder, or ask questions. Iterate until approved.

### 4. Create Staging Directory

Create a `.tickets/` directory in the repository root, organized by batch:

```
.tickets/
├── batch-1/
│   ├── 01-<slug>.md
│   ├── 02-<slug>.md
│   └── 03-<slug>.md
└── batch-2/
    ├── 01-<slug>.md
    └── 02-<slug>.md
```

The numbering reflects execution order within each batch. The slug is derived from the ticket title.

**Add `.tickets/` to `.gitignore`** to prevent accidental commits of staging artifacts.

### 5. Draft Tickets

**Spawn one subagent per ticket** to draft ticket content. Each subagent receives:
- The approved project plan (from step 3)
- The codebase exploration findings relevant to that ticket
- The ticket's position in the batch structure (what comes before it, what depends on it)

**Each subagent writes a markdown file** in the `.tickets/` directory following this format:

```markdown
---
title: <ticket title>
batch: <batch name>
order: <execution order within batch>
depends_on: []
labels: [batch-N, <other labels>]
---

## Problem Statement
[What problem does this ticket solve? Why is it needed?]

## Proposed Solution
[High-level approach — what to build, not how to build it line-by-line]

## Acceptance Criteria
- [ ] [Specific, testable criterion]
- [ ] [Another criterion]

## Technical Notes
[Implementation considerations, affected components, relevant code paths]
- Affected files: [list key files]
- Key functions: [list functions to modify/create]
- Patterns to follow: [existing patterns in the codebase]
- Security considerations: [if applicable — new attack surface, input handling, auth/authz changes, trust boundary impacts]

## Implementation Notes
[Guidance for the implementer — current function signatures, module
boundaries, integration points. The kind of context that saves the
implementer from having to rediscover what the planner already found.]

## Dependencies
- Depends on: [list ticket slugs this depends on]
- Blocks: [list ticket slugs that depend on this]

## Out of Scope
[What explicitly will NOT be done in this ticket]
```

**Subagent coordination:**
- Subagents run in parallel where possible (independent tickets)
- Sequential for tickets with dependencies (later ticket needs to reference earlier ticket's content)
- Each subagent writes its file and reports completion

### 6. Adversarial Review Loop

This is the heart of the workflow. A planner and an implementer iterate on the tickets until the implementer is satisfied.

#### 6a. Spawn Implementer

**Spawn a fresh implementer agent** to review all tickets. Select the appropriate agent type:

- If the project is primarily in one language with a dedicated SME (Go, Zig, Docker, Makefile, GraphQL, Ansible): spawn that SME
- If mixed-language or no dedicated SME: spawn a general-purpose agent

**The implementer's mandate:** Review every ticket as if you were assigned to implement it tomorrow. Identify anything that would leave you guessing, blocked, or making assumptions.

**Prompt the implementer with:**
```
You are reviewing a set of project tickets as a prospective implementer.
Your job is adversarial: find every gap, ambiguity, missing dependency,
and unanswered question. Be thorough and specific.

For each ticket, evaluate:
1. Could I implement this without guessing? Are requirements precise?
2. Are acceptance criteria testable and unambiguous?
3. Are dependencies explicit? Do I know what must exist before I start?
4. Are there missing tickets? Work that's assumed but not assigned?
5. Do any tickets overlap or conflict?
6. Is the batch assignment correct? Any forward dependencies within a batch?
7. Are implementation notes accurate? Do code references check out?
8. Is anything out of scope that shouldn't be?

Also evaluate the project holistically:
- Are there gaps between tickets? Work that falls through the cracks?
- Is the batch ordering sound?
- Are cross-cutting concerns addressed?

Produce a structured review with:
- Per-ticket findings (categorized: blocker / question / suggestion)
- Cross-ticket findings
- Missing ticket proposals (if any)
- Verdict: APPROVED or NEEDS REVISION
```

#### 6b. Planner Addresses Feedback

The orchestrator (you, the planner) reviews the implementer's findings and addresses each one:

- **Blockers:** Must be resolved. Revise the affected ticket(s).
- **Questions:** Answer them — either by revising the ticket to include the answer, or by asking the human for clarification.
- **Suggestions:** Use judgment — accept valuable suggestions, decline ones that over-specify.
- **Missing tickets:** Draft new tickets if the gap is real. Decline if the work is genuinely out of scope.
- **Batch reassignments:** Adjust batch structure if the implementer's reasoning is sound.

**Asking the human is normal and productive.** If the implementer surfaces a question that the planner genuinely can't answer (design decision, business requirement, user preference), ask the human. This is the workflow working as intended — surfacing questions during planning rather than during implementation.

**Update the `.tickets/` files** with revisions. If new tickets are added or batch structure changes, update the directory structure accordingly.

#### 6c. Re-Review

**Spawn a fresh implementer agent** (clean context) to review the revised tickets. The fresh instance prevents anchoring on previous findings.

**Repeat steps 6a-6c until:**
- The implementer returns `APPROVED` — all tickets are implementable without guessing
- **Or** the process has stalemated — the same issues keep cycling without resolution

**On stalemate:** Escalate to the human. Present the unresolved issues and ask for direction. The planner and implementer may have a legitimate disagreement that requires human judgment.

**There is no hard iteration cap.** The goal is convergence. Most projects should converge in 2-3 rounds. If it takes more, something fundamental may be underspecified — which is exactly what this workflow is designed to surface.

### 7. Present Final Tickets to User

After the implementer approves, present the complete ticket set to the user:

**Summary view:**
```
## Project Plan: <name>

### Batch 1: <name>
1. <title> — <one-line summary>
2. <title> — <one-line summary>
3. <title> — <one-line summary>

### Batch 2: <name>
1. <title> — <one-line summary>
2. <title> — <one-line summary>

### Review Summary
- Total tickets: N
- Adversarial review rounds: N
- Human clarifications requested: N
- Missing tickets identified during review: N
```

**Offer to show full ticket details** for any ticket the user wants to inspect.

**Wait for user approval.** The user may request final adjustments before tickets go upstream.

### 8. Cut Tickets Upstream

**Detect issue tracker** using the same detection as `/scope` and `/implement-batch`:
- Check `CLAUDE.md` for tracker preference
- Auto-detect from `git remote -v`
- GitHub → `gh`, Gitea → MCP tools, GitLab → `glab`

**Create batch labels/tags first:**
- For each batch, create a label (e.g., `batch-1`, `batch-2`) if it doesn't already exist
- Use a consistent color scheme or prefix for batch labels

**Spawn one subagent per ticket** to create issues upstream. Each subagent:
- Creates the issue with title and body (from the `.tickets/` file)
- Applies labels: batch tag + any additional labels from the ticket frontmatter
- Reports back with the issue URL and number

**Subagent coordination:**
- Create tickets within a batch sequentially (so earlier tickets can be referenced by later ones in "depends on" links)
- Batches can be processed in parallel if the tracker supports it

**After all tickets are created, present the results:**
```
## Tickets Created

### Batch 1: <name> (label: batch-1)
- #12: <title> — <url>
- #13: <title> — <url>
- #14: <title> — <url>

### Batch 2: <name> (label: batch-2)
- #15: <title> — <url>
- #16: <title> — <url>

All N tickets created successfully.
```

### 9. Clean Up

- Remove the `.tickets/` directory
- Remove the `.tickets/` entry from `.gitignore` (if this workflow added it)
- Confirm cleanup is complete

## Ticket Quality Criteria

The implementer evaluates tickets against these criteria:

| Criterion                                | What it means                                                                                          |
|------------------------------------------|--------------------------------------------------------------------------------------------------------|
| **Implementable without guessing**       | Requirements are precise enough that two different developers would build substantially the same thing  |
| **Testable acceptance criteria**         | Each criterion can be verified with a concrete action ("run X, expect Y"), not a subjective judgment ("it should be fast") |
| **Explicit dependencies**               | Every ticket states what must exist before work begins — no implicit "presumably ticket A runs first"  |
| **No batch-internal forward dependencies** | Ticket B in batch 1 must not depend on ticket C in batch 1 if C comes after B in execution order     |
| **No gaps**                              | Every piece of necessary work is assigned to a ticket — nothing falls through the cracks               |
| **No overlaps**                          | No two tickets modify the same code in conflicting ways                                                |
| **Accurate code references**            | File paths, function names, and module references in technical/implementation notes are correct         |
| **Appropriate scope**                    | Each ticket is a coherent unit of work — not so large it's unmanageable, not so small it's trivial     |

## Agent Coordination

**Sequential phases:**
- Steps 1-3 are interactive with the user (sequential)
- Step 5 uses parallel subagents for ticket drafting
- Step 6 is sequential (planner → implementer → planner → ...)
- Step 8 uses parallel subagents for ticket creation

**Context management:**
- The orchestrator maintains the project plan and tracks revision history
- Ticket drafting subagents receive focused context (just their ticket's scope)
- Implementer agents receive all tickets but no implementation history
- Fresh implementer instances per review round (prevents anchoring)

**State:**
- `.tickets/` directory is the source of truth for ticket content
- The orchestrator tracks: review round count, unresolved issues, human clarifications requested

## Abort Conditions

**Escalate to human:**
- Planner-implementer iteration has stalemated (same issues cycling)
- Fundamental ambiguity that only the user can resolve
- Issue tracker unavailable or tickets can't be created

**Abort entire workflow:**
- User interrupts
- Critical system error

**Do NOT abort for:**
- Implementer finding many issues (that's the workflow working)
- Multiple rounds of revision (convergence takes time)
- Human clarification needed (normal and productive)

## Integration with Other Skills

**Relationship to `/scope`:**
- `/scope` explores and creates a single ticket interactively
- `/scope-project` plans an entire project with adversarial review
- `/scope-project` uses a lighter-weight ticket drafting process (subagents with project context) rather than invoking full `/scope` per ticket
- For individual tickets that prove deeply underspecified during adversarial review, the orchestrator may invoke `/scope` as targeted escalation

**Relationship to `/implement-project`:**
- `/scope-project` creates tickets; `/implement-project` implements them
- Tickets go upstream already tagged with batch labels that `/implement-project` consumes
- Typical flow: `/scope-project` → `/implement-project`

**Relationship to `/deliberate`:**
- `/scope-project`'s adversarial review is specialized for planning quality
- `/deliberate` may be used within `/scope-project` if the planner faces a difficult design decision during ticket revision

## Example Session

```
User: /scope-project

What project are you planning?
> I want to add MCP server support to our CLI tool. It should expose
  the tool's core functionality as MCP tools, handle JSON-RPC, and
  support stdio transport.

Let me explore the codebase to understand the current architecture...

[Codebase exploration: CLI structure, command handlers,
 existing transport code, third-party MCP libraries]

A few questions:
- Which commands should be exposed as MCP tools? All of them, or a subset?
- Should the MCP server be a subcommand (`tool mcp-server`) or a separate binary?
- Any authentication requirements for the MCP transport?
> All commands. Subcommand. No auth needed for stdio.

## Project Plan

### Batch 1: Core MCP Infrastructure
1. Add MCP server subcommand — entry point, stdio transport, JSON-RPC handler
2. Define MCP tool schema — map CLI commands to MCP tool definitions
3. Implement tool dispatch — route MCP tool calls to existing command handlers

### Batch 2: Tool Implementations
4. Expose read commands — list, get, search as MCP tools
5. Expose write commands — create, update, delete as MCP tools
6. Add MCP resource support — expose data as MCP resources

### Batch 3: Polish
7. Error handling — map CLI errors to JSON-RPC error codes
8. Integration tests — end-to-end MCP protocol tests
9. Documentation — MCP server usage docs, tool catalog

Cross-batch dependencies: batch 2 depends on batch 1, batch 3 depends on both.

Approve this plan?
> Looks good. Proceed.

Creating .tickets/ directory...
Drafting tickets (9 subagents)...
All tickets drafted.

[Adversarial Review — Round 1]
Spawning implementer (swe-sme-golang)...

Implementer findings:
- BLOCKER: Ticket #1 doesn't specify which MCP SDK to use or how
  JSON-RPC parsing works. I'd be guessing at the transport layer.
- BLOCKER: Ticket #2 says "map CLI commands to MCP tool definitions"
  but doesn't specify the schema format. MCP has specific schema
  requirements (JSON Schema for inputs).
- QUESTION: Ticket #6 mentions MCP resources — is this MCP spec
  resources, or something custom? The acceptance criteria are vague.
- SUGGESTION: Tickets #4 and #5 could be one ticket — the dispatch
  mechanism is the same, just different commands.
- MISSING TICKET: No ticket for MCP protocol version negotiation
  (initialize/initialized handshake).
- Verdict: NEEDS REVISION

Addressing findings...
- Ticket #1: Added MCP SDK specification, JSON-RPC transport details
- Ticket #2: Added JSON Schema mapping requirements
- Ticket #6: Clarifying with user...

User, the implementer asks: for ticket #6 (MCP resources), are these
MCP spec resources (URI-addressable data)? What data should be exposed?
> Yes, MCP spec resources. Expose the tool's config file and the
  data index as resources.

- Ticket #6: Updated with specific resources and URI scheme
- Tickets #4/#5: Keeping separate — read vs write have different
  error handling characteristics
- New ticket: Added #10 "MCP protocol handshake" to batch 1

[Adversarial Review — Round 2]
Spawning fresh implementer...

Implementer findings:
- SUGGESTION: Ticket #10 (handshake) should come before #2 in
  execution order — can't define tools before the protocol is set up.
- SUGGESTION: Ticket #8 implementation notes should reference the
  specific MCP SDK test utilities.
- Verdict: APPROVED (with minor suggestions)

Addressing suggestions...
- Reordered batch 1: #1, #10, #2, #3
- Updated ticket #8 implementation notes

## Final Tickets

### Batch 1: Core MCP Infrastructure (label: batch-1)
1. Add MCP server subcommand
2. MCP protocol handshake
3. Define MCP tool schema
4. Implement tool dispatch

### Batch 2: Tool Implementations (label: batch-2)
5. Expose read commands as MCP tools
6. Expose write commands as MCP tools
7. Add MCP resource support

### Batch 3: Polish (label: batch-3)
8. Error handling and JSON-RPC error codes
9. Integration tests
10. Documentation

Review rounds: 2
Human clarifications: 1

Approve for upstream creation?
> Yes

Creating batch labels...
Creating tickets (10 subagents)...

## Tickets Created

### Batch 1: Core MCP Infrastructure (label: batch-1)
- #31: Add MCP server subcommand — github.com/.../issues/31
- #32: MCP protocol handshake — github.com/.../issues/32
- #33: Define MCP tool schema — github.com/.../issues/33
- #34: Implement tool dispatch — github.com/.../issues/34

### Batch 2: Tool Implementations (label: batch-2)
- #35: Expose read commands — github.com/.../issues/35
- #36: Expose write commands — github.com/.../issues/36
- #37: Add MCP resource support — github.com/.../issues/37

### Batch 3: Polish (label: batch-3)
- #38: Error handling — github.com/.../issues/38
- #39: Integration tests — github.com/.../issues/39
- #40: Documentation — github.com/.../issues/40

All 10 tickets created successfully.
Cleaned up .tickets/ directory.

Ready for implementation with: /implement-project all tickets tagged batch-1, batch-2, batch-3
```
