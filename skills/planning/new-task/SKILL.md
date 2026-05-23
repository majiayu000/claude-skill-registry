---
name: new-task
description: "Analyze task complexity and create actionable implementation plan with risk assessment"
---

# New Task Analysis

Analyze the following task and create a clear, actionable implementation plan.

## Task

$ARGUMENTS

## Analysis Framework

### 1. **Task Breakdown**
- Understand requirements
- Identify dependencies
- List affected files/components
- Estimate complexity (Small/Medium/Large)

### 2. **Complexity Assessment**
- **Small**: 1-2 hours (simple bug fix, minor feature)
- **Medium**: Half day to 1 day (new component, API endpoint)
- **Large**: 2-5 days (complex feature, multiple integrations)
- **Very Large**: 1+ week (major refactor, new subsystem)

### 3. **Risk Assessment**
Identify potential blockers:
- Unknown dependencies
- API limitations
- Data migration needs
- Breaking changes
- Third-party service issues

### 4. **Implementation Steps**

Create sequential, logical steps:
1. Setup/preparation
2. Backend changes
3. Frontend changes
4. Testing
5. Documentation
6. Deployment

### 5. **Success Criteria**

Define "done":
- Feature works as specified
- Tests pass
- No regressions
- Code reviewed
- Documented

## Output Format

### Task Analysis
- **Type**: [Bug Fix / Feature / Refactor / Infrastructure]
- **Complexity**: [Small / Medium / Large / Very Large]
- **Priority**: [High / Medium / Low]

### Implementation Plan

**Phase 1: [Name]**
- [ ] Step 1
- [ ] Step 2

**Phase 2: [Name]**
- [ ] Step 3
- [ ] Step 4

### Files to Modify/Create
```
app/page.tsx (modify)
components/NewComponent.tsx (create)
lib/utils.ts (modify)
```

### Dependencies
```bash
npm install package-name
```

### Testing Strategy
- Unit tests for X
- Integration tests for Y
- Manual testing steps

### Potential Issues
- Issue 1 and mitigation
- Issue 2 and mitigation

### Next Steps
1. Start with Phase 1, Step 1
2. Test incrementally
3. Commit often

Provide a clear, solo-developer-friendly plan that breaks down complex tasks into manageable steps.
