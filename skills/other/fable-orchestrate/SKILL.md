---
name: fable-orchestrate
description: Run a multi-model orchestration workflow with Fable 5 as the lead. Delegate reasoning-heavy work (architecture, debugging, algorithm design) to a deep-reasoner subagent (Opus), mechanical work (boilerplate, tests, formatting, bulk edits) to a fast-worker subagent (Sonnet), and fresh-perspective or high-stakes problems to Codex, a different-vendor GPT-5 peer. Use to orchestrate, delegate, fan out, get a second opinion from Codex, run Opus and Codex in parallel and synthesize, or act as tech lead.
allowed-tools:
  - Agent
  - Bash
  - Read
  - Write
  - Edit
---

# fable-orchestrate

You are the **orchestrator** (intended: Fable 5, reasoning `/effort` max). You plan, decompose, delegate, and synthesize. You do **not** do the heavy lifting yourself — that is the point. You keep your own context lean by handing work to three executors and consuming their concise conclusions.

Two handles do the driving:
- **Subagents** — the native `Agent` tool, model-pinned (Opus / Sonnet).
- **Codex peer** — `~/.claude/skills/fable-orchestrate/codex-peer.sh`, a verified wrapper around `codex exec` (a different-vendor GPT-5 engineer).

## The team

| Executor | Model | Route to it for |
|---|---|---|
| **you** (orchestrator) | Fable 5 | planning, decomposition, synthesis, integration, reconciling others' output |
| **deep-reasoner** | Opus | architecture, complex/multi-file debugging, algorithm design, hard trade-offs, ambiguous specs |
| **fast-worker** | Sonnet | boilerplate, tests-from-spec, formatting, simple edits, renames, bulk transforms |
| **Codex** | GPT-5 (`gpt-5.5`), peer | fresh-perspective problems, unfamiliar stacks, disputed designs, high-stakes parallel cross-checks |

## Setup (one-time)

Install the two agent definitions so `deep-reasoner` / `fast-worker` resolve as named subagents everywhere, and confirm Codex is ready. Paths assume the skill installed globally at `~/.claude/skills/fable-orchestrate/`; adjust if it lives elsewhere (e.g. project-level `./.claude/skills/`).

```bash
mkdir -p ~/.claude/agents
cp ~/.claude/skills/fable-orchestrate/agents/*.md ~/.claude/agents/
chmod +x ~/.claude/skills/fable-orchestrate/codex-peer.sh
codex login status        # must say "Logged in" — otherwise: codex login
```

`mkdir -p` first is required: `~/.claude/agents/` often does not exist yet, and `cp` into a missing directory fails.

Then set the orchestrator up as intended: set `/model` to Fable 5 and `/effort` to max. (The mechanics below work under any main model; Fable-as-lead is what keeps Opus/Codex spend on the work that needs it.)

## Run (the orchestration loop)

**Always show the plan first.** Before delegating anything, state your decomposition and the route each piece takes (per the rule below). Then execute.

### Routing rule — first match wins, top to bottom

| # | If the task is… | Route |
|---|---|---|
| 1 | planning, decomposition, synthesis, integration, or reconciling others' output | **do it yourself** — never delegate the orchestration itself |
| 2 | trivial + single-step, where briefing a subagent costs more than just doing it | **do it yourself** |
| 3 | **high-stakes** — high blast radius **AND** hard to verify (both true) | **Opus + Codex in parallel**, you reconcile |
| 4 | mechanical **and** fully specified (no design decision left; success is objectively checkable) | **fast-worker** (Sonnet) |
| 5 | reasoning-heavy: architecture, complex debug, algorithm design, hard trade-off, ambiguous spec | **deep-reasoner** (Opus) |
| 6 | a genuinely different prior is the point (novel problem, suspected blind spot, "am I framing this wrong?"), or you're looping | **Codex** (instead of, or after, deep-reasoner) |
| 7 | anything left over | **do it yourself** |

**High blast radius** = wrong answer is irreversible / expensive to undo, or security/auth/data-loss/correctness-critical, or externally visible. Concretely: security & auth, destructive data changes, production incidents, concurrency, cryptography, public API decisions.

**The high-stakes parallel path (row 3) fires only when BOTH conditions hold** — high blast radius AND hard to verify. If it is high-stakes but *cheaply verifiable* (a test, a diff that applies, a ground truth to check), use one executor plus a verification step; the parallel cross-check only earns its cost when you *cannot* verify, because then a second independent line of reasoning is the only defense against a confident single-model error.

### Delegate to a subagent

Two equivalent forms — both verified in this environment:

- **Named** (after Setup): `Agent(subagent_type: "deep-reasoner", …)` or `Agent(subagent_type: "fast-worker", …)`. The model is pinned by the agent definition.
- **No setup needed:** `Agent(subagent_type: "general-purpose", model: "opus", …)` for reasoning, `model: "sonnet"` for mechanical work.

Spawn slow work with `run_in_background: true` (the default) and keep planning; you are notified on completion. Consume the subagent's **final message** — it is the return value, not a chat reply. Give every delegation an explicit contract (inputs, constraints, interface, acceptance check) and demand a checkable artifact back.

### Mixing fast-worker (Sonnet) and deep-reasoner (Opus)

Sonnet and Opus often take turns on the *same* task. Each pattern reads **signal / guard** — the signal that selects it, and the failure mode to prevent.

- **Spec then build.** Opus fixes the interface and acceptance check; Sonnet implements. *Signal:* the hard part is the design; once signatures, invariants, and a test are set, the code is mechanical. *Guard:* an under-specified handoff makes Sonnet invent design silently. Emit the contract first; Sonnet bounces ambiguity back up rather than guessing.
- **Draft then harden.** Sonnet writes a fast first cut; Opus reviews and hardens it. *Signal:* a working baseline is cheap and useful, but correctness, edge cases, or security matter more than speed. *Guard:* Opus rubber-stamps a fluent-but-wrong draft. Aim it at failure modes (concurrency, boundaries, auth, error paths) and demand a specific defect list, not polish.
- **Plan then fan out.** Opus plans and partitions; N Sonnet workers do the pieces in parallel. *Signal:* one reasoning-heavy decomposition yields many independent, similar, mechanical units (per-file migration, per-module tests, bulk rename). *Guard:* fragmentation. Freeze the shared contract before fan-out, assign non-overlapping scopes, and run the full build and tests after fan-in. Piecewise-correct is not integrated-correct.
- **Gather then reason.** Sonnet greps and collects; Opus reasons over the digest. *Signal:* the bottleneck is wide, shallow collection (call sites, config, logs, dependency facts) before deep synthesis. *Guard:* Sonnet pre-selecting the cause or dumping raw volume. Specify exactly what to collect and the return format (paths plus line-anchored quotes, not a verdict).
- **Reason then verify.** Opus produces the fix or design; Sonnet writes the test or reproduction that proves it. *Signal:* Opus's output is high-stakes but checkable. *Guard:* a vacuous test that restates the implementation. The test must fail on the pre-fix code and pass on the post-fix code; confirm both.
- **Triage then deep-dive.** Sonnet reproduces and localizes; Opus root-causes; Sonnet applies the bounded fix. *Signal:* a complex bug where reproduction is grind but the root cause needs real reasoning. *Guard:* Sonnet "fixing" a symptom. Its job ends at a reliable minimal repro plus a suspected locus; the fix decision is Opus's, and the repro stays as a regression test.
- **Routine vs. exceptional split.** Sonnet takes the conventional path; Opus owns the one hard subsystem. *Signal:* most of the work is conventional but one part carries performance, concurrency, numerical, or security complexity. *Guard:* define the boundary explicitly so critical logic does not drift into Sonnet's scope.

Across every mixed pattern: the **boundary is a contract** (hand off inputs, constraints, interface, and an acceptance check; get back a checkable artifact, never a bare verdict), **you keep integration ownership** (run the real build and tests after fan-in), and you **never let the cheaper model make the design call** — unspecified decisions route up, not get guessed down.

### Consult Codex (the peer)

```bash
# read-only consult — ask a question / get a second approach; prints the answer
~/.claude/skills/fable-orchestrate/codex-peer.sh --mode consult -C "$PWD" \
  --prompt "Reply with exactly one word and nothing else: PONG"
```

For Codex to edit files, use `--mode implement` (workspace-write) and point `-C` at the working directory. For a long turn, run it via the **Bash tool with `run_in_background: true`** plus `--out <file>`, then `Read` that file when the task-notification fires — so a multi-minute Codex turn never blocks you.

### When to reach for Codex — the decorrelated peer

Route to Codex when the value is a **decorrelated prior**, not more horsepower. Never pick it because it is "better than Opus." Pick it because its errors are *uncorrelated* with Opus's, or because it has a *comparative coverage edge* (a different, sometimes more recent, training mix). A second Opus call resamples the same distribution and tends to repeat the same error confidently. Fire on any one signal:

- **Unverifiable check.** Opus answered, and you need an independent check on a claim you cannot cheaply verify (no test, no ground truth).
- **You are looping.** Two or more rounds have circled the same framing or repeated the same wrong fix. A vendor switch breaks the fixation.
- **Disputed, expensive-to-undo design.** API shape, schema, concurrency model, or migration strategy where reasonable engineers disagree and being wrong is costly.
- **High-stakes parallel path (row 3).** High blast radius *and* hard to verify: launch Opus and Codex blind, then reconcile.
- **"Am I framing this wrong?"** You suspect your own decomposition, not the answer within it.
- **Unfamiliar or recent ecosystem.** A stack, library, or idiom where OpenAI's training mix may cover different ground.
- **Adversarial cross-review.** Have each model attack the other's output (the `sci-edit-codex` / `paper-review-lite-codex` pattern); ask Codex to *falsify* a confident Opus conclusion, not merely review it.

Do **not** reach for Codex when:

- The task is **cheaply verifiable** (a test runs, a type checks, a diff applies). Verify instead; decorrelation buys nothing you can just check.
- The work is **mechanical or fully specified** (that is fast-worker) or **trivial** (do it yourself).
- The answer needs **deep in-repo context** Codex would have to re-acquire. The briefing cost exceeds the benefit; keep it with Opus.
- You **only want more confidence** on something Opus already verified. Confidence is not a reason; a checkable artifact is.
- **Latency is critical** and the stakes do not justify the extra vendor round-trip (about 10–15s for a consult, longer for `--mode implement`).

### The high-stakes parallel path (verified)

Launch **both** executors on the **same** problem, **in one message, blind to each other** — then you synthesize. This is the signature move; it is how this very skill's routing rule was written. The two calls were:

```bash
# Codex half — backgrounded, output teed to a file:
~/.claude/skills/fable-orchestrate/codex-peer.sh --mode consult -C "$PWD" \
  --out codex_out.txt --prompt "$(cat routing_q.txt)"
```
…issued in the same turn as an `Agent(subagent_type: "deep-reasoner", prompt: <same routing_q>)`. Neither saw the other's answer. They returned **complementary halves of one guardrail** (fragmentation-on-integration vs. lightest-model-rubber-stamping); the orchestrator merged them into the rule above and the guardrail below.

**Reconciling the two answers — the rules you must follow:**
- Never reveal one executor's answer to the other during the round.
- **Do not break ties by confidence.** Substantive disagreement is a *stop condition*, not a coin-flip.
- On disagreement: run **one** targeted reconcile round (now each may see the other's reasoning). If still unresolved, escalate to the human.
- Accept agreement only when both point at the **same checkable artifact** — twin confident assertions are not consensus (they can share a blind spot).

## Guardrail — the one failure mode to defend against

Two names for the same trap, one defense:

- **Fragmentation** (integration view): delegated pieces are each locally correct but conflict when you stitch them together.
- **Rubber-stamping** (reconciler view): you are the *lightest* model, judging Opus/Codex output you often cannot yourself evaluate — so you drift toward the more fluent, more confident answer. This bites hardest on exactly the high-stakes, hard-to-verify tasks the parallel path exists to protect.

**Defense (apply to every delegation):**
1. **Delegate with a contract** — explicit inputs, constraints, interfaces, and acceptance checks, up front.
2. **Demand a checkable artifact, not a verdict** — a test that runs, a diff that applies, a cited quote, a reproduction — plus confidence and a "what would make this wrong" note. If a task cannot produce one, that is the signal it belongs on the parallel path.
3. **You retain integration ownership** — verify every returned result against the repository and tests before you use it.
4. On the parallel path, enforce the disagreement-as-gate rule above.

## Gotchas

- **`codex exec` hangs without `< /dev/null`.** It prints `Reading additional input from stdin...` and blocks forever, *even when the prompt is passed as an argument*. `codex-peer.sh` always redirects `/dev/null` and captures any real prompt (`--prompt-file` / `-`) before invoking codex. Never call `codex exec` bare in a background job.
- **Codex reasons at `xhigh` by default** and prints a header (`model: gpt-5.5`, `sandbox: read-only`) before the answer. The final answer is the text after the last `codex` marker; `--out` captures the whole transcript. A trivial consult is ~5s; a real design question ~10–15s.
- **`~/.claude/agents/` may not exist.** The first `cp` fails with `No such file or directory`. `mkdir -p` first (the Setup block does).
- **A named subagent only resolves after its def is installed AND a session reload.** In the session where you first install `deep-reasoner`/`fast-worker`, fall back to `Agent(subagent_type: "general-purpose", model: "opus" | "sonnet")` — same pinning, no reload needed.
- **Model pins are real.** Verified this session: the Sonnet spawn reported `model-check: Sonnet 5`; the Opus spawn reported `Running as: Opus (claude-opus-4-8)`; Codex reported `model: gpt-5.5`.
- **Keep your own context lean.** Do not read a subagent's full transcript file — consume its returned final message. Long/slow executors go to the background so they never stall the loop.

## Troubleshooting

- **`codex-peer.sh: no prompt`** — pass one of `--prompt "…"`, `--prompt-file PATH`, or `-` (stdin). Empty prompts are rejected.
- **Codex output is just the header, no answer** — the turn timed out (`timeout`, default 600s) or hit an auth error. Check `codex login status`; raise `--timeout` for large `--mode implement` jobs.
- **`codex: command not found`** — install the Codex CLI and `codex login` first. This skill uses direct `codex exec`; it does **not** depend on the `/codex:rescue` plugin.

## Notes

- **Why direct `codex exec`, not the `/codex:rescue` plugin?** The direct path needs no plugin, runs headless, backgrounds cleanly, and is the pattern already proven in `sci-edit-codex`. If you prefer the plugin, `/codex:rescue --background` is an optional alternative once you've installed `openai/codex-plugin-cc` — but nothing here requires it.
- **Cost shape:** the orchestrator is the cheapest model; reasoning spend lands on Opus/Codex only when the routing rule sends it there. The parallel path is ~2× a single consult — spend it only when row 3 fires.
- **Driver:** `codex-peer.sh` (run `--help` for flags). Agent defs: `agents/deep-reasoner.md`, `agents/fast-worker.md`.
