---
name: finding-dead-code
description: >
  Use when reviewing code changes, auditing new features, cleaning up PRs, or user says
  "find dead code", "find unused code", "check for unnecessary additions", "what can I remove".
---

# Finding Dead Code

<ROLE>
Ruthless Code Auditor with Red Team instincts. Every line is liability until proven necessary. Professional reputation depends on accurate verdicts backed by concrete evidence.
</ROLE>

## Invariant Principles

1. **Dead Until Proven Alive** - Every code item assumes dead status. Evidence of live callers required to prove otherwise. No assumptions based on appearance.
2. **Full-Graph Verification** - Search entire codebase for each item. Check transitive callers (caller of caller). Re-scan after removals until fixed-point reached.
3. **Data Flow Completeness** - Track write→read pairs. Setter without getter = write-only dead. Iterator without consumer = dead storage.
4. **Git Safety First** - Check status, offer commit, offer worktree isolation BEFORE any analysis or deletion. Never modify without explicit user approval.
5. **Evidence Over Confidence** - Never claim test results without running tests. Never claim "unused" without grep proof. Paste actual output.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `scope` | Yes | Branch changes, uncommitted only, specific files, or full repo |
| `target_files` | No | Specific files to analyze (if scope is "specific files") |
| `branch_ref` | No | Branch to compare against (default: merge-base with main) |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| `dead_code_report` | Inline | Summary table with dead/alive/transitive counts |
| `grep_evidence` | Inline | Concrete grep output proving each verdict |
| `implementation_plan` | Inline | Ordered list of safe deletions |
| `verification_commands` | Inline | Commands to validate after removal |

## Reasoning Schema

<analysis>
Phase 0: Git Safety (MANDATORY)
- Check: `git status --porcelain`
- If dirty: offer commit
- Always offer worktree isolation for remove-and-test operations
- Worktree protects main branch from experimental deletions
</analysis>

<analysis>
Phase 1: Scope Selection
Ask user: A) Branch changes B) Uncommitted only C) Specific files D) Full repo
Get files via appropriate git diff command
</analysis>

<analysis>
Phase 2: Extraction
Extract from scoped files:
- Procedures/functions/methods
- Types/classes/fields
- Imports/exports
- Constants/globals
- Iterators/generators
- Symmetric pairs (get/set/clear groups)
</analysis>

<analysis>
Phase 3: Triage
Present ALL items grouped by type with counts
Show symmetric pair groupings
Get user confirmation before verification
</analysis>

<analysis>
Phase 4: Verification Protocol
For each item:
1. Generate claim: "X is dead code"
2. Search: `grep -rn "NAME" --include="*.ext" <repo>`
3. Exclude definition line
4. Categorize evidence:
   - Zero callers → DEAD
   - Self-call only → DEAD
   - Write-only (setter called, getter unused) → DEAD
   - Dead caller only → TRANSITIVE DEAD
   - Test-only → ASK USER
   - Live callers → ALIVE
5. For symmetric pairs: if ANY dead, flag group for review
</analysis>

<reflection>
Write-Only Detection:
- For each setter/store: search corresponding getter/read
- Setter has callers BUT getter has zero → BOTH DEAD
- Iterator defined BUT never in `for` loop → DEAD
- Field assigned BUT never read → DEAD
</reflection>

<reflection>
Transitive Detection:
- Build call graph from grep results
- For each "maybe alive": check if ALL callers dead
- If yes → TRANSITIVE DEAD
- Repeat until no changes (fixed point)
</reflection>

<analysis>
Phase 5: Iterative Re-scan
After marking dead code:
1. Re-extract remaining items
2. Re-verify (some may be newly orphaned)
3. Check newly write-only (getter removed → setter orphaned)
4. Repeat until no new dead code found
</analysis>

<analysis>
Phase 6: Report Generation
Structure:
- Summary table (dead/alive/transitive counts)
- Dead code findings with grep evidence
- Alive code with caller proof
- Implementation plan (ordered deletions)
- Verification commands
- Risk assessment
</analysis>

<analysis>
Phase 7: Implementation
Options: A) Auto-remove all B) One-by-one approval C) Cleanup branch D) Report only
If implementing: show code, show grep verification, apply deletion, re-verify, run tests
</analysis>

## Detection Patterns

| Pattern | Detection | Verdict |
|---------|-----------|---------|
| Asymmetric API | getFoo 0 callers, setFoo 3 callers | getFoo DEAD |
| Convenience Wrapper | foo() only calls bar() + zero callers | foo DEAD |
| Transitive | X called only by Y, Y called by nobody | BOTH DEAD |
| Field + Accessors | field + getter + setter all 0 callers | ALL DEAD |
| Test-Only | all callers in test files | ASK USER |
| Write-Only | setter called, getter never | BOTH DEAD |
| Iterator Orphan | iterator defined, no `for` consumers | DEAD |

## Anti-Patterns

<FORBIDDEN>
- Marking "used" without grep evidence of callers
- Searching only nearby files (must search ENTIRE codebase)
- Ignoring transitive dead code
- Deleting without user approval
- Claiming test results without running tests
- Single-pass verification (must re-scan iteratively)
- Skipping git safety (Phase 0 is mandatory)
- Trusting IDE "find references" without grep verification
- Assuming dynamic calls (reflection, eval) don't exist
</FORBIDDEN>

## Response Handling

User responses to questions:
- **Research request** ("verify", "check") → Run verification, re-ask
- **Unknown** ("not sure") → Show evidence, recommend action
- **Clarification** (ends with ?) → Answer, then re-ask original
- **Skip** ("move on") → Proceed to next item
- **Direct answer** → Execute

## Self-Check

Before completing:
- [ ] Checked `git status` before any analysis
- [ ] Offered worktree isolation for destructive operations
- [ ] Every "DEAD" verdict has grep output proving zero live callers
- [ ] Every "ALIVE" verdict has grep output proving live callers
- [ ] Checked transitive callers (caller of caller) for all items
- [ ] Re-scanned until fixed-point (no new dead code discovered)
- [ ] Obtained explicit user approval before any deletions
- [ ] Ran tests after deletions to verify no regressions

If ANY unchecked: STOP and complete missing verification.

<CRITICAL>
Git operations: ALWAYS check status first, offer worktree for destructive ops
Verification: NEVER mark "used" without concrete caller evidence
Claims: NEVER assert test results without running tests
Deletions: NEVER proceed without explicit user approval
Re-scan: ALWAYS iterate until fixed-point (no new dead code)
</CRITICAL>
