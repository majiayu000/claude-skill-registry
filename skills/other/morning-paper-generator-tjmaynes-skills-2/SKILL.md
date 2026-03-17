---
name: morning-paper-generator
description: Generate Julia Cameron-style morning paper prompts and scaffold daily journal entries. Use when someone requests a new morning pages session and needs a dated markdown file seeded with a reflective prompt.
license: MIT
allowed-tools: Read Write Edit Bash(ls:*) Bash(mkdir:*) Bash(find:*) Bash(tree:*) Bash(jq:*) Bash(pwd:*)
metadata:
  generated-at: "2026-01-11T00:00:00Z"
  group: "wellness"
  category: "journaling"
  difficulty: "beginner"
  step-count: "4"
---

# Morning Paper Generator

## What You'll Do
- 🌅 Clarify the writer's focus, mood, and desired depth for a Julia Cameron-style morning pages session
- 🧠 Generate or select a reflective, emotionally honest prompt directly with the LLM, keeping a Julia Cameron-inspired morning pages tone throughout
- 🗂️ Ensure a `morning-papers/` directory exists (confirm the target directory with the writer before creating it) and create a dated markdown file (`YYYY-MM-DD.md`) with the prompt and writing scaffold
- ✍️ Provide gentle instructions to transition from prompt into free-writing, including warm-up techniques and follow-up reminders

---

## Phase 1 · Gather Context
1. **Understand today's focus**
   - Ask about emotional state, themes (gratitude, blocks, creative risks), or any constraints (time, word count).
   - Confirm whether the writer wants a single prompt or multiple mini-prompts.
   - Ask if they would like the skill to generate a fresh random prompt, choose from past favorites, or co-create something bespoke.
2. **Check existing morning papers**
    - List files in `morning-papers/` if present. Note prior prompts to avoid repetition.
    - If the directory is missing, note that you will confirm the intended location with the writer in Phase 3 before creating it.

3. **Clarify prompt generation approach**
   - Offer to have the LLM craft a random morning pages prompt in Julia Cameron’s voice, or collaborate on a bespoke prompt.
   - Capture every candidate prompt surfaced (random, custom, or historical) in a short list so the writer can choose later.
   - Confirm if the writer prefers additional sections (gratitude list, affirmations, action steps).
   - Check that `jq` is available (needed later to log used prompts). If missing, note that you will append to the JSON file manually.
4. **Resolve unknowns**
   - If timelines or expectations are unclear (e.g., “How long should the entry be?”), ask the user before proceeding.

> **Outcome:** A short set of notes capturing today’s intent, avoided topics, candidate prompts, prompt-generation method, and desired structure.

---

## Phase 2 · Design the Entry
1. **Select prompt strategy**
   - Generate 2–3 candidate prompts with the LLM (ask for Julia Cameron-style morning pages voice) and add them to your list.
   - Optionally remix past prompts or co-create bespoke versions if the writer has a theme in mind.
   - Review the candidate list with the writer and confirm the final choice before writing the file.
2. **Plan the file structure**
   - Default sections: `# Morning Paper – YYYY-MM-DD`, `## Prompt`, `## Stream`, `## Noticings`, `## Next Gentle Step`.
   - Add optional sections per user preference (e.g., “Gratitude Snapshot”, “Affirmation”).
3. **Determine guidance copy**
   - Include short reminders: write longhand if possible, keep the pen moving, no self-editing.
   - Suggest a timer or page count to set expectations.

> **Checklist:** Prompt candidate list captured, final prompt chosen, sections defined, supportive guidance ready.

---

## Phase 3 · Compose the Markdown Entry
1. **Create directory & filename**
    - Check whether `morning-papers/` exists.
    - If it is missing, share the current directory path (`pwd`) and confirm with the writer before creating it here or choosing another location.
    - Once confirmed, create the directory (`mkdir -p morning-papers`).
    - Filename format: `morning-papers/YYYY-MM-DD.md` (use the writer’s local date).

2. **Write the file**
    - Add YAML frontmatter with the session date and the chosen prompt:
     ```yaml

     ---
     date: 2026-01-11
     prompt: >-
       Write about the first thought that met you when you woke up and how it
       wants you to move through today.
     ---
     ```
   - Include the planned sections and the selected prompt below the frontmatter.
   - Optionally add a “Prompt Shelf” appendix listing alternate prompts the writer declined (helpful for future sessions).
   - Add a warm-up instruction block (e.g., breathe, notice surroundings).
   - Preserve blank space under each heading to invite handwriting or typing.
3. **Log the prompt**
   - Ensure `morning-papers/.completed-prompts.json` exists. If not, create it with `jq -n '[]' > morning-papers/.completed-prompts.json` (or write `[]` manually when `jq` is unavailable).
   - Append today’s prompt and date using placeholders (substitute the real values):
     ```bash
     tmp=$(mktemp)
     jq --arg date "$SESSION_DATE" --arg prompt "$PROMPT_TEXT" \
       '. + [{date: $date, prompt: $prompt}]' \
       morning-papers/.completed-prompts.json >"$tmp" && \
       mv "$tmp" morning-papers/.completed-prompts.json
     ```
   - When `jq` is missing, append a JSON object manually and validate the file structure before finishing.
4. **Avoid duplicates**
   - Check if today’s file already exists; if so, append a numbered suffix (e.g., `YYYY-MM-DD-2.md`) or confirm with the writer before overwriting.
5. **Optional resources**
   - Link to prior entries or related prompts if helpful (e.g., `See also: morning-papers/2026-01-05.md`).

---

## Phase 4 · Wrap Up & Handoff
1. **Self-review**
   - File created in `morning-papers/` with correct date.
   - Prompt is nurturing, specific, and not a repeat from previous entries.
   - `.completed-prompts.json` contains the new entry with correct date/prompt values.
   - Guidance includes reminders about free-writing and self-compassion.
2. **Support the writer**
   - Offer a short “start now” script (e.g., set a 20-minute timer, reread the prompt aloud).
   - Invite the writer to note insights afterward in the `Noticings` section.
3. **Summarize output**
   - Share the file path, the chosen prompt, the shortlist of alternative prompts, and confirm that `.completed-prompts.json` was updated.
   - Suggest next steps (e.g., create a recurring reminder, archive insights).

---

## Reference Templates

### Minimal Entry
```markdown
---
date: 2026-01-11
prompt: >-
  Write about the first thought that met you when you woke up and how it wants
  you to move through today.
---

# Morning Paper – 2026-01-11

## Prompt
Write about the first thought that met you when you woke up and how it wants you to move through today.

## Stream
_(Keep the pen moving for three pages or 20 minutes. No editing.)_

## Noticings
- What surprised me
- What I’m releasing

## Next Gentle Step
- One compassionate action I can take today:
```

### Timer-Friendly Add-on
```markdown
> 🕰️ Suggested flow: 2-minute grounding · 15-minute freestyle · 3-minute reflection
```

Use these scaffolds as starting points and tailor sections based on the writer’s request. Aim for warmth, clarity, and momentum.
