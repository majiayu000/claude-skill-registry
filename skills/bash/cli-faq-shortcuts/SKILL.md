---
name: faq-shortcuts
description: Turn the questions and instructions a user keeps typing into a project into short slash-command skills, mined from their real Claude Code and Codex session history and git log. The shortcuts load in Claude Code, Codex and Cursor. Use when the user says they ask the same things every day, wants an FAQ or shortcuts or abbreviations for a project, wants to "stop writing the whole command", or asks what they repeat most.
argument-hint: "[project dir, default cwd] [--source all|claude|codex] [--since YYYY-MM-DD]"
---

# FAQ shortcuts from your own history

People working with an agent on one project type the same asks over and over: "how many
signed up", "did it go out?", "send a reminder to those who haven't…". Each time the agent
starts cold and has to relearn the traps. This skill mines what was actually asked and
turns the most repeated asks into short project skills (`/joined`, `/sent`, `/remind`…).
Each one records the right tool and the mistakes already made on that path.

Build from evidence, not from guesses about what might be useful.

## 1. Collect the asks

```bash
python3 scripts/extract_asks.py <project_dir> [--source all|claude|codex] [--since YYYY-MM-DD] > asks.tsv
```

On Windows, run it with `python` instead of `python3`. This prints every prompt typed in
that project's sessions, oldest first, as
`date<TAB>source<TAB>prompt`. It reads Claude Code (`~/.claude/projects/`, plus
`~/.claude/history.jsonl` for sessions older than the 30 days Claude Code keeps
transcripts) and Codex (`~/.codex/sessions/`, or `$CODEX_HOME`) by default, and skips
subagent turns and scripted runs such as `codex exec`, because nobody typed those. An ask
repeated across both tools counts as one cluster. Cursor history is not read yet: it lives
in an undocumented SQLite store.

Write the output to a scratch location, not into the repo, because prompts can contain
names, emails and tokens.

Also read the commit subjects (`git log --format='%ad %s' --date=short`). Commits show which
*operations* recur, like repeated `send-*`, `sync-*` and `import-*` scripts. Prompts show how
the user *phrases* them.

## 2. Cluster by intent, then count

Read the whole list. Group prompts that want the same outcome whatever their wording
("how many joined", "how many confirmed", "how many members now" → one head-count ask).
Count each cluster and keep 2–3 verbatim phrasings, which become the description's triggers.

A cluster earns a shortcut when:
- it recurs (roughly 5+ times, or on most working days), and
- it takes more than one lookup to answer properly, or it has already gone wrong at least
  once. Look for follow-ups like "you did it wrong", "why did you…", "did you check…".

Drop one-offs and anything a single command already answers.

## 3. Check what already exists

List `.claude/skills/`, `.claude/commands/`, `.agents/skills/` and the project's CLAUDE.md
and AGENTS.md. Extend an existing skill instead of adding a near-duplicate. Then find the
project's existing tools for each cluster, such as scripts, CLI commands and API routes.
**A shortcut should point to the tool that exists.** Don't write a new one.

Read those tools' headers and the commits that fixed them. The traps you find there are the
most valuable part of each skill.

## 4. Propose before writing

Show the user a short table with shortcut name, the ask it replaces, and how often it
appeared. Let them pick. Short names beat descriptive ones here, because the point is less
typing. Use one lowercase word, and never shadow a built-in command.

## 5. Write each skill

`.claude/skills/<name>/SKILL.md`, committed with the project so it travels. Claude Code
and Cursor load skills from `.claude/skills/`. Codex loads them from `.agents/skills/`, so
link each one there as well:

```bash
mkdir -p .agents/skills && ln -s ../../.claude/skills/<name> .agents/skills/<name>
```

Link each skill folder, not `.agents/skills` itself: Codex follows a symlinked skill folder
but does not scan a symlinked `.agents/skills`.

The skill file itself:

```markdown
---
name: <short>
description: <what it does>. Use for "<verbatim phrasing 1>", "<phrasing 2>", "<phrasing 3>".
argument-hint: "[optional arg]"
---
# <What it answers>

Report only / Dry run first — **never <write/send> from this skill without a yes.**

## Query / tool       ← the existing script or query, with its real flags
## Traps              ← only ones that actually happened, each with the consequence
## Report             ← exactly what to print, then ask
```

Rules:
- **Split reading from acting.** Question skills only report. Action skills dry-run, show the
  list with every exclusion and its reason, then apply only after a yes.
- **Point to the source for every trap**, like the script header, commit or incident. If you
  can't trace a trap to something that happened, leave it out.
- Verify every field, flag and file name against the code before you write it down. A
  shortcut that cites a wrong column fails silently on the day it's needed.
- Keep a skill short enough to read in a minute. Leave out history, keep the lesson.
- Quote the frontmatter `description` if it contains `: ` or ` #`, or YAML will truncate it.

## 6. Make them findable

Add a table to the project's CLAUDE.md (and AGENTS.md, if the project has one) that maps
each shortcut to the sentence it replaces. It serves as both documentation and a reminder
to use it.

## Report

The shortcuts added, the ask each replaces with its count, and any frequent cluster you
deliberately left out and why.
