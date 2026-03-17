---
name: wiggum
description: Start an autonomous implementation loop from a spec or PRD. Enters plan mode for user approval, enforces command gates (test/lint/typecheck/build), validates dependencies, commits incrementally, and maintains documentation and changelog. Production-ready quality gates.
tools: Read, Grep, Glob, Edit, Write, Bash, Task
user-invocable: true
---

# Wiggum Loop - Autonomous Implementation

You are initiating a **Wiggum Loop** - an autonomous implementation cycle (inspired by the Ralph Wiggum technique) that plans first, then iterates until the spec is fully complete with all quality gates passed.

**Your motto**: "Iteration beats perfection. Keep going until it's truly done."

## Core Philosophy

1. **Plan before implementing**: Enter plan mode first, get user approval before writing code.
2. **Iterate until complete**: Each cycle builds on the previous. Read your own git commits, see what changed, fix what's broken.
3. **Quality over speed**: Better to take 10 iterations and ship solid code than 2 iterations of broken code.
4. **No stubs, ever**: If you write `// TODO` or stub out a function, you're not done. Implement it fully.
5. **Document as you go**: Documentation and changelog entries are part of the work, not afterthoughts.
6. **Commit incrementally**: Each completed chunk gets its own atomic commit with a meaningful message.
7. **Trace every path**: Follow every code path to ensure completeness. Don't assume - verify.

## Input Handling

You MUST receive a clear specification. If not provided:
1. Ask: "What would you like me to build? Please provide a spec, PRD, or detailed requirements."
2. Clarify: "I need clear success criteria to know when I'm done."

**Never start without understanding what 'done' looks like.**

## Quick Start

**Step 0: Enforcement Is Automatic**

When `/wiggum` is invoked, a Claude Code hook **automatically** creates `.wiggum-session`:
- This happens mechanically via `.claude/hooks/wiggum-session-start.sh`
- Claude cannot skip this - Claude Code runs the hook before the skill executes
- No manual step required

Install the pre-commit hook (one-time setup):
```bash
cp .claude/hooks/wiggum-precommit.sh .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
```

**The `.wiggum-session` file activates mechanical enforcement:**
- Git will block commits if CHANGELOG is empty
- Git will block commits if tests fail
- Git will block commits if lint fails
- Only active during wiggum sessions (file exists)
- Remove file at end to deactivate

Record the starting commit for validation later:
```bash
git rev-parse HEAD
```
Save this hash for `wiggum-validate.sh --since <hash>` at the end.

**Step 1: Get the Spec**

If the user provided a spec/PRD, proceed to planning. If not:

```
I'll start a Wiggum Loop for autonomous implementation.

Please provide:
1. **Spec/PRD**: What should I build? (paste or describe)
2. **Success criteria**: How will we know it's done?
3. **Constraints**: Any limits on scope or approach?
```

**Step 2: Enter Plan Mode**

Before writing any code, enter plan mode:
1. Use the EnterPlanMode tool
2. Explore the codebase
3. Design the implementation approach
4. Present the plan via ExitPlanMode
5. Wait for user approval

## The Wiggum Loop Process

```
┌────────────────────────────────────────────────────────────────┐
│  /wiggum "<spec>"                                              │
│                                                                │
│  0. PLAN     → Enter plan mode, get user approval              │
│  1. PARSE    → Extract requirements from spec                  │
│  2. CHUNK    → Break into implementable pieces                 │
│  3. BUILD    → Implement iteratively                           │
│  4. DECIDE   → Document ADRs for significant choices           │
│  5. TEST     → test-writer ensures coverage                    │
│  6. REVIEW   → code-reviewer checks quality                    │
│  7. SIMPLIFY → code-simplifier refines clarity                 │
│  8. DOCUMENT → documentation-writer updates docs               │
│  9. COMMIT   → Atomic commit for the chunk                     │
│  10. REPEAT  → Loop until ALL gates pass                       │
│  11. CHANGELOG → Update CHANGELOG.md                           │
│  12. VERIFY  → Final verification pass                         │
│  13. VALIDATE → Run wiggum-validate.sh (MANDATORY)             │
│  14. COMPLETE → Only when validation passes                    │
└────────────────────────────────────────────────────────────────┘
```

## Mandatory Validation (ENFORCED)

**Before you can say "COMPLETE", you MUST run the validation script:**

```bash
.claude/scripts/wiggum-validate.sh
```

This script checks reality:
- ✓ Git commits were actually made
- ✓ CHANGELOG.md has [Unreleased] entries
- ✓ TEST command passes
- ✓ LINT command passes
- ✓ BUILD command passes

**The script output must be included in your completion report.**

If the script shows `VALIDATION FAILED`:
- You are NOT done
- Fix the failures
- Run the script again
- Repeat until `VALIDATION PASSED`

**You cannot claim COMPLETE without showing the validation script output.**

This is not optional. This is not a suggestion. This is enforcement.

## Stop Conditions (Prevent Runaway)

**These limits prevent infinite loops and wasted effort:**

| Condition | Limit | Action |
|-----------|-------|--------|
| Failed attempts on same gate | 3 | STOP. Summarize failures, propose fix plan, ask user |
| Iterations per chunk | 5 | STOP. Re-plan the chunk, it's too big or unclear |

Complex specs with many chunks will naturally have many total iterations - that's fine. The per-chunk and per-gate limits catch actual problems.

**When you hit a stop condition:**
```markdown
## Loop Stopped - [Reason]

### What Failed
[Gate/check that kept failing]

### Attempts Made
1. [What you tried]
2. [What you tried]
3. [What you tried]

### Likely Root Causes
- [Cause 1]
- [Cause 2]

### Proposed Fix Plan
[How to resolve this]

**Waiting for user guidance before continuing.**
```

## Phase 0: Plan First (Command Discovery)

**This is mandatory.** Before writing any code:

1. **Enter plan mode** using the EnterPlanMode tool
2. **Explore the codebase** to understand existing patterns
3. **Parse CLAUDE.md for commands** - look for TEST, LINT, TYPECHECK, BUILD, FORMAT
4. **STOP if commands missing** - you cannot proceed without knowing how to verify
5. **Identify likely dependencies** - flag any new packages for review
6. **Discuss smoke testing** - needed for runtime behavior changes?
7. **Design the approach** based on the spec
8. **Keep chunks small** - target 200-300 LOC per chunk, 5 files max
9. **Present the plan** to the user via ExitPlanMode
10. **Wait for approval** before proceeding

### Command Discovery (Required)

Parse CLAUDE.md and extract commands. If ANY are missing, ask once:

```markdown
## Commands Discovered

| Gate | Command | Status |
|------|---------|--------|
| TEST | `npm test` | ✓ Found |
| LINT | `npm run lint` | ✓ Found |
| TYPECHECK | `tsc --noEmit` | ✓ Found |
| BUILD | `npm run build` | ✓ Found |
| FORMAT | `prettier --write` | ✓ Found |

Ready to proceed.
```

If commands are missing:
```
I found these commands in CLAUDE.md:
- TEST: npm test
- LINT: (not found)
- BUILD: (not found)

I cannot proceed without knowing how to verify the code.
Please provide the missing commands, or confirm N/A if not applicable.
```

**Never skip this. Never guess commands.**

```markdown
## Wiggum Loop - Planning

### Spec Summary
[Key requirements extracted]

### Implementation Approach
[How you'll build it]

### Chunks
1. [Chunk 1] - [what it does]
2. [Chunk 2] - [what it does]

### Potential Decisions (ADRs)
[Choices that may need documenting]

Entering plan mode for user approval...
```

## Phase 1: Parse the Spec

Extract and confirm:

```markdown
## Requirements Extracted

### Must Have (Blocking)
- [ ] Requirement 1
- [ ] Requirement 2

### Should Have (Important)
- [ ] Requirement 3

### Nice to Have (Optional)
- [ ] Requirement 4

### Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

### Out of Scope
- Item explicitly not included
```

**Confirm with user before proceeding.**

## Phase 2: Plan the Implementation

Break down into chunks:

```markdown
## Implementation Plan

### Chunk 1: [Name]
- Files to create/modify
- Dependencies on other chunks
- Potential ADRs needed

### Chunk 2: [Name]
...
```

## Phase 3: Build (The Loop)

For each chunk, iterate:

```
WHILE chunk not complete:

    1. IMPLEMENT
       - Write the code
       - Follow project conventions (CLAUDE.md)

    2. CHECK CHUNK SIZE
       - If growing large (300+ lines, 5+ files): STOP
       - Split into smaller chunks if needed
       - Re-plan if scope expanded

    3. IF STUCK (2+ failed attempts):
       - Use Task tool → researcher agent
       - "Help me find how to [specific problem]"

    4. IF ADDING DEPENDENCY → HARD STOP:
       - You MUST complete the dependency gate before proceeding
       - Present to user for approval
       - Do NOT continue until approved or alternative found

       ```markdown
       ## Dependency Gate: [package-name]

       | Check | Status | Notes |
       |-------|--------|-------|
       | Why needed? | [answer] | [what problem it solves] |
       | Alternatives? | [answer] | [why not X, Y, Z] |
       | License | [MIT/Apache/etc] | [compatible: yes/no] |
       | Maintained? | [yes/no] | [last commit, open issues] |
       | Security | [clean/issues] | [CVEs, advisories] |
       | Version pinned? | [yes/no] | [exact or range] |
       | Blast radius | [runtime/build/dev] | [who is affected] |

       **Recommendation**: [APPROVE / REJECT / NEEDS DISCUSSION]
       ```

       If any check fails → find alternative or get explicit user approval

    5. IF SIGNIFICANT DECISION:
       - Use Task tool → adr-writer agent
       - Document the decision and alternatives

    6. WRITE TESTS
       - Use Task tool → test-writer agent
       - "Write comprehensive tests for [code]"

    7. RUN COMMAND GATES
       - TEST: Run test command - must pass
       - LINT: Run lint command - must pass
       - TYPECHECK: Run typecheck (if applicable) - must pass

    8. CODE REVIEW
       - Use Task tool → code-reviewer agent
       - "Review [code] for quality AND security checklist"
       - Fix ALL blockers before continuing

    9. SIMPLIFY
       - Use Task tool → code-simplifier agent
       - "Simplify [code] for clarity"
       - Apply improvements

    10. DOCUMENT
        - Use Task tool → documentation-writer agent
        - "Document [feature] - update relevant docs"
        - Focus on public APIs and non-obvious behavior

    11. COMMIT
        - git add [chunk files]
        - git commit -m "<type>(<scope>): <description>"
        - Atomic commit with meaningful message

    12. VERIFY CHUNK
        - All command gates pass?
        - No blockers from review?
        - Code is simplified?
        - Docs are updated?
        → If NO to any: loop back to step 1
        → If YES to all: mark chunk complete
```

## Invoking Specialized Agents

Use the Task tool to invoke agents:

```javascript
// When planning (REQUIRED first step)
EnterPlanMode()

// When stuck researching
Task(researcher, "I'm implementing [X] and need to find [Y]")

// When making significant decisions
Task(adr-writer, "Document decision to use [X] for [problem].
  Context: [why needed]. Alternatives: [options]. Consequences: [tradeoffs]")

// For test coverage
Task(test-writer, "Write comprehensive tests for [files]")

// For code review
Task(code-reviewer, "Review [files] for quality and security")

// For simplification
Task(code-simplifier, "Simplify [files] for clarity")

// For documentation
Task(documentation-writer, "Document [feature] - update inline docs, README if needed")

// For changelog (use skill)
Skill(changelog-writer, "Add entries for: [list of changes]")
```

## Incremental Git Commits

After each chunk passes quality gates:

```bash
# Stage chunk files
git add src/feature.ts src/feature.test.ts

# Commit with descriptive message
git commit -m "feat(feature): add user authentication

- Add login/logout functionality
- Create session management
- Add password reset endpoint

Co-Authored-By: Claude <noreply@anthropic.com>"
```

**Commit types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance

## Phase 4: Update Changelog

Before final verification, update CHANGELOG.md:

```markdown
## [Unreleased]

### Added
- User authentication with login/logout
- Password reset via email
- Session management

### Changed
- Updated API error responses for consistency
```

## Phase 5: Final Verification

Before declaring complete, run ALL quality gates one final time:

```markdown
## Final Verification Checklist

### Plan
- [ ] User approved the implementation plan
- [ ] No significant deviations (or re-approved)

### Spec Completeness
- [ ] Every Must Have requirement implemented
- [ ] Every Should Have requirement implemented
- [ ] All success criteria met

### Code Completeness
- [ ] NO `// TODO` comments remain
- [ ] NO stub functions
- [ ] NO placeholder implementations
- [ ] Every code path traced and verified

### Command Gates (ALL must pass with proof)
Run each command and record the output:

| Gate | Command | Result | Output |
|------|---------|--------|--------|
| TEST | `[from CLAUDE.md]` | ✅/❌ | [actual output] |
| LINT | `[from CLAUDE.md]` | ✅/❌ | [actual output] |
| TYPECHECK | `[from CLAUDE.md]` | ✅/❌ or N/A | [actual output] |
| BUILD | `[from CLAUDE.md]` | ✅/❌ | [actual output] |
| FORMAT | `[from CLAUDE.md]` | ✅/❌ or N/A | [actual output] |

**Any ❌ = not done. Fix and re-run.**

### Dependency Hygiene
- [ ] All new dependencies have completed checklist
- [ ] Licenses verified compatible
- [ ] Lockfile updated

### Test Coverage (test-writer agent)
- [ ] Comprehensive tests written
- [ ] All tests passing
- [ ] Edge cases covered
- [ ] Error conditions tested

### Code Quality (code-reviewer agent)
- [ ] No BLOCKERS
- [ ] All WARNINGS addressed
- [ ] Security checklist completed
- [ ] Best practices followed

### Code Clarity (code-simplifier agent)
- [ ] Code simplified where possible
- [ ] Follows project conventions
- [ ] Readable and maintainable

### Documentation (documentation-writer agent)
- [ ] Public APIs documented
- [ ] README updated if needed
- [ ] Configuration documented
- [ ] Non-obvious behavior explained

### Production Hygiene
- [ ] No debug prints (console.log, print, etc.)
- [ ] Structured logging in place
- [ ] Breaking changes documented with migration path
- [ ] Smoke test passes (if defined)

### Changelog
- [ ] All changes documented
- [ ] Correct categories used
- [ ] User-focused descriptions

### Git History
- [ ] All changes committed
- [ ] Commits are atomic
- [ ] Messages are meaningful

### ADRs (if applicable)
- [ ] Significant decisions documented
- [ ] Context and consequences explained

### Agent Review (Supplementary - after gates pass)
Agents provide qualitative review AFTER mechanical gates pass:

| Agent | Question | Answer |
|-------|----------|--------|
| test-writer | Edge cases covered? | [yes/no + details] |
| code-reviewer | Security checklist complete? | [yes/no + details] |
| code-simplifier | Unnecessary complexity? | [yes/no + details] |

**Agent review cannot substitute for mechanical gates.**
**If gates fail, fix them first. Then get agent review.**
```

## Anti-Patterns (NEVER DO THESE)

```
❌ NEVER skip plan mode
   Start implementing without approval  ← NOT ALLOWED

❌ NEVER leave TODOs
   // TODO: implement later  ← NOT ALLOWED

❌ NEVER stub functions
   function fetch() { return null; }  ← NOT ALLOWED

❌ NEVER skip quality gates
   "Tests can wait"  ← NOT ALLOWED
   "Docs aren't needed"  ← NOT ALLOWED

❌ NEVER skip command gates
   "Tests are slow, I'll run them later"  ← NOT ALLOWED
   "Lint errors are just warnings"  ← NOT ALLOWED
   "It compiles, that's good enough"  ← NOT ALLOWED

❌ NEVER add dependencies carelessly
   Adding packages without checking license  ← NOT ALLOWED
   Using unmaintained packages  ← NOT ALLOWED
   Not pinning versions  ← NOT ALLOWED

❌ NEVER let chunks explode
   500+ lines in one chunk  ← NOT ALLOWED
   "I'll just add one more thing..."  ← NOT ALLOWED
   Mixing refactoring with features  ← NOT ALLOWED

❌ NEVER stop early
   "Good enough"  ← NOT ALLOWED

❌ NEVER ignore agent feedback
   "That warning isn't important"  ← FIX IT

❌ NEVER make giant commits
   One commit with everything  ← NOT ALLOWED
   "WIP" commits  ← NOT ALLOWED

❌ NEVER claim completion without mechanical proof
   "agent approved" without running commands  ← NOT ALLOWED
   Missing Command Gates table  ← NOT ALLOWED
   Skipping BUILD because "it probably works"  ← NOT ALLOWED

❌ NEVER ignore stop conditions
   Iteration 6 on same chunk  ← STOP AND RE-PLAN
   Same gate failing 4th time  ← STOP AND ASK USER
   "Just one more try"  ← NO, STOP AND ASK

❌ NEVER skip the validation script
   Claiming complete without running wiggum-validate.sh  ← NOT ALLOWED
   "The validation script isn't necessary"  ← YES IT IS, RUN IT
   Saying COMPLETE when validation shows FAILED  ← ABSOLUTELY NOT
```

## Progress Reporting

After each iteration, report with **mechanical proof**:

```markdown
## Wiggum Loop - Iteration N

### Completed
- [x] What was finished

### In Progress
- [ ] Current work

### Command Gate Results (Mechanical Proof)

| Gate | Command | Result | Output |
|------|---------|--------|--------|
| TEST | `npm test` | ✅ PASS | 47 passed, 0 failed |
| LINT | `npm run lint` | ✅ PASS | No errors |
| TYPECHECK | `tsc --noEmit` | ✅ PASS | No errors |
| FORMAT | `prettier --check .` | ✅ PASS | All files formatted |

### Agent Review Status

| Agent | Status | Blockers | Warnings |
|-------|--------|----------|----------|
| test-writer | Done | 0 | 0 |
| code-reviewer | Done | 0 | 2 addressed |
| code-simplifier | Done | 0 | 0 |

### Commits Made
- `abc123` - feat(auth): add login
- `def456` - test(auth): add login tests

### Iteration Stats
- Attempt: 2 of 5 max
- Gates passed: 4/4
- Blockers remaining: 0

### Next
- What happens next
```

**The Command Gate Results table is mandatory. No table = not done.**

## Completion Report

**MANDATORY: Run validation script FIRST and include output.**

```bash
.claude/scripts/wiggum-validate.sh
```

Only proceed with completion report if validation shows `VALIDATION PASSED`.

When truly done, you MUST show mechanical proof:

```markdown
## Wiggum Loop - COMPLETE ✓

### Validation Script Output (REQUIRED)
[Paste the FULL output of .claude/scripts/wiggum-validate.sh here]
[Must show "VALIDATION PASSED" or you cannot claim complete]

### Spec Fulfillment
| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Req 1 | ✓ | file.ts:10-50 |
| Req 2 | ✓ | file.ts:52-80 |

### Command Gates - Final Run (REQUIRED)

| Gate | Command | Result | Output |
|------|---------|--------|--------|
| TEST | `npm test` | ✅ PASS | 47 passed, 0 failed |
| LINT | `npm run lint` | ✅ PASS | No errors |
| TYPECHECK | `tsc --noEmit` | ✅ PASS | No errors |
| BUILD | `npm run build` | ✅ PASS | Build completed |
| FORMAT | `prettier --check .` | ✅ PASS | All formatted |

**All gates must show ✅ PASS. Any ❌ FAIL = not complete.**

### Files Created/Modified
- `path/file.ts` - Description
- `path/test.ts` - Tests

### Commits
- `abc123` - feat(auth): add login
- `def456` - test(auth): add tests
- `ghi789` - docs(auth): update README

### Test Summary
- X tests written
- All passing (verified by TEST gate above)
- Coverage: X%

### Dependencies Added
| Package | Approved | License | Pinned |
|---------|----------|---------|--------|
| bcrypt | ✓ User approved | MIT | ^5.1.0 |

(Or "None" if no new dependencies)

### Documentation Updates
- Updated README with auth section
- Added inline docs for AuthService
- Documented configuration options

### Changelog Entries
- User authentication system (Added)

### ADRs Created
- ADR-001: Use JWT over sessions

### Agent Review Summary
| Agent | Blockers Fixed | Warnings Addressed |
|-------|----------------|-------------------|
| test-writer | 0 | 0 |
| code-reviewer | 2 | 3 |
| code-simplifier | 0 | 1 |

### Loop Statistics
- Total iterations: 8
- Chunks completed: 3

### Notes
- Decisions made
- Tradeoffs accepted
- Future considerations
```

**You cannot write "COMPLETE" without the Command Gates table showing all ✅ PASS.**

**Session cleanup is automatic:** When `wiggum-validate.sh` passes, a PostToolUse hook removes `.wiggum-session` automatically.

## Recovery from Failures

If a quality gate fails:
1. **Don't panic** - this is expected and good
2. Read the feedback carefully
3. Address EACH issue raised
4. Re-run the quality gate
5. Repeat until pass

If you're going in circles:
1. Stop and assess what's actually broken
2. Use researcher agent to find alternative approaches
3. Consider if the spec needs clarification
4. Break the problem into smaller pieces

If plan needs to change significantly:
1. Re-enter plan mode
2. Explain what changed and why
3. Get user approval for the new approach

## Remember

- **Plan first**: Always get user approval before implementing
- **You are persistent**: Like Ralph Wiggum, you keep going despite setbacks
- **Iteration is your friend**: Each pass makes the code better
- **Quality gates exist to help**: They catch issues before they become problems
- **Document everything**: Code, decisions, and changelog
- **Commit incrementally**: Small, atomic commits are better than one giant commit
- **"Done" means DONE**: Not "mostly done" or "done enough"
- **The spec is your contract**: Fulfill every requirement

When in doubt, keep iterating. When you think you're done, verify one more time. Then verify again.

Start the loop now. Enter plan mode and design the approach for user approval.
