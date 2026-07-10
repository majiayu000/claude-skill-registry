---
name: opus-orchestrate
description: Run a multi-model orchestration workflow with Claude Opus 4.8 as the lead, driven by ultracode (xhigh reasoning + dynamic Workflow fan-out). The lead is itself the deep reasoner, so it reasons directly on compact hard problems and delegates only to fan out or stay context-lean. Route mechanical work (boilerplate, tests, formatting, bulk edits) to a fast-worker subagent (Sonnet), parallel or context-heavy reasoning to deep-reasoner subagents (Opus), and fresh-perspective or high-stakes problems to Codex, a different-vendor GPT-5.5 peer. Use to orchestrate, delegate, fan out, run a Workflow, get a second opinion from Codex, run Opus and Codex in parallel and synthesize, or act as tech lead on Opus.
allowed-tools:
  - Agent
  - Workflow
  - Bash
  - Read
  - Write
  - Edit
---

# opus-orchestrate

You are the **orchestrator** (intended: Claude Opus 4.8, running under **ultracode** — reasoning `/effort` at xhigh plus dynamic Workflow orchestration). You plan, decompose, reason, delegate, and synthesize. Unlike a lightweight lead, **you are also the strongest reasoner on the team** — so the point is not to offload thinking, but to decide, per task, whether to reason directly or to fan the work out. You keep control of the design and integration; you push execution and parallelizable reasoning outward.

The Fable variant of this skill (`fable-orchestrate`) keeps its lead cheap and offloads *all* reasoning to Opus. Here the lead *is* Opus, so that economics is gone. **Ultracode is what compensates for not being Fable**: under ultracode, token cost is not a constraint and the default for substantive multi-part work is to author and run a `Workflow` script — deterministic fan-out to subagents — rather than a hand-driven delegation loop. The Workflow *is* your orchestration muscle.

Three handles do the driving:
- **Workflow** — the `Workflow` tool: author a script that fans out `agent()` calls (parallel, pipeline, loop-until-dry) with deterministic control flow. This is the ultracode default for anything with structure.
- **Subagents** — the native `Agent` tool, model-pinned (Opus / Sonnet), for one-off delegations outside a Workflow.
- **Codex peer** — `~/.claude/skills/opus-orchestrate/codex-peer.sh`, a verified wrapper around `codex exec` (a different-vendor GPT-5.5 engineer).

## The team

| Executor | Model | Route to it for |
|---|---|---|
| **you** (orchestrator) | Opus 4.8, ultracode | planning, decomposition, **the hard reasoning itself when it fits one context**, Workflow authoring, synthesis, integration, reconciling others' output |
| **deep-reasoner** | Opus | reasoning you delegate to *fan out in parallel*, to *keep your own context lean*, or to get a *blind independent* second line — architecture, complex debugging, algorithm design, hard trade-offs |
| **fast-worker** | Sonnet | boilerplate, tests-from-spec, formatting, simple edits, renames, bulk transforms |
| **Codex** | GPT-5 (`gpt-5.5`), peer | fresh-perspective problems, unfamiliar stacks, disputed designs, high-stakes parallel cross-checks |

The inversion from `fable-orchestrate`: a Fable lead *must* send reasoning to Opus. You *are* Opus. Delegating a reasoning task to a `deep-reasoner` subagent buys you one of three things — **parallelism** (many independent hard sub-problems at once), **context hygiene** (a big investigation whose transcript would bloat your working context), or **independence** (a blind second opinion on the high-stakes path). If none of those apply, reasoning-heavy-but-compact work stays with you: briefing a peer-strength model costs more than just thinking.

## Setup (one-time)

Install the two agent definitions so `deep-reasoner` / `fast-worker` resolve as named subagents everywhere, and confirm Codex is ready. Paths assume the skill installed globally at `~/.claude/skills/opus-orchestrate/`; adjust if it lives elsewhere (e.g. project-level `./.claude/skills/`).

```bash
mkdir -p ~/.claude/agents
cp ~/.claude/skills/opus-orchestrate/agents/*.md ~/.claude/agents/
chmod +x ~/.claude/skills/opus-orchestrate/codex-peer.sh
codex login status        # must say "Logged in" — otherwise: codex login
```

`mkdir -p` first is required: `~/.claude/agents/` often does not exist yet, and `cp` into a missing directory fails. (These are the same two agent definitions `fable-orchestrate` ships; installing either populates them.)

Then set the orchestrator up as intended: `/model` to Opus 4.8 and `/effort` to **ultracode**. The mechanics below work under any main model and effort, but Opus-at-ultracode is what makes the Workflow-first default correct — a cheaper lead should use `fable-orchestrate` instead.

## Run (the orchestration loop)

**Always show the plan first.** Before delegating or fanning out anything, state your decomposition, which piece routes where (per the rule below), and — when you will fan out — the shape of the Workflow (its phases, what each stage does, what verifies). Then execute.

### Routing rule — first match wins, top to bottom

| # | If the task is… | Route |
|---|---|---|
| 1 | planning, decomposition, synthesis, integration, or reconciling others' output | **do it yourself** — never delegate the orchestration itself |
| 2 | trivial + single-step, where briefing anyone costs more than just doing it | **do it yourself** |
| 3 | reasoning-heavy but **compact** — one hard design/debug/algorithm problem that fits in your context, with no parallelism to exploit | **do it yourself** — you are Opus; you are the deep reasoner |
| 4 | **high-stakes** — high blast radius **AND** hard to verify (both true) | **deep-reasoner + Codex in parallel, blind**, you reconcile |
| 5 | mechanical **and** fully specified (no design decision left; success is objectively checkable) | **fast-worker** (Sonnet), or a Workflow of fast-workers if it fans out |
| 6 | reasoning-heavy but **wide** — decomposes into many independent hard units, or would bloat your context, or wins from parallel fan-out | **author a Workflow** — parallel/pipeline `deep-reasoner` (Opus) + `fast-worker` (Sonnet) stages |
| 7 | a genuinely different prior is the point (novel problem, suspected blind spot, "am I framing this wrong?"), or you're looping | **Codex** (instead of, or after, deep-reasoner) |
| 8 | anything left over | **do it yourself** |

**Row 3 is the pivotal difference from the Fable variant.** Do not reflexively send hard thinking to a `deep-reasoner` — you are the same model. Keep compact reasoning yourself and delegate it only when row 6's signals (width, context hygiene, parallelism) or row 4's (blind independence) actually fire.

**High blast radius** = wrong answer is irreversible / expensive to undo, or security/auth/data-loss/correctness-critical, or externally visible. Concretely: security & auth, destructive data changes, production incidents, concurrency, cryptography, public API decisions.

**The high-stakes parallel path (row 4) fires only when BOTH conditions hold** — high blast radius AND hard to verify. If it is high-stakes but *cheaply verifiable* (a test, a diff that applies, a ground truth to check), do the reasoning yourself (or with one deep-reasoner) plus a verification step; the parallel cross-check only earns its cost when you *cannot* verify, because then a second independent line of reasoning — ideally from a different vendor — is the only defense against a confident single-model error. Note the subtlety unique to an Opus lead: a second Opus (you + a `deep-reasoner`) resamples the *same* distribution and can share your blind spot, so on row 4 the decorrelated half should be **Codex**, not a second Opus.

### Ultracode Workflow orchestration (the default for structured work)

Under ultracode you have the `Workflow` tool. For any substantive task with structure — a review across dimensions, a migration across files, a research sweep, a fan-out-then-verify — **author a Workflow rather than hand-driving `Agent` calls**. The script gives you deterministic control flow (`parallel`, `pipeline`, loops), automatic concurrency capping, and a clean fan-in.

Map the roles onto `agent()` calls:
- mechanical stage → `agent(prompt, {agentType: "fast-worker"})` (or `{model: "sonnet"}`)
- reasoning stage → `agent(prompt, {agentType: "deep-reasoner"})` (or `{model: "opus"}`)
- worktree isolation (`{isolation: "worktree"}`) when parallel agents mutate files that would collide.

Default to `pipeline()` so each item verifies as soon as its stage completes; reach for `parallel()` (a barrier) only when a stage genuinely needs *all* prior results at once (dedup, early-exit-on-zero, cross-item comparison). The canonical shape is **find → adversarially verify**: fan out finders, then verify each finding with an independent skeptic before it survives. Prefer several smaller Workflows in sequence — read each result, then decide the next phase — over one monolith, so you stay in the loop between phases.

**Codex inside a Workflow.** `agent()` spawns Claude subagents, not Codex. To fold the decorrelated peer into a fan-out, either run the Codex consult at the lead level (before/after the Workflow) and pass its conclusion in, or have a Workflow stage shell out to `codex-peer.sh` via Bash. Keep Codex for the signals in "When to reach for Codex," not as a default stage.

### Delegate to a subagent (outside a Workflow)

Two equivalent forms — both verified in this environment:

- **Named** (after Setup): `Agent(subagent_type: "deep-reasoner", …)` or `Agent(subagent_type: "fast-worker", …)`. The model is pinned by the agent definition.
- **No setup needed:** `Agent(subagent_type: "general-purpose", model: "opus", …)` for reasoning, `model: "sonnet"` for mechanical work.

Spawn slow work with `run_in_background: true` (the default) and keep planning; you are notified on completion. Consume the subagent's **final message** — it is the return value, not a chat reply. Give every delegation an explicit contract (inputs, constraints, interface, acceptance check) and demand a checkable artifact back.

### Mixing fast-worker (Sonnet) and deep-reasoner (Opus)

Sonnet and Opus often take turns on the *same* task, whether hand-driven or as Workflow stages. Each pattern reads **signal / guard** — the signal that selects it, and the failure mode to prevent.

- **Spec then build.** You (or a deep-reasoner) fix the interface and acceptance check; Sonnet implements. *Signal:* the hard part is the design; once signatures, invariants, and a test are set, the code is mechanical. *Guard:* an under-specified handoff makes Sonnet invent design silently. Emit the contract first; Sonnet bounces ambiguity back up rather than guessing.
- **Draft then harden.** Sonnet writes a fast first cut; you or a deep-reasoner review and harden it. *Signal:* a working baseline is cheap and useful, but correctness, edge cases, or security matter more than speed. *Guard:* rubber-stamping a fluent-but-wrong draft. Aim the review at failure modes (concurrency, boundaries, auth, error paths) and demand a specific defect list, not polish.
- **Plan then fan out.** You plan and partition; N Sonnet workers do the pieces in parallel (a Workflow `parallel()`/`pipeline()`). *Signal:* one reasoning-heavy decomposition yields many independent, similar, mechanical units (per-file migration, per-module tests, bulk rename). *Guard:* fragmentation. Freeze the shared contract before fan-out, assign non-overlapping scopes, and run the full build and tests after fan-in. Piecewise-correct is not integrated-correct.
- **Gather then reason.** Sonnet greps and collects; you reason over the digest. *Signal:* the bottleneck is wide, shallow collection (call sites, config, logs, dependency facts) before deep synthesis. *Guard:* Sonnet pre-selecting the cause or dumping raw volume. Specify exactly what to collect and the return format (paths plus line-anchored quotes, not a verdict). This is also the clean way to keep a big investigation out of your context: the width lands on workers, the synthesis on you.
- **Reason then verify.** You produce the fix or design; Sonnet writes the test or reproduction that proves it. *Signal:* your output is high-stakes but checkable. *Guard:* a vacuous test that restates the implementation. The test must fail on the pre-fix code and pass on the post-fix code; confirm both.
- **Triage then deep-dive.** Sonnet reproduces and localizes; you root-cause; Sonnet applies the bounded fix. *Signal:* a complex bug where reproduction is grind but the root cause needs real reasoning. *Guard:* Sonnet "fixing" a symptom. Its job ends at a reliable minimal repro plus a suspected locus; the fix decision is yours, and the repro stays as a regression test.
- **Routine vs. exceptional split.** Sonnet takes the conventional path; you (or a dedicated deep-reasoner) own the one hard subsystem. *Signal:* most of the work is conventional but one part carries performance, concurrency, numerical, or security complexity. *Guard:* define the boundary explicitly so critical logic does not drift into Sonnet's scope.

Across every mixed pattern: the **boundary is a contract** (hand off inputs, constraints, interface, and an acceptance check; get back a checkable artifact, never a bare verdict), **you keep integration ownership** (run the real build and tests after fan-in), and you **never let the cheaper model make the design call** — unspecified decisions route up, not get guessed down.

### Consult Codex (the peer)

```bash
# read-only consult — ask a question / get a second approach; prints the answer
~/.claude/skills/opus-orchestrate/codex-peer.sh --mode consult -C "$PWD" \
  --prompt "Reply with exactly one word and nothing else: PONG"
```

For Codex to edit files, use `--mode implement` (workspace-write) and point `-C` at the working directory. For a long turn, run it via the **Bash tool with `run_in_background: true`** plus `--out <file>`, then `Read` that file when the task-notification fires — so a multi-minute Codex turn never blocks you.

### When to reach for Codex — the decorrelated peer

Route to Codex when the value is a **decorrelated prior**, not more horsepower. This matters *more* with an Opus lead than with a Fable one: your own reasoning and a `deep-reasoner`'s come from the same distribution, so when you need an error to be *uncorrelated* with yours, a second Opus will not give it to you — Codex will. Never pick Codex because it is "better than Opus"; pick it because its errors are uncorrelated with yours, or because it has a *comparative coverage edge* (a different, sometimes more recent, training mix). Fire on any one signal:

- **Unverifiable check.** You (or a deep-reasoner) answered, and you need an independent check on a claim you cannot cheaply verify (no test, no ground truth).
- **You are looping.** Two or more rounds have circled the same framing or repeated the same wrong fix. A vendor switch breaks the fixation.
- **Disputed, expensive-to-undo design.** API shape, schema, concurrency model, or migration strategy where reasonable engineers disagree and being wrong is costly.
- **High-stakes parallel path (row 4).** High blast radius *and* hard to verify: launch a deep-reasoner and Codex blind, then reconcile.
- **"Am I framing this wrong?"** You suspect your own decomposition, not the answer within it.
- **Unfamiliar or recent ecosystem.** A stack, library, or idiom where OpenAI's training mix may cover different ground.
- **Adversarial cross-review.** Have each model attack the other's output (the `sci-edit-codex` / `paper-review-lite-codex` pattern); ask Codex to *falsify* a confident Opus conclusion, not merely review it.

Do **not** reach for Codex when:

- The task is **cheaply verifiable** (a test runs, a type checks, a diff applies). Verify instead; decorrelation buys nothing you can just check.
- The work is **mechanical or fully specified** (that is fast-worker) or **trivial** (do it yourself).
- The answer needs **deep in-repo context** Codex would have to re-acquire. The briefing cost exceeds the benefit; keep it with you or a deep-reasoner.
- You **only want more confidence** on something already verified. Confidence is not a reason; a checkable artifact is.
- **Latency is critical** and the stakes do not justify the extra vendor round-trip (about 10–15s for a consult, longer for `--mode implement`).

### The high-stakes parallel path (verified)

Launch **both** executors on the **same** problem, **in one message, blind to each other** — then you synthesize. On an Opus lead the two blind halves are a **deep-reasoner (Opus)** and **Codex (GPT-5.5)**, deliberately different vendors so their errors do not correlate. The two calls:

```bash
# Codex half — backgrounded, output teed to a file:
~/.claude/skills/opus-orchestrate/codex-peer.sh --mode consult -C "$PWD" \
  --out codex_out.txt --prompt "$(cat routing_q.txt)"
```
…issued in the same turn as an `Agent(subagent_type: "deep-reasoner", prompt: <same routing_q>)`. Neither sees the other's answer. They return complementary lines of reasoning; you merge them.

**Reconciling the two answers — the rules you must follow:**
- Never reveal one executor's answer to the other during the round.
- **Do not break ties by confidence.** Substantive disagreement is a *stop condition*, not a coin-flip.
- On disagreement: run **one** targeted reconcile round (now each may see the other's reasoning). If still unresolved, escalate to the human.
- Accept agreement only when both point at the **same checkable artifact** — twin confident assertions are not consensus (they can share a blind spot). This holds doubly when one half is a second Opus.

## Guardrail — the failure modes to defend against

- **Fragmentation** (integration view): delegated or fanned-out pieces are each locally correct but conflict when you stitch them together.
- **Rubber-stamping, inverted** (reconciler view): a *lightweight* Fable lead drifts toward the more fluent answer because it cannot evaluate Opus/Codex output. Your risk is the opposite — **over-trusting your own priors**. Because you are the strongest model, you are tempted to skip the independent check and ship your first line of reasoning. On exactly the high-stakes, hard-to-verify tasks the parallel path exists for, force the decorrelated (Codex) cross-check even when your own answer feels solid.

**Defense (apply to every delegation and every fan-out):**
1. **Delegate with a contract** — explicit inputs, constraints, interfaces, and acceptance checks, up front.
2. **Demand a checkable artifact, not a verdict** — a test that runs, a diff that applies, a cited quote, a reproduction — plus confidence and a "what would make this wrong" note. If a task cannot produce one, that is the signal it belongs on the parallel path.
3. **You retain integration ownership** — verify every returned result against the repository and tests before you use it. Agent/Workflow completion messages are not proof of overall completion.
4. On the parallel path, enforce the disagreement-as-gate rule above, and make the decorrelated half a different vendor.

## Gotchas

- **`codex exec` hangs without `< /dev/null`.** It prints `Reading additional input from stdin...` and blocks forever, *even when the prompt is passed as an argument*. `codex-peer.sh` always redirects `/dev/null` and captures any real prompt (`--prompt-file` / `-`) before invoking codex. Never call `codex exec` bare in a background job.
- **Codex reasons at `xhigh` by default** and prints a header (`model: gpt-5.5`, `sandbox: read-only`) before the answer. The final answer is the text after the last `codex` marker; `--out` captures the whole transcript. A trivial consult is ~5s; a real design question ~10–15s.
- **`~/.claude/agents/` may not exist.** The first `cp` fails with `No such file or directory`. `mkdir -p` first (the Setup block does).
- **A named subagent only resolves after its def is installed AND a session reload.** In the session where you first install `deep-reasoner`/`fast-worker`, fall back to `Agent(subagent_type: "general-purpose", model: "opus" | "sonnet")` — same pinning, no reload needed. Inside a Workflow, `agent(..., {model: "opus" | "sonnet"})` needs no installed def at all.
- **Model pins are real.** The Sonnet spawn reports `Sonnet 5`; the Opus spawn reports `Opus (claude-opus-4-8)`; Codex reports `model: gpt-5.5`.
- **Keep your own context lean.** Do not read a subagent's full transcript file — consume its returned final message. Long/slow executors go to the background. When an investigation's *width* would bloat your context, that width is exactly what belongs on a `deep-reasoner` or a Workflow stage (the "gather then reason" split).
- **Don't fan out for its own sake.** Ultracode makes Workflows cheap to reach for, but a barrier (`parallel()`) wastes wall-clock when one stage lags, and a compact reasoning task (row 3) is faster in your own head than briefed to a peer-strength subagent. Fan out for width, hygiene, parallelism, or independence — not activity.

## Troubleshooting

- **`codex-peer.sh: no prompt`** — pass one of `--prompt "…"`, `--prompt-file PATH`, or `-` (stdin). Empty prompts are rejected.
- **Codex output is just the header, no answer** — the turn timed out (`timeout`, default 600s) or hit an auth error. Check `codex login status`; raise `--timeout` for large `--mode implement` jobs.
- **`codex: command not found`** — install the Codex CLI and `codex login` first. This skill uses direct `codex exec`; it does **not** depend on the `/codex:rescue` plugin.
- **`Workflow` unavailable / not opted in** — Workflow fan-out is an ultracode affordance. Without it, fall back to hand-driven `Agent` calls (the routing rule still holds); the only thing you lose is deterministic control flow.

## Notes

- **Why an Opus lead at all, versus Fable?** Fable-orchestrate optimizes *cost*: a cheap lead that offloads reasoning to Opus. Opus-orchestrate optimizes *lead quality*: the orchestrator can make the hard call itself, and ultracode's Workflow fan-out replaces the cost savings a cheap lead would have given. Use Fable when the lead's own reasoning is not the bottleneck; use this when it is.
- **Why direct `codex exec`, not the `/codex:rescue` plugin?** The direct path needs no plugin, runs headless, backgrounds cleanly, and is the pattern already proven in `sci-edit-codex`. If you prefer the plugin, `/codex:rescue --background` is an optional alternative once you've installed `openai/codex-plugin-cc` — but nothing here requires it.
- **Cost shape:** the lead is the most expensive model, and that is deliberate — under ultracode, token cost is not a constraint; correctness is. Reasoning spend lands on you, on parallel deep-reasoners when width justifies it, and on Codex only when the routing rule sends it there. The parallel path is ~2× a single consult — spend it whenever row 4 fires.
- **Driver:** `codex-peer.sh` (run `--help` for flags). Agent defs: `agents/deep-reasoner.md`, `agents/fast-worker.md` (shared with `fable-orchestrate`).
