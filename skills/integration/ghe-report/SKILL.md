---
name: ghe-report
description: |
  Generate detailed workflow reports with metrics, health assessments, and epic-specific analysis for GitHub Elements. Covers throughput, cycle times, compliance status, and thread history.
---

## IRON LAW: User Specifications Are Sacred

**THIS LAW IS ABSOLUTE AND ADMITS NO EXCEPTIONS.**

1. **Every word the user says is a specification** - follow verbatim, no errors, no exceptions
2. **Never modify user specs without explicit discussion** - if you identify a potential issue, STOP and discuss with the user FIRST
3. **Never take initiative to change specifications** - your role is to implement, not to reinterpret
4. **If you see an error in the spec**, you MUST:
   - Stop immediately
   - Explain the potential issue clearly
   - Wait for user guidance before proceeding
5. **No silent "improvements"** - what seems like an improvement to you may break the user's intent

**Violation of this law invalidates all work produced.**

## Background Agent Boundaries

When running as a background agent, you may ONLY write to:
- The project directory and its subdirectories
- The parent directory (for sub-git projects)
- ~/.claude (for plugin/settings fixes)
- /tmp

Do NOT write outside these locations.

---

## GHE_REPORTS Rule (MANDATORY)

**ALL reports MUST be posted to BOTH locations:**

1. **GitHub Issue Thread** - Full report text (NOT just a link!)
2. **GHE_REPORTS/** - Same full report text (FLAT structure, no subfolders!)

**Report naming:** `<TIMESTAMP>_<title or description>_(<AGENT>).md`
**Timestamp format:** `YYYYMMDDHHMMSSTimezone`

**Example:** `20251206200000GMT+01_status_report_(Hermes).md`

**ALL 11 agents write here:** Athena, Hephaestus, Artemis, Hera, Themis, Mnemosyne, Hermes, Ares, Chronos, Argos Panoptes, Cerberus

**REQUIREMENTS/** is SEPARATE - permanent design documents, never deleted.

**Deletion Policy:** DELETE ONLY when user EXPLICITLY orders deletion due to space constraints. DO NOT delete during normal cleanup.

---

## Settings Awareness

Respects `.claude/ghe.local.md`:
- `enabled`: If false, return minimal report
- `notification_level`: verbose/normal/quiet - affects detail level
- `stale_threshold_hours`: Used for stale thread detection

---

# GitHub Elements Report (Detailed Analysis)

**Purpose**: Generate detailed reports with metrics, health assessment, or epic analysis. More comprehensive than quick status.

## Report Types

### 1. Metrics Report
Performance indicators and trends:
- Throughput (features completed, bugs fixed)
- Cycle times (average sessions per phase)
- First-pass REVIEW rate
- Demotion rate
- Agent performance comparison

### 2. Health Report
Workflow compliance assessment:
- Rule compliance status
- Stale threads detection
- Violation history
- Memory bank synchronization status
- Overall health score

### 3. Epic Report
Single epic deep dive:
- Thread history (all DEV/TEST/REVIEW cycles)
- Current phase and progress
- Key technical decisions
- Remaining work estimation

## When to Use

- Performance analysis
- Compliance audits
- Epic-specific status
- Trend analysis
- Health assessment

## How to Execute

Spawn **reporter** agent with appropriate report type:

```
reporter(type="metrics")  → Performance report
reporter(type="health")   → Compliance report
reporter(type="epic", epic="epic-name") → Epic report
```

## Output Formats

### Metrics Report
```markdown
## GitHub Elements Metrics Report

### Throughput
| Metric | Value | Trend |
|--------|-------|-------|
| Features completed | N | +/- vs last week |
| Bugs fixed | N | +/- vs last week |

### Cycle Times
| Phase | Avg Duration | Issues Processed |
|-------|--------------|------------------|
| DEV | N sessions | N |
| TEST | N sessions | N |
| REVIEW | N sessions | N |

### Quality Metrics
- First-pass REVIEW rate: N%
- Demotion rate: N%
- Test coverage (avg): N%
```

### Health Report
```markdown
## GitHub Elements Health Report

### Compliance Status
| Rule | Status | Notes |
|------|--------|-------|
| One thread at a time | PASS/FAIL | |
| Phase order | PASS/FAIL | |
| Checkpoint frequency | PASS/WARN | |

### Stale Threads
[Threads with no activity > 24h]

### Violation History
[Recent violations and resolutions]

### Overall Health
[HEALTHY / WARNINGS / CRITICAL]
```

### Epic Report
```markdown
## Epic Report: [Epic Name]

### Thread History
| Issue | Type | Status | Duration |
|-------|------|--------|----------|

### Current Phase
[Current phase with progress]

### Key Decisions
[Technical decisions made]

### Remaining Work
[Estimated remaining effort]
```

## Key Differentiator

This skill provides DETAILED ANALYSIS. For a quick current-state overview, use `ghe-status` instead.
