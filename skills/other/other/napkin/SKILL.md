---
name: napkin
description: |
  Maintain a per-repo napkin file that tracks mistakes, corrections, and
  what works. Activates EVERY session, unconditionally. Read the napkin
  before doing anything. Write to it continuously as you work — not just at
  session boundaries. Log your own mistakes, not just user corrections. The
  napkin lives in the repo at `.opencode/napkin.md`.
version: 1.0.0
date: 2026-02-06
---

# Napkin

You maintain a per-repo markdown file that tracks mistakes, corrections, and
patterns that work or don't. You read it before doing anything and update it
continuously as you work — whenever you learn something worth recording.

**This skill is always active. Every session. No trigger required.**

## Session Start: Read Your Notes

First thing, every session — read `.opencode/napkin.md` before doing anything
else. Internalize what's there and apply it silently. Don't announce that you
read it. Just apply what you know.

If no napkin exists yet, create one at `.opencode/napkin.md`:

```markdown
# Napkin

## Corrections
| Date | Source | What Went Wrong | What To Do Instead |
|------|--------|----------------|-------------------|

## User Preferences
- (accumulate here as you learn them)

## Patterns That Work
- (approaches that succeeded)

## Patterns That Don't Work
- (approaches that failed and why)

## Domain Notes
- (project/domain context that matters)
```

Adapt the sections to fit the repo's domain. Design something you can usefully
consume.

## Continuous Updates

Update the napkin as you work, not just at session start and end. However,
**never write to the napkin directly from the main session.** Instead,
delegate all writes through the `Task` tool. This keeps napkin housekeeping
out of your main context window.

When you learn something worth recording, use the Task tool like this:

```
Task(
  description="Update napkin",
  prompt="Read `.opencode/napkin.md` and apply the following update.

Section: <one of: Corrections | User Preferences | Patterns That Work | Patterns That Don't Work | Domain Notes>

Entry to add:
<provide the full entry content — for Corrections, use the table format:
| <date> | <source: self or user> | <what went wrong> | <what to do instead> |
For other sections, use a bullet point with specific, actionable detail.>

After updating, check if the file exceeds 150 lines. If so, consolidate:
merge redundant entries, promote repeated corrections to preferences,
remove already-captured items, archive outdated notes. Keep under 200 lines.

Return only a one-line confirmation of what was added or changed."
)
```

**You are responsible for composing the prompt with all the details.** The
task worker has no prior context — it only knows what you put in the prompt.
Include the date, source, what happened, and what to do instead. Be specific.

Triggers for writing — fire the `Task` tool whenever:

- **You hit an error and figure out why.** Log it immediately. Don't wait.
- **The user corrects you.** Log what you did and what they wanted instead.
- **You catch your own mistake.** Log it. Your mistakes count the same as
  user corrections — maybe more, because you're the one who knows what went
  wrong internally.
- **You try something and it fails.** Log the approach and why it didn't work
  so you don't repeat it.
- **You try something and it works well.** Log the pattern.

You can still **re-read the napkin mid-task** directly when you're about to do
something you've gotten wrong before. Reading is fine in the main session —
only writes get delegated.

The napkin is a living document. Treat it like working memory that persists
across sessions, not a journal you write in once.

## What to Log

Log anything that would change your behavior if you read it next session:

- **Your own mistakes**: wrong assumptions, bad approaches, misread code,
  failed commands, incorrect fixes you had to redo.
- **User corrections**: anything the user told you to do differently.
- **Tool/environment surprises**: things about this repo, its tooling, or its
  patterns that you didn't expect.
- **Preferences**: how the user likes things done — style, structure, process.
- **What worked**: approaches that succeeded, especially non-obvious ones.

Be specific. "Made an error" is useless. "Assumed the API returns a list but
it returns a paginated object with `.items`" is actionable.

## Napkin Maintenance

Maintenance is handled by the task worker as part of each write. The Task tool
prompt above instructs the task worker to consolidate when the file exceeds 150
lines. You do not need to do maintenance yourself.

If you notice the napkin is getting noisy during a session-start read, you
can fire a dedicated maintenance Task:

```
Task(
  description="Consolidate napkin",
  prompt="Read `.opencode/napkin.md` and consolidate it:
- Merge redundant entries into single rules.
- Promote repeated corrections to User Preferences.
- Remove entries now captured as top-level rules.
- Archive resolved or outdated notes.
- Keep total length under 200 lines of high-signal content.

Return a one-line summary of what changed."
)
```

A 50-line napkin of hard-won rules beats a 500-line log of raw entries.

## Example

**Early in a session** — you misread a function signature and pass args in the
wrong order. You catch it yourself. Log it:

```markdown
| 2026-02-06 | self | Passed (name, id) to createUser but signature is (id, name) | Check function signatures before calling, this codebase doesn't follow conventional arg ordering |
```

**Mid-session** — user corrects your import style. Log it:

```markdown
| 2026-02-06 | user | Used relative imports | This repo uses absolute imports from `src/` — always |
```

**Later** — you re-read the napkin before editing another file and use
absolute imports without being told. That's the loop working.
