---
name: weekly-review
description: Weekly review and next-week planning for Obsidian monthly planning files. Analyze the current or specified week, infer the local section style, summarize milestones and risks, and update one week-level review section inside the week block without nesting it under personal subheadings. Use when the user asks for “周复盘”“本周总结”“下周计划”“这周进度怎么样”“weekly review”“week summary” or similar week-level review/planning tasks.
---

# Weekly Review

Use this skill to update one week block inside `Plan/每日规划/{YYYY}/Q{Q}/{YYYY.MM}.md`.

Read [references/obsidian-weekly-patterns.md](references/obsidian-weekly-patterns.md) before editing. It captures the observed 2026 week structures, naming variants, insertion boundaries, counting rules, and fallback template.

## Workflow

1. Resolve the target week. Default to the current week. Honor an explicit date range or week name from the user.
2. Find candidate month files. Read the current month file first:
   ```bash
   obsidian read path="Plan/每日规划/{YYYY}/Q{Q}/{YYYY.MM}.md"
   ```
   Also inspect the adjacent month file when the week spans two months. If the exact path is uncertain, use `obsidian search query="{week heading text}"` to locate the right file. Treat the week heading text as the source of truth even when the span is not a standard 7-day week.
3. Detect the local weekly style from the current file. Reuse the existing section name if the file already uses `周总结`, `本周总结`, or `📝 本周复盘`.
4. Update in place:
   - If a weekly review section already exists in the target week block, update that section instead of creating a second one.
   - Insert the weekly review at week-block top level, after the weekly goal sections and before the first day heading.
   - Match the heading depth used by sibling week-level sections and day headings. Do not nest the review under `## 个人` or any category subsection.
   - For inserting a new review section, use `obsidian append path="..." content="..." silent`. For patching an existing section, use the Edit tool directly on the vault file.
5. Analyze progress using the counting rules in the reference file. Prefer parent-task counts when parent tasks own child checkboxes.
6. If the week is still in progress, say `统计截至 {Today}` in chat output.
7. Produce a concise summary with milestones, risks, and next-week adjustments. Prefer insight over task-by-task narration.

## Output

- In chat, report work/personal progress, 1-3 milestones, the main bottleneck, and 2-3 next-week adjustments.
- In file, preserve the local naming and tone instead of forcing a new review title.

## Guardrails

- If Obsidian is not running, fall back to reading vault files directly with the Read tool.
- Support non-standard week spans such as holiday blocks. Do not assume every week covers exactly seven days.
- Keep the edit inside the target week block and before the next week heading.
- Ignore malformed checklist lines and explanatory bullets without checkboxes.
- If more than one week heading could match, prefer the heading explicitly named by the user or the one containing today's date. If ambiguity remains, explain it before editing.
