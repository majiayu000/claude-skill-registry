---
name: prompt-iteration
description: Use when iteratively improving agent prompts through automated LLM-as-Judge evaluation. Runs eval→fix→commit loop with circuit breakers.
---

# Prompt Iteration Skill

Iteratively improve teaching agent prompts using automated evaluation with local Qwen 2.5-7B as judge.

## When to Use

- After identifying functional issues with the agent
- When prompt changes need validation before deployment
- For systematic prompt engineering with measurable improvement

## Pre-flight Checks

Before starting, verify:

1. **vLLM is running**:
   ```bash
   curl http://localhost:8004/v1/models
   ```

2. **Golden dataset exists**:
   ```bash
   ls tests/golden/
   ```

3. **Create iteration branch**:
   ```bash
   git checkout -b eval/prompt-iteration-$(date +%Y%m%d-%H%M)
   ```

## Guardrails (USER-DEFINED)

| Guardrail | Value |
|-----------|-------|
| Max iterations | 5 |
| Success gate | 80% pass rate |
| Circuit breaker 1 | Score drops >20% on any dimension |
| Circuit breaker 2 | 3 consecutive iterations with no improvement |
| Rollback mechanism | Git commit after each iteration |

## Iteration Loop

### Step 1: Baseline Evaluation

Run evaluation on all dimensions:

```bash
python -m tests.evaluation.cli --dimension all --output baseline.json
```

Record the baseline pass rate for each dimension in a TodoWrite checklist.

### Step 2: Identify Worst Dimension

From baseline.json, find the dimension with lowest pass rate. Focus on one dimension at a time.

### Step 3: Analyze Failures

Run verbose evaluation on the failing dimension:

```bash
python -m tests.evaluation.cli --dimension <failing_dimension> --verbose
```

Review failed test cases to understand the failure pattern:
- What is the agent doing wrong?
- Which prompt file controls this behavior?
- What specific language could fix it?

### Step 4: Edit Prompt

Modify the relevant prompt file based on analysis:

| Dimension | Primary Prompt File |
|-----------|---------------------|
| language_choice | `src/backend/app/prompts/agent/mode_practice.md` |
| tool_usage | `src/backend/app/prompts/agent/tools.md` |
| output_cleanliness | `src/backend/app/prompts/agent/tools.md` |
| confusion_recovery | `src/backend/app/prompts/agent/base.md` |
| persona_consistency | `src/backend/app/prompts/agent/mode_practice.md` |
| curriculum_alignment | `src/backend/app/prompts/agent/base.md` |

Make targeted, minimal changes. Do not rewrite the entire prompt.

### Step 5: Re-evaluate

Run evaluation on the dimension you're fixing:

```bash
python -m tests.evaluation.cli --dimension <dimension> --output iteration-N.json
```

### Step 6: Check Circuit Breakers

Compare iteration-N.json to baseline.json:

1. **Did any dimension drop >20%?**
   - YES: `git checkout src/backend/app/prompts/` and STOP
   - NO: Continue

2. **Did the target dimension improve?**
   - YES: Commit and continue
   - NO: Increment no-improvement counter

3. **3 consecutive no-improvement?**
   - YES: STOP and report
   - NO: Continue

### Step 7: Commit if Improved

If pass rate improved:

```bash
git add src/backend/app/prompts/
git commit -m "prompt: improve <dimension> pass rate N% -> M%

- [Description of what changed]
- [Why this should help]

Tested with: python -m tests.evaluation.cli --dimension <dimension>
"
```

### Step 8: Repeat or Stop

Continue loop until one of these conditions:
- **SUCCESS**: All dimensions >= 80% pass rate
- **MAX ITERATIONS**: 5 iterations completed
- **REGRESSION**: Any dimension dropped >20% from baseline
- **STALLED**: 3 consecutive iterations with no improvement

## Output Format

After loop completes, produce this summary:

```markdown
## Evaluation Summary

**Baseline**: 45% overall
**Final**: 82% overall
**Iterations**: 4
**Status**: SUCCESS / STOPPED (reason)

### Dimension Results

| Dimension | Baseline | Final | Change |
|-----------|----------|-------|--------|
| language_choice | 40% | 85% | +45% |
| tool_usage | 60% | 95% | +35% |
| output_cleanliness | 50% | 90% | +40% |
| confusion_recovery | 30% | 70% | +40% |
| persona_consistency | 40% | 80% | +40% |
| curriculum_alignment | 50% | 75% | +25% |

### Commits Made

- `abc123` prompt: improve language_choice 40% -> 65%
- `def456` prompt: improve tool_usage 60% -> 95%
- `ghi789` prompt: improve output_cleanliness 50% -> 90%

### Next Steps

- [If success] Ready to merge to main
- [If stopped] Manual review needed for dimension X
```

## Quick Reference

```bash
# Full evaluation
python -m tests.evaluation.cli --dimension all

# Single dimension
python -m tests.evaluation.cli --dimension language_choice --verbose

# Check judge availability
python -m tests.evaluation.cli --check

# List test cases
python -m tests.evaluation.cli --list

# A/B comparison (if testing prompt variants)
python -m tests.evaluation.cli --compare prompts/v1.md prompts/v2.md
```

## Prompt Files Reference

```
src/backend/app/prompts/agent/
├── base.md           # Core rules, language handling, confusion recovery
├── mode_help.md      # Vocabulary helper mode behavior
├── mode_practice.md  # Conversation practice mode behavior
└── tools.md          # Tool definitions (speak, render_vocabulary, etc.)
```
