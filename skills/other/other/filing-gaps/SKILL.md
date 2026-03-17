---
name: filing-gaps
description: Create GitHub/Linear issues from gap analysis reports with proper taxonomy labels. Use when you need to file a gap as a trackable issue.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Filing Gaps

Create structured issues from Laboratory gap analysis reports with proper taxonomy labels and artifact linking.

---

## Trigger

```
/file-gap {journey-id} {gap-id}              # File specific gap as issue
/file-gap {journey-id} --all                 # File all open gaps
/file-gap {journey-id} {gap-id} --provider {github|linear}  # Specify provider
/file-gap {journey-id} {gap-id} --dry-run    # Preview without creating
```

**Examples:**
```bash
/file-gap reward-understanding GAP-reward-understanding-3
/file-gap reward-understanding --all
/file-gap deposit-flow GAP-deposit-flow-1 --provider github
/file-gap reward-understanding GAP-reward-understanding-4 --dry-run
```

---

## Taxonomy Labels

Issues are tagged with a structured taxonomy for organization:

### [A] Artifact Type

| Label | Description | Use Case |
|-------|-------------|----------|
| `[A] Bug Report` | Defect in existing functionality | Code doesn't work as designed |
| `[A] Feature Request` | New functionality needed | Missing capability |
| `[A] Experiment Design` | Hypothesis to validate | Need to test before building |
| `[A] Product Spec` | Specification document | Design/scope definition |
| `[A] Tech Debt` | Technical improvement | Refactoring, optimization |

### [W] Workstream

| Label | Description | Use Case |
|-------|-------------|----------|
| `[W] Discovery` | Research and validation | Understanding user needs |
| `[W] Delivery` | Implementation work | Building features |
| `[W] Experimentation` | Hypothesis testing | A/B tests, prototypes |
| `[W] Tech Debt` | Technical improvements | Performance, maintainability |
| `[W] Operations` | Operational work | Monitoring, support |

### [J] Job-to-be-Done

Maps to user JTBD from UTC canvases:

| Label | Description |
|-------|-------------|
| `[J] Find Information` | User needs to discover/learn something |
| `[J] Reassure Me This Is Safe` | User needs trust/confidence |
| `[J] Make Transaction` | User needs to execute an action |
| `[J] Give Me Peace of Mind` | User needs ongoing assurance |
| `[J] Reduce My Anxiety` | User needs clarity about state |
| `[J] Help Me Feel Smart` | User wants to understand/verify |
| `[J] Organize Assets` | User wants control/organization |

### [LS] Learning Status

From UTC learning status of affected users:

| Label | Description |
|-------|-------------|
| `[LS] Strongly Validated` | Multiple users, high confidence |
| `[LS] Directionally Correct` | Some evidence, medium confidence |
| `[LS] Smol Evidence` | Limited data, low confidence |

### [SO] Source

| Label | Description |
|-------|-------------|
| `[SO] User Research` | From user interviews/feedback |
| `[SO] Analytics` | From usage data |
| `[SO] Code Review` | From code analysis |
| `[SO] Walkthrough` | From interactive testing |
| `[SO] Gap Analysis` | From Laboratory gap analysis |

---

## Workflow

### Step 1: Load Gap Report

Read gap report:
```bash
grimoires/crucible/gaps/{journey-id}-gaps.md
```

Parse frontmatter and find specified gap by ID.

### Step 2: Load Gap Details

For the specified gap, extract:
- Gap ID
- Type (Bug/Feature/Flow/Communication/Strategy)
- Severity (Critical/High/Medium/Low)
- JTBD impact
- User Expects (with quotes and source canvas)
- Code Does (with file:line references)
- Gap description
- Resolution recommendations

### Step 3: Load Source Canvas Context

For each linked canvas:
- Read UTC file
- Extract learning status
- Get JTBD (primary/secondary)
- Get relevant quotes

### Step 3.5: Source Fidelity Classification

Before creating any GitHub issue, classify the gap's evidence to prevent filing inferred features as concrete requests.

**4-Category Evidence Taxonomy:**

| Category | Criteria | Filing Action |
|----------|----------|---------------|
| **(a) User-reported bug** | Direct quote describes broken behavior ("X doesn't work", "X shows wrong value") | File as issue |
| **(b) User-expressed need** | Quote contains explicit request ("I wish...", "Would like to see...", "Can I...") | File as issue |
| **(c) Observed behavioral gap** | User behavior implies X but no explicit quote requesting it | File with `observed-pattern` label added to labels array |
| **(d) Inferred feature** | Extrapolated from user vision/sentiment — no direct quote supports the specific issue | **BLOCK — do not file** |

**Gate Logic:**

1. Locate the supporting quote in the source canvas's Quotes Library
2. Verify the quote **directly** supports the issue being filed — no interpretation required
3. If the quote requires interpretation to connect to the issue → classify as category (c) or (d)
4. For category (d): output warning explaining why this gap cannot be filed, suggest keeping it in canvas hypotheses. Log the block to `grimoires/loa/NOTES.md` learnings section
5. For category (c): proceed with filing but add `observed-pattern` to the GitHub labels

**Provenance**: This gate was added after midi#95 was retracted (2026-02-17) — a user's vision statement was extrapolated into a feature request without direct quote support.

---

### Step 4: Map to Taxonomy Labels

**Gap Type → Artifact Type:**
| Gap Type | Artifact Label |
|----------|----------------|
| Bug | `[A] Bug Report` |
| Feature | `[A] Feature Request` |
| Flow | `[A] Feature Request` or `[A] Experiment Design` |
| Communication | `[A] Product Spec` |
| Strategy | `[A] Experiment Design` |

**Gap Severity → Priority:**
| Severity | Priority |
|----------|----------|
| Critical | P0 / Urgent |
| High | P1 / High |
| Medium | P2 / Medium |
| Low | P3 / Low |

**Gap Type → Workstream:**
| Gap Type | Workstream |
|----------|------------|
| Bug | `[W] Delivery` or `[W] Tech Debt` |
| Feature | `[W] Delivery` |
| Flow | `[W] Discovery` |
| Communication | `[W] Delivery` |
| Strategy | `[W] Discovery` or `[W] Experimentation` |

### Step 5: Generate Issue Content

**Title Format:**
```
[{Gap Type}] {Short Title}
```

**Body Template:**
```markdown
## Gap Analysis

**Journey**: {journey-id}
**Gap ID**: {gap-id}
**Severity**: {severity}
**Type**: {type}

### User Expects

> {User expectation description}
>
> Source: **{canvas-username}**, quote: "{relevant quote}"

### Code Does

> {Actual code behavior description}
>
> Source: `{file}:{line}`

### Gap Description

{Detailed description of the discrepancy}

### Proposed Resolution

{Resolution recommendations from gap report}

---

## Labels

- {Artifact label}
- {Workstream label}
- {JTBD label}
- {Learning Status label}
- `[SO] Gap Analysis`
- `laboratory`
- `{journey-id}`

---

## Evidence

### User Research

| User | Quote | Canvas |
|------|-------|--------|
| {username} | "{quote}" | [Link]({canvas-path}) |

### Code References

| File | Line | Description |
|------|------|-------------|
| {file} | {line} | {description} |

---

## Laboratory Artifacts

- **Gap Report**: `grimoires/crucible/gaps/{journey-id}-gaps.md`
- **Journey**: `grimoires/observer/journeys/{journey-id}.md`
- **Reality**: `grimoires/observer/reality/{component}-reality.md`
- **Canvas(es)**: {list of source canvases}
```

### Step 5.5: Enrich with Visual Evidence

Before generating the issue command, scan the MER timeline for snapshots of the affected wallet:

```bash
# Find MERs for the affected wallet(s) from gap report
wallet_alias=$(echo "$gap" | grep -oP 'Canvas: `canvas/\K[^.]+')
mer_files=$(grep -rl "wallet_alias: $wallet_alias" grimoires/observer/timeline/MER-*.md 2>/dev/null || true)
```

If MER(s) found:

1. Extract from the most recent MER:
   - `screenshot_url` from frontmatter (may be null)
   - `combined_score`, `overall_rank`, `crowd_tier_display`, `elite_tier_display` from Data State
   - `mer_id` for cross-reference

2. Append a **Visual Evidence** section to the issue body (before Labels):

```markdown
### Visual Evidence

**MER**: [[timeline/{mer_id}]]
**Snapshot Date**: {event_date}

![Profile Snapshot]({screenshot_url})

### Score Position at Capture

| Metric | Value |
|--------|-------|
| Combined Score | {combined_score} |
| Overall Rank | #{overall_rank} |
| Crowd Tier | {crowd_tier_display} |
| Elite Tier | {elite_tier_display} |
```

3. If no screenshot URL (visual capture failed or data-only MER):

```markdown
### Visual Evidence

**MER**: [[timeline/{mer_id}]] (data-only, no screenshot)

### Score Position at Capture

| Metric | Value |
|--------|-------|
| Combined Score | {combined_score} |
| Overall Rank | #{overall_rank} |
| Crowd Tier | {crowd_tier_display} |
| Elite Tier | {elite_tier_display} |
```

**Graceful fallback**: If no MER exists for the affected wallet, skip this section entirely — the issue is filed with text-only evidence (existing behavior).

### Step 6: Output Issue Command

**For GitHub:**
```bash
gh issue create \
  --title "[{Type}] {Title}" \
  --body "$(cat <<'EOF'
{issue body content}
EOF
)" \
  --label "{label1}" \
  --label "{label2}" \
  --label "laboratory"
```

**For Linear:**
```bash
# Linear CLI command (if using linear-cli)
linear issue create \
  --title "[{Type}] {Title}" \
  --description "{issue body}" \
  --label "{label1}" \
  --priority "{priority}"
```

### Step 7: Update Gap Report

If issue created (not dry-run), update gap report:

```markdown
### Gap {N}: {Title}

...

**Linked Artifacts**:
- Canvas: `canvas/{username}.md`
- Reality: `reality/{component}-reality.md:{line}`
- Issue: `{REPO}#{NUMBER}` ← NEW
```

### Step 8: Report Output

**Dry Run:**
```
┌─────────────────────────────────────────────────────────────────┐
│ FILE GAP: DRY RUN                                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Gap: GAP-reward-understanding-3                                │
│  Type: Communication                                            │
│  Severity: Medium                                               │
│                                                                 │
│  Proposed Issue:                                                │
│  ───────────────                                                │
│  Title: [Communication] Transaction dialog lacks step context   │
│                                                                 │
│  Labels:                                                        │
│  - [A] Product Spec                                             │
│  - [W] Delivery                                                 │
│  - [J] Reassure Me This Is Safe                                 │
│  - [LS] Strongly Validated                                      │
│  - [SO] Gap Analysis                                            │
│  - laboratory                                                   │
│                                                                 │
│  Priority: P2 (Medium)                                          │
│                                                                 │
│  Body Preview:                                                  │
│  {first 200 chars of body}...                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

To create issue:
  /file-gap reward-understanding GAP-reward-understanding-3

Or manually:
  gh issue create --title "[Communication] Transaction dialog lacks step context" ...
```

**Issue Created:**
```
✓ Issue created: {REPO}#{NUMBER}

Gap: GAP-reward-understanding-3
Issue: https://github.com/{owner}/{repo}/issues/{number}

Labels Applied:
  - [A] Product Spec
  - [W] Delivery
  - [J] Reassure Me This Is Safe
  - [LS] Strongly Validated
  - [SO] Gap Analysis
  - laboratory

Gap report updated with issue link.

Next Steps:
  - View issue: gh issue view {number}
  - File next gap: /file-gap reward-understanding GAP-reward-understanding-4
  - View all gaps: Read grimoires/crucible/gaps/reward-understanding-gaps.md
```

---

## File All Mode (`--all`)

When `--all` is specified:

1. Read gap report
2. Filter to open gaps (no issue linked)
3. For each gap:
   - Generate issue content
   - Create issue (or dry-run)
   - Update gap report
4. Report summary

```
✓ Filed 3 issues

| Gap ID | Title | Issue | Priority |
|--------|-------|-------|----------|
| GAP-3 | Transaction context | #123 | P2 |
| GAP-4 | APY calculation | #124 | P1 |
| GAP-5 | Loading indicator | #125 | P3 |

Gap report updated: grimoires/crucible/gaps/reward-understanding-gaps.md
```

---

## Provider Configuration

**GitHub (default):**
- Uses `gh` CLI
- Requires `gh auth login`
- Creates issues in current repo

**Linear:**
- Uses Linear CLI or API
- Requires Linear API key
- Creates issues in configured team

**Detection:**
- Check for `.github` directory → GitHub
- Check for `linear.config.json` → Linear
- Use `--provider` flag to override

---

## Counterfactuals — Issue Routing & Gap Classification

Filing gaps bridges the research layer (canvases, gap reports) and the engineering layer (GitHub issues, labels, repos). The failure modes are routing errors — sending the right signal to the wrong destination, or mislabeling the signal's nature.

### Target (Correct Behavior)

The skill reads a gap report from `/analyze-gap`, resolves the target repository by examining which codebase owns the affected component, selects labels from the repo's existing label taxonomy, drafts an issue body with evidence from the gap report (user quotes, expected vs. actual, source canvases), and files via `gh issue create`. Before filing, it checks for existing issues with similar titles or gap IDs to prevent duplicates.

The repo routing decision follows component ownership:
- Score calculation logic → `score-api`
- Frontend display, UX, page behavior → `midi-interface`
- Framework/tooling → `loa` or `loa-constructs`
- Ambiguous → ask the operator

### Near Miss — Semantic Drift

The seductively wrong behavior: routing by keyword rather than component ownership.

A gap report says: "User expected their OG score to reflect recent mints, but the displayed score hasn't updated." The word "score" appears — so the skill routes to `score-api`. But the actual gap may be:
- **score-api**: The scoring engine hasn't recalculated (calculation bug)
- **midi-interface**: The frontend is caching stale data (display bug)
- **Both**: The score updated but the frontend didn't refetch (integration gap)

Keyword matching ("score" → score-api) creates systematic misrouting. The correct signal is the *component boundary where the gap lives*: if the score-api returns the correct value but the frontend shows the old one, it's a frontend issue regardless of the word "score" in the description.

The skill should trace the data flow: user action → API call → response → display. The gap lives at the boundary where expected and actual diverge. Filing to the wrong repo means the issue sits unnoticed by the team that can fix it.

### Category Error — Layer Violation

The fundamentally wrong behavior: filing a gap as a bug when it is actually a feature request, or vice versa.

The distinction matters because bugs and feature requests follow different workflows:
- **Bug**: something broke or doesn't match specification → fix, regression test
- **Feature request**: something works as designed but doesn't match user expectation → evaluate, prioritize, maybe build
- **Discoverability gap**: the feature exists but the user can't find it → UX improvement, documentation

A user says "I thought cubquest badges would show up in my score." This could be:
- A **bug** if cubquest badges are supposed to be included in the scoring model
- A **feature request** if cubquest badges are intentionally excluded
- A **discoverability gap** if cubquest badges *are* included but under a different label

The gap report from `/analyze-gap` provides the `gap_type` field (Bug | Feature | Discoverability), but the skill must verify this classification against code reality before filing. A gap report generated from user quotes alone may misclassify — the user's expectation is not the specification. Cross-referencing the gap report's `expected` field against the actual codebase behavior (from `/ground` reality files) resolves the ambiguity.

Filing a feature request as a bug creates false urgency. Filing a bug as a feature request creates false patience. Both waste engineering time.

A concrete example from this ecosystem: a user reports "my cubquest badges don't show in my score." The gap report says `expected: cubquest badges contribute to score` vs `actual: cubquest badges not visible in score breakdown`.

Possible classifications:
- **Bug**: The scoring model includes cubquest badges but the frontend `holdings_breakdown` component doesn't display them → fix the display code
- **Feature**: The scoring model intentionally excludes cubquest badges (only mibera badges count) → product decision needed, not a code fix
- **Discoverability**: Cubquest badges DO contribute (via the `nft_score` dimension) but aren't labeled as "cubquest" in the UI → improve labeling

Each classification routes to a different team with different urgency. The filing skill must check the score-api's factor configuration (which badge types are included) before choosing the classification. The gap report alone — based on user quotes — cannot resolve this ambiguity because the user's expectation is not the specification.

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Gap not found | List available gaps in report |
| Gap report not found | Suggest running /analyze-gap first |
| Gap already filed | Show existing issue link, offer to update |
| gh CLI not found | Provide installation instructions |
| Not in git repo | Prompt for repo context |
| Auth required | Guide through `gh auth login` |

---

## Gap ID Format

Gap IDs follow the pattern:
```
GAP-{journey-id}-{number}
```

**Examples:**
- `GAP-reward-understanding-1`
- `GAP-deposit-flow-3`
- `GAP-informed-decision-2`

---

## Integration Points

- **analyzing-gaps**: Gap reports as input
- **walking-through**: Gaps discovered during walkthroughs
- **iterating-feedback**: Gap resolution tracking
- **GitHub/Linear**: Issue creation

---

## Related

- `/analyze-gap` - Create gap reports
- `/walkthrough` - Discover gaps interactively
- `/iterate` - Update artifacts after resolution
- `/diagram --with-reality` - Visualize gaps in diagrams
