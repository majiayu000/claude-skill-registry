---
name: doc-rigor-verify
description: Write-then-verify documentation pipeline — a doc-rigor agent writes/improves docs, then a separate fresh doc-verify agent checks accuracy against code reality with zero confirmation bias
---

# Doc Rigor Verify

An end-to-end documentation pipeline that composes `/doc-rigor` (write) and
`/doc-verify` (verify) into a single invocation with enforced agent isolation.
The writer and verifier never share context — the verifier only sees the code
and whatever the writer produced, not what the writer intended.

## When to Use

- After writing or modifying code that needs documentation
- When you want both doc generation and accuracy checking in one pass
- As a replacement for manually running `/doc-rigor` then `/doc-verify`
- Before merging branches that touch public APIs or complex internals

## When NOT to Use

- **Only writing docs** (no verification needed) — use `/doc-rigor` directly
- **Only verifying existing docs** (no writing needed) — use `/doc-verify` directly
- **Reviewing code logic** — use `/review-dispatch`
- **Verifying dist-sys claims** — use `/dist-sys-auditor`

---

## Invocation

```
/doc-rigor-verify [files]
```

- With no argument: targets recently changed files (unstaged + staged)
- With file paths: targets those specific files
- With a directory: targets all `.rs` files in that directory

### Flags

| Flag | Effect |
|------|--------|
| `--code-only` | Passed to the verify phase: skip external claim verification |
| `--strict` | Passed to the verify phase: promote all WARNs to BLOCKs |
| `--summary` | Passed to the verify phase: output only the summary table |
| `--rigor-only` | Run only the doc-rigor phase (equivalent to `/doc-rigor`) |
| `--verify-only` | Run only the doc-verify phase (equivalent to `/doc-verify`) |

---

## Agent Isolation — Non-Negotiable

This skill enforces a hard separation between writing and verifying:

```
Invoking Agent (orchestrator)
    │
    ├──▶ Agent 1: Doc-Rigor Writer   (writes/improves docs)
    │         ↓
    │    [docs are written to files]
    │
    └──▶ Agent 2: Doc-Verify Checker  (verifies docs against code)
              ↓
         [verification report]
```

- **Agent 1** (doc-rigor) runs as a `general-purpose` subagent with full edit
  access. It reads the code, understands intent, and writes documentation.
- **Agent 2** (doc-verify) runs as a **separate** `general-purpose` subagent
  with **zero knowledge** of what Agent 1 intended. It receives only the
  file contents (code + docs as they exist on disk after Agent 1's edits)
  and verifies every claim against code reality.

**Why**: The verifier must not know what the writer *meant* to say — only what
they *did* say. This eliminates confirmation bias. A writer who knows they
intended "returns None on empty" won't catch that the code actually panics.
A fresh verifier will.

**Never** inline both phases in the same agent context. **Always** use two
separate Task agents.

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
- Read adjacent module files (siblings in the same directory) for context

### 3. Parse Flags

Extract any flags from the invocation and route them to the appropriate phase.

### 4. Check for References

If the project has `references/documentation-style.md`, read it — it will be
passed to the doc-rigor agent as a style reference.

---

## Phase 2: Doc-Rigor Agent (Writer)

Launch **1 agent** using the Task tool with `subagent_type="general-purpose"`.

### Writer Agent Prompt

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
   - Type/function docs: guarantees, preconditions, side effects, errors, complexity.
   - Inline comments only for local, tricky reasoning (why now, why this order,
     why this bound).

4. **Enforce rigor**:
   - Remove comments that restate code or obvious control flow.
   - Check for consistency with code and tests.
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

- Use `///` for item docs and `//!` for module docs
- For unsafe code, add a `# Safety` section describing required invariants
- Include `# Examples` sections in public APIs if usage is non-obvious

### Rules

- Edit the target files directly using the Edit tool
- Do NOT edit adjacent context files
- Do NOT add tracking IDs, issue references, or external tracker info in comments
- Do NOT add version suffixes, deprecated annotations, or compatibility shims
- Focus on WHY, not WHAT — don't restate what the code already says
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

## Phase 3: Doc-Verify Agent (Verifier)

Launch **1 agent** using the Task tool with `subagent_type="general-purpose"`.
This agent receives **only** the current file contents (post-edit) and
verification instructions. It has zero context about what the writer intended.

### Verifier Agent Prompt

```
You are a documentation verification specialist. Your job is to verify that
every claim in the documentation is factually correct against what the code
actually does and what external sources actually say. You have ZERO knowledge
of the author's intent — you can only check what is written against what the
code does. Trust nothing, verify everything.

## Target Files (verify docs in these)

{UPDATED_FULL_FILE_CONTENTS}

## Adjacent Context (for cross-reference only)

{ADJACENT_FILE_CONTENTS}

{FLAGS — e.g., --code-only, --strict, --summary}

## Step A: Extract All Testable Claims

Read every doc comment in the target files. Extract every testable claim —
any statement that can be verified as true or false against the code or an
external source.

Categorize each claim:

| Category | What to look for |
|----------|------------------|
| **Behavioral** | "this function returns X when Y", "panics if Z", "calls W internally" |
| **Invariant** | "this value is always positive", "the list is sorted", "monotonically increasing" |
| **Type/Structural** | "contains N fields", "implements trait T", "generic over X" |
| **Count** | "there are N variants", "supports M strategies", "N phases" |
| **Relationship** | "A calls B", "X depends on Y", "Z wraps W" |
| **Precondition/Postcondition** | "caller must ensure X", "on return, Y holds" |
| **Complexity** | "O(n log n)", "amortized O(1)", "linear in the number of X" |
| **Performance** | "zero-copy", "no allocation", "lock-free", "wait-free" |
| **Safety** | "safe because X", "unsafe requires Y", "SAFETY: Z" |
| **External** | "uses algorithm from [paper]", "follows RFC N", "compatible with library X" |
| **Negative** | "does NOT do X", "never Y", "no Z" |

For each claim, record:
- Location: file:line
- Category: from the table above
- Claim text: the exact statement (quoted)
- Testable assertion: rewrite as a concrete true/false statement

## Step B: Verify Code-Level Claims

For each claim category, verify against the actual code:

**Behavioral**: Trace the code path. Does the function actually return X when Y?
Does it actually panic if Z? Read the implementation, not just the signature.

**Invariant**: Check constructors, mutation methods, and all code paths that
touch the value. Is the invariant enforced everywhere, or only in some paths?

**Type/Structural**: Count the actual fields, variants, or implementations.
Open the struct/enum definition and count.

**Count**: Count the actual items. Off-by-one counts are a WARN, off-by-more
is a BLOCK.

**Relationship**: Verify call graphs. Does A actually call B? Check imports
and usage.

**Precondition/Postcondition**: Check if the precondition is enforced
(assert/debug_assert) or just documented. Check if the postcondition actually
holds by reading the return paths.

**Complexity**: Verify the algorithm matches the claimed complexity. Count
nested loops, check data structure operations.

**Performance**: "Zero-copy" — check for .clone(), .to_vec(), .to_string().
"No allocation" — check for Vec::new(), Box::new(), String::from().
"Lock-free" — check for Mutex, RwLock.

**Safety**: For unsafe blocks, verify the stated safety justification actually
holds.

**Negative**: "Never panics" — check for .unwrap(), .expect(), indexing.
"No allocation" — check for heap allocations. Verify the absence of what
the doc says is absent.

## Step C: Identify External Claims

Extract all references to named algorithms, academic papers, libraries,
standards/RFCs, cryptographic properties, or complexity claims from literature.

## Step D: Verify External Claims

(Skip this step if --code-only flag is active.)

For claims requiring verification, use WebFetch to find authoritative sources.
Record results as: Confirmed, Contradicted (BLOCK), Unverifiable (WARN),
or Partially correct (WARN).

## Step E: Produce Findings

### Severity Classification

**BLOCK — Must Fix**:
- Factually wrong claim (code does X, doc says Y)
- Incorrect safety comment
- False external claim
- Count wrong by more than 1
- Behavioral claim opposite of reality

**WARN — Should Fix**:
- Misleading claim (technically true but creates false impression)
- Stale count (off by 1)
- Stale structural claim
- Unverifiable external claim
- Ambiguous invariant claim
- Precondition documented but not enforced

**INFO — Consider Fixing**:
- Imprecise language
- Slightly stale wording
- Missing doc where one would help

(If --strict flag is active, promote all WARNs to BLOCKs.)

### Output Format

Return this structured report:

# Documentation Verification Report

## Summary

| Metric | Count |
|--------|-------|
| Files verified | N |
| Claims extracted | N |
| Verified correct | N |
| BLOCK | N |
| WARN | N |
| INFO | N |

**Verdict**: PASS / PASS WITH WARNINGS / FAIL

(FAIL if any BLOCKs exist.)

## Findings

| # | Severity | File:Line | Category | Claim | Verdict | Evidence |
|---|----------|-----------|----------|-------|---------|----------|

## Detailed Findings

### BLOCK-N: [title]
- Location: file:line
- Claim: "[quoted]"
- Reality: [what the code actually does]
- Evidence: [specific code reference]
- Suggested fix: [concrete wording correction]

### WARN-N: [title]
(same format)

## External Claims Verification

| # | Claim | Source Checked | Result | Notes |
|---|-------|---------------|--------|-------|

## Verification Coverage

| File | Claims Found | Verified | BLOCK | WARN | INFO |
|------|-------------|----------|-------|------|------|
```

---

## Phase 4: Presentation (Invoking Agent)

After both agents complete, present a combined report to the user:

### 1. Writer Summary

Briefly state what the doc-rigor agent did:
- Which files were edited
- What types of documentation were added or improved
- Any gaps the writer noted

### 2. Verification Report

Present the doc-verify agent's findings directly. Do not filter or soften them.

- **If verdict is FAIL**: Highlight all BLOCKs at the top. Emphasize that the
  documentation edits contain factual errors that must be corrected.
- **If verdict is PASS WITH WARNINGS**: Note warnings that should be addressed.
- **If verdict is PASS**: Confirm that all documentation claims verified against
  code reality.

### 3. Next Steps

Based on the verification result:

- **FAIL**: Suggest running `/execute-review-findings` to fix BLOCKs, then
  re-running `/doc-verify` to confirm fixes.
- **PASS WITH WARNINGS**: List the WARNs as follow-up items.
- **PASS**: Documentation is ready.

---

## Common Drift Caught by This Pipeline

The write-then-verify pattern is especially good at catching:

- **Writer assumed intent, not reality**: The writer reads a function named
  `try_get` and documents "returns None on failure" — but the code actually
  panics. The verifier catches this because it traces the actual code path.
- **Stale counts**: The writer copies a count from module docs without
  recounting. The verifier counts the actual items.
- **Overstated guarantees**: The writer documents "lock-free" based on the
  design intent, but the implementation uses a Mutex. The verifier checks
  for actual lock usage.
- **Safety invariant gaps**: The writer documents a safety contract, but the
  verifier finds code paths that violate it.

---

## Related Skills

- `/doc-rigor` — the writing half of this pipeline, used standalone
- `/doc-verify` — the verification half of this pipeline, used standalone
- `/execute-review-findings` — implements fixes for BLOCK findings
- `/review-dispatch` — multi-lens code review (broader than docs)
- `/dist-sys-auditor` — specialized for distributed systems claims
