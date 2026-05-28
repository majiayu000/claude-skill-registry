---
name: llm-judge
description: "Use when comparing two or more code implementations against a spec or requirements doc. Triggers on \"which repo is better\", \"compare these implementations\", \"evaluate both solutions\", \"rank these codebases\", or \"judge which approach wins\". Also covers choosing between competing PRs or vendor submissions solving the same problem. Does NOT review a single codebase for quality \u2014 use code review skills instead. Does NOT evaluate strategy docs \u2014 use strategy-review. Requires a spec file and 2+ repo paths."
disable-model-invocation: true
---

# LLM Judge

Compare code implementations across multiple repositories using structured evaluation.

## Usage

```bash
/beagle-analysis:llm-judge <spec> <repo1> <repo2> [repo3...] [--labels=...] [--weights=...] [--branch=...]
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `spec` | Yes | Path to spec/requirements document |
| `repos` | Yes | 2+ paths to repositories to compare |
| `--labels` | No | Comma-separated labels (default: directory names) |
| `--weights` | No | Override weights, e.g. `functionality:40,security:30` |
| `--branch` | No | Branch to compare against main (default: `main`) |

## Workflow

1. Parse `$ARGUMENTS` into `spec_path`, `repo_paths`, `labels`, `weights`, and `branch`.
2. Validate the spec file, each repo path, and the minimum repo count.
3. Read the spec document into memory.
4. Load this skill and the supporting reference files.
5. Spawn one Phase 1 repo agent per repository to gather facts only.
6. Validate the repo-agent JSON results before proceeding.
7. Spawn one Phase 2 judge agent per dimension.
8. Aggregate scores, compute weighted totals, rank repos, and write the report.
9. Display the markdown summary and verify the JSON report.

## Hard gates

Sequenced workflow: **do not start the next phase until the current gate passes.** Each pass condition must be checkable (file on disk, non-empty content, or `json.load` succeeds)—not “I reviewed internally.”

| Gate | Pass condition | Unblocks |
|------|----------------|----------|
| **A — Inputs** | `spec_path` is a readable file and non-empty; `len(repo_paths) ≥ 2`; each path contains `.git`. | Phase 1 repo agents |
| **B — Phase 1 facts** | For **each** repo agent output: stdin/stdout parses as JSON; required keys/shape match `references/fact-schema.md`. | Phase 2 judge agents |
| **C — Phase 2 scores** | **Five** judge outputs (one per dimension) each parse as JSON; each includes a score (and justification) for **every** repo label. | Aggregation |
| **D — Report file** | `.beagle/llm-judge-report.json` exists; `python3 -c "import json; json.load(open('.beagle/llm-judge-report.json'))"` exits 0. | Markdown summary to the user |
| **E — Consistency** | Summary table and verdict use the same labels, weights, and per-dimension scores as the JSON report. | Mark task complete |

Parallelism is allowed **within** a phase (all Phase 1 tasks together; all Phase 2 tasks together), but Phase 2 must not start until Gate B passes, and the user-visible summary must not precede Gate D.

## Command Workflow

### Step 1: Parse Arguments

Parse `$ARGUMENTS` to extract:
- `spec_path`: first positional argument
- `repo_paths`: remaining positional arguments (must be 2+)
- `labels`: from `--labels` or derived from directory names
- `weights`: from `--weights` or defaults
- `branch`: from `--branch` or `main`

**Default Weights:**

```json
{
  "functionality": 30,
  "security": 25,
  "tests": 20,
  "overengineering": 15,
  "dead_code": 10
}
```

### Step 2: Validate Inputs

```bash
[ -f "$SPEC_PATH" ] || { echo "Error: Spec file not found: $SPEC_PATH"; exit 1; }

for repo in "${REPO_PATHS[@]}"; do
  [ -d "$repo/.git" ] || { echo "Error: Not a git repository: $repo"; exit 1; }
done

[ ${#REPO_PATHS[@]} -ge 2 ] || { echo "Error: Need at least 2 repositories to compare"; exit 1; }
```

### Step 3: Read Spec Document

```bash
SPEC_CONTENT=$(cat "$SPEC_PATH") || { echo "Error: Failed to read spec file: $SPEC_PATH"; exit 1; }
[ -z "$SPEC_CONTENT" ] && { echo "Error: Spec file is empty: $SPEC_PATH"; exit 1; }
```

### Step 4: Load the Skill

Load the llm-judge skill: `Skill(skill: "beagle-analysis:llm-judge")`

### Step 5: Phase 1 - Spawn Repo Agents

Spawn one Task per repo:

```text
You are a Phase 1 Repo Agent for the LLM Judge evaluation.

**Your Repo:** $LABEL at $REPO_PATH

**Spec Document:**
$SPEC_CONTENT

**Instructions:**
1. Load skill: Skill(skill: "beagle-analysis:llm-judge")
2. Read references/repo-agent.md for detailed instructions
3. Read references/fact-schema.md for the output format
4. Load Skill(skill: "beagle-core:llm-artifacts-detection") for analysis

Explore the repository and gather facts. Return ONLY valid JSON following the fact schema.

Do NOT score or judge. Only gather facts.
```

Collect all repo outputs into `ALL_FACTS`.

### Step 6: Validate Phase 1 Results

```bash
echo "$FACTS" | python3 -c "import json,sys; json.load(sys.stdin)" 2>/dev/null || { echo "Error: Invalid JSON from $LABEL"; exit 1; }
```

### Step 7: Phase 2 - Spawn Judge Agents

Spawn five judge agents, one per dimension:

```text
You are the $DIMENSION Judge for the LLM Judge evaluation.

**Spec Document:**
$SPEC_CONTENT

**Facts from all repos:**
$ALL_FACTS_JSON

**Instructions:**
1. Load skill: Skill(skill: "beagle-analysis:llm-judge")
2. Read references/judge-agents.md for detailed instructions
3. Read references/scoring-rubrics.md for the $DIMENSION rubric

Score each repo on $DIMENSION. Return ONLY valid JSON with scores and justifications.
```

### Step 8: Aggregate Scores

```python
for repo_label in labels:
    scores[repo_label] = {}
    for dimension in dimensions:
        scores[repo_label][dimension] = judge_outputs[dimension]['scores'][repo_label]

    weighted_total = sum(
        scores[repo_label][dim]['score'] * weights[dim] / 100
        for dim in dimensions
    )
    scores[repo_label]['weighted_total'] = round(weighted_total, 2)

ranking = sorted(labels, key=lambda l: scores[l]['weighted_total'], reverse=True)
```

### Step 9: Generate Verdict

Name the winner, explain why they won, and note any close calls or trade-offs.

### Step 10: Write JSON Report

```bash
mkdir -p .beagle
```

Write `.beagle/llm-judge-report.json` with version, timestamp, repo metadata, weights, scores, ranking, and verdict.

### Step 11: Display Summary

Render a markdown summary with the scores table, ranking, verdict, and detailed justifications.

### Step 12: Verification

```bash
python3 -c "import json; json.load(open('.beagle/llm-judge-report.json'))" && echo "Valid report"
```

### Output Shape

The generated report should include:

- repo labels and paths
- per-dimension scores and justifications
- weighted totals and ranking
- a verdict explaining the winner

## Reference Files

| File | Purpose |
|------|---------|
| [references/fact-schema.md](references/fact-schema.md) | JSON schema for Phase 1 facts |
| [references/scoring-rubrics.md](references/scoring-rubrics.md) | Detailed rubrics for each dimension |
| [references/repo-agent.md](references/repo-agent.md) | Instructions for Phase 1 agents |
| [references/judge-agents.md](references/judge-agents.md) | Instructions for Phase 2 judges |

## Scoring Model

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

```text
You are a Phase 1 Repo Agent for the LLM Judge evaluation.

**Your Repo:** $REPO_LABEL at $REPO_PATH
**Spec Document:**
$SPEC_CONTENT

**Instructions:** Read @beagle:llm-judge references/repo-agent.md

Gather facts and return a JSON object following the schema in references/fact-schema.md.

Load @beagle:llm-artifacts-detection for dead code and overengineering analysis.

Return ONLY valid JSON, no markdown or explanations.
```

Collect all repo-agent outputs into `ALL_FACTS`.

## Phase 2: Spawning Judge Agents

After all Phase 1 agents complete, spawn 5 judge agents, one per dimension:

```text
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

1. Collect the five judge outputs.
2. Compute each repo's weighted total with the configured weights.
3. Rank repos by weighted total in descending order.
4. Generate a verdict that explains the result and any close calls.
5. Write `.beagle/llm-judge-report.json`.

## Output

Display a markdown summary with scores, ranking, verdict, and detailed justifications.

## Verification

Before completing (maps to **Hard gates** D and E):

1. **Gate D:** `.beagle/llm-judge-report.json` exists and `json.load` succeeds.
2. **Gate E / completeness:** Every repo label has scores for every dimension; each `weighted_total` equals the sum over dimensions of `(score × weight / 100)` using the configured weights; markdown summary matches the JSON report.

## Rules

- Always validate inputs before proceeding
- Spawn Phase 1 agents in parallel, then wait before Phase 2
- Spawn Phase 2 agents in parallel, one per dimension
- Every score must have a justification
- Write the JSON report before displaying the summary
