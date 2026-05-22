---
name: faion-ux-ui-designer
user-invocable: false
description: "UX/UI Designer role: Nielsen Norman 10 Heuristics, UX research methods, usability testing, persona development, journey mapping, wireframing, prototyping, design systems, accessibility. 32 methodologies."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*), Task, AskUserQuestion, TodoWrite
---

# UX Domain Skill

**Communication: User's language. Docs/code: English.**

## Purpose

Orchestrates UX (User Experience) research, design, and evaluation. This domain skill provides comprehensive UX methodology based on Nielsen Norman Group research and industry best practices.

## Philosophy

**"Design is not just what it looks like. Design is how it works."** — Steve Jobs

User experience is measured by how well users can achieve their goals, not by aesthetic appeal alone.

## 3-Layer Architecture

```
Layer 1: Domain Skills (this) - orchestrators
    |
    v call
Layer 2: Agents - executors
    |
    v use
Layer 3: Technical Skills - tools
```

## Agents Called

| Agent | Purpose | Methods Used |
|-------|---------|--------------|
| **faion-ux-researcher-agent** | User interviews, surveys, research synthesis | M-UX-011 to M-UX-022 |
| **faion-usability-agent** | Usability testing, heuristic evaluation | M-UX-001 to M-UX-010, M-UX-023 to M-UX-032 |

---

# Part 1: Nielsen Norman 10 Usability Heuristics

## Overview

Jakob Nielsen's 10 general principles for interaction design. They are called "heuristics" because they are broad rules of thumb, not specific usability guidelines.

---

## M-UX-001: Visibility of System Status

### Problem

Users feel lost when they don't know what's happening in the system.

### Heuristic

**The design should always keep users informed about what is going on, through appropriate feedback within a reasonable amount of time.**

### Framework

1. **Loading States**
   - Show progress indicators for operations > 1 second
   - Use skeleton screens for content loading
   - Display percentage for long operations

2. **Action Feedback**
   - Confirm successful actions (saved, sent, deleted)
   - Show errors immediately with clear messages
   - Indicate pending states (processing, waiting)

3. **Navigation Context**
   - Highlight current location in navigation
   - Use breadcrumbs for deep hierarchies
   - Show step indicators in multi-step flows

4. **State Indicators**
   - Online/offline status
   - Connection quality
   - Sync status

### Examples

| Good | Bad |
|------|-----|
| "Saving... Saved 5 seconds ago" | Silent save with no feedback |
| Progress bar: "Uploading 45%" | Spinner with no context |
| "Step 2 of 4: Payment Details" | No indication of progress |
| "You are here" marker on map | Map without user location |

### Checklist

- [ ] Every action has immediate visual feedback
- [ ] Loading states shown for operations > 1 second
- [ ] Current location is always visible in navigation
- [ ] System state changes are communicated clearly
- [ ] Error states are distinguishable from normal states

### Agent

**faion-usability-agent** - Heuristic Evaluation mode

---

## M-UX-002: Match Between System and Real World

### Problem

Users struggle when interfaces use unfamiliar terminology or concepts.

### Heuristic

**The design should speak the users' language, with words, phrases, and concepts familiar to the user, rather than internal jargon. Follow real-world conventions, making information appear in a natural and logical order.**

### Framework

1. **Language Audit**
   - Replace technical terms with user terms
   - Use verbs users would use (not system actions)
   - Match industry-specific vocabulary when appropriate

2. **Mental Models**
   - Organize information as users expect
   - Use familiar metaphors (folders, shopping cart)
   - Follow real-world object behaviors

3. **Logical Ordering**
   - Chronological for timelines
   - Alphabetical for lists
   - Priority-based for tasks
   - Geographic for locations

4. **Cultural Considerations**
   - Date formats (MM/DD vs DD/MM)
   - Number formats (1,000 vs 1.000)
   - Reading direction (LTR vs RTL)
   - Color meanings (red = danger/luck)

### Examples

| Technical | User-Friendly |
|-----------|---------------|
| "Execute query" | "Search" |
| "Terminate session" | "Log out" |
| "Invalid input" | "Please enter a valid email" |
| "Repository" | "Project" |
| "Instance" | "Copy" or "Server" |

### Checklist

- [ ] No technical jargon visible to end users
- [ ] Icons match real-world objects they represent
- [ ] Information order matches user expectations
- [ ] Dates, times, currencies match user locale
- [ ] Error messages use plain language

### Agent

**faion-usability-agent** - Content Review mode

---

## M-UX-003: User Control and Freedom

### Problem

Users often make mistakes or change their minds. They need a way out.

### Heuristic

**Users often perform actions by mistake. They need a clearly marked "emergency exit" to leave the unwanted action without having to go through an extended process.**

### Framework

1. **Undo/Redo**
   - Support undo for destructive actions
   - Provide redo capability
   - Show undo confirmation ("Deleted. Undo?")

2. **Cancel Operations**
   - Allow canceling long operations
   - Confirm before irreversible actions
   - Provide "Back" navigation

3. **Easy Exit**
   - Clear close buttons
   - Escape key support for modals
   - "Cancel" button always available

4. **Graceful Recovery**
   - Soft delete with recovery period
   - Draft auto-save
   - Session restoration

### Examples

| Good | Bad |
|------|-----|
| "Message deleted. Undo (10s)" | Permanent delete with no undo |
| "Cancel" button on every form | No way to exit form without saving |
| Escape key closes modal | Click outside to close (not discoverable) |
| "Discard changes?" confirmation | Silent loss of unsaved work |

### Checklist

- [ ] Undo available for destructive actions
- [ ] Cancel button on all forms and dialogs
- [ ] Escape key closes modals
- [ ] Confirmation before irreversible actions
- [ ] Auto-save for important content

### Agent

**faion-usability-agent** - Interaction Review mode

---

## M-UX-004: Consistency and Standards

### Problem

Users shouldn't wonder whether different words, situations, or actions mean the same thing.

### Heuristic

**Users should not have to wonder whether different words, situations, or actions mean the same thing. Follow platform and industry conventions.**

### Framework

1. **Internal Consistency**
   - Same action, same name everywhere
   - Same icon, same meaning
   - Same position for same function
   - Same color for same state

2. **External Consistency**
   - Follow platform conventions (iOS, Android, Web)
   - Use industry-standard terminology
   - Match competitor UX patterns

3. **Design System**
   - Components library
   - Color palette with meanings
   - Typography scale
   - Spacing system

4. **Interaction Patterns**
   - Consistent click/tap targets
   - Same gesture for same action
   - Predictable navigation

### Examples

| Inconsistent | Consistent |
|--------------|------------|
| "Save" / "Submit" / "Confirm" for same action | "Save" everywhere |
| Blue links on page A, green on page B | Blue links everywhere |
| Menu on left on some pages, right on others | Menu always in same position |
| Different button sizes for same importance | Button hierarchy system |

### Checklist

- [ ] Design system documented and followed
- [ ] Same terminology for same concepts
- [ ] Same colors for same meanings
- [ ] Platform conventions respected
- [ ] Components reused, not recreated

### Agent

**faion-usability-agent** - Design Consistency Audit mode

---

## M-UX-005: Error Prevention

### Problem

Errors frustrate users and cost businesses money. Prevention is better than recovery.

### Heuristic

**Good error messages are important, but the best designs carefully prevent problems from occurring in the first place. Either eliminate error-prone conditions, or check for them and present users with a confirmation option before they commit to the action.**

### Framework

1. **Eliminate Error-Prone Conditions**
   - Use dropdowns instead of text input for known values
   - Disable buttons until valid input
   - Use date pickers instead of text dates
   - Auto-format inputs (phone, credit card)

2. **Constrain Input**
   - Set min/max values
   - Limit character count
   - Restrict file types
   - Validate in real-time

3. **Confirm Risky Actions**
   - "Are you sure you want to delete?"
   - Preview before publish
   - Review before payment

4. **Provide Defaults**
   - Smart defaults based on context
   - Remember user preferences
   - Suggest common values

### Examples

| Error-Prone | Error-Proof |
|-------------|-------------|
| Text input for country | Dropdown with countries |
| "Enter date" text field | Date picker calendar |
| Free-form phone input | Masked input: (___) ___-____ |
| Immediate delete | "Delete" -> Confirm -> Deleted |

### Checklist

- [ ] Dropdowns used for known value sets
- [ ] Date/time pickers instead of text input
- [ ] Real-time validation with helpful messages
- [ ] Confirmation for destructive actions
- [ ] Smart defaults reduce input needed

### Agent

**faion-usability-agent** - Form Review mode

---

## M-UX-006: Recognition Rather Than Recall

### Problem

Users should not have to remember information from one part of the interface to another.

### Heuristic

**Minimize the user's memory load by making elements, actions, and options visible. The user should not have to remember information from one part of the dialogue to another. Instructions for use of the system should be visible or easily retrievable whenever appropriate.**

### Framework

1. **Make Options Visible**
   - Show all available actions
   - Use menus instead of command lines
   - Display recent items
   - Show shortcuts inline

2. **Reduce Memory Load**
   - Display context (current file name, user name)
   - Show breadcrumbs for navigation history
   - Preview selections before confirming

3. **Provide Help In-Context**
   - Tooltips on hover
   - Inline help text
   - Examples in placeholders
   - Progressive disclosure

4. **Remember User Context**
   - Recently opened files
   - Search history
   - Form field suggestions
   - Last used settings

### Examples

| Requires Recall | Supports Recognition |
|-----------------|----------------------|
| "Enter command" | Menu with all commands |
| "Enter product code" | Searchable product list |
| "Confirm password" (hidden) | Show password toggle |
| Empty search box | Recent searches dropdown |

### Checklist

- [ ] All available actions are visible or easily discoverable
- [ ] Recent items and history easily accessible
- [ ] Tooltips explain unclear elements
- [ ] Form fields have helpful placeholders
- [ ] Search suggestions based on history

### Agent

**faion-usability-agent** - Cognitive Load Review mode

---

## M-UX-007: Flexibility and Efficiency of Use

### Problem

Different users have different needs. Novices need guidance, experts need speed.

### Heuristic

**Shortcuts - hidden from novice users - can speed up the interaction for the expert user such that the design can cater to both inexperienced and experienced users. Allow users to tailor frequent actions.**

### Framework

1. **Keyboard Shortcuts**
   - Common shortcuts (Ctrl+S, Ctrl+Z)
   - Custom shortcut assignment
   - Shortcut cheat sheet

2. **Accelerators**
   - Type-ahead search
   - Quick actions
   - Bulk operations
   - Drag and drop

3. **Customization**
   - Configurable dashboard
   - Custom workflows
   - Saved filters/views
   - Personalized defaults

4. **Progressive Complexity**
   - Simple mode by default
   - Advanced options available
   - Expert mode toggle

### Examples

| Novice Path | Expert Path |
|-------------|-------------|
| Click File > Save | Ctrl+S |
| Navigate through menu | Command palette (Cmd+K) |
| Single item edit | Bulk edit mode |
| Wizard-based setup | Import configuration |

### Checklist

- [ ] Keyboard shortcuts for common actions
- [ ] Shortcuts documented and discoverable
- [ ] Bulk operations for repetitive tasks
- [ ] Search/filter can be saved
- [ ] Power user features don't complicate novice experience

### Agent

**faion-usability-agent** - Efficiency Review mode

---

## M-UX-008: Aesthetic and Minimalist Design

### Problem

Every extra unit of information competes with relevant information and diminishes visibility.

### Heuristic

**Interfaces should not contain information which is irrelevant or rarely needed. Every extra unit of information in an interface competes with the relevant units of information and diminishes their relative visibility.**

### Framework

1. **Content Hierarchy**
   - Most important information first
   - Progressive disclosure for details
   - Clear visual hierarchy

2. **Remove Clutter**
   - Eliminate unnecessary elements
   - Reduce decorative graphics
   - Simplify navigation

3. **White Space**
   - Generous padding
   - Group related items
   - Separate unrelated content

4. **Focus on Essentials**
   - One primary action per screen
   - Hide advanced options
   - Default to simple view

### Examples

| Cluttered | Minimalist |
|-----------|------------|
| 10 buttons on toolbar | 3 primary, "More" for rest |
| Full feature list on home | Key benefits, link to details |
| All settings visible | Organized in categories |
| Dense text walls | Scannable bullet points |

### Checklist

- [ ] Primary action clearly visible
- [ ] Secondary actions de-emphasized
- [ ] Adequate white space
- [ ] Content scannable, not wall of text
- [ ] Decorative elements serve a purpose

### Agent

**faion-usability-agent** - Visual Design Review mode

---

## M-UX-009: Help Users Recognize, Diagnose, and Recover from Errors

### Problem

Errors will happen. Good error messages help users fix problems quickly.

### Heuristic

**Error messages should be expressed in plain language (no error codes), precisely indicate the problem, and constructively suggest a solution.**

### Framework

1. **Error Message Structure**
   - What happened (plain language)
   - Why it happened (if helpful)
   - How to fix it (actionable)
   - Link to help (if complex)

2. **Visual Error States**
   - Red border on invalid fields
   - Error icon with message
   - Inline error placement
   - Clear error vs warning distinction

3. **Error Prevention vs Recovery**
   - Prevent before it happens (validation)
   - Recover quickly if it happens (suggestions)
   - Learn from errors (analytics)

4. **Error Types**
   - Validation errors (user input)
   - System errors (server issues)
   - Network errors (connectivity)
   - Permission errors (access denied)

### Examples

| Bad Error | Good Error |
|-----------|------------|
| "Error 500" | "Something went wrong. Please try again or contact support." |
| "Invalid input" | "Email address is not valid. Example: name@example.com" |
| "Operation failed" | "Could not save. Check your connection and try again." |
| "Unauthorized" | "You don't have permission. Request access from admin@company.com" |

### Error Message Template

```
[What] Your password is too short.
[Why] Passwords must be at least 8 characters for security.
[Fix] Add more characters to your password.
```

### Checklist

- [ ] Error messages in plain language
- [ ] Specific problem identified
- [ ] Actionable solution provided
- [ ] Errors placed near the problem
- [ ] Recovery path is clear

### Agent

**faion-usability-agent** - Error Handling Review mode

---

## M-UX-010: Help and Documentation

### Problem

Even the best designs sometimes need explanation. Help should be accessible when needed.

### Heuristic

**It is better if the system can be used without documentation, but it may be necessary to provide help and documentation. Any such information should be easy to search, focused on the user's task, list concrete steps to be carried out, and not be too large.**

### Framework

1. **Types of Help**
   - Onboarding tours (first-time users)
   - Tooltips (contextual help)
   - Help center (searchable docs)
   - FAQs (common questions)
   - Live chat/support (complex issues)

2. **Help Content Principles**
   - Task-oriented (how to achieve goals)
   - Searchable (full-text search)
   - Scannable (short paragraphs, lists)
   - Current (updated with product)

3. **Contextual Help**
   - "?" icons next to complex fields
   - Empty state guidance
   - First-use walkthroughs
   - Inline documentation

4. **Progressive Help**
   - Start with basics
   - Link to advanced topics
   - Offer video alternatives
   - Provide examples

### Examples

| Poor Help | Good Help |
|-----------|-----------|
| PDF manual download | Searchable help center |
| Generic FAQ | Context-sensitive help |
| "See documentation" | Link to specific article |
| Text-only instructions | Step-by-step with screenshots |

### Checklist

- [ ] Help is searchable
- [ ] Help is contextual (relates to current task)
- [ ] Instructions are step-by-step
- [ ] Screenshots or videos for complex tasks
- [ ] Help content is up-to-date

### Agent

**faion-usability-agent** - Documentation Review mode

---

# Part 2: UX Research Methods

## Overview

Research methods for understanding user needs, behaviors, and experiences. Choosing the right method depends on research goals, timeline, and resources.

---

## M-UX-011: User Interviews

### Problem

You need deep understanding of user motivations, pain points, and workflows.

### When to Use

- Early discovery phase
- Understanding "why" behind behaviors
- Exploring new problem spaces
- Validating personas

### Framework

1. **Preparation**
   - Define research questions (not interview questions)
   - Recruit 5-8 participants per segment
   - Prepare discussion guide
   - Set up recording (with consent)

2. **Interview Structure**
   - Introduction (5 min): Build rapport, explain purpose
   - Warm-up (5 min): Easy background questions
   - Main body (30-40 min): Core research questions
   - Wrap-up (5 min): Summary, additional thoughts

3. **Question Types**
   - Open-ended: "Tell me about..."
   - Follow-up: "Why do you think that is?"
   - Behavioral: "Walk me through the last time..."
   - Hypothetical: "What if you could..."

4. **Analysis**
   - Transcribe or review recordings
   - Identify themes and patterns
   - Create affinity diagram
   - Document quotes

### Interview Guide Template

```markdown
## Research Goal
[What we want to learn]

## Participant Criteria
[Who to recruit]

## Discussion Guide

### Introduction (5 min)
- Introduce yourself
- Explain purpose (learning, not testing)
- Ask permission to record
- "No right or wrong answers"

### Background (5 min)
- Role and responsibilities
- Experience with [topic]

### Core Questions (30 min)
1. [Question 1]
   - Follow-up: [Probe]
2. [Question 2]
   - Follow-up: [Probe]

### Wrap-up (5 min)
- Anything else to share?
- Any questions for us?
```

### Checklist

- [ ] Research goals defined before interviews
- [ ] Discussion guide prepared and reviewed
- [ ] Participants recruited from target audience
- [ ] Recording consent obtained
- [ ] Notes taken during interview
- [ ] Analysis completed within 48 hours

### Agent

**faion-ux-researcher-agent** - Interview mode

---

## M-UX-012: Contextual Inquiry

### Problem

You need to observe real behavior in natural environment, not just hear about it.

### When to Use

- Understanding actual workflows
- Discovering workarounds
- Learning environmental constraints
- Early design discovery

### Framework

1. **Master-Apprentice Model**
   - User is the expert (master)
   - Researcher is learning (apprentice)
   - Observe, then ask questions

2. **Four Principles**
   - **Context:** Observe in real environment
   - **Partnership:** Collaborate, don't just watch
   - **Interpretation:** Discuss observations in the moment
   - **Focus:** Stay on research topic

3. **Session Structure**
   - Introduction (10 min): Explain approach
   - Observation (60-90 min): Watch and ask
   - Summary (15 min): Review understanding

4. **Documentation**
   - Photos (with permission)
   - Sketches of workspace
   - Artifact collection
   - Audio/video recording

### Checklist

- [ ] Environment access arranged
- [ ] Participant comfortable with observation
- [ ] Research focus defined
- [ ] Permission for photos/recording
- [ ] Artifacts collected
- [ ] Same-day notes completed

### Agent

**faion-ux-researcher-agent** - Contextual Inquiry mode

---

## M-UX-013: Surveys and Questionnaires

### Problem

You need quantitative data from large number of users.

### When to Use

- Measuring satisfaction (NPS, CSAT)
- Prioritizing features
- Benchmarking over time
- Reaching large audiences

### Framework

1. **Survey Design**
   - Define objectives first
   - Keep surveys short (5-10 min)
   - Use clear, unbiased language
   - Include progress indicator

2. **Question Types**
   - **Closed:** Multiple choice, rating scales
   - **Open:** Free text (use sparingly)
   - **Scale:** Likert (1-5 or 1-7)
   - **Ranking:** Order preferences

3. **Response Scales**
   | Scale | Use For |
   |-------|---------|
   | 1-5 Likert | Agreement, satisfaction |
   | 1-10 NPS | Likelihood to recommend |
   | Semantic differential | Opposing adjectives |
   | Frequency | How often |

4. **Analysis**
   - Quantitative: Means, distributions, correlations
   - Qualitative: Theme coding for open responses
   - Segmentation: Compare groups

### Survey Template

```markdown
## Survey Objective
[What decision will this inform?]

## Target Audience
[Who should respond?]

## Questions

### Screening
1. [Role/criteria check]

### Core Questions
2. On a scale of 1-5, how satisfied are you with [feature]?
   - [ ] 1 - Very dissatisfied
   - [ ] 2 - Dissatisfied
   - [ ] 3 - Neutral
   - [ ] 4 - Satisfied
   - [ ] 5 - Very satisfied

3. What is your primary challenge with [topic]?
   - [ ] Option A
   - [ ] Option B
   - [ ] Other: ____

### Open-Ended
4. What would make [product] more useful for you?
   [Text field]

### Demographics
5. Role: [Dropdown]
6. Company size: [Dropdown]
```

### Checklist

- [ ] Objectives clearly defined
- [ ] Survey length under 10 minutes
- [ ] Questions unbiased and clear
- [ ] Scale types appropriate
- [ ] Pilot tested before launch
- [ ] Response rate acceptable (>20%)

### Agent

**faion-ux-researcher-agent** - Survey mode

---

## M-UX-014: Usability Testing

### Problem

You need to validate that users can complete tasks with your design.

### When to Use

- Validating prototypes
- Finding usability issues
- Comparing design options
- Measuring task success

### Framework

1. **Test Types**
   | Type | When | Pros | Cons |
   |------|------|------|------|
   | Moderated | Complex flows | Deep insights | Time-intensive |
   | Unmoderated | Simple tasks | Scale, speed | Less context |
   | Remote | Access users anywhere | Convenience | Tech issues |
   | In-person | Observe body language | Rich data | Logistics |

2. **Session Structure**
   - Pre-test interview (5 min)
   - Task scenarios (20-40 min)
   - Post-test questions (10 min)
   - SUS questionnaire (5 min)

3. **Task Writing**
   - Scenario-based (not "click here")
   - Realistic goals
   - No hints about solution
   - Clear success criteria

4. **Metrics**
   - Task success rate
   - Time on task
   - Error rate
   - SUS score
   - Task difficulty rating

### Usability Test Script

```markdown
## Introduction
"Thank you for participating. We're testing [product], not you.
There are no right or wrong answers. Please think aloud."

## Warm-up
"First, tell me a bit about yourself and your role."

## Tasks

### Task 1: [Goal]
Scenario: "Imagine you need to [realistic context].
Please show me how you would [specific goal]."

Success criteria:
- [ ] Completed task
- [ ] Found [specific element]
- [ ] Time under [X] minutes

### Task 2: [Goal]
[Same format]

## Post-Test
"Overall, how would you describe this experience?"
"What was most confusing?"
"What did you like?"

## SUS Questionnaire
[10-item System Usability Scale]
```

### Checklist

- [ ] Test objectives defined
- [ ] 5+ participants per design
- [ ] Realistic task scenarios
- [ ] Think-aloud protocol used
- [ ] Metrics captured
- [ ] Findings prioritized by severity

### Agent

**faion-usability-agent** - Usability Testing mode

---

## M-UX-015: A/B Testing

### Problem

You need to make data-driven decisions between design alternatives.

### When to Use

- Optimizing conversions
- Validating design hypotheses
- Iterating on existing features
- Measuring real user behavior

### Framework

1. **Test Design**
   - One variable per test
   - Control (A) vs Variant (B)
   - Define success metric
   - Calculate sample size

2. **Statistical Requirements**
   - Confidence level: 95%
   - Statistical power: 80%
   - Minimum detectable effect: 5-10%
   - Sample size calculator

3. **Implementation**
   - Random assignment
   - Even split (50/50)
   - Consistent experience per user
   - Run for full business cycle

4. **Analysis**
   - Statistical significance
   - Practical significance
   - Segment analysis
   - Secondary metrics

### A/B Test Plan Template

```markdown
## Hypothesis
If we [change], then [metric] will [improve/increase] by [amount]
because [reason].

## Test Design
- Control (A): [Current design]
- Variant (B): [New design]
- Variable: [Single change]

## Metrics
- Primary: [Conversion rate, clicks, etc.]
- Secondary: [Engagement, time on page]
- Guardrail: [Metrics that should not decrease]

## Sample Size
- MDE: [5%]
- Confidence: [95%]
- Power: [80%]
- Required sample: [X users per variant]

## Duration
- Estimated: [X days/weeks]
- Minimum: [1 full business cycle]

## Segmentation
- [ ] Device type
- [ ] New vs returning
- [ ] User segment
```

### Checklist

- [ ] Single variable isolated
- [ ] Sample size calculated
- [ ] Success metric defined
- [ ] Test ran for full cycle
- [ ] Results statistically significant
- [ ] Decision documented

### Agent

**faion-ux-researcher-agent** - A/B Testing mode

---

## M-UX-016: Card Sorting

### Problem

You need to understand how users categorize and label information.

### When to Use

- Designing information architecture
- Creating navigation
- Labeling categories
- Understanding mental models

### Framework

1. **Types**
   | Type | Description | Use |
   |------|-------------|-----|
   | **Open** | Users create categories | New IA |
   | **Closed** | Users sort into predefined categories | Validate IA |
   | **Hybrid** | Predefined + can create new | Iterate IA |

2. **Setup**
   - 30-60 cards (content items)
   - 15-30 participants
   - Physical or digital (OptimalSort, Maze)
   - Clear instructions

3. **Analysis**
   - Similarity matrix
   - Dendrogram (clustering)
   - Category agreement
   - Labeling patterns

### Card Sort Plan

```markdown
## Objective
[What IA decision will this inform?]

## Type
- [ ] Open (users create groups)
- [ ] Closed (predefined groups)
- [ ] Hybrid

## Cards
1. [Content item 1]
2. [Content item 2]
...
[30-60 items]

## Categories (for closed/hybrid)
- [Category A]
- [Category B]
...

## Participants
- Number: [15-30]
- Criteria: [Target users]

## Analysis Plan
- Similarity matrix threshold: [70%]
- Report format: [Dendrogram + recommendations]
```

### Checklist

- [ ] Card content matches real labels
- [ ] 30-60 cards prepared
- [ ] 15+ participants completed
- [ ] Similarity matrix analyzed
- [ ] Recommendations documented

### Agent

**faion-ux-researcher-agent** - Card Sorting mode

---

## M-UX-017: Tree Testing

### Problem

You need to validate that users can find content in your navigation structure.

### When to Use

- Validating information architecture
- Testing navigation labels
- Before implementing navigation
- After card sorting

### Framework

1. **Setup**
   - Text-only navigation tree
   - No visual design
   - 8-10 tasks
   - 50+ participants

2. **Task Design**
   - Goal-based scenarios
   - No hints in wording
   - Single correct answer
   - Varying difficulty

3. **Metrics**
   - Success rate (found correct location)
   - Directness (no backtracking)
   - Time to complete
   - First click accuracy

4. **Analysis**
   - Task-level success
   - Path analysis
   - Problem categories identification
   - Recommendations

### Tree Test Plan

```markdown
## Navigation Tree
```
Home
|-- Products
|   |-- Category A
|   |-- Category B
|-- Support
|   |-- FAQ
|   |-- Contact
|-- About
```

## Tasks

### Task 1
Scenario: "You want to [goal]."
Correct answer: Home > Products > Category A

### Task 2
[Continue for 8-10 tasks]

## Success Criteria
- Overall success: >80%
- Directness: >60%
```

### Checklist

- [ ] Navigation tree matches proposed IA
- [ ] Tasks cover key user goals
- [ ] 50+ participants completed
- [ ] Problem areas identified
- [ ] Improvements recommended

### Agent

**faion-ux-researcher-agent** - Tree Testing mode

---

## M-UX-018: Journey Mapping

### Problem

You need to understand the complete user experience across touchpoints and time.

### When to Use

- Understanding end-to-end experience
- Identifying pain points
- Aligning teams on user perspective
- Finding improvement opportunities

### Framework

1. **Journey Map Components**
   - **Stages:** Major phases of experience
   - **Actions:** What user does
   - **Thoughts:** What user thinks
   - **Emotions:** How user feels
   - **Touchpoints:** Where interaction happens
   - **Pain Points:** Friction and frustration
   - **Opportunities:** Improvement ideas

2. **Process**
   - Define scope and persona
   - Gather research data
   - Map current state
   - Identify pain points
   - Propose future state

3. **Data Sources**
   - User interviews
   - Analytics
   - Support tickets
   - Surveys
   - Usability tests

### Journey Map Template

```markdown
## Journey: [Name]
## Persona: [User type]
## Scenario: [Specific goal]

| Stage | Awareness | Consideration | Decision | Use | Support |
|-------|-----------|---------------|----------|-----|---------|
| **Actions** | Searches online | Compares options | Signs up | Uses feature | Contacts support |
| **Thoughts** | "How do I solve this?" | "Which is best?" | "Is this worth it?" | "How do I do X?" | "Why isn't this working?" |
| **Emotions** | Curious | Overwhelmed | Hopeful | Frustrated | Anxious |
| **Touchpoints** | Google, social | Website, reviews | Pricing page | App | Support chat |
| **Pain Points** | Hard to find info | Too many options | Pricing unclear | Feature hard to find | Long wait time |
| **Opportunities** | SEO, content | Comparison tool | Clear pricing | Onboarding | Self-service help |
```

### Checklist

- [ ] Persona defined
- [ ] Journey scope bounded
- [ ] Based on real user data
- [ ] Pain points identified
- [ ] Opportunities prioritized
- [ ] Stakeholders aligned

### Agent

**faion-ux-researcher-agent** - Journey Mapping mode

---

## M-UX-019: Empathy Mapping

### Problem

You need to build shared understanding of user perspective within your team.

### When to Use

- Synthesizing research findings
- Workshop activity
- Building empathy
- Preparing for design

### Framework

1. **Quadrants**
   - **Says:** Direct quotes from research
   - **Thinks:** Inferred thoughts, beliefs
   - **Does:** Observable behaviors, actions
   - **Feels:** Emotions, frustrations, delights

2. **Extended Model**
   - **Goals:** What user wants to achieve
   - **Pain Points:** What frustrates them
   - **Gains:** What would delight them

3. **Process**
   - Gather research artifacts
   - Create individual maps
   - Synthesize into composite
   - Validate with team

### Empathy Map Template

```markdown
## User: [Name/Persona]
## Context: [Situation being mapped]

### SAYS
- "[Direct quote 1]"
- "[Direct quote 2]"

### THINKS
- Believes [belief]
- Wonders about [question]
- Worries that [concern]

### DOES
- [Observable behavior 1]
- [Observable behavior 2]
- Workaround: [coping mechanism]

### FEELS
- Frustrated when [trigger]
- Delighted by [positive]
- Anxious about [concern]

### GOALS
- Primary: [Main goal]
- Secondary: [Supporting goals]

### PAIN POINTS
1. [Major frustration]
2. [Minor frustration]

### GAINS
1. [What would delight]
2. [Unmet need]
```

### Checklist

- [ ] Based on real research
- [ ] All quadrants filled
- [ ] Team participated
- [ ] Insights actionable
- [ ] Documented and shared

### Agent

**faion-ux-researcher-agent** - Empathy Mapping mode

---

## M-UX-020: Persona Development

### Problem

You need a shared reference for who you're designing for.

### When to Use

- Starting new project
- Aligning team on target users
- Making design decisions
- Prioritizing features

### Framework

1. **Persona Components**
   - Name and photo (realistic)
   - Demographics
   - Goals and motivations
   - Frustrations and pain points
   - Behaviors and habits
   - Technology comfort
   - Quote that captures essence

2. **Types**
   | Type | Description | Use |
   |------|-------------|-----|
   | **Proto-persona** | Assumption-based | Before research |
   | **Research-based** | Data-driven | After research |
   | **Composite** | Combined from multiple users | When patterns emerge |

3. **Process**
   - Conduct user research
   - Identify patterns and segments
   - Create 3-5 distinct personas
   - Validate with stakeholders
   - Keep personas alive (reference often)

### Persona Template

```markdown
## [Persona Name]

### Photo
[Realistic stock photo representing demographic]

### Quote
"[Characteristic quote that captures perspective]"

### Demographics
- Age: [Range]
- Role: [Job title]
- Location: [Geography]
- Tech comfort: [Low/Medium/High]

### Bio
[2-3 sentences about background and context]

### Goals
1. [Primary goal]
2. [Secondary goal]
3. [Tertiary goal]

### Frustrations
1. [Major pain point]
2. [Minor pain point]

### Behaviors
- [Relevant behavior 1]
- [Relevant behavior 2]

### Tools Used
- [Tool/platform 1]
- [Tool/platform 2]

### A Day in the Life
[Brief narrative of typical day]
```

### Checklist

- [ ] Based on research data
- [ ] 3-5 distinct personas
- [ ] Goals clearly defined
- [ ] Frustrations specific
- [ ] Team has access
- [ ] Referenced in decisions

### Agent

**faion-ux-researcher-agent** - Persona Development mode

---

## M-UX-021: Diary Studies

### Problem

You need to understand behavior over time in natural context.

### When to Use

- Long-term behavior patterns
- Infrequent activities
- Emotional journeys
- Context-dependent behavior

### Framework

1. **Setup**
   - Duration: 1-4 weeks
   - Participants: 10-15
   - Entry frequency: Daily or per event
   - Platform: App, email, or physical diary

2. **Entry Design**
   - Short entries (2-5 minutes)
   - Mix of structured and open
   - Photo/video capture
   - Emotion capture

3. **Engagement**
   - Daily reminders
   - Mid-study check-ins
   - Incentives for completion
   - Support channel

4. **Analysis**
   - Timeline analysis
   - Pattern identification
   - Cross-participant themes
   - Quote extraction

### Diary Study Plan

```markdown
## Study Objective
[What long-term behavior are we studying?]

## Duration
[X weeks]

## Participants
- Number: [10-15]
- Criteria: [Target users]
- Compensation: [Incentive]

## Entry Prompt

### Daily Entry
1. What [activity] did you do today?
2. On a scale of 1-5, how was your experience?
3. What was most challenging?
4. Photo: [If relevant, capture image]

### Event-Triggered Entry
1. What just happened?
2. What were you trying to do?
3. How did you feel?
```

### Checklist

- [ ] Duration appropriate for behavior
- [ ] Entry prompts tested
- [ ] Reminder system in place
- [ ] Mid-study engagement planned
- [ ] Analysis framework ready
- [ ] Participant dropout managed

### Agent

**faion-ux-researcher-agent** - Diary Study mode

---

## M-UX-022: Competitive Analysis

### Problem

You need to understand the competitive landscape and identify opportunities.

### When to Use

- New product planning
- Feature prioritization
- Positioning strategy
- UX benchmarking

### Framework

1. **Competitor Categories**
   - **Direct:** Same product, same market
   - **Indirect:** Different product, same need
   - **Future:** Emerging competitors

2. **Analysis Dimensions**
   - Features and capabilities
   - User experience
   - Pricing and business model
   - Strengths and weaknesses
   - Market positioning

3. **Methods**
   - Product teardown
   - User reviews analysis
   - Heuristic evaluation
   - Feature matrix
   - SWOT analysis

### Competitive Analysis Template

```markdown
## Product: [Your product]
## Market: [Market segment]

## Competitors

### [Competitor A]
- Website: [URL]
- Pricing: [Model]
- Target: [User segment]

#### Strengths
- [Strength 1]
- [Strength 2]

#### Weaknesses
- [Weakness 1]
- [Weakness 2]

#### UX Notes
- [Notable UX pattern]
- [Pain point observed]

### [Competitor B]
[Same format]

## Feature Matrix

| Feature | Us | Comp A | Comp B |
|---------|------|--------|--------|
| Feature 1 | Yes | Yes | No |
| Feature 2 | No | Yes | Yes |

## Opportunities
1. [Gap in market]
2. [Competitor weakness to exploit]

## Threats
1. [Competitor advantage]
2. [Market trend]
```

### Checklist

- [ ] Direct and indirect competitors identified
- [ ] Feature comparison complete
- [ ] UX evaluated systematically
- [ ] Opportunities identified
- [ ] Threats documented
- [ ] Regularly updated

### Agent

**faion-ux-researcher-agent** - Competitive Analysis mode

---

# Part 3: UX Design Methods

## Overview

Methods for translating research into design solutions.

---

## M-UX-023: Information Architecture

### Problem

You need to organize content so users can find what they need.

### Framework

1. **IA Components**
   - **Organization schemes:** How content is categorized
   - **Labeling systems:** How content is named
   - **Navigation systems:** How users move through content
   - **Search systems:** How users find specific content

2. **Organization Schemes**
   | Scheme | Example | Use |
   |--------|---------|-----|
   | Alphabetical | A-Z directory | Known-item search |
   | Chronological | Blog posts | Time-based content |
   | Geographical | Store locations | Location-based |
   | Topic | Product categories | Browsing |
   | Audience | For developers/designers | Role-based |
   | Task | What you can do | Action-oriented |

3. **Process**
   - Content audit
   - Card sorting
   - Create sitemap
   - Tree testing
   - Iterate

### Sitemap Template

```markdown
## [Product Name] Sitemap

### Level 1: Primary Navigation
1. Home
2. Products
3. Resources
4. Pricing
5. About

### Level 2: Products
2.1. Category A
2.2. Category B
2.3. All Products

### Level 3: Category A
2.1.1. Product 1
2.1.2. Product 2
```

### Checklist

- [ ] Content inventory complete
- [ ] Organization scheme chosen
- [ ] Labels user-tested
- [ ] Navigation validated (tree test)
- [ ] Search requirements defined

### Agent

**faion-usability-agent** - Information Architecture mode

---

## M-UX-024: Wireframing

### Problem

You need to explore layout and structure before visual design.

### Framework

1. **Fidelity Levels**
   | Level | Detail | Tool | Purpose |
   |-------|--------|------|---------|
   | Low | Boxes, lines | Paper, Whimsical | Explore ideas |
   | Medium | Real content, basic layout | Balsamiq, Figma | Validate structure |
   | High | Detailed, interactive | Figma, Sketch | Test interactions |

2. **Wireframe Elements**
   - Content blocks (text, images)
   - Navigation
   - Forms and inputs
   - Calls to action
   - Annotations

3. **Best Practices**
   - Use real content (no lorem ipsum)
   - Focus on hierarchy, not aesthetics
   - Include annotations explaining choices
   - Create multiple variations
   - Test with users before high-fidelity

### Checklist

- [ ] Key screens identified
- [ ] Real content used
- [ ] Hierarchy clear
- [ ] Annotations included
- [ ] Multiple options explored
- [ ] Stakeholder review complete

### Agent

**faion-usability-agent** - Wireframing Review mode

---

## M-UX-025: Prototyping

### Problem

You need to test interactions before building.

### Framework

1. **Prototype Types**
   | Type | Tool | Use |
   |------|------|-----|
| Paper | Sketches | Very early exploration |
   | Clickable | Figma, InVision | Flow validation |
   | Interactive | Figma, Framer | Micro-interactions |
   | Coded | HTML/CSS | Developer handoff |

2. **Prototyping Principles**
   - Right fidelity for the question
   - Realistic enough to test
   - Fast to iterate
   - Disposable

3. **Testing Prototypes**
   - Define what to learn
   - Create task scenarios
   - Run usability tests
   - Iterate based on findings

### Checklist

- [ ] Fidelity matches research goals
- [ ] Key flows prototyped
- [ ] Realistic interactions
- [ ] Tested with users
- [ ] Findings documented

### Agent

**faion-usability-agent** - Prototype Review mode

---

## M-UX-026: Design Systems

### Problem

You need consistency and efficiency across a product.

### Framework

1. **Design System Components**
   - **Foundations:** Color, typography, spacing, icons
   - **Components:** Buttons, inputs, cards, modals
   - **Patterns:** Forms, navigation, data display
   - **Guidelines:** Usage rules, accessibility, voice

2. **Documentation**
   - Component specifications
   - Do's and don'ts
   - Code snippets
   - Live examples

3. **Maintenance**
   - Version control
   - Contribution process
   - Deprecation policy
   - Governance model

### Design System Structure

```markdown
## [Product] Design System

### Foundations
- Colors: Brand, UI, Semantic
- Typography: Scale, Weights, Usage
- Spacing: 4px base unit scale
- Icons: Library, Usage guidelines

### Components
- Button: Primary, Secondary, Destructive
- Input: Text, Number, Select, Checkbox
- Card: Default, Interactive, Featured
- Modal: Alert, Confirmation, Form

### Patterns
- Form Layout
- Navigation
- Data Table
- Empty States
- Loading States
```

### Checklist

- [ ] Foundations defined
- [ ] Core components documented
- [ ] Accessibility built in
- [ ] Code implementation aligned
- [ ] Governance established

### Agent

**faion-usability-agent** - Design System Review mode

---

## M-UX-027: Accessibility Design

### Problem

You need to design for users of all abilities.

### Framework

1. **WCAG Principles (POUR)**
   - **Perceivable:** Content available to senses
   - **Operable:** Interface can be used
   - **Understandable:** Content and UI clear
   - **Robust:** Works with assistive tech

2. **Common Requirements**
   | Category | Requirement |
   |----------|-------------|
   | Vision | Color contrast 4.5:1, alt text, resizable text |
   | Hearing | Captions, transcripts |
   | Motor | Keyboard navigation, large targets |
   | Cognitive | Simple language, consistent navigation |

3. **Design Checklist**
   - [ ] Color not only indicator
   - [ ] Focus states visible
   - [ ] Form labels associated
   - [ ] Error messages descriptive
   - [ ] Skip navigation available
   - [ ] Heading hierarchy correct

### Accessibility Audit Template

```markdown
## Page: [URL]

### Perceivable
- [ ] Images have alt text
- [ ] Color contrast passes (4.5:1)
- [ ] Text resizable to 200%

### Operable
- [ ] All interactive elements keyboard accessible
- [ ] Focus order logical
- [ ] No keyboard traps
- [ ] Skip links available

### Understandable
- [ ] Language declared
- [ ] Form inputs labeled
- [ ] Error messages clear

### Robust
- [ ] Valid HTML
- [ ] ARIA used correctly
- [ ] Works with screen readers
```

### Checklist

- [ ] WCAG 2.1 AA compliance targeted
- [ ] Automated testing run
- [ ] Manual testing completed
- [ ] Screen reader tested
- [ ] Keyboard navigation verified

### Agent

**faion-usability-agent** - Accessibility Audit mode

---

## M-UX-028: Mobile UX Design

### Problem

You need to design for touch interfaces and small screens.

### Framework

1. **Mobile-First Principles**
   - Design for smallest screen first
   - Prioritize content ruthlessly
   - Optimize for touch
   - Consider context

2. **Touch Targets**
   - Minimum size: 44x44px (iOS), 48x48dp (Android)
   - Adequate spacing between targets
   - Primary actions in thumb zone

3. **Mobile Patterns**
   | Pattern | Use |
   |---------|-----|
   | Bottom navigation | 3-5 primary destinations |
   | Pull to refresh | Content updates |
   | Swipe actions | Quick operations |
   | Floating action button | Primary action |

4. **Performance**
   - Optimize images
   - Minimize JavaScript
   - Lazy load content
   - Offline support

### Mobile UX Checklist

- [ ] Touch targets 44px minimum
- [ ] Content prioritized for small screen
- [ ] Forms optimized (input types, autofill)
- [ ] Loading states shown
- [ ] Works offline (critical features)
- [ ] Tested on real devices

### Agent

**faion-usability-agent** - Mobile UX Review mode

---

## M-UX-029: Form Design

### Problem

You need to create forms that are easy to complete.

### Framework

1. **Form Principles**
   - Ask only what you need
   - Use appropriate input types
   - Show clear labels and help
   - Validate in real-time
   - Make errors easy to fix

2. **Input Best Practices**
   | Input | Best Practice |
   |-------|---------------|
   | Text | Appropriate width for expected content |
   | Email | email input type for keyboard |
   | Phone | tel input type, auto-format |
   | Date | Date picker, not text |
   | Select | Searchable for long lists |
   | Checkbox | For multi-select, binary |
   | Radio | For single select, few options |

3. **Layout**
   - One column (mobile-friendly)
   - Labels above inputs
   - Group related fields
   - Clear progress for multi-step

4. **Validation**
   - Validate on blur, not on change
   - Inline error messages
   - Describe what's wrong and how to fix
   - Don't clear valid fields on error

### Form Design Checklist

- [ ] Only necessary fields included
- [ ] Input types appropriate
- [ ] Labels clear and visible
- [ ] Help text where needed
- [ ] Validation real-time
- [ ] Error messages actionable
- [ ] Primary action clear
- [ ] Works without JavaScript

### Agent

**faion-usability-agent** - Form Review mode

---

## M-UX-030: Onboarding Design

### Problem

You need to help new users get value quickly.

### Framework

1. **Onboarding Types**
   | Type | When | Example |
   |------|------|---------|
   | Benefits-oriented | First visit | Value proposition |
   | Function-oriented | First use | Feature tour |
   | Progressive | Over time | Contextual tips |

2. **Onboarding Principles**
   - Show value before asking for info
   - Minimize steps to first success
   - Let users skip and return later
   - Personalize based on goals

3. **Patterns**
   - Welcome screens
   - Feature tours
   - Empty states with guidance
   - Checklists and progress
   - Contextual tooltips

4. **Metrics**
   - Completion rate
   - Time to first value
   - Drop-off points
   - Feature adoption

### Onboarding Flow Template

```markdown
## Onboarding: [Product]

### Step 1: Welcome
- Headline: [Value proposition]
- CTA: Get started

### Step 2: Quick Wins
- Goal: [First success moment]
- Actions: [Minimal steps]

### Step 3: Personalization (optional)
- Question: [Relevant customization]
- Impact: [How it improves experience]

### Step 4: Feature Highlight
- Feature: [Key capability]
- Action: [Try it now]

### Success State
- Celebration: [Positive feedback]
- Next: [Clear next step]
```

### Checklist

- [ ] First value achieved quickly
- [ ] Steps skippable
- [ ] Progress visible
- [ ] Help accessible
- [ ] Drop-off tracked
- [ ] Optimized based on data

### Agent

**faion-usability-agent** - Onboarding Review mode

---

## M-UX-031: Microcopy and UX Writing

### Problem

You need to write interface text that guides and delights users.

### Framework

1. **UX Writing Principles**
   - Clear over clever
   - Concise over complete
   - Useful over promotional
   - Human over robotic

2. **Content Types**
   | Type | Purpose | Example |
   |------|---------|---------|
   | Labels | Identify elements | "Email address" |
   | Instructions | Guide actions | "Enter your email to get started" |
   | Errors | Explain problems | "This email is already registered" |
   | Confirmation | Verify actions | "Your changes have been saved" |
   | Empty states | Guide next steps | "No messages yet. Start a conversation!" |

3. **Voice and Tone**
   - Voice: Consistent personality
   - Tone: Adapts to context (error vs success)

4. **Best Practices**
   - Front-load important information
   - Use verbs for buttons (Save, not Okay)
   - Be specific (not "Error occurred")
   - Match user's language

### UX Writing Checklist

- [ ] Button text uses verbs
- [ ] Error messages explain and solve
- [ ] Confirmation messages reassure
- [ ] Empty states guide action
- [ ] Tone appropriate for context
- [ ] Terminology consistent

### Agent

**faion-usability-agent** - Content Review mode

---

## M-UX-032: UX Metrics and KPIs

### Problem

You need to measure UX quality objectively.

### Framework

1. **Metric Categories**
   | Category | Metrics | Measures |
   |----------|---------|----------|
   | Behavioral | Task success, time on task, error rate | Performance |
   | Attitudinal | SUS, NPS, CSAT | Satisfaction |
   | Business | Conversion, retention, support tickets | Impact |

2. **Common UX Metrics**
   - **SUS (System Usability Scale):** 10-question standardized survey (0-100)
   - **NPS (Net Promoter Score):** Likelihood to recommend (-100 to +100)
   - **Task Success Rate:** Percentage completing tasks
   - **Time on Task:** Efficiency measure
   - **Error Rate:** Mistakes per task

3. **Benchmarking**
   - SUS average: 68
   - Good SUS: 80+
   - NPS average varies by industry
   - Track over time for trends

4. **Measurement Plan**
   - Define metrics per feature
   - Establish baselines
   - Set targets
   - Measure regularly
   - Act on findings

### UX Metrics Dashboard

```markdown
## [Product] UX Metrics

### Overall
- SUS Score: [X] (Target: 80)
- NPS: [X] (Target: +50)

### Task Performance
| Task | Success Rate | Avg Time | Benchmark |
|------|--------------|----------|-----------|
| Sign up | 85% | 2m 30s | 90%, 2m |
| Find product | 75% | 45s | 80%, 30s |

### Trends
- SUS: [trend over time]
- Task success: [trend over time]

### Action Items
1. [Improvement based on data]
2. [Improvement based on data]
```

### Checklist

- [ ] Key metrics defined
- [ ] Baseline established
- [ ] Targets set
- [ ] Regular measurement cadence
- [ ] Findings shared with team
- [ ] Actions taken on insights

### Agent

**faion-usability-agent** - Metrics Review mode

---

# Quick Reference

## Methodology Index

| ID | Name | Category | Agent |
|----|------|----------|-------|
| M-UX-001 | Visibility of System Status | Heuristic | faion-usability-agent |
| M-UX-002 | Match Between System and Real World | Heuristic | faion-usability-agent |
| M-UX-003 | User Control and Freedom | Heuristic | faion-usability-agent |
| M-UX-004 | Consistency and Standards | Heuristic | faion-usability-agent |
| M-UX-005 | Error Prevention | Heuristic | faion-usability-agent |
| M-UX-006 | Recognition Rather Than Recall | Heuristic | faion-usability-agent |
| M-UX-007 | Flexibility and Efficiency of Use | Heuristic | faion-usability-agent |
| M-UX-008 | Aesthetic and Minimalist Design | Heuristic | faion-usability-agent |
| M-UX-009 | Help Users Recognize, Diagnose, Recover from Errors | Heuristic | faion-usability-agent |
| M-UX-010 | Help and Documentation | Heuristic | faion-usability-agent |
| M-UX-011 | User Interviews | Research | faion-ux-researcher-agent |
| M-UX-012 | Contextual Inquiry | Research | faion-ux-researcher-agent |
| M-UX-013 | Surveys and Questionnaires | Research | faion-ux-researcher-agent |
| M-UX-014 | Usability Testing | Research | faion-usability-agent |
| M-UX-015 | A/B Testing | Research | faion-ux-researcher-agent |
| M-UX-016 | Card Sorting | Research | faion-ux-researcher-agent |
| M-UX-017 | Tree Testing | Research | faion-ux-researcher-agent |
| M-UX-018 | Journey Mapping | Research | faion-ux-researcher-agent |
| M-UX-019 | Empathy Mapping | Research | faion-ux-researcher-agent |
| M-UX-020 | Persona Development | Research | faion-ux-researcher-agent |
| M-UX-021 | Diary Studies | Research | faion-ux-researcher-agent |
| M-UX-022 | Competitive Analysis | Research | faion-ux-researcher-agent |
| M-UX-023 | Information Architecture | Design | faion-usability-agent |
| M-UX-024 | Wireframing | Design | faion-usability-agent |
| M-UX-025 | Prototyping | Design | faion-usability-agent |
| M-UX-026 | Design Systems | Design | faion-usability-agent |
| M-UX-027 | Accessibility Design | Design | faion-usability-agent |
| M-UX-028 | Mobile UX Design | Design | faion-usability-agent |
| M-UX-029 | Form Design | Design | faion-usability-agent |
| M-UX-030 | Onboarding Design | Design | faion-usability-agent |
| M-UX-031 | Microcopy and UX Writing | Design | faion-usability-agent |
| M-UX-032 | UX Metrics and KPIs | Measurement | faion-usability-agent |

## When to Use What

| Goal | Method |
|------|--------|
| Understand user needs | User Interviews (M-UX-011), Contextual Inquiry (M-UX-012) |
| Validate information architecture | Card Sorting (M-UX-016), Tree Testing (M-UX-017) |
| Test usability | Usability Testing (M-UX-014), Heuristic Evaluation (M-UX-001-010) |
| Measure satisfaction | Surveys (M-UX-013), UX Metrics (M-UX-032) |
| Optimize conversion | A/B Testing (M-UX-015), Form Design (M-UX-029) |
| Map experience | Journey Mapping (M-UX-018), Empathy Mapping (M-UX-019) |
| Design for accessibility | Accessibility Design (M-UX-027) |
| Ensure consistency | Design Systems (M-UX-026), Consistency Heuristic (M-UX-004) |

---

## Sources

- [Nielsen Norman Group](https://www.nngroup.com/) - 10 Usability Heuristics
- [IDEO Design Kit](https://www.designkit.org/) - Human-Centered Design Methods
- [Rosenfeld Media](https://rosenfeldmedia.com/) - Information Architecture
- [A List Apart](https://alistapart.com/) - Web Design Standards
- [WCAG 2.2](https://www.w3.org/WAI/WCAG22/quickref/) - Accessibility Guidelines
- [Material Design](https://m3.material.io/) - Google Design System
- [Human Interface Guidelines](https://developer.apple.com/design/) - Apple Design

---

*UX Domain Skill v1.0*
*32 Methodologies (M-UX-001 to M-UX-032)*
*Agents: faion-ux-researcher-agent, faion-usability-agent*


---

## Methodologies

| ID | Name | File |
|----|------|------|
| M-UX-001 | Visibility Of System Status | [methodologies/M-UX-001_visibility_of_system_status.md](methodologies/M-UX-001_visibility_of_system_status.md) |
| M-UX-002 | Match Real World | [methodologies/M-UX-002_match_real_world.md](methodologies/M-UX-002_match_real_world.md) |
| M-UX-003 | User Control Freedom | [methodologies/M-UX-003_user_control_freedom.md](methodologies/M-UX-003_user_control_freedom.md) |
| M-UX-004 | Consistency Standards | [methodologies/M-UX-004_consistency_standards.md](methodologies/M-UX-004_consistency_standards.md) |
| M-UX-005 | Error Prevention | [methodologies/M-UX-005_error_prevention.md](methodologies/M-UX-005_error_prevention.md) |
| M-UX-006 | Recognition Over Recall | [methodologies/M-UX-006_recognition_over_recall.md](methodologies/M-UX-006_recognition_over_recall.md) |
| M-UX-007 | Flexibility Efficiency | [methodologies/M-UX-007_flexibility_efficiency.md](methodologies/M-UX-007_flexibility_efficiency.md) |
| M-UX-008 | Aesthetic Minimalist | [methodologies/M-UX-008_aesthetic_minimalist.md](methodologies/M-UX-008_aesthetic_minimalist.md) |
| M-UX-009 | Error Recovery | [methodologies/M-UX-009_error_recovery.md](methodologies/M-UX-009_error_recovery.md) |
| M-UX-010 | Help Documentation | [methodologies/M-UX-010_help_documentation.md](methodologies/M-UX-010_help_documentation.md) |
| M-UX-011 | User Interviews | [methodologies/M-UX-011_user_interviews.md](methodologies/M-UX-011_user_interviews.md) |
| M-UX-012 | Usability Testing | [methodologies/M-UX-012_usability_testing.md](methodologies/M-UX-012_usability_testing.md) |
| M-UX-013 | Surveys | [methodologies/M-UX-013_surveys.md](methodologies/M-UX-013_surveys.md) |
| M-UX-014 | Card Sorting | [methodologies/M-UX-014_card_sorting.md](methodologies/M-UX-014_card_sorting.md) |
| M-UX-015 | Personas | [methodologies/M-UX-015_personas.md](methodologies/M-UX-015_personas.md) |
| M-UX-016 | Journey Mapping | [methodologies/M-UX-016_journey_mapping.md](methodologies/M-UX-016_journey_mapping.md) |
| M-UX-017 | Wireframing | [methodologies/M-UX-017_wireframing.md](methodologies/M-UX-017_wireframing.md) |
| M-UX-018 | Prototyping | [methodologies/M-UX-018_prototyping.md](methodologies/M-UX-018_prototyping.md) |
| M-UX-019 | Ab Testing | [methodologies/M-UX-019_ab_testing.md](methodologies/M-UX-019_ab_testing.md) |
| M-UX-020 | Heuristic Evaluation | [methodologies/M-UX-020_heuristic_evaluation.md](methodologies/M-UX-020_heuristic_evaluation.md) |
| M-UX-021 | Contextual Inquiry | [methodologies/M-UX-021_contextual_inquiry.md](methodologies/M-UX-021_contextual_inquiry.md) |
| M-UX-022 | Focus Groups | [methodologies/M-UX-022_focus_groups.md](methodologies/M-UX-022_focus_groups.md) |
| M-UX-023 | Tree Testing | [methodologies/M-UX-023_tree_testing.md](methodologies/M-UX-023_tree_testing.md) |
| M-UX-024 | Accessibility Evaluation | [methodologies/M-UX-024_accessibility_evaluation.md](methodologies/M-UX-024_accessibility_evaluation.md) |
| M-UX-025 | Design Critique | [methodologies/M-UX-025_design_critique.md](methodologies/M-UX-025_design_critique.md) |
| M-UX-026 | Competitive Analysis | [methodologies/M-UX-026_competitive_analysis.md](methodologies/M-UX-026_competitive_analysis.md) |
| M-UX-027 | Content Audit | [methodologies/M-UX-027_content_audit.md](methodologies/M-UX-027_content_audit.md) |
| M-UX-028 | Cognitive Walkthrough | [methodologies/M-UX-028_cognitive_walkthrough.md](methodologies/M-UX-028_cognitive_walkthrough.md) |
| M-UX-029 | Information Architecture | [methodologies/M-UX-029_information_architecture.md](methodologies/M-UX-029_information_architecture.md) |
| M-UX-030 | Mobile Ux | [methodologies/M-UX-030_mobile_ux.md](methodologies/M-UX-030_mobile_ux.md) |
| M-UX-031 | Voice Ui | [methodologies/M-UX-031_voice_ui.md](methodologies/M-UX-031_voice_ui.md) |
| M-UX-032 | Diary Studies | [methodologies/M-UX-032_diary_studies.md](methodologies/M-UX-032_diary_studies.md) |
