---
# VERSION: 2.88.0
name: bugs
description: "Bug hunting with Codex CLI Use when: (1) /bugs is invoked, (2) task relates to bugs functionality."
context: fork
user-invocable: true
allowed-tools:
  - LSP
  - Read
  - Bash
  - Grep
  - Glob
hooks:
  PreToolUse:
    - path: .claude/hooks/validate-lsp-servers.sh
      match_tool: LSP
---

# /bugs (v2.37)

Deep bug analysis using Codex gpt-5.2-codex with the bug-hunter skill and **TLDR context optimization**.

## v2.88 Key Changes (MODEL-AGNOSTIC)

- **Model-agnostic**: Uses model configured in `~/.claude/settings.json` or CLI/env vars
- **No flags required**: Works with the configured default model
- **Flexible**: Works with GLM-5, Claude, Minimax, or any configured model
- **Settings-driven**: Model selection via `ANTHROPIC_DEFAULT_*_MODEL` env vars

## Agent Teams Integration (v2.88)

**Optimal Scenario**: Pure Custom Subagents

This skill uses Pure Custom Subagents (no Agent Teams) for specialized, focused bug analysis.

### Why Scenario B for Bug Hunting
- **Specialized task**: Bug analysis is a focused, single-purpose operation
- **Less coordination needed**: Direct spawn faster than team creation for single-file analysis
- **Tool restrictions important**: ralph-reviewer restricted to Read/Grep/Glob prevents accidental modifications
- **Scalable pattern**: For large codebases, spawn multiple reviewers directly without team overhead

### Configuration
1. **No TeamCreate**: Skip team creation overhead for faster execution
2. **Direct Task**: Spawn ralph-reviewer agents directly with analysis prompts
3. **Tool Restrictions**: Leverage per-agent tool limits (Read/Grep/Glob only for reviewers)
4. **Model Inheritance**: Use model configured in settings.json

### Workflow Pattern
```
Task(subagent_type="ralph-reviewer", prompt="Analyze $TARGET for bugs...")
  → Agent executes with restricted tools (no Write/Edit)
  → Returns structured bug findings
  → Complete (no team cleanup needed)
```

### For Large Codebases (Parallel Scanning)
When analyzing directories with many files:
```bash
# Spawn multiple reviewers in parallel (no team needed)
Task(subagent_type="ralph-reviewer", prompt="Analyze files 1-10...")
Task(subagent_type="ralph-reviewer", prompt="Analyze files 11-20...")
Task(subagent_type="ralph-reviewer", prompt="Analyze files 21-30...")

# Aggregate results manually or via simple script
```

### When NOT to Use Agent Teams
- Single-file bug analysis (most common case)
- Quick scans without multi-phase coordination
- When tool restrictions (no Write/Edit) are more important than coordination
- When team creation overhead exceeds analysis time

## Pre-Bugs: TLDR Context Preparation (v2.37)

**AUTOMATIC** - Before bug hunting, gather context with 95% token savings:

```bash
# Get function signatures and call flow
tldr context "$TARGET_FILE" . > /tmp/bugs-context.md

# Get dependency graph for tracking bug propagation
tldr deps "$TARGET_FILE" . > /tmp/bugs-deps.md

# Get codebase structure for understanding module relationships
tldr structure . > /tmp/bugs-structure.md

# Semantic search for error handling patterns
tldr semantic "try catch error exception throw" .
```

## Overview

The `/bugs` command performs comprehensive static analysis using **TLDR-compressed context** to identify potential bugs, logic errors, race conditions, edge cases, and other code issues that could cause runtime failures or unexpected behavior. It uses Codex GPT-5.2 model with specialized bug-hunting capabilities to analyze code paths, detect anti-patterns, and suggest fixes.

Unlike traditional linters, Codex bug hunting performs deep semantic analysis:
- **Context-aware**: Understands code intent and business logic
- **Multi-file analysis**: Traces bugs across module boundaries
- **Pattern recognition**: Identifies common bug patterns and anti-patterns
- **Fix suggestions**: Provides actionable remediation steps

## When to Use

Use `/bugs` when:
- Investigating mysterious test failures or production issues
- Auditing newly merged code for potential issues
- Debugging complex interactions between modules
- Preparing critical code paths for production deployment
- Reviewing legacy code for modernization
- Searching for edge cases before stress testing
- Performing pre-merge quality checks (complexity >= 7)

## Analysis Methodology

Codex bug hunting follows a systematic approach:

1. **Static Analysis**: Parse AST and control flow graphs
2. **Pattern Matching**: Compare against known bug patterns database
3. **Semantic Understanding**: Analyze code intent and data flow
4. **Edge Case Detection**: Identify boundary conditions and error paths
5. **Severity Assessment**: Classify bugs by impact and probability
6. **Fix Generation**: Propose concrete remediation steps

### Bug Categories

| Category | Examples | Severity |
|----------|----------|----------|
| **Logic Errors** | Off-by-one, incorrect conditions, wrong operators | HIGH |
| **Race Conditions** | Unprotected shared state, TOCTOU bugs | HIGH |
| **Memory Issues** | Leaks, use-after-free, buffer overflows | CRITICAL |
| **Type Errors** | Implicit conversions, type coercion bugs | MEDIUM |
| **Error Handling** | Uncaught exceptions, missing null checks | HIGH |
| **Edge Cases** | Empty arrays, boundary values, overflow | MEDIUM |
| **Async Issues** | Unhandled promises, callback hell, deadlocks | HIGH |
| **Security Bugs** | Injection, XSS, CSRF (see /security for full audit) | CRITICAL |

## CLI Execution

```bash
# Bug hunt on specific file
ralph bugs src/auth/login.ts

# Bug hunt on directory
ralph bugs src/components/

# Bug hunt on entire codebase
ralph bugs .

# Background execution with logging
ralph bugs src/ > bugs-report.json 2>&1 &
```

## Task Tool Invocation (TLDR-Enhanced)

Use the Task tool to invoke Codex bug hunting with TLDR context:

```yaml
Task:
  subagent_type: "debugger"
  model: "sonnet"
  run_in_background: true
  description: "Codex bug hunting analysis"
  prompt: |
    # Context (95% token savings via tldr)
    Structure: $(tldr structure .)
    File Context: $(tldr context $ARGUMENTS .)
    Dependencies: $(tldr deps $ARGUMENTS .)

    Execute Codex bug hunting via CLI:
    cd /Users/alfredolopez/Documents/GitHub/multi-agent-ralph-loop && \
    codex exec --yolo --enable-skills -m gpt-5.2-codex \
    "Use bug-hunter skill. Find bugs in: $ARGUMENTS

    Output JSON: {
      bugs: [
        {
          severity: 'CRITICAL|HIGH|MEDIUM|LOW',
          type: 'logic|race|memory|type|error-handling|edge-case|async|security',
          file: 'path/to/file.ts',
          line: 42,
          description: 'Clear bug description',
          fix: 'Concrete remediation steps'
        }
      ],
      summary: {
        total: 5,
        high: 2,
        medium: 2,
        low: 1,
        approved: false
      }
    }"

    Apply Ralph Loop: iterate until all HIGH+ bugs are resolved or approved.
```

### Direct Codex Execution

For immediate results without Task orchestration:

```bash
codex exec --yolo --enable-skills -m gpt-5.2-codex \
  "Use bug-hunter skill. Find bugs in: src/

  Focus on:
  - Race conditions in async code
  - Uncaught promise rejections
  - Type coercion issues
  - Edge case handling

  Output JSON with severity, type, file, line, description, fix"
```

## Output Format

The bug hunting analysis returns structured JSON:

```json
{
  "bugs": [
    {
      "severity": "HIGH",
      "type": "race",
      "file": "src/auth/session.ts",
      "line": 87,
      "description": "Race condition: session.user accessed before async initialization completes",
      "fix": "Add await before accessing session.user, or use Promise.all() to ensure initialization"
    },
    {
      "severity": "MEDIUM",
      "type": "edge-case",
      "file": "src/utils/parser.ts",
      "line": 23,
      "description": "Empty array not handled: arr[0] will throw if arr is empty",
      "fix": "Add guard: if (arr.length === 0) return null; before accessing arr[0]"
    }
  ],
  "summary": {
    "total": 2,
    "high": 1,
    "medium": 1,
    "low": 0,
    "approved": false
  }
}
```

### Severity Levels

| Severity | Meaning | Action |
|----------|---------|--------|
| **CRITICAL** | Production-breaking, security issues | MUST FIX before merge |
| **HIGH** | Likely to cause failures, data corruption | SHOULD FIX before merge |
| **MEDIUM** | Edge cases, potential issues under load | Review and decide |
| **LOW** | Code smells, minor improvements | Optional fix |

## Integration

The `/bugs` command integrates with other Ralph workflows:

### With @debugger Agent

```yaml
Task:
  subagent_type: "debugger"
  model: "opus"  # Opus for deep analysis
  description: "Full debugging workflow"
  prompt: |
    1. Run /bugs on $TARGET
    2. Analyze top 5 HIGH severity bugs
    3. Trace execution paths to root cause
    4. Propose fixes with test cases
    5. Validate fixes pass quality gates
```

### With /adversarial

When a bug fix needs a clarified spec:

```bash
# Step 1: Bug hunting
ralph bugs src/payment/

# Step 2: Draft a short spec for the fix
ralph adversarial "Draft: Fix payment retry logic with idempotency"
```

### With /unit-tests

Generate tests that specifically target discovered bugs:

```yaml
Task:
  subagent_type: "test-architect"
  model: "sonnet"
  prompt: |
    Read bugs-report.json
    For each HIGH/CRITICAL bug:
    - Write failing test that reproduces bug
    - Verify test fails before fix
    - Apply fix from bug report
    - Verify test passes after fix

    Use TDD pattern: RED → FIX → GREEN
```

## Related Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/security` | Security-focused audit (CWE checks) | Before production deploy |
| `/unit-tests` | Generate test coverage | After bug fixes |
| `/refactor` | Improve code structure | After identifying patterns |
| `/adversarial` | Adversarial spec refinement | Critical code paths |
| `/full-review` | Comprehensive analysis (6 agents) | Major features/releases |

## Ralph Loop Integration

The `/bugs` command follows the Ralph Loop pattern with these hooks:

```
┌─────────────────────────────────────────────────────────┐
│ RALPH LOOP: Bug Hunting                                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 1. EXECUTE   → codex exec bug-hunter                    │
│ 2. VALIDATE  → Check severity counts                    │
│ 3. ITERATE   → Fix HIGH+ bugs                           │
│ 4. VERIFY    → Re-run until summary.approved = true     │
│                                                         │
│ Quality Gate: No HIGH+ bugs OR all explicitly approved  │
│ Max Iterations: 15 (Codex GPT-5.2)                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Approval Criteria

The bug hunting loop continues until:
- **Zero HIGH+ bugs** detected, OR
- **All HIGH+ bugs** explicitly approved by user with justification
- **Quality gates** pass (no new bugs introduced by fixes)

## Example Workflow

Full bug hunting and remediation workflow:

```bash
# 1. Initial bug scan
ralph bugs src/

# 2. Review report
cat ~/.ralph/tmp/codex_bugs.json | jq '.summary'

# 3. Fix HIGH severity bugs
# (manual or via /refactor)

# 4. Verify fixes
ralph bugs src/  # Should show reduced bug count

# 5. Generate regression tests
ralph unit-tests src/

# 6. Run quality gates
ralph gates

# 7. Final approval (if LOW bugs remain)
# Add to bugs-report.json: "approved": true, "justification": "Low risk edge cases"
```

## Best Practices

1. **Run before merge**: Always scan critical paths before PR approval
2. **Prioritize HIGH+**: Focus on CRITICAL and HIGH severity first
3. **Fix root causes**: Don't just patch symptoms
4. **Add tests**: Every fixed bug needs a regression test
5. **Track patterns**: If same bug type appears multiple times, refactor pattern
6. **Combine with /security**: Bug hunting finds logic errors, security finds vulnerabilities
7. **Use Opus for critical**: Switch to `--model opus` for payment/auth/crypto code

## Cost Optimization

| Model | Cost | Speed | When to Use |
|-------|------|-------|-------------|
| GPT-5.2-Codex | ~15% | Fast | Default for bug hunting |
| Opus | 100% | Slow | Critical code paths |
| Sonnet | 60% | Medium | Task orchestration only |

**Recommended**: Codex GPT-5.2 for bug hunting (optimized for code analysis)


## Action Reporting (v2.93.0)

**Esta skill genera reportes automáticos completos** para trazabilidad:

### Reporte Automático

Cuando esta skill completa, se genera automáticamente:

1. **En la conversación de Claude**: Resultados visibles
2. **En el repositorio**: `docs/actions/bugs/{timestamp}.md`
3. **Metadatos JSON**: `.claude/metadata/actions/bugs/{timestamp}.json`

### Contenido del Reporte

Cada reporte incluye:
- ✅ **Summary**: Descripción de la tarea ejecutada
- ✅ **Execution Details**: Duración, iteraciones, archivos modificados
- ✅ **Results**: Errores encontrados, recomendaciones
- ✅ **Next Steps**: Próximas acciones sugeridas

### Ver Reportes Anteriores

```bash
# Listar todos los reportes de esta skill
ls -lt docs/actions/bugs/

# Ver el reporte más reciente
cat $(ls -t docs/actions/bugs/*.md | head -1)

# Buscar reportes fallidos
grep -l "Status: FAILED" docs/actions/bugs/*.md
```

### Generación Manual (Opcional)

```bash
source .claude/lib/action-report-lib.sh
start_action_report "bugs" "Task description"
# ... ejecución ...
complete_action_report "success" "Summary" "Recommendations"
```

### Referencias del Sistema

- [Action Reports System](docs/actions/README.md) - Documentación completa
- [action-report-lib.sh](.claude/lib/action-report-lib.sh) - Librería helper
- [action-report-generator.sh](.claude/lib/action-report-generator.sh) - Generador
