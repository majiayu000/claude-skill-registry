# approval-workflow

Multi-stakeholder approval routing with status tracking and escalation.

## Triggers

- "submit for approval"
- "route for approval"
- "approval workflow"
- "get sign-off"
- "approval status"
- "who needs to approve"

## Purpose

This skill manages the complete approval lifecycle for marketing assets by:
- Defining approval chains based on asset type and value
- Routing assets to appropriate approvers
- Tracking approval status in real-time
- Managing escalations and deadlines
- Recording approval history for audit

## Behavior

When triggered, this skill:

1. **Determines approval requirements**:
   - Identify asset type and category
   - Calculate approval tier (budget, risk, visibility)
   - Load approval chain configuration

2. **Initializes approval request**:
   - Create approval record
   - Attach asset and supporting materials
   - Set deadlines based on priority

3. **Routes to approvers**:
   - Notify approvers in sequence or parallel
   - Provide context and review materials
   - Track response status

4. **Manages workflow**:
   - Process approvals/rejections
   - Handle revision requests
   - Escalate overdue items
   - Route to next approver

5. **Records decisions**:
   - Document approval/rejection rationale
   - Maintain audit trail
   - Archive final approved version

## Approval Tiers

### Tier 1: Standard Content

```yaml
tier_1:
  description: Routine content with low risk
  criteria:
    - budget: <$5,000
    - audience_reach: <10,000
    - brand_impact: low
    - legal_risk: none

  approvers:
    - role: content-owner
      required: true
      timeout: 24h
    - role: brand-guardian
      required: true
      timeout: 24h

  routing: parallel
  total_sla: 48h
```

### Tier 2: Campaign Content

```yaml
tier_2:
  description: Campaign materials with moderate visibility
  criteria:
    - budget: $5,000-$50,000
    - audience_reach: 10,000-100,000
    - brand_impact: medium
    - legal_risk: low

  approvers:
    - role: content-owner
      required: true
      timeout: 24h
    - role: brand-guardian
      required: true
      timeout: 24h
    - role: campaign-manager
      required: true
      timeout: 24h
    - role: legal-reviewer
      required: if_claims
      timeout: 48h

  routing: sequential_then_parallel
  sequence:
    - [content-owner]
    - [brand-guardian, campaign-manager]
    - [legal-reviewer]
  total_sla: 72h
```

### Tier 3: High-Value/High-Risk

```yaml
tier_3:
  description: Major campaigns, brand partnerships, sensitive content
  criteria:
    - budget: >$50,000
    - audience_reach: >100,000
    - brand_impact: high
    - legal_risk: medium-high

  approvers:
    - role: content-owner
      required: true
      timeout: 24h
    - role: brand-guardian
      required: true
      timeout: 24h
    - role: creative-director
      required: true
      timeout: 48h
    - role: legal-reviewer
      required: true
      timeout: 48h
    - role: marketing-director
      required: true
      timeout: 48h

  routing: staged
  stages:
    - name: content_review
      approvers: [content-owner, brand-guardian]
      routing: parallel
    - name: creative_review
      approvers: [creative-director]
      routing: sequential
    - name: compliance_review
      approvers: [legal-reviewer]
      routing: sequential
    - name: executive_approval
      approvers: [marketing-director]
      routing: sequential

  total_sla: 120h
```

### Tier 4: Executive/Crisis

```yaml
tier_4:
  description: Brand-defining, crisis response, executive communications
  criteria:
    - brand_impact: critical
    - legal_risk: high
    - crisis_response: true
    - executive_messaging: true

  approvers:
    - role: brand-guardian
      required: true
      timeout: 4h
    - role: legal-reviewer
      required: true
      timeout: 4h
    - role: creative-director
      required: true
      timeout: 4h
    - role: marketing-director
      required: true
      timeout: 8h
    - role: cmo
      required: true
      timeout: 8h
    - role: legal-counsel
      required: if_crisis
      timeout: 4h

  routing: expedited_parallel
  escalation: immediate
  total_sla: 24h
```

## Approval Statuses

```yaml
statuses:
  draft:
    description: Not yet submitted
    actions: [edit, submit]

  pending:
    description: Awaiting review
    actions: [view, remind, withdraw]

  in_review:
    description: Actively being reviewed
    actions: [view]

  revision_requested:
    description: Changes needed
    actions: [edit, resubmit]

  approved:
    description: Approved by current approver
    actions: [view]

  rejected:
    description: Not approved
    actions: [view, appeal]

  escalated:
    description: Overdue, escalated to manager
    actions: [view, respond]

  fully_approved:
    description: All approvals complete
    actions: [publish, archive]

  expired:
    description: Approval window closed
    actions: [resubmit]
```

## Approval Request Format

```yaml
approval_request:
  id: APR-2025-001234
  asset:
    name: Q1 Product Launch - Email Campaign
    type: email_campaign
    path: .aiwg/marketing/assets/q1-launch/email-hero.html
    version: 2.1.0

  submitter:
    name: Jane Smith
    role: marketing-manager
    email: jane.smith@company.com
    submitted_at: 2025-12-08T10:00:00Z

  tier: 2
  priority: high
  deadline: 2025-12-11T10:00:00Z

  context:
    campaign: Q1 Product Launch
    budget: $25,000
    audience: 75,000 subscribers
    launch_date: 2025-01-15
    notes: "Launch email for new product line. Needs legal review for pricing claims."

  attachments:
    - email-hero.html
    - email-preview.png
    - brand-compliance-report.md
    - qa-report.md

  approval_chain:
    - role: content-owner
      assignee: Jane Smith
      status: approved
      approved_at: 2025-12-08T10:30:00Z

    - role: brand-guardian
      assignee: Sarah Chen
      status: pending
      due_at: 2025-12-09T10:00:00Z

    - role: legal-reviewer
      assignee: Elena Rodriguez
      status: not_started
      due_at: 2025-12-10T10:00:00Z
```

## Approval Record Format

```markdown
# Approval Record: APR-2025-001234

**Asset**: Q1 Product Launch - Email Campaign
**Version**: 2.1.0
**Submitted**: 2025-12-08 10:00 AM
**Final Status**: FULLY APPROVED
**Approved**: 2025-12-10 3:45 PM

## Summary

| Metric | Value |
|--------|-------|
| Tier | 2 (Campaign Content) |
| Total Approvers | 4 |
| Approvals | 4 |
| Rejections | 0 |
| Revisions | 1 |
| Elapsed Time | 53h 45m |
| SLA Target | 72h |
| SLA Status | Within SLA |

## Approval Chain

### Stage 1: Content Review

#### Content Owner - Jane Smith
- **Status**: APPROVED
- **Reviewed**: 2025-12-08 10:30 AM
- **Time to Review**: 30 minutes
- **Comments**: "Ready for brand review"
- **Conditions**: None

### Stage 2: Brand & Campaign Review

#### Brand Guardian - Sarah Chen
- **Status**: APPROVED with Conditions
- **Reviewed**: 2025-12-09 2:15 PM
- **Time to Review**: 28h 15m
- **Comments**: "Logo placement approved. Please update CTA button to brand green."
- **Conditions**:
  - [ ] Update CTA color to #00AA55
  - [x] Condition met in revision v2.1.0

#### Campaign Manager - David Kim
- **Status**: APPROVED
- **Reviewed**: 2025-12-09 11:00 AM
- **Time to Review**: 25h
- **Comments**: "Aligns with campaign strategy. Good to proceed."
- **Conditions**: None

### Stage 3: Compliance Review

#### Legal Reviewer - Elena Rodriguez
- **Status**: APPROVED
- **Reviewed**: 2025-12-10 3:45 PM
- **Time to Review**: 28h 30m
- **Comments**: "Pricing claims substantiated. Disclosure text approved."
- **Conditions**: None

## Revision History

### Revision 1 (v2.0.0 → v2.1.0)
- **Date**: 2025-12-09 4:00 PM
- **Requested By**: Sarah Chen (Brand Guardian)
- **Changes Made**:
  - Updated CTA button color from #CCCCCC to #00AA55
  - Adjusted button contrast ratio
- **Resubmitted**: 2025-12-09 4:30 PM

## Audit Trail

| Timestamp | Action | User | Details |
|-----------|--------|------|---------|
| 2025-12-08 10:00 | Submitted | Jane Smith | Initial submission v2.0.0 |
| 2025-12-08 10:05 | Routed | System | Sent to content-owner |
| 2025-12-08 10:30 | Approved | Jane Smith | Content owner approval |
| 2025-12-08 10:31 | Routed | System | Sent to brand-guardian, campaign-manager |
| 2025-12-09 11:00 | Approved | David Kim | Campaign manager approval |
| 2025-12-09 2:15 | Conditional | Sarah Chen | Requested CTA color change |
| 2025-12-09 4:30 | Resubmitted | Jane Smith | Updated to v2.1.0 |
| 2025-12-09 4:45 | Approved | Sarah Chen | Condition satisfied |
| 2025-12-09 4:46 | Routed | System | Sent to legal-reviewer |
| 2025-12-10 3:45 | Approved | Elena Rodriguez | Final approval |
| 2025-12-10 3:45 | Completed | System | All approvals received |

## Approved Asset

- **Final Version**: 2.1.0
- **Checksum**: sha256:abc123...
- **Archive Path**: .aiwg/marketing/approved/2025/12/q1-launch-email-v2.1.0/
- **Publish Authorized**: Yes

## Sign-offs

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Content Owner | Jane Smith | ✓ | 2025-12-08 |
| Brand Guardian | Sarah Chen | ✓ | 2025-12-09 |
| Campaign Manager | David Kim | ✓ | 2025-12-09 |
| Legal Reviewer | Elena Rodriguez | ✓ | 2025-12-10 |
```

## Usage Examples

### Submit for Approval

```
User: "Submit this email for approval"

Skill executes:
1. Identify asset type: Email campaign
2. Calculate tier: Tier 2 (budget $25k, audience 75k)
3. Load approval chain
4. Create approval request
5. Notify first approvers

Output:
"Approval Request Created: APR-2025-001234

Asset: Q1 Product Launch Email
Tier: 2 (Campaign Content)
SLA: 72 hours

Approval Chain:
1. ⏳ Content Owner (Jane Smith) - 24h
2. ⏳ Brand Guardian (Sarah Chen) - 24h
3. ⏳ Campaign Manager (David Kim) - 24h
4. ⏳ Legal Reviewer (Elena Rodriguez) - 48h

Deadline: December 11, 10:00 AM

Notifications sent to initial approvers."
```

### Check Status

```
User: "Approval status"

Skill returns:
"APR-2025-001234: Q1 Launch Email

Progress: 2/4 approvals (50%)
Current Stage: Brand & Campaign Review

✅ Content Owner: Approved (Dec 8)
⏳ Brand Guardian: In Review (due Dec 9)
⏳ Campaign Manager: In Review (due Dec 9)
⬜ Legal Reviewer: Waiting

Time Remaining: 48h of 72h SLA
On Track: Yes"
```

### Handle Revision Request

```
User: "Brand guardian requested changes"

Skill processes:
1. Log revision request
2. Notify submitter
3. Pause approval chain
4. Track revision status

Output:
"Revision Requested by Sarah Chen (Brand Guardian)

Required Changes:
1. Update CTA button to brand green (#00AA55)

Status: REVISION_REQUESTED
Original Chain: Paused

To continue:
1. Make requested changes
2. Update asset version
3. Resubmit: 'resubmit approval APR-2025-001234'

Deadline extended: +24h for revision"
```

### Escalation

```
User: "Escalate overdue approval"

Skill executes:
1. Identify overdue approver
2. Notify escalation path
3. Update status

Output:
"Escalation Initiated: APR-2025-001234

Overdue Approver: Sarah Chen (Brand Guardian)
Overdue By: 8 hours

Escalated To: James Wilson (Creative Director)
Notification: Sent

New Deadline: 24h from now
Status: ESCALATED"
```

## Integration

This skill uses:
- `artifact-metadata`: Track approval status
- `project-awareness`: Context for tier determination
- `review-synthesis`: Aggregate reviewer feedback before approval

## Workflow Configuration

### Approval Routing

```yaml
routing_config:
  parallel:
    description: All approvers notified simultaneously
    complete_when: all_approved

  sequential:
    description: Approvers review in order
    complete_when: all_approved_in_sequence

  staged:
    description: Groups of parallel approvers in sequence
    complete_when: all_stages_complete

  expedited_parallel:
    description: All approvers simultaneously with aggressive reminders
    complete_when: all_approved
    reminder_frequency: 2h
```

### Notification Settings

```yaml
notifications:
  on_submit:
    - approver: email, slack
    - submitter: confirmation

  on_approve:
    - next_approver: email, slack
    - submitter: status_update

  on_reject:
    - submitter: email, slack
    - stakeholders: email

  on_revision:
    - submitter: email, slack

  reminders:
    - at: 50% of deadline
    - at: 75% of deadline
    - at: 90% of deadline
    - overdue: hourly for 4h, then escalate
```

### Escalation Rules

```yaml
escalation:
  auto_escalate:
    trigger: overdue + 4h
    to: approver_manager

  manual_escalate:
    allowed_by: [submitter, stakeholder]
    to: [marketing-director, project-manager]

  crisis_escalate:
    trigger: tier_4 + overdue
    to: [cmo, legal-counsel]
    notification: immediate
```

## Output Locations

- Approval requests: `.aiwg/marketing/approvals/pending/`
- Approval records: `.aiwg/marketing/approvals/completed/`
- Approved assets: `.aiwg/marketing/approved/{year}/{month}/`
- Audit logs: `.aiwg/marketing/approvals/audit/`

## References

- Approval tier definitions: .aiwg/marketing/config/approval-tiers.yaml
- Escalation procedures: docs/escalation-process.md
- Approval templates: templates/governance/approval-request.md
