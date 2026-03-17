---
name: batch-observing
description: Parallel multi-user processing using Claude Code native teams. Leader spawns workers per user, each runs /ingest-dm, leader aggregates for cross-canvas patterns.
user-invocable: true
allowed-tools: Read, Write, Glob, Grep, Edit, Bash
---

# Batch Observing

Process multiple user DM exports in parallel using Claude Code native teams. A leader agent spawns one worker per user, each worker runs the `/ingest-dm` pipeline independently, then the leader aggregates results for cross-canvas pattern detection.

---

## Core Principle

**Parallel independence, centralized synthesis.** Each worker processes one user independently. Cross-user patterns only emerge at the leader level after all workers complete.

---

## Triggers

```
/batch-observe <path1> <path2> ...                        # Multiple DM export files
/batch-observe grimoires/observer/imports/*.csv            # Glob pattern
/batch-observe --dir grimoires/observer/imports/           # All files in directory
```

---

## When to Use

- Beta expansion: 5+ new users to onboard simultaneously
- Batch DM exports from Discord
- Initial population of the observer canvas set
- Re-processing after Score API data refresh

---

## Workflow

### Step 1: Parse Input

Collect the list of DM export files:
- Direct file paths from arguments
- Glob expansion from patterns
- Directory listing from `--dir`

Validate each file exists and is readable.

### Step 2: Create Team

```
TeamCreate:
  team_name: "observer-batch-{date}"
  description: "Parallel DM ingestion for {N} users"
```

### Step 3: Create Tasks

For each input file, create a task:

```
TaskCreate:
  subject: "Ingest DM: {filename}"
  description: "Run /ingest-dm pipeline for {filename}"
```

### Step 4: Spawn Workers

For each task, spawn a worker agent:

```
Task:
  subagent_type: general-purpose
  team_name: "observer-batch-{date}"
  name: "worker-{username}"
  prompt: |
    You are an observer worker. Run the /ingest-dm pipeline for this file:

    File: {filepath}

    Steps:
    1. Read the file and extract the username
    2. Run: scripts/observer/wallet-resolve.sh {username}
    3. Run: scripts/observer/score-api-query.sh profile {wallet} --format snapshot
    4. Create the enriched canvas at grimoires/observer/canvas/{username}.md
    5. Follow the /ingest-dm SKILL.md template exactly
    6. When done, mark your task as completed and send a message to the leader
       with the canvas path and a summary of what was extracted.
```

**Stagger starts**: Delay 2-3 seconds between worker spawns to avoid Supabase rate limiting.

### Step 5: Monitor Progress

Leader monitors via TaskList and incoming messages:
- Track completed vs pending workers
- Handle partial failures gracefully (some workers may fail)
- Collect canvas paths from worker completion messages

### Step 6: Cross-Canvas Pattern Detection

Once all workers complete (or timeout after reasonable period), the leader:

**6a: Common Gaps**
- Read all new canvases
- Grep for `### GAP-` sections
- Identify gaps appearing in 2+ canvases (e.g., "data staleness")

**6b: Archetype Clustering**
- Group users by behavior signals from hypotheses:
  - Comparison-driven (earned vs possible)
  - Completionist (badge/collection focused)
  - Social (mention other users, community)
  - Accuracy-focused (data verification)

**6c: Signal Distribution**
- Aggregate signal types across all canvases
- Calculate weight distribution (HIGH/MEDIUM/LOW)
- Identify dominant signal patterns

### Step 7: Present Summary

Display archetype map and pattern summary to operator:

```
Batch Observation Complete: {N} users processed

Canvases Created:
  - grimoires/observer/canvas/user1.md (Rank #X, {tier})
  - grimoires/observer/canvas/user2.md (Rank #X, {tier})
  ...

Cross-Canvas Patterns:
  - Data staleness: 3/5 users reported (xabbu, elcapitan, ncs)
  - Badge display: 2/5 users mentioned (xabbu, cory)

Archetype Clusters:
  - Comparison-driven: user1, user3 (focus on earned vs possible)
  - Completionist: user2, user5 (badge/collection focus)

Signal Distribution:
  - FEEL: 40% | ACCURACY: 30% | WEIGHTINGS: 20% | UX: 10%

Next Steps:
  1. Review canvases and refine hypotheses to Level 3
  2. Run /gap-to-issues to file cross-user gaps
  3. Run /shape when ready to synthesize journeys
```

### Step 8: Shutdown Team

```
SendMessage:
  type: shutdown_request
  recipient: each worker
```

Then: `TeamDelete`

---

## Counterfactuals — Team Spawning Failures & Partial Results

Batch observing parallelizes canvas creation across multiple users via Claude Code teams. The failure modes are emergent — they arise from the interaction between concurrent workers, not from any single worker's logic.

### Target (Correct Behavior)

The leader spawns one worker per user, each running `/ingest-dm` independently. Workers resolve wallets, call Score API, create canvases, and emit FeedbackEvents. The leader waits for all workers, collects results, detects cross-canvas patterns (shared pain points, common journey fragments), and produces an aggregate report. If a worker fails, the leader logs the failure and continues with successful results.

The critical invariant: the aggregate report accurately reflects which canvases were created, which failed, and what patterns were detected across *only the successful canvases*. Partial success is reported as partial — never inflated to full success.

### Near Miss — Layer Violation

The seductively wrong behavior: treating partial results as complete when calculating cross-canvas patterns.

Scenario: 5 users in batch. Workers for users A, B, C succeed. Workers for D and E fail (wallet resolution timeout). The leader detects a pattern: "3 out of 3 users mentioned score confusion" and reports it as a strong signal. But D and E might have had different experiences — the pattern confidence should be "3 out of 5 attempted" (60%), not "3 out of 3 successful" (100%).

The layer violation is reporting a denominator that excludes failures:
- "All users reported X" (wrong — all *successful* users reported X)
- "Pattern detected across the cohort" (wrong — pattern detected across the successful subset)
- "No users mentioned Y" (wrong — two users weren't asked)

The correct behavior: always report patterns with both denominators — `detected_in / successful_count` and `successful_count / total_attempted`. A pattern found in 3/3 successes from 3/5 attempts is weaker evidence than 3/3 successes from 3/3 attempts. The aggregate report should include a "Coverage" metric showing what fraction of the intended batch completed.

### Category Error — Semantic Collapse

The fundamentally wrong behavior: spawning team workers for users who already have canvases, then merging the new canvas with the existing one as if they were the same observation session.

Batch observing is designed for initial canvas creation from DM exports. If a user already has a canvas (from a prior `/observe` or `/ingest-dm`), spawning a worker for them creates a collision:
- Worker creates a new canvas from the DM export (complete scaffold)
- Existing canvas has curated hypotheses, validated quotes, enrichment history
- Merging overwrites curated content with raw scaffold data

The semantic collapse: treating "create" and "update" as the same operation because the output is the same file format. A new canvas is a hypothesis scaffold (LOW confidence, everything provisional). An existing canvas may contain validated hypotheses (MEDIUM confidence, evidence-backed). Overwriting validated with provisional is data loss.

The correct behavior: before spawning a worker, check if `grimoires/observer/canvas/{username}-canvas.md` exists. If it does, either skip that user (report as "already observed") or run the worker in append-only mode (add new quotes to Quotes Library, do not overwrite User Profile or Level 3 Hypotheses). The leader should report skipped users separately from failed and successful users.

A concrete scenario demonstrating both failure modes together:

Batch of 8 users. Workers for users A, B, C succeed (new canvases). Worker for D fails (Score API timeout). Workers for E, F succeed (new canvases). Worker for G fails (wallet resolution error). Worker for H succeeds but H already had a canvas — the worker overwrites curated hypotheses with a raw scaffold.

The aggregate report says: "6 canvases created, pattern detected: 5/6 users mentioned score confusion." But the actual situation is:
- 5 genuinely new canvases (A, B, C, E, F)
- 1 overwritten canvas (H) — data loss, not creation
- 2 failures (D, G) — unknown user experiences
- Pattern denominator should be "5 out of 8 attempted" not "5 out of 6 successful"

The leader's report should categorize results into four buckets: created (new), updated (existing, append-only), failed (error), and skipped (existing, no new data). Each bucket affects pattern confidence differently.

Additionally, the team spawning itself can fail partially. If Claude Code's team infrastructure limits concurrent workers (e.g., max 5), a batch of 8 users requires sequencing. If the first 5 workers exhaust a rate limit (Score API, Supabase), workers 6-8 may all fail for infrastructure reasons, not data reasons. The leader should distinguish infrastructure failures (retry-worthy) from data failures (skip-worthy) in its error summary.

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Worker fails for one user | Log failure, continue with others. Report partial results. |
| Wallet resolution fails | Worker creates canvas without Score API data |
| Rate limiting on Supabase | Workers retry with backoff (built into supabase-query.sh caching) |
| Team creation fails | Fall back to sequential processing |
| All workers fail | Report error summary, no pattern detection |
| Duplicate canvas (user already has one) | Worker appends new quotes to existing canvas |

---

## Validation

- [ ] One worker spawned per input file
- [ ] Each worker produces a valid canvas
- [ ] Cross-canvas pattern detection runs after all workers complete
- [ ] Partial failures don't block other workers
- [ ] Team is properly shut down after completion
- [ ] Rate limiting respected (staggered starts)

---

## Related

- `/ingest-dm` — Single-user pipeline (this skill parallelizes it)
- `/daily-synthesis` — Complementary pipeline for UI feedback
- `/shape` — Next step after batch observation (requires 3+ canvases)
- `/gap-to-issues` — File cross-user gaps detected in Step 6
