---
name: codex-code-review
description: "Automate code review remediation loops with the codex CLI. Requests reviews from codex, classifies findings by severity (P0-P4), fixes critical issues (P0/P1) through iterative cycles, defers quality improvements to backlog, and escalates after 3 review cycles. Use when working with code that needs structured remediation: 'codex review' in a request triggers this workflow."
---

# Codex Code Review Loop

## Overview

This skill orchestrates the complete remediation workflow for code under review by the codex agent. It handles:

- **Requesting reviews** from codex using the `codex --full-auto c` CLI
- **Parsing review output** to identify P0 (security/correctness), P1 (reliability), P2-P4 (quality) findings
- **Remediating critical issues** through up to 3 review-fix-review cycles
- **Deferring quality improvements** to backlog with implementation plans and `origin:ai-review` labels
- **Monorepo handling** for selective file commits when working alongside other agents
- **Circuit breaker escalation** after 3 cycles if P0/P1 issues persist

## When to Use

Trigger this skill when code requires codex review. Common usage patterns:

- **"codex review this code"** — Initiate review loop on current changes
- **"run codex review on my changes"** — Same as above
- **"codex review --uncommitted"** — Review all uncommitted changes
- **"codex review --commit <SHA>"** — Review specific commit in monorepo
- **Questions about codex** (e.g., "how does codex work?") — Do not trigger this skill; answer directly

**Do not trigger on questions.** Only activate for direct review requests.

---

## The Review Loop: Step by Step

```
ENTRY: User requests codex review or skill is triggered by "codex review" in a message

┌──────────────────────────┐
│ 1. INVOKE CODEX REVIEW   │ ← Run: codex --full-auto c [--uncommitted|--commit <SHA>|--base <BRANCH>]
└──────┬───────────────────┘   Output goes to .agent/reviews/review-<timestamp>.md
       │
       ▼
┌──────────────────────────┐
│ 2. READ & PARSE REVIEW   │ ← Read markdown file, extract P0/P1/P2-P4 findings and verdict
└──────┬───────────────────┘
       │
       ├─────────────────────────────────────────┐
       │                                         │
       ▼                                         ▼
  ANY P0/P1?              NO         FILE P2-P4 ISSUES → Exit loop
       │                              (via backlog CLI)
       │ YES                         Create issue per finding with
       │                             - label: origin:ai-review
  ┌────────────────┐                - Implementation plan
  │ 3. REMEDIATE   │                - Priority (P2 or P3)
  │ P0/P1 FINDINGS │
  └────┬───────────┘
       │ (amend commit or new changes)
       │
       ▼
  ┌──────────────────────┐
  │ 4. LOOP CHECK        │
  │ Cycle count < 3?     │
  └────┬───────────────┬─┘
       │ YES           │ NO
       │               └─→ SUMMARIZE & ASK USER TO CONTINUE
       │                   (or exit if user declines)
       ▼
  Re-run codex review (step 1, same files/scope)
  Loop back to step 2
```

### Cycle Management

- **Cycle 1**: Initial review after implementation
- **Cycle 2**: After first remediation
- **Cycle 3**: After second remediation
- **After Cycle 3**: If P0/P1 remain, stop. Summarize findings and ask user if they want to continue (rare; usually indicates design-level issues)

---

## Decision Tree: Handling Findings

### When review shows P0/P1 findings (verdict: REQUEST CHANGES)

1. Read the codex review markdown file
2. Extract each P0 and P1 finding with:
   - Finding ID and title
   - File location
   - Suggested fix
3. Fix ONLY the cited findings in the code
4. Do NOT refactor, do NOT introduce new functionality
5. If a fix requires significant design changes, note this and let codex re-evaluate on next cycle
6. Amend your commit OR create a new one (user's choice via git config; by default amend to keep one commit at end)
7. Increment cycle counter and re-run codex review

### When review shows P2-P4 findings (verdict: APPROVE or PASS WITH ISSUES)

1. For each P2/P3 finding, decide:
   - **Fix now**: You have discretion; implement the improvement in the same cycle
   - **Defer**: Create a backlog issue with:
     - Type label: `remediation`
     - Severity label: `P2` or `P3`
     - Custom label: `origin:ai-review`
     - Implementation plan based on codex's suggested approach
     - Acceptance criteria from the review

2. Examples:
   ```
   # P2 finding deferred to backlog
   backlog task create "Code clarity: add docstring to validateInput()" \
     -d "Review finding: missing documentation on public function" \
     -l remediation -p 2 \
     --ac "Add docstring explaining parameter types and return value" \
     --plan "Add JSDoc comment above function definition per project style"
   ```

### When review shows no findings (verdict: APPROVE)

Exit the loop. Code is clean. Proceed to test review (if applicable) or commit for merge.

---

## Monorepo Handling

In a monorepo with multiple agents, be selective about what you commit and what scope you review.

### Scenario 1: Only Your Changes

If the working directory has ONLY your changes:
```bash
codex --full-auto c --uncommitted
```
Commit your changes once review loop completes.

### Scenario 2: Mixed Changes (You + Other Agents)

If there are untracked or uncommitted changes from other agents:
1. Commit ONLY your files first:
   ```bash
   git add <your-files-only>
   git commit -m "Your commit message"
   ```
2. Note the commit SHA
3. Run review on your commit:
   ```bash
   codex --full-auto c --commit <SHA>
   ```
4. Remediate by amending your commit:
   ```bash
   git add <fixed-files>
   git commit --amend --no-edit
   ```
   (Preserve the original message; the amend adds the fixes)
5. Loop back to review as normal

**Result:** One clean commit with your changes and fixes. Other agents' work remains separate.

---

## File Locations

- **Review output:** `.agent/reviews/review-<timestamp>.md` (relative to project root)
- **One review file per cycle** — new file created on each `codex --full-auto c` invocation
- **Always read the latest file** — check the timestamp to ensure you're reading the current cycle's review

---

## Bundled References

**See `references/codex-cli-reference.md`** for:
- Complete codex CLI syntax and invocation patterns
- How to select `--uncommitted` vs. `--commit` vs. `--base`
- When to use each mode

**See `references/review-format.md`** for:
- Structure of the review markdown output
- How to parse P0/P1/P2/P3 sections
- How to identify the verdict (APPROVE / REQUEST CHANGES / BLOCKED)
- Example review output

**See `references/backlog-integration.md`** for:
- How to create backlog issues from deferred findings
- Label and priority conventions
- Implementation plan templates
- Examples of issues filed from reviews

**See `scripts/parse_codex_review.sh`** for:
- Helper script to extract findings from review markdown
- Counts P0/P1/P2/P3 per cycle
- Quick verdict extraction

---

## Key Rules

1. **All P0/P1 must be fixed** before exiting the loop. No exceptions.
2. **P2-P4 can be deferred** to backlog or fixed at your discretion.
3. **File one issue per finding** — do not batch unrelated P2/P3s into one issue.
4. **Deferred issues must include a plan** — codex identified the problem; you provide the structured approach.
5. **Amend commits** (not new commits) during remediation so you end with one clean commit.
6. **Max 3 review cycles** — after cycle 3, if P0/P1 remain, summarize and ask user to continue.
7. **In monorepos, commit selectively** — review and fix only the files you touched.

---

## Escalation: When Circuit Breaker Triggers

After 3 review cycles, if P0/P1 findings persist:

1. Stop remediating. Do not attempt a 4th cycle.
2. Produce a structured summary including:
   - What was attempted in each cycle
   - What P0/P1 findings remain
   - Why they persist (agent assessment — design issue? conflicting requirements? ambiguity in spec?)
   - Recommended human action
3. Present this summary to the user and ask how to proceed.

Escalation usually indicates the original task spec needs clarification or the code requires architectural changes beyond remediation scope.

---

## Integration with Other Skills

- **backlog-md**: File deferred P2/P3 findings using `backlog task create` with `origin:ai-review` label
- **git-ops**: Commit handling, amending, and selective staging in monorepos
- **requesting-code-review**: Use after codex review loop completes if human code review is also required

---

## Quick Reference: The Full Workflow

```
1. User: "codex review"
        │
        ▼
2. Invoke: codex --full-auto c --uncommitted
        │
        ▼
3. Read: .agent/reviews/review-<timestamp>.md
        │
        ├─────────────────────────────────────────┐
        ▼                                         ▼
   P0/P1 FOUND?              NO         FILE P2-P4 ISSUES
   ├─ YES: Fix + Loop ────────────────► backlog task create ... --plan "..."
   └─ NO: File P2-P4 → Exit            (each finding = one issue)
        │
        ├─ Cycle 1 → Fix → Review
        ├─ Cycle 2 → Fix → Review
        ├─ Cycle 3 → Fix → Review
        │
        └─ If P0/P1 remain → Summarize + Ask User
                │
                └─► Continue? (rare) / Stop & Escalate
```
