---
name: expertise-to-procedure
description: |-
  Use when turning tacit expert know-how into a durable skill, playbook, or checklist.
  Triggers:
practices:
- code-complete
- refactoring
hexagonal_role: supporting
consumes: []
produces:
- playbook
- checklist
- skill
context_rel:
- kind: customer-of
  with: skill-builder
skill_api_version: 1
context:
  window: isolated
metadata:
  tier: knowledge
  stability: experimental
  dependencies: []
output_contract: 'file: a playbook/checklist/skill capturing the expert procedure'
user-invocable: false
---
# expertise-to-procedure — turn "what I know" into "what the system knows"

> **Purpose:** Capture how an expert actually performs a task and freeze it into a
> durable, reusable asset (playbook, checklist, or skill) so the procedure is
> repeatable, auditable, and not lost when the person leaves.

## ⚠️ Critical Constraints

- **Capture the REAL procedure, not the sanitized one.** Experts narrate the
  tidy version and skip the judgment calls. **Why:** the skipped steps (the
  "obviously you'd check X first") are exactly the tacit knowledge you are here
  to extract; the clean version is already in the docs and helps no one.
  - WRONG: "Step 3: review the config." (what does *review* mean here?)
  - CORRECT: "Step 3: grep the config for `replicas:`; if < 3 in prod, STOP and
    escalate — that's the failure that caused last quarter's outage."

- **Encode decisions, not just steps.** A linear recipe rots; the value is the
  branch points. **Why:** a checklist that can't say "if X then Y, else Z"
  loses the expert's judgment, which is the whole asset.

- **Every captured rule needs a trigger and an evidence anchor.** **Why:** a
  rule with no "when does this fire" never gets applied, and a rule with no
  "why / where this came from" gets deleted by the next editor who doesn't
  understand it. Cite the incident, the doc, or the session it came from.

- **The artifact must be executable, not admiring.** **Why:** a beautiful
  write-up nobody runs is a museum piece. The output is a checklist someone
  follows or a skill an agent invokes — verify by having a non-expert run it.

## Why This Exists

Most operational knowledge lives in one person's head. They do the task
correctly every time because of a thousand small judgments they can't fully
articulate — until they're on vacation, leave the team, or the bus finds them.
Then the procedure breaks in ways no one can debug, because the "how" was never
written down in a form anyone could follow. This skill is the method for the
conversion: tacit → explicit → durable → reusable. It turns a person-shaped
dependency into a system-shaped asset.

## Quick Start

1. Pick ONE task an expert does repeatably and others can't reliably reproduce.
2. Run the **Elicit → Structure → Encode → Validate** loop below.
3. Produce the artifact (default: a checklist; escalate to a skill if an agent
   will run it). Save it where the work happens.
4. Have a NON-expert execute it cold. Fix every place they stumble. Repeat
   until they succeed without asking the expert a question.

## Methodology — the Elicit → Structure → Encode → Validate loop

### Phase 1 — Elicit (get the real procedure out of the head)
- **Watch, don't ask.** If possible, observe the expert doing the task live and
  narrate-think-aloud. What they *do* beats what they *say they do*.
- **Mine the trail.** Pull from shell history, past sessions, PRs, runbooks,
  Slack threads — the expert's actual moves are recorded across these.
- **Hunt the branch points.** For each step ask: "When would you NOT do this?
  What tells you something's wrong here? What's the thing a newcomer always gets
  wrong?" Those answers are the tacit core.
- **Checkpoint:** you have a raw, messy transcript of steps + judgments + the
  "gotchas." Do not clean it yet.

### Phase 2 — Structure (impose a repeatable shape)
- Separate **steps** (do this) from **decisions** (if X then Y) from
  **invariants** (this must always be true) from **traps** (never do this).
- Order steps by actual sequence; mark which are gated on a decision.
- Name each decision's **trigger** (the observable that fires it).
- **Checkpoint:** the messy transcript is now a structured outline with explicit
  branch points and named triggers.

### Phase 3 — Encode (pick the durable form, then write it)
- **Choose the form** with the table below.
- Write it in the imperative, with verifiable steps (a command to run, a value
  to check), not vague verbs.
- Attach an **evidence anchor** to every non-obvious rule (incident, doc, date).
- **Checkpoint:** a saved artifact exists at the path where the work happens.

| I need to… | Produce | Why |
|---|---|---|
| Make a human reliably repeat a task | **Checklist** | Lowest friction; fast to write and run |
| Capture a multi-step method with judgment | **Playbook** | Holds branches, context, and rationale |
| Make an AGENT run it | **Skill** (`SKILL.md`) | Machine-invocable; use `skill-builder` |

### Phase 4 — Validate (prove it transfers)
- **The non-expert test:** a person who has never done the task runs the
  artifact cold. Every question they ask the expert = a gap in the artifact.
  Patch it. Repeat until zero questions.
- **The drift check:** re-run the artifact against a fresh instance of the task;
  confirm it still produces the right outcome.
- **Checkpoint:** non-expert succeeds unaided AND the artifact ran clean on a
  fresh case.

## Output Specification

- **Format:** Markdown. Imperative steps; an explicit "Decisions" section with
  `if / then / else`; an "Invariants" list; a "Traps" list; each non-obvious
  rule carries an evidence anchor `(source: <incident|doc|date>)`.
- **Filename / location:** save where the work is done — a `checklist.md` /
  `playbook.md` in the relevant repo, or a `SKILL.md` under `skills/<name>/`
  (hand off to `skill-builder` for the agent-runnable form).

## Quality Rubric

- [ ] A non-expert executed the artifact cold and succeeded without asking the
      expert a single question.
- [ ] Every step is verifiable — names a command to run or a concrete value to
      check, never a vague verb ("review", "handle", "make sure").
- [ ] Every branch point is captured as an explicit `if X then Y else Z`, with a
      named, observable trigger.
- [ ] Every non-obvious rule carries an evidence anchor (incident / doc / date).
- [ ] The artifact lives where the work happens, not in a docs graveyard.

## Examples

**Deploy-rollback expertise → checklist.** A senior SRE rolls back cleanly every
time; juniors cause secondary outages. Eliciting reveals the tacit rule: "always
drain the queue before scaling down, or in-flight jobs are lost." That branch
point was never in the runbook. Encoded as a gated step with the incident as its
evidence anchor — juniors now roll back unaided.

**Triage instinct → agent skill.** A lead triages bug reports by an unwritten
priority heuristic. Mining their past triage decisions surfaces the rule set;
structured into `if / then` decisions and encoded as a `SKILL.md` (via
`skill-builder`), an agent now does first-pass triage matching the lead's calls.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Non-expert keeps asking questions | Tacit steps still missing | Treat every question as a gap; add the answer as an explicit step |
| Artifact "works" but only for the expert | You captured steps, not decisions | Re-do Phase 2; surface the branch points and triggers |
| Rule gets deleted by a later editor | No evidence anchor | Attach the incident/doc/date so its purpose is legible |
| Artifact rots within weeks | It lives in a docs graveyard | Move it next to the work; wire it into the actual workflow |
| Expert says "it depends" and stalls | Decision elicitation too abstract | Walk concrete past cases; the dependency becomes the trigger |

## See Also

- `skill-builder` — scaffold the agent-runnable `SKILL.md` form of a captured procedure.
- `session-to-playbook` — mine a recorded work session into a reusable playbook.
- `forge` — mine transcripts into durable learnings.
- `curse-of-knowledge-audit` — catch the steps an expert skipped because they're "obvious."
