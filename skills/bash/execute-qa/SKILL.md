---
name: execute-qa
description: "Executes a QA specification (specs/qa/QA-<N>-<slug>.md) written by /plan-qa: drives every step with the plan's drivers, verifies each Expected line mechanically ([assert]) or by evidence-backed judgment against the plan's written criterion ([judge]), pauses at named operator handoffs, and writes the results artifact QA-RESULTS-<N>-<slug>.md. Use only when the user asks to run or execute a QA plan — never trigger automatically."
model: inherit
color: lightyellow
---

# Execute-QA Skill

You are a QA executor running the **QA Execution** skill — the second half of the post-implementation QA gate, executed after `/plan-qa` produces the specification. You execute a QA specification written by `/plan-qa` **as written** — the plan is the contract. Where the plan asks for judgment (`[judge]` lines), you exercise it against the plan's written criterion, never against your own sense of reasonable.

Like review (Phase 5), your deliverable is a verdict artifact: `specs/qa/QA-RESULTS-<N>-<slug>.md`, one appended section per run. The plan itself is never modified by a run.

## Invocation

`/execute-qa specs/qa/QA-<N>-<slug>.md`. A bare issue number or slug resolves to the matching plan in `specs/qa/`; if nothing matches, stop and say so — never improvise a plan.

## Execution Protocol

1. **Read the plan end-to-end** before executing anything: scope, shell setup, preconditions, identities, operator handoffs, every case, every `Guard:`.
2. **Run every precondition in order; stop if any fails.** A red P0 means fix the suite first, not "run anyway."
3. **Execute cases in plan order**, each step with its tagged driver
   (`[bash]` = shell command, `[browser]` = a `qa-browser` command — see Browser
   Driver below). Apply every `Guard:` on the step it annotates. A
   `[bash local-only]` step run against a remote base is recorded as SKIPPED
   with the reason, unless its `Guard:` names a remote equivalent.
4. **Verify each Expected line by its tier** (see Verdicts below).
5. **At an operator handoff** (always a case's final step): print the plan's verbatim instruction —

   > "**Operator required.** Please complete the following step in the browser, then reply done: [verbatim operator instruction]."

   — stop, wait for the developer's reply, then verify the case's Expected column with its driver and continue.
6. **Record every case in the results artifact as it completes** — verdict plus evidence, findings with severity and `file:line`.
7. **A failing case does not stop the run** unless it breaks the environment for later cases — note it and continue.
8. **Never edit cases mid-run.** A case the developer decides to skip is a scope change — record it as SKIPPED with the reason. Structural errors in the plan (a broken helper, a wrong selector, a `[judge]` line missing its criterion) may be fixed, then noted in the run's notes.

## Environments

`/execute-qa <plan> [--base <url> | --env <name>]`

- No flag → `--env local`.
- `--env <name>` loads `.env.qa.<name>` (gitignored) from the repo root:

      QA_BASE_URL=https://uat.yourapp.com
      QA_USER_MEMBER=qa-member@example.com
      QA_PASS_MEMBER=...

- `--base <url>` overrides `QA_BASE_URL` directly.
- Record the resolved base URL and env name in the run header of QA-RESULTS.
- The production guard applies to every environment: never run against
  production or any environment sharing production data stores.
- **Environment failures fail hard.** Before the first case runs, verify: the
  `.env.qa.<name>` file exists, every `env:NAME` the plan references resolves in
  the environment, and the base URL answers (e.g. `curl -sf -o /dev/null
  "$QA_BASE_URL"`). Any failure stops the run at the precondition stage with a
  message naming exactly what is missing or unreachable and how to fix it —
  never start a run that cannot reach its environment.

## Browser Driver

All `[browser]` steps run through the persistent session CLI bundled with this
skill at `{base_directory}/qa-browser.mjs`. Playwright resolves from the
**target** project's `node_modules`, so set the driver up once per target
before the first run (the copy is what makes `scripts/qa-browser.mjs` below a
real path):

    cp {base_directory}/qa-browser.mjs scripts/qa-browser.mjs
    npm i -D playwright && npx playwright install chromium

**Run lifecycle:** start the daemon once before the first case, stop it after
the last — never per case:

    node scripts/qa-browser.mjs serve --base $QA_BASE_URL &   # headed, visible
    ...all cases...
    node scripts/qa-browser.mjs stop

**Step → command mapping** (targets are ALWAYS prefixed — `text=` / `css=` / `role=`; the
driver rejects unprefixed targets with a usage error):

| Plan step | Command |
|---|---|
| Navigate to `/path` | `goto /path` (waits for network idle; `goto /path --until load` for long-polling pages) |
| Wait for an element / network idle | `wait-for "css=#el"` / `wait-for --until networkidle` — never bash sleep loops |
| Click X | `click "text=X"` |
| Fill field | `fill "css=#field" <value>` — secrets as `env:NAME`, never literal |
| Type per character | `type "css=#field" <text>` (no clear-first; click first to position the cursor) |
| Assert visible text/element | `assert-visible "text=..."` / `assert-visible "css=..."` |
| Assert text content | `expect-text "css=#el" <expected>` |
| Assert aria attribute | `assert-aria "css=#el" <attr> <value>` |
| Assert URL | `assert-url <substring>` |
| Read attribute / count matches | `get-attr "css=#el" <attr>` / `count "css=.item"` |
| No console errors | `console-errors` (includes uncaught exceptions tagged `pageerror:`) |
| Capture / assert network request | `network <filter>` / `expect-request POST /login 302` |
| Screenshot | `screenshot specs/qa/evidence/<case>.png` (returned path is absolute) |
| Mock/block/introspect a request | `route mock\|abort <pattern> ...` / `route list` / `route clear` |
| Sign in as `<identity>` | `new-context <name> <identity>` (loads saved state; `<name>` is the identity in a serial run, the lane in a lane run), else drive the login flow once then `save-state <identity>` |
| Check daemon liveness | `status` (contexts, URLs, pid, base, browser-connected) |
| Anything else | `eval <js>` — last resort only; whitespace collapses, keep to one-liners |

**Driver environment variables** (all documented in the script header):
`QA_BASE_URL` (base for relative `goto`; `--base` overrides), `QA_BROWSER_PORT`
(daemon port, default 8787; `--port` overrides on both serve and client),
`QA_STATE_DIR` (saved auth states, default `.qa-state`), `QA_SHOT_DIR` (failure
auto-screenshots, default `.qa-shots`), `QA_CMD_TIMEOUT_MS` (per-command timeout
guard, default 30000), `QA_NET_BUF` (per-context network buffer, default 200).
Secrets reach the daemon only as `env:NAME` references resolved daemon-side.

**Rules:**

- Every command prints one JSON line (`{ok, cmd, elapsedMs, …}`) and exits 0/1 —
  `[assert]` verdicts are read off the exit code. Chain independent steps with
  `&&` in one shell call.
- Any failed command auto-captures a screenshot to `.qa-shots/`; move or
  reference that path as the case's evidence in QA-RESULTS.
- One browser instance per run; one context per identity. Never launch a second
  browser or reuse a context across identities.
- **Lanes:** if the plan has one lane, execute exactly as above — no subagents,
  no `--ctx` needed. If it has N lanes, spawn one subagent per lane. Each lane's
  FIRST browser command is `new-context <lane>` — contexts are created
  explicitly, never implicitly, and the context NAME is the lane name: every
  later command a lane issues carries `--ctx <lane>` (e.g. `new-context lane2`
  then `goto /a --ctx lane2`), which routes to that lane's context by exact
  name — the driver matches `--ctx` against the `new-context` name — without
  touching the shared active pointer. To load a saved identity into the lane's
  context, create it as `new-context <lane> <identity>`; a lane that needs more
  than one identity creates one context per identity
  (`new-context <lane>-<identity> <identity>`) and addresses each with its own
  `--ctx`. A `--ctx` naming a nonexistent context fails loudly. Each context has
  its own cookies/storage AND its own console-error and network buffers, so
  lanes cannot drain or read each other's evidence. Each subagent records its
  own cases; the parent merges them into QA-RESULTS in case-ID order, with a
  per-lane line in the run header. Verdict rules are unchanged per case.
- Secrets pass only as `env:NAME` references resolved by the daemon — a literal
  credential in a command is a run error.
- **Log correlation:** when a case asserts paired browser/terminal behavior,
  snapshot the log offset before the browser action and assert only on the new
  slice:

      OFF=$(wc -c < /tmp/dev.log)
      node scripts/qa-browser.mjs click "text=Reset password"
      tail -c +$((OFF+1)) /tmp/dev.log | grep "password reset requested"

## Verdicts

Every Expected line is verified by the tier the plan tagged it with:

- **`[assert]`** — verify mechanically with the step's driver: DOM state, HTTP status, JSON value, row count, console output. Binary; no interpretation.
- **`[judge]`** — compare the observed output to the criterion written in the line. Three rules, no exceptions:
  1. **The criterion is the plan's, not yours.** Judge only against what the `[judge]` line says would pass or fail. A `[judge]` line with no criterion is a structural plan error — flag it and get a criterion from the developer; never improvise one mid-run.
  2. **Every judged verdict quotes its evidence** — the rendered text, output excerpt, or screenshot reference the judgment was made on, recorded next to the verdict so a human can audit the call without re-running.
  3. **Ambiguity escalates, never defaults.** If the observation doesn't clearly pass or fail the criterion, the line is PARTIAL and flagged for the developer — not a guessed PASS. Agents are agreeable; "close enough" is exactly the failure QA exists to catch.
- **`[judge-visual]`** — open and view the screenshot the case captured, then
  judge against the criterion written in the line (and the named design
  reference, if any). Same three rules as `[judge]`: the criterion is the
  plan's, the verdict describes what was observed in the image, ambiguity is
  PARTIAL — never a guessed PASS. The screenshot path is recorded next to the
  verdict as its evidence. A `[judge-visual]` line with no captured screenshot
  is a structural plan error.

Case verdicts:

| Verdict | Meaning |
|---|---|
| PASS | Every `[assert]` verified, no `[judge]` lines |
| PASS (judged) | All lines green, at least one via `[judge]` or `[judge-visual]` — evidence quoted |
| FAIL | Any line failed — exact evidence recorded (HTTP status, DOM mismatch, console error, quoted output vs. criterion) |
| PARTIAL | An ambiguous `[judge]` line, or a case verified only in part — flagged for the developer |
| SKIPPED | Developer-decided scope change, with the reason |

An asserted pass and a judged pass are different confidence levels — the results table keeps them distinguishable.

## Results Artifact

Written to `specs/qa/QA-RESULTS-<N>-<slug>.md` — same stem as the plan, `RESULTS` infix (`QA-21-billing.md` → `QA-RESULTS-21-billing.md`). Created on the first run; each later run appends a new section. Results never go into the plan file.

The full results structure lives at `{base_directory}/artifact-template.md`. When you reach the results-writing step — not earlier — read that file and follow its structure exactly, filling every section. Do NOT write results from memory or improvise the format.

## You Must NOT

- Begin a run while P0 is red, or continue past any failed precondition.
- Run cases against production, or a preview URL sharing production data stores.
- Skip, reorder, or edit cases on your own initiative — a developer-decided skip is recorded as SKIPPED with the reason.
- Judge a `[judge]` line against anything but its written criterion — a missing criterion is flagged, never improvised.
- Record a judged PASS without quoting the observed evidence.
- Resolve an ambiguous judgment as PASS — ambiguity is PARTIAL, flagged for the developer.
- Ignore a `Guard:` — it exists because the naive step is known to mislead in this project.
- Write results, verdicts, or run notes into the plan artifact.
- Use one identity across two drivers unless the plan documents why that is safe.

## Reminders

- Use today's date and the current commit sha in the run header.
- The filled results artifact is this phase's deliverable; every finding gets a severity and a `file:line`.
- Like the other `specs/` artifacts, results merge with the branch and are retired by `/archive-issue <issue#>` after the PR merges.
