---
name: independent-review-loop
user-invocable: false
description: |
  Independent review loop run before delivery in code work. An independent reviewer (Codex, or fresh Codex-style subagents) reads the whole PR against the approved outcome; the lead fixes in-scope functional findings and re-reviews until none remain. Its differentiator is independence and exhaustiveness — a reviewer that fails differently from the authors, run to clean — distinct from the recursive-refinement ladder. Invoked by the team lead from the unified pre-ship gate (code-mode and /swarm:refine) after the ship steps.
keywords: independent review, codex review, review loop, pre-delivery review, bug surface, edge cases
---

Operational spec for the **team lead**. This skill runs an independent review pass at delivery: a reviewer that fails differently from the author reads the whole PR against the approved outcome, the lead fixes what is in scope, and the loop repeats until the reviewer finds no more in-scope functional issues. It is the automated form of "ship, then loop the PR through Codex until it stops finding edge cases" — with the lead acting as the operator who keeps findings on-scope.

What distinguishes this from the team's own review and the recursive-refinement ladder is **independence and exhaustiveness**: the reviewer is a different model (Codex) or a fresh-context agent that fails differently from the authors, and it runs to exhaustion — until no in-scope functional finding remains — rather than the bounded rung ladder. (The ladder hunts bugs too, as it drives the work to the full scope of the outcome; the new axis here is the *independent eye run to clean*, not bug-hunting per se.) It is a distinct pass; it never replaces the ladder.

Only the lead runs this. Reviewers (Codex, or fresh subagents) are read-only; the lead is the sole writer, same as every other phase.

## When this runs

Invoked from the **unified pre-ship gate** in code-mode's Refine/Deliver (and `/swarm:refine`) — the gate the lead presents once the team reaches 9/10+, offering: *recursive refinement + independent review* / *independent review loop only* / *ship as is*. This skill runs for the first two options (after the recursive ladder completes, when both were chosen; or on its own when only the independent loop was chosen).

It runs **after the ship steps complete** (PR-then-loop on the common path): when a PR was created, the loop reviews the PR's diff and pushes each round's fixes to it; on a commit-only / push-only ship with no PR, it reviews the pushed branch against its base. The diff base is resolvable from the PR when one exists (see the loop's base resolution below for the no-PR fallback).

## Engine choice (Codex or Swarm fallback)

When invoked, select the reviewer engine with **AskUserQuestion** (header "Reviewer"). Detect Codex once: `command -v codex` (exit 0 = present). Offer **both engines every time** — `command -v codex` only sets the **order/default** and a neutral note. No affordability language, ever. ("No loop" is not offered here — that is the gate's "ship as is.")

- **Codex present** → 1) "Codex" 2) "Swarm fallback".
- **Codex absent** → 1) "Swarm fallback" 2) "Codex *(requires Codex CLI)*".

Descriptions (neutral): Codex = "An independent model (Codex) reviews the whole PR; fails differently from the code's author." Swarm fallback = "A fresh Claude reviewer in a Codex style — sharp, but shares the author's model blind spots; always available, no Codex needed."

If the user picks Codex while it is absent/unauthed, surface Codex's own message + how to enable (`codex login`, or install per Codex's docs) once, then offer the Swarm fallback or stopping — never hang. While this gate is live and teammates exist, apply the launch.md live-team gate rules (ask teammates to hold; re-ask once if the modal is preempted).

## The loop (identical control flow on both engines)

Resolve the diff base once. The review is simply the branch's **committed** diff against the branch it targets — `main`, or the repo's equivalent default/target branch. **A GitHub PR is not required**: Codex does a PR-style review of any branch, and the PR (when the ship definition uses one) is only the push target, not a precondition. Pick the base as the PR base if a PR exists (`gh pr view --json baseRefName` just names the target branch), otherwise the repo's default branch (`git symbolic-ref refs/remotes/origin/HEAD --short`, stripped of `origin/`); compare against the up-to-date base — the fetched remote-tracking ref (e.g. `origin/main`), not a possibly-stale local copy. The base must be the point the work **diverged from**, so the diff covers this run's changes; if the work was committed directly onto the base branch (so `<base>` and `HEAD` coincide), use the pre-work commit instead. If the base can't be resolved, ask the user to provide or confirm the base (or to explicitly opt out of the loop) — never silently **skip** the review the user selected, and never error. And if the resolved `git diff <base>...HEAD` comes back **empty**, that is NOT a clean review — nothing was reviewed — so surface it to the user to correct the base rather than terminating clean. Then each round:

1. **Review the WHOLE PR diff, every round** — the full `git diff <base>...HEAD`, never just the delta since the last fix. New findings hide behind old fixes; only a whole-PR pass surfaces them.
2. **Collect findings** in Codex's native shape (see Output format).
3. **The lead triages each finding against the approved outcome** — the lead is the codified "operator once in a while":
   - Bears on the outcome and is a real functional defect → **fix it** (lead writes the change).
   - Out of scope (new feature, adjacent refactor, gold-plating, pre-existing issue, style) OR genuinely ambiguous → **do not fix; add to the out-of-scope pile.** When unsure, surface — never silently drop and never silently fix.
4. **Surface the out-of-scope pile to the user** (plain text) at the end of the loop, or immediately if a pile item is consequential (a real defect you're declining because it exceeds the approved outcome) — that is the rare operator escalation the user asked for. The diff may legitimately grow toward outcome-completeness (e.g., fixing an off-diff caller the outcome requires); that growth is bounded by the outcome, grounded in `git diff --stat <base>...HEAD`, and surfaced — not silent scope expansion.
5. **Commit this round's fixes (push per the ship definition), then re-run.** The review reads the *committed* `git diff <base>...HEAD` (the reviewer runs git locally), so the lead MUST commit each round's fixes (e.g., `review: round N — <summary>`) before re-running — otherwise the reviewer re-reads stale committed state, the loop never converges, and every just-fixed finding reappears unchanged and is misread as oscillation. **Pushing is governed by the approved ship definition, not the loop:** if the ship definition pushes (a PR or push workflow), push each round — to the PR if one exists, else the branch — to keep the remote reflecting the work; if it is **commit-only**, do NOT push (committing is enough for the review, and pushing would silently change the user's approved delivery or fail on a branch with no upstream). After committing (and pushing where the ship definition calls for it), re-run the review on the whole diff.

**Termination (engine-neutral — identical on both paths)** — stop when, after the lead's triage of a **valid** review, **no in-scope functional findings remain**. Two cases satisfy this and both terminate: (a) the review is an explicit, format-conformant affirmative "no findings" result; or (b) the review returned findings but the lead triaged them **all** as out-of-scope/ambiguous — terminate and surface the out-of-scope pile. Do NOT re-run a round whose only findings are out-of-scope (re-running an already-on-scope-clean state just churns to the backstop). What must NOT be read as termination is a **non-review**: empty output, a truncated or off-format response, a clarifying question, or a non-zero exit is a **FAILED review, not a clean one** — retry once, then degrade (Codex: take the error path / offer the Swarm fallback; Swarm: re-spawn the reviewer). Never read silence or a non-answer as "done": a false "done" silently ships bugs while reporting success, defeating the loop's whole purpose. (This is a validity check — *was this a real, well-formed review?* — combined with the lead's in/out-of-scope triage; not a field-by-field parser.) Both Codex and the swarm-native reviewers emit the same finding format, so the terminator never depends on an engine-specific field; on the Codex path an `overall_correctness: patch is correct` verdict, when present, is a convenience corroborator only, not the stop signal. Expect this to take many rounds — 8–10 rounds of genuinely different findings is normal and runs fully autonomously — but the stop condition is the **clean review itself, not a round count**: once a valid review returns no in-scope findings (case (a) or (b) above), terminate; do NOT re-run an already-clean review hoping to surface more. "Don't stop early" means don't declare done *without* a clean review (a small-but-nonempty round is not a clean review) — it never means re-running a review that already came back clean.

**Backstop** — a hard cap of **15 rounds** (a fixed constant, not a config knob) guards against a non-converging loop. Reaching it does NOT silently abort: escalate to the user (continue / stop here / take over) — as do repeated invalid reviews (several consecutive failed/malformed reviews after retry/degrade), rather than silently riding the cap. An **oscillating** finding — the *same finding*, matched by its title + `file:line` (never by `[P#]`, which is severity and is shared across unrelated findings), resurfacing after ≥2 fix attempts — is a disagreement, not a grind: stop auto-fixing it and **surface it to the user** with both positions for an operator decision. (Unlike a standing-team review dispute, this loop's reviewer is Codex or an ephemeral one-shot — not an addressable teammate — so `swarm:resolve-dispute`, which messages the reviewer, does not apply here; the user is the arbiter. This is the spirit of the "break review loops with evidence" rule, routed to the operator.)

**Auditability** — the lead is both loop-driver and fixer, so keep it honest: surface the reviewer's verbatim output to the user each round (at minimum at termination), so the user — not the self-interested driver — is the backstop on "are we actually done."

## The steer (one string, both engines — this is the over-reach guard)

Send the reviewer exactly this (substituting the approved outcome verbatim and the resolved base):

> The outcome this change is meant to achieve:
> «approved outcome, verbatim»
>
> Review the ENTIRE change on this branch relative to `«base»` — the full PR diff (`git diff «base»...HEAD`), not just the latest edits. Report only material, FUNCTIONAL findings that bear on that outcome: incorrect logic, defects, broken or unhandled edge cases, and regressions in code this change touches.
>
> Do NOT report: style, naming, or formatting; low-value cleanup; pre-existing issues this change did not introduce; speculation you cannot tie to a concrete failing input or condition; or choices the author clearly made intentionally. A finding must be discrete, actionable, and something the author would fix if they knew.
>
> Prioritize each finding [P0]–[P3]. **No code suggestions** — for each finding, explain in prose what breaks, the exact conditions that trigger it, and the consequence. **Format:** open with a 1–3 sentence summary, then a line `Full review comments:`, then one bullet per finding as `- [P#] <imperative title> — <file>:<line-range>` followed by the indented prose paragraph. If you find no in-scope functional issues, **state that explicitly** (e.g., "No in-scope functional findings.") — do not return an empty or merely terse response.

The closing affirmative-clean instruction is load-bearing: it is what lets the termination guard above distinguish a genuinely clean review from a malformed/empty/aborted one. Without it a clean reviewer may return nothing, the guard reads that absence as a FAILED review, and the loop never terminates — burning to the round cap and firing a spurious "didn't converge" escalation on work that was actually clean.

Telling the reviewer the outcome and asking only for functional findings is the steer that keeps the loop on-scope — the input-side guard, paired with the lead's triage on the output side.

<!-- SYNC: the steer's "Format:" clause above and the "Output format" section below must stay identical. If either changes, update both — termination treats an off-format response as a FAILED review, and the oscillation key parses `title + file:line` from this exact shape, so drift breaks both. (Same convention as launch.md Step 1 ↔ workflow-rules.) -->

## Codex path

Codex is the preferred reviewer because it is a genuinely different model and fails differently from the code's author. Run it via **Bash** (the lead can run shell; `/codex:*` slash commands are not model-callable, so do not rely on them):

- Invoke with the steer as a **custom review prompt passed on STDIN** — never as a double-quoted shell argument. The steer contains backticks (e.g. `` `git diff …` ``, `` `codex login` ``); inside double quotes bash runs them as command substitution and corrupts the prompt. Both `codex review` and `codex exec review` accept the prompt from stdin via the `-` positional, so write the steer to a temp file (or a single-quoted heredoc) and pipe it: `printf '%s' "$steer" | codex exec review -`. (Codex's `review` flags `--base`/`--uncommitted`/`--commit` are mutually exclusive with a custom prompt, so the steer rides as the stdin prompt and itself names the `git diff «base»...HEAD` scope; codex still applies its built-in review rubric as the system prompt.)
- Capture stdout, stderr, and the exit code explicitly — `codex exec` exits non-zero on a fatal error, which is the degradation path below. If the invocation errors, check `codex exec review --help` / `codex review --help` and adapt — do not hardcode against version drift. The pass is read-only; if codex's default sandbox blocks the `git` the steer relies on, surface that and degrade rather than hang (runtime-validate).
- Depend only on the **`codex` binary**, never on the codex plugin, its install path, or its companion script.
- **Auth/errors degrade, never hang:** the first failing call → surface Codex's verbatim error + `codex login`, then offer the Swarm fallback or stopping.
- **Codex's own Stop review-gate** (`/codex:setup --enable-review-gate`) is a separate, unbounded per-turn loop that will collide with this one. Warn the user once in prose to disable it for this run; do not read or modify the user's Codex config.
- **Review depth tracks the user's Codex config, don't hardcode it.** The 8–10-round expectation assumes a strong reviewer (the practice this automates runs the best available model at high/xhigh effort); let the user's codex model/effort settings drive depth rather than pinning a model in the invocation.
- **Guard against a stalled invocation, not just a failed one.** A review that hangs (no progress, no exit) is distinct from a non-zero exit — bound each call with a no-progress/timeout cutoff and treat a stall as a failed review (degrade per above), so one hung review can't hang the loop. (Applies to any review invocation, including a swarm-fallback reviewer that goes dark.)

## Swarm fallback

When Codex is absent — or the user picks it deliberately — run the same loop with **fresh, ephemeral, read-only reviewer subagents** spawned via the Agent tool (`subagent_type: swarm-member`), not the standing team. Fresh per round: each reviewer's spawn prompt MUST carry the **full steer verbatim** — the same string the Codex path uses, *including the affirmative-clean instruction and the output format* — plus the diff and the approved outcome, with no Converge/Approve history. This approximates an outside reviewer and avoids the "I already looked, looks fine" fatigue of re-soliciting standing members. **Verify the affirmative-clean line is actually in the spawn prompt** (don't assemble the spawn from persona + a loose paraphrase that drops it): it is what lets the termination guard tell a genuinely clean swarm review from a malformed/empty one; if it's dropped, a clean fallback review never terminates — the exact regression this guards against. Spawn **serially by default** (one reviewer at a time — the swarm serial-default / parallel-opt-out toggle applies unchanged); use distinct lenses across reviewers (e.g. correctness & logic, edge cases & failure modes, regressions in touched code). They return findings only; the lead triages and fixes exactly as on the Codex path.

Each reviewer's identity is a **Codex-style reviewer** (adapt this as the subagent's identity, not as extra brief sections):

> a code reviewer in the style of Codex — terse, analytical, matter-of-fact, zero flattery or praise. Flags only discrete, actionable, functional defects introduced by the change that the author would fix if they knew; states the exact conditions that trigger each bug and the provably-affected code; never speculates and never nitpicks style. Reviews the whole PR against the stated outcome and reports findings in the prescribed format with no code suggestions.

Honest limit, worth stating to the user: a fresh Codex-style Claude reviewer is sharp and adversarial but shares the model-level blind spots of the team that wrote the code — it buys *stance*, not the independence Codex's different model gives. That is why Codex is offered first when present.

## Output format (both engines — Codex's native shape)

<!-- SYNC: this format must stay identical to the steer's "Format:" clause in "The steer" section above — keep both in step (see that SYNC note). -->

Findings are rendered as:

```
«1–3 sentence overall summary of the themes»

Full review comments:

- [P1] «imperative finding title» — path/to/file.ext:120-128
  «one prose paragraph: what breaks, the exact conditions that trigger it, the consequence, and what to do — no code blocks»

- [P2] «next finding title» — path/to/other.ext:40-44
  «…»
```

`[P#]` is a presentation/severity label only. It is neither the action gate (what the lead fixes is decided solely by the in-scope/out-of-scope triage above, anchored on the outcome) nor the oscillation key (recurrence is matched by finding identity — title + `file:line`).

## What this skill reuses (do not rebuild)

The round structure, batch-fix-then-re-review discipline ("wait for all of a round's findings before fixing"), escalation, and the serial-default/parallel-opt-out cadence are all existing swarm machinery — this skill only adds the independent reviewer, the outcome steer, the triage gate, the termination/backstop, and the output contract. (Oscillation routes to the user, not `swarm:resolve-dispute` — that skill messages a teammate reviewer, and this loop's reviewer is Codex or an ephemeral one-shot.) No new phase, no new hard rules, no changes to the team-member briefing templates.

---

*The reviewer rubric, priority tags ([P0]–[P3]), finding format, and steer are adapted from OpenAI Codex (`codex-rs`, Apache-2.0), with one deliberate deviation: Codex permits short `suggestion` blocks; swarm requires prose-only findings with no code suggestions.*
