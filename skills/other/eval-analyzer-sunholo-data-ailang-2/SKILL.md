---
name: Eval Analyzer
description: Analyze evaluation baseline results, identify failure patterns, and generate actionable insights. Use after running eval baselines or when user asks to analyze eval results, check benchmarks, investigate failures, or understand what's failing.
---

# Eval Analyzer

Analyze AILANG evaluation baseline results to identify failure patterns, compare model performance, and generate actionable insights.

## Quick Start

**Most common usage:**
```bash
# User says: "Analyze the v0.3.24 eval results"
# This skill will:
# 1. Run eval-analyze to categorize failures (standard eval)
# 2. Run agent KPIs to analyze efficiency (agent eval)
# 3. Generate summary with jq queries
# 4. Identify top failing benchmarks
# 5. Show model performance comparison
# 6. Provide optimization recommendations
```

**For agent evaluation analysis** (NEW - optimization focus):
```bash
# Step 1: Get efficiency metrics (turns, tokens, cost)
.claude/skills/eval-analyzer/scripts/agent_kpis.sh eval_results/baselines/v0.3.24

# Step 2: Investigate expensive benchmarks
.claude/skills/eval-analyzer/scripts/agent_transcripts.sh eval_results/baselines/v0.3.24 simple_print

# Step 3: Compare Python vs AILANG
./tools/compare_agents.sh eval_results/baselines/v0.3.24
```

**See [`resources/agent_optimization_guide.md`](resources/agent_optimization_guide.md) for complete optimization strategies.**

## When to Use This Skill

Invoke this skill when:
- User asks to "analyze eval results", "check benchmarks", "what's failing"
- After running an eval baseline
- When investigating why benchmark performance changed
- User wants to understand failure patterns or model performance
- Comparing two versions of AILANG

## Key Eval Commands

All commands work on baseline directories like `eval_results/baselines/v0.3.16/`.

### 1. Quick Overview - `eval-matrix`

Shows comprehensive statistics with model/language breakdowns.

```bash
ailang eval-matrix eval_results/baselines/v0.3.16 0.3.16 | head -60
```

**Shows**: Overall stats, per-model performance, per-language breakdown, top error codes.

### 2. Detailed Analysis - `eval-analyze`

Categorizes failures and can generate design docs for issues.

```bash
# Dry run (no design docs, just analysis)
ailang eval-analyze -results eval_results/baselines/v0.3.16 -dry-run

# Full analysis with design doc generation
ailang eval-analyze -results eval_results/baselines/v0.3.16
```

**⚠️ CRITICAL**: Must use `-results` flag, NOT positional argument!

**Output**: Categorized failures (compile_error, logic_error, runtime_error) with frequency, affected benchmarks, models, and sample errors.

### 3. Query-Friendly Summary - `eval-summary`

Generates JSONL for easy querying with jq.

```bash
ailang eval-summary eval_results/baselines/v0.3.16
```

**Output**: `eval_results/baselines/v0.3.16/summary.jsonl`

### 4. Compare Versions - `eval-compare`

Shows what changed between two versions.

```bash
ailang eval-compare eval_results/baselines/v0.3.15 eval_results/baselines/v0.3.16
```

### 5. Fair Comparison (RECOMMENDED) - `fair_comparison.py`

**Use this for accurate version comparisons!** The `eval-compare` command may include duplicates or different model sets. This script normalizes data for apple-to-apples comparison.

```bash
.claude/skills/eval-analyzer/scripts/fair_comparison.py
```

**What it does:**
- Deduplicates runs (keeps last run per benchmark+model)
- Filters to dev models only (gpt5-mini, claude-haiku-4-5, gemini-2-5-flash)
- AILANG only (ignores Python results)
- Shows net fixes vs regressions
- Per-model breakdown

**Output:**
```
v0.4.0: 56/123 = 45.5%
v0.4.2: 59/123 = 48.0%
Delta:  +3 (+2.4pp)

✅ Fixed:   11 benchmarks
❌ Broken:  8 benchmarks
NET:       +3 benchmarks
```

**When to use:** Before making decisions based on eval results (e.g., reverting changes, merging PRs).

### 6. Validate Results - `validate_eval_results.py`

**Check for output corruption and race conditions** in eval results.

```bash
python3 tools/validate_eval_results.py eval_results/baselines/v0.4.2
```

**Checks:**
- Output corruption (fibonacci outputting "All results equal", etc.)
- Duplicate runs for same benchmark+model
- Code hash validation (if available)
- Success rate statistics

**When to use:** After running eval baselines, especially if results look suspicious.

## Agent Analysis Scripts (NEW!)

**For agent-based evaluation results** (Python vs AILANG comparisons with Claude Code):

### 1. Agent KPIs - Minimize Tokens & Turns

Shows efficiency metrics for agent runs - **key for optimizing language and prompts**.

```bash
.claude/skills/eval-analyzer/scripts/agent_kpis.sh eval_results/WITH_ALL_FIXES
```

**Output:**
- Average turns, tokens, cost by language (Python vs AILANG)
- Most expensive benchmarks (by turns) - candidates for optimization
- Most efficient benchmarks - learn from these
- Success rates and performance comparison

**Goal**: Minimize agent turns and tokens → indicates clearer prompts and simpler language.

### 2. Agent Transcripts - View AILANG Conversations

View full agent conversation logs to understand what happened.

```bash
# View all transcripts
.claude/skills/eval-analyzer/scripts/agent_transcripts.sh eval_results/WITH_ALL_FIXES

# View only failures
.claude/skills/eval-analyzer/scripts/agent_transcripts.sh eval_results/WITH_ALL_FIXES --failed-only

# View specific benchmark
.claude/skills/eval-analyzer/scripts/agent_transcripts.sh eval_results/WITH_ALL_FIXES fizzbuzz
```

**Output:**
- Turn-by-turn conversation showing agent's thought process
- Metrics: turns, tokens, duration
- Success/failure status with error category
- First 100 lines of transcript (with hint to view full)

**Use for**: Understanding why AILANG solutions fail or take many turns.

### 3. Python vs AILANG Comparison

Use the existing `tools/compare_agents.sh` script for side-by-side comparison:

```bash
./tools/compare_agents.sh eval_results/WITH_ALL_FIXES
```

**Output:**
- Side-by-side metrics table
- Solution code comparison
- Transcripts for failed solutions (automatic)
- Winner indicators for each metric

## Standard Eval Workflow (Non-Agent)

### Step 1: Get High-Level Overview

```bash
# Show overall statistics
ailang eval-matrix eval_results/baselines/v0.3.16 0.3.16 | head -60
```

**Look for:**
- Overall success rate (target: >60%)
- AILANG vs Python gap (current: ~54%)
- Model performance variance
- Top error codes

### Step 2: Identify Problem Areas

```bash
# Categorize all failures
ailang eval-analyze -results eval_results/baselines/v0.3.16 -dry-run
```

**Key metrics:**
- compile_error frequency (parse/syntax issues)
- logic_error frequency (wrong output)
- runtime_error frequency (crashes)
- Which benchmarks fail most

### Step 3: Query with jq (Custom Analysis)

Use jq queries on summary.jsonl for custom analysis:

```bash
# Ensure summary exists
ailang eval-summary eval_results/baselines/v0.3.20

# AILANG-only success rate (all models)
jq -s 'map(select(.lang == "ailang")) |
  {total: length, success: (map(select(.stdout_ok == true)) | length),
   rate: ((map(select(.stdout_ok == true)) | length) * 100.0 / length)}' \
  eval_results/baselines/v0.3.20/summary.jsonl

# Dev models only (useful for prompt testing)
jq -s 'map(select(.lang == "ailang" and
  (.model == "gpt5-mini" or .model == "claude-haiku-4-5" or .model == "gemini-2-5-flash"))) |
  {total: length, success: (map(select(.stdout_ok == true)) | length),
   rate: ((map(select(.stdout_ok == true)) | length) * 100.0 / length)}' \
  eval_results/baselines/v0.3.20/summary.jsonl

# Check specific benchmark across all models
jq -s 'map(select(.benchmark == "explicit_state_threading" and .lang == "ailang")) |
  map({model, success: .stdout_ok, error: .error_category})' \
  eval_results/baselines/v0.3.20/summary.jsonl

# Compare two versions (dev models AILANG-only)
jq -s 'map(select(.lang == "ailang" and
  (.model == "gpt5-mini" or .model == "claude-haiku-4-5" or .model == "gemini-2-5-flash"))) |
  {total: length, success: (map(select(.stdout_ok == true)) | length),
   rate: ((map(select(.stdout_ok == true)) | length) * 100.0 / length)}' \
  eval_results/baselines/v0.3.20/summary.jsonl \
  eval_results/baselines/v0.3.21/summary.jsonl
```

**For more jq patterns**, see [`resources/jq_queries.md`](resources/jq_queries.md)

### Step 4: Deep Dive with Helper Scripts

Use the provided helper scripts for detailed code inspection:

```bash
# Failure analysis with error categorization
.claude/skills/eval-analyzer/scripts/analyze_failures.sh eval_results/baselines/v0.3.16

# Model performance comparison
.claude/skills/eval-analyzer/scripts/compare_models.sh eval_results/baselines/v0.3.16

# Examine specific benchmark failures
.claude/skills/eval-analyzer/scripts/examine_code.sh eval_results/baselines/v0.3.16 api_call_json
```

### Step 4: Compare with Previous Version

```bash
# Show regressions and improvements
ailang eval-compare eval_results/baselines/v0.3.15 eval_results/baselines/v0.3.16
```

### Step 5: Generate Insights

Based on the data, identify:

1. **Systemic Issues**: Categories with >50 failures
2. **Model Patterns**: Which models struggle with which features
3. **Benchmark Hotspots**: Benchmarks with 100% failure rate
4. **Cost Efficiency**: Which models give best success/cost ratio
5. **Trends**: Improvements or regressions vs previous version

## Key Metrics to Track

1. **Overall Success Rate**: AILANG vs Python gap (target: reduce below 50%)
2. **Error Code Distribution**:
   - PAR_001 (parse errors) - indicates prompt/syntax issues
   - WRONG_LANG - models writing Python instead of AILANG
   - IMPERATIVE - models using imperative patterns
3. **Model Performance**: Which models work best with AILANG
4. **Benchmark-Level**: Which benchmarks consistently fail
5. **Cost Efficiency**: Success rate per dollar spent
6. **Repair Success**: Is self-repair helping? (currently low)

## Common Issues

### Issue 1: "Total Runs: 6" instead of 408

**Symptom**: eval-analyze only finds 6 results

**Cause**: Used positional argument instead of `-results` flag

**Solution**:
```bash
# ❌ WRONG
ailang eval-analyze eval_results/baselines/v0.3.16

# ✅ CORRECT
ailang eval-analyze -results eval_results/baselines/v0.3.16
```

### Issue 2: Summary file not found

**Symptom**: jq queries fail with "file not found"

**Cause**: Need to run eval-summary first

**Solution**:
```bash
ailang eval-summary eval_results/baselines/v0.3.16
```

### Issue 3: Design docs not generated

**Symptom**: eval-analyze shows issues but doesn't create docs

**Cause**: Using `-dry-run` flag

**Solution**: Run without `-dry-run` to generate design docs

## Helper Scripts

The skill includes helper scripts in `scripts/` directory:

### quick_summary.sh

Fast overview using eval-matrix.

```bash
.claude/skills/eval-analyzer/scripts/quick_summary.sh eval_results/baselines/v0.3.16
```

**Output**: Overall stats, model performance, language breakdown, top error codes.

### analyze_failures.sh

Detailed failure analysis with error categorization.

```bash
.claude/skills/eval-analyzer/scripts/analyze_failures.sh eval_results/baselines/v0.3.16 ailang
```

**Output**: Overall statistics, error categories, top failing benchmarks, model performance, error codes.

### compare_models.sh

Model-by-model performance comparison.

```bash
.claude/skills/eval-analyzer/scripts/compare_models.sh eval_results/baselines/v0.3.16
```

**Output**: Success rates, first-attempt vs final, cost analysis, token usage, best model per benchmark.

### examine_code.sh

Inspect generated code from specific benchmarks.

```bash
.claude/skills/eval-analyzer/scripts/examine_code.sh eval_results/baselines/v0.3.16 api_call_json
.claude/skills/eval-analyzer/scripts/examine_code.sh eval_results/baselines/v0.3.16 api_call_json gpt5
```

**Output**: Generated code, compiler errors, success status, error codes for each model run.

### examine_prompts.sh

View prompts used for specific benchmarks.

```bash
.claude/skills/eval-analyzer/scripts/examine_prompts.sh eval_results/baselines/v0.3.16 api_call_json
```

**Output**: System prompt, user prompt, success status for benchmark runs.

### verify_prompt_accuracy.sh

Check if prompt documentation matches actual implementation.

```bash
.claude/skills/eval-analyzer/scripts/verify_prompt_accuracy.sh v0.3.16
```

**Output**: Reports false limitations, undocumented features, and prompt-code mismatches.

**Use this**: After creating new prompt versions to catch documentation bugs!

## Resources

### Analysis Documents

- [`resources/failure_analysis_v0.3.16.md`](resources/failure_analysis_v0.3.16.md) - Comprehensive analysis of v0.3.16 eval results with root cause analysis

### Common jq Patterns

See [`resources/jq_queries.md`](resources/jq_queries.md) for more query examples and patterns.

## Progressive Disclosure

This skill loads information progressively:

1. **Always loaded**: This SKILL.md file (workflow + commands + scripts)
2. **Execute as needed**: `ailang eval-*` commands and helper scripts
3. **Load on demand**: `resources/jq_queries.md`, analysis documents

## Notes

- All eval commands work offline (no API calls for analysis)
- `eval-analyze` generates design docs using LLM (default: gpt5)
- Summary JSONL format is stable and queryable
- Use `-dry-run` to preview before generating design docs
- baseline directories typically at `eval_results/baselines/vX.X.X/`
- This skill complements `post-release` skill (which runs baselines)
