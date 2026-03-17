---
name: argument-flow
description: Use when mapping the logical structure of a biblical passage using discourse markers and morphological data. Use when a user asks for argument flow, logical structure, proposition chain, connective analysis, or how Paul's argument works in an epistle. Produces a numbered proposition chain grounded in MCP data before any prose is written.
allowed-tools: Read, WebSearch, mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_morphology, mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_discourse_features, mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_paragraph_breaks, mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_vocabulary, mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_themes_for_lemmas, mcp__plugin_claude-of-alexandria_claude-of-alexandria-mcp__query_theme
---

# Argument Flow

## Purpose

Map the logical argument of a biblical passage using discourse markers and morphological data. Produces a connective-anchored proposition chain showing how clauses relate to each other.

**Foundational principle:** Violating the letter of the rules is violating the spirit of the rules.

---

## Iron Rules

### Rule 1: Call MCP Tools BEFORE Composing Any Prose

**`query_morphology` with `pos_filter: "conjunction"` is called BEFORE writing a single sentence of analysis.**

Do not compose the argument from training data and then verify. Let the data shape the analysis.

**NT passages:**
```
query_morphology: {"book": "Philippians", "range": "2:1-2:4", "pos_filter": "conjunction"}
query_discourse_features: {"book": "Philippians"}
```

**OT passages:**
```
query_morphology: {"book": "Genesis", "testament": "ot", "range": "22:1-22:14"}
query_paragraph_breaks: {"book": "Genesis"}
```

**If MCP returns no data:** State this explicitly. Confidence ceiling drops to MEDIUM. Do not proceed from training data alone.

**Wrong:**
```
Paul uses εἰ conditionals to ground the command — this is a standard Pauline pattern.
```
(No MCP call. Training data presented as verified analysis.)

**Correct:**
```
[Called query_morphology for Phil 2:1-4 with pos_filter "conjunction"]
[Result: εἰ (2:1 ×4), οὖν (2:1), ἵνα (2:2)]
Connectives: εἰ = condition, οὖν = inference, ἵνα = purpose [query_morphology]
```

---

### Rule 2: State Confidence Tier First — Always

**Every response begins with a confidence declaration.**

```
CONFIDENCE: HIGH
Evidence: query_morphology (Phil 2:1-4), query_discourse_features (Philippians)
```

| Tier | Required evidence |
|------|-----------------|
| **HIGH** | MCP tool data for the specific passage |
| **MEDIUM** | MCP inconclusive; scholarly commentary (web search, cited) |
| **LOW** | MCP failed; only training data available |
| **CANNOT ANSWER** | No data, no scholarship; outside scope |

Training-data knowledge is NOT Tier 1 evidence. Only MCP output counts.

---

### Rule 3: Output the Proposition Chain

**Every response includes a numbered proposition chain. No exceptions.**

```
## Proposition Chain

1. [Condition] εἰ (2:1) — "If there is encouragement in Christ..."
   → Grounds: the following command rests on this shared reality

2. [Inference] οὖν (2:1) — "complete my joy therefore..."
   → Command follows from accumulated conditions

3. [Specification] (asyndeton, 2:2) — "having the same love, united in spirit"
   → Unpacks what "same mind" means

4. [Contrast] μηδέν (2:3) — "nothing from selfish ambition"
   → Negative boundary of the command

5. [Purpose] ἵνα (2:4, implicit) — "looking to others' interests"
   → Application of the preceding command
```

Format rules:
- One proposition per clause
- Label each with connective type: Condition / Inference / Purpose / Contrast / Ground / Result / Concession / Asyndeton
- Include the Greek connective with verse reference
- Each proposition's logical relationship to adjacent propositions is stated

---

### Rule 4: Genre Detection Before Analysis

**Detect genre from the book. Apply the correct structural method.**

| Genre | Primary method | MCP tools |
|-------|---------------|-----------|
| **NT Epistle** | Conjunction analysis (γάρ, οὖν, δέ, ἵνα, εἰ, ἀλλά, ὥστε) | `query_morphology` + `query_discourse_features` |
| **NT Narrative** | Scene / dialogue / resolution | `query_discourse_features` (historical present, left dislocation) |
| **OT Narrative** | Scene / climax / resolution | `query_morphology (ot)` + `query_paragraph_breaks` |
| **OT Poetry** | Semantic parallelism (A / B / intensification) | `query_morphology (ot)` |
| **Apocalyptic** | Vision units / heavenly scene / response | `query_discourse_features` |

**Genre must be stated at the top of the analysis.** Do not apply epistle logic to narrative. Do not apply narrative logic to poetry.

---

### Rule 5: Scope Warning for Large Passages

**If the passage exceeds 30 verses, warn before proceeding.**

```
⚠️ SCOPE WARNING: Romans 1:1–8:39 (239 verses) exceeds practical scope for
argument-flow analysis. Recommend subdividing into units:
- Romans 1:1-17 (thesis)
- Romans 3:21-31 (righteousness)
- Romans 8:1-17 (life in the Spirit)

Continue with the full range? Or map one sub-section?
```

Do not produce a high-level summary pretending to map 239 verses. If the user confirms, note the limitation in Section 1.

---

### Rule 6: No Devotional Language

**This skill produces analytical output. Application is the user's domain.**

The skill maps what the text's logic is. It does not:
- Tell the user what to do with the analysis
- Frame propositions in devotional language
- Use warm, applicatory images ("God standing sentinel over the inner life")
- Tell the user how this passage "speaks to" their situation

**Wrong:**
```
Paul's argument calls us to lay down our self-interest, trusting that God's
peace will guard our hearts.
```

**Correct:**
```
v. 7: [Result] "the peace of God... will guard your hearts"
→ Consequence of the preceding practice (v. 6 prayer with thanksgiving)
```

---

### Rule 7: Argument-Flow Does Not Render Theological Verdicts

**If the user asks to map the argument AND validate a theological claim, handle ARGUMENT-FLOW first.**

After completing the proposition chain, note: "Evaluation of [theological claim] requires `consult-biblical-scholar`." Do not issue a verdict from within this skill.

**Wrong (mode conflation):**
```
Verdict: The claim that faith is a gift is exegetically imprecise for this text.
```

**Correct:**
```
## Proposition Chain
[...argument-flow output...]

Note: The question of whether faith is the referent of τοῦτο (v. 8) is an
active interpretive debate. Evaluating that claim requires consult-biblical-scholar.
```

---

## Connective Reference

| Greek | Transliteration | Function | Proposition label |
|-------|----------------|----------|------------------|
| γάρ | gar | Ground / reason | [Ground] |
| οὖν | oun | Inference / therefore | [Inference] |
| δέ | de | Contrast or continuation | [Contrast] or [Continuation] |
| ἀλλά | alla | Strong contrast | [Contrast: strong] |
| ἵνα | hina | Purpose | [Purpose] |
| ὥστε | hōste | Result | [Result] |
| εἰ | ei | Condition | [Condition] |
| διότι | dioti | Causal | [Ground: causal] |
| ὅτι | hoti | Content or causal | [Content] or [Ground] |
| (none) | asyndeton | No connective — note relationship | [Asyndeton] |

---

## Workflow

```
1. Parse invocation
   → Extract book, range
   → Detect genre from book name
   → If no passage: cannot run (passage required; no topic mode)

2. Scope check
   → If > 30 verses: warn, await confirmation
   → If confirmed: proceed with note

3. MCP tool calls (BEFORE any prose)
   NT: query_morphology (pos_filter: "conjunction") + query_discourse_features
   OT: query_morphology (testament: "ot") + query_paragraph_breaks

4. Confidence tier
   → Based only on what MCP returned
   → If MCP failed: MEDIUM ceiling, noted explicitly

5. Compose output
   → Confidence tier first
   → Connective inventory table
   → Proposition chain (numbered, labeled)
   → Preachable summary (1-2 sentences, analytical tone)
   → Data sources

6. Boundary check
   → If user asked a theological question alongside: note consult-biblical-scholar
```

---

## Output Format

**Required in every response:**

```markdown
CONFIDENCE: [HIGH / MEDIUM / LOW]
Evidence: [MCP tools called + key data returned]
Genre: [Epistle / Narrative / Poetry / Apocalyptic]

## Connective Inventory

| Verse | Greek | Function | Count |
|-------|-------|----------|-------|
| [ref] | [term] | [label] | [n] |

[Note any significant asyndeton (missing connectives) — these also carry meaning]

## Proposition Chain

1. [Label] [Greek connective] ([ref]) — "[English clause]"
   → [Relationship to adjacent propositions]

2. ...

## Preachable Summary

[1-2 sentences stating the argument's movement in plain language.
Analytical tone only. No applicatory framing.]

## Data Sources

- query_morphology: [book, range, pos_filter used]
- query_discourse_features: [book] (if NT)
- query_paragraph_breaks: [book] (if OT)
```

---

## Red Flags

| Red flag | What the skill forces |
|----------|-----------------------|
| **Composing before MCP** | MCP called BEFORE any prose |
| **No confidence tier** | CONFIDENCE: declared at top |
| **Training data as Tier 1** | Only MCP output is Tier 1 |
| **Prose summary instead of chain** | Numbered proposition chain required |
| **Devotional framing** | Analytical language only |
| **Mode conflation (verdict on claim)** | Note consult-biblical-scholar boundary |
| **Epistle conjunctions on narrative** | Genre detected; correct tools applied |
| **No scope warning** | > 30 verses triggers warning |
| **"Scholars agree" without citation** | Every scholarly claim cites author + work |

---

## Invocation

```
/argument-flow Phil 2:1-4
/argument-flow Romans 8:1-11
/argument-flow Hebrews 11:1-12
/argument-flow 1 Corinthians 13:1-7
/argument-flow Genesis 22:1-14
```

Output is inline (not saved to file). Every response includes confidence tier,
connective inventory, proposition chain, and data sources.
