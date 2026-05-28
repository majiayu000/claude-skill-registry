---
name: reset
description: Restructure Dex system based on new role or preferences
disable-model-invocation: true
---

## Purpose

Re-run the onboarding flow to restructure your Dex system. Useful when:
- Your role changes (promotion, new job, pivot)
- You want to reorganize after using Dex for a while
- You're experimenting with different structures
- Your company size tier changes (startup → scaling, etc.)

## Behavior

When the user types `/reset`, execute the following:

### Step 1: Acknowledge and Explain

Say: "Let's reset your Dex setup. I'll walk you through the same questions as initial setup, then reorganize your structure. **Your existing content will be preserved** - I'll move files to match the new structure, not delete them."

### Step 2: Current State Check

Before asking questions, check and display:
- Current role (from CLAUDE.md User Profile section)
- Current company size
- Current pillars
- Existing folder structure

Say: "Here's your current setup: [summary]. Want to change it?"

### Step 3: Role Selection (if changing)

If user wants to change role, present the numbered role list:

```
**Core Functions**
1. Product Manager
2. Sales / Account Executive
3. Marketing
4. Engineering
5. Design

**Customer-Facing**
6. Customer Success
7. Solutions Engineering

**Operations**
8. Product Operations
9. RevOps / BizOps
10. Data / Analytics

**Support Functions**
11. Finance
12. People (HR)
13. Legal
14. IT Support

**Leadership**
15. Founder

**C-Suite**
16. CEO
17. CFO
18. COO
19. CMO
20. CRO
21. CTO
22. CPO
23. CIO
24. CISO
25. CHRO / Chief People Officer
26. CLO / General Counsel
27. CCO (Chief Customer Officer)

**Independent / Advisory**
28. Fractional CPO
29. Consultant
30. Coach

Type a number, or describe your role:
```

### Step 4: Company Size (if changing)

```
1. 1-100 people (startup/small)
2. 100-1,000 people (scaling)
3. 1,000-10,000 people (enterprise)
4. 10,000+ people (large enterprise)
```

### Step 5: Priorities (if changing)

Ask: "What are your 2-3 main priorities right now?"

### Step 6: Migration Plan

Before making changes, show the user:
1. What folders will be created
2. What folders will be renamed/merged
3. Where existing content will move
4. What templates will be added

Ask: "Does this look right? Type 'yes' to proceed or suggest changes."

### Step 7: Execute Changes

1. **Create new folder structure** using standard PARA structure
2. **Move existing content** to appropriate new locations:
   - Match by folder name where possible
   - Put ambiguous content in `00-Inbox/` for user to sort
   - Never delete user content
3. **Update CLAUDE.md** User Profile section with:
   - New role
   - New company size
   - New pillars
4. **Update `System/user-profile.yaml`** with new role and preferences

### Step 8: Summary

After completion, show:
- What changed
- Where to find moved content
- Any items in Inbox that need manual sorting
- Suggested next actions

## Content Preservation Rules

**NEVER delete user content during reset.** Follow these rules:

1. **Exact matches** - If old folder name matches new structure, keep content in place
2. **Similar matches** - If folders are similar (e.g., `Pipeline/` → `Opportunities/`), move content
3. **No match** - Move to `00-Inbox/To_Sort/` with a note about original location
4. **Person pages** - Always preserve `People/` folder structure
5. **Meeting notes** - Always preserve `00-Inbox/Meetings/` content

## Example Migrations

### PM at Startup → PM at Enterprise
- Add `Governance/` folder
- Expand `Relationships/` with more stakeholder categories
- Add enterprise-specific templates
- Keep all existing content in place

### Sales → Customer Success
- Rename `Pipeline/` → `Portfolio/`
- Add `Health/`, `Renewals/` folders
- Move account folders to new structure
- Add CS-specific templates

### Engineer → Engineering Manager
- Add `Team/` folder for 1:1s, hiring
- Keep `04-Projects/` and `Systems/`
- Add management templates
- Adjust focus from IC to leadership

## Error Handling

If something goes wrong:
1. Stop immediately
2. Show what was changed and what wasn't
3. Offer to rollback (if possible)
4. Suggest manual recovery steps

## Notes

- Reset is non-destructive by design
- User can run `/reset` as many times as needed
- Each reset creates a log entry in `System/reset_log.md`
