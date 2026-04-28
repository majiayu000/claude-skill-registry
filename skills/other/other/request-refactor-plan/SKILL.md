---
name: request-refactor-plan
description: Plan a refactor as a sequence of tiny, working commits via adversarial interview. Default output is a markdown plan at `<project-root>/docs/refactor-plans/<name>.md`; pass `--emit-issue` to additionally file a GitHub issue. Trigger when user proposes a structural refactor (rename, extract, move, split, deduplicate) — NOT for new features.
---

Adversarial interview to break a refactor into the smallest commits that each leave the codebase green.

## Scope fence

Refactor-plan is **structural-only and scope-narrow**: rename, extract, move, split, merge, dedupe, type-tighten, dependency invert. No behavior change. No new features. No bug fixes bundled in.

For general feature work or behavior change, use general implementation planning. For executing a refactor that intentionally breaks compat, use the break-compat refactor workflow.

## Output

**Default:** write plan to `<project-root>/docs/refactor-plans/<kebab-name>.md`.

**Optional `--emit-issue`:** after writing the file, also file a GitHub issue with `gh issue create --body-file <path>`.

## Interview protocol (linear)

1. Solicit a long description of the perceived problem and any sketched solutions. Do not act yet.
2. Dispatch Explore agent to verify the user's claims against the actual code; produce a structural map of the affected surface.
3. Confront with alternatives. List 2-3 options with concrete trade-offs and a recommendation.
4. Pin scope explicitly. Enumerate what changes AND what stays untouched.
5. Audit test coverage of the affected surface. Use `git grep -l` for callsite-adjacent assertions, plus extension-and-glob test discovery: `fd -g '*.test.ts' -g '*.spec.ts'` (Node), `fd -g '*_test.go'` (Go), `fd -g 'test_*.py' -g '*_test.py'` (Python), `fd -g '*_test.rs'` plus `git grep -n '#\[test\]'` (Rust), `fd -g 'test_*.ml' -g '*_test.ml'` (OCaml).
6. Decompose into the smallest commits where each leaves the tree green. Fowler's rule: "make each refactoring step as small as possible."
7. Write the plan file using the template below.
8. If `--emit-issue` was passed, mirror to GitHub.

## Plan file template

```
# Refactor: <name>

## Problem
<developer's framing of the pain>

## Solution
<chosen approach in one paragraph>

## Commits
<numbered list; each commit is one concern; each leaves the tree green; plain English, no file paths>

## Decisions
- modules touched
- interfaces modified
- schema/API contract changes
- explicit non-decisions

## Testing
- what counts as a good test (external behavior, not internals)
- modules under test
- prior-art tests in the repo

## Out of scope
<explicit non-goals>
```

Avoid file paths and code snippets in the plan; both go stale within hours.

## Parallel examples

**TypeScript (Nest module split):** "Extract `BillingModule` from `AppModule`" decomposes into: (1) move providers, (2) re-export public types, (3) update import sites in batches of 5, (4) delete dead re-exports. Each commit passes `pnpm typecheck && pnpm test`.

**Rust (crate carve-out):** "Split `parser` from `core` crate" decomposes into: (1) add new `parser` crate skeleton, (2) move types with `pub use` shim, (3) move impls behind shim, (4) flip downstream `use` paths, (5) delete shim. Each commit passes `cargo check --workspace && cargo test`.
