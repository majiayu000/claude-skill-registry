---
name: deferred-finding
description: Use when a review finding cannot be fixed in current PR - creates properly documented tracking issue with full context, linked to parent, following full issue-driven-development process
allowed-tools:
  - mcp__github__*
model: opus
---

# Deferred Finding

## Overview

Process for creating tracking issues when review findings cannot be addressed in the current PR.

**Core principle:** No finding disappears. Every deferral is tracked.

**ABSOLUTE REQUIREMENT:** Deferred findings MUST have tracking issues. There is no other option.

## When to Defer

A finding may ONLY be deferred when:

| Valid Reason | Example |
|--------------|---------|
| Out of scope | Finding requires architectural change beyond PR scope |
| External dependency | Requires infrastructure/config change |
| Breaking change | Would require major version bump |
| Separate concern | Logically independent from current work |

## Never Defer Without Tracking

| Invalid Approach | Reality |
|------------------|---------|
| "We'll fix it later" | Without tracking, later never comes |
| "It's minor" | Minor issues compound into major problems |
| "Not my problem" | You found it, you track it |
| "Good enough" | Good enough creates technical debt |

## Deferral Process

### Step 1: Verify Deferral is Appropriate

Ask yourself:
- Can this reasonably be fixed in this PR? If yes, FIX IT.
- Is there a valid reason from the "When to Defer" table?
- Have you tried to fix it first?

### Step 2: Determine Finding Details

Document:
- What is the finding?
- Why is it a problem?
- Where in the code?
- What's the severity?
- Why can't it be fixed now?

### Step 3: Create Tracking Issue

Use this template:

```markdown
## [Finding] [Brief description] (from #[PARENT])

### Origin

This issue was created during code review of #[PARENT_ISSUE].

| Property | Value |
|----------|-------|
| Parent Issue | #[PARENT_ISSUE] |
| Parent PR | #[PARENT_PR] (if exists) |
| Finding ID | F-[PARENT]-[N] |
| Severity | [CRITICAL/HIGH/MEDIUM/LOW] |
| Review Criterion | [Which of 7 criteria OR OWASP category] |
| Depth | [N] |

### Finding Details

**What was found:**
[Detailed description of the issue - be specific]

**Location:**
- File: `[path/to/file.ts]`
- Line(s): [N-M]
- Function: `[functionName()]`

**Why it matters:**
[Impact if not addressed - be concrete]

**Evidence:**
```[language]
[Code snippet showing the issue]
```

### Why Deferred

[Explain why this cannot be fixed in the parent PR]

| Reason | Details |
|--------|---------|
| Category | [out-of-scope / external-dependency / breaking-change / separate-concern] |
| Justification | [Specific explanation] |

### Acceptance Criteria

- [ ] [Specific criterion 1 - must be verifiable]
- [ ] [Specific criterion 2]
- [ ] [How to verify the fix]

### Links

- Parent Issue: #[PARENT_ISSUE]
- Review Comment: [Link to review artifact if applicable]

---
**Labels:** `review-finding`, `spawned-from:#[PARENT]`, `depth:[N]`, `[severity]`

*This issue follows the full issue-driven-development process including its own code review.*
```

### Step 4: Create Issue via CLI

```bash
gh issue create \
  --title "[Finding] Rate limiting needed on auth endpoint (from #123)" \
  --body "$(cat <<'EOF'
[Full template body here]
EOF
)" \
  --label "review-finding" \
  --label "depth:1" \
  --label "high"
```

Note: Create the `spawned-from:#N` label if it doesn't exist:
```bash
gh label create "spawned-from:#123" --color "C2E0C6" --description "Spawned from issue #123" 2>/dev/null || true
gh issue edit [NEW_ISSUE] --add-label "spawned-from:#123"
```

### Step 5: Update Review Artifact

Add the new issue to the "Findings Deferred" section:

```markdown
### Findings Deferred (With Tracking Issues)

| # | Severity | Finding | Tracking Issue | Justification |
|---|----------|---------|----------------|---------------|
| 1 | HIGH | Rate limiting needed | #456 | Requires infrastructure changes |
```

### Step 6: Update Parent Issue (If Deviation Required)

If the deferred finding BLOCKS the parent PR (e.g., critical security issue):

```bash
# Add awaiting label
gh issue edit 123 --add-label "status:awaiting-dependencies"

# Post deviation comment
gh issue comment 123 --body "$(cat <<'EOF'
## Deviation: Awaiting Dependencies

This issue cannot proceed until deferred findings are resolved.

| Property | Value |
|----------|-------|
| Blocked At | Step 9 (Code Review) |
| Dependencies | #456 |
| Reason | Critical deferred finding blocks PR |

Work will resume when #456 is complete.
EOF
)"
```

## Tracking Issue Lifecycle

Once created, the tracking issue:

1. **Is a first-class issue** - Full issue-driven-development process
2. **Gets its own review** - Cannot skip comprehensive-review
3. **May create its own deferrals** - Depth increments
4. **Closes independently** - Does not auto-close with parent

## Depth Tracking

| Depth | Meaning |
|-------|---------|
| 1 | Finding from original issue's review |
| 2 | Finding from a depth-1 issue's review |
| 3+ | Deeper nesting - flag for human attention |

At depth 3+:
```markdown
**Deep Finding Chain Detected**

This issue is at depth [N]. Chain:
- #100 (original)
  - #101 (depth 1)
    - #102 (depth 2)
      - #103 (depth 3) - Current

Consider: Is there a systemic issue requiring broader attention?
```

## Labels

Required labels for tracking issues:

| Label | Purpose |
|-------|---------|
| `review-finding` | Identifies as born from review |
| `spawned-from:#N` | Links to parent issue |
| `depth:N` | Tracks nesting level |
| `[severity]` | critical/high/medium/low |

Optional labels:
- `security` - Security-related finding
- `status:pending` - Ready for work

## Checklist

Before marking finding as deferred:

- [ ] Verified cannot fix in current PR
- [ ] Valid deferral reason documented
- [ ] Tracking issue created with full template
- [ ] Issue has all required labels
- [ ] Issue linked to parent
- [ ] Review artifact updated with tracking issue number
- [ ] Parent issue updated (if deviation required)

## Integration

This skill is called by:
- `apply-all-findings` - When finding cannot be fixed
- `comprehensive-review` - When documenting deferrals

This skill creates:
- New GitHub issues following full `issue-driven-development` process
- Deviation state on parent issue (if blocking)

This skill references:
- `issue-lifecycle` - Issue management
- `issue-driven-development` - Process for new issues
