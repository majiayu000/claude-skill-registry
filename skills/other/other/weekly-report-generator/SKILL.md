---
name: weekly-report-generator
description: "Automatically generates a 1-page weekly progress report PPTX based on Obsidian daily notes. Trigger this skill on Saturdays. It (1) Identifies the date range from last Saturday to this Saturday, (2) Reads daily notes from '50 Archive/Daily Notes/' and extracts only research (科研) and project (项目) related content, (3) Fills exactly ONE slide with '本周进展' and '下周计划', (4) Never touches the slide master or header area (name lives in the master), and (5) Saves to '00 Inbox/UserName_YYYY_MMDD_MMDD_week_report.pptx'."
---

# Weekly Report Generator

Generates a **single-slide** weekly PPTX report for the user, summarizing research and project progress from Obsidian daily notes. The audience is the supervisor — only meaningful research/project work matters.

## Template Rules (CRITICAL)

The template already has:
- A **slide master** containing the user's name and the lab logo in the header area.
- A blue **task line** near the top (e.g. `任务：Project A，重点研发（Project B）、科研C`).
- Two body sections: `本周进展：` (with bullet points) and `下周计划：` (with bullet points).

**DO NOT:**
- Add, move, or modify any title/header text box. The name and logo come from the slide master — leave them alone.
- Add a second slide. Everything must fit on ONE slide.
- Delete or rearrange existing placeholder shapes.
- Change fonts or color scheme — follow what the template already uses.

**DO:**
- Only edit the **body text** inside the existing text placeholders for `本周进展` and `下周计划`.
- Update the task line date range if one exists.
- Keep the slide layout and structure identical to the template.

## Content Rules

### What to Include
- Research work (科研): paper reading, experiments, algorithm design, simulation results, data analysis, writing.
- Project work (项目): engineering tasks, development milestones, testing, demos, deployments.
- Summarize by **topic/theme**, not by day. Group related items across the week.

### What to Exclude
- Tool setup, environment configuration, agent/IDE tweaks (e.g. "配置了XXX环境", "装了XXX插件").
- Personal or administrative items unrelated to research/projects.
- Trivial items that don't reflect meaningful progress.

### Tone
- Concise, professional, teacher-facing. Highlight outcomes and progress, not process.
- Use short bullet points (one line each when possible). Avoid long paragraphs.

## Formatting Rules

- **Line spacing**: Use consistent, moderate line spacing (1.0–1.2×). Avoid overly sparse layouts or cramped text.
- **Font size**: Body bullets ~14–16pt. Section headers (`本周进展：`, `下周计划：`) bold, ~18–20pt.
- **Bullet count**: Aim for 3–6 bullets under `本周进展` and 2–4 under `下周计划`. Condense if needed to keep the slide clean and readable.
- **Whitespace balance**: `本周进展` section should take roughly 60% of the body area, `下周计划` the remaining 40%. Adjust spacing so neither section looks empty or overflowing.

## Workflow

1. **Calculate Dates**: Determine the range — previous Saturday (MMDD) to this Saturday (MMDD).
2. **Read Daily Notes**: Scan `50 Archive/Daily Notes/` for each date in range. Look for sections under `今日已毕` or equivalent daily log headings.
3. **Filter & Summarize**: Extract only 科研/项目 items. Group by theme across the week into concise bullet points.
4. **Fill Template**: Use the `pptx` skill to edit the template. Only modify body text placeholders — never touch the slide master, header, or layout structure. Ensure the result is exactly 1 slide.
5. **Output**: Save as `00 Inbox/UserName_YYYY_MMDD_MMDD_week_report.pptx`.

## QA Checklist

Before delivering, verify:
- [ ] Exactly 1 slide
- [ ] Header area (name + logo) is untouched — matches template exactly
- [ ] `本周进展` and `下周计划` sections are both present and populated
- [ ] No tool/config/setup items leaked into the content
- [ ] Line spacing is even and the slide doesn't look cramped or sparse
- [ ] No placeholder text (e.g. `xxxx`, `1.`) left over from template
