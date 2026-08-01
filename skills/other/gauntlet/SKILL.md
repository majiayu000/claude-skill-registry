---
description: >-
  Runs a Gauntlet Loop: turns an ambitious goal and optional quality references
  into a minimal builder/critic prompt judged against a concrete comparison
  bar, confirms with the user, then executes it as the lead agent until the
  output beats the bar or the user stops the run. Use for long-horizon goals
  judged against an inspectable reference. Long-running; spawns many subagents
  and edits project files.
disable-model-invocation: true
argument-hint: "<goal> [possible references or quality bars]"
---

# Gauntlet

Turn an ambitious goal into a builder/critic improvement loop judged against a
concrete quality bar, and run that loop until the output wins or the user
stops it.

The user's arguments are the goal, plus any references or quality bars they
mentioned. If no goal was given, ask for one.

Gauntlet prompts are modeled on Matt Shumer's prompt for the Claude-of-Duty
game:

> I want you to build a first-person shooter at the level of the most recent
> Call of Duty games. It should be utterly perfect, visually beautiful, with
> every single thing done at AAA quality—from textures to physics to anything
> you could think of.
>
> Fan out sub-agents and have sub-agents tackle each one individually so that
> the game is utterly perfect. You should /loop on each item and have a
> separate sub-agent check it visually to ensure it looks triple A. That
> separate sub-agent should be a really harsh critic, and if it doesn't look
> triple A, it should keep going.
>
> Don't stop until each sub-agent is utterly wowed with the quality when
> compared with the actual Call of Duty game. It should literally compare them
> side by side blind and say which one looks better. Do this in ThreeJS. /loop
> until it's utterly perfect. Fan out sub-agents and ultracode.

Copy its register — short, concrete, goal-first, harsh about quality — not its
literal tokens. `/loop` and `ultracode` there are one user's shorthand typed
into a live session; as commands they mean something else entirely. Never
carry slash commands or effort keywords into the prompt you write.

## 1. Choose the bar

Choose the strongest concrete bar that an agent can actually inspect and
compare its work against. If the user has not supplied one, propose a useful
comp or measurement that plays the same role for this task that real Call of
Duty screenshots played for the Claude-of-Duty game.

Then resolve it into something a fresh agent with no prior context can open:
file paths, a URL, a command that renders it, or screenshots saved to disk. A
bar that cannot be resolved that way cannot be judged against — say so and fall
back to the strongest one that can. Explain the chosen bar in one sentence.

## 2. Write the gauntlet prompt

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/constraint-doc-loading.md`
and load the docs it lists. The bar defines what "good" means from outside;
these define what this project requires from inside. The prompt carries both.

Write a short prompt in that register (minimal is better here — the lead agent
decides the specifics).

Give the lead agent the goal and the bar, but let it choose the approach. Tell
it to divide the goal into the smallest pieces that can be improved and judged
independently. For each important piece, it should fan out a builder and a
separate critic with fresh context.

Every critic prompt carries the resolved bar materials themselves — the paths,
URL, or command — plus the artifact under judgment, and nothing from the
builder: not its report, its reasoning, or its round history. A critic that
cannot open the bar grades from memory, which is the builder-grades-itself
failure this loop exists to prevent.

Each critic returns one of two verdicts: **beats the bar**, or the single
biggest remaining gap, which goes back for another round. It compares directly
against the bar — blind A/B when the artifacts allow it, side by side
otherwise. A piece is done when its critic returns *beats the bar*.

The run ends when every piece is done or when the user stops it — and in
practice it is usually the second. Never end it on your own: if a piece's last
two rounds close no gap its critic can still name, report the plateau to the
user and let them decide whether it is worth more compute. Stopping is their
call, not yours.

If the project has a test command, the suite stays green: a piece is not done
while its tests fail.

Have the lead agent maintain a simple live progress page that shows the work
evolving over time — a rendered HTML page when the work is visual, markdown
otherwise — at `.claude/gauntlet-progress.html` or `.md`. Keep the goal, the
resolved bar, this prompt, and every piece's rounds and verdicts in it, and
write it before dispatching each round, so it doubles as the anchor a later
session resumes from.

Do not prescribe the architecture, exact decomposition, or a fixed number of
rounds. Keep the prompt short, but short is a budget for phrasing, not licence
to drop guarantees: fresh-context critics, the bar materials in every critic
prompt, and the two-way verdict all survive to the final draft.

## 3. Confirm and run

Show the user the bar and the prompt. Recommend ultracode for serious runs
(`/effort` → ultracode), noting it has to be set before approving because the
run starts immediately after.

Run `git status --porcelain`. If it reports anything, say so before asking:
this run rewrites the same files for hours with no per-change approval, and
uncommitted work will not survive it. Offer `/optimus:worktree` or committing
first.

Then use `AskUserQuestion` — header "Gauntlet", question confirming the start
of a long-running multi-agent run that spawns many subagents, edits files
without per-change approval, and consumes credits in proportion to how long it
runs — with options "Start the run", "Adjust first", and "Cancel". Apply
requested adjustments and ask again. On "Cancel", stop.

On approval, execute the prompt yourself as the lead agent. There is no
arbitrary final round: the run ends when the output beats the bar or when the
user stops it. Long runs can leave pieces that are individually good but
slightly inconsistent with each other — offer a smoothing pass before closing.

Close on the outcome — uncommitted work → `/optimus:commit`; already committed
→ `/optimus:pr`, then `/optimus:code-review` in a fresh conversation — and say
plainly whether the run beat the bar, plateaued, or was interrupted, and
whether the suite is green.
