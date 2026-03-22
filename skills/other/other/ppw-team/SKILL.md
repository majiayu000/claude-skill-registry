---
name: ppw:team
description: >-
  Orchestrate parallel paper processing. Split paper into sections and run
  any eligible Skill (polish, translation, de-ai) across sections via subagents.
  团队协作模式：将论文拆分为章节并行处理。
triggers:
  primary_intent: orchestrate parallel section-level paper processing
  examples:
    - "ppw:team polish paper.tex"
    - "团队模式润色论文"
    - "ppw:team translation draft.md"
    - "并行翻译论文各章节"
    - "ppw:team de-ai paper.tex"
tools:
  - Read
  - Write
  - Structured Interaction
  - Agent
references:
  required: []
  leaf_hints: []
input_modes:
  - file
output_contract:
  - section_files
  - manifest
  - poc_output
---

## Purpose

This Skill orchestrates parallel paper processing by splitting a paper into H1 sections and dispatching eligible Skills to subagents. In Phase 19 (current), it validates the proof-of-concept gate by running a single subagent on one section. Full parallel dispatch across all sections is Phase 20.

## Trigger

**Activates on:** `ppw:team [skill] [file]` invocations.

**Examples:**
- "ppw:team polish paper.tex" / "团队模式润色论文"
- "ppw:team translation draft.md" / "并行翻译论文各章节"
- "ppw:team de-ai paper.tex"

## Modes

| Mode | Default | Behavior |
|------|---------|----------|
| `guided` | Yes | split -> user confirms sections -> user selects PoC section -> run PoC -> user confirms quality |
| `direct` | | skip confirmations, auto-select all body sections and first section for PoC |

**Mode inference:** "直接" or "direct" in trigger switches to direct mode.

## References

`required: []` -- This Skill does not produce academic text itself. It orchestrates other Skills that load their own references at runtime. No reference files are needed by the orchestrator.

## Ask Strategy

**Guided mode** -- three interaction points via AskUserQuestion:
1. Section selection (multiSelect) after splitting
2. PoC section selection (single select) from selected sections
3. PoC quality confirmation (approve/retry/exit)

**Direct mode** -- skip all three: auto-select all body sections (exclude preamble and bibliography), auto-select first body section for PoC, auto-approve PoC output.

## Workflow

### Step 0: Workflow Memory (Recording Only)

- Skip pattern detection -- orchestrator is not suitable for auto-direct-mode recommendation.
- Recording happens after Step 1 validation (see Step 1).

### Step 1: Parse Arguments and Validate

- Parse `$ARGUMENTS` to extract: Skill name (first word) and file path (remaining words).
- Validate Skill name against whitelist: `["translation", "polish", "de-ai"]`
- If Skill is not in whitelist, reject with exact message: "[Skill] requires full-paper context and cannot run in parallel. Please run /ppw:[skill] directly."
- Validate file exists and is `.tex` or `.md` format. If file not found or wrong format, report error and stop.
- Read the paper file content.
- **Record workflow:** Append `{"skill": "ppw:team", "ts": "<ISO timestamp>"}` to `.planning/workflow-memory.json`. Create file as `[]` if missing. Drop oldest entry if log length >= 50.

### Step 2: Create Working Directory

- Create `.paper-team/` directory structure: `sections/`, `output/`.
- If `.paper-team/` already exists: in guided mode, ask to overwrite or cancel; in direct mode, overwrite silently.
- Create backup of original paper: `.paper-team/{filename}-backup-{YYYYMMDD-HHmm}.{ext}` (timestamped to prevent overwrite on re-runs).
- Initialize `.paper-team/manifest.json`:

```json
{
  "version": "1.0",
  "created": "<ISO timestamp>",
  "source_file": "<original file path>",
  "source_format": "tex|md",
  "target_skill": "<skill name>",
  "sections": [],
  "poc": { "section_id": null, "status": "pending", "timestamp": null },
  "backup": "<backup filename>"
}
```

### Step 3: Split Paper into Sections

**For .tex files:**
- Preamble: everything from start through `\begin{document}` (inclusive). Label "00 - Preamble".
- Bibliography: from `\bibliography{}` or `\printbibliography` through `\end{document}`. Label "99 - Bibliography".
- Section boundaries: each `\section` command. Match `\section` followed by optional `*` and optional `[...]` then `{...}`. Ignore lines starting with `%` (LaTeX comments).
- Content between `\begin{document}` and the first `\section{}` is "00 - Pre-section content" (if non-empty after trimming).
- Each section: content from its `\section{Title}` line through the line before the next `\section{` or the bibliography boundary.

**For .md files:**
- Frontmatter: content before the first `# ` heading. Label "00 - Frontmatter" (if non-empty).
- Split at lines beginning with `# ` (H1 headings).
- Each H1 heading and its content until the next `# ` is one section.

**Section file naming:** `{NN}-{sanitized-title}.{ext}` where NN = zero-padded sequence number, sanitized-title = title lowercased, spaces to hyphens, special chars removed, max 50 chars. Preamble: `00-preamble.{ext}`. Pre-section: `00-presection.{ext}`. Bibliography: `99-bibliography.{ext}`. Frontmatter: `00-frontmatter.md`.

**Edge cases:**
- No `\section{}` commands: treat entire body as "01 - Full Body".
- Only one section: warn parallel processing has no benefit; proceed with PoC anyway.
- Empty section (no content between boundaries): skip, do not create file.

Write each section to `.paper-team/sections/{filename}`. Update `manifest.json` sections array with `{ "id": "NN", "title": "...", "file": "sections/filename", "selected": false, "status": "pending" }` for each section.

### Step 4: Section Selection

**Guided mode:** Present all detected sections via AskUserQuestion multiSelect:

```
AskUserQuestion({
  question: "Select sections to process with ppw:{skill}:\n选择要用 ppw:{skill} 处理的章节：",
  multiSelect: true,
  options: [
    { label: "NN - Title", description: "brief description or first line" }
  ]
})
```

Update `manifest.json` to set `selected: true` for chosen sections.

**Direct mode:** Auto-select all sections EXCEPT those with id "00" (preamble/presection/frontmatter) and "99" (bibliography). Update manifest accordingly. Display selected sections to user.

### Step 5: PoC Section Selection

**Guided mode:** Present selected sections via AskUserQuestion (single select):

```
AskUserQuestion({
  question: "Select one section for proof-of-concept test:\n选择一个章节进行概念验证测试：",
  options: [
    { label: "NN - Title", description: "will be processed by a subagent" }
  ]
})
```

**Direct mode:** Auto-select the first selected section (lowest NN number among selected).

### Step 6: PoC Gate Execution

- Read the target Skill's SKILL.md from `.claude/skills/ppw-{skill}/SKILL.md`. If not found, report error: "Skill ppw:{skill} not found at .claude/skills/ppw-{skill}/SKILL.md" and stop.
- Read the selected section file from `.paper-team/sections/{file}`.
- Construct the subagent prompt (use this template verbatim, filling in placeholders):

```
You are executing a paper section processing task in direct mode.

## Skill Instructions

{FULL CONTENT OF TARGET SKILL.MD INSERTED HERE}

## Task

Process the following paper section file using the Skill instructions above.

- Input file: .paper-team/sections/{section-filename}
- Mode: direct (skip all AskUserQuestion calls, skip Workflow Memory Step 0)
- Write output to: .paper-team/output/{section-filename}
- Do NOT ask the user any questions. Proceed with defaults.
- Load all required references as specified in the Skill instructions.
- Produce output as if you were running the Skill directly on this section.
- If the Skill normally edits in-place, instead write the processed output to the output path above.
```

- Spawn a single subagent via the Agent tool with this prompt.
- Wait for subagent completion.
- Update `manifest.json`: set `poc.section_id`, `poc.status` to "completed", `poc.timestamp` to current ISO timestamp. Set the section's `status` to "completed".

### Step 7: PoC Quality Confirmation

**Guided mode:** Read the subagent output from `.paper-team/output/{file}`. Display a brief excerpt (first 20-30 lines) to the user. Then ask:

```
AskUserQuestion({
  question: "PoC gate: Is the subagent output quality acceptable?\n概念验证：子代理输出质量是否可接受？",
  options: [
    { label: "Approved - PoC gate passed", description: "Quality is comparable to main-session execution" },
    { label: "Retry", description: "Re-run PoC on the same section" },
    { label: "Exit", description: "Stop orchestration, quality is not acceptable" }
  ]
})
```

- **Approved:** Update `manifest.json` poc.status to "passed". Display: "PoC gate passed. The ppw:team orchestrator is validated. To process all sections in parallel, use Phase 20's parallel dispatch (coming soon)."
- **Retry:** Go back to Step 6. Loop at most 3 times, then suggest Exit.
- **Exit:** Update `manifest.json` poc.status to "failed". Display message and suggest running the Skill directly: "/ppw:{skill} {file}"

**Direct mode:** Auto-approve (set poc.status to "passed"), display the first 10 lines of output and the success message.

## Output Contract

| Output | Format | Condition |
|--------|--------|-----------|
| `section_files` | Individual files in `.paper-team/sections/` | Always produced after Step 3 |
| `manifest` | `.paper-team/manifest.json` | Always produced, updated throughout workflow |
| `poc_output` | Single file in `.paper-team/output/` | Produced after Step 6 |

## Edge Cases

| Situation | Handling |
|-----------|----------|
| Paper has no `\section{}` commands | Treat entire body as one section "01 - Full Body" |
| Paper has only one section | Warn parallel processing has no benefit; proceed with PoC |
| File path has spaces | Quote file paths in all Read/Write operations |
| `.paper-team/` already exists | Ask to overwrite or cancel (guided) / overwrite silently (direct) |
| Subagent fails or times out | Report error, suggest retry or exit |
| `\section*{}` (unnumbered) | Match as section boundary (pattern includes optional `*`) |
| `\section[short]{long}` (optional arg) | Match as section boundary (pattern includes optional `[...]`) |
| Empty section (no content between boundaries) | Skip empty sections, do not create files |

## Fallbacks

| Scenario | Fallback |
|----------|----------|
| Structured Interaction unavailable | Ask plain-text questions for section selection |
| Agent tool fails | Report error; suggest running Skill directly on the section |
| Target Skill SKILL.md not found | Report: "Skill ppw:{skill} not found at .claude/skills/ppw-{skill}/SKILL.md" |
| `.planning/workflow-memory.json` missing | Create as `[]` before appending |

---

*Skill: ppw-team*
*Conventions: references/skill-conventions.md*
