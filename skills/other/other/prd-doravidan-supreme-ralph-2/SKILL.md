---
name: prd
description: Generate detailed Product Requirements Documents (PRDs) through interactive conversation.
allowed-tools: Read, Write, Bash
---

# PRD Skill

Generate detailed Product Requirements Documents (PRDs) through interactive conversation.

## Trigger

This skill activates when the user asks to:
- Create a PRD
- Write requirements for a feature
- Plan a new feature

## Process

### Step 1: Clarifying Questions

Ask 3-5 clarifying questions to understand the feature. Format each question with lettered options:

```
Before I create the PRD, I have a few questions:

**1. What is the primary goal?**
   a) [Option 1]
   b) [Option 2]
   c) [Option 3]
   d) Something else (please specify)

**2. Who is the target user?**
   a) [Option 1]
   b) [Option 2]
   ...
```

Wait for the user's answers before proceeding.

### Step 2: Generate PRD

Create a detailed PRD in Markdown format with these sections:

```markdown
# PRD: [Feature Name]

## Overview
[2-3 sentence summary of what we're building and why]

## Goals
1. [Primary goal]
2. [Secondary goal]
3. [Tertiary goal]

## User Stories

### US-001: [Story Title]
**As a** [user type]
**I want** [capability]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Typecheck passes

**Priority:** 1 (Highest)

### US-002: [Story Title]
...

## Functional Requirements

### FR-001: [Requirement Name]
[Description of the requirement]

### FR-002: [Requirement Name]
...

## Non-Goals
- [What we are explicitly NOT doing]
- [Scope limitations]

## Technical Considerations
- [Architecture decisions]
- [Dependencies]
- [Performance requirements]

## Success Metrics
- [How we measure success]
- [KPIs]

## Open Questions
- [Unresolved decisions]
- [Items needing clarification]
```

### Step 3: Save the PRD

Save to: `tasks/prd-[feature-name].md`

```bash
mkdir -p tasks
cat > tasks/prd-[feature-name].md << 'EOF'
[PRD content]
EOF
```

## Rules

1. **Story Sizing** - Each story must be completable in ONE iteration (small scope)
2. **Dependency Order** - Order stories by dependency (data model → logic → API → UI)
3. **Acceptance Criteria** - Every story MUST include "Typecheck passes"
4. **UI Stories** - Frontend stories must include "Verify in browser"
5. **Be Specific** - Avoid vague criteria like "works well"

## Example Clarifying Questions

For a "user authentication" feature:

```
**1. What authentication methods are needed?**
   a) Email/password only
   b) Email/password + OAuth (Google, GitHub)
   c) Magic link (passwordless)
   d) All of the above

**2. What should happen after login?**
   a) Redirect to dashboard
   b) Return to previous page
   c) Show welcome modal
   d) Custom behavior

**3. Is MFA (Multi-Factor Authentication) required?**
   a) Yes, mandatory for all users
   b) Yes, optional per user preference
   c) No, not needed initially
   d) Only for admin users
```

## Output

After generating the PRD:

1. Show a summary of the PRD
2. Tell the user the file location
3. Explain next steps:

```
PRD created at: tasks/prd-[feature-name].md

Next steps:
1. Review the PRD and make any adjustments
2. Convert to prd.json: /ralph-convert tasks/prd-[feature-name].md
3. Run RALPH: ./scripts/ralph/ralph.sh 20
```
