---
name: codex-audit
description: Use Codex CLI for sandboxed auditing, debugging, and autonomous prototyping
allowed-tools: Bash, Read, Write, TodoWrite, Glob, Grep
---

# Codex Audit Skill



---

## LIBRARY-FIRST PROTOCOL (MANDATORY)

**Before writing ANY code, you MUST check:**

### Step 1: Library Catalog
- Location: `.claude/library/catalog.json`
- If match >70%: REUSE or ADAPT

### Step 2: Patterns Guide
- Location: `.claude/docs/inventories/LIBRARY-PATTERNS-GUIDE.md`
- If pattern exists: FOLLOW documented approach

### Step 3: Existing Projects
- Location: `D:\Projects\*`
- If found: EXTRACT and adapt

### Decision Matrix
| Match | Action |
|-------|--------|
| Library >90% | REUSE directly |
| Library 70-90% | ADAPT minimally |
| Pattern exists | FOLLOW pattern |
| In project | EXTRACT |
| No match | BUILD (add to library after) |

---

## Purpose

Route auditing and debugging tasks to Codex CLI when:
- Autonomous iteration is needed (test-fix-retest loops)
- Sandboxed execution required for safety
- Rapid prototyping without approval overhead

## Unique Capability

**What Codex Does Better**:
- Fully autonomous execution (no approval needed mid-task)
- Sandboxed isolation (no network, CWD only)
- Iterative debugging loops
- GPT-5-Codex optimized for agentic coding

## When to Use

### Perfect For:
- Automated test fixing
- Code auditing in isolation
- Rapid prototyping of features
- Refactoring with test verification
- Build failure recovery
- Security scanning in sandbox

### Don't Use When:
- Need network access (sandbox disables it)
- Need to access files outside CWD
- Production debugging (use Claude with oversight)
- Complex multi-file coordination

## Usage

### Basic Audit
```bash
/codex-audit "Find and fix all type errors" --context src/
```

### Test Fixing
```bash
/codex-audit "Fix failing tests" --context tests/ --max-iterations 10
```

### Prototyping
```bash
/codex-audit "Build REST API with CRUD endpoints" --context .
```

## Command Pattern

```bash
bash scripts/multi-model/codex-audit.sh "<task>" "<context>" "<task_id>" "<max_iterations>"
```

## Safety Constraints

| Constraint | Value |
|------------|-------|
| Network | DISABLED |
| File Access | CWD only |
| Isolation | macOS Seatbelt / Docker |
| Max Iterations | 5 (configurable) |

## Memory Integration

Results stored to Memory-MCP:
- Key: `multi-model/codex/audit/{task_id}`
- Tags: WHO=codex-cli, WHY=audit

## Output Format

```json
{
  "raw_output": "Audit findings...",
  "metrics": {
    "files_analyzed": 15,
    "findings_count": 7,
    "fixes_applied": 5
  },
  "context_path": "src/",
  "sandbox_mode": true
}
```

## Handoff to Claude

After Codex audit completes:
1. Findings stored in Memory-MCP
2. Claude agents review findings
3. Apply or escalate based on severity

```javascript
// Claude agent reads Codex audit
const audit = memory_retrieve("multi-model/codex/audit/{task_id}");
if (audit.metrics.findings_count > 0) {
  Task("Reviewer", `Review findings: ${audit.raw_output}`, "reviewer");
}
```

## Integration with Audit Pipeline

```bash
# Phase 1: Theater detection (Claude)
/theater-detection-audit

# Phase 2: Functionality audit (Codex)
/codex-audit "Verify all functions work" --context src/

# Phase 3: Style audit (Claude)
/style-audit
```
