---
name: recall
description: >-
  Spaced repetition and retrieval practice engine for the vault. Use when the
  user wants a review session, recall practice, to test what they remember,
  or to resurface notes. Triggers on "review session", "what should I review",
  "recall practice", "resurface notes", "spaced repetition", "quiz me",
  "what do I know about", "inbox triage", "surprise connection".
allowed-tools: Bash, Read, Edit, Grep, Glob, mcp__obsidian-vault__search_notes, mcp__obsidian-vault__read_note, mcp__obsidian-vault__get_frontmatter, mcp__obsidian-vault__get_notes_info, mcp__obsidian-vault__update_frontmatter
argument-hint: "[number of cards, default 5]"
---

<Purpose>
Run an interactive spaced repetition session: build a mixed queue of retrieval
practice cards, inbox triage items, and a surprise cross-domain connection.
For each card, show only the title first — forcing recall before revealing
content (retrieval practice). Interleave domains to exploit the spacing and
interleaving effects. Surface a non-obvious connection the user hasn't made yet.
</Purpose>

<Use_When>
- User wants a review session ("what should I review?", "quiz me", "recall practice")
- User wants to resurface notes they haven't seen in a while
- User wants to triage their inbox
- User wants to discover connections across domains
- User asks "what do I remember about X?"
- Periodic knowledge maintenance (daily, weekly reviews)
</Use_When>

<Do_Not_Use_When>
- User wants to deeply process a specific note (use /process)
- User wants vault structure analysis (use /vault-graph)
- User wants to synthesize across a cluster (use /synthesize)
- User is actively reading or adding a new source note
</Do_Not_Use_When>

<Execution_Policy>
- INTERACTIVE — never skip ahead. Each card requires the user to respond before
  the answer is shown. The friction IS the learning.
- Never show note content before the user attempts recall
- Prefer notes with updated_date older than 14 days (spacing effect)
- MUST interleave domains — draw from at least 3 different topic folders
- Use MCP tools (search_notes, get_frontmatter) when available; fall back to Grep/Glob
- Session size: default 5 retrieval cards, 2 inbox items, 1 surprise connection
  (adjust to user's argument if provided)
- After each reveal, offer to update the note if it's stale
</Execution_Policy>

<Steps>

## Stage 1: BUILD THE QUEUE

### 1a. Retrieval Practice Cards (default 3–5)

Candidate selection using MCP:
```
search_notes(query="processing_status: processed OR processing_status: evergreen", limit=50)
search_notes(query="type: term OR type: note", limit=50)
```

Or fall back to Grep:
```
Grep(pattern="processing_status: (processed|evergreen)", path="notes/", glob="*.md")
Grep(pattern="^type: (term|note)$", path="notes/", glob="*.md")
```

Filter and rank candidates:
1. Prefer notes with `updated_date` older than 14 days — compute from today (2026-03-20)
2. Prefer notes with the `[ ](#anki-card)` anchor (marked for spaced repetition)
3. Prefer notes with `processing_status: processed` over `evergreen`
   (evergreen notes are maintained; processed ones need re-testing)
4. **Enforce domain interleaving**: collect the topic folder for each candidate
   (`notes/ml/`, `notes/psychology/`, `notes/startup/`, etc.) and ensure the
   final selection spans at least 3 different folders
5. If fewer than 3 domains are available, accept 2 minimum

Read the frontmatter to confirm `updated_date` and `type`:
```
get_frontmatter(path="notes/PATH/filename.md")
```

### 1b. Inbox Triage Items (1–2)

Find the oldest unprocessed source notes:
```
search_notes(query="processing_status: inbox", limit=20)
```
Or:
```
Grep(pattern="processing_status: inbox", path="notes/", glob="*.md")
```

Filter to types: `paper`, `post`, `book`, `lecture`, `course`.
Sort by `created_date` ascending — oldest first.
Pick 1–2.

### 1c. Surprise Connection (1)

Goal: find two notes from DIFFERENT domain folders that share a concept keyword
but have NO wikilink between them.

Algorithm:
1. Pick a retrieval card already in the queue (it has topic keywords in its body)
2. Extract 2–3 key concept words from that note's title or content
3. Search a DIFFERENT domain folder for notes containing those keywords:
   ```
   Grep(pattern="KEYWORD", path="notes/OTHER_DOMAIN/", glob="*.md")
   ```
4. Check that the two notes do NOT link to each other:
   ```
   Grep(pattern="\\[\\[.*TITLE.*\\]\\]", path="notes/SOURCE_NOTE.md")
   ```
5. If no match, try a second keyword or a second candidate note
6. Present both notes with the shared concept as the "bridge"

Non-obvious pairings to prioritize (cross-domain > within-domain):
- ml/ ↔ psychology/ (learning algorithms ↔ cognitive science)
- startup/ ↔ design/ (product strategy ↔ UX)
- finance/ ↔ ml/ (optimization ↔ market dynamics)
- psychology/ ↔ startup/ (behavioral economics ↔ business)
- computer science/ ↔ logic/ (formal systems ↔ reasoning)

## Stage 2: PRESENT QUEUE OVERVIEW

Before starting, show the session plan:

```
Review session — [N] cards queued

Retrieval practice ([count]):
  1. [Note title] — [domain]
  2. [Note title] — [domain]
  ...

Inbox triage ([count]):
  • [Note title] ([type], [age] days old)
  ...

Surprise connection: [teaser — e.g., "a bridge between ML and psychology"]

Ready? I'll show you one card at a time. Type anything to start, or "skip [N]"
to skip a card.
```

## Stage 3: RUN THE SESSION

### For each retrieval practice card:

**Turn 1 — Prompt recall:**
```
─────────────────────────────────────
Card [N/total] · [domain folder]

[[ (Type) Note Title ]]

What do you remember about this concept?
(Type your answer, or "skip" to reveal)
─────────────────────────────────────
```

Wait for user response.

**Turn 2 — Reveal:**
Read the full note content:
```
read_note(path="notes/PATH/filename.md")
```
Or: `Read(file_path="/absolute/path/to/note.md")`

Show the note content (truncate at 400 words if very long — show key sections).

Then ask:
```
How did you do? Is this note still accurate?
[u] Update note  [n] Next card  [e] Evergreen (promote status)
```

If user wants to update: help them edit inline, then update `updated_date`
in frontmatter using `update_frontmatter`.

If user types "e" or "evergreen": update `processing_status` to `evergreen`.

### For each inbox triage item:

```
─────────────────────────────────────
Inbox triage · [type] · [age] days old

[[ (Type) Note Title ]]
```

Read the note, show the first 5–7 bullets (or Abstract section for papers).

Then ask:
```
Worth processing deeply, or archive?
[p] Process (I'll run /process next)  [a] Archive  [s] Skip for now
```

- `p` → note it as a recommendation; optionally update `processing_status: processing`
- `a` → update `processing_status: archived`
- `s` → leave unchanged

### For the surprise connection:

```
─────────────────────────────────────
Surprise connection

These two notes share the concept "[KEYWORD]" but don't link to each other:

[[ (Type) Note A ]] (domain: X)
[[ (Type) Note B ]] (domain: Y)

[Brief excerpt from each showing the shared concept]

Do you see a meaningful connection? What would the link say?
─────────────────────────────────────
```

Wait for user response. If they see a connection:
- Help them decide which note gets the wikilink (or both)
- Offer to add the link: `[[  (Type) Note B  ]]` into Note A's Related links section
- Update `updated_date` on both notes

## Stage 4: SESSION SUMMARY

```
─────────────────────────────────────
Session complete

Reviewed: [N] cards
Updated: [N] notes
Promoted to evergreen: [list]
Archived: [list]
Queued for /process: [list]
New connections made: [count]

Oldest unreviewed term: [title] ([N] days)
─────────────────────────────────────
```

Optionally suggest: "Run /process on [oldest inbox item] next."

</Steps>

<Examples>
<Good>
User: "review session"
1. Build queue: 4 term notes (ml/, psychology/, startup/, finance/), 2 inbox papers, 1 surprise
2. Show overview → user starts
3. Card 1: "[[  (Term) Attention Mechanism  ]]" — user recalls, sees note, updates a stale bullet
4. Card 2: "[[  (Term) Loss Aversion  ]]" — user blanks, reads note, promotes to evergreen
5. Inbox: "(Paper) Chinchilla Scaling Laws" — 60 days old → user says archive
6. Surprise: "(Term) Gradient Descent" ↔ "(Term) Operant Conditioning" — shared keyword "reward signal"
   → user says "oh, both use incremental feedback to converge on a target behavior" → adds link
7. Summary: 6 reviewed, 2 updated, 1 evergreen, 1 archived, 1 connection made
</Good>

<Good>
User: "quiz me on 3 cards"
→ Session with 3 retrieval cards (not 5), 1 inbox item, 1 surprise connection
</Good>

<Bad>
Showing note content immediately without prompting recall first.
→ This destroys the retrieval practice effect. ALWAYS show title first, wait for response.
</Bad>

<Bad>
Picking 4 cards all from notes/ml/.
→ Violates interleaving. Domains must be mixed. If ml/ only has enough candidates,
   pull from any other folder before repeating a domain.
</Bad>
</Examples>

<Escalation_And_Stop_Conditions>
- **Not enough processed notes** (<3): Inform user, offer to run /process first on top inbox items
- **All notes recently reviewed** (updated within 7 days): Report "vault is fresh — nothing due for spacing"
- **No inbox items**: Skip inbox triage stage, replace with an extra retrieval card
- **Surprise connection not found after 3 attempts**: Skip it, note "no unlinked cross-domain pairs found today"
- **User types "stop" or "quit"**: End session immediately, show partial summary
- **MCP unavailable**: Fall back to Grep/Glob for all searches; behavior is identical
</Escalation_And_Stop_Conditions>

$ARGUMENTS
