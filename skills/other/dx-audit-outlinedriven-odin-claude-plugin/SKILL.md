---
name: dx-audit
description: 'Use when auditing the developer-facing surface of a CLI, SDK, library, or package: API contracts, errors, public types, onboarding, and config.'
---

# DX audit

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Audit my CLI, make this CLI agent-friendly, is this API ergonomic, SDK review, library DX, developer onboarding |
| Authority | Read-only. No file, VCS, credential, paid, published, deployed, or remote mutation. Produces recommended fixes as chat output; never applies them. |
| Side effect | Chat output only: severity-tiered findings with root-cause analysis and committable fix recommendations. No repository mutation. |
| Done | Returns bounded, root-caused DX findings for the smallest relevant public surface. |

## Inputs

Required: the developer-facing surface to audit, a named CLI command, exported API, package, error path, config loader, or the changed public surface from a diff.

Optional: a comparison baseline or prior release contract when the diff changes a public export, signature, or return shape.

## Procedure

1. **Lock scope.** Choose the narrowest mode: targeted (the default; inspect and report on the named or changed public surface) or exhaustive (only when the user explicitly asks for the whole package or every public surface). Write a one-line scope receipt that names the mode, surfaces, selected audit categories, and exclusions (end-user UI, docs prose, repo architecture, private internals). Done when: a one-line scope receipt names the mode, surfaces, categories, and exclusions.
2. **Identify the public surface.** Default to `git diff` against the repository's normal base, keeping only changed files reachable through a public entry point. With no useful diff, use the command, export, package, error, or config named by the user. Public reachability comes from `package.json` `exports`/`bin`, a command registry, an exported type, a documented config loader, or an observed error path. Do not audit a private helper unless a public caller exposes its behavior. Done when: the public surface is identified from the diff or user-named entry point.
3. **Follow the evidence ladder, then stop.** (a) Read local instructions, the relevant manifest, and the diff or named entry point. (b) Trace only direct public dependencies and the nearest tests that establish behavior. (c) For a CLI, use a small safe probe set when useful: `--help`, `--version`, one success path, and one invalid-input path. Do not trigger a real mutation merely to test DX. (d) Check a prior release contract only when the diff changes a public export, signature, or return shape. Stop when the behavior is proven, disproven, private, or outside scope. Do not browse general best-practice articles, inventory unrelated apps, or build static repo maps. Done when: behavior is proven, disproven, private, or outside scope with no unnecessary browsing.
4. **Select audit categories candidate-first.** Map locked surfaces to these categories; applicability outranks global priority:

   | Priority | Category | Default impact | Checks |
   |---|---|---|---|
   | 1 | Public API and SDK | CRITICAL | Argument order, naming consistency, async consistency, no hidden side effects, predictable return shape, sensible defaults, stable contract |
   | 2 | Developer-facing errors | CRITICAL | Fail-fast validation, name/cause/value, no raw stack as message, stable error codes, suggest the fix |
   | 3 | CLI UX | HIGH | Flag naming, help and version, exit codes, structured I/O, pipes/TTY/JSON, schema introspection, agent input hardening, delta polling, idempotent resume, order-independent flags, responsiveness and progress, safe mutations, suggest corrections |
   | 4 | Exported type ergonomics | HIGH | No leaked any, prefer inference, helpful generics, discriminated unions, public JSDoc |
   | 5 | Install and first run | HIGH | Zero-config quickstart, minimal install, no required env, tree-shakeable |
   | 6 | Config ergonomics | MEDIUM | Optional with defaults, validate and discover, XDG and precedence |

   For a public API entry point, audit the API, types, and reached error paths. For a CLI, audit the CLI and reached error paths. For exported declarations, audit types and include API only when behavior changes. For install and first run, audit onboarding. For config loaders, audit config and reached error paths. Done when: categories are selected candidate-first with applicability outranking global priority.

5. **Capability-gate within selected categories.** Structured JSON input and schema introspection apply when automation or agent use is promised, requested, or already supported. Dry-run and confirmation apply to destructive, expensive, or difficult-to-reverse mutations. Progress, delta polling, and resume apply to operations that can block, outlive one command, or be retried after ambiguous output. `stdin` applies when the command semantically accepts file or stream data. Stable-contract comparison applies only when a public contract changed. Done when: capability gates are applied within each selected category.
6. **Rank root causes, not instances.** CRITICAL findings first, then HIGH, then MEDIUM. Merge repeated instances of one root cause into one finding with up to three representative locations. Do not flag a hypothetical missing feature with no current consumer path; YAGNI is not a defect. Do not turn absence of JSDoc, error codes, or a flag into one finding per symbol or command. In targeted mode, report all CRITICAL findings, then the highest-value remaining findings up to five total; summarize any remainder by category rather than expanding the audit. Done when: findings are ranked by root cause with CRITICAL first and repeated instances merged.
7. **Verify on the same scope.** Re-open every cited location, rerun the same safe probes and focused project checks, and reapply the same category checks. A clean build alone does not prove CLI behavior; a runtime probe alone does not prove exported types. Verification evidence must match the finding. Done when: every cited location is re-verified with matching evidence.

## Failure and recovery
- No public surface found: If no changed file is reachable through a public entry point and the user named no surface, return that state and ask for a named command, export, or package. Do not audit private internals to fill the gap.
- Probe resolves the published binary, not the local build: `npx <pkg>` and an existing global install resolve the registry copy, so `--help`, exit codes, and error strings describe a release that does not include the working-tree changes. Build, then invoke the local entry point (e.g., `node ./dist/cli.js`). If the local build cannot be produced, report that the probe reflects the published version and cannot confirm working-tree behavior.
- Scope creep: "DX", "gold standard", or "review everything" do not authorize a multi-repo or whole-package sweep. If the request expands past the scope receipt, stop and re-lock scope rather than widening.
- Partial-result rule: Report all confirmed findings within the locked scope. Summarize out-of-scope candidates by category rather than expanding the audit. Never swallow an error or pretend the done predicate holds when evidence is missing.
- Non-converged: If evidence cannot prove or disprove a behavior (local build unavailable, probe inconclusive), report the finding as unconfirmed with the specific blocker rather than asserting pass or fail.

## Output
A compact report with scope receipt, findings ranked CRITICAL/HIGH/MEDIUM by root cause with file/line/evidence/fix, and deferred out-of-scope candidates summarized by category, or one pass line naming the surfaces and categories checked when no findings are material.
