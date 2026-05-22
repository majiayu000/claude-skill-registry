---
name: ux-creator
description: This skill should be used when creating user experiences from requirements or evaluating and improving existing UX designs. Covers translating requirements into effective UX flows, user journey mapping, information architecture, interaction patterns, and UX evaluation methodologies (heuristic evaluation, cognitive walkthrough). Use when tasks involve UX design, user flow creation, UX analysis, or improving user experience.
---

# UX Creator

## Overview

To create effective user experiences, translate requirements into well-designed user flows, information architectures, and interaction patterns while applying established UX principles. This skill provides comprehensive guidance for creating new UX designs from requirements and evaluating existing interfaces to identify improvements.

**User Experience (UX)** encompasses all aspects of a user's interaction with a product, including usability, accessibility, efficiency, and satisfaction. Unlike UI (visual design and implementation), UX focuses on the overall journey, flow, and experience.

**Current Standards (2025):**
- **Principles**: Nielsen's 10 Usability Heuristics, Gestalt principles
- **Accessibility**: WCAG 2.2 Level AA as UX foundation
- **Design Systems**: Material 3 Expressive, iOS Liquid Glass (iOS 26)
- **Evaluation**: Heuristic evaluation, cognitive walkthrough
- **Mobile-first**: Responsive, adaptive layouts for all screen sizes

## Decision Tree: Choosing Your Workflow

```
User Request → What is the goal?
    |
    ├─ Creating new UX from requirements?
    │   ├─ Simple feature or page? → Quick Start: Requirements to UX
    │   └─ Complex user journey? → Workflow 1: Creating UX from Requirements
    │
    ├─ Evaluating existing UX?
    │   ├─ Need quick assessment? → Quick Start: UX Evaluation
    │   └─ Comprehensive analysis? → Workflow 2: Evaluating and Improving UX
    │
    ├─ Need UX principles guidance?
    │   └─ Load references/ux-principles.md
    │
    ├─ Looking for interaction patterns?
    │   └─ Load references/interaction-patterns.md
    │
    ├─ Need evaluation methodology?
    │   └─ Load references/ux-evaluation-framework.md
    │
    ├─ Converting requirements to UX?
    │   └─ Load references/requirements-to-ux.md
    │
    └─ Reviewing UX mistakes?
        └─ Load references/anti-patterns.md
```

## Quick Start: Requirements to UX

To quickly translate a simple requirement into UX design:

### Step 1: Clarify the Requirement

Identify:
- **User goal**: What does the user want to accomplish?
- **Context**: Where, when, and why will they do this?
- **Success criteria**: What makes this experience successful?

**Example:**
- Requirement: "Users should be able to reset their password"
- User goal: Regain access to account when password is forgotten
- Context: Login page, user has forgotten password
- Success: User receives reset link and successfully creates new password

### Step 2: Design the User Flow

Map the sequential steps:

```
Password Reset Flow:
1. User clicks "Forgot password?" on login page
2. System displays email input form
3. User enters email address
4. System validates email (exists in system)
5. System sends reset link to email
6. System confirms "Check your email"
7. User clicks link in email
8. System validates link (not expired, correct token)
9. System displays new password form
10. User enters and confirms new password
11. System validates password requirements
12. System updates password
13. System confirms success and redirects to login
```

### Step 3: Apply Interaction Patterns

Choose appropriate patterns from `references/interaction-patterns.md`:
- **Form pattern**: Inline validation, clear error messages
- **Feedback pattern**: Loading state while sending email, success confirmation
- **Error handling**: Clear recovery path if email not found

### Step 4: Validate Against UX Principles

Check against Nielsen's heuristics:
- ✅ **Visibility of system status**: Show "Sending email..." and "Email sent"
- ✅ **Error prevention**: Validate email format before submission
- ✅ **Help users recover from errors**: Clear message if email not found with option to try again
- ✅ **Recognition rather than recall**: Show email address in confirmation message

For detailed principles, load `references/ux-principles.md`.

## Quick Start: UX Evaluation

To quickly evaluate an existing UX:

### Run Quick Heuristic Check

Evaluate against Nielsen's 10 heuristics:

1. **Visibility of system status**: Does the system always inform users what's happening?
2. **Match between system and real world**: Does it use familiar language and concepts?
3. **User control and freedom**: Can users easily undo/redo actions?
4. **Consistency and standards**: Are patterns consistent throughout?
5. **Error prevention**: Does it prevent errors before they occur?
6. **Recognition rather than recall**: Are options visible, not requiring memorization?
7. **Flexibility and efficiency**: Does it support both novice and expert users?
8. **Aesthetic and minimalist design**: Does it avoid unnecessary elements?
9. **Help users recover from errors**: Are error messages helpful and constructive?
10. **Help and documentation**: Is help available when needed?

### Document Findings

Use `assets/ux-evaluation-template.md` for quick documentation:

```markdown
## UX Evaluation: [Feature Name]

### Overall Score: [X/10]

### Critical Issues (Must Fix):
- [Issue 1 with heuristic violated]

### Major Issues (Should Fix):
- [Issue 2 with heuristic violated]

### Minor Issues (Nice to Fix):
- [Issue 3 with heuristic violated]

### Recommendations:
1. [Specific improvement with rationale]
```

For comprehensive evaluation methodology, use Workflow 2 below.

## Workflow 1: Creating UX from Requirements

Follow this systematic approach to transform requirements into effective UX designs.

### Step 1: Analyze Requirements

To begin UX design, deeply understand the requirements:

1. **Identify user needs**: What problem is being solved?
2. **Define user personas**: Who will use this? (roles, goals, context)
3. **List functional requirements**: What must the system do?
4. **Identify constraints**: Technical, business, or design limitations
5. **Define success metrics**: How to measure UX effectiveness?

**Questions to ask:**
- Who is the primary user? Secondary users?
- What tasks will they perform?
- What are their pain points with current solutions?
- What is their technical expertise level?
- What devices/contexts will they use this in?
- What are the performance expectations?

Load `references/requirements-to-ux.md` for detailed requirement analysis techniques.

### Step 2: Create User Journey Map

To visualize the end-to-end experience:

1. **Define stages**: What phases does the user go through?
2. **Identify touchpoints**: Where does the user interact with the system?
3. **Map emotions**: What does the user feel at each stage?
4. **Find pain points**: Where does friction occur?
5. **Spot opportunities**: Where can UX be improved?

**Use the template:** `assets/user-journey-template.md`

**Example: E-commerce Purchase Journey**

| Stage | Touchpoint | User Actions | Emotions | Pain Points | Opportunities |
|-------|------------|--------------|----------|-------------|---------------|
| Discovery | Homepage | Browse products | Curious, interested | Too many options | Personalized recommendations |
| Research | Product page | Read details, reviews | Uncertain | Missing information | Clear comparison tool |
| Decision | Cart | Add items, review | Anxious | Unexpected fees | Transparent pricing upfront |
| Purchase | Checkout | Enter info, pay | Rushed, stressed | Too many form fields | Autofill, saved payment |
| Confirmation | Order confirmation | Review order | Relieved | Unclear delivery time | Clear timeline, tracking link |

### Step 3: Design Information Architecture

To organize content and functionality:

1. **List all content/features**: Inventory everything needed
2. **Group related items**: Create logical categories
3. **Create hierarchy**: Organize by importance and relationships
4. **Define navigation**: How users move between sections
5. **Validate with card sorting**: Would users group things this way?

**Example: Dashboard IA**

```
Dashboard (Home)
├── Overview
│   ├── Key Metrics
│   ├── Recent Activity
│   └── Quick Actions
├── Analytics
│   ├── Traffic
│   ├── Conversions
│   └── User Behavior
├── Content
│   ├── Pages
│   ├── Media Library
│   └── Comments
└── Settings
    ├── Profile
    ├── Preferences
    └── Integrations
```

### Step 4: Design User Flows

To define how users accomplish their goals:

1. **Identify key tasks**: What are the main user goals?
2. **Map happy path**: Ideal flow from start to completion
3. **Define decision points**: Where does the user make choices?
4. **Add alternative paths**: What if they choose differently?
5. **Include error states**: What happens when things go wrong?
6. **Optimize for efficiency**: Minimize steps, reduce cognitive load

**Example: User Registration Flow**

```
Start
  ↓
[Landing Page]
  ↓
Click "Sign Up"
  ↓
[Registration Form]
  ├─ Enter email → Validate email
  │   ├─ Valid? Continue
  │   └─ Invalid? Show error, allow retry
  ├─ Enter password → Validate strength
  │   ├─ Strong? Continue
  │   └─ Weak? Show requirements, allow retry
  └─ Agree to terms → Required checkbox
      ↓
Click "Create Account"
  ↓
[Loading State] "Creating your account..."
  ↓
Create account in system
  ├─ Success? → Send verification email → [Success Page] → Redirect to onboarding
  └─ Failure? → [Error Page] → Allow retry
```

### Step 5: Select Interaction Patterns

To design specific UI behaviors:

1. **Match patterns to tasks**: Choose appropriate patterns for each interaction
2. **Ensure consistency**: Use same pattern for similar interactions
3. **Prioritize familiarity**: Use established patterns users recognize
4. **Consider accessibility**: Ensure keyboard, screen reader support
5. **Optimize for mobile**: Touch-friendly, thumb-reachable

Load `references/interaction-patterns.md` for comprehensive pattern library.

**Common pattern selections:**
- **Navigation**: Tab bar (mobile), sidebar (desktop), breadcrumbs (deep hierarchy)
- **Forms**: Inline validation, progressive disclosure, smart defaults
- **Feedback**: Toast notifications (non-critical), modal alerts (critical), loading skeletons
- **Search**: Autocomplete, filters, recent searches

### Step 6: Apply UX Principles

To ensure high-quality UX:

1. **Apply Nielsen's heuristics**: Validate against all 10 principles
2. **Follow Gestalt principles**: Use proximity, similarity, continuity for visual organization
3. **Reduce cognitive load**: Minimize working memory requirements
4. **Ensure accessibility**: WCAG 2.2 AA compliance as foundation
5. **Optimize performance**: Fast load times, responsive interactions

Load `references/ux-principles.md` for detailed guidance on applying principles.

**Key checks:**
- ✅ Is the user always informed about system status?
- ✅ Can users easily undo mistakes?
- ✅ Are critical actions protected from accidental triggering?
- ✅ Is help available without leaving the current context?
- ✅ Are related elements grouped visually?

### Step 7: Document UX Design

To communicate the UX design:

1. **Use the template**: `assets/ux-design-doc-template.md`
2. **Include user flows**: Diagrams showing key paths
3. **Document IA**: Hierarchy and navigation
4. **List interaction patterns**: Specify patterns for each feature
5. **Add rationale**: Explain key UX decisions
6. **Include wireframes**: Low/mid-fidelity mockups (optional)

**Documentation ensures:**
- Developers understand the intended UX
- Stakeholders can review and approve
- Future iterations maintain consistency
- UX decisions are traceable

## Workflow 2: Evaluating and Improving UX

Follow this approach to systematically evaluate existing UX and identify improvements.

### Step 1: Understand the Context

To begin evaluation, gather context:

1. **Identify the system**: What is being evaluated? (feature, page, flow, entire product)
2. **Define user goals**: What should users be able to accomplish?
3. **Know the users**: Who are the primary users? Their expertise level?
4. **Understand constraints**: Technical, business, or legacy constraints
5. **Define scope**: What aspects of UX are being evaluated?

### Step 2: Choose Evaluation Method

To select appropriate evaluation approach:

**Heuristic Evaluation** (recommended for most cases):
- **Best for**: Identifying broad usability issues
- **Time required**: 1-4 hours depending on scope
- **Evaluators**: 3-5 UX experts or knowledgeable individuals
- **Output**: List of issues mapped to heuristics with severity ratings

**Cognitive Walkthrough** (task-specific evaluation):
- **Best for**: Evaluating learnability of specific tasks
- **Time required**: 2-6 hours for key tasks
- **Evaluators**: 2-3 people (can be non-experts)
- **Output**: Issues with task completion, especially for new users

**Combined Approach** (most comprehensive):
- Use heuristic evaluation for broad issues
- Use cognitive walkthrough for critical tasks
- Combine findings for complete picture

Load `references/ux-evaluation-framework.md` for detailed methodologies.

### Step 3: Conduct Heuristic Evaluation

To perform heuristic evaluation:

1. **Review against each heuristic**: Go through Nielsen's 10 systematically
2. **Document violations**: Note where each heuristic is violated
3. **Rate severity**: Critical (blocks users), Major (frustrates users), Minor (annoys users)
4. **Provide examples**: Screenshot or describe specific instances
5. **Suggest improvements**: How could this be fixed?

**Evaluation template:**

| Heuristic | Violation | Severity | Location | Recommendation |
|-----------|-----------|----------|----------|----------------|
| #1 Visibility of system status | No feedback after form submission | Critical | Checkout page | Add loading state and confirmation message |
| #5 Error prevention | No confirmation before deleting account | Critical | Settings page | Add confirmation modal with consequences explained |
| #8 Aesthetic and minimalist design | Homepage cluttered with 20+ links | Major | Homepage | Group links into categories, hide secondary actions |

### Step 4: Conduct Cognitive Walkthrough

To evaluate task learnability:

1. **Define the task**: Specific goal a new user should accomplish
2. **List the correct actions**: Step-by-step ideal path
3. **For each action, ask**:
   - Will users know what to do?
   - Will users see how to do it?
   - Will users understand they did the right thing?
   - Will users know they're making progress?
4. **Document issues**: Where do users likely struggle?
5. **Suggest improvements**: How to make each step clearer?

**Example: Task = "Change profile picture"**

| Step | Action | Will users know what to do? | Issues | Fix |
|------|--------|------------------------------|--------|-----|
| 1 | Navigate to profile | Maybe - "Profile" in menu, but might expect "Settings" | Users may look in wrong place | Add "Edit Profile" to settings menu too |
| 2 | Click profile picture | Unlikely - no visual affordance indicating it's clickable | No hover state, no edit icon | Add camera icon overlay on hover |
| 3 | Upload new image | Yes - file picker is standard | Large files cause slow upload with no progress | Add progress bar and file size limit |

### Step 5: Analyze and Prioritize Issues

To organize findings:

1. **Group by severity**: Critical → Major → Minor
2. **Group by heuristic/principle**: See patterns in violations
3. **Identify systemic issues**: Are similar problems repeated?
4. **Estimate impact**: How many users affected? How often?
5. **Consider effort**: What's the fix complexity?
6. **Prioritize**: Critical + high impact + low effort first

**Prioritization matrix:**

```
Impact    | Critical       | Major          | Minor
----------|----------------|----------------|---------------
High      | Fix now        | Fix next       | Fix when possible
Medium    | Fix next       | Fix soon       | Backlog
Low       | Fix soon       | Fix when time  | Optional
```

### Step 6: Design Improvements

To fix identified issues:

1. **Apply UX principles**: Use established best practices
2. **Use proven patterns**: Don't reinvent, use familiar interactions
3. **Maintain consistency**: Follow existing design system
4. **Consider accessibility**: Improvements should be inclusive
5. **Validate with principles**: Check improvement against heuristics

Load `references/anti-patterns.md` to avoid common UX mistakes.

**Example improvements:**

| Issue | UX Principle Applied | Improvement |
|-------|---------------------|-------------|
| No feedback after form submit | Visibility of system status | Add loading spinner + success message |
| Confusing error message "Error 422" | Help users recover from errors | "Email already registered. Try logging in or use a different email." |
| Too many form fields | Aesthetic and minimalist design | Progressive disclosure: show only required fields, hide optional behind "More options" |

### Step 7: Document Recommendations

To communicate findings and improvements:

1. **Use the template**: `assets/ux-evaluation-template.md`
2. **Summarize findings**: Overall UX score, key issues
3. **Provide evidence**: Screenshots, examples, severity ratings
4. **Recommend improvements**: Specific, actionable changes
5. **Prioritize**: What to fix first, second, third
6. **Include rationale**: Why these changes improve UX

**Effective recommendation format:**

```markdown
## Issue: No confirmation before deleting account
**Severity:** Critical
**Heuristic violated:** #5 Error prevention
**Impact:** Users accidentally delete accounts, cannot recover

**Current behavior:**
- Single "Delete Account" button in settings
- Immediately deletes account when clicked
- No warning about consequences
- No way to undo

**Recommended improvement:**
1. Add confirmation modal with:
   - Clear warning: "This will permanently delete your account and all data"
   - List of consequences (lose access, data deleted, subscriptions canceled)
   - Require typing account email to confirm
   - Separate "Cancel" and "Yes, delete account" buttons
2. Send confirmation email with 7-day grace period to undo
3. Add loading state during deletion process
4. Show success message with next steps after deletion

**UX principles applied:**
- Error prevention: Confirmation prevents accidents
- Help users recover from errors: Grace period allows undo
- Visibility of system status: Clear feedback during/after action
```

## Resources

This skill includes comprehensive reference materials and templates for UX design and evaluation:

### references/ux-principles.md
Core UX design principles including Nielsen's 10 Usability Heuristics (2025), Gestalt principles (proximity, similarity, closure, continuity), Fitts's Law, Hick's Law, cognitive load reduction, progressive disclosure, and accessibility foundations (WCAG 2.2).

**Load when:** Creating new UX, applying design principles, validating UX decisions, need foundational guidance, explaining UX choices.

### references/interaction-patterns.md
Common UI/UX interaction patterns for navigation (tab bars, sidebars, breadcrumbs), forms (inline validation, multi-step, autosave), feedback (loading states, errors, success), progressive disclosure (accordions, modals, drawers), search and filtering, empty states, and onboarding. Includes when to use / when not to use for each pattern.

**Load when:** Selecting interaction patterns, designing specific UI behaviors, ensuring consistency, looking for established solutions, mobile vs desktop patterns.

### references/ux-evaluation-framework.md
Comprehensive UX evaluation methodologies including heuristic evaluation process, cognitive walkthrough steps, UX scoring rubric, severity rating system (critical/major/minor), identifying pain points and friction, and documenting findings effectively.

**Load when:** Evaluating existing UX, conducting heuristic evaluation, performing cognitive walkthrough, rating severity, documenting UX issues.

### references/requirements-to-ux.md
Process for translating requirements into UX designs including requirement analysis techniques, user story mapping, creating user journey maps, information architecture methods (card sorting, tree testing), wireframing approaches (low-fi to hi-fi), and UX documentation standards.

**Load when:** Converting requirements to UX, creating user journeys, designing information architecture, mapping user flows, documenting UX designs.

### references/anti-patterns.md
Common UX mistakes to avoid including dark patterns, over-complexity, feature bloat, poor error handling, inconsistent interactions, accessibility violations, and mobile UX mistakes. Provides bad vs. good examples for each anti-pattern.

**Load when:** Reviewing UX designs, avoiding common mistakes, evaluating existing UX, learning what not to do, explaining UX problems.

### assets/ux-evaluation-template.md
Ready-to-use template for documenting UX evaluations. Includes sections for heuristic analysis, findings with severity ratings, issues by category, recommendations with rationale, and prioritization matrix.

**Use when:** Documenting UX evaluation results, presenting findings to stakeholders, creating evaluation reports, tracking issues.

### assets/ux-design-doc-template.md
Template for documenting UX design decisions. Includes sections for requirements summary, user personas, user journeys, information architecture, user flows, interaction patterns, wireframes/mockups, and design rationale.

**Use when:** Documenting new UX designs, communicating UX to developers, creating design specifications, recording UX decisions.

### assets/user-journey-template.md
Template for mapping user journeys. Includes columns for stages, touchpoints, user actions, emotions, pain points, and opportunities. Helps visualize end-to-end user experience.

**Use when:** Creating user journey maps, identifying touchpoints, finding pain points, spotting UX opportunities, understanding user emotions.

## Tips for Success

1. **Start with users, not features**: Understand user needs before designing solutions
2. **Use established patterns**: Don't reinvent interactions users already know
3. **Prioritize accessibility**: WCAG 2.2 AA is the foundation, not an afterthought
4. **Validate early and often**: Test UX assumptions with real users when possible
5. **Apply principles systematically**: Check against all 10 Nielsen heuristics
6. **Document decisions**: Future you (and others) will need to understand why
7. **Learn from anti-patterns**: Study common mistakes to avoid repeating them
8. **Consider mobile first**: Design for smallest screen, progressively enhance
9. **Reduce cognitive load**: Minimize what users need to remember
10. **Iterate based on feedback**: UX is never "done", continuously improve

## When to Load Reference Files

To optimize context usage, load reference files strategically:

- **Load ux-principles.md** when:
  - Creating new UX designs from scratch
  - Applying design principles to decisions
  - Validating UX against heuristics
  - Need foundational UX guidance
  - Explaining why certain UX choices were made

- **Load interaction-patterns.md** when:
  - Selecting patterns for specific interactions
  - Designing navigation, forms, or feedback
  - Ensuring pattern consistency
  - Need examples of proven solutions
  - Choosing between mobile and desktop patterns

- **Load ux-evaluation-framework.md** when:
  - Conducting heuristic evaluation
  - Performing cognitive walkthrough
  - Rating issue severity
  - Need evaluation methodology
  - Documenting UX findings

- **Load requirements-to-ux.md** when:
  - Translating requirements into UX
  - Creating user journey maps
  - Designing information architecture
  - Mapping detailed user flows
  - Need wireframing guidance

- **Load anti-patterns.md** when:
  - Reviewing existing UX for problems
  - Learning what to avoid
  - Evaluating UX quality
  - Need examples of bad vs. good UX
  - Explaining UX issues to stakeholders
