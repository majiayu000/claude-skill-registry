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

Read `~/.claude/settings.json`. If `autoMode.environment` is absent or contains no string mentioning a source-control hostname (e.g., `github.com`, `gitlab.com`, `bitbucket.org`, `github.example.com`), show the user a block to paste — `autoMode.environment: ["$defaults", "Source control: <host>/<org>. Creating feature branches, pushing them for the first time, and opening pull requests against the configured target branch is part of the standard development workflow."]` — and explain it must live in user scope (the classifier ignores project-scoped `autoMode`). Run `git remote get-url origin 2>/dev/null` to extract `<host>` and `<org>` and substitute them into the shown block. Check for `ssh://` prefix first to disambiguate SSH-with-port from SSH-shorthand. Handle three URL forms in this order: SSH-with-port (`ssh://git@host:port/org/repo.git` — strip the port), SSH shorthand (`git@host:org/repo.git`), HTTPS (`https://host/org/repo.git`). Fall back to `<your-host>` / `<your-org>` placeholders if no remote exists. Phrase the question as "is missing or doesn't declare" since the file may not exist on a fresh install, and add a parenthetical noting auto mode requires a Max, Team, Enterprise, or API plan (not Pro) so users on unsupported plans can dismiss with informed consent. Note that the live permission mode cannot be detected from inside the session (Shift+Tab activations leave no signal); the check runs against settings only. Do not auto-write user settings. This check is informational, not blocking — proceed regardless.

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

#### Convergence

- **CONVERGED requires observable peer challenge.** Before sending CONVERGED, the facilitator must verify: (1) At least one member sent a message directly to another member engaging their position — not a challenge relayed by the facilitator on a member's behalf; the facilitator cannot be the exclusive routing layer. (2) At least one disagreement was named, with the specific claim at issue quoted or paraphrased, and either resolved with the conceding member naming what moved them, or explicitly tabled as an accepted trade-off. (3) No position was conceded without the conceding member naming what changed their position. If any item is unmet, reopen discussion. Any member may send DISPUTE UNRESOLVED to the facilitator before CONVERGED reaches the lead; the facilitator must reopen.
- **CONFIDENCE REACHED requires independent reasoning.** Before sending CONFIDENCE REACHED, each reviewer's score must be accompanied by named reasoning — what the work is still missing or what gave them confidence from their own read — not a bare number or adoption of another reviewer's conclusion. A score without independent reasoning is not a valid review response; the facilitator must solicit the reasoning before sending CONFIDENCE REACHED.

#### Review Process

- **Wait for ALL reviews before making changes.** Never fix findings mid-review. Wait for every team member to respond, then batch fixes.
- **Intermediate review cycles are autonomous.** The facilitator drives review rounds and determines when the team has reached sufficient confidence. The lead processes feedback and implements fixes between rounds without blocking on the user.
- **Ask about refinement before delivering.** When 9/10+ confidence is reached, the lead MUST ask the user via AskUserQuestion whether to refine or deliver — the user decides, not the lead. See the Refine phase in the mode skill (if defined) for the question and options to present.
- **Final delivery requires user approval.** When the team reaches 9/10+ confidence, present the completed work to the user. Do not ship (push/PR) without explicit user sign-off — rung commits during Recursive Refinement are authorized by the user's opt-in to refine.
- **Reviews must reach 9/10+ confidence before shipping.** Keep plan docs updated every cycle. Run gap analysis every cycle.
- **Name what's missing before scoring.** A rung asserts the work is complete at that rung, not that the reviewer ran out of things to say. Before scoring, name what the user's ask requires that the work has not yet addressed — including items once treated as optional whose absence now leaves the work incomplete for the purpose it was approved to serve, not merely improved.
- **The facilitator and lead keep probing past self-caps.** Score convergence is not a rung transition. A reviewer's self-cap ("I'm at my limit") is not clearance to advance — it is a signal for the facilitator and lead to keep soliciting until the team has genuinely looked, not until reviewers have given up. A score above the current rung confirms the current rung only; the next rung must be established on its own evidence.
- **Hold the rung before advancing.** After fixes at any rung in the refine ladder, re-review must reach the same rung or higher with every solicited reviewer before advancing. If any reviewer scores below the current rung, iterate at that rung — batch fixes and re-review. If the rung fails to hold after two consecutive fix cycles, the facilitator invokes `swarm:resolve-dispute` to break the loop.
- **Break review loops with evidence.** If a finding survives arbitration without new evidence, the facilitator invokes `swarm:resolve-dispute` to force a put-up-or-concede exchange.

Note: what "9/10+ confidence" means and what happens during each phase depends on the active mode. The mode skill defines this.

#### Transparency & Honesty

- **No performative shortcuts.** The user reads every message in real time, including DMs between teammates. There is no internal channel. Any claim of completion — CONVERGED, CONFIDENCE REACHED, "team agrees" — must be supportable by observable peer-to-peer engagement where position changes name the argument that moved them. Agreement without named reasoning is indistinguishable from rubber-stamping and will be treated as such. Never misrepresent what was done.
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
- You MUST send RESEARCH COMPLETE to the lead when the lead notifies you all non-facilitator members have submitted their research findings. Treat the lead's confirmation as authoritative — you do not need to independently verify each member's submission. Then convene the roundtable.
- You MUST send CONVERGED to the lead with your synthesis when the roundtable closes.
- When the lead signals implementation is complete, solicit a review and confidence score from each non-lead, non-facilitator team member individually. When all solicited members have responded and 9/10+ is met, you MUST send CONFIDENCE REACHED to the lead with the confidence score. 9/10+ means all solicited reviewers confirm the work is ready to present to the user.
- If any member sends DISPUTE UNRESOLVED before CONVERGED reaches the lead, you MUST reopen discussion and address the named dispute before sending CONVERGED.

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

Use the **Skill** tool to invoke your mode skill. A mode skill is either a **full mode** or an **extension mode**:

- **Full mode.** Returns the complete spec: Lead Identity, Facilitator Title, Facilitator Identity, Lead Allowlist (optional), Pre-flight Reads (optional), Mode-Specific Rules, Information Flow (optional), Outcomes Question (optional), Suggest-Members Guidance, and Phase Arc.
- **Extension mode.** The frontmatter declares `extends:` naming a base (e.g., `extends: swarm:code-mode`, `extends: swarm:writing-mode`, or `extends: swarm:general-mode`). Read the frontmatter directly from the mode skill file at `.claude/skills/<name>/SKILL.md` to detect this — do not rely on body prose. Invoke the base via the Skill tool **immediately after** the extension. The base provides Lead Identity, Facilitator, Phase Arc, base Mode-Specific Rules, base Lead Allowlist, and base Suggest-Members Guidance. The extension adds supplementary Mode-Specific Rules, additive Lead Allowlist entries (Permitted and Forbidden additions), and a Suggest-Members Guidance supplement — all additive, never replacing.

Apply the lead identity to yourself. Use the facilitator title and facilitator identity in the facilitator brief. Treat mode-specific rules (base plus extension additions) as equally binding to the hard rules above. If the mode skill (or its base) includes **Pre-flight Reads**, read those files now — before spawning any agents. Carry their content into spawn prompts where relevant.

If the mode skill was already invoked earlier in the workflow (e.g., during setup), skip re-invocation — apply the spec from that earlier invocation. The same rule applies to a base mode invoked on behalf of an extension.

When invoking `swarm:suggest-members`, pass the mode skill's **Suggest-Members Guidance** (for extension modes: the base's guidance plus the extension's supplement) and the confirmed outcomes as context.

**Extension hard contract.** Extension modes cannot override the base's phase arc, lead identity, or facilitator. Their Mode-Specific Rules and Lead Allowlist contributions are additive-only — they may add new rules, new permitted actions, or new forbidden items, but cannot remove or contradict base-mode governance. When combining the extension with the base: apply the extension's additive Mode-Specific Rules alongside the base rules, merge the extension's Lead Allowlist Permitted additions into the base's Permitted list, merge the extension's Lead Allowlist Forbidden additions into the base's Forbidden list, and append the extension's Suggest-Members Guidance supplement to the base's guidance. If an extension declares anything that violates this contract (e.g., redefines a phase, removes a base Forbidden entry), treat the file as malformed: surface the conflict to the user before proceeding. The contract exists to keep wrappers thin and governance inherited; a mode that needs to change phase semantics should be authored as a full mode instead.

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

Read `.claude/swarm-ship.md`. If it exists, apply it at Execute (branch creation), Refine (rung commits), and Deliver (shipping). Skip to the phase arc.

If it does not exist, first check `git rev-parse --is-inside-work-tree`. If not a git repo, skip detection and present standard AskUserQuestion directly. If it is a git repo, spawn an Explore sub-agent (regardless of lead research setting — housekeeping, not research) to detect conventions. The sub-agent must NOT write files. It runs: `git log --oneline --merges -10`, `git remote show origin 2>/dev/null | grep "HEAD branch"`, `git branch -a`, `which gh && gh pr list --state merged --limit 3`. It returns: a proposed definition, confidence (high = clear pattern, low = ambiguous or no history), and one-line reasoning. If high confidence, use AskUserQuestion with options: "Use suggested" (description includes reasoning) / "Create a PR" / "Commit and push" / "Commit only" / "Custom". If low confidence, present options directly: "Create a PR" / "Commit and push" / "Commit only" / "Custom". For "Custom", ask: "How did you handle branching?" / "How did you ship?" For PR workflow, ask target branch and naming convention. Write the confirmed definition to `.claude/swarm-ship.md`:

```
# Ship Definition
## Branch Strategy
[e.g., "Create a feature branch from main. Naming: feat/<description>."]
## Delivery
[e.g., "Commit, push, open PR against main."]
```

---

## Rung Commit Rule (Recursive Refinement)

Modes using Recursive Refinement (9 → 9.25 → 9.5 → 9.75 → 10) apply this rule for every rung commit:

- Each rung commit is a new commit — never amend.
- Before committing, run `git branch --show-current`. If the ship definition specifies a branch strategy that the current branch does not satisfy, stop. Check whether the correct branch already exists (`git branch --list <correct-branch>`) and whether the working tree is clean. Present only the options that apply: **Keep** (current branch satisfies structural intent but not the naming template), **Rename** (`git branch -m <new-name>` — stays on this branch), **Switch** (`git checkout <correct-branch>` — omit unless the branch exists and the working tree is clean), or **Abort** (stop work, resolve manually). Never silently change branch state.
- If no branch strategy is specified, commit to the current branch. If that is the repo's default (main/master), inform the user and confirm before the first commit.
- If nothing to commit at this rung, skip and continue.
- If a pre-commit hook rejects the commit, stop and surface the hook output; do not retry with `--no-verify`.
- Commit messages: `checkpoint: rung 9 — <one-line summary>` for the baseline, `refine: rung <score> — <one-line summary>` for 9.25/9.5/9.75/10.
- **Use file-based input for commit messages.** Run `mktemp` and capture its output (e.g., `/tmp/tmp.aB3xK9`) as a single file path. Use that exact captured path string in every subsequent step: write the message to it via Write, then `git commit -F <captured-path>`, then `rm <captured-path>`. Do not regenerate the path between steps — one `mktemp` call binds one path used across all four operations. Inline `-m "$(cat <<EOF ...)"` triggers the bash safety heuristic and prompts unconditionally in auto mode — file-based input does not. `mktemp` (rather than a fixed `/tmp/swarm-*.md` path) defends against symlink-race attacks on shared systems where another user could pre-create the predictable path as a symlink.

---

Follow the **phase arc from your mode skill**. Universal rules:
- Lead does no research unless the user explicitly enabled it (exception: the ship definition detection sub-agent runs unconditionally)
- Questions the team cannot resolve go to the user via AskUserQuestion — most consequential first, one at a time
- Post-greenlight execution is autonomous — escalate only per the hard rules
- Phase transitions that require user input (Approve, Refine, Deliver) are mandatory stops — do not advance past them autonomously
- After 9/10+ review confidence, ask the user about recursive refinement before delivering — do not skip to Deliver
- Final delivery requires explicit user sign-off — follow the ship definition from `.claude/swarm-ship.md` and execute the defined shipping steps with the user's approval. If a rung commit already landed in Refine (per the Rung Commit Rule above), the commit is done; Deliver begins from push/PR.
- **Use file-based input for PR bodies.** Run `mktemp` and capture its output as a single file path. Use that exact captured path string in every subsequent step: write the body to it via Write, then `gh pr create --body-file <captured-path>`, then `rm <captured-path>`. Do not regenerate the path between steps — one `mktemp` call binds one path used across all three operations. Inline `--body "$(cat <<EOF ...)"` triggers the bash safety heuristic and prompts unconditionally in auto mode. `mktemp` defends against symlink-race attacks on shared systems.
- When an explicit shutdown request has been received, delete the pulse cron job using CronDelete
