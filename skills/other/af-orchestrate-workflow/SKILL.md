---
name: af-orchestrate-workflow
description: Orchestrate AgentFlow's 4-phase development process with agent delegation patterns. Use when coordinating phase transitions, managing intervention points, or understanding deep orchestration workflows.

title: Orchestration Skill
created: 2026-01-05
updated: 2026-01-05
last_checked: 2026-01-05
tags: [skill, orchestration, workflow, coordination, phases, roles]
parent: ../README.md
related:
  - ../../CLAUDE-agentflow.md
---

# Orchestration Skill

## When to Use This Skill

Load this skill when you need:
- Detailed guidance on phase transitions
- Role-specific workflow details (PM, UX, QA, SE)
- Troubleshooting when work is stuck or off track
- Understanding approval gates and intervention points
- Coordinating multi-role collaboration

**Note:** Core orchestration context is in CLAUDE-agentflow.md (always loaded). This skill provides the detailed playbook.

## Quick Reference

**You ARE the orchestrator.** CLAUDE-agentflow.md establishes this. This skill helps you execute.

| Phase | Process Skill | Key Agents |
|-------|--------------|------------|
| Setup | `af-setup-project` | - |
| Discovery | `af-discover-scope` | `af-work-management-agent` |
| Refinement | `af-refine-specifications` | `af-bdd-agent`, `af-ux-design-agent` |
| Delivery | `af-deliver-features` | `af-dev-test-agent`, `af-code-quality-agent` |
| Quality (cross-cutting) | `af-validate-quality` | `af-docs-quality-agent`, `af-architecture-quality-agent` |

## Rules

### Phase Identification

Identify the current phase from context:

| Keywords/Signals | Phase |
|-----------------|-------|
| "setup", "initialize", "bootstrap", "new project" | Setup |
| "explore", "discover", "understand", "what should we build" | Discovery |
| "requirements", "BDD", "scenarios", "specifications", "mini-PRD" | Refinement |
| "implement", "develop", "code", "TDD", "build the feature" | Delivery |
| "validate", "quality", "check", "audit", "review" | Quality (any phase) |

### Sub-agent Invocation

**MUST invoke sub-agents when:**
- Process skill explicitly recommends agent for task
- Task requires specialized execution context
- Validation or transformation needed
- Large volume of similar work

**MUST NOT invoke sub-agents when:**
- Task can be handled in main conversation
- Simple information retrieval
- Direct command execution
- You have unique context costly to transfer

### Approval Gates

Never proceed past these without human approval:

| Gate | When | Who Approves |
|------|------|--------------|
| Discovery → Refinement | Feature scope defined, ADRs written | PM |
| Mini-PRD approval | Scenarios and designs complete (`approval:bdd-approved` + `approval:ux-approved` labels set) | PM + QA |
| Refinement → Delivery | Specifications locked | PM |
| Merge to main | Tests passing, code reviewed | SE |
| Release to Production | QA verification complete | PM |

## Workflows

### Workflow: Starting a New Session

**When:** Session begins or resumes after compaction

**Procedure:**
```
1. SessionStart hook fires
2. Check for current-task.md
   - EXISTS: Read it, identify phase and role, resume work
   - MISSING: Ask user what they want to work on
3. Identify human's role (PM, UX, QA, SE, or multi-hat)
4. Load appropriate process skill for current phase
5. Summarize context and propose next steps
6. Wait for human direction
```

### Workflow: Phase Transition

**When:** Current phase work is complete, ready to move forward

**Procedure:**
```
1. Verify phase completion criteria met
2. STOP - Ask human for approval to transition
3. On approval:
   - Update Linear status
   - Update current-task.md with new phase
   - Load new phase's process skill
   - Summarize what's next
4. On rejection:
   - Ask what's missing
   - Continue in current phase
```

### Workflow: Role-Specific Guidance

**When:** Human identifies their role or you need role-appropriate guidance

**PM + AI Workflow:**
```
Setup:      Create project brief, define scope
Discovery:  Discover requirements, create estimates, configure Linear
Refinement:   Approve designs, approve requirements, plan milestones
Delivery:   Approve releases to production
```

**UX + AI Workflow:**
```
Setup:      Establish brand system specification, reference class
Discovery:  Define base design tokens, identify atoms (shadcn/ui primitives)
Refinement:   Catalog Check → Create molecules/organisms → Storybook → Tests
Delivery:   Engineering wires components, UX Review before PR
```

**QA + AI Workflow:**
```
Setup:      -
Discovery:  -
Refinement:   Refine requirements, develop test definitions, verify designs
Delivery:   Approve Dev→Test, verify Test→Prod transitions
```

**SE + AI Workflow:**
```
Setup:      Architecture analysis, GI Standard setup, auth implementation
Discovery:  Review ADRs, set up tooling (logging, alerting, observability)
Refinement:   Review ADRs
Delivery:   Implement tests, implement features, approve merges
```

### Workflow: Estimation

**When:** Estimating effort during Discovery or Refinement phase

**Procedure:**
```
1. Load af-estimate-effort

2. Discovery phase (feature-level):
   - Decompose each feature by functional area (FE, BE, INFRA, TEST, UX, DOCS)
   - Estimate hours per area, sum total, convert to fibonacci points
   - Set story points on each Linear feature issue
   - Post [Discovery Estimate] comment with structured breakdown
   - Confidence is typically Low or Medium

3. Refinement phase (atomic with roll-up):
   - After mini-PRD and BDD scenarios are complete
   - For features > 3 points: create sub-issues with individual estimates
   - Estimate each sub-issue by functional area in hours
   - Roll up BOTH hours AND points to parent feature
   - Post [Refined Estimate] comment on parent feature
   - Complete mini-PRD Section 7 (Effort Estimation)
   - Story points must be set before moving to "Approved"

4. Key rules:
   - Always decompose before estimating (never guess a single number)
   - 1 point = 3 hours = half a productive day (6 hours/day)
   - Round up to next fibonacci value, never down
   - Include testing (30-50% of implementation), docs, and infrastructure
```

### Workflow: Troubleshooting Stuck Work

**When:** Progress has stalled, unclear how to proceed

**Procedure:**
```
1. Identify the blocker type:
   - UNCLEAR REQUIREMENTS → Ask PM for clarification
   - TECHNICAL BLOCKERS → Research, ask SE for help
   - APPROVAL PENDING → Identify approver, prompt for decision
   - DESIGN INCOMPLETE → Check with UX
   - TESTS FAILING → Debug, check af-configure-test-frameworks

2. Update current-task.md with blocker details

3. If blocker persists:
   - Document in Linear issue
   - Propose alternative approaches
   - Ask human for decision

4. Never silently skip blocked work
```

### Workflow: Multi-Role Coordination

**When:** Work requires handoffs between roles

**Procedure:**
```
1. Identify handoff point (e.g., UX → SE, QA → PM)
2. Ensure deliverables are complete:
   - UX → SE: Storybook stories, selector contracts
   - SE → QA: Feature on dev branch, test evidence
   - QA → PM: Test report, verification status
3. Update Linear with handoff status
4. Notify receiving role (or prompt human to notify)
5. Document handoff in current-task.md
```

## Examples

**User: "Let's start building the signup feature"**
```
→ Identify: Delivery phase (implementation request)
→ Check: Is there an approved mini-PRD? (Refinement gate)
→ If NO: "We need to complete Refinement first. Shall I start /refinement:refine?"
→ If YES: Load af-deliver-features, begin TDD cycle
```

**User: "I'm the PM, what should I focus on?"**
```
→ Identify: Role = PM
→ Check: Current phase from current-task.md or Linear
→ Consult role-phase matrix for PM activities in current phase
→ Propose specific next steps based on PM responsibilities
```

**User: "This feature is stuck, help"**
```
→ Read current-task.md for context
→ Check Linear for status and blockers
→ Identify blocker type (requirements? technical? approval?)
→ Propose resolution based on blocker type
→ Ask human for decision on path forward
```

**User: "The designer finished the mockups"**
```
→ Identify: UX → SE handoff (or UX → QA for review)
→ Check: Are Storybook stories created?
→ Check: Is selector contract defined?
→ If complete: Update Linear, propose next steps for SE
→ If incomplete: List missing deliverables for UX
```

## Common Pitfalls

### 1. Skipping Approval Gates
**Problem:** Proceeding to implementation without mini-PRD approval
**Solution:** Always check for approval before phase transitions

### 2. Wrong Phase for Request
**Problem:** User asks to "implement" but Refinement not complete
**Solution:** Identify phase gaps, propose completing prerequisites

### 3. Role Confusion
**Problem:** Giving SE tasks to PM or vice versa
**Solution:** Confirm role, consult role-phase matrix

### 4. Lost Context After Compaction
**Problem:** Forgetting phase/role after context compaction
**Solution:** SessionStart hook reminds, current-task.md stores state

### 5. Autonomous Phase Transitions
**Problem:** Moving to next phase without human approval
**Solution:** Always stop and ask at phase boundaries

## Essential Reading

- **Core orchestration context:** `CLAUDE-agentflow.md` (always loaded)
- **Work state management:** `af-manage-work-state`
- **Phase-specific workflows:** `af-{phase}-process` skills

---

**Remember:** You ARE the orchestrator. Drive work forward, but respect human decision points. When in doubt, ask.
