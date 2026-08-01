---
name: git-commit
description: Turn the working changes into one or more atomic commits with well-written messages. Use whenever the user runs /git-commit or asks to commit their work, wrap up a feature, or "commit what I have."
argument-hint: "[optional note or context to fold into the message]"
---

## What this does

Look at everything that has changed in the working tree, decide how the changes should be split into commits, and then create those commits — messages and all — without stopping to ask for approval. The user invoked `/git-commit` because they trust you to make the call, so make it and report what you did afterward.

Any argument the user passes is context, not a command: a hint about intent ("addressing review feedback", "this is risky, note the migration") that should inform how you group and what you write. It is never the literal commit message.

## Step 1: Understand what changed

Before grouping anything, build a real picture of the diff. Run these together:

- `git status` — what's modified, added, deleted, untracked
- `git diff` — unstaged changes
- `git diff --staged` — anything already staged
- `git log --oneline -15` — recent history, to match the tone and see referenced issues/PRs

Read the diff to understand the _why_, not just the _what_. You are about to explain these changes to a future reader; you can't do that if you only know which lines moved. If something is genuinely unclear, it's fine to ask one focused question — but usually the diff plus recent history tells the story.

If there's nothing to commit, say so and stop. Never create an empty commit.

## Step 2: Decide the grouping — this is the judgment call

The goal is **atomic commits**: each commit is one complete, coherent change that stands on its own. The hard part is knowing how many commits that means, and there's no mechanical rule — it depends on what the work actually is.

**Lean toward a single commit when the changes tell one story.** If the user just built a feature — new model, its migration, the controller, the view, the tests — that's _one_ logical change even though it spans many files. Splitting it into "add migration", "add model", "add tests" produces commits that are individually broken and useless to revert. Keep it together.

**Split into separate commits when the changes are genuinely independent.** The tell is that the work is a _set of unrelated things_ rather than one thing:

- Addressing several distinct review comments — each comment is its own commit
- A handful of unrelated refactors or cleanups that happen to be sitting in the tree together
- A bug fix that got made alongside feature work — the fix is its own commit
- A dependency bump plus the feature that needed it — often two commits

Ask yourself: _if someone had to revert one part of this, would the rest still make sense?_ If yes, they're separate commits. If reverting one piece would leave the others broken, they belong together.

When in doubt, prefer fewer, larger commits over many tiny ones. An over-split history is harder to read than a cohesive one.

## Step 3: Stage each group precisely

Commit the groups one at a time. For each:

- If a group is cleanly whole files, `git add <paths>` for just those files.
- If a single file contains changes belonging to _different_ logical groups, stage only the relevant hunks. Write the intended hunks to a patch and apply them with `git apply --cached <patch>`, since interactive `git add -p` isn't available to you. Verify with `git diff --staged` before committing.
- Never `git add .` or `git add -A` blindly — that defeats the point of grouping.

Then commit that group (Step 4), and move to the next.

Respect any pre-commit hooks. If a hook modifies files or fails, don't fight it — surface what happened. Don't use `--no-verify` unless the user asked for it.

Do not push, and do not amend or rewrite existing commits. This command's job ends at creating new commits from uncommitted work.

## Step 4: Write the message

Match the voice below and let the body earn its place — a message exists so a future reader understands a decision they couldn't reconstruct from the diff.

### Subject line

- Imperative mood, capitalized, **no** trailing period: "Prevent double-filtering of labels", "Introduce category methods", "Optimize initialization"
- Wrap code identifiers in backticks: "Refactor `TopSecret::Text::GlobalMapping`"
- Keep it under ~50 characters where you can
- Add a semantic prefix only when it carries real information: "Breaking change: Validate labels"
- Do **not** append `(#123)` PR-number suffixes — those are added by GitHub on merge, not by hand

### Body

Include a body whenever there's a _why_ worth recording, which is most of the time. Skip it only for changes so self-evident the subject says everything ("Fix typo in README"). When you write one:

- Blank line after the subject, wrap prose at ~72 characters
- **Explain the why, not the what.** The diff already shows what changed. Say what problem this solves or what it makes possible.
- **Be concise.** A few tight sentences beat a wall of text. Cut anything that just restates the code.
- **Call out anything surprising, or alternatives you tried.** If there was a simpler approach you rejected, say why — that's exactly what saves a future reader from re-treading it.
- **Flag risks and dependencies.** A migration that needs care, a change that depends on another PR shipping first, a config value that must be set in production — name it.
- **Write for a non-technical reader.** Prefer plain language over jargon. Someone skimming the history to understand _what shipped and why_ should follow it without reading the code.
- **Reference issues or PRs only when it's obvious** which one applies — e.g. the branch clearly maps to a PR (check `gh pr view` if a PR exists) or the user named it. Never invent or guess a number. Use reference-style markdown links, matching the examples.

### End every commit with the Claude co-author trailer

Attribute the commit to Claude with a `Co-Authored-By` trailer on its own line, after a blank line:

```
Co-Authored-By: Claude <noreply@anthropic.com>
```

Use whatever trailer this Claude Code session normally appends. It often names the specific model, and that name changes from one model and version to the next (for example `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>` or `Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>`). Credit the model you're actually running rather than copying a fixed version from these examples — the point is to attribute the commit to Claude, not to assert one exact build.

This is attribution metadata and is expected — it is _not_ the "AI-generated writing" the next section warns about.

## Voice and tone

Write the way the user writes. The prose should read like a careful engineer explaining a decision to a teammate — never like a language model. Concretely, strip the tells of AI-generated writing:

- No hype or filler adjectives ("comprehensive", "robust", "seamless", "powerful", "significantly")
- No throat-clearing ("It's worth noting that", "In order to", "This change aims to")
- No summarizing the diff back as a bulleted list of file edits
- No em-dash-heavy, uniformly-hedged cadence — vary sentence length like a person does

Reach for the framings the user actually uses:

- "Prior to this commit, we were making multiple passes over the substituted text, resulting in labels being filtered. This commit substitutes the text on one pass."
- "In an effort to support dynamically generating predicate methods, we first need to ensure labels are formatted consistently."
- "Now that RubyLLM::TopSecret is live, we should promote the project here to help with discoverability."
- "Although a simpler approach exists, it's not practical because..."

### Worked examples

**Example 1 — a cohesive feature, one commit:**

```
Introduce `TopSecret::Text.scan`

There are cases where callers want to know whether text contains
sensitive information without filtering it. `scan` answers that
question and returns the mapping it found.

`filter` now uses `scan` internally, which is a small speed-up: we
skip the filtering work entirely when the input has nothing sensitive
in it.

Relates to the discussion in #50.

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Example 2 — a risk worth flagging:**

```
Cache `Mitie::NER`

Initializing `Mitie::NER` is expensive, so we cache it behind a Mutex
to keep it thread-safe.

We tried the simpler approach of memoizing without a lock (#85), but
it breaks when assets are precompiled at deploy time: the model file
doesn't exist yet, so the first cache write fails. The Mutex version
was tested in a production-like environment — the first request is
slow, every request after is fast.

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Example 3 — trivial change, subject only:**

```
Fix typo in installation instructions

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Step 5: Report what you did

After committing, show the user the result — `git log --oneline` of the new commits is usually enough — so they can see how you grouped and worded things. If you made a judgment call worth knowing about ("I split the bug fix out from the feature"), say so in a sentence.
