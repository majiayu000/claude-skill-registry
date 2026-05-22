---
name: doc-verify
description: Verify documentation accuracy against code reality and external claims — runs as a fresh agent after /doc-rigor to prevent confirmation bias
---

# Doc Verify

Verify that documentation is factually correct against what the code actually does
and what external sources actually say. The verifier has **zero knowledge of author
intent** — every claim is checked against code reality and external sources. Trust
nothing, verify everything.

## When to Use

- After `/doc-rigor` generates or updates documentation
- After manual doc edits to confirm accuracy
- Periodic audits of critical module documentation
- Before publishing API docs externally
- When refactoring changes code that existing docs describe

## When NOT to Use

- **Writing docs** — that's `/doc-rigor`
- **Reviewing code logic** — that's `/review-dispatch`
- **Verifying dist-sys claims** — that's `/dist-sys-auditor`
- **Checking API ergonomics** — that's `/interface-design-review`

---

## Invocation

```
/doc-verify [files]
```

- With no argument: verify docs in recently changed files (unstaged + staged)
- With file paths: verify those specific files
- With a directory: verify all `.rs` files in that directory

---

## Fresh Agent Requirement

**CRITICAL: Non-negotiable.** Every verification runs inside a fresh `Task` agent
with `subagent_type="general-purpose"`. The invoking agent resolves scope and
dispatches; the fresh agent performs all verification.

**Why**: The invoking agent may have written or reviewed the documentation. A fresh
agent has zero prior context about what the documentation *should* say — it can only
check what it *does* say against what the code *does* do. This eliminates confirmation
bias.

**Never** run verification inline. **Always** dispatch to a fresh agent.

---

## Phase 1: Scope Resolution (Invoking Agent)

The invoking agent performs these steps before dispatching the verification agent:

### 1. Identify Target Files

- If files are specified: use those
- If no argument: run `git diff --name-only HEAD` and `git diff --cached --name-only`
  to find recently changed `.rs` files
- Filter to files that contain doc comments. Use the Grep tool (NOT bash grep) with
    pattern: ^(///|//!) to find files with doc comments. Do NOT pass these patterns
    through Bash — use the Grep tool directly.

### 2. Read File Contents

- Read each target file in full
- Read adjacent module files (siblings in the same directory) for context —
  the verifier needs to see the types, traits, and functions that docs reference

### 3. Check for Configuration Flags

Parse any flags from the invocation:

| Flag | Effect |
|------|--------|
| `--code-only` | Skip external claim verification (Step D) |
| `--external-only` | Skip code-level verification (Step B), only check external claims |
| `--strict` | Promote all WARNs to BLOCKs |
| `--summary` | Output only the summary table, suppress detailed write-ups |

### 4. Dispatch Verification Agent

Launch a `Task` agent with `subagent_type="general-purpose"`. The prompt must include:

- The full contents of every target file
- The full contents of adjacent module files (for cross-reference)
- Any active configuration flags
- The complete Phase 2 instructions below (copy them verbatim into the prompt)

---

## Phase 2: Verification (Fresh Agent)

These instructions are sent to the fresh verification agent.

### Step A: Extract All Testable Claims

Read every doc comment in the target files. Extract every **testable claim** —
any statement that can be verified as true or false against the code or an external
source.

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
- **Location**: file:line
- **Category**: from the table above
- **Claim text**: the exact statement (quoted)
- **Testable assertion**: rewrite as a concrete true/false statement

### Step B: Verify Code-Level Claims

For each claim category, verify against the actual code:

**Behavioral**: Trace the code path. Does the function actually return X when Y?
Does it actually panic if Z? Read the implementation, not just the signature.

**Invariant**: Check constructors, mutation methods, and all code paths that touch
the value. Is the invariant enforced everywhere, or only in some paths?

**Type/Structural**: Count the actual fields, variants, or implementations. Open the
struct/enum definition and count. Check `impl` blocks for trait implementations.

**Count**: Count the actual items. If the doc says "5 variants", count the variants.
If it says "3 phases", trace the phases. Off-by-one counts are a WARN.

**Relationship**: Verify call graphs. Does A actually call B? Use Grep to check.
Does X actually depend on Y? Check imports and usage.

**Precondition/Postcondition**: Check if the precondition is enforced (assert/debug_assert)
or just documented. Check if the postcondition actually holds by reading the return paths.

**Complexity**: Verify the algorithm matches the claimed complexity. Count nested loops,
check data structure operations. A HashMap lookup claimed as O(1) is fine; a Vec scan
claimed as O(1) is a BLOCK.

**Performance**: "Zero-copy" — check for `.clone()`, `.to_vec()`, `.to_string()` in the
path. "No allocation" — check for `Vec::new()`, `Box::new()`, `String::from()`, etc.
"Lock-free" — check for Mutex, RwLock, or any blocking operations.

**Safety**: For `unsafe` blocks, verify the stated safety justification. Does the code
actually uphold the invariants claimed in the `// SAFETY:` comment?

**Negative**: These are often the most important claims. "Never panics" — check for
`.unwrap()`, `.expect()`, indexing, division. "No allocation" — check for heap
allocations. Verify the absence of what the doc says is absent.

### Step C: Identify External Claims

Extract all references to:

- Named algorithms (e.g., "SipHash", "FNV", "xxHash", "AES-GCM")
- Academic papers (e.g., "Lamport 1978", "Raft consensus")
- Libraries or external tools (e.g., "compatible with serde", "follows tokio conventions")
- Standards or RFCs (e.g., "RFC 7519", "OWASP", "NIST SP 800-132")
- Cryptographic properties (e.g., "collision-resistant", "constant-time")
- Complexity claims from literature (e.g., "O(1) amortized per Tarjan 1975")

### Step D: Verify External Claims

For each external claim, determine if web verification is needed:

**Always verify**:
- Cryptographic property claims (collision resistance, constant-time, key sizes)
- Library behavior claims ("serde does X", "tokio guarantees Y")
- Paper/algorithm attribution ("algorithm X from paper Y")
- Standard compliance claims ("follows RFC N section M")

**Skip web research for**:
- Claims that are purely code-verifiable (covered in Step B)
- Well-known facts that don't need a source (e.g., "HashMap is O(1) average")

For claims requiring verification, use `WebFetch` or `WebSearch` to find
authoritative sources:
- Official library documentation
- RFC text
- Paper abstracts or summaries
- NIST/OWASP published standards

Record the verification result:
- **Confirmed**: source agrees with claim
- **Contradicted**: source disagrees — this is a BLOCK
- **Unverifiable**: no authoritative source found — this is a WARN
- **Partially correct**: source agrees with part of claim — this is a WARN

### Step E: Produce Findings

Assemble the complete findings report using the output format below.

---

## Phase 3: Presentation (Invoking Agent)

When the verification agent returns:

1. Present the findings directly to the user
2. Highlight all BLOCKs prominently at the top
3. If verdict is FAIL, emphasize that documentation must be corrected before
   it can be considered accurate
4. If any external claims were contradicted, include the authoritative source

---

## Severity Classification

Three-tier system matching `/dist-sys-auditor`:

### BLOCK — Must Fix

- Factually wrong claim (code does X, doc says Y)
- Incorrect safety comment (unsafe justification doesn't hold)
- False external claim (doc cites wrong paper, wrong algorithm name, wrong RFC)
- Count that is wrong by more than 1 (doc says 5 fields, struct has 3)
- Behavioral claim that is the opposite of reality

### WARN — Should Fix

- Misleading claim (technically true but creates false impression)
- Stale count (off by 1 — e.g., doc says 5 variants, enum has 6)
- Stale structural claim (field renamed, type changed, but doc not updated)
- Unverifiable external claim (no authoritative source found)
- Ambiguous invariant claim (could be read multiple ways)
- Precondition documented but not enforced

### INFO — Consider Fixing

- Imprecise language (e.g., "fast" without qualification)
- Slightly stale wording that doesn't mislead
- External claim where stronger evidence is available
- Missing doc where one would improve clarity (but absence isn't wrong)

---

## Output Format

The verification agent must produce this structured report:

```markdown
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

(FAIL if any BLOCKs exist. PASS WITH WARNINGS if WARNs but no BLOCKs.)

## Findings

| # | Severity | File:Line | Category | Claim | Verdict | Evidence |
|---|----------|-----------|----------|-------|---------|----------|
| 1 | BLOCK | path:42 | Behavioral | "returns None on empty input" | WRONG — returns panic | `fn foo()` at line 45: `input[0]` with no empty check |
| 2 | WARN | path:88 | Count | "5 variants" | STALE — now 6 | `enum Bar` at line 12 has 6 variants |
| ... | | | | | | |

## Detailed Findings

### BLOCK-1: [title]
- **Location**: file:line
- **Claim**: "[quoted claim]"
- **Reality**: [what the code actually does]
- **Evidence**: [specific code reference]
- **Suggested fix**: [concrete wording correction]

### WARN-1: [title]
...

## External Claims Verification

| # | Claim | Source Checked | Result | Notes |
|---|-------|---------------|--------|-------|
| 1 | "SipHash is collision-resistant" | [source URL] | Confirmed | ... |
| 2 | "follows RFC 7519 section 4" | [RFC URL] | Partially correct | Section 4.1, not 4 |

## Verification Coverage

| File | Claims Found | Verified | BLOCK | WARN | INFO |
|------|-------------|----------|-------|------|------|
| path/a.rs | 12 | 12 | 0 | 1 | 0 |
| path/b.rs | 8 | 8 | 1 | 0 | 2 |
```

---

## Common Drift Patterns

Documentation most commonly becomes stale after refactoring in these areas.
Pay extra attention to:

- **File/module counts** — "this module contains N files" after files are added/removed
- **Field/variant counts** — "this struct has N fields" after fields are added
- **Function signatures** — doc describes parameters that were renamed or reordered
- **Derivation chains** — "derived from X via Y" when the chain changed
- **Domain constant counts** — "supports N rule types" after rules are added
- **Visibility claims** — "private to this module" after `pub` was added
- **Feature flag references** — doc mentions a feature flag that was removed or renamed
- **Example code** — inline examples that no longer compile or produce stated output
- **Import paths** — doc references `crate::old::path` that was moved
- **Error type references** — "returns `FooError`" when the error type was renamed

---

## Integration with doc-rigor Workflow

Recommended pipeline for documentation quality:

```
write code
    |
    v
/doc-rigor          (write/improve documentation)
    |
    v
/doc-verify         (verify accuracy — fresh agent, no bias)
    |
    v
fix findings        (manual or /execute-review-findings)
    |
    v
/doc-verify         (re-verify — confirm fixes are correct)
```

The key property: `/doc-rigor` and `/doc-verify` run in **separate agents**.
The verifier never sees what the writer intended — only what the writer wrote
and what the code does.

---

## Related Skills

- `/doc-rigor` — writes documentation. Doc-verify checks what doc-rigor wrote.
- `/dist-sys-auditor` — verifies distributed systems claims with citations.
  Use dist-sys-auditor for coordination patterns; doc-verify for general doc accuracy.
- `/review-dispatch` — multi-lens code review. Doc-verify focuses exclusively
  on documentation accuracy, going deeper than review-dispatch's docs lens.
- `/interface-design-review` — checks API ergonomics. Doc-verify checks whether
  the API docs accurately describe the API.
- `/execute-review-findings` — implements fixes. Feed doc-verify BLOCK findings
  to execute-review-findings for automated correction.
- `/deep-research` — gathers evidence. Use before doc-verify when external claims
  reference obscure papers or niche standards.
