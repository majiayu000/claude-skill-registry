---
name: issue-review
description: Perform iterative issue tracker review using Rule of 5 methodology. Reviews completeness, scope, dependencies, plan alignment, and executability.
---

# Iterative Issue Tracker Review (Rule of 5)

Perform thorough issue review using the Rule of 5 - iterative refinement until convergence.

## Setup

### Gathering Issues to Review

**For Beads:**
```bash
bd list                    # All issues
bd ready                   # Unblocked issues
bd graph                   # Dependency visualization
bd show <id>               # Individual issue details
bd dep tree                # Dependency tree
bd dep cycles              # Check for circular dependencies
```

**For GitHub Issues:**
```bash
gh issue list --label "needs-review" --json number,title,body,labels
gh issue view <number>
```

**For other systems:**
- Export issues to JSON/CSV
- Use API or CLI tools
- Provide issue data as input

## Process

Perform 5 passes, each focusing on different aspects. After each pass (starting with pass 2), check for convergence.

### PASS 1 - Completeness & Clarity

**Focus on:**
- Title clearly describes the work
- Description has enough context to implement
- File paths and changes are concrete (not vague)
- Success criteria or tests are defined
- No ambiguous or vague language
- Acceptance criteria clear

**Output format:**
```
PASS 1: Completeness & Clarity

Issues Found:

[CLRT-001] [CRITICAL|HIGH|MEDIUM|LOW] - Issue ID/Number
Title: [Issue title]
Description: [What's unclear or incomplete]
Evidence: [Why this is a problem]
Recommendation: [How to fix - specific command or action]

[CLRT-002] ...
```

**What to look for:**
- Vague titles: "Fix auth" (fix what?)
- No description or minimal description
- "Implement X" without saying how or where
- Missing file paths
- No verification steps
- Unclear done criteria

**For Beads:**
```bash
# Fix issues found
bd edit <id> description     # Update description
bd update <id> --title="New clear title"
```

**For GitHub:**
```bash
gh issue edit <number> --title "New title"
gh issue edit <number> --body "New description"
```

### PASS 2 - Scope & Atomicity

**Focus on:**
- Each issue represents one logical unit of work
- Issues not too large (should complete in one session)
- Issues not too small (trivial changes bundled appropriately)
- Clear boundaries between issues
- No overlapping scope between issues
- Each issue independently valuable

**Prefix:** SCOPE-001, SCOPE-002, etc.

**What to look for:**
- "Implement entire authentication system" (too large)
- "Fix typo in README line 42" (maybe too small, could bundle)
- Two issues both say "update user model"
- Issue requires changes across 10+ files
- Issue mixes refactoring with feature work

**For Beads:**
```bash
# Split large issues
bd create --title="Phase 1: ..." --description="..."
bd create --title="Phase 2: ..." --description="..."
bd dep add phase2-id phase1-id  # phase2 depends on phase1

# Merge small issues
bd close small-issue-1 --reason="merged into main-issue"
bd update main-issue --description="Now includes work from small-issue-1"
```

### PASS 3 - Dependencies & Ordering

**Focus on:**
- Dependencies correctly defined
- No missing dependencies (B needs A but not linked)
- No circular dependencies (A→B→C→A)
- Critical path is sensible
- Parallelizable work not falsely serialized
- Dependency rationale is clear

**Prefix:** DEP-001, DEP-002, etc.

**What to look for:**
- Issue requires another to be done but not linked
- Circular dependency chains
- Everything depends on one issue (bottleneck)
- No dependencies when clear order exists
- Dependencies prevent parallel work unnecessarily

**For Beads:**
```bash
# Check for problems
bd dep cycles                           # Find circular dependencies
bd dep tree                            # Visualize dependencies

# Fix dependencies
bd dep add <blocked-id> <blocker-id>   # Add missing dependency
bd dep remove <blocked-id> <blocker-id> # Remove incorrect dependency
```

**For GitHub:**
```bash
# Use labels and issue references
gh issue edit <number> --add-label "blocked-by-#123"
# Or reference in description: "Depends on #123"
```

### PASS 4 - Plan & Spec Alignment

**Focus on:**
- Issues trace back to plan phases
- Plan references in descriptions
- Related specs linked where applicable
- TDD approach clear (tests defined before impl)
- All plan phases have corresponding issues
- Issue breakdown matches plan structure

**Prefix:** ALIGN-001, ALIGN-002, etc.

**What to look for:**
- Plan has 5 phases but only 3 issues
- Issue doesn't reference source plan
- Plan says "test first" but issue doesn't mention tests
- Spec requirements not covered by any issue
- Issue contradicts plan approach

**For Beads:**
```bash
# Add plan reference
bd update <id> --description="...

Ref: plans/2026-01-12-feature.md#phase-2"
```

**For GitHub:**
```bash
gh issue edit <number> --body "...

Related Plan: `plans/2026-01-12-feature.md#phase-2`"
```

### PASS 5 - Executability & Handoff

**Focus on:**
- Can be picked up by any developer/agent
- No implicit knowledge required
- Verification steps clear and specific
- Handoff points defined for multi-issue work
- Priority and labels appropriate
- Estimation realistic (if used)

**Prefix:** EXEC-001, EXEC-002, etc.

**What to look for:**
- "You know what to do" (no, they don't)
- Assumes knowledge of previous conversations
- "Test it" without saying how
- No verification steps
- Priority/labels missing or incorrect

## Convergence Check

After each pass (starting with pass 2), report:

```
Convergence Check After Pass [N]:

1. New CRITICAL issues: [count]
2. Total new issues this pass: [count]
3. Total new issues previous pass: [count]
4. Estimated false positive rate: [percentage]

Status: [CONVERGED | ITERATE | NEEDS_HUMAN]
```

**Convergence criteria:**
- **CONVERGED**: No new CRITICAL, <10% new issues vs previous pass, <20% false positives
- **ITERATE**: Continue to next pass
- **NEEDS_HUMAN**: Found blocking issues requiring human judgment

**If CONVERGED before Pass 5:** Stop and report final findings.

## Final Report

After convergence or completing all passes:

```
## Issue Tracker Review Final Report

**System:** [Beads/GitHub/Linear/Jira]
**Scope:** [All issues / Milestone X / Labels Y]

### Summary

Total Issues Reviewed: [count]

Issues Found by Severity:
- CRITICAL: [count] - Must fix before work starts
- HIGH: [count] - Should fix before work starts
- MEDIUM: [count] - Consider addressing
- LOW: [count] - Nice to have

Convergence: Pass [N]

### Top 3 Most Critical Findings

1. [DEP-001] Circular dependency detected
   Issues: #42 → #43 → #44 → #42
   Impact: Cannot start any of these issues
   Fix: `bd dep remove 42 44` to break cycle

2. [SCOPE-002] Issue too large to complete
   Issue: #38 "Implement authentication system"
   Impact: Unmanageable scope, blocks other work
   Fix: Split into 5 issues for each plan phase

3. [CLRT-003] Missing implementation details
   Issue: #29 "Update API"
   Impact: Cannot implement without more info
   Fix: Add file paths, endpoints, and success criteria

### Recommended Actions

Provide specific commands for fixes:

**Beads Commands:**
```bash
# Fix circular dependency
bd dep remove 42 44

# Split large issue
bd create --title="Phase 1: Auth tokens" --description="..."
bd create --title="Phase 2: Auth middleware" --description="..."
bd dep add phase2-id phase1-id
bd close 38 --reason="split into phase issues"

# Update missing details
bd edit 29 description
# Then add: Files: api/routes.ts, api/handlers.ts; Tests: api/routes.test.ts
```

**GitHub Commands:**
```bash
gh issue edit 29 --body "...

Files to change:
- api/routes.ts
- api/handlers.ts
- api/routes.test.ts

Success criteria:
- [ ] Tests pass
- [ ] Endpoints return correct status codes"
```

### Verdict

[READY_TO_WORK | NEEDS_UPDATES | NEEDS_REPLANNING]

**Rationale:** [1-2 sentences explaining the verdict]

### Issue Quality Assessment

- **Clarity**: [Excellent|Good|Fair|Poor] - [brief comment]
- **Scope**: [Excellent|Good|Fair|Poor] - [brief comment]
- **Dependencies**: [Excellent|Good|Fair|Poor] - [brief comment]
- **Completeness**: [Excellent|Good|Fair|Poor] - [brief comment]
```

## Rules

1. **Reference specific issues** - Use issue IDs/numbers precisely
2. **Provide actionable commands** - Show exact commands to fix issues
3. **Check actual content** - Don't assume, verify with issue details
4. **Prioritize correctly**:
   - CRITICAL: Blocks all work (circular deps, missing info)
   - HIGH: Blocks specific work or causes confusion
   - MEDIUM: Could be clearer but workable
   - LOW: Minor improvements
5. **If converged before pass 5** - Stop and report
