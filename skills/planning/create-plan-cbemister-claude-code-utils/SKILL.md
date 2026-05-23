---
name: create-plan
description: Initialize a feature development plan with phases and task tracking
---

# Create Feature Plan

Initialize a structured plan for feature development with phases, tasks, and tracking.

## When to Use

Use this when:
- Starting a complex feature requiring multiple steps
- Want to track progress through development phases
- Need to break down large features into manageable parts
- Working with worktrees and want integrated planning

## Usage

```
/create-plan <feature-name> [--template=TYPE]
```

**Arguments:**
- `feature-name` - Name of the feature (kebab-case)
- `--template` - Optional template type (feature, bugfix, refactor, migration)

## Instructions

### Step 1: Validate and Normalize Input

```bash
if [ -z "$1" ]; then
  echo "Error: Feature name required"
  echo "Usage: /create-plan <feature-name> [--template=TYPE]"
  echo ""
  echo "Templates: feature (default), bugfix, refactor, migration"
  exit 1
fi

# Convert to kebab-case
FEATURE_NAME=$(echo "$1" | tr '[:upper:]' '[:lower:]' | tr '_' '-' | tr ' ' '-')

# Extract template type
TEMPLATE="feature"
if [[ "$2" == --template=* ]]; then
  TEMPLATE="${2#*=}"
fi

PLAN_DIR="plans/active/$FEATURE_NAME"
```

### Step 2: Check if Plan Already Exists

```bash
if [ -d "$PLAN_DIR" ]; then
  echo "⚠️  Plan already exists at: $PLAN_DIR"
  read -p "Overwrite existing plan? (y/n) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Plan creation cancelled"
    exit 1
  fi
  rm -rf "$PLAN_DIR"
fi
```

### Step 3: Create Plan Directory

```bash
mkdir -p "$PLAN_DIR"
echo "Creating plan at: $PLAN_DIR"
```

### Step 4: Generate Plan from Template

**Feature Template (Default):**

```bash
if [ "$TEMPLATE" == "feature" ]; then
  cat > "$PLAN_DIR/plan.md" <<'EOF'
---
title: [Feature Title]
type: feature
status: planning
created: $(date +%Y-%m-%d)
worktree: $FEATURE_NAME
phases:
  - id: research
    status: pending
  - id: design
    status: pending
  - id: implementation
    status: pending
  - id: testing
    status: pending
---

# [Feature Name]

## Overview
[Brief description of what this feature does and why it's needed]

## User Story
As a [user type]
I want [goal]
So that [benefit]

## Success Criteria
- [ ] [Functional criterion 1]
- [ ] [Functional criterion 2]
- [ ] [Non-functional criterion - performance, accessibility, etc.]
- [ ] Tests pass
- [ ] Documentation updated

---

## Phases

### Phase 1: Research
**Status:** Pending
**Estimated:** [X days]

**Objectives:**
- Understand requirements
- Research existing solutions
- Identify technical approach

**Tasks:**
- [ ] Review user requirements
- [ ] Research similar features
- [ ] Document technical approach
- [ ] Identify dependencies

**Outcome:** Technical specification document

---

### Phase 2: Design
**Status:** Pending
**Estimated:** [X days]

**Objectives:**
- Design data models
- Design API interfaces
- Design UI/UX

**Tasks:**
- [ ] Database schema design
- [ ] API endpoint design
- [ ] UI wireframes/mockups
- [ ] Review design with team

**Outcome:** Approved design specifications

---

### Phase 3: Implementation
**Status:** Pending
**Estimated:** [X days]

**Objectives:**
- Build core functionality
- Implement UI
- Integrate components

**Tasks:**
- [ ] Database migrations
- [ ] API endpoint implementation
- [ ] UI component development
- [ ] Integration work
- [ ] Error handling
- [ ] Logging/monitoring

**Outcome:** Working feature in development environment

---

### Phase 4: Testing
**Status:** Pending
**Estimated:** [X days]

**Objectives:**
- Ensure quality
- Verify all criteria met
- Performance testing

**Tasks:**
- [ ] Unit tests
- [ ] Integration tests
- [ ] E2E tests
- [ ] Manual testing
- [ ] Performance testing
- [ ] Accessibility testing
- [ ] Code review

**Outcome:** Production-ready feature

---

## Technical Details

### Database Changes
- Tables to create/modify
- Indexes needed
- Migration strategy

### API Changes
- New endpoints
- Modified endpoints
- Breaking changes (if any)

### UI Changes
- New components
- Modified components
- Routes added

### Dependencies
- External libraries
- Internal services
- Third-party APIs

---

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [Strategy] |
| [Risk 2] | High/Med/Low | High/Med/Low | [Strategy] |

---

## Open Questions
- [ ] Question 1
- [ ] Question 2

## Notes
[Any additional context, decisions, or considerations]

---

## Timeline
- **Start Date:** [YYYY-MM-DD]
- **Target Completion:** [YYYY-MM-DD]
- **Actual Completion:** [YYYY-MM-DD]

EOF
fi
```

**Bugfix Template:**

```bash
if [ "$TEMPLATE" == "bugfix" ]; then
  cat > "$PLAN_DIR/plan.md" <<'EOF'
---
title: [Bug Title]
type: bugfix
status: investigating
severity: high | medium | low
created: $(date +%Y-%m-%d)
worktree: $FEATURE_NAME
phases:
  - id: investigation
    status: pending
  - id: fix
    status: pending
  - id: verification
    status: pending
---

# Bug: [Bug Title]

## Problem Description
[Clear description of the bug and its impact]

## Reproduction Steps
1. Step 1
2. Step 2
3. Step 3

**Expected:** [What should happen]
**Actual:** [What actually happens]

## Impact
- **Users Affected:** [All users, specific segment, etc.]
- **Severity:** [High/Medium/Low]
- **Business Impact:** [Revenue, UX, reputation, etc.]

---

## Investigation

### Symptoms
- Symptom 1
- Symptom 2

### Initial Findings
- Finding 1
- Finding 2

### Root Cause
[To be determined during investigation]

---

## Fix Plan

### Phase 1: Investigation
**Tasks:**
- [ ] Reproduce bug locally
- [ ] Identify root cause
- [ ] Document affected code paths
- [ ] Assess scope of fix

### Phase 2: Implementation
**Tasks:**
- [ ] Implement fix
- [ ] Add test for this bug
- [ ] Update related code if needed
- [ ] Code review

### Phase 3: Verification
**Tasks:**
- [ ] Verify fix works locally
- [ ] Run full test suite
- [ ] Deploy to staging
- [ ] QA verification
- [ ] Monitor after production deploy

---

## Solution
[Description of the fix once implemented]

## Prevention
[How to prevent similar bugs in the future]

EOF
fi
```

### Step 5: Create Initial Sub-Plans (Optional)

```bash
# Create first phase sub-plan
cat > "$PLAN_DIR/01-research.md" <<'EOF'
---
parent: $FEATURE_NAME
phase: research
status: pending
started: null
completed: null
---

# Phase 1: Research

## Objectives
[What we're trying to learn/understand]

## Current Understanding
[What we know so far]

## Questions to Answer
- [ ] Question 1
- [ ] Question 2

## Research Tasks
- [ ] Task 1
- [ ] Task 2

## Findings
[To be filled in during research]

## Next Steps
[What comes after research phase]

EOF

echo "Created initial sub-plan: 01-research.md"
```

### Step 6: Link to Worktree (if exists)

```bash
WORKTREE_PATH="worktrees/$FEATURE_NAME"
if [ -d "$WORKTREE_PATH" ]; then
  echo ""
  echo "📁 Linked to existing worktree: $WORKTREE_PATH"
fi
```

### Step 7: Output Success Message

```bash
echo ""
echo "✅ Plan created successfully!"
echo ""
echo "📋 Plan location: $PLAN_DIR/plan.md"
echo "📝 Template used: $TEMPLATE"
echo ""
echo "Next steps:"
echo "1. Edit $PLAN_DIR/plan.md to fill in details"
echo "2. Use /plan-status to track progress"
if [ ! -d "$WORKTREE_PATH" ]; then
  echo "3. Create worktree: /worktree-create $FEATURE_NAME"
fi
echo ""
echo "Phase management:"
echo "- Update phase status in plan.md frontmatter"
echo "- Create sub-plans for each phase (01-research.md, 02-design.md, etc.)"
```

## Example Usage

**Create feature plan:**
```bash
/create-plan user-authentication
```

**Create bugfix plan:**
```bash
/create-plan payment-failure --template=bugfix
```

**Create refactor plan:**
```bash
/create-plan api-modernization --template=refactor
```

## Plan Structure

```
plans/
└── active/
    └── feature-name/
        ├── plan.md              # Master plan
        ├── 01-research.md       # Phase 1 sub-plan
        ├── 02-design.md         # Phase 2 sub-plan
        ├── 03-implementation.md # Phase 3 sub-plan
        └── 04-testing.md        # Phase 4 sub-plan
```

## Best Practices

**Before Creating Plan:**
- Understand the feature requirements
- Know your success criteria
- Estimate rough timeline

**During Planning:**
- Break large features into 3-5 phases
- Each phase should be 1-5 days of work
- Include verification steps in each phase
- Document risks and dependencies

**Maintaining Plans:**
- Update status as you progress
- Add notes and decisions
- Track open questions
- Move completed plans to archive

## Integration with Worktrees

Plans and worktrees work together:

```bash
# Option 1: Create plan first
/create-plan user-auth
# Edit plan
/worktree-create user-auth

# Option 2: Create worktree first
/worktree-create user-auth
# Plan is auto-created
# Edit the generated plan
```

## Tips

**Phase Breakdown:**
- Research: 10-20% of time
- Design: 15-25% of time
- Implementation: 40-50% of time
- Testing: 20-30% of time

**Task Granularity:**
- Each task should be < 4 hours
- Checkboxes make progress visible
- Link to specific files/PRs

**Success Criteria:**
- Should be testable/verifiable
- Include non-functional requirements
- Think about edge cases
