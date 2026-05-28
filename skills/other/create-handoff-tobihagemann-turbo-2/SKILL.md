---
name: create-handoff
description: "Write a handoff file at .turbo/handoff/<YYYY-MM-DD>-<slug>.md capturing current session state — task, status, open decisions, in-flight changes, next step — so a fresh session can continue without re-deriving context. Use when the user asks to \"create a handoff\", \"create handoff\", \"save handoff\", \"handoff before compact\", \"save session state\", \"handoff for next session\", or \"capture session state\"."
---

# Create Handoff

Write a session handoff file at `.turbo/handoff/<YYYY-MM-DD>-<slug>.md` so a fresh session can pick up where this one left off.

## Step 1: Resolve the Target Path

Get today's date: `date +%Y-%m-%d`.

Pick a slug for the current task:

- Lowercase
- Replace non-alphanumeric characters with hyphens
- Collapse consecutive hyphens
- Trim leading and trailing hyphens
- Truncate to 40 characters at a word boundary

If the work is anchored to an existing artifact (a plan at `.turbo/plans/<slug>.md`, a shell at `.turbo/shells/<slug>.md`, or a spec at `.turbo/specs/<slug>.md`), reuse that artifact's slug verbatim.

The user may pass an explicit slug or path; honor it.

The target path is `.turbo/handoff/<YYYY-MM-DD>-<slug>.md`. If the path already exists, append `-2`, `-3`, etc. until the path is free.

State the chosen path before continuing.

## Step 2: Gather Session State

Run `git status --short` to see uncommitted changes in the working tree.

Survey the conversation context for:

- **Current task**: what is being worked on, in one or two sentences
- **Workflow status**: where in the workflow this session is (drafting, refining iteration N, applying findings, implementing step M of K, investigating, blocked on Q, etc.)
- **Active artifact**: path to the plan, shell, spec, or other file at the center of the work, if one exists
- **Open decisions**: questions raised but not resolved, choices the user is still weighing, escalations awaiting input
- **In-flight changes**: staged or unstaged edits that are not yet committed; what each change is doing and what is missing
- **Next step**: the first concrete action the new session should take

When something is genuinely unclear and would leave a gap in the handoff, use `AskUserQuestion` to resolve it. Default to inferring quietly when the conversation makes the answer clear.

## Step 3: Write the Handoff File

Create `.turbo/handoff/` if it does not exist. Write the file at the path picked in Step 1.

Lead with `# Handoff: <Task Title>`. Cover the items gathered in Step 2 in whatever structure fits the session — drafting, refining, implementing, and investigating sessions each have different shapes and don't all map to the same headings. Close with a clear statement of the next concrete action so the new session knows exactly what to do first.

Keep it dense. Omit anything that has no real content.

## Step 4: Confirm

Tell the user where the handoff was written and quote the next-step statement so the path forward is visible at a glance.

Then use the TaskList tool and proceed to any remaining task.
