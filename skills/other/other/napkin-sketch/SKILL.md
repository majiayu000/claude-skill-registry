---
name: napkin-sketch
description: ASCII wireframes + browser capture for design matching
---

# Napkin Sketch Skill

Create quick wireframes as ASCII art OR capture existing UI from browser to match design systems.

## Quick Start

1. Tell me what screen or feature you want to sketch
2. I'll ask: **New design** (ASCII wireframe) or **Match existing** (browser capture)?
3. For new designs, I ask about layout, key components, and states
4. I generate ASCII wireframes with annotations and state variations
5. Use the wireframe in PRDs, tickets, or as input for `/generate-ai-prototype`

**Example:** "Sketch a settings page with tabs for Profile, Security, and Billing"

**Output:** Wireframe delivered inline, also saved to `outputs/prototypes/[feature]-napkin-sketch.md`

**Time:** 5-10 minutes per screen

## When to Use This Skill

**ASCII Wireframes (New Designs):**
- Communicating initial UI concepts
- Before involving designers
- PRD illustrations
- Quick stakeholder alignment

**Browser Capture (Existing Patterns):**
- "Make it look like our existing product"
- Referencing design system components
- Showing exactly what UI to match
- Documenting current state before changes

## Two Modes

### Mode 1: ASCII Wireframe
Quick sketch of new UI concept using text/symbols

### Mode 2: Browser Capture
Screenshot existing product UI to reference for new features

## Workflow - Mode 1: ASCII Wireframe

### Step 1: Define Layout Structure

Choose layout type:

**Single Column (Simple):**
```
┌────────────────────────────────────┐
│ Header                             │
├────────────────────────────────────┤
│                                    │
│ Main Content Area                  │
│                                    │
├────────────────────────────────────┤
│ Footer                             │
└────────────────────────────────────┘
```

**Two Column (Dashboard):**
```
┌──────────┬─────────────────────────┐
│          │                         │
│ Sidebar  │  Main Content           │
│          │                         │
│          │                         │
└──────────┴─────────────────────────┘
```

**Three Column (Complex):**
```
┌──────┬────────────────────┬────────┐
│ Nav  │                    │ Aside  │
│      │    Main Content    │        │
│      │                    │        │
└──────┴────────────────────┴────────┘
```

### Step 2: Add UI Components

Common component representations:

**Buttons:**
```
[ Button Text ]   ← Primary button
( Button Text )   ← Secondary button
< Back            ← Navigation
```

**Text Input:**
```
[_______________]  ← Input field
[_____________] 🔍 ← Search box
```

**Dropdown:**
```
[Select Option ▼]
```

**Checkboxes/Radio:**
```
[ ] Checkbox option
[x] Checked option
( ) Radio option
(•) Selected radio
```

**Toggle:**
```
[ON |  OFF ]  ← Toggle switch
```

**Tabs:**
```
┌─────┬─────┬─────┐
│ Tab1│ Tab2│ Tab3│
└─────┴─────┴─────┘
```

**Cards:**
```
┌─────────────────────────┐
│ Card Title              │
│ ─────────────────────── │
│ Card content goes here  │
│                         │
│ [ Action ]              │
└─────────────────────────┘
```

**Lists:**
```
• List item 1
• List item 2
• List item 3
```

**Tables:**
```
┌────────┬──────────┬────────┐
│ Col 1  │  Col 2   │  Col 3 │
├────────┼──────────┼────────┤
│ Data 1 │  Data 2  │ Data 3 │
│ Data 4 │  Data 5  │ Data 6 │
└────────┴──────────┴────────┘
```

**Icons (use emoji):**
```
⚙️ Settings
👤 Profile
🔔 Notifications
📊 Analytics
✏️ Edit
🗑️ Delete
+ Add
× Close
```

### Step 3: Build Complete Screen

Example: User Profile Page

```
┌───────────────────────────────────────────────────────────┐
│  Logo              Search [___________] 🔍    👤 Profile ▼ │
└───────────────────────────────────────────────────────────┘
┌──────────────┬────────────────────────────────────────────┐
│              │                                            │
│  Navigation  │  ┌──────────────────────────────────────┐ │
│              │  │  Profile Picture                     │ │
│  > Dashboard │  │       [   Photo   ]                  │ │
│    Profile   │  │                                      │ │
│    Settings  │  │  Name: John Doe                      │ │
│    Billing   │  │  Email: john@example.com             │ │
│              │  │  Role: Product Manager               │ │
│              │  │                                      │ │
│              │  │  [ Edit Profile ]                    │ │
│              │  └──────────────────────────────────────┘ │
│              │                                            │
│              │  ┌──────────────────────────────────────┐ │
│              │  │  Recent Activity                     │ │
│              │  │  ────────────────────────────────── │ │
│              │  │  • Updated PRD: Feature X   2h ago   │ │
│              │  │  • Commented on ticket #123 5h ago   │ │
│              │  │  • Reviewed design mockups  1d ago   │ │
│              │  └──────────────────────────────────────┘ │
│              │                                            │
└──────────────┴────────────────────────────────────────────┘
```

### Step 4: Add Annotations

```
┌─────────────────────────────────────┐
│  [Search bar] 🔍   [+ New] [Filter]│ ← Actions top-right
├─────────────────────────────────────┤
│                                     │
│  ┌─────────────┐  ┌─────────────┐  │
│  │ Card 1      │  │ Card 2      │  │ ← Grid of cards
│  │ [...]       │  │ [...]       │  │
│  └─────────────┘  └─────────────┘  │
│                                     │
│  ┌─────────────┐  ┌─────────────┐  │
│  │ Card 3      │  │ Card 4      │  │
│  │ [...]       │  │ [...]       │  │
│  └─────────────┘  └─────────────┘  │
│                                     │
└─────────────────────────────────────┘
      ↑
    Pagination: < 1 2 3 4 5 >
```

### Step 5: Show States

Document different UI states:

**Empty State:**
```
┌─────────────────────────────────┐
│                                 │
│       No items yet              │
│                                 │
│   [ + Create First Item ]       │
│                                 │
└─────────────────────────────────┘
```

**Loading State:**
```
┌─────────────────────────────────┐
│                                 │
│         Loading...              │
│          ⏳                      │
│                                 │
└─────────────────────────────────┘
```

**Error State:**
```
┌─────────────────────────────────┐
│  ⚠️ Error                        │
│  Something went wrong.          │
│  [ Try Again ]                  │
└─────────────────────────────────┘
```

## Workflow - Mode 2: Browser Capture

### Step 1: Navigate to Reference UI

Use browser automation to capture existing product UI:

```
1. Open browser to product
2. Navigate to relevant screen
3. Take screenshot of specific component
4. Annotate what to match
```

### Step 2: Capture Component

```
Target component: [e.g., "Navigation bar"]
Screenshot: [Capture of existing nav]

Annotations:
→ Match this exact color scheme
→ Use same button style
→ Keep icon placement consistent
```

### Step 3: Document Design Tokens

Extract design system details:

```
From screenshot analysis:

Colors:
- Primary: #3B82F6 (blue)
- Secondary: #10B981 (green)
- Background: #F9FAFB (light gray)

Typography:
- Headings: 24px, bold
- Body: 16px, regular
- Labels: 14px, medium

Spacing:
- Padding: 16px
- Gaps: 12px
- Border radius: 8px

Components:
- Button height: 40px
- Input height: 40px
- Card shadow: 0 1px 3px rgba(0,0,0,0.1)
```

### Step 4: Create "Match This" Spec

```
New Feature: [Feature name]

Design Requirement: Match existing [Component]

Reference Screenshot: [Link/embedded image]

What to match:
✅ Color palette (use primary blue #3B82F6)
✅ Button style (rounded, 40px height)
✅ Spacing (16px padding, 12px gaps)
✅ Typography (16px body text)

What can differ:
⚠️ Layout structure (new feature has different content)
⚠️ Icon choices (use similar style from icon library)
```

## Example Wireframes

### Example 1: Login Screen

```
┌─────────────────────────────────────┐
│                                     │
│         [   App Logo   ]            │
│                                     │
│     Welcome Back!                   │
│     Sign in to continue             │
│                                     │
│     Email                           │
│     [_____________________]         │
│                                     │
│     Password                        │
│     [_____________________] 👁️      │
│                                     │
│     [x] Remember me  Forgot pwd?    │
│                                     │
│     [ Sign In ]                     │
│                                     │
│     ─────── or ───────              │
│                                     │
│     ( Sign in with Google )         │
│     ( Sign in with GitHub )         │
│                                     │
│     Don't have an account? Sign up  │
│                                     │
└─────────────────────────────────────┘
```

### Example 2: Dashboard

```
┌──────────────────────────────────────────────────────────────┐
│ 📊 Dashboard    [Search...] 🔍    🔔 👤 ⚙️                    │
└──────────────────────────────────────────────────────────────┘
┌────────┬─────────────────────────────────────────────────────┐
│        │                                                     │
│ Home   │  Overview                                          │
│ Team   │  ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│ Files  │  │ Total    │ │ Active   │ │ Revenue  │           │
│ Reports│  │ Users    │ │ Projects │ │ $125K    │           │
│ Settings│  │ 1,234    │ │ 42       │ │ +12% ▲   │           │
│        │  └──────────┘ └──────────┘ └──────────┘           │
│        │                                                     │
│        │  Recent Activity                                   │
│        │  ┌──────────────────────────────────────────────┐  │
│        │  │ Project Alpha completed          2h ago      │  │
│        │  │ New user signup: john@co.com     3h ago      │  │
│        │  │ Team Beta shipped v2.0           5h ago      │  │
│        │  │ [View All Activity →]                        │  │
│        │  └──────────────────────────────────────────────┘  │
│        │                                                     │
└────────┴─────────────────────────────────────────────────────┘
```

### Example 3: Settings Page with Tabs

```
┌────────────────────────────────────────────────────────────┐
│ ⚙️ Settings                                                 │
└────────────────────────────────────────────────────────────┘
┌─────────┬──────────┬──────────┬──────────┐
│ Profile │ Security │ Billing  │ Team     │ ← Tabs
└─────────┴──────────┴──────────┴──────────┘
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  Profile Information                                       │
│  ────────────────                                         │
│                                                            │
│  Photo                                                     │
│  [  Avatar  ]  ( Upload New Photo )                        │
│                                                            │
│  Full Name                                                 │
│  [John Doe___________________________]                     │
│                                                            │
│  Email Address                                             │
│  [john@example.com___________________]                     │
│                                                            │
│  Job Title                                                 │
│  [Product Manager____________________]                     │
│                                                            │
│  Bio                                                       │
│  [____________________________________]                    │
│  [____________________________________]                    │
│  [____________________________________]                    │
│                                                            │
│  [ Save Changes ]  ( Cancel )                              │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Example 4: Mobile View (Narrow)

```
┌──────────────────────┐
│ ☰  Logo      🔔 👤   │
└──────────────────────┘
│                      │
│  Welcome, John!      │
│                      │
│  ┌────────────────┐  │
│  │ Quick Actions  │  │
│  │ ────────────── │  │
│  │ + New Task     │  │
│  │ 📊 View Stats  │  │
│  │ 👥 Team        │  │
│  └────────────────┘  │
│                      │
│  Today's Tasks       │
│  ────────────────    │
│  [x] Task 1          │
│  [ ] Task 2          │
│  [ ] Task 3          │
│                      │
│  [View All →]        │
│                      │
└──────────────────────┘
```

## Output Format

Every napkin sketch delivery should follow this structure:

```markdown
### [Feature Name] - Napkin Sketch
**Context:** [1-2 sentences on what this solves]
**Screens:** [N screens]

#### Screen 1: [Name]
[ASCII wireframe]
**Key interactions:** [What users can do]
**State variations:** [Empty, loading, error, success]

#### Screen 2: [Name]
[ASCII wireframe]
**Key interactions:** [What users can do]
**State variations:** [Empty, loading, error, success]

#### Flow Summary
[ASCII flow diagram showing screen-to-screen navigation]
e.g.,
[Screen 1] --click "Next"--> [Screen 2] --submit--> [Screen 3: Confirmation]
                                  \--click "Back"--> [Screen 1]

#### Design Notes
- [Key design decisions and rationale]
- [Accessibility considerations]
- [Mobile considerations]
```

## Mobile-First Variant

If the feature is primarily mobile or responsive, include a mobile viewport wireframe (320px width) alongside the desktop version.

**Mobile frame format:**
```
┌──────────┐
│ ☰  Logo  │
├──────────┤
│          │
│ Content  │
│ stacked  │
│ vertically│
│          │
│ [Button] │
│          │
└──────────┘
```

**When to include mobile wireframes:**
- Feature is mobile-first or mobile-only
- PM explicitly asks for responsive design
- Feature involves touch interactions (swipe, pinch, tap)
- The PRD specifies mobile as a target platform

**Side-by-side format for responsive features:**
```
Desktop (1024px+)                    Mobile (320px)
┌──────────┬────────────────────┐    ┌──────────┐
│ Sidebar  │ Main Content       │    │ ☰ Header │
│          │                    │    ├──────────┤
│          │                    │    │ Content  │
└──────────┴────────────────────┘    └──────────┘
```

## Pro Tips

1. **Start simple:** Rectangle with labels → detailed wireframe
2. **Consistency:** Use same symbols throughout (don't mix styles)
3. **Annotations matter:** Arrow + note explains what text can't
4. **Show state variations:** Normal, hover, error, loading, empty
5. **Mobile-first:** Start with narrow layout if responsive
6. **Real content:** Use realistic text, not "lorem ipsum"
7. **Component library:** Save common patterns to reuse

## Common Symbols Reference

```
Boxes/Containers:
┌─┐ └─┘ ├─┤ ┬ ┴ ┼

Lines:
─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼

Arrows:
← → ↑ ↓ ↔ ↕

Bullets/Icons:
• ○ ◦ ■ □ ▪ ▫ ▸ ▹ ► ◄ ▲ ▼

Checkboxes:
[ ] [x] [~]

Common UI:
⚙️ 🔔 👤 📊 🗑️ ✏️ 🔍 + × ⋮ ☰
```

## Integration with Other Skills

**Feeds into:**
- `/prd-draft` - Include wireframes in PRDs
- `/generate-ai-prototype` - Use as reference for AI prototype prompts
- `/create-tickets` - Engineers see wireframe in ticket

**Follows:**
- `/interview-guide` - Wireframes help structure interview questions
- `/journey-map` - Map user journey, wireframe each touchpoint

## Context Routing (Check Before Wireframing)

Before creating any wireframe, check these sources:

| Source | Files | What to Extract |
|--------|-------|-----------------|
| Active PRD | `context-library/prds/*.md`, `outputs/prds/*.md` | UI requirements, user flows, feature scope, non-goals (what NOT to design) |
| User Research | `context-library/research/*.md` | Pain points to solve, user quotes about current UX frustrations |
| Stakeholder Profiles | `context-library/stakeholder-template.md` | Designer preferences (e.g., Lisa wants accessibility-first), exec priorities |
| Design System | Any design docs or style references in workspace | Colors, component patterns, layout conventions to follow |
| Past Prototypes | `outputs/prototypes/*.md` | Existing wireframes for consistency, decisions already made |
| Business Context | `context-library/business-info-template.md` | Product type, user personas, platform (web/mobile/both) |

**Priority:** PRD requirements first (the wireframe must match the spec), then user research (ground the design in real pain points), then past prototypes (maintain consistency).

## Questions to Ask Before Wireframing

1. **What's the goal?** Align stakeholders or guide designers?
2. **Desktop or mobile?** Or both?
3. **Match existing UI?** Use browser capture if yes
4. **What states?** Empty, loading, error, success?
5. **Who's the audience?** Engineers, designers, stakeholders?

## Output Quality Self-Check

Before delivering the napkin sketch, verify:

- [ ] **Output format followed** -- Uses the structured output template (context, screens, flow summary, design notes)
- [ ] **All requested screens included** -- Every screen the PM asked for is sketched
- [ ] **State variations shown** -- At minimum: default state and one alternate state (empty, error, or loading)
- [ ] **Annotations are clear** -- Key interactions and non-obvious elements are labeled
- [ ] **Consistent symbols** -- Same symbol conventions used throughout (no mixing button styles, etc.)
- [ ] **Realistic content** -- Sample text looks production-like, not placeholder "lorem ipsum"
- [ ] **Mobile variant included** -- If feature is mobile/responsive, a mobile wireframe is provided
- [ ] **Flow diagram present** -- For multi-screen features, screen-to-screen navigation is shown
- [ ] **Context checked** -- PRD requirements, user research, and past prototypes referenced before wireframing
- [ ] **Actionable for next step** -- Wireframe is clear enough to feed into `/generate-ai-prototype` or `/create-tickets`

If any check fails, fix it before delivering. A 5-minute wireframe should save hours of miscommunication.

---

Remember: Wireframes are thinking tools, not art. Good enough to communicate is perfect. The best wireframe is the one you can draw in 5 minutes.
