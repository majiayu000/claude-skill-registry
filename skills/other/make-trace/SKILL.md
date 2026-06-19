---
name: make-trace
description: Turn any source that describes how a kind of task gets done (a SKILL.md, a chat log, a runbook, plain prose) into a runnable Morph trace. Lift it into a DAG, write a contract per step, place inputs, and drive the full run lifecycle to verify it. Use whenever someone wants to make a trace from a source.
---

# Make Trace

You turn a **source** (anything that describes how a kind of task gets done) into a **trace**: a folder holding a DAG that a human and an AI both read while the work runs. This skill covers the whole path, from a blank folder to a finished run.

## Before you start

Two reads give you the full surface. Do them once:

1. `references/CLI.md` (bundled next to this file) is the system contract: every command, the `trace.json` schema, the reply payload schema, the path rules, the state machine.
2. The source itself. Read it closely; the steps you need are usually hiding in its prose. For a large or multi-file source, read the spine in full (the main document and any workflow section) and only sample the rest to confirm a step exists, rather than reading every file to the same depth.

The `flowtrace` binary drives everything. Get it in this order: honor `$TRACE_BIN` if it is set; else use it if it is on your `PATH`; else, inside a flowtrace checkout, use the build under `target/` (`target/release/flowtrace`, else `target/debug/flowtrace`) or build one with `./scripts/install.sh` from the repo root; else clone the repo first (`git clone https://github.com/AIScientists-Dev/Flowtrace.git`) and run its `./scripts/install.sh`. Building needs Node and Rust and takes a few minutes the first time — it builds the web UI and the CLI and symlinks `flowtrace` to `~/.local/bin`. When you forget a shape mid-task, the binary self-documents: `flowtrace <cmd> --help`, and `flowtrace explain <type>` (e.g. `flowtrace explain trace`, `flowtrace explain reply`).

## The cycle

### 1. Scaffold

```bash
cd <wherever you keep traces>   # conventionally ~/traces/
flowtrace init <slug>               # creates <slug>/ with .git and an empty trace.json
```

`flowtrace init` makes a subfolder named `<slug>` under the current directory, not in place.

### 2. Lift the source into a DAG (the hard part)

Read the source and pull out the steps hiding in it. Fill `trace.json#steps`, and for each step set `from_steps`, its upstream dependencies. The DAG is the whole point: decide what runs in parallel and what fans in.

**The arrows are the knowledge.** A source often reads as a flat list, but the real shape is a fan-in/fan-out graph. Do not flatten it into a straight line. Common patterns: independent ingests run as parallel roots and fan in at a join; an analysis branch and a recommendation branch fan out from the same join; the final write-up fans in from everything. Some sources are honestly sequential, though; a step-by-step creative pipeline really is a straight line, and forcing fake parallelism onto it is its own kind of unfaithful. Lift the shape that is actually there.

**What becomes a node vs. folded into a `STEP.md`.** Promote something to its own step only if it is a distinct cognitive move with its own input and output. If it is *how to do* an existing step (a rule, a special case, a reference detail), fold it into that step's `STEP.md` instead. This is the criterion that keeps a 25-file source from exploding into 25 nodes.

**Mutually-exclusive paths are not one trace.** If the source branches on input into paths that produce different deliverables (make a film *or* a deck *or* a prototype), that is several traces sharing an early spine, not one trace full of conditionals; traces describe shape, not control flow. Split on the deliverable. Same deliverable reached by a different internal pipeline is still one trace, though; branch inside a `STEP.md`, not in the DAG. Split on the deliverable, not on method.

Then check it:

```bash
flowtrace validate
flowtrace show --fmt mermaid
```

### 3. Verify faithfulness (do not skip)

Lifting is judgment, and judgment flattens fan-in/fan-out graphs into straight lines that are wrong. Have a **second, independent** pass (a fresh agent is ideal) compare your DAG against the source: does every step appear, is every dependency real, was anything dropped or invented? Fix what it finds. This catches the mistakes you cannot see in your own lift.

If you cannot spawn a fresh agent, do it cold yourself: set your DAG aside, re-read the source from scratch, re-derive the edge list independently, then diff that against what you built. Reconcile every difference before moving on.

### 4. Write a contract per step

Each step gets a `steps/<id>/STEP.md`: a short Markdown file with optional YAML frontmatter on top and prose below. The frontmatter `reads`/`writes` show up in the UI; the body says how to do the step. Fold cross-cutting guidance (do's/don'ts, special cases) into the steps they affect.

```markdown
---
name: score_bullets
description: Score each resume bullet against the keywords.
reads:
  - extract_keywords/keywords.json
  - resources/resume_before.md
writes:
  - bullet_scores.json
---

# Score Bullets

Read the keywords and the parsed resume, then score every bullet 0 to 1 by
relevance and note the gap on each. Scoring is judgment, not keyword counting.
```

### 5. Provide inputs

A run's inputs are plain files. There is no `inputs` field. Drop the input files in the trace's `resources/` folder, and point the relevant step's `reads:` at them. Paths in `reads:`/`writes:` are written relative to the trace root: a resource reads as `resources/<file>`, an upstream step's asset as `<step_id>/<file>`.

### 6. Run the lifecycle

Each CLI write makes one git commit. For every step: mark it running, produce its asset on disk, mark it done with that asset, and emit a structured reply. Then close the deliverable.

**The reply is how each step shows its work — write it rich, not bare.** A bare `{ "headline", "status" }` renders as a lonely title and wastes the step. Before you write replies, read the schema instead of writing from memory: `flowtrace explain reply` lists the top-level fields, and `flowtrace explain reply.evidence` lists the typed evidence blocks and each block's own options (e.g. a figure's caption). Use what they document and match the reply to what the step actually produced. Skipping this read is the single most common reason a reply lands as just a title with nothing under it.

```bash
RUN=$(flowtrace run new --name "first run" | tail -1)

flowtrace step <id> running --message "..."
#   ... do the step's work; write its asset under runs/$RUN/<id>/ ...
flowtrace step <id> done --asset <file>
flowtrace reply < reply.json
# ... repeat for every step, then:

flowtrace deliverable done --asset <step_id>/<final-output>
flowtrace run show          # confirm every step is done and the deliverable is done
```

### 7. Watch it

```bash
flowtrace serve             # opens the DAG at http://localhost:3000
```

## Reuse a trace on new input

A finished trace is a method, not a one-off: run it again on new input and you reuse the structure instead of rebuilding it. The plan stays put — `trace.json` and the `STEP.md` contracts do not change. You start a fresh run and regenerate the contents inside it.

Inputs are files, not declared variables: `from_inputs` and a step's `reads:` are cosmetic labels for the UI, never consumed at runtime. So reuse is four moves — recover the plan, open a new run, swap the input files, drive the lifecycle again.

**0. Recover the plan.** If you did not build this trace, you do not know its step IDs, their order, or each step's asset filename — and the snippets below are all placeholders (`<id>`, `<file>`, `<step_id>`). Read them off the trace, don't guess:

```bash
flowtrace show --fmt json | jq -r '.steps | keys[]'   # the step IDs (unordered)
flowtrace show --fmt mermaid                           # the edges — drive steps in dependency order, roots first
```

Each step's declared asset filename is `trace.json#steps.<id>.assets`; the deliverable's asset list (run-relative paths) is `trace.json#deliverable.assets` — reuse the same set when you close the deliverable. The body of each `steps/<id>/STEP.md` tells you what that asset should contain.

```bash
RUN=$(flowtrace run new --name "<new instance>" | tail -1)   # a fresh, isolated run
```

1. **Swap the input.** Replace **every** file under `resources/` that this run should change — a trace often has more than one input, and swapping only some silently mixes new and old (the CLI never reads these files, so it cannot warn you). The CLI only ever commits `state.json` and declared assets, never your input files — so commit them yourself if you want the new input in the history:

```bash
git add resources/ && git commit -m "swap inputs: <new instance>"
```

2. **Drive the lifecycle for this run.** Exactly step 6 again, in dependency order, with `--run "$RUN"` on **every** write (`step`, `reply`, and `deliverable` all take it). Pass it every time: omit it and the CLI targets the *most recently created* run, which is your new run only until any other run appears — then an un-`--run`'d write lands in the wrong run with no error. For each step: mark it `running` (the step folder need not exist yet), then write its asset under `runs/$RUN/<id>/`, then `done --asset` (which fails if the file is not on disk), then emit a reply. Then close the deliverable.

```bash
flowtrace step <id> running --run "$RUN" --message "..."
mkdir -p "runs/$RUN/<id>"
#   ... regenerate the step's asset at runs/$RUN/<id>/<file> from the new input ...
flowtrace step <id> done --asset <file> --run "$RUN"   # --asset is step-relative: just <file>
flowtrace reply --run "$RUN" < reply.json
# ... every step in dependency order, then close with the deliverable's own asset set:
flowtrace deliverable done --asset <step_id>/<final-output> --run "$RUN"   # --asset is run-relative here
```

Runs are isolated: each `runs/<run_id>/` carries its own assets and `state.json`, so a new run never disturbs an earlier one. `flowtrace run list` shows them side by side, and every prior run's outputs stay exactly as they were. (Re-entering a *step within one run* to redo it, after changing your mind about a node, is a different move — steering, covered next.)

## Steer a run: change a step, re-run what depends on it

Steering is the other half of a live run: you changed your mind about a step and want that change to flow through, without starting over. It stays inside the *same* run — `done` is not final, so you re-enter the step and re-run only what depended on it. (Reuse opens a new run for new input; steering edits a node within one run.)

The CLI does not track staleness for you — the trace is soft, you own propagation. Ask it for the exact set to re-run — `show` reads the static plan, so it takes no `--run`:

```bash
flowtrace show --downstream <id>   # the step's transitive dependents, in topological order
```

1. **Redo the step you changed** — re-enter it and produce its new asset, exactly as in step 6. The re-run writes below take `--run "$RUN"` (the run you are steering; omit it for the latest):

```bash
flowtrace step <id> running --run "$RUN" --message "why you changed it"
#   ... rewrite runs/$RUN/<id>/<file> ...
flowtrace step <id> done --asset <file> --run "$RUN"
flowtrace reply --run "$RUN" < reply.json
```

2. **Re-run the downstream, front to back.** Walk the `--downstream` list in the order it printed (it is topologically sorted) and re-run each one the same way — every step in it was computed from the old output and is now stale.

3. **Re-confirm the deliverable.** It is not in `--downstream` and carries no staleness signal, so once a steer changes the final output, close it again:

```bash
flowtrace deliverable done --asset <step_id>/<final-output> --run "$RUN"
```

The full state-machine rules live in `references/CLI.md` § "Re-running and steering".

## Precipitating a completed run

A source does not have to be prose written ahead of time. A task you (or an agent) just finished is also a source, often the best one, because the topology is given: you already walked the dependency edges, so you transcribe a graph instead of inferring one. The cycle above still applies, with three shifts:

- **Generalize by subtraction.** A finished run is fully concrete: one product, one set of outputs. The trace is that shape with the specifics removed. Strip every instance detail out of `trace.json` and the `STEP.md` bodies (no product names, no one-off values); the concrete outputs become the assets of run #1, not part of the method. (A step's `does` should read `condense the cleaned draft into a thread`, not `condense the Redis-to-NVMe post into a thread`.)
- **Re-point the faithfulness check.** Step 3 flips. The risk is no longer a flattened graph (the trace cannot flatten, it happened); it is *instance leak*: specifics bleeding into the skeleton. Re-read `trace.json` and each `STEP.md` asking "would this read the same for the next instance?"
- **Register, don't regenerate.** The assets already exist from the run you did. The lifecycle is recording them into `runs/<id>/<step_id>/`, not producing them again.

The run's concrete input becomes a file in `resources/`, pointed at by the root step's `reads:` (see step 5). If the run's steps each called a skill, name that skill in the step's `STEP.md`; the trace is the composition layer, and its nodes still call the moves.

## Rules that trip people

- **Asset path anchoring differs by command.** `flowtrace step --asset` is **step-relative** (resolved under `runs/<id>/<step_id>/`, so `--asset out.md`). `flowtrace deliverable --asset` is **run-relative** (`<step_id>/out.md`). An `evidence[].path` inside a reply is **run-relative** too. One file, three forms.
- **A reply needs at minimum `{ "headline": "...", "status": "..." }`.** Add `checkpoint.step_id` to bind it to a step; add `evidence[]` for figures, tables, checks, or citations. `flowtrace explain reply` and `flowtrace explain reply.evidence` list every field. The `--output example` skeleton is bare; build richer replies from `flowtrace explain reply` or `references/CLI.md` section 6.
- **Only declared assets are committed.** Scratch files in a step folder stay untracked. `STEP.md` files and your input files are not assets, so the run lifecycle never commits them. Commit them yourself if you want them in the history.
- **A terminal step that feeds the deliverable is not an orphan.** Older binaries may `lint` such a sink node as `orphan_step`; that is benign for a node whose asset is in the deliverable.

## The one thing this cannot hand you

A trace is the composition layer above individual moves, drawn as a visible, steerable DAG. The right topology for a given source is judgment, made in step 2; step 3 exists to check it. Everything else here is mechanical.
