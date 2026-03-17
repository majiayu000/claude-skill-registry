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

- **WRITE/EDIT/CREATE**: ONLY within the current working directory and its subdirectories. This is the project root. All changes must be git-trackable.
- **READ**: Can read any file anywhere for context (node_modules, global configs, other projects for reference, etc.)
- **NEVER WRITE** to: parent directories, home directory, system files, other projects, anything outside project root.

The working directory when you were spawned IS the project root. Stay within it for all modifications.

## MCP Tool Checklist (MANDATORY)

**STOP. Before doing ANYTHING, complete this checklist.**

**CRITICAL PREREQUISITE:** You MUST call `mcp-cli info <server>/<tool>` BEFORE ANY `mcp-cli call <server>/<tool>`. This is a BLOCKING REQUIREMENT.

### Task Start

```bash
# ALWAYS check schema first
mcp-cli info plugin_goodvibes_analysis-engine/detect_stack
mcp-cli info plugin_goodvibes_registry-engine/recommend_skills
mcp-cli info plugin_goodvibes_project-engine/project_issues

# Then make the calls
mcp-cli call plugin_goodvibes_analysis-engine/detect_stack '{}'
mcp-cli call plugin_goodvibes_registry-engine/recommend_skills '{"task":"codebase review quality audit"}'
mcp-cli call plugin_goodvibes_project-engine/project_issues '{}'
```

### Review Phase

```bash
# Check schemas first
mcp-cli info plugin_goodvibes_analysis-engine/find_circular_deps
mcp-cli info plugin_goodvibes_analysis-engine/scan_for_secrets
mcp-cli info plugin_goodvibes_project-engine/analyze_dependencies
mcp-cli info plugin_goodvibes_analysis-engine/find_dead_code
mcp-cli info plugin_goodvibes_project-engine/get_test_coverage

# Then execute
mcp-cli call plugin_goodvibes_analysis-engine/find_circular_deps '{}'
mcp-cli call plugin_goodvibes_analysis-engine/scan_for_secrets '{}'
mcp-cli call plugin_goodvibes_project-engine/analyze_dependencies '{}'
mcp-cli call plugin_goodvibes_analysis-engine/find_dead_code '{}'
mcp-cli call plugin_goodvibes_project-engine/get_test_coverage '{}'
```

### Before Every Edit

```bash
# Check schemas
mcp-cli info plugin_goodvibes_analysis-engine/scan_patterns
mcp-cli info plugin_goodvibes_project-engine/find_tests_for_file
mcp-cli info plugin_goodvibes_analysis-engine/validate_edits_preview

# Execute
mcp-cli call plugin_goodvibes_analysis-engine/scan_patterns '{}'
mcp-cli call plugin_goodvibes_project-engine/find_tests_for_file '{"file":"path/to/file.ts"}'
mcp-cli call plugin_goodvibes_analysis-engine/validate_edits_preview '{}'
```

### After Every Edit

```bash
# Check schema
mcp-cli info plugin_goodvibes_project-engine/project_issues

# Execute
mcp-cli call plugin_goodvibes_project-engine/project_issues '{}'
```

**THE LAW: If a goodvibes MCP tool can do it, USE THE TOOL. No exceptions.**

---

## Precision Tools (MANDATORY)

**CRITICAL: Use precision tools, NOT system tools.**

| Instead Of | Use | Why |
|------------|-----|-----|
| `Read` | `precision_read` | Extract modes, line ranges, outline/symbols |
| `Grep` | `precision_grep` | Output modes, batch queries, context control |
| `Glob` | `precision_glob` | Output modes, filters, preview |
| `Edit` | `precision_edit` | Atomic transactions, validation, hints |
| `Write` | `precision_write` | Atomic, templates, validation |
| `Bash` | `precision_exec` | Batch commands, expectations, output control |

### Precision Tool Patterns

```yaml
# Find files with pattern (minimal output)
precision_grep:
  queries:
    - pattern: "TODO|FIXME|HACK"
      glob: "src/**/*.ts"
  output:
    mode: files_only

# Read file structure without content
precision_read:
  files: ["src/index.ts", "src/app.ts"]
  extract: outline
  output:
    mode: minimal

# Batch edit multiple files atomically
precision_edit:
  edits:
    - file: "src/api.ts"
      find: "const API_URL = 'http://localhost'"
      replace: "const API_URL = process.env.API_URL"
    - file: "src/config.ts"
      find: "debug: true"
      replace: "debug: process.env.NODE_ENV !== 'production'"
  transaction:
    mode: atomic
    rollback_on_fail: true
  output:
    mode: minimal

# Execute commands with expectations
precision_exec:
  commands:
    - cmd: "npm run typecheck"
      expect:
        exit_code: 0
    - cmd: "npm run lint"
      expect:
        exit_code: 0
  output:
    mode: minimal
```

---

## Discovery -> Batch Workflow

**CRITICAL: Always discover before batching.**

The `discover` tool runs multiple queries in parallel to gather context before building a batch. This prevents wasted operations and ensures you target exactly the right files.

### Discovery Tool Usage

```yaml
# Run parallel discovery queries
discover:
  queries:
    - id: find_components
      type: glob
      patterns: ["src/components/**/*.tsx"]
    - id: find_api_routes
      type: glob
      patterns: ["src/api/**/*.ts", "src/app/api/**/*.ts"]
    - id: find_issues
      type: grep
      pattern: "TODO|FIXME|HACK"
      glob: "src/**/*.{ts,tsx}"
    - id: find_hooks
      type: symbols
      query: "use"
      kinds: ["function"]
  output_mode: files_only  # count_only | files_only | locations
```

### Workflow Pattern

1. **Discover** - Run queries to understand scope
   - Use `count_only` first to gauge magnitude
   - Then `files_only` to get target list

2. **Plan** - Build batch operations using discovery results
   - Reference discovered files in batch operations
   - Scope work to exactly what was found

3. **Execute** - Run batch with full context

### Example: Feature Implementation

```yaml
# Step 1: Discover current state
discover:
  queries:
    - id: existing_files
      type: glob
      patterns: ["src/features/auth/**/*.ts"]
    - id: existing_patterns
      type: grep
      pattern: "export (function|const|class)"
      glob: "src/features/**/*.ts"
  output_mode: files_only

# Step 2: Use results to build targeted batch
batch:
  id: implement-feature
  operations:
    read:
      - id: analyze
        type: files
        targets: "{{existing_files.files}}"  # From discovery
        extract: outline
```

**Benefits:**
- Prevents blind operations on wrong files
- Ensures consistent patterns across the codebase
- Reduces token usage by targeting exactly what's needed
- Enables informed decisions about implementation approach

---

## Mode-Aware Behavior

Your behavior adapts based on the current mode:

### vibecoding Mode
- **Communicate**: Show progress, explain decisions, report results in detail
- **Ask**: On ambiguity or risk, ask the user before proceeding
- **Checkpoint**: Create checkpoints per batch
- **Output**: Standard verbosity, show diffs

### justvibes Mode
- **Silent**: Minimal communication, log to `.goodvibes/logs/activity.md`
- **Autonomous**: Make best-guess decisions, proceed with checkpoints on risk
- **Auto-chain**: Continue to next logical batch automatically
- **Output**: Minimal verbosity, no diffs

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      CODEBASE REVIEW                        │
├─────────────────────────────────────────────────────────────┤
│  Phase 1: Review      │  Run MCP tools, analyze all code   │
│  Phase 2: Report      │  Generate codebase-review-report.md │
│  Phase 3: Plan        │  Create remediation-plan.md        │
│  Phase 4: Execute     │  WORK-REVIEW-FIX-CHECK (max 6)     │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Codebase Review

### MCP Tool Mapping

| Category | Primary Tools | Fallback |
|----------|---------------|----------|
| **Quality** | `find_dead_code`, `scan_patterns` | grep for patterns |
| **Architecture** | `find_circular_deps`, `get_api_surface` | manual analysis |
| **Security** | `scan_for_secrets`, `check_permissions` | grep for patterns |
| **Performance** | `get_prisma_operations`, `analyze_bundle` | none |
| **Documentation** | `explain_codebase` | file scan |
| **Testing** | `get_test_coverage`, `find_tests_for_file`, `suggest_test_cases` | jest --coverage |
| **Config** | `read_config`, `env_audit` | env file scan |
| **Dependencies** | `analyze_dependencies` | npm audit |
| **Errors** | `parse_error_stack`, `explain_type_error` | tsc output |
| **Style** | `scan_patterns`, `get_conventions` | eslint output |

### Review Checklist

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
**Execution Strategy**: WORK-REVIEW-FIX-CHECK with parallel goodvibes agents (max 6 concurrent)

## Execution Rules

| Rule | Value |
|------|-------|
| Max concurrent agents | 6 |
| Agent type | goodvibes background |
| Context model | Fresh per task (no accumulation) |
| Tool priority | MCP tools > bash |
| Monitoring | Self-report via SubagentStop hook |
| Workflow | WORK → REVIEW → PASS/FAIL → (FIX → CHECK) |

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

**Context from Report:**
```
{relevant finding details}
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

## Phase 4: Parallel Agent Execution

### WORK-REVIEW-FIX-CHECK Workflow

```
For each remediation task:

  WORK Agent ─────────────────────> REVIEW Agent
  (goodvibes:engineer)              (goodvibes:reviewer)
       │                                  │
       │                                  ├─> PASS ─> Commit ─> Update Log ─> Next Task
       │                                  │
       │                                  └─> FAIL ─> FIX Agent ─> CHECK Agent
                                                         │              │
                                                         │              ├─> PASS ─> Commit
                                                         │              │
                                                         └──────────────┴─> FAIL (loop)
```

### Agent Role Mapping

| Phase | Agent | Purpose |
|-------|-------|---------|
| WORK | `goodvibes:engineer` | Implements remediation task |
| REVIEW | `goodvibes:reviewer` | Verifies work quality (100% required) |
| FIX | `goodvibes:engineer` | Addresses ALL review issues |
| CHECK | `goodvibes:reviewer` | Re-verifies fixes |

### Waiting for Agents (CRITICAL)

**NEVER use these to check agent status:**
- `tail` command on transcript files
- `TaskOutput` tool
- Any form of polling

**INSTEAD, the orchestrator:**
1. Spawns agent with `run_in_background: true`
2. Stops taking actions (turn ends)
3. Receives SubagentStop hook notification when agent completes
4. Hook message appears in context with status

### Concurrency Rules

| Rule | Value |
|------|-------|
| Max concurrent agents | 6 |
| Agents per task | 1 (one agent works on a task at a time) |
| Completion requirement | 100% (not 99.9%) |

---

### WORK Agent Prompt Template

```markdown
# Remediation Task: {TASK_ID}

## MCP Tool Checklist (MANDATORY)

**CRITICAL PREREQUISITE:** You MUST call `mcp-cli info <server>/<tool>` BEFORE ANY `mcp-cli call <server>/<tool>`.

Before ANY edit:
```bash
# Check schemas first
mcp-cli info plugin_goodvibes_analysis-engine/scan_patterns
mcp-cli info plugin_goodvibes_project-engine/find_tests_for_file

# Then execute
mcp-cli call plugin_goodvibes_analysis-engine/scan_patterns '{}'
mcp-cli call plugin_goodvibes_project-engine/find_tests_for_file '{"file":"{TARGET_FILE}"}'
```

After EVERY edit:
```bash
# Check schema first
mcp-cli info plugin_goodvibes_project-engine/project_issues

# Then execute
mcp-cli call plugin_goodvibes_project-engine/project_issues '{}'
```

## Assignment

| Field | Value |
|-------|-------|
| Task ID | {TASK_ID} |
| Severity | {SEVERITY} |
| Description | {DESCRIPTION} |
| Files | {FILE_LIST} |

## Context from Report

{FINDING_DETAILS}

## Instructions

1. Complete ONLY this assigned task
2. Use goodvibes MCP tools BEFORE bash
3. Use precision tools (precision_edit, precision_exec) for all operations
4. Run validation tools after every edit
5. If edit causes new errors, fix them before completing

## Tool Priority (MANDATORY)

1. First: Check `mcp-cli info` then `mcp-cli call plugin_goodvibes_*`
2. Second: Use precision tools (precision_edit, precision_read, etc.)
3. Only then: Fall back to standard tools if no MCP/precision tool exists

## Completion Report

When done, output:

```json
{
  "task_id": "{TASK_ID}",
  "status": "success|failed",
  "files_modified": ["file1.ts", "file2.ts"],
  "tests_passed": true|false,
  "type_check_passed": true|false,
  "notes": "Any relevant context"
}
```
```

---

### REVIEW Agent Prompt Template

```markdown
# Review Task: {TASK_ID}

## MCP Tool Checklist (MANDATORY)

**CRITICAL PREREQUISITE:** You MUST call `mcp-cli info <server>/<tool>` BEFORE ANY `mcp-cli call <server>/<tool>`.

```bash
# Check schemas first
mcp-cli info plugin_goodvibes_project-engine/project_issues
mcp-cli info plugin_goodvibes_analysis-engine/scan_patterns
mcp-cli info plugin_goodvibes_project-engine/get_test_coverage

# Then execute
mcp-cli call plugin_goodvibes_project-engine/project_issues '{}'
mcp-cli call plugin_goodvibes_analysis-engine/scan_patterns '{}'
mcp-cli call plugin_goodvibes_project-engine/get_test_coverage '{}'
```

## Assignment

| Field | Value |
|-------|-------|
| Task ID | {TASK_ID} |
| Work Agent | {WORK_AGENT_ID} |
| Files Modified | {FILE_LIST} |

## Context from WORK Agent

{WORK_COMPLETION_REPORT}

## Review Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Correctness | 30% | Does it solve the problem correctly? |
| Completeness | 25% | Are all aspects addressed? |
| Quality | 20% | Is the code clean, maintainable? |
| Safety | 15% | No new errors, security issues? |
| Tests | 10% | Tests pass, coverage maintained? |

## Review Process

1. Read all modified files
2. Run MCP validation tools
3. Check for:
   - Type errors
   - Test failures
   - Security issues
   - Code quality issues
   - Incomplete fixes
4. Calculate score based on criteria weights
5. Provide verdict

## Review Output

```json
{
  "task_id": "{TASK_ID}",
  "verdict": "PASS|FAIL",
  "score": 8.5,
  "issues": [
    {
      "severity": "critical|major|minor",
      "file": "path/to/file.ts",
      "line": 47,
      "issue": "Description of the issue",
      "fix_guidance": "Specific guidance on how to fix"
    }
  ],
  "recommendation": "Details for FIX agent if FAIL"
}
```

## Verdict Rules

- **PASS**: Score >= 8.0 AND no critical issues AND all criteria pass
- **FAIL**: Score < 8.0 OR any critical issue OR any criterion fails

**CRITICAL: Be honest. Better to catch issues now than in production.**
```

---

### FIX Agent Prompt Template

```markdown
# Fix Task: {TASK_ID} (Iteration {N})

## MCP Tool Checklist (MANDATORY)

**CRITICAL PREREQUISITE:** You MUST call `mcp-cli info <server>/<tool>` BEFORE ANY `mcp-cli call <server>/<tool>`.

Before ANY edit:
```bash
# Check schemas first
mcp-cli info plugin_goodvibes_analysis-engine/scan_patterns
mcp-cli info plugin_goodvibes_project-engine/find_tests_for_file

# Then execute
mcp-cli call plugin_goodvibes_analysis-engine/scan_patterns '{}'
mcp-cli call plugin_goodvibes_project-engine/find_tests_for_file '{"file":"{TARGET_FILE}"}'
```

After EVERY edit:
```bash
# Check schema first
mcp-cli info plugin_goodvibes_project-engine/project_issues

# Then execute
mcp-cli call plugin_goodvibes_project-engine/project_issues '{}'
```

## Review Feedback

{ISSUES_FROM_REVIEW}

## Instructions

1. Address EVERY issue from the review - no skipping
2. Follow the `fix_guidance` provided for each issue
3. Use precision tools for all operations
4. Run validation after each fix
5. If you cannot fix an issue, document WHY and mark as blocked

## Completion Report

```json
{
  "task_id": "{TASK_ID}",
  "iteration": {N},
  "status": "success|blocked",
  "issues_addressed": N,
  "issues_remaining": N,
  "blocked_issues": [
    {
      "issue": "Description",
      "reason": "Why it cannot be fixed"
    }
  ],
  "notes": "Any relevant context"
}
```
```

---

### CHECK Agent Prompt Template

```markdown
# Check Task: {TASK_ID} (Verification Round {N})

## MCP Tool Checklist (MANDATORY)

**CRITICAL PREREQUISITE:** You MUST call `mcp-cli info <server>/<tool>` BEFORE ANY `mcp-cli call <server>/<tool>`.

```bash
# Check schemas first
mcp-cli info plugin_goodvibes_project-engine/project_issues
mcp-cli info plugin_goodvibes_analysis-engine/scan_patterns

# Then execute
mcp-cli call plugin_goodvibes_project-engine/project_issues '{}'
mcp-cli call plugin_goodvibes_analysis-engine/scan_patterns '{}'
```

## Assignment

| Field | Value |
|-------|-------|
| Task ID | {TASK_ID} |
| FIX Agent | {FIX_AGENT_ID} |
| Iteration | {N} |

## Previous Issues

{ISSUES_TO_VERIFY}

## Context from FIX Agent

{FIX_COMPLETION_REPORT}

## Verification Process

1. Read all modified files
2. Run MCP validation tools
3. Verify each previous issue is resolved
4. Check for new issues introduced by fixes
5. Provide verdict

## Verdict Output

```json
{
  "task_id": "{TASK_ID}",
  "iteration": {N},
  "verdict": "PASS|FAIL",
  "resolved_issues": N,
  "unresolved_issues": [
    {
      "issue": "Description",
      "status": "still_present|new_issue"
    }
  ],
  "recommendation": "Next action if FAIL"
}
```

## Verdict Rules

- **PASS**: ALL previous issues resolved AND no new critical issues
- **FAIL**: ANY issue unresolved OR new critical issues found

**If FAIL after 3 iterations, escalate to human review.**
```

---

### Commit Protocol

After REVIEW or CHECK verdict is PASS, create commit:

```
fix({CATEGORY}): {TASK_ID} - {SHORT_DESCRIPTION}

{DETAILED_DESCRIPTION}

## Changes
- {FILE_1}: {WHAT_CHANGED}
- {FILE_2}: {WHAT_CHANGED}

## Review
- Reviewed by: REVIEW agent
- Score: {SCORE}/10
- Iterations: {FIX_ITERATIONS}

Task-ID: {TASK_ID}
Severity: {SEVERITY}
Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

### Completion Cleanup

After ALL remediation tasks have passed review and been committed, archive the output files:

**Archive Location:** `.goodvibes/completed/`

**Archive Commands:**
```bash
# Run all commands together in a single shell session:
# Create archive directory if it doesn't exist
mkdir -p .goodvibes/completed

# Generate timestamp
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# Move and rename files
mv codebase-review-report.md .goodvibes/completed/code-review-${TIMESTAMP}.md
mv remediation-plan.md .goodvibes/completed/remediation-plan-${TIMESTAMP}.md
mv remediation-log.md .goodvibes/completed/remediation-log-${TIMESTAMP}.md
```

**Archive Checklist:**
- [ ] All remediation tasks show status: completed in remediation-log.md
- [ ] All commits pushed (if applicable)
- [ ] Memory files updated (.goodvibes/memory/)
- [ ] Archive directory created
- [ ] Files moved with timestamp suffix

**File Naming Convention:**
| Original | Archived |
|----------|----------|
| `codebase-review-report.md` | `code-review-{YYYYMMDD-HHMMSS}.md` |
| `remediation-plan.md` | `remediation-plan-{YYYYMMDD-HHMMSS}.md` |
| `remediation-log.md` | `remediation-log-{YYYYMMDD-HHMMSS}.md` |

**Why Archive:**
- Keeps project root clean
- Preserves historical review data
- Enables tracking of codebase health over time
- Prevents confusion with future reviews

### Completion Logging

Maintain `remediation-log.md`:

```markdown
# Remediation Log

## Active Agents

| Task ID | Description | Agent | Phase | Started | Elapsed |
|---------|-------------|-------|-------|---------|---------|
| TASK-002 | Remove secrets | agent-abc | WORK | 10:05:00 | 5m |
| TASK-003 | Fix auth flow | agent-def | REVIEW | 10:08:00 | 2m |

## Completed Tasks

| Task ID | Description | Status | Duration | Iterations | Changes |
|---------|-------------|--------|----------|------------|---------|
| TASK-001 | Fix SQL injection | ✅ PASS | 15m32s | 1 | `api/users.ts` |

## Failed Tasks

| Task ID | Description | Status | Iterations | Reason | Retry? |
|---------|-------------|--------|------------|--------|--------|
| TASK-005 | Fix type errors | ❌ FAIL | 3 | Blocked by external dependency | No |

## Summary

- **Total Tasks**: N
- **Completed**: N (X%)
- **In Progress**: N
- **Failed**: N
- **Remaining**: N
- **Active Agents**: N/6
```

---

## Output Artifacts

| File | Purpose |
|------|---------|
| `codebase-review-report.md` | Complete findings with quantified metrics and scores |
| `remediation-plan.md` | Prioritized task checklist by severity with context |
| `remediation-log.md` | Real-time execution tracking with WORK-REVIEW-FIX-CHECK status |

**Note:** After all remediation tasks are completed, these files are archived to `.goodvibes/completed/` with timestamp suffixes. See "Completion Cleanup" section for details.

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

## Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max concurrent agents | 6 | Resource management |
| Agent type | goodvibes background | Telemetry via hooks |
| Tasks per agent | 1 | Fresh context per task |
| Context inheritance | None | Prevent cross-contamination |
| Monitoring method | Self-report | SubagentStop hook handles |
| Tool priority | MCP > precision > bash | Consistency and telemetry |
| Review requirement | 100% | Ensure quality before commit |
