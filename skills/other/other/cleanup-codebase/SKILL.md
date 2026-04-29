---
name: cleanup-codebase
description: Reduce concepts, duplication, and ceremony in internal code while touching nearby code. Use when working an existing path and you spot dead fields, redundant wrappers, or speculative abstractions; distinct from refactor-break-bw-compat (internal hygiene, not public API removal).
---

# Cleanup codebase — local simplicity, ruthlessly applied

Code rots in two directions: outward (drift from the original design) and downward (accretion of dead state, redundant indirection, speculative ceremony). This skill addresses the second. The thesis is local: you are already in nearby code for some other reason; while you are there, remove what does not earn its keep.

**Modern insight (2025)**: Tidy First (Kent Beck) and the dataflow-first design heuristic (Casey Muratori) converge on the same conclusion — small, frequent, atomic cleanups embedded in the active commit stream beat scheduled "cleanup PRs" by a wide margin. Scheduled cleanups bundle unrelated concerns and become unreviewable; embedded cleanups stay reviewable because their scope is the file already in your hands.

See [dead-fields](references/dead-fields.md) for examples of dead struct fields, props, and class members.
See [redundant-wrappers](references/redundant-wrappers.md) for examples of single-line passthrough functions that should be inlined.
See [dead-config](references/dead-config.md) for stale feature flags, environment variables, and dead config branches.

---

## Mandates, not suggestions

These are mandates, not suggestions. Internalize them as rules; do not paraphrase.

### 1. Minimize concepts, duplication, and ceremony.

Every concept the reader has to hold in their head has a cost. Every duplicated piece of logic has two places to drift apart. Every ceremonial wrapper, factory, or builder that does not protect a real boundary is a tax on every future reader. Reducing concepts is not the same as reducing lines — it is reducing the number of distinct things a reader has to track.

### 2. One real owner per contract. No mirroring, no wrappers unless they remove real coupling.

A "contract" is the truth about what some piece of state means or what some operation does. It must have exactly one owner. Mirroring (two structures holding the same field; two services maintaining the same cached state) is a guaranteed-future-bug pattern. Wrappers are coupling-removal tools — if a wrapper just renames or forwards without removing coupling, it is ceremony.

### 3. Local simplicity over speculative abstraction. Add indirection only when it removes real coupling or protects a real boundary.

"Speculative" means "I might need this later." You will not need it later in the form you imagine now, and the indirection you add now will make the actual future change harder. Indirection earns its keep when it removes coupling that *currently* exists, or when it protects a *current* boundary (process, untrusted-input, async/sync seam). Otherwise it is dead-weight ceremony.

### 4. When caller and callee are both local with no real boundary, change both directly.

A "local change" that has to ripple through three wrapper layers is not local — it is coupled. If `caller` and `callee` are both yours, both in the same module, with no API boundary between them, refactoring them in lockstep is correct. Resist the urge to "preserve the interface" of internal functions; an internal function's interface is whoever calls it.

### 5. Remove dead code, fields, config, and stale state while touching nearby code.

Dead code is not free. It misleads readers about what the system does, it survives grep searches and pulls attention, it tricks reviewers into preserving it "just in case." While you are in nearby code for some other reason, remove what is dead. Make the deletion its own atomic commit so reviewers see exactly what disappeared.

---

## What "real boundary" means

Indirection earns its keep at: **public API surfaces**, **process/network seams** (RPC, HTTP, queues), **untrusted-input boundaries**, **async/sync seams**, **runtime seams** (FFI, WASM, JNI), and **test/production seams** where mocks legitimately substitute. A swappable-implementation contract counts only when >1 real impl ships today — not "might exist later."

Not boundaries: internal modules in the same crate/package, helpers in the same file, cross-module calls without a constraint that prevents co-change.

---

## When to Apply

- You are editing `foo.py` for an unrelated feature; while reading the file, you notice a dead field
- A refactor commit just ripped out a code path; the leftover wrapper, dead branch, or stale flag should leave with it
- Reviewing a PR diff that adds an unnecessary wrapper or duplicates state; flag and request inline simplification
- Onboarding to a codebase — surface candidates for the original author to confirm dead

## When NOT to Apply

- **Standalone "cleanup sweep" PRs** — these mix unrelated changes, become unreviewable, and conflict with the `<git>` charter's "one concern per commit" rule. Solution: `git move --fixup` to embed the cleanup as an atomic commit alongside the active change.
- **Files you are not otherwise touching** — opportunistic edits become unreviewable noise; the cleanup must ride alongside work that justifies you being in that file.
- **Speculative removals you cannot prove are safe** — if you cannot grep-confirm that nothing reads a field, do not delete it; investigate first.
- **Public API surfaces** — that is `refactor-break-bw-compat`'s territory and needs a migration plan.

---

## Decision rubric

| Pattern | Action | Notes |
|---------|--------|-------|
| Wrapper that adds nothing but a rename | Inline, then delete the wrapper | Renames are not abstractions |
| Field set in constructor, never read after | Delete the field and its assignment | Grep all consumers first |
| Config flag where both branches are dead (always-on or always-off) | Delete the flag, keep the winning path | Often legacy migration debt |
| Adapter between two structurally equivalent local types | Collapse to one type | Different names ≠ different concepts |
| Helper used in 3+ places that genuinely names a shared concept | Keep | Real reuse, real naming |
| Helper used in 1 place that wraps a 2-line body | Inline | The wrapper is overhead |
| State mirrored across two services / two structs | Pick one owner; the other reads from it | Mirroring is the bug |
| Comment that contradicts the code | Update or delete the comment | Stale comments mislead |
| `TODO` from > 6 months ago | Open issue or delete | Indefinite TODOs are noise |

---

## Workflow

1. **Identify candidate** — while in the file for another reason, spot dead/redundant code.
2. **Confirm dead** — `git --no-pager grep -n` (or `ast-grep`) to verify no consumers; check tests, docs, configs, error messages.
3. **Check coupling effects** — does removal break the build? Force a refactor of the only consumer? That is a separate decision; record it.
4. **Verify against `~/.claude/claude/system-prompt-baseline.md` `<git>` charter** — cleanup is its own atomic commit. If it is mixed in with behavior change, split via `git move --fixup` / `git split`.
5. **Apply the deletion** — `git rip` the file or precise `Edit` for partial removal; never comment-out.
6. **Verify** — build, tests, type-check still pass. If a test was the only consumer of the dead code, that test was probably testing the dead code; see `tests-purge-unneeded`.
7. **Search for ghosts** — string references in docs, error messages, config keys, env vars, log lines that mention the removed concept.

---

## Constitutional Rules (Non-Negotiable)

1. **Never bundle cleanup with behavior change in one commit** — split via `git move --fixup` so each commit has exactly one concern. Cleanup commits ride alongside behavior commits in the same PR; that is fine and encouraged.
2. **Never add an abstraction during cleanup** — cleanup removes; if a new abstraction is genuinely warranted, that is a *separate* commit with its own justification.
3. **Never extend cleanup beyond files already touched by the active change** — opportunistic sweeps across the codebase are out of scope; they belong in scheduled refactor work that has its own plan.
4. **If conflict with `~/.claude/claude/system-prompt-baseline.md`, system-prompt-baseline.md wins** — this skill complies with the user's git charter and tidy-first principles; if drift is detected, system-prompt-baseline.md is the source of truth.

## Validation Gates

| Gate | Pass Criteria | Blocking |
|------|---------------|----------|
| Atomic commit | Cleanup is its own commit, separate from behavior change | Yes |
| Dead confirmation | `grep`/`ast-grep` confirms no consumers in code, tests, docs, configs | Yes |
| No new abstractions | Diff is net-deletion (or inline-and-delete) only | Yes |
| Build + tests pass | Repo-native verification on every touched language | Yes |
| Ghost search | No leftover references in docs, error messages, env vars | Yes |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Clean — atomic deletion landed, all consumers updated, build green |
| 11 | Consumer found that was not in the original grep — investigate and either preserve or migrate |
| 12 | Build / test regression — rollback required |
| 13 | Mixed-concern commit — must split via `git move --fixup` before merging |
| 14 | New abstraction introduced — separate the commit, justify the abstraction independently |
| 15 | Ghost references found — cleanup incomplete |

---

## See also

- `tests-purge-unneeded` — sibling deletion discipline for test code; the same thesis (delete what does not earn its keep), applied to the test suite
- `refactor-break-bw-compat` — when the deletion crosses a public-API boundary; that skill handles migration plans, blast-radius mapping, and consumer coordination
- `~/.claude/claude/system-prompt-baseline.md` `<git>` charter — atomic-commit and one-concern-per-commit rules this skill enforces
