---
name: create-prd
description: Interactive PRD creation wizard with comprehensive question flow
argument-hint: <product-name>
---

# create-prd

**Category**: Product & Strategy

## Usage

```bash
create-prd <product-name>
```

## Arguments

- `<product-name>`: Required - The name of the product (will be used for filename and document title)

## Execution Instructions for Claude Code

When this command is run, Claude Code should:

1. Read the PRD template from `claude_settings/python/shared/templates/prd-template.md`
2. Start an interactive session with a welcome message
3. Guide the user through each section with detailed questions and examples
4. Allow users to review and edit responses before moving forward
5. Generate a complete PRD document with all responses
6. Save the document as `<product-name>-prd.md` in the current directory
7. Offer to create a summary or next steps document

## Interactive Session Flow

### Welcome & Overview
```
Welcome to the PRD Creation Wizard!

We'll work together to create a comprehensive Product Requirements Document for [product-name].
This process has 15 sections and typically takes 30-45 minutes.

You can:
- Type 'skip' to leave any optional section blank
- Type 'back' to review/edit the previous section
- Type 'preview' to see the document so far
- Type 'help' for assistance

Ready to begin? (yes/no)
```

### 1. **Document Setup** [Section 1/15]
```
Let's set up the document metadata:

Product Name: [pre-filled with <product-name>]
Is this correct? (yes/no):

Document Version [default: 1.0]:

Your Name/Author:

Document Status:
  1. Draft (default)
  2. Review
  3. Approved
  4. Released
Select (1-4):
```

### 2. **Executive Summary** [Section 2/15]
```
The executive summary should capture the essence of your product in 2-3 sentences.

Think about:
- What is the product?
- Who is it for?
- What key problem does it solve?

Example: "TaskMaster is a project management tool designed for remote teams. It solves
the challenge of coordinating work across time zones by providing async-first features
and intelligent scheduling. This enables teams to maintain productivity without requiring
constant real-time communication."

Please write your executive summary:
```

### 3. **Problem Statement** [Section 3/15]
```
Let's define the problem your product solves. We'll break this into 4 parts:

Part 1: The Core Problem
What specific problem are you solving? Be concrete and specific.

Example: "Remote teams struggle to coordinate work effectively across different time zones,
leading to delayed decisions, missed deadlines, and team frustration."

Your problem statement:
```

```
Part 2: Who Experiences This Problem?
Describe the people or organizations affected by this problem.

Example: "Small to medium software companies (10-200 employees) with distributed teams
across 3+ time zones, particularly those in tech, consulting, and creative industries."

Who experiences your problem:
```

```
Part 3: Current Solutions & Limitations
What solutions do people use today? What's wrong with them?

Example: "Teams currently use combinations of Slack, email, and basic project tools.
These lack timezone awareness, require manual coordination, and create information silos."

Current solutions and their limitations:
```

```
Part 4: Cost of Not Solving
What happens if this problem isn't addressed? Include metrics if possible.

Example: "Companies report 20% productivity loss due to coordination delays,
$50K+ annual cost in missed deadlines, and 30% higher turnover in remote positions."

Cost/impact of not solving:
```

### 4. **Product Vision & Objectives** [Section 4/15]
```
Let's establish your product vision and measurable objectives.

Part 1: Vision Statement
Write ONE sentence describing the ideal future state your product enables.

Example: "A world where distributed teams collaborate as effectively as co-located ones,
regardless of time zones or geography."

Your vision statement:
```

```
Part 2: Key Objectives
List 3-5 specific objectives your product aims to achieve.
Format as bullet points, starting each with an action verb.

Example:
- Reduce cross-timezone coordination time by 50%
- Enable 24-hour development cycles for global teams
- Improve remote employee satisfaction scores by 30%
- Decrease project delays caused by timezone misalignment to <5%

Your key objectives (one per line):
```

```
Part 3: Success Metrics
How will you measure success? Be specific and quantifiable.

Example:
- Time to decision: <4 hours (down from 24 hours)
- User adoption: 80% daily active users within teams
- NPS score: >50 within 6 months
- Customer retention: >90% annual

Your success metrics (one per line):
```

### 5. **Target Users & Personas** [Section 5/15]
```
Let's define your primary user persona in detail.

Primary User Name/Title:
Example: "Sarah Chen, Engineering Manager"

Your primary user:
```

```
Their Role/Job Description:
Example: "Manages a team of 8 engineers across US, Europe, and Asia. Responsible for
sprint planning, code reviews, and team coordination."

Role description:
```

```
Their Main Goals (what are they trying to achieve?):
Example: "Ship features on schedule, maintain code quality, keep team engaged and productive,
advance her career to Director level"

Main goals (list 2-4):
```

```
Their Pain Points (what frustrates them?):
Example: "Waiting hours for responses, duplicate work due to poor handoffs, difficulty
scheduling meetings, feeling disconnected from team"

Pain points (list 2-4):
```

```
Technical Proficiency:
  1. Low (basic computer skills)
  2. Medium (comfortable with standard tools)
  3. High (technical/power user)

Select (1-3):
```

```
Secondary User Types:
Do you have other important user types? (yes/no/skip)

[If yes, collect: name, role, and key differences from primary persona]
```

### 6. **User Stories & Requirements** [Section 6/15]
```
Let's prioritize features using the MoSCoW method:
- P0 (Must Have): Critical for launch, product fails without these
- P1 (Should Have): Important but can launch without if needed
- P2 (Nice to Have): Enhances experience but not essential

We'll use the format: "As a [user], I want to [action] so that [benefit]"

Must-Have Features (P0):
Example: "As an engineering manager, I want to see my team's availability across time zones
so that I can schedule work effectively"

Enter your P0 features (type 'done' when finished):
1:
```

```
Should-Have Features (P1):
Example: "As a team member, I want to set my preferred working hours so that colleagues
know when to expect responses"

Enter your P1 features (type 'done' when finished):
1:
```

```
Nice-to-Have Features (P2):
Example: "As a manager, I want AI-suggested optimal meeting times so that I can minimize
disruption across time zones"

Enter your P2 features (type 'done' when finished):
1:
```

### 7. **Solution Overview** [Section 7/15]
```
Now let's describe how your product solves the problem.

Part 1: Solution Approach
Describe your solution in 2-3 paragraphs. Focus on the "how" and "why" of your approach.

Example: "TaskMaster reimagines project management for async-first teams. Instead of
real-time dashboards, we provide time-shifted views that show each team member their
relevant work context. Our AI-powered handoff system ensures smooth transitions between
time zones...

[2-3 paragraphs continuing the example]"

Your solution approach:
```

```
Part 2: Key Differentiating Features
What makes your solution unique? List 3-5 features that competitors don't have.

Example:
- Timezone-aware task routing that automatically assigns work to available team members
- Async video standups with AI-generated summaries
- Predictive deadline alerts based on global team availability
- Cultural calendar integration to respect holidays/working patterns

Your key differentiators (one per line):
```

```
Part 3: User Journey
Describe the main user journey step-by-step from problem to solution.

Example:
1. Sarah logs in Monday morning in San Francisco
2. Sees AI-prioritized tasks handed off from Asia team overnight
3. Reviews async video updates from team members
4. Adjusts sprint tasks based on progress
5. Records handoff video for European team
6. Sets up automated task routing for her evening

Your user journey (numbered steps):
```

### 8. **Technical Considerations** [Section 8/15]
```
Let's define the technical requirements and architecture.

Part 1: Technical Requirements & Constraints
List specific technical needs and limitations.

Example:
- Must support 10,000+ concurrent users
- Real-time sync with <1 second latency
- 99.9% uptime SLA
- GDPR and SOC2 compliant
- Mobile-first responsive design

Your technical requirements:
```

```
Part 2: High-Level Architecture
Describe the technical approach (keep it high-level).

Example: "Microservices architecture on AWS with React frontend. Core services include
user management, task engine, notification system, and analytics. PostgreSQL for data,
Redis for caching, WebSockets for real-time updates."

Your architecture overview:
```

```
Part 3: Integration Requirements
What external systems must you integrate with?

Example:
- Google Calendar and Outlook for scheduling
- Slack and MS Teams for notifications
- GitHub/GitLab for code repositories
- Jira for issue tracking import/export

Your integrations (type 'none' if not applicable):
```

```
Part 4: Security & Compliance
What security and compliance requirements exist?

Example:
- End-to-end encryption for sensitive data
- GDPR compliance for EU users
- SOC2 Type II certification required
- Role-based access control (RBAC)
- Audit logs for all data access

Your security/compliance needs:
```

```
Part 5: Performance Requirements
Define specific performance targets.

Example:
- Page load time: <2 seconds on 3G
- API response time: <200ms for 95th percentile
- Support 1M API calls/day
- Data retention: 2 years active, 7 years archived

Your performance requirements:
```

### 9. **Design & User Experience** [Section 9/15]
```
Let's define the design and UX requirements.

Part 1: Design Principles
What principles should guide the design? (3-5 principles)

Example:
- Clarity over cleverness - every feature should be immediately understandable
- Async-first - optimize for non-real-time interaction
- Information density - show relevant context without overwhelming
- Accessibility - WCAG 2.1 AA compliant

Your design principles:
```

```
Part 2: Specific UI/UX Requirements
List concrete UI/UX needs.

Example:
- Dark mode support for late-night work
- Customizable dashboard layouts
- Keyboard shortcuts for power users
- Mobile app with offline capability
- Localization for 10+ languages

Your UI/UX requirements:
```

```
Part 3: Accessibility Standards
What accessibility requirements must be met?

Example:
- WCAG 2.1 AA compliance minimum
- Screen reader compatibility
- Keyboard-only navigation
- High contrast mode
- Closed captions for all video content

Your accessibility requirements:
```

### 10. **Dependencies & Risks** [Section 10/15]
```
Let's identify what could impact your project.

Part 1: Dependencies
What does your success depend on? Include technical, organizational, and external factors.

Example:
- Technical: AWS infrastructure, third-party APIs availability
- Organizational: Executive buy-in, dedicated dev team of 8+
- External: Regulatory approval for data handling
- Market: No major competitor launches similar feature

Your dependencies (categorize if helpful):
```

```
Part 2: Risks & Mitigation
Identify major risks and how you'll address them.

Format: Risk | Impact | Probability | Mitigation

Example:
- Risk: Third-party API changes break integrations
  Impact: High - core features unavailable
  Probability: Medium - happens 1-2x per year
  Mitigation: Abstract APIs, maintain vendor relationships, 30-day buffer

Your risks and mitigation strategies:
```

### 11. **Go-to-Market Strategy** [Section 11/15]
```
How will you launch and market this product?

Part 1: Launch Strategy
Describe your approach to launching.

Example: "Phased rollout starting with 10 beta customers in Q1, expanding to 100 in Q2,
public launch in Q3. Focus on tech companies with 50-200 employees already using
competing tools."

Your launch strategy:
```

```
Part 2: Marketing & Communication Plan
How will you reach your target users?

Example:
- Content marketing: Blog series on async work best practices
- Partner channels: Integration partnerships with Slack/Teams
- Direct sales: Target Fortune 500 remote-first companies
- Community: Build async work community on Discord

Your marketing plan:
```

```
Part 3: Training & Documentation
What training and docs are needed?

Example:
- Interactive onboarding tutorial (20 min)
- Video library for each major feature
- Admin guide for IT teams
- API documentation for developers
- Monthly webinars for new features

Your training/documentation plan:
```

### 12. **Timeline & Resources** [Section 12/15]
```
Let's plan the timeline and resource needs.

Part 1: Development Phases
Define major phases from now to launch and beyond.

Example:
- Phase 1 (Months 1-3): Core infrastructure and basic features
- Phase 2 (Months 4-6): Advanced features and integrations
- Phase 3 (Months 7-8): Beta testing and refinement
- Phase 4 (Month 9): Public launch
- Phase 5 (Months 10-12): Scale and optimize

Your development phases:
```

```
Part 2: Key Milestones
List specific milestones with target dates.

Example:
- Jan 15: Architecture finalized
- Mar 1: Alpha version with core features
- May 15: Beta launch with 10 customers
- Jul 1: Feature complete
- Sep 1: Public launch
- Dec 15: 1,000 customers milestone

Your milestones (include dates):
```

```
Part 3: Resource Requirements
What team and resources do you need?

Example:
- Engineering: 2 senior, 4 mid-level developers
- Design: 1 senior product designer
- Product: 1 PM (you)
- QA: 1 dedicated tester
- DevOps: 0.5 FTE shared resource
- Budget: $1.2M for first year

Your resource needs:
```

### 13. **Success Criteria & KPIs** [Section 13/15]
```
How will you measure and track success?

Part 1: Success Criteria
Define what success looks like (qualitative and quantitative).

Example:
- 1,000 paying customers within 12 months
- 4.5+ star rating on review sites
- <2% monthly churn rate
- Break-even by month 18
- Recognized as leader in async tools category

Your success criteria:
```

```
Part 2: Key Performance Indicators
List 3-5 specific KPIs with target values.

Example:
- Monthly Recurring Revenue (MRR): $100K by month 12
- Daily Active Users (DAU): 60% of total users
- Customer Acquisition Cost (CAC): <$500
- Net Promoter Score (NPS): >50
- Feature Adoption Rate: >70% using core features weekly

Your KPIs with targets:
```

```
Part 3: Monitoring & Reporting Plan
How will you track and communicate progress?

Example: "Weekly metrics dashboard in Mixpanel, monthly stakeholder reports, quarterly
board presentations. Real-time alerts for critical metrics. Customer success team
monitors NPS and churn indicators daily."

Your monitoring plan:
```

### 14. **Open Questions & Risks** [Section 14/15]
```
What questions remain unanswered?

List any open questions, unknowns, or areas needing research.

Example:
- Pricing model: Freemium vs trial? Needs market research
- Infrastructure costs at scale: Need AWS architect consultation
- Regulatory requirements in Asia: Legal review needed
- Optimal team size limits: UX research required

Your open questions:
```

### 15. **Appendix Content** [Section 15/15]
```
Do you have additional supporting information to include?

Options:
1. Competitive analysis
2. User research data
3. Technical specifications
4. Market research
5. Financial projections
6. None - skip appendix

Select what to include (comma-separated numbers, or 'none'):
```

[For each selected appendix section, provide appropriate prompts]

### Final Review
```
Great work! Your PRD is ready for review.

Would you like to:
1. Preview the complete document
2. Edit any section
3. Save and finish
4. Save and create an executive summary

Select (1-4):
```

## Output Format

Generate a well-formatted markdown document that:
- Replaces all template placeholders with collected responses
- Maintains professional tone and formatting
- Uses proper markdown syntax (headers, lists, tables, emphasis)
- Includes a table of contents for easy navigation
- Adds helpful formatting like horizontal rules between major sections
- Preserves all user formatting and line breaks in responses

## Example Usage

```bash
create-prd awesome-product
```

This starts the interactive wizard to create `awesome-product-prd.md`

## Implementation Tips for Claude Code

1. **Progress Tracking**: Always show section numbers (e.g., "[Section 3/15]")
2. **Input Validation**:
   - Don't accept empty responses for required fields
   - Confirm before accepting 'skip' on important sections
3. **Navigation**: Support 'back', 'preview', and 'help' commands at any point
4. **Auto-save**: Save progress every 3 sections to prevent data loss
5. **Smart Defaults**: Pre-fill obvious fields (date, version 1.0, etc.)
6. **Examples**: Provide relevant examples for complex sections
7. **Review**: Allow editing any section before final save
8. **Output**:
   - Save to current directory as `<product-name>-prd.md`
   - Show full file path after saving
   - Offer to open in default editor

## Error Handling

- If template file is missing: Provide error and suggest checking installation
- If write fails: Offer alternative location or clipboard copy
- If user abandons: Offer to save partial progress
- For invalid inputs: Provide specific guidance on correct format
