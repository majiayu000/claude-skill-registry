---
name: eta
description: |
  When a user asks how long a task will take, requests a time estimate, or before
  starting any non-trivial coding task, immediately run scripts/estimate_task.py
  to analyze the codebase scope and provide a data-driven time estimate. Show the
  estimate breakdown, risk factors, and checkpoint recommendations without asking.
allowed-tools: |
  bash: python, ls, find, wc
  file: read
---

# ETA

<purpose>
Provides realistic time estimates for coding tasks before work begins. Users often
underestimate task complexity. This skill analyzes codebase scope, categorizes task
complexity, identifies risk factors, and calculates estimates based on measured
Claude Code performance baselines. Prevents surprise delays and enables better planning.
</purpose>

## Instructions

### Step 1: Gather Task Context

When triggered, collect:
- Task description from the user
- Path to relevant codebase (default: current directory)
- Number of files likely in scope (if known)

### Step 2: Run Estimation

```bash
python scripts/estimate_task.py --task "<task_description>" --path "<codebase_path>"
```

Optional flags:
- `--files <n>`: Override estimated files in scope
- `--json`: Output structured JSON for programmatic use

### Step 3: Present Estimate

Return the formatted estimate showing:
- Task category (trivial/simple/medium/complex/major)
- Scope analysis (files, lines, test coverage)
- Time range (low-high estimate)
- Breakdown by phase (analysis, implementation, testing, verification)
- Risk factors with explanations
- Checkpoint recommendations for long tasks

### Step 4: Adjust Based on Feedback

If user provides more context:
- Re-run with `--files` override if scope is clearer
- Adjust category interpretation based on domain knowledge

## NEVER

- Start a complex task without providing an estimate first
- Give single-point estimates (always provide ranges)
- Ignore risk factors when they're detected
- Skip the estimate for tasks over 15 minutes
- Promise exact completion times

## ALWAYS

- Run the estimate script before non-trivial tasks
- Show the breakdown so users understand where time goes
- Flag risk factors visibly with explanations
- Recommend checkpoints for tasks over 30 minutes
- Update estimates if scope changes mid-task

## Examples

### Example 1: User asks about task duration

**Input:** "How long will it take to add user authentication?"

**Workflow:**
1. Run `scripts/estimate_task.py --task "Add user authentication" --path .`
2. Output shows:
   - Category: Complex
   - Estimated time: 24-53 minutes
   - Risk factors: High-risk changes, External dependencies
   - Recommendation: Break into phases with commits between each

### Example 2: Before starting a feature

**Input:** "Add a dark mode toggle to settings"

**Workflow:**
1. Detect this is a non-trivial task (feature keyword)
2. Run `scripts/estimate_task.py --task "Add dark mode toggle to settings" --path ./src`
3. Present estimate: 10-22 minutes (Medium complexity)
4. Begin implementation with checkpoint plan

### Example 3: Quick fix request

**Input:** "Fix the typo in the README"

**Workflow:**
1. Detect trivial task (typo keyword)
2. Run quick estimate: 3-6 minutes
3. Proceed immediately (no detailed breakdown needed for trivial tasks)
