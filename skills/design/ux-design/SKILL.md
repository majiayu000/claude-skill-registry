---
name: ux-design
description: UX design expert for user research, personas, journey mapping, information architecture, wireframing, prototyping, usability testing, and accessibility. Creates user-centered designs with WCAG 2.1 AA/AAA compliance.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# UX Design Skill

Expert in user experience design, creating intuitive, accessible, and user-centered digital experiences.

## When to Use This Skill

Use this skill when:

- Conducting user research and creating personas
- Designing information architecture and user flows
- Creating wireframes and prototypes
- Planning usability tests
- Ensuring accessibility compliance (WCAG 2.1 AA/AAA)
- Developing design systems and component libraries
- Analyzing user feedback and iterating on designs

## Core UX Design Process

### 1. Discover & Research

**User Research**

- Conduct user interviews and surveys
- Analyze user pain points and goals
- Create data-driven user personas
- Map user journeys and scenarios
- Perform competitive analysis
- Identify accessibility requirements

**Deliverables:**

- User personas with demographics, goals, pain points, behaviors
- Journey maps showing touchpoints and emotions
- Competitive analysis reports
- Research insights summary

### 2. Define & Strategize

**Information Architecture**

- Define content hierarchy
- Create site maps and navigation structures
- Organize information logically
- Plan user flows and task flows
- Identify key user paths

**Deliverables:**

- Site maps and IA diagrams
- User flow diagrams
- Task flow documentation
- Navigation structures

### 3. Design & Prototype

**Wireframing**

- Start with low-fidelity sketches
- Create mid-fidelity wireframes
- Progress to high-fidelity mockups
- Focus on layout, hierarchy, and content placement
- Ensure responsive design across breakpoints (mobile, tablet, desktop)

**Prototyping**

- Create interactive prototypes for testing
- Design meaningful microinteractions
- Plan transitions and animations
- Consider loading states and error handling

**Deliverables:**

- Low-fidelity wireframes
- High-fidelity mockups
- Interactive prototypes
- Responsive design specifications

### 4. Validate & Test

**Usability Testing**

- Create test protocols and scenarios
- Define success metrics
- Conduct moderated/unmoderated tests
- Gather qualitative and quantitative feedback
- Identify usability issues

**Accessibility Audits**

- Test with screen readers
- Verify keyboard navigation
- Check color contrast ratios
- Validate ARIA labels and semantic HTML
- Ensure WCAG 2.1 AA/AAA compliance

**Deliverables:**

- Usability test protocols
- Test results and insights
- Accessibility audit reports
- Recommended improvements

### 5. Iterate & Refine

**Design Iteration**

- Analyze test results
- Prioritize issues by severity
- Implement improvements
- Retest critical flows
- Document design decisions

## Design Principles

### User-Centered Design

- **Empathy First**: Always design for the user, not for yourself
- **Accessibility is Non-Negotiable**: WCAG 2.1 AA minimum, AAA when possible
- **Progressive Disclosure**: Show only what users need, when they need it
- **Clear Feedback**: Provide immediate, clear feedback for all actions
- **Error Prevention**: Design to prevent errors before they happen

### Visual Hierarchy

- Use size, color, contrast, and spacing to guide attention
- Most important elements should be most prominent
- Group related elements together (proximity)
- Use consistent patterns for similar elements

### Cognitive Load

- Minimize user memory burden
- Use recognition over recall
- Provide clear labels and instructions
- Break complex tasks into simple steps
- Use familiar patterns and conventions

## Accessibility Guidelines (WCAG 2.1)

### Perceivable

- **Text Alternatives**: Alt text for images, labels for icons
- **Color Contrast**: Minimum 4.5:1 for normal text, 3:1 for large text
- **Resizable Text**: Support up to 200% zoom
- **Non-Text Contrast**: 3:1 for UI components and graphics

### Operable

- **Keyboard Navigation**: All functionality accessible via keyboard
- **Focus Indicators**: Clear, visible focus states
- **No Keyboard Traps**: Users can navigate away from all elements
- **Skip Links**: Allow skipping repetitive content
- **Timing**: Provide controls for time-based content

### Understandable

- **Clear Language**: Use simple, concise language
- **Predictable Navigation**: Consistent patterns across pages
- **Error Identification**: Clearly identify and describe errors
- **Input Assistance**: Provide labels, instructions, and validation

### Robust

- **Valid HTML**: Use semantic, valid markup
- **ARIA Attributes**: Use ARIA when native HTML isn't sufficient
- **Screen Reader Compatible**: Test with NVDA, JAWS, VoiceOver
- **Cross-Browser**: Work across modern browsers

## Design System Components

### Design Tokens

- Colors (primary, secondary, accent, semantic)
- Typography (font families, sizes, weights, line heights)
- Spacing (margins, padding, gaps)
- Shadows and elevation
- Border radius and borders
- Breakpoints (mobile, tablet, desktop, wide)

### Component Library

- Buttons (primary, secondary, tertiary, danger)
- Forms (inputs, selects, checkboxes, radio buttons)
- Navigation (headers, footers, menus, breadcrumbs)
- Feedback (alerts, toasts, modals, tooltips)
- Data display (tables, lists, cards, badges)
- Loading states (spinners, skeletons, progress bars)

### Patterns

- Authentication flows (login, signup, password reset)
- CRUD operations (create, read, update, delete)
- Search and filtering
- Pagination and infinite scroll
- Empty states and error states

## Integration with Project

When using this skill in the st44-home project:

### With Frontend Skill

1. **UX Design** defines the structure, flows, and interactions
2. **Frontend** implements using Angular 21+ patterns
3. **Frontend Design** applies aesthetic polish

### With Database Skill

- Design data models based on user needs
- Plan for user-friendly data display
- Consider performance for user experience

### Workflow Integration

1. **Research Phase**: Use this skill to understand users
2. **Design Phase**: Create wireframes and flows
3. **Implementation**: Hand off to `frontend` skill with specs
4. **Polish**: Apply `frontend-design` for aesthetics
5. **Validate**: Return here for usability testing

## Deliverable Templates

### User Persona Template

```markdown
## Persona Name

**Demographics:**

- Age, location, occupation, tech proficiency

**Goals:**

- What they want to achieve
- Why they use the product

**Pain Points:**

- Current frustrations
- Barriers to success

**Behaviors:**

- How they currently solve problems
- Preferred platforms and devices

**Quote:**
"A representative quote that captures their mindset"
```

### User Flow Template

```markdown
## User Flow: [Task Name]

**Entry Point:** Where the user starts
**Goal:** What the user wants to accomplish
**Success Criteria:** How we know they succeeded

**Steps:**

1. Action → System Response
2. Action → System Response
3. [Continue...]

**Alternative Paths:**

- Error scenarios
- Edge cases

**Exit Points:**

- Success state
- Abandon points
```

### Wireframe Specifications

```markdown
## Page/Component: [Name]

**Purpose:** Brief description
**User Need:** What problem this solves

**Layout:**

- Header: [Elements]
- Main Content: [Sections]
- Sidebar: [Components]
- Footer: [Elements]

**Key Elements:**

- Element 1: Purpose, behavior, states
- Element 2: Purpose, behavior, states

**Interactions:**

- Hover states
- Click actions
- Form validation
- Loading states

**Responsive Behavior:**

- Mobile: [Changes]
- Tablet: [Changes]
- Desktop: [Default]
```

## Success Criteria

Before marking UX design work complete:

- [ ] User research conducted with clear insights
- [ ] Personas created based on real user data
- [ ] User flows mapped for key tasks
- [ ] Wireframes created (low to high fidelity)
- [ ] Accessibility requirements defined (WCAG 2.1 AA minimum)
- [ ] Interactive prototypes ready for testing
- [ ] Usability test plan created
- [ ] Design system tokens and components documented
- [ ] Responsive behavior specified for all breakpoints
- [ ] Handoff documentation clear for implementation

## Tools & Testing

### Recommended Testing Approach

```bash
# Accessibility testing tools
# - AXE DevTools (browser extension)
# - Lighthouse (Chrome DevTools)
# - WAVE (browser extension)

# Screen readers
# - NVDA (Windows) - free
# - JAWS (Windows) - commercial
# - VoiceOver (macOS/iOS) - built-in

# Keyboard navigation testing
# - Test all functionality with Tab, Enter, Escape, Arrow keys
# - Verify focus order is logical
# - Ensure no keyboard traps
```

## Philosophy

> Great UX design is invisible. Users should accomplish their goals effortlessly, without thinking about the interface. Design with empathy, test with real users, and iterate based on evidence, not assumptions.

## Resources

### Key Principles

- **Don't Make Me Think** (Steve Krug): Minimize cognitive load
- **Fitts's Law**: Larger, closer targets are faster to acquire
- **Hick's Law**: More choices = longer decision time
- **Miller's Law**: People remember 7±2 items
- **Jakob's Law**: Users expect your site to work like others

### Accessibility Resources

- WCAG 2.1 Guidelines: https://www.w3.org/WAI/WCAG21/quickref/
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
- A11y Project Checklist: https://www.a11yproject.com/checklist/
