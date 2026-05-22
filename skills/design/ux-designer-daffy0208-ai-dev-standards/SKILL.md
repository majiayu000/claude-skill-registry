---
name: UX Designer
description: Design user experiences and interfaces. Use when creating user journeys, wireframes, prototypes, or improving usability. Covers user flows, information architecture, interaction design, and accessibility.
version: 1.0.0
---

# UX Designer

Design intuitive, accessible user experiences grounded in research.

## Core Principle

**Design for users, not yourself.** Base design decisions on user research and usability testing, not personal preference.

## 5-Phase UX Design Process

### Phase 1: Information Architecture

**Goal**: Organize content and functionality logically

**Activities**:

- Card sorting: Let users organize content into categories
- Site mapping: Create hierarchy of pages and features
- Navigation design: Primary, secondary, utility navigation
- Labeling: Clear, user-friendly terminology

**Validation**:

- [ ] IA tested with 5+ users (tree testing)
- [ ] Navigation paths clear and logical
- [ ] Labels match user mental models

---

### Phase 2: User Flows

**Goal**: Map paths users take to complete tasks

**Key Flows to Design**:

- Onboarding: First-time user experience
- Core tasks: Primary use cases (80% of usage)
- Error states: Recovery from mistakes
- Edge cases: Less common but important scenarios

**Flow Diagram Elements**:

```
[Entry Point] → [Decision] → [Action] → [Outcome]
                    ↓
               [Alternative Path]
```

**Validation**:

- [ ] Happy path documented
- [ ] Error states designed
- [ ] Exit points identified
- [ ] Flows match user research

---

### Phase 3: Wireframing

**Goal**: Create low-fidelity layouts focusing on structure

**Fidelity Levels**:

- **Low-fi**: Sketches, boxes, placeholder text (fastest)
- **Mid-fi**: Grayscale, realistic content, basic interactions
- **High-fi**: Styled, branded, detailed interactions

**Key Screens to Wireframe**:

- Homepage/Dashboard
- Core task screens (CRUD operations)
- Navigation (header, sidebar, footer)
- Forms and input validation
- Empty states, loading states, error states

**Wireframe Checklist**:

- [ ] Clear visual hierarchy
- [ ] Consistent layout patterns
- [ ] Accessible contrast and sizing
- [ ] Touch targets ≥44x44px (mobile)
- [ ] Forms grouped logically

---

### Phase 4: Prototyping & Testing

**Goal**: Create interactive prototypes for usability testing

**Prototyping Tools**:

- Figma (recommended): Collaborative, browser-based
- Adobe XD: Design system friendly
- Framer: Code-based prototyping
- InVision: Simple click-through prototypes

**Usability Testing**:

```
Script:
1. Welcome (5 min): Explain process, get consent
2. Context (5 min): Ask about current solutions
3. Tasks (20 min): "Try to [complete task]"
4. Think-aloud: "What are you thinking?"
5. Debrief (5 min): Overall impressions

Metrics:
- Task completion rate (target: >70%)
- Time on task
- Error rate
- Satisfaction (1-5 scale)
```

**Validation**:

- [ ] Prototype covers main user flows
- [ ] 5+ users tested
- [ ] Task completion >70%
- [ ] Critical issues documented and fixed

---

### Phase 5: UI Design & Handoff

**Goal**: Create high-fidelity, production-ready designs

**Design System Elements**:

- Colors: Primary, secondary, neutrals, semantic (error, success)
- Typography: Scale (h1-h6, body, small), weights
- Spacing: 4pt or 8pt grid system
- Components: Buttons, inputs, cards, modals, etc.
- Icons: Consistent set (Heroicons, Lucide, Font Awesome)

**Accessibility (WCAG 2.1 AA)**:

- Color contrast: 4.5:1 for text, 3:1 for large text/UI
- Keyboard navigation: Tab order logical
- Screen readers: Semantic HTML, ARIA labels
- Focus states: Visible focus indicators
- Alt text: Descriptive image alternatives

**Developer Handoff**:

- Design specs: Spacing, colors, fonts (inspect mode)
- Component states: Default, hover, active, disabled, error
- Responsive breakpoints: Mobile, tablet, desktop
- Interactions: Animations, transitions, micro-interactions
- Assets: Icons, images, logos (exported)

**Validation**:

- [ ] Designs match brand guidelines
- [ ] Accessibility checked (Contrast, keyboard nav)
- [ ] Responsive layouts for all breakpoints
- [ ] Component library documented
- [ ] Handoff reviewed with developers

---

## Key UX Principles

### 1. Consistency

Use familiar patterns. Don't reinvent standard UI elements.

### 2. Feedback

Confirm user actions (success messages, loading states).

### 3. Error Prevention

Design to prevent errors, not just handle them.

### 4. Recognition Over Recall

Show options rather than requiring memory.

### 5. Flexibility

Support both novice and expert users (shortcuts, defaults).

---

## Design Patterns

**Form Design**:

- Label above field (not placeholder)
- Inline validation (real-time feedback)
- Clear error messages ("Email must include @")
- One column layout (faster completion)
- Group related fields

**Navigation**:

- Current page highlighted
- Breadcrumbs for deep hierarchies
- Search for large sites
- Max 7 items in top nav (Miller's Law)

**Empty States**:

- Explain why it's empty
- Provide clear next action
- Use illustration or icon
- Example: "No tasks yet. Create your first task to get started."

**Loading States**:

- Skeleton screens (better than spinners)
- Progress indicators for long operations
- Optimistic UI (show result before confirmed)

---

## Accessibility Checklist

- [ ] Color contrast ≥4.5:1 for text
- [ ] Keyboard navigation works (Tab, Enter, Esc)
- [ ] Focus indicators visible
- [ ] Alt text for images
- [ ] Form labels associated with inputs
- [ ] Semantic HTML (headings, nav, main, etc.)
- [ ] ARIA labels for icon buttons
- [ ] Screen reader tested
- [ ] Zoom to 200% works (responsive)
- [ ] No flashing content (seizure risk)

---

## Tools & Resources

**Design Tools**:

- Figma: Collaborative design
- Tailwind CSS: Utility-first CSS framework
- shadcn/ui: Component library
- Heroicons/Lucide: Icon sets

**Prototyping**:

- Figma: Built-in prototyping
- Framer: Advanced interactions
- ProtoPie: Complex micro-interactions

**Testing**:

- Maze: Remote usability testing
- UserTesting: Moderated and unmoderated tests
- Hotjar: Session recordings and heatmaps

**Accessibility**:

- WAVE: Accessibility checker
- axe DevTools: Browser extension
- Lighthouse: Automated audits

---

## Related Resources

**Related Skills**:

- `user-researcher` - For grounding design in research
- `frontend-builder` - For implementing designs
- `product-strategist` - For validating design direction

**Related Patterns**:

- `STANDARDS/design-systems/component-library.md` - Component standards (when created)
- `STANDARDS/best-practices/accessibility.md` - Accessibility guidelines (when created)

**Related Playbooks**:

- `PLAYBOOKS/conduct-usability-test.md` - Testing procedure (when created)
- `PLAYBOOKS/design-handoff.md` - Developer handoff process (when created)
