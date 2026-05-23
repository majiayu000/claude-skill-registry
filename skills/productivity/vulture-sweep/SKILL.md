---
name: vulture-sweep
description: Circle high above the issue board, spotting what's dead (implemented but not closed), what's decaying (stale/outdated), and what needs consolidation. The vulture descends, cleans up the carcass, and leaves the backlog healthy. Use when your issue board needs hygiene—closing completed work, consolidating fragments, and removing decay.
---

# Vulture Sweep 🦅

The vulture circles patiently above, seeing what others miss. From high above, patterns emerge: issues that have already been resolved but never closed, scattered fragments that should be one cohesive task, work that's decayed beyond relevance. The vulture doesn't judge. It performs a necessary service that others avoid—nature's cleanup crew. When the vulture descends, it verifies before consuming. When it rises again, the backlog is healthy.

## When to Activate

- Issue board has accumulated cruft over time
- User says "clean up my issues" or "sweep the backlog"
- User calls `/vulture-sweep` or mentions vulture/cleanup
- Suspecting issues are done but never closed
- Finding scattered related issues that should be consolidated
- Quarterly or monthly backlog hygiene
- After a major release (catch implemented-but-not-closed issues)

**IMPORTANT:** This animal NEVER closes issues without codebase verification. It only closes what has been proven complete.

**Pair with:** `bee-collect` when finding work that needs new issues, `badger-triage` for organizing what remains

---

## The Sweep

```
CIRCLE → SPOT → DESCEND → CLEAN → REPORT
   ↓        ↓        ↓         ↓        ↓
 Survey   Identify  Verify   Close/   Summary
 Board    Stale     in Code  Consol.  & Stats
```

### Phase 1: CIRCLE

_The vulture rises on thermal currents, patient eyes scanning the landscape below..._

Survey the entire issue board:

**Gather all open issues:**

```bash
# Get all open issues with metadata
gh issue list --repo AutumnsGrove/GroveEngine --state open --limit 200 --json number,title,labels,createdAt,updatedAt,body
```

**Build the mental map:**

- Group by age (>90 days old = potential decay)
- Group by labels (component clusters)
- Group by keywords in titles (similar work patterns)
- Note issues with "implemented", "done", "completed" in comments

**Age thresholds:**
| Age | Status |
|-----|--------|
| < 30 days | Fresh |
| 30-90 days | Aging |
| 90-180 days | Stale |
| > 180 days | Decaying |

**Output:** Complete map of the issue board with age and pattern analysis

---

### Phase 2: SPOT

_Sharp eyes catch movement. Something dead lies in the grass..._

Identify candidates for cleanup:

**Category 1: Likely Implemented (Dead)**
Look for signals that work may be done:

- Old issues with recent related commits
- Issues mentioning features that now exist
- Bug reports for bugs that may be fixed
- Enhancement requests that match current behavior

**Category 2: Stale/Outdated (Decaying)**
Look for signals of irrelevance:

- References to deprecated technology
- Issues about removed features
- Problems that no longer apply to current architecture
- Outdated acceptance criteria

**Category 3: Fragmented (Scattered Bones)**
Look for consolidation opportunities:

- Multiple issues about the same component
- Overlapping acceptance criteria
- Issues that are subtasks of a larger effort
- Duplicates with slightly different wording

**Candidate List Format:**

```markdown
## Candidates Spotted

### Likely Implemented

| #    | Title                | Age  | Signal                    |
| ---- | -------------------- | ---- | ------------------------- |
| #234 | Add dark mode toggle | 120d | Feature exists in Foliage |
| #267 | Fix login redirect   | 85d  | Recent auth commits       |

### Potentially Stale

| #    | Title                 | Age  | Signal         |
| ---- | --------------------- | ---- | -------------- |
| #189 | Update webpack config | 200d | Now using Vite |

### Consolidation Candidates

| Issues           | Theme               | Recommendation            |
| ---------------- | ------------------- | ------------------------- |
| #301, #305, #312 | Accessibility fixes | Combine into "A11y audit" |
```

**Output:** Categorized candidates ready for verification

---

### Phase 3: DESCEND

_The vulture folds its wings and drops, examining closely what it found from above..._

Verify each candidate in the codebase:

**For "Likely Implemented" candidates:**

```bash
# Grove Find — verify implementation exists
gf --agent search "darkMode"          # Does the feature exist in code?
gf --agent search "ThemeToggle"       # Find the component
gf --agent func "toggleDarkMode"      # Find the function

# Check git history for evidence
git log --oneline --all --grep="dark mode" -10
git log --oneline --all -- "src/lib/stores/theme*"
```

**Verification Checklist:**

- [ ] Core functionality exists in code
- [ ] No TODO comments indicating incomplete work
- [ ] Tests pass (if applicable)
- [ ] Feature accessible in the UI (if applicable)

**Verification Outcomes:**

| Outcome        | Evidence Required                      | Action                               |
| -------------- | -------------------------------------- | ------------------------------------ |
| Fully Done     | Code exists, tests pass, feature works | Close with detailed comment          |
| Partially Done | Some code exists, more needed          | Keep open, update description        |
| Not Started    | No evidence found                      | Keep open                            |
| Obsolete       | Feature no longer relevant             | Close as "won't do" with explanation |

**For "Fragmented" candidates:**

- Read all related issues
- Identify the unifying theme
- Draft consolidated issue description
- List which issues would be closed

**Output:** Verified candidates with evidence documented

---

### Phase 4: CLEAN

_The vulture consumes what is dead, leaving the ecosystem healthier..._

Execute the cleanup:

**Grove Tools for bulk cleanup:**

```bash
# Single issue close
gw gh issue close --write NUMBER --comment "Verified complete — evidence in src/lib/..."

# Bulk operations — close multiple verified issues at once
gw gh issue batch --write --close 234,267,289 --comment "Vulture sweep: verified implemented"
```

**Closing Implemented Issues (with detailed comments):**

```bash
gh issue close NUMBER --comment "$(cat <<'EOF'
🦅 **Vulture Sweep: Verified Complete**

This issue has been implemented and verified in the codebase:

**Evidence Found:**
- Feature implemented in `src/lib/stores/theme.ts`
- Dark mode toggle exists in `src/lib/components/ThemeToggle.svelte`
- Tests passing in `tests/theme.test.ts`
- Verified working in production UI

**Commits:**
- abc1234 feat(foliage): add dark mode support
- def5678 test(foliage): add theme toggle tests

Closing as complete. Thank you for the contribution!
EOF
)"
```

**Closing Obsolete Issues:**

```bash
gh issue close NUMBER --reason "not planned" --comment "$(cat <<'EOF'
🦅 **Vulture Sweep: No Longer Applicable**

This issue is being closed as it no longer applies to the current codebase:

**Reason:**
- Grove migrated from Webpack to Vite in January 2026
- Webpack configuration no longer exists
- The underlying problem this addressed is obsolete

If similar issues arise with the current Vite setup, please open a new issue.
EOF
)"
```

**Creating Consolidated Issues:**

```bash
gh issue create --title "Consolidated: Accessibility improvements" --body "$(cat <<'EOF'
## Summary

This issue consolidates several related accessibility tasks into a single trackable effort.

## Consolidated From

- #301 — Add aria labels to navigation
- #305 — Fix focus ring visibility
- #312 — Improve screen reader announcements

## Acceptance Criteria

- [ ] All navigation elements have appropriate aria labels
- [ ] Focus rings are visible in all themes
- [ ] Screen reader announcements work for dynamic content
- [ ] WCAG AA compliance verified

## Context

These issues were identified during vulture sweep as fragments of a larger accessibility effort. Consolidating for clearer tracking.
EOF
)" --label "accessibility,enhancement"

# Close the original issues with reference
gh issue close 301 --comment "🦅 Consolidated into #NEW_NUMBER"
gh issue close 305 --comment "🦅 Consolidated into #NEW_NUMBER"
gh issue close 312 --comment "🦅 Consolidated into #NEW_NUMBER"
```

**Output:** Issues closed, consolidations created, backlog cleaned

---

### Phase 5: REPORT

_The vulture rises again, circling once more to survey the cleaner landscape..._

Report the sweep results:

```markdown
🦅 VULTURE SWEEP COMPLETE

## Summary

| Action                            | Count |
| --------------------------------- | ----- |
| Issues Closed (Implemented)       | 7     |
| Issues Closed (Obsolete)          | 3     |
| Consolidations Created            | 2     |
| Issues Kept (Verified Incomplete) | 5     |

## Issues Closed as Implemented

| #    | Title                | Evidence                  |
| ---- | -------------------- | ------------------------- |
| #234 | Add dark mode toggle | Feature in theme.ts       |
| #267 | Fix login redirect   | Verified in auth flow     |
| #289 | Add loading states   | Skeleton components exist |
| ...  | ...                  | ...                       |

## Issues Closed as Obsolete

| #    | Title                 | Reason                   |
| ---- | --------------------- | ------------------------ |
| #189 | Update webpack config | Migrated to Vite         |
| #201 | Fix IE11 support      | IE11 no longer supported |
| #215 | Update Node 14 deps   | Now on Node 20           |

## Consolidations

| New Issue | Absorbed         | Theme             |
| --------- | ---------------- | ----------------- |
| #534      | #301, #305, #312 | Accessibility     |
| #535      | #298, #303       | Mobile navigation |

## Remaining Cleanup Opportunities

These issues may need attention but require human decision:

- #245 "Improve performance" — too vague to verify
- #278 "Consider alternative auth" — needs design decision
- #291 "Maybe add feature X" — unclear if still wanted

## Backlog Health

| Metric            | Before  | After   |
| ----------------- | ------- | ------- |
| Open Issues       | 87      | 72      |
| Average Age       | 95 days | 67 days |
| Issues > 180 days | 12      | 3       |

_The carrion is cleared. The forest breathes easier._
```

---

## Vulture Rules

### Patience

Circle first. Never swoop without surveying. The full picture matters.

### Verification

**Always verify before closing.** The vulture's reputation depends on accuracy. Never close an issue without codebase evidence that it's truly complete or obsolete.

### Respect

Close with detailed comments. The original reporter deserves to know _why_ their issue is being closed and _what_ was found.

### Consolidation Over Fragmentation

When you find scattered related issues, consolidate them. One clear issue beats five overlapping ones.

### Communication

Use sweep metaphors:

- "Circling the board..." (surveying)
- "Spotting candidates..." (identifying)
- "Descending to verify..." (checking codebase)
- "Cleaning up..." (closing/consolidating)
- "Rising to report..." (summary)

---

## Anti-Patterns

**The vulture does NOT:**

- Close issues without codebase verification
- Assume something is done because it's old
- Touch issues marked "in progress" or assigned
- Delete issues (only closes with clear reasoning)
- Close issues that need human decision (marks for review instead)
- Guess at implementation status
- Skip the detailed closure comment

---

## Example Sweep

**User:** "/vulture-sweep — the backlog is getting crusty"

**Vulture flow:**

1. 🦅 **CIRCLE** — "Circling the board... 87 open issues found. 12 over 180 days old. 23 between 90-180 days. Patterns emerging in auth, UI, and infrastructure clusters."

2. 🦅 **SPOT** — "Spotted 15 candidates:
   - 7 likely implemented (dark mode, auth fixes, loading states)
   - 3 potentially obsolete (webpack, IE11, Node 14)
   - 5 fragmentation opportunities (a11y cluster, mobile nav)"

3. 🦅 **DESCEND** — "Descending to verify...
   - #234 dark mode: VERIFIED (found in theme.ts, toggle component exists)
   - #267 login redirect: VERIFIED (auth flow handles it)
   - #245 'improve performance': CANNOT VERIFY (too vague, keeping open)"

4. 🦅 **CLEAN** — "Closing 10 verified issues with detailed comments. Creating 2 consolidations. Marking 5 for human review."

5. 🦅 **REPORT** — "Sweep complete: 15 issues resolved, 2 consolidations created, backlog reduced from 87 to 72. Average age improved from 95 to 67 days."

---

## Quick Decision Guide

| Situation                | Approach                                             |
| ------------------------ | ---------------------------------------------------- |
| Issue clearly done       | Verify in code, close with evidence                  |
| Issue partially done     | Keep open, update description with findings          |
| Issue obsolete           | Close as "not planned" with explanation              |
| Multiple related issues  | Consolidate into one, close originals with reference |
| Issue vague/unclear      | Keep open, flag for human review                     |
| Issue has assignee       | Skip (someone's working on it)                       |
| Recent issue (< 30 days) | Skip unless clearly implemented                      |

---

## Integration with Other Skills

**Before Sweeping:**

- `bloodhound-scout` — If you need to understand the codebase first

**During Sweeping:**

- `bee-collect` — If you find new work that needs issues
- `badger-triage` — If remaining issues need organizing

**After Sweeping:**

- `owl-archive` — To document any patterns discovered
- `gathering-planning` — If cleanup revealed planning needs

---

_Nature's cleanup crew. Patient, thorough, necessary._ 🦅
