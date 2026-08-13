---
description: Generate and run a coder-eval activation suite for a Claude Code skill — does the agent actually engage it when it should, and leave it alone when it shouldn't? Use when the user asks whether a skill triggers, wants to test skill activation, or worries a skill has silently stopped firing.
allowed-tools: ["Read", "Glob", "Grep", "Write", "Bash"]
---

# Skill activation check

A skill only earns its keep if the model reaches for it at the right moment. That
decision is made almost entirely from the skill's frontmatter `description` — so
"does my skill trigger?" is a measurable question, and this is how you measure it:
build a labelled set of user requests, run a real agent against each one, and score
whether the skill was engaged.

The user's request is: `$ARGUMENTS`

## Step 1 — Locate the target skill

`$ARGUMENTS` may be a path to a `SKILL.md`, a path to the skill's **directory**, a
skill name, or empty.

- Empty: glob `.claude/skills/*/SKILL.md` and `**/skills/*/SKILL.md`. One match →
  use it. Several → list them and ask which. None → say so and stop.
- A directory: use the `SKILL.md` inside it.
- A name: find the matching skill directory.

The **bare skill name is the directory name** containing `SKILL.md`. Read the
frontmatter `description` and keep it in front of you: that string is what the model
matches against, so it is the primary input to row design and the thing you will end
up recommending edits to.

**Measure its length while you are there — two separate budgets truncate it, and either
one produces a low-recall result that looks exactly like bad wording.**

1. **Per-skill truncation.** `description` and `when_to_use` are concatenated and cut at a
   fixed character budget — **1,536 characters**, configurable via the
   `skillListingMaxDescChars` setting. Trigger text past the cutoff cannot affect
   activation at all, so it may as well not exist.
2. **The whole-listing budget, which matters more in exactly the repositories that run
   activation suites.** The listing always contains every skill *name*, but its total
   character budget scales at about **1% of the model's context window**, shared across
   **every** skill the user has installed. When it overflows, Claude Code drops
   descriptions **starting with the skills you invoke least**.

The second one has a consequence worth stating plainly: in a many-skill repository a skill
can score near-zero recall with a **perfectly good description**, because its description
was never in the listing. Rewriting the wording then fixes nothing. And the drop order is
least-invoked-first, so a *newly authored* skill — which is by definition rarely invoked,
and is exactly what someone runs this suite on — is the most likely victim. That is a
systematic bias against the skill under test.

Levers, if the listing is the problem: `skillListingBudgetFraction` (the 1% default), the
`SLASH_COMMAND_TOOL_CHAR_BUDGET` environment variable (a fixed character count), and
`skillOverrides` set to `"name-only"` to free budget from skills you do not need matched.

If the skill has **no `description`** in its frontmatter, stop and report that as the
finding — a skill with no description can never be model-invoked, so a suite would
score zero recall by construction and tell you nothing you don't already know.

## Step 2 — Confirm coder-eval is installed

Run `coder-eval --version`. Installing this plugin did not install the CLI, and the
suite cannot be validated or run without it.

If it is missing, follow `${CLAUDE_PLUGIN_ROOT}/reference/cli-setup.md`: offer the
install, **ask before running it**, and confirm with `coder-eval --version`
afterwards. Never install unprompted, and do not continue if the user declines.

That reference also covers the other half of the version check — whether this project
pins a coder-eval version, and what to do when the installed one does not match it.

## Step 3 — Check what already covers this skill

Before designing anything, look at what the repository already has. Locate the task tree
per `${CLAUDE_PLUGIN_ROOT}/reference/repo-layout.md` and glob it for a task carrying a
`skill_triggered` criterion.

**If an existing suite already names this skill**, report its coverage — how many
positive and distractor rows, which `suite_thresholds` it gates on — and **offer to
extend it** by appending rows to its dataset, rather than scaffolding a parallel suite.
Two suites for one skill drift apart and the user pays for both on every run. Scaffold
only when nothing covers this skill, or when the user chooses to after seeing what is
there.

Two things worth reporting rather than silently working around:

- **An existing suite with no distractor rows.** Precision is 1.0 by definition, so half
  its result is meaningless. Offer to add distractors — a real improvement over both
  scaffolding a rival suite and saying nothing.
- **A neighbouring suite that names a *different* skill.** That is not coverage. Go ahead
  and scaffold, and say why the neighbour did not count.

**Then check where `agent.plugins` should come from.** If an experiment the task will
resolve against already supplies that block, **inherit it and do not write one** — a task
that redeclares what the experiment provides drifts from it, with nothing to catch the
divergence. Write the template's own block only when nothing already exposes the skill to
the sandbox. If several experiments exist and it is unclear which one this task resolves
against, ask rather than guess.

## Step 4 — Design the rows

This step is the whole experiment. The rest is mechanics.

**Positive rows** — requests a real user would plausibly make that the description
claims to cover. Paraphrase; never copy phrasing out of the description. A row lifted
from the description tests string matching, not activation. Vary the vocabulary and
include at least one oblique row where the user describes their *problem* rather than
the operation the skill performs.

**Distractor rows** — adjacent requests the skill should *not* claim, especially ones
that share vocabulary with the description. These are what make precision meaningful.

**Sibling-owned rows** *(optional)* — requests that legitimately belong to a **named
other skill in the same repository**, with `expected_skill` set to that sibling. In a
multi-skill repository, misrouting between two adjacent skills is the common failure, and
a plain distractor only shows *that* a misfire happened, not *where it went*. These rows
say where.

Add them when two skills have overlapping subject matter and you want to know which one
wins. They cost extra rows, and **every row is a full agent run** — so treat them as a
targeted follow-up, not a default.

**Never name the skill in a prompt.** That tests obedience, not activation:

- Bad: "Use the pdf-forms skill to fill in this application."
- Good: "I need to fill in the fields on this application PDF and send it back."

This rule is unaffected by sibling-owned rows: `expected_skill` is a **label** in the
dataset, read by the criterion and never shown to the agent. The row's `prompt` still must
not name any skill, the sibling included.

**Sizing.** Minimum 3 positive + 3 distractor. Aim for **8–12 of each** for a signal
you can act on — recall over 3 rows moves in 33-point jumps, which is too coarse to
tell a real regression from noise. The shipped template holds 6 rows because that is
the illustrative minimum, not a target. Any sibling-owned rows are **on top** of that:
8–12 positives plus 8–12 distractors is already 16–24 runs, so state the resulting total
before writing the suite.

**Refuse to generate a suite with no distractor rows.** With no negatives, precision
is 1.0 by definition and half the result is meaningless. Say why and ask for the
adjacent cases instead.

## Step 5 — Write the suite

Copy the two template files into the user's task tree, located by following
`${CLAUDE_PLUGIN_ROOT}/reference/repo-layout.md` (if the repository has none, propose a
location and ask):

- `${CLAUDE_PLUGIN_ROOT}/reference/templates/activation.yaml`
- `${CLAUDE_PLUGIN_ROOT}/reference/templates/activation-rows.jsonl`

Then substitute, keeping the JSONL beside the YAML (`dataset.paths` entries resolve
relative to the task file):

- `task_id` → `<skill-name>-activation`
- `skill_name` → the **bare** skill name
- each positive row's `expected_skill` → the same bare name; distractor rows keep `""`;
  a sibling-owned row's `expected_skill` → that **sibling's** bare name
- every row's `prompt` → the requests designed in step 4, one JSON object per line

**Then make the skill reachable, which is the step that decides whether the suite measures
anything.** The task runs in a fresh sandbox that contains none of the user's files, so the
agent is offered no skills unless the task says where they live. That is the `agent.plugins`
block in the template — and it is the template's job only **when nothing already exposes the
skill**: if step 3 found an experiment supplying that block, inherit it and delete the
template's copy rather than writing a second declaration.

Otherwise, fill it in: `path` is the directory **containing** the skill's own directory —
for `.claude/skills/pdf-forms/SKILL.md` that is `.claude/skills`. Tell the user to export it
before running, and to use the same variable in CI:

```bash
export SKILL_SOURCE_PATH="$(pwd)/.claude/skills"
```

Keep it an environment variable rather than baking an absolute path into the YAML — the
suite is committed and re-run on other machines. If the variable is unset the skill is simply
absent, every positive row scores 0, and the result is indistinguishable from a skill that
never triggers, so confirm it is set before reporting any low-recall finding.

`skill_name` must be the bare name even when the skill comes from a plugin and is
invoked as `plugin:skill` — the checker strips the namespace before comparing. A
namespaced value here silently scores zero recall on every row, which reads exactly
like a broken skill.

For criterion fields beyond this template, read
`${CLAUDE_PLUGIN_ROOT}/reference/criteria.md`.

## Step 6 — Validate before spending anything

`coder-eval plan <path-to-activation.yaml>` must exit 0. It is a schema check only —
it does not read the dataset file — so also confirm the JSONL sits next to the YAML
and has one object per line.

## Step 7 — Run

Every row is a full agent run: **N rows means N runs and real token cost**. State the
row count and the agent/model that will be used, then ask before starting.

```bash
coder-eval run <path-to-activation.yaml>
```

The criterion is agent-agnostic — it detects Claude engaging the skill via the `Skill`
tool, and any agent without that tool (Codex, for instance) by reading the skill's
files off disk — so the same suite works whichever agent the task resolves to.

## Step 8 — Report and interpret

Present recall, precision, F1 and the confusion matrix, then say what they mean:

- **Low recall** (misses rows it should have caught): **rule out truncation and listing
  eviction before concluding the description under-claims.** Both produce a low-recall
  result indistinguishable from bad wording, and both are cheap to check: `/doctor`
  estimates the listing's context cost and its biggest contributors, and the **Skills row
  in `/context`** reports the listing size *after* the budget is applied — that is what the
  model actually received. Only once the description is demonstrably *in* the listing and
  inside the per-skill cutoff is the wording the culprit: it does not name the situations,
  file types, or phrasings that should trigger it.
- **Low precision** (fires on distractors): the description over-claims and is
  stealing adjacent requests. Narrow it, and say explicitly what the skill is *not*
  for.
- **Misfires concentrated on one sibling** (with sibling-owned rows): that is a boundary
  dispute between two descriptions, not one vague description. Fixing the skill under test
  alone tends to move the failure rather than remove it — say explicitly what **each** of
  the two skills is not for, and re-run.
- **Both high**: report the numbers and the row count, and note that a small suite
  says little — offer to widen it.

Point at the frontmatter `description` as the thing to edit, quote the specific rows
that failed as evidence, and offer to re-run after the edit so the change is measured
rather than assumed. Re-running the same suite after a description change is the whole
point: it turns skill wording from taste into a number that moves.
