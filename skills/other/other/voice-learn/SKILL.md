---
name: voice-learn
description: Learn from user's manual edits to improve voice profile over
  time. Compares text at three stages (pre-review, post-review, manually
  edited) to identify recurring edit patterns and propose register updates.
version: 1.8.4
globs: "**/*.{md,txt}"
alwaysApply: false
category: writing-quality
tags:
- voice
- learning
- improvement
- feedback
- iteration
tools:
- Read
- Write
- Bash
- Glob
- Agent
- TodoWrite
complexity: high
model_hint: opus
estimated_tokens: 2000
progressive_loading: true
modules:
- snapshot-management
- pattern-analysis
dependencies:
- scribe:voice-extract
- scribe:voice-generate
- scribe:voice-review
---

# Voice Learning Skill

Learn from user edits to improve the voice profile over time.

## Method: Three-Stage Comparison

Every piece flows through three stages:
1. **Pre-review**: Raw generation output (before review agents)
2. **Post-review**: After user accepts/rejects advisory fixes
3. **Post-edit**: User's manually edited final version

The learning agent compares stages 2 and 3 (post-review vs
post-edit) to identify patterns in what the user changed.
These patterns inform register and rule updates.

## Core Rules

1. **Sharpen, don't add**: Modify existing rules to cover new
   patterns. Rule bloat degrades output.
2. **Tag specificity**: Register-specific patterns go to
   registers. Universal patterns go to craft rules or agents.
3. **Flag contradictions**: Opposite patterns across pieces
   require user resolution.
4. **Evidence threshold**: Patterns need 3+ instances (or 1-2
   matching existing accumulator entries) before becoming rules.
5. **Detection surface**: Structural changes increase AI
   detectability. Craft-level changes are neutral. Prefer
   craft-level updates.
6. **Rule count check**: Suggest consolidation if any section
   has 8+ rules.

## Required TodoWrite Items

1. `voice-learn:snapshots-loaded` - All three stages read
2. `voice-learn:diff-analyzed` - Changes categorized
3. `voice-learn:accumulator-checked` - Prior patterns reviewed
4. `voice-learn:proposals-generated` - Updates proposed
5. `voice-learn:user-approved` - Changes accepted by user

## Step 1: Load Snapshots

Load: `@modules/snapshot-management`

```bash
PROFILE_DIR="$HOME/.claude/voice-profiles/{name}"
SNAP_DIR="$PROFILE_DIR/learning/snapshots"

# Find the most recent snapshot set
# Format: {piece-name}-{timestamp}-{stage}.md
```

Read all three stages for the target piece.

## Step 2: Diff Analysis

Load: `@modules/pattern-analysis`

Compare post-review vs post-edit. Categorize every change:

| Category | Example |
|----------|---------|
| Tone adjustment | Softened a claim, added hedge |
| Voice insertion | Added parenthetical, aside, humor |
| Structure change | Broke paragraph, reordered |
| Precision edit | Replaced vague with specific |
| Deletion | Removed fluff or decoration |
| Addition | Added context, example, anchor |

## Step 3: Check Accumulator

Read `learning/accumulator.json`:

```json
{
  "patterns": [
    {
      "id": "pat-001",
      "category": "tone_adjustment",
      "description": "Softens confident claims about tool capabilities",
      "instances": [
        {"piece": "blog-post-1", "date": "2026-04-08", "diff": "..."}
      ],
      "target": "register",
      "status": "accumulating",
      "first_seen": "2026-04-08",
      "last_seen": "2026-04-08"
    }
  ],
  "staleness_threshold_days": 30
}
```

Match new changes against existing patterns:
- Semantic similarity (same category + similar description)
- If match found: merge instance, check if threshold reached
- If no match: create new accumulator entry

## Step 4: Generate Proposals

For patterns that reach threshold (3+ instances or 1-2
matching prior accumulator entries with 2+ instances):

### Apply (strong evidence)

```markdown
## Proposed Update

**Pattern**: {description}
**Target**: {register file or craft-rules.md}
**Evidence**: {N instances across M pieces}

| Piece | Date | Change Made |
|-------|------|-------------|
| ... | ... | ... |

**Proposed edit**:
- File: {path}
- Section: {section name}
- Current: "{current text or 'new addition'}"
- Proposed: "{new text}"
```

### Hold (insufficient evidence)

Add to accumulator with current instances. Report:
```
Holding: "{pattern description}" (N instances, need 3+)
```

### Contradictions

If a new pattern contradicts an existing accumulator entry:
```
Contradiction detected:
- Existing: "{accumulator pattern}"
- New: "{contradicting pattern}"
- Resolution required: user must choose
```

## Step 5: User Approval

Present proposals to user:
```
Learning found N patterns ready to apply:

[1] {pattern}: {proposed change}
    Evidence: {N instances}
    [a]pply / [s]kip / [v]iew evidence?

[2] ...
```

Apply approved changes to the target files.

## Staleness

Patterns in the accumulator expire after `staleness_threshold_days`
(default 30). If a pattern hasn't recurred within that window,
it was likely a one-off preference rather than a voice trait.

On each learning pass, prune stale entries:
```bash
# Remove patterns older than threshold with < 3 instances
```

## Snapshot Capture

The learning system captures snapshots automatically when
voice-review completes. Snapshot naming:

```
{piece-filename}-{YYYYMMDD-HHMMSS}-pre-review.md
{piece-filename}-{YYYYMMDD-HHMMSS}-post-review.md
{piece-filename}-{YYYYMMDD-HHMMSS}-post-edit.md
```

The post-edit snapshot is captured when the user runs
`/voice-learn` after finishing their manual edits.

## Exit Criteria

- Snapshots loaded and compared
- Changes categorized
- Accumulator checked and updated
- Proposals generated for threshold patterns
- User approved/rejected proposals
- Approved changes applied to profile files
- Stale accumulator entries pruned
