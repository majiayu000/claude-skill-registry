---
name: ux-grill
description: Use when a running web app's UX has to be audited reproducibly rather than by feel — a deterministic mechanical pass over routes and viewports (axe, target size, horizontal overflow, page title, scripted journeys) followed by a screenshot-grounded interrogation of the operator, journey by journey, with two persona lenses from the target repo's manifest. Triggered by "grill the UX", "roast the dashboard", "UX-Audit", "/ux-grill". Bootstraps its own manifest from a loopback URL on the first run, so it never requires a hand-written file to start.
model: inherit
color: magenta
tools: Read, Grep, Glob, Bash, Write
---

# UX-Grill Skill

> Two stages, hard boundary. **Stufe 1** measures — a Node pass over routes × viewports that calls `agent-browser` and writes JSON, with no model in the loop. **Stufe 2** grills — the `/grill` loop applied to journeys, where every claim carries a screenshot path. Severity is never a judgment here; it comes out of `schema.mjs`.

## Soul Reference

Read `soul.md` in this skill directory before anything else. It defines WHO you are — the UX Interrogator — the persona-lens discipline, and the six tactics in their UX form. The rubric you measure against is `rubric-v2.md`; read it before Phase 1 so you can read `findings.jsonl` without guessing what a `checkId` means.

## When to use

- A web app is running on loopback and the operator wants its UX improved systematically, not by single impressions
- The same audit has to be re-runnable later, so that "did this get better?" is answerable by fingerprint diff rather than memory
- Mobile and desktop need judging against the SAME journeys, with the viewport verified rather than assumed
- Journeys exist (or can be written) as executable `agent-browser` command lines

## When NOT to use

- A CI-shaped end-to-end run over an existing test profile → `/test` (driver + `agents/ux-evaluator.md`). `ux-evaluator` is deliberately NOT reused here: Stufe 1 is LLM-free by construction.
- A plan, PRD or design needs stress-testing before it is built → `/grill`. There is no running app to measure yet.
- Per-wave design drift against the design source → `design-reviewer` (SO#1300 B4). That checks whether the built thing matches the design; `/ux-grill` checks whether a person gets through the journey.
- A native macOS app → out of scope in v2; web only.
- A non-loopback target → refused, not degraded. Both `loadManifest()` and `collect()` assert it.

## Phase 0: Target + Stufe 1

### 0.1 Resolve the argument

Per `commands/ux-grill.md` § Argument Validation: a loopback URL selects the bootstrap path, a file path or empty selects `DEFAULT_MANIFEST_PATH` from `scripts/lib/ux-grill/manifest.mjs`.

### 0.2 Bootstrap (URL, no manifest yet)

This path exists because the predecessor skill died of its absence: a tool that presupposes a hand-written manifest is never started.

1. **Ask ONCE, up to three questions in a single `AskUserQuestion` call** — the env FILE name and the two login env NAMES. Never a value; the manifest and everything downstream carry names only.

```
AskUserQuestion({
  questions: [
    { question: "Which env file of the target repo holds the login credentials?",
      header: "Env-Datei",
      options: [
        { label: ".env.local (Recommended)", description: "The usual dev file. Cost: none — only the NAME is stored; values stay in the gitignored file." },
        { label: ".env.e2e.local", description: "A separate e2e file, where one exists. Same storage contract." },
        { label: "Ohne Login", description: "No credentials at all — personas stay empty and only the unauthenticated navigation is crawled. Cost: journeys behind the login are invisible." },
        { label: "Other / describe below", description: "Name a different file." } ],
      multiSelect: false },
    { question: "Which env variable holds the login e-mail?",
      header: "Mail-Env",
      options: [
        { label: "TEST_USER_EMAIL (Recommended)", description: "The most common name in the env file you picked. Cost: none — the NAME is stored, the value never is." },
        { label: "LOGIN_EMAIL", description: "Use when the target repo names it that way." },
        { label: "Other / describe below", description: "Name the variable yourself; read it from the env file first." } ],
      multiSelect: false },
    { question: "Which env variable holds the password?",
      header: "Pass-Env",
      options: [
        { label: "TEST_USER_PASSWORD (Recommended)", description: "Pairs with the e-mail name above. Same storage contract: only the NAME reaches the manifest." },
        { label: "LOGIN_PASSWORD", description: "Use when the target repo names it that way." },
        { label: "Other / describe below", description: "Name the variable yourself." } ],
      multiSelect: false }
  ]
})
```

2. **Crawl.** Open an `agent-browser` session of your own (`session id --scope worktree --prefix uxgrill` — never the shared default daemon), log in with the named credentials when they were given, `snapshot`, and collect the links inside the `navigation` landmark plus the visible links on the landing screen. Each discovered route becomes `{path, title}`.
3. **Write.** `buildBootstrapManifest({baseUrl, build, envFile, loginEnvEmail, loginEnvPassword, routes})` → `writeBootstrapManifest({repoRoot, text})`. `journeys[]` is always empty; personas carry exactly one entry, or none under "ohne Login". The writer REFUSES to overwrite (`ManifestError` code `manifest-exists`) — that is a correct refusal, not a failure to work around.
4. **END the run with a hint, not an error.** Name the file written and the three things only a person can supply: `journeys[]` (name, persona, start, `steps[]` as `agent-browser` command lines, `success`, `max-steps`), `guarded-url-envs` (the env NAMES whose values must be loopback), and each persona's `goal`. Then stop. The first run's product is the manifest.

### 0.3 Load (manifest exists)

`loadManifest({repoRoot, manifestPath})` returns `{frontmatter, body, envMap, manifestHash, path}`. Two `ManifestError` codes are exit-2 refusals and must be reported verbatim, with no retry and no fallback:

| code | message to print | exit |
|---|---|---|
| `base-url-not-loopback` | `base-url must be loopback` | 2 |
| `guarded-env-not-loopback` | `guarded env <NAME> must be loopback` | 2 |

Both name a variable and never its value. A guarded env pointing at production is exactly the case where echoing the value would leak a live endpoint into a run record.

### 0.4 Stufe 1 — one Bash call, coordinator-direct

Hash `rubric-v2.md` first (`rubric_hash` is the comparability key, and `collect()` requires `rubricHash` as a caller-supplied argument — it does not hash the file itself). Then run the mechanical pass as **exactly one** Bash invocation from the coordinator thread: a short ESM runner written to `.orchestrator/tmp/` that imports `loadManifest` from `scripts/lib/ux-grill/manifest.mjs` and `collect` from `scripts/lib/ux-grill/collect.mjs`, calls `collect({repoRoot, manifest, envMap, rubricHash})`, and prints the returned `{runId, runDir, findings, runRecord, skipped}` as JSON on stdout.

Three properties of this step are load-bearing:

- **No dispatched agent runs Stufe 1.** It is deterministic and LLM-free; an agent would add cost, non-determinism and a transcript for nothing.
- **Working files live in `.orchestrator/tmp/`**, never `/tmp` (does not survive a resume) and never an untracked path that the owner-leakage gate would scan.
- **A `CollectError` is a stop, not a warning.** `base-url-unreachable` means the app is not running; every later measurement would be meaningless.

Then compare and reconcile, in the same runner. Call `compareRuns` from `scripts/lib/ux-grill/compare.mjs` — it uses `findPreviousRun` and `readFindings` from `scripts/lib/ux-grill/run-record.mjs` to locate the last run with the same `manifest_hash`, delegates the set arithmetic to `compareFingerprints`, and classifies each fingerprint as `new | persisting | fixed` (runs whose `rubric_hash` differs are non-comparable — everything reads `new`). Write the counts back with `updateRunRecordCompare` from `scripts/lib/ux-grill/run-record.mjs`; the record `appendRunRecord` wrote during Stufe 1 carries the schema defaults until you do. Then call `reconcileFindings` from `scripts/lib/ux-grill/reconcile.mjs`, which wraps `triageDecision` / `createFinding` / `updateFinding` from `scripts/lib/test-runner/issue-reconcile.mjs` and builds each issue's text with `buildIssueTitle` / `buildIssueBody`. When `pencil.file` is set, the optional coverage step is `scripts/lib/ux-grill/pencil-coverage.mjs`; unreachable Pen.app is a `pencil-unavailable` skip, never an error.

### 0.5 Read the artefacts — and only them

Read `findingsPath(repoRoot, runId)` (`findings.jsonl`), the run record appended to `UX_GRILL_LEDGER`, and the `skipped[]` array. Screenshots sit under `runDirPath(repoRoot, runId)`; findings reference them relatively.

**Stufe 2 reads the manifest and the Stufe-1 artefacts, never the product specification.** The judge sees the artefact, not the intent — a screen that only makes sense once you have read the PRD has already failed the user who has not.

## Phase 1: Journey Map

For each journey in the manifest, lay out its steps from the step screenshots as four lines — **understand** (what does the screen say is possible), **decide** (can the right action be chosen), **act** (can it be performed without a wrong click), **recover** (what happens after a wrong turn). One line each; the screenshot path belongs on the line it describes.

Then table the mechanical findings PER ROUTE. They are context for the journey map, never questions:

| checkId | severity | locator | screenshot |
|---|---|---|---|
| `target-size-floor` | high | `/dashboard\|mobile\|button:nth-of-type(3)` | `screenshots/dashboard-mobile-full.png` <!-- path-check: example --> |

A mechanical finding is NEVER raised as an `AskUserQuestion`. It was measured; there is nothing for the operator to decide about its existence, and an AUQ that decides nothing is an interrupt spent on nothing (AUQ-001, AUQ-005).

## Phase 2: The Grill Loop

Walk the journeys one at a time. A **journey finding** is one of exactly four things:

1. a `journey-failed` or `journey-step-count` finding from Stufe 1,
2. a contradiction between two screens of one journey (an empty state that says "nothing here" beside a banner that says "create your first invoice"),
3. a persona-lens observation — `skills/persona-panel/presets/designer-lens.md` § Evaluation Criteria, narrowed by the manifest persona's `goal`,
4. a catalogue item from `rubric-v2.md` § Stufe 2 that a screenshot actually shows.

Per finding, **exactly one** `AskUserQuestion` call:

```
AskUserQuestion({
  questions: [{
    question: "The onboarding AVV step reports success but writes nothing — 6 steps, no persisted state. Is the step required?",
    header: "AVV-Schritt",
    options: [
      { label: "Fix the silent failure (Recommended)", description: "screenshots/onboarding-avv-step-4.png shows the success toast on an unsaved form. Cost: one backend write path; blocks the journey until it lands." },
      { label: "Remove the step", description: "Drops the AVV from onboarding entirely. Cost: the legal requirement moves elsewhere and needs its own home." },
      { label: "Leave, file as known", description: "Cost: the next user hits the same dead end; the finding persists in the next run." },
      { label: "Other / describe below", description: "Resolve it a different way — describe how." }
    ],
    multiSelect: false
  }]
})
```

**Rules, every question:** option 1 is `(Recommended)` with its cost named; the screenshot path stands IN the description, so the operator can judge without opening the run directory (AUQ-002); the persona lens is named when the finding comes from one; `header` stays at 12 codepoints where the language allows; `Other / describe below` is always present.

**Subagents ask nothing.** `AskUserQuestion` does not exist inside a dispatched agent (AUQ-004). The whole grill loop is coordinator-side, which is also why Stufe 1 — the part that COULD be dispatched — deliberately needs no judgment.

**Budget.** Read `efficiency.output-level` from `owner.yaml` and apply the matching block in `soul.md` § Output Levels. The AUQ budget is separate and harder: at most one question per journey finding, and mechanical findings never become questions at all. **Stop** when every journey is walked, when the operator says it is enough, or when the remaining findings need a product decision no screenshot can inform — the last case goes to Phase 3 as an open question, not to a fifth AUQ.

## Phase 3: Recap

Plain text, in this order:

- **Resolved decisions** — each journey finding and how the operator settled it.
- **Contradictions surfaced** — the primary output. Two screens of ONE journey that cannot both be true, with BOTH screenshot paths. If none: say so plainly; a run that surfaces none either had a coherent product or was not grilling hard enough.
- **Open questions** — genuine unknowns; no confident guess in their place.
- **Mechanical summary** — counts by severity from `countBySeverity()`, the provisional count (`target-size-*` on a `build: dev` manifest), the `new | persisting | fixed` split, and **every** entry of `skipped[]` with its reason. All four `SKIP_REASONS` are shown, never folded away — `device-mismatch`, `measure-failed`, `route-unreachable`, `pencil-unavailable`. A skipped mobile viewport reported as a clean one is the exact failure the verification exists to prevent, and a check that never ran reads as `fixed` in the next compare.

## Phase 4: Hand-off

```
AskUserQuestion({
  questions: [{
    question: "UX-Grill complete. Where should the result land?",
    header: "Hand-off",
    options: [
      { label: "Dossier in the target repo (Recommended)", description: "Writes docs/audits/YYYY-MM-DD-ux-grill.md beside the code it describes. Cost: one file, committed with the repo." },
      { label: "Dossier in the vault", description: "For a PUBLIC target repo — findings naming routes and personas stay out of the public tree. Cost: further from the code." },
      { label: "Issues only", description: "No prose file; high findings filed, medium/low batched. Cost: the contradictions live only in the issue bodies." },
      { label: "Done — nothing written", description: "The interrogation itself was the value. Cost: the run artefacts remain, the judgments do not." }
    ],
    multiSelect: false
  }]
})
```

The dossier path is `docs/audits/YYYY-MM-DD-ux-grill.md` <!-- path-check: example --> in the TARGET repo. When that repo is public, take the vault option instead — route names, persona goals and a live dev endpoint are not public artefacts.

**Issue creation runs through `reconcileFindings` in `reconcile.mjs` only, never `glab` or `gh` directly** — the fingerprint dedupe lives there, and a hand-filed issue is a duplicate the next run cannot recognise. Severity routing is adopted verbatim from `skills/test-runner/SKILL.md` § Severity Routing and § Batched AUQ Triage; read it there rather than expecting a second copy here. Three deltas apply:

1. Stufe 1 never emits `critical` — no measured ux-grill violation is release-blocking on its own — so the auto-create lane is `high` alone.
2. `medium` and `low` go into ONE batched AUQ for the whole run, not one per route.
3. The cap is Session Config `issue-budget:` (`max-per-session`, `mode`, `overflow`). When the budget is reached, stop filing and report the remainder in the dossier — do not spend the overflow on `low` findings.

A `provisional: true` finding is never auto-filed. Reproduce it against a `build: prod` manifest first, or carry it in the dossier as provisional.

## Secrets

The manifest carries env NAMES; values live in the target repo's gitignored env file and go nowhere else. `resolvePersonaCredentials()` in `scripts/lib/ux-grill/manifest.mjs` states the contract in its own JSDoc warning: the object it returns carries SECRET VALUES and must never be serialised into a run record, a findings file, a dossier, an issue body or a log line — it is handed to the browser login step and dropped. The same holds for everything you author in Phase 3 and Phase 4: a dossier, an AUQ description and an issue body may say `LOGIN_PASSWORD`, never what it is set to. The acceptance test is a grep of the run directory for the password value returning zero hits.

## Anti-Patterns

- **Raising a mechanical finding as an AUQ** — it was measured; asking about it spends an interrupt on a settled fact
- **Judging severity** — severity comes from `SEVERITY_BY_CHECK` / `severityForAxeImpact` in `schema.mjs`; a model verdict on impact was measured at 56% consistency and has no place here
- **Reading the product spec before judging** — Stufe 2 sees the artefact, never the intent; the spec would tell you what the screen MEANT to say
- **Hiding a skip** — a `device-mismatch` viewport reported as clean turns a broken measurement into a passing grade
- **Filing issues directly with `glab`** — bypasses the fingerprint dedupe, so the next run files the same finding again
- **Auto-filing a `provisional` finding** — a dev build is not a geometry measurement basis
- **Using the shared `agent-browser` daemon** — two sessions then contaminate each other's captures; always `session id --scope worktree --prefix uxgrill`
- **Dispatching an agent for Stufe 1** — it is deterministic; an agent adds cost and non-determinism and removes nothing

## See Also

- `skills/ux-grill/rubric-v2.md` — checks, severity table, fingerprint contract, skip reasons
- `skills/grill/SKILL.md` — the phase skeleton and AUQ discipline this mirrors
- `skills/test-runner/SKILL.md` — severity routing and batched AUQ triage, adopted not duplicated
- `skills/persona-panel/presets/designer-lens.md` — the persona lens, narrowed by the manifest's `personas[].goal`
- `templates/_shared/ux-manifest.template.md` — the manifest a target repo commits
- `.claude/rules/ask-via-tool.md` — AUQ-001..006, the budget this skill spends carefully
- `.claude/rules/security.md` — env-name-only discipline for credentials
