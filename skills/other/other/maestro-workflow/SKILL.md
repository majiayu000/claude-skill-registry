---
name: maestro-workflow
description: >
  Multi-LLM orchestration implementing the 5-stage coding workflow:
  Example Analysis → Hypothesis → Implementation → Debug Loop → Recursive Improvement.

  Based on "Towards a Science of Scaling Agent Systems" (Kim et al., 2025):
  - Centralized Consult architecture (Claude orchestrates, others advise)
  - Measured coordination (avoid MAS overhead in tool-heavy stages)
  - Tests-first selection (Poetiq pattern, not voting)

  Use when: Debugging complex issues, analyzing unfamiliar code, refactoring,
  or any task that benefits from diverse LLM perspectives with verification.
---

# Maestro Workflow: Multi-LLM Orchestration with Measured Coordination

## Core Philosophy (Paper-Based)

This workflow implements findings from "Towards a Science of Scaling Agent Systems":

### 1. Tool-Coordination Trade-off
- **Paper finding**: Tool-heavy tasks suffer from multi-agent coordination overhead
- **Our rule**: Only Claude Code (orchestrator) runs tools (edit files, run tests)
- **Sub-agents** (Codex/Gemini) provide TEXT ADVICE ONLY

### 2. Capability Saturation (~45% threshold)
- **Paper finding**: When single-agent baseline exceeds ~45%, MAS returns diminish
- **Our rule**: If you're confident about the solution, SKIP ensemble generation
- **Ask yourself**: "Am I stuck, or do I just want confirmation?"

### 3. Error Amplification Prevention
- **Paper finding**: Independent agents amplify errors 17.2x without verification
- **Our rule**: ALWAYS verify with tests before accepting any candidate
- **Use `maestro_select_best` with `tests_first` mode (not voting!)**

## Available Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `maestro_consult` | Single model consultation | Analysis, code review, specific questions |
| `maestro_ensemble_generate` | Multiple candidates | Hypothesis generation, solution exploration |
| `maestro_select_best` | Pick best candidate | After ensemble, with test/lint results |
| `maestro_pack_context` | Smart context packing | Before any consultation |
| `maestro_run_stage` | Execute workflow stage | Structured 5-stage execution |
| `maestro_workflow_state` | Check progress | Monitor budget, see history |
| `maestro_get_metrics` | Paper-aligned metrics | Performance analysis |

## The 5-Stage Workflow

### Stage 1: Example Analysis (analyze)
**Goal**: Freeze facts before guessing.

**Process**:
1. Gather context with file reads, `grep`, `ls`
2. Optionally use `maestro_consult(provider="gemini")` for large file summarization
3. Document observations, repro steps, affected modules

**Output** (JSON):
```json
{
  "observations": ["Test fails with IndexError on line 42"],
  "repro_steps": ["Run pytest test_auth.py::test_login"],
  "affected_modules": ["src/auth.py", "src/db.py"],
  "invariants": ["Must not break existing login flow"]
}
```

**Coordination Policy**: Low overhead allowed (2 consults max)

---

### Stage 2: Hypothesis Formulation (hypothesize)
**Goal**: Generate competing explanations with testable predictions.

**Process**:
1. Use `maestro_ensemble_generate(task="Top 3 root causes...", providers=["codex", "gemini"])`
2. Each hypothesis must have a VERIFICATION TEST
3. Use `maestro_select_best` to pick most testable hypothesis

**Output** (JSON):
```json
{
  "hypotheses": [
    {
      "id": "H1",
      "claim": "Off-by-one error in array indexing",
      "verification_test": "Add edge case test with empty array",
      "confidence": 0.7
    }
  ],
  "selected": "H1",
  "test_command": "pytest test_auth.py::test_empty_users -v"
}
```

**Coordination Policy**: Ensemble ENCOURAGED (best stage for MAS)

---

### Stage 3: Code Implementation (implement)
**Goal**: Apply minimal, testable changes.

**Process**:
1. Claude Code (orchestrator) edits the file directly
2. Optionally consult `maestro_consult(provider="codex")` for diff suggestions
3. Run tests IMMEDIATELY after edit

**Key Rules**:
- NO parallel implementations (creates conflicts)
- ONE change at a time
- Test after EVERY change

**Coordination Policy**: Single agent PREFERRED (tool-heavy = bad for MAS)

---

### Stage 4: Iterative Debugging (debug)
**Goal**: Fix without divergence.

**Process**:
1. Analyze the NEW error (what changed?)
2. Update hypothesis confidence
3. Make SINGLE smallest change
4. Test again

**WARNING**: Paper shows sequential debugging DEGRADES with multi-agent!

**Coordination Policy**:
- Single agent ONLY for first 2 iterations
- Consult external ONLY if stuck for 3+ iterations
- Feed error logs into context

**Iteration Limit**: 5 (escalate if exceeded)

---

### Stage 5: Recursive Improvement (improve)
**Goal**: Refactor and stabilize after tests pass.

**Process**:
1. Review for code quality (but don't over-engineer!)
2. Identify edge cases
3. Add regression tests
4. Optional: `maestro_consult(provider="claude")` for safety review

**Entry Condition**: ALL TESTS MUST PASS

**Coordination Policy**: Ensemble OK for review/suggestions

---

## Example Usage Patterns

### Pattern 1: Bug Investigation
```
User: "The login test is failing, can you debug it?"

1. [ANALYZE] Read test file, error logs
   maestro_pack_context(files=["tests/test_auth.py"], errors=[error_log], stage="analyze")

2. [HYPOTHESIZE] Generate root cause theories
   maestro_ensemble_generate(task="Top 3 causes for IndexError in auth...", providers=["codex", "gemini"])

3. [SELECT] Pick most testable hypothesis
   maestro_select_best(candidates=..., mode="tests_first", test_results=[...])

4. [IMPLEMENT] Fix (Claude edits directly)
   Edit file, run pytest

5. [DEBUG] If test still fails, iterate
   Single agent mode, minimal changes

6. [IMPROVE] After tests pass
   Add edge case tests, review for safety
```

### Pattern 2: Code Review with Diverse Perspectives
```
User: "Review this PR for security issues"

1. maestro_pack_context(files=[changed_files], stage="analyze")

2. maestro_ensemble_generate(
     task="Security review: identify vulnerabilities in...",
     providers=["codex", "gemini", "claude"]
   )

3. maestro_select_best(candidates=..., mode="llm_judge", criteria=["security", "severity"])
```

### Pattern 3: Checking Metrics Mid-Workflow
```
User: "How much coordination overhead have we used?"

maestro_workflow_state()
# Returns: consults used, budget remaining, efficiency score
```

## Coordination Budget

**Per Workflow Limits** (configurable):
- Max consults per stage: 2
- Max total consults: 6
- Capability threshold: 45%

**When to SKIP ensemble**:
- You're confident in the solution
- It's a tool-heavy stage (implement, debug)
- Budget is exhausted

## Error Handling

If a sub-agent fails:
1. Check `stderr` in the response
2. Try a different provider
3. Fall back to single-agent mode
4. Document the failure in tracing

## Metrics (Paper-Aligned)

After any workflow, check:
```
maestro_get_metrics()
```

Key metrics:
- **Coordination Overhead (O%)**: Extra calls vs single-agent
- **Efficiency Score (Ec)**: Success / overhead ratio
- **Test Coverage Rate**: Selections that had test signals

Target: O% < 300%, Ec > 0.4, Test Coverage > 80%
