---
name: vision
description: "Parses and analyzes project vision to extract structured requirements. Use at project start to understand goals, scope, and constraints. Triggers on: analyze vision, parse project goals, understand requirements."
---

# Vision Analysis Skill

Parse the project vision document and extract structured requirements for architecture and planning.

---

## The Job

1. Read `project.vision.md` from the project root
2. Validate all required sections are present
3. Extract and structure the requirements
4. Identify project type and scale
5. Output analysis to guide architecture decisions
6. Save analysis to `project.vision-analysis.md`

---

## Input: project.vision.md

The vision document should contain:

### Required Sections

| Section | Purpose |
|---------|---------|
| **What** | One-sentence description of the project |
| **Why** | Motivation and problem being solved |
| **Target Users** | Who will use this product |
| **Success Criteria** | Measurable definition of success |

### Optional Sections

| Section | Purpose |
|---------|---------|
| **Constraints** | Technical, budget, or time limitations |
| **Inspirations** | Reference products or desired style |
| **Non-Goals** | What the project explicitly won't do |

---

## Analysis Process

### Step 1: Validate Vision Document

Check that `project.vision.md` exists and contains required sections:

```markdown
## Validation Checklist
- [ ] What section present and clear
- [ ] Why section explains motivation
- [ ] Target Users defined
- [ ] Success Criteria are measurable
```

If sections are missing or unclear, document what's needed before proceeding.

### Step 2: Identify Project Type

Classify the project:

| Type | Characteristics |
|------|-----------------|
| **CLI Tool** | Command-line interface, no UI |
| **Web App** | Browser-based, frontend + backend |
| **API Service** | Backend only, REST/GraphQL |
| **Library** | Reusable code package |
| **Desktop App** | Native desktop application |
| **Mobile App** | iOS/Android application |
| **Full Stack** | Complete web application |
| **Infrastructure** | DevOps, deployment tools |

### Step 3: Estimate Project Scale

| Scale | Stories | Duration | Complexity |
|-------|---------|----------|------------|
| **Small** | 5-15 | Days | Single component |
| **Medium** | 15-50 | Weeks | Multiple components |
| **Large** | 50-200 | Months | Full system |
| **Enterprise** | 200+ | Quarters | Multiple systems |

### Step 4: Extract Core Features

From the vision, identify:

1. **Must-Have Features** - Critical for MVP
2. **Should-Have Features** - Important but not blocking
3. **Nice-to-Have Features** - Enhancements for later
4. **Out of Scope** - Explicitly excluded

### Step 5: Identify Technical Implications

Based on features, note:

- Data storage needs (database type, scale)
- Authentication requirements
- External integrations
- Performance requirements
- Security considerations
- Deployment environment

---

## Output: project.vision-analysis.md

```markdown
# Vision Analysis

**Generated:** [timestamp]
**Vision Version:** [hash or date of vision.md]

## Project Classification

- **Type:** [Web App | API Service | CLI Tool | ...]
- **Scale:** [Small | Medium | Large | Enterprise]
- **Estimated Stories:** [range]

## Core Requirements

### Must-Have (MVP)
1. [Feature 1]
2. [Feature 2]
3. ...

### Should-Have (Post-MVP)
1. [Feature 1]
2. ...

### Nice-to-Have (Future)
1. [Feature 1]
2. ...

### Out of Scope
- [Excluded item 1]
- [Excluded item 2]

## Technical Implications

### Data & Storage
- [Storage needs analysis]

### Authentication & Security
- [Auth requirements]

### Integrations
- [External system integrations]

### Performance
- [Performance requirements]

### Deployment
- [Deployment environment needs]

## Constraints Summary

| Constraint | Impact |
|------------|--------|
| [Constraint 1] | [How it affects decisions] |

## Open Questions

- [ ] [Question that needs clarification]
- [ ] [Another question]

## Recommended Next Steps

1. Run Architect Skill to determine technology stack
2. Address any open questions before proceeding
3. ...

## Architecture Hints

Based on this vision, consider:
- [Hint about architecture approach]
- [Hint about technology category]
```

---

## Decision Points

### When Vision is Unclear

If the vision document lacks detail:

1. **Do NOT guess** - Document what's missing
2. **List specific questions** - What exactly needs clarification
3. **Provide options** - Suggest possible interpretations
4. **Proceed cautiously** - Make conservative assumptions and note them

### When Scope is Too Large

If estimated scale is "Large" or "Enterprise":

1. **Recommend phased approach** - Break into multiple major milestones
2. **Identify MVP subset** - What's the smallest useful version
3. **Flag risk** - Note that large projects need careful management

### When Constraints Conflict

If constraints seem to conflict with goals:

1. **Document the conflict** - Be explicit about the tension
2. **Propose resolutions** - Suggest possible compromises
3. **Prioritize** - Recommend which constraint to relax

---

## Integration with Orchestrator

After vision analysis:

1. Save `project.vision-analysis.md` to project root
2. Signal completion to orchestrator
3. Architect Skill uses this analysis as input

---

## Example Analysis

**Input Vision:**
```markdown
# Project Vision

## What
A personal finance tracker that helps users manage their budget and track expenses.

## Why
Existing apps are too complex. Users need a simple, focused tool.

## Target Users
Individuals who want basic expense tracking without complexity.

## Success Criteria
- Users can add expenses in under 5 seconds
- Monthly reports generated automatically
- Works offline

## Constraints
- Must be a web app (PWA for offline)
- No paid APIs (keep it free)
- Single developer, limited time
```

**Output Analysis:**
```markdown
# Vision Analysis

## Project Classification
- **Type:** Web App (PWA)
- **Scale:** Medium
- **Estimated Stories:** 20-35

## Core Requirements

### Must-Have (MVP)
1. Quick expense entry (< 5 seconds)
2. Expense categorization
3. Monthly report generation
4. Offline support (PWA)
5. Data persistence

### Should-Have (Post-MVP)
1. Budget setting and tracking
2. Expense trends visualization
3. Export functionality

### Nice-to-Have (Future)
1. Multiple currencies
2. Receipt photo capture
3. Bank import

### Out of Scope
- Multi-user/sharing features
- Investment tracking
- Tax preparation

## Technical Implications

### Data & Storage
- Local-first (IndexedDB for offline)
- Optional cloud sync later

### Authentication & Security
- Initially: None (local only)
- Later: Simple auth for sync

### Performance
- Critical: Fast expense entry
- PWA service worker for offline

### Deployment
- Static hosting (Netlify, Vercel)
- No backend initially

## Constraints Summary

| Constraint | Impact |
|------------|--------|
| PWA required | Must use service workers, IndexedDB |
| No paid APIs | Use free/open solutions only |
| Limited time | Focus on MVP, defer nice-to-haves |

## Recommended Next Steps

1. Run Architect Skill to select frontend framework
2. Design offline-first data architecture
3. Plan PWA implementation strategy
```

---

## Checklist

Before completing vision analysis:

- [ ] All required vision sections validated
- [ ] Project type identified
- [ ] Scale estimated
- [ ] Features categorized (must/should/nice/out)
- [ ] Technical implications documented
- [ ] Constraints analyzed
- [ ] Open questions listed
- [ ] Analysis saved to `project.vision-analysis.md`
