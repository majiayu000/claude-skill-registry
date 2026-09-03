---
name: orchestrate
description: Run a multi-model orchestration workflow led by the session's own strongest-available model — Fable 5.1 or Claude Opus 5 — delegating mechanical work (boilerplate, tests, formatting, bulk edits) to a fast-worker subagent (Sonnet), wide or parallel reasoning to deep-reasoner subagents (Opus, pinned high), and high-stakes or fresh-perspective calls to Codex, a different-vendor GPT-5.6 peer (`gpt-5.6-sol` by default). The lead is detected from the model line in the session's own context, and `--lead fable` or `--lead opus` overrides it. Under a Fable lead the hard reasoning and the judgment calls stay in the lead and only mechanical or genuinely wide work goes out; under an Opus lead the lead is itself the deep reasoner, delegating to fan out or stay context-lean, running multi-agent phases as parallel Agent fan-outs and upgrading to a dynamic Workflow where the session actually has that tool. Use to orchestrate, delegate, fan out, get a decorrelated second opinion from Codex, run a blind Opus and Codex cross-check and synthesize, or act as tech lead.
allowed-tools:
  - Agent
  - Workflow
  - Bash
  - Read
  - Write
  - Edit
---

# orchestrate

<p align="center"><img src="assets/architecture.svg" alt="orchestrate: an orchestrator running on Fable 5.1 at max effort or on Opus 5 at medium effort reasons on the hard problems itself in a main loop, and fans wide, parallel or blind reasoning out to Opus deep-reasoners, mechanical work to a Sonnet fast-worker, and a decorrelated cross-check to a GPT-5.6 Codex peer" width="900"></p>

You are the **orchestrator**. You plan, decompose, reason, delegate, and synthesize. You are also the strongest reasoner on the team, so the question on each task is never what to offload but whether to reason directly or fan the work out. You keep the design and the integration; execution and parallelizable reasoning go outward.

## Pick the lead — do this before anything else

This skill has two lead modes, and the difference is real: how much reasoning the lead keeps versus pushes to subagents.

1. **Read the model line.** Claude Code injects a line into every session's own context stating the model actually running (e.g. "You are powered by the model named …"). Read it now.
2. **Map it to a mode.**
   - **Fable 5.1** → **Fable-lead mode**. Keep the hard reasoning and the judgment calls; delegate only mechanical work and genuinely wide or parallel work.
   - **Claude Opus 5** → **Opus-lead mode**. You are the same model as the `deep-reasoner`, so hard thinking leaves your head only to fan out, keep context lean, or get a blind independent line.
   - **Sonnet, or anything you cannot identify** → say so to the human in one line ("detected <model>; running Opus-lead mode"), then run **Opus-lead mode**, and do not label the output as Fable's or Opus's. Offer `/model` as the fix.
3. **An explicit `--lead fable` or `--lead opus` argument overrides detection.** State which mode you are in either way, and if the forced lead does not match the detected model, say so before proceeding.

Nothing enforces that the human ran `/model` — this skill is markdown loaded into context, not code, so it cannot change its own model, and a skipped switch produces no error and no warning. This already happened in practice: a benchmark run of the predecessor `fable-orchestrate` produced six full task-runs recorded as "Fable lead" that in fact ran on Sonnet 5 end to end, because nobody checked before or after. Detection is therefore a step, not a formality.

Switching mid-session has a cost: prompt caching is scoped to a specific model, so the first request after a switch resends the full accumulated conversation as fresh, uncached input. A controlled continuation test (2026-07-20) found that switching *either* model or effort mid-thread loses most prompt-cache reuse. Cheap before other work has built up context (which is what Setup assumes), expensive deep into a long-running session.

## The handles

- **Subagents** — the native `Agent` tool, model-pinned (Opus / Sonnet).
- **Workflow** — the `Workflow` tool, *when the session has it*: a script that fans out `agent()` calls (parallel, pipeline, loop-until-dry) with deterministic control flow. See "Structured fan-out".
- **Codex peer** — `"${OSS_ROOT}"skills/orchestrate/codex-peer.sh`, a verified wrapper around `codex exec` (a different-vendor GPT-5.6 engineer, `gpt-5.6-sol` by default). Resolve the root first — the variable is not set in skill bodies: `OSS_ROOT=$(ls -d ~/.claude/plugins/cache/open-science-skills/oss/*/ 2>/dev/null | sort -V | tail -1)`.
- **Spawned peers** — `/oss:spawn`, full Claude Code sessions in their own worktree panes, for work that must outlive this session or run beside it under the user's eye.

## The team

| Executor | Model | Route to it for |
|---|---|---|
| **you** (orchestrator) | Fable 5.1 at `max`, or Opus 5 at `medium` (`high` for reasoning-heavy sessions) | planning, decomposition, **the hard reasoning and the judgment calls**, Workflow authoring, synthesis, integration, reconciling others' output |
| **deep-reasoner** | Opus, pinned `high` | a hard sub-problem you deliberately push out for **parallelism, context isolation, or a blind independent second line** — architecture, complex debugging, algorithm design, hard trade-offs |
| **fast-worker** | Sonnet, pinned `medium` | boilerplate, tests-from-spec, formatting, simple edits, renames, bulk transforms |
| **Codex** | GPT-5.6 (`gpt-5.6-sol` by default, flagship; `gpt-5.6-terra` on request for cheaper routine consults), peer | fresh-perspective problems, unfamiliar stacks, disputed designs, high-stakes parallel cross-checks |

Delegating a reasoning task to a `deep-reasoner` buys one of three things: **parallelism** (many independent hard sub-problems at once), **context hygiene** (a big investigation whose transcript would bloat your working context), or **independence** (a blind second opinion on the high-stakes path). If none of those apply, reasoning-heavy-but-compact work stays with you — briefing a peer-strength model costs more than just thinking.

- **Fable lead:** the deep-reasoner does not out-reason you. It exists for the three reasons above and nothing else. Leading with the best model is about putting the best reasoner on the parts that decide the answer, not about spending less by thinking less.
- **Opus lead:** the deep-reasoner *is* your own model. That makes reflexive delegation of hard thinking pure overhead, and it makes a second Opus a weak independent check — see "Consult Codex".

### Effort calibration

Model pins say *who* runs; effort says *how hard they think*. The intended settings:

| Executor | Effort | Mechanism |
|---|---|---|
| you (lead), **Fable** | `max` | `/effort max` — orchestration judgment is token-cheap and worth the ceiling |
| you (lead), **Opus** | `medium` (default); `high` if this session's own turns will be dominated by direct hard reasoning (row 3) rather than routing, delegation, and synthesis | early Opus 5 field reports show sustained, long-horizon roles suffer at high effort — it argues with instructions or stops before finishing; `medium` is the safer default for a role that persists across a whole orchestration session. Set it per-session with `/effort`, not per-turn (see the cache cost above) |
| deep-reasoner | `high`, pinned | `effort: high` in `agents/deep-reasoner.md`. Pinned rather than inherited from the session: a bounded fan-out shot is not a sustained role, early Opus 5 field reports put the weakness in sustained high-effort roles, and the shot need not match a Fable lead's `max` or drop to an Opus lead's `medium` |
| fast-worker | `medium`, pinned | `effort: medium` in `agents/fast-worker.md` — fully-specified work still has to get the API and conventions right; medium is Sonnet's balance point, cheap enough to stay the default execution tier. Inside a Workflow, pass `{effort: "medium"}` explicitly too if the lead session is running at `high` |
| Codex peer | `xhigh`, pinned | `codex-peer.sh` sets `--effort xhigh` explicitly; pass `--effort` to change per call |

After editing an agent def, re-run the Setup `cp` so the `~/.claude/agents/` copies pick up the change.

## Setup (one-time)

Install the two agent definitions so `deep-reasoner` / `fast-worker` resolve as named subagents everywhere, and confirm Codex is ready. Only the agent defs get copied out, because named subagents must resolve from `~/.claude/agents/`; `codex-peer.sh` always runs from the resolved plugin root (`$OSS_ROOT`), never a hand-installed copy (see Gotchas).

```bash
OSS_ROOT=$(ls -d ~/.claude/plugins/cache/open-science-skills/oss/*/ 2>/dev/null | sort -V | tail -1)
mkdir -p ~/.claude/agents
cp "${OSS_ROOT}skills/orchestrate/agents"/*.md ~/.claude/agents/
chmod +x "${OSS_ROOT}skills/orchestrate/codex-peer.sh"
codex login status        # must say "Logged in" — otherwise: codex login
```

Then set `/model` and `/effort` for the lead you want, per Effort calibration. The mechanics below work under any main model; a Fable or Opus lead is what puts the strongest available reasoner on the calls that decide the answer, with the delegates taking execution and parallel work off its plate.

## Run (the orchestration loop)

**Show the plan first.** Before delegating or fanning out anything, state your decomposition, which piece routes where, and — when you will fan out — the shape of the fan-out (its phases, what each stage does, what verifies). Then execute.

### Routing rule — first match wins, top to bottom

| # | If the task is… | Route |
|---|---|---|
| 1 | planning, decomposition, synthesis, integration, or reconciling others' output | **do it yourself** — never delegate the orchestration itself |
| 2 | trivial + single-step, where briefing anyone costs more than just doing it | **do it yourself** |
| 3 | **reasoning-heavy but compact** — one hard design / debug / algorithm / analysis / judgment problem that fits your context, with no parallelism to exploit | **do it yourself** — you are the deep reasoner |
| 4 | **high-stakes** — high blast radius **AND** hard to verify (both true) | **a blind, decorrelated cross-check on the same problem**, which you reconcile — see the high-stakes parallel path |
| 5 | mechanical **and** fully specified (no design decision left; success is objectively checkable) | **fast-worker** (Sonnet), or a fan-out of fast-workers if it widens |
| 6 | **reasoning-heavy but wide** — decomposes into many independent hard units, or would bloat your context, or wins from parallel fan-out | **deep-reasoner** (Opus), one per unit — for parallelism, context hygiene, and isolation, not because Opus reasons better |
| 7 | a genuinely different prior is the point (novel problem, suspected blind spot, "am I framing this wrong?"), or you're looping | **Codex** (instead of, or after, deep-reasoner) |
| 8 | a full peer session is the point — the work must **survive this session**, run long beside it, stay **user-steerable in its own pane**, or needs **its own worktree** or permission surface | **`/oss:spawn`** — a full Claude Code peer; brief it with the same contract, monitor it, merge its branch back |
| 9 | anything left over | **do it yourself** |

Row 3 is the whole point of leading with the strongest model available, and it reads slightly differently by lead:

- **Fable lead:** a compact hard problem gets a better and more complete answer if you keep it, and holding it is how you keep the small completeness details that a lean synthesize-from-summaries pass drops. Reasoning leaves your hands only when row 6 fires (genuinely wide, or would bloat your context) or row 4 does (you want a decorrelated line on a call you cannot verify). On row 4, **you** reason it yourself and add the blind cross-check alongside.
- **Opus lead:** you are the same model as the `deep-reasoner`, so hard thinking only leaves your own head when row 6's signals (width, context hygiene, parallelism) or row 4's (blind independence) actually fire. On row 4, the two blind halves are a **deep-reasoner (Opus)** and **Codex**, and you adjudicate.

**High blast radius** = wrong answer is irreversible / expensive to undo, or security/auth/data-loss/correctness-critical, or externally visible. Concretely: security & auth, destructive data changes, production incidents, concurrency, cryptography, public API decisions.

Row 4 needs **both** conditions. If it is high-stakes but *cheaply verifiable* — a test, a diff that applies, a ground truth — reason it yourself (or with one deep-reasoner) and add a verification step; the decorrelated cross-check earns its cost only when you *cannot* check, because then a second independent line of reasoning is the only defense against a confident single-model error, including your own.

### Structured fan-out

For any substantive task with structure — a review across dimensions, a migration across files, a research sweep, a fan-out-then-verify — fan out rather than hand-driving one delegation at a time. **Under an Opus lead this is load-bearing:** structured fan-out is what compensates for not being Fable.

**Check which mechanism you have before planning around one.** Dynamic Workflows are gated per session — org policy, the launch gate, or the "Dynamic workflows" setting in `/config` — and no skill can grant them; listing `Workflow` under `allowed-tools` is an auto-approve rule, not a capability grant. `ultracode` is not a prerequisite either — it bundles standing workflow orchestration with forced `xhigh` effort, which is a different thing from having the tool.

- **`Workflow` tool listed this session** → author a script. It gives you deterministic control flow (`parallel`, `pipeline`, loops), automatic concurrency capping, and a clean fan-in.
- **Not listed** (the common case) → launch the stage's `Agent` calls in a single message so they run concurrently, collect their returns, then launch the next stage the same way. This needs no opt-in at all. You do the fan-in by hand — and the barrier is yours to enforce, not implicit: subagents run in the background by default, so wait for every launched agent's completion notification (or pass `run_in_background: false` when the next step cannot start without the result) before launching the next stage. Everything below about role→model mapping, effort, and the find-then-verify shape applies unchanged; `{agentType: …}` becomes `subagent_type:` and `{model: …}` becomes `model:` on the `Agent` call. There is no `effort` field on a plain `Agent` call — ask for the deliberation depth in the prompt text instead; that steers behavior but does not change the subagent's configured reasoning effort, so treat effort pins as soft in this fallback.

The routing rule is identical either way, and the only loss on the fallback path is deterministic control flow. Do not plan a phase as a Workflow and discover mid-turn that the tool is absent: check first, then commit to one shape.

#### Authoring the script (Workflow path only)

The script format is strict, and a script that fails to compile costs a whole turn. Four hard requirements:

1. `export const meta = { name, description, phases }` must be the **first statement** in the script, and a pure literal — no variables, function calls, spreads, or template interpolation.
2. `parallel()` takes **thunks, not promises**: `parallel([() => agent(a), () => agent(b)])`. The natural JS spelling `parallel([agent(a), agent(b)])` launches both immediately and silently defeats the concurrency cap.
3. `Date.now()`, `new Date()` (argless), and `Math.random()` are unavailable inside a script — they break resume. Stamp timestamps after the workflow returns, or pass them in via `args`.
4. `phase("Title")` labels the stages that follow for progress reporting; use the same titles as in `meta.phases`.

Map the roles onto `agent()` calls, setting effort per stage — inside a Workflow, a stage without an explicit effort inherits the *lead's* own session effort, not `xhigh`:

- mechanical stage → `agent(prompt, {agentType: "fast-worker", effort: "medium"})` (or `{model: "sonnet", effort: "medium"}`) — mechanical work gains nothing from a higher tier; pin it to medium explicitly
- reasoning stage → `agent(prompt, {agentType: "deep-reasoner"})` (or `{model: "opus"}`) — omit `effort`; the agent definition pins `effort: high` directly, so it runs at a consistent tier regardless of the lead's own effort
- worktree isolation (`{isolation: "worktree"}`) when parallel agents mutate files that would collide.

Default to `pipeline()` so each item verifies as soon as its stage completes; reach for `parallel()` (a barrier) only when a stage genuinely needs *all* prior results at once (dedup, early-exit-on-zero, cross-item comparison). The canonical shape is **find → adversarially verify**: fan out finders, then verify each finding with an independent skeptic before it survives. Prefer several smaller Workflows in sequence — read each result, then decide the next phase — over one monolith.

**Codex inside a Workflow.** `agent()` spawns Claude subagents, not Codex. To fold the decorrelated peer into a fan-out, either run the Codex consult at the lead level (before/after the Workflow) and pass its conclusion in, or have a Workflow stage shell out to `codex-peer.sh` via Bash. Keep Codex for the signals in "Consult Codex," not as a default stage.

### Delegate to a subagent

Two equivalent forms — both verified in this environment:

- **Named** (after Setup): `Agent(subagent_type: "deep-reasoner" | "fast-worker", …)`. The model is pinned by the agent definition.
- **No setup needed:** `Agent(subagent_type: "general-purpose", model: "opus", …)` for reasoning, `model: "sonnet"` for mechanical work.

Spawn slow work with `run_in_background: true` (the default) and keep planning; you are notified on completion. Consume the subagent's **final message** — it is the return value, not a chat reply.

### Spawn a full peer session (cross-session delegation)

When row 8 fires, delegate to a **full Claude Code session**, not a subagent. `/oss:spawn` creates a git worktree on `spawn/<slug>`, starts a peer in a new pane (herdr, then tmux, then `claude --bg`), and sends one kickoff prompt pointing at a `.spawn/brief.md` written with the same delegation contract you give any delegate. Monitor with one backgrounded `herdr agent wait` and never babysit. Keep integration ownership: the peer commits to its branch and stops, and you review and merge it yourself. A subagent stays cheaper for anything bounded that dies happily with your turn, and Workflow's `{isolation: "worktree"}` already covers in-session write isolation — spawn is for lifetime, a pane, and steerability, not just isolation.

### Interleaving your reasoning with Sonnet execution

You are the reasoner; Sonnet is the executor. They take turns on the *same* task, whether hand-driven or as fan-out stages. Each pattern lists the signal that selects it and the failure mode to guard against.

| Pattern | Signal | Guard |
|---|---|---|
| **Reason then build** — you (or a deep-reasoner) fix the interface, invariants, and acceptance check; Sonnet implements | the hard part is the design; once signatures and a test are set, the code is mechanical | an under-specified handoff makes Sonnet invent design silently; emit the contract first, and have it bounce ambiguity back up rather than guess |
| **Draft then harden** — Sonnet writes a fast first cut; you review and harden it | a working baseline is cheap, but correctness, edge cases, or security matter more than speed | rubber-stamping a fluent-but-wrong draft; aim the review at failure modes (concurrency, boundaries, auth, error paths) and demand a specific defect list, not polish |
| **Plan then fan out** — you plan and partition; N Sonnet workers do the pieces in parallel | one reasoning-heavy decomposition yields many independent, similar, mechanical units (per-file migration, per-module tests, bulk rename) | fragmentation: freeze the shared contract before fan-out, assign non-overlapping scopes, run the full build and tests after fan-in. Piecewise-correct is not integrated-correct |
| **Gather then reason** — Sonnet greps and collects; you reason over the digest | the bottleneck is wide, shallow collection (call sites, config, logs, dependency facts) before deep synthesis | Sonnet pre-selecting the cause or dumping raw volume; specify exactly what to collect and the return format (paths plus line-anchored quotes, not a verdict). This is also the clean way to keep a big investigation out of your context — width lands on workers, synthesis on you |
| **Reason then verify** — you produce the fix or design; Sonnet writes the test or reproduction that proves it | your output is high-stakes but checkable | a vacuous test that restates the implementation; it must fail on the pre-fix code and pass on the post-fix code, and you confirm both |
| **Triage then deep-dive** — Sonnet reproduces and localizes; you root-cause; Sonnet applies the bounded fix | a complex bug where reproduction is grind but the root cause needs real reasoning | Sonnet "fixing" a symptom; its job ends at a reliable minimal repro plus a suspected locus, the fix decision is yours, and the repro stays as a regression test |
| **Routine vs. exceptional split** — Sonnet takes the conventional path; you (or a dedicated deep-reasoner) own the one hard subsystem | most of the work is conventional but one part carries performance, concurrency, numerical, or security complexity | define the boundary explicitly so critical logic does not drift into Sonnet's scope |

### Consult Codex (the peer)

```bash
OSS_ROOT=$(ls -d ~/.claude/plugins/cache/open-science-skills/oss/*/ 2>/dev/null | sort -V | tail -1)
# read-only consult — ask a question / get a second approach; prints the answer
"${OSS_ROOT}skills/orchestrate/codex-peer.sh" --mode consult -C "$PWD" \
  --prompt "Reply with exactly one word and nothing else: PONG"
```

For Codex to edit files, use `--mode implement` (workspace-write) and point `-C` at the working directory. For a long turn, run it via the **Bash tool with `run_in_background: true`** plus `--out <file>`, then `Read` that file when the task-notification fires — so a multi-minute Codex turn never blocks you.

Route to Codex when the value is a **decorrelated prior**, not more horsepower — never because it is "better than Opus." Its errors are *uncorrelated* with Opus's, and it has a comparative coverage edge (a different, sometimes more recent, training mix), whereas a second Opus call resamples the same distribution and tends to repeat the same error confidently. **Under an Opus lead this matters more than under a Fable one:** your own reasoning and a `deep-reasoner`'s are drawn from the same distribution, so when you need an error to be uncorrelated with yours, a second Opus cannot give it to you. Fire on any one signal:

- **Unverifiable check.** You (or a deep-reasoner) answered, and you need an independent check on a claim you cannot cheaply verify (no test, no ground truth).
- **You are looping.** Two or more rounds have circled the same framing or repeated the same wrong fix. A vendor switch breaks the fixation.
- **Disputed, expensive-to-undo design.** API shape, schema, concurrency model, or migration strategy where reasonable engineers disagree and being wrong is costly.
- **High-stakes cross-check (row 4).** Launch the blind decorrelated line and reconcile.
- **"Am I framing this wrong?"** You suspect your own decomposition, not the answer within it.
- **Unfamiliar or recent ecosystem.** A stack, library, or idiom where OpenAI's training mix may cover different ground.
- **Adversarial cross-review.** Have each model attack the other's output (the `paper-review-lite --codex` pattern); ask Codex to *falsify* a confident Opus conclusion, not merely review it.

Skip Codex when the work is cheaply verifiable — verify instead, decorrelation buys nothing you can just check — or when the answer needs deep in-repo context Codex would have to re-acquire, since the briefing cost then exceeds the benefit. Skip it for mechanical or trivial work. Wanting more confidence in something already verified is not a signal; confidence is not a reason and a checkable artifact is. A consult costs about 10–15s, longer for `--mode implement`; where latency is critical the stakes have to justify the vendor round-trip.

### The high-stakes parallel path (verified)

Launch a **decorrelated** cross-check on the **same** problem, **in one message, blind to each other** — then you synthesize.

- **Fable lead:** you reason the problem yourself and, in the same turn, launch a blind Codex (a different vendor), optionally a blind Opus deep-reasoner; then reconcile your own line against theirs.
- **Opus lead:** the two blind halves are a **deep-reasoner (Opus)** and **Codex (GPT-5.6, `gpt-5.6-sol` by default)**, deliberately different vendors, and you adjudicate rather than supplying one of the halves.

```bash
OSS_ROOT=$(ls -d ~/.claude/plugins/cache/open-science-skills/oss/*/ 2>/dev/null | sort -V | tail -1)
# Codex half — backgrounded, output teed to a file:
"${OSS_ROOT}skills/orchestrate/codex-peer.sh" --mode consult -C "$PWD" \
  --out codex_out.txt --prompt "$(cat routing_q.txt)"
```

…issued in the same turn as an `Agent(subagent_type: "deep-reasoner", prompt: <same routing_q>)`. Neither sees the other's answer. They return complementary lines of reasoning; you merge them.

This is the signature move, and it is verified: this skill's own routing rule came out of one such turn, where the blind Codex and the blind Opus returned complementary halves of one guardrail (fragmentation-on-integration vs. over-trusting your own line).

**Reconciling the answers — the rules you must follow:**

- Never reveal one executor's answer to the other during the round.
- **Do not break ties by confidence.** Substantive disagreement is a *stop condition*, not a coin-flip.
- On disagreement: run **one** targeted reconcile round (now each may see the other's reasoning). If still unresolved, escalate to the human.
- Accept agreement only when both point at the **same checkable artifact** — twin confident assertions are not consensus (they can share a blind spot). This holds doubly when one half is a second Opus.

## Guardrail — the failure modes to defend against

Two names for the same trap.

- **Fragmentation** (the integration view): delegated or fanned-out pieces are each locally correct but conflict when you stitch them together.
- **Over-trusting your own line** (the reconciler view): a *lightweight* lead drifts toward the more fluent answer because it cannot evaluate Opus/Codex output. Your trap is the opposite of rubber-stamping — you are the strongest model here, so you skip the independent check and ship your first line of reasoning. Even the best single model can be confidently wrong on a high-stakes, hard-to-verify call, so on exactly the tasks the parallel path exists for, run the decorrelated cross-check and actually weigh it, rather than waving it through because it agrees or dismissing it because it does not.

**Defense (apply to every delegation and every fan-out):**

1. **Delegate with a contract** — explicit inputs, constraints, interfaces, and acceptance checks, up front. Unspecified design decisions route up to you; they never get guessed down by the cheaper model.
2. **Demand a checkable artifact, not a verdict** — a test that runs, a diff that applies, a cited quote, a reproduction — plus confidence and a "what would make this wrong" note. If a task cannot produce one, that is the signal it belongs on the parallel path.
3. **You retain integration ownership — of correctness *and* rigor.** Verify every returned result against the repository and tests; Agent and Workflow completion messages are not proof of overall completion. Then read the deliverable as the domain expert you are: a fast delegate returns work that is correct but *thin* — an approximate figure where precision matters, a result asserted where the mechanism behind it should be explained, a lone headline where a careful reader needs the comparison or the bound. Add that depth instead of shipping the delegate's summary as-is.
4. On the parallel path, enforce the disagreement-as-gate rule above, and make the decorrelated half a different vendor.

## Gotchas

- **`codex exec` hangs without `< /dev/null`.** It prints `Reading additional input from stdin...` and blocks forever, *even when the prompt is passed as an argument*. `codex-peer.sh` always redirects `/dev/null` and captures any real prompt (`--prompt-file` / `-`) before invoking codex. Never call `codex exec` bare in a background job.
- **Codex reasons at `xhigh` by default; `codex-peer.sh` sets it explicitly** via `--effort xhigh` → `-c model_reasoning_effort=xhigh`, rather than relying on Codex's own implicit default. It prints a header (`model: gpt-5.6-sol`, `sandbox: read-only`) before the answer. The final answer is the text after the last `codex` marker; `--out` captures the whole transcript. A trivial consult is ~5s; a real design question ~10–15s. Pass `--effort` to override per-call for a stronger or cheaper tier.
- **`~/.claude/agents/` may not exist.** The first `cp` fails with `No such file or directory`. `mkdir -p` first (the Setup block does).
- **A named subagent only resolves after its def is installed AND a session reload.** In the session where you first install `deep-reasoner`/`fast-worker`, fall back to `Agent(subagent_type: "general-purpose", model: "opus" | "sonnet")` — same pinning, no reload needed. Inside a Workflow, `agent(..., {model: "opus" | "sonnet"})` needs no installed def at all.
- **Model pins are real.** Verified: the Sonnet spawn reported `model-check: Sonnet 5`; the Opus spawn reported `Running as: Opus (claude-opus-5)`; Codex is pinned to `gpt-5.6-sol` and reports `model: gpt-5.6-sol` in its header. **`gpt-5.6` alone is not a valid slug** — there are three distinct GPT-5.6 tiers (`gpt-5.6-sol` flagship, `gpt-5.6-terra` balanced, `gpt-5.6-luna` fast); the bare `gpt-5.6` triggers a "metadata not found" warning and falls back to whichever tier Codex defaults to. `gpt-5.6-sol` is the default here because it's the strongest peer for a decorrelated cross-check — confirmed working (as of July 2026) on ChatGPT-account-authenticated Codex CLI (an earlier "rejected outright" finding no longer reproduces; if it ever errors, check `codex --version` before assuming a gate, since an outdated CLI rejects sol/luna too, with a different error). Pass `--model gpt-5.6-terra` explicitly for a cheaper peer on routine consults.
- **Keep your own context lean.** Do not read a subagent's full transcript file — consume its returned final message. Long/slow executors go to the background so they never stall the loop. When an investigation's *width* would bloat your context, that width is exactly what belongs on a `deep-reasoner` or a fan-out stage (the "gather then reason" split).
- **A stray global `codex-peer.sh` shadows the plugin's own and can silently drop the model pin.** Earlier docs told you to hand-install `codex-peer.sh` under `~/.claude/skills/`; that copy never updates on plugin upgrade. If it is older than the `--model` pin, it calls bare `codex exec` with no `--model` flag, and Codex falls back to whatever tier it defaults to — observed once as an older, cheaper tier rather than `gpt-5.6-sol`, with no error, so the drift is invisible until you read the `model:` line in Codex's own header. Delete any `~/.claude/skills/orchestrate/codex-peer.sh` (or the older `fable-orchestrate` / `opus-orchestrate` paths) you may have installed under the old instructions; always invoke `"${OSS_ROOT}skills/orchestrate/codex-peer.sh"`. Trust the CLI's printed `model:` header over anything Codex says about itself when asked directly — models cannot reliably self-report their own version.
- **Don't fan out for its own sake.** Fan-outs are cheap to reach for, but a barrier (`parallel()`) wastes wall-clock when one stage lags, and a compact reasoning task (row 3) is faster in your own head than briefed to a peer-strength subagent. Fan out for width, hygiene, parallelism, or independence — not activity.

## Troubleshooting

- **`codex-peer.sh: no prompt`** — pass one of `--prompt "…"`, `--prompt-file PATH`, or `-` (stdin). Empty prompts are rejected.
- **Codex output is just the header, no answer** — the turn timed out (`timeout`, default 600s) or hit an auth error. Check `codex login status`; raise `--timeout` for large `--mode implement` jobs.
- **`codex: command not found`** — install the Codex CLI and `codex login` first. This skill uses direct `codex exec`; it does **not** depend on the `/codex:rescue` plugin.
- **`Workflow` unavailable / not opted in** — the normal case, not a fault: dynamic Workflows are gated per session (org policy, launch gate, or the "Dynamic workflows" setting in `/config`), and nothing this skill does changes that. Fan out with parallel `Agent` calls instead (the routing rule still holds); the only loss is deterministic control flow. Do not argue with the refusal.

## Notes

- **Fable lead versus Opus lead.** Both modes reason in place and delegate execution and parallel work. Fable is the stronger reasoner and the more expensive tier, so a Fable lead is the higher-quality orchestrator and holds more of the hard reasoning itself. An Opus lead is the one to run when Opus is the model you have, or when you specifically want its 1M-context window; it leans harder on structured fan-out, which is what compensates for not being Fable.
- **Why direct `codex exec`, not the `/codex:rescue` plugin?** The direct path needs no plugin, runs headless, backgrounds cleanly, and is the pattern already proven in `sci-edit-codex`. `/codex:rescue --background` is an optional alternative once you've installed `openai/codex-plugin-cc`, but nothing here requires it.
- **Cost shape.** Under a Fable lead the strongest model is on the reasoning, so the lead is the most valuable part of the run rather than the cheapest, and spend leaves your plate only where it does not decide the answer. Under an Opus lead the lead is the priciest model on the team but runs at `medium`, so spend the higher tiers where they are a bounded, verifiable shot — `high` on parallel deep-reasoners whenever width justifies fan-out. Either way Codex spend lands only where the routing rule sends it; the decorrelated cross-check is ~1 extra Codex consult (the Opus-lead parallel path is ~2× a single consult), worth it whenever row 4 fires.
- **Driver:** `codex-peer.sh` (run `--help` for flags). Agent defs: `agents/deep-reasoner.md`, `agents/fast-worker.md`.
