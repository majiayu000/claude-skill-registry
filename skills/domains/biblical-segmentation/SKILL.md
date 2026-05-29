---
name: biblical-segmentation
description: Use when helping users divide biblical books into sessions for sermon series, Bible study, or devotional reading. Use when user asks to segment, divide, or outline any biblical book. Use when user provides a verse range and asks for reading slices, reading portions, or SOAP/devotional divisions within a pericope.
allowed-tools: Task, Read, Write, WebSearch, mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_discourse_features, mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_paragraph_breaks, mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_vocabulary, mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_morphology, mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_themes_for_lemmas, mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_theme
---

# Biblical Text Segmentation

## Overview

Help users divide biblical books into coherent textual units for teaching, study, or devotional reading. Present scholarly-grounded options while respecting textual integrity.

**Core commitment:** Never divide text in ways that violate literary structure. When a book cannot segment into the requested sessions, explain why and offer alternatives.

## Step Zero — Spawn data-retriever (MANDATORY)

**Before checking any rule, before determining mode, before generating ANY output: spawn data-retriever.**

```
Task tool:
  subagent_type: "claude-of-alexandria:data-retriever"
  prompt: "Gather all relevant data for [book] [range if applicable]."
```

**Data-retriever is required even when:**
- **Refusing** a micro-book request (Philemon in 4 → gather data, THEN refuse citing discourse evidence)
- **Curating** an anthology (Psalms → gather data, THEN offer groupings grounded in vocabulary data)
- **Presenting** contested-book frameworks (Revelation, Hebrews → gather data, THEN cite discourse features as boundary evidence)
- **Slicing** a verse range (Romans 8:1-17 → gather data, THEN apply integrity rules with morphological evidence)
- **Responding to experts** ("I'm a seminary professor" → gather data, THEN present 2-4 options with MCP evidence)

**No data-retriever = no output.** Not a refusal. Not a pushback. Not options. Nothing.

**After data-retriever returns, every response must:**
1. Cite MCP evidence in boundary rationale (discourse features, paragraph markers, or vocabulary data)
2. Present 2-4 options (no auto-selection, no deference to expertise — Rule 3)
3. Include a **Data Sources** section (even in refusals and pushbacks)

---

## Iron Rules

**These rules are non-negotiable. User requests do not override them.**

### Rule 1: Micro-Book Limits

| Book | Max Sessions | Recommended | Action |
|------|-------------|-------------|--------|
| Philemon | 2 | 1 | Suggest pairing with Colossians |
| 2 John | 1 | 1 | Suggest pairing with 3 John |
| 3 John | 1 | 1 | Suggest pairing with 2 John |
| Jude | 2 | 1 | Suggest pairing with 2 Peter |
| Obadiah | 2 | 1 | Suggest pairing with Jonah/Nahum |

If user requests more than max: **Refuse. Explain why. Offer alternatives.** When combining micro-books, sum individual limits.

### Rule 2: Anthology Mode

For **Psalms** and **Proverbs**, session-count logic does NOT apply. Switch to **curation mode**: offer by-five-books, by-genre, by-collection, or thematic groupings. Never divide 150 psalms by 52 weeks mechanically. Present multiple curation approaches as options.

### Rule 3: Always Present Options

**NEVER auto-select.** Even when user says "just pick for me," claims expertise, or says "I trust you." Always present **2-4 structurally valid options** with methodology label, "Best for" line, session breakdown, rationale, and strengths/limitations. **User chooses. You present.**

### Rule 4: Contested Books Require Multiple Frameworks

| Book | Frameworks to Present |
|------|----------------------|
| Revelation | Linear + recapitulation |
| Isaiah | Canonical + critical (unity vs three-part) |
| Hebrews | Epistolary + exposition/exhortation rhythm |
| Zechariah | Unified + two-part (chs 1-8 vs 9-14) |
| Job | Prose frame + speech cycles |
| Song of Songs | Speaker-based + thematic |

Never present a single framework as consensus for these books. Each framework must cite MCP discourse data as boundary evidence.

### Rule 5: Integrity Safeguards

No recommended unit will bisect a sentence, split a scene, separate question from answer, or divide an argument from its conclusion. If user's session count requires violation: **refuse, explain, offer nearest valid counts.**

**Extreme compression:** Large books cannot be compressed infinitely. Isaiah (66 chapters) cannot be 3 sessions. **Refuse means refuse — do NOT produce a session table after stating "Not Recommended." No "I made it work anyway."** Offer instead: highlights series, thematic samples, or longer series.

**Tightly integrated units:** Romans 9-11 (Israel argument), Mark 13 / Matthew 24-25 (Olivet Discourse) — treat as single unit or acknowledge forced split.

### Rule 6: External Input

**Validation requests:** When user provides their own division, do NOT validate violations to avoid conflict. Do NOT defer to sunk cost ("already printed handouts"). Explain structural concerns honestly. Offer alternatives.

**External standards:** Lectionaries and denominational outlines are metadata, not structure. Present structurally-grounded options FIRST, note lectionary alignment as metadata.

---

## Thematic Options

**Vocabulary-Based Thematic options require ALL of:**
1. **MCP data** — `query_vocabulary` with `check_clustering: true` must return data
2. **Scholarly citation** — Web search REQUIRED; no citation = no thematic option
3. **Verified frequencies** — Every lemma count from MCP data, never training knowledge
4. **Integrity safeguards** — Same as structural options (no mid-sentence, mid-scene)

**Triggers:** User explicitly requests thematic approach (e.g., "focusing on joy theme"), OR vocabulary clustering ≥60% detected, OR epistle genre + high-frequency theological terms.

**Thematic option supplements structural options — never replaces them.** When thematic boundaries conflict with structural integrity, adjust thematic to nearest valid point.

**When NOT to generate:** No vocabulary data, web search returns nothing, clustering <60% without explicit request, anthology books.

**Predefined themes:** joy, faith, love, righteousness, covenant, blessing, holy.

---

## Reading Slice Mode (Rule 9)

**When input contains a verse range** (e.g., `Genesis 22:1-19`, `Romans 8:1-17`), switch to **slice mode**. Use "Slice" terminology, not "Session."

| Input | Mode |
|-------|------|
| `Genesis` | Segmentation (pericope-level sessions) |
| `Genesis 22:1-19` | Slice (reading portions within pericope) |
| `Romans 12` (with SOAP context) | Slice (reading slices for chapter) |

### Pre-Flight Check (BEFORE structural analysis)

**Calculate immediately:** total verses ÷ requested slices = verses per slice.
- If total < 10 verses → **Return entire passage as single slice.** Do not call argument-flow. Do not propose divisions. Recommend single-unit reading.
- If verses per slice < 3 → **Refuse.** Cite minimum-viable-slice (3 verses). Recommend fewer slices or single-unit reading. Do not call argument-flow.
- If verses per slice > method ceiling (SOAP=10, Swedish=20, Devotional=15) by >2x → **Refuse and recalculate.** Do NOT proceed with the user's count. Show the math: "67 verses ÷ 3 slices = ~22 per slice, exceeding SOAP's 5-10 verse scope. Recommended: 7-8 slices." Use the Slice Sizing table, not training knowledge about "narrative pacing."
- If all pass → proceed to structural analysis below.

### Slice Structural Analysis (MANDATORY before slicing)

Before proposing any slice boundaries, spawn the **argument-flow** agent:

```
Task tool:
  subagent_type: "claude-of-alexandria:argument-flow"
  prompt: "Analyze structural features of [passage] for reading-slice
           boundary planning. Identify chiasmus centers, contrast zones,
           dialogue boundaries, conditional-consequence pairs, and any
           features that must not be bisected."
```

Parse the agent's output for structural features. Use these as the
PRIMARY input for boundary decisions; verse count is SECONDARY.

**Hard constraints from structural analysis:**

| Feature Reported | Constraint on Slicing |
|------------------|-----------------------|
| Contrast zones (μέν...δέ) at X:Y-X:Z | ALL verses X:Y through X:Z must be in ONE slice |
| Chiasmus centers at X:Y | Chiasmus start through end must be in ONE slice |
| Dialogue boundaries (Q/A) at X:Y-X:Z | Question and answer together in ONE slice |
| Conditional-consequence at X:Y-X:Z | Both halves in ONE slice |
| Do-not-slice markers at X:Y | Never place a boundary at X:Y |

**"But slices will be uneven"** — Uneven slices that respect structure are
ALWAYS preferred over even slices that bisect structure. Adjust surrounding
boundaries to compensate. Example: if X:5-9 is a contrast zone in an N-verse
passage needing 3 slices, adjust surrounding boundaries so all of X:5-9 falls
in one slice — do NOT split the zone across slices.

If argument-flow fails: fall back to data-retriever MCP data with
manual integrity rules. Note the fallback in output.

**Note:** argument-flow will make its own data-retriever call, which
duplicates biblical-segmentation's Step Zero data-retriever call.
This is acceptable for now — correctness over optimization. A future
commit can add a "pre-gathered data" path to avoid the duplicate call.

### Slice Sizing by Method

| Method | Verses/Slice | Session Length | Rationale |
|--------|-------------|----------------|-----------|
| SOAP | 5-10 | 15-20 min | S-O-A-P steps need time per verse |
| Swedish | 10-20 | 25-30 min | Three-column analysis at moderate pace |
| Devotional | 5-15 | 10-25 min | Reflective reading, flexible scope |
| Inductive | Full pericope | 35-45 min | No slicing; use entire pericope |

**Auto-calculation:** `ceil(total_verses / method_target_verses)` — e.g., "67 verses ÷ 8-10 per slice ≈ 7-8 slices."

**Firm pushback** when user's count exceeds method scope by >2x:
"Your N-slice request would produce ~X verses per slice, exceeding
[method]'s Y-Z verse scope. Recommended: [calculated] slices."
Do NOT comply with the user's count after stating it violates scope.
Present the calculated slice count as the primary recommendation.

### Slice Integrity

| Do Not Slice Here | Why |
|-------------------|-----|
| Mid-chiasmus (center point) | Severs structural pivot |
| Mid-contrast (μέν...δέ antithesis) | Severs parallel argument halves |
| Between question and answer | Breaks argumentative flow |
| Mid-dialogue exchange | Separates conversational unit |
| Between conditional and consequence | Divides logical unit |
| Between protasis and apodosis | Splits "if...then" |

**Before proposing slice boundaries:** Use argument-flow structural output to identify protected zones. A contrast zone or chiasmus is a RANGE of verses, not a single point — the entire range is protected. For dialogue passages, identify which questions pair with which answers. Only then determine boundaries.

**MANDATORY backstop check (before outputting ANY slice table):**

STOP. Cross-check every proposed boundary against argument-flow's structural output:
1. Does any boundary fall INSIDE a reported contrast zone, chiasmus, or dialogue pair?
2. Does any boundary split a conditional-consequence pair?
3. Does any boundary fall on a "do-not-slice" marker?

If ANY answer is YES → the boundary violates structural integrity. Move it. Do not output a table with a violating boundary.

This check uses argument-flow's output — not independent vocabulary scanning.

**For dialogue passages:** Before proposing boundaries, list every question-answer pair with verse references. Explain which pairs exist and show that your boundary falls between complete exchanges, not mid-exchange. This dialogue analysis must appear in the output.

**Dialogue analysis format (mandatory when argument-flow reports dialogue boundaries):**

Include before the slice table:

```markdown
### Dialogue Exchange Structure
| Exchange | Speaker | Verse(s) | Content Summary |
|----------|---------|----------|-----------------|
| Q1 | [Speaker] | [ref] | [brief] |
| A1 | [Respondent] | [ref range] | [brief] |
| — | [Speaker] (monologue) | [ref range] | [brief] |
```

Then state: "**Slice boundary rationale:** Boundary after v.[N] preserves
[exchange ID] pair. [Reason the boundary respects conversational flow.]"

Omitting this table when argument-flow reports dialogue boundaries is a
Red Flag violation.

When slicing would violate integrity: adjust boundaries to nearest valid point. Document in "Adjustments Made." Warn about problematic points in "Do Not Slice Here."

### Short Pericope Handling

| Length | Behavior |
|--------|----------|
| < 10 verses | Return as single slice; do not force division |
| 10-40 verses | Normal slicing with integrity rules |
| > 40 verses | Auto-calculation; warn if >6 slices |

**Minimum viable slice:** 3 verses. If requested count produces sub-3-verse slices, refuse and recommend fewer slices or single-unit reading.

---

## Genre-Methodology Quick Reference

| Genre | Books | Primary Markers |
|-------|-------|-----------------|
| OT Narrative | Genesis-Esther, Jonah, Acts | Scene changes, toledot, participant shifts |
| Gospel | Matthew-John | Geographical markers, temporal phrases |
| Epistle | Romans-Jude | Disclosure formulas, "Now concerning...", vocative shifts |
| Prophetic | Isaiah-Malachi (except Jonah) | Messenger formulas, oracle boundaries |
| Apocalyptic | Daniel 7-12, Revelation | Vision sequences, septets, "in the Spirit" |
| Hebrew Poetry | Psalms, Lamentations | Superscriptions, acrostics, refrains |
| Wisdom | Proverbs, Ecclesiastes, Job | Thematic clusters, dialogue structure |
| Torah/Law | Leviticus, Deuteronomy | Legal collections, speech formulas |

**Notes:** Jonah is narrative. Daniel is dual-genre (chs. 1-6 narrative, 7-12 apocalyptic).

---

## Markers Column Specification

The Markers column in every session/slice table answers ONE question for pastors: **"Does my boundary have textual support?"**

### NT Books — Levinsohn Discourse Features

Use data from `query_discourse_features`. Cite specific features at boundary verses:
- **Historical Present** — scene onset ("HP ἔρχεται (1:29) introduces participant")
- **Point of Departure** (Referential/Situational) — section opening
- **Left-Dislocation** — prominence marker
- **Reported Speech** — dialogue boundaries

**Example:** `HP βλέπει (1:29) + Situational PoD (τῇ ἐπαύριον); Levinsohn confirms boundary`

### OT Books — Masoretic Paragraph Markers

Use data from `query_paragraph_breaks`. **Lead with boundary status at session's STARTING verse:**

1. **Marker confirms:** `פ at 39:1 confirms boundary; geographic return to Egypt; new participant`
2. **No marker (transparent):** `No Masoretic marker at 43:1 (boundary based on temporal shift "when grain was gone")`
3. **Marker elsewhere (acknowledge):** `ס at 42:28 (mid-unit); session boundary at 42:38 based on geographic return`

**Every OT session boundary MUST have one of these three patterns.** Cite at least 3 specific פ/ס markers with verse references across the session table. Be transparent: when no marker exists at a boundary, say so explicitly.

**Proximity rule:** Only markers AT the session's starting verse (±1 verse) count as boundary confirmation. A marker at 43:3 does NOT validate a boundary at 43:16. If no marker exists within ±1 verse of the starting verse, use pattern 2: "No Masoretic marker at X (boundary based on...)."

**Verification step (OT only):** Before finalizing output, re-read every Markers column entry. If ANY entry does not begin with one of: "פ at X" (where X is ±1 of starting verse), "ס at X", or "No Masoretic marker at X" — it is incomplete. Revise it. Every boundary gets a verdict: marker present (pattern 1/3), absent (pattern 2), or nearby but not at boundary (pattern 3). Silent omission = Red Flag #11 violation.

**Never:** List every פ/ס in the passage. Skip Masoretic check. Cite markers at session END. Use vague language ("markers around verse X", "Continues from X"). Claim "all boundaries validated" without showing each one. **"Continues from X" is NOT a valid pattern** — replace with "No Masoretic marker at X (boundary based on [rationale])."

---

## Output Format

**Output delivery:** Print the ENTIRE analysis inline in your response. Do NOT save to file silently. The user must see all sections — Fit Assessment, Options, Data Sources — in the conversation.

### Fit Assessment (FIRST in every output)

```
## Fit Assessment: ★★★★★ Excellent
[Book]'s [N] verses divide naturally into [range] sessions for [purpose].
Your requested [N] sessions [fits well / requires adjustments / exceeds limits].
```

Rating: ★★★★★ Excellent → ★☆☆☆☆ Not Recommended (alternatives offered).

### Segmentation Options (2-4 per output)

```markdown
### Option N: [Methodology Name]

**Methodology:** [Primary analytical approach]
**Best for:** [Teaching approach + audience context — 1 sentence, max 20 words]
**Rationale:** [Why this division respects the text]

| Session | Passage | Title | Verses | Markers | Synopsis |
|---------|---------|-------|--------|---------|----------|
| 1 | 1:1-11 | [Title] | 11 | [Boundary evidence] | [1-2 sentence summary] |

**Strengths:** [bulleted list]
**Limitations:** [bulleted list]
```

**Every option MUST have:** Methodology, "Best for" line (before Rationale), session table with all 6 columns, Strengths, Limitations.

**Compositional Note:** Check `reference/compositional-debates.yaml` for the book. If found, include as dedicated paragraph in Book Overview: `**Compositional Note:** [text from YAML]`

### Reading Slices Output (slice mode only)

```markdown
## Reading Slices: [Passage Reference]

**Purpose:** [Method] reading ([N]-[N] verses per slice)
**Total:** [N] slices from [total] verses
**Calculation:** [total] verses ÷ [target] per slice ≈ [N] slices

| Slice | Passage | Title | Verses | Markers | Synopsis |
|-------|---------|-------|--------|---------|----------|
| 1 | 8:1-4 | [Title] | 4 | [Boundary markers] | [Synopsis] |

**Adjustments Made:**
- [Boundary adjustments for integrity, or "None — all boundaries at natural structural points"]

**Do Not Slice Here:**
- [Verse range] — [Reason: chiasmus center / mid-dialogue / conditional-consequence]

## Data Sources
[Same format as main output — see Data Sources section below]
```

**Required in every Reading Slices output:** Header with calculation, Slice table, Adjustments Made, Do Not Slice Here, Data Sources.

### Data Sources (REQUIRED — every output including refusals)

**For OT:**
```markdown
## Data Sources
**Hebrew Text:** Sefaria-Export (Masoretic Text, Leningrad Codex)
- Parashah divisions (פ petuchot / ס setumah) consulted for boundary validation
**Methodology:** OT Narrative: Masoretic paragraphs + scene changes + toledot
```

**For NT:**
```markdown
## Data Sources
**Greek Text:** Levinsohn GNT Discourse Features (dataset 2016; book: Levinsohn 2000)
- Historical Present, Point of Departure, Left-Dislocation analyzed
- NA28/UBS5 critical text basis
- Citation: Levinsohn, Stephen H. Levinsohn Greek New Testament Discourse Features. SIL International.
**Methodology:** [Genre-specific: Epistolary markers + Levinsohn / Levinsohn + geographic markers]
```

**When data unavailable:**
```markdown
## Data Sources
**Note:** Levinsohn/Masoretic data not available. Using genre-appropriate markers for boundaries.
```

---

## Red Flags — STOP

If you think any of these, you are about to violate the skill:

| # | Thought | Rule |
|---|---------|------|
| 1 | "User requested N sessions for micro-book" | Rule 1: Check limits. Refuse if exceeded. |
| 2 | "User said just pick one / I trust you" | Rule 3: Present 2-4 options anyway. |
| 3 | "User is an expert, skip options" | Rule 3: Expertise doesn't bypass options. |
| 4 | "Psalms can be divided by session count" | Rule 2: Switch to curation mode. |
| 5 | "This is the standard Revelation outline" | Rule 4: Present both linear and recapitulation. |
| 6 | "Isaiah in 3 is fine" / "I'll warn then comply" | Rule 5: Refuse = no session table. Do NOT produce divisions after saying "Not Recommended." |
| 7 | "I'll validate their division to be helpful" | Rule 6: Note structural concerns. Don't rubber-stamp. |
| 8 | "Use lectionary as requested" | Rule 6: Lectionary = metadata. Present structural options. |
| 9 | "I'll skip the fit assessment" | Every output starts with Fit Assessment. |
| 10 | "Markers are obvious" | Show your work. Cite Levinsohn/Masoretic evidence. |
| 11 | "No פ/ס here, so skip it" | State "No Masoretic marker at X" — transparency required. |
| 12 | "I'll cite markers at session END" | Markers validate session STARTING verse. |
| 13 | "I know the joy count in Philippians" | Call `query_vocabulary`. Never cite from training knowledge. |
| 14 | "Web search failed, cite Fee anyway" | No web search = no thematic option. |
| 15 | "Verse range is just small segmentation" | Verse range = slice mode. Different output. |
| 16 | "3 slices for 67 verses is fine" | Calculate: 67 ÷ 8 ≈ 8 slices. Push back. |
| 17 | "Psalm 23 can be 3 slices" | 6 verses ÷ 3 = 2 per slice. Below minimum. Refuse. |
| 18 | "I'll slice mechanically by verse count" | Check dialogue, chiasmus, conditionals first. |
| 19 | "Micro-book/Psalms don't need MCP" | Every path goes through data-retriever. No exceptions. |
| 20 | "Data-retriever failed, use training knowledge" | Fall back to direct MCP calls. Never substitute training. |
| 21 | "I'll figure out structure myself" | Spawn argument-flow for structural analysis. |

---

## Reference Files

- `reference/book-exceptions.yaml` — Micro-books, anthologies, contested books
- `reference/book-genres.yaml` — Genre mapping for all 66 books
- `reference/genre-methodology.yaml` — Markers and methodology per genre
- `reference/compositional-debates.yaml` — Partition theory notes (2 Cor, Philippians)
- MCP tool `query_discourse_features` — Levinsohn discourse features (NT)
- MCP tool `query_paragraph_breaks` — Masoretic paragraph markers (OT)
- MCP tool `query_vocabulary` — Vocabulary frequencies and clustering
