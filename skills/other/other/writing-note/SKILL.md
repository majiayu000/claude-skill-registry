---
name: writing-note
description: >-
  Use this skill to read, write, search, or modify files in the user's local
  Obsidian vault (markdown notes). This is the user's personal knowledge base
  stored as local files. Trigger whenever the request involves personal notes —
  including "save this to my notes", "幫我記", "幫我存", "daily note", "筆記",
  "幫我找...筆記", "我之前有存", "更新筆記", "meeting note", "project note", or
  appending entries to today's log. This skill is the default for any request to
  persist, retrieve, or edit personal knowledge when no external service (Jira,
  GitHub, Confluence, Linear, Things, Slack, email) is explicitly specified. Also
  trigger on any mention of "Obsidian", "vault", or "my notes".
argument-hint: [note-request]
model: sonnet
---

# Obsidian Notes

If `$ARGUMENTS` is provided, treat it as the user's note request and proceed directly without asking for clarification.

## Overview

Standard operations for reading, writing, and organizing notes in the Obsidian vault (Obsidian Flavored Markdown with YAML frontmatter and wikilinks). All vault operations use Obsidian MCP tools with vault-relative paths.

## Companion Skills

Obsidian supports more than plain markdown notes. Before proceeding, consider whether the user's request is better served by one of these formats:

| Skill | Format | When to use |
|-------|--------|-------------|
| `obsidian-markdown` | `.md` | **Always invoke** when creating or editing notes — ensures correct Obsidian Flavored Markdown (wikilinks, callouts, embeds, properties) |
| `obsidian-bases` | `.base` | User wants a database view, filtered table, card gallery, or summary of notes by properties |
| `json-canvas` | `.canvas` | User wants a visual layout — mind map, flowchart, project board, or spatial arrangement of ideas |

Invoke the relevant skill(s) before writing content so you follow the correct syntax.

## Directory Structure

Top-level categories: `Work/`, `Dev/`, `Games/`, `Personal/`, `Travel/`, `DailyNote/`

- Max depth: **3 levels** for general notes
- Exception: Projects and Meetings allow **4 levels**

## Special Note Types (use templates)

| Type | Path pattern | Template |
|------|-------------|----------|
| Project | `Work/Projects/[ProjectName]/[ProjectName].md` | `assets/project.md` |
| Meeting | `Work/Meetings/YYYY/MM/[title] YYYY-MM-DD.md` | `assets/meeting.md` |
| DailyNote | `DailyNote/YYYY/MM/YYYY-MM-DD.md` | Use `get_periodic_note`, `append_periodic_note`, `patch_periodic_note` |

## Note Creation Checklist

1. Determine note type (project / meeting / daily / general)
2. Select template if applicable
3. Create with `create_note(path, content)`
4. Verify frontmatter fields: `title`, `created`, `updated`, `tags`
5. Verify creation: `read_note(path)` to confirm file was created and YAML is valid

## Reference Files

| File | When to read |
|------|-------------|
| `references/note-organization.md` | Naming, tag system, frontmatter standards |
| `references/tool-selection.md` | Unsure which tool to use |
| `references/error-handling.md` | File not found, YAML errors, search returns nothing |
| `references/meeting-workflow.md` | Any meeting note operation (create, query, update status) |
| `references/project-workflow.md` | Any project note operation (query, create, update, Jira integration) |
