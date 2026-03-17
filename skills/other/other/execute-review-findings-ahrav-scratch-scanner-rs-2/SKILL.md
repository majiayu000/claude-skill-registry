---
name: execute-review-findings
description: Use when you have code review findings, PR comments, or review reports that need to be systematically addressed — especially when there are multiple findings across different files and severities
---

# Execute Review Findings

Systematically convert review findings into tracked tasks and execute them in priority waves with parallel agents where files don't overlap.

**Core principle:** Normalize findings → create self-contained beads tasks → analyze concurrency → execute in priority waves with parallel dispatch.

## When to Use

- After `/review-dispatch` produces a ranked findings report
- After receiving multiple PR review comments
- When handed an ad-hoc review document (security audit, perf report, etc.)
- When a review produced 3+ findings that span multiple files

## When NOT to Use

- Single finding — just fix it directly
- Findings are all in the same function — no parallelism benefit
- You haven't read the code yet — understand first, then act

## Invocation

```
/execute-review-findings <source>
```

**Source options:**
- `pr` or `pr:<number>` — fetch PR comments via `gh api`
- `review` — use the most recent `/review-dispatch` output in conversation
- `<file-path>` — read a markdown review document from disk
- *(no argument)* — prompt user to paste or describe findings

## Phase 1: Gather & Normalize

Parse findings from any source into a uniform list. Each normalized finding has:

| Field | Description |
|-------|-------------|
| `id` | Sequential number (F1, F2, ...) |
| `severity` | MUST FIX / SHOULD FIX / CONSIDER / NIT |
| `type` | bug, performance, safety, documentation, design, complexity |
| `file` | File path(s) affected |
| `line` | Line number(s) or range |
| `summary` | One-line description |
| `detail` | Full finding with current → desired behavior |
| `specialists` | Which reviewers flagged it (if from `/review-dispatch`) |

**Parsing rules by source:**

- **`/review-dispatch` output**: Parse the ranked tables directly. Map importance 9-10 → MUST FIX, 7-8 → SHOULD FIX, 5-6 → CONSIDER, 1-4 → NIT.
- **PR comments**: Fetch via `gh api repos/{owner}/{repo}/pulls/{number}/comments`. Categorize each: bug claim → bug type, style suggestion → design/complexity, question → skip (reply only).
- **Markdown document**: Look for severity markers, tables, or heading-based grouping. Map to standard severities.

### Severity Normalization

Reviewers use different severity vocabularies. Normalize all external labels to the
four canonical levels before filtering:

| External Label | Canonical Severity |
|----------------|-------------------|
| CRITICAL, P0, Blocker, MUST FIX | **MUST FIX** |
| HIGH, P1, Major, SHOULD FIX | **SHOULD FIX** |
| MEDIUM, P2, Moderate, CONSIDER | **CONSIDER** |
| LOW, P3, Minor, NIT, Trivial, Style, INFO | **NIT** |

When a finding lacks an explicit severity label, infer from type:
- Bug → default SHOULD FIX (unless clearly cosmetic)
- Safety / Security → default MUST FIX
- Performance → default SHOULD FIX
- Documentation / Design / Complexity → default CONSIDER

Present the normalized table to the user for confirmation before proceeding.

### Severity Filter (Default: MUST FIX + SHOULD FIX + CONSIDER)

After normalization, **discard NIT-severity findings by default**.
Only MUST FIX, SHOULD FIX, and CONSIDER proceed to Phase 2.

In reviewer terms: CRITICAL and HIGH are always addressed. MEDIUM is addressed
(maps to CONSIDER). LOW, Minor, NIT, Trivial, Style, and INFO are skipped — these
are cosmetic or informational and dilute agent focus.

Discarded findings are listed in the summary report (Phase 6) with status "Skipped (below threshold)".

**Override**: Use `--include=nit` to opt in to NIT-severity findings when the user
explicitly wants them addressed.

## Phase 2: Create Beads Tasks

Create one `bd create` per finding. Each task description must be **fully self-contained** — a fresh agent can work it without reading the original review.

### Task Description Template (All Types)

The template follows the project's Task Quality Standard. The orchestrator reads
each affected file during Phase 2 to extract Current State and Code References
inline (no Explore agent — keeps latency low for multi-finding workflows).

```
## Finding: {summary}

**Severity**: {severity}
**File(s)**: {file}:{line}
**Type**: {type}
**Flagged by**: {specialists}

### Context
{Why this finding matters. What user/system impact does the current behavior have?
What symptom or risk prompted it?}

### Current State
{The actual code at the finding location — 5-20 lines with file:line header.
The orchestrator reads the affected file during Phase 2 to extract this.}

```rust
// {file}:{start_line}-{end_line} — {brief description of what this code does}
{actual code extracted from reading the file}
```

### Problem
{detail — full finding including current behavior and why it matters}

### Desired State
{What the code should look like or how it should behave after the fix.
Be specific: new return type, changed logic, added check, etc.}

### Resolution Steps
{type-specific steps — see below}

### Code References
{Additional context beyond the primary finding location:
- Callers of the affected function (with file:line)
- Related functions that follow the pattern this fix should match
- Test module location for the affected file
Include 2-4 snippets, each 5-15 lines with file:line headers.}

### Related Work
{Run `bd search "{file path}" --limit 5` during Phase 2 task creation.
List related open tasks.}

| Task ID | Title | Relationship |
|---------|-------|-------------|
{Or "None found" — section must always be present.}

### Acceptance Criteria
- [ ] {specific, verifiable conditions}
- [ ] All existing tests pass: `cargo test`
- [ ] Code compiles clean: `cargo fmt --all && cargo check && cargo clippy --all-targets --all-features -- -D warnings`

### Pointers
{Where to look for additional context:
- Review source (which reviewer/skill produced this finding)
- Test module path for the affected file
- Adjacent files worth reading for patterns
- Relevant documentation or design docs}
```

### Type-Specific Resolution Steps

**Bug** (TDD mandatory + test-consolidate):
```
1. Analyze existing tests using /test-consolidate principles BEFORE writing any test:
   a. Read the test module for the affected file
   b. Identify existing test clusters that cover the same function/method
   c. Determine the right test form for the new test:
      - If existing tests for this function use rstest: ADD A NEW #[case] to the
        existing parameterized test rather than writing a standalone #[test]
      - If existing tests use proptest: check if the bug reveals a property violation
        — if so, tighten the property assertion rather than adding a separate test
      - If existing tests use table-driven: add the bug's input/expected to the table
      - If no existing tests or tests are standalone: write a new test, but prefer
        rstest #[case] format if 3+ similar tests already exist for the same function
   d. NEVER duplicate test structure that already exists — extend, don't clone
2. Write the failing test in the form determined by step 1
   - Test name: descriptive of the behavior, NOT the review
   - Place in the appropriate test module for the file
3. Run test, confirm it FAILS: `cargo test <test_name> -- --nocapture`
4. Fix the production code — minimal change to pass the test
5. Run full suite: `cargo test`
6. Verify clean: `cargo fmt --all && cargo check && cargo clippy --all-targets --all-features -- -D warnings`
```

**Performance**:
```
1. Establish baseline: run relevant benchmark or add one if none exists
   - Use `/bench-compare` if Criterion benchmarks cover this path
2. Implement the optimization
3. Re-benchmark and compare against baseline
4. Verify no regressions: `cargo test`
5. Verify clean: `cargo fmt --all && cargo check && cargo clippy --all-targets --all-features -- -D warnings`
```

**Safety** (unsafe code):
```
1. Write a test exercising the unsafe path with edge-case inputs
2. Fix the safety issue (bounds checks, invariant enforcement, etc.)
3. Add or update `// SAFETY:` comment documenting invariants
4. Run tests: `cargo test`
5. If Miri-compatible: `cargo +nightly miri test <test_name>`
6. Verify clean: `cargo fmt --all && cargo check && cargo clippy --all-targets --all-features -- -D warnings`
```

**Documentation**:
```
1. Read the code the docs describe — understand actual behavior
2. Write or update documentation to match reality
3. Check AGENTS.md consistency table — if touched file is listed, update corresponding docs
4. Verify doc tests compile: `cargo test --doc`
5. Verify clean: `cargo fmt --all && cargo check && cargo clippy --all-targets --all-features -- -D warnings`
```

**Design / Complexity**:
```
1. Read surrounding code to understand existing patterns
2. Refactor to address the finding while preserving behavior
3. Run full test suite to confirm no regressions: `cargo test`
4. Verify clean: `cargo fmt --all && cargo check && cargo clippy --all-targets --all-features -- -D warnings`
```

### Priority Mapping for `bd create`

| Severity | bd priority |
|----------|-------------|
| MUST FIX | 1 |
| SHOULD FIX | 2 |
| CONSIDER | 3 |
| NIT | 4 |

### Example

```bash
bd create --title="Fix off-by-one in window boundary check" --type=bug --priority=1
```

Then update the description with the full self-contained template using `bd update <id> --description="..."`.

## Phase 3: Concurrency Analysis

Determine which tasks can run in parallel vs. must run sequentially.

### Step 1: Build File-Touch Map

For each task, list every file it will read or write:

| Task | Writes | Reads |
|------|--------|-------|
| F1 | src/engine/core.rs | src/engine/mod.rs |
| F2 | src/engine/scratch.rs | - |
| F3 | src/engine/core.rs | src/api.rs |

### Step 2: Identify Conflicts

Two tasks conflict if they **write to the same file**. Read-read and read-write of different files are fine.

### Step 3: Form Parallel Groups

Within each severity wave, group non-conflicting tasks:

```
Wave 1 (MUST FIX):
  Group A (parallel): F1, F4  — no file overlap
  Group B (sequential after A): F3  — conflicts with F1 on core.rs

Wave 2 (SHOULD FIX):
  Group C (parallel): F5, F6, F7  — no file overlap
```

### Step 4: Register Dependencies

```bash
bd dep add <F3-id> <F1-id>   # F3 depends on F1 (same file)
```

## Phase 4: Execute in Priority Waves

Execute findings wave by wave: MUST FIX → SHOULD FIX → CONSIDER.
NIT and INFO findings are skipped by default (see Phase 1 severity filter).

### Within Each Wave

1. **Dispatch parallel agents** for each non-conflicting group using the Task tool with `subagent_type=general-purpose`. Each agent gets the full self-contained task description from Phase 2.

2. **Agent prompt structure:**
   ```
   You are fixing a code review finding. Follow the resolution steps exactly.

   {full task description from Phase 2}

   IMPORTANT:
   - Follow the resolution steps in order
   - For bugs: BEFORE writing any test, read the existing test module and apply
     /test-consolidate principles:
     * If the function already has rstest parameterized tests, add a #[case] — do NOT
       create a new standalone test function
     * If the function has proptest coverage, tighten the property or add a targeted
       prop_assert — do NOT duplicate with a unit test
     * If similar tests exist as a table-driven loop, add your case to the table
     * Only create a new standalone #[test] when no consolidation opportunity exists
     * NEVER create a test that duplicates coverage already provided by existing tests
   - For bugs: write the failing test BEFORE fixing code
   - Run all verification commands listed in acceptance criteria
   - Report back: what you changed, test results, any issues encountered
   ```

3. **Collect results** from all agents in the group.

4. **Sequential groups**: After a parallel group completes, dispatch the next group that depended on it.

5. **Close completed tasks**: `bd close <id>` for each successfully resolved finding.

### Quality Gate Between Waves

Before moving to the next wave, run:

```bash
cargo fmt --all && cargo check && cargo clippy --all-targets --all-features -- -D warnings
cargo test
```

If anything fails, fix it before proceeding. Do not let failures from Wave 1 propagate into Wave 2.

### Handling `--plan-only` Mode

If invoked with `--plan-only`, stop after Phase 3. Present the task list, dependency graph, and execution plan without dispatching agents. The user can then:
- Reorder or remove tasks
- Adjust groupings
- Execute manually or re-invoke without `--plan-only`

## Phase 5: Doc Verification

After all waves pass the quality gate, dispatch a **separate** `/doc-verify` agent on every
source file modified during execution. This catches documentation drift introduced by the fixes.

### Step 1: Collect Modified Files

Gather the list of all `.rs` files that were modified across all waves. Use `git diff --name-only`
(unstaged) to identify them. Filter to `.rs` files only — skip test-only files and Cargo.toml.

### Step 2: Dispatch Doc-Verify Agent

Launch a fresh `Task` agent with `subagent_type="general-purpose"`. The agent prompt must:

1. Read every modified source file in full
2. Read adjacent module files for cross-reference context
3. Follow the `/doc-verify` Phase 2 verification protocol:
   - Extract all testable claims from doc comments
   - Verify each claim against the actual (now-modified) code
   - Classify findings as BLOCK / WARN / INFO
4. Produce the standard doc-verify report

```
You are a documentation verifier. You have zero prior context about why these files
were changed — verify only what the documentation says against what the code does.

Files to verify:
{list of modified .rs files}

Follow the /doc-verify Phase 2 protocol exactly:
- Step A: Extract all testable claims from doc comments
- Step B: Verify code-level claims against actual implementation
- Step C: Identify external claims
- Step D: Verify external claims (skip with --code-only if time-constrained)
- Step E: Produce findings report

Output the standard doc-verify report format with BLOCK/WARN/INFO findings.
```

### Step 3: Handle Findings

- **No BLOCKs**: Proceed to summary report.
- **BLOCKs found**: Present findings to the user. Doc BLOCKs indicate the fixes introduced
  documentation inaccuracies (e.g., a doc comment now describes old behavior). These should
  be fixed before considering the review execution complete.
  - If the BLOCK is a trivial doc update (stale count, renamed parameter), fix it inline.
  - If the BLOCK requires judgment (rewriting a behavioral description), flag it for the user.

### When to Skip

- If `--skip-doc-verify` flag is set, skip this phase entirely.
- If no modified files contain doc comments (verified via quick Grep for doc-comment prefixes),
  skip with a note in the summary.

## Phase 6: Summary Report

After all waves complete, present:

```markdown
## Review Findings Execution Summary

**Source**: {source description}
**Total findings**: N
**Executed**: X resolved, Y skipped, Z failed

### Results

| # | Finding | Severity | Status | Task ID | Notes |
|---|---------|----------|--------|---------|-------|
| F1 | Off-by-one in window check | MUST FIX | Resolved | beads-xxx | TDD: test added + fix |
| F2 | Missing capacity hint | SHOULD FIX | Resolved | beads-yyy | 12% alloc reduction |
| F3 | Unclear doc comment | CONSIDER | Resolved | beads-zzz | Updated doc |
| F4 | Rename variable | NIT | Skipped | - | User opted out |

### Verification

- All tests passing: yes/no
- Clippy clean: yes/no
- New tests added: N
- Tests consolidated (extended existing rstest/proptest): N
- Files modified: [list]

### Doc Verification (Phase 5)

- Files verified: N
- Claims checked: N
- BLOCKs: N (list if any)
- WARNs: N
- Verdict: PASS / PASS WITH WARNINGS / FAIL
```

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Do This Instead |
|--------------|----------------|-----------------|
| Fixing a bug without a failing test first | You don't know if the fix works or if the bug was real | TDD: failing test → fix → green |
| Putting multiple findings in one task | Agents lose focus, partial completion is messy | One `bd create` per finding |
| Skipping documentation findings | Doc debt compounds silently | Documentation findings are never optional |
| Dispatching agents that write to the same file | Merge conflicts and lost work | Concurrency analysis in Phase 3 |
| Task description says "see review for details" | Fresh agent can't work it — context is lost | Self-contained descriptions with full context |
| Running all severities in parallel | A MUST FIX might invalidate a NIT | Execute in priority waves |
| Skipping the quality gate between waves | Broken state cascades into subsequent fixes | `cargo test` + clippy between every wave |
| Writing a new standalone test when rstest cases exist | Test proliferation, maintenance burden, inconsistent patterns | Add a `#[case]` to the existing rstest instead |
| Ignoring existing proptest coverage for a bug | Duplicates coverage, misses the property violation | Tighten the property assertion or add a targeted `prop_assert` |
| Skipping doc-verify after fixes | Fixes can invalidate doc comments, creating silent drift | Always run Phase 5 doc-verify on modified files |

## Configuration

| Flag | Effect |
|------|--------|
| `--plan-only` | Stop after Phase 3 — show tasks and execution plan, don't execute |
| `--wave=N` | Execute only wave N (1=MUST FIX, 2=SHOULD FIX, 3=CONSIDER) |
| `--include=nit` | Include NIT findings (skipped by default) |
| `--include=nit,info` | Include both NIT and INFO findings |
| `--skip=consider` | Also skip CONSIDER findings (only MUST FIX and SHOULD FIX) |
| `--dry-run` | Parse and normalize findings without creating beads tasks |
| `--skip-doc-verify` | Skip Phase 5 doc verification |

## Related Skills

- `/review-dispatch` — produces the findings this skill consumes
- `/pr-comment-response` — TDD verify-first pattern for individual PR comments
- `/bench-compare` — baseline/comparison benchmarks for performance findings
- `/test-strategy` — choose appropriate test type (unit, property, fuzz, Kani)
- `/test-consolidate` — referenced in bug resolution steps to avoid test duplication
- `/doc-verify` — runs as Phase 5 to catch documentation drift from fixes
