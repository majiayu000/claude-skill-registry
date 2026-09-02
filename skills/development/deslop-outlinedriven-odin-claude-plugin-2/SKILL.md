---
name: deslop
description: 'Use when the user says deslop, debloat, tidy, simplify, clean up this diff, or deslop a branch diff, or asks to remove dead code, placeholders, stubs, dead fields, redundant wrappers, or stale config, or the slop skill routes here. Not for remote, credential, publish, deploy, or irreversible changes.'
---

# Deslop

Four modes share one spine: bound scope, verify with the repo's own command, rollback on regression, atomic commits separate from behavior changes.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The user says deslop, debloat, tidy, simplify, clean up this diff, deslop a branch diff, remove dead code, find placeholders or stubs, remove dead fields, redundant wrappers, or stale config, or the slop skill routes code findings here |
| Authority | Reversible local writes to production source files or prose artifacts; may run the repo verifier and `git restore` on regression |
| Side effect | Local writes to production source files or prose artifacts; no edits to tests, fixtures, mocks, examples, generated, vendored, or lockfile/build artifacts |
| Done | Mode-specific done predicate holds; verifier green or rollback confirmed |

## Refusal

Not for behavior changes, new abstractions, or refactors that introduce patterns — a tidy pass that would change observable behavior stops and reports a candidate for a separate refactor. Not for remote, credential, publish, deploy, or irreversible changes. Not for duplication across artifacts or drift — those are handed off, not force-compressed. Not for non-code targets (memory, git workspace, docs) — route to their owners. Not for opportunistic sweeps across untouched files in tidy mode — the candidate must lie in code already under edit.

## Mode selection

| User says | Mode | Target |
|---|---|---|
| deslop, remove debug code, find placeholders or stubs, remove dead code, slop routed here | slop | Production source files |
| debloat, tighten this, too long | bloat | One padded prose artifact (document, skill, spec) |
| tidy this up, simplify, clean up this diff, polish my changes, make this simpler | tidy | Code in the working tree |
| dead field, redundant wrapper, stale config, duplicate state, speculative abstraction | tidy | Code already under edit |
| deslop this branch diff, remove AI debris from my branch, clean up added lines only | diff | Added/modified lines in a branch diff |

## Shared spine

1. **Bound scope.** Prefer changed files unless the user requested a full sweep. Exclude tests, fixtures, mocks, examples, generated output, vendored code, lockfiles, build artifacts, and minified bundles: `**/test/**`, `**/tests/**`, `**/__tests__/**`, `*.test.*`, `*.spec.*`, `*_test.*`, `*Test.java`, `**/fixtures/**`, `**/mocks/**`, `**/testdata/**`, `**/examples/**`, `**/benches/**`, `dist/**`, `build/**`, `target/**`, `coverage/**`, `vendor/**`, `node_modules/**`, `*.min.*`, generated/protobuf/openapi outputs. Keep Markdown out of whitespace cleanup — trailing spaces can be semantic line breaks. Done when: the file set is enumerated and exclusions applied.

2. **Verify.** Run the repo's own test command after fixes. Derive it from manifests in this order: package script (`test`, then `check`, then `typecheck`), `cargo test`, `go test ./...`, `pytest`, `mvn test`, `gradle test`, `dotnet test`, `bundle exec rspec` or `rake test`, `composer test` or `phpunit`, `swift test`, or the project's documented command. If no command exists, run the narrowest parser/type check available, state the limitation, and treat every fix as unverified. Done when: the verifier has run or the limitation is stated.

3. **Rollback on regression.** If verification fails, immediately `git restore -- <file...>` every changed file, rerun the verifier to confirm baseline, and report the failed fix group as blocked with file/line and failing command. Never suppress tests, rewrite expectations, or keep partial results. Done when: baseline is confirmed restored or fixes are verified green.

4. **Commit separately.** Cleanup commits are always separate from behavior commits. Use atomic commits with clear messages naming what was removed. If a cleanup is mixed into a behavior commit, split it with `git move --fixup` or `git split` before merging. Done when: each commit has exactly one concern and the diff is net-deletion or inline-and-delete only.

## Slop mode

Certainty-graded mechanical slop removal from production source. Full category catalog, per-language instances, and autofix strategy semantics: `references/slop-catalog.md`.

1. **HIGH deterministic scan.** Use `search` for line patterns and `ast-grep` where syntax shape matters. Record `{file, line, pattern, certainty: HIGH, strategy}` for each finding. Categories: debug output (stream-writing mechanism left behind after debugging — exclude output that is the product: CLIs, loggers, entrypoints), placeholder or unimplemented body (empty block, no-op, not-yet-implemented throw, TODO-marked panic), swallowed failure (catch/except/rescue that discards the error so the unhappy path continues with invalid state), crash-on-failure shortcut (forced unwrap, unchecked cast, abort-on-error where failure is recoverable — flag only), hardcoded credential (`sk-`, `ghp_`/`github_pat_`, `AKIA`, `Bearer <token>`, JWT strings, private-key blocks — flag only), placeholder text (lorem ipsum, `asdf asdf`, `foo bar baz`, `replace this`, `TODO: implement`), privilege and supply-chain hazard (`chmod 777`, piping download into shell — flag only), whitespace artifact (mixed tabs+spaces on one indentation prefix, trailing whitespace outside Markdown). Done when: every HIGH category has been scanned.

2. **MEDIUM contextual scan.** Use codegraph first when indexed; otherwise combine `ast-grep`, `search`, and direct reads of the narrow files. Report only, no auto-fix: comment bloat (doc-to-code ratio >3 for a real function with ≥3 code lines, or >2 comments per code line inside a function; filler/hedging/buzzword comments), dead or unreachable code (statements after `return`/`throw`/`break`/`continue` that are not a language-required fallthrough), commented-out code (consecutive comment lines whose content is code), mutable global state (module-level binding named as constant but declared mutable, or mutable global collection outside settings/constants), missing safety justification (escape-hatch construct entered without the adjacent comment its convention requires), suppression escape (warning or type-check suppression applied instead of fixing the finding), over-engineering indicators (file/export ratio >20, lines/export >500, directory depth >4 without real module boundaries), unsubstantiated capability claim ("production-ready", "secure", "enterprise-grade", "scalable" with fewer than two concrete supporting code signals), infrastructure without implementation (`Client`/`Connection`/`Pool`/`Service`/`Provider`/`Manager`/`Factory`/`Repository`/`Gateway`/`Queue`/`Cache`/`Store` values created but never used beyond setup/export), stub return values (function whose only significant body line returns `0`/`null`/`undefined`/`None`/`nil`/`false`/`true`/`[]`/`{}`/`""`/empty collections/`Default::default()`/`Optional.empty()` — escalate attention when adjacent TODO/FIXME/STUB text exists, keep auto-fix disabled). Done when: MEDIUM findings are recorded.

3. **LOW optional CLI scan.** Run only tools already available in the repo or PATH; never install. Record findings as LOW and `flag-only`: `jscpd` for duplication, `madge` for cycles, and the linter the project already declares (derived from its manifest or config: `eslint`, `clippy`, `golangci-lint`, `ruff`, `ktlint`, `rubocop`, `phpstan`, `swiftlint`, the .NET analyzers, and equivalents). If a tool is absent, write `missing: <tool>` and continue. Done when: available tools have run.

4. **Prioritize.** Sort HIGH before MEDIUM before LOW; then severity; then scope proximity to changed files; then fix strategy. Keep a separate `fixes` list containing only HIGH findings with `remove-line`, `remove-block`, `replace-whitespace`, or `add-comment` strategies. Exclude every `flag-only` finding from automatic edits. Done when: the fix list is ordered and flag-only findings are excluded.

5. **Fix HIGH only.** Apply the smallest edit that removes the deterministic slop: `remove-line` (debug prints, trailing whitespace, isolated commented-out code blocks), `replace-whitespace` (convert mixed indentation to the file's dominant style; strip trailing spaces), `add-comment` (empty catch/except blocks only when the correct behavior is intentionally swallowing the error and the surrounding code proves that intent — otherwise flag, do not invent logging), `remove-block` (placeholder block only when it is unreachable/dead and removal cannot change API behavior — stubs on live API surfaces are report-only), `flag-only` (hardcoded secrets, crash-on-failure shortcuts, placeholder implementations, dead code requiring control-flow judgment, architectural smells). Done when: all HIGH non-flag fixes are applied.

Done when: HIGH fixes applied and verified, MEDIUM/LOW findings left flagged for manual inspection, verifier green or rollback confirmed.

## Bloat mode

Compress one padded but fully binding prose artifact in place. Every rule present before the pass is present after; the artifact is materially denser.

1. **Read end to end.** Note in one line what each section must convey. No second artifact is read or written. Done when: the artifact's load-bearing structure is mapped.

2. **Find padding.** A needless qualifier, a sentence fusing three ideas, an enumeration better expressed as a rule plus a short list, a nearby restatement, litigation history where the rule alone suffices. Done when: padding candidates are listed.

3. **Compress in place.** Cut the padding, split fused sentences, replace excessive enumerations with a rule and short list, keep repeated points once. Move nothing to another artifact and re-derive nothing. Done when: the artifact is materially denser.

4. **Keep every load-bearing claim.** If cutting a word would lose one, keep the word. Do not accept the loss. Done when: every prior rule and claim is confirmed present.

5. **Hand off non-bloat.** Duplication across artifacts and drift are not bloat; do not force-compress them. State that they were handed off rather than removing them. Done when: non-bloat defects are named and left for their owner.

6. **Review and cut again with fresh eyes.** The first pass always leaves some. Done when: a second pass finds nothing genuine to cut.

Done when: every prior rule and claim remains, the artifact is materially denser, and non-bloat problems are handed off.

## Tidy mode

Remove constructs that do not earn their keep from code in the working tree, then verify. Branch-specific detection patterns: `references/dead-fields.md` (dead fields and members), `references/dead-config.md` (dead flags, env vars, branches), `references/redundant-wrappers.md` (inline-then-delete wrappers).

1. **Confirm scope.** In cleanup-codebase trigger shape (dead field, redundant wrapper, stale config), the candidate must lie in a file already touched by the active change. If it does not, stop: opportunistic sweeps across untouched files are out of scope. In tidy trigger shape (tidy this up, simplify), the scope is the user-named target, the active file, or the current diff. Done when: the exact files and functions in scope are identified.

2. **Read end to end.** Understand what each function, type, and module in scope must do or convey. Note the behavioral contract each piece serves. Done when: the scope's contracts are mapped.

3. **Classify candidates.** For each construct in scope:
   - Dead code: unreachable paths, unused imports, unexported helpers with zero callers, commented-out blocks, stale feature-flag branches that are always-on or always-off.
   - Redundant construct: duplicated logic, a wrapper that only forwards, a variable assigned once and immediately consumed, a conditional whose guard is always true or false in context, a type alias that adds no clarity.
   - Special case: a branch that handles one input shape identically to the general case, a guard that duplicates the default, a fallback that cannot trigger.
   - Ceremony: a factory/builder/adapter with one real implementation, a generic parameter with one concrete use, an abstraction layer with no real boundary behind it.
   - Not a candidate: live behavior, public API contracts, real boundary seams (process, network, untrusted input, FFI, async/sync, test/production where mocks substitute), code that is verbose but not wrong. A swappable-implementation contract counts only when more than one real implementation ships today.

   Indirection earns its keep only at a real boundary: public API surfaces, process or network seams, untrusted-input boundaries, async/sync seams, runtime FFI seams, or test/production seams where mocks substitute. Internal modules in the same package, same-file helpers, and cross-module calls without a co-change constraint are not boundaries. Done when: every construct in scope is classified.

4. **Confirm dead across all consumers.** Run `git --no-pager grep -n` (or `ast-grep`) for every reference to the candidate in code, tests, docs, configs, error messages, and log lines. A field is dead only if it is never read after assignment; a wrapper is redundant only if it adds nothing but a rename or forward. If any consumer is unverified, stop and investigate rather than delete. Done when: every candidate is confirmed dead or redundant across all consumers.

5. **Check coupling.** Determine whether removal breaks the build or forces a refactor of the only consumer. If it does, that is a separate decision; record it and do not delete in this pass. Done when: coupling effects are assessed and blocking couplings are recorded.

6. **Remove in place.** Delete dead code. Inline single-use wrappers at every call site, then delete the wrapper. Collapse special cases into the general path. Fuse duplicated logic into one copy. Remove ceremony that does not protect a real boundary. Never comment out code as a substitute for deletion. Never introduce new patterns, abstractions, or dependencies — the diff must be net-deletion or inline-and-delete only. Done when: all confirmed candidates are removed.

7. **Search for ghosts.** Grep docs, error messages, config keys, env vars, and log lines for string references to the removed concept. Leftover references mean the cleanup is incomplete — remove them, or roll back if they indicate the candidate was not actually dead. Done when: no ghost references remain.

Done when: working tree has fewer dead/redundant/special-cased constructs, every removal is confirmed dead across all consumers, build/lint passes, and no ghost references remain.

## Diff mode

Remove AI-generated debris from a branch diff, bounded to added/modified diff lines only. The shared spine applies; the diff-specific steps below resolve the branch scope and bound every edit to the lines the branch introduced.

1. **Resolve the branch diff scope.** Capture every commit since the branch diverged from its base plus staged and unstaged changes. Try base refs in order and use the first that resolves: `git merge-base HEAD origin/main`, then `origin/master`, then `main`, then `master`, then `@{upstream}`. Run `git diff <base>` (no `..HEAD`, so working-tree changes are included). If none resolves, check HEAD: if `git rev-parse --verify HEAD` fails, HEAD is unborn and the scope is user-named files only; if `HEAD^` fails, HEAD is the root commit and the scope is the working tree (`git diff HEAD`); otherwise stop and request an explicit base, because falling back to `git diff HEAD` on a local-only branch with committed work would silently drop that work. Done when: a base ref resolves and `git diff <base>` runs, or the scope is confirmed as user-named files / working tree / root commit, or the skill stops to request an explicit base.
2. **Enumerate changed files from the diff.** Exclude tests, fixtures, mocks, examples, benchmarks, generated output, vendored code, lockfiles, and build artifacts; they may intentionally contain placeholders, fake tokens, and debug output. Done when: the changed-file list is produced with exclusions applied.
3. **Read local style context.** For each changed file, read the diff hunks plus enough surrounding unchanged lines to judge the file's dominant indentation, naming, comment density, and import ordering. "Matching local style" is the done predicate, so this context is required before any edit. Done when: per-file dominant indentation, naming, comment density, and import ordering are recorded.
4. **Identify AI-generated debris in added lines only.** Scan the lines the branch introduced, not unchanged context. Debris classes: debug output left after debugging (console/print/debug macros/shell tracing), excluding output that is the product (CLIs, loggers, entrypoints); placeholder or unimplemented bodies (empty block, no-op, not-yet-implemented throw/abort, `TODO: implement`); commented-out code blocks; restating-the-code comments and motivational or hedging comments ("Let me...", "Now we...", "Here we..."); placeholder text in string literals (lorem ipsum, `foo bar baz`, `replace this`); unused imports or variables introduced by the change; redundant defensive guards that duplicate a check already present in the same path; mixed tabs+spaces or trailing whitespace on added lines. Done when: every added line is scanned and findings are listed by debris class.
5. **Classify each finding before editing.** Apply only removals that cannot change behavior: delete debug prints, delete restating/hedging/motivational comments, delete commented-out code blocks, delete unused added imports and variables, and normalize added-line indentation and trailing whitespace to the file's dominant convention. Flag-only, no edit: placeholder implementations on live API surfaces, hardcoded credentials, crash-on-failure shortcuts (forced unwrap, unchecked cast, abort-on-error where failure is recoverable), and dead code requiring control-flow judgment. Done when: each finding is marked remove or flag-only.
6. **Bound every edit to added/modified diff lines.** Never edit unchanged context lines, never reformat the whole file, and never introduce new logic, imports, or abstractions. The diff must shrink or stay focused; it must not grow. Done when: edits are applied only on added/modified lines and the diff has not grown.

Done when: focused diff matching local style, verifier green or rollback confirmed.

## Failure and recovery

| Failure mode | Rule |
|---|---|
| Scope violation (auto-fix touches an excluded file) | Revert that file with `git restore`; do not widen scope |
| Certainty violation (MEDIUM or LOW finding edited in slop mode) | Revert the edit; the finding stays report-only |
| Behavior regression (verifier fails after fixes) | `git restore -- <file...>` every changed file, rerun the verifier, report the failed fix group as blocked with file/line and failing command. Keep no partial cleanup |
| Lost-claim cut (bloat mode — cutting a word would lose a load-bearing claim) | Keep the word. Do not accept the loss |
| Not-bloat problem (bloat mode — defect is duplication across artifacts or drift) | Hand it off; do not mutate the artifact for it |
| Unverified consumer (tidy mode — a consumer was not in the original grep) | Do not delete. Investigate and either preserve the candidate or migrate the consumer first |
| Candidate might be live behavior (tidy mode) | Classify as "not a candidate" and skip. Do not remove to find out |
| Mixed-concern commit (cleanup bundled with behavior change) | Split with `git move --fixup` or `git split` before merging; never merge a mixed commit |
| New abstraction introduced during cleanup | Cleanup must be net-deletion. Separate the abstraction into its own commit with independent justification, or drop it |
| No verifier available | Treat every fix as unverified; state the limitation; do not claim the done predicate holds |
| Nothing to improve | A pass that finds nothing genuine to improve changes nothing |
| Empty change-set (diff mode) | No diff after all resolutions and no user-named files. Stop, report pass-through, make no edits |
| No base ref resolves and committed history exists (diff mode) | Stop and request an explicit base (`deslop against <ref>`). Do not fall back to working-tree-only, which would silently drop committed branch work |
| Finding requires behavior or control-flow judgment (diff mode) | Flag-only, no edit. Never swallow the failure or pretend the done predicate holds |

Partial-result rule: applied fixes that verify stay; any fix whose verification is unconfirmed or failed is reverted and reported as blocked. In tidy mode, a pass that confirms some candidates dead and leaves others unverified lands only the confirmed deletions; unverified candidates stay untouched. Non-mutation rule (tidy mode): nothing is deleted until the dead-confirmation grep covers code, tests, docs, configs, and error messages. Never swallow an error or pretend the done predicate holds.

## Output

A compact report naming the mode, changed files, fixes applied (HIGH only in slop mode), findings left for manual inspection, the verifier command and its result, and any rollback action taken. Bloat mode: the artifact rewritten in place plus a one-line summary of what was cut and which non-bloat problems were handed off. Tidy mode: removed/fixed/skipped counts with one-phrase skip reasons. Diff mode: resolved base ref (or working-tree/root-commit note), changed files cleaned, debris classes removed with file/line, flag-only findings left for manual review, the verifier command and its result, and any rollback action taken. If nothing needed doing: `Deslop: nothing to do.`

