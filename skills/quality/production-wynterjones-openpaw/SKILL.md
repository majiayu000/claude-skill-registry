---
name: production
description: Production readiness check from UX perspective - update BROWNFIELD.md with implemented features, check GREENFIELD alignment, note documentation impacts. Use when user says "go to production", "production check", "ready to ship", "pre-release check", or wants to verify implementation status before deployment.
allowed-tools: Read, Edit, Glob, Grep, Task
---

# Production Skill

Production readiness check focusing on implementation status and strategy alignment.

## When to Use
- Before production deployment
- Feature completion verification
- Strategy alignment check
- Documentation impact assessment

## Workflow

### Step 1: Update BROWNFIELD.md
Scan codebase and update `_OFFICE/BROWNFIELD.md`:

1. Identify implemented features:
   - Check routes and pages
   - Find feature directories
   - Look for user-facing components

2. Compare against last production snapshot

3. Document changes:
   - **Added:** New features since last production
   - **Removed:** Features that were removed
   - **Modified:** Significant changes

4. Update Production History table

### Step 2: Check Documentation Impacts
Scan changes against documentation:

**USER_GUIDE.md:**
- List features needing documentation updates
- Identify new features without docs

**ONBOARDING.md:**
- Check if onboarding elements need updates
- Identify new flows without guidance

### Step 3: Check GREENFIELD Alignment
Compare vision against implementation:

1. Read `_OFFICE/GREENFIELD.md` (vision)
2. Read `_OFFICE/BROWNFIELD.md` (reality)
3. Assess alignment: High / Medium / Low
4. Ask user about any perceived misalignment
5. Document strategy changes if needed

### Step 4: Generate Readiness Report

```
## Production Readiness: Implementation Check

### BROWNFIELD Status
- Last Updated: YYYY-MM-DD
- New Features: X added
- Removed Features: X removed
- Modified Features: X changed

### Documentation Impact
- USER_GUIDE.md needs updates: [list or "None"]
- ONBOARDING.md needs updates: [list or "None"]

### Strategy Alignment
- GREENFIELD vision: [summary]
- BROWNFIELD reality: [summary]
- Alignment: High/Medium/Low

### Recommendation
[Ready for production / Needs attention: ...]
```

### Step 5: Confirm with User
Ask: "Production check complete. Ready to proceed with deployment?"
Wait for explicit confirmation.

## Important
This skill checks implementation status. Use `/push` for code quality gates and pushing to remote.
