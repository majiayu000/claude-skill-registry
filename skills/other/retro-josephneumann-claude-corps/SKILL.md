---
name: retro
description: "Engineering retrospective analyzing git commit history for shipping metrics, work patterns, and trends. Persistent history with trend tracking. Use weekly to review shipping velocity, or after milestones. Invoke with /retro [7d|14d|30d|24h] or /retro compare to see trends."
allowed-tools: Bash, Read, Write, Glob
---

# /retro — Engineering Retrospective

Analyze git commit history to produce shipping metrics, work patterns, and trends. Outputs a narrative summary to the conversation and saves a JSON snapshot to `.context/retros/` for trend tracking.

## Arguments

```
/retro              → Last 7 days (default)
/retro 24h          → Last 24 hours
/retro 14d          → Last 14 days
/retro 30d          → Last 30 days
/retro compare      → 7-day window vs. prior 7 days
/retro compare 14d  → 14-day window vs. prior 14 days
```

**Validation**: If the argument doesn't match `<N>d`, `<N>h`, `compare`, or `compare <N>d`, print usage and stop. Do not guess.

## Rules

- **Self-contained**: Do not read CLAUDE.md, reference.md, or other project docs. Everything needed is in this file.
- **Output discipline**: ALL narrative output goes to the conversation. The ONLY file written is the JSON snapshot to `.context/retros/`.
- **Use `origin/main`** for all git queries. Run `git fetch origin` first. If your repo uses a different default branch (e.g., `master`), adjust the git commands accordingly.
- **Zero commits**: If the window contains zero commits, say so clearly and suggest trying a different window. Stop the pipeline.
- **Round LOC/hour** to the nearest 50.
- **Merge commits** are treated as PR boundaries.
- **First run**: If no prior retro JSON exists, skip comparison gracefully — no errors, just note it's the first snapshot.
- **All times in local timezone**. Do not hardcode any timezone.

## Pipeline (13 Steps)

Execute each step in order. Collect all data before writing any output.

### Step 1: Gather Raw Data

```bash
git fetch origin

# Set window boundaries
SINCE="<computed from argument, e.g., 7 days ago>"
UNTIL="now"

# All commits on origin/main in window
git log origin/main --since="$SINCE" --until="$UNTIL" --format="%H|%ai|%s" --no-merges

# Merge commits (PR boundaries)
git log origin/main --since="$SINCE" --until="$UNTIL" --merges --format="%H|%ai|%s"

# Diff stats
git log origin/main --since="$SINCE" --until="$UNTIL" --no-merges --numstat --format="%H"

# File change counts
git log origin/main --since="$SINCE" --until="$UNTIL" --no-merges --name-only --format=""
```

### Step 2: Compute Core Metrics

Build a metrics table from the raw data:

| Metric | How |
|--------|-----|
| Total commits | Count non-merge commits in window |
| PRs merged | Count merge commits in window |
| Lines inserted | Sum insertions from `--numstat` |
| Lines deleted | Sum deletions from `--numstat` |
| Net LOC | Insertions − deletions |
| Test LOC ratio | Lines in test/spec files ÷ total insertions. Flag if < 0.1 |
| Active days | Distinct dates with at least one commit |
| Sessions | Detected in Step 4 |
| LOC/session-hour | Net LOC ÷ total session hours (round to nearest 50) |

### Step 3: Commit Time Distribution

Build an hourly histogram (0–23) of commit timestamps. Display as a horizontal bar chart using block characters. Identify peak hour and quiet hours (zero commits).

```
Hour  Commits
 06   ▓▓ 2
 07   ▓▓▓▓▓ 5
 ...
 22   ▓ 1
```

### Step 4: Work Session Detection

A **session** is a sequence of commits where no gap exceeds **45 minutes**.

For each session, compute:
- Start time, end time, duration
- Commit count within session
- Classification:
  - **Deep** (≥ 2 hours)
  - **Medium** (30 min – 2 hours)
  - **Micro** (< 30 min)

Report counts by classification and average session length.

### Step 5: Commit Type Breakdown

Parse commit prefixes (`feat:`, `fix:`, `refactor:`, `test:`, `chore:`, `docs:`, `other`). Compute percentages.

```
feat      42%  ████████
fix       28%  █████
refactor  15%  ███
test       8%  █
chore      5%  █
docs       2%
```

**Flag**: If `fix` ratio exceeds 50%, note: "High fix ratio — consider whether this signals tech debt, flaky tests, or rushed shipping."

### Step 6: Hotspot Analysis

List the **top 10 most-changed files** (by number of commits touching them). For each, show commit count and whether insertions or deletions dominate.

Flag files changed 5+ times — these are refactoring candidates or areas of active development.

### Step 7: PR Size Distribution

Classify each PR (merge commit) by total lines changed:

| Bucket | Lines Changed |
|--------|---------------|
| Small  | < 100 |
| Medium | 100–300 |
| Large  | 300–1000 |
| XL     | > 1000 |

Report distribution. Flag if > 30% are Large/XL — "Large PRs are harder to review and more likely to ship bugs."

### Step 8: Focus Score + Ship of the Week

**Focus score**: Percentage of commits touching the most active top-level directory. Higher = more focused. > 70% is focused, < 40% is scattered.

**Ship of the week**: The single most notable commit or PR. Pick based on:
1. Largest feature (by commit message and LOC)
2. If no clear feature, the most impactful fix
3. If nothing stands out, the most frequently touched area

One sentence describing what shipped and why it matters.

### Step 9: Week-over-Week Trends

**Only compute if the window is ≥ 14 days.** Split the window in half and compare:

- Commits: first half vs. second half
- LOC: first half vs. second half
- Session count: first half vs. second half

Show deltas with arrows: ↑ increase, ↓ decrease, → stable (< 10% change).

### Step 10: Streak Tracking

Count **consecutive days** with at least one commit, ending at the most recent day in the window.

- Current streak length
- Longest streak in the window
- If streak ≥ 7 days: "Solid consistency."
- If streak = 0 on the most recent day: "Streak broken — last commit was N days ago."

### Step 11: Load Prior Retro

Look for the most recent JSON file in `.context/retros/`. If found, load it for comparison in Step 12.

If no prior retro exists, note "First retro snapshot — no prior data for comparison" and skip Step 12 comparison logic.

### Step 12: Compare with Prior Retro

If a prior retro was loaded, compute deltas for:

- Total commits (Δ and %)
- PRs merged (Δ and %)
- Net LOC (Δ)
- Active days (Δ)
- Session count (Δ)
- Focus score (Δ percentage points)

Present as a compact delta table. Only highlight changes > 20% as notable.

### Step 13: Save JSON Snapshot + Write Narrative

**Save JSON** to `.context/retros/retro-YYYY-MM-DD.json`:

```json
{
  "date": "YYYY-MM-DD",
  "window_days": 7,
  "commits": 42,
  "prs_merged": 8,
  "insertions": 1200,
  "deletions": 400,
  "net_loc": 800,
  "test_loc_ratio": 0.15,
  "active_days": 5,
  "sessions": 12,
  "deep_sessions": 3,
  "medium_sessions": 6,
  "micro_sessions": 3,
  "avg_session_minutes": 85,
  "loc_per_session_hour": 350,
  "focus_score": 0.65,
  "focus_directory": "src/",
  "current_streak": 5,
  "longest_streak": 5,
  "commit_types": {
    "feat": 0.42,
    "fix": 0.28,
    "refactor": 0.15,
    "test": 0.08,
    "chore": 0.05,
    "docs": 0.02
  },
  "peak_hour": 14,
  "ship_of_the_week": "Added streaming API support for real-time data processing",
  "pr_size_distribution": {
    "small": 3,
    "medium": 3,
    "large": 1,
    "xl": 1
  }
}
```

Create `.context/retros/` directory if it doesn't exist.

**Write Narrative** to the conversation (not to a file). Structure:

```
## Engineering Retro — <start date> to <end date>

### Metrics
<table from Step 2>

### Commit Rhythm
<histogram from Step 3>
<session summary from Step 4>

### What Shipped
<commit type breakdown from Step 5>
<ship of the week from Step 8>

### Code Health
<hotspot analysis from Step 6>
<PR size distribution from Step 7>

### Patterns
<focus score from Step 8>
<trends from Step 9, if applicable>
<streak from Step 10>

### vs. Last Retro
<deltas from Step 12, or "First snapshot" note>

### Tweetable Summary
<One sentence, ≤ 280 chars. Specific numbers, what shipped, honest tone.>
```

## Compare Mode

When invoked as `/retro compare` or `/retro compare <N>d`:

1. Compute the full pipeline for the current window (e.g., last 7 days).
2. Compute the full pipeline for the **prior window** of equal length (e.g., 7–14 days ago).
3. Present side-by-side with deltas for every metric.
4. Save only the current window's JSON snapshot.
5. Narrative should call out what improved, what regressed, and what held steady.

## Tone

- Encouraging but candid. Never generic ("Great job!").
- Specific — cite exact numbers, file names, commit messages.
- If metrics look bad, say so directly with constructive framing.
- If metrics look good, acknowledge with specifics, not cheerleading.
