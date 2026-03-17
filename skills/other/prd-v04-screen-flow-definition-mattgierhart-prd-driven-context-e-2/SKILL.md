---
name: prd-v04-screen-flow-definition
description: Connect user journeys to screens, defining the UI structure and navigation paths during PRD v0.4 User Journeys. Triggers on requests to define screens, design screen flows, map UI structure, plan navigation, or when user asks "what screens do we need?", "define screens", "screen flow", "UI structure", "information architecture", "navigation design", "wireframe planning". Consumes UJ- (User Journey Mapping), FEA- (Feature Value Planning), BR- (constraints). Outputs SCR- entries for screens and DES- entries for design system elements. Feeds v0.5 Red Team Review.
---

# Screen Flow Definition

Position in workflow: v0.4 User Journey Mapping → **v0.4 Screen Flow Definition** → v0.5 Red Team Review

Screens are where journeys become tangible. This skill transforms user journeys into a screen inventory with navigation paths and feature mappings.

## Screen Types

| Type | Definition | Design Priority | Example |
|------|------------|-----------------|---------|
| **Page** | Full viewport, primary navigation target | High | Dashboard, Settings |
| **Modal** | Overlay, blocks underlying page | Medium | Confirmation, Quick Edit |
| **Panel** | Slide-out, contextual detail | Medium | Detail View, Filters |
| **Component** | Reusable UI element | Varies | Header, Data Table |

**Rule**: Start with Pages, then identify where Modals/Panels reduce navigation friction.

## Navigation Patterns

Choose a pattern based on product type:

| Pattern | When to Use | Example Products |
|---------|-------------|------------------|
| **Hub & Spoke** | Dashboard-centric apps | Analytics, CRM |
| **Linear Flow** | Wizard/checkout processes | Onboarding, E-commerce |
| **Hierarchical** | Content-heavy apps | Documentation, CMS |
| **Flat** | Simple single-purpose apps | Timer, Calculator |

Most SaaS products use **Hub & Spoke** with occasional **Linear Flows** for onboarding/purchase.

## Mapping Process

1. **Pull UJ-** (journeys) and FEA- (features) from prior steps
   - Journeys define the paths; features define the capabilities

2. **Inventory unique screens** needed across all journeys
   - Walk through each journey step and ask: "What screen does this happen on?"

3. **Map features to screens** (many:many relationship)
   - One feature may appear on multiple screens
   - One screen may contain multiple features

4. **Define navigation structure**
   - How do users get from screen to screen?
   - What's the hierarchy? What's always accessible?

5. **Identify shared components**
   - Headers, footers, navigation bars
   - Common patterns: data tables, forms, cards

6. **Create SCR- entries** with journey and feature traceability

7. **Create DES- entries** for design system elements

## SCR- Output Template

```
SCR-XXX: [Screen Name]
Type: [Page | Modal | Panel | Component]
Purpose: [What user accomplishes on this screen]
Journeys: [UJ-XXX, UJ-YYY that use this screen]
Features: [FEA-XXX, FEA-YYY rendered on this screen]

Primary Actions: [Key user actions available]
Secondary Actions: [Less common but available actions]

Navigation:
  From: [SCR-XXX, SCR-YYY — how users arrive]
  To: [SCR-XXX, SCR-YYY — where users can go next]

Content:
  - [Data/element 1]
  - [Data/element 2]

Constraints: [BR-XXX rules affecting this screen]
Design Notes: [Persona-specific considerations from PER-]
```

**Example SCR- entry:**
```
SCR-001: Main Dashboard
Type: Page
Purpose: Central hub showing key metrics and quick actions
Journeys: UJ-001 (Step 4), UJ-002 (Step 5), UJ-003 (Step 1)
Features: FEA-007 (dashboard), FEA-003 (reports preview), FEA-012 (notifications)

Primary Actions: Create Report, View Data Sources, Access Settings
Secondary Actions: Invite Team, View Help

Navigation:
  From: SCR-000 (Login), any screen via nav bar
  To: SCR-002 (Report Builder), SCR-003 (Data Sources), SCR-010 (Settings)

Content:
  - Key metrics summary (3-5 cards)
  - Recent reports list
  - Data source health status
  - Notification bell

Constraints: BR-015 (data refresh rate), BR-020 (role-based visibility)
Design Notes: PER-001 needs "busy dashboard" - show progress at a glance
```

## DES- Output Template

```
DES-XXX: [Component/Pattern Name]
Type: [Component | Pattern | Layout]
Used In: [SCR-XXX, SCR-YYY]
Purpose: [What this element does]

States:
  - Default: [Normal state]
  - Loading: [When fetching data]
  - Empty: [No data state]
  - Error: [Error state]
  - Disabled: [When not interactive]

Variants: [If multiple versions exist]
Accessibility: [A11y considerations]
```

**Example DES- entry:**
```
DES-001: Data Card
Type: Component
Used In: SCR-001 (Dashboard), SCR-005 (Analytics)
Purpose: Display single metric with trend indicator

States:
  - Default: Shows value + trend arrow
  - Loading: Skeleton placeholder
  - Empty: "No data yet" message
  - Error: "Failed to load" with retry

Variants: Small (dashboard), Large (detail view)
Accessibility: ARIA labels for trend direction
```

## Screen Categories

Organize screens by function:

| Category | Examples | Design Priority |
|----------|----------|-----------------|
| **Entry Points** | Login, Landing, Signup | High (first impressions) |
| **Core Workflow** | Main task screens | High (value delivery) |
| **Settings/Admin** | Preferences, Account, Billing | Medium (necessary) |
| **Support/Help** | Docs, Contact, FAQ | Low (failure recovery) |

**Rule**: Invest design effort proportional to priority. Don't over-design settings screens.

## Feature-to-Screen Matrix

Create a mapping matrix:

| Feature | SCR-001 | SCR-002 | SCR-003 | SCR-004 |
|---------|---------|---------|---------|---------|
| FEA-001 (auto-sync) | | ✓ | | |
| FEA-003 (reports) | Preview | Full | | |
| FEA-007 (dashboard) | ✓ | | | |
| FEA-010 (auth) | | | | ✓ |

This reveals:
- Features spread across multiple screens (normal)
- Features on no screens (problem: orphaned)
- Screens with no features (problem: unnecessary)

## Anti-Patterns to Avoid

| Anti-Pattern | Signal | Fix |
|--------------|--------|-----|
| **Screen explosion** | >20 unique screens for MVP | Consolidate; use modals/panels instead |
| **Feature-per-screen** | 1:1 FEA to SCR mapping | Group related features on screens |
| **No shared components** | Every screen is unique | Extract DES- patterns |
| **Navigation dead-ends** | Can't get back from a screen | Ensure bidirectional paths |
| **Journey disconnect** | SCR- not tied to UJ- | Every screen serves a journey |
| **Modal abuse** | Everything is a modal | Modals for confirmations/quick edits only |

## Quality Gates

Before proceeding to v0.5 Red Team Review:

- [ ] All UJ- steps mapped to screens
- [ ] All FEA- features appear on at least one screen
- [ ] Navigation paths are bidirectional (no dead-ends)
- [ ] Shared components identified as DES- entries
- [ ] Screen count reasonable for MVP (<15 pages)
- [ ] Entry points and core workflow prioritized

## Downstream Connections

SCR- and DES- entries feed into:

| Consumer | What It Uses | Example |
|----------|--------------|---------|
| **v0.5 Technical Stack Selection** | Screen complexity informs frontend needs | "20 screens → need component library" |
| **v0.6 Technical Specification** | Screens inform API data needs | SCR-001 → API-001 (dashboard data) |
| **v0.7 Build Execution** | Screens become implementation tasks | EPIC-03 builds SCR-001–005 |
| **Design** | SCR- entries become wireframes/mockups | SCR-001 → Figma design |

## Detailed References

- **Screen flow examples**: See `references/examples.md`
- **SCR- entry template**: See `assets/scr.md`
- **DES- entry template**: See `assets/des.md`
- **Navigation patterns guide**: See `references/navigation-patterns.md`
