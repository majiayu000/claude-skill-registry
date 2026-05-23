---
name: digest-this
description: "Digests any long, dense, or complex content — documents, PDFs, transcripts, long messages — into a short, low cognitive load summary. Use this skill whenever someone pastes in something long, sends a wall of text, or needs to understand something quickly without reading it in full. Always produces short, scannable output regardless of how long the input is. Use proactively when content is long or complex even if the user hasn't explicitly asked for a digest."
---

# Digest This

A skill that sits between you and long or complex content, making it accessible without losing what matters.

This skill does one thing: takes something long, dense, or hard to read and turns it into something short, clear, and scannable. The output is always brief regardless of how long the input is. A ten page document and a long email get the same treatment — a short, structured summary the user can actually absorb.

---

## What Makes This Different From a Standard Summary

Claude's default behaviour is to produce summaries proportional to the input — long document, long summary. This skill enforces the opposite. The output is always short. Always structured. Never a wall of text.

It also asks one question before acting, so the output is shaped around what the user actually needs rather than what Claude assumes they need. And it produces the same reliable format every time, regardless of how the user asks.

---

## When to Apply

**Apply automatically when:**
- The user pastes in a long block of text, document, transcript, or message
- The content is clearly longer than the user needs to read in full
- The user says things like "what does this say", "can you summarise this", "digest this", "what's this about", "too long didn't read", or "tldr"

**Apply on manual trigger with `/digest-this`**

**Do not apply when:**
- The content is already short and clear
- The user is asking a specific question about the content rather than wanting a summary
- The user wants to discuss or analyse the content in depth rather than get a quick digest

---

## Core Principles

**Always short**
The output must be short regardless of input length. This is non-negotiable. A one page document and a fifty page report both get a short digest. If the user needs more depth they can ask.

**Scannable over readable**
Structure matters more than prose. Use headings, short bullets, and white space. A user should be able to get the key information in under sixty seconds without reading every word.

**Never add interpretation**
Only report what is in the content. Do not add opinions, caveats, or background knowledge. The user is digesting what was sent to them, not getting Claude's view on it.

**Preserve important specifics**
Numbers, dates, names, deadlines, and decisions should survive the digest intact. Everything else can be compressed.

**One question, then act**
Ask one low-effort question before producing the digest. If the user does not answer or just says "digest this" with no context, default to the gist — a plain English summary of what the content is saying and any actions it contains.

---

## Step 1 — Receive the Content

Accept whatever is pasted or shared. This includes:
- Pasted text of any length
- PDF content
- Email chains or messages
- Transcripts
- Reports or documents
- Any other long form written content

Do not comment on the length or complexity of what has been shared. Just proceed.

---

## Step 2 — Ask One Question

Before producing any output, ask:

> "What do you need from this — the gist, the key points, any actions, or an explanation of something specific?"

Present these as clear options:
- **Gist** — plain English summary of what this is saying
- **Key points** — the most important information, bulleted
- **Actions** — what this is asking you to do
- **Explain** — break down something complex or unclear

If the user does not respond to the question, or says something like "just digest it" or "surprise me" — default to **gist plus any actions** and proceed without asking again.

Only ask this one question. Do not ask about the content itself, do not ask for clarification on what was shared.

---

## Step 3 — Produce the Digest

### Gist

```
## What this is saying
[2–3 sentences maximum. Plain English. No jargon. What is the core message?]

## Actions (if any)
- [Action 1]
- [Action 2]

## Worth noting
- [Any date, deadline, name, or number that matters]
```

### Key Points

```
## Key points
- [Point 1 — one line]
- [Point 2 — one line]
- [Point 3 — one line]
- [Point 4 — one line]
- [Point 5 — one line]

## Actions (if any)
- [Action 1]

## Worth noting
- [Any date, deadline, name, or number that matters]
```

Maximum five key points. If there are more than five important things, pick the five most important. The user can ask for more if needed.

### Actions

```
## What this is asking you to do
1. [Action — specific and plain]
2. [Action — specific and plain]
3. [Action — specific and plain]

## By when (if mentioned)
- [Deadline or date if present]

## Context
[One sentence of context if needed to make the actions make sense]
```

### Explain

If the user selects Explain but has not specified what they want explained, ask one short follow-up before proceeding:

> "What specifically do you want me to break down?"

Present 3–4 options drawn directly from the content — not generic options, but the actual topics in the document. Then wait for the answer before producing any output.

This is the only exception to the one question rule. Explain mode requires a target.

```
## What this means in plain English
[Short explanation of the complex part — 3–5 sentences maximum]

## The simple version
[One sentence. If you had to explain this to someone in thirty seconds, what would you say?]

## What it means for you (if relevant)
[One or two lines on implications if they are clear from the content]
```

---

## Output Rules — Apply to All Modes

- **Never exceed one screen of output** — if it does not fit on one screen it is too long
- **No preamble** — do not say "here is your digest" or "I have summarised this for you" — just produce the output
- **No commentary on the original** — do not say "this is a well written document" or "this email is quite complex"
- **Preserve the user's language where possible** — if the content uses specific terms the user will recognise, keep them
- **Bold only what is critical** — a date, a deadline, a decision. Do not bold for decoration

---

## Closing Line

After the digest, end with one short line offering to go deeper if needed:

> "Want me to go deeper on any part of this, or is that enough to work with?"

One line only. Do not list everything Claude could do next.

---

## What This Skill Does Not Do

This skill does not analyse, critique, or offer opinions on the content. It does not help the user respond to the content — that is a separate task. It does not produce a long summary. If the user needs depth, they ask for it after receiving the digest.
