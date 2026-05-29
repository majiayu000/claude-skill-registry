---
name: compound
description: Capture and apply knowledge from course development to improve future runs.
license: MIT
metadata:
  author: Andamio
  version: 1.0.0
---

# Skill: Compound Knowledge

## Description
Extracts patterns, heuristics, and calibration data from course development artifacts. Feeds knowledge back into `/draft-slts`, `/assess-slts`, `/self-assess-readiness`, and `/classify-lesson-types` to make each run smarter than the last.

## Invocation Modes

```
/compound                          # Interactive: asks what to compound
/compound quality-review           # Compound from specific phase
/compound readiness                # Compound from readiness assessment
/compound classification           # Compound from lesson type classification
/compound --course=go-pbl --rollup # Full course retrospective
```

## Instructions

### Path Resolution

Resolve file paths based on your execution context:

- **Plugin context** (`${CLAUDE_PLUGIN_ROOT}` is set): Read knowledge from `${CLAUDE_PLUGIN_DATA}/knowledge/` (user data), falling back to `${CLAUDE_PLUGIN_ROOT}/knowledge/` (seed data). **Write all knowledge updates to `${CLAUDE_PLUGIN_DATA}/knowledge/`** — never modify the plugin's bundled seed data.
- **Clone/symlink context** (default): Read and write knowledge at `knowledge/` relative to the project root.

All `knowledge/` paths referenced below follow this resolution. In plugin context, substitute the appropriate prefix.

### Phase Selection

If invoked without arguments, present phase options:

```markdown
## What would you like to compound?

| # | Phase | Source Artifact | Extracts |
|---|-------|-----------------|----------|
| 1 | quality-review | 02-slts-quality-review.md, 01-slts.md | Successful rewrites, quality issues |
| 2 | readiness | 05-readiness-assessment.md | Tier distribution, context shopping list |
| 3 | classification | 04-lesson-type-classification.md | Verb patterns, edge cases, heuristics |
| 4 | lesson-build | lessons/*.md | Actual vs self-assessed confidence |
| 5 | context-add | assets/ + re-run readiness | Which resources unlocked which SLTs |
| 6 | rollup | All artifacts | Full course retrospective |

Which phase? (Or specify course: --course=slug)
```

### Course Selection

If no course specified, scan `courses-in-progress/` and ask which course to compound from:

```markdown
## Select Course

| # | Course | Status | Artifacts Available |
|---|--------|--------|---------------------|
| 1 | andamio-for-contributors | building | 01, 02, 03, 04, 05 |
| 2 | andamio-for-api-developers | building | 01, 02, 03, 04, 05 |

Which course?
```

Also check `examples/` for seeding data (like `go-slts-readiness-assessment.md`).

### Extraction Logic by Phase

#### Phase: quality-review

**Source files:**
- `02-slts-quality-review.md` (assessment output)
- `01-slts.md` (revised SLTs, if exists)

**Extract:**

1. **Successful rewrites**: Compare SLTs between quality review suggestions and revised SLTs. For each rewrite:
   ```yaml
   - before: "original SLT text"
     after: "improved SLT text"
     issue_type: unmeasurable_verb | task_focused | too_broad | etc.
     key_change: "what made the difference"
     course: "course-slug"
     date: "YYYY-MM-DD"
   ```
   Append to `knowledge/slt-patterns/successful-rewrites.yaml`

2. **Quality issues**: Extract patterns from "Needs Work" SLTs:
   ```yaml
   - pattern: "how to detect"
     description: "what the problem is"
     impact: ["Student-Facing Language", "Specificity"]
     frequency: 1
     example_bad: "I can understand blockchain"
     example_fix: "I can explain how a blockchain maintains data integrity by identifying three mechanisms"
     courses_seen_in: ["course-slug"]
   ```
   Append to `knowledge/slt-patterns/quality-issues.yaml`

3. **Verb effectiveness**: Extract verbs from "Strong" SLTs and add to verb bank:
   ```yaml
   - verb: "compare"
     bloom_level: analyze
     success_count: 1
     example_slts: ["I can compare X to Y by identifying..."]
   ```
   Update `knowledge/slt-patterns/verb-bank.yaml`

#### Phase: readiness

**Source files:**
- `05-readiness-assessment.md`
- `examples/go-slts-readiness-assessment.md` (for seeding)

**Extract:**

1. **Context leverage**: Parse the Context Shopping List and update rankings:
   ```yaml
   - resource: "Apollo API reference + transaction building examples"
     type: "Docs + Example Code"
     slts_unlocked: ["102.2", "102.3", "102.5", "102.6", ...]
     priority: High
     obtained: false
     effectiveness: null
   ```
   Update `knowledge/readiness/context-leverage.yaml`

2. **Calibration baseline**: Record self-assessed tiers for later comparison:
   ```yaml
   - slt_id: "go-pbl:099.1"
     self_assessed: Ready
     actual_outcome: null  # filled in after lesson-build
     dimensions_off: null
     notes: null
     date: "YYYY-MM-DD"
   ```
   Append to `knowledge/readiness/calibration.yaml`

#### Phase: classification

**Source files:**
- `04-lesson-type-classification.md`

**Extract:**

1. **Verb patterns**: From the Heuristics Developed section:
   ```yaml
   - verb: "explain"
     suggests: exploration
     confidence: high
     count: 1
     examples: ["I can explain why Bursa was built..."]
   ```
   Update `knowledge/lesson-types/heuristics.yaml`

2. **Subject patterns**: From topic clusters:
   ```yaml
   - keywords: ["API", "endpoint", "library"]
     suggests: developer_documentation
     confidence: high
     count: 1
     examples: ["I can build a web API using Fiber..."]
   ```
   Update `knowledge/lesson-types/heuristics.yaml`

3. **Edge cases**: From ambiguous classifications:
   ```yaml
   - slt: "I can set up my development environment..."
     candidates: ["how_to_guide", "organization_onboarding"]
     chosen: how_to_guide
     deciding_factor: "Generic procedure, not org-specific"
     question_that_helped: "Would this SLT exist in a generic course?"
     course: "course-slug"
     date: "YYYY-MM-DD"
   ```
   Append to `knowledge/lesson-types/edge-cases.yaml`

#### Phase: lesson-build

**Source files:**
- `lessons/*.md`
- `05-readiness-assessment.md` (for comparison)

**Extract:**

1. **Calibration updates**: Compare actual lesson-building experience to self-assessed readiness:
   ```yaml
   - slt_id: "course:module.slt"
     self_assessed: Ready
     actual_outcome: success | partial | failure
     dimensions_off: ["Code Demo was actually Weak"]
     notes: "Apollo API changed since training"
     date: "YYYY-MM-DD"
   ```
   Update existing entries in `knowledge/readiness/calibration.yaml`

2. **Compute calibration stats**: After updating entries:
   - Calculate accuracy_rate
   - Identify common_overconfidence patterns
   - Identify common_underconfidence patterns
   - Generate adjustment rules

#### Phase: context-add

**Source files:**
- `assets/` (newly added context)
- Re-run `/self-assess-readiness` (or compare to previous)

**Extract:**

1. **Context effectiveness**: For resources that were obtained:
   ```yaml
   - resource: "gOuroboros README"
     obtained: true
     effectiveness: confirmed | partial | unhelpful
     notes: "Unlocked 4/5 expected SLTs, one still needs examples"
   ```
   Update `knowledge/readiness/context-leverage.yaml`

#### Phase: rollup

Run all extraction phases for a single course. Produce a summary report:

```markdown
## Compound Report: [Course Name]

### Knowledge Captured

| Category | Count | Files Updated |
|----------|-------|---------------|
| Successful Rewrites | 3 | successful-rewrites.yaml |
| Quality Issues | 2 | quality-issues.yaml |
| Verb Bank Entries | 5 | verb-bank.yaml |
| Context Resources | 8 | context-leverage.yaml |
| Calibration Entries | 12 | calibration.yaml |
| Lesson Type Heuristics | 4 | heuristics.yaml |
| Edge Cases | 2 | edge-cases.yaml |

### Aggregate Stats Update

- Courses processed: [n]
- Total SLTs analyzed: [n]
- Successful rewrites captured: [n]
- Calibration accuracy: [%]

### Top Insights

1. [Most impactful pattern discovered]
2. [Second most impactful]
3. [Third most impactful]
```

### Output Format

After extraction, always report:

```markdown
## Compound Complete

**Phase:** [phase name]
**Course:** [course name]

### Extracted

| Knowledge Type | Count | Status |
|----------------|-------|--------|
| [type] | [n] | Added / Updated / Unchanged |

### Files Modified

- `knowledge/slt-patterns/successful-rewrites.yaml` - Added 2 entries
- `knowledge/readiness/context-leverage.yaml` - Updated 3 entries

### Index Updated

- `last_updated`: [timestamp]
- `slts_analyzed`: [new total]
```

### Knowledge Consumption Check

Before modifying knowledge files, read the current state. When updating:
- **Increment counts** (don't reset)
- **Append to lists** (don't overwrite)
- **Merge patterns** (combine evidence from multiple courses)
- **Deduplicate** (same pattern from different courses = one entry with multiple course references)

### Integration Points

This skill produces knowledge that other skills consume:

| Skill | Reads From | Uses For |
|-------|------------|----------|
| `/draft-slts` | verb-bank.yaml, quality-issues.yaml | Prefer effective verbs, avoid problematic patterns |
| `/assess-slts` | quality-issues.yaml, successful-rewrites.yaml | Flag known issues, suggest proven fixes |
| `/self-assess-readiness` | calibration.yaml, context-leverage.yaml | Adjust confidence, prioritize shopping list |
| `/classify-lesson-types` | heuristics.yaml, edge-cases.yaml | Improve initial guesses, handle known ambiguities |

### Guidelines

- **Always read before writing.** Load current YAML state before appending.
- **Preserve existing data.** Never overwrite — merge and increment.
- **Be specific in patterns.** Vague patterns don't compound.
- **Update the index.** Always update `knowledge/index.yaml` stats after any extraction.
- **Report what changed.** The user should see exactly what knowledge was captured.
- **Seed from examples.** Use `examples/go-slts-readiness-assessment.md` to prime the knowledge base.
