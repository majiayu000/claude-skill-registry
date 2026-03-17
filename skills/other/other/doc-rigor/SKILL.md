---
name: doc-rigor
description: Write-then-verify documentation pipeline. Use when a user asks to
  improve comments or docs, explain algorithms or design choices, write or upgrade
  docstrings, or raise documentation quality for a codebase (especially Rust crates).
  Writes docs, then automatically verifies every claim against code reality using
  a fresh agent to eliminate confirmation bias.
user-invocable: true
---

# Doc Rigor

## Overview

Produce documentation that lets a new reader grok the code without reading every
line, then verify every claim against code reality with a fresh agent. Treat
comments as first-class: explain intent, invariants, and trade-offs, not syntax.
The writer and verifier never share context — the verifier only sees the code and
whatever the writer produced, not what the writer intended.

## When to Use

- After writing or modifying code that needs documentation
- To improve comments, docstrings, or module-level docs
- To explain algorithms, design choices, or non-obvious reasoning
- Before merging branches that touch public APIs or complex internals

## When NOT to Use

- **Reviewing code logic** — use `/review-dispatch`
- **Verifying dist-sys claims** — use `/dist-sys-auditor`
- **Checking API ergonomics** — use `/interface-design-review`
- **Only verifying existing docs** (no writing) — use `/doc-verify` directly

---

## Invocation

```
/doc-rigor [files]
```

- With no argument: target recently changed files (unstaged + staged)
- With file paths: target those specific files
- With a directory: target all `.rs` files in that directory

### Flags

| Flag | Effect |
|------|--------|
| `--skip-verify` | Skip verification phase (write only, no agent 2) |
| `--code-only` | Passed to verify phase: skip external claim verification |
| `--strict` | Passed to verify phase: promote all WARNs to BLOCKs |
| `--summary` | Passed to verify phase: output only the summary table |

---

## Phase 1: Scope Resolution (Invoking Agent)

The invoking agent performs these steps before launching subagents:

### 1. Identify Target Files

- If files are specified: use those
- If no argument: run `git diff --name-only HEAD` and `git diff --cached --name-only`
  to find recently changed `.rs` files
- Filter to `.rs` files only

### 2. Read File Contents

- Read each target file in full
- Read adjacent module files (siblings in the same directory) for context —
  the writer needs surrounding types, traits, and functions

### 3. Parse Flags

Extract any flags from the invocation. Route `--skip-verify`, `--code-only`,
`--strict`, and `--summary` to the appropriate phase.

### 4. Check for References

If the project has `references/documentation-style.md`, read it — it will be
passed to the doc-writing agent as a style reference.

---

## Phase 2: Doc Writing (Agent 1 — general-purpose subagent)

Launch **1 agent** using the Task tool with `subagent_type="general-purpose"`.

### Writer Agent Prompt

Include in the prompt:
- Full contents of every target file
- Full contents of adjacent module files (marked as context, not to be edited)
- Style reference (if `references/documentation-style.md` exists)
- The complete writer instructions below

### Writer Instructions

```
You are a documentation specialist. Your job is to write and improve
documentation for Rust code following the doc-rigor methodology.

## Target Files

{FULL_FILE_CONTENTS}

## Adjacent Context (for reference, do NOT edit these)

{ADJACENT_FILE_CONTENTS}

{STYLE_REFERENCE — include only if references/documentation-style.md exists}

## Your Task

Produce documentation that lets a new reader grok the code without reading
every line. Treat comments as first-class: explain intent, invariants, and
trade-offs, not syntax.

### Workflow

1. **Read for intent** — Identify the core problem, invariants, and boundaries
   of each module/type/function. Mark non-obvious logic, algorithms, and design
   decisions that need explanation.

2. **Draft a documentation map** — Decide which scopes need docs: module-level,
   type-level, function-level, or inline. Prefer fewer, richer comments over
   many shallow ones.

3. **Write documentation in layers**:
   - Module-level docs: purpose, invariants, high-level algorithm, references.
   - Type/function docs: guarantees, preconditions, side effects, errors,
     complexity.
   - Inline comments only for local, tricky reasoning (why now, why this order,
     why this bound).

4. **Enforce rigor**:
   - Remove comments that restate code or obvious control flow.
   - Check for consistency with code and tests; update docs when behavior
     changes.
   - Call out any missing context you cannot infer.

### Comment Content Checklist

Every doc you write should cover the applicable items:

- Problem statement and scope
- Invariants and safety/soundness rules
- Algorithm overview with key steps and why they matter
- Design trade-offs (why this approach vs alternatives)
- Edge cases and failure modes
- Complexity or performance constraints when relevant
- Concrete examples when behavior is subtle

### Rust-Specific Guidance

- Use `//!` for module-level docs, `///` for items, `//` for inline reasoning
- For unsafe code, add a `# Safety` section describing required invariants
- Include `# Examples` in public APIs if usage is non-obvious

### Rules

- Edit the target files directly using the Edit tool
- Do NOT edit adjacent context files
- Do NOT add tracking IDs, issue references, or external tracker info in comments
- Do NOT add version suffixes, deprecated annotations, or compatibility shims
- Focus on WHY, not WHAT — do not restate what the code already says
- Be factually precise — every claim in a doc comment must be true

### Output

After editing all files, provide a summary listing:
- Files edited
- Types of docs added/improved (module, type, function, inline)
- Any gaps you could not fill due to missing context
```

### Collecting Writer Results

When the writer agent completes:

1. Capture its summary (files edited, docs added, gaps noted)
2. **Re-read the target files from disk** — the writer has edited them, and the
   verifier needs the updated contents, not the pre-edit versions
3. Also re-read adjacent module files (they were not edited but provide context
   for verification)

---

## Phase 3: Doc Verification (Agent 2 — fresh general-purpose subagent)

**Skip this entire phase if `--skip-verify` flag is active.**

### Agent Isolation — Non-Negotiable

```
Invoking Agent (orchestrator)
    |
    +-->  Agent 1: Doc-Rigor Writer   (writes/improves docs)
    |         |
    |    [docs are written to files]
    |
    +-->  Agent 2: Doc-Verify Checker  (verifies docs against code)
              |
         [verification report]
```

- **Agent 2** runs as a **separate** `general-purpose` subagent with **zero
  knowledge** of what Agent 1 intended. It receives only the current file
  contents (code + docs as they exist on disk after Agent 1's edits) and
  verifies every claim against code reality.
- **Why**: The verifier must not know what the writer *meant* to say — only what
  they *did* say. This eliminates confirmation bias. A writer who knows they
  intended "returns None on empty" will not catch that the code actually panics.
  A fresh verifier will.
- **Never** inline both phases in the same agent context. **Always** use two
  separate Task agents.

### Verification Agent Prompt

Include in the prompt:
- Full contents of every target file (post-edit, re-read from disk)
- Full contents of adjacent module files
- Active flags (`--code-only`, `--strict`, `--summary`)
- The complete verification instructions from `references/verification-methodology.md`

The verification agent follows Steps A through E from the methodology reference:

1. **Extract all testable claims** from doc comments, categorized across 11
   claim types (Behavioral, Invariant, Type/Structural, Count, Relationship,
   Precondition/Postcondition, Complexity, Performance, Safety, External,
   Negative)
2. **Verify code-level claims** by tracing actual code paths, counting real
   fields/variants, checking call graphs, and validating safety invariants
3. **Identify external claims** referencing algorithms, papers, libraries,
   standards, or cryptographic properties
4. **Verify external claims** against authoritative sources (unless `--code-only`)
5. **Produce findings** with severity classification and structured report

See `references/verification-methodology.md` for the complete procedure,
category definitions, verification steps per category, and output format template.

### Severity Tiers

- **BLOCK**: Factually wrong, incorrect safety comment, false external claim,
  count off by more than 1, behavioral claim opposite of reality
- **WARN**: Misleading, stale count (off by 1), stale structural claim,
  unverifiable external, ambiguous invariant, unenforced precondition
- **INFO**: Imprecise language, slightly stale wording, missing doc

### Verdict

- **FAIL**: Any BLOCKs exist
- **PASS WITH WARNINGS**: WARNs but no BLOCKs
- **PASS**: All claims verified correct

---

## Phase 4: Presentation (Invoking Agent)

After both agents complete, present a combined report to the user.

### 1. Writer Summary

Briefly state what the doc-rigor agent did:
- Which files were edited
- What types of documentation were added or improved
- Any gaps the writer noted

### 2. Verification Report

Present the verification agent's findings directly. Do not filter or soften them.

- **If verdict is FAIL**: Highlight all BLOCKs at the top. Emphasize that the
  documentation edits contain factual errors that must be corrected.
- **If verdict is PASS WITH WARNINGS**: Note warnings that should be addressed.
- **If verdict is PASS**: Confirm that all documentation claims verified against
  code reality.

If `--skip-verify` was active, note that verification was skipped and recommend
running `/doc-verify` separately.

### 3. Next Steps

Based on the verification result:

- **FAIL**: Suggest running `/execute-review-findings` to fix BLOCKs, then
  re-running `/doc-verify` to confirm fixes.
- **PASS WITH WARNINGS**: List the WARNs as follow-up items.
- **PASS**: Documentation is ready.

---

## Use References

- Read `references/documentation-style.md` for documentation patterns and
  templates when the user wants high-rigor style or asks to mirror a
  well-documented crate.
- Read `references/verification-methodology.md` for the complete verification
  procedure including claim categories, per-category verification steps, severity
  definitions, and output format template.

---

## Related Skills

- `/doc-verify` — standalone verification against code reality. Use when docs
  already exist and only need accuracy checking (no writing phase).
- `/execute-review-findings` — implements fixes for BLOCK findings from
  verification reports.
- `/review-dispatch` — multi-lens code review (broader than docs).
- `/dist-sys-auditor` — specialized for distributed systems claims with
  citations.
