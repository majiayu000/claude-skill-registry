---
description: Set up coder-eval in this repository — scan for what is worth evaluating (Claude Code skills, an MCP server, a CLI), then scaffold a task directory with one real, passing-or-failing task and the exact command to run it.
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Write", "Bash"]
---

# Set up coder-eval in this repository

Goal: leave the user with a task directory containing **one real task** they can run
immediately, not an empty scaffold. The task must exercise something this repository
actually ships.

The user's request is: `$ARGUMENTS`

## Step 1 — Check prerequisites

Run `coder-eval --version`. Installing this plugin did not install the CLI, and
every later step needs it.

If it is missing, follow `${CLAUDE_PLUGIN_ROOT}/reference/cli-setup.md`: offer the
install, **ask before running it**, and confirm with `coder-eval --version`
afterwards. Never install unprompted, and do not continue if the user declines.

That reference also covers the other half of the version check — whether this project
pins a coder-eval version, and what to do when the installed one does not match it.

## Step 2 — Check whether this repository is already configured

This skill scaffolds a first suite. Run against a repository that already has one, it
would write a "first task" beside an existing tree and report success — so find out
before writing anything.

Locate the eval tree per `${CLAUDE_PLUGIN_ROOT}/reference/repo-layout.md`. **If the
repository already has tasks, report the inventory and stop**: how many task files and
where, how many run directories, and whether there are experiments. Then point the user
at the skills that act on what exists —

- `/coder-eval:lint-tasks` to review the tasks already there;
- `/coder-eval:analyze` to read a finished run.

Only scaffold if the repository has none, or if the user explicitly asks for more after
seeing the inventory. **Never overwrite an existing task file**, whatever they ask for;
add alongside it.

A repository with tasks but no experiments is **partially** configured, not empty.
Report that as it is and offer the missing piece — do not scaffold a first task as
though there were nothing there.

## Step 3 — Scan for what is testable

Look for these, in priority order, and **report what you found before writing
anything**:

1. **Claude Code skills** — glob `.claude/skills/*/SKILL.md` and `**/skills/*/SKILL.md`.
   Skills are the highest-value thing to evaluate, because whether they trigger is
   invisible until it fails. If you find any, recommend `/coder-eval:check-skill` for
   each of them — that is a purpose-built activation suite, not something to hand-roll
   here.
2. **An MCP server** — an `.mcp.json`, an `mcpServers` key in `package.json` or
   `pyproject.toml`, or a server entry point (a `server.py` / `index.ts` that registers
   tools). Note which tools it exposes.
3. **A CLI entry point** — `[project.scripts]` in `pyproject.toml`, `bin` or `scripts` in
   `package.json`, or a `Makefile` with usable targets.

If the repository is a monorepo with many skill or package directories, cap the scan
and ask which subtree to focus on rather than reporting fifty candidates.

If you find **nothing** in these three categories, say so plainly. Then offer the
smallest useful thing instead — a task that runs a script or test command the repo
already has and checks its output — rather than scaffolding an empty suite that proves
nothing.

## Step 4 — Scaffold one real task

Write into the tree step 2 resolved. If the repository has none, propose a location and
ask. Step 2's never-overwrite rule still applies here — it is the one place that rule
lives.

Write one task derived from what step 3 found:

- **A CLI** — a task whose prompt asks for something the CLI does, with criteria that
  check the resulting file's *content*, not just that a file appeared.
- **An MCP server** — a task that exercises one specific tool and verifies its effect.
- **Skills** — point at `/coder-eval:check-skill` instead; an activation suite is a
  different shape from a capability task and that skill builds it properly.

Prompts instruct, criteria validate. Do not restate in the prompt what the criteria
check — a prompt that says "make sure the file contains X" tests reading
comprehension, not capability.

Before writing the criteria, read `${CLAUDE_PLUGIN_ROOT}/reference/task-rubric.md`. It is
the shared checklist for whether a task can pass for the wrong reason, and the one task you
scaffold here is the example every later task in this repository gets modelled on — so it
is worth getting right rather than fixing later. For criterion types and their fields, read
`${CLAUDE_PLUGIN_ROOT}/reference/criteria.md`.

Use `/coder-eval:task` if the user wants more tasks after this one; it is the same
authoring loop with a natural-language brief.

## Step 5 — Environment variables

Write the variables the chosen agent needs (e.g. `ANTHROPIC_API_KEY` for the default
`claude-code` agent) to **`.env.example`** — create it or append to it.

Never write `.env`: it may already hold real secrets. If `.env` does not exist, check
whether it is gitignored before suggesting the user create one, and say so if it is
not.

## Step 6 — Validate

Run `coder-eval plan <task-directory>/*.yaml` and iterate until it exits 0. This
validates the task schema through the real models, so a field name you guessed wrong
surfaces here. `plan` takes task *files*: a bare directory argument is rejected
outright (`Expected a YAML task file but got a directory`), so always pass explicit
paths or a glob. Do not suggest `coder-eval plan` with no argument — zero-argument
discovery only works from a coder-eval source checkout and exits 1 anywhere else.

An empty or task-less directory does not produce a meaningful success — if `plan`
reports no tasks, treat that as a failure to scaffold, not a pass. Note that the
bare-directory error is a different outcome: that one means you passed the wrong
argument shape, not that the scaffold is empty.

## Step 7 — Report

Tell the user:

- what you found in the scan, and what you chose to evaluate first;
- the exact command to run it: `coder-eval run <path>`, plus a note that it costs real
  tokens and needs the credentials from step 5;
- that `/coder-eval:check-skill` is the next step if the repo ships skills;
- that `/coder-eval:analyze` reads the run directory afterwards, and `/coder-eval:ci`
  turns the suite into a GitHub Actions gate.
