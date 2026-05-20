---
name: keine-chat
description: >
  Use this skill whenever the user wants to discuss, explore, or ask questions about a topic using
  the local knowledge base as grounding. Trigger on phrases like "what do you know about X",
  "let's talk about X", "explain X", "I'm trying to understand X", "discuss X with me", "what does
  the KB have on X", "help me think through X", "tell me about X", or any conversational question
  about a concept or idea. Also trigger when the user asks a question that could be answered from
  stored knowledge, even if they don't explicitly say "knowledge base". This is the default skill
  for knowledge-grounded conversation — prefer it over answering from memory alone whenever the KB
  might have relevant content. Do NOT trigger for: deep research reports (use keine-research),
  adding new entries (use keine-update-entries), or creating maps (use keine-update-maps).
---

# Keine Chat

A conversational skill for exploring ideas and answering questions using the local knowledge base.
The KB is the primary source of truth — answer from it, be honest about its limits, and offer to
fill gaps with web research when the user wants more.

## Mindset

This is a conversation, not a report. Stay concise and direct. The goal is to give the user
a grounded, honest answer — citing what the KB actually says, noting what it doesn't cover, and
offering to go further if they want.

---

## Workflow

### Step 1 — Understand the question

Before searching, make sure you understand what the user actually wants:
- Is this a factual lookup ("what is X"), conceptual exploration ("how does X relate to Y"), or
  open-ended discussion ("let's think through X")?
- What level of depth does the user seem to want? Match your answer to their tone.

If the question is ambiguous, make a reasonable interpretation and proceed — you can clarify inline
as you answer.

### Step 2 — Mine the knowledge base

Search efficiently. Start broad, narrow as needed:

```sh
# Check for relevant topic maps (fastest orientation)
ls docs/maps/

# Check tags for the topic area
ls docs/tags/

# Full-text search for keywords
grep -ri "keyword" docs/ -l

# Read a tag index to find related entries
cat docs/tags/<slug>.md
```

Read the most relevant files. For a focused question, 2–5 entries is usually enough. For a broad
topic, read the map file first — it gives the quickest overview and links to key entries.

As you read, track:
- What the KB covers (and how well)
- What it's silent on or only partially covers
- Any tensions or interesting connections across entries

### Step 3 — Answer from the KB

Compose your answer from what you found. Keep it conversational:

- Lead with the most relevant content, not with a preamble about what you searched
- Cite entries where they add credibility: "According to [entry title](path/to/entry.md), ..."
- Be honest about gaps: "The KB doesn't cover X directly, but based on Y..."
- If the topic has a map, mention it for further reading

**Don't pad.** A sharp 3-paragraph answer is better than a bloated 10-paragraph one. If the KB
has a lot of depth, offer to go deeper on a specific facet rather than dumping everything at once.

### Step 4 — Surface gaps and offer to enrich

After answering, briefly note what's missing if it's relevant to the user's question:

> "The KB doesn't have much on [aspect]. Want me to search the web and add entries for it?"

Only offer this when the gap is meaningful. Don't prompt for web research if the KB already
answered the question well.

If the user says yes, move to Step 5.

### Step 5 — Web research and KB enrichment (only if user approves)

Search the web to fill the gaps. For each significant finding:

1. Use `keine-update-entries` to create a new KB entry if the knowledge is worth keeping
2. If several new entries form a coherent topic, consider updating or creating a map with
   `keine-update-maps`
3. After creating entries, run tag maintenance `scripts/maintain_tags.py`
4. Then return to the conversation and incorporate the new knowledge into your answer

Commit new entries:
```sh
git add docs/ docs/tags/
git commit -m "docs: add <topic>"
```

---

## Tone and format

- **Conversational**: write like you're talking to someone, not filing a report
- **Grounded**: tie claims to KB entries where possible; don't invent facts
- **Honest**: "the KB doesn't cover this" is a better answer than a vague non-answer
- **Proportionate**: match response length to the question's complexity
- **Invite dialogue**: end with a follow-up question or offer to go deeper if the topic warrants it

## What this skill is NOT for

- **Deep research reports** → use `keine-research` (heavyweight, multi-phase, produces a file in `reports/`)
- **Adding a specific document or URL** → use `keine-update-entries`
- **Creating or editing a topic map** → use `keine-update-maps`
- **Answering from memory without KB grounding** → just answer directly without this skill
