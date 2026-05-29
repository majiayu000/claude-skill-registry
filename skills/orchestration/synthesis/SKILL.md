---
name: synthesis
description: |
  Traceability matrix, quality validation, completion decision.
  Semantic matching for requirement-deliverable traceability (EFL V4.0).
  Sub-Orchestrator pattern with convergence detection.
user-invocable: true
context: fork
model: opus
version: "4.1.0"
argument-hint: "[--strict | --lenient | --dry-run] [--workload <slug>]"
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Task
  - mcp__sequential-thinking__sequentialthinking
hooks:
  Setup:
    - type: command
      command: "source /home/palantir/.claude/skills/shared/workload-files.sh"
      timeout: 5000

# EFL Pattern Configuration
agent_delegation:
  enabled: true
  default_mode: true
  mode: "sub_orchestrator"
  agents:
    - type: "explore"
      role: "Phase 3-A: Semantic requirement-deliverable matching"
    - type: "explore"
      role: "Phase 3-B: Quality validation (3C checks)"
  output_paths:
    l1: ".agent/prompts/{slug}/synthesis/l1_summary.yaml"
    l2: ".agent/prompts/{slug}/synthesis/synthesis_report.md"
    l3: ".agent/prompts/{slug}/synthesis/l3_details/"

parallel_agent_config:
  enabled: true
  complexity_detection: "auto"
  agent_count_by_complexity:
    simple: 1
    moderate: 2
    complex: 3

agent_internal_feedback_loop:
  enabled: true
  max_iterations: 3
  convergence_threshold: "improvement < 5%"

review_gate:
  enabled: true
  phase: "3.5"
  criteria:
    - requirement_alignment
    - design_flow_consistency
    - gap_detection
    - conclusion_clarity

selective_feedback:
  enabled: true
  threshold: "MEDIUM"
---

# /synthesis - Traceability and Quality Validation

> **Version:** 4.1.0 | **EFL Pattern:** P1 + P3 + P5 + P6
> **Role:** Sub-Orchestrator for semantic traceability and completion decision
> **Pipeline:** After /collect, before /commit-push-pr or /rsil-plan

## 1. Purpose

Synthesis Sub-Orchestrator that:
1. Delegates analysis to specialized agents (P1)
2. Performs semantic requirement-deliverable matching (P3)
3. Validates quality (consistency, completeness, coherence)
4. Executes Phase 3.5 Review Gate (P5)
5. Tracks convergence across iterations (P6)
6. Makes COMPLETE or ITERATE decision

## 2. Invocation

```bash
/synthesis                    # Standard (80% threshold)
/synthesis --strict           # Strict mode (95% threshold)
/synthesis --lenient          # Lenient mode (60% threshold)
/synthesis --dry-run          # Analysis only, no decision
/synthesis --workload <slug>  # Explicit workload
```

## 3. Execution Flow

```
/synthesis (Sub-Orchestrator)
    |
    +-- Phase 0: Context Loading
    |   +-- Read requirements from /clarify
    |   +-- Read collection report from /collect
    |   +-- Load iteration history
    |
    +-- Phase 1: Agent Delegation (P1)
    |   +-- Agent 1: Phase 3-A Semantic Matching
    |   +-- Agent 2: Phase 3-B Quality Validation
    |
    +-- Phase 2: Convergence Detection (P6)
    |   +-- Compare with previous iteration
    |   +-- Detect improvement stall
    |
    +-- Phase 3.5: Review Gate (P5)
    |   +-- Holistic verification
    |
    +-- Phase 4: Decision
        +-- COMPLETE -> /commit-push-pr
        +-- ITERATE -> /rsil-plan
```

## 4. L1/L2/L3 Output Format

### L1 Summary (returned to main context)

```yaml
taskId: synthesis-{timestamp}
agentType: synthesis
status: success
summary: "Coverage 85%, Decision: COMPLETE"

decision: "COMPLETE"
coverage: 85.0
threshold: 80
criticalIssues: 0

l2Path: .agent/prompts/{slug}/synthesis/synthesis_report.md
requiresL2Read: false
nextActionHint: "/commit-push-pr"

eflMetrics:
  agentDelegation: true
  internalIterations: 2
  reviewGatePassed: true
  converged: false
```

### L2 Report Structure

```markdown
# Synthesis Report

## Summary
| Metric | Value |
|--------|-------|
| Coverage | 85.0% |
| Threshold | 80% |
| Decision | COMPLETE |

## Traceability Matrix
| Requirement | Status | Deliverables |
|-------------|--------|--------------|
| REQ-001 | covered | file1.py |

## Quality Validation
- Consistency: PASSED
- Completeness: PASSED
- Coherence: PASSED

## Decision
**COMPLETE** - Proceed to /commit-push-pr
```

## 5. Semantic Matching (Phase 3-A)

Unlike keyword matching, semantic analysis:
- Understands requirement intent
- Matches conceptual relationships
- Assigns confidence scores (0.0-1.0)
- Considers architectural patterns

**Coverage Classification:**
- Covered (100%): confidence >= 0.7
- Partial (50%): 0.4 <= confidence < 0.7
- Missing (0%): confidence < 0.4

## 6. Quality Validation (Phase 3-B)

**3C Checks:**
1. **Consistency**: No duplicate/conflicting implementations
2. **Completeness**: All P0 requirements covered, tests exist
3. **Coherence**: Components integrate properly

## 7. Convergence Detection (P6)

Tracks iteration progress:
- Improvement rate < 5% -> converged
- Critical issues not reducing -> escalate
- Coverage plateau (3 iterations < 2%) -> manual review
- Max iterations (5) -> force escalate

## 8. Decision Logic

| Condition | Decision | Next Action |
|-----------|----------|-------------|
| coverage >= threshold, critical=0 | COMPLETE | /commit-push-pr |
| coverage >= threshold-20, critical=0 | COMPLETE_WITH_WARNINGS | /commit-push-pr --with-warnings |
| otherwise | ITERATE | /rsil-plan |

## 9. Integration Points

### Input Dependencies
| Source | Path | Purpose |
|--------|------|---------|
| /clarify | `.agent/prompts/{slug}/clarify.yaml` | Requirements |
| /collect | `.agent/prompts/{slug}/collection_report.md` | Deliverables |

### Output Destinations
| Destination | Path | Purpose |
|-------------|------|---------|
| /commit-push-pr | synthesis_report.md | Completion evidence |
| /rsil-plan | Gaps list | Remediation input |

## 10. Handoff Contract

```yaml
handoff:
  skill: "synthesis"
  workload_slug: "{slug}"
  status: "completed"
  next_action:
    skill: "/commit-push-pr"  # or "/rsil-plan"
    arguments: "--workload {slug}"
    reason: "Coverage {X}% - {COMPLETE|ITERATE}"
```

---

### Version History

| Version | Change |
|---------|--------|
| 4.1.0 | Cleaned duplicate blocks, normalized frontmatter |
| 4.0.0 | EFL V4.0 integration (P1, P3, P5, P6) |
| 3.0.0 | Semantic matching, convergence detection |
| 2.2.0 | /rsil-plan integration |
| 1.0.0 | Initial traceability matrix |
