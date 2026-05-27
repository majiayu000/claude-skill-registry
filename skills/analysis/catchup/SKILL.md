---
name: catchup
description: |

Triggers: follow-ups, catchup, insights, context-acquisition, summarization
  Methodology for summarizing changes, extracting insights, and identifying follow-up actions.

  Triggers: catchup, what changed, summarize changes, context acquisition, handoff,
  progress review, recent changes, git log analysis, sprint summary

  Use when: resuming work after absence, preparing handoff documentation, reviewing
  sprint progress, analyzing git history for context

  DO NOT use when: doing detailed diff analysis - use diff-analysis instead.
  DO NOT use when: full code review needed - use review-core instead.

  Use this skill to quickly understand "what changed and what matters".
category: analysis-methods
tags: [summarization, context-acquisition, insights, follow-ups]
dependencies: [imbue:evidence-logging]
tools: [git, log-tools]
usage_patterns: [context-catchup, handoff-preparation, progress-review]
complexity: intermediate
estimated_tokens: 700
progressive_loading: true
module_strategy: context-based
---

# Catchup Analysis Methodology

## Overview

Structured method for quickly understanding recent changes in git repositories, meeting notes, sprint progress, document revisions, or system logs. Answers "what changed and what matters?" efficiently.

## When to Use
- Joining ongoing work or returning after absence
- Before planning or reviewing handoffs
- Any "what happened and what's next" context

## Activation
**Keywords**: catchup, summary, status, progress, context, handoff
**Cues**: "get me up to speed", "current status", "summarize progress"

## Progressive Loading

Load modules based on context:

**Git**: Load `modules/git-catchup-patterns.md` for git commands. Consider `sanctum:git-workspace-review` for initial data gathering.

**Documents/Notes**: Load `modules/document-analysis-patterns.md` for meeting notes, sprint tracking, document revisions.

**Logs/Events**: Load `modules/log-analysis-patterns.md` for time-series and metric analysis.

**Always Available**: `imbue:evidence-logging`, TodoWrite workflow, structured output.

## Required TodoWrite Items
1. `catchup:context-confirmed` - Boundaries established
2. `catchup:delta-captured` - Changes enumerated
3. `catchup:insights-extracted` - Themes identified
4. `catchup:followups-recorded` - Actions captured

## 4-Step Methodology

### Step 1: Confirm Context
Define scope (git branch, sprint, meetings), baseline (last state), and current target. See modules for commands.

### Step 2: Capture Delta
Enumerate changed items with metrics. Prioritize source/config/docs over generated artifacts. See modules for strategies.

### Step 3: Extract Insights
Per item: **What** (change), **Why** (motivation), **Implications** (tests/risks/deps). Rollup into themes.

### Step 4: Record Follow-ups
Capture: Tests, Documentation, Reviews, Blockers, Questions. If none, state explicitly.

## Output Format
```
## Summary
[2-3 sentence theme + risk overview]

## Key Changes
- [Item]: [what/why/implication]

## Follow-ups
- [ ] [Action with owner]

## Blockers/Questions
- [Item requiring resolution]
```
**Verification:** Run the command with `--help` flag to verify availability.

## Integration
Use `imbue:diff-analysis` for risk assessment, `imbue:evidence-logging` for reproducibility, `sanctum:git-workspace-review` for git data. Feed to `brainstorming` or `writing-plans` as needed.

## Token Conservation
Reference paths + lines (don't reproduce). Summarize outputs. Defer deep analysis. Use progressive loading.

## Exit Criteria
- Four TodoWrite items completed
- Context/delta/insights/follow-ups captured
- Stakeholders understand state without re-reading sources
## Troubleshooting

### Common Issues

**Command not found**
Ensure all dependencies are installed and in PATH

**Permission errors**
Check file permissions and run with appropriate privileges

**Unexpected behavior**
Enable verbose logging with `--verbose` flag
