---
name: score-backlog
description: Score and rank backlog items using RICE, ICE, or custom weighted scoring when the user asks to prioritize a backlog, rank features, or score items for prioritization
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Write
argument-hint: "[path to backlog file, issue list, or inline items]"
read-only: false
destructive: false
idempotent: false
open-world: false
user-invocable: true
tags: backlog, prioritization, planning
---

# Score Backlog

## Overview

Read backlog items from a file, issue tracker export, or user input, then score and rank them using a structured prioritization framework (RICE by default, ICE or custom weights on request). Every score includes transparent rationale per dimension so the team can audit, debate, and adjust priorities with shared context instead of gut feelings. Items with low confidence are flagged for further research rather than ranked with false precision.

## Workflow

1. **Read product context** — Load `.chalk/docs/product/0_product_profile.md`, existing research syntheses, JTBD canvases, and OSTs. These inform scoring — an item connected to a validated customer need gets higher confidence than one based on a hunch. If no product context exists, note this and proceed, but flag that scores will be lower confidence without research backing.

2. **Load backlog items** — Parse `$ARGUMENTS` to identify the source of backlog items:
   - A file path (e.g., `.chalk/docs/product/backlog.md`, a CSV, or a list in markdown)
   - Inline items provided by the user in their message
   - A glob pattern or folder to scan

   For each item, extract: title, description (if available), and any existing metadata (priority, labels, estimates). If items lack descriptions, work with titles only but note that scores will be less reliable.

3. **Choose the scoring framework** — Default to RICE unless the user requests otherwise:
   - **RICE** (default): Reach, Impact, Confidence, Effort
   - **ICE**: Impact, Confidence, Ease
   - **Custom**: user-defined dimensions with custom weights

   If the user asks for custom scoring, ask for: dimension names, scale for each dimension, and weight for each dimension.

4. **Score each item** — For each backlog item, evaluate every dimension:

   **RICE Scoring**:
   - **Reach**: How many users/accounts will this affect per quarter? Use concrete numbers based on product data or estimates. Scale: actual user count or estimate.
   - **Impact**: How much will this move the needle for each user who encounters it? Scale: 3x (massive), 2x (high), 1x (medium), 0.5x (low), 0.25x (minimal).
   - **Confidence**: How sure are you about the Reach and Impact estimates? Scale: 100% (validated data), 80% (strong evidence), 50% (educated guess), 20% (speculation). This is the most important dimension to be honest about.
   - **Effort**: How many person-months of work? Include design, engineering, QA, and rollout. Scale: person-months (can be fractional, e.g., 0.5).
   - **RICE Score** = (Reach x Impact x Confidence) / Effort

   **ICE Scoring**:
   - **Impact**: How much will this improve the target metric? Scale: 1-10.
   - **Confidence**: How sure are you about the impact? Scale: 1-10.
   - **Ease**: How easy is this to implement? Scale: 1-10 (10 = trivial).
   - **ICE Score** = Impact x Confidence x Ease

5. **Write rationale** — For every score on every dimension, write a 1-2 sentence rationale explaining why you chose that value. This is mandatory — scores without rationale are meaningless numbers. Reference product context, research, or user input where possible.

6. **Flag low-confidence items** — Any item with Confidence below 50% (RICE) or below 5 (ICE) gets a "NEEDS RESEARCH" flag. These items should not be prioritized based on their score alone. Include a recommendation for what research would increase confidence.

7. **Rank and sort** — Sort items by score descending. Group into tiers:
   - **Tier 1 (Do First)**: top quartile by score AND confidence >= 50%
   - **Tier 2 (Do Next)**: second quartile or high score but moderate confidence
   - **Tier 3 (Investigate)**: low confidence items regardless of score
   - **Tier 4 (Deprioritize)**: bottom quartile by score with high confidence — these are genuinely low priority

8. **Generate scoring anti-patterns section** — Include a section in the output documenting common scoring pitfalls specific to this backlog, so the team can self-audit.

9. **Determine the next file number** — Read filenames in `.chalk/docs/product/` to find the highest numbered file. The next number is `highest + 1`.

10. **Write the file** — Save to `.chalk/docs/product/<n>_backlog_scores.md`.

11. **Confirm** — Tell the user the scoring was completed, share the file path, report the number of items scored, the framework used, highlight the top 3 items, and call out any items flagged as needing research.

## Scoring Output Structure

```markdown
# Backlog Scores

Last updated: <YYYY-MM-DD> (Initial draft)

## Scoring Framework

**Method**: RICE / ICE / Custom
**Items scored**: <N>
**Items flagged for research**: <N>

### Dimension Definitions

| Dimension | Scale (Units/Range) | Description |
|-----------|---------------------|-------------|
| Reach | users/quarter | Number of users who will encounter this per quarter |
| Impact | 0.25x - 3x | Degree of change for each affected user |
| Confidence | 20% - 100% | Certainty about Reach and Impact estimates |
| Effort | person-months | Total work including design, eng, QA, rollout |

## Ranked Results

| Rank | Item | Reach | Impact | Confidence | Effort | Score | Tier |
|------|------|-------|--------|------------|--------|-------|------|
| 1 | ... | ... | ... | ... | ... | ... | Tier 1 |
| 2 | ... | ... | ... | ... | ... | ... | Tier 1 |
| ... | ... | ... | ... | ... | ... | ... | ... |

## Detailed Rationale

### 1. <Item Name> — Score: <N> | Tier: <N>

| Dimension | Value | Rationale |
|-----------|-------|-----------|
| Reach | ... | ... |
| Impact | ... | ... |
| Confidence | ... | ... |
| Effort | ... | ... |

### 2. <Item Name> — Score: <N> | Tier: <N>

...

## Items Needing Research

| Item | Current Confidence | What Would Increase Confidence | Suggested Research |
|------|--------------------|-------------------------------|-------------------|
| ... | ... | ... | ... |

## Scoring Anti-patterns (Self-Audit Checklist)

Review these common pitfalls before finalizing priorities:

- [ ] **Confidence inflation**: Did you rate confidence above 50% for items without supporting data? If your only evidence is "it feels right", the confidence is 20%.
- [ ] **Effort underestimation**: Did you account for design, QA, edge cases, rollout, and documentation — not just the happy-path engineering time?
- [ ] **Equal reach fallacy**: Did you treat "all users" as reach for every item? Most features only affect a segment. Be specific about which users and how many.
- [ ] **Missing rationale**: Can someone who was not in the room understand WHY each score was assigned? If not, add more context.
- [ ] **Score gaming**: Did you adjust inputs to get a desired ranking? Scoring should inform decisions, not justify them.
- [ ] **Ignoring strategic context**: Is a strategically important item ranked low because it has low immediate reach? Consider whether the scoring framework is capturing what matters.
```

## Output

- **File**: `.chalk/docs/product/<n>_backlog_scores.md`
- **Format**: Plain markdown, no YAML frontmatter
- **First line**: `# Backlog Scores`
- **Second line**: `Last updated: <YYYY-MM-DD> (Initial draft)`

## Anti-patterns

- **Gaming confidence scores** — The most common abuse of scoring frameworks. Teams inflate confidence to push their preferred items higher. Confidence must reflect actual evidence: 100% means you have data, 80% means strong qualitative evidence, 50% means educated guess, 20% means speculation. If you catch yourself assigning 80% confidence to an item with no research backing, stop and correct it.
- **Ignoring effort** — RICE without honest effort estimates is just a popularity contest. A high-reach, high-impact item that takes 6 person-months may rank below a moderate item that takes 1 week. Include design, QA, edge-case handling, rollout, and documentation in effort estimates — not just the happy-path engineering time.
- **Treating all reach as equal** — "All users" is rarely the correct reach. A notification feature might reach all users but a power-user workflow might reach 5%. Be specific: which users, how often, in what context. If you cannot estimate reach concretely, your confidence should be low.
- **Not documenting rationale** — A score without rationale is a random number. If someone asks "why did this get 2x impact?" and the answer is "it felt right," the scoring exercise was theater. Every dimension gets a written justification.
- **Scoring without understanding the items** — Scoring items you do not understand produces garbage rankings. If a backlog item has no description and the title is ambiguous, ask for clarification or flag it as unscorable rather than guessing.
- **Using scores as absolute truth** — Scores are a conversation tool, not a mandate. A team that blindly follows the ranked list without discussion is abdicating judgment. The output should inform prioritization discussions, not replace them.
- **Scoring one-time vs. recurring items on the same scale** — A one-time infrastructure investment and a user-facing feature have fundamentally different value profiles. Note this in the rationale when it applies and consider whether the scoring framework adequately captures the difference.
- **Forgetting strategic alignment** — A perfectly scored backlog that ignores company strategy is optimizing for the wrong thing. If the company is betting on enterprise, a consumer feature with high RICE may still be the wrong priority. Call out strategic misalignment explicitly when you see it.
