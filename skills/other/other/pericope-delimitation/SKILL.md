---
name: pericope-delimitation
description: Use when validating whether a biblical passage constitutes a coherent discourse unit. Use when user asks to check passage boundaries, evaluate if a text range is a natural pericope, or needs to know if their selected passage should be extended or contracted.
allowed-tools: Read, WebSearch, mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_discourse_features, mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_paragraph_breaks, mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_morphology
---

# Pericope Delimitation

## Purpose

Validate whether a user-provided passage constitutes a coherent discourse unit.
Recommend extensions or contractions based on **linguistic evidence from bundled data**.

**Output:** Inline conversation response (not saved to file).

**Critical rule:** Never validate or reject a boundary without checking the actual data.
Training knowledge about "famous passages" or commentary traditions does NOT substitute
for discourse feature evidence.

---

## Iron Rules

**These rules are non-negotiable. Override them only if the data explicitly requires it.**

### Rule 1: Data First, Memory Last

Always check discourse data BEFORE forming a verdict:
- **NT passages:** Call `query_discourse_features` MCP tool for Levinsohn GNT data
- **OT passages:** Call `query_paragraph_breaks` MCP tool for Masoretic markers
- **Both:** Check genre-specific conventions from book-genres.yaml

Never say "this passage works well" based on training knowledge alone.

### Rule 2: Separate Boundary Assessment

Always assess start and end boundaries INDEPENDENTLY:
- Start boundary: Is this where a discourse unit begins?
- End boundary: Is this where a discourse unit ends?
- A boundary is **Confirmed** (data evidence), **Weak** (no discontinuity), or **Mid-unit** (cuts into an ongoing unit)

### Rule 3: Structured Verdict First

Lead with the verdict before explanation:
- **VALID** — passage is a coherent discourse unit with boundary evidence
- **EXTEND** — passage should include additional verses (specify which + why)
- **CONTRACT** — passage includes multiple units (specify split point + why)
- **ADJUST** — both start and end need adjustment

### Rule 4: Always Recommend What To Do

Never just say "no." Every non-VALID verdict must specify:
- What the correct boundaries are
- Why those boundaries are supported by data
- If constraints apply (e.g., session length), the minimum viable pericope

### Rule 5: Include Data Sources

Every assessment must end with a `### Data Sources` subsection citing:
- Levinsohn GNT Discourse Features (for NT, specify which features checked)
- Masoretic paragraph markers (for OT, specify which markers found/absent)
- Genre-specific conventions applied

---

## Workflow

```
1. Parse passage reference
   → Identify: book, start verse, end verse, testament, genre

2. Check boundary data (NT or OT)
   NT: Call query_discourse_features MCP tool for features at/near start and end verse
   OT: Call query_paragraph_breaks MCP tool for markers (פ/ס) at/near start and end verse

3. Check genre-specific markers
   → Epistolary formulas (NT letters), toledot (Genesis), etc.

4. Assess each boundary
   Start boundary: Confirmed / Weak / Mid-unit
   End boundary: Confirmed / Weak / Mid-unit

5. Determine verdict
   VALID = both boundaries confirmed or well-supported
   EXTEND = weak/mid-unit end (or start)
   CONTRACT = both boundaries OK but multiple units within
   ADJUST = weak/mid-unit on both ends

6. Draft output in standard format

7. [Optional] Cross-check data claims against MCP tool output if verifiable claims present
```

---

## Output Format

```markdown
## Pericope Assessment: [Book Chapter:Verse-Chapter:Verse]

**Verdict:** [VALID | EXTEND to X:Y | CONTRACT at X:Y | ADJUST]

### Start Boundary ([Chapter:Verse])
**Status:** [Confirmed | Weak | Mid-unit]
- [Evidence item 1 - cite specific discourse feature or marker]
- [Evidence item 2]
- [Genre convention: ...]

### End Boundary ([Chapter:Verse])
**Status:** [Confirmed | Weak | Mid-unit]
- [Evidence item]
- [Why this is the boundary or why it is not]

### Recommendation
[What to do: exact verse range, why it's better, what it accomplishes]

[If applicable:] **Minimum viable pericope:** [range] — [what this covers]

### Data Sources
- [Primary data used: Levinsohn feature names checked OR Masoretic markers found/absent]
- [Genre conventions consulted: book-genres.yaml entry]
- [MorphGNT/SBLGNT if vocabulary noted]
```

---

## Evidence Standards

### What Counts as Confirmed Boundary Evidence (NT)

- **Levinsohn PoD (Point of Departure):** Referential or Situational — strong boundary signal
- **Disclosure formula:** γινώσκειν, γνωρίζω, θέλω δὲ ὑμᾶς εἰδέναι — new section opener
- **Vocative address:** ἀδελφοί, ἀγαπητοί — common new unit marker in epistles
- **Historical Present at unit start:** Marked onset signal in narrative
- **Over-encoding (full noun phrase resuming a referent):** New scene/unit signal

### What Counts as Confirmed Boundary Evidence (OT)

- **פ (petucha):** Open/major paragraph break — strong boundary signal
- **ס (setumah):** Closed/minor paragraph break — moderate boundary signal
- **Toledot formula:** אֵלֶּה תּוֹלְדוֹת — structural book marker in Genesis
- **Resumptive formula:** "And it came to pass..." after interpolation

### What Counts as Weak/Mid-Unit

- **No feature at claimed boundary, but continuity of subject** → Weak
- **Discourse features within passage indicating internal boundaries** → check for CONTRACT
- **Passage begins with continuation particle (δέ, καί, וַ)** → may be Mid-unit start

---

## Genre-Specific Guidance

### NT Epistles (Romans, Corinthians, Galatians, Ephesians, Philippians, etc.)

**Natural pericope boundaries:**
- Epistolary opening (salutation + thanksgiving period)
- Disclosure formulas: γινώσκειν, παρακαλῶ, ἐρωτῶ
- Vocative transitions: ἀδελφοί, ἀγαπητοί
- Body-closing boundary (paraenesis beginning, travel plans, greetings)

**Minimum pericope:** At least one complete epistolary sub-unit (not mid-argument)

**Common mistakes to avoid:**
- Isolating "thesis statements" from their argument units (e.g., Rom 1:16-17 is embedded in opening)
- Cutting before the prayer-request that completes a thanksgiving (e.g., Phil 1:3-8 needs 1:9-11)

### NT Narrative (Gospels, Acts)

**Natural pericope boundaries:**
- Scene changes (location, participants, time)
- Historical Present at onset (Levinsohn data)
- Reported Speech conclusion
- Summary statements

**Minimum pericope:** Complete scene or discourse unit (not mid-dialogue)

### OT Narrative (Genesis-2 Kings, Ruth, Esther, etc.)

**Natural pericope boundaries:**
- פ (petucha) marker — always check sefaria/Masoretic data
- Scene/character shifts
- Toledot formula (Genesis)
- Resumptive narrative formula

**Minimum pericope:** Complete episode (single unified action + outcome)

### OT Poetry (Psalms, Proverbs, etc.)

**Natural pericope boundaries:**
- Psalm = individual poem
- Proverbs = collection boundaries (ch. 1-9, 10:1-22:16, etc.)
- Acrostic structures (Lamentations, some Psalms)

---

## Common Failure Patterns

These represent the Red Flags this skill prevents:

| Failure | How to Avoid |
|---------|--------------|
| "This famous passage works as a unit" | Check data first — famous ≠ coherent unit |
| "1:16-17 is the thesis so it's valid" | Check Levinsohn at 1:16 — is there a boundary feature? |
| "Any passage can be preached" | True homiletically, but discourse unit ≠ "any verses" |
| "Commentary tradition validates this" | Commentaries work with inherited divisions, not always discourse-sound |
| "There's no obvious problem" | Absence of obvious problem ≠ confirmed boundary |
| Weak boundary stated as Confirmed | Only use "Confirmed" when data positively attests the boundary |
| Missing Data Sources section | Every assessment must include what was checked |

---

## Reference Data Access

### NT: Levinsohn Discourse Features

**Call:** `query_discourse_features` MCP tool with `{"book": "{book}", "chapter_range": "{range}"}`

Key features for boundary detection:
- **Referential PoD** — strong section boundary signal
- **Situational PoD** — strong section boundary signal
- **Historical Present** — narrative scene onset
- **Reported Speech** — embedded discourse boundaries
- **Over-encoding** — new unit onset signal

**How to use:** Check if the start verse or the verse AFTER the claimed end verse
has features that would confirm a boundary.

### OT: Masoretic Paragraph Markers

**Call:** `query_paragraph_breaks` MCP tool with `{"book": "{book}", "chapter_range": "{range}"}`

**How to use:** Check for פ (petucha) or ס (setumah) at or near the claimed boundary verse.
If present: boundary is Confirmed.
If absent: boundary is Weak (state this explicitly).

### Genre Reference

Data location: `skills/biblical-segmentation/reference/book-genres.yaml`

Check the genre entry for the book to apply the correct boundary methodology.

---

## Example Assessment

### /pericope-delimitation Phil 1:3-8

```markdown
## Pericope Assessment: Philippians 1:3-8

**Verdict:** EXTEND to 1:3-11

### Start Boundary (1:3)
**Status:** Confirmed
- Epistolary convention: εὐχαριστῶ formula begins standard thanksgiving period
- Levinsohn: Referential PoD at 1:3 signals new section after prescriptio (1:1-2)
- The prescriptio (salutation) ends at 1:2; thanksgiving period begins at 1:3

### End Boundary (1:8)
**Status:** Weak — mid-argument
- Levinsohn: No PoD or boundary feature at 1:9; continuity markers present
- No discourse discontinuity between 1:8 and 1:9
- The grounds for the thanksgiving (1:7-8) set up the prayer request (1:9-11)
- Levinsohn: Disclosure formula γινώσκειν at 1:12 confirms NEXT unit begins there

### Recommendation
Extend to **1:3-11**. The thanksgiving-prayer period (εὐχαριστῶ...ἐπιτελέσει...
καρπὸν δικαιοσύνης) is a single rhetorical movement. Ending at 1:8 severs
the prayer request (1:9-11) from the thanksgiving it responds to.

The boundary at 1:12 is positively confirmed by the disclosure formula
γινώσκειν (1:12) — this is the standard Pauline signal for new section onset.

**Minimum viable pericope:** 1:3-6 (thanksgiving proper, ending with the
ἐπιτελέσει promise). But this loses the grounds (1:7-8) and prayer (1:9-11)
that give the thanksgiving its epistolary completeness.

### Data Sources
- Levinsohn GNT Discourse Features (dataset 2016; book: Levinsohn 2000): Referential_PoD checked for Phil 1:3;
  boundary features checked for 1:8-1:9 (none found); γινώσκειν formula confirmed at 1:12
- Genre: Epistle (epistolary markers primary) — book-genres.yaml: Philippians = epistle
- MorphGNT/SBLGNT: γινώσκειν form confirmed at 1:12
```

---

## Invocation

```
/pericope-delimitation Phil 1:3-8
/pericope-delimitation Genesis 37:2-11
/pericope-delimitation Romans 9:1-11:36
/pericope-delimitation "Mark 1:1-20"
```

Pass a verse range in `Book Chapter:Verse-Chapter:Verse` format.
Book name can be abbreviated (Phil, Gen, Rom, etc.) or full.
