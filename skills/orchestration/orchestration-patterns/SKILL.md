---
name: orchestration-patterns
description: Agentic orchestration patterns for long-running tasks. Implements evidence-based delivery and Simon Willison's agent loop. Use when managing multi-step work, coordinating subagents, or orchestrating PR workflows.
---

# Orchestration Patterns Skill

## Purpose

Codify evidence-based delivery and iterative agent loop for orchestrating complex, long-running tasks. These patterns ensure verifiable progress and intelligent escalation.

## When This Skill Applies

Invoke this skill when:

- Orchestrating multi-step implementation tasks
- Managing work across multiple subagents
- Running long-running sessions that need checkpoints
- Preparing PRs for merge (mandatory QAS gate)
- Coordinating team handoffs

## Simon Willison's Agent Loop

**Core Philosophy**: "Iterate until success or blocked, then escalate."

```text
┌─────────────────────────────────────────────────────────┐
│  THE AGENT LOOP (for every task)                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. GOAL DEFINITION                                     │
│     └─ Clear acceptance criteria (from BSA/ticket)      │
│                                                         │
│  2. PATTERN DISCOVERY                                   │
│     └─ Search codebase, docs, previous sessions         │
│     └─ Use: pattern-discovery skill (auto-invoked)      │
│     └─ Or: /search-pattern for explicit code search     │
│                                                         │
│  3. ITERATIVE EXECUTION LOOP:                           │
│     ┌─────────────────────────────────────────────┐     │
│     │  Implement approach                         │     │
│     │       ↓                                     │     │
│     │  Run validation (yarn ci:validate)          │     │
│     │       ↓                                     │     │
│     │  If PASS → proceed to evidence              │     │
│     │  If FAIL → analyze error, adjust, repeat    │     │
│     │  If BLOCKED → escalate to TDM with context  │     │
│     └─────────────────────────────────────────────┘     │
│                                                         │
│  4. EVIDENCE ATTACHMENT                                 │
│     └─ Attach proof to Linear (see templates below)     │
│                                                         │
│  5. QAS GATE (MANDATORY before merge)                   │
│     └─ Invoke QAS subagent for independent review       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Evidence-Based Delivery

**Core Principle**: "All work requires verifiable evidence - no 'trust me, it works'"

### Evidence Types

| Type           | What It Proves             | Example                    |
| -------------- | -------------------------- | -------------------------- |
| Test Results   | Code works as expected     | `yarn ci:validate` output  |
| Screenshots    | UI changes are correct     | Before/after comparison    |
| Command Output | Operations completed       | Build logs, migration logs |
| QAS Report     | Independent verification   | QA validation markdown     |
| Session ID     | Full audit trail available | Claude Code session ref    |

### Phase Evidence Requirements

| Phase       | Evidence Required              | Linear Template        |
| ----------- | ------------------------------ | ---------------------- |
| **Dev**     | Test results, command output   | Dev Evidence Template  |
| **Staging** | UAT validation or N/A + reason | Staging Template       |
| **Done**    | QAS report, merge confirmation | Done Evidence Template |

## QAS Pre-Merge Gate

**MANDATORY**: Before merging any PR, invoke QAS for independent review.

### Why QAS Gate Matters

1. **Separation of Concerns**: QAS validates but doesn't write product code
2. **Independent Verification**: Catches what implementer missed
3. **Bias Prevention**: Fresh eyes on commit messages, patterns
4. **Evidence in Linear**: QAS posts final evidence + verdict to Linear (system of record)

### QAS Invocation Pattern

```text
# After implementation complete, before merge:
Task tool: QAS subagent
Prompt: "Review PR #XXX for WOR-YYY. Validate:
  - Commit message format (ticket in subject line)
  - Code patterns (RLS, naming, structure)
  - CI status (all checks passing)
  - Evidence attachments in Linear
  Generate validation report to docs/agent-outputs/qa-validations/"
```

### QAS Output Location

All QAS reports go to: `docs/agent-outputs/qa-validations/WOR-{number}-qa-validation.md`

## Escalation Patterns

### When to Escalate

| Condition              | Escalate To | Include                     |
| ---------------------- | ----------- | --------------------------- |
| Blocked > 4 hours      | TDM         | Full context, attempts made |
| Architecture ambiguity | ARCHitect   | Options, trade-offs         |
| Cross-team dependency  | TDM         | Which teams, what's blocked |
| Security concern       | SecEng      | Specific risk, evidence     |

### Escalation Template

```markdown
**Escalation Required**

**Blocked On**: [specific blocker]
**Attempts Made**:

1. [what you tried]
2. [what you tried]

**Context**:

- Ticket: WOR-XXX
- Session ID: [if available]
- Time blocked: X hours

**Request**: [specific ask - what do you need?]
```

## Long-Running Task Checkpoints

For tasks spanning multiple tool calls or sessions:

### Checkpoint Pattern

```text
Every 10-15 tool calls:
1. Update todo list with current progress
2. If nearing context limit, summarize state
3. If handoff needed, provide continuation context

At session boundaries:
1. Summarize completed work
2. List remaining items
3. Document any blockers
4. Attach evidence to Linear
```

### State Preservation

```markdown
**Session Checkpoint**

**Completed**:

- [x] Task 1
- [x] Task 2

**In Progress**:

- [ ] Task 3 (at step X)

**Remaining**:

- [ ] Task 4
- [ ] Task 5

**Blockers**: [if any]

**Next Action**: [specific next step]
```

## Orchestration Workflow Example

```text
# Complete workflow for feature implementation:

1. /start-work WOR-XXX
   └─ Syncs to dev, creates branch, sets context

2. Pattern discovery (skill auto-invokes or use /search-pattern)
   └─ Finds relevant patterns before implementation

3. [Implementation with agent loop]
   ├─ Implement
   ├─ Validate (yarn ci:validate)
   ├─ Adjust if needed
   └─ Repeat until passing

4. /pre-pr
   └─ Full validation checklist

5. Create PR with evidence

6. [QAS GATE - MANDATORY]
   └─ Invoke QAS subagent for review
   └─ Fix any blocking issues
   └─ Commit QAS report

7. Merge (only after QAS approval)

8. /end-work
   └─ Updates Linear, cleans up
```

## Authoritative References

- **wtfb-safe-agentic-workflow**: Core agentic principles
- **AGENT_WORKFLOW_SOP.md**: Full agent workflow documentation
- **CONTRIBUTING.md**: Workflow requirements
- **linear-sop skill**: Evidence templates for Linear

## Anti-Patterns to Avoid

| Anti-Pattern             | Why It's Bad                | Do This Instead               |
| ------------------------ | --------------------------- | ----------------------------- |
| Skip QAS review          | Miss commit message issues  | Always invoke QAS pre-merge   |
| No evidence in Linear    | No audit trail              | Attach evidence every phase   |
| Ignore CI failures       | Broken code reaches dev     | Fix in agent loop, don't skip |
| Force-push without check | May lose teammate's changes | Use --force-with-lease        |
| Continue when blocked    | Waste time, no progress     | Escalate with context         |
