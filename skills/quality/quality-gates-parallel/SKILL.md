---
# VERSION: 1.0.0 (Native Multi-Agent Integration)
name: quality-gates-parallel
description: Launch 4 quality subagents in parallel using Claude Code 2.1+ native Task tool. Reads results post-analysis for orchestrator decision-making.
allowed-tools: TaskCreate, TaskUpdate, TaskList, TaskGet, Read, Write, Bash
---

# Quality Gates Parallel (Native Multi-Agent)

Orchestrator integration for launching 4 quality subagents in parallel using Claude Code 2.1+ native Task tool with **teammate coordination**.

## Quick Start

```bash
# Launch quality checks after implementation
/quality-gates-parallel src/auth.ts --complexity 7

# Read aggregated results post-analysis
/quality-gates-parallel --read-results <run_id>
```

## Native Multi-Agent Architecture (Claude Code 2.1.16+)

Based on: [claude-sneakpeek native-multiagent-gates](https://github.com/mikekelly/claude-sneakpeek/blob/main/docs/research/native-multiagent-gates.md)

### Features Available

- **TaskCreate**: Create tasks for subagents
- **TaskUpdate**: Update task status
- **TaskList**: List all tasks
- **TaskGet**: Get task details
- **Parallel execution**: Multiple agents work independently
- **Result aggregation**: Collect findings from all agents

## Workflow

### Phase 1: Launch Parallel Quality Checks

After implementation (orchestrator step 6b), launch 4 subagents:

```javascript
// Pseudo-code for orchestrator integration
1. Classify task complexity (1-10)
2. If complexity >= 5:
3.    Create 4 tasks using TaskCreate:
4.      - Security auditor (sec-context-depth)
5.      - Code reviewer (code-reviewer)
6.      - Code cleanup (deslop)
7.      - Prose cleanup (stop-slop)
8.    Tasks execute in parallel (non-blocking)
9.    Continue orchestrator workflow
10. Else: Skip quality checks (low complexity)
```

### Phase 2: Read Results (Pre-Validation)

Before validation (orchestrator step 7), poll for results:

```bash
# Run results reader
.claude/scripts/read-quality-results.sh <run_id>
```

### Phase 3: Orchestrator Decision-Making

Orchestrator reads aggregated results and decides:

```javascript
// Pseudo-code for decision logic
results = readQualityResults(run_id)

if (results.total_findings == 0) {
    // No issues - proceed to validation
    proceedToValidation()
} else if (results.critical_findings > 0) {
    // Critical issues - block and fix
    blockMerge()
    requireFixes()
} else {
    // Minor issues - advisory only
    proceedWithWarnings()
}
```

## Quality Agents (4 Parallel)

### 1. Security Auditor (`sec-context-depth`)

**Agent**: `security-auditor` or `glm-reviewer`
**Purpose**: 27 security anti-patterns (OWASP/CWE)
**Findings**: P0 (Critical), P1 (High), P2 (Medium)
**Command**: `/sec-context-depth <file>`

**Coverage**:
- 86% XSS failure rate detection
- 72% Java AI code vulnerability detection
- SQL injection, command injection, XSS
- JWT none algorithm, weak hashing, ECB mode

### 2. Code Reviewer (`code-reviewer`)

**Agent**: `code-reviewer` or `codex-cli`
**Purpose**: Official Claude Code plugin with 4 parallel agents
**Features**: Confidence scoring (≥80 threshold)
**Command**: `/code-review <file>`

**Architecture**:
- Agent #1: CLAUDE.md compliance
- Agent #2: CLAUDE.md compliance (redundancy)
- Agent #3: Bug detection (changes only)
- Agent #4: Git blame/history analysis

### 3. Code Cleanup (`deslop`)

**Agent**: `refactorer` or `gemini-cli`
**Purpose**: Remove AI-generated code slop
**Command**: `/deslop`

**Removes**:
- Extra comments inconsistent with codebase
- Extra defensive checks/try/catch blocks
- Casts to `any` for type issues
- Inline imports (move to top)

### 4. Prose Cleanup (`stop-slop`)

**Agent**: `docs-writer` or `minimax`
**Purpose**: Remove AI writing patterns from prose
**Command**: `/stop-slop <file>`

**Removes**:
- Filler phrases ("Certainly!", "It is important to note")
- Structural clichés (binary contrasts, dramatic fragmentation)
- Stylistic habits (tripling, metronomic endings)

## Integration with Orchestrator

### Step 6b.5: Quality Parallel (NEW)

**Location**: After implementation (6b), before validation (7)

**Trigger**: `complexity >= 5` OR security-related code

**Execution**:
```bash
# Non-blocking parallel launch
.claude/scripts/quality-coordinator.sh <target_file> <complexity>
```

**Output**: JSON with 4 task definitions

### Step 7: Validation with Quality Results

**Before validation**: Read aggregated results

```bash
# Poll for completed checks
.claude/scripts/read-quality-results.sh <run_id>
```

**Output**: Aggregated JSON with all findings

**Decision Logic**:
- 0 findings: Proceed to validation
- Critical findings: Block and require fixes
- Minor findings: Advisory warnings

## Results Storage

```
.claude/quality-results/
├── aggregated_<run_id>.json        # Aggregated results
├── sec-context_<run_id>.json       # Security findings
├── code-review_<run_id>.json       # Code review findings
├── deslop_<run_id>.json            # Code cleanup findings
├── stop-slop_<run_id>.json         # Prose cleanup findings
├── *_<run_id>.done                 # Completion markers
└── coordinator.log                # Execution log
```

## Usage Examples

### Manual Execution

```bash
# Launch quality checks
./.claude/scripts/quality-coordinator.sh src/auth.ts 7

# Read results
./.claude/scripts/read-quality-results.sh 20250128_221437_12345
```

### Orchestrator Integration

```bash
# In orchestrator step 6b (after implementation)
quality_check_result=$(./.claude/scripts/quality-coordinator.sh "$file" "$complexity")

# Parse result and create tasks
if [[ "$complexity" -ge 5 ]]; then
    # Create 4 tasks using TaskCreate
    # Tasks execute in parallel
    # Store run_id for later retrieval
fi

# In orchestrator step 7 (before validation)
quality_results=$(./.claude/scripts/read-quality-results.sh "$run_id")

# Parse results and make decision
critical_count=$(echo "$quality_results" | jq '.summary.critical_findings // 0')
if [[ "$critical_count" -gt 0 ]]; then
    # Block and require fixes
    echo "CRITICAL: $critical_count security issues found"
else
    # Proceed to validation
    echo "No critical issues, proceeding to validation"
fi
```

## Scripts

- **quality-coordinator.sh**: Launch 4 quality tasks in parallel
- **read-quality-results.sh**: Poll and aggregate results

## Hooks

- **quality-parallel-async.sh**: Async hook for Edit/Write operations
  - Uses `async: true` in settings.json
  - Non-blocking background execution
  - Results stored for later reading

## Version History

- **1.0.0** (2026-01-28): Initial native multi-agent integration
  - Based on Claude Code 2.1.16+ Task tool
  - 4 parallel quality agents
  - Result aggregation and polling

## References

- Native Multi-Agent Gates: [claude-sneakpeek documentation](https://github.com/mikekelly/claude-sneakpeek/blob/main/docs/research/native-multiagent-gates.md)
- Claude Code 2.1.16+ features: Swarms, TeammateTool, teammate coordination
- Quality consolidation: `docs/analysis/QUALITY_PARALLEL_CONSOLIDATION_v2.80.3.md`
- Async hooks correction: `docs/analysis/ASYNC_HOOKS_CORRECTION_v2.80.2.md`
