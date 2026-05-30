---
name: process
description: >-
  CORE learning workflow — use this whenever the user has a source note open
  (paper, post, book, lecture, course, clipping) and wants to extract knowledge,
  understand what they just read, or build it into their vault. Triggers on
  "process this note", "process this paper", "extract concepts", "what can I
  learn from this", "atomize this", "add this to my vault", "what's important
  here", or when the user shares a note and asks for help understanding it.
  Do NOT wait for an explicit /process command — if the user is engaging with a
  source note and wants to go deeper, this skill applies.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, mcp__obsidian-vault__search_notes, mcp__obsidian-vault__read_note, mcp__obsidian-vault__update_frontmatter, mcp__obsidian-vault__write_note, mcp__obsidian-vault__get_frontmatter
argument-hint: "(no args — reads current note context from user)"
---

<Purpose>
Extract knowledge from a source note into the vault's permanent knowledge base.
Implements three evidence-backed learning principles:
- **Generation effect**: writing from memory > copying (McCurdy et al. 2020)
- **Elaborative interrogation**: explaining WHY deepens retention
- **Cross-domain transfer**: explicit abstraction is what moves knowledge across fields

This skill is INTERACTIVE by design. The desirable-difficulty questions in Stage 3
are not optional ceremony — the friction IS the learning. The user's answers shape
what gets extracted and how.
</Purpose>

<Use_When>
- User has a source note (paper, post, book, lecture, course, clipping) to process
- User wants to extract concepts into Term or Note entries
- User asks what's important in something they've read
- User wants to build wikilink connections from a note into the rest of the vault
- User says "process this", "atomize this", "extract concepts", "what did I learn"
</Use_When>

<Do_Not_Use_When>
- User wants to find new papers on a topic (use /paper-discover)
- User wants web research on something new (use /research)
- User wants to synthesize ACROSS multiple existing vault notes (use /synthesize)
- The note is already a Term, Note, or Thought (not a source note)
</Do_Not_Use_When>

<Steps>

## Stage 1: READ THE SOURCE NOTE

Ask the user which note to process if it's not clear from context. Then read it.

Verify the note type is a source type: `paper`, `post`, `book`, `lecture`,
`course`, or a Clipping. If the note is a Term, Note, or Thought, stop and
explain why this workflow doesn't apply.

Read the frontmatter and body:
```
mcp__obsidian-vault__read_note(path="path/to/note.md")
```

Or if MCP is unavailable:
```
Read("/absolute/path/to/note.md")
```

## Stage 2: MARK AS PROCESSING

Update frontmatter to signal active work:
```
mcp__obsidian-vault__update_frontmatter(
  path="path/to/note.md",
  updates={"processing_status": "processing", "updated_date": "YYYY-MM-DD"}
)
```

## Stage 3: ASK DESIRABLE-DIFFICULTY QUESTIONS

**Do NOT skip this stage.** Present these three questions and wait for the user's answers before proceeding:

---
**Q1.** In one sentence — what is the single most important idea in this note?
*(Don't look at the note. Reconstruct it from memory. That struggle is the point.)*

**Q2.** How does this connect to something you already know? Name a specific vault note, or a concept from a completely different domain.

**Q3.** What surprised you, or pushed back against something you already believed?

---

Wait for the user's responses. Their answers determine:
- Which concepts are worth extracting (Q1 focus)
- Which wikilinks to create (Q2 connections)
- Where the note's real epistemic value lives (Q3 surprises)

If the user skips a question or gives a short answer, acknowledge it and move on — don't block the workflow.

## Stage 4: VAULT CONCEPT SCAN

Search the vault thoroughly for concepts mentioned in the note. Use multiple strategies:

**By keyword (MCP preferred):**
```
mcp__obsidian-vault__search_notes(query="CONCEPT NAME", limit=10)
```

**By keyword (Grep fallback):**
```
Grep(pattern="concept name", path="notes/", glob="*.md", output_mode="files_with_matches", head_limit=15)
```

**By type — check all Term notes in relevant domain:**
```
Grep(pattern="type: term", path="notes/ml/", glob="*.md", output_mode="files_with_matches")
```

For each key concept extracted from the note (aim for 5–12 concepts), classify it:

| Classification | Meaning | Action |
|---|---|---|
| **EXISTING** | Term/Note already in vault | Add [[wikilink]] to source note |
| **NEW TERM** | Atomic concept, one clear definition | Extract as new (Term) note |
| **NEW NOTE** | Multi-facet idea, needs more depth | Extract as new (Note) note |
| **SKIP** | Tangential, not reusable | Don't extract |

Search ACROSS domain folders — a psychology concept may already exist under
a different framing in notes/startup/ or notes/design/. Cross-domain matches
are the most valuable finds.

## Stage 5: PRESENT EXTRACTION PLAN

Present the plan clearly before creating anything:

```
## Existing concepts — add [[wikilinks]]
- [[(Term) Attention Mechanism]] — mention it in the Architecture section
- [[(Paper) Attention Is All You Need]] — link in Related links

## New concepts to extract
### 1. (Term) Flash Attention
- Type: Term
- Folder: notes/ml/
- Core idea: memory-efficient attention that avoids materializing the full N×N matrix
- Why it matters: enables training on longer sequences with same GPU budget
- Tags: #ml #attention #efficiency #MM-YYYY

### 2. (Note) IO-Aware Algorithm Design
- Type: Note (too broad for a Term)
- Folder: notes/computer science/
- Core idea: design algorithms around memory bandwidth, not just FLOPs
- Cross-domain angle: same principle appears in database query planning
- Tags: #systems #algorithms #MM-YYYY

## Questions this note raises
- Why doesn't standard PyTorch implement this by default?
- → Could become a (Question) note
```

Ask the user: "Which concepts should I create? (say 'all', list numbers, or
adjust the plan)"

## Stage 6: CREATE APPROVED NOTES

For each approved concept, create the note. Use this exact structure:

**For Term notes:**
```markdown
---
id: YYYYMMDDHHMMSS
type: term
processing_status: processed
created_date: YYYY-MM-DD
updated_date: YYYY-MM-DD
---

# Concept Name [ ](#anki-card)

- **🏷️Tags** : #term #all-anki #topic-tag #MM-YYYY

[One sentence that captures the core intuition — lead with WHY it matters, not just what it is]

- [Bullet 1: concrete mechanism or definition]
- [Bullet 2: why it matters, what problem it solves]
- [Bullet 3: concrete example — make it visualizable]
- [Bullet 4: cross-domain connection or counterintuitive angle]

## Related
- Source: [[(Type) Source Note Title]]
- [[(Term) Related Concept]]
```

**For Note entries (richer, multi-section):**
```markdown
---
id: YYYYMMDDHHMMSS
type: note
processing_status: processed
created_date: YYYY-MM-DD
updated_date: YYYY-MM-DD
---

# Concept Name

- **🏷️Tags** : #note #topic-tag #MM-YYYY

[ ](#anki-card)

[Lead insight — the one thing someone should remember]

## [Section 1]
- [bullets]

## [Section 2]
- [bullets]

## Related links
- Source: [[(Type) Source Note Title]]
- [[(Term) Related Concept]]
```

Generate the timestamp ID for each note:
```bash
date +%Y%m%d%H%M%S
```

Place notes in the appropriate subfolder under `notes/`. Match the domain:
- ML, AI → `notes/ml/`
- Papers → `notes/paper/` (or stay in the source's folder)
- Psychology, cognition → `notes/psychology/`
- Business, startups → `notes/startup/`
- CS, algorithms → `notes/computer science/`
- Original ideas → `notes/thoughts/`

**Quality gate before creating each note:**
- Does the first bullet lead with insight, not context?
- Is there at least one concrete example?
- Is there a cross-domain link (explicit or implicit)?
- Could you cut 20% and lose nothing? If yes, cut it.

## Stage 7: UPDATE THE SOURCE NOTE

After creating new notes, update the source note:

1. Add `[[wikilinks]]` inline where concepts are first mentioned — use the full
   `(Type) Title` prefix that matches the created filename exactly:
   - `[[(Term) Flash Attention]]` not `[[Flash Attention]]`
   - `[[(Note) IO-Aware Algorithm Design]]` not `[[IO-Aware]]`

2. Update frontmatter:
```
mcp__obsidian-vault__update_frontmatter(
  path="path/to/source-note.md",
  updates={"processing_status": "processed", "updated_date": "YYYY-MM-DD"}
)
```

3. Confirm with a brief summary:
```
Done. Created 3 notes, updated 2 wikilinks.

New notes:
- notes/ml/(Term) Flash Attention.md
- notes/computer science/(Note) IO-Aware Algorithm Design.md
- notes/ml/(Term) Tiling (GPU).md

Added wikilinks to source note for 5 concepts (2 existing, 3 new).

Cross-domain connection worth exploring:
- [[(Note) IO-Aware Algorithm Design]] ↔ database query planning (no vault note yet)
```

</Steps>

<Examples>
<Good>
User: "process this paper on Flash Attention"
1. Read note → confirmed type: paper, status: inbox
2. Mark → processing_status: processing
3. Questions → user answers: "main idea is recomputing activations to save memory",
   connects to "(Note) Memory Hierarchy", surprised that IO is the bottleneck not compute
4. Scan vault → finds (Term) Attention Mechanism (existing), (Term) Softmax (existing),
   no term for Flash Attention, no term for tiling
5. Plan → 3 new terms, 2 existing links, 1 question note candidate
6. Create → (Term) Flash Attention, (Term) Kernel Fusion, (Note) IO-Aware Algorithm Design
7. Update → adds 5 wikilinks to source note, marks processed
</Good>

<Good>
User: "what can I learn from this blog post?" (post about Stripe's pricing strategy)
1. Read → type: post, about willingness-to-pay segmentation
2. Questions → user: "main idea is pricing tiers create self-selection",
   connects to "(Term) Price Discrimination" already in vault
3. Scan vault → finds (Term) Price Discrimination, (Term) Bundling,
   nothing on willingness-to-pay metering
4. Plan → 1 new term (Metered Pricing), link to 2 existing terms
5. Create → (Term) Metered Pricing with cross-domain link to SaaS AND utility billing
6. Update → processed, 3 wikilinks added
</Good>

<Bad>
- Skipping Stage 3 questions and going straight to extraction — violates the
  generation effect principle; the user misses the retrieval practice
- Creating terms that are too broad: "(Term) Machine Learning" is not atomic
- Wikilinks without (Type) prefix: [[Flash Attention]] instead of [[(Term) Flash Attention]]
- Terms that transcribe the paper instead of synthesizing: quoting abstract bullets verbatim
- Leading with definition instead of insight: "Flash Attention is an algorithm that..."
  instead of "Attention's real bottleneck is memory bandwidth, not FLOPs — Flash Attention
  fixes this by never materializing the full N×N matrix"
</Bad>
</Examples>

<Escalation_And_Stop_Conditions>
- **Not a source note**: Tell the user this workflow is for source notes (paper, post, book,
  lecture, course, clipping). For Term/Note/Thought, suggest editing directly.
- **Note has no content yet**: Prompt the user to fill in the note before processing.
- **User skips all Stage 3 questions**: Proceed with extraction but note that retrieval
  practice was skipped — flag the concepts as lower-confidence extractions.
- **Concept already exists in vault as a Term**: Don't duplicate — add a wikilink and
  optionally suggest enriching the existing term.
- **Too many concepts (15+)**: Present the plan in priority order; ask user to triage
  rather than extracting everything.
</Escalation_And_Stop_Conditions>

$ARGUMENTS
