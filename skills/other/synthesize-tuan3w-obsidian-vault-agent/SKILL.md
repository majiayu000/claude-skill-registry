---
name: synthesize
description: >-
  Deep cross-domain synthesis engine for the vault. Triggers on "synthesize X",
  "what do I know about X", "connect ideas about X", "cross-domain analysis of X",
  "map everything in the vault about X". Searches comprehensively, surfaces
  non-obvious patterns and tensions, then challenges the user to generate
  original thought. The vault should surprise you — if synthesis only confirms
  what you already think, it failed.
argument-hint: "<topic>"
allowed-tools: Bash, Read, Grep, Glob, mcp__obsidian-vault__search_notes, mcp__obsidian-vault__read_note, mcp__obsidian-vault__read_multiple_notes, mcp__obsidian-vault__write_note, mcp__obsidian-vault__update_frontmatter
---

<Purpose>
Exhaust the vault's knowledge on a topic — across ALL domains — then act as
Luhmann's communication partner: surface contradictions the user hasn't noticed,
identify the hidden principle generalizing across examples, and demand original
synthesis. This is not a retrieval tool. It is a thinking provocation.

Science grounding: far transfer (Tempel & Frings 2024), generation effect
(McCurdy et al. 2020), elaborative interrogation, desirable difficulty
(Bjork & Bjork 2020).
</Purpose>

<Use_When>
- User wants to understand what the vault collectively says about a concept
- User is writing a Thought note and wants to pressure-test an idea
- User is preparing a talk, essay, or decision and needs cross-domain ammunition
- User says "synthesize X", "what do I know about X", "connect ideas about X"
- User wants to find contradictions or gaps in their own thinking
</Use_When>

<Do_Not_Use_When>
- User wants to process a single source note — use /process instead
- User wants spaced repetition review — use /recall instead
- User has a specific paper to analyze — use /paper instead
- Topic is too narrow to generate cross-domain connections (single paper, single event)
</Do_Not_Use_When>

<Steps>

## Stage 1: PARSE THE TOPIC

Extract the core concept(s) from the user's input. Identify:
- **Primary term**: the exact word(s) to search (e.g., "attention", "loss aversion")
- **Synonyms / adjacent**: related terms likely to appear in notes (e.g., "focus", "salience", "bias")
- **Domain anchors**: which domains likely hold relevant notes (ML, psychology, design, startup...)

If the topic is ambiguous, briefly clarify before searching (one question max).

## Stage 2: PARALLEL SEARCH — run ALL of these simultaneously

**MCP search (preferred):**
```
search_notes(query="PRIMARY TERM", limit=30)
search_notes(query="SYNONYM 1", limit=15)
search_notes(query="SYNONYM 2", limit=15)
```

**Grep fallback (if MCP unavailable):**
```
Grep(pattern="PRIMARY TERM", path="notes/", glob="*.md", output_mode="files_with_matches")
Grep(pattern="#TAG-NAME", path="notes/", glob="*.md", output_mode="files_with_matches")
Grep(pattern="\[\[.*PRIMARY TERM.*\]\]", path="notes/", glob="*.md", output_mode="files_with_matches")
```

**Also search:**
- Thought notes referencing this topic: `Grep(pattern="PRIMARY TERM", path="notes/thoughts/", glob="*.md")`
- Cross-domain appearances: search each domain folder separately to surface unexpected hits
- Existing Term notes: `Grep(pattern="type: term", path="notes/", glob="*.md")` then filter

Collect all matching file paths. Deduplicate. Aim for 15–25 notes across diverse domains.

## Stage 3: READ THE NOTES

Read up to 20 most relevant notes using `read_multiple_notes` or individual `read_note` calls.

Prioritize:
1. Thought notes (user's own synthesis — highest signal)
2. Term/Note notes (distilled concepts)
3. Paper/book/post notes with substantial content
4. Notes from UNEXPECTED domains (highest cross-domain value)

While reading, track:
- Key claims and insights
- Domain of each note
- Wikilinks that connect to the topic
- Any explicit contradictions or tensions
- Claims that could conflict with each other

## Stage 4: PRESENT THE SYNTHESIS

Output this structure (adapt headings as needed, cut any section with nothing real to say):

---

## What the vault says about [TOPIC]

### Key insights
[3–6 bullets. Each = one non-obvious claim distilled from multiple notes. Lead with the sharpest insight. No filler.]

### Cross-domain appearances
[Table or bullet list: Domain → how the concept appears there. Include only non-obvious mappings — skip domains where the concept is trivially expected.]

| Domain | How [topic] appears |
|--------|---------------------|
| [domain] | [specific claim from that note] |

### Agreements
[What multiple notes converge on — the vault's "consensus". 2–4 bullets max.]

### Tensions & contradictions
[Where notes disagree — including tensions the user may not have noticed. THIS IS THE MOST VALUABLE SECTION. If two notes from different domains make opposing claims, surface it explicitly. Quote the note titles.]

### Gaps
[What's missing: questions the vault raises but doesn't answer, adjacent concepts not yet captured, domains that probably have something to say but no notes exist]

---

## Stage 5: CHALLENGE QUESTIONS — do NOT skip, do NOT soften

Ask 3–4 questions. Make them uncomfortable. Reference the user's OWN notes by name.

Rules for good challenge questions:
- Anchor in specific vault evidence: "Your note [[(Thought) X]] claims Y, but [[(Paper) Z]] shows the opposite — which do you actually believe?"
- Force abstraction: "These 4 examples from different domains all share [pattern]. Is there a general principle here that deserves its own Term note?"
- Force disagreement: "What would someone who thinks [vault consensus claim] is WRONG say? Do you have any evidence for their view?"
- Force transfer: "You have strong notes on [concept A] and [concept B]. How does [concept A] change your understanding of [concept B]?"

**Wait for user responses before proceeding to Stage 6.**

The vault should not just confirm what you know. If the synthesis has no tension and no surprises, say so explicitly: "I found strong consensus but no real tension — either the topic is genuinely settled, or the vault has a blind spot here."

## Stage 6: HELP CREATE OUTPUT (only if something emerged)

### If a new Thought emerged from the conversation:

Help the user create a Thought note. Do NOT write it for them — Thoughts are where human understanding lives. Instead:
1. Ask: "What's the single sentence that captures the insight?"
2. Offer to create the note structure, leaving the content for them to fill
3. Generate the frontmatter + skeleton only

Thought note template:
```markdown
---
id: YYYYMMDDHHMMSS
created_date: YYYY-MM-DD
updated_date: YYYY-MM-DD
type: thought
processing_status: processed
---

# (Thought) [Title]
- **🏷️Tags** : #thought #[topic-tag] #MM-YYYY

[ ](#anki-card)

## Notes
[User fills this]

## Links
- [[(Type) Source Note 1]]
- [[(Type) Source Note 2]]
```

### If a new Term should be extracted:

Only propose this if the concept appeared across multiple notes but has no dedicated Term note. Create the Term note with:

```markdown
---
id: YYYYMMDDHHMMSS
created_date: YYYY-MM-DD
updated_date: YYYY-MM-DD
type: term
processing_status: processed
---

# (Term) [Concept Name]
- **🏷️Tags** : #term #all-anki #[topic-tag] #MM-YYYY

[ ](#anki-card)

## Notes
[Distilled definition — Feynman-style: intuition first, formalism second]

- [Key insight 1]
- [Key insight 2]
- **Example**: [concrete example]
- **Cross-domain**: [where else this appears]

## Links
- [[(Type) Source 1]]
```

### Wikilink rule (always):
Every internal reference must use the full filename stem including `(Type)` prefix:
- Correct: `[[(Thought) My insight note]]`
- Wrong: `[[My insight note]]`

If unsure of the exact filename, search before linking.

</Steps>

<Examples>

<Good>
User: "synthesize everything about attention mechanisms"
→ Search returns: 3 ML papers on attention, 1 psychology note on selective attention,
  1 design note on visual hierarchy, 1 thought note on "attention as resource allocation"
→ Cross-domain: ML attention ≠ psychological attention — but both involve a scoring
  function that weights inputs. Surface this non-obvious parallel.
→ Tension: vault's ML notes say "attention is O(n²)" (a problem), but the thought note
  says "the bottleneck IS the feature" — unresolved.
→ Challenge: "Your [[(Thought) Attention as resource allocation]] treats attention as
  scarce. But transformers have unlimited heads. Does scarcity still apply? What breaks?"
</Good>

<Good>
User: "what do I know about loss aversion"
→ Search finds notes in: psychology, behavioral economics, startup, design (dark patterns)
→ Agreements: loss aversion is asymmetric (losses hurt ~2x more than gains)
→ Gap: no notes on whether loss aversion weakens with experience/expertise — ask if worth capturing
→ Challenge: "You have [[(Paper) Prospect Theory]] and [[(Post) Pricing psychology]].
  Your startup notes apply this to pricing, but never to hiring. Where else in
  the vault could loss aversion explain something you attributed to something else?"
</Good>

<Bad>
User: "synthesize ML"
→ Too broad — ask: "ML is too wide to synthesize well. What angle?
  Scaling, optimization, architectures, learning theory, RL...?"
</Bad>

<Bad>
Synthesis that produces no tension:
→ "Everything agrees that attention is useful." — This is not synthesis. Push harder:
  find the domains that don't agree, find the edge cases, find what the vault hasn't said.
</Bad>

</Examples>

<Escalation_And_Stop_Conditions>
- **Too few notes** (< 3 relevant): Say so — "The vault is thin on this topic. Suggest reading X or running /paper-discover to build coverage."
- **Topic too broad**: Ask user to narrow. One clarifying question, not a list.
- **Only one domain represented**: Flag it — "All your notes on this come from ML. This might be a blind spot. Want me to /paper-discover adjacent psychology or design literature?"
- **No tension found**: Report honestly. Don't manufacture fake contradictions.
- **User disagrees with a challenge question**: Engage — don't retreat. The job is productive friction.
- **User wants to skip challenge questions**: Gently push back once. "The questions are the point — skip them and you're just reading an index." Then respect their choice.
</Escalation_And_Stop_Conditions>

$ARGUMENTS
