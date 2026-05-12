# Debugging

Read this when a run failed, stalled, or produced unexpected output. The bulk of agent debugging in Deepline reduces to four classes of failure; each has a specific signal and a specific fix.

## First commands when a run goes sideways

```bash
deepline plays runs <play-name> --json      # which runs exist; which failed
deepline plays status <run-id> --json       # detailed state and last event
deepline plays tail <run-id> --json         # stream the play's log output
```

A failed run shows up in `status` as `failed` with a final-event message. `tail` shows the `ctx.log(...)` output up to the failure. For a play that never completes, `tail` reveals whether it is stuck on a tool call (provider hang), a retry loop (rate limit), or genuinely waiting.

## Failure: replay-safety violation

Symptom: the run fails at registration or mid-execution with an error mentioning replay, determinism, or non-deterministic operation.

Cause: the play body uses an effect that does not go through `ctx.*`. The most common culprits:

- `Date.now()`, `new Date()`, `Math.random()`, `crypto.randomUUID()` called outside a `ctx.step`.
- `fs.readFile` / `fs.writeFile`.
- Bare `fetch(url)` instead of `ctx.fetch(url)`.
- `process.env.X` reads inside the play body.
- A top-level side effect at module load (e.g. opening a file, instantiating a global client).

Fix: route the operation through the appropriate `ctx.*` method. For arbitrary operations with no dedicated method, wrap in `ctx.step('stable-id', () => operation())`. See `shared/play-anatomy.md` for the full list of safe surfaces.

## Failure: set-live mismatch

Symptom: `deepline plays run <name>` produces output that does not match the local `*.play.ts` file. Or `set-live` rejects with a "local differs from stored source" error.

Cause: the live registered version of the play is older than the local file. The runtime ran the registered version, not the local one.

Fix: pick one path:

```bash
# Option A: re-publish the local file as the new live version.
deepline plays set-live <file.play.ts> --json

# Option B: run the file directly without going through the registry.
deepline plays run <file.play.ts> --input '...' --watch
```

Use option B for iteration. Use option A when the file is stable and you want other plays / agents calling it by name to get the new version.

## Failure: locked output / concurrent run

Symptom: a play fails immediately with a lock-file error or "another run is in progress" message.

Cause: a previous run is still active (or its lock did not clean up). Deepline serializes by output destination to prevent two runs from writing to the same target concurrently.

Fix: check for the prior run, and either wait or cancel.

```bash
deepline plays runs <play-name> --json | jq '.[] | select(.status == "running")'
deepline plays stop <run-id> --reason "stale lock"
```

Lock files in the working directory (typically a `.deepline.lock` directory next to the output) are safety mechanisms, not bugs. If no run is actually active and the lock is genuinely stale, the lock can be removed manually — but verify the run is finished first.

## Failure: input shape rejected

Symptom: the run fails with a schema or input validation error, or an empty result set when the same payload worked yesterday.

Cause: tool / play input contract changed, or the agent guessed at field names without confirming.

Fix: re-confirm the contract.

```bash
deepline plays describe <play-name> --json
deepline tools describe <tool-id> --json
```

Compare the actual input contract to the payload being sent. The most common form of this failure: a previously-named field was renamed, or an enum value moved (e.g. `c_level` became `C-Level`). The CLI's `describe` is authoritative.

## Failure: provider returns nothing

Symptom: every row's column is `null`. The play succeeded but the data is missing.

Cause: usually one of three:

1. Wrong filter shape (e.g. `"United States"` where the provider wants `"USA"`). Run a count probe with the same filter before the full pull (see `jobs/finding-companies-and-contacts.md` rules on enum validation and ISO codes).
2. Wrong provider for the data class (e.g. work-email provider for personal-email request — see `jobs/enriching-and-researching.md`).
3. Sales Navigator URL fed into an email waterfall — every provider rejects `/sales/lead/` URLs.

Fix: pilot with `--rows 0:1` and inspect the raw response. If the provider returned nothing for row 1, the filter is wrong; if it returned data and the play column is null, the extraction is wrong.

## Failure: `ctx.csv` or `ctx.map` errors

Symptom: errors like "csv input not staged" or "duplicate map key" or "cannot read .length of dataset."

Cause:

- "csv input not staged": the play was invoked with `--input` instead of `--csv`, but the play calls `ctx.csv(input.file)`. Either run with `--csv`, or change the play to accept a different input shape.
- "duplicate map key": two `ctx.map` calls in the same play used the same key. Pick distinct names per stage.
- "cannot read .length of dataset": the code is treating the `PlayDataset` returned by `ctx.csv` or `ctx.map` as an array. Pass the dataset directly to `ctx.map`; do not call `.length` or iterate manually.

Fix: confirm the intended input shape (`--csv` vs `--input`), the stage keys, and the dataset handling pattern. See `shared/play-anatomy.md` for the contract.

## When `tail` shows the play is stuck

Symptom: `tail` stops emitting log lines, but `status` shows the run as still active.

Cause: the play is waiting on something. Common waits:

- A provider call that is taking longer than expected (some structured providers are slow under load — Apify actors, large company searches).
- A `ctx.sleep(...)` that is intentionally long.
- A rate limit backoff (the runtime retries quietly).

Fix: check whether the wait is intentional (read the play source for the current step). For long-running provider calls, the right move is usually to wait — the runtime handles retries and timeouts. For genuinely stuck runs (no progress in 10+ minutes for a synchronous tool that should be fast), `stop` and rerun.

```bash
deepline plays stop <run-id> --reason "stuck on provider call" --json
```

## When everything looks right and it still fails

Run the eval-style verification:

```bash
deepline plays run <play-name> --input '<known-good-payload>' --watch
```

If the same payload that worked yesterday now fails, check:

1. `deepline auth status --json` — auth may have expired or be pointing at a different host.
2. `deepline health` — the runtime may be unreachable.
3. The tool's `describe` output — the input contract may have changed.
4. The play's set-live version — a teammate may have published a breaking change.

The four discovery commands plus `auth status` and `health` answer 80% of "why did this stop working" questions before you read any code.

## Useful one-liners

```bash
# Latest failed run for a play
deepline plays runs <name> --json | jq '.[] | select(.status == "failed") | .id' | head -1

# Tail the most recent run
deepline plays runs <name> --json | jq -r '.[0].id' | xargs -I {} deepline plays tail {} --json

# Find runs older than a day that are still active (likely stuck)
deepline plays runs <name> --json | jq '.[] | select(.status == "running" and (.started_at | fromdate) < (now - 86400))'
```
