---
name: "UI/UX Design Review"
description: "Comprehensive design review for websites and desktop applications with extensive accessibility analysis. Use this skill when users ask you to review UI/UX designs, wireframes, mockups, prototypes, or deployed interfaces for usability, accessibility (WCAG compliance), visual design, interaction patterns, responsive design, and best practices for web and desktop applications."
---

# UI/UX Design Review

This skill provides comprehensive design review capabilities for websites and desktop applications, with a strong focus on accessibility compliance and best practices.

## When to Use This Skill

Activate this skill when the user requests:
- Review of UI/UX designs, wireframes, or mockups
- Accessibility audit (WCAG 2.1/2.2 compliance)
- Usability assessment
- Visual design critique
- Interaction pattern review
- Responsive design evaluation
- Design system assessment
- Component library review
- User flow analysis
- Information architecture review
- Desktop application UI review

## Review Framework

### 1. Initial Analysis

When a user provides a design or interface, begin by:

1. **Understanding Context**
   - Ask clarifying questions about:
     - Target audience and personas
     - Platform(s): web, desktop (Windows/Mac/Linux), mobile
     - Accessibility requirements and compliance level needed
     - Brand guidelines or design system in use
     - User research or testing conducted
     - Technical constraints
     - Browser/OS support requirements
     - Key user goals and tasks

2. **Design Artifact Analysis**
   - If designs, screenshots, or prototypes are provided, analyze:
     - Visual hierarchy and layout
     - Color usage and contrast
     - Typography and readability
     - Component patterns and consistency
     - Navigation structure
     - Interactive elements
     - Responsive behavior
     - State variations (hover, active, disabled, error, etc.)

### 2. Comprehensive Review Areas

Evaluate the design across these dimensions:

#### A. Accessibility (WCAG 2.1/2.2 Compliance)

This is a CRITICAL area that must be thoroughly reviewed for all interfaces.

**Level A Requirements (Minimum):**

**1.1 Text Alternatives**
- [ ] All images have appropriate alt text
- [ ] Decorative images have empty alt attributes
- [ ] Icons have accessible labels
- [ ] Complex images have detailed descriptions
- [ ] Image buttons have descriptive text

**1.2 Time-based Media**
- [ ] Video content has captions
- [ ] Audio content has transcripts
- [ ] Pre-recorded media has alternatives

**1.3 Adaptable**
- [ ] Content structure is logical without CSS
- [ ] Reading order is meaningful
- [ ] Instructions don't rely solely on sensory characteristics
- [ ] Semantic HTML is used properly
- [ ] Form labels are programmatically associated

**1.4 Distinguishable**
- [ ] Color is not the only visual means of conveying information
- [ ] Audio controls are available
- [ ] Text has sufficient contrast (4.5:1 for normal text, 3:1 for large text)
- [ ] Text can be resized up to 200% without loss of functionality
- [ ] Images of text are avoided (except logos)

**2.1 Keyboard Accessible**
- [ ] All functionality is keyboard accessible
- [ ] No keyboard traps exist
- [ ] Keyboard shortcuts don't conflict with assistive technologies
- [ ] Focus order is logical
- [ ] Focus is visible at all times

**2.2 Enough Time**
- [ ] Time limits can be adjusted, extended, or turned off
- [ ] Moving, blinking, scrolling content can be paused
- [ ] Auto-updating content can be paused or controlled

**2.3 Seizures and Physical Reactions**
- [ ] Content doesn't flash more than 3 times per second
- [ ] No content violates flash threshold

**2.4 Navigable**
- [ ] Skip links allow bypassing repeated content
- [ ] Page titles are descriptive and unique
- [ ] Focus order preserves meaning
- [ ] Link purpose is clear from context
- [ ] Multiple navigation methods exist
- [ ] Headings and labels are descriptive

**2.5 Input Modalities**
- [ ] All functionality works with pointer gestures
- [ ] Touch targets are sufficiently large (minimum 44x44px)
- [ ] Accidental activation is prevented

**3.1 Readable**
- [ ] Page language is identified
- [ ] Language changes are marked up

**3.2 Predictable**
- [ ] Focus doesn't trigger unexpected changes
- [ ] Input doesn't trigger unexpected changes
- [ ] Navigation is consistent across pages
- [ ] Components are identified consistently

**3.3 Input Assistance**
- [ ] Form errors are identified and described
- [ ] Labels and instructions are provided
- [ ] Error suggestions are offered
- [ ] Critical actions can be reversed, checked, or confirmed

**4.1 Compatible**
- [ ] HTML is valid and properly nested
- [ ] IDs are unique
- [ ] ARIA attributes are used correctly
- [ ] Status messages are programmatically determinable

**Level AA Requirements (Recommended):**

- [ ] Contrast ratio is at least 4.5:1 (3:1 for large text)
- [ ] Text can be resized up to 200% without assistive technology
- [ ] Images of text are avoided unless customizable
- [ ] Visual presentation of text allows customization
- [ ] Audio content doesn't interfere with screen readers
- [ ] Multiple ways to locate pages exist
- [ ] Headings and labels are descriptive
- [ ] Focus indicator is visible
- [ ] Section headings are used to organize content

**Level AAA Requirements (Best Practice):**

- [ ] Contrast ratio is at least 7:1 (4.5:1 for large text)
- [ ] No images of text are used
- [ ] Text spacing can be adjusted
- [ ] Content reflows to 320px without scrolling
- [ ] Hover/focus content is dismissible and persistent

**Provide Feedback On:**
- Specific WCAG violations with severity level
- Missing ARIA labels and landmarks
- Color contrast issues with measured ratios
- Keyboard navigation problems
- Screen reader compatibility issues
- Missing alternative text
- Form accessibility issues
- Focus management problems
- Semantic HTML issues

**Testing Recommendations:**
- Use automated tools: axe DevTools, WAVE, Lighthouse
- Manual keyboard navigation testing
- Screen reader testing (NVDA, JAWS, VoiceOver)
- Color contrast analyzers
- Focus indicator visibility
- Zoom testing (200%, 400%)

#### B. Visual Design & Aesthetics

**Evaluate:**
- Visual hierarchy and layout structure
- Color palette and color theory application
- Typography choices and hierarchy
- White space and density
- Visual balance and alignment
- Consistency with brand guidelines
- Modern vs dated design patterns
- Visual weight distribution
- Grid system usage
- Component visual consistency

**Provide Feedback On:**
- Cluttered or overwhelming layouts
- Poor visual hierarchy
- Inconsistent spacing
- Typography issues (too many fonts, poor sizing)
- Color palette problems
- Lack of visual breathing room
- Misaligned elements
- Inconsistent component styling
- Dated design patterns

**Design System Considerations:**
- Design token usage (colors, spacing, typography)
- Component library consistency
- Pattern library adherence
- Brand guideline compliance

#### C. User Experience & Usability

**Evaluate:**
- User flow logic and efficiency
- Information architecture
- Navigation patterns and clarity
- Cognitive load
- Task completion efficiency
- Error prevention and recovery
- Feedback mechanisms
- Learnability for new users
- Efficiency for experienced users
- Mental models and user expectations
- Consistency with platform conventions

**Provide Feedback On:**
- Confusing navigation
- Too many steps to complete tasks
- Unclear labeling or terminology
- Missing or unclear feedback
- Poor error messages
- Inconsistent interaction patterns
- Violation of established conventions
- High cognitive load
- Missing confirmation for destructive actions

**Jakob Nielsen's Usability Heuristics:**
1. Visibility of system status
2. Match between system and real world
3. User control and freedom
4. Consistency and standards
5. Error prevention
6. Recognition rather than recall
7. Flexibility and efficiency of use
8. Aesthetic and minimalist design
9. Help users recognize and recover from errors
10. Help and documentation

#### D. Responsive Design & Layout

**Evaluate:**
- Breakpoint strategy
- Mobile-first approach
- Touch target sizes (minimum 44x44px)
- Content reflow behavior
- Layout patterns (sidebar, hamburger menu, etc.)
- Image and media responsiveness
- Typography scaling
- Navigation adaptation
- Form layout on mobile
- Table handling on small screens

**Provide Feedback On:**
- Missing breakpoints
- Horizontal scrolling on mobile
- Too-small touch targets
- Overlapping content
- Poor mobile navigation
- Unreadable text on mobile
- Missing mobile-specific patterns
- Inefficient use of screen space

**Desktop-Specific Considerations:**
- Window resizing behavior
- Minimum/maximum window dimensions
- Multi-monitor support
- Native OS patterns (Windows, macOS, Linux)
- Keyboard shortcuts
- Context menus
- Drag and drop

#### E. Typography & Readability

**Evaluate:**
- Font choices and pairings
- Type scale and hierarchy
- Line length (45-75 characters optimal)
- Line height (1.5-1.8 for body text)
- Font size (minimum 16px for body text)
- Letter spacing and word spacing
- Text alignment and justification
- Heading hierarchy
- Font rendering and smoothing

**Provide Feedback On:**
- Too many font families (limit to 2-3)
- Poor font size choices
- Insufficient contrast
- Lines too long or too short
- Inadequate line height
- Missing heading hierarchy
- Justified text without hyphenation
- All-caps text for long content
- Poor font weight choices

**Best Practices:**
- Use system fonts for performance
- Include fallback fonts
- Implement proper font loading strategy
- Use relative units (rem, em)
- Ensure readability at 200% zoom

#### F. Color & Contrast

**Evaluate:**
- Color palette cohesion
- Contrast ratios (WCAG compliance)
- Color meaning and semantics
- Color blindness accessibility
- Dark mode support
- Brand color usage
- Color consistency
- Accent and action colors

**Provide Feedback On:**
- Insufficient contrast ratios
- Relying solely on color to convey information
- Too many colors in the palette
- Poor color combinations
- Missing dark mode
- Inconsistent color usage
- Colors that don't work for color blindness
- Clashing or garish combinations

**Tools for Testing:**
- Contrast checkers (WebAIM, Stark)
- Color blindness simulators
- Color palette analyzers

**Contrast Requirements:**
- Normal text: 4.5:1 (AA), 7:1 (AAA)
- Large text (18pt+/14pt bold+): 3:1 (AA), 4.5:1 (AAA)
- UI components and graphics: 3:1 (AA)

#### G. Interactive Elements & Components

**Evaluate:**
- Button styles and states
- Form controls and inputs
- Links and their appearance
- Interactive feedback (hover, active, focus, disabled)
- Loading states and skeletons
- Error states and validation
- Success states and confirmations
- Tooltips and popovers
- Modals and dialogs
- Dropdown and select menus
- Toggle switches and checkboxes
- Radio buttons
- Accordions and collapsible content

**Provide Feedback On:**
- Unclear clickable areas
- Missing hover/focus states
- Poor button hierarchy
- Inconsistent interactive patterns
- Missing loading indicators
- Unclear disabled states
- Poor error messaging
- Ambiguous icons without labels
- Too many action options
- Destructive actions without confirmation

**Component Checklist:**
- [ ] All states are designed (default, hover, focus, active, disabled, error, success)
- [ ] Touch targets meet minimum size
- [ ] Interactive elements have clear affordances
- [ ] Focus indicators are visible
- [ ] Loading states prevent multiple submissions
- [ ] Error messages are helpful and specific

#### H. Navigation & Information Architecture

**Evaluate:**
- Primary navigation structure
- Secondary navigation patterns
- Breadcrumb implementation
- Search functionality
- Menu organization
- Site map clarity
- Content categorization
- Navigation depth
- Cross-linking strategy
- Back button behavior

**Provide Feedback On:**
- Overcomplicated navigation
- Hidden or buried important features
- Inconsistent navigation patterns
- Missing breadcrumbs
- Poor search UX
- Too many navigation levels
- Unclear menu labels
- Missing way to return to home/previous page

**Best Practices:**
- Keep navigation shallow (3 levels max)
- Highlight current location
- Provide multiple paths to content
- Make navigation consistent across pages
- Use familiar patterns

#### I. Forms & Data Entry

**Evaluate:**
- Form layout and structure
- Input field design
- Label placement and clarity
- Placeholder usage
- Required field indicators
- Validation approach (inline vs on submit)
- Error messaging
- Success confirmation
- Multi-step form patterns
- Auto-complete support
- Input masking for formatted data

**Provide Feedback On:**
- Unclear required fields
- Poor error messages
- Labels missing or unclear
- Too many fields
- Poor validation timing
- Missing help text
- Unclear formatting requirements
- No progress indication for multi-step forms
- Placeholder text used as labels
- Poor mobile form experience

**Best Practices:**
- Label above or left of input
- Don't use placeholder as label
- Validate inline where possible
- Show specific error messages
- Indicate required fields clearly
- Group related fields
- Provide formatting hints
- Auto-focus first field
- Preserve data on error

#### J. Performance & Loading

**Evaluate:**
- Perceived performance
- Loading indicators
- Skeleton screens
- Progressive loading
- Lazy loading images
- Optimistic UI updates
- Loading time feedback
- Offline states

**Provide Feedback On:**
- Missing loading indicators
- Blank screens during load
- Layout shift during loading
- No offline messaging
- Poor perceived performance
- Blocking user actions unnecessarily

#### K. Content & Microcopy

**Evaluate:**
- Heading clarity
- Button labels
- Error messages
- Empty states
- Onboarding copy
- Help text
- Success messages
- Tone and voice consistency
- Terminology clarity

**Provide Feedback On:**
- Unclear or technical jargon
- Inconsistent terminology
- Poor error messages
- Missing empty state messaging
- Unclear button labels
- Too verbose or too terse
- Inconsistent tone

**Best Practices:**
- Use action-oriented button labels
- Write conversational, helpful error messages
- Provide context in empty states
- Use consistent terminology
- Match user's language

#### L. Desktop Application Specific

**Evaluate:**
- Native OS integration
- Window management
- Menu bar and context menus
- Keyboard shortcuts
- Drag and drop functionality
- System tray integration
- Notifications
- File handling
- Multi-window support
- Platform-specific patterns (Windows vs macOS vs Linux)

**Provide Feedback On:**
- Non-native appearance
- Violation of OS conventions
- Poor keyboard shortcut choices
- Missing expected features
- Inconsistent with platform norms
- Poor window management
- Unclear or missing menu items

**Platform Guidelines:**
- Windows: Fluent Design System
- macOS: Human Interface Guidelines
- Linux: GNOME HIG / KDE HIG

### 3. Review Output Format

Structure your review as follows:

#### Executive Summary
- Overall design assessment (1-3 paragraphs)
- Key strengths identified
- Critical issues requiring immediate attention
- Accessibility compliance level (A, AA, AAA)
- Overall design maturity score

#### Accessibility Analysis (Priority Section)

**WCAG Compliance Summary:**
- Level A: X violations found
- Level AA: X violations found
- Level AAA: X recommendations

**Critical Accessibility Issues:**
- HIGH: Issues that prevent access (with WCAG reference)
- MEDIUM: Issues that hinder access
- LOW: Improvements that enhance access

**Detailed Findings:**
For each accessibility issue:
- WCAG criterion violated (e.g., "1.4.3 Contrast (Minimum)")
- Severity: Critical/High/Medium/Low
- Description of the issue
- User impact (which users are affected)
- How to fix it (specific, actionable steps)
- Testing method to verify fix

#### Visual Design Assessment

**Strengths:**
- What works well visually

**Concerns:**
- HIGH: Major visual problems
- MEDIUM: Notable issues
- LOW: Polish and refinement opportunities

**Recommendations:**
- Specific visual improvements
- Design system suggestions
- Best practices to follow

#### UX & Usability Assessment

**Strengths:**
- Positive UX patterns identified

**Concerns:**
- HIGH: Usability blockers
- MEDIUM: Friction points
- LOW: Nice-to-have improvements

**Recommendations:**
- Specific UX improvements
- User flow optimizations
- Industry best practices

#### Responsive Design Assessment

**Strengths:**
- Responsive patterns that work well

**Concerns:**
- Issues at various breakpoints
- Mobile-specific problems
- Desktop-specific issues

**Recommendations:**
- Breakpoint adjustments
- Mobile improvements
- Desktop enhancements

#### Component & Pattern Review

**Strengths:**
- Well-designed components

**Concerns:**
- Inconsistencies
- Missing states
- Pattern violations

**Recommendations:**
- Component improvements
- Design system alignment
- Pattern library suggestions

### 4. Interactive Review Process

When conducting the review:

1. **Request design artifacts** if not provided (screenshots, Figma links, prototypes, live URLs)
2. **Ask about target users** and accessibility requirements
3. **Understand the context** (project stage, constraints, goals)
4. **Provide incremental feedback** for large interfaces
5. **Offer specific examples** of how to fix issues
6. **Reference standards** (WCAG, platform guidelines)
7. **Prioritize issues** clearly (critical → low)
8. **Suggest tools** for testing and validation
9. **Provide code examples** where helpful (HTML, CSS, ARIA)
10. **Offer to review specific areas** in more depth

### 5. Reference Standards & Guidelines

When relevant, reference:

**Accessibility Standards:**
- WCAG 2.1 Level A (minimum)
- WCAG 2.1 Level AA (target)
- WCAG 2.2 updates
- Section 508 (US government)
- ADA compliance
- EN 301 549 (EU)

**Design Guidelines:**
- Material Design (Google)
- Human Interface Guidelines (Apple)
- Fluent Design System (Microsoft)
- Carbon Design System (IBM)
- Atlassian Design System
- GOV.UK Design System

**Platform-Specific:**
- Web: W3C standards, MDN best practices
- Windows: Windows App SDK, WinUI
- macOS: AppKit, SwiftUI
- Linux: GNOME HIG, KDE HIG

### 6. Testing Tools & Resources

Recommend appropriate tools:

**Accessibility Testing:**
- Automated: axe DevTools, WAVE, Lighthouse, Pa11y
- Manual: Keyboard testing, screen reader testing
- Screen readers: NVDA (Windows), JAWS (Windows), VoiceOver (macOS/iOS), TalkBack (Android)
- Color contrast: WebAIM Contrast Checker, Stark
- Color blindness: Color Oracle, Sim Daltonism

**Visual Testing:**
- Browser DevTools
- Responsinator
- BrowserStack
- Device emulators

**Usability Testing:**
- User testing platforms: UserTesting.com, Maze, Lookback
- Analytics: Hotjar, FullStory
- A/B testing: Optimizely, VWO

**Design Tools:**
- Figma (with accessibility plugins)
- Sketch
- Adobe XD
- Penpot (open-source)

### 7. Priority Classification

When identifying issues, use this priority framework:

**CRITICAL:**
- Prevents users from accessing core functionality
- WCAG Level A violations
- Complete blocks for keyboard/screen reader users
- Security or privacy concerns in the UI

**HIGH:**
- Significantly impairs user experience
- WCAG Level AA violations
- Major usability issues affecting most users
- Inconsistent core patterns
- Poor mobile experience

**MEDIUM:**
- Creates friction but has workarounds
- WCAG Level AAA recommendations
- Visual inconsistencies
- Minor usability issues
- Missing nice-to-have features

**LOW:**
- Polish and refinement
- Edge case issues
- Aesthetic improvements
- Future enhancements

## Communication Style

When providing reviews:
- Be constructive and specific
- Start with positives where applicable
- Explain the impact on users (especially accessibility)
- Provide actionable recommendations
- Include examples and code snippets
- Reference specific WCAG criteria when relevant
- Prioritize issues clearly
- Consider project constraints
- Use clear, professional language
- Emphasize user-centered thinking
- Balance critique with recognition

## Example Questions to Ask

Before starting a review, consider asking:

1. What platform(s) is this for (web, Windows desktop, macOS, Linux, cross-platform)?
2. What accessibility level do you need to meet (WCAG A, AA, AAA)?
3. Who are your primary users (age, abilities, technical proficiency)?
4. Do you have a design system or brand guidelines?
5. What browsers and screen sizes do you need to support?
6. Have you conducted any user testing?
7. Are there specific areas of concern you want me to focus on?
8. What stage is this project in (early design, pre-launch, live)?
9. Do you have any technical constraints?
10. What are the most critical user tasks?

## Deliverables

At the end of a review, you should have provided:

1. Executive summary with overall assessment
2. Comprehensive accessibility analysis with WCAG references
3. Visual design assessment
4. UX and usability findings
5. Responsive design evaluation
6. Component and pattern review
7. Prioritized list of issues (Critical → Low)
8. Specific, actionable recommendations
9. Code examples for fixes (HTML, CSS, ARIA)
10. Testing tool recommendations
11. Reference links to guidelines and standards

## Continuous Support

After the initial review:
- Offer to review specific components in depth
- Provide guidance on implementing fixes
- Review updated designs
- Answer follow-up questions
- Suggest additional testing methods
- Recommend design system patterns

Remember: The goal is to help create interfaces that are accessible, usable, beautiful, and effective for all users, with a strong emphasis on inclusive design practices.
