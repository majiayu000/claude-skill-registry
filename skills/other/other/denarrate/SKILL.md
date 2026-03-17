---
name: denarrate
description: Strip narrative mode from descriptive artifacts. Comments describe state and intent — they don't tell stories.
args: "[file or directory paths, or 'staged' for git diff --staged]"
---

# Denarrate

Comments are a descriptive channel. They operate in the atemporal
present. When narrative leaks in — sequence, causation, history —
it violates the channel's discourse mode.

## The Principle

Every artifact has one semantic role:

| Artifact | Role | Temporal mode |
|----------|------|---------------|
| Code | What is | Present |
| Comments | Why it's surprising | Atemporal |
| Commits | What changed | Past |
| PRs | What to evaluate | Imperative |

Narrative belongs in commits and PRs. Comments that narrate are
operating in the wrong discourse mode. They presuppose a temporal
context the reader doesn't have, imply false relevance, and decay
without a mechanism to clean them up.

## Narrative Signals

**Temporal language** — verbs and adverbs that anchor to a timeline:

- "Moved from X to Y" — git carries transitions
- "Was previously..." — presupposes a "before" the reader can't access
- "No longer needed since..." — delete the code, not narrate its departure
- "Renamed from..." — git blame exists for this
- "Added in PR #123" — git log exists for this
- "After the refactor..." — there is no "after" in a comment
- "Now uses X instead of Y" — just describe X

**Restating the obvious** — narrating what the reader can already see:

- `# Load the config` above `load_config()`
- `# Initialize the database` above `db.init()`
- `# Return the result` above `return result`

Cover the comment. Can the reader still understand the code? If
yes, the comment is narration.

**Dangling presupposition** — narrative context that doesn't resolve:

- "Unlike the old implementation..." — what old implementation?
- "This replaces the previous approach" — what approach?
- "For historical reasons..." — either explain the constraint or don't

**Hedging as narration** — telling the story of the code's uncertainty:

- "This is a temporary workaround" — file an issue or fix it
- "TODO: clean up after migration" — the migration is over or it isn't
- "Might not be needed anymore" — find out

## What Survives

Not every comment is a target. These are in-register:

- **Intent**: "Retry with backoff because the upstream API rate-limits"
- **Constraints**: "Must stay sorted — binary search depends on it"
- **Non-obvious behavior**: "Returns None on timeout, not an error"
- **Warnings**: "Not thread-safe — caller must hold the lock"

These describe atemporal properties of the code. They'd be true
yesterday, today, and tomorrow. That's the test.

## On Activation

1. **Resolve targets** — if args are file paths, read them. If
   "staged", read `git diff --staged`. If a directory, find source
   files in it. If no args, ask.
2. **Extract every comment** from the target files.
3. **Evaluate each** — is it descriptive (in-register) or narrative
   (out-of-register)?
4. **Present findings** — file, line, the comment, which narrative
   signal it triggers, and the fix (revised wording or deletion).
5. **Ask** before applying.
6. **Apply** — edit files, show the diff.
