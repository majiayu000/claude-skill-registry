---
name: context-dump
description: Create or update a task context dump document by scanning existing content and appending only new, non-duplicative progress. Use only when the user explicitly requests a context dump, handoff note, or progress log to be written into a document.
---

# Context Dump

## Overview

Capture the current task state into a document by scanning existing notes and appending only new progress without duplication. Always confirm whether the user wants to create a new document or update an existing one before writing.

## Workflow

### 1) Confirm target document
- Ask: "Do you want to create a new document or update an existing one?"
- If updating, ask for the exact path or search criteria.
- If creating, ask for the filename/path and preferred location.

### 2) Locate and read existing content (update only)
- Find the document with `rg --files` and/or `rg -n` based on user-provided hints.
- Read relevant sections to avoid duplicating existing content.
- Identify the best insertion point (e.g., “Progress Notes”, “Updates”, or append at end).

### 3) Draft new material (non-duplicate only)
- Summarize new progress since the last update.
- Do not repeat items already present; only add deltas.
- Use concise bullet lists and clear dates when helpful.

### 4) Write updates
- Use `apply_patch` to update existing documents.
- If creating a new document, write a minimal template:
  - Title
  - Date
  - Summary
  - Progress / Changes
  - Open Questions / Risks
  - Next Steps

## Guardrails

- Trigger this skill only when the user explicitly asks for a context dump / handoff / progress log.
- Always ask whether to create a new document or update an existing one.
- Do not duplicate existing information; add only new or changed items.
- Keep updates terse and structured for handoff.
