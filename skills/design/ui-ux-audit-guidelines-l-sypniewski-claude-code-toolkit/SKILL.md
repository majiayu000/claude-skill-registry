---
name: ui-ux-audit-guidelines
description: 'Professional UI/UX audit methodology and design vocabulary. Use when:
  conducting UI/UX audits, evaluating visual hierarchy, analyzing responsive design,
  assessing interaction patterns. Do NOT use for:'
---

---
name: ui-ux-audit-guidelines
description: Professional UI/UX audit methodology and design vocabulary. Use when: conducting UI/UX audits, evaluating visual hierarchy, analyzing responsive design, assessing interaction patterns. Do NOT use for: code reviews, accessibility audits (WCAG), performance analysis, or security assessments.
---

# UI/UX Audit Guidelines

This skill provides professional UI/UX audit methodology and evaluation criteria for comprehensive visual and interaction analysis.

## Audit Viewports

Standard viewport configurations for responsive testing:

### Mobile
- **428×926** - Large phone (iPhone 14 Pro Max equivalent)

### Tablets
- **768×1024** - Portrait orientation (iPad portrait)
- **1024×768** - Landscape orientation (iPad landscape)

### Desktop
- **1160×720** - Small desktop/laptop
- **1920×1080** - Large desktop (Full HD)

## Evaluation Categories

### 1. Visual Hierarchy and Typography

**Issues to identify:**
- Unclear heading hierarchy (inconsistent size progression)
- Poor typographic scale (jumps between sizes too large/small)
- Insufficient weight contrast between headings and body
- Competing visual elements without clear focal points
- Inconsistent font families or weights

**Terminology:**
- Typographic scale, visual weight, font pairing
- Heading hierarchy, body text readability
- Line height (leading), letter spacing (tracking)
- Measure (line length), orphans and widows

### 2. Spacing and Layout

**Issues to identify:**
- Inconsistent vertical rhythm (varying spacing between elements)
- Irregular horizontal gutters
- Unbalanced whitespace distribution
- Overcrowded or overly sparse layouts
- Misaligned elements within the same context

**Terminology:**
- Padding, margin, gutter
- Vertical rhythm, baseline grid
- Breathing room, visual density
- Proximity principle, grouping

### 3. Grid and Alignment

**Issues to identify:**
- Elements breaking out of grid structure
- Inconsistent column spans
- Poor edge alignment between related elements
- Uneven container widths
- Misaligned form labels and inputs

**Terminology:**
- Grid system, column structure
- Edge alignment, center alignment
- Baseline alignment, optical alignment
- Proportional structure, golden ratio

### 4. Color and Contrast

**Issues to identify:**
- Insufficient text-to-background contrast (WCAG compliance)
- Unbalanced color weight distribution
- Overuse of accent colors
- Inconsistent color application across similar elements
- Poor use of color for state indication

**Terminology:**
- Contrast ratio, color weight
- Primary, secondary, accent colors
- Color temperature, saturation balance
- Semantic color usage

### 5. Navigation and Wayfinding

**Issues to identify:**
- Unclear active/current state indicators
- Poor discoverability of navigation elements
- Ambiguous or overly technical labeling
- Inconsistent navigation patterns across pages
- Missing breadcrumbs or context indicators

**Terminology:**
- Navigation hierarchy, active states
- Discoverability, affordance
- Information scent, wayfinding cues
- Progressive disclosure

### 6. Component Affordance and Interaction

**Issues to identify:**
- Buttons that don't look clickable
- Links that look like plain text
- Form elements with unclear boundaries
- Missing or weak hover/focus states
- Ambiguous interactive elements

**Terminology:**
- Affordance, signifiers
- Perceived affordance, learned affordance
- Interactive cues, click targets
- Touch target size, tap zones

### 7. Feedback States

**Issues to identify:**
- Missing hover states
- Unclear focus indicators
- No visual feedback for active/pressed states
- Missing disabled state styling
- Absent or inadequate loading indicators

**Terminology:**
- Hover state, focus ring, active state
- Disabled state, loading state
- Pressed state, selected state
- State transitions, micro-feedback

### 8. Dialog and Modal Behavior

**Issues to identify:**
- Modals not centered or poorly positioned
- Missing or broken backdrop/overlay
- No focus trap (can tab outside modal)
- Scroll not locked on body
- Missing close button or escape key handling
- Jarring or missing transitions

**Terminology:**
- Modal positioning, overlay opacity
- Focus trap, focus management
- Scroll lock, body scroll prevention
- Entry/exit transitions

### 9. Responsive Adaptation

**Issues to identify:**
- Content overflow at breakpoints
- Horizontal scrolling on mobile
- Touch targets too small on mobile
- Inappropriate layout patterns for viewport size
- Hidden content without proper disclosure

**Terminology:**
- Breakpoints, fluid layout
- Content reflow, stack order
- Mobile-first, responsive patterns
- Adaptive vs responsive design

### 10. Cross-Page Consistency

**Issues to identify:**
- Component styling variations between pages
- Inconsistent spacing scale usage
- Different typography treatment for same element types
- Color inconsistencies
- Varying interaction patterns

**Terminology:**
- Design system adherence
- Component consistency
- Pattern library compliance
- Visual language unity

### 11. Empty and Error States

**Issues to identify:**
- Generic or missing empty states
- Unhelpful zero-data views
- Missing first-time user guidance
- Unclear error messages
- No recovery path from errors

**Terminology:**
- Empty state design
- Zero-data state, blank slate
- Onboarding patterns
- Error recovery, graceful degradation

### 12. Loading Experiences

**Issues to identify:**
- No loading indication
- Jarring content jumps when loaded
- Inappropriate spinner vs skeleton usage
- Poor perceived performance
- Missing progress indicators for long operations

**Terminology:**
- Loading skeletons, shimmer effects
- Spinners, progress indicators
- Perceived performance
- Optimistic updates, lazy loading

### 13. Information Architecture

**Issues to identify:**
- Poor content grouping
- Unclear labeling or terminology
- High cognitive load from information density
- Missing or unclear section headers
- Illogical content ordering

**Terminology:**
- Information hierarchy
- Content grouping, chunking
- Cognitive load, mental models
- Labeling systems, taxonomy

### 14. Microinteractions and Transitions

**Issues to identify:**
- Missing subtle feedback animations
- Inconsistent animation timing/easing
- Jarring state changes without transitions
- Overuse of animation (distracting)
- Missing confirmation animations

**Terminology:**
- Microinteractions, motion design
- Easing curves, duration
- State transitions, animation choreography
- Feedback loops

### 15. Large Viewport Optimization

**Issues to identify:**
- Content stretching excessively on wide screens
- Oversized whitespace creating dead zones
- Tables or text blocks without max-width constraints
- Unused horizontal space
- Loss of visual hierarchy at scale

**Terminology:**
- Max-width constraints
- Content centering, container widths
- Widescreen optimization
- Layout scaling, proportional spacing

## Improvement Recommendations Format

When suggesting improvements, use professional design language:

### Good Examples
- "Establish a consistent 8px spacing scale across all components"
- "Increase heading weight differentiation (currently 500 vs 400, suggest 600 vs 400)"
- "Add subtle hover state transition (150ms ease-out) for all interactive elements"
- "Implement skeleton loading pattern for data-heavy sections"
- "Constrain content container to max-width of 1200px on large viewports"

### Avoid
- "Change the CSS to..."
- "Add padding: 16px to..."
- "Use display: flex..."
- "Modify the HTML structure..."

## Markdown Output Format

Structure audit findings per page, per viewport:

```markdown
# Page – [Page Name/URL]

## Viewport: [Width]×[Height] ([Device Type])

### Screenshot
[Screenshot or reference to captured screenshot]

### Issues Found

#### Visual Hierarchy
- [Issue description using professional terminology]

#### Spacing and Layout
- [Issue description]

#### [Other applicable categories...]

### Recommended Improvements

1. [Actionable design recommendation]
2. [Actionable design recommendation]
3. [Actionable design recommendation]

---
```

## Error State Simulation

Use Playwright route interception to simulate error states without destructive actions:

### Patterns to Simulate

| Scenario | Simulation Approach |
|----------|---------------------|
| API Failures | Intercept API routes and return 500 status code |
| Network Errors | Block specific endpoints to simulate offline state |
| Slow Loading | Add artificial delays to observe loading states |
| Empty Data | Return empty arrays/objects to test zero-data states |

**Note**: The skill file provides technical guidance for agents implementing these patterns via Playwright route interception APIs.

## Integration Points

Works with:
- `ui-ux-audit-orchestrator` agent for crawling and coordination
- `ui-ux-page-auditor` agent for individual page analysis
- `/ui-ux-audit` command to initiate audits
