---
name: mind-recorder
description: Record thoughts, ideas, reflections, and insights into the user's Obsidian vault DailyNote system. Use this skill whenever the user wants to capture a thought, jot down an idea, record a reflection, save a memo, or write down something they're thinking about. Triggers include phrases like "记录一下""写个想法""记一下这个""帮我记下来""save this thought""record this idea""我有个想法""突然想到""随便写写""帮我记到obsidian", or any situation where the user is sharing a personal thought, opinion, or reflection and wants it persisted to their notes. Also use when the user says things like "这个值得记一下""帮我存一下这个想法""想法记录" etc.
---

# Mind Recorder

Capture the user's thoughts and ideas into their Obsidian vault's DailyNote system. Thoughts are stored under `DailyNote/` within the vault.

Read [references/dailynote-patterns.md](references/dailynote-patterns.md) for the exact file structure, naming conventions, entry types, and formatting rules before making any edits. This reference is essential — it contains the real examples and format details that keep entries consistent with the user's existing notes.

## Locate the Vault

The vault path varies across machines, so discover it dynamically rather than hardcoding:

1. **Preferred**: use `obsidian` CLI — all `path=` arguments are vault-relative, so the CLI resolves the absolute path automatically.
2. **Fallback** (Obsidian not running): run `obsidian vault` or check `~/Library/Application Support/obsidian/obsidian.json` to find the vault root, then use Read/Edit/Write tools with the resolved path.

## Core Workflow

### 1. Understand the thought

Listen to what the user wants to record. Identify:
- **Title**: a concise Chinese title summarizing the thought (the user may provide one, or help draft one)
- **Tags**: relevant tags (e.g., `#ai`, `#认知`, `#想法`, `#活动`). Suggest tags based on content if the user doesn't specify — see the reference for commonly used tags.
- **Content**: the actual thought — could be a single sentence or a long essay

### 2. Determine the target file

Based on today's date (or a date the user specifies):

- **Summary file**: `DailyNote/{YYYY}/{YYYY} 想法汇总.md` — always updated; this is where all entries are indexed
- **Standalone file**: `DailyNote/{YYYY}/{YYYY-MM-DD}.md` — created only for longer entries, referenced via embed in the summary

### 3. Decide inline vs. standalone

- **Short thoughts** (a few sentences, under ~300 characters): write content directly inline in the summary file.
- **Long thoughts** (multiple paragraphs, structured content with sub-headings): create a standalone `{YYYY-MM-DD}.md` file, then add an embed reference (`![[{YYYY-MM-DD}#标题]]`) in the summary file.
- If a standalone file for that date already exists, append the new content as a new `#` heading section rather than overwriting — the user may record multiple thoughts in one day.

### 4. Write to the vault

Use the `obsidian` CLI when Obsidian is running. Fall back to direct file editing if Obsidian is not available.

1. Read the current summary file to check existing structure.
2. Find the correct month section (`# {N}月`). If it doesn't exist yet, create it at the top of the file — months are ordered newest-first.
3. Insert the new entry under the correct month section. Entries within a month are also newest-first.
4. For standalone files, create via `obsidian create` with the `silent` flag, or use the Write tool directly.

### 5. Confirm to the user

After recording, briefly confirm: the file path, title, tags, and whether it was inline or standalone.

## Example

**User says**: "帮我记一下，我觉得现在很多人对 AI 的使用还停留在问答层面，真正用 Agent 去解决复杂工作流的人很少"

**Skill produces** — appends to `DailyNote/{YYYY}/{YYYY} 想法汇总.md` under the current month:

```markdown
## 03.17 大多数人对 AI 的使用还停留在问答层面

#ai #认知

我觉得现在很多人对 AI 的使用还停留在问答层面，真正用 Agent 去解决复杂工作流的人很少
```

**And replies**: "已记录到 DailyNote/{YYYY}/{YYYY} 想法汇总.md，标题「大多数人对 AI 的使用还停留在问答层面」，标签 #ai #认知"

## Guardrails

- Always read the existing summary file before editing — the file has a specific ordering and structure that's easy to break if you insert blindly.
- Preserve the user's writing voice. The note is the user's thought, not yours — organize lightly if needed, but don't rewrite or add commentary.
- If the user's thought includes links, quotes, or references, use Obsidian-flavored markdown (callouts `> [!tip]`, embeds `![[...]]`, etc.) to preserve them naturally.
- When creating a new year's directory or summary file, follow the existing `{YYYY} 想法汇总.md` convention exactly.
- Avoid creating entries for future dates — the DailyNote system is a record of thoughts as they happen, so forward-dating would break the chronological intent.
