---
name: dry-walkthrough
description: Validate an implementation plan by tracing through each change without implementing. Use when user says dry walkthrough, drywalkthrough, validate plan, or check plan. Identifies gaps, fixes the plan directly, and reports changes to terminal.
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo '🔎 [SKILL: dry-walkthrough] Validating plan...'"
          once: true
---

# Dry Walkthrough Skill

Validate a proposed implementation plan by performing a dry walkthrough of each change without implementing. Fix issues directly in the plan and report what changed to the terminal.

## Key Principle

The plan file must remain a **clean, self-contained implementation instruction set**. No gap analysis, no commentary, no "issues found" sections in the plan itself. All reporting goes to terminal output.

**Your role is technical validation, not strategic decision-making.** Fix factual inaccuracies (wrong file paths, nonexistent functions, incorrect line numbers). Preserve all goals and scope.

## When to Use

- User says "dry walkthrough", "drywalkthrough", "dry walk", "dry run"
- User wants to "validate plan" or "check plan"
- User says "before implementing" and wants verification
- After creating a plan, before implementation

## Arguments

`{plan_path}`   — Absolute path to the plan file to validate (optional: falls back to most recent temp/ artifact if omitted)

## Critical Constraints

**NEVER:**
- Modify any source code files
- Implement any part of the plan
- Add backward compatibility to the plan
- Add fallback mechanisms
- Write gap analysis or commentary INTO the plan file
- Add a rollback plan
- Add deprecation notes, stubs, code, warnings
- Include alternative approaches that will not be part of implementation in plan
- Remove or defer goals or phases from the plan
- Reduce the plan's scope to a "simpler fix" - the plan defines the problem scope, not you
- Consider effort as a reason for choosing one approach over another

**ALWAYS:**
- Keep the plan as clean implementation instructions only (information/background helpful to implementation is okay)
- Use `model: "sonnet"` when spawning all subagents via the Task tool
- Report all findings to terminal output (your response text)
- Fix issues by directly updating the plan content
- Verify assumptions against actual codebase
- Remove deprecation code/notes and rollback mechanisms
- Make sure the plan includes warning against using the codebase as a notepad with useless comments
- Prefer the long term health of project over quick, easy, and minimal fixes

## Dry Walkthrough Workflow

### Step 1: Load the Plan

Read the plan from:
- Path provided by user
- Plan content pasted directly
- Most recent plan in temp/ subdirectories

### Multi-Part Plan Detection

After resolving the plan path, check whether this is a part file of a multi-part plan:

1. **Detect the part suffix:** If the plan filename contains `_part_` (e.g., `_part_a`, `_part_b`, `_part_1`), this is one part of a multi-part plan. Extract the part identifier (A, B, C… or number) from the suffix.

2. **⚠️ SCOPE BOUNDARY — CRITICAL:** If a part suffix is detected, immediately output to the terminal:
   > "⚠️ MULTI-PART PLAN DETECTED: Validating PART {X} ONLY. This session MUST NOT read, open, reference, or validate any other part files. Sibling part files visible in temp/ or any other directory are entirely out of scope and must be ignored."

3. **Verify the scope warning block:** Check that the plan file contains the mandatory scope warning block immediately after the title line. The block must match this form:
   ```
   > **PART {X} ONLY. Do not implement any other part. Other parts are separate tasks requiring explicit authorization.**
   ```
   If the block is absent, or contains the wrong part label or wording, insert or correct it as your **first** edit to the plan file before proceeding to phase validation.

### Step 2: Extract and Validate Each Phase

For each phase, verify using subagents:

```
1. Do the target files exist?
2. Do the referenced functions/classes exist?
3. Are the assumptions about current state correct?
4. Will the changes introduce circular dependencies?
5. Are there hidden dependencies not mentioned?
6. Does this violate any project rules?
7. Does the implmentation make sense given the reality of the current state of code?
8. Is every new component, class, or function actually wired into the call chain? Nothing should be created but left unconnected.
```

### Step 3: Check Cross-Phase Dependencies

Verify phase ordering:
- Does Phase N depend on Phase N-1 completion?
- Are there implicit dependencies not stated?
- Could phases be reordered for safety?

### Step 4: Validate Against Project Rules

```
PROJECT RULES CHECKLIST:
[ ] No backward compatibility code
[ ] No fallbacks that hide errors
[ ] No stakeholder sections
[ ] No PR breakdown sections
[ ] Follows existing architectural patterns
[ ] Uses existing utilities (not reinventing) unless refactoring is part of plan or provides major improvement
[ ] Test command uses the project's configured `test_check.command` (from `.autoskillit/config.yaml`, default: `task test-check`) — no unconfigured direct test runner invocations (pytest, python -m pytest, etc.)
[ ] Worktree setup uses `worktree_setup.command` or `task install-worktree` — no hardcoded `uv venv`, `pip install`, or direct package manager invocations
```

**Test command enforcement:** Scan the entire plan for any test invocation. Read the project's configured test command from `test_check.command` in `.autoskillit/config.yaml` (default: `task test-check` if absent or unconfigured). If the plan contains `pytest`, `python -m pytest`, `make test`, or any other unconfigured test runner invocation, replace it with the config-driven command.

**Worktree setup enforcement:** Scan the plan for any worktree environment setup. The plan should reference the project's configured `worktree_setup.command` or `task install-worktree`. If the plan contains hardcoded `uv venv`, `uv pip install`, `pip install -e`, `npm install` (as worktree setup, not as a configured command), flag it and replace with the config-driven approach.

### Step 4.5: Historical Regression Check

Run a lightweight two-part scan to detect whether the plan risks reintroducing
patterns that were previously fixed or conflicts with tracked GitHub issues.
This is a quick cross-reference sanity check — not a deep audit.

**Defaults:** Last 100 recent commits · Issues closed in last 30 days

**A. Git History Scan**

1. Extract the set of source files the plan proposes to touch by grepping the plan
   text for paths matching `src/**/*.py` and `tests/**/*.py`. Store as `PLAN_FILES`.

2. Scan recent commit messages on those files for fix/revert/remove/replace keywords:
   ```bash
   git log --oneline -100 --format="%H %s" --grep="fix\|revert\|remove\|replace\|delete" -- {PLAN_FILES}
   ```

3. For each matching commit, determine signal strength:
   - **Strong signal:** The plan proposes to add a function or class name that appears
     in the commit's diff as a deletion — check with:
     `git show {hash} | grep "^-def \|^-class \|^-async def "` and compare against
     function/class names the plan introduces.
   - **Weak signal:** Same file touched + fix/revert keyword in message, but no
     symbol-level match.

4. Classify:
   - **Strong signal → Actionable:** Insert a warning note into the affected plan step:
     `> ⚠️ Historical note: {symbol} was removed in {hash} ("{commit_message}") — verify this addition is intentional and does not reintroduce a known bug.`
   - **Weak signal → Informational:** Record for terminal output (collected in Part C).

**B. GitHub Issues Cross-Reference**

1. Check `gh` authentication:
   ```bash
   gh auth status 2>/dev/null
   ```
   If this fails, skip Part B and record an informational note:
   "GitHub issues scan skipped — gh not authenticated."

2. Fetch open and recently closed issues:
   ```bash
   gh issue list --state open --json number,title,body --limit 100
   gh issue list --state closed --json number,title,body,closedAt --limit 100
   ```
   Filter closed issues to those `closedAt` within the last 30 days.

3. Build a keyword set from the plan: target file basenames (without `.py`), function
   names mentioned in the plan, and key terms from described changes.

4. Cross-reference each issue's title and body against the keyword set:
   - **Closed issue match → Actionable:** The issue specifically fixed a pattern the
     plan proposes to introduce. Insert a warning note into the affected plan step:
     `> ⚠️ Historical note: Issue #{N} ("{title}") addressed this area — ensure the plan does not reintroduce the fixed pattern.`
   - **Open issue match → Informational:** Record for terminal output:
     "Issue #{N}: {title} — addresses the same area. Verify alignment before implementing."

**C. Collect informational findings**

Gather all weak-signal git findings and open-issue area overlaps into a list.
These are forwarded to Step 7 for inclusion in the `### Historical Context` terminal section.
If Part A and Part B produce no findings, record: "No historical regressions or issue overlaps detected."

### Step 5: Fix the Plan

For each issue found:
1. Directly edit the plan file to fix it
2. Do NOT add any "gap analysis" or "issues" sections to the plan
3. The plan should read as if it was correct from the start

### Step 6: Mark Plan as Verified

After fixing all issues, add this exact line as the **first line** of the plan file:

```
Dry-walkthrough verified = TRUE
```

This marker indicates the plan has been validated and is ready for implementation. The implement-worktree skill checks for this marker before proceeding.

### Step 7: Report to Terminal

After updating the plan, output a summary to the terminal (your response text):

```
## Dry Walkthrough Complete

**Plan:** {path}
**Status:** {PASS - Ready to implement / REVISED - See changes below}

### Changes Made
1. {What was changed and why}
2. {What was changed and why}

### Verified
- {Key assumption that was confirmed}
- {Key assumption that was confirmed}

### Historical Context
- {finding}: {description}
  (or: No historical regressions or issue overlaps detected.)

### Recommendation
{Implement as-is / Review changes before implementing}
```

## Output Rules

| Content | Where it goes |
|---------|---------------|
| Fixed plan content | Written to plan file (Edit tool) |
| Gap analysis | Terminal output (your response text) |
| Change summary | Terminal output (your response text) |
| Recommendations | Terminal output (your response text) |

## Example

**Input:** User says "dry walkthrough temp/make-plan/api_retry_plan.md"

**Process:**
1. Read the plan
2. Validate Phase 1: File exists, function exists - PASS
3. Validate Phase 2: Found similar pattern in `src/db/client.py` not referenced - needs fix
4. Validate Phase 3: Test command correct - PASS
5. Edit the plan to add reference to existing pattern
6. Output summary to terminal

**Terminal Output:**
```
## Dry Walkthrough Complete

**Plan:** temp/make-plan/api_retry_plan.md
**Status:** REVISED

### Changes Made
1. Phase 2: Added reference to existing retry pattern in `src/db/client.py:45-67` - implementation should follow this pattern for consistency

### Verified
- `src/api/client.py` exists with expected `__init__` signature
- No circular dependency risk identified
- Test commands are correct

### Historical Context
- Issue #302: "consolidate retry logic" — addresses the same area. Verify alignment before implementing.

### Recommendation
Ready to implement. Review the updated Phase 2 to see the pattern reference.
```

**Plan file:** Updated cleanly with no gap analysis sections - just the corrected implementation instructions.
