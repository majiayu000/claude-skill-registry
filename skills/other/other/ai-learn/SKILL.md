---
name: ai-learn
description: "Use when analyzing merged PRs for AI blind spots, extracting patterns from human reviewer feedback, or applying accumulated learnings to context files."
effort: medium
argument-hint: "single <pr>|batch|apply"
---


# Learn

## Purpose

Continuous improvement from delivery outcomes. Analyzes merged PRs to find where AI missed what human reviewers caught, identifies false positives, and synthesizes recurring patterns into context updates. The feedback loop that makes the framework smarter over time.

## Trigger

- Command: `/ai-learn single <pr>|batch|apply`
- Context: after PR merge (single), periodic review (batch), enough patterns accumulated (apply).

## Modes

### single <pr> -- Analyze one merged PR

1. **Fetch PR data** -- `gh pr view <pr> --json body,reviews,comments,files,additions,deletions`.
2. **Collect AI findings** -- read the AI-generated PR description, guard advisories, and verify results from the PR.
3. **Collect human feedback** -- extract all review comments, requested changes, and approval notes.
4. **Cross-reference** -- compare AI findings with human feedback:

   | Category | Description |
   |----------|-------------|
   | **AI miss** | Human reviewer found an issue AI did not flag |
   | **False positive** | AI flagged something human reviewer dismissed or overrode |
   | **AI hit** | AI flagged an issue human reviewer agreed with |
   | **Novel insight** | Human added context AI could not have known |

5. **Record** -- append learning entry to `.ai-engineering/learnings/index.jsonl`:
   ```json
   {"pr": 123, "date": "2026-03-19", "misses": 2, "false_positives": 1, "hits": 5, "patterns": ["missed-null-check", "over-flagged-naming"]}
   ```

### batch -- Process unanalyzed PRs

1. **Find unanalyzed** -- list merged PRs not yet in `index.jsonl`.
2. **Process each** -- run single-mode analysis for each.
3. **Summary** -- report total misses, false positives, and emerging patterns.

### apply -- Synthesize into context updates

1. **Load learnings** -- read `.ai-engineering/learnings/index.jsonl`.
2. **Find recurring patterns** -- group by pattern, count occurrences.
3. **Threshold check** -- only act on patterns with 3+ occurrences.
4. **Propose updates** -- for each qualifying pattern:
   - If AI consistently misses a check: propose adding it to the relevant standard or guard advisory
   - If AI consistently false-positives: propose relaxing the rule or adding an exception
   - If humans add the same context repeatedly: propose adding it to a skill or agent instruction
5. **Present changes** -- show proposed updates to user for approval before modifying any files.
6. **Apply** -- update the relevant context files (standards, skills, agent instructions).

## Pattern Categories

| Pattern | Example | Action |
|---------|---------|--------|
| Missed check | AI never flags missing error handling in async code | Add to guard advisory rules |
| Over-flagging | AI flags every single-letter variable in list comprehensions | Add exception to naming standard |
| Missing context | Reviewers always explain why a specific pattern is used in this codebase | Add to project context |
| Style drift | Reviewers consistently request a style AI does not enforce | Add to stack standard |

## Quick Reference

```
/ai-learn single 123         # analyze PR #123
/ai-learn batch               # process all unanalyzed merged PRs
/ai-learn apply               # synthesize patterns into context updates
```

## Storage

- Learnings index: `.ai-engineering/learnings/index.jsonl`
- One JSON object per line, per PR analyzed

## Post-Correction Learning

When a user corrects AI behavior during a session (not just PR review):
1. Capture the correction: what was wrong, what the user wanted instead
2. Append the pattern to `.ai-engineering/contexts/team/lessons.md` following the format in that file
3. On next `/ai-learn apply`, include lesson-type decisions in synthesis

$ARGUMENTS
