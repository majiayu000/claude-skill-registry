---
name: llm-judge
description: LLM-as-judge methodology for comparing code implementations across repositories. Scores implementations on functionality, security, test quality, overengineering, and dead code using weighted rubrics. Used by /beagle:llm-judge command.
---

# LLM Judge Skill

Compare code implementations across 2+ repositories using structured evaluation.

## Overview

This skill implements a two-phase LLM-as-judge evaluation:

1. **Phase 1: Fact Gathering** - Parallel agents explore each repo and extract structured facts
2. **Phase 2: Judging** - Parallel judges score each dimension using consistent rubrics

## Reference Files

| File | Purpose |
|------|---------|
| [references/fact-schema.md](references/fact-schema.md) | JSON schema for Phase 1 facts |
| [references/scoring-rubrics.md](references/scoring-rubrics.md) | Detailed rubrics for each dimension |
| [references/repo-agent.md](references/repo-agent.md) | Instructions for Phase 1 agents |
| [references/judge-agents.md](references/judge-agents.md) | Instructions for Phase 2 judges |

## Scoring Dimensions

| Dimension | Default Weight | Evaluates |
|-----------|----------------|-----------|
| Functionality | 30% | Spec compliance, test pass rate |
| Security | 25% | Vulnerabilities, security patterns |
| Test Quality | 20% | Coverage, DRY, mock boundaries |
| Overengineering | 15% | Unnecessary complexity |
| Dead Code | 10% | Unused code, TODOs |

## Scoring Scale

| Score | Meaning |
|-------|---------|
| 5 | Excellent - Exceeds expectations |
| 4 | Good - Meets requirements, minor issues |
| 3 | Average - Functional but notable gaps |
| 2 | Below Average - Significant issues |
| 1 | Poor - Fails basic requirements |

## Phase 1: Spawning Repo Agents

For each repository, spawn a Task agent with:

```
You are a Phase 1 Repo Agent for the LLM Judge evaluation.

**Your Repo:** $REPO_LABEL at $REPO_PATH
**Spec Document:**
$SPEC_CONTENT

**Instructions:** Read @beagle:llm-judge references/repo-agent.md

Gather facts and return a JSON object following the schema in references/fact-schema.md.

Load @beagle:llm-artifacts-detection for dead code and overengineering analysis.

Return ONLY valid JSON, no markdown or explanations.
```

## Phase 2: Spawning Judge Agents

After all Phase 1 agents complete, spawn 5 judge agents (one per dimension):

```
You are the $DIMENSION Judge for the LLM Judge evaluation.

**Spec Document:**
$SPEC_CONTENT

**Facts from all repos:**
$ALL_FACTS_JSON

**Instructions:** Read @beagle:llm-judge references/judge-agents.md

Score each repo on $DIMENSION using the rubric in references/scoring-rubrics.md.

Return ONLY valid JSON following the judge output schema.
```

## Aggregation

After Phase 2 completes:

1. Collect scores from all 5 judges
2. For each repo, compute weighted total:
   ```
   weighted_total = sum(score[dim] * weight[dim]) / 100
   ```
3. Rank repos by weighted total (descending)
4. Generate verdict explaining the ranking

## Output

Write results to `.beagle/llm-judge-report.json` and display markdown summary.

## Dependencies

- `@beagle:llm-artifacts-detection` - Reused by repo agents for dead code/overengineering
