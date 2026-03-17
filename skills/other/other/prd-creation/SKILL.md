---
name: prd-creation
description: Use when creating standalone PRD from user input - gathers requirements through interactive session, validates with prd-validation, and writes PRD file using template
---

# PRD Creation

## Purpose

Create individual Product Requirements Document through interactive session:
- Structured requirements gathering across 8 phases
- Apply PRD validation rubric
- Generate PRD file from template
- No fabrication - leave unknown sections as TBD

## When to Use

Activate when:
- User invokes `/project:create-prd`
- Manual PRD creation needed
- Capturing product requirements from conversation

## Guiding Principles

1. **PRD is a living document** — It will evolve through collaboration and discovery
2. **Narrow scope is better** — One PRD ≈ One Jira Epic ≈ One quarter of work
3. **Share and link** — PRDs should be accessible with links to Slack channels
4. **No fabrication** — Leave sections blank/TBD rather than making up information
5. **Reflect what was delivered** — At close, PRD should document actual outcomes

## Workflow

### Phase 1: Core Identity

**Ask user:**
- **Project Name**: What is this PRD called?
- **One-liner Description**: 1-3 sentence summary for quick context
- **Background**: Why does this project exist? What problem does it solve?

### Phase 2: Ownership (DACE)

**Ask user:**
- **Driver**: Who is driving this initiative?
- **Approver**: Who has final approval authority?
- **Contributors**: Who is contributing to the work?
- **Escalation Path**: Where to escalate blockers or decisions?
- **Driving Teams**: Which teams own this work? (include PM, PMO, Engineering, Design roles)
- **Contributing Teams**: Which teams are contributing?
- **Other Stakeholders**: Legal, Security, etc.

*If user doesn't know, leave as TBD.*

### Phase 3: Objectives

**Ask user:**
- **Target Customer/User**: Who is this for? (Customer/Partner/Developer/etc.)
- **Customer Statement**:
  - I am: (narrow description of customer with motivations/attributes)
  - I'm trying to: (desired outcome)
  - But: (problem/barrier)
  - Because: (root cause)
  - Which makes me feel: (emotion)
- **Success Metrics**: How will we measure success? (User Experience, Technical Capabilities)
- **Opportunity Sizing**: What's the potential impact?

*Source from meeting signals if available. Leave blank if not known.*

### Phase 4: Scope

**Ask user:**
- **Use Cases In Scope**: What specific use cases will be supported? Include descriptions.
- **Out of Scope**: What are we explicitly NOT doing? Include reasons.

*Be specific. Think through edge cases.*

### Phase 5: Requirements

**For each milestone, ask:**
- **Milestone Name/Summary**: What does this milestone deliver?
- **Requirements** with:
  - Priority (P0 = must do, P1 = nice to have, P2 = if time permits)
  - Dependent Teams
  - User Story: "In order to accomplish X, we will build Y"
  - Acceptance Criteria: How we know requirements are met
  - Figma links (if available)
  - JIRA tickets (if available)

*Only include requirements that are known. Don't fabricate.*

### Phase 6: Timeline

**Ask user:**
- **Milestones**: List of major milestones (e.g., Architecture, Design, Development, Testing, Launch)
- **Expected Delivery Timeline**: Target dates/quarters for each milestone
- **Teams Leading Each Phase**: Who owns each milestone?

*If timeline is not yet determined, leave as TBD.*

### Phase 7: Links and Resources

**Ask user:**
- **Slack Channels**: Related Slack channels for discussion
- **Figma/Design Links**: Experience design and content
- **Architecture/Technical Design Docs**: Lucidcharts, Miro, etc.
- **JIRA Project/Tracking Links**: Project plan / tracking
- **Any Other Relevant Links**

*Only include links that exist. Don't create placeholder URLs.*

### Phase 8: Metrics and Learning Agenda

**Ask user:**
- **Goals and Hypotheses**: What do you want to happen?
- **Signals**: What would indicate success or validation?
- **Metrics**: What to measure to see these signals?

### Fact-Checking Requirements

**CRITICAL**: Do not fabricate information. For any section where information is not provided:
- Leave the section blank or marked "TBD"
- Note in changelog that section needs input
- Prompt user: "Do you have this information available?"

### Validate PRD

**Invoke:** `prd-validation` skill

- Apply 6-point rubric
- Drafting PRDs may have warnings but not blockers
- Actionable PRDs must pass all criteria

### Write PRD File

**Use template:** `datasets/product/templates/prd-template.md`

**Output:** `datasets/product/prds/{YYYY}/PRD_{slug}.md`

**Set initial status:** 🚧 Drafting

**Add changelog entry:**
```markdown
| {YYYY-MM-DD} | Initial draft created | {user} |
```

### Optionally Update Backlog

**Ask user:**
"Add to backlog.md? (yes/no)"

If yes: Prepend to `datasets/product/backlog.md`

## PRD Statuses

| Status | When to Use |
|--------|-------------|
| 🚧 Drafting | Initial creation, known to be incomplete |
| 🏃 Actionable | Eng has agreed there's enough to start work |
| 🔒 Closed | Represents what was finally delivered |
| ❗ Abandoned | Project cancelled or superseded |

## Success Criteria

- PRD created with all provided information
- Unknown sections marked as TBD (not fabricated)
- PRD file written to correct location
- Template structure followed
- Changelog entry added
- Optionally added to backlog

## Related Skills

- `prd-validation`: Validates PRD quality
- `product-planning`: Batch PRD creation from meetings
- `meeting-synthesis`: Gathers evidence from meeting transcripts




