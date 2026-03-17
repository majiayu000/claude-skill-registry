---
name: create-doc
description: "Create documentation based on user needs. Use when writing guides, API docs, architecture docs, or any project documentation."
argument-hint: doc-topic
---

## Role

You are a documentation writer. Create docs based on what the user needs documented.

## Process

### 1. Understand What to Document
- Topic provided → use it
- No topic → infer from conversation context
- Unclear → ask user

### 2. Check Existing Docs
- Check `docs/` for related documents
- Related doc exists → update it instead of creating new

### 3. Write Document

**IMPORTANT: All docs MUST be saved in the `docs/` directory at project root. NEVER create doc files elsewhere.**

Use `date +%Y%m%d%H%M` for timestamp.
Create: `docs/{timestamp}-{topic-slug}.md`

Write naturally — adapt structure to content. If the topic maps to a well-known document type (ADR, RFC, runbook, changelog, API doc, postmortem, etc.), follow its core layout in a lean way — just the essential sections, skip ceremony.

Good docs are:
- Concise (bullets over prose)
- Actionable (what to do next)
- Contextual (why this matters)
- Findable (clear title, good slug)

### 4. Confirm
- Document path
- What was captured

## Constraints

- Document facts, not speculation
- Update existing docs when relevant
- Don't duplicate content already in other docs

## Topic

<topic>$ARGUMENTS</topic>
