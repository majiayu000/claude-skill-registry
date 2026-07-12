---
name: ln-22-codebase-auditor
description: "Audits cross-cutting code health across security, delivery, maintainability, dependencies, diagnosability, concurrency, and lifecycle. Use when no specialist audit is primary."
---

# Codebase Auditor

Perform a broad, read-only production-code health audit. Find concrete cross-cutting failure, security, delivery, and maintenance risks without turning detector matches or personal style preferences into findings. Do not substitute for documentation trust, test-portfolio, whole-architecture, or persistence-specific review.

## Tool Routing

| Need | Preferred tool | Use it when | Fallback |
|---|---|---|---|
| Repository map and stack detection | Native file listing, manifests, build files, and repository instructions | Establishing scope, generated areas, entrypoints, supported runtimes, and commands | Targeted tree inspection and known entrypoints |
| Symbols, callers, ownership, and data flow | Language server or host-native code intelligence | A finding depends on symbol identity, references, overrides, route wiring, or cross-file behavior | Narrow text search plus direct inspection of every relevant match |
| Current changes and historical context | Git status, diff, log, and blame | Separating current work, regressions, intentional constraints, and dead compatibility paths | Current implementation and explicit decision records |
| Delivery health | Repository-defined build, lint, type, test, and smoke commands | Establishing whether the project can ship in its documented environment | Inspect CI and scripts; mark execution unavailable |
| Dependency and security state | Native package-manager audit, manifests, lockfiles, and official advisories | Checking known vulnerabilities, unsupported versions, and dependency health | Official registry and vendor sources; never guess severity |
| Runtime evidence | Existing logs, metrics, traces, profiles, and diagnostics | Static analysis cannot establish frequency, reachability, or operational impact | Call-path analysis with an explicit static-only limitation |
| Current external behavior | Official specifications, vendor documentation, and release notes | A finding depends on current API, runtime, or standard behavior | Primary-source web research; otherwise mark `UNVERIFIED` |

Start with summary-level discovery and narrow before reading deeply. Run only repository-defined or clearly safe diagnostic commands; never publish, deploy, migrate production data, rotate secrets, or rewrite files during the audit.

## Evidence Rules

- A pattern match is a candidate, not a finding. Confirm reachability, context, and consequence.
- Runtime failure or deterministic command output outweighs static suspicion; static evidence remains valid when execution is unavailable and the limitation is explicit.
- Generated, vendored, fixture, migration-history, and intentionally compatible code require context-specific treatment.
- External best practice is actionable only when it addresses a concrete repository defect or risk.
- Score or count only findings with distinct root causes; deduplicate symptoms that share one correction.

## Checklist

### 1. Establish Scope and Baseline

- [ ] Detect languages, frameworks, package managers, entrypoints, deployment model, generated areas, and the repository's supported verification commands.
- [ ] Classify each runtime surface as long-running service, CLI, library, job, serverless function, or platform-managed component before requiring probes, telemetry, signal handling, or shutdown behavior.
- [ ] Read applicable instructions and identify security boundaries, critical business paths, public interfaces, and irreversible operations.
- [ ] Inspect Git state so the audit does not overwrite, misattribute, or ignore unrelated user changes.
- [ ] Establish build, lint, type, test, and smoke baseline where feasible; record commands, environment, exit status, and relevant output.
- [ ] Define exclusions and depth based on risk rather than scanning every file with equal effort.
- [ ] Keep the audit read-only. Allow only permitted caches and build artifacts and disclose them when created.

### 2. Audit Security and Delivery Boundaries

- [ ] Search for committed secrets, unsafe credential patterns, sensitive defaults, debug bypasses, and accidental exposure through logs or errors.
- [ ] For credential findings, never expose the raw value: distinguish live material from placeholders, fixtures, examples, and allowlisted fingerprints; report only the type, location, and redacted evidence, and recommend revocation, rotation, or history remediation only for confirmed exposure without performing it during the audit.
- [ ] Trace untrusted input into SQL, shell, templates, HTML, file paths, URLs, deserialization, redirects, and other injection-sensitive sinks.
- [ ] Check authentication, authorization, tenant or ownership isolation, privilege transitions, insecure direct object access, and default-deny behavior.
- [ ] Check validation at trust boundaries, canonicalization, size and rate limits, unsafe file operations, and destructive-action confirmation or guards.
- [ ] Verify security findings against actual call paths, framework behavior, configuration, and current official guidance before assigning severity.
- [ ] Inspect compiler, linter, type checker, tests, packaging, and CI configuration for skipped gates, ignored failures, environment drift, and non-reproducible delivery.
- [ ] Verify that successful packaging produces the intended entrypoints, assets, metadata, target platform, and deployable artifact; exit code zero alone does not prove a shippable build.
- [ ] Find stale skip, quarantine, allow-failure, continue-on-error, and warning-suppression paths that make required signals appear green.
- [ ] Check configuration completeness, required environment validation, unsafe fallbacks, missing examples, and differences between local, CI, and deployment settings.

### 3. Audit Maintainability and Dependencies

- [ ] Find evidence-backed duplication across functions, handlers, modules, configuration, and integration code; distinguish shared domain concepts from coincidental similarity.
- [ ] Identify over-abstraction, unused extension points, excessive factories or wrappers, parallel mechanisms, and custom utilities that duplicate declared platform capabilities.
- [ ] Before merging duplication or removing an abstraction, check lifecycle and ownership boundaries, intentional decoupling, dependency injection or test seams, framework requirements, public extension contracts, and expected independent evolution.
- [ ] Inspect complexity hotspots, long methods, god modules, deep nesting, excessive parameters, boolean-mode APIs, misleading names, and mixed responsibilities.
- [ ] Check algorithms for early-exit mistakes, duplicate-key loss, boundary errors, unbounded work, repeated scans, mutation during iteration, and hidden shared state.
- [ ] Check hardcoded operational values, URLs, timeouts, limits, identifiers, and environment-specific behavior that should be explicit configuration or named policy.
- [ ] Trace one concept across external contracts, DTOs, services, persistence, and storage; flag synonym or casing drift only when no explicit serializer, code-generation, or ORM boundary mapping explains it.
- [ ] Audit dependency vulnerabilities, support status, license or runtime constraints, duplicate packages, unused packages, and credible replacement or removal opportunities.
- [ ] Verify vulnerability findings against the installed version and whether the vulnerable API or feature is reachable; distinguish affected code from a package merely present in the lockfile.
- [ ] Recommend native, existing-dependency, or external replacements only after checking required feature parity, migration surface, maintenance, license, security history, and domain-specific behavior.
- [ ] Find unreachable code, unused imports and exports, commented-out implementations, obsolete flags, dead compatibility shims, and replacement code left beside its successor.
- [ ] Confirm dead-code findings against reflection, registration, framework discovery, configuration, serialization, templates, and external entrypoints before reporting deletion as safe.

### 4. Audit Diagnosability, Concurrency, and Lifecycle

- [ ] Check whether logs are structured, correctly leveled, actionable, correlated across a request or job, and free of secrets and excessive payload data.
- [ ] Verify that correlation context crosses outbound calls, queues, retries, scheduled work, and detached async boundaries instead of existing only in the first request log.
- [ ] Check metrics, traces, health signals, and error context for critical paths; require observability only where operators need it to detect or diagnose failure.
- [ ] Trace shared mutable state, lock ordering, atomicity, async task ownership, cancellation, retries, and race windows on reachable concurrent paths.
- [ ] Inspect read-modify-write across await or yield points and build a resource/accessor timeline for shared files, subprocesses, terminal or OS resources, and repeated user triggers; include accessors outside the current process.
- [ ] Check blocking I/O or synchronous waits in async paths, unbounded concurrency, orphan tasks, deadlocks, TOCTOU hazards, and thread-unsafe resources.
- [ ] Inspect startup ordering, dependency readiness, configuration validation, fail-fast behavior, signal handling, graceful shutdown, and in-flight work draining.
- [ ] Inventory resources acquired during startup and runtime, then match each to idempotent cleanup in safe reverse dependency order on success, failure, timeout, cancellation, and repeated shutdown signals.
- [ ] Keep probe semantics distinct: liveness proves the process can recover without checking fragile dependencies, while readiness withholds traffic until required dependencies and initialization are usable; neither probe should create material load or side effects.

### 5. Validate Findings and Report

- [ ] Research external APIs, standards, vulnerabilities, and runtime behavior only when they can change a finding, using official sources matching the relevant version.
- [ ] Filter framework conventions, generated code, bounded administrative paths, tests, examples, and documented tradeoffs before confirming a candidate.
- [ ] Reproduce high-severity issues with a safe command, test, minimal call trace, or complete static failure path whenever possible.
- [ ] Classify findings as `P0`-`P3` based on exploitability, data or availability impact, delivery blockage, recurrence, and remediation urgency.
- [ ] Include location, evidence, trigger or failure path, impact, confidence, effort, and smallest credible remediation for every finding.
- [ ] Order remediation by risk reduction and dependency, not by file order or detector category.
- [ ] Use `BLOCKED` when a required safety environment, high-risk behavior, or authoritative contract cannot be verified without a credible fallback; use `FAIL` for an evidenced unresolved `P0/P1`, required failing delivery gate, or demonstrated unsafe behavior; use `CONCERNS` only for verified non-blocking risks, and `PASS` only when required checks complete with no material finding.
- [ ] Return the verdict with executed checks, excluded scope, verified findings, unverified candidates, and residual codebase risk.

## Output Contract

```markdown
# Codebase Audit

**Verdict:** PASS | CONCERNS | FAIL | BLOCKED

## Scope and baseline
- Stack, entrypoints, and exclusions
- Commands and environments checked
- Static and runtime evidence available

## Health summary
| Area | Status | Evidence |
|---|---|---|
| Security | PASS / CONCERNS / FAIL | ... |
| Delivery | PASS / CONCERNS / FAIL | ... |
| Maintainability | PASS / CONCERNS / FAIL | ... |
| Dependencies and dead code | PASS / CONCERNS / FAIL | ... |
| Diagnosability, concurrency, lifecycle | PASS / CONCERNS / FAIL | ... |

## Findings
### [P0 | P1 | P2 | P3] Finding title
- Location and path to failure
- Evidence and confidence
- Impact and affected surface
- Required change and effort

## Remediation order and residual risks
Dependency-aware next actions, blind spots, and unverified candidates.
```
