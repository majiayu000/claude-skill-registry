---
name: goodvibes-codebase-review
description: >-
  Comprehensive codebase review and parallel agent-based remediation skill. 
  Use PROACTIVELY when agent needs to perform full codebase audit, generate 
  master findings report with quantified metrics, and execute remediation 
  using parallel goodvibes background agents (max 6 concurrent, one task 
  per agent with fresh context). Triggers on: codebase review, code audit, 
  full project analysis, quality assessment, technical debt analysis, 
  parallel remediation, bulk fixes.
---

# Goodvibes Codebase Review & Remediation

Systematic codebase analysis with parallelized remediation using goodvibes agents.

**CRITICAL: Be objective & completely honest. No sugar coating, EVER.**

- **Honest Review**: Honest reviews yield better results. Never consider emotions or feelings in your assessments.

## Filesystem Boundaries

**CRITICAL: Write-local, read-global.**

- **WRITE/EDIT/CREATE**: ONLY within the current working directory and its subdirectories
- **READ**: Can read any file anywhere for context
- **NEVER WRITE** to: parent directories, home directory, system files, other projects

## MCP Tool Checklist (MANDATORY)

**STOP. Before doing ANYTHING, complete this checklist.**

### Task Start

```bash
mcp__plugin_goodvibes_goodvibes-tools__detect_stack '{}'
mcp__plugin_goodvibes_goodvibes-tools__recommend_skills '{"task":"codebase review quality audit"}'
mcp__plugin_goodvibes_goodvibes-tools__project_issues '{}'
```

### Review Phase

```bash
mcp__plugin_goodvibes_goodvibes-tools__check_types '{}'
mcp__plugin_goodvibes_goodvibes-tools__find_circular_deps '{}'
mcp__plugin_goodvibes_goodvibes-tools__scan_for_secrets '{}'
mcp__plugin_goodvibes_goodvibes-tools__analyze_dependencies '{}'
mcp__plugin_goodvibes_goodvibes-tools__identify_tech_debt '{}'
mcp__plugin_goodvibes_goodvibes-tools__find_dead_code '{}'
mcp__plugin_goodvibes_goodvibes-tools__get_test_coverage '{}'
```

### Before Every Edit

```bash
mcp__plugin_goodvibes_goodvibes-tools__scan_patterns '{}'
mcp__plugin_goodvibes_goodvibes-tools__find_tests_for_file '{"file":"..."}'
mcp__plugin_goodvibes_goodvibes-tools__validate_edits_preview '{}'
```

### After Every Edit

```bash
mcp__plugin_goodvibes_goodvibes-tools__check_types '{}'
mcp__plugin_goodvibes_goodvibes-tools__get_diagnostics '{"file":"..."}'
```

**THE LAW: If a goodvibes tool can do it, USE THE TOOL. No exceptions.**

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      CODEBASE REVIEW                        │
├─────────────────────────────────────────────────────────────┤
│  Phase 1: Review      │  Run MCP tools, analyze all code   │
│  Phase 2: Report      │  Generate codebase-review-report.md │
│  Phase 3: Plan        │  Create remediation-plan.md        │
│  Phase 4: Execute     │  Parallel agents (max 6)           │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Codebase Review

### MCP Tool Mapping

| Category | Primary Tools | Fallback |
|----------|---------------|----------|
| **Quality** | `find_dead_code`, `scan_patterns`, `identify_tech_debt` | grep for patterns |
| **Architecture** | `find_circular_deps`, `get_call_hierarchy`, `get_api_surface` | manual analysis |
| **Security** | `scan_for_secrets`, `check_permissions` | grep for patterns |
| **Performance** | `get_prisma_operations`, `profile_function`, `analyze_bundle` | none |
| **Documentation** | `explain_codebase`, `get_document_symbols` | file scan |
| **Testing** | `get_test_coverage`, `find_tests_for_file`, `suggest_test_cases` | jest --coverage |
| **Config** | `get_env_config`, `validate_env_complete`, `read_config` | env file scan |
| **Dependencies** | `analyze_dependencies` | npm audit |
| **Errors** | `get_diagnostics`, `parse_error_stack`, `explain_type_error` | tsc output |
| **Style** | `scan_patterns`, `get_conventions` | eslint output |

### Review Checklist

See `references/review-checklist.md` for complete 200+ item checklist.

**Minimum per category:**
- 5 specific file:line findings OR explicit "no issues found"
- Quantified measurements (counts, percentages, LOC)
- Severity classification (critical/high/medium/low)

---

## Phase 2: Master Report

Generate `codebase-review-report.md`:

```markdown
# Codebase Review Report

**Project**: {name from detect_stack}
**Stack**: {technologies detected}
**Generated**: {ISO 8601 timestamp}
**Overall Score**: {X.X}/10

## Executive Summary

| Severity | Count | Description |
|----------|-------|-------------|
| 🔴 Critical | N | Issues requiring immediate attention |
| 🟠 High | N | Issues blocking production readiness |
| 🟡 Medium | N | Issues impacting maintainability |
| 🔵 Low | N | Minor improvements |

## Score Breakdown

| Category | Weight | Raw | Deductions | Score | Grade |
|----------|--------|-----|------------|-------|-------|
| Quality | 15% | 10 | -X.X | X.X | A-F |
| Architecture | 15% | 10 | -X.X | X.X | A-F |
| Security | 20% | 10 | -X.X | X.X | A-F |
| Performance | 10% | 10 | -X.X | X.X | A-F |
| Documentation | 5% | 10 | -X.X | X.X | A-F |
| Testing | 15% | 10 | -X.X | X.X | A-F |
| Config | 5% | 10 | -X.X | X.X | A-F |
| Dependencies | 5% | 10 | -X.X | X.X | A-F |
| Errors | 5% | 10 | -X.X | X.X | A-F |
| Style | 5% | 10 | -X.X | X.X | A-F |
| **TOTAL** | 100% | - | - | **X.X** | **X** |

## Score Calculation

{Show the math for each category deduction}

## Detailed Findings

### {Category Name}

#### Finding: {Title}

| Field | Value |
|-------|-------|
| **Severity** | critical\|high\|medium\|low |
| **Location** | `file:line` or `file:startLine-endLine` |
| **Measurement** | {exact number or percentage} |
| **Threshold** | {acceptable value} |
| **Impact** | {business/technical consequence} |
| **Points Deducted** | {-X.X from Category} |

**Evidence:**
```
{code snippet or tool output}
```

**Required Fix:**
```
{specific remediation code or steps}
```

---

{repeat for all findings}

## What's Working Well

{List genuinely good patterns found, with file references}

## Improvement Roadmap

| Phase | Focus | Expected Impact | New Score |
|-------|-------|-----------------|-----------|
| 1 | Critical fixes | +X.X points | X.X |
| 2 | High priority | +X.X points | X.X |
| 3 | Medium priority | +X.X points | X.X |
| 4 | Polish | +X.X points | X.X |
```

---

## Phase 3: Remediation Plan

Generate `remediation-plan.md`:

```markdown
# Remediation Plan

**Generated**: {timestamp}
**Total Tasks**: {N}
**Execution Strategy**: Parallel goodvibes agents (max 6 concurrent)

## Execution Rules

| Rule | Value |
|------|-------|
| Max concurrent agents | 6 |
| Agent type | goodvibes background |
| Context model | Fresh per task (no accumulation) |
| Tool priority | MCP tools > bash |
| Monitoring | Self-report via SubagentStop hook |

## Task Definitions

### Wave 1: Critical [P0] - Execute Immediately

#### TASK-001: {Description}

| Field | Value |
|-------|-------|
| **Severity** | critical |
| **Target Files** | `file1.ts`, `file2.ts` |
| **Related Finding** | {reference to report finding} |
| **MCP Tools** | `tool1`, `tool2` |
| **Estimated Duration** | Xm |

**Agent Instructions:**
```
{specific instructions for this task}
```

---

{repeat for all tasks, grouped by wave}

### Wave 2: High [P1]

### Wave 3: Medium [P2]

### Wave 4: Low [P3]

## Dependency Graph

{Show task dependencies if any exist}
```

---

## Phase 4: Parallel Execution

### Agent Spawn Protocol

```python
# Pseudocode for orchestration
MAX_AGENTS = 6
active_agents = {}
task_queue = load_tasks("remediation-plan.md")

while task_queue or active_agents:
    # Spawn new agents up to limit
    while len(active_agents) < MAX_AGENTS and task_queue:
        task = task_queue.pop(0)
        
        agent_prompt = generate_agent_prompt(task)
        
        # Use Task tool to spawn background agent
        agent_id = Task(
            description=f"REMEDIATION: {task.id} - {task.description}",
            prompt=agent_prompt,
            background=True  # Critical: must be background
        )
        
        active_agents[task.id] = {
            "agent_id": agent_id,
            "started": now(),
            "task": task
        }
        
        log_task_start(task)
    
    # SubagentStop hook handles completion notifications
    # No polling required - hook updates remediation-log.md
```

### Agent Task Template

```markdown
# Goodvibes Remediation Agent

## MCP Tool Checklist (MANDATORY)

Before ANY edit:
```bash
mcp__plugin_goodvibes_goodvibes-tools__scan_patterns '{}'
mcp__plugin_goodvibes_goodvibes-tools__find_tests_for_file '{"file":"{TARGET}"}'
mcp__plugin_goodvibes_goodvibes-tools__validate_edits_preview '{}'
```

After EVERY edit:
```bash
mcp__plugin_goodvibes_goodvibes-tools__check_types '{}'
mcp__plugin_goodvibes_goodvibes-tools__get_diagnostics '{"file":"{EDITED}"}'
mcp__plugin_goodvibes_goodvibes-tools__run_smoke_test '{}'
```

## Assignment

| Field | Value |
|-------|-------|
| **Task ID** | {TASK_ID} |
| **Severity** | {SEVERITY} |
| **Description** | {DESCRIPTION} |
| **Target Files** | {FILE_LIST} |

## Context from Report

{RELEVANT_FINDING_DETAILS}

## Instructions

1. Complete ONLY this assigned task
2. Use goodvibes MCP tools BEFORE bash
3. Run validation tools after every edit  
4. If edit causes new errors, fix them before completing
5. Report completion with status

## Tool Priority (MANDATORY)

1. First: Check `mcp__plugin_goodvibes_goodvibes-tools__*`
2. Only then: Fall back to bash if no MCP tool exists

## Completion Report

When done, output:

```json
{
  "task_id": "{TASK_ID}",
  "status": "success|failed|partial",
  "files_modified": ["file1.ts", "file2.ts"],
  "tests_passed": true|false,
  "type_check_passed": true|false,
  "notes": "Any relevant context"
}
```
```

### Completion Logging

Maintain `remediation-log.md`:

```markdown
# Remediation Log

## Active Agents

| Task ID | Description | Agent | Started | Elapsed |
|---------|-------------|-------|---------|---------|
| TASK-002 | Remove secrets | agent-abc | 10:05:00 | 5m |

## Completed Tasks

| Task ID | Description | Status | Duration | Changes |
|---------|-------------|--------|----------|---------|
| TASK-001 | Fix SQL injection | ✅ success | 15m32s | `api/users.ts` |

## Failed Tasks

| Task ID | Description | Status | Reason | Retry? |
|---------|-------------|--------|--------|--------|
| TASK-005 | Fix auth flow | ❌ failed | Type errors | Yes |

## Summary

- **Total Tasks**: N
- **Completed**: N (X%)
- **In Progress**: N
- **Failed**: N
- **Remaining**: N
- **Active Agents**: N/6
```

---

## Tool Priority Enforcement

See `references/tool-priority.md` for complete reference.

### Quick Reference

| Need | Use This Tool | NOT This |
|------|---------------|----------|
| Type check | `check_types` | `tsc` directly |
| Find usages | `find_references` | grep |
| Rename symbol | `rename_symbol` | find-replace |
| Check diagnostics | `get_diagnostics` | compile errors |
| Dead code | `find_dead_code` | manual search |
| Circular deps | `find_circular_deps` | madge/deptree |
| Secrets scan | `scan_for_secrets` | grep for keys |
| Test coverage | `get_test_coverage` | jest --coverage |
| Bundle analysis | `analyze_bundle` | webpack-bundle-analyzer |

---

## Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max concurrent agents | 6 | Resource management |
| Agent type | goodvibes background | Telemetry via hooks |
| Tasks per agent | 1 | Fresh context per task |
| Context inheritance | None | Prevent cross-contamination |
| Monitoring method | Self-report | SubagentStop hook handles |
| Tool priority | MCP > bash | Consistency and telemetry |

---

## Memory Integration

After review/remediation, update `.goodvibes/memory/`:

| File | Update With |
|------|-------------|
| `decisions.md` | Architectural decisions made during remediation |
| `patterns.md` | Patterns discovered or enforced |
| `failures.md` | Failed remediations with root cause analysis |
| `preferences.md` | Tool preferences that worked well |

---

## Output Artifacts

| File | Purpose |
|------|---------|
| `codebase-review-report.md` | Complete findings with quantified metrics |
| `remediation-plan.md` | Prioritized task checklist by severity |
| `remediation-log.md` | Real-time execution tracking |
