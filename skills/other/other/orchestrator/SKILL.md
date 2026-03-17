---
name: orchestrator
description: Claude as intelligent orchestrator for multi-agent workflows. Coordinates specialized agents (Gemini, local models, tools) using Shell-As-Bus pattern with capability-based delegation.
version: 1.1.0
---

# Orchestrator - Multi-Agent Coordination

Claude orchestrates specialized agents to solve complex tasks efficiently.

## Core Principle

**"Shell-As-Bus"**: Every agent is a CLI tool. Bash is the universal communication bus. Files and stdout for data exchange.

## Workflow

1. **Analyze request** (Planning Mode):
   - Break down into sub-tasks
   - Identify required capabilities
   - Match tasks to agents via Decision Matrix
   - Check quota constraints (PROVIDER-LIMITS.md)

2. **Create execution plan**:
   - Sequential for dependent tasks
   - Parallel for independent tasks
   - Hybrid for complex workflows

3. **Delegate intelligently**:
   ```yaml
   Decision Matrix:
     High Creativity/Reasoning → Execute directly (Claude)
     Massive Context (>200k tokens) → gemini-specialist
     Bulk/Repetitive Processing → local-model
     Real-time Information → gemini-specialist (Search grounding)
     Sensitive/Private Data → local-model
   ```

4. **Monitor execution**:
   - Check agent outputs (stdout, exit codes)
   - Validate against expectations
   - Intervene on errors (fallback to Claude)

5. **Synthesize results**:
   - Combine agent outputs
   - Validate consistency
   - Present unified result

6. **Handle failures** (Try-Catch-Escalate):
   - Try: Delegate to specialist
   - Catch: Agent fails or produces bad output
   - Escalate: Claude fixes directly

## Agent Interface Standard

All delegated agents must:
- Be callable via CLI
- Return clean stdout (not debug logs)
- Use exit codes (0=success, non-zero=error)
- Save artifacts to known paths

**Good output:**
```
Task completed. Summary: [brief]. Artifacts: [path].
```

**Bad output:**
```
[DEBUG] Loading...
[INFO] Processing...
[WARNING] ...
```

## Delegation Patterns

### Pattern 1: Staggered Parallel Execution (Independent Tasks)
```bash
# CRITICAL: Use staggered launch (1s delay) to avoid Gemini CLI race condition
# Workers run simultaneously AFTER startup - 4-8x faster than sequential!

TASKS=("task1" "task2" "task3" "task4")

for i in "${!TASKS[@]}"; do
  gemini -p "${TASKS[$i]}" --yolo -o text > /tmp/result$i.txt &
  sleep 1  # ← CRITICAL: Prevents concurrent startup bug (Issue #3161)
done

wait  # Wait for all to complete

# Synthesize results
for f in /tmp/result*.txt; do
  cat "$f"
done
```

**Why staggered?** Gemini CLI v0.21.1 has race condition during startup. 500ms-1s delay fixes it. Workers still run in parallel after startup!

### Pattern 2: Sequential Pipeline (Dependent Tasks)
```bash
# Output of one feeds the next
gemini -p "analyze code" < code.py --yolo -o text > analysis.md
# Claude reads analysis
cat analysis.md
# Claude implements based on analysis
```

### Pattern 3: Evaluator-Optimizer (Review Loop)
```bash
# Claude generates code
cat > draft.py << EOF
...code...
EOF

# Gemini reviews
gemini -p "security audit this code" < draft.py --yolo -o text > review.md

# Claude refines based on review
cat review.md
# Apply improvements
```

## When to Orchestrate

✅ **Use orchestration when:**
- Task requires multiple distinct capabilities
- Massive context exceeds Claude's window
- Parallel execution saves time
- Need specialized tools/search
- Cross-validation desired

❌ **Don't orchestrate when:**
- Task is simple (single-step)
- Only Claude's capabilities needed
- Overhead exceeds benefit

## Key Principle

**Delegation > Monopolization**. Use specialized agents for their strengths. Claude orchestrates and synthesizes, not does everything.

---

See PATTERNS.md for detailed workflows, AGENTS.md for available agent catalog, and PROVIDER-LIMITS.md for quota constraints.
