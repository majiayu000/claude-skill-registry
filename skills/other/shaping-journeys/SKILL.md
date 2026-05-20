---
name: shaping-journeys
description: List user canvases and shape common patterns into journey definitions. Use when consolidating user research into testable user flows.
user-invocable: true
allowed-tools: Read, Write, Glob, Grep, Edit
---

# Shaping Journeys

Manage user canvases and shape common patterns into journey definitions for flow diagramming and testing.

---

## Triggers

```
/shape              # List all canvases with status
/shape --run        # Shape canvases into journeys
/shape --journey {id}  # Show journey details
```

---

## Step 0: Collect All Signal Sources (Pre-Workflow)

Before any mode executes, gather enriched signal data from all canvases.

For each canvas in `grimoires/observer/canvas/*.md`:

1. **Read existing sections**:
   - `## Journey Fragments` (existing behavioral context)
   - `## Feedback Entries (from UI)` (sentiment data from `/synthesize-feedback`)
   - `## Score Context` (user position for weighting)

2. **Merge into unified signal list**:
   - Journey fragments provide behavioral context (goals, actions, expectations)
   - Feedback entries provide sentiment data (FEEL, WEIGHTINGS, ACCURACY, UX)
   - Score context provides user weight for pattern prioritization

3. **Weight patterns by Score Context**:

   | Signal Weight | Multiplier | Source |
   |---------------|------------|--------|
   | HIGH (top 1%, godfather/all_night tier) | 3x | Patterns from these users are prioritized in detection |
   | MEDIUM (top 25%, devoted/regular tier) | 1x | Standard weight |
   | LOW (below 25th percentile) | 0.5x | De-prioritized but not ignored |

   Apply weight multiplier when counting pattern occurrences in Step 3 (Pattern Detection).
   A HIGH-weight user's feedback entry counts as 3 occurrences toward confidence thresholds.

---

## List Mode (Default)

When invoked without arguments, display canvas summary.

### Step 1: Read All Canvases

```bash
grimoires/observer/canvas/*.md
```

### Step 2: Parse Canvas Frontmatter

Extract from each canvas:
- User
- Status
- Quotes count
- Goals count
- Linked journeys

### Step 3: Display Summary Table

```
┌─────────────────────────────────────────────────────────────────┐
│ LABORATORY CANVASES                                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User            Status    Quotes  Goals   Journeys             │
│  ─────────────   ───────   ──────  ─────   ─────────            │
│  papa-flavio     active    3       2       deposit-flow         │
│  tchallason      active    5       3       rewards-display      │
│  testuser        active    1       1       -                    │
│                                                                 │
│  Total: 3 canvases, 9 quotes, 6 goals                          │
│                                                                 │
│  Pending Synthesis: 1 canvas (testuser)                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Next Steps:
  - Add more feedback: /observe @{user} "quote"
  - Shape journeys: /shape --run
  - View journey: /shape --journey {journey-id}
```

---

## Run Mode (`--run`)

Extract patterns from canvases to create journey definitions.

### Step 1: Load All Canvases

Read all `grimoires/observer/canvas/*.md` files.
Parse YAML frontmatter and markdown sections.

### Step 2: Extract Level 3 Goals

From each canvas, extract:
- Goal text
- Validation status
- Supporting quotes
- User type

### Step 2.5: Load Domain Glossary

Before pattern detection, load domain vocabulary to prevent misinterpretation during synthesis:

1. Read `grimoires/observer/glossary.yaml`
2. During pattern detection and goal extraction, check if any glossary term appears in user quotes (case-insensitive match on the `term` field)
3. If a match is found:
   - Use the `meaning` field as the canonical interpretation
   - Note the `not` field to explicitly avoid the common misinterpretation
   - Annotate journey steps with `[glossary: {term}]` where relevant
4. If glossary file does not exist, proceed without — log a warning to the operator

---

### Step 3: Pattern Detection

Identify common patterns across canvases:

**Grouping Rules:**
- Similar Level 3 goals → Journey candidates
- Overlapping journey fragments → Shared steps
- Common expectation gaps → Error states

**Confidence Thresholds:**
| Canvases | Confidence | Action |
|----------|------------|--------|
| 1 | LOW | Flag for manual review |
| 2 | MEDIUM | Create draft journey |
| 3+ | HIGH | Create journey, auto-validate |

### Step 4: Generate Journey Files

For MEDIUM/HIGH confidence patterns, create journey files:

**Journey Template:**
```markdown
---
type: journey
id: {journey-id}
title: {Human Readable Title}
source_canvases: [{usernames}]
created: {timestamp}
updated: {timestamp}
status: draft
confidence: medium | high
---

# {Journey Title}

## Summary

{1-2 sentence description synthesized from goals}

---

## User Types

- **Primary**: {most common type from source canvases}
- **Secondary**: [{other types}]

---

## Steps

### Step 1: {Step Name}

- **Trigger**: {what initiates this step}
- **Action**: {what user does}
- **Expected**: {what should happen}
- **Selector**: {suggested data-testid or selector}
- **Potential Errors**:
  - {error state from canvas gaps}

### Step 2: {Step Name}

...

---

## Success Condition

{What constitutes successful completion of this journey}

---

## Known Gaps

| Gap | Type | Source Canvas | Resolution |
|-----|------|---------------|------------|
| {gap} | {Bug/Feature/Discoverability} | {canvas} | {status} |

---

## Source Quotes

> "{quote}" — @{user}

```

### Step 5: Update Source Canvases

Add journey link to each source canvas frontmatter:
```yaml
linked_journeys:
  - {journey-id}
```

### Step 5.5: Re-Wire Obsidian Links

After creating or updating journey files and updating source canvas frontmatter, re-wire all affected canvases to reflect the new journey membership:

```bash
# Re-wire all canvases and journeys to reflect updated source_canvases
bash scripts/observer/wire-obsidian-links.sh --canvases-journeys

# Verify consistency
bash scripts/observer/wire-obsidian-links.sh --canvases-journeys --verify
```

This ensures newly created journeys and their source canvases have bidirectional wiki-links. The `--canvases-journeys` mode is idempotent — safe to re-run.

### Step 6: Update Laboratory State

Update `grimoires/observer/state.yaml`:
```yaml
active:
  phase: synthesis

journeys:
  {journey-id}:
    status: draft
    created: {timestamp}
    source_canvases: [{users}]

queue:
  pending_synthesis: []  # Clear processed
```

### Step 7: Report Output

```
✓ Synthesis complete

Journeys Created:
  - deposit-flow (HIGH confidence)
    Sources: papa-flavio, tchallason
    Steps: 4
    Gaps: 2

  - rewards-display (MEDIUM confidence)
    Sources: tchallason
    Steps: 3
    Gaps: 1

Low Confidence (Manual Review):
  - testuser canvas: 1 goal, no pattern match

Next Steps:
  - View journey: /shape --journey deposit-flow
  - Generate diagram: /diagram deposit-flow
  - Add more feedback: /observe @testuser "..."
```

---

## Journey Details Mode (`--journey {id}`)

Display full journey details:

```
/shape --journey deposit-flow
```

Output:
```
┌─────────────────────────────────────────────────────────────────┐
│ JOURNEY: deposit-flow                                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Status: draft                                                  │
│  Confidence: HIGH                                               │
│  Sources: papa-flavio, tchallason                              │
│                                                                 │
│  Steps:                                                         │
│  1. Open deposit modal (trigger: click deposit button)          │
│  2. Enter amount (action: input token amount)                   │
│  3. Approve token (action: wallet approval)                     │
│  4. Confirm deposit (action: execute deposit)                   │
│                                                                 │
│  Known Gaps: 2                                                  │
│  - Approval stuck on some wallets (Bug)                         │
│  - No loading indicator during tx (Feature)                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Actions:
  - Generate diagram: /diagram deposit-flow
  - Generate test: /validate deposit-flow
  - Edit journey: Read grimoires/observer/journeys/deposit-flow.md
```

---

## Journey ID Generation

Journey IDs are generated from goal patterns:
- Lowercase, hyphenated
- Max 30 characters
- Unique within laboratory

**Examples:**
- "deposit tokens and stake" → `deposit-stake-flow`
- "view accumulated rewards" → `rewards-display`
- "plan burn timing" → `burn-planning`

---

## Pattern Matching Algorithm

### Goal Similarity

Compare goals using semantic patterns:

1. **Action verbs**: deposit, withdraw, claim, stake, view
2. **Object nouns**: tokens, rewards, balance, position
3. **Intent markers**: planning, checking, tracking

**Match Criteria:**
- Same action verb OR
- Same object noun AND similar intent OR
- Explicit user-stated connection

### Fragment Merging

When multiple canvases have journey fragments:
1. Align by trigger similarity
2. Merge actions into steps
3. Combine expected outcomes
4. Aggregate error states

---

## Validation

Before creating journey:
- [ ] At least 2 canvases match (or explicit manual trigger)
- [ ] Steps have clear triggers
- [ ] Success condition defined
- [ ] YAML frontmatter valid

---

## Error Handling

| Error | Resolution |
|-------|------------|
| No canvases found | Prompt to create with /observe |
| No patterns detected | List canvases, suggest manual journey |
| Journey ID collision | Append numeric suffix |
| Canvas parse error | Report, skip canvas |

---

## Integration Points

- **observing-users**: Canvases as input
- **diagramming-states**: Journeys as input for diagram generation
- **Laboratory state**: Updates journey registry

---

## Related

- `/observe` - Create canvases from quotes
- `/diagram` - Generate diagrams from journeys
- `/validate` - Generate tests from diagrams
