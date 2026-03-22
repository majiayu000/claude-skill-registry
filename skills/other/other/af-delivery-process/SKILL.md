---
name: af-delivery-process
description: Use when implementing features from mini-PRDs, writing code with TDD, running tests, or creating pull requests. Covers Red-Green-Refactor cycle, test-first development, PR creation workflow, and code review preparation.

# AgentFlow documentation fields
title: Delivery Process
created: 2025-10-29
updated: 2026-02-26
last_checked: 2026-02-26
tags: [skill, process, delivery, tdd, implementation]
parent: ../README.md
---

# Delivery Process

## Quick Reference

The delivery process transforms approved mini-PRDs into working code through iterative Test-Driven Development (TDD). Implementation happens in local development (localhost:3000 + Amplify sandbox) with continuous testing, documentation, and pull request creation.

**Typical duration:** 4-12 hours per feature
**End result:** Working code, passing tests, complete documentation, ready-for-review PR
**Scope:** Local development only (up to PR creation, not deployment)

## When to Use

**✅ Use Delivery Process for:**
- Implementing approved mini-PRDs from Refinement
- Writing code using TDD (Red → Green → Refactor)
- Running tests iteratively until clean
- Creating documentation and PRs

**❌ Not Delivery Phase:**
- Defining requirements (use Refinement)
- Deployment to production (separate process)
- Exploratory work without specs (use Discovery)

## Git Workflow

**Delivery work happens on issue branches** (see ADR-009).

```bash
# Start implementation (only works if Linear status >= "Approved")
start-work myproject JCN-123    # Creates issue worktree + tmux

# After PR merged, cleanup
stop-work myproject JCN-123     # Removes worktree + tmux
```

**Prerequisites:**
- Specs must be PRd from `specs` branch to `develop` first
- Linear status must be "Approved" or later
- `start-work` will warn if feature isn't ready

**Issue branches are short-lived** - they only exist during implementation. Specs (mini-PRD, scenarios) are already in `develop` from the Refinement phase.

See [Work Management Guide](../../docs/guides/work-management.md#branch-strategy-adr-009) for full branching details.

## Entry Criteria

Before starting Delivery, MUST have:
- ✅ Complete mini-PRD from Refinement phase
- ✅ Approved BDD scenarios with glossary compliance
- ✅ Visual specifications (Storybook stories for UI)
- ✅ Linear issue in "In Development" status
- ✅ Development environment ready (localhost + sandbox)
- ✅ Story points set on Linear issue (Refined Estimate preferred)

**Do NOT start Delivery without approved Refinement**

**Estimation check:** If the issue has no story points (`estimate` is null), flag this to the orchestrator before starting implementation. Load `af-estimation-expertise` and produce at minimum a Discovery Estimate. If only a Discovery Estimate exists (check comments for `[Discovery Estimate]` tag), consider whether a Refined Estimate is needed given that Refinement is now complete.

## Core Workflow

### TDD Cycle: Red → Green → Refactor

```
1. Write failing test (Red)
2. Write minimal code to pass (Green)
3. Refactor for quality
4. Repeat for next requirement
```

### Implementation Pattern

```
Implement → Test → Fix → Retest → Document → PR
```

**Key characteristic:** Iterative with continuous testing

### When Tests Are Written

**Refinement Phase (ALREADY DONE before Delivery):**
- Storybook stories with play functions (primary UI component tests) - PASSING
- RTL tests for non-visual logic (hooks, utils, state management) - PASSING
- Selector contract defined in mini-PRD Section 5
- Markdown scenarios written in mini-PRD Section 4

**Delivery Phase (RED):**
- AI generates E2E and Integration test files FROM scenarios + selector contract
- Test files go to `tests/e2e/` and `tests/integration/`
- These tests start as `test.todo()` (no backend/API yet) — visible in output as "todo" count
- Do NOT regenerate RTL or Storybook tests that already exist from Refinement

**Delivery Phase (GREEN):**
- Implementation makes E2E/Integration tests pass
- Components use selector contract: `data-testid={AUTH.signup.email}`
- Tests use same contract: `[data-testid="${AUTH.signup.email}"]`

**The selector contract is the bridge** between specifications, tests, and implementation. Single source of truth prevents drift.

### Step 1: Feature Implementation

**A. Start with test generation (RED)**
- Read BDD scenarios from mini-PRD Section 4
- Import selector contract from mini-PRD Section 5
- Verify existing tests from Refinement phase still pass (Storybook + RTL)
- Generate NEW test files for E2E and Integration only:
  - E2E → Playwright specs in `tests/e2e/`
  - Integration → Jest tests in `tests/integration/`
- New tests start as `test.todo('description')` (Red state) — never `test.skip()`

**B. Implement minimal code**
- Write code to make tests pass (Green state)
- Follow existing project patterns
- Keep changes focused on mini-PRD requirements

**C. Refactor for quality**
- Improve code structure
- Remove duplication
- Enhance readability
- Maintain all tests passing

### Step 2: Iterative Testing

**Because dev-test-agent is stateless, use iterative invocation pattern:**

**❌ Bad Pattern (won't work):**
```
Task → dev-test-agent: "Monitor tests while I fix issues"
# Agent can't maintain state across iterations
```

**✅ Good Pattern (will work):**
```
Task → dev-test-agent: "Run authentication tests"
# Agent reports: 3 failures
# Orchestrator fixes issues
Task → dev-test-agent: "Run authentication tests again"
# Agent reports: 1 failure
# Orchestrator fixes issue
Task → dev-test-agent: "Run authentication tests once more"
# Agent reports: All passing ✅
```

**Testing layers:**
1. **Unit tests** - Individual functions/components
2. **Integration tests** - API endpoints, data flow
3. **E2E tests** - Complete user flows (if configured)

### Step 3: Background Process Management

**Important:** Port numbers and backend configuration are defined in your project's `CLAUDE.md` file.

**Frontend (varies by framework):**
```bash
# Next.js, React, Vue, etc.
npm run dev &  # Start in background (port defined in CLAUDE.md)

# Check status
Task → dev-test-agent: "Check if frontend running on <port-from-CLAUDE.md>"

# Monitor errors
Task → dev-test-agent: "Check frontend console for errors"
```

**Backend (varies by stack):**

**AWS Amplify (AgentFlow default):**
```bash
npx ampx sandbox  # Start Amplify sandbox

# Verify APIs
Task → dev-test-agent: "Check if backend APIs responding"
```

**Other backends** (Express, Django, Flask, FastAPI, etc.):
- Configuration and startup commands in project's `CLAUDE.md`
- Each project defines its backend stack and ports
- Follow project-specific setup instructions

### Step 4: Documentation Creation

**After implementation is stable:**

**A. API Documentation**
```
Task → technical-writer-agent:
Input: "Create API documentation for auth endpoints"
Output: /docs/api/auth-endpoints.md
```

**B. Code Comments**
```
Task → technical-writer-agent:
Input: "Add JSDoc comments to auth service"
Output: Inline JSDoc in source files
```

**C. User Guides (if needed)**
```
Task → technical-writer-agent:
Input: "Create user guide for authentication flow"
Output: /docs/guides/authentication.md
```

### Step 5: Quality Validation

**A. Documentation Validation**
```
Task → docs-quality-agent:
Input: "Validate all documentation created"
Output: Validation report, auto-fixed issues
```

**B. Code Quality Check**
```
Task → quality-agent:
Input: "Check code quality standards"
Output: Code review, improvement suggestions
```

### Step 5.5: Coverage Validation

**Before creating PR, verify test coverage:**

```bash
npm run test:coverage
```

**Check for gaps:**
1. Open `coverage/lcov-report/index.html`
2. Review files with <80% coverage
3. Identify missing test cases:
   - API routes without unit tests
   - Utility functions without unit tests
   - Components without RTL tests
   - Error handling paths not covered

**Coverage categories:**

| Category | Target | Test Type |
|----------|--------|-----------|
| API routes | 85%+ | Unit (mocked deps) |
| Utility modules (`lib/`) | 80%+ | Unit or Integration |
| Components | 80%+ | RTL |
| Business logic | 90%+ | Unit |

**If coverage gaps found:**
- Write missing unit tests for infrastructure code
- BDD scenarios cover behaviour; infrastructure tests cover plumbing
- Add per-file thresholds for critical modules in `jest.config.js`

### Step 5.6: Local Code Review (Pre-PR)

**Before creating a PR, get fresh eyes on the diff:**

1. Spawn `af-code-quality-agent` with the full diff (`git diff develop...HEAD`)
2. Subagent reviews cold — same criteria as the GitHub CR Action:
   - Code quality and best practices
   - Potential bugs or issues
   - Performance considerations
   - Security concerns
   - Test coverage
3. Read findings, address substantive issues
4. If significant changes made, run the subagent again (max 2 local review cycles)
5. Local CR does NOT create Linear issues — findings go directly to the delivery agent

**Why fresh eyes:** The delivery agent built the code and has context bias. A subagent reviewing cold catches what the author misses — same principle as the GitHub CR, but faster (no round-trip).

### Step 6: Pull Request Creation

**Human Approval Gate:**
- ✋ Orchestrator presents changes summary
- ✋ Human approves PR creation

**PR creation includes:**
- Clean commit history
- Descriptive PR description referencing mini-PRD
- Links to Linear issue
- Test summary (all passing)
- Implementation notes

### Step 7: Post-PR Code Review Loop

**After creating the PR, the delivery agent stays "In Progress" through the full CR cycle:**

1. Post Linear comment: `[Delivery] PR #X created: <link>` (permanent artifact)
2. Post Zulip notification: "PR ready for review" (working conversation)
3. **Poll for CI/CR results** — use `gh pr checks <number>` and `gh pr reviews <number>`
4. When Claude Code Review comments arrive, read via `gh api repos/{owner}/{repo}/pulls/{number}/comments`
5. Address each comment, push fixes
6. Repeat steps 3-5 (max 3 GitHub CR cycles)
7. **When clean** → move to "In Review" + "Waiting for Feedback"
8. Agent hibernates — human merges

**CR escalation** (stop and ask the human via Zulip):
- 3 GitHub CR cycles with unresolved comments
- Same comment recurs after fix attempt
- CR suggests changes beyond original issue scope
- Architectural disagreement
- Cannot understand what CR is asking for

On escalation: post to Zulip with summary of unresolved comments and reason, set "Waiting for Feedback", hibernate.

**PR notifications:**
- **Linear comment**: Only the PR link (permanent artifact on the issue)
- **Zulip**: Everything else (PR created, CI results, CR status, escalation)
- **Status transitions**: Not notifications — Linear status IS the signal

**Scope ends at PR merge - deployment uses label-driven progression (see CLAUDE-agentflow.md)**

## Human-in-the-Loop Checkpoints

Orchestrator MUST pause for human input at:

1. **After initial implementation**
   - "Does this approach look correct?"
   - Verify implementation matches mini-PRD

2. **When tests fail repeatedly**
   - "Need help with this test failure"
   - Get guidance on tricky issues

3. **When technical limitation discovered** ⚠️
   - STOP immediately - do not work around it
   - "I discovered [TECH] doesn't support [CAPABILITY]"
   - Present options: re-scope, defer, or investigate alternatives
   - Wait for decision before continuing

4. **Before major refactoring**
   - "Should I refactor this for better structure?"
   - Confirm structural changes

5. **Before creating PR**
   - "Ready to create PR with these changes?"
   - Final approval gate

## Agent Coordination

### dev-test-agent (Stateless Testing)
**Purpose:** Execute tests and report results
**Pattern:** Iterative invocation (call → fix → call again)
**Limitations:** Cannot maintain state across calls
**Usage:** Each test run is independent

### technical-writer-agent (Documentation)
**Purpose:** Create documentation artifacts
**Outputs:**
- API documentation
- Component documentation
- JSDoc/TSDoc comments
- User guides

### code-quality-agent (Quality Review)
**Purpose:** Enforce coding standards
**Actions:**
- Review code patterns
- Suggest improvements
- Verify best practices

### docs-quality-agent (Validation)
**Purpose:** Validate documentation completeness
**Actions:**
- Check frontmatter compliance
- Verify bidirectional links
- Update last_checked dates

## Decision Points

### Should I refactor now or later?
- **Tests passing and code working?** → Refactor now (safe)
- **Tests failing?** → Fix tests first, then refactor
- **Major structural change?** → Get human approval first

### How much testing is enough?
- **Minimum:** All BDD scenarios passing
- **Standard:** + Unit tests for business logic
- **Comprehensive:** + Integration tests + E2E (if configured)

### When should I invoke agents?
- **Every code change?** → NO (too frequent)
- **After each test run?** → YES (for dev-test-agent)
- **After implementation complete?** → YES (for documentation/quality agents)

## Common Patterns

### API-Heavy Features
**Focus on:**
- GraphQL resolver implementation
- Database query optimization
- Error handling and validation
- API integration tests

### UI-Heavy Features
**Focus on:**
- Component implementation from Storybook stories
- State management
- Event handling
- Responsive design
- Accessibility (ARIA, keyboard nav)

### Data-Heavy Features
**Focus on:**
- Database migrations
- Data validation
- Query performance
- Backup/recovery procedures

## Output Artifacts

### 1. Working Code
- ✅ Feature implementation complete
- ✅ All tests passing (unit, integration, E2E)
- ✅ Code quality validated
- ✅ Follows project patterns
- ✅ No console errors or warnings

### 2. Documentation
- ✅ API documentation (if backend changes)
- ✅ Component documentation (if UI changes)
- ✅ JSDoc/TSDoc comments (inline)
- ✅ User guides (if complex feature)
- ✅ Architecture diagrams (if new patterns)

### 3. Pull Request
- ✅ Clean commit history
- ✅ Descriptive PR title and description
- ✅ Links to Linear issue and mini-PRD
- ✅ Test summary included
- ✅ Screenshots/videos (for UI changes)
- ✅ Ready for peer review

## Handling Implementation Blockers

**When you discover a technical limitation that prevents implementing a feature as specified:**

### ✅ MUST DO

1. **STOP immediately** - Do not continue implementation
2. **Inform the human** - Explain the limitation clearly:
   - What you were trying to implement
   - What technical constraint prevents it
   - What the impact is (feature won't work as spec'd)
3. **Return to Refinement** - The mini-PRD needs to be updated
4. **Wait for decision** - Human/PM decides:
   - Re-scope the feature (what CAN we build?)
   - Defer the feature (move to backlog)
   - Investigate alternatives (different approach?)

### ❌ MUST NOT DO

1. **Don't build mock/fake implementations**
   - "Illustrative" UI that doesn't actually work
   - Hardcoded data pretending to be real
   - Comments saying "this doesn't really work"

2. **Don't write tests that pass for broken features**
   - Tests should verify BEHAVIOR, not just UI presence
   - `toBeVisible()` ≠ "feature works"
   - A passing test must mean the feature works

3. **Don't make scope decisions alone**
   - "I'll just build what I can" - NO
   - "I'll add a note in the code" - NO
   - "The test passes so it's fine" - NO

### Why This Matters

**Bad outcome (what we're preventing):**
```
Spec: "User can view active sessions"
     ↓
Discovery: Platform doesn't support session listing
     ↓
❌ Dev builds mock UI with fake data
     ↓
❌ Dev writes test: "element is visible" ✓
     ↓
Test passes, feature broken, false confidence
```

**Good outcome (what we want):**
```
Spec: "User can view active sessions"
     ↓
Discovery: Platform doesn't support session listing
     ↓
✅ Agent STOPS and informs human
     ↓
✅ Return to Refinement phase
     ↓
✅ PM decides: Re-scope to "Sign out all devices" only
     ↓
✅ Mini-PRD updated, BDD scenarios updated
     ↓
✅ Implementation matches updated spec
     ↓
Test passes, feature works, real confidence
```

### Example Human Notification

When you hit a blocker, tell the human:

> **⚠️ Implementation Blocker**
>
> I discovered that [PLATFORM/TECH] does not support [CAPABILITY].
>
> **Spec says:** User can view their active sessions
> **Reality:** Cognito API does not provide session listing
>
> **Options:**
> 1. Re-scope: Only implement "Sign out all devices" (which IS supported)
> 2. Defer: Move feature to backlog, investigate custom session tracking later
> 3. Alternative: Implement custom session tracking (significant extra work)
>
> **I have NOT implemented any workarounds. Awaiting your decision.**

## Common Pitfalls

1. **Starting without approved Refinement**
   - Always verify mini-PRD is approved
   - Implementation without specs leads to rework

2. **Skipping tests**
   - TDD is mandatory, not optional
   - Tests document behavior and prevent regressions

3. **Not running tests iteratively**
   - dev-test-agent is stateless
   - Must call repeatedly after each fix

4. **Forgetting documentation**
   - Documentation is part of "done"
   - Undocumented code is incomplete

5. **Creating PR without human approval**
   - Always get approval before PR creation
   - Human validates implementation matches intent

6. **Deploying to production**
   - Delivery phase ends at PR creation
   - Deployment is separate approval process

7. **Working around technical limitations silently**
   - Never build mock/fake implementations
   - Never write tests that pass for broken features
   - Always escalate to human immediately

## Integration with Other Phases

**Before Delivery:**
- ← **Refinement Phase** - Provides approved mini-PRD and BDD scenarios

**After Delivery:**
- → **Code Review** - PR reviewed by team
- → **Deployment** - After PR approved and merged
- → **Monitoring** - Production monitoring and alerts

**Delivery provides:**
- Working implementation
- Complete test coverage
- Documentation
- Merge-ready PR

## Detailed Reference

**For complete delivery documentation:**
- Read `.claude/docs/guides/delivery-guide.md` (full workflow details)

**For testing strategies:**
- Load `af-testing-expertise` skill
- Read `.claude/docs/guides/testing-guide.md`

**For agent interactions:**
- Read `.claude/agents/dev-test-agent.md`
- Read `.claude/agents/technical-writer-agent.md`
- Read `.claude/agents/code-quality-agent.md`

## Success Criteria

Delivery complete when:
- ✅ All BDD scenarios passing (zero `test.todo()` remaining — all implemented)
- ✅ Unit tests passing (business logic covered)
- ✅ Integration tests passing (API endpoints verified)
- ✅ Zero `test.skip()` in committed code
- ✅ No console errors or warnings
- ✅ Code quality validated
- ✅ Documentation complete and validated
- ✅ Human has approved implementation
- ✅ PR created and linked to Linear issue
- ✅ Ready for peer review
