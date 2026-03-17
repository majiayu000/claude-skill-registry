---
name: bugfix
description: Bug-fixing workflow that coordinates diagnosis, test-driven reproduction, root-cause analysis, and targeted fixes. Use when the user wants to fix a bug with thorough investigation and regression testing.
model: opus
---

# Bugfix - Automated Bug-Fixing Workflow

Coordinates specialist agents through a bug-fixing cycle: clarify bug -> reproduce with failing test -> diagnose root cause -> implement fix -> verify -> review -> document.

## Workflow

### 1. Clarify the bug

**Gather bug details from user:**
- What are the symptoms? (error messages, unexpected behavior, crashes)
- What is the expected behavior vs actual behavior?
- How do you reproduce it? (steps, inputs, configuration)
- When did it start? Any recent changes that might be related?
- Environment specifics? (OS, versions, configuration)

**Ask clarifying questions if needed:**
- Ambiguous symptoms
- Missing reproduction steps
- Unclear expected behavior

Loop back to user until the bug is clearly understood. You need enough information to write a test that demonstrates the failure.

### 2. Write Failing Test(s)

**Detect project language/framework:**
- Check for language-specific files (go.mod, package.json, Cargo.toml, Dockerfile, Makefile, etc.)
- Determine which specialist agent to use

**Spawn appropriate SME agent:**
- If Golang project: spawn `swe-sme-golang` agent
- If GraphQL schema/resolvers: spawn `swe-sme-graphql` agent
- If Dockerfile changes: spawn `swe-sme-docker` agent
- If Makefile changes: spawn `swe-sme-makefile` agent
- If Ansible playbooks/roles: spawn `swe-sme-ansible` agent
- If Zig project: spawn `swe-sme-zig` agent
- Otherwise: write tests directly with general best practices

**SME agent task:**
- Write test(s) that reproduce the reported bug
- Tests should encode the *expected* behavior (so they fail against the *current* buggy behavior)
- Run the tests and **verify they actually fail**
- If the tests pass (bug cannot be reproduced): report back with findings — the bug may be environmental, already fixed, or misunderstood

**This is the contract.** When these tests pass, the bug is fixed.

**If reproduction fails:**
- Return to step 1 for more information from the user
- Report what was tried and why reproduction failed
- Max 2 reproduction attempts before escalating to user with findings

### 3. Diagnosis

**Spawn `swe-diagnostician` agent:**
- Pass: bug description, failing test(s) from step 2, reproduction results
- Agent performs root-cause analysis:
  - Traces execution paths through the code
  - Git archaeology at agent's discretion (shallow for obvious bugs, deep for systemic ones)
  - Identifies the root cause with supporting evidence
  - Identifies related failure modes that may share the same root cause
- Agent produces a structured diagnosis report

**Diagnosis report includes:**
- Root cause (immediate and underlying)
- Evidence (code paths, git history, test results)
- Recommended fix approach
- Related failure modes (specific, actionable — not vague possibilities)
- Confidence level

### 4. Implement the Fix

**Re-invoke the same SME agent from step 2:**
- Pass the diagnosis report as guidance
- SME implements the fix following the diagnostician's recommended approach
- SME writes additional tests for related failure modes identified in step 3
- SME verifies: the originally-failing test(s) from step 2 now pass
- SME runs the full test suite to check for regressions

**Implementation agent responsibilities:**
- Fix the bug as narrowly and precisely as possible
- Don't refactor unrelated code (that's a separate workflow)
- Write tests for each related failure mode the diagnostician identified
- Ensure all new and existing tests pass

### 5. Quality Assurance - Verify Fix (CRITICAL GATE)

**Spawn `qa-engineer` agent:**
- Pass: original bug description, reproduction steps, and acceptance criteria (the bug should no longer occur)
- The agent infers its mode from context: presence of acceptance criteria triggers acceptance verification
- Agent performs **practical verification first** — actually reproducing the originally-reported scenario and confirming it's fixed
- This means: executing CLI commands, spawning subagents to test MCP tools, making API calls, etc.
- Only AFTER practical verification confirms the fix works does the agent run the full test suite
- Agent also checks the related failure modes identified by the diagnostician

**Practical verification by feature type:**
- CLI tools: Run commands in subshell (skip destructive operations)
- MCP servers/Claude skills: Spawn subagent to actually use the feature
- API integrations: Make actual calls (with caution for dangerous operations)
- Libraries: Quick sanity checks, then unit tests

**This is a CRITICAL GATE:**
- The originally-reported bug must be demonstrably fixed (practical test) AND tests must pass to proceed
- If practical verification fails: return to step 4 (implementation) immediately
- If verification passes but tests fail: debug tests, not implementation
- Track iteration count (max 3 attempts before escalating to user)

**Expected output:** Practical verification results, pass/fail determination with specific findings.

### 6. Code Review (Conditional)

**Only proceed to code review if fix verification passed.** Don't review broken code.

Conditionally invoke specialized reviewers based on code changes and complexity. All reviewers provide feedback; implementation agent responds to all feedback in step 7.

#### 6a. Security Review (Conditional - Has Authority)

**If security-sensitive code changed (auth, crypto, input validation, data access):**

**Spawn `sec-blue-teamer` agent:**
- Evaluates defensive security posture of changed code
- Checks control consistency, defense-in-depth, and configuration
- Identifies systemic gaps that enable vulnerability classes
- **Has authority to demand changes** - security issues should block or require explicit user approval

**Output**: Defense evaluation with severity levels (critical/high/low)

#### 6b. Refactoring Review (Conditional - Advisory)

**If non-trivial implementation (>50 lines changed, multiple files, or complex logic):**

**Spawn `swe-refactor` agent:**
- Reviews implementation for code quality issues
- Identifies refactoring opportunities (DRY violations, dead code, complexity, etc.)
- Provides structured recommendations organized by priority
- Agent will report "No refactoring needed" if code is already clean

**Output**: Refactoring recommendations (advisory only)

#### 6c. Performance Review (Conditional - Advisory)

**If performance-critical code changed (hot paths, loops, database queries, API endpoints):**

**Spawn `swe-perf-engineer` agent:**
- Runs benchmarks and profiling
- Identifies performance bottlenecks
- Provides optimization recommendations

**Output**: Performance metrics and recommendations (advisory only)

### 7. Implement Review Feedback

**Aggregate all review feedback from step 6 and provide to implementation agent.**

**If specialist was used in steps 2/4 (swe-sme-golang, swe-sme-graphql, etc.):**
- Re-invoke the same specialist agent
- Provide all review feedback (security, refactoring, performance)
- Specialist reviews all feedback and **uses own discretion** to implement
- **Security findings**: Must address or get explicit user approval to skip
- **Other feedback**: Advisory only - specialist has final authority
- Specialist may decline recommendations that conflict with language idioms
- Specialist implements accepted changes and commits

**If no specialist (general implementation):**
- Re-invoke the same agent that did implementation in step 4
- Provide all review feedback
- Agent addresses security issues and implements accepted recommendations
- Agent commits changes

**Note**: Security issues have authority to block; other feedback is advisory. Implementation agent makes final decisions on advisory feedback.

### 8. SME Peer Review (Conditional)

**Condition:** Non-trivial changes (>50 lines changed, multiple files, or complex logic).

**Skip if:**
- Changes are trivial (single file, <50 lines, simple logic)
- No language-specific SME was used in step 2 (general implementation)

**If applicable, spawn a fresh instance of the same SME type used in step 2:**
- Fresh context window - reviewer sees only current code state via git diff
- Reviews with "would I accept this PR" lens
- Focuses on: minor oversights, idiomatic patterns, naming, small cleanups
- **Has authority to make small fixes directly**

**Scope constraints (critical):**
- Small cleanups and nits only
- No architectural changes
- No re-implementing features
- No changing approaches or patterns chosen by original SME
- If something seems wrong at a deeper level, flag it rather than fix it

**Expected output:** Small fixes committed, or "no changes needed" if code is clean.

### 9. Quality Assurance - Coverage & Quality Verification

**Spawn `qa-engineer` agent:**
- The agent infers its mode from context: absence of acceptance criteria triggers general assessment
- Agent performs general QA assessment of all changed code (from steps 4, 7, and 8)
- Assess test coverage for new/modified code
- Identify gaps and write missing tests
- Run linters/formatters and fix issues
- Evaluate test quality (assertions, edge cases)
- **Verify implementations from steps 7 and 8 didn't break tests** - catches issues from refactoring, security fixes, or peer review cleanups

**This is SUPPLEMENTARY:**
- Issues found here don't block the workflow by default
- Agent documents issues and proposes fixes
- Minor issues: proceed to documentation
- Significant issues (tests broken, major bugs): return to step 7 (review feedback) or step 4 (implementation)

**Expected output:** Coverage metrics, tests added/modified, quality issues found, confirmation that all changes still pass tests.

### Feedback Loops

**Reproduction failure (step 2):**
- Return to step 1 (clarification)
- Report what was tried and why reproduction failed
- Max 2 reproduction attempts before escalating to user

**Fix verification failure (step 5):**
- Return to step 4 (implementation)
- Track iteration count (max 3 attempts before escalating to user)
- Report specific failures (which tests still fail, what practical verification showed)

**Security review findings (step 6a):**
- Critical/High severity: Must address in step 7 or get explicit user approval to skip
- Medium/Low severity: Advisory - implementation agent decides in step 7

**Code review feedback (steps 6b-6c):**
- All refactoring and performance feedback is advisory
- Implementation agent in step 7 uses discretion to implement

**Peer review issues (step 8):**
- If peer review changes break tests: revert peer review changes and proceed (nits aren't worth breaking functionality)
- If peer review flags deeper issues: escalate to user for decision

**Coverage & quality issues (step 9):**
- Tests broken by changes from step 7: Return to step 7 to fix or revert
- Tests broken by changes from step 8: Revert step 8 changes (peer review nits shouldn't break tests)
- Major bugs found: Return to step 4 (implementation)
- Minor issues (low coverage in non-critical code, style nitpicks): document and proceed
- User can approve proceeding despite issues if acceptable

### 10. Documentation

**Spawn `doc-maintainer` agent:**
- Review git diff to identify which files/modules changed
- Determine which documentation is affected:
  - README.md if user-facing functionality changed
  - CLAUDE.md if architecture/integration points changed
  - API docs if public interfaces changed
  - Internal docs (doc/, adr/) if implementation details relevant to architecture changed
- Focus review on documentation related to changed code
- Verify code examples in affected docs still work
- Check for broken links in modified documentation

**Agent should be targeted, not comprehensive:**
- Only review documentation relevant to the changes made
- Skip full codebase documentation scan
- Report "no documentation changes needed" if changes are purely internal with no doc impact

### 11. Final verification

**Run comprehensive checks:**
- Execute full test suite (must pass)
- Run all linters and formatters
- Verify no new warnings introduced
- Check git status (document any uncommitted changes)

**Present summary to user:**
- Bug that was fixed (original report)
- Root cause identified (from diagnosis)
- Files changed
- Tests added/modified (regression tests for the bug + related failure modes)
- Any remaining TODOs or follow-ups

**If verification fails:**
- Determine root cause (implementation bug vs. refactoring issue vs. test issue)
- Return to appropriate step (step 4 for implementation bugs, step 7 for refactoring issues)
- Report specific failures to user

### 12. Workflow Completion (Optional)

**After presenting summary from step 11, ask user if they want to complete the workflow.**

User may also explicitly request workflow completion at any point after step 11 succeeds.

**If user confirms, perform housekeeping tasks:**

#### 12a. Commit Changes

**If uncommitted changes exist:**
- Review git status to see what changed
- Create commit with descriptive message
- If ticket number is known (from branch name, prior context, or user input):
  - Reference ticket in commit message (e.g., "Fixes #123" or "Closes: #123")
- Include Co-Authored-By line: `Co-Authored-By: Claude <noreply@anthropic.com>`
- Use heredoc format for multi-line commit messages

**Example commit message format:**
```
Fix off-by-one error in pagination boundary check

Root cause: boundary comparison used < instead of <= when calculating
the last page, causing the final item to be excluded from results.
Also added regression tests for adjacent edge cases identified during
diagnosis.

Fixes #456

Co-Authored-By: Claude <noreply@anthropic.com>
```

#### 12b. Update/Close Issue Tracker Ticket (Conditional)

**Detect issue tracker:**
- Check for platform integration (CLI, MCP server, or API)
- Skip if not available

**Determine ticket number:**
- Try to extract from current branch name (e.g., `fix/456-pagination-bug` -> #456)
- Check commit messages for ticket references
- Ask user for ticket number if not found and they indicated a ticket exists

**If ticket number identified:**
- Ask user: "Do you want to update and/or close ticket #456?"
  - Options: "Update only", "Update and close", "Skip"

**If user chooses to update:**
- Post comment with summary:
  - Root cause identified
  - Fix applied
  - Tests added (regression + related failure modes)
  - Files changed
- Use available integration to comment on issue

**If user chooses to close:**
- Close the ticket with final comment
- Use available integration to close issue

#### 12c. Sync with Main Branch (Conditional)

**Check branch state:**
- Identify main branch name (master or main)
- Check if current branch is not main
- Check if there are new commits on main that current branch doesn't have

**If current branch is behind main:**
- Ask user: "Your branch is behind main. Would you like to rebase on main?"
- If user confirms:
  - Perform: `git fetch origin main && git rebase origin/main`
  - If conflicts arise, report to user and halt (don't auto-resolve)
  - If rebase succeeds, report success

**Skip if:**
- Current branch is main/master
- Current branch is up to date with main
- No main/master branch exists

**Present final status:**
- Changes committed
- Ticket updated/closed
- Branch rebased on main
- Ready to push or move to next task

## Agent Coordination

**Sequential execution:**
- Agents run one at a time (no parallel spawning)
- Each agent completes before next begins
- Use Task tool to spawn agents

**State management:**
- Track current workflow step
- Track reproduction attempt count (for step 2 failures)
- Track QA iteration count (for fix verification failures)
- Accumulate summary information
- Preserve original bug report for passing to QA verification
- Preserve diagnosis report for passing to implementation agent

**Agent self-skipping:**
- Agents should skip work if not applicable
- Report "nothing to do" rather than making unnecessary changes

**SME continuity:**
- The same SME type is used across steps 2 (failing test), 4 (fix), 7 (review feedback), and 8 (peer review)
- Steps 2 and 4 should ideally be the same instance or carry forward context
- Step 8 (peer review) must be a fresh instance for independent perspective

**Diagnosis pass-through:**
- The diagnostician's report from step 3 is passed to the SME in step 4
- The SME should acknowledge the diagnosis and follow its recommended approach
- The SME should write tests for each related failure mode the diagnostician identified

## Iteration Limits

**Maximum iterations:**
- Reproduction loop (step 2): 2 attempts, then escalate to user
- Fix verification loop (step 5): 3 attempts, then escalate to user
- Overall workflow: 12 total agent spawns (safety limit)

**Escalation to user:**
- Present current state
- Explain what's blocking progress
- Request guidance
