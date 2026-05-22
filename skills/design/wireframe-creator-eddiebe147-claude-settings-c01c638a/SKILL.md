---
name: Wireframe Creator
slug: wireframe-creator
description: Create low-fidelity wireframes for rapid prototyping
category: design
complexity: simple
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "create wireframe"
  - "wireframe"
  - "low-fi mockup"
  - "sketch layout"
  - "prototype structure"
tags:
  - wireframes
  - prototyping
  - UX
  - design
---

# Wireframe Creator

A UX design expert that creates low-fidelity wireframes for rapid prototyping and iteration. This skill focuses on structure, hierarchy, and user flow without the distraction of visual design, enabling quick validation of concepts before investing in high-fidelity design.

Whether you need a quick sketch of a landing page, a complete user flow for an app, or a dashboard layout, this skill produces clear, annotated wireframes that communicate information architecture and interaction patterns.

## Core Workflows

### Workflow 1: Website/Landing Page Wireframe
1. **Define page structure**
   - Header/navigation
   - Hero section
   - Content sections
   - Footer

2. **Create ASCII wireframe**
   - Use boxes, lines, and text to represent layout
   - Show hierarchy with spacing and sizing
   - Indicate interactive elements
   - Label all components

3. **Add annotations**
   - Content descriptions
   - Interaction notes
   - Responsive behavior
   - Priority markers

4. **Define user flow**
   - Entry points
   - CTAs and paths
   - Exit points

5. **Provide next steps**
   - Content requirements
   - Design considerations
   - Development notes

### Workflow 2: App Screen Wireframes
1. **Map user journey**
   - List all screens needed
   - Define flow between screens
   - Identify decision points

2. **Design each screen**
   - Navigation structure
   - Content placement
   - Interactive elements
   - States (empty, loading, error, success)

3. **Show connections**
   - Arrows indicating flow
   - Numbered steps
   - Decision trees

4. **Document interactions**
   - Tap/click actions
   - Swipe gestures
   - Long-press behaviors
   - Transitions

### Workflow 3: Dashboard Wireframe
1. **Define data hierarchy**
   - Most important metrics
   - Secondary information
   - Detail views
   - Filter/control placement

2. **Layout panels**
   - Primary content area
   - Sidebar navigation
   - Top bar utilities
   - Widget placement

3. **Design data visualizations**
   - Chart placeholders
   - Table structures
   - Card layouts
   - Empty states

4. **Plan interactions**
   - Drill-down flows
   - Filter behaviors
   - Export/actions
   - Refresh patterns

### Workflow 4: User Flow Wireframes
1. **Map complete flow**
   - Start state
   - All decision points
   - Success paths
   - Error paths
   - End states

2. **Wireframe each step**
   - One screen per step
   - Show state changes
   - Indicate validation

3. **Connect flow**
   - Arrows between screens
   - Annotate triggers
   - Note conditional logic

4. **Document edge cases**
   - What if scenarios
   - Error handling
   - Validation feedback

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Landing page wireframe | "Wireframe a landing page for [product]" |
| App screen wireframe | "Create wireframe for [feature] screen" |
| User flow | "Map user flow for [task]" |
| Dashboard | "Wireframe dashboard for [use case]" |
| Form wireframe | "Design form for [purpose]" |
| Navigation | "Wireframe navigation for [site]" |

## Wireframe Elements Library

### Layout Components
```
+----------------------------------+
|           HEADER                 |
| [Logo]    [Nav] [Nav] [Nav] [CTA]|
+----------------------------------+

+----------------------------------+
|         HERO SECTION             |
|                                  |
|   [Headline]                     |
|   [Subheading]                   |
|   [CTA Button]                   |
|                                  |
+----------------------------------+

+-------+  +-------+  +-------+
|       |  |       |  |       |
| Card  |  | Card  |  | Card  |
|       |  |       |  |       |
+-------+  +-------+  +-------+

+----------------------------------+
|           FOOTER                 |
| [Links] [Links] [Social] [Legal] |
+----------------------------------+
```

### Form Elements
```
[Input Field Label]
[___________________]

[Dropdown Label]
[Select ▼]

[Radio Options]
( ) Option 1
( ) Option 2
(•) Option 3

[Checkbox Options]
[✓] Option A
[ ] Option B
[✓] Option C

[Text Area]
[                    ]
[                    ]
[                    ]

[Button]  [Secondary Button]
```

### Navigation Patterns
```
Horizontal Nav:
[Logo] [Link] [Link] [Link] [Link] [Button]

Sidebar Nav:
+--------+
| [Logo] |
|        |
| [Nav]  |
| [Nav]  |
| [Nav]  |
| [Nav]  |
+--------+

Hamburger Nav (Mobile):
[☰] [Logo]          [🔍][👤]

Tabs:
[Active Tab] [Tab] [Tab] [Tab]
─────────────────────────────
```

### Data Display
```
Table:
+--------+----------+--------+
| Header | Header   | Header |
+--------+----------+--------+
| Cell   | Cell     | Cell   |
| Cell   | Cell     | Cell   |
+--------+----------+--------+

Card Grid:
+-------+  +-------+  +-------+
|[IMG]  |  |[IMG]  |  |[IMG]  |
| Title |  | Title |  | Title |
| Text  |  | Text  |  | Text  |
| [Link]|  | [Link]|  | [Link]|
+-------+  +-------+  +-------+

List:
• Item with icon
• Item with icon
• Item with icon
```

## Annotation Symbols

```
[Component Name] - Placeholder for element
(...) - Truncated/overflow content
[IMG] - Image placeholder
[LOGO] - Logo placement
[CTA] - Call to action button
[---] - Divider/separator
→ - User flow direction
* - Important note
? - Decision point
! - Error/warning state
✓ - Success state
```

## Wireframe Best Practices

- **Keep it low-fidelity**: Resist urge to add visual polish
- **Focus on structure**: Hierarchy and layout, not colors/fonts
- **Use real content**: Actual text, not lorem ipsum when possible
- **Show states**: Empty, loading, error, success for each component
- **Annotate heavily**: Explain interactions, behaviors, constraints
- **Think mobile-first**: Start with smallest screen
- **Number elements**: Make annotations easy to reference
- **Use consistent spacing**: Visual rhythm even in wireframes
- **Indicate content types**: [Headline], [Body text], [Button label]
- **Show all interactions**: Hovers, clicks, swipes, gestures
- **Document edge cases**: What happens when things go wrong
- **Keep it simple**: Boxes, lines, and labels are enough

## Common Patterns

### Landing Page Structure
```
1. Header (sticky)
   - Logo + Navigation + CTA

2. Hero (above fold)
   - Headline + Subheading + CTA + Visual

3. Social Proof
   - Logos or testimonials

4. Features (3-column)
   - Icon + Headline + Description × 3

5. How It Works (stepped)
   - Step 1, Step 2, Step 3 with visuals

6. Pricing (table or cards)
   - 3 tiers with features listed

7. Final CTA
   - Headline + Button + Trust signals

8. Footer
   - Links, social, legal
```

### Dashboard Layout
```
+-----+---------------------------+
| Nav | Top Bar [Search] [User]   |
| [L] +---------------------------+
| [I] |                           |
| [N] |     Main Content          |
| [K] |     (Charts, Tables)      |
| [S] |                           |
|     |                           |
+-----+---------------------------+
```

### Form Flow
```
Step 1: Basic Info
[Name Input]
[Email Input]
[Next Button]
  ↓
Step 2: Details
[Multiple fields]
[Back] [Next]
  ↓
Step 3: Confirmation
[Review info]
[Edit] [Submit]
  ↓
Success State
[✓] Thank you message
[Next action]
```

## Deliverables Format

```
WIREFRAME SPECIFICATION
Project: [Name]
Page/Screen: [Landing Page / Dashboard / etc.]
Date: [Date]

USER FLOW
Entry → Action → Result → Next Step

WIREFRAME
[ASCII diagram of layout]

COMPONENTS

1. Header
   - Height: 64px
   - Elements: Logo (left), Nav (center), CTA (right)
   - Behavior: Sticky on scroll
   - Mobile: Collapses to hamburger menu

2. Hero Section
   - Height: 100vh
   - Layout: 60% text (left), 40% image (right)
   - Elements:
     * H1 headline (max 60 chars)
     * Subheading (max 120 chars)
     * Primary CTA button
     * Secondary CTA link
   - Responsive: Stacks vertically on mobile

3. Feature Cards
   - Layout: 3-column grid
   - Card structure:
     * Icon (top)
     * Headline (h3)
     * Description (2-3 lines)
     * Optional link
   - Responsive: 1 column mobile, 2 tablet, 3 desktop

[... more components ...]

INTERACTIONS

Hover States:
- Nav links: Underline
- Buttons: Darken background
- Cards: Lift shadow

Click Actions:
- Primary CTA → Opens signup form
- Feature cards → Expands details
- Nav links → Smooth scroll to section

CONTENT REQUIREMENTS

Copy Needed:
- [ ] H1 headline (max 60 characters)
- [ ] Subheading (max 120 characters)
- [ ] 3 feature headlines
- [ ] 3 feature descriptions
- [ ] CTA button text

Images Needed:
- [ ] Hero image (1600x900px)
- [ ] 3 feature icons (SVG)
- [ ] Logo (SVG, white and color versions)

RESPONSIVE BREAKPOINTS

Mobile (<768px):
- Single column layout
- Hamburger navigation
- Stacked hero content
- Larger touch targets (min 44px)

Tablet (768-1024px):
- 2-column feature grid
- Partial navigation visible
- Balanced hero layout

Desktop (>1024px):
- Full layout as wireframed
- All navigation visible
- Multi-column grids

STATES

Default: As shown in wireframe
Loading: Show skeleton placeholders
Error: Display error message with retry option
Empty: Show empty state with CTA
Success: Show confirmation message

NOTES
- Prioritize above-fold content
- Ensure clear CTA visibility
- Test mobile interaction zones
- Consider accessibility (focus states, screen readers)
- Plan for content that may overflow
```

## Tools Integration

- Use **layout-designer** skill for detailed grid specifications
- Use **ui-builder** skill to convert wireframes to code
- Use **Midjourney** to generate visual design from wireframes
- Use **Playwright** to test wireframe interactions

## Wireframe Fidelity Levels

**Low-Fidelity** (this skill)
- Boxes and lines
- Grayscale
- Placeholder content
- Focus: Structure
- Speed: Very fast
- Use: Early ideation, quick iteration

**Mid-Fidelity**
- More refined shapes
- Some real content
- Basic interactions shown
- Focus: Layout + content
- Speed: Moderate
- Use: Stakeholder reviews, user testing

**High-Fidelity**
- Visual design applied
- Real content
- Interactive prototype
- Focus: Final design
- Speed: Slower
- Use: Developer handoff, final approval

## Common Requests

**E-commerce product page**: Hero image + details + CTA + related products
**SaaS signup flow**: Multi-step form with progress indicator
**Blog homepage**: Featured post + grid of articles + sidebar
**Mobile app onboarding**: 3-4 swipeable screens + skip/next
**Admin dashboard**: Sidebar nav + metric cards + data tables
**Profile page**: Header + tabs + content sections
