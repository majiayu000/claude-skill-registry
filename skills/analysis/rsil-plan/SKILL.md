---
name: rsil-plan
description: |
  Requirements-Synthesis Integration Loop (RSIL).
  Performs code-level gap analysis and creates remediation plans.
  Called after /synthesis ITERATE decision.
user-invocable: true
context: fork
model: opus
version: "3.1.0"
argument-hint: "[--iteration <n>] [--auto-remediate] [--workload <slug>]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Task
  - TaskCreate
  - TaskUpdate
  - TaskList
  - Write
  - mcp__sequential-thinking__sequentialthinking
hooks:
  Setup:
    - type: command
      command: "source /home/palantir/.claude/skills/shared/workload-files.sh && source /home/palantir/.claude/skills/shared/validation-feedback-loop.sh"
      timeout: 5000

# EFL Pattern Configuration
agent_delegation:
  enabled: true
  default_mode: true
  max_sub_agents: 3
  delegation_strategy: "phase-based"
  strategies:
    gap_verification:
      description: "Delegate code-level gap verification to explore agents"
    evidence_collection:
      description: "Delegate evidence collection from codebase"
  output_paths:
    l1: ".agent/prompts/{slug}/rsil-plan/l1_summary.yaml"
    l2: ".agent/prompts/{slug}/rsil-plan/iteration_{n}.md"
    l3: ".agent/prompts/{slug}/rsil-plan/l3_details/"

parallel_agent_config:
  enabled: true
  complexity_detection: "auto"
  agent_count_by_complexity:
    simple: 1
    moderate: 2
    complex: 3
  gap_areas:
    - requirement_verification
    - code_evidence_collection
    - test_coverage_check

agent_internal_feedback_loop:
  enabled: true
  max_iterations: 3
  validation_criteria:
    completeness:
      - "All requirements verified against codebase"
      - "Evidence collected for each finding"
    quality:
      - "Code evidence includes file paths and snippets"
      - "Remediation recommendations specific"

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

# /rsil-plan - Requirements-Synthesis Integration Loop

> **Version:** 3.1.0 | **EFL Pattern:** P1 + P2 + P5 + P6
> **Role:** Gap Analysis and Remediation Planning
> **Pipeline:** After /synthesis ITERATE, before /orchestrate or /clarify

## 1. Purpose

RSIL handles iteration cycles when /synthesis returns ITERATE:

1. Verifies gaps at code level (not just keyword matching)
2. Collects evidence from codebase
3. Classifies gaps (COVERED/PARTIAL/MISSING)
4. Creates remediation tasks
5. Decides AUTO_REMEDIATE or ESCALATE

## 2. Invocation

```bash
/rsil-plan                          # Auto-detect iteration
/rsil-plan --iteration 2            # Specific iteration
/rsil-plan --auto-remediate         # Skip user confirmation
/rsil-plan --workload <slug>        # Explicit workload
```

## 3. Pipeline Integration

```
/synthesis
    |
    +-- ITERATE --> /rsil-plan <-- THIS SKILL
                        |
                        +-- Phase 1: Parallel Explore Agents (P2)
                        +-- Phase 2: L1 Aggregation
                        +-- Phase 3-A: L2 Horizontal Synthesis
                        +-- Phase 3-B: L3 Vertical Verification
                        +-- Phase 3.5: Review Gate (P5)
                        +-- Phase 4: Selective Feedback (P4)
                        +-- Phase 5: User Decision
                        |
                        +-- AUTO_REMEDIATE --> /orchestrate
                        +-- ESCALATE --> /clarify
```

## 4. L1/L2/L3 Output Format

### L1 Summary (returned to main context)

```yaml
taskId: rsil-{iteration}-{timestamp}
agentType: rsil-plan
status: success
summary: "RSIL complete: 3 gaps, 2 tasks, EFL verified"

priority: HIGH
decision: "AUTO_REMEDIATE"
gapStats:
  total: 3
  missing: 1
  partial: 2
  highComplexity: 0

l2Path: .agent/prompts/{slug}/rsil-plan/iteration_{n}.md
requiresL2Read: false
nextActionHint: "/orchestrate --workload {slug}"

eflMetrics:
  totalAgents: 2
  parallelPhases: 3
  feedbackLoops: 1
  internalIterations: 4
```

### L2 Report Structure

```markdown
# RSIL Gap Analysis Report - Iteration {n}

## Summary
| Metric | Value |
|--------|-------|
| COVERED | 5 (62%) |
| PARTIAL | 2 (25%) |
| MISSING | 1 (13%) |

## Decision
**AUTO_REMEDIATE** - Proceeding with /orchestrate

## Gap Details

### MISSING
| ID | Requirement | Complexity |
|----|-------------|------------|
| REQ-003 | Error handling | medium |

### PARTIAL
| ID | Requirement | Evidence |
|----|-------------|----------|
| REQ-002 | Auth flow | src/auth.ts (1 match) |

## Remediation Tasks Created
| Task ID | Requirement | Complexity |
|---------|-------------|------------|
| #101 | REQ-003 | medium |

## Next Action
/orchestrate --workload {slug}
```

## 5. Gap Classification

| Status | Code Evidence | Action |
|--------|---------------|--------|
| COVERED | 3+ matches | No action |
| PARTIAL | 1-2 matches | Complete implementation |
| MISSING | 0 matches | Full implementation |

## 6. Evidence Collection

```javascript
// Generate Grep patterns from requirement
const patterns = [
  { regex: "(function|class|def).*keyword", fileType: "ts,js,py" },
  { regex: "(describe|test|it).*keyword", fileType: "ts,js" },
  { regex: "(import|from).*keyword", fileType: "ts,js,py" }
];

// Search codebase
for (pattern of patterns) {
  results = await Grep({ pattern: pattern.regex, type: pattern.fileType });
  evidence.files.push(...results.files);
}
```

## 7. Decision Logic

| Condition | Decision |
|-----------|----------|
| gaps <= 3, highComplexity < 1 | AUTO_REMEDIATE |
| gaps > 3 OR highComplexity >= 1 | ESCALATE |

## 8. Remediation Task Creation

```javascript
const task = await TaskCreate({
  subject: `[RSIL-${iteration}] ${action}: ${requirement}`,
  description: generateTaskDescription(gap),
  activeForm: `Remediating: ${requirementId}`
});
```

## 9. Input Dependencies

| Source | Path | Purpose |
|--------|------|---------|
| /clarify | `.agent/prompts/{slug}/clarify.yaml` | Requirements |
| /synthesis | `.agent/prompts/{slug}/synthesis/synthesis_report.md` | Gaps |
| /research | `.agent/prompts/{slug}/research.md` | Patterns |
| /planning | `.agent/prompts/{slug}/plan.yaml` | Phases |

## 10. Output Destinations

| Destination | Path | Purpose |
|-------------|------|---------|
| Native Tasks | TaskCreate API | Remediation tasks |
| /orchestrate | iteration_{n}_remediation.yaml | Plan YAML |
| /clarify | Gap descriptions | Requirements update |

## 11. Handoff Contract

```yaml
handoff:
  skill: "rsil-plan"
  workload_slug: "{slug}"
  status: "completed"
  next_action:
    skill: "/orchestrate"  # or "/clarify"
    arguments: "--workload {slug}"
    reason: "Gap analysis complete, {n} tasks created"
```

## 12. Configuration

```javascript
const DEFAULT_CONFIG = {
  gapThreshold: 3,           // Max gaps for auto-remediate
  highComplexityThreshold: 1, // Max high-complexity gaps
  maxIterations: 5,          // Max RSIL iterations
  evidenceThreshold: {
    covered: 3,              // Matches for COVERED
    partial: 1               // Matches for PARTIAL
  }
};
```

---

### Version History

| Version | Change |
|---------|--------|
| 3.1.0 | Cleaned duplicate blocks, normalized frontmatter |
| 3.0.0 | Full EFL implementation (P1-P6) |
| 1.2.0 | Standalone execution, handoff contract |
| 1.1.0 | Workload-scoped output paths |
| 1.0.0 | Initial RSIL implementation |
