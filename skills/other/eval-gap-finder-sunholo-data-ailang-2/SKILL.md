---
name: Eval Gap Finder
description: Find AILANG vs Python eval gaps and improve prompts/language. Use when user says 'find eval gaps', 'analyze benchmark failures', 'close Python-AILANG gap', or after running evals.
---

# Eval Gap Finder

Automates the process of finding and closing the gap between Python and AILANG benchmark success rates. Identifies language limitations, prompt gaps, and missing stdlib functions.

## Quick Start

**Most common usage:**
```bash
# User says: "Find eval gaps" or "Analyze benchmark failures"
# This skill will:
# 1. Run evals with dev models (gemini-3-flash, claude-haiku-4-5)
# 2. Compare Python vs AILANG success rates
# 3. Identify benchmarks where Python passes but AILANG fails
# 4. Analyze error patterns and categorize them
# 5. Check if gaps are documented in prompt
# 6. Test proposed examples and add to prompt
# 7. Create design docs for language limitations
```

## When to Use This Skill

Invoke this skill when:
- User asks to "find eval gaps" or "close the Python-AILANG gap"
- User wants to analyze benchmark failures
- After running evals and seeing lower AILANG success
- User says "why is AILANG failing?" or "improve AILANG benchmarks"
- User wants to identify language limitations

## Available Scripts

### `scripts/run_gap_analysis.sh [eval_dir]`
Run full gap analysis on eval results.

```bash
.claude/skills/eval-gap-finder/scripts/run_gap_analysis.sh eval_results/v0.6.5
```

### `scripts/identify_python_only.sh <eval_dir>`
List benchmarks where Python passes but AILANG fails.

```bash
.claude/skills/eval-gap-finder/scripts/identify_python_only.sh eval_results/v0.6.5
```

### `scripts/categorize_errors.sh <eval_dir>`
Categorize AILANG failures by error type.

```bash
.claude/skills/eval-gap-finder/scripts/categorize_errors.sh eval_results/v0.6.5
```

### `scripts/test_example.sh <code>`
Test if an AILANG code example compiles and runs correctly.

```bash
.claude/skills/eval-gap-finder/scripts/test_example.sh /tmp/test.ail
```

## Workflow

### 1. Run Evals with Dev Models

```bash
ailang eval-suite --models gemini-3-flash,claude-haiku-4-5 --output eval_results/gap-analysis
```

Target: Run with cheap/fast models first. If they succeed, larger models should too.

### 2. Generate Summary and Identify Gaps

```bash
ailang eval-summary eval_results/gap-analysis
.claude/skills/eval-gap-finder/scripts/identify_python_only.sh eval_results/gap-analysis
```

Key metrics:
- AILANG success rate (target: >70%)
- Python success rate (baseline)
- Gap (python_only benchmarks)

### 3. Analyze Error Patterns

For each Python-only pass, categorize the error:

| Category | Pattern | Fix Approach |
|----------|---------|--------------|
| WRONG_LANG | Model wrote Python syntax | Stronger "NOT Python" in prompt |
| PAR_001 | Parse errors (syntax) | Add more examples to prompt |
| Type errors | Type unification failures | May be language limitation |
| Logic errors | Compiles but wrong output | Better examples or algorithm |
| EOF errors | Incomplete code generation | Model limitation, not prompt |

### 4. Check Prompt Coverage

For each gap, check if the pattern is documented:

```bash
grep -n "pattern" prompts/v0.6.5.md
```

If not documented, add:
- Working example to Quick Reference section
- Entry in "What AILANG Does NOT Have" table (if limitation)
- New section if pattern is complex

### 5. Test Examples Before Adding

**CRITICAL**: Always test examples before adding to prompt!

```bash
cat > /tmp/test.ail << 'EOF'
module benchmark/solution
-- Your example code here
EOF
ailang run --caps IO --entry main /tmp/test.ail
```

If example fails, it reveals a language gap - create a design doc instead.

### 6. Create Design Docs for Language Gaps

If testing reveals a language limitation:

1. Create design doc: `design_docs/planned/vX_Y_Z/m-<feature>.md`
2. Document:
   - Minimal reproduction
   - Error message
   - Workaround (for prompt)
   - Proposed fix
3. Add workaround to prompt with note

### 7. Track Improvement

After updates, re-run evals:

```bash
ailang eval-suite --models gemini-3-flash,claude-haiku-4-5 --output eval_results/gap-analysis-v2
```

Compare:
- Success rate improvement
- Which benchmarks fixed
- Any regressions

## Error Categories Reference

| Error | Meaning | Fix |
|-------|---------|-----|
| WRONG_LANG | Wrote Python instead | Prompt emphasis |
| PAR_001 | Parser error | Syntax examples |
| PAR_UNEXPECTED_TOKEN | Wrong token | Syntax examples |
| TC_* | Type check error | Type examples or design doc |
| "undefined variable" | Missing import/letrec | Document pattern |
| EOF errors | Incomplete code | Model limitation |
| logic_error | Wrong output | Algorithm examples |

## Resources

### Gap Analysis Template
See [`resources/gap_analysis_template.md`](resources/gap_analysis_template.md) for structured analysis format.

### Common Patterns
See [`resources/common_patterns.md`](resources/common_patterns.md) for frequently encountered gaps.

## Progressive Disclosure

This skill loads information progressively:

1. **Always loaded**: This SKILL.md file (workflow overview)
2. **Execute as needed**: Scripts in `scripts/` directory
3. **Load on demand**: Resources for templates and patterns

## Notes

- Always test examples before adding to prompt
- Prefer fixing language over prompt workarounds
- Track improvements with before/after eval runs
- Create design docs for language limitations
- Update prompt hash in versions.json after changes
