---
name: code-slimming
description: >
  · Audit read-only code slimming: safe deletion, deduplication, wrapper removal, shared contracts. Triggers: 'slim codebase', 'LOC deletion review', 'dedupe safely'. Not for style/slop, bugs, tests, or broad reviews.
license: MIT
compatibility: "None - works on any codebase"
metadata:
  source: iuliandita/skills
  date_added: "2026-05-02"
  effort: medium
  argument_hint: "[scope-or-diff]"
---

# Code Slimming: Read-Only Refactor Opportunity Audit

Find behavior-preserving opportunities to make a codebase smaller, clearer, and less repetitive.
This skill reports opportunities only. It does not edit code and does not write tests.

The goal is not fewer lines at any cost. The goal is lower maintenance burden with behavior,
performance, readability, and validation made explicit.

## When to use

- Finding opportunities to simplify a repository, package, module, or PR
- Finding behavior-preserving refactor opportunities without implementing them
- Auditing duplicated logic, classes, structs, helpers, types, schemas, handlers, or adapters
- Looking for safe centralization candidates before a cleanup/refactor PR
- Reviewing a bot or human cleanup PR that claims to reduce code size
- Ranking maintainability refactors by value, risk, and validation needs
- Handling duplicate code only when the main goal is smaller behavior-preserving structure,
  not general cleanliness or AI-slop detection

## When NOT to use

- Bug-focused reviews, regressions, races, edge cases, or crashes - use **code-review**
- General cleanup, naming, comments, AI tells, dependency creep, overengineering, or
  duplicate-code-as-slop without an explicit slimming goal - use **anti-slop**
- Security vulnerabilities, secret scanning, auth flaws, or exploitability - use **security-audit**
- Writing, debugging, or adding validation tests for a slimming recommendation - use **testing**
- Broad quick merge checks - use **full-review**
- Comprehensive repo audits across all applicable dimensions - use **deep-audit**
- Direct implementation work - use the relevant language, framework, or domain skill

## Routing boundaries

| User intent | Use |
|---|---|
| "Slim this codebase", "find safe deletions", "review LOC deletion" | **code-slimming** |
| "Clean this up", "does this look AI-written?", "overengineered/verbose" | **anti-slop** |
| "This prose/comments read AI-written, clean them up" | **anti-ai-prose** |
| "Review this", "find bugs", "sanity check", "will this break?" | **code-review** |
| "Write/add/debug tests for this refactor" | **testing** |
| "Run all checks", "full review", "audit this repo" | **full-review** or **deep-audit** |
| "Implement the slimming/refactor" | Relevant language/framework/domain skill |

Do not activate this skill for generic review, cleanup, or audit wording unless the user explicitly
asks for slimming, deduplication, deletion, wrapper removal, or behavior-preserving size reduction.

---

## AI Self-Check

Before returning a code-slimming audit, verify:

- [ ] **Read-only boundary held**: no source files were edited and no tests were written
- [ ] **Behavior preserved**: every recommendation names the behavior that must stay identical
- [ ] **Value explained**: every recommendation states why the slimmer shape is better
- [ ] **Tradeoffs assessed**: performance, coupling, readability, bundle size, allocation count,
  and test brittleness were considered where relevant
- [ ] **Validation named**: each `Do now` or `Do with tests` item lists concrete validation
  commands or test coverage needs
- [ ] **No abstraction theater**: no vague "make this generic" or "create a base class" advice
  without the proposed shape
- [ ] **Duplication judged in context**: likely divergence, framework conventions, and explicitness
  were considered before recommending centralization
- [ ] **Correctness and security routed**: bugs go to code-review; vulnerabilities go to security-audit
- [ ] **Routing lane held**: generic cleanup, slop, correctness, security, test-writing,
  broad-review, and implementation work were routed instead of reported as code-slimming findings
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: recommendations do not duplicate anti-slop, code-review, testing, full-review, or deep-audit responsibilities
- [ ] **Spec claims verified**: any statement about skill behavior, output contracts, or repo conventions is checked against current skill files and scripts

---

## Performance

- Start with changed files, shared modules, and repeated directory shapes before scanning the whole repo.
- Group repeated examples into one finding with representative paths.
- Prefer cheap structural searches before expensive test suites.

---

## Best Practices

- Treat smaller code as a hypothesis, not a win.
- Prefer deleting wrappers over adding a new abstraction layer only after proving the wrapper has no
  boundary, policy, observability, compatibility, or lifecycle role.
- Prefer a small well-named helper over a framework-shaped base class.
- Keep domain-specific duplication when the variants are likely to diverge.
- Keep defensive duplication when checks intentionally repeat across trust boundaries, process
  boundaries, public APIs, persistence layers, or privileged operations. Do not remove a repeated
  guard just because an upstream layer appears to validate the same condition.
- Avoid centralizing across independently versioned modules, separately owned teams, protocol or API
  versions, tenant-specific behavior, or plugin/provider boundaries unless the shared contract is
  explicit and stable.
- Recommend tests before centralization when behavior differences are subtle or undercovered.

## Workflow

### Step 1: Determine scope

Pick the narrowest useful scope:

- **PR or diff** - default when uncommitted changes or a branch diff exists
- **Specific path** - use when the user names files or directories
- **Whole repo** - use when the user asks for a repo-wide slimming audit

For git repos, gather cheap preflight context before deciding:

- repo root and branch: `git rev-parse --show-toplevel`, `git branch --show-current`
- uncommitted files: `git diff --name-only`, `git diff --cached --name-only`
- branch base when available: `git merge-base HEAD @{upstream}`; otherwise detect the default
  branch and use `git merge-base HEAD origin/<default-branch>`
- default branch when needed: `git symbolic-ref refs/remotes/origin/HEAD --short 2>/dev/null`
  or inspect `git remote show origin`
- changed files and size: `git diff --name-only <base>...HEAD`, `git diff --stat <base>...HEAD`

Scope precedence:

1. User-provided diff or path
2. Uncommitted changes
3. Current branch against upstream
4. Current branch against the default branch
5. Whole repo, or ask one concise question when interactive

If the scope is unclear and no diff exists, ask one concise question. In headless contexts, default
to whole repo and state the assumption.

### Step 2: Gather context

Read project instructions and manifests before judging code shape:

- instruction files: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursor/rules`, `.windsurfrules`
- manifests: `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`,
  `build.gradle`, `CMakeLists.txt`, `Makefile`
- test and check scripts
- existing shared modules, helper directories, framework conventions, and recent related commits

Note the language and framework patterns in the report header. A good centralization in Python may
be a bad abstraction in Rust, Java, or C.

### Step 3: Identify validation without over-running it

Running existing read-only validation commands is allowed unless the user forbids command execution
or the commands have side effects. Separate validation into three passes:

1. **Early baseline validation** - cheap checks that describe current repo or diff health:
   - lint or format checks when fast and obvious
   - type or compile checks when fast and local
   - documented project validation commands
2. **Candidate coverage evidence** - after finding a slimming candidate, inspect existing tests,
   callers, snapshots, fixtures, or examples that exercise the behavior to preserve.
3. **Implementation validation** - commands or tests someone must run if they implement the
   recommendation.

Do not run expensive full suites before candidate discovery unless the user asked for PR validation
or the project makes the command cheap and standard. If a check is missing, slow, flaky, noisy,
unavailable, external-service-dependent, or exits zero while printing warnings, report that as a
validation gap. Do not call an opportunity safe when validation is absent.

Passing current checks does not by itself make a proposed slimming safe. `Do now` requires
behavior-specific coverage evidence, or a trivial mechanical change whose invariant is directly
verifiable. Generic lint, type, and build commands alone are not enough for behavioral
deduplication or centralization.

For future work, identify the validation an implementation must pass. Do not write tests in this
skill.

### Step 4: Search for candidates

Use structural and textual searches to find:

- near-duplicate files, classes, structs, functions, methods, hooks, handlers, or components
- repeated type, interface, schema, DTO, record, enum, or data container shapes
- repeated request parsing, query construction, pagination, validation, mapping, serialization, or error handling
- wrappers with little behavior beyond forwarding to another object or function
- oversized `utils`, `helpers`, `common`, `shared`, or `misc` modules
- parallel provider, client, repository, service, or adapter implementations with the same skeleton
- dependencies or helpers duplicating standard library or framework features
- generated-looking copy-paste that survived human maintenance, after checking whether a generator,
  schema, template, or vendored source owns it

Discovery recipe:

1. Build a candidate map from changed files, same-role siblings, repeated basenames, large generic
   modules, and repeated exported symbols, routes, schemas, DTOs, handlers, parsers, validators,
   mappers, and serializers.
2. Use cheap searches before manual reading: compare same-role trees such as `providers/*`,
   `clients/*`, `services/*`, `repositories/*`, `handlers/*`, `routes/*`, and `adapters/*`; search
   repeated declarations and one-line wrappers that only forward to another call; find large generic
   modules named `utils`, `helpers`, `common`, `shared`, or `misc`.
3. For each candidate, read the full candidate files, at least one nearby caller, and nearby tests
   to see whether the behavior contract is already captured, before classifying.

Skip or de-prioritize generated files, vendored dependencies, lockfiles, snapshots, fixtures,
minified bundles, protobuf/OpenAPI generated clients, and build artifacts unless the user scopes them.
When duplication appears in generated output, recommend changing the generator, schema, or template,
or exclude it from slimming findings. Do not recommend hand-editing generated output.

Read surrounding code before judging. Similar shape is not enough. The question is whether one
shared behavior path would be clearer, safer, and easier to validate.

### Step 5: Classify opportunities

Use these labels:

- **Do now** - small, obvious, low risk, and already covered by meaningful validation
- **Do with tests** - likely worthwhile, but needs focused tests before implementation
- **Defer** - valid but too broad, risky, or low-value for current churn
- **Leave alone** - duplication is clearer, faster, intentional, or likely to diverge

These labels are audit recommendations only. Even `Do now` does not authorize this skill to edit
code; it means the proposed change appears safe for a separate implementation pass.

Every classified item must cite:

- representative file paths and line ranges
- the repeated behavior or wrapper behavior observed
- the behavior invariant that must remain identical
- existing validation evidence or the missing validation gap
- why similar-looking cases are included, excluded, or left alone

Most findings are not merge blockers. Say so clearly.

For `Do now`, cite behavior-specific validation evidence: exact test files or cases that exercise
the preserved behavior, or explain why the change is purely local, mechanical, and directly
inspectable. Generic lint, type, and build commands alone are not enough for behavioral
deduplication or centralization. If you cannot cite behavior-specific evidence, classify as
`Do with tests` or `Defer`.

### Step 6: Evaluate tradeoffs

For every recommendation, answer:

- What behavior must remain identical?
- What gets smaller: LOC, concept count, duplicated call sites, public API surface, dependency
  count, file count, or test surface?
- What might get worse: runtime performance, bundle size, allocation count, readability, coupling,
  test brittleness, or onboarding clarity?
- Why is the proposed centralization better than the current duplication?
- What validation would prove the change is safe?
- Are duplicated checks intentionally defensive at separate boundaries, and what fails closed if one
  layer is bypassed?

If a slimmer implementation affects hot paths, rendering loops, query batching, serialization,
startup, memory layout, build output, or binary size, require performance-sensitive validation
before classifying it as `Do now`.

### Step 7: Report

It is acceptable and often correct to return zero high-value opportunities. Do not manufacture a
slimming recommendation to fill the report. Prefer a well-justified `Leave alone` finding over a
low-confidence abstraction.

Use this format:

```markdown
## Code Slimming Audit: [scope]

Context:
- Languages/frameworks: [detected]
- Baseline validation run: [commands and results; implementation validation not run because this audit is read-only]
- Validation gaps: [missing, noisy, skipped, or unavailable checks]

### High-Value Opportunities

**Do with tests** `services/*/list-items.*` - Centralize repeated pagination and filter parsing.
Affected files: `services/users/list-items.*`, `services/projects/list-items.*`
Evidence: `services/users/list-items.ts:24-58`, `services/projects/list-items.ts:19-55`
Current duplication: both modules parse the same page, limit, sort, and filter parameters.
Refactor shape: extract a shared parser with endpoint-specific allowlists.
Behavior invariant: page and limit defaults, max-limit handling, sort allowlists, and error messages stay identical.
Call-site impact: 2 endpoint handlers, no public import path changes.
Why better: one behavior path for defaults and validation, with fewer divergent call sites.
Tradeoffs: one shared helper couples list endpoints to a common pagination contract.
Risk: medium
Validation needed: add boundary tests for page and limit values, then run lint/type/build/test commands.

### Removed-Code Safety Review

Include this section only when reviewing a diff or PR that removed code.

**Needs evidence** `[area]`
Removed behavior: [code path, wrapper, branch, fallback, type, validation, or dependency removed]
Replacement path: [what now handles it]
Behavior invariant: [what must still happen]
Evidence checked: [diff lines, call sites, tests, type checks]
Risk: [low/medium/high]
Validation needed: [specific command/test/case]

### Low-Value Or Risky Opportunities

**Leave alone** `integrations/*` - Duplication is likely to diverge per provider.
Why not: each provider already has different retry, auth, pagination, and error semantics.

### Summary

- High-value opportunities: 1
- Low-value or risky opportunities: 1
- Merge blockers: none from this audit lens
- Residual risk / skipped areas: [large dirs, generated files, expensive checks, external services]
- Net recommendation: [slim / defer / leave mostly unchanged], based on risk-adjusted maintenance value, not LOC delta
```

If no useful slimming opportunities are found, say so explicitly:

```markdown
### High-Value Opportunities
None found within scope.

### Search Coverage
- Scope inspected: [diff/path/repo areas]
- Patterns checked: [wrappers, duplicate schemas, repeated parsers, adapters, utils]
- Files/directories skipped: [generated/vendor/tests/etc.]
- Validation checked: [commands/tests found or unavailable]

### Why no action is recommended
- Existing duplication appears intentional because: [...]
- Thin wrappers are retained because: [...]
- Shared abstraction would likely worsen: [...]

### Low-Value Or Risky Opportunities
[optional leave-alone observations]

### Summary
- High-value opportunities: 0
- Low-value or risky opportunities: N
- Merge blockers: none from this audit lens
- Residual risk: [what was not inspected]
- Net recommendation: leave mostly unchanged
```

Keep the report concise. Show the refactor shape, not a lecture.

## Common Patterns

### Repeated boundary parsing

Request parsing, CLI argument normalization, env var parsing, and config loading often duplicate
defaulting and validation rules. Centralize only when the same boundary contract really applies.

### Near-twin adapters

Provider/client/repository adapters often start identical and then diverge. Recommend
centralization only when the shared part is stable and the provider-specific differences stay
explicit.

### Duplicate data shapes

Repeated DTOs, schemas, records, structs, or interfaces can be centralized when they represent the
same contract. Keep separate shapes when they describe different lifecycle stages or trust
boundaries. Do not merge inbound untrusted request shapes, internal/domain shapes, persistence
entities, queue/event payloads, and outbound response shapes merely because fields overlap. Shared
field lists are not shared contracts; centralize only the truly common validated subset, or keep
explicit mappers.

### Wrapper layers

Thin wrappers that only forward calls usually add concept count without value. Prefer deleting or
inlining them unless they isolate an external dependency, provide a stable public contract, or make
testing materially easier. Leave them alone when they enforce validation, auth/authorization,
tenant isolation, retries, idempotency, transactions, caching, rate limits, logging, tracing,
metrics, feature flags, compatibility shims, dependency inversion, or fault isolation.

### Oversized helper modules

Large `utils`, `helpers`, `common`, `shared`, or `misc` modules are often junk drawers. Recommend
splitting by domain concern or moving helpers closer to their only caller.

### Performance-sensitive slimming

Shorter code can be slower. Centralized generic code can add allocation, dynamic dispatch, reflection,
bundle weight, cache misses, or indirect calls. In hot paths, require measurement or classify as
`Defer`.

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** CODE-SLIMMING
- **Deliverable bucket:** `audits`
- **Mode:** always-on for audit and review invocations. Every invocation that analyses existing code emits the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table. For a quick factual question (e.g., "what is wrapper removal?") respond freely without the contract.
- **Deliverable path:** `docs/local/audits/code-slimming/<YYYY-MM-DD>-<slug>.md`
- **Severity scale:** not the shared P0-P3 scale. Findings are classified by action - `Do now | Do with tests | Defer | Leave alone` - plus a `Risk: low | medium | high` field per finding (see the Workflow). This skill proposes deletions, not severity-ranked defects.

## Related Skills

- **anti-slop** - code quality audit for AI-like patterns, over-abstraction, noisy comments,
  hallucinated APIs, and test theater.
- **anti-ai-prose** - prose-slimming for AI voice in docs, comments, and docstrings. Use when the
  goal is removing AI-written prose patterns rather than reducing code size.
- **code-review** - correctness audit for bugs, regressions, races, edge cases, and broken contracts.
- **testing** - writes and debugs tests required before implementing a slimming recommendation.
- **security-audit** - reviews security-sensitive code where "defensive" duplication may be necessary.
- **full-review** - quick four-pass merge-safety audit; does not include code-slimming by default.
- **deep-audit** - comprehensive repo audit; includes code-slimming as a Wave 2 maintainability pass.

## Rules

1. **Do not edit code.** This skill reports opportunities only.
2. **Do not write tests.** Name missing tests and route test implementation to testing.
3. **Do not chase LOC alone.** Smaller code that is slower, more coupled, or harder to understand
   is not automatically better.
4. **Require a concrete refactor shape.** Every recommendation must describe what would be
   extracted, deleted, moved, or centralized.
5. **Explain why.** Every recommendation must state the maintenance benefit and the behavior that
   must remain unchanged.
6. **Validate before calling it safe.** A `Do now` recommendation needs behavior-specific
   validation evidence, or a purely local mechanical invariant that was directly inspected.
7. **Respect language idioms.** Generic helpers, inheritance, macros, templates, reflection, and
   dynamic dispatch have different costs across Python, JavaScript/TypeScript, Java, Rust, C/C++,
   shell, and infrastructure code.
8. **Keep bugs and vulnerabilities in their lanes.** Route correctness findings to code-review and
   security findings to security-audit.
