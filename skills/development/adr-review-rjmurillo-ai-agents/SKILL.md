---
name: adr-review
description: Multi-agent debate orchestration for Architecture Decision Records. Automatically triggers on ADR create/edit/delete. Coordinates architect, critic, independent-thinker, security, analyst, and high-level-advisor agents in structured debate rounds until consensus.
license: MIT
metadata:
  subagent_model: claude-opus-4-5
  domains: [architecture, governance, multi-agent, consensus]
  type: orchestrator
  inputs: [adr-file-path, change-type]
  outputs: [debate-log, updated-adr, recommendations]
  file_triggers:
    patterns:
      - ".agents/architecture/ADR-*.md"
      - "docs/architecture/ADR-*.md"
    events: [create, update, delete]
    auto_invoke: true
---

# ADR Review

Multi-agent debate pattern for rigorous ADR validation. Orchestrates 6 specialized agents through structured review rounds until consensus or 10 rounds maximum.

## Quick Start

```text
# Manual triggers:
/adr-review .agents/architecture/ADR-005-api-versioning.md
"review this ADR"
"validate ADR-005"
```

**Automatic Detection**: A Claude Code hook (`Invoke-ADRChangeDetection.ps1`) runs at session start and detects ADR changes, prompting you to invoke this skill. The pre-commit hook also detects staged ADR files and displays a reminder.

| Input | Output | Consensus Required |
|-------|--------|-------------------|
| ADR file path | Debate log + Updated ADR | 6/6 Accept or D&C |

## File Triggers

| Pattern | Location | Events |
|---------|----------|--------|
| `ADR-*.md` | `.agents/architecture/` | create, update, delete |
| `ADR-*.md` | `docs/architecture/` | create, update, delete |

**Detection**: `.claude/skills/adr-review/scripts/Detect-ADRChanges.ps1`

## When to Use

**MANDATORY Triggers** (automatic):

- Architect creates or updates an ADR
- ANY agent modifies `.agents/architecture/ADR-*.md`

**User-Initiated Triggers** (manual):

- User requests ADR review ("review this ADR", "validate this decision")
- User requests multi-perspective validation for strategic decisions

## Agent Roles

| Agent | Focus | Tie-Breaker Role |
|-------|-------|------------------|
| **architect** | Structure, governance, coherence, ADR compliance | Structural questions |
| **critic** | Gaps, risks, alignment, completeness | None |
| **independent-thinker** | Challenge assumptions, surface contrarian views | None |
| **security** | Threat models, security trade-offs | None |
| **analyst** | Root cause, evidence, feasibility | None |
| **high-level-advisor** | Priority, resolve conflicts, break ties | Decision paralysis |

## Debate Protocol

| Phase | Purpose | Details |
|-------|---------|---------|
| **Phase 0** | Related work research | Search issues/PRs for context |
| **Phase 1** | Independent review | Each agent reviews ADR |
| **Phase 2** | Consolidation | Identify consensus and conflicts |
| **Phase 3** | Resolution | Propose updates for P0/P1 issues |
| **Phase 4** | Convergence check | Agents vote: Accept/D&C/Block |

**Consensus**: All 6 agents Accept OR Disagree-and-Commit. Max 10 rounds.

See [references/debate-protocol.md](references/debate-protocol.md) for full phase details.

## Deletion Workflow

| Phase | Purpose |
|-------|---------|
| **D1** | Detection - identify deleted ADR |
| **D2** | Impact assessment - find dependencies |
| **D3** | Archival decision - archive accepted ADRs |
| **D4** | Cleanup - update references |

See [references/deletion-workflow.md](references/deletion-workflow.md) for full workflow.

## Issue Resolution

| Priority | Requirement | Gate |
|----------|-------------|------|
| **P0** | Must resolve | BLOCKING |
| **P1** | Resolve OR defer with issue | BLOCKING |
| **P2** | Document | Non-blocking |

See [references/issue-resolution.md](references/issue-resolution.md) for deferral protocol.

## Phase 4: Strategic Review (Principal-Level Validation)

After structural and technical review, apply strategic lenses:

### Strategic Validation Checklist

#### Chesterton's Fence (Change Justification)

- [ ] If removing/changing existing patterns: Original purpose documented
- [ ] Investigation evidence provided (git archaeology, interviews, documentation)
- [ ] Confirmation original problem no longer exists
- [ ] Assessment: [PASS | FAIL | N/A]

#### Path Dependence (Irreversibility Recognition)

- [ ] Historical constraints identified and documented
- [ ] Reversibility assessment complete (rollback capability, vendor lock-in)
- [ ] Migration/exit strategy defined if adding dependencies
- [ ] Irreversible decisions explicitly flagged and justified
- [ ] Assessment: [PASS | FAIL | N/A]

#### Core vs Context (Investment Prioritization)

- [ ] Capability classified as Core (differentiating) or Context (commodity)
- [ ] If building Context: Justification for not buying/outsourcing
- [ ] If Core: Competitive differentiation explained
- [ ] Assessment: [PASS | FAIL | N/A]

#### Second-System Effect (Over-Engineering Detection)

- [ ] If replacing existing system: Scope boundaries explicit
- [ ] Feature list justified (not "everything we didn't do last time")
- [ ] Simplicity preservation strategy documented
- [ ] Assessment: [PASS | FAIL | N/A]

### Strategic Review Verdict

**Overall Strategic Assessment**: [APPROVED | CONCERNS | REJECTED]

**Blocking Issues**:

- [Strategic issue 1 with required mitigation]
- [Strategic issue 2 with required mitigation]

**Recommendations**:

- [Strategic improvement 1]
- [Strategic improvement 2]

## Scripts

| Script | Purpose |
|--------|---------|
| `Detect-ADRChanges.ps1` | Detect ADR file changes for auto-trigger |

```powershell
# Basic detection
& .claude/skills/adr-review/scripts/Detect-ADRChanges.ps1

# Compare to specific commit
& .claude/skills/adr-review/scripts/Detect-ADRChanges.ps1 -SinceCommit "abc123"
```

## Verification Checklist

After skill invocation:

- [ ] Debate log exists at `.agents/critique/ADR-NNN-debate-log.md`
- [ ] ADR status updated (proposed/accepted/needs-revision)
- [ ] All P0 issues addressed or documented
- [ ] Dissent captured for Disagree-and-Commit positions
- [ ] Recommendations provided to orchestrator

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Single-agent ADR review | Misses domain expertise | Use full 6-agent debate |
| Skipping Phase 0 | Duplicates existing work | Always research first |
| Ignoring D&C dissent | Loses important context | Document all reservations |
| Manual ADR monitoring | Error-prone | Use Detect-ADRChanges.ps1 |
| Deleting accepted ADRs without archive | Loses knowledge | Always archive accepted ADRs |

## References

| Document | Content |
|----------|---------|
| [debate-protocol.md](references/debate-protocol.md) | Full Phases 0-4 workflow |
| [deletion-workflow.md](references/deletion-workflow.md) | Phases D1-D4 workflow |
| [issue-resolution.md](references/issue-resolution.md) | P0/P1/P2 handling and deferral |
| [artifacts.md](references/artifacts.md) | Output formats and templates |
| [agent-prompts.md](references/agent-prompts.md) | Detailed agent prompt templates |
