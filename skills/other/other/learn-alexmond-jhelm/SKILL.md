---
name: learn
description: >
  Save a learning to project memory. Invoke automatically (without user asking) whenever
  a task required more than one fix cycle to resolve — e.g. a test failed and needed a
  second attempt, a compile error required a correction, an API behaved unexpectedly, or
  an assumption proved wrong mid-task. ALWAYS invoke when a command fails due to a
  platform-specific argument (macOS vs Linux shell differences). Also invoke when the
  user explicitly asks to remember something. Do NOT invoke for routine single-pass work.
argument-hint: "[topic] [what you learned]"
---

## Save a learning to project memory

$ARGUMENTS

### Determine the learning

If triggered **automatically** (multi-cycle resolution), synthesise the learning from the conversation:
- What was the root cause of the extra cycle(s)?
- What assumption or gap in knowledge caused the first attempt to fail?
- What is the correct approach / API / behaviour?
- What should be checked first next time to avoid the same detour?

If triggered **by the user**, record exactly what they stated in `$ARGUMENTS`.

### Steps

1. Read the current memory file:
   `/Users/alex.mondshain/.claude/projects/-Users-alex-mondshain-claude-jhelm/memory/MEMORY.md`

2. Check whether a relevant topic file already exists in that same directory (e.g. `dependencies.md`, `testing.md`, `debugging.md`). If so, read it too.

3. Decide where to write:
   - Short, self-contained insight that fits an existing `MEMORY.md` section → add it there (keep file ≤ 200 lines).
   - Detailed or topic-specific learning → append to or create a dedicated topic file, then add/update a one-line reference in `MEMORY.md`.

4. Write in concise, actionable form:
   - Bullet points, not prose.
   - Lead with *what to do / what to check*, follow with *why*.
   - If it supersedes an existing note, update or remove the old one.

5. **Scan for reusable scripts** (see section below).

6. Confirm to the user what was saved and where (one line is enough).

### What to save
- Root causes of multi-cycle failures and the correct fix
- Non-obvious library behaviours or API quirks discovered during the task
- Version constraints and compatibility issues (e.g. BCrypt prefix `$2y$` vs `$2a$`)
- Architectural decisions and their rationale
- Workflow or tool preferences the user has stated
- Patterns confirmed to work that aren't obvious from the code
- **Platform-specific shell/CLI argument failures** — save to the `## macOS / Platform-Specific Shell Quirks` section in `MEMORY.md` with the failing invocation and the correct macOS alternative

### What NOT to save
- Routine outcomes that worked first time
- Temporary task state or in-progress work
- Anything already covered verbatim in `CLAUDE.md`
- Guesses or conclusions that were not verified by a passing test or explicit confirmation

---

### Scan for reusable scripts (token-saving step)

After saving the main learning, check whether any inline scripts generated during the current session should be promoted to persistent memory to avoid regenerating them in future sessions.

**When to do this scan:** Any time the session generated a Python or shell script of 10+ lines inline (in the conversation, not already in a skill file).

**How:**

1. Look at the current conversation for `python3 -c`, `python3 /tmp/`, or multi-line shell scripts that were written ad-hoc.

2. For each script found, ask:
   - Is this script already embedded in a skill (e.g. `/checkstyle`, `/jacoco`)? → Skip.
   - Was this script written once for a one-off task? → Skip.
   - Is this something likely to be needed again (analysis, bulk edits, data parsing)? → **Save it.**

3. If saving is warranted, choose the destination:
   - Script belongs to an existing skill → embed it in that skill's `skill.md` under a named section.
   - General utility with no existing skill → save as `.claude/scripts/<name>.py` (or `.sh`) in the repository.
   - Complex enough to deserve its own skill → note it in `MEMORY.md` as a candidate for a new skill.

4. Save the script file to `.claude/scripts/<descriptive-name>.<ext>` with a comment header:
   ```python
   # Purpose: <one-line description>
   # Run: python3 .claude/scripts/<name>.py [args]
   <script content>
   ```

5. Add a one-line reference in `MEMORY.md` under a `## Scripts` section (create if absent):
   ```
   - `.claude/scripts/<name>.py` — <purpose>
   ```

6. Commit the new script directly to `main` (skill-only rule applies to `.claude/` changes):
   ```bash
   git add .claude/scripts/<name>.<ext>
   git commit -m "Add reusable <name> script"
   git push
   ```

**Goal:** scripts live in the repo, are version-controlled, and can be run directly with a known path — no regeneration, no memory file bloat.
