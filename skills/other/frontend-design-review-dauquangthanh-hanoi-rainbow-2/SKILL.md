---
name: frontend-design-review
description: Conducts comprehensive frontend design reviews covering UI/UX design quality, design system validation, accessibility compliance, responsive design patterns, component library architecture, and visual design consistency. Evaluates design specifications, Figma/Sketch files, design tokens, interaction patterns, and user experience flows. Identifies usability issues, accessibility violations, design system deviations, and provides actionable recommendations for improvement. Produces detailed design review reports with severity-rated findings, visual examples, and implementation guidelines. Use when reviewing frontend designs, validating design systems, ensuring accessibility compliance, evaluating component libraries, assessing responsive designs, or when users mention design review, UI/UX review, Figma review, design system validation, accessibility audit, or frontend design quality.
---

# Frontend Design Review

## Overview

This skill provides expert guidance for conducting thorough frontend design reviews, covering UI/UX design quality, design system consistency, accessibility compliance, and responsive design patterns. The skill helps identify design issues early in the development lifecycle, ensuring designs meet quality standards, accessibility requirements, and business objectives before implementation.

## Core Capabilities

## 1. UI/UX Design Quality Review

- Visual design assessment (typography, color, spacing, layout, visual hierarchy)
- User experience evaluation (flows, interactions, navigation, usability)
- Design consistency verification across screens and journeys
- Brand alignment and visual identity validation
- Cognitive load analysis

### 2. Design System Validation

- Component library review (design, variants, states, reusability)
- Design tokens validation (colors, typography, spacing)
- Pattern library assessment for consistency
- Documentation quality evaluation
- Design system governance assessment

### 3. Accessibility Compliance

- WCAG 2.1 AA compliance verification
- Color contrast validation (4.5:1 text, 3:1 UI components)
- Keyboard navigation and focus management
- Screen reader support validation
- Accessible interaction patterns review

### 4. Responsive Design Review

- Breakpoint strategy evaluation
- Mobile-first approach assessment
- Touch target sizing verification (44x44px minimum)
- Content adaptation across viewports
- Performance considerations

### 5. Component Architecture Assessment

- Component hierarchy and composition patterns
- Reusability and flexibility evaluation
- State management review (default, hover, active, disabled, error, loading)
- Component variants and customization patterns
- Component documentation quality

## Workflow

### Phase 1: Pre-Review Preparation

**1. Gather Design Assets**

- Collect Figma/Sketch files, design specifications, mockups
- Obtain design system documentation and component library
- Review brand guidelines and style guides
- Gather user research findings and personas

**2. Understand Context**

- Review project requirements and business objectives
- Understand target users and use cases
- Identify key user journeys and critical flows
- Note technical constraints and platform requirements

**3. Define Review Scope**

- Identify screens/flows to review
- Determine review depth (high-level vs. detailed)
- Set priorities based on importance
- Establish timeline and deliverables

### Phase 2: Conduct Design Review

**Step 1: Visual Design Review**

- Assess typography (font selection, type scale, line heights, consistency)
- Evaluate color system (palette, contrast, semantic usage, tokens)
- Review spacing and layout (grid system, whitespace, alignment)
- Check visual hierarchy (size, color, position, emphasis)
- Validate iconography (style, size, clarity, consistency)
- Assess imagery and media (quality, aspect ratios, optimization)

**Step 2: Design System Compliance**

- Verify component usage matches design system
- Check for design token usage (no hard-coded values)
- Identify deviations from established patterns
- Validate component variants and states
- Review custom components vs. system components

**Step 3: Accessibility Audit**

- Test color contrast ratios for all text and UI elements
- Verify keyboard navigation and tab order
- Check focus indicators visibility and clarity
- Validate ARIA labels and semantic structure
- Review alternative text for images
- Assess form label associations
- Test interactive element accessibility

**Step 4: Responsive Design Evaluation**

- Review breakpoint strategy (mobile, tablet, desktop)
- Check content adaptation at different viewports
- Verify touch target sizes on mobile
- Assess navigation patterns for mobile
- Review image responsiveness and optimization
- Validate typography scaling across devices

**Step 5: Component Architecture Analysis**

- Evaluate component organization and hierarchy
- Review component reusability and composition
- Check component state coverage
- Assess variant design and flexibility
- Validate component props and customization

**Step 6: User Experience Assessment**

- Analyze user flows and task completion paths
- Evaluate navigation structure and findability
- Check interaction patterns and feedback
- Assess error states and error handling
- Review empty states and loading states
- Validate form design and validation patterns

### Phase 3: Document Findings

**1. Categorize Issues by Severity**

- **Critical**: Blocking issues, must fix before launch
- **High**: Significant usability/accessibility issues
- **Medium**: Issues with workarounds, should fix soon
- **Low**: Minor polish, nice-to-haves

**2. Create Detailed Findings Report**
See [design-review-report-template.md](references/design-review-report-template.md) for comprehensive report structure

Include:

- Executive summary with key statistics
- Review scope documentation
- Findings by category with specific examples
- Severity-rated issue list
- Positive observations (what's working well)
- Actionable recommendations with priorities
- Action items with owners and timelines

**3. Provide Visual Examples**

- Screenshot issues with annotations
- Show before/after for recommendations
- Include contrast ratio measurements
- Document component state issues visually

### Phase 4: Collaborate on Solutions

**1. Prioritize Fixes**

- Separate must-fix from nice-to-have
- Consider implementation effort
- Balance user impact with development cost

**2. Create Action Plan**

- Assign owners (design team vs. development team)
- Set realistic timelines
- Schedule follow-up review

**3. Document Decisions**

- Record accepted risks or trade-offs
- Note items deferred to future work
- Update design system if patterns change

## Severity Level Guidelines

**Critical (Blocking)**

- Violates WCAG AA requirements (legal risk)
- Completely blocks core user tasks
- Causes data loss or security issues
- Severely damages brand or user trust

**High Priority**

- Significantly degrades user experience
- Impacts large number of users
- Creates major accessibility barriers
- Inconsistent with design system causing confusion

**Medium Priority**

- Negatively impacts experience but has workarounds
- Affects subset of users
- Minor accessibility issues (WCAG AAA)
- Design inconsistencies that are noticeable

**Low Priority**

- Polish and optimization items
- Edge case issues
- Minor visual refinements
- Nice-to-have enhancements

## Accessibility Quick Reference

**WCAG 2.1 AA Requirements:**

- Color contrast: 4.5:1 for normal text, 3:1 for large text (18pt+ or 14pt+ bold)
- UI component contrast: 3:1 minimum
- Keyboard accessible: All functionality available via keyboard
- Focus visible: Clear focus indicators on interactive elements
- Text alternatives: All images have appropriate alt text
- Form labels: All inputs have associated labels
- Semantic HTML: Proper heading hierarchy and landmarks
- Touch targets: 44x44 CSS pixels minimum

**Testing Tools:**

- Color contrast: WebAIM Contrast Checker, Stark plugin
- Keyboard nav: Manual testing with Tab/Shift+Tab
- Screen reader: Test with VoiceOver (Mac), NVDA (Windows)

## Design System Review Checklist

**Component Usage:**

- [ ] All components sourced from design system
- [ ] No one-off custom variations without justification
- [ ] Component variants used appropriately
- [ ] All component states designed (default, hover, active, disabled, error, loading)

**Design Tokens:**

- [ ] Colors use token references (not hex values)
- [ ] Typography uses token references (not hard-coded sizes)
- [ ] Spacing uses token references (8px grid system)
- [ ] Shadows and effects use token references

**Patterns:**

- [ ] Navigation patterns consistent with system
- [ ] Form patterns follow system conventions
- [ ] Modal/dialog patterns match system
- [ ] Empty states use system patterns
- [ ] Error handling follows system patterns

## Reference Files

**Load these references based on specific review needs:**

- **[best-practices-for-design-reviews.md](references/best-practices-for-design-reviews.md)** - Review methodology, tools, and techniques for effective design reviews

- **[common-design-issues-to-watch-for.md](references/common-design-issues-to-watch-for.md)** - Frequently encountered design problems and red flags to identify during reviews

- **[design-review-process.md](references/design-review-process.md)** - Comprehensive step-by-step process with detailed checklists for each review phase

- **[design-system-patterns.md](references/design-system-patterns.md)** - Design system validation criteria, component patterns, and token usage guidelines

- **[responsive-design-patterns.md](references/responsive-design-patterns.md)** - Breakpoint strategies, mobile-first patterns, and responsive design best practices

- **[accessibility-guidelines.md](references/accessibility-guidelines.md)** - Detailed WCAG 2.1 AA compliance guidelines, testing procedures, and accessibility patterns

- **[severity-levels.md](references/severity-levels.md)** - Detailed severity level definitions and criteria for categorizing design issues

- **[design-review-report-template.md](references/design-review-report-template.md)** - Complete report template with all sections for documenting review findings

## Example Review Flow

**Scenario**: Reviewing a new checkout flow design in Figma

1. **Preparation** (30 min)
   - Review checkout requirements and success metrics
   - Identify 5 screens in checkout flow
   - Gather payment compliance requirements
   - Review design system component library

2. **Visual Design Review** (45 min)
   - Check typography consistency across all 5 screens
   - Verify color contrast on CTA buttons (found 2 issues)
   - Validate spacing follows 8px grid
   - Review visual hierarchy on payment screen

3. **Accessibility Audit** (60 min)
   - Test color contrast: 3 text elements fail (4.2:1, need 4.5:1)
   - Check keyboard flow: Tab order jumps incorrectly on screen 3
   - Verify ARIA labels: Payment input missing label association
   - Review error states: Error messages lack semantic markup

4. **Responsive Review** (30 min)
   - Check mobile breakpoint: Form inputs too small (38px height)
   - Verify tablet layout: Good adaptation
   - Test content reflow: Success

5. **Design System Check** (20 min)
   - Found custom button variant not in system
   - Spacing uses hard-coded values instead of tokens
   - Form patterns match system conventions ✅

6. **Document Findings** (45 min)
   - 3 Critical issues: Contrast failures, touch target sizes
   - 5 High issues: Keyboard navigation, missing labels
   - 4 Medium issues: Design token usage, custom components
   - Create report using template with visual examples

7. **Deliverables**
   - Design review report with 12 findings
   - Annotated Figma comments on specific issues
   - Prioritized action items with owners
   - Schedule follow-up review in 1 week

**Total Time**: ~3.5 hours for comprehensive review

## Tips for Effective Reviews

**Be Specific**: Don't say "improve contrast". Say "Body text on blue background has 3.8:1 contrast, needs 4.5:1. Darken text to #1a1a1a or lighten background."

**Show Examples**: Include screenshots with annotations. Show the issue and suggest visual fixes.

**Prioritize**: Clearly separate must-fix from nice-to-have. Focus on user impact.

**Provide Context**: Explain why an issue matters. "This contrast failure affects 8% of users with low vision."

**Be Constructive**: Acknowledge what works well. Balance criticism with recognition.

**Collaborate**: Review findings with designers before finalizing. Get their input on solutions.

**Follow Up**: Schedule re-review to verify fixes. Track issues to completion.
