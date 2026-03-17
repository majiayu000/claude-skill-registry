---
name: professional-rust-review
description: Use when reviewing Rust code for craft quality, when writing new Rust code that should follow professional patterns, or when the user asks to judge, audit, or improve Rust code against best practices. Covers type design, function signatures, trait architecture, error handling, visibility, macros, testing, and performance patterns.
---

# Professional Rust Review

Deep code surgery using a field guide extracted from ripgrep (46K LOC), clap (41K LOC), parsel (6K LOC), and ring_api (2.3K LOC). Not design patterns. The actual craft — line-by-line decisions that separate code that rots from code that lives.

## When to Use

- Reviewing Rust code for quality (any crate, any size)
- Writing new Rust types, traits, or modules and want professional patterns
- Auditing a crate for scaling problems before they compound
- Reviewing or designing crate/module organization and structure
- User says "review", "judge", "audit", "improve" about Rust code

## References

| File                                  | Contents                                                                                                                             | When to load                                                           |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| `references/professional-rust.md`     | 47 principles on types, signatures, traits, errors, modules, macros, config, testing, performance, discipline                        | Dispatching a code surgery worker — the worker reads it as rubric      |
| `references/codebase-organization.md` | Module layout, facade pattern, privacy ladder, dependency direction, `std_ext` mirroring, unsafe auditing, encapsulation progression | Dispatching a structural review worker — the worker reads it as rubric |

## How It Works

Two review modes. Pick based on what the user asks for, or run both.

- **Code surgery** — line-level craft quality. Uses `references/professional-rust.md`.
- **Structural review** — module layout, privacy design, dependency flow. Uses `references/codebase-organization.md`.

Delegate an opus-level worker with the relevant guide as rubric. Do NOT summarize the guide in the prompt — the worker reads it directly.

### Step 1: Identify the Target

Determine which Rust files or crates to review. Use `fd -e rs` and `wc -l` to scope the work. Exclude auto-generated files (bindings, protobuf output).

### Step 2: Delegate the crew

Delegate using `teams` with `anthropic/claude-opus-4-6`.

### Step 2a.: Delegate the Surgeon

The worker must:

1. Read `references/professional-rust.md` completely first
2. Read the target code broadly before diving deep
3. Find **specific locations** where applying a principle materially changes the code
4. Show BEFORE and AFTER code for each finding
5. Explain why the change matters HERE, not in general

**Critical instruction quality rules:**

- "Find ALL specific locations" — not "check all 47 principles"
- "Show the exact current code and the exact rewritten code" — not "this pattern is missing"
- "Explain what breaks as the codebase grows without this change" — not "best practice says X"
- "Do NOT produce a checklist. Do NOT say '❌ Missing'."

### Step 2b.: Delegate the Zen Master

The worker must:

1. Read `references/codebase-organization.md` completely first
2. Read the target code broadly before diving deep (not just filenames)
3. Find **specific locations** where applying a principle materially improves the architecture
4. Show BEFORE and AFTER for each finding
5. Explain why the change matters HERE, not in general

**Critical instruction quality rules:**

- "Find ALL specific locations" — not "check all principles"
- "Show the current state VS acceptable end state
- "Explain what breaks as the codebase grows without this change" — not "best practice says X"
- "Do NOT produce a checklist. Do NOT say '❌ Missing'."

### Step 3: Formulate the Dispatch

Dispatch both workers in parallel using a single `teams` call:

```
teams(action: 'delegate', tasks: [
  {
    text: '<surgeon request — see template A below>',
    assignee: 'rust-surgeon',
    model: 'anthropic/claude-opus-4-6'
  },
  {
    text: '<zen-master request — see template B below>',
    assignee: 'rust-zen-master',
    model: 'anthropic/claude-opus-4-6'
  }
])
```

#### Template A: Surgeon

Fill in `{placeholders}`:

```
# Deep Rust Code Surgery

Read the professional Rust field guide at {skill_dir}/references/professional-rust.md completely first. It contains 47 principles with reasoning and failure modes.

## Target
{description of crates/files to review, with paths}
{any files to EXCLUDE like auto-generated bindings}

## Rules
- Do NOT produce a checklist. Do NOT say '❌ Missing'.
- Do NOT list principles that don't apply.
- Every finding must include BEFORE code and AFTER code from the actual codebase.
- The AFTER code must compile (or be obviously close). No pseudocode.
- Focus on changes that affect SCALABILITY — what makes adding the next feature harder or easier.

## What to Find
Find ALL locations where applying a principle would materially change the code. For each:

1. Show the EXACT current code (file path, line range, the actual code)
2. Explain what principle applies and WHY it matters HERE (not in general)
3. Show the REWRITTEN code — the actual diff
4. Explain what breaks or degrades without the change as the codebase grows

## What to Look For
Don't grep for keywords. READ the code and find:

- A function that takes `String` where `&str` or `impl Into<>` would prevent unnecessary allocation
- An enum matched on externally when methods on the enum would centralize logic
- A struct with `pub` fields mutated from 3 modules when encapsulation would help
- A `HashMap<u64, X>` where a newtype key would prevent mixing up ID types
- A `Result<(), String>` that forces callers to parse strings to understand failures
- A function returning `Option<T>` without `#[must_use]` where callers forget to check
- A hot loop calling a cross-crate function without `#[inline]`
- A type constructed once and never mutated with `String` fields that should be `Box<str>`
- An `.unwrap()` that will panic in production under specific conditions
- A 200+ line function that should be 5 methods on a struct

Read broadly first. Then dive deep.

## Output
Write to {output_path}. Structure each finding as:

# Surgery N: [descriptive title]
**File:** path:line_range
**Principle:** §N — [name]
**Why here:** [specific reasoning for THIS code]

### Before
```rust
[actual current code]
```

### After
```rust
[rewritten code]
```

**What this prevents:** [specific scaling problem avoided]

Order by impact (most impactful first). Do NOT create tickets.
```

#### Template B: Zen Master

Fill in `{placeholders}`:

```
# Rust Codebase Structural Review

Read the codebase organization guide at {skill_dir}/references/codebase-organization.md completely first. It contains principles for module layout, privacy, dependency direction, and encapsulation with concrete patterns.

## Target
{description of crates/workspace to review, with paths}
{workspace layout if multi-crate}

## Rules
- Do NOT produce a checklist. Do NOT say '❌ Missing'.
- Do NOT list principles that don't apply.
- Every finding must reference specific files, modules, and dependency paths.
- Proposed restructuring must be concrete — show the directory tree or module moves.
- Focus on what makes the NEXT feature harder to add or the next developer slower to onboard.

## What to Find
Find ALL structural problems in this codebase. For each:

1. Show the CURRENT structure (module tree, file paths, pub/use chains)
2. Explain what organizational principle applies and WHY it matters HERE
3. Show the PROPOSED structure — the actual module moves, visibility changes, or re-exports
4. Explain what breaks or degrades without the change as the codebase grows

## What to Look For
Map the codebase first. THEN find:

- Modules organized by technical role (models/, utils/, helpers/) instead of by feature
- A module re-exporting everything with `pub use` — no facade, just a pass-through
- Cross-module dependency loops (A uses B, B uses A)
- `pub` fields on structs where `pub(crate)` or private + methods would enforce invariants
- A `utils.rs` or `helpers.rs` grab-bag that should be `std_ext/` mirroring std
- Tooling (benchmarks, fuzz targets, CLI tools) living inside the main crate instead of workspace members
- A deeply nested module path that should be facaded at a higher level
- Private items that are `pub` for no reason — check who actually imports them
- An `unsafe` block without a safety comment or justification
- A struct with a reset/clear/serialize method that doesn't destructure (risks missing new fields)

Read the full module tree first. Then dive deep.

## Output
Write to {output_path}. Structure each finding as:

# Finding N: [descriptive title]
**Location:** module path / file paths involved
**Principle:** [name from the guide]
**Why here:** [specific reasoning for THIS codebase]

### Current Structure
[actual module tree, dependency arrows, or visibility chain]

### Proposed Structure
[concrete restructuring — directory moves, visibility changes, new modules]

**What this prevents:** [specific scaling or maintainability problem avoided]

Order by impact (most impactful first). Do NOT create tickets.
```

### Step 4: Present Results

When both workers return, synthesize findings from both into a single report. Summarize the top 5 findings from each worker in a table, then point to the full reports.

If the user wants to act on findings, create tickets for the top-priority items using `tk`.

---

## What the Guides Cover (for reference, do not load into worker prompt)

The 47 principles span 10 areas:

| Part | Principles | Area |
|------|-----------|------|
| I | §1–§7 | Types: newtypes, enums vs bools, hidden inner enums, right-sized types, Box\<str\>, Cow, bytes vs strings |
| II | §8–§13 | Signatures: Into vs AsRef, ?Sized, monomorphization firewall, &mut Self vs self, #[must_use] |
| III | §14–§19 | Traits: minimum surface, iteration style, generics vs trait objects, closure adapters, associated types |
| IV | §20–§25 | Errors: custom vs anyhow, user vs programmer, structured context, mechanical context, bool callbacks |
| V | §26–§29 | Modules: pub(crate), deny(missing_docs), facade crates, types-carry-behavior |
| VI | §30–§32 | Macros: boilerplate only, field-type bounds, dummy impls |
| VII | §33–§35 | Config: private config/public builder/frozen product, two-phase processing, cost-tiered dispatch |
| VIII | §36–§39 | Testing: Result-returning tests, roundtrip testing, behavior not structure, colocated tests |
| IX | §40–§42 | Performance: #[inline], FlatMap, no unnecessary async |
| X | §43–§47 | Discipline: lint config, #[non_exhaustive], documenting omissions, owning critical path, FromStr before serde |

## Common Mistakes

**Checklist mode:** The worker produces a table of "present/absent" for each principle. Useless. The instructions explicitly forbid this — if the worker falls into checklist mode, the dispatch prompt needs sharpening.

**Theoretical findings:** "You could use Cow here." Without showing the current code, the rewrite, and why it matters for THIS codebase, it's noise.

**Too many findings, too shallow:** 15 deep findings beat 47 shallow ones. The worker should read broadly, then pick the 15 highest-impact sites and go deep on each.

**Ignoring auto-generated code:** Always exclude bindings, protobuf output, and other generated files from review scope.
```
