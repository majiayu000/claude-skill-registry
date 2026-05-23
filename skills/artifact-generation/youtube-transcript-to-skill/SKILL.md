---
name: youtube-transcript-to-skill
description: Convert a YouTube video transcript into Claude Code skills. Extracts tips, evaluates against selection criteria, and generates SKILL.md files with full transparency.
disable-model-invocation: true
argument-hint: [path/to/transcript.txt]
---

# YouTube Transcript to Skill

Convert a video transcript (or article) about Claude Code / AI coding tools into reusable skills. Extracts discrete tips, evaluates each against a structured selection framework, and generates SKILL.md files for tips that qualify — with full transparency at every step.

## Usage

`/youtube-transcript-to-skill path/to/transcript.txt`

Supported file types: `.txt`, `.md`, `.pdf`

## Procedure

### Step 1: Load and Validate Transcript

1. If `$ARGUMENTS` is empty, ask the user: "Please provide a file path to the transcript (`.txt`, `.md`, or `.pdf`)."
2. Check the file extension:
   - **Supported**: `.txt`, `.md`, `.pdf` — proceed
   - **Unsupported**: Stop and tell the user: "I can't read `.<ext>` files directly. Please convert it to `.txt`, `.md`, or `.pdf` first, then re-run the skill."
3. Read the file using the Read tool. For large PDFs (10+ pages), read in chunks using the `pages` parameter.
4. Estimate the word count and assess the topic.
5. **Topic check**: If the content is clearly unrelated to Claude Code, AI coding tools, or developer workflows (e.g., a cooking tutorial, a political speech), warn the user:
   > "This transcript appears to be about [detected topic], not about Claude Code or AI-assisted development workflows. No skills can be extracted. Would you like me to proceed anyway in case I missed something?"
   If the user says stop, end here. If they say proceed, continue but expect zero skill-worthy tips.
6. Show: "Loaded transcript: ~N words from `[filename]`, appears to be about [topic]."

### Step 2: Extract Discrete Tips

1. Parse the transcript into individually actionable tips or techniques. A tip is a discrete, specific piece of advice that describes something a developer could DO — not a general observation or opinion.
2. Number them sequentially starting from 1.
3. For each tip, extract:
   - **Short name**: 3-6 word label (e.g., "Plan before coding", "Auto-format with hooks")
   - **Description**: 1-2 sentences explaining what the tip recommends
4. Show the full numbered list to the user.
5. If zero tips were extracted, report:
   > "I couldn't extract any discrete, actionable tips from this transcript. The content appears to be [description]. Tips need to be specific techniques or workflows that Claude could execute. No skills can be generated."
   Write the analysis report (Step 8) explaining why, then stop.
6. Ask: "I found N tips. Any to add, remove, or split?"
7. Incorporate the user's feedback before proceeding.

### Step 3: Load Selection Criteria

Read the selection criteria reference file bundled with this skill:

```
.claude/skills/youtube-transcript-to-skill/selection-criteria.md
```

This contains the full Gate (G1-G4), Value (V1-V4), and Exclusion (E1-E6) framework used for evaluation.

### Step 4: Evaluate Each Tip

For EACH extracted tip (show results as you go, not batched at the end):

1. **Gate G1 — Automatable**: Can Claude execute this programmatically? If no, classify as UI/Shortcut and move on.
2. **Gate G2 — Recurring**: Would someone invoke this more than once? If no, classify as One-time.
3. **Gate G3 — Not built-in**: Does Claude Code already do this? If yes, classify as Built-in.
4. **Gate G4 — Best mechanism**: Is a Skill the right mechanism?
   - If it should always apply -> classify as CLAUDE.md
   - If it must run deterministically on events -> classify as Hook
   - If it requires external service connection -> classify as MCP
5. **Value check**: For tips that pass all gates, check V1-V4. At least one must pass. If none pass, note why.
6. **Exclusion check**: Check E1-E6. If any exclusion applies, classify accordingly.

For each tip, show a brief verdict:
> "Tip N: [name] — [PASS/FAIL] — [reason]. Category: [category]"

### Step 5: Present Classification Summary

1. Show a summary table grouping all tips by their classification category:

```
| Category       | Count | Tip Numbers        |
|----------------|-------|--------------------|
| Skill-worthy   | N     | #3, #7, #12, ...   |
| UI/Shortcut    | N     | #1, #6, ...        |
| Built-in       | N     | #4, ...            |
| One-time       | N     | #2, ...            |
| Philosophy     | N     | #8, ...            |
| CLAUDE.md      | N     | #5, ...            |
| Hook           | N     | #9, ...            |
| MCP            | N     | #11, ...           |
```

2. For each rejected tip, show the specific gate/exclusion that failed and what mechanism would be better.
3. If zero tips are skill-worthy, report:
   > "I extracted N tips, but none passed the skill selection criteria. Here's why: [summary]. No SKILL.md files will be generated, but the full analysis is saved to [report path]."
   Write the analysis report (Step 8), then stop.
4. Ask: "Any disagreements with this classification?"
5. Incorporate feedback before proceeding.

### Step 6: Group Tips into Skills

1. Examine the skill-worthy tips for natural groupings:
   - **Shared domain**: Tips about the same subsystem or feature area
   - **Sequential workflow**: Tips that form a natural ordered sequence
   - **Setup + usage**: Configuration tip paired with a usage tip
2. For each proposed skill, define:
   - **Skill name** (kebab-case)
   - **Description** (one sentence)
   - **Source tips** (which tip numbers it covers)
   - **Grouping rationale** (why these tips belong together)
3. Prefer fewer, more capable skills over many tiny ones. A skill with 3-6 steps is ideal.
4. Show the grouping to the user.
5. Ask: "Should I adjust any groupings?"
6. Incorporate feedback before proceeding.

### Step 7: Generate Skills

For each proposed skill:

1. Generate a complete SKILL.md following project conventions:
   - YAML frontmatter with `name`, `description`, `disable-model-invocation: true`, and `argument-hint` (if the skill takes input)
   - H1 title and brief description
   - `## Usage` section with invocation syntax
   - `## Procedure` section with numbered steps (`### Step N: Name`)
   - Each step should have clear, specific instructions Claude can follow
2. Show the full generated SKILL.md to the user.
3. After showing all generated skills, ask: "Write these skills to disk?"
4. If the user wants changes, revise and re-show before writing.

### Step 8: Write Output

1. **Write SKILL.md files** to the current project's `.claude/skills/<skill-name>/SKILL.md`.
   - NEVER write to `~/.claude/skills/` (user-global scope).
   - Create the directory if it doesn't exist.
2. **Write the analysis report** to the current project's `docs/<video-slug>-analysis.md`. Derive the slug from the video title or filename (kebab-case, lowercase). The report contains:

```markdown
# Transcript Analysis: [Title]

**Source**: [filename]
**Author**: [if known]
**Topic**: [detected topic]
**Tips extracted**: N
**Skills generated**: M

## Extracted Tips

[Numbered list of all tips with short name and description]

## Evaluation Results

[Per-tip evaluation showing gates, values, exclusions, and verdict]

## Classification Summary

[Summary table by category]

## Skill Grouping

[Which tips combined into which skills, with rationale]

## Generated Skills

[List of skills created with file paths]

## Non-Skill Recommendations

[Tips better served by other mechanisms, with specific guidance]
```

3. Show a final summary:
   > "Done. Extracted N tips, created M skills, redirected K tips to other mechanisms. Analysis report: `docs/[slug]-analysis.md`. Skills installed to `.claude/skills/` (project-local only)."
