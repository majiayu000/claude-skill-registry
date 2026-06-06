---
name: deslop
description: Correct code hygiene by detecting AI slop with a three-phase HIGH/MEDIUM/LOW certainty scan, safely auto-fixing only deterministic HIGH findings, verifying with the repo's own test command, and rolling back on regression. Use when the user says "deslop", "clean AI slop", "remove debug code", "find placeholders", "find stub code", or "remove dead code".
metadata:
  short-description: Certainty-graded slop cleanup
---

# deslop — correct slop invariant, preserve behavior

Run a `correct` op-cell: restore the invariant that production code has no debug leftovers, placeholder bodies, swallowed errors, hardcoded credentials, or formatter noise. Classify every finding by certainty; apply only HIGH-certainty mechanical fixes; MEDIUM and LOW are report-only unless the user explicitly asks for a separate manual refactor.

The detailed pattern catalog lives in `references/slop-catalog.md`. Load it when choosing exact pattern recipes or deciding whether a finding is fixable.

## When to Apply / NOT

Apply when the request names AI slop, debug-code cleanup, placeholder/stub cleanup, empty error handlers, hardcoded secrets, dead code, or a pre-PR hygiene sweep.

Do **not** apply for broad architecture simplification, ordinary lint formatting, security audit beyond hardcoded credential patterns, or behavior-changing cleanup. Do not use this to justify deleting code whose purpose is unclear.

## Certainty Contract

| Level | Source | Action |
|---|---|---|
| **HIGH** | Deterministic regex/AST match in non-test, non-fixture, non-generated code | Eligible for mechanical fix, then repo tests |
| **MEDIUM** | Reasoned structural signal or codegraph/context signal | Report only; cite evidence; no auto-fix |
| **LOW** | Optional external CLI heuristic, if tool already exists | Report only; no install; no auto-fix |

Certainty is not severity. A hardcoded token is HIGH certainty and high severity, but still usually `flag-only` because the safe fix is secret rotation plus replacement by an environment read. A trailing-space match is HIGH certainty and low severity, but safe to remove.

## Workflow

1. **Scope files.** Prefer changed files when the user did not request a full sweep. Exclude tests, fixtures, mocks, examples, generated output, vendored code, lockfiles, build artifacts, and minified bundles:
   - `**/test/**`, `**/tests/**`, `**/__tests__/**`, `*.test.*`, `*.spec.*`, `*_test.*`, `*Test.java`
   - `**/fixtures/**`, `**/mocks/**`, `**/testdata/**`, `**/examples/**`, `**/benches/**`
   - `dist/**`, `build/**`, `target/**`, `coverage/**`, `vendor/**`, `node_modules/**`, `*.min.*`, generated/protobuf/openapi outputs
   - keep Markdown out of whitespace cleanup because trailing spaces can be semantic line breaks.

2. **Phase 1 — HIGH deterministic scan.** Use `search` for line patterns and `ast-grep` where syntax shape matters. Record `{file, line, pattern, certainty: HIGH, strategy}`. Recipes:
   - Debug output: `console.log/debug`, Python `print(`/`breakpoint(`/`import pdb`, Rust `println!`/`dbg!`/`eprintln!`, Go `fmt.Print*` with debug labels, Java/Kotlin `System.out/println` when not CLI output.
   - Placeholder bodies: `throw new Error("TODO/not implemented")`, `todo!()`, `unimplemented!()`, `panic!("TODO")`, `raise NotImplementedError`, `def x(): pass`, `def x(): ...`, Go `panic("TODO")`, Java `UnsupportedOperationException`, Kotlin `TODO()`.
   - Empty handlers: JS/TS `catch (...) {}`, Python `except ...: pass`, Java/Kotlin/C++ empty catch blocks, Go `if err != nil {}`.
   - Rust panic shortcuts: bare `.unwrap()` and `.expect()` in non-test code. Flag them HIGH for presence, but do not rewrite automatically.
   - Hardcoded credentials: `sk-`, `ghp_`/`github_pat_`, `AKIA`, `Bearer <token>`, JWT-looking strings, private-key blocks, Slack/Stripe/NPM/Twilio/SendGrid/Discord token forms. Flag only.
   - Mechanical whitespace: mixed tabs+spaces on one indentation prefix, trailing whitespace outside Markdown.

3. **Phase 1b — MEDIUM contextual scan.** Use codegraph first when indexed; otherwise combine `ast-grep`, `search`, and direct reads of the narrow files. Report only:
   - Doc-to-code ratio >3 for a real function with at least 3 code lines.
   - Verbosity ratio >2 comments per code line inside a function; filler/hedging/buzzword comments.
   - Dead code after `return`, `throw`, `break`, or `continue` that is not a language-required fallthrough case.
   - Over-engineering indicators: file/export ratio >20, lines/export >500, directory depth >4 without real module boundaries.
   - Buzzword inflation: claims like "production-ready", "secure", "enterprise-grade", "scalable" with fewer than two concrete supporting code signals.
   - Infrastructure without implementation: `Client`, `Connection`, `Pool`, `Service`, `Provider`, `Manager`, `Factory`, `Repository`, `Gateway`, `Queue`, `Cache`, or `Store` values created but never used beyond setup/export.
   - Stub return values: a function whose only significant body line returns `0`, `null`, `undefined`, `None`, `nil`, `false`, `true`, `[]`, `{}`, `""`, empty collections, `Default::default()`, or `Optional.empty()`. Escalate attention when adjacent TODO/FIXME/STUB text exists, but keep auto-fix disabled.

4. **Phase 2 — LOW optional CLI scan.** Run only tools already available in the repo or PATH; never install. Record findings as LOW and `flag-only`:
   - `jscpd` for duplication.
   - `madge` for cycles.
   - Existing `eslint`, `clippy`, `golangci-lint`, or language-native lint commands from package manifests / project config.
   - If absent, write `missing: <tool>` in the report and continue.

5. **Prioritize.** Sort HIGH before MEDIUM before LOW; then severity; then scope proximity to changed files; then fix strategy. Keep a separate `fixes` list containing only HIGH findings with `remove-line`, `remove-block`, `replace-whitespace`, or `add-comment` strategies. Exclude every `flag-only` finding from automatic edits.

6. **Fix HIGH only.** Apply the smallest edit that removes the deterministic slop:
   - `remove-line`: debug prints, trailing whitespace, isolated commented-out code blocks.
   - `replace-whitespace`: convert mixed indentation to the file's dominant indentation style; strip trailing spaces.
   - `add-comment`: empty catch/except blocks only when the correct behavior is intentionally swallowing the error and the surrounding code proves that intent. Otherwise flag; do not invent logging.
   - `remove-block`: placeholder block only when it is unreachable/dead and removal cannot change API behavior. Stubs on live API surfaces are report-only.
   - `flag-only`: hardcoded secrets, Rust unwrap/expect, placeholder implementations, dead code requiring control-flow judgment, architectural smells.

7. **Verify.** Run the repo's own test command after fixes. Derive it from manifests in this order: package script (`test`, then `check`, then `typecheck`), `cargo test`, `go test ./...`, `pytest`, `mvn test`, `gradle test`, or the project's documented command. If no command exists, run the narrowest parser/type check available and state the limitation.

8. **Rollback on regression.** If verification fails after applying fixes, immediately restore every changed file from the cleanup attempt with `git restore -- <file...>` and rerun the same verifier to confirm the baseline is back. Report the failed fix group as blocked, with file/line and failing command. Never suppress tests, rewrite expectations, or keep a partial cleanup after regression.

## Native Recipes

### Phase 1 search recipes

Use separate narrow searches so the match class is obvious:

```text
search pattern="console\\.(log|debug)\\(" paths=[source globs]
search pattern="\\b(print\\(|breakpoint\\(|import pdb|import ipdb)" paths=["**/*.py"]
search pattern="(println!|dbg!|eprintln!)\\(" paths=["**/*.rs"]
search pattern="throw\\s+new\\s+Error\\s*\\(\\s*['\"`].*(TODO|implement|not\\s+impl)" paths=["**/*.{js,jsx,ts,tsx,mjs,cjs}"]
search pattern="\\b(todo|unimplemented)!\\s*\\(|\\bpanic!\\s*\\(\\s*['\"].*(TODO|implement)" paths=["**/*.rs"]
search pattern="raise\\s+NotImplementedError|def\\s+\\w+\\s*\\([^)]*\\)\\s*:\\s*(pass|\\.\\.\\.)" paths=["**/*.py"]
search pattern="catch\\s*(\\([^)]*\\))?\\s*\\{\\s*\\}|except\\s*[^:]*:\\s*pass\\s*$|if\\s+err\\s*!=\\s*nil\\s*\\{\\s*\\}" paths=[source globs]
search pattern="sk-[A-Za-z0-9]{32,}|ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{80,}|AKIA[0-9A-Z]{16}|Bearer [A-Za-z0-9._~+/-]{20,}|-----BEGIN (RSA )?PRIVATE KEY-----" paths=[source globs]
search pattern="^\\t+ +|^ +\\t+|[ \\t]+$" paths=[source globs excluding markdown]
```

Use `ast-grep` for shapes that regex overmatches:

```text
ast-grep pat="console.log($$$ARGS)" paths=["**/*.{js,jsx,ts,tsx,mjs,cjs}"]
ast-grep pat="try { $$$BODY } catch ($E) { }" paths=["**/*.{js,jsx,ts,tsx,mjs,cjs}"]
ast-grep pat="$X.unwrap()" paths=["**/*.rs"]
ast-grep pat="$X.expect($MSG)" paths=["**/*.rs"]
ast-grep pat="throw new UnsupportedOperationException($$$ARGS)" paths=["**/*.java"]
```

### Phase 1b codegraph recipes

Prefer indexed codegraph for blast-radius and cross-file claims:

```text
codegraph_explore("exports, entry points, callers, callees, infrastructure setup and usage in <scope>")
codegraph_callers(<symbol>)
codegraph_callees(<symbol>)
codegraph_impact(<symbol>)
```

Fallback when not indexed:

```text
ast-grep pat="function $NAME($$$ARGS) { return $VALUE }" paths=[source globs]
ast-grep pat="$NAME = new $TYPE($$$ARGS)" paths=[source globs]
git grep -n -E "(production-ready|production-grade|enterprise-grade|secure by default|scalable|highly available)" -- ':!**/test/**' ':!**/fixtures/**'
git grep -n -E "(Client|Connection|Pool|Service|Provider|Manager|Factory|Repository|Gateway|Queue|Cache|Store)" -- ':!**/test/**' ':!**/fixtures/**'
```

## Anti-patterns

- **Auto-fixing MEDIUM/LOW.** Contextual signals are evidence for a human edit, not permission to delete.
- **Installing scanners.** Phase 2 uses existing tools only.
- **Formatting the repo.** Do not turn slop cleanup into style normalization.
- **Secret deletion as remediation.** Removing a token from source is not enough; require rotation and replacement with environment/config access.
- **Deleting placeholder APIs.** A stub that is part of public surface is a product gap, not dead code.
- **Inventing catch behavior.** Empty handler fixes require known intended behavior; otherwise flag.
- **Counting tests/fixtures/generated files.** They intentionally contain fake tokens, placeholders, console output, and fixture weirdness.
- **Keeping fixes after red verification.** Regression means restore changed files immediately.

## Validation Gates

| Gate | Pass Criteria | Blocks |
|---|---|---|
| Scope gate | Tests/fixtures/generated/vendored files excluded | Any auto-fix touching excluded files |
| Certainty gate | Only HIGH deterministic findings enter `fixes` | MEDIUM/LOW edit attempt |
| Strategy gate | Every fix has `remove-line`, `replace-whitespace`, `add-comment`, `remove-block`, or `flag-only` | Unclassified edit |
| Behavior gate | Repo verifier passes after fixes | Keep no cleanup; run rollback |
| Rollback gate | `git restore -- <file...>` restores changed files after regression and verifier confirms baseline | Any failed verification with retained edits |

Deliver a compact report: changed files, HIGH fixes applied, MEDIUM/LOW findings left for manual inspection, verifier command and result, rollback action if any.