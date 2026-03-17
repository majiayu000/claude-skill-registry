---
name: prd-documentation
description: Product Requirements Document creation and feature specification writing. Use when writing PRDs, technical specs, feature documentation, or requirements. Triggers on "PRD", "product requirements", "feature spec", "technical requirements", "functional spec".
allowed-tools: Read, Write, Edit, Grep, Glob
model: inherit
---

# PRD Documentation Skill - Professional Product Requirements Writing

This Skill provides expertise in writing comprehensive, clear, and actionable Product Requirements Documents (PRDs) and Feature Specifications.

## When to Use This Skill

Use this Skill when you need to:
- Write complete PRD documents
- Create feature specifications
- Define technical requirements
- Document acceptance criteria
- Specify non-functional requirements
- Create user stories with details
- Plan product launches

## Core Process

### Step 1: Gather Requirements

**Essential Inputs:**
- Validated business idea (from idea-agent)
- Target users and personas
- Business objectives and success metrics
- Key features and scope
- Technical constraints
- Timeline and resources

**If Missing, Ask:**
- "What problem does this product solve?"
- "Who are the primary users?"
- "What are the must-have features for MVP?"
- "What are the business goals and KPIs?"
- "What technical constraints exist?"
- "When is the target launch date?"

### Step 2: Use Reference Templates

**Always read these templates:**

```bash
# Use Read tool:
/reference/prd-templates/standard-prd-template.md
/reference/prd-templates/feature-spec-template.md
```

These provide:
- Complete PRD structure (15 sections)
- Feature specification format
- Acceptance criteria templates
- Technical requirements checklist
- Success metrics frameworks

### Step 3: PRD Structure

Follow this comprehensive 15-section structure:

#### 1. Document Information
```markdown
- Product Name: [Name]
- Version: [1.0]
- Author: [Name]
- Last Updated: [Date]
- Status: [Draft | In Review | Approved | In Development]
```

#### 2. Executive Summary
**Product Overview:**
- One-paragraph description
- Core value proposition

**Problem Statement:**
- What problem we're solving
- Why it matters now

**Success Criteria:**
- Primary metric and target
- Secondary metrics

#### 3. Goals and Objectives

**Business Goals:**
- Revenue impact
- Market position
- Strategic alignment

**User Goals:**
- User benefits
- Problem solved
- Outcome achieved

**Product Objectives (OKRs):**
```markdown
Objective 1: [Qualitative, inspiring goal]
├─ Key Result 1.1: [Measurable, time-bound]
├─ Key Result 1.2: [Measurable, time-bound]
└─ Key Result 1.3: [Measurable, time-bound]

Objective 2: [Qualitative goal]
├─ Key Result 2.1: [Measurable]
└─ Key Result 2.2: [Measurable]
```

#### 4. Target Audience

**Primary Persona:**
```markdown
### Persona: [Name]

Demographics:
- Age: [Range]
- Location: [Where]
- Job/Role: [Title]
- Tech Proficiency: [High/Medium/Low]

Goals:
- [Goal 1]
- [Goal 2]

Pain Points:
- [Pain 1]
- [Pain 2]

Current Solutions:
- [What they use today]

Quote:
"[In their own words]"
```

#### 5. User Stories and Use Cases

**Format:**
```markdown
### User Story: [Title]

As a [specific user type],
I want to [specific action],
So that [specific benefit].

**Acceptance Criteria:**

Given [precondition]
When [action]
Then [expected outcome]
And [additional outcome]

**Priority:** P0 | P1 | P2
**Story Points:** [1-13]
```

**Use Case Format:**
```markdown
### Use Case: [Title]

**Actor:** [Who performs this]
**Trigger:** [What initiates this]
**Preconditions:** [What must be true]

**Main Flow:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Alternative Flows:**
- If [condition], then [alternative steps]

**Postconditions:** [System state after completion]
```

#### 6. Features and Requirements

**For Each Feature:**

```markdown
## Feature: [Name]

**Description:**
[What it is and why it's important]

**User Value:**
[How it benefits users]

**User Story:**
As a [user],
I want to [action],
So that [benefit].

**Functional Requirements:**
1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]

**Acceptance Criteria:**
Given [context]
When [action]
Then [outcome]

**Priority:** P0 (Must) | P1 (Should) | P2 (Could)
**Effort:** XS | S | M | L | XL
**Dependencies:** [Feature IDs or systems]
**Technical Notes:** [Implementation considerations]

**Edge Cases:**
- [Edge case 1 and handling]
- [Edge case 2 and handling]

**Error Handling:**
- [Error scenario 1]: [Error message and action]
- [Error scenario 2]: [Error message and action]
```

**Non-Functional Requirements:**

```markdown
### Performance
- Page Load Time: < [X] seconds
- API Response Time: < [Y] ms
- Concurrent Users: [Z] minimum
- Data Processing: [Rate/volume]

### Security
- Authentication: [Method]
- Authorization: [RBAC, ABAC]
- Data Encryption: [At rest, in transit]
- Compliance: [GDPR, HIPAA, SOC 2]
- Input Validation: [Rules]
- Rate Limiting: [Limits]

### Scalability
- Horizontal Scaling: [Yes/No]
- Auto-scaling: [Yes/No]
- Peak Load Capacity: [X users/requests]
- Database Sharding: [If applicable]

### Reliability
- Uptime SLA: [99.9%]
- Disaster Recovery: RPO/RTO
- Backup Strategy: [Frequency, retention]
- Monitoring: [Tools, alerts]

### Accessibility
- WCAG Level: [AA | AAA]
- Screen Reader: [Supported]
- Keyboard Navigation: [Full support]
- Color Contrast: [Ratio]
- Focus Indicators: [Visible]

### Browser/Platform Support
**Desktop:**
- Chrome: [Latest 2 versions]
- Firefox: [Latest 2 versions]
- Safari: [Latest 2 versions]
- Edge: [Latest 2 versions]

**Mobile:**
- iOS Safari: [Latest 2 versions]
- Chrome Mobile: [Latest 2 versions]
```

#### 7. Design and UX

```markdown
### Design Principles
1. [Principle 1: e.g., Simplicity first]
2. [Principle 2: e.g., Progressive disclosure]
3. [Principle 3: e.g., Accessible by default]

### Key Screens
**Screen 1: [Name]**
- Purpose: [What users do here]
- Key Elements: [Components, CTAs]
- User Flow: [Navigation]

### User Flows
**Flow: [Name]**
1. [Entry point]
2. [Step 1]
3. [Decision point]
4. [Step 2]
5. [Exit/Success state]

### Design Assets
- Wireframes: [Link to Figma/Sketch]
- Mockups: [Link]
- Design System: [Link]
- Style Guide: [Link]
```

#### 8. Technical Specifications

```markdown
### System Architecture
[High-level architecture diagram or description]

```
Frontend <-> API Gateway <-> Backend Services <-> Database
                   ↓
            Third-party APIs
```

### Technology Stack
- Frontend: [React, Vue, Angular]
- Backend: [Node.js, Python, Java]
- Database: [PostgreSQL, MongoDB]
- Infrastructure: [AWS, GCP, Azure]
- Cache: [Redis, Memcached]

### API Requirements
**Endpoint:** `POST /api/resource`

Request:
```json
{
  "field1": "value",
  "field2": 123
}
```

Response:
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "created_at": "timestamp"
  }
}
```

Error Codes:
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Internal Server Error

### Data Model
**Entity: User**
```
{
  id: UUID (PK)
  email: String (unique, indexed)
  name: String
  created_at: Timestamp
  updated_at: Timestamp
}
```

**Relationships:**
- User has_many Orders
- Order belongs_to User

### Integrations
| Service | Purpose | API | Auth |
|---------|---------|-----|------|
| Stripe | Payments | REST | API Key |
| SendGrid | Email | REST | API Key |
| AWS S3 | Storage | SDK | IAM |
```

#### 9. Analytics and Metrics

```markdown
### Key Performance Indicators

**Product KPIs:**
- Acquisition: [New users/month]
- Activation: [% completing onboarding]
- Engagement: [DAU, session length]
- Retention: [Day 7, Day 30]
- Revenue: [MRR, ARPU]
- Referral: [NPS, viral coefficient]

**Success Metrics:**
| Metric | Current | Target | Timeline |
|--------|---------|--------|----------|
| User Adoption | 0 | 10K users | 3 months |
| Activation Rate | - | 40% | Launch+30d |
| DAU/MAU | - | 25% | Launch+90d |
| NPS | - | 40+ | Launch+90d |

### Event Tracking Plan

| Event Name | Description | Properties | Priority |
|------------|-------------|------------|----------|
| user_signup | User completes registration | source, plan | P0 |
| feature_used | User activates key feature | feature_name, duration | P0 |
| conversion | User upgrades to paid | plan, amount | P0 |
| error_occurred | System error | error_type, page | P1 |

### A/B Testing

**Test 1: [Onboarding Flow]**
- Hypothesis: [Simplified onboarding will increase activation by 20%]
- Variants: Control vs Variant A
- Success Metric: [Onboarding completion rate]
- Sample Size: [10,000 users]
- Duration: [2 weeks]
```

#### 10. Risks and Mitigations

```markdown
| Risk | Probability | Impact | Mitigation Strategy |
|------|-------------|--------|---------------------|
| Technical complexity | Medium | High | Prototype early, allocate buffer time |
| Low user adoption | Low | High | Beta test, user research, iterative launch |
| Third-party dependency | Medium | Medium | Alternative vendor, fallback plan |
| Competitive response | High | Medium | Focus on differentiation, speed to market |
| Scope creep | High | Medium | Strict prioritization, clear MVP definition |
```

#### 11. Timeline and Milestones

```markdown
### Project Phases

**Phase 1: Planning (Weeks 1-2)**
- [ ] PRD Approval
- [ ] Design Review
- [ ] Technical Spec Complete

**Phase 2: Development (Weeks 3-8)**
- Sprint 1 (Weeks 3-4): Core features
- Sprint 2 (Weeks 5-6): Integration
- Sprint 3 (Weeks 7-8): Polish and bug fixes

**Phase 3: Testing (Weeks 9-10)**
- [ ] QA Testing
- [ ] User Acceptance Testing
- [ ] Performance Testing
- [ ] Security Audit

**Phase 4: Launch (Week 11)**
- [ ] Soft Launch (10% rollout)
- [ ] Monitor metrics
- [ ] Full Launch (100% rollout)

### Dependencies
| Dependency | Owner | Status | Due Date | Blocker? |
|------------|-------|--------|----------|----------|
| [API from Team B] | [Name] | In Progress | [Date] | Yes |
| [Design System Update] | [Name] | Not Started | [Date] | No |
```

#### 12. Open Questions and Assumptions

```markdown
### Open Questions
1. **[Question about feature X]**
   - Decision needed by: [Date]
   - Owner: [Name]
   - Options: A, B, C
   - Recommendation: [Option A because...]

2. **[Question about technical approach]**
   - Decision needed by: [Date]
   - Owner: [Name]

### Assumptions
1. Users have stable internet connection
2. 80% of traffic from mobile devices
3. Third-party API has 99.9% uptime
4. Users familiar with similar products

### Out of Scope (Explicitly NOT Included)
1. [Feature X] - Planned for v2.0
2. [Platform Y support] - Not in roadmap
3. [Integration Z] - Deprioritized
```

#### 13-15. Supporting Sections

```markdown
### Resources and Team
**Core Team:**
- Product Manager: [Name]
- Engineering Lead: [Name]
- Design Lead: [Name]
- QA Lead: [Name]

**Extended Team:**
- Engineers: [X people]
- Designers: [Y people]
- QA: [Z people]

### Launch Plan
**Pre-Launch:**
- [ ] Beta program (100 users, 2 weeks)
- [ ] Marketing materials
- [ ] Support documentation
- [ ] Team training

**Launch:**
- [ ] Announcement (blog, email, social)
- [ ] Press release
- [ ] Customer outreach

**Post-Launch:**
- [ ] Monitor metrics daily
- [ ] User feedback collection
- [ ] Iteration plan

### Change Log
| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2024-01-15 | 1.0 | Initial draft | PM Name |
| 2024-01-20 | 1.1 | Added technical specs | PM Name |
| 2024-01-25 | 2.0 | Final for review | PM Name |
```

## Best Practices

### Writing Style
✅ **Do:**
- Use clear, unambiguous language
- Be specific and measurable
- Include examples
- Use tables and bullets
- Write from user perspective
- Define acronyms on first use

❌ **Don't:**
- Use vague terms ("user-friendly", "fast")
- Mix implementation with requirements
- Skip edge cases and errors
- Write lengthy paragraphs
- Assume technical knowledge

### Acceptance Criteria
✅ **Do:**
- Use Given-When-Then format
- Cover happy path, errors, edge cases
- Make testable and measurable
- Include visual feedback requirements
- Specify error messages

❌ **Don't:**
- Write vague criteria ("works well")
- Focus only on happy path
- Skip error handling
- Forget accessibility
- Leave untestable criteria

### Prioritization
Use MoSCoW:
- **P0 (Must Have)**: Blocking for launch
- **P1 (Should Have)**: Important, not blocking
- **P2 (Could Have)**: Nice to have
- **P3 (Won't Have)**: Out of scope

### Review Checklist

Before finalizing PRD:
- [ ] All sections complete
- [ ] User stories have acceptance criteria
- [ ] Success metrics defined and measurable
- [ ] Technical requirements clear
- [ ] Dependencies identified
- [ ] Risks assessed with mitigations
- [ ] Timeline realistic
- [ ] Open questions documented
- [ ] Reviewed by engineering
- [ ] Reviewed by design
- [ ] Reviewed by QA
- [ ] Approved by stakeholders

## Output Format

**File Naming:**
```
[product-name]-prd-v[version].md
Example: ai-study-planner-prd-v1.0.md
```

**Location:**
```
/docs/prd/[filename]
```

**Format:**
- Markdown with proper headings (##, ###)
- Tables for comparisons and data
- Code blocks for technical specs
- Checkboxes for action items
- Links to external resources

## Example Output

See `/reference/prd-templates/standard-prd-template.md` for complete example.

## Integration Points

This Skill works with:
- **prd-agent**: Primary user of this skill
- **idea-generation**: Takes validated idea as input
- **userstory-documentation**: Provides requirements for story breakdown
- **pm-knowledge-base**: Uses OKR, metrics, prioritization frameworks

Always use reference templates as foundation, customizing for specific product needs.
