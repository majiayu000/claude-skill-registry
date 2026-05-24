---
name: guiding-users
description: Implements onboarding and help systems including product tours, interactive tutorials, tooltips, checklists, help panels, and progressive disclosure patterns. Use when building first-time experiences, feature discovery, guided walkthroughs, contextual help, setup flows, or user activation features. Provides timing strategies, accessibility patterns (keyboard, screen readers, reduced motion), and metrics for measuring onboarding success.
---

# Guiding Users Through Onboarding and Help Systems

## Purpose

This skill provides systematic patterns for onboarding users and delivering contextual help, from first-time product tours to ongoing feature discovery. It covers the complete spectrum of user guidance mechanisms, ensuring optimal user activation, feature adoption, and self-service support.

## When to Use

Activate this skill when:
- Building first-time user experiences or product tours
- Implementing feature discovery and announcements
- Creating interactive tutorials or guided tasks
- Adding tooltips, hints, or contextual help
- Designing setup flows or completion checklists
- Building help panels or documentation systems
- Implementing progressive disclosure patterns
- Measuring onboarding effectiveness and user activation
- Ensuring onboarding accessibility

## Quick Decision Framework

Select the appropriate guidance mechanism based on user state and content type:

```
First-time user          → Product Tour (step-by-step)
New feature launch       → Feature Spotlight (tooltip + animation)
Complex workflow         → Interactive Tutorial (guided tasks)
Account setup            → Checklist (progress tracking)
Contextual help needed   → Tooltip/Hint system
Ongoing support          → Help Panel (sidebar/searchable)
Feature unlock           → Progressive Disclosure
```

Reference `references/selection-framework.md` for detailed selection criteria.

## Core Guidance Mechanisms

### Product Tours

Step-by-step walkthroughs that guide users through key features:
- Sequential spotlights with modal overlays
- Progress indicators (Step 2 of 5)
- Skip, Previous, and Next controls
- Dismiss and resume capability
- Context-sensitive activation

**Implementation:**
```bash
npm install react-joyride
```

See `examples/first-time-tour.tsx` for complete implementation.
Reference `references/product-tours.md` for patterns and best practices.

### Feature Spotlights

Announce new features to existing users:
- Pulsing hotspot animations
- Contextual tooltip with arrow
- "Got it" acknowledgment
- Auto-dismiss after first view
- Non-blocking overlay

See `examples/feature-spotlight.tsx` for implementation.
Reference `references/tooltips-hints.md` for patterns.

### Interactive Tutorials

Guided task completion with validation:
- "Complete these tasks to get started"
- Checkbox completion tracking
- Celebration animations on completion
- Sandbox mode with sample data
- Undo and reset capabilities

See `examples/guided-tutorial.tsx` for implementation.
Reference `references/interactive-tutorials.md` for patterns.

### Setup Checklists

Track multi-step onboarding progress:
- Visual progress indicators (3/4 complete)
- Direct links to each task
- Profile completion percentages
- Achievement badges and gamification
- Persistent until completed

See `examples/setup-checklist.tsx` for implementation.
Reference `references/checklists.md` for patterns.

### Contextual Tooltips and Hints

Just-in-time help when users need it:
- Hover or click-triggered tooltips
- Progressive hint levels (1, 2, 3)
- "Need help?" assistance triggers
- Context-aware suggestions
- Keyboard-accessible

See `examples/contextual-help.tsx` for implementation.
Reference `references/tooltips-hints.md` for complete patterns.

### Help Panels

Comprehensive help systems:
- Sidebar or drawer interface
- Contextual help based on current page
- Search help articles and docs
- Video tutorials and demos
- Contact support integration
- Collapsible and resizable

See `examples/help-panel.tsx` for implementation.
Reference `references/help-systems.md` for patterns.

## Timing and Triggering Strategies

### When to Show Onboarding

Appropriate triggers:
- First login (always)
- Immediately after signup
- New feature launch (to existing users)
- User appears stuck (smart triggering based on inactivity)
- User explicitly requests help

### When NOT to Show Onboarding

Avoid showing when:
- User is mid-task or focused
- Shown in every session (becomes annoying)
- Before allowing free exploration
- Tour exceeds 7 steps (too long)
- User already dismissed or completed

**Auto-dismiss timing:**
- Simple tooltips: 5-7 seconds
- Feature announcements: 10-15 seconds or manual dismiss
- Tours: User-controlled, no auto-dismiss
- Persistent hints: Until user acknowledges

Reference `references/timing-strategies.md` for detailed guidelines.

## Progressive Disclosure Patterns

Show only what's needed, when it's needed:

**Techniques:**
1. **Accordion Help**: Collapsed by default, expand for details
2. **"Learn More" Links**: Deep dive content optional
3. **Advanced Settings**: Hidden behind "Show advanced" toggle
4. **Gradual Feature Introduction**: Unlock features as user progresses
5. **Contextual Hints**: Show based on user actions

Reference `references/progressive-disclosure.md` for implementation patterns.

## Accessibility Requirements

### Keyboard Navigation

Essential keyboard support:
- Tab through tour steps and controls
- ESC to dismiss tours and tooltips
- Arrow keys for Previous/Next navigation
- Enter/Space to activate buttons
- Focus visible indicators

### Screen Reader Support

ARIA patterns for announcements:
- Announce step number and total (Step 2 of 5)
- Read tooltip and help content
- Describe highlighted UI elements
- Announce progress completion
- Alert on errors or blockers

### Reduced Motion

Respect `prefers-reduced-motion`:
- Disable pulsing animations
- Use instant transitions instead of animations
- Remove parallax and complex effects
- Maintain functionality without motion

To validate accessibility:
```bash
node scripts/validate_accessibility.js
```

Reference `references/accessibility-patterns.md` for complete implementation.

## Library Recommendations

### Primary: react-joyride (Feature-Rich, Accessible)

**Library:** `/gilbarbara/react-joyride`
**Trust Score:** 9.6/10
**Code Snippets:** 29+

Best for comprehensive product tours:
- WAI-ARIA compliant out of the box
- Full keyboard navigation support
- Highly customizable styling
- Programmatic control
- Localization support
- Active maintenance

```bash
npm install react-joyride
```

See `examples/joyride-tour.tsx` for complete setup.

### Alternative: driver.js (Lightweight, Modern)

Best for minimal bundle size:
- Vanilla JavaScript (framework agnostic)
- ~5KB gzipped
- Modern API design
- No dependencies

```bash
npm install driver.js
```

### Alternative: intro.js (Classic, Proven)

Best for traditional tours:
- Battle-tested library
- Wide browser support
- JSON-based tour configuration
- Extensive plugin ecosystem

```bash
npm install intro.js
```

Reference `references/library-comparison.md` for detailed analysis and selection criteria.

## Design Token Integration

All onboarding components use the design-tokens skill for consistent theming:

**Token categories used:**
- **Colors**: Tour spotlight, overlay, tooltip backgrounds, hotspot colors
- **Spacing**: Tour padding, tooltip spacing, arrow size
- **Typography**: Title sizes, body text, help content
- **Borders**: Border radius for modals and tooltips
- **Shadows**: Elevation for tour spotlights and tooltips
- **Motion**: Transition durations, pulse animations

Supports light, dark, high-contrast, and custom brand themes.
Reference the design-tokens skill for complete theming documentation.

## Measuring Success

### Key Metrics

Track these indicators:
- Tour completion rate (target: >60%)
- Time to first value (faster = better)
- Feature adoption rate post-tour
- Support ticket reduction
- User activation rate (completed key actions)
- Drop-off points in tours

### Optimization Strategies

Iterate based on data:
- A/B test tour length (shorter often better)
- Test different messaging and copy
- Measure drop-off at each step
- Simplify steps with high abandonment
- Add skip options for returning users
- Personalize based on user type

To analyze onboarding metrics:
```bash
python scripts/analyze_onboarding_metrics.py
```

Reference `references/measuring-success.md` for complete analytics implementation.

## Anti-Patterns to Avoid

Common mistakes that harm user experience:

❌ **Forced Tours**: Requiring tour completion before product use
❌ **Too Long**: Tours exceeding 7 steps lose user attention
❌ **Every Session**: Showing same tour repeatedly
❌ **No Skip Option**: Preventing users from exploring independently
❌ **Wall of Text**: Using lengthy explanations instead of visuals
❌ **Blocking Everything**: Preventing interaction during tours
❌ **Premature Guidance**: Showing help before users explore
❌ **Poor Timing**: Interrupting focused work
❌ **No Context**: Generic tips without specific relevance

## Implementation Workflow

### Step 1: Map User Journey

Identify key moments:
1. First login and account creation
2. Core value delivery (aha moment)
3. Feature discovery points
4. Potential confusion or abandonment
5. Achievement and progress milestones

### Step 2: Choose Guidance Mechanisms

Match mechanisms to moments:
- First login → Product tour (3-5 steps max)
- Core features → Interactive tutorial
- Setup requirements → Checklist
- New features → Spotlight + tooltip
- Ongoing help → Help panel

### Step 3: Implement with Progressive Enhancement

Build incrementally:
1. Start with essential guidance only
2. Add contextual help based on user behavior
3. Implement analytics to measure effectiveness
4. Iterate based on data
5. A/B test variations

### Step 4: Test Accessibility

Verify compliance:
- Keyboard navigation works completely
- Screen reader announces properly
- Reduced motion preference honored
- Focus management correct
- ARIA labels descriptive

Run validation:
```bash
node scripts/validate_accessibility.js
```

### Step 5: Monitor and Optimize

Track and improve:
- Monitor completion rates
- Identify drop-off points
- Gather user feedback
- A/B test improvements
- Update based on findings

## Working Examples

Start with the example matching the use case:

```
first-time-tour.tsx           # Product walkthrough with react-joyride
feature-spotlight.tsx         # New feature announcement
guided-tutorial.tsx           # Interactive task completion
setup-checklist.tsx           # Multi-step onboarding progress
contextual-help.tsx           # Tooltips and progressive hints
help-panel.tsx                # Sidebar help with search
celebration-animation.tsx     # Completion feedback
```

## Resources

### Scripts (Token-Free Execution)
- `scripts/generate_tour_config.js` - Generate tour configurations from user flows
- `scripts/analyze_onboarding_metrics.py` - Analyze completion and drop-off rates
- `scripts/validate_accessibility.js` - Test keyboard and screen reader support

### References (Detailed Documentation)
- `references/product-tours.md` - Tour patterns, step design, navigation
- `references/interactive-tutorials.md` - Guided tasks and sandbox modes
- `references/tooltips-hints.md` - Contextual help and progressive hints
- `references/checklists.md` - Progress tracking and gamification
- `references/help-systems.md` - Help panels, videos, and documentation
- `references/progressive-disclosure.md` - Advanced patterns and feature unlocking
- `references/timing-strategies.md` - When and how to trigger guidance
- `references/accessibility-patterns.md` - WCAG compliance and ARIA patterns
- `references/measuring-success.md` - Analytics and optimization
- `references/library-comparison.md` - Detailed library evaluation
- `references/selection-framework.md` - Decision trees for choosing mechanisms

### Examples (Implementation Code)
- Complete working implementations for all guidance types
- Integration examples with common frameworks
- Accessibility-compliant patterns
- Design token integration examples

### Assets (Templates and Configs)
- `assets/celebration-animations/` - Success animations and confetti
- `assets/tour-templates.json` - Reusable tour configurations
- `assets/message-templates.json` - Tooltip and hint copy templates
- `assets/timing-config.json` - Recommended timing values

## Cross-Skill Integration

This skill works with other component skills:

- **Forms**: Guided form completion, validation hints
- **Dashboards**: Feature tours, widget explanations
- **Tables**: Data grid tutorials, feature discovery
- **AI Chat**: Chat interface walkthroughs
- **Navigation**: Menu and navigation guidance
- **Feedback**: Success celebrations, progress notifications
- **Design Tokens**: All visual styling and theming

## Key Principles

1. **Respect User Time**: Keep tours under 7 steps, make skippable
2. **Show, Don't Tell**: Use visuals and interactions over text
3. **Progressive Enhancement**: Start simple, add guidance as needed
4. **Context is King**: Show help when and where it's relevant
5. **Measure Everything**: Track completion, iterate based on data
6. **Accessibility First**: Keyboard, screen reader, reduced motion support
7. **Celebrate Progress**: Acknowledge completion and achievements
8. **Allow Exploration**: Don't force tours, enable discovery

## Next Steps

1. Map the user journey and identify key moments
2. Choose appropriate guidance mechanisms for each moment
3. Install react-joyride or preferred library
4. Start with one critical flow (usually first-time experience)
5. Implement with accessibility built-in
6. Add analytics tracking
7. Test with real users
8. Iterate based on metrics and feedback
