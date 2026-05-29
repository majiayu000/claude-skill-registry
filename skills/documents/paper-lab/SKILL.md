---
name: paper-lab
description: >
  Self-improving documentation convergence loop. Computes quality deltas between
  review rounds, identifies recurring issues, applies targeted fixes, and converges
  on quality thresholds. Uses /review-paper as the quality signal and /create-paper
  or direct editing for fixes. Tracks convergence trajectory across rounds.
allowed-tools: [Bash, Read, Write, Edit, Task, Glob, Grep]
triggers:
  - paper lab
  - improve documentation
  - converge documentation
  - self improve docs
  - iterate on docs
  - documentation convergence
  - doc quality loop
  - improve paper
  - fix documentation issues
  - documentation self improvement
  - iterate paper
  - paper convergence
metadata:
  short-description: Self-improving documentation with convergence + write-back
  author: "Embry Lawson (The Aerospace Corporation)"
  version: "1.0.0"

provides:
  - paper-lab
composes:
  - review-paper
  - memory
  - scillm
  - create-paper
  - task-monitor

taxonomy:
  - creation
  - iteration
  - self-improvement
---

# paper-lab

Self-improving documentation convergence loop. Takes a document, reviews it via
`/review-paper`, computes the quality delta, applies targeted fixes, reviews again,
and repeats until quality converges above threshold or max rounds are exhausted.

## Why This Exists

Documentation quality is exactly the kind of problem that benefits from convergence
loops. Each round of `/review-paper` identifies issues. Each fix addresses some issues
but may introduce new ones. `/paper-lab` tracks the delta between rounds and knows
when to stop — either because quality has converged above threshold, or because
further iteration yields diminishing returns.

Same pattern as `/pdf-lab` (extraction convergence) and `/prompt-lab` (prompt
evaluation convergence), applied to written documentation.

## Quick Start

```bash
# Main: review, fix, review, converge
/paper-lab tune docs/ARCHITECTURE.md --threshold 8.5 --max-rounds 3

# Dry run: review and compute deltas without writing fixes
/paper-lab tune docs/ARCHITECTURE.md --threshold 8.5 --dry-run

# Focus on specific dimensions
/paper-lab tune docs/API_REFERENCE.md --threshold 9.0 --dimensions accuracy,completeness

# Focus on specific personas
/paper-lab tune docs/ARCHITECTURE.md --focus brandon,margaret --threshold 8.5

# With doc-code alignment verification each round
/paper-lab tune docs/API_REFERENCE.md --verify-code --threshold 9.0

# Status: show convergence history
/paper-lab status docs/ARCHITECTURE.md

# Compare two documents' convergence trajectories
/paper-lab compare docs/ARCHITECTURE.md docs/API_REFERENCE.md
```

## Convergence Loop Architecture

```
Round 0: Initial State
    |
    v
+-------------------------------------------+
|  /review-paper docs/ARCHITECTURE.md       |
|  --verify-code --format json --round N    |
+-------------------------------------------+
    |
    v
+-------------------------------------------+
|  Compute Delta                            |
|  - Score delta vs previous round          |
|  - New issues found                       |
|  - Issues resolved since last round       |
|  - Recurring issues (appeared 2+ rounds)  |
|  - Convergence rate (delta / round)       |
+-------------------------------------------+
    |
    v
+-------------------------------------------+
|  Convergence Check                        |
|  IF overall_score >= threshold: STOP      |
|  IF delta < epsilon (0.1): STOP           |
|  IF round >= max_rounds: STOP             |
|  IF score regressed 2 rounds: STOP        |
|  ELSE: continue to fix phase              |
+-------------------------------------------+
    |
    v
+-------------------------------------------+
|  Fix Phase                                |
|  - Prioritize HIGH severity issues first  |
|  - Apply targeted edits to document       |
|  - Each fix attributed to reviewing       |
|    persona (git trailer)                  |
|  - Verify fix doesn't break cross-refs    |
+-------------------------------------------+
    |
    v
+-------------------------------------------+
|  /review-paper (Round N+1)                |
|  Loop back to top                         |
+-------------------------------------------+
```

## Convergence Criteria

The loop stops when ANY of these conditions are met:

| Condition | Threshold | Rationale |
|-----------|-----------|-----------|
| **Quality met** | `overall_score >= threshold` | Target quality achieved |
| **Converged** | `abs(delta) < epsilon` (default: 0.1) | Further iteration won't improve |
| **Max rounds** | `round >= max_rounds` (default: 5) | Budget exhausted |
| **Regression** | Score decreased for 2 consecutive rounds | Edits are making it worse |
| **Diminishing returns** | `delta / round < 0.05` after round 2 | Not worth the compute |

## Delta Computation

Between rounds N-1 and N:

```json
{
  "round": 2,
  "previous_score": 7.8,
  "current_score": 8.4,
  "delta": 0.6,
  "convergence_rate": 0.3,
  "issues": {
    "resolved": [
      {"id": "R1-H1", "description": "Cascade depth 5 vs 3", "fixed_in_round": 2}
    ],
    "new": [
      {"id": "R2-M1", "description": "New env var EMBRY_LOG_LEVEL undocumented"}
    ],
    "recurring": [],
    "total_open": 3,
    "total_resolved": 4
  },
  "dimension_deltas": {
    "accuracy": {"prev": 8.0, "curr": 9.0, "delta": 1.0},
    "voice": {"prev": 8.0, "curr": 8.0, "delta": 0.0},
    "completeness": {"prev": 7.0, "curr": 8.0, "delta": 1.0},
    "cross_references": {"prev": 9.0, "curr": 10.0, "delta": 1.0},
    "compliance": {"prev": 8.0, "curr": 8.5, "delta": 0.5}
  },
  "persona_deltas": {
    "embry": {"prev": 8.2, "curr": 8.6, "delta": 0.4},
    "brandon": {"prev": 7.5, "curr": 8.3, "delta": 0.8},
    "margaret": {"prev": 7.8, "curr": 8.5, "delta": 0.7},
    "jennifer": {"prev": 8.0, "curr": 8.2, "delta": 0.2}
  }
}
```

## Fix Strategies

Fixes are applied in priority order:

| Priority | Issue Type | Fix Strategy |
|----------|-----------|--------------|
| 1 | **Doc-code discrepancy** | Read source file, update documentation to match code |
| 2 | **Broken cross-reference** | Fix link target or remove dead reference |
| 3 | **Missing content** | Generate from source code using persona voice |
| 4 | **Accuracy error** | Verify against source, correct claim |
| 5 | **Voice drift** | Rewrite section in persona's voice using their manifest as guide |
| 6 | **Completeness gap** | Add missing endpoints/signals/env vars from source scan |

### Fix Attribution

Every edit includes a comment identifying which persona flagged the issue:

```markdown
<!-- Fixed in paper-lab round 2: Brandon flagged cascade depth as 5, code uses 3 -->
```

For git commits (when `--commit` is enabled):

```
fix(docs): correct cascade traversal depth to match implementation

Reviewed-By: Brandon Bailey (SPARTA)
Issue: R1-H1 (cascade depth 5 vs 3 in sparta-daemon/main.py:142)
Paper-Lab-Round: 2
```

## Commands

### `tune` - Run Convergence Loop

```bash
/paper-lab tune <document> [OPTIONS]

Options:
  --threshold FLOAT    Target overall score (default: 8.5)
  --max-rounds INT     Maximum review rounds (default: 5)
  --epsilon FLOAT      Minimum delta to continue (default: 0.1)
  --dimensions TEXT     Focus dimensions (accuracy, voice, completeness, cross_references, compliance)
  --focus TEXT          Focus personas (embry, brandon, margaret, jennifer)
  --verify-code        Enable doc-code alignment each round
  --dry-run            Review and compute deltas without writing fixes
  --commit             Git commit after each fix round
  --provider TEXT       LLM provider for review (claude, codex, gemini, copilot)
  --output PATH        Output directory for convergence data
```

### `status` - Show Convergence History

```bash
/paper-lab status <document>

Output:
  Round 1: 7.2/10 (baseline)
  Round 2: 8.4/10 (+1.2, 4 issues resolved, 1 new)
  Round 3: 8.7/10 (+0.3, 2 issues resolved, 0 new) <- converged

  Trajectory: CONVERGING
  Rounds to threshold (8.5): achieved at round 2
  Recurring issues: none
  Total issues resolved: 6/7 (85.7%)
```

### `compare` - Compare Document Trajectories

```bash
/paper-lab compare docs/ARCHITECTURE.md docs/API_REFERENCE.md

Output:
  ARCHITECTURE.md: 3 rounds, 7.2 -> 8.7 (+1.5), converged
  API_REFERENCE.md: 2 rounds, 8.1 -> 8.9 (+0.8), converged

  Weakest shared dimension: completeness (avg 7.5)
  Strongest shared dimension: cross_references (avg 9.8)
```

### `diagnose` - Identify Stalled Dimensions

```bash
/paper-lab diagnose docs/ARCHITECTURE.md

Output:
  Stalled dimensions (delta < 0.1 for 2+ rounds):
    - voice (8.0 -> 8.0 -> 8.1): Persona voice is stable, minor improvements only
    - compliance (8.5 -> 8.5 -> 8.5): At ceiling for current content

  Improving dimensions:
    - accuracy (7.0 -> 8.5 -> 9.0): Strong upward trajectory
    - completeness (6.5 -> 7.5 -> 8.0): Steady improvement

  Recommendation: Focus next round on completeness (most room to grow)
```

### `rollback` - Revert to Previous Round

```bash
/paper-lab rollback docs/ARCHITECTURE.md --round 2
```

Reverts the document to the state after round 2 fixes. Requires git history.

## Convergence Visualization

When `--output` is specified, generates a convergence chart:

```
Score
10 |
 9 |                          *---*  (converged at 8.7)
 8 |              *----------*
 7 |  *----------*
 6 |
   +---+---+---+---+---+---
     R0  R1  R2  R3  R4  R5
                        Round

 Legend: * overall_score
 Threshold: ---- 8.5
 Epsilon: delta < 0.1 triggers stop
```

## Memory Integration

### Pre-hook: `recall_prior_convergence(document_name)`
- Recalls past convergence results for this document
- Loads recurring issues that persisted across previous convergence runs
- Retrieves optimal fix strategies that worked before
- Skips fix strategies that previously failed (negative learning)

### Post-hook: `learn_convergence(document, rounds, trajectory, final_score)`
- Stores convergence outcome: rounds needed, final score, fix strategies that worked
- Tags: `["paper_lab", "convergence", "documentation"] + persona_tags`
- Bridge keywords: Precision (accuracy fixes), Resilience (convergence success), Fragility (regression detection), Corruption (voice drift)

### Cross-Document Learning
When fixing document A reveals a pattern (e.g., "socket paths were wrong in 3 daemons"),
the memory entry enables paper-lab to check document B for the same class of error
before even running a review round.

## Integration with Other Skills

| Skill | Role in Convergence |
|-------|-------------------|
| `/review-paper` | Quality signal — provides per-round scores and issue lists |
| `/create-paper` | Can generate replacement sections when completeness is low |
| `/memory` | Convergence history, recurring issues, fix strategy recall |
| `/assess` | Doc-code alignment substrate for `--verify-code` |
| `/scillm` | LLM calls for voice rewriting and content generation |
| `/create-figure` | Regenerate diagrams if figure references are broken |

## Example Session

```
$ /paper-lab tune docs/ARCHITECTURE.md --threshold 8.5 --verify-code --max-rounds 3

[PAPER-LAB] Starting convergence loop for docs/ARCHITECTURE.md
[PAPER-LAB] Threshold: 8.5 | Max rounds: 3 | Epsilon: 0.1
[PAPER-LAB] Recalling prior convergence data...
[MEMORY] No prior convergence found for ARCHITECTURE.md

--- Round 1: Review ---
[REVIEW-PAPER] Analyzing docs/ARCHITECTURE.md...
[REVIEW-PAPER] Personas: embry, brandon, margaret, jennifer
[REVIEW-PAPER] Doc-code alignment: checking 7 daemon source files...

[ROUND 1] Score: 7.8/10
  HIGH: Cascade depth documented as 5, code uses 3 (brandon)
  HIGH: Missing EMBRY_LOG_LEVEL env var in config section (embry)
  MEDIUM: Extraction batch quality scores not included (margaret)
  MEDIUM: DISA STIG reference missing revision number (jennifer)
  LOW: Skill count "200+" should be specific (embry)

[PAPER-LAB] Delta: +7.8 (baseline)
[PAPER-LAB] Applying fixes...
  [FIX] Updated cascade depth 5 -> 3 (line 139)
  [FIX] Added EMBRY_LOG_LEVEL to config section
  [FIX] Added batch-3 quality score (89% PASS) to Section 6
  [FIX] Updated DISA STIG V-222659 with revision
  [FIX] Updated skill count to 217

--- Round 2: Review ---
[REVIEW-PAPER] Re-analyzing docs/ARCHITECTURE.md...

[ROUND 2] Score: 8.6/10 (+0.8)
  MEDIUM: New env var EMBRY_DATALAKE_MAX_PAGES undocumented (margaret)
  LOW: Brandon's voice could be more skeptical in security section (brandon)

[PAPER-LAB] Delta: +0.8
[PAPER-LAB] Score 8.6 >= threshold 8.5
[PAPER-LAB] CONVERGED at round 2

--- Summary ---
  Rounds: 2
  Score: 7.8 -> 8.6 (+0.8)
  Issues resolved: 5/7 (71.4%)
  Issues remaining: 2 (1 medium, 1 low)
  Convergence: ABOVE THRESHOLD

[MEMORY] Stored convergence result for ARCHITECTURE.md
```

## Environment

| Variable | Purpose |
|----------|---------|
| `PAPER_LAB_OUTPUT_DIR` | Default output directory (default: `paper_lab_output/`) |
| `PAPER_LAB_THRESHOLD` | Default convergence threshold (default: 8.5) |
| `PAPER_LAB_MAX_ROUNDS` | Default max rounds (default: 5) |
| `PAPER_LAB_EPSILON` | Default minimum delta (default: 0.1) |

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `/review-paper` | Quality signal (called each round) |
| `/pdf-lab` | Sister skill: same convergence pattern for PDF extraction |
| `/prompt-lab` | Sister skill: same convergence pattern for LLM prompts |
| `/classifier-lab` | Sister skill: same convergence pattern for classifiers |
| `/create-paper` | Upstream: creates documents that paper-lab improves |
| `/skill-lab` | Meta: paper-lab itself was created following skill-lab patterns |
