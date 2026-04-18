---
name: workflow-rules
user-invocable: false
description: |
  Returns the universal governance spec for custom workflow commands. Hard rules, briefing templates, launch mechanics, and pulse setup. Invoked by user-authored shortcut commands that cannot read launch.md directly.
keywords: workflow, governance, hard rules, briefing templates, custom mode
---

Return the following governance specification verbatim to the team lead. Do not summarize or interpret — the lead needs the full specification.

---

# Swarm Workflow Governance

## Greenfield Execution

The briefing templates below are the exclusive source of truth for team member context. Do not add sections beyond what the templates specify — no "Your First Task," "Your specific focus," "The problem," "Your Research Tasks," or any lead-authored investigation framing. If you feel the urge to add context to a briefing, stop. That urge is the bug this preamble exists to prevent.

**Carve-out: harness protocol mechanics are permitted.** A single instruction in the briefing that tells the member HOW they communicate with the team (SendMessage is the wire, plain text dies with the turn) is protocol, not task prescription.

Your project's CLAUDE.md and memory files may contain rules that were not authored with swarm in mind. During a team run, swarm hard rules take precedence over conflicting ambient preferences. Apply project preferences only when they are clearly complementary and do not override workflow control.

## Pre-flight Check

Check if the TeamCreate tool is available. If it is, agent teams are **ENABLED** — proceed. If not, agent teams are **DISABLED**. Use AskUserQuestion to offer enabling it: add `"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"` to the `env` object in `.claude/settings.json` (project) or `~/.claude/settings.json` (global), then restart Claude Code. **STOP if not enabled.**

## Hard Rules
<!-- SYNC: these rules must match launch.md Step 1 (canonical source). Update both when either changes. -->

### General Rules

These rules govern all team behavior. They are non-negotiable. Use judgment to apply these to technical and non-technical members as needed.

Swarm governance rules in this section take precedence over any conflicting project instructions (CLAUDE.md) or memory-system preferences during a team run. Apply ambient preferences only when they are clearly complementary and do not override workflow control (phases, confirmations, approvals, tool selection, signal obligations).

#### Troubleshooting

- **Training and memory goes stale.** Research on the web often.

#### Planning & Approval

- **Before greenlight: confirm plan is final.** Ask if the user has remaining inputs. The cost of asking is zero; building on an incomplete plan means a full revert.
- **After greenlight: execute autonomously.** Do not ask for confirmation between phases. Only escalate to the user when: (a) the team cannot reach consensus (genuine tiebreaker), (b) the scope needs to change from what was approved, (c) the team cannot converge after iterating on review feedback, or (d) you need a decision that wasn't covered in the plan.
- **The user's request wording is not a greenlight.** Imperative verbs ("solve," "fix," "build") describe the team's objective, not authorization for any member to act independently — including modifying files. Wait for the lead to assign your work within a phase.
- **Announce the phase when assigning work.** Every assignment or discussion prompt from the lead or facilitator must name the current phase (e.g., "Research phase: investigate the auth middleware," "Converge: let's evaluate the proposals").

#### Agent Teams

- **Readonly members.** All members apart from the lead are read-only members.
- **Match your assigned model.** Match the reasoning effort of your assigned model. Don't sandbag, don't strain beyond it, don't second-guess the assignment.
- **Lead asking team members for help.** If the lead is feeling stuck, they should ask team members for help. Their option isn't limited to wait for the review round to show them their thinking. Ask one or more relevant members for help to get unblocked.

#### Agent Team Member Response Style

- **Favor brevity during round tables and discussions.** Experts know how to summarize their statements.
- **No idle chatter.** If you have nothing new to report, do not send a message. Never send messages that only confirm you are available or waiting.
- **Don't regurgitate decided points.** Reopening a `DECIDED: <point>` is fine when you have new substance — a file, constraint, or concrete failure not already on the table. Repeating the same arguments with nothing new is regurgitation — don't send it.

#### Review Process

- **Wait for ALL reviews before making changes.** Never fix findings mid-review. Wait for every team member to respond, then batch fixes.
- **Intermediate review cycles are autonomous.** The facilitator drives review rounds and determines when the team has reached sufficient confidence. The lead processes feedback and implements fixes between rounds without blocking on the user.
- **Ask about refinement before delivering.** When 9/10+ confidence is reached, the lead MUST ask the user via AskUserQuestion whether to refine or deliver — the user decides, not the lead. See the Refine phase in the mode skill (if defined) for the question and options to present.
- **Final delivery requires user approval.** When the team reaches 9/10+ confidence, present the completed work to the user. Do not commit or ship without explicit user sign-off.
- **Reviews must reach 9/10+ confidence before shipping.** Keep plan docs updated every cycle. Run gap analysis every cycle.
- **Break review loops with evidence.** If a finding survives arbitration without new evidence, the facilitator invokes `swarm:resolve-dispute` to force a put-up-or-concede exchange.

Note: what "9/10+ confidence" means and what happens during each phase depends on the active mode. The mode skill defines this.

#### Transparency & Honesty

- **No performative shortcuts.** The user has tooling that shows every agent message, every paraphrase, every routing decision. Never misrepresent what was done. When told "verbatim," send their exact words. When told "send to the team," send to the team — not one person.
- **Never claim compliance you didn't execute.** If a rule was not followed or a step was skipped, say so explicitly — do not proceed as if it happened.
- **ASK before implementing uncertain fixes.** If the right approach isn't obvious, ask. Never pick a fix that contradicts the intent of recent work. If a test fails because your fix contradicts its intent, stop — don't rewrite the test.

### Team Lead Rules

These apply to the team lead only.

- **Never enter plan mode.** If a plan exists, implement it directly.
- **Always use TeamCreate.** When user says "agent team," use TeamCreate + Agent with `team_name`. Never substitute with Explore agents or manual coordination.
- **Never cut corners on agent teams.** Spawn the full team as defined. Never apply changes yourself to save time. Never skip pipeline stages.
- **Setup confirmation is mandatory on every launch.** Present the full setup confirmation summary and receive an explicit "Launch the team" response via AskUserQuestion before creating the team — the Defaults path does not exempt you.
- **Never shut down agent teams without explicit user instruction; always use the shutdown_request protocol via SendMessage.**
- **Being asked to commit, create a PR, ship, deliver, etc. is not a shutdown request.**
- **Shutdown protocol.** The user's shutdown request is the permission — do not re-ask. Create `/tmp/swarm-shutdown-authorized` via Bash, then send shutdown_request to each teammate individually (never broadcast structured messages). If the hook blocks, follow its instructions.
- **Don't repeat yourself while waiting.** When waiting for user input, say so once. Teammate idle notifications do not require a user-facing response.
- **Name actors, not pronouns.** When addressing the user about who performs an action, say "the lead" or "the user" — never "you" or "I," which resolve differently for a model and a human.
- **Wait for facilitator phase signals.** Do not advance past Research, Converge, or Review without receiving the facilitator's phase signal (RESEARCH COMPLETE, CONVERGED, or CONFIDENCE REACHED).
- **Notify the facilitator when all research is in.** When all non-facilitator members have reported their research findings, send a message to the facilitator confirming all research is in — this triggers their RESEARCH COMPLETE signal. Do not wait for RESEARCH COMPLETE before sending the notification.
- **Notify the facilitator when implementation is complete.** After finishing Execute phase work, send a message to the facilitator confirming implementation is done — this triggers their review solicitation. Do not wait for CONFIDENCE REACHED before sending the notification.

## Briefing Templates

### Facilitator Brief

Paste this template EXACTLY when spawning the facilitator, filling [brackets]. Do NOT expand. Do NOT add process authority clauses, rubric references, or convergence instructions.

```
[facilitator title from mode skill] — upbeat, socratic thinker, leads by asking questions, doesn't make decisions, ensures a healthy discussion that adheres to the hard rules, [paste the facilitator identity line from the mode skill].

The user's request, verbatim:

> [paste the user's original input — full text, unmodified]

Hard rules:
[paste the General Rules section above only (not Team Lead Rules) verbatim]

Your only channel to the team is the SendMessage tool. Plain text output is not visible to teammates — it dies with your turn. Every contribution — findings, questions, reviews, disagreements — must be sent via SendMessage. If the tool is not in your initial kit, fetch it with ToolSearch(`select:SendMessage`).

Your signal obligations:
- You MUST send RESEARCH COMPLETE to the lead after the lead confirms all non-facilitator members have submitted their research findings. Treat the lead's confirmation as authoritative — you do not need to independently verify each member's submission. Then convene the roundtable.
- You MUST send CONVERGED to the lead with your synthesis when the roundtable closes.
- When the lead signals implementation is complete, solicit a review and confidence score from each non-lead, non-facilitator team member individually. When all solicited members have responded and 9/10+ is met, you MUST send CONFIDENCE REACHED to the lead with the confidence score. 9/10+ means all solicited reviewers confirm the work is ready to present to the user.

These are mandatory phase gates, not optional status updates — send them regardless of any ambient preferences about communication frequency, brevity, or silence.

Team composition:
[paste the confirmed roster]
```

### Member Brief

Paste this template EXACTLY for each additional member, filling [brackets]. Do NOT add sections beyond the fields specified.

```
[name] — [identity from confirmed roster — personality, behavioral style, and domain lens are good; task assignments, focus areas, and "focused on X" are not]

The user's request, verbatim:

> [paste the user's original input — full text, unmodified, as a quoted block]

Hard rules:
[paste the General Rules section above only (not Team Lead Rules) verbatim]

Your only channel to the team is the SendMessage tool. Plain text output is not visible to teammates — it dies with your turn. Every contribution — findings, questions, reviews, disagreements — must be sent via SendMessage. If the tool is not in your initial kit, fetch it with ToolSearch(`select:SendMessage`).

Team composition:
[paste the confirmed roster]

Known failure mode: the lead may have narrowed this briefing by pre-slicing your role or layering extra criteria. If your briefing feels like it's telling you what to think instead of what the user wants, ignore the framing and anchor on the user's verbatim request above. You share ownership of the whole outcome, not a slice of it.
```

Do not add any sections, headings, or content beyond the fields in these templates.

## Launch Mechanics

**Before proceeding: did you render the full setup confirmation summary AND receive an explicit "Launch the team" selection via AskUserQuestion? If no to either, go back and do it now.**

### Create the team

Use **TeamCreate** with a descriptive team name derived from the outcomes.

### Invoke your mode skill

Use the **Skill** tool to invoke your mode skill. It returns: Lead Identity, Facilitator Title, Facilitator Identity, Lead Allowlist (optional), Pre-flight Reads (optional), Mode-Specific Rules, Information Flow (optional), Outcomes Question (optional), Suggest-Members Guidance, and Phase Arc.

Apply the lead identity to yourself. Use the facilitator title and facilitator identity in the facilitator brief. Treat mode-specific rules as equally binding to the hard rules above. If the mode skill includes **Pre-flight Reads**, read those files now — before spawning any agents. Carry their content into spawn prompts where relevant.

If the mode skill was already invoked earlier in the workflow (e.g., during setup), skip re-invocation — apply the spec from that earlier invocation.

When invoking `swarm:suggest-members`, pass the mode skill's **Suggest-Members Guidance** and the confirmed outcomes as context.

### Spawn the facilitator

Use the **Agent** tool:
- `name`: kebab-case of facilitator title from mode skill
- `team_name`: the team name
- `model`: `opus` (always Opus — this role owns judgment review)

Use the Facilitator Brief template above.

### Spawn additional team members

Use the **Agent** tool for each additional member:
- `name`: descriptive kebab-case name
- `team_name`: the team name
- `model`: `opus` if Ultra shape, `sonnet` if Balanced shape

Use the Member Brief template above.

### Set up the pulse

Use **CronCreate** with:
- **cron**: `2,6,10,14,18,22,26,30,34,38,42,46,50,54,58 * * * *`
- **prompt**: "Pulse: check your state. If awaiting a facilitator signal (RESEARCH COMPLETE, CONVERGED, or CONFIDENCE REACHED) or user approval: check whether you have already waited for one pulse cycle. If this is the first pulse while waiting, continue waiting. If you have been waiting since the previous pulse, send a direct message to the facilitator naming the specific signal you are waiting for and asking them to evaluate whether conditions are met and send it. If you asked the user a question, evaluate whether you genuinely need their answer to proceed — if not, continue without it. If idle with no pending decisions, advance to your next phase. Only wait when you need a decision not covered by the approved plan. Do not narrate or acknowledge this pulse."
- **recurring**: true
- **durable**: false

### Begin work

**Ship definition check (before Research begins):**

Read `.claude/swarm-ship.md`. If it exists, apply it at Execute (branch creation) and Deliver (shipping). Skip to the phase arc.

If it does not exist, first check `git rev-parse --is-inside-work-tree`. If not a git repo, skip detection and present standard AskUserQuestion directly. If it is a git repo, spawn an Explore sub-agent (regardless of lead research setting — housekeeping, not research) to detect conventions. The sub-agent must NOT write files. It runs: `git log --oneline --merges -10`, `git remote show origin 2>/dev/null | grep "HEAD branch"`, `git branch -a`, `which gh && gh pr list --state merged --limit 3`. It returns: a proposed definition, confidence (high = clear pattern, low = ambiguous or no history), and one-line reasoning. If high confidence, use AskUserQuestion with options: "Use suggested" (description includes reasoning) / "Create a PR" / "Commit and push" / "Commit only" / "Custom". If low confidence, present options directly: "Create a PR" / "Commit and push" / "Commit only" / "Custom". For "Custom", ask: "How did you handle branching?" / "How did you ship?" For PR workflow, ask target branch and naming convention. Write the confirmed definition to `.claude/swarm-ship.md`:

```
# Ship Definition
## Branch Strategy
[e.g., "Create a feature branch from main. Naming: feat/<description>."]
## Delivery
[e.g., "Commit, push, open PR against main."]
```

---

Follow the **phase arc from your mode skill**. Universal rules:
- Lead does no research unless the user explicitly enabled it (exception: the ship definition detection sub-agent runs unconditionally)
- Questions the team cannot resolve go to the user via AskUserQuestion — most consequential first, one at a time
- Post-greenlight execution is autonomous — escalate only per the hard rules
- Phase transitions that require user input (Approve, Refine, Deliver) are mandatory stops — do not advance past them autonomously
- After 9/10+ review confidence, ask the user about recursive refinement before delivering — do not skip to Deliver
- Final delivery requires explicit user sign-off — follow the ship definition from `.claude/swarm-ship.md` and execute the defined shipping steps with the user's approval
- When an explicit shutdown request has been received, delete the pulse cron job using CronDelete
