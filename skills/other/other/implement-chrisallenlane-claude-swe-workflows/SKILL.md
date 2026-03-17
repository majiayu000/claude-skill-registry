---
name: implement
description: Iterative development workflow that coordinates implementation, refactoring, QA, and documentation agents to complete features systematically. Use when the user wants a full development workflow with quality checks.
model: opus
---

# Implement - Automated Development Workflow

Coordinates specialist agents through a complete development cycle: requirements -> planning -> implementation -> refactoring -> QA -> documentation.

## Workflow

### 1. Receive and clarify requirements

**Gather requirements from user:**
- What feature/bug/change is being requested?
- What are the acceptance criteria?
- Any constraints or preferences?

**Ask clarifying questions if needed:**
- Ambiguous requirements
- Missing information
- Multiple valid approaches

Loop back to user until requirements are clear.

### 2. Planning (Conditional)

**Assess task complexity:**

After requirements are clear, assess whether planning is warranted:

**Invoke `swe-planner` agent for complex tasks:**
- Large architectural changes (refactoring entire subsystems, technology migrations)
- Cross-cutting concerns (multi-tenancy, i18n, audit logging)
- Features touching many modules with unclear implementation path
- Changes requiring database migrations and backward compatibility
- Multiple valid approaches with significant trade-offs
- Tasks where diving straight into implementation risks going down wrong path

**Skip planning for simple tasks:**
- Single-file changes or small bug fixes
- Straightforward CRUD operations
- Simple refactorings (rename, extract method, remove duplication)
- Clear, well-defined changes with obvious implementation path
- Tasks that can be completed in <100 lines of code

**Note:** `swe-planner` has a safety valve to exit early if invoked for a task simpler than assessed. If planner reports "planning not needed," proceed directly to implementation with planner's brief recommendation.

**If planning invoked:**
- `swe-planner` will produce implementation plan with ordered sub-tasks
- Each sub-task includes: What/Why/How/Verify/Risks
- Plan identifies risk areas (prototyping needs, user decisions, performance/security concerns)
- Plan applies YAGNI, emphasizes starting small and working incrementally

**Use plan to guide implementation:**
- Implementation agent should follow plan's sequencing
- Implement one sub-task at a time
- Verify each sub-task before moving to next
- If plan identifies prototyping needs, create scratch repos in `/tmp` first

### 3. Implementation

**Detect project language/framework:**
- Check for language-specific files (go.mod, package.json, Cargo.toml, Dockerfile, Makefile, etc.)
- Determine which specialist agent to use

**Spawn appropriate implementation agent:**
- If Dockerfile changes: spawn `swe-sme-docker` agent
- If Makefile changes: spawn `swe-sme-makefile` agent
- If Golang project: spawn `swe-sme-golang` agent
- If GraphQL schema/resolvers: spawn `swe-sme-graphql` agent
- If Ansible playbooks/roles: spawn `swe-sme-ansible` agent
- If Zig project: spawn `swe-sme-zig` agent
- If TypeScript project (`.ts` files, `tsconfig.json`): spawn `swe-sme-typescript` agent
- If vanilla JavaScript (`.js` files, no TypeScript): spawn `swe-sme-javascript` agent
- If HTML/markup changes: spawn `swe-sme-html` agent
- If CSS/styling changes: spawn `swe-sme-css` agent
- Otherwise: implement directly with general best practices

**Pass plan to implementation agent if planning was done:**
- Implementation agent should follow plan's sequencing
- Work incrementally through sub-tasks
- Verify each step as specified in plan

**Implementation agent responsibilities:**
- Write code following language idioms
- Follow project conventions
- Handle edge cases and errors
- Write unit tests for pure functions as part of TDD (encouraged, not just QA's job)
- If following plan: implement sub-tasks sequentially, verify each before proceeding

### 4. Quality Assurance - Verify Acceptance Criteria (CRITICAL GATE)

**Spawn `qa-engineer` agent:**
- Pass original requirements and acceptance criteria to the agent
- The agent infers its mode from context: presence of acceptance criteria triggers acceptance verification
- Agent performs **practical verification first** - actually running/using the feature to confirm it works
- This means: executing CLI commands, spawning subagents to test MCP tools, making API calls, etc.
- Only AFTER practical verification confirms the feature works does the agent write unit tests
- This prevents the failure mode of "passing unit tests for broken code"

**Practical verification by feature type:**
- CLI tools: Run commands in subshell (skip destructive operations)
- MCP servers/Claude skills: Spawn subagent to actually use the feature
- API integrations: Make actual calls (with caution for dangerous operations)
- Libraries: Quick sanity checks, then unit tests

**This is a CRITICAL GATE:**
- Implementation must demonstrably work (practical test) AND have tests to proceed
- If practical verification fails: return to step 3 (implementation) immediately
- If verification passes but tests fail: debug tests, not implementation
- Track iteration count (max 3 attempts before escalating to user)

**Expected output:** Practical verification results, integration test recommendations, pass/fail determination with specific findings about each acceptance criterion.

### 5. Code Review (Conditional)

**Only proceed to code review if acceptance verification passed.** Don't review broken code.

Conditionally invoke specialized reviewers based on code changes and complexity. All reviewers provide feedback; implementation agent responds to all feedback in step 6.

#### 5a. Security Review (Conditional - Has Authority)

**If security-sensitive code changed (auth, crypto, input validation, data access):**

**Spawn `sec-blue-teamer` agent:**
- Evaluates defensive security posture of changed code
- Checks control consistency, defense-in-depth, and configuration
- Identifies systemic gaps that enable vulnerability classes
- **Has authority to demand changes** - security issues should block or require explicit user approval

**Output**: Defense evaluation with severity levels (critical/high/low)

#### 5b. Refactoring Review (Conditional - Advisory)

**If non-trivial implementation (>50 lines changed, multiple files, or complex logic):**

**Spawn `swe-refactor` agent:**
- Reviews implementation for code quality issues
- Identifies refactoring opportunities (DRY violations, dead code, complexity, etc.)
- Provides structured recommendations organized by priority
- Agent will report "No refactoring needed" if code is already clean

**Output**: Refactoring recommendations (advisory only)

#### 5c. Performance Review (Conditional - Advisory)

**If performance-critical code changed (hot paths, loops, database queries, API endpoints):**

**Spawn `swe-perf-engineer` agent:**
- Runs benchmarks and profiling
- Identifies performance bottlenecks
- Provides optimization recommendations

**Output**: Performance metrics and recommendations (advisory only)

### 6. Implement Review Feedback

**Aggregate all review feedback from step 5 and provide to implementation agent.**

**If specialist was used in step 3 (swe-sme-golang, swe-sme-graphql, etc.):**
- Re-invoke the same specialist agent that did implementation
- Provide all review feedback (security, refactoring, performance)
- Specialist reviews all feedback and **uses own discretion** to implement
- **Security findings**: Must address or get explicit user approval to skip
- **Other feedback**: Advisory only - specialist has final authority
- Specialist may decline recommendations that conflict with language idioms
- Specialist implements accepted changes and commits

**If no specialist (general implementation):**
- Re-invoke the same agent that did implementation in step 3
- Provide all review feedback
- Agent addresses security issues and implements accepted recommendations
- Agent commits changes

**Note**: Security issues have authority to block; other feedback is advisory. Implementation agent makes final decisions on advisory feedback.

### 7. SME Peer Review (Conditional)

**Condition:** Non-trivial changes (>50 lines changed, multiple files, or complex logic).

**Skip if:**
- Changes are trivial (single file, <50 lines, simple logic)
- No language-specific SME was used in step 3 (general implementation)

**If applicable, spawn a fresh instance of the same SME type used in step 3:**
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

### 8. Quality Assurance - Coverage & Quality Verification

**Spawn `qa-engineer` agent:**
- The agent infers its mode from context: absence of acceptance criteria triggers general assessment
- Agent performs general QA assessment of all changed code (from steps 3, 6, and 7)
- Assess test coverage for new/modified code
- Identify gaps and write missing tests
- Run linters/formatters and fix issues
- Evaluate test quality (assertions, edge cases)
- **Verify implementations from steps 6 and 7 didn't break tests** - catches issues from refactoring, security fixes, or peer review cleanups

**This is SUPPLEMENTARY:**
- Issues found here don't block the workflow by default
- Agent documents issues and proposes fixes
- Minor issues: proceed to documentation
- Significant issues (tests broken, major bugs): return to step 6 (review feedback) or step 3 (implementation)

**Expected output:** Coverage metrics, tests added/modified, quality issues found, confirmation that all changes still pass tests.

### Feedback Loops

**Acceptance verification failure (step 4):**
- Return to step 3 (implementation)
- Track iteration count (max 3 attempts before escalating to user)
- Report specific acceptance criteria that failed
- Report practical verification results (what was tried, what failed)

**Security review findings (step 5a):**
- Critical/High severity: Must address in step 6 or get explicit user approval to skip
- Medium/Low severity: Advisory - implementation agent decides in step 6

**Code review feedback (steps 5b-5c):**
- All refactoring and performance feedback is advisory
- Implementation agent in step 6 uses discretion to implement

**Peer review issues (step 7):**
- If peer review changes break tests: revert peer review changes and proceed (nits aren't worth breaking functionality)
- If peer review flags deeper issues: escalate to user for decision

**Coverage & quality issues (step 8):**
- Tests broken by changes from step 6: Return to step 6 to fix or revert
- Tests broken by changes from step 7: Revert step 7 changes (peer review nits shouldn't break tests)
- Major bugs found: Return to step 3 (implementation)
- Minor issues (low coverage in non-critical code, style nitpicks): document and proceed
- User can approve proceeding despite issues if acceptable

### 9. Documentation

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

### 10. Final verification

**Run comprehensive checks:**
- Execute full test suite (must pass)
- Run all linters and formatters
- Verify no new warnings introduced
- Check git status (document any uncommitted changes)

**Present summary to user:**
- Files changed
- Tests added/modified
- Coverage improvements
- Any remaining TODOs or follow-ups

**If verification fails:**
- Determine root cause (implementation bug vs. refactoring issue vs. test issue)
- Return to appropriate step (step 3 for implementation bugs, step 5 for refactoring issues)
- Report specific failures to user

### 11. Workflow Completion (Optional)

**After presenting summary from step 10, ask user if they want to complete the workflow.**

User may also explicitly request workflow completion at any point after step 10 succeeds.

**If user confirms, perform housekeeping tasks:**

#### 11a. Commit Changes

**If uncommitted changes exist:**
- Review git status to see what changed
- Create commit with descriptive message
- If ticket number is known (from branch name, prior context, or user input):
  - Reference ticket in commit message (e.g., "Fixes #123" or "Closes: #123")
- Include Co-Authored-By line: `Co-Authored-By: Claude <noreply@anthropic.com>`
- Use heredoc format for multi-line commit messages

**Example commit message format:**
```
Add user authentication with JWT tokens

Implements login/logout endpoints with refresh token rotation.
Includes rate limiting and CSRF protection.

Fixes #123

Co-Authored-By: Claude <noreply@anthropic.com>
```

#### 11b. Update/Close Issue Tracker Ticket (Conditional)

**Detect issue tracker:**
- Check for platform integration (CLI, MCP server, or API)
- Skip if not available

**Determine ticket number:**
- Try to extract from current branch name (e.g., `feature/123-add-auth` → #123)
- Check commit messages for ticket references
- Ask user for ticket number if not found and they indicated a ticket exists

**If ticket number identified:**
- Ask user: "Do you want to update and/or close ticket #123?"
  - Options: "Update only", "Update and close", "Skip"

**If user chooses to update:**
- Post comment with summary of changes:
  - List of files changed
  - Key changes made
  - Tests added
  - Documentation updated
- Use available integration to comment on issue

**If user chooses to close:**
- Close the ticket with final comment
- Use available integration to close issue

#### 11c. Sync with Main Branch (Conditional)

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
- ✓ Changes committed
- ✓ Ticket #123 updated and closed
- ✓ Branch rebased on main
- Ready to push or move to next task

## Agent Coordination

**Sequential execution:**
- Agents run one at a time (no parallel spawning)
- Each agent completes before next begins
- Use Task tool to spawn agents

**State management:**
- Track current workflow step
- Track QA iteration count (for acceptance verification failures)
- Accumulate summary information
- Preserve original requirements for passing to QA acceptance verification

**Agent self-skipping:**
- Agents should skip work if not applicable
- Report "nothing to do" rather than making unnecessary changes

**Planning pass-through:**
- If swe-planner produces a plan, pass it to implementation agent
- Implementation agent should acknowledge plan and follow it
- Plan helps coordinate implementation approach

**TDD coordination:**
- SWE agents are encouraged to write unit tests for pure functions during implementation
- QA agent focuses on practical verification and integration tests
- This prevents duplicate test-writing while ensuring comprehensive coverage

## Iteration Limits

**Maximum iterations:**
- Acceptance verification loop (step 4): 3 attempts, then escalate to user
- Overall workflow: 10 total agent spawns (safety limit)

**Escalation to user:**
- Present current state
- Explain what's blocking progress
- Request guidance
