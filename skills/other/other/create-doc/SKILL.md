---
name: create-doc
description: "Use when the user wants to save knowledge as a file so others don't have to rediscover it — \"turn this into a doc\", \"write this up\", \"document how X works\", \"we figured this out and want to capture it\", \"nobody should have to figure this out again\". Covers any request to create or update durable written artifacts: onboarding guides, runbooks, ADRs, API docs, architecture notes, postmortems, changelogs, setup guides. The trigger: user wants knowledge captured in a file for future reference, not just a conversation. Do NOT use when still making decisions (→ give-plan), just asking for explanation without a file (→ ask), or writing code (→ cook)."
argument-hint: doc-topic
---

ultrathink

## Process

Check conversation context and skip completed steps.

### 1. Identify the doc job
Figure out the document type, audience, purpose, whether to update an existing doc or create new, and what source material it draws from. If any of these would materially change the output and are unclear, ask.

If the request is still evaluating options, stop and discuss — drafting docs before a decision is made locks in the wrong answer.

If the doc type is a recognized structured format (runbook, ADR, postmortem, onboarding guide, API/architecture doc), read `references/doc-types.md` now — it has the required sections for each type.

### 2. Ground in evidence
Before writing factual claims, read relevant sources — existing docs, code, config, tickets, PRs, prior discussion. Don't present guesses as fact. Label uncertain details explicitly, or collect them in an "Open questions" section rather than hedging every sentence.

### 3. Choose destination
Prefer updating the canonical existing doc when one exists.

For new documents, MUST default to `docs/` at the repo root (create it if missing). Only deviate when:
- A more specific existing doc home clearly fits (ADR directory, changelog, README section, established project docs tree) — use it
- The repo already follows a convention of keeping docs next to the code they explain — match that
- The doc is event-like (postmortem, incident note) — use a timestamped filename

When you need a fresh timestamp, use `date +%Y%m%d%H%M%S`.

### 4. Outline first when substantial
For large or structurally ambiguous docs, propose a title and section outline before drafting. For small or routine docs, write directly.

### 5. Write the artifact
Write the file at the path from Step 3 — don't paste in chat without creating the file. Adapt structure to the document type (ADRs, runbooks, postmortems, API docs, etc.) and include only sections that earn their keep.

A strong document is accurate, concise, audience-aware, scannable, explicit about *why* something matters, and clear about what is current behavior vs. decision vs. open question. Write for the intended reader, not for completeness theater. Prefer concrete repo-specific details over generic filler. When sources conflict, name the conflict instead of quietly picking one.

### 6. Report and stop
Report the path, whether you updated or created, what was captured, and any assumptions or gaps. Do not drift into implementation unless explicitly asked.

## Topic

<topic>$ARGUMENTS</topic>
