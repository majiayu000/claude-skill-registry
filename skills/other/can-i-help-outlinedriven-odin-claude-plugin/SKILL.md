---
name: can-i-help
description: 'Use when the user asks "where to help", "contribution opportunities", or "find a good first issue". Returns data-backed first steps. Not for PR review queues: use gh-review-requests.'
---

# Can I help

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The user asks "where can I help", "what can I contribute", "find a good first issue", or "what should I work on". |
| Authority | Read-only. No file, VCS, credential, paid, published, deployed, or remote mutation. |
| Side effect | None; ranked recommendations only. |
| Done | Two to five evidenced recommendations with what, why, location, and first step, each based on a read source range and carrying a certainty label. |

## Inputs

- Target repository (optional): defaults to the current working directory. If the user supplies a path, use it.
- Developer interest (collected during execution, not supplied upfront): a single-select choice that routes signal ranking.

## Procedure

1. **Bound scope.** If the user already named an exact task or issue, stop: solve that task instead. If the request is pure project orientation with no contribution decision, produce orientation, not recommendations. If the repo cannot be read locally and no public issue tracker is available, report what is missing and stop. **Done when:** scope is bounded to contribution recommendations, or the request is redirected to the named task or orientation.

2. **Resolve target and collect base context.** Default target is the current repo unless the user supplied a path. Capture the project shape before ranking:
   - Manifests: `fd '^(package.json|pyproject.toml|Cargo.toml|go.mod|pom.xml|build.gradle|deno.json|bun.lockb|pnpm-lock.yaml|requirements.txt)$' <repo>`.
   - Top-level structure: `fd --max-depth 3 --type f <repo>`; exclude generated/vendor directories.
   - README / contributing docs: `fd '^(README|CONTRIBUTING|DEVELOPMENT|HACKING)(\..*)?$' <repo>` then read the relevant file ranges.
   - Test roots: `fd '(^test$|^tests$|__tests__|spec$|\.test\.|\.spec\.)' <repo>`.
   - Build/test commands: derive from manifest scripts, Makefile targets, CI config, or existing docs; mark certainty MEDIUM unless a command is explicitly declared. **Done when:** the project shape and active local modifications are recorded.

3. **Collect contribution signals with native recipes.** Prefer indexed codegraph when available; otherwise use `ast-grep`, `rg`, `fd`, and git history. Keep every signal as `{kind, file, line?, metric, confidence, evidence}`. Missing `kind`, `file` for file-backed work, or `evidence` downgrades the candidate to LOW. **Done when:** every collected signal has kind, file where applicable, evidence, and confidence.
   - Good-first areas: low blast radius, clear adjacent patterns, nearby tests, recent maintainer activity, low bug density. Fallback: count importers with `rg -n 'from .*/<module>|require\(.*/<module>|use .*<module>|import .*<module>'` and prefer files with few dependents plus visible neighboring tests.
   - Test gaps: hot source files with no co-changing test file. `git --no-pager log --since='180 days ago' --name-only --format='commit:%H' -- <src-paths>`; rank source files by touches, then subtract files whose commits include a matching `test|tests|spec|__tests__` path. HIGH when source churn ≥5 and zero matching test co-change; MEDIUM when no test root exists but naming conventions are unclear.
   - Doc drift: docs with zero or weak code coupling, stale inline identifiers, or examples importing paths that no longer exist. `git --no-pager log --since='365 days ago' --name-only --format='commit:%H' -- docs README* CONTRIBUTING*`; compute doc commits with no source files. Extract backticked identifiers/import paths from docs, check via codegraph search, else `rg -n '<identifier-or-path>' <repo>`. HIGH for broken import/path; MEDIUM for zero code coupling over the window.
   - Bugspots: files repeatedly touched by fix commits. `git --no-pager log --since='365 days ago' --regexp-ignore-case --grep='fix|bug|regression|crash|panic|race|leak|broken' --name-only --format='commit:%H' -- <repo>`; bug-fix rate = `fix_touches / max(total_touches, 1)`. HIGH when fix_touches ≥3 and rate ≥0.25; MEDIUM when only one threshold holds.
   - Open issues: `gh issue list --state open --limit 15 --json number,title,labels`. Route labels: `bug`/`regression`/`crash` → bugs; `good first issue`/`help wanted` → newcomer; `documentation`/`docs` → docs; `test`/`testing`/`coverage` → tests; `cleanup`/`refactor`/`chore` → cleanup only after repo verification. If `gh` fails, mark issue signal unavailable and continue.
   - Slop-deletion candidates: commented-out code, orphan exports, passthrough wrappers, and always-true/always-false conditions. Use AST where possible; never promise zero-behavior cleanup until the slop verification gate (step 8) passes.

4. **Ask the developer's interest, mandatory and first, before recommendations.** Present a single-select with exactly one Recommended option. Do this even if signals already look obvious. **Done when:** the developer selects one interest.
   Prompt: `What kind of contribution do you want to make?`
   Options:
   - `New to the stack`: Recommended when good-first areas or cleanup candidates exist.
   - `Experienced`: hard problems, bugspots, architecture-adjacent issues.
   - `Want to write tests`: test gaps and bugspot overlap.
   - `Want to fix bugs`: bug-labelled issues, bugspots, suspicious conditions.
   - `Want to improve docs`: stale references, doc drift, documentation issues.
   - `Want quick cleanup`: verified deletion-only or tightly-contained cleanup.

5. **Route interest to signals.** Lead with the strongest non-empty primary signal for the chosen interest; skip empty subsections with one sentence, not a filler apology. If the chosen interest has no supporting signal, name which signal was empty and pivot to the nearest adjacent interest with data. **Done when:** the selected interest is routed to its strongest available signal or an explicit data-backed pivot.
   - New to the stack → good-first areas (primary), verified cleanup / `good first issue` labels (secondary); prefer one-file tasks with examples nearby and low blast radius.
   - Experienced → bugspots, high-impact open issues, repeated-churn areas (primary); suspicious conditions, architectural labels (secondary); prefer bug-fix rate + open issue overlap.
   - Want to write tests → test gaps, test-gap ∩ bugspot (primary); `test`/`testing`/`coverage` labels, nearby test templates (secondary); sort by hotness + bug-fix rate.
   - Want to fix bugs → `bug`/`regression`/`crash` issues, bugspots (primary); always-true/false conditions, flaky-test labels, recent reverts (secondary); issue + bugspot overlap first.
   - Want to improve docs → stale inline symbols/import paths, zero-coupling docs (primary); `documentation` labels, README examples failing lookup (secondary); broken symbol/path beats coarse zero-coupling.
   - Want quick cleanup → verified commented-out code, verified orphan exports (primary); passthrough wrappers, redundant branches as bug investigation (secondary); pure deletion HIGH before contained refactor MEDIUM.

6. **Score and rank candidates.** Order candidates within the selected interest:
   `base = confidence(HIGH=3, MEDIUM=2, LOW=1); overlap_bonus = 2 if two primary signals match else 0; locality_bonus = 1 if one file and nearby examples exist else 0; issue_bonus = 1 if matching open issue label exists else 0; risk_penalty = 2 if exported/public/entrypoint, 1 if generated-looking, 3 if no file read yet; score = base + overlap_bonus + locality_bonus + issue_bonus - risk_penalty`.
   Suppress candidates with `score <= 1` unless every signal is weak; in that case disclose LOW certainty and ask whether to inspect deeper. Prioritize file-level evidence over directory-level evidence. Prefer overlap (test gap ∩ bugspot beats standalone test gap). Cap to 5 recommendations. Exclude generated, vendored, lockfile, snapshot, and build-output files. **Done when:** candidates are scored, ranked, filtered, and capped to five.

7. **Read before explaining.** For every candidate that survives ranking, read the target file range plus enough surrounding code to understand the local pattern. For docs, read the stale doc and the current code target. For tests, read one nearby existing test pattern. Structural claims without a read are Graft; exclude them. **Done when:** every surviving candidate has a read source range backing its explanation.

8. **Apply the slop cleanup gate when a recommendation is cleanup-shaped and claims "zero behavior change".** A recommendation that makes no such claim never routes through this gate. Before any zero-behavior wording:
   - Read the file and surrounding block.
   - Check references: codegraph callers/search when indexed; fallback `rg -n '<symbol>' <repo>` and language-specific `ast-grep` for import/export sites.
   - Check framework entry reachability: route files, plugin registries, CLI command tables, dynamic imports, reflection decorators, config exports, generated public APIs.
   - Classify: **Pure deletion HIGH**: commented-out code that re-parses as old code with no live marker, or orphan export with no references and no entry reachability. **Contained refactor MEDIUM**: passthrough wrapper with all call sites visible; first step is call-site inventory, not deletion. **Bug investigation MEDIUM**: always-true/false condition; likely wrong predicate, not cleanup.
   - If any entry-reachability doubt remains, phrase as "cleanup candidate" and make the first step verification, not removal. **Done when:** each zero-behavior cleanup claim is verified or downgraded to a candidate with verification first.

9. **Emit 2 to 5 recommendations.** Each uses the four-field shape so a contributor can act without re-reading the code:
   - What: exact file and line/range, function, issue number, or doc section. If issue-backed, include `#<number>` and still name the file once known.
   - Why: data-backed metric: bug-fix rate, test-gap touch count, zero doc coupling, broken symbol lookup, issue label, confidence score.
   - How: 2 to 3 sentences based on reading the file. Explain the local pattern, what would change, and why this is a bounded contribution. For tests, name the branch/case to cover. For docs, name the stale claim and the current code truth. For cleanup, state whether it is pure deletion, contained refactor, or bug investigation.
   - First step: exact command or action. Prefer `bat -P -p -n <file>`, `rg -n '<symbol>' <paths>`, `gh issue view <number>`, or a concrete edit after verification. If line numbers are unavailable, the First step must produce them.
   Do not include a recommendation that cannot fill all four fields. **Done when:** two to five recommendations fill all four fields and carry certainty labels.

10. **Offer the next depth step.** Close with: `Want me to walk you through one of these? I can read the target code, outline the exact diff, or draft the PR description.` **Done when:** the depth-step offer is delivered.

## Failure and recovery
- Not a git repo: history-backed signals (bugspots, test gaps, doc drift) are unavailable. Use file structure, tests/docs presence, and open issues if available. Do not fabricate git history.
- `gh` unavailable or unauthenticated: open issues signal unavailable. Continue with local bugspots, test gaps, doc drift, and cleanup signals.
- No manifests found: mark stack certainty LOW. Infer from extensions only after reading representative files.
- No test root found: do not claim absent tests globally. Treat test-gap confidence as MEDIUM until conventions are known.
- Churn history too shallow: avoid bug-fix-rate percentages. Use current issue labels and code reads.
- Developer picks interest with no signal: name the empty signal explicitly. Pivot to the nearest adjacent interest with non-empty evidence.
- **Cleanup candidate touches public/exported surface**: downgrade safety claim. Make caller/reachability verification the First step.
- Only LOW-certainty candidates exist: present at most two with LOW label. Ask whether to inspect deeper before editing.
- No contribution opportunities survive: report that no safe, data-backed recommendation was found. Offer to broaden scope to issues, docs, or tests after more context.
- Partial results: return whatever non-empty signals survived with their certainty labels. Never present LOW as fact or suppress a failed signal silently.
- Non-mutation: this skill performs no file, VCS, or remote mutation. No rollback is needed; the only recovery is to report what is missing and continue with available signals.

## Output
A ranked list of 2 to 5 recommendations, each in the four-field shape (What / Why / How / First step), preceded by the developer's chosen interest and the signals that routed to it. Each recommendation carries a certainty label (HIGH, MEDIUM, or LOW). The list closes with an offer to walk through one recommendation in depth. If no safe recommendation survives, a terminal report stating that no data-backed contribution opportunity was found, naming the signals checked and the reason each was empty.
