---
name: wireframing
description: "Create low-fidelity wireframes to explore layout, structure, and content hierarchy before visual design. Use for: early-stage design, layout exploration, content planning, stakeholder alignment, and rapid iteration."
---

# Wireframing

## Description

Wireframing is creating low-fidelity layouts that establish content hierarchy, layout structure, and functionality before visual design. Wireframes focus on "what" goes where, not "how" it looks. They're intentionally rough to encourage iteration.

## When to Use

- After information architecture is defined
- Before visual design to validate structure
- When exploring multiple layout approaches
- For quick stakeholder alignment
- When designing new screens or features

---

## Instructions for AI Agents

### Step 1: Identify Screens to Wireframe

**Prompt to prioritize screens:**
```
Based on the user flows for [PRODUCT], identify screens to wireframe:

**Priority 1 - Critical Screens** (define core experience):
[List screens that must be wireframed first]

**Priority 2 - Important Screens** (support main flows):
[List secondary screens]

**Priority 3 - Supporting Screens** (can be derived):
[List screens that follow patterns of above]
```

### Step 2: Create ASCII Wireframes

**Wireframe notation:**

```
┌───────────────────────┐
│ █████ Logo        ███ │  <- Header
├───────────────────────┤
│                       │
│  ████████████████  │  <- Large heading
│  ████████████████  │
│                       │
│  [███ Button ███]    │  <- Button
│                       │
│  ─────────────────  │  <- Text line
│  ─────────────────  │
│  ───────────       │  <- Shorter text
│                       │
│  ┌───────┐ ┌───────┐ │  <- Cards
│  │ Card  │ │ Card  │ │
│  └───────┘ └───────┘ │
│                       │
│  [█ Input field    ]  │  <- Input
│                       │
│  [●] Option one       │  <- Radio
│  [ ] Option two       │
│                       │
│  [✓] Checkbox item    │  <- Checkbox
│                       │
│  ┌─────────────────┐  │  <- Image placeholder
│  │    [✕] IMAGE   │  │
│  └─────────────────┘  │
│                       │
└───────────────────────┘
```

**Symbol legend:**
- `████` = Text/heading (more blocks = larger)
- `[███]` = Button
- `────` = Body text line
- `┌─┐└─┘` = Container/card borders
- `[✕]` = Image placeholder
- `[●][ ]` = Radio button
- `[✓][ ]` = Checkbox
- `[█ ]` = Input field

### Step 3: Wireframe Templates

**Common layout patterns:**

#### Landing Page Hero
```
┌──────────────────────────────────────────────────┐
│  LOGO        Nav  Nav  Nav    [CTA Button] │
├──────────────────────────────────────────────────┤
│                                                  │
│    ███████████████          ┌──────────────┐  │
│    ███████████████          │              │  │
│    Big Hero Headline         │   PRODUCT    │  │
│                              │    IMAGE     │  │
│    ──────────────────         │              │  │
│    ──────────────────         └──────────────┘  │
│    Supporting subheadline                        │
│                                                  │
│    [██ Primary CTA ██]  [Secondary]              │
│                                                  │
└──────────────────────────────────────────────────┘
```

#### Dashboard
```
┌──────────┬──────────────────────────────────────┐
│  LOGO    │  [Search...      ]        🔔  👤  │
├──────────┼──────────────────────────────────────┤
│          │  Page Title              [+ Action] │
│  ▶ Nav 1 │                                      │
│    Nav 2 ├────────────┬────────────┬────────────┤
│    Nav 3 │   STAT 1   │   STAT 2   │   STAT 3   │
│    Nav 4 │   ██████   │   ██████   │   ██████   │
│          ├────────────┴────────────┴────────────┤
│  ──────  │                                      │
│  ▶ Nav 5 │  MAIN CONTENT / TABLE                │
│    Nav 6 │  ──────────────────────────────────  │
│          │  ──────────────────────────────────  │
│          │  ──────────────────────────────────  │
│          │  ──────────────────────────────────  │
│  ──────  │                                      │
│  [+ New] │                       [Pagination]   │
└──────────┴──────────────────────────────────────┘
```

#### Mobile Screen
```
┌─────────────────┐
│  ←  Title   ⋮  │  <- Top bar
├─────────────────┤
│                 │
│  ███████████  │  <- Heading
│                 │
│  ────────────  │  <- Content
│  ────────────  │
│                 │
│  ┌───────────┐  │  <- Card
│  │  Card     │  │
│  └───────────┘  │
│                 │
│  ┌───────────┐  │
│  │  Card     │  │
│  └───────────┘  │
│                 │
├─────────────────┤
│ 🏠  📁  [+]  ✅  ⋮ │  <- Tab bar
└─────────────────┘
```

### Step 4: Annotate Wireframes

**Annotation format:**

```markdown
## Screen: [Screen Name]

### Wireframe
[ASCII Wireframe Here]

### Annotations

1. **[Element Name]** (A1)
   - Purpose: [What it does]
   - Behavior: [How it works]
   - Content: [What content goes here]

2. **[Element Name]** (A2)
   - Purpose: [What it does]
   - Behavior: [How it works]
   - Content: [What content goes here]

### Responsive Notes
- **Desktop**: [How it looks/works]
- **Tablet**: [Adaptations]
- **Mobile**: [Adaptations]

### Open Questions
- [ ] [Question about this screen]
```

---

## Example Input/Output

### Example Input

```markdown
**Product**: TaskFlow project management
**Screen**: Dashboard (main screen after login)
**User**: Sarah (Creative Director) - wants quick project status overview
```

### Example Output

```markdown
## Screen: Dashboard

### Purpose
Provide at-a-glance overview of all projects and personal tasks. Help Sarah quickly identify projects needing attention without diving into details.

### Desktop Wireframe

```
┌───────────┬─────────────────────────────────────────────────┐
│           │  [🔍 Search or jump to... ⌘K]          🔔  ┌─┐ │
│  TaskFlow │                                        │AV│ │
├───────────┼──────────────────────────────────────└─┘──────┤
│           │                                                   │
│  🏠 Dash   │  Good morning, Sarah           Friday, Mar 5     │
│           │                                                   │
│  📁 Proj   ├───────────────┬───────────────┬───────────────┤
│           │  ACTIVE PROJ  │  TASKS DUE    │  AT RISK       │
│  ✅ Tasks  │     12       │    5 today   │     2          │
│           │               │               │  🟡 Acme, 🔴 Foo  │
│  👥 Team   ├───────────────┴───────────────┴───────────────┤
│           │                                                   │
│  🏬 Client │  MY TASKS TODAY (5)                [View All →]  │
│           │                                                   │
│  ⏱ Time   │  ☐ Review homepage mockups     Acme • Due today  │
│           │  ☐ Client feedback call         Beta • Due today  │
│  📊 Report │  ☐ Approve final assets        Acme • Due today  │
│           │  ☐ Sprint planning             Team • Due today  │
│           │  ☐ Review contractor work      Misc • Due today  │
│  ───────  │                                                   │
│           ├─────────────────────────────────────────────────┤
│           │                                                   │
│  [+ New]  │  ACTIVE PROJECTS (12)              [View All →]  │
│           │                                                   │
│           │  ┌────────────┐ ┌────────────┐ ┌────────────┐  │
│           │  │ Acme       │ │ Beta       │ │ Gamma      │  │
│           │  │ Rebrand    │ │ Website    │ │ App Design │  │
│           │  │            │ │            │ │            │  │
│           │  │ 🟡 4 tasks  │ │ 🟢 On track │ │ 🟢 On track │  │
│           │  │ Due Fri    │ │ Due Mar 15 │ │ Due Mar 20 │  │
│           │  └────────────┘ └────────────┘ └────────────┘  │
│           │                                                   │
└───────────┴─────────────────────────────────────────────────┘
```

### Annotations

1. **Global Search** (Top bar)
   - Purpose: Quick access to any project, task, or person
   - Behavior: Cmd+K opens command palette style search
   - Shows recent items, quick actions, and search results

2. **Stat Cards** (Top row)
   - Purpose: At-a-glance health metrics
   - "At Risk" is clickable - shows projects needing attention
   - Color-coded: green = good, yellow = warning, red = alert

3. **My Tasks Today**
   - Purpose: Personal task list for the day
   - Behavior: Checkboxes for quick completion
   - Click task to open detail panel (slide-in)
   - "View All" goes to full task list

4. **Active Projects Grid**
   - Purpose: Quick access to current projects
   - Shows: Project name, client, status, next deadline
   - Color indicator matches project health
   - Click card to open project

### Mobile Wireframe

```
┌───────────────────────┐
│  ☰  TaskFlow    🔍  🔔  │
├───────────────────────┤
│                       │
│  Morning, Sarah       │
│                       │
│  ┌───────┬───────┬─────┐  │
│  │  12   │   5   │  2  │  │  <- Compact stats
│  │ Proj  │ Tasks │ Risk│  │
│  └───────┴───────┴─────┘  │
│                       │
│  Today (5)   [See all]│
│                       │
│  ☐ Review mockups     │
│    Acme • Due today   │
│  ───────────────────  │
│  ☐ Client call        │
│    Beta • Due today   │
│  ───────────────────  │
│  ☐ Approve assets     │
│    Acme • Due today   │
│                       │
│  Projects    [See all]│
│  ┌───────────────────┐  │
│  │ Acme Rebrand  🟡   │  │
│  └───────────────────┘  │
│                       │
├───────────────────────┤
│  🏠   📁  (➕)  ✅   ⋮   │  <- Tab bar
└───────────────────────┘
```

### Responsive Notes
- **Desktop (1200px+)**: Full sidebar, 3-column project grid
- **Tablet (768-1199px)**: Collapsible sidebar, 2-column grid
- **Mobile (<768px)**: Bottom tabs, single column, compact stats

### Open Questions
- [ ] Should "At Risk" show inline list or link to filtered view?
- [ ] How many projects to show before "View All"?
- [ ] Include time tracking widget on dashboard?
```

---

## Prompts Library

### Quick Wireframe
```
Create an ASCII wireframe for a [SCREEN TYPE] that:
- Primary purpose: [MAIN PURPOSE]
- Key elements: [LIST ELEMENTS]
- User: [PERSONA]
- Must include: [REQUIRED ELEMENTS]
```

### Layout Variations
```
Create 3 different layout approaches for [SCREEN]:

**Variation A**: [Description of approach]
[Wireframe]

**Variation B**: [Description of approach]
[Wireframe]

**Variation C**: [Description of approach]
[Wireframe]

Recommendation: [Which to pursue and why]
```

### Mobile Adaptation
```
Adapt this desktop wireframe for mobile:
[DESKTOP WIREFRAME]

Consider:
1. What content is essential vs. can be hidden?
2. How does navigation change?
3. What interactions need touch optimization?
4. What order should stacked elements appear?
```

---

## Success Criteria

### Minimum Requirements
- [ ] All critical screens wireframed
- [ ] Desktop and mobile versions
- [ ] Content hierarchy clear
- [ ] Navigation included
- [ ] Annotations for key elements

### Quality Indicators
- [ ] Wireframes are appropriately rough (not too detailed)
- [ ] Layout supports user goals from personas
- [ ] Consistent patterns across screens
- [ ] Responsive considerations documented
- [ ] Questions and assumptions noted

---

## Related Skills

- **Previous**: `information_architecture.md` - Structure to wireframe
- **Next**: `layout_grids.md` - Formalize grid system
- **Next**: `component_design.md` - Design components shown in wireframes
