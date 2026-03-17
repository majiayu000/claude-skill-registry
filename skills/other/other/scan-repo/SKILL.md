---
name: scan-repo
description: Scan docs/business-os/ for changes and create business-relevant ideas from findings.
---

# Scan Repo

Scan the Business OS document tree for changes since the last scan, analyze updates for business relevance, and optionally create ideas based on findings. Provides context for prioritization and review.

## Operating Mode

**READ + ANALYZE + OPTIONAL WRITE (IDEAS ONLY)**

**Allowed:**
- Run git commands to detect changes in `docs/business-os/`
- Read and analyze changed files
- Create scan result artifacts in `docs/business-os/scans/`
- Create new ideas in inbox if findings warrant it
- Update last-scan timestamp

**Not allowed:**
- Modifying existing cards or ideas
- Creating cards directly (use `/work-idea` for that)
- Scanning outside `docs/business-os/` directory
- Automated actions based on scan (Phase 0: informational only)

## Inputs

**Optional:**
- Scan mode: `full` (scan all files) or `incremental` (since last scan, default)
- Create ideas: `true` (auto-create ideas from significant findings) or `false` (report only, default)

## Scan Output Schema

### `docs/business-os/scans/last-scan.json`
```json
{
  "lastCommit": "abc123def456",
  "scanDate": "2026-01-28T14:30:00Z",
  "changedFiles": [
    {
      "path": "docs/business-os/cards/BRIK-ENG-0001.user.md",
      "status": "M",
      "changeType": "modified"
    },
    {
      "path": "docs/business-os/ideas/inbox/new-idea.md",
      "status": "A",
      "changeType": "added"
    }
  ],
  "summary": {
    "cardsModified": 3,
    "cardsAdded": 1,
    "cardsDeleted": 0,
    "ideasModified": 2,
    "ideasAdded": 1,
    "plansModified": 0
  }
}
```

### `docs/business-os/scans/active-docs.json`
```json
{
  "scanDate": "2026-01-28T14:30:00Z",
  "cards": [
    {
      "id": "BRIK-ENG-0001",
      "lane": "Fact-finding",
      "priority": "P2",
      "business": "BRIK",
      "owner": "Pete",
      "lastUpdated": "2026-01-28",
      "title": "Add user authentication to guide booking flow"
    }
  ],
  "ideas": [
    {
      "id": "BRIK-OPP-0002",
      "status": "raw",
      "business": "BRIK",
      "location": "inbox",
      "createdDate": "2026-01-27"
    }
  ],
  "plans": [
    {
      "business": "BRIK",
      "lastReviewed": "2026-01-15",
      "path": "docs/business-os/strategy/BRIK/plan.user.md"
    }
  ]
}
```

### `docs/business-os/scans/history/{timestamp}.json`
Snapshot of scan results for audit trail (same schema as `last-scan.json`).

## Workflow

### 1. Determine Scan Scope

```bash
# Get last scan commit (from last-scan.json)
LAST_COMMIT=$(jq -r '.lastCommit' docs/business-os/scans/last-scan.json 2>/dev/null || echo "HEAD~30")

# If full scan requested, use initial commit
if [ "$FULL_SCAN" = "true" ]; then
  LAST_COMMIT=$(git rev-list --max-parents=0 HEAD)
fi
```

### 2. Scan for Changes

```bash
# Get changed files since last scan
git diff $LAST_COMMIT...HEAD --name-status -- docs/business-os/ > /tmp/changes.txt

# Get unstaged/untracked files
git status --porcelain docs/business-os/ >> /tmp/changes.txt

# Parse output:
# M  docs/business-os/cards/BRIK-ENG-0001.user.md (modified)
# A  docs/business-os/ideas/inbox/new-idea.md (added)
# D  docs/business-os/cards/archive/OLD-001.user.md (deleted)
# ?? docs/business-os/ideas/inbox/untracked.md (untracked)
```

### 3. Categorize Changes

Parse each changed file and categorize:

- **Cards:**
  - Modified: Lane transitions, owner changes, priority updates
  - Added: New opportunities or feature requests
  - Deleted: Archived or cancelled work

- **Ideas:**
  - Inbox: New submissions, raw opportunities
  - Worked: Ideas being developed into cards

- **Plans:**
  - Business plan updates (strategy changes)
  - People updates (team changes)

- **Stage Docs:**
  - Fact-finding progress
  - Plan document updates
  - Build/Done documentation
  - Reflections

### 4. Analyze Business Relevance

For each significant change, assess:

**High relevance (create idea):**
- New card in P0/P1 priority
- Card moved to Blocked lane (needs attention)
- Fact-finding complete but no plan created
- Business plan updated with new strategic direction

**Medium relevance (report only):**
- Card progressing normally (Inbox → Fact-finding → Planned)
- Routine updates to existing cards
- Stage doc updates

**Low relevance (omit from report):**
- Formatting changes
- Typo fixes
- Archive operations

### 5. Create Ideas (If Enabled)

When `createIdeas: true` and high-relevance changes detected:

```markdown
---
Type: Idea
ID: SCAN-BRIK-001
Business: BRIK
Status: raw
Created-Date: 2026-01-28
Tags: ["scan-generated", "review-needed"]
Source: Repository scan
---

# Review blocked card: BRIK-ENG-0001

## Finding
Card BRIK-ENG-0001 moved to Blocked lane on 2026-01-28.

## Blocker
Waiting for platform auth team to confirm GDPR compliance.

## Recommendation
1. Follow up with legal team
2. Consider alternative approach if blocker takes >1 week
3. Document decision in stage doc

## Evidence
- Card: `docs/business-os/cards/BRIK-ENG-0001.user.md`
- Change: Lane transition (In progress → Blocked)
- Date: 2026-01-28
```

### 6. Generate Scan Reports

**`last-scan.json`:**
```json
{
  "lastCommit": "abc123def456",
  "scanDate": "2026-01-28T14:30:00Z",
  "changedFiles": [...],
  "summary": {...}
}
```

**`active-docs.json`:**
```json
{
  "scanDate": "2026-01-28T14:30:00Z",
  "cards": [...],
  "ideas": [...],
  "plans": [...]
}
```

**`history/2026-01-28T14-30-00Z.json`:**
Snapshot copy of scan results for audit trail.

### 7. Output Summary

Display human-readable summary:

```
Repository Scan Complete
========================

Scan Range: abc123 → def456 (since 2026-01-26)
Scan Date: 2026-01-28 14:30:00 UTC

Changes Detected:
- Cards: 3 modified, 1 added, 0 deleted
- Ideas: 2 modified, 1 added (inbox)
- Plans: 0 modified
- Stage Docs: 4 updated

Highlights:
✓ BRIK-ENG-0001: Moved to Blocked (needs review)
✓ BRIK-ENG-0002: Fact-finding complete, ready for planning
✓ BRIK-OPP-0003: New idea submitted in inbox

Ideas Created: 1
- SCAN-BRIK-001: Review blocked card BRIK-ENG-0001

Next Actions:
1. Review ideas created from scan
2. Use /work-idea to convert promising ideas to cards
3. Use /propose-lane-move to progress unblocked cards

Scan artifacts saved to docs/business-os/scans/
```

## Integration with Other Skills

- **After scan:** Use `/work-idea` to convert scan-generated ideas to cards
- **Blocked cards:** Use scan to identify blockers, then `/propose-lane-move` when unblocked
- **Business plan updates:** Scan detects changes, use `/update-business-plan` to sync plan with reality
- **Fact-finding gaps:** Scan finds cards in Fact-finding with stale stage docs, prompts review

## Example Session

```
User: /scan-repo

Agent:
Scanning docs/business-os/ for changes since last scan...

[Running git diff]
Last scan: 2026-01-26 (commit abc123)
Current: 2026-01-28 (commit def456)

[Analyzing 8 changed files]
✓ Cards: 3 modified
  - BRIK-ENG-0001: Inbox → Fact-finding (2026-01-27)
  - BRIK-ENG-0001: Fact-finding → Blocked (2026-01-28) ⚠️
  - BRIK-ENG-0002: Fact-finding stage doc updated

✓ Ideas: 2 new
  - BRIK-OPP-0003: Guide offline mode (inbox)
  - BRIK-OPP-0004: Mobile app push notifications (inbox)

✓ Plans: 0 changes

[Business relevance analysis]
High relevance:
- BRIK-ENG-0001 blocked (needs attention)

Medium relevance:
- 2 new ideas in inbox (normal flow)
- 1 stage doc update (routine)

[Creating idea for blocked card]
✓ Created: SCAN-BRIK-001 (Review blocked card)

[Saving scan artifacts]
✓ docs/business-os/scans/last-scan.json
✓ docs/business-os/scans/active-docs.json
✓ docs/business-os/scans/history/2026-01-28T14-30-00Z.json

Scan complete! 1 idea created, 3 cards updated.

Next steps:
1. Review SCAN-BRIK-001 (blocked card alert)
2. Work up BRIK-OPP-0003 and BRIK-OPP-0004 (new inbox ideas)
```

## Scan Frequency Recommendations

- **Daily scans:** During active development periods
- **Weekly scans:** During quieter periods
- **On-demand scans:** Before planning sessions, after major milestones
- **Full scans:** Monthly, to catch missed changes and verify consistency

## Error Handling

- **No last-scan.json:** Treat as first scan, use `HEAD~30` as baseline
- **Git errors:** Fail gracefully, suggest running `git status` manually
- **Malformed docs:** Log warning, skip file, continue scan
- **Scan artifacts locked:** Wait and retry, or skip if non-critical

## Phase 0 Constraints

- Pete-triggered only (no automated scheduling)
- Agent identity for scan artifact commits
- Informational only (no automated actions on scan results)
- Scan limited to `docs/business-os/` (no cross-repo scanning)
- Single business context (global board shows P0/P1 from all businesses)

## Success Metrics

- Scan completion time: <2 seconds for incremental, <10 seconds for full
- False positives: <10% (ideas created that Pete immediately dismisses)
- Coverage: 100% of changes in `docs/business-os/` detected
- Idea conversion: ≥50% of scan-generated ideas become cards
