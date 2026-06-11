---
name: verification-before-completion
description: "Defense-in-depth verification before declaring any task complete."
user-invocable: false
success-criteria:
  - "All tests pass (full suite, not just changed files)"
  - "Build succeeds without errors or warnings"
  - "Changed files validated against task requirements"
  - "No stub patterns (TODO, FIXME, pass, not implemented) in new code"
  - "Artifacts exist at expected paths (4-level verification)"
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
routing:
  triggers:
    - "verify completion"
    - "run tests"
    - "check build"
    - "defense in depth"
    - "final verification"
  category: process
  pairs_with:
    - systematic-code-review
    - with-anti-rationalization
---

# Verification Before Completion Skill

## Overview

Enforce rigorous, adversarial verification before declaring any task complete. Implements defense-in-depth validation with multiple independent checks to catch errors before they reach users. The core principle: verify independently rather than trusting executor claims — verify what ACTUALLY exists in the codebase through testing, inspection, and data-flow tracing.

This skill prevents the most common form of premature completion: claiming success without running tests, summarizing results instead of showing evidence, or trusting code that "looks right" without verification.

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| verifying artifacts are real and substantive, not stubs | `adversarial-methodology.md` | Loads detailed guidance from `adversarial-methodology.md`. |
| checklist-driven work | `checklist.md` | Loads detailed guidance from `checklist.md`. |
| good-vs-bad verification walkthroughs: bug fix, refactor, migration, config change | `verification-examples.md` | Loads detailed guidance from `verification-examples.md`. |

## Instructions

**Verification means execution, not reasoning.** Run the command. Do not reason about whether the command would pass. Do not summarize the expected output. Execute the check, paste the exit code, paste the relevant output. A verification phase that produces a verdict without an observed tool result is not a verification — it is a guess with a rigor aesthetic.

### Step 1: Identify What Changed

Before verification, understand the scope of changes:

```bash
# For git repositories
git diff --name-only
```

**Why:** Use `git status --short` (not just `git diff`) to capture both modified AND untracked (new) files. New files created during the session are easy to miss in status summaries. Over-engineering prevention requires limiting scope to what was actually changed — limit verification to what was actually changed. Focus only on the specific changes made.

For each changed file:
- Read the file with the Read tool to validate the actual contents
- Summarize what changed
- Identify affected systems/modules and dependencies

Report separately:
- **New files**: [files with `??` or `A` status in git]
- **Modified files**: [files with `M` status]

### Step 2: Run Domain-Specific Tests

Run the appropriate test suite and show **complete** output (not summaries):

| Language | Test Command | Build Command | Lint Command |
|----------|-------------|---------------|-------------|
| Python | `pytest -v` | `python -m py_compile {files}` | `ruff check {files}` |
| Go | `go test ./... -v -race` | `go build ./...` | `golangci-lint run ./...` |
| JavaScript | `npm test` | `npm run build` | `npm run lint` |
| TypeScript | `npm test` | `npx tsc --noEmit` | `npm run lint` |
| Rust | `cargo test` | `cargo build` | `cargo clippy` |

**Why full test suite, not just changed files**: ALWAYS run relevant tests before saying "done". The same agent that writes code has inherent bias toward believing its own output is correct. Running the full suite catches regressions and unintended side effects that focused testing misses.

**Output Requirements:**
- Show COMPLETE test output (not "X tests passed")
- Display all test names that ran
- Show any warnings or deprecation notices
- Include execution time

**Critical constraint**: Show test output when reporting test results. Summary claims document what was SAID, not what IS. Evidence-based reporting is required.

### Step 3: Verify Build/Compilation

Run the build command from the table above and show the full output. Confirm:
- Build completes without errors
- No new warnings introduced
- Output artifacts are created (if applicable)

```bash
# Example: Go project
go build ./...

# Example: Python - check syntax of changed files
python -m py_compile path/to/changed_file.py

# Example: JavaScript/TypeScript
npm run build
```

**Critical gate**: If the build fails, stop immediately. Fix build issues before proceeding to any other verification step. A failed build is a blocker that supersedes all other checks. Re-run from Step 1 after fixing. This prevents declaring "done" when the code doesn't compile.

### Step 4: Validate Changed Files

For each changed file, use the Read tool to inspect the actual file contents. **Validate assumptions**: Re-read the file to confirm the actual contents — re-read the file to confirm. Verify that what you think happened actually happened.

For each file verify:
1. **Syntax** is correct (no unterminated strings, mismatched brackets)
2. **Logic** makes sense (no inverted conditions, off-by-one errors)
3. **Formatting** is consistent with surrounding code
4. **Imports/dependencies** are present and correct
5. **No leftover artifacts** (commented-out code, placeholder values, TODO markers)

This step counteracts confirmation bias where executors believe their own edits are correct without evidence.

### Step 5: Check for Unintended Changes

```bash
# Check git diff for unexpected changes
git diff

# Look for debug code that should be removed
grep -r "console.log\|print(\|fmt.Println\|debugger\|pdb.set_trace" {changed_files}

# Check for TODO/FIXME comments that should be resolved
grep -r "TODO\|FIXME\|HACK\|XXX" {changed_files}

# Verify no sensitive data
grep -r "password\|secret\|api_key\|token" {changed_files}
```

**Why this matters**: If `git diff` shows changes to files you didn't intend to modify, investigate before proceeding. Unintended changes are a red flag for accidental side effects. Detecting this early prevents silent regressions that reach users.

**Constraint**: No stub patterns (TODO, FIXME, pass, not implemented) should remain in new code created by the task.

### Step 6: Review Verification Checklist

**Core Verification (Required):**
- [ ] Tests pass (actual output shown)
- [ ] Build succeeds (actual output shown)
- [ ] Changed files reviewed (Read tool used)
- [ ] No unintended changes (diff checked)
- [ ] No debug/console statements left
- [ ] No sensitive data exposed

**Extended Verification (Recommended):**
- [ ] Documentation updated if needed
- [ ] No new warnings introduced
- [ ] Error handling adequate
- [ ] Backwards compatibility maintained

> See `references/checklist.md` for domain-specific checklists (Python, Go, JavaScript, Database, Infrastructure).

### Step 7: Final Verification Statement

**ONLY AFTER all checks pass, provide verification statement:**

```
Verification Complete

**Tests Run:**
{paste actual test output}

**Build Status:**
{paste actual build output}

**Files Verified:**
- {file1}: Reviewed, syntax valid, logic correct
- {file2}: Reviewed, syntax valid, logic correct

**Checklist Status:** X/X core checks passed

Test if this addresses the issue.
```

**Critical constraints on communication:**
- Show test output when reporting test results. Show complete verification output, not summaries.
- Report verification results concisely without self-congratulation. Show command output rather than describing it.
- Verify that what you think happened actually happened. Use Read tool on changed files, not memory.

**Replace with:**
- "Should be fixed now"
- "This is working"
- "All done"
- "Tests pass" (without showing output)

**ALWAYS say:**
- "Test if this addresses the issue"
- "Please verify the changes work for your use case"

---

## 4-Level Adversarial Artifact Verification

> See `references/adversarial-methodology.md` for the complete methodology: goal-backward framing, all four verification levels (EXISTS, SUBSTANTIVE, WIRED, DATA FLOWS), stub detection patterns with automated scan command, completion shortcut scan, verification report format, and the "when to apply each level" table.

Steps 1-7 above verify that tests pass, builds succeed, and files contain what you expect. The adversarial methodology goes deeper: it verifies that artifacts are real implementations (not stubs), actually integrated (not orphaned), and processing real data (not hardcoded empties). Apply this methodology after Steps 1-7 pass, focusing on artifacts that are part of the stated goal.

**Summary of levels:**
- **L1 EXISTS**: File is present on disk (catches forgotten writes)
- **L2 SUBSTANTIVE**: File contains real logic, not stubs (catches placeholder implementations)
- **L3 WIRED**: Artifact is imported and used by other code (catches orphaned files)
- **L4 DATA FLOWS**: Real data reaches the artifact and real results come out (catches dead integration)

## Error Handling

**Error: "Tests failed after changes"**
- Resolve stubs before declaring task complete
- Show full test failure output
- Analyze what went wrong
- Fix issues and re-run full verification

**Error: "Build failed"**
- Stop immediately
- Show complete build error output
- Fix build issues before proceeding
- Re-run verification from Step 1

**Error: "No tests exist for changed code"**
- Acknowledge lack of test coverage
- Recommend writing tests (but include only if user requests)
- Perform extra manual validation
- Document that changes are untested

**Error: "Cannot run tests (missing dependencies)"**
- Document what's missing
- Attempt alternative verification (syntax checks, manual review)
- Be explicit about verification limitations

**Error: "Stub patterns detected in changed files"**
- Review each match individually — some stubs are intentional (e.g., `return []` when empty list is the correct result)
- For confirmed stubs: flag as blocker, resolve stubs before declaring task complete
- For intentional patterns: document in verification report with rationale
- If unsure: treat as stub (false positive is safer than false negative)

**Error: "Artifact exists but is not wired (Level 3 failure)"**
- Identify what should import/reference the artifact
- Check if the wiring was planned but not executed (common in multi-step tasks)
- Flag as blocker with specific guidance: "File X exists but is not imported by Y"

**Error: "Data flow gap detected (Level 4 failure)"**
- Trace the call chain to identify where real data stops flowing
- Common cause: function called with hardcoded `[]` or `{}` instead of computed values
- Flag as blocker: "Function X is called but receives empty data at call site Y"

## References

**Core Principles**
- **Adversarial distrust**: Verify independently. The same agent that writes code has inherent bias toward believing its own output is correct. Structural distrust in the verification process counteracts this bias.
- **Evidence over claims**: Summary claims document what was SAID, not what IS. Always show actual test output, build logs, and file contents. Verification without evidence is unverifiable.
- **Goal-backward framing**: Derive verification conditions from what must be true for the goal, not from executor task lists. This prevents executors from confirming their own narrative.
- **4-level artifact verification**: EXISTS → SUBSTANTIVE → WIRED → DATA FLOWS. Each level catches distinct classes of premature-completion failures.

**Key Constraints (Integrated Above)**
- Run tests before declaring completion
- Show complete verification output (not summaries or "X tests passed")
- Check all changed files using Read tool (not memory)
- Show actual test output when reporting test results
- Run full test suite for affected domain (not just changed files)
- Flag any stub patterns as blockers — mark complete only after full verification
- Build failures are gates that stop all other verification
- Over-engineering prevention: only verify what was actually changed

**Reference Files**
- `references/adversarial-methodology.md` — 4-level verification system, stub detection, goal-backward framing
- `references/checklist.md` — Domain-specific checklists (Python, Go, JS, Database, Infrastructure)
- `references/verification-examples.md` — Good vs bad verification examples per language

**Schema gate for review artifacts**

When the artifact being verified is a code-review output, prefer a deterministic schema check over reading the prose for completeness: `python3 scripts/validate-review-output.py --type {systematic|parallel|sapcc-review|sapcc-audit} <file.md>` (exit 0 = valid, 1 = schema errors, 2 = unparseable, 3 = `jsonschema` not installed — `pip install jsonschema`). The parallel and systematic review skills wire this as a validate-on-return + retry-once-then-stop gate. This is the L1/L2 EXISTS/SUBSTANTIVE check for review documents: it confirms a verdict, severity buckets, and `file:line` locations are actually present, not just that a file was written.
