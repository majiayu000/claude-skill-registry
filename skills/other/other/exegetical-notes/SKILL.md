---
name: exegetical-notes
description: Use when producing structured exegetical analysis of a biblical passage. Use when user asks for exegetical notes, verse analysis, passage study, word study with morphology, or detailed interpretive framework for a text. Always English output.
allowed-tools: Read, Write, WebSearch, mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_discourse_features, mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_paragraph_breaks, mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_vocabulary, mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_morphology, mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_ot_quotes, mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_lemmas, mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_themes_for_lemmas, mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_theme
---

# Exegetical Notes

## Purpose

Produce structured, context-neutral exegetical analysis of a biblical passage.
Data-grounded. Always English. Output to file (default) or inline (`--output print`).

**Key constraint:** Every data claim must come from bundled data or web-verified scholarly sources.
Training knowledge supplements but never substitutes for data.

---

## Iron Rules

### Rule 1: Run Pericope Check First — Warning BEFORE Notes

Before generating notes, run a lightweight boundary check:

1. Identify passage boundaries
2. Check Levinsohn (NT) or Masoretic (OT) for boundary confirmation
3. **If boundaries are problematic:** Print the warning BEFORE the notes header. The warning is a standalone block that appears BEFORE `# Exegetical Notes:`. Do not embed it inside Section 1. Do not skip it.
4. **If user confirms problematic passage:** Proceed with note in Pericope Status

**Warning format (print this BEFORE the notes):**
```
⚠️ Boundary check: [Book] [Range] may be a partial unit.
[Specific issue with discourse evidence]
Recommended passage: [better range]

Proceeding with [original range] — boundary issue noted in Pericope Status.
```

**Correct output order for problematic boundaries:**
1. First: ⚠️ Boundary check warning (standalone)
2. Then: `# Exegetical Notes: [Book] [Range]` header and all 10 sections

**Wrong:** Embedding the boundary warning inside Section 1 without a standalone warning first.

### Rule 2: Lexical Analysis Uses query_morphology MCP Tool

Section 4 (Lexical Analysis) must:
- Call `query_morphology` MCP tool for parsing data
- Cite actual counts from `query_vocabulary` MCP tool
- Never say "appears frequently" — give exact count and verse references
- Format: `lemma (reference): morph description [query_morphology]`

**Valid:** `ἐναρξάμενος (1:6): lemma ἐνάρχομαι, aorist middle participle, nom. sg. masc. [query_morphology]`
**Invalid:** `ἐναρξάμενος is an aorist participle meaning "having begun"`

### Rule 3: Tier All Interpretive Claims

Section 6 must use exactly four tiers, each labeled:

- **Tier 1: Linguistic Evidence** — morphology/grammar directly contradicts the misreading
- **Tier 2: Discourse Evidence** — Levinsohn features or structure contradicts
- **Tier 3: Scholarly Consensus** — web-search-verified with real citations
- **Tier 4: Interpretive Notes** — agent assessment, labeled as such

Never mix tiers. If no Tier 3 source found after web search, state this explicitly.

### Rule 4: Tier 3 Source Quality

For web searches (Tier 3 guardrails):

**Prefer (Tier A):** NICNT, NIGTC, ICC, WBC, BECNT, Hermeneia, BNTC, AB, BDAG
**Accept (Tier B):** Study Bibles with scholarly notes, TDNT, ABD, NAC
**Use with caution (Tier C — always cite tier):** Popular commentaries (BST, TNTC), credentialed scholar blogs
**Reject (Tier D):** Devotional websites, AI content, uncredited blogs, forums

If only Tier C sources found, state: "[Tier C source, use with caution]"
If no verifiable source found, state: "No Tier A/B source located for this claim."

### Rule 5: Cross-Check Data Claims Before Delivering

After generating the full notes:
1. For each data claim in the output (lemma frequencies, morphological parsings, discourse features), re-query the relevant MCP tool to confirm the cited value matches
2. Report cross-check results in Section 10
3. If any mismatches: correct the claim before delivering

### Rule 6: Exactly 10 Sections, Exactly These Names

The output format has exactly 10 sections. Use exactly these section titles:
1. Passage in Literary Context
2. Internal Structure
3. Propositional Summary
4. Lexical Analysis
5. Exegetical Conclusions
6. Interpretive Guardrails
7. Open Questions
8. Intertextual Links
9. Data Sources
10. Verification

**Do not rename sections.** Do not substitute "Homiletical Trajectories" for "Interpretive Guardrails." Do not substitute "Theological Themes" for "Exegetical Conclusions." Do not substitute "Discourse Structure" for "Internal Structure." Do not omit sections. Do not add sections. Do not reorder sections.

**Do not abbreviate the output** even if the user asks for "brief" or "essentials." All 10 sections are required for every invocation. The Verification section (Section 10) is never optional.

### Rule 7: Deliver Output

**File mode** (default, or `--output file`):
Save to:
```
~/.claude/exegetical-notes/{book_name}/{YYYY-MM-DD}-{chapter-verse-to-chapter-verse}.md
```
Examples:
- `~/.claude/exegetical-notes/philippians/2026-02-18-1-1-11.md`
- `~/.claude/exegetical-notes/genesis/2026-02-18-37-2-11.md`

After saving, report the saved path to user.

**Print mode** (`--output print`):
Output the complete notes inline in your response. Do not save to file. Do not summarize. Print ALL 10 sections in full, directly in the response. The user sees only what you print — if you save to file instead, the user gets nothing useful.

**Never ignore `--output print`.** If the invocation says `--output print`, you MUST print inline. Do not save to a file and return a summary. Do not "display" a summary of what you generated. Print the full document.

---

## Workflow

```
Step 1: Parse invocation → book, range, --output, --context

Step 2: PERICOPE CHECK (MANDATORY — DO NOT SKIP)
   │
   ├─ Call query_discourse_features for the book
   ├─ Check if range aligns with discourse boundaries
   │
   ├─ Boundaries OK? → Proceed to Step 3
   │
   └─ Boundaries PROBLEMATIC?
      │
      ├─ STOP. Print the ⚠️ warning BEFORE anything else.
      │  Format: "⚠️ Boundary check: [Book] [Range] may be a partial unit..."
      │  This warning must appear BEFORE the "# Exegetical Notes" header.
      │  Do NOT embed it in Section 1. Print it FIRST, separately.
      │
      └─ Then proceed to Step 3 (with boundary issue noted in Pericope Status)

Step 3: Gather data via MCP tools
   NT: query_morphology, query_discourse_features, query_vocabulary
   OT: query_morphology (testament: ot), query_paragraph_breaks, query_vocabulary (testament: ot)
   Epistles: also query_morphology with pos_filter: "conjunction"

   Logical connectives for Section 2 (epistles):
   γάρ=grounds, οὖν=inference, δέ=contrast/continuation, ἀλλά=strong contrast,
   ἵνα=purpose, ὥστε=result, εἰ=condition, διότι/ὅτι=causal

Step 4: Web search for Tier 3 scholarly sources
   → Prefer Tier A/B (NICNT, NIGTC, ICC, WBC, BECNT, Hermeneia, BDAG)
   → Note author, title, publisher

Step 5: Generate ALL 10 sections using EXACT template titles (Rule 6)
   Every section is mandatory. Never skip, rename, or merge sections.

Step 6: Cross-check data claims against MCP tool output

Step 7: Fix any mismatches found in cross-check

Step 8: DELIVER OUTPUT
   │
   ├─ --output print? → Print ALL 10 sections inline. Do NOT save to file.
   │                     Do NOT summarize. The full document goes in the response.
   │
   └─ --output file (or default)? → Save to file path. Report path to user.
```

---

## Output Format (All 10 Sections Required — Use Exact Titles)

```markdown
# Exegetical Notes: [Book] [Range]

**Generated:** [YYYY-MM-DD]
**Passage:** [Book Chapter:Verse-Chapter:Verse] (SBLGNT/NA28 for NT; MT/OSHB for OT)
**Genre:** [epistle | narrative | poetry | prophecy | wisdom | apocalyptic]
**Pericope Status:** [Valid unit | Extended from user input | Confirmed problematic — noted in Section 1]

---

## 1. Passage in Literary Context

[Where this unit sits in the book's argument or narrative arc]
[Connection to preceding unit — what it follows from]
[Connection to following unit — what leads into next section]
[If --context provided: reference the segmentation context]
[If pericope check found issues: note here]

## 2. Internal Structure

[Clause-level structure using discourse features]
[Table required:]

| Verses | Element | Function |
|--------|---------|----------|
| [range] | [label] | [discourse role] |

[Levinsohn feature names cited for internal divisions]
[Masoretic markers cited for OT internal structure]

## 3. Propositional Summary

[The passage's central proposition in 1-2 sentences]
[Secondary propositions if argument is complex]
[Keep strictly descriptive — no Tier 4 claims here]

## 4. Lexical Analysis

[For each key lemma:]
**[Greek/Hebrew] ([reference])**: lemma [lemma form], [full parsing] [query_morphology]
Gloss: "[translation]"
[Semantic group from semantic_groups.yaml if applicable]
[Frequency in book from query_vocabulary]
[Significance for passage interpretation]

[Flag hapax legomena or unusual forms]
[Note semantic range if relevant to interpretive decision]

## 5. Exegetical Conclusions

[Numbered list of defensible interpretive claims]
[Each grounded in sections 2-4]
[Example:]
1. [Claim grounded in morphology — cite the parsing]
2. [Claim grounded in discourse structure — cite the feature]
3. [Claim grounded in intertextual connection — cite the link]

## 6. Interpretive Guardrails

[For each common misreading:]

### [Misreading description]

**Tier 1: Linguistic Evidence**
[How morphology/grammar contradicts this reading]
[Cite: specific parsing, form, or grammatical construction]

**Tier 2: Discourse Evidence**
[How discourse structure contradicts this reading]
[Cite: specific Levinsohn feature or Masoretic marker]

**Tier 3: Scholarly Consensus** (web-verified)
[Citation: Author, Title, Publisher, Year, pp.]
[Tier level: A | B | C — state if C]

**Tier 4: Interpretive Notes** (Agent assessment)
[Clearly labeled as agent assessment, not established fact]

## 7. Open Questions

[Unresolved exegetical issues where data is insufficient]
[Areas of genuine scholarly debate]
[Questions this analysis cannot settle]
[What additional research would be needed]

## 8. Intertextual Links

[Cross-references with verse citations]
[Format: "Reference → Connection to current passage"]
[OT quotations or allusions (call query_ot_quotes for NT passages)]
[Semantic group connections across testaments]
[Parallel passages with significant differences noted]

## 9. Data Sources

- MorphGNT/SBLGNT (CC BY-SA 3.0) — morphological parsing via query_morphology MCP tool
- [OR] Open Scriptures Hebrew Bible morphhb (CC BY 4.0) — Hebrew morphology
- Levinsohn GNT Discourse Features (dataset 2016; book: Levinsohn 2000) — discourse analysis via query_discourse_features MCP tool
- [OR] Sefaria / OpenScriptures paragraph markers — Masoretic structure
- [Vocabulary source: query_vocabulary MCP tool with per-book data]
- [Semantic groups: semantic_groups.yaml]
- [Tier 3 sources: full citations as used in Section 6]

## 10. Verification

**MCP cross-check results:**
- Data claims checked: [N]
- Claims confirmed (PASS): [N]
- Claims corrected: [N — list each correction below if any]
- Claims not cross-checkable: [N — e.g., Tier 3 citations, semantic notes]
- Overall: [PASS | CORRECTED]

[If corrections made: list each original claim, the MCP query result, and the correction]
```

---

## Invocation Format

```
/exegetical-notes Phil 1:1-11
/exegetical-notes Phil 1:1-11 --output print
/exegetical-notes Genesis 37:2-11
/exegetical-notes Romans 3:21-26
/exegetical-notes Genesis 37:2-11 --context "segmentation: Joseph narrative, 8 sessions"
```

- `--output`: Optional. `file` (default) saves to disk. `print` outputs inline.
- `--context`: Optional. Provides segmentation context for Section 1.
- Book names accept abbreviations (Phil, Gen, Rom, etc.) or full names.
- Testament auto-detected from book name.

---

## Reference Data Access

### NT Morphological Data

Call `mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_morphology` with `{"book": "[Book]", "range": "[chapter:verse-chapter:verse]"}`

### OT Morphological Data

Call `mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_morphology` with `{"book": "[Book]", "testament": "ot", "range": "[chapter:verse-chapter:verse]"}`

### Vocabulary Frequencies

Call `mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_vocabulary` with `{"book": "[Book]", "testament": "[nt|ot]"}`

### Levinsohn Discourse Features (NT)

Call `mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_discourse_features` with `{"book": "[Book]"}`

### Masoretic Markers (OT)

Call `mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_paragraph_breaks` with `{"book": "[Book]"}`

### Claim Verification

Cross-reference MCP tool output against cited verse and morphological claims.

### Semantic Groups

Located at: `skills/biblical-segmentation/reference/vocabulary/semantic_groups.yaml`

---

## Semantic Groups Reference

Key semantic families from `semantic_groups.yaml` (for Section 4 connections):

| Group | NT lemmas | OT Strong's |
|-------|-----------|-------------|
| Joy | χαίρω, χαρά | H8057, H8056 |
| Faith | πίστις, πιστεύω | H0539 |
| Love | ἀγάπη, ἀγαπάω | H0157, H2617 |
| Righteousness | δικαιοσύνη, δίκαιος | H6663, H6664 |
| Covenant | — | H1285 (בְּרִית) |
| Holy | — | H6918, H6944 |

---

## Common Failure Patterns (Red Flags)

| Failure | Prevention |
|---------|-----------|
| "χαρά appears frequently" | Call query_vocabulary: χαρά (5x) at 1:4, 1:25, 2:2, 2:29, 4:1 |
| Wrong voice in morphology | Always verify via query_morphology MCP tool |
| "Scholars agree..." without citation | Web search required; cite author/title/year |
| Mixing Tier 1 and Tier 4 | Label every tier claim explicitly |
| Skipping Section 10 cross-check | Re-query MCP tools to confirm every data claim before delivering |
| `--output print` but saved to file | If `--output print` is in the invocation, print ALL 10 sections inline. Never save to file and return a summary. |
| Renaming sections | Use the exact 10 section titles from the template. "Homiletical Trajectories" is not "Interpretive Guardrails." |
| Only 6 sections instead of 10 | Every invocation produces exactly 10 sections. No abbreviation, no "brief" mode. |
| User says "keep it brief" → skip sections | All 10 sections are mandatory. "Brief" may shorten prose within sections but never removes sections. |
| Proceeding past problematic pericope without warning | Pericope check is mandatory Step 1 |
| No logical connectives in epistle analysis | For epistles: query_morphology pos_filter "conjunction", map γάρ/οὖν/δέ/ἀλλά/ἵνα flow |

---

## Example Output Fragment: Section 4 (Lexical Analysis)

```markdown
## 4. Lexical Analysis

**ἐναρξάμενος (1:6)**: lemma ἐνάρχομαι, aorist middle participle,
nominative singular masculine [query_morphology]
Gloss: "having begun"
Semantic note: Middle voice is significant — "begun in/among themselves" or
reflexive causative. Contrast with active voice ἐναρχόμενος (not attested here).
Frequency in Philippians: 1x (this passage) [query_vocabulary]

**ἐπιτελέσει (1:6)**: lemma ἐπιτελέω, future active indicative,
3rd person singular [query_morphology]
Gloss: "will complete/finish"
Temporal referent: ἄχρι ἡμέρας Χριστοῦ Ἰησοῦ — eschatological frame.
Frequency in Philippians: 1x [query_vocabulary]

**χαρά (1:4)**: lemma χαρά (noun), [not a verb form — check pos in morphology data]
Frequency in Philippians: 5x (1:4, 1:25, 2:2, 2:29, 4:1) [query_vocabulary]
Semantic group: Joy family — see also χαίρω (9x in Philippians) [semantic_groups.yaml]
```
