---
name: feature-spec-writing
description: Creates focused feature specifications with user stories, acceptance criteria, and edge cases. Lighter than PRD, focuses on single feature implementation. Use when specifying individual features after PRD approval or for standalone feature work.
version: 1.0.0
---

# Feature Spec Writing

## Purpose

Creates implementation-ready feature specifications that break down PRD requirements into detailed, actionable specs with comprehensive edge case coverage.

## When NOT to Use This Skill

- Initial product requirements (use `prd-writing` instead)
- System architecture design (use `technical-spec-writing` instead)
- Reviewing existing specs (use `feature-spec-reviewing` instead)
- Bug fixes (no spec needed, just fix it)
- Minor enhancements < 1 day of work (overkill)

## Key Differences from PRD

| Aspect | PRD | Feature Spec |
|--------|-----|--------------|
| Scope | Product/Initiative | Single Feature |
| Audience | Stakeholders | Engineers |
| Detail Level | High-level | Implementation-ready |
| Edge Cases | Summary | Exhaustive |
| User Stories | Multiple (3-7) | Single primary + variants |
| Success Metrics | Business outcomes | Feature-level KPIs |

## Workflow

### Step 1: Context Gathering

Invoke `check-history` to understand project context.

If a parent PRD exists, reference it:

```markdown
Questions to gather:
1. Which PRD/user story does this feature implement?
2. What's the single-sentence feature description?
3. Who is the primary user persona?
4. What technical constraints exist?
5. What's the target implementation timeline?
```

### Step 2: Feature Definition

Write a clear, one-sentence feature definition:

```markdown
**Feature:** [Verb] [what] for [whom] to [achieve outcome]

Examples:
✅ "Display shipping cost estimates on product pages for shoppers to compare options before checkout"
✅ "Allow admins to create custom permission roles to match their organization structure"
✅ "Send real-time push notifications for transactions to help users detect fraud immediately"

❌ "Improve the shipping experience" (too vague)
❌ "Add role management" (missing who and why)
```

### Step 3: User Story

Write the primary user story with variants:

```markdown
## Primary User Story

**As a** [specific user type]
**I want** [specific goal]
**So that** [concrete benefit]

## Story Variants (if applicable)

**Variant A - [Scenario Name]:**
As a [user], I want [alternative goal], so that [benefit]

**Variant B - [Scenario Name]:**
As a [user], I want [different goal], so that [benefit]
```

### Step 4: Acceptance Criteria

Define comprehensive acceptance criteria covering:

1. **Happy Path** - Normal successful flow
2. **Input Validation** - What's valid/invalid
3. **Edge Cases** - Boundary conditions
4. **Error States** - Failure handling
5. **Performance** - Speed/resource expectations
6. **Security** - Authentication/authorization
7. **Accessibility** - A11y requirements (if UI)

```gherkin
## Acceptance Criteria

### Happy Path
Scenario: Successful [action]
  Given [precondition]
  And [additional context]
  When [user action]
  Then [expected outcome]
  And [additional outcome]

### Validation
Scenario: Invalid [input type]
  Given [context]
  When [user provides invalid input]
  Then [validation message shown]
  And [action is prevented]

### Edge Cases
Scenario: [Boundary condition]
  Given [edge case setup]
  When [action at boundary]
  Then [expected behavior]

### Error Handling
Scenario: [Failure type]
  Given [normal context]
  And [dependency fails]
  When [user action]
  Then [graceful degradation]
  And [user informed of issue]

### Performance
Scenario: Response time under load
  Given [load conditions]
  When [action performed]
  Then [response within X ms]

### Security
Scenario: Unauthorized access attempt
  Given [user without permission]
  When [user attempts action]
  Then [access denied]
  And [attempt logged]
```

### Step 5: Error States Matrix

Document all error conditions:

```markdown
## Error States

| Error Condition | User Message | System Action | Recovery |
|-----------------|--------------|---------------|----------|
| Invalid input | "Please enter valid X" | Highlight field | User corrects |
| Network failure | "Connection lost. Retrying..." | Auto-retry 3x | Manual retry button |
| Server error | "Something went wrong" | Log error, alert oncall | Show support contact |
| Timeout | "Taking too long" | Cancel request | Offer retry |
| Not found | "Item not available" | 404 response | Suggest alternatives |
| Unauthorized | "Access denied" | 403 response | Redirect to login |
| Rate limited | "Too many requests" | 429 response | Show wait time |
```

### Step 6: UI/UX Considerations (if applicable)

For user-facing features:

```markdown
## UI/UX Notes

### User Flow
1. Entry point: [Where user starts]
2. Key interactions: [Click, type, swipe, etc.]
3. Exit points: [Where user ends up]

### Responsive Behavior
- Desktop: [Layout/behavior]
- Tablet: [Adaptations]
- Mobile: [Mobile-specific behavior]

### Loading States
- Initial load: [Skeleton/spinner]
- Action pending: [Button state, progress]
- Background refresh: [Indicator]

### Empty States
- No data: [What to show]
- Error state: [Recovery UI]
- First-time user: [Onboarding]

### Accessibility
- Keyboard navigation: [Tab order, shortcuts]
- Screen reader: [ARIA labels, announcements]
- Color contrast: [WCAG AA compliance]
```

### Step 7: Technical Constraints

Document implementation constraints:

```markdown
## Technical Constraints

### Dependencies
| Dependency | Type | Status | Owner |
|------------|------|--------|-------|
| [API/Service] | Internal | Ready/Pending | [Team] |
| [Third-party] | External | Integrated/Pending | [Vendor] |

### Limitations
- [Technical limitation 1 and workaround]
- [Technical limitation 2 and workaround]

### Non-Functional Requirements
| Requirement | Target | Measurement |
|-------------|--------|-------------|
| Response time | < 200ms p95 | APM |
| Availability | 99.9% | Monitoring |
| Throughput | 1000 req/s | Load test |

### Data Requirements
- Input: [Data types, formats, sizes]
- Output: [Response format, caching]
- Storage: [Persistence requirements]
```

### Step 8: Output Generation

Generate the feature spec using TEMPLATE.md. Verify:

- [ ] Clear one-sentence feature definition
- [ ] Primary user story with variants if needed
- [ ] Comprehensive acceptance criteria (happy + edge + error)
- [ ] Error states matrix complete
- [ ] Technical constraints documented
- [ ] Definition of done checklist included

## Examples

### Example 1: E-Commerce - Product Quick View

**Feature:** Display product quick view modal on hover for shoppers to preview details without leaving the catalog page.

**Parent PRD:** Catalog Browsing Experience (PRD-2024-015)

**Primary Story:**
```
As a shopper browsing the catalog,
I want to preview product details without leaving the page,
so that I can quickly evaluate products and continue browsing.
```

**Key Acceptance Criteria:**
```gherkin
Scenario: Quick view on hover
  Given I am on the product catalog page
  When I hover over a product card for 500ms
  Then a quick view modal appears
  And shows product image, name, price, and sizes
  And shows "Add to Cart" and "View Details" buttons

Scenario: Quick view on mobile
  Given I am on mobile device
  When I tap the quick view icon on a product card
  Then a bottom sheet slides up with product details

Scenario: Image gallery in quick view
  Given the quick view modal is open
  When I click the next arrow
  Then the next product image displays
  And current position indicator updates
```

**Error States:**
| Condition | Message | Action |
|-----------|---------|--------|
| Image load failure | Shows placeholder | Retry on visibility |
| Product out of stock | "Sold Out" badge | Hide Add to Cart |
| Network timeout | "Loading..." | Show retry button |

---

### Example 2: SaaS - Role Permission Editor

**Feature:** Allow admins to configure granular permissions for custom roles through a visual permission editor.

**Parent PRD:** Team Permissions System (PRD-2024-023)

**Primary Story:**
```
As an organization admin,
I want to configure exactly what each role can access,
so that I can enforce our security policies.
```

**Story Variants:**
```
Variant A - Bulk Permission Update:
As an admin managing many roles,
I want to update permissions across multiple roles at once,
so that I can efficiently apply policy changes.

Variant B - Permission Templates:
As an admin setting up a new role,
I want to start from a template,
so that I don't have to configure from scratch.
```

**Acceptance Criteria:**
```gherkin
Scenario: Grant permission to role
  Given I am editing the "Manager" role
  And I expand the "Reports" permission group
  When I toggle "View Financial Reports" to enabled
  Then the permission is added to the role
  And a "Save Changes" button appears
  And no changes are persisted until I click Save

Scenario: Permission dependency
  Given "Edit Reports" requires "View Reports"
  When I enable "Edit Reports"
  Then "View Reports" is automatically enabled
  And shows "Required by Edit Reports" tooltip

Scenario: Conflicting permissions
  Given the role has "View All Data"
  When I try to add "Restrict to Own Data"
  Then a conflict warning appears
  And I must resolve before saving
```

---

### Example 3: Fintech - Transaction Dispute Flow

**Feature:** Enable cardholders to dispute transactions directly from transaction alerts with guided flow and document upload.

**Parent PRD:** Fraud Detection & Response (PRD-2024-031)

**Primary Story:**
```
As a cardholder who received a suspicious transaction alert,
I want to dispute the charge immediately from the notification,
so that I can protect my account without calling support.
```

**Acceptance Criteria:**
```gherkin
Scenario: Initiate dispute from alert
  Given I received a transaction alert
  When I tap "Dispute This Charge"
  Then I see dispute reason options
  And can select "Fraudulent", "Duplicate", "Not Received", "Other"

Scenario: Upload supporting documents
  Given I selected "Not Received" as dispute reason
  When I reach the evidence step
  Then I can upload photos or documents
  And supported formats are JPG, PNG, PDF
  And max file size is 10MB

Scenario: Dispute submission confirmation
  Given I completed all dispute steps
  When I tap "Submit Dispute"
  Then I see confirmation with case number
  And I receive email confirmation
  And card is temporarily frozen pending review
```

**Error States:**
| Condition | Message | Action |
|-----------|---------|--------|
| File too large | "File exceeds 10MB limit" | Offer compression |
| Invalid file type | "Please upload JPG, PNG, or PDF" | Show accepted types |
| Submission failed | "Couldn't submit. Saved as draft." | Auto-save, retry later |
| Duplicate dispute | "Dispute already filed for this transaction" | Show existing case |

## Anti-Patterns to Avoid

### Too Broad Scope
```
❌ "User authentication feature" (multiple features bundled)
✅ "Password reset via email flow" (single, focused feature)
```

### Missing Edge Cases
```
❌ Only documenting happy path
✅ Including validation, errors, timeouts, rate limits
```

### Vague Acceptance Criteria
```
❌ "User can see products quickly"
✅ "Quick view modal appears within 300ms of hover"
```

### No Error States
```
❌ Assuming everything works
✅ Documenting what happens when things fail
```

### Implementation Details
```
❌ "Use Redis for caching with 5-minute TTL"
✅ "Response should be cached for improved performance"
(Save implementation details for technical spec)
```

## Integration with Other Skills

**Receives From:**
- `prd-writing` - High-level requirements to break down
- `prd-reviewing` - Approved PRD ready for feature specs

**Works With:**
- `feature-spec-reviewing` - Review and validate feature specs

**Leads To:**
- `technical-spec-writing` - Technical design for implementation
- `sparc-planning` - Implementation task breakdown

## Output Validation

Before finalizing the feature spec:

- [ ] One-sentence feature definition is clear
- [ ] Primary user story follows format
- [ ] Happy path acceptance criteria defined
- [ ] Edge cases documented (minimum 3)
- [ ] Error states matrix complete
- [ ] Performance expectations stated
- [ ] Security considerations noted
- [ ] Definition of done checklist included
- [ ] Links to parent PRD if applicable

## Resources

- See TEMPLATE.md for the complete feature spec output format


---

## Related Agent

For comprehensive specification guidance that coordinates this and other spec skills, use the **`specification-architect`** agent.
