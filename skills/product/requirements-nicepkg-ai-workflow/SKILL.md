---
name: requirements-specification
version: "2.0.0"
description: Master requirements gathering, user story writing, acceptance criteria definition, and scope management. Transform insights into clear, actionable specifications.
sasmp_version: "1.3.0"
bonded_agent: 03-requirements-definition
bond_type: PRIMARY_BOND
parameters:
  - name: feature_context
    type: string
    required: true
  - name: output_format
    type: string
    enum: [user_stories, prd, bdd, use_cases]
retry_logic:
  max_attempts: 3
  backoff: exponential
logging:
  level: info
  hooks: [start, complete, error]
---

# Requirements & Specification Skill

Transform customer insights into clear, detailed specifications that engineering can build from. Master user story writing, define acceptance criteria, and manage scope ruthlessly.

## User Story Writing (INVEST Format)

### INVEST Principles

**I** - Independent (minimal dependencies)
**N** - Negotiable (details can be discussed)
**V** - Valuable (delivers customer value)
**E** - Estimable (team can estimate effort)
**S** - Small (can complete in 1-2 sprints)
**T** - Testable (clear success criteria)

### User Story Template

```
As a [user role]
I want [action/capability]
So that [benefit/outcome]

Acceptance Criteria:
Given [context]
When [user action]
Then [expected result]
```

### Good vs Bad Examples

**Bad Story:**
```
As a user
I want a better dashboard
So that I can see my data
```
Problem: Too vague, not testable, too large

**Good Story:**
```
As a project manager
I want to see all tasks assigned to me in the last 24 hours
So that I can track what happened while I was offline

Acceptance Criteria:
Given I'm logged in
When I view the Home dashboard
Then I see a "Recent Tasks" section
And it shows tasks assigned to me from last 24 hours
And tasks are sorted by assignment time (newest first)
And clicking a task opens the task detail page
```

## Acceptance Criteria (BDD Format)

### Scenario Template

```
Scenario: [Specific user action]
Given [initial context/state]
When [user performs action]
Then [expected result]
And [additional verification]
```

### Example: Password Reset Feature

```
Scenario: User resets password with valid email
Given I'm on the login page
And I'm not logged in
When I click "Forgot Password?"
And enter my email address
And click "Send Reset Email"
Then I see message "Check your email for reset link"
And a password reset email is sent to that address
And the email contains a valid reset link

Scenario: User uses expired reset link
Given I received a password reset email
And the reset link is more than 24 hours old
When I click the reset link
Then I see "Link has expired"
And I'm offered to request a new reset link

Scenario: Password doesn't meet requirements
Given I'm on password reset page
When I enter password "123"
Then I see error "Password must be 8+ characters"
And the form doesn't submit
```

## Requirements Document Structure

### Executive Summary (1 page)
- Overview of feature/product
- Business goal/context
- Key benefits
- Timeline
- Success metrics

### Requirements Overview (5-10 pages)

**Functional Requirements**
- What the system must do
- Features and capabilities
- User interactions
- Data handling

**Non-Functional Requirements**
- Performance (response time < 2s)
- Scalability (support 10K concurrent users)
- Security (encrypt PII)
- Availability (99.9% uptime)
- Accessibility (WCAG AA compliance)

**Business Requirements**
- Why we're building this
- Business metrics
- Customer need
- Competitive advantage

**Constraints**
- Technical constraints
- Budget constraints
- Timeline constraints
- Resource constraints

### User Stories & Epics (20-50 pages)

Structure:
- **Epic:** Large initiative grouping related stories
- **User Stories:** Individual features (10-20 stories per epic)
- **Tasks:** Engineering breakdown (if needed)

**Each Story Includes:**
- Story ID and title
- As a... I want... so that...
- Acceptance criteria (3-8 scenarios)
- Story points estimate
- Dependencies
- Design reference (wireframe/mockup)
- Note/clarifications

### Use Cases & Flows (10-20 pages)

**Use Case Template:**
```
Use Case: [Use Case Name]
Primary Actor: [User role]
Precondition: [State before action]

Main Flow:
1. User does X
2. System responds with Y
3. User does Z
4. System returns result

Alternative Flows:
3a. If data invalid
    - System shows error
    - User corrects and resubmits
```

### Data Models (10 pages)

**Entity Relationship Diagram**
- Entities (User, Post, Comment)
- Relationships (User creates Posts)
- Attributes (Post title, content, creation_date)
- Primary keys, foreign keys

### UI/Wireframes (Attached)
- User interface mockups
- User flows and navigation
- Key interactions

## Scope Management

### MVP vs Nice-to-Have

**MoSCoW Method:**

**MUST Have** (Non-negotiable)
- Core functionality
- Without these: product won't work
- Must launch with these
- Example: User login, basic content view

**SHOULD Have** (Important but not critical)
- Enhance user experience
- Value add
- If time allows
- Example: Advanced search, saved preferences

**COULD Have** (Nice-to-have)
- Polish features
- Low priority
- Do if extra time/budget
- Example: Dark mode, animations

**WON'T Have** (Explicitly out of scope)
- Clear for future
- Helps say "no" to stakeholders
- Plan for later version
- Example: Mobile app (launching web first)

### Scope Creep Prevention

**Red Flags:**
- "Can we just add...?"
- "This would be better if..."
- "What about also including..."
- "One more thing..."

**Responses:**
- "That's a great idea. Let's add it to the roadmap for Q2."
- "That would add 3 weeks. What would you deprioritize?"
- "That's outside current scope. Document for next phase."

### Change Management

**Change Request Process:**
1. Document the change
2. Assess impact (time, complexity)
3. Present trade-offs
4. Get stakeholder decision
5. Update requirements document
6. Communicate to team

## Common Pitfalls

### Too Vague
❌ "Improve performance"
✅ "Reduce page load time from 4s to under 2s"

### No Success Criteria
❌ "Build dashboard"
✅ "Build dashboard showing active users in last 24h with 95% accuracy"

### Missing Context
❌ "Fix the bug"
✅ "When searching with special characters, results show error. Fix to handle special chars."

### Over-Specifying
❌ "Use Redux with saga middleware for state management"
✅ "State changes must be traceable and debuggable"

### Ambiguous Acceptance Criteria
❌ "System should be fast"
✅ "API response time < 200ms for 95th percentile"

## Requirements Review Checklist

- ✓ Each requirement is testable
- ✓ No requirement specifies implementation
- ✓ Dependencies identified and documented
- ✓ Acceptance criteria clear and complete
- ✓ Engineering has estimated effort
- ✓ Design mockups provided
- ✓ Data models documented
- ✓ Edge cases considered
- ✓ Scope clearly defined (MVP vs future)
- ✓ Success metrics identified
- ✓ Timeline realistic
- ✓ Reviewed by engineering lead
- ✓ Reviewed by design lead
- ✓ Stakeholder aligned

## Troubleshooting

### Yaygın Hatalar & Çözümler

| Hata | Olası Sebep | Çözüm |
|------|-------------|-------|
| Story çok büyük | Epic olarak yazıldı | Story breakdown |
| AC belirsiz | Vague criteria | Given/When/Then format |
| Scope creep | Change mgmt yok | Change request process |
| Missing edge cases | Happy path focus | Edge case workshop |

### Debug Checklist

```
[ ] Her story INVEST criteria geçiyor mu?
[ ] Acceptance criteria testable mı?
[ ] Non-functional requirements tanımlı mı?
[ ] Dependencies documented mı?
[ ] Engineering review yapıldı mı?
```

### Recovery Procedures

1. **Ambiguous Requirements** → Clarification meeting
2. **Scope Creep** → Trade-off matrix
3. **Missing Feasibility** → Engineering spike

---

**Write clear requirements and avoid 90% of project problems!**
