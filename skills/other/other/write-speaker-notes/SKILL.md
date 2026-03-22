---
name: write-speaker-notes
description: Generate speaker notes (presentation script) for Quarto RevealJS slides. Supports English and Korean. Use when user asks to "write speaker notes", "add presentation script", "speaker script", "발표 스크립트", or "스피커 노트".
argument-hint: "[PaperName] [--lang en|ko]"
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob", "Agent"]
---

# Speaker Notes (Presentation Script) Workflow

Generate a verbatim reading script for Quarto RevealJS slides. The presenter should be able to read these notes as-is during the talk.

**CRITICAL: These are presentation scripts (대본), NOT talking points.** Full spoken sentences that flow naturally when read aloud.

---

## Phase 0: Pre-Flight Checks

### 0A. Identify Target File
Parse the argument to find `Quarto/[PaperName].qmd`. If no argument, ask the user.

### 0B. Language Selection
Parse `--lang` flag. If not provided, ask the user:
- `en` — English script (~3,000–3,500 words for 30 min, speaking rate ~130 words/min)
- `ko` — Korean script (~8,000–8,500 chars for 30 min, speaking rate ~280 chars/min)

### 0C. Check for Existing Notes
Search the QMD for `::: {.notes}` blocks.
- If notes already exist: warn user and ask whether to overwrite or skip slides that have notes.
- If no notes: proceed.

### 0D. Locate Source Materials
1. **QMD file** — primary source (must exist)
2. **Source paper** — search `target-papers/` for matching paper directory
3. **Beamer .tex** — search `Slides/` for matching file

Report what sources are available.

---

## Phase 1: Read & Analyze Slides

1. Read the complete QMD file
2. Count total slides (level-2 headings `##`) and sections (level-1 headings `#`)
3. Identify slide structure: which slides are content-heavy, which are light
4. Note section boundaries for narrative arc planning
5. Calculate target total budget based on language selection

Report to user:
- Total slides found
- Section breakdown
- Target script length
- Source materials available

---

## Phase 2: Batch Generation

Delegate to the `script-writer` agent in batches of 8–10 slides.

For each batch, provide the agent with:
1. The QMD content for those slides
2. The overall presentation context (paper title, what came before, what comes after)
3. The language setting
4. Approximate per-batch budget (total budget / number of batches, adjusted for content density)
5. Relevant source paper sections (for technical slides only)

**Batch sequencing:**
- Process batches sequentially (each batch needs context from previous batches for transitions)
- After each batch, verify the notes were properly inserted with `::: {.notes}` syntax
- Track running word/char count

**Notes placement rule:**
- Place `::: {.notes}` at the end of each slide, before the next `##` heading
- Section dividers (`#`) get brief transition notes
- References slide: skip (no notes)

---

## Phase 3: Count Verification

After all batches are complete:

1. Count total script length:
   - **Korean:** count characters excluding spaces, punctuation, and markdown syntax
   - **English:** count words excluding markdown syntax
2. Compare against target range:
   - Korean: 8,000–8,500 chars (acceptable: 7,200–9,350, i.e., ±10%)
   - English: 3,000–3,500 words (acceptable: 2,700–3,850, i.e., ±10%)
3. If outside acceptable range:
   - **Too long:** identify the longest notes and ask the script-writer agent to trim
   - **Too short:** identify slides with thin notes and ask for expansion
   - Re-count after adjustment

---

## Phase 4: Render & Verify

1. Run `cd Quarto && quarto render [PaperName].qmd`
2. Verify render succeeds without errors
3. Check the HTML output for `<aside class="notes">` elements
4. Report number of slides with notes vs total slides

---

## Phase 5: Timing Report

Generate a timing report and save to `quality_reports/[PaperName]_speaker_notes_report.md` using the template at `templates/speaker-notes-report.md`.

The report should include:
- Per-section breakdown (section name, number of slides, word/char count, estimated time)
- Total estimated presentation time
- Quality checklist status

Present a summary to the user including:
- Total script length (words or chars)
- Estimated presentation time
- Coverage (slides with notes / total slides)
- Any quality concerns

---

## Non-Negotiable Constraints

1. **Script, not notes.** Every note must be a complete, speakable script.
2. **No verbatim repetition.** Notes must add value beyond the slide content.
3. **Transitions matter.** Each note should flow naturally from the previous slide.
4. **Budget compliance.** Total must fall within ±10% of target range.
5. **Proper syntax.** Every `::: {.notes}` must have a matching `:::` closure.
6. **No notes on References slide.** Skip it entirely.

---

## Examples

### Example 1: First-time script generation
**User says:** `/write-speaker-notes DreamZero --lang ko`
**Actions:**
1. Find `Quarto/DreamZero.qmd`
2. Set language to Korean, target 8,000–8,500 chars
3. Read QMD, count slides, locate source paper
4. Generate notes in 4-5 batches via script-writer agent
5. Verify total char count within range
6. Render and verify
7. Generate timing report

### Example 2: Adding notes to already-annotated file
**User says:** "Add speaker notes to the new slides I added"
**Actions:**
1. Find QMD, detect existing `::: {.notes}` blocks
2. Identify slides WITHOUT notes
3. Generate notes only for unannotated slides
4. Verify count and render

### Example 3: Language switch
**User says:** "/write-speaker-notes DreamZero --lang en"
**Actions:**
1. If Korean notes exist, warn and ask whether to replace
2. If replacing, remove all existing `::: {.notes}` blocks first
3. Generate English script targeting 3,000–3,500 words
4. Verify and render
