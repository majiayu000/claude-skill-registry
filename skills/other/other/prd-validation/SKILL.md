---
name: prd-validation
description: Use when creating or reviewing PRDs - enforces 6-point rubric ensuring PRDs have clear objectives, defined use cases, structured requirements, timeline, measurable success criteria, and DACE assignment
---

# PRD Validation

## The Iron Law

**NO PRD BECOMES ACTIONABLE WITHOUT PASSING ALL 6 RUBRIC CHECKS**

If a PRD fails any rubric criterion, it must be:
1. Refined until it passes, OR
2. Demoted to a ticket (if too small for a PRD), OR
3. Split into multiple PRDs (if too large for one quarter), OR
4. Kept in Drafting status (if information is pending)

No "good enough" PRDs. No "we'll fill it in later" for Actionable status. Pass or fail.

## Purpose

Ensure all PRDs maintain consistent quality standards:
- Clear objectives with customer problem statement
- Defined use cases (in scope and out of scope)
- Structured requirements with priorities
- Timeline with milestones
- Measurable success criteria
- Assigned ownership (DACE)

## When to Use This Skill

Activate automatically when:
- Creating new PRDs from meeting synthesis
- Reviewing PRD proposals before transitioning to Actionable
- User requests PRD validation
- `product-planning` workflow invokes this quality gate
- PRDs are being prioritized or scheduled

## Validation by PRD Status

| Status | Validation Requirement |
|--------|----------------------|
| 🚧 Drafting | Warnings allowed, no blockers. Must have: Project name, description, at least one objective |
| 🏃 Actionable | **ALL 6 criteria must pass**. No TBD in critical fields |
| 🔒 Closed | All criteria passed + reflects actual delivery |
| ❗ Abandoned | No validation required |

## The 6-Point PRD Rubric

All PRDs must pass **all six criteria** to become Actionable:

### 1. Objectives Clear
**Requirement**: PRD has a well-defined customer statement with problem and desired outcome

**Pass**:
```
I am: A marketing manager at a mid-size e-commerce company
I'm trying to: Export campaign performance data to our BI tool
But: The current export is manual and takes 2+ hours per week
Because: There's no automated integration with our data warehouse
Which makes me feel: Frustrated and inefficient
```

**Fail**:
- Only vague problem statement ("Users need better exports")
- Missing customer description
- No clear desired outcome
- Generic statements without specifics

### 2. Use Cases Defined
**Requirement**: PRD has explicit in-scope use cases with descriptions

**Pass**:
```
In Scope:
- UC-1: Marketing manager exports campaign metrics to Google Sheets on demand
- UC-2: Scheduled weekly export to team's shared folder
- UC-3: Custom date range selection for historical analysis

Out of Scope:
- Real-time sync (not needed for current use case)
- Excel format export (Google Sheets covers needs)
- Custom field mapping (v2 feature)
```

**Fail**:
- No use cases listed
- Only bullet points without context
- "Out of scope: TBD"
- Missing out-of-scope section entirely

### 3. Requirements Structured
**Requirement**: PRD has requirements organized by milestone with priority levels

**Pass**:
```
Milestone 1: Core Export
| P  | Teams      | Requirement                    | Acceptance Criteria         |
|----|------------|--------------------------------|------------------------------|
| P0 | Platform   | Export to Google Sheets        | File appears in user's Drive |
| P0 | Platform   | Include key metrics            | Contains: sends, opens, clicks |
| P1 | Platform   | Custom date range              | User can select start/end dates |
```

**Fail**:
- Flat list of requirements without milestones
- No prioritization (P0/P1/P2)
- Missing acceptance criteria
- Just feature descriptions without user stories

### 4. Timeline Present
**Requirement**: PRD has milestones with expected delivery timeline

**Pass**:
```
| Milestone          | Team(s)           | Deliverable              | Timeline   |
|--------------------|-------------------|--------------------------|------------|
| Architecture       | Platform          | Technical design doc     | Week 1     |
| Design             | Design, Product   | Figma mockups           | Week 2     |
| Development        | Platform, Frontend| Core export feature     | Weeks 3-4  |
| Testing & Launch   | QA, Platform      | Production release      | Week 5     |
```

**Fail**:
- No timeline section
- "Timeline: TBD" without any milestones
- No ownership identified for phases
- Missing delivery expectations

### 5. Success Measurable
**Requirement**: PRD has success metrics and/or opportunity sizing

**Pass**:
```
Goals and Hypotheses: Reduce time spent on manual exports by 80%
Signals: Users adopt automated export; support tickets for export decrease
Metrics: 
- Weekly active users of export feature
- Average exports per user per week
- Time from export request to completion
Opportunity Sizing: 500 customers affected, ~$50K ARR at risk from churn
```

**Fail**:
- "We'll know it when we see it"
- No measurement plan
- Impact not quantified
- No success criteria defined

### 6. DACE Assigned
**Requirement**: PRD has Driver, Approver, and key Contributors identified

**Pass**:
```
| Role        | Person/Team         |
|-------------|---------------------|
| Driver      | Jane Smith (PM)     |
| Approver    | John Doe (VP Prod)  |
| Contributors| Platform team, Design |
| Escalation  | VP Engineering      |
```

**Fail**:
- "Driver: TBD"
- No approval authority identified
- No team ownership
- Missing escalation path

## Validation Process

### 1. Load PRD

Read PRD from:
- `datasets/product/prds/{YYYY}/PRD_{slug}.md`, OR
- PRD proposal in backlog intake section, OR
- In-memory PRD draft

### 2. Apply Rubric

Check each criterion sequentially:

```
✓ Objectives Clear? [Yes/No] → [Has customer statement with all elements]
✓ Use Cases Defined? [Yes/No] → [Count in-scope, count out-of-scope]
✓ Requirements Structured? [Yes/No] → [Has milestones with priorities]
✓ Timeline Present? [Yes/No] → [Has delivery expectations]
✓ Success Measurable? [Yes/No] → [Has metrics/opportunity sizing]
✓ DACE Assigned? [Yes/No] → [Has Driver, Approver identified]
```

### 3. Generate Report

**If all pass:**
```markdown
# PRD Validation Report: PASS

**PRD**: [Title]
**Current Status**: [Status]
**Target Status**: Actionable

✓ Objectives Clear: Customer statement complete
✓ Use Cases Defined: N in-scope, N out-of-scope
✓ Requirements Structured: N milestones, N requirements with priorities
✓ Timeline Present: Milestones with delivery dates
✓ Success Measurable: N metrics defined, opportunity sized
✓ DACE Assigned: Driver: [name], Approver: [name]

**Recommendation**: Approve for Actionable status
```

**If any fail:**
```markdown
# PRD Validation Report: FAIL

**PRD**: [Title]
**Current Status**: [Status]
**Target Status**: Actionable

Failed criteria:
✗ [Criterion name]: [Specific failure reason]

**Required fixes**:
1. [Specific action to address failure]
2. [Specific action to address failure]

**Recommendation**: Keep as Drafting / Needs Revision
```

### 4. Block or Approve

**If PASS:**
- PRD can transition to Actionable
- PRD can proceed to roadmap
- Engineering can begin work

**If FAIL:**
- PRD stays in Drafting status
- Must address failures before re-validation
- User notified of required additions

## Integration with Workflows

### Product Planning Integration

**Invoked by:**
- `product-planning` workflow (after drafting, before output)
- `prd-creation` workflow (before writing PRD file)

**Blocking behavior:**
- Failed PRDs remain in Drafting status
- Failed PRDs flagged in validation report
- User notified of required additions

### Manual Validation

**Direct usage:**
User can invoke validation on existing PRDs:
```
"Validate the PRD at datasets/product/prds/2025/PRD_google-sheets-export.md"
```

## Success Criteria

PRD validation passes when:
- All 6 rubric criteria satisfied
- Validation report shows PASS status
- Customer statement is complete
- Scope boundaries are clear
- Requirements have priorities and milestones
- Timeline is defined
- Success metrics exist
- DACE is assigned

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Vague objectives ("improve exports") | Complete customer statement with all elements |
| Missing out-of-scope | Explicitly state what's excluded and why |
| Flat requirements list | Organize by milestone with P0/P1/P2 |
| No timeline | Add milestones table with delivery expectations |
| No metrics | Define specific success signals and measurements |
| TBD for Driver/Approver | Assign specific people or roles |

## Quality Gate Failures

**Auto-fail conditions:**

1. **Missing customer statement**
   - Example: "Users want this feature"
   - Fix: Complete "I am / I'm trying to / But / Because / Which makes me feel"

2. **No use cases**
   - Example: Only feature descriptions
   - Fix: Define specific use cases with descriptions

3. **Unstructured requirements**
   - Example: Flat bullet list
   - Fix: Organize by milestone with P0/P1/P2 priorities

4. **No timeline**
   - Example: "We'll figure it out"
   - Fix: Add milestones table with expected dates

5. **No success metrics**
   - Example: "It will be better"
   - Fix: Define measurable success criteria

6. **No DACE**
   - Example: "Team owns it"
   - Fix: Name specific Driver and Approver

## Related Skills

- **meeting-synthesis**: Gathers evidence from meeting transcripts
- **product-planning**: Invokes this quality gate before PRD output
- **prd-creation**: Invokes this quality gate before writing PRD file

## Anti-Rationalization Blocks

Common excuses that are **explicitly rejected**:

| Rationalization | Reality |
|-----------------|---------|
| "We can fill in details later" | Actionable PRDs need complete critical fields |
| "Everyone knows what this means" | Make it explicit and documented |
| "Timeline will become clear" | Timeline required for Actionable status |
| "DACE can be assigned later" | Driver and Approver required for Actionable |
| "Out of scope is obvious" | Explicitly state exclusions |
| "Close enough to pass" | All 6 criteria or remain in Draft |




