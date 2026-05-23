# claims-validator

Validate documentation for unsupported claims, made-up metrics, and unverifiable statements.

## Triggers

- "check for unsupported claims"
- "validate claims"
- "review for BS"
- "check metrics"
- "verify claims in this document"
- "find made-up stats"

## Purpose

This skill identifies statements that make claims without evidence, including:
- Performance metrics without benchmarks or data
- Time/cost estimates without basis
- Percentage claims without citation
- Comparative statements without baselines
- Features described as implemented that don't exist
- Marketing superlatives presented as facts

## Behavior

When triggered, this skill:

1. **Scans for metric claims**:
   - Percentage improvements ("40% faster", "reduces by 60%")
   - Time estimates ("saves 2-3 hours", "in minutes not hours")
   - Cost projections ("$50-150/month", "ROI of 3x")
   - Performance numbers ("99x faster", "sub-millisecond")

2. **Identifies unsupported comparatives**:
   - "faster than", "better than", "more efficient"
   - "best", "leading", "revolutionary", "game-changing"
   - "comprehensive", "complete", "full-featured"

3. **Checks for feature claims**:
   - Commands or flags mentioned that don't exist in codebase
   - Features described in present tense that aren't implemented
   - Integration claims without actual integration code

4. **Validates citations**:
   - Claims that reference data should have sources
   - Benchmarks should link to methodology
   - Statistics should be reproducible

5. **Generates report**:
   - List each claim found
   - Classification (metric, comparative, feature, cost)
   - Recommendation (remove, add citation, verify, rephrase)

## Claim Categories

### Metrics Without Data

```markdown
# Flagged
"Time Saved: 92-96% (9-15 hours → 45-60 minutes)"
"99x faster routing"
"45x cache speedup"

# Problem
No benchmark data, methodology, or reproducible test

# Fix
Remove claim, or add: "Based on [benchmark/test], measured [how]"
```

### Cost Estimates Without Basis

```markdown
# Flagged
"Budget $20-50/month for moderate use"
"Light usage: ~$10-20/month"
"Enterprise teams may see $100-500+/month"

# Problem
No actual usage data, varies wildly by use case

# Fix
Remove specific numbers, or link to pricing calculator/methodology
```

### Time Estimates Without Data

```markdown
# Flagged
"Deploy Full SDLC Framework (2 Minutes)"
"5 minutes, replaces 2-4 hours manual work"
"campaign setup from 2-3 weeks → 1 week"

# Problem
No measurement, varies by project complexity

# Fix
Remove time claims, describe what it does instead
```

### Comparative Claims Without Baseline

```markdown
# Flagged
"faster than manual processes"
"more efficient than traditional approaches"
"better than existing solutions"

# Problem
No specific comparison, no baseline defined

# Fix
Remove comparison, or specify exactly what's being compared
```

### Feature Claims for Unimplemented Features

```markdown
# Flagged
"aiwg -migrate-workspace  # Optional migration tool"
"Run 'config-validator --fix' to apply automated fixes"

# Problem
Command doesn't exist in codebase

# Fix
Remove until implemented, or mark as "Planned:"
```

### Marketing Superlatives

```markdown
# Flagged
"comprehensive", "revolutionary", "game-changing"
"best-in-class", "industry-leading", "cutting-edge"
"seamless", "effortless", "zero-friction"

# Problem
Subjective claims that can't be verified

# Fix
Replace with specific, factual descriptions
```

## Validation Report Format

```markdown
# Claims Validation Report

**Document**: README.md
**Date**: 2025-12-09
**Claims Found**: 12
**Issues**: 8

## Summary

| Category | Found | Unsupported | Action Needed |
|----------|-------|-------------|---------------|
| Metrics | 5 | 4 | Remove or cite |
| Time estimates | 3 | 3 | Remove |
| Cost estimates | 2 | 2 | Remove |
| Comparatives | 1 | 1 | Rephrase |
| Features | 1 | 1 | Remove (not implemented) |

## Issues

### 1. Unsupported Metric
**Line 204**: "Time Savings: 20-98% reduction across 5 core use cases"
**Problem**: No benchmark data or methodology
**Action**: Remove claim

### 2. Cost Estimate Without Data
**Line 1180**: "Light usage: ~$10-20/month"
**Problem**: No actual usage data to support estimate
**Action**: Remove specific numbers

### 3. Non-existent Feature
**Line 583**: "aiwg -migrate-workspace"
**Problem**: Command not implemented
**Action**: Remove until implemented

## Recommendations

1. **Remove all percentage-based time savings claims**
2. **Remove cost estimates** - direct users to measure their own usage
3. **Remove non-existent commands** - only document what exists
4. **Replace superlatives with specifics** - say what it does, not how good it is
```

## Usage Examples

### Validate a Document

```
User: "Check README.md for unsupported claims"

Output:
"Claims Validation: README.md

Found 8 unsupported claims:

Metrics (4):
- Line 204: '20-98% reduction' - no data
- Line 362: '56-63% time saved' - no data
- Line 588: '99x faster routing' - no benchmark
- Line 589: '45x cache speedup' - no benchmark

Time Estimates (2):
- Line 187: '5 minutes, replaces 2-4 hours' - unmeasured
- Line 366: '2 Minutes' in heading - varies by project

Non-existent Features (2):
- Line 583: 'aiwg -migrate-workspace' - not implemented
- Line 651: 'aiwg -rollback-workspace' - not implemented

Recommendation: Remove these claims. Describe what features
do, not how much time/money they save."
```

### Quick Check

```
User: "Any BS in this section?"

Output:
"Found 2 issues:

1. 'Revolutionary approach' - marketing speak, be specific
2. '10x productivity gain' - no measurement

Suggest: Replace with factual descriptions of functionality."
```

## Integration

This skill complements:
- **Voice Framework**: Voice defines *how* to write, claims-validator checks *what* you claim
- **config-validator**: Validates config files, claims-validator validates prose claims

## What This Skill Does NOT Flag

- Factual descriptions of features that exist
- Documented benchmarks with methodology
- Qualified statements ("may vary", "depending on", "in our testing")
- User testimonials clearly attributed
- Comparative claims with specific baselines cited

## Output Location

- Validation reports: `.aiwg/reports/claims-validation.md`
