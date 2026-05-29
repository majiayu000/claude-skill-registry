---
name: eval-recipes-runner
version: 1.0.0
description: Run Microsoft's eval-recipes benchmarks to validate amplihack improvements against baseline agents. Activates when testing with eval-recipes, running evals, or benchmarking changes.
---

# eval-recipes Runner Skill

## Purpose

Run Microsoft's eval-recipes benchmarks to validate amplihack improvements against baseline agents.

## When to Use

- User asks to "test with eval-recipes"
- User says "run the evals" or "benchmark this change"
- User wants to validate improvements against codex/claude_code
- Testing a PR branch to prove it improves scores

## Capabilities

I can run eval-recipes benchmarks to:
1. Test specific amplihack branches
2. Compare against baseline agents (codex, claude_code)
3. Run specific tasks (linkedin_drafting, email_drafting, etc.)
4. Compare before/after scores for PRs
5. Generate reports with score improvements

## How It Works

### Setup (One-Time)

```bash
# Clone eval-recipes from Microsoft
git clone https://github.com/microsoft/eval-recipes.git ~/eval-recipes
cd ~/eval-recipes

# Copy our agent configs
cp -r $(pwd)/.claude/agents/eval-recipes/* data/agents/

# Install dependencies
uv sync
```

### Running Benchmarks

**Test a specific branch:**
```bash
# Update install.dockerfile to use specific branch
# Then run benchmark
cd ~/eval-recipes
uv run eval_recipes/main.py --agent amplihack --task linkedin_drafting --trials 3
```

**Compare before/after:**
```bash
# Test baseline (main)
uv run eval_recipes/main.py --agent amplihack --task linkedin_drafting

# Test PR branch (edit install.dockerfile to checkout PR branch)
uv run eval_recipes/main.py --agent amplihack_pr1443 --task linkedin_drafting

# Compare scores
```

### Available Tasks

Common tasks from eval-recipes:
- `linkedin_drafting` - Create tool for LinkedIn posts (scored 6.5/100 before PR #1443)
- `email_drafting` - Create CLI tool for emails (scored 26/100 before)
- `arxiv_paper_summarizer` - Research tool
- `github_docs_extractor` - Documentation tool
- Many more in `~/eval-recipes/data/tasks/`

### Typical Workflow

When user says "test this change with eval-recipes":

1. **Identify the branch/PR** to test
2. **Update agent config** to use that branch:
   ```dockerfile
   # In .claude/agents/eval-recipes/amplihack/install.dockerfile
   RUN git clone https://github.com/rysweet/...git /tmp/amplihack && \
       cd /tmp/amplihack && \
       git checkout BRANCH_NAME && \
       pip install -e .
   ```
3. **Copy to eval-recipes:**
   ```bash
   cp -r .claude/agents/eval-recipes/* ~/eval-recipes/data/agents/
   ```
4. **Run benchmark:**
   ```bash
   cd ~/eval-recipes
   uv run eval_recipes/main.py --agent amplihack --task TASK_NAME --trials 3
   ```
5. **Report scores** and compare with baseline

### Expected Scores

**Baseline (main branch):**
- Overall: 40.6/100
- LinkedIn: 6.5/100
- Email: 26/100

**With PR #1443 (task classification):**
- Expected: 55-60/100 (+15-20 points)
- LinkedIn: 30-40/100 (creates actual tool)
- Email: 45/100 (consistent execution)

## Example Usage

**User says:** "Test PR #1443 with eval-recipes on the LinkedIn task"

**I do:**
1. Update install.dockerfile to checkout `feat/issue-1435-task-classification`
2. Copy to eval-recipes: `cp -r .claude/agents/eval-recipes/* ~/eval-recipes/data/agents/`
3. Run: `cd ~/eval-recipes && uv run eval_recipes/main.py --agent amplihack --task linkedin_drafting --trials 3`
4. Report results: "Score: 35.2/100 (up from 6.5 baseline)"

## Prerequisites

- eval-recipes cloned to `~/eval-recipes`
- API key in environment: `export ANTHROPIC_API_KEY=sk-ant-...`
- Docker installed (for containerized runs)
- uv installed: `curl -LsSf https://astral.sh/uv/install.sh | sh`

## Notes

- Benchmarks take 2-15 minutes per task depending on complexity
- Multiple trials (3-5) give more reliable averages
- Docker builds can be cached for speed
- Results saved to `.benchmark_results/` in eval-recipes repo

## Automation

For fully autonomous testing:
```bash
# Test suite for a PR
tasks="linkedin_drafting email_drafting arxiv_paper_summarizer"
for task in $tasks; do
  uv run eval_recipes/main.py --agent amplihack --task $task --trials 3
done

# Compare results
cat .benchmark_results/*/amplihack/*/score.txt
```
