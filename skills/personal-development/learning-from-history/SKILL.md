---
name: learning-from-history
description: Analyzes history/ directories to extract patterns, writes learned rules to .claude/rules/learned/ (auto-loaded), updates CLAUDE.local.md with personal preferences.
---

# Learning from History

## Overview

Mines patterns from versioned outputs in history/ directories. Extracts success patterns, failure patterns, and personal preferences. Writes findings to `.claude/rules/learned/` (auto-loaded by Claude Code) and `CLAUDE.local.md` (personal preferences).

This skill closes the "Learn" loop : Observe → Think → Plan → Build → Execute → Verify → **Learn** → Improve.

## When to Use

- **Automatic:** Triggered weekly by session hook
- **Manual:** When you want to analyze a specific skill's history
- **After major milestone:** Post-launch, post-quarter, post-strategy cycle

## Core Pattern

**Step 1: Identify Analysis Scope**

Ask user (or determine from hook trigger):
- "Which skill should I analyze?" (e.g., generating-quarterly-charters)
- "What time period?" (e.g., last 6 months, all time)
- "Looking for anything specific?" (e.g., what makes charters get approved?)

**Step 2: Read History Files**

For the target skill, read all files in `history/[skill-name]/`:
- Count total outputs
- Note date range
- Identify versions (e.g., charter v1, v2, v3)

Also read related decision logs:
- `outputs/decisions/*.md` for outcome data
- Look for feedback ratings, success/failure notes

**Step 3: Pattern Detection**

Analyze for:

### Success Patterns
- What do successful outputs have in common?
- Format patterns (tables vs bullets, length, structure)
- Content patterns (evidence types, specificity, metrics format)
- Process patterns (review cycles, stakeholder involvement)

### Failure Patterns
- What do rejected/reworked outputs have in common?
- What causes revisions?
- What warnings were ignored?

### Personal Preferences
- User's consistent choices (format, detail level, tone)
- User's typical review cycle
- User's stakeholder patterns
- User's domain-specific patterns

**Step 4: Quantify Patterns**

For each pattern, provide evidence:
- **Sample size:** N outputs analyzed
- **Correlation:** X/Y successful outputs had this pattern
- **Confidence:** Strong (>80%), Medium (50-80%), Weak (<50%)

**Example:**
"Charters with ≤3 strategic bets: 10/12 approved on first review (83% → Strong correlation)"

**Step 5: Generate Learned Rules File**

Write to `.claude/rules/learned/[skill-name]-patterns.md`:

```markdown
---
generated: YYYY-MM-DD HH:MM
skill: learning-from-history
analyzed_skill: [skill-name]
sample_size: [N]
date_range: [YYYY-MM-DD to YYYY-MM-DD]
paths:
  - "outputs/[output-dir]/**/*.md"
  - "history/[skill-name]/**/*.md"
---

# Learned Patterns: [Skill Name]

## Analysis Summary
- **Outputs analyzed:** [N] files from history/[skill-name]/
- **Time period:** [Date range]
- **Outcomes tracked:** [M] decision logs with results
- **Confidence:** Patterns based on [N] data points

## Success Patterns (Correlate with Approved/Successful Outputs)

### Pattern 1: [Title]
**Observation:** [What we see in successful outputs]
**Evidence:** [X/Y] successful outputs had this ([%])
**Recommendation:** Default to this pattern

**Example from history:**
```
[Snippet from successful output showing pattern]
```

### Pattern 2: [Title]
**Observation:** [What we see]
**Evidence:** [X/Y] successful outputs ([%])
**Recommendation:** [What to do]

## Failure Patterns (Correlate with Rejected/Reworked Outputs)

### Anti-Pattern 1: [Title]
**Observation:** [What we see in failed outputs]
**Evidence:** [X/Y] rejected outputs had this ([%])
**Recommendation:** Avoid this pattern

**Example from history:**
```
[Snippet from rejected output showing anti-pattern]
```

### Anti-Pattern 2: [Title]
**Observation:** [What we see]
**Evidence:** [X/Y] rejected outputs ([%])
**Recommendation:** [What to avoid]

## Recommendations for [Skill Name]

Based on analysis of [N] outputs:

1. **[Recommendation 1]:** [Specific guidance]
   - Evidence: [X/Y outputs ([%])]
   - Confidence: Strong/Medium/Weak

2. **[Recommendation 2]:** [Specific guidance]
   - Evidence: [X/Y outputs ([%])]
   - Confidence: Strong/Medium/Weak

3. **[Recommendation 3]:** [Specific guidance]
   - Evidence: [X/Y outputs ([%])]
   - Confidence: Strong/Medium/Weak

## Quality Trends Over Time

| Time Period | Outputs | Approved First Try | Avg Revisions | Quality Trend |
|-------------|---------|-------------------|---------------|---------------|
| [Q1 YYYY] | [N] | [%] | [N] | ↗/→/↘ |
| [Q2 YYYY] | [N] | [%] | [N] | ↗/→/↘ |
| [Q3 YYYY] | [N] | [%] | [N] | ↗/→/↘ |

**Trend:** [Improving / Stable / Declining]
**Why:** [Hypothesis about cause]

## Unknowns / Need More Data

- [Pattern needs more data points to confirm]
- [Outcome data missing for X outputs]
- [Confounding variable Y not tracked]

## Next Analysis
Run this analysis again after [N more outputs] or [time period] to validate patterns.
```

**Step 6: Update Personal Preferences**

Append or update `CLAUDE.local.md`:

```markdown
# Learned Preferences (from history analysis)

## [Skill Name] Preferences
**Last updated:** YYYY-MM-DD
**Based on:** [N] outputs

- User prefers [format/style choice] ([X/Y times, [%]])
- User's typical review cycle: [N rounds before approval]
- User always requests [specific thing] ([observed pattern])
- User's common stakeholders: [Names from stakeholder maps]

## Domain Context
- Key terms user uses: [Terms from outputs]
- User's product area: [Context from outputs]
- User's success metrics: [Metrics user tracks]
```

**Step 7: Generate Analysis Report**

Write detailed analysis to `outputs/learning/learning-summary-[skill-name]-YYYY-MM-DD.md`:

```markdown
---
generated: YYYY-MM-DD HH:MM
skill: learning-from-history
analyzed_skill: [skill-name]
sample_size: [N]
---

# Learning Analysis: [Skill Name]

## Data Analyzed
- **History files:** [N] from history/[skill-name]/
- **Decision logs:** [M] from outputs/decisions/
- **Date range:** [YYYY-MM-DD to YYYY-MM-DD]
- **Outcomes available:** [X/N] outputs have outcome data ([%])

## Methodology
1. Read all files in history/[skill-name]/
2. Extract structural patterns (format, length, sections)
3. Extract content patterns (evidence types, specificity)
4. Cross-reference with decision logs for outcomes
5. Identify correlations between patterns and success/failure
6. Quantify confidence based on sample size

## Key Findings

### Finding 1: [Title]
**Pattern:** [Description]
**Evidence:** [X/Y] successful outputs ([%])
**Confidence:** Strong/Medium/Weak
**Implication:** [What this means for future outputs]

### Finding 2: [Title]
**Pattern:** [Description]
**Evidence:** [X/Y] outputs ([%])
**Confidence:** Strong/Medium/Weak
**Implication:** [What this means]

## Recommended Skill Updates

### Update: `skills/[skill-name]/SKILL.md`

**Section:** [Which section]
**Current instruction:**
```
[Old way if it exists]
```

**Recommended addition:**
```
[New guidance based on learned patterns]
```

**Rationale:** Analysis of [N] outputs shows [pattern] correlates with success.

## Personal Preferences Detected

- [Preference 1]: Observed in [X/Y] outputs
- [Preference 2]: Observed in [X/Y] outputs
- [Preference 3]: Observed in [X/Y] outputs

## Limitations

- **Small sample:** Only [N] outputs (need [M] for high confidence)
- **Outcome data incomplete:** [X/N] outputs lack outcome tracking
- **Confounding variables:** [Other factors that may explain patterns]
- **Recency bias:** Recent outputs may not reflect long-term patterns

## Next Steps

1. **Apply patterns:** Use learned rules in next [skill-name] execution
2. **Validate:** Track whether patterns improve outcomes
3. **Re-analyze:** After [N more outputs] or [time period]
4. **Update skill:** Implement recommended changes to skill file
```

**Step 8: Copy to History**

- Copy analysis to `history/learning-from-history/learning-[skill-name]-YYYY-MM-DD.md`

## Quick Reference

### Pattern Confidence Levels

| Confidence | Sample Size | Correlation | Interpretation |
|------------|-------------|-------------|----------------|
| **Strong** | N ≥ 10 | ≥80% | Reliable pattern, use as default |
| **Medium** | N ≥ 5 | 50-80% | Promising pattern, test more |
| **Weak** | N < 5 | <50% | Insufficient data, need more |

### What to Look For

| Pattern Type | Examples |
|--------------|----------|
| **Format** | Table vs bullets, length (short vs detailed), section order |
| **Structure** | Presence/absence of sections, level of nesting, use of examples |
| **Content** | Evidence types cited, specificity level, metric formats, tone |
| **Process** | Review cycles, stakeholder involvement, timing of creation |
| **Outcomes** | Approved/rejected, revision count, time to approval |

## Common Mistakes

- **Overfitting:** Seeing patterns in noise (need sufficient sample size)
- **Confirmation bias:** Only looking for patterns you expect
- **Ignoring context:** Not considering external factors (team changes, market shifts)
- **No validation:** Not tracking whether patterns actually improve outcomes
- **Stale patterns:** Not re-analyzing as data grows

## Verification Checklist

- [ ] Read all history files for target skill
- [ ] Counted outputs and date range
- [ ] Cross-referenced decision logs for outcomes
- [ ] Identified 3-5 success patterns with evidence
- [ ] Identified 3-5 failure patterns with evidence
- [ ] Quantified confidence levels
- [ ] Wrote learned rules to `.claude/rules/learned/`
- [ ] Updated `CLAUDE.local.md` with preferences
- [ ] Generated detailed analysis report
- [ ] Copied to history

## Evidence Tracking

| Claim | Type | Source |
|-------|------|--------|
| [Pattern X correlates with success] | Evidence | [Analyzed N=X outputs] |
| [User prefers Y] | Evidence | [Observed in M outputs] |
| [Pattern will improve outcomes] | Assumption | [Needs validation] |
