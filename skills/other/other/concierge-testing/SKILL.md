---
name: concierge-testing
description: Validate gap hypotheses by manually simulating features for individual users and measuring commitment, not satisfaction.
user-invocable: true
allowed-tools: Read, Write, Glob, Grep, Edit, Bash
---

# Concierge Testing

Validate a gap hypothesis before any code is written. Manually simulate the proposed feature for ONE user whose canvas shows the strongest evidence, then measure commitment — not satisfaction, not compliments, commitment.

This skill sits between `/analyze-gap` and `/file-gap` in the pipeline. It is the validation step that separates Level 4 (Obstacle) from Level 5 (Validated Obstacle).

---

## Core Principle

**Commitment is the only metric that matters.** "That's cool" is a kill signal. "How do I keep this?" is a build signal. The difference between a feature worth building and a feature that wastes Zerker's time is whether users change their behavior when given the thing.

---

## Triggers

```
/concierge-test {hypothesis-id}
/concierge-test {hypothesis-id} --canvas {username}
/experiment {hypothesis-id}
/experiment {hypothesis-id} --canvas {username}
```

**Examples:**
```bash
/concierge-test H3                              # Test hypothesis H3, auto-select best user
/concierge-test H3 --canvas xabbu              # Test H3 specifically with xabbu
/experiment H5 --canvas el-capitan             # Alias: test H5 with el-capitan
```

**Arguments:**
- `{hypothesis-id}`: Hypothesis ID from canvas Level 3 Hypotheses (required)
- `--canvas {username}`: Override user selection (optional — auto-selects strongest evidence)

---

## When to Use

- A gap hypothesis has reached Pattern level (3+ canvases with supporting evidence)
- Before filing a GitHub issue that would trigger implementation
- When the team is debating whether to build a feature
- When a workaround has been detected but commitment to a solution is unknown

## When NOT to Use

- Hypothesis has < 3 canvas sources (not yet Pattern level — gather more evidence)
- The gap is a confirmed bug (bugs get fixed, not tested)
- The user is unresponsive or churning (can't measure commitment from silence)
- The feature already exists but is undiscoverable (that's a UX fix, not a validation question)

---

## Workflow

### Step 1: Select Hypothesis

1. Read canvas(es) containing the target hypothesis
2. Verify hypothesis has reached Pattern level (3+ independent sources)
3. Extract:
   - Hypothesis text and confidence level
   - Supporting quotes with provenance hashes
   - Workaround evidence (if any)
   - Journey context (which step this maps to)

If hypothesis has fewer than 3 sources, WARN:
```
Hypothesis {id} has only {N} source(s). Concierge tests are most
reliable at Pattern level (3+ sources). Proceed anyway? Results
will carry lower confidence.
```

### Step 2: Select User

If `--canvas` provided, use that user. Otherwise, select the best candidate:

**Selection Criteria (in priority order):**

1. **Strongest evidence** — most quotes supporting this hypothesis
2. **Active lifecycle** — `power_user` or `reactivating` preferred over `churning`
3. **Reachable** — has existing DM channel or known contact method
4. **Signal weight diversity** — prefer users whose tier is underrepresented in existing evidence

Load selected canvas:
```bash
grimoires/observer/canvas/{username}-canvas.md
```

Extract:
- User profile and score context
- Relevant quotes for this hypothesis
- Conversation frameworks (how to approach this user)
- Prior follow-ups (avoid repeating questions)

### Step 3: Design Simulation

Create a manual simulation of the proposed feature. The simulation must be:

- **Concrete**: Not "imagine if you could..." but actually doing the thing
- **Minimal**: Smallest possible version that tests the hypothesis
- **Reversible**: Can be undone without lasting effects

**Simulation Types:**

| Hypothesis Type | Simulation Approach |
|-----------------|---------------------|
| Recognition / status | Manually assign a title or badge via DM: "We noticed you did X; we've flagged your wallet as [title]." |
| Information gap | Send them the data they were missing: "Here's what your profile looks like behind the scenes: [data]" |
| Workflow friction | Walk them through the manual workaround: "Try doing X → Y → Z. Does that get you what you need?" |
| Social / comparison | Share relevant context: "You're one of {N} wallets that [behavior]. Here's how that compares: [data]" |

**Draft the DM message.** Use the user's own words as anchors:

```
hey {username} — you mentioned "{exact quote from canvas}". we
[describe simulation]. does that help with what you're doing?
```

### Step 3.5: Provenance Gate

Before sending, record the simulation in provenance:

```bash
echo -n "{simulation_message}" | scripts/provenance/gate.sh \
  --source-type concierge_test \
  --confidence exact \
  --canvas-target "{username}" \
  --raw-source-ref "concierge-{hypothesis_id}-{username}-{date}" \
  --ingested-by concierge-test
```

### Step 4: Execute

**This step requires human action.** The agent prepares the message; the operator sends it.

Output the prepared message:

```
--- CONCIERGE TEST: {hypothesis_id} ---

Target: @{username}
Hypothesis: {hypothesis text}
Simulation: {what we're manually doing}

Message to send:
─────────────────────────────────────
{prepared DM message}
─────────────────────────────────────

After sending, run:
  /concierge-test {hypothesis_id} --record {commitment_level}

Commitment levels:
  strong  — asked how to keep it, changed behavior
  social  — bragged to others, shared it
  kill    — "that's cool, thanks" (polite dismissal)
  silence — no response after 72 hours
```

### Step 5: Measure Commitment

When the operator reports back with `--record {level}`:

| Response | Classification | Signal | Action |
|----------|---------------|--------|--------|
| Asked how to keep it | **Strong** | Build signal | Create Problem-Constraint Doc → Zerker handoff |
| Changed behavior after receiving it | **Strong** | Build signal | Create Problem-Constraint Doc → Zerker handoff |
| Bragged to others / shared it | **Social** | Build with sharing | Create Problem-Constraint Doc with social context → Zerker handoff |
| "That's cool, thanks" | **Kill** | Don't build | Close hypothesis. Note in canvas. Save as Atomic Learning. |
| Asked clarifying questions, then engaged | **Strong** | Build signal | Create Problem-Constraint Doc → Zerker handoff |
| Polite but no follow-up action | **Kill** | Don't build | Close hypothesis. Note in canvas. |
| No response after 72 hours | **Silence** | Need isn't strong enough | Close hypothesis unless user is known to be inactive. |

### Step 6: Record Result

Update the user's canvas with concierge test result:

```markdown
## Concierge Tests

### Test: {hypothesis_id} — {date}

| Field | Value |
|-------|-------|
| **Hypothesis** | {hypothesis text} |
| **Simulation** | {what we manually did} |
| **Commitment Level** | {strong / social / kill / silence} |
| **User Response** | "{exact response quote}" |
| **Provenance** | `[prov:{hash}]` |

**Interpretation**: {what this tells us about the hypothesis}
```

Update hypothesis confidence:
- **Strong/Social** → confidence: High, validated: true
- **Kill** → confidence: Low, status: falsified
- **Silence** → confidence: unchanged, status: inconclusive

### Step 7: Route Result

**If Strong or Social signal:**

1. Generate Problem-Constraint Doc from template:
   ```bash
   grimoires/observer/templates/problem-constraint-doc.md
   ```
2. Populate with:
   - 3 evidence quotes from canvases (with provenance hashes)
   - Workaround evidence
   - Concierge test result and commitment level
   - Build spec (WHAT to build, not HOW)
3. Write to:
   ```bash
   grimoires/observer/problem-constraints/{hypothesis_id}-{date}.md
   ```
4. Report: ready for Zerker handoff via `/file-gap`

**If Kill or Silence signal:**

1. Update canvas hypothesis status to `falsified` or `inconclusive`
2. Record as Atomic Learning in `grimoires/observer/learnings/`:
   ```markdown
   ## Learning: {hypothesis_id} — {date}

   **Hypothesis**: {text}
   **Test**: {simulation description}
   **Result**: {kill/silence}
   **Lesson**: {what we learned — why the need wasn't strong enough}
   **Reuse**: {when this learning applies to future hypotheses}
   ```
3. Close the gap. Do NOT file a GitHub issue.

---

## Output

```
Concierge Test Complete

Hypothesis: {id} — {text}
Target User: @{username}
Simulation: {description}
Commitment: {strong / social / kill / silence}

Result:
  {If strong/social:}
  ✓ Problem-Constraint Doc created: grimoires/observer/problem-constraints/{id}-{date}.md
  ✓ Ready for Zerker handoff: /file-gap {id}

  {If kill/silence:}
  ✗ Hypothesis {falsified/inconclusive}
  ✓ Learning recorded: grimoires/observer/learnings/{id}-{date}.md
  ✗ No issue filed — need not validated

Next Steps:
  {If validated:} /file-gap {id} — file as GitHub issue for implementation
  {If falsified:} Review canvas for alternative hypotheses
  {If inconclusive:} Consider re-testing with different user or different simulation
```

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Hypothesis ID not found | List available hypotheses from canvases |
| No canvas with hypothesis | Suggest running `/observe` or `/analyze-gap` first |
| Canvas has no wallet / score context | Proceed without score weighting, note limitation |
| User unreachable | Suggest alternative user or defer test |
| Provenance gate error | Log error, proceed with test (degrade gracefully) |
| Operator doesn't report back | After 7 days, auto-classify as `silence` |

---

## Integration Points

- **analyzing-gaps**: Provides hypotheses to test (upstream)
- **filing-gaps**: Receives validated obstacles for issue creation (downstream)
- **observing-users**: Canvas data as input
- **generating-followups**: Prior follow-ups inform simulation design
- **Problem-Constraint Doc**: Output format for validated obstacles
- **Provenance system**: All test messages tracked with content hashes

---

## Validation

After concierge test:
- [ ] Hypothesis existed at Pattern level (3+ sources) or warning issued
- [ ] User selected with documented rationale
- [ ] Simulation message anchored on exact user quote
- [ ] Provenance gate recorded the simulation
- [ ] Commitment level classified correctly (not mistaking politeness for signal)
- [ ] Canvas updated with test result
- [ ] If validated: Problem-Constraint Doc complete with 3 quotes + provenance
- [ ] If falsified: Learning recorded, hypothesis status updated, NO issue filed
- [ ] No future-tense language in simulation message
- [ ] No feature announcements in simulation message

---

## Related

- `/analyze-gap` — Upstream: identifies gaps to test
- `/file-gap` — Downstream: files validated obstacles as issues
- `/observe` — Signal capture that populates canvases
- `/follow-up` — Prior messages inform simulation design
- `grimoires/observer/ARCHETYPE.md` — The Listener archetype governing this skill
- `grimoires/observer/templates/problem-constraint-doc.md` — Output template
