---
name: compare-attempts
description: This SOP compares evaluated brazil-bench attempts across multiple dimensions to produce a ranked leaderboard and detailed comparison summary. It supports up to 10 attempts in the "Top 10" format, automatically pruning lower-ranked entries when more are added.
type: anthropic-skill
version: "1.1"
---

# Compare Benchmark Attempts

## Overview
This SOP compares evaluated brazil-bench attempts across multiple dimensions to produce
a ranked leaderboard and detailed comparison summary. It supports up to 10 attempts
in the "Top 10" format, automatically pruning lower-ranked entries when more are added.

## Parameters
- **results_dir** (optional, default: `./results`): Directory containing evaluation reports
- **output_file** (optional, default: `./results/LEADERBOARD.md`): Output comparison file
- **max_entries** (optional, default: 10): Maximum entries in leaderboard

## Steps

### 1. Discover Evaluation Results
Find all completed evaluation reports in the results directory.

**Constraints:**
- You MUST scan for `*.md` files in the results directory (excluding LEADERBOARD.md)
- You MUST verify each file is a valid evaluation report (has "# Evaluation:" header)
- You MUST extract the attempt name from each report
- You SHOULD skip any malformed or incomplete reports
```bash
ls {results_dir}/*.md | grep -v LEADERBOARD.md
```

### 2. Extract Metrics from Each Report
Parse each evaluation report to extract comparable metrics.

**Constraints:**
- You MUST extract all metrics from the Metrics table in each report
- You MUST extract the pattern/orchestration type
- You MUST extract spec compliance (X/Y format)
- You MUST extract test counts if available
- You MUST extract git metrics (commits, duration, fix commits)
- You SHOULD normalize duration to hours for comparison
- You MUST handle missing metrics gracefully (mark as "N/A")
- You MUST check for evaluation methodology differences (see Step 2a)

**Required Metrics:**
| Metric | Source | Notes |
|--------|--------|-------|
| Pattern | Summary section | swarm, hive, solo, crew, custom |
| Spec Compliance | Summary or checklist | Count of implemented requirements |
| Lines of Code | Metrics table | Source code only |
| Files | Metrics table | Python files in src |
| Dependencies | Metrics table | Package count |
| Commits | Metrics table | Total git commits |
| Duration | Metrics table | Development time |
| Fix Commits | Git Analysis | Commits with "fix" in message |
| Test Scenarios | Test Summary | BDD or unit test count |
| Token Usage | Token Usage section | From prompts.txt if available |
| Phase Durations | Duration Breakdown | Initial coding, tests working, human intervention |

### 2a. Check for Evaluation Methodology Differences

Compare how each attempt was evaluated to ensure fair comparison.

**Constraints:**
- You MUST verify all attempts use the same requirement denominator (should be 16)
- You MUST flag attempts evaluated with different methodologies
- You MUST document any normalization applied to make scores comparable
- You SHOULD recommend re-evaluation for attempts with non-standard methodology

**Detection Commands:**
```bash
# Check spec compliance denominators across all evaluations
grep -h "Spec Compliance" {results_dir}/*.md | grep -v LEADERBOARD

# Look for different requirement counts
grep -E "requirements|/16|/12|/15" {results_dir}/*.md
```

**Canonical Requirements (16 total):**
All evaluations should use this breakdown:
- Functional Requirements: 6 (FR-1 through FR-6)
- Query Performance: 3 (QP-1 through QP-3)
- Data Coverage: 3 (DC-1 through DC-3)
- Technical Requirements: 4 (TR-1 through TR-4)

**Methodology Difference Table:**

| Attempt | Denominator | Categories Evaluated | Difference | Action |
|---------|-------------|---------------------|------------|--------|
| {name} | /16 | All 4 categories | None | OK |
| {name} | /12 | Missing TR-* | -4 requirements | Flag for re-eval |
| {name} | /10 | Custom | Non-standard | Flag for re-eval |

**Include in Report:**
```markdown
## Evaluation Methodology Check

⚠️ **Inconsistency Detected:** The following attempts were evaluated with different requirement counts:

| Attempt | Evaluated As | Expected | Difference |
|---------|--------------|----------|------------|
| gastown | 12/12 | 16/16 | Missing TR-1 through TR-4 |

These attempts should be re-evaluated using the canonical 16-requirement checklist.
Until re-evaluated, their compliance scores are normalized: 12/12 → 12/16 (75%).
```

**Normalization Rules:**
- If an attempt shows X/Y where Y ≠ 16, normalize to X/16
- Example: 12/12 becomes 12/16 (not 16/16)
- Flag in leaderboard with asterisk: "12/16*"
- Add footnote explaining the normalization

### 3. Calculate Ranking Score
Compute a composite score for ranking attempts.

**Constraints:**
- You MUST use a weighted scoring formula
- You MUST prioritize spec compliance (highest weight - 50%)
- You MUST prioritize test coverage second (30%)
- You SHOULD reward fewer fix commits (cleaner development)
- Duration is a minor factor - completeness matters more than speed
- You MUST document the scoring formula used

**Scoring Formula:**
```
Score = (Spec Compliance % × 50)
      + (Test Coverage Score × 30)
      + (Code Quality Score × 15)
      + (Efficiency Score × 5)

Where:
- Spec Compliance % = (implemented / total) × 100
- Test Coverage Score = min(100, effective_tests × 1.5)  # Use EFFECTIVE tests, not total
- Code Quality Score = 100 - (fix_commits × 10) - (skip_penalty)
- Efficiency Score = 100 - min(100, (LOC / 100))  # Minor factor for code bloat

Skip Penalty Calculation:
- skip_ratio = skipped_tests / total_tests
- skip_penalty = max(0, (skip_ratio - 0.10) × 50)  # Penalize if >10% skipped
- Example: 25% skip ratio → (0.25 - 0.10) × 50 = 7.5 point penalty
```

**IMPORTANT: Use Effective Tests, Not Total Tests**
- Effective Tests = Passed + Failed (excluding Skipped)
- Skipped tests do NOT count toward test coverage score
- Attempts with >20% skip ratio should be flagged as "inflated test count"

**Ranking Priority (for ties or qualitative ranking):**
1. **Primary:** Spec Compliance (higher = better)
2. **Secondary:** Effective Test Count (more = better, excluding skipped)
3. **Tertiary:** Fix Commits (fewer = better)
4. **Quaternary:** Skip Ratio (lower = better)
5. **Quinary:** Duration (faster = better, but less important)

Duration is intentionally weighted low because a complete, well-tested implementation
is more valuable than a fast but incomplete one.

### 4. Rank and Sort Attempts
Order attempts by composite score.

**Constraints:**
- You MUST sort by score descending (highest first)
- You MUST handle ties by using secondary sort (more tests wins, then fewer fix commits)
- You MUST limit to top {max_entries} entries
- You MUST assign rank numbers (1, 2, 3, ...)
- You SHOULD note if entries were pruned

### 5. Generate Comparison Tables
Create detailed comparison tables for the report.

**Constraints:**
- You MUST create a summary leaderboard table
- You MUST create a detailed metrics comparison table
- You MUST create a pattern distribution summary
- You SHOULD create a requirements coverage matrix
- You SHOULD include trend indicators if historical data exists

### 6. Analyze Development Phases
Break down development duration into distinct phases for each attempt.

**Constraints:**
- You MUST analyze git commit timestamps to identify phase boundaries
- You MUST identify three phases where data is available:
  - **Phase 1: Initial Coding** - Time from first code commit to initial implementation
  - **Phase 2: Tests Working** - Time from initial implementation to 100% test pass
  - **Phase 3: Human Intervention** - Any post-completion human-driven changes
- You MUST calculate autonomous duration (Phase 1 + Phase 2)
- You SHOULD note parallel vs sequential agent patterns
- You SHOULD identify which phases each pattern excels at

**Phase Analysis Table:**
| Phase | Description | How to Identify |
|-------|-------------|-----------------|
| Setup | Human preparation | Initial commits before implementation |
| Initial Coding | Autonomous implementation | First "implement" or "add" commit |
| Tests Working | Test fixing iterations | Commits from implementation to "100% pass" |
| Human Intervention | Post-completion changes | Commits after tests pass (data, docs, etc.) |

### 7. Extract Initial Prompts
Extract the orchestration command and prompt used to start each attempt.

**Constraints:**
- You MUST check for prompts.txt in each attempt's cloned repository
- You MUST search for `npx claude-flow@alpha` commands (hive-mind spawn, swarm, etc.)
- You MUST extract the full prompt text in quotes
- You MUST identify the orchestration pattern from the command
- You SHOULD note if prompts are identical across attempts (controlled experiment)

**Command Patterns:**
| Command | Pattern | Description |
|---------|---------|-------------|
| `hive-mind spawn "..." --claude` | Hive | Multi-agent parallel execution |
| `swarm "..." --claude` | Swarm | Sequential solo development |
| Direct Claude Code | Solo | No orchestration framework |

### 8. Analyze Token Usage
Extract and compare token consumption from prompts.txt files.

**Constraints:**
- You MUST check for prompts.txt in each attempt's cloned repository
- You MUST extract "Done (X tool uses · Yk tokens · Zm)" entries
- You MUST sum total tokens and tool uses per attempt
- You MUST calculate tokens per LOC for efficiency comparison
- You MUST add disclaimer that data is from manually captured prompts
- You SHOULD note if token data is incomplete or missing

**Token Metrics:**
| Metric | Calculation | Notes |
|--------|-------------|-------|
| Total Tokens | Sum of all "Done" entries | May be incomplete |
| Tool Uses | Sum of tool use counts | Indicates iteration count |
| Sessions/Agents | Count of "Done" entries | Parallel vs sequential |
| Tokens per LOC | Total tokens / Lines of Code | Efficiency measure |

### 9. Collect Issue Counts
Fetch open and closed issue counts for each attempt repository.

**Constraints:**
- You MUST query GitHub for each attempt's issue counts
- You MUST capture both open and closed issue counts
- You MUST include issue counts in the leaderboard table
- You SHOULD categorize issues by type ([Missing], [Test Quality], [Docs], [Compliance])

**Commands:**
```bash
# Get issue counts for an attempt
gh issue list -R brazil-bench/{attempt_repo} --state open --json number -q 'length'
gh issue list -R brazil-bench/{attempt_repo} --state closed --json number -q 'length'

# Get issue details with titles
gh issue list -R brazil-bench/{attempt_repo} --state all --json number,title,state
```

**Issue Tracking Table:**
| Attempt | Open | Closed | Total | Categories |
|---------|------|--------|-------|------------|
| {name} | {n} | {n} | {n} | {types} |

### 10. Generate Analysis
Provide insights from the comparison.

**Constraints:**
- You MUST identify the winning attempt and why
- You MUST note patterns that performed better/worse
- You MUST compare phase durations between patterns
- You MUST compare token efficiency if data available
- You MUST include issue tracking summary in analysis
- You SHOULD identify common strengths across top performers
- You SHOULD identify areas where all attempts struggled
- You MUST NOT make subjective quality judgments beyond metrics

### 11. Write Comparison Report
Output the final comparison document.

**Constraints:**
- You MUST write to {output_file}
- You MUST use the output format specified below
- You MUST include generation timestamp
- You MUST include source file references
- You SHOULD include methodology notes

## Output Format

```markdown
# Brazil-Bench Leaderboard

> Last updated: {timestamp}
> Attempts evaluated: {count}

## Evaluation Methodology Check

{If all attempts use 16/16 denominator:}
✅ All attempts evaluated using canonical 16-requirement checklist.

{If inconsistencies found:}
⚠️ **Inconsistency Detected:** The following attempts were evaluated with different requirement counts:

| Attempt | Evaluated As | Normalized To | Missing Requirements |
|---------|--------------|---------------|---------------------|
| {name} | {X/Y} | {X/16} | {list of missing req IDs} |

*Scores marked with asterisk (*) have been normalized. Re-evaluation recommended.*

---

## 🏆 Top 10 Leaderboard

| Rank | Attempt | Pattern | Score | Spec | LOC | Tests | Duration | Issues |
|------|---------|---------|-------|------|-----|-------|----------|--------|
| 1 🥇 | {name} | {pattern} | {score} | {X/Y} | {loc} | {tests} | {duration} | {n} open |
| 2 🥈 | {name} | {pattern} | {score} | {X/Y} | {loc} | {tests} | {duration} | {n} open |
| 3 🥉 | {name} | {pattern} | {score} | {X/Y} | {loc} | {tests} | {duration} | {n} open |
| 4 | ... | ... | ... | ... | ... | ... | ... | ... |

*Spec column: X/16 expected. Entries with asterisk (*) were normalized from different denominators.*

## Initial Prompts

{Note whether prompts are identical or different across attempts}

**{attempt1}:** `npx claude-flow@alpha {command} "..." --claude`
- {Description of orchestration pattern}

**{attempt2}:** `npx claude-flow@alpha {command} "..." --claude`
- {Description of orchestration pattern}

**Common prompt text:** (if applicable)
> "{The shared prompt text}"

## Development Phase Comparison

| Phase | {attempt1} | {attempt2} | ... | Notes |
|-------|------------|------------|-----|-------|
| **Setup (Human)** | {duration} | {duration} | ... | {notes} |
| **Phase 1: Initial Coding** | {duration} | {duration} | ... | {notes} |
| **Phase 2: Tests Working** | {duration} | {duration} | ... | {notes} |
| **Total Autonomous** | {duration} | {duration} | ... | {notes} |
| **Phase 3: Human Intervention** | {description} | {description} | ... | {notes} |

### Phase Details
{Narrative description of each attempt's phase breakdown}

## Token Usage Comparison

> ⚠️ **Note:** Token counts are from manually captured prompts.txt files and may not be complete or accurate.

| Metric | {attempt1} | {attempt2} | ... | Notes |
|--------|------------|------------|-----|-------|
| **Total Tokens** | {tokens} | {tokens} | ... | {notes} |
| **Tool Uses** | {count} | {count} | ... | {notes} |
| **Sessions/Agents** | {count} ({type}) | {count} ({type}) | ... | {notes} |
| **Tokens per LOC** | {ratio} | {ratio} | ... | {notes} |

## Detailed Metrics Comparison

| Metric | {attempt1} | {attempt2} | ... | Notes |
|--------|------------|------------|-----|-------|
| **Pattern** | {val} | {val} | ... | - |
| **Spec Compliance** | {X/Y} | {X/Y} | ... | {winner} |
| **Lines of Code** | {loc} | {loc} | ... | {winner} |
| **Python Files** | {n} | {n} | ... | {winner} |
| **Dependencies** | {n} | {n} | ... | {winner} |
| **Commits** | {n} | {n} | ... | {winner} |
| **Autonomous Duration** | {duration} | {duration} | ... | {winner} |
| **Tokens (approx)** | {tokens} | {tokens} | ... | {winner} |
| **Fix Commits** | {n} | {n} | ... | {winner} |
| **Test Scenarios** | {n} | {n} | ... | {winner} |
| **Real Data** | {yes/no} | {yes/no} | ... | {winner} |

## Pattern Performance

| Pattern | Attempts | Avg Score | Best Rank | Avg LOC | Avg Duration |
|---------|----------|-----------|-----------|---------|--------------|
| Hive | {n} | {score} | {rank} | {loc} | {hours}h |
| Swarm | {n} | {score} | {rank} | {loc} | {hours}h |
| Solo | {n} | {score} | {rank} | {loc} | {hours}h |
| Crew | {n} | {score} | {rank} | {loc} | {hours}h |

## Requirements Coverage Matrix

| Requirement | {attempt1} | {attempt2} | ... | Coverage |
|-------------|------------|------------|-----|----------|
| search_player | ✅ | ✅ | ... | 100% |
| get_player_stats | ✅ | ✅ | ... | 100% |
| ... | ... | ... | ... | ... |

## Analysis

### Winner: {attempt_name}
{Brief explanation of why this attempt ranked first}

### Key Differentiators

| Aspect | {attempt1} | {attempt2} | Winner |
|--------|------------|------------|--------|
| Spec completeness | {X/Y} | {X/Y} | 🏆 {winner} |
| Autonomous duration | {duration} | {duration} | 🏆 {winner} |
| Token usage* | {tokens} | {tokens} | 🏆 {winner} |
| Initial coding speed | {duration} | {duration} | 🏆 {winner} |
| Test fixing speed | {duration} | {duration} | 🏆 {winner} |
| Real data included | {yes/no} | {yes/no} | 🏆 {winner} |
| Test coverage | {scenarios} | {scenarios} | 🏆 {winner} |
| Code efficiency | {LOC} | {LOC} | 🏆 {winner} |

*Token counts from manually captured prompts.txt, may be incomplete

### Pattern Insights
- **Best performing pattern:** {pattern} (avg score: {score})
- **Most efficient pattern:** {pattern} (lowest avg LOC: {loc})
- **Fastest pattern:** {pattern} (avg duration: {duration})
- **Most token-efficient:** {pattern} (tokens per LOC: {ratio})

### Common Strengths
- {observation 1}
- {observation 2}

### Areas for Improvement
- {observation 1}
- {observation 2}

## Methodology

### Scoring Formula
```
Score = (Spec Compliance % × 50) + (Effective Test Score × 30) + (Quality × 15) + (Efficiency × 5)

Where:
- Test Score uses EFFECTIVE tests (excluding skipped)
- Quality includes skip penalty: -max(0, (skip_ratio - 0.10) × 50)
```

**Priority Order:** Compliance > Effective Tests > Quality > Skip Ratio > Duration

### Data Sources
- {attempt1}: results/{attempt1}.md
- {attempt2}: results/{attempt2}.md
- ...

## Issue Tracking Summary

| Attempt | Open | Closed | Total | Categories |
|---------|------|--------|-------|------------|
| {name} | {n} | {n} | {n} | {types} |
| ... | ... | ... | ... | ... |

**Total Open Issues:** {total}

### Issue Distribution by Type

| Issue Type | Count | Description |
|------------|-------|-------------|
| `[Missing]` | {n} | Missing spec requirements |
| `[Test Quality]` | {n} | Skipped tests, best practices |
| `[Compliance]` | {n} | Summary issues linking requirements |
| `[Docs]` | {n} | README documentation gaps |

---
Generated by compare-attempts SOP on {timestamp}
```

## Troubleshooting

**No evaluation reports found**
- Verify results_dir path is correct
- Run evaluate-attempt SOP first for each attempt
- Check file permissions

**Missing metrics in report**
- Re-run evaluate-attempt SOP for that attempt
- Check if the attempt used a different report format
- Mark as "N/A" and note in analysis

**Scoring seems unfair**
- Review the scoring formula weights
- Consider adjusting for specific benchmark goals
- Document any formula modifications

**Too many attempts (>10)**
- Only top 10 are shown in leaderboard
- Full data preserved in detailed comparison
- Consider archiving older/lower-ranked attempts

**Missing token usage data**
- Check if prompts.txt exists in the attempt's cloned repository
- Token data is manually captured and may not be available for all attempts
- Mark as "N/A" and note in the disclaimer
- Do not penalize attempts without token data in scoring

**Phase duration analysis unclear**
- Use git log with timestamps: `git log --format="%ai | %s"`
- Look for key commit messages: "implement", "fix", "100% pass"
- Human intervention starts after "100% pass" or similar milestone
- Note any ambiguity in the phase details section

**Parallel vs sequential patterns**
- Hive pattern: Look for multiple agents spawned simultaneously
- Swarm pattern: Look for sequential sessions in prompts.txt
- Check for "In progress" entries showing parallel execution
- Document agent/session count in the comparison
