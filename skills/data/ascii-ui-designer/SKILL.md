---
name: ascii-ui-designer
description: 'Create high-quality ASCII art UI/UX previews for web development with
  a two-phase approach. Phase 1: Design & Preview - visualize interfaces, explore
  layouts, refine ideas in ASCII format without code'
---

---
name: ascii-ui-designer
description: Create high-quality ASCII art UI/UX previews for web development with a two-phase approach. Phase 1: Design & Preview - visualize interfaces, explore layouts, refine ideas in ASCII format without code. Phase 2: Implementation - when ready, get HTML/CSS/React code and design tokens. Use for exploring ideas, getting stakeholder feedback, and iterating on design before development.
---

# ASCII UI Designer

A two-phase design system for web interfaces. Start with ASCII art previews to explore, iterate, and refine. When ready, move to implementation with code.

## Two-Phase Workflow

### 📐 Phase 1: Design & Preview (Exploration)
**Visualize ideas. Explore layouts. Get feedback. Iterate. NO CODE.**

- Create ASCII mockups quickly (5-10 minutes)
- Explore multiple design directions
- Iterate based on stakeholder feedback
- Refine information hierarchy and layout
- Validate design before development
- Share with team easily

**Use Phase 1 when**: You want to explore ideas, get feedback, iterate, or validate a design before coding.

### 💻 Phase 2: Implementation (Development)
**Build the code. Use patterns. Ship the design.**

- Move to implementation when design is finalized
- Access HTML/CSS patterns and React components
- Apply consistent design tokens
- Build responsive interfaces
- Translate ASCII directly to code

**Use Phase 2 when**: Your design is approved and you're ready to implement.

**Key Point**: You can use Phase 1 alone for design exploration, or combine both phases for complete development workflow.

## Core Principles

**Aesthetic Quality**: Professional box-drawing characters, proper spacing, and visual hierarchy create polished designs.

**Design-First**: Explore and refine ideas in ASCII before touching any code.

**Separation of Concerns**: Design phase is separate from implementation phase. Iterate on design without worrying about code.

**Iterative Refinement**: Create, show, get feedback, adjust, repeat until design is perfect.

**Clarity Over Perfection**: Readable ASCII designs with clear intent beat perfect alignment.

---

# Phase 1: Design & Preview

## Design-Only Phase

In Phase 1, you're **exploring ideas, not building code**. The focus is purely on:
- Layout and structure
- Information hierarchy
- User interactions and flow
- Visual clarity
- Stakeholder feedback

**Don't worry about**: CSS, React, HTML, or any implementation details. That comes in Phase 2.

## ASCII Design Elements

Use these box-drawing characters for professional appearance:

```
┌─┬─┐  Top border with columns
├─┼─┤  Row dividers
└─┴─┘  Bottom border

│      Vertical lines
─      Horizontal lines
┼      Intersections

╔═╗    Heavy borders for emphasis
╚═╝

Special characters:
★ for emphasis/logo
● for bullets
► for navigation/direction
✓ for checkmarks
⚙ for settings
🔍 for search
👤 for user/profile
```

Width constraint: Keep designs **under 100 characters wide** for readability.

## Design Workflow in Phase 1

### Step 1: Clarify the Need
Before sketching, understand:
- **What problem** does this solve?
- **Who uses** this interface?
- **What are they trying** to accomplish?
- **What information** do they need to see?

### Step 2: Explore Layout Options
Create 2-3 different layout directions:
- **Option A**: Sidebar + Content layout
- **Option B**: Top nav + Card grid layout
- **Option C**: Full-width content with filters

Show all options in ASCII. Get feedback on which direction is best.

### Step 3: Refine the Best Option
Once you choose a direction:
- Adjust spacing and alignment
- Improve information hierarchy
- Clarify all interactive elements
- Mark buttons, inputs, navigation
- Show loading states if relevant

### Step 4: Show Interactions
Clearly indicate:
- **Buttons**: `[Button Text]`
- **Inputs**: `[________________]`
- **Links**: `Home  About  Services`
- **Active states**: Highlight current selection
- **Navigation**: Use `►` to show menu items
- **Data display**: Use tables, cards, lists

### Step 5: Iterate Based on Feedback
Share the design ASCII with stakeholders:
- Is the layout clear?
- Is information easy to find?
- Are all actions obvious?
- Does it feel complete?

Adjust based on feedback:
- Move sections around
- Add/remove content
- Reorganize information
- Improve clarity

### Step 6: Create Multiple Sizes (Optional)
For responsive designs, create versions:
- **Mobile** (40 chars wide): Single column, stacked
- **Tablet** (70 chars wide): 2-column, flexible
- **Desktop** (100 chars wide): Full layout

### Step 7: Move to Phase 2 (When Ready)
Once design is approved:
- Ask for implementation guidance
- Get HTML structure
- Get CSS approach
- Get React components
- Move to Phase 2

## Common Layout Patterns (Phase 1 Only)

### Navigation Bar Pattern
```
┌──────────────────────────────────────────────────┐
│ ★ Logo    Home  About  Services    🔍 Search    │
└──────────────────────────────────────────────────┘
```

**When to use**: Every page needs top-level navigation

**Design questions**:
- How many nav items?
- Should search be visible?
- User account icon location?
- Mobile? Hamburger menu?

### Sidebar + Content Pattern
```
┌─────────┬──────────────────────────────┐
│ ★ Logo  │ Main Content Area            │
│ ───     │ ────────────────────────     │
│ ► Home  │                              │
│ ► Items │                              │
│ ► Users │                              │
└─────────┴──────────────────────────────┘
```

**When to use**: Apps with multiple sections, navigation, main content

**Design questions**:
- How many nav items?
- Should sidebar collapse?
- Logo needed?
- Search in sidebar or main area?

### Card Grid Pattern
```
┌──────────────┐  ┌──────────────┐
│ Title        │  │ Title        │
│ ────────────│  │ ────────────│
│ Content      │  │ Content      │
│ [Action]     │  │ [Action]     │
└──────────────┘  └──────────────┘
```

**When to use**: Displaying collections (products, articles, cards)

**Design questions**:
- How many cards per row?
- What information in each card?
- Action button or link?
- How many cards shown initially?

### Form Pattern
```
┌─────────────────────────────┐
│ Form Title                  │
├─────────────────────────────┤
│ Label                       │
│ [_____________________]     │
│                             │
│ Label                       │
│ [_____________________]     │
│                             │
│ [Submit]  [Cancel]          │
└─────────────────────────────┘
```

**When to use**: Data entry, user input

**Design questions**:
- How many fields?
- Required vs optional?
- Validation messages?
- Single or multi-step?
- Submit/Cancel buttons needed?

### Data Table Pattern
```
┌────────┬──────────┬──────────┐
│ Name   │ Email    │ Status   │
├────────┼──────────┼──────────┤
│ John   │ j@ex.cm  │ Active   │
│ Jane   │ j@ex.cm  │ Inactive │
└────────┴──────────┴──────────┘
```

**When to use**: Displaying structured data

**Design questions**:
- What columns?
- Sortable?
- Searchable?
- Actions per row?
- How many rows shown?

## Tips for Phase 1 Design

**Do**:
- ✓ Focus on layout and structure
- ✓ Keep it simple and clear
- ✓ Use proper spacing
- ✓ Align elements consistently
- ✓ Show all interactive elements
- ✓ Iterate multiple times
- ✓ Get feedback early and often
- ✓ Explore multiple directions

**Don't**:
- ✗ Worry about colors yet
- ✗ Think about CSS classes
- ✗ Plan React structure
- ✗ Concern yourself with responsive breakpoints
- ✗ Plan for animations
- ✗ Over-perfect the ASCII art
- ✗ Try to implement anything
- ✗ Get stuck on one direction

## When to Move to Phase 2

Move to Phase 2 (Implementation) when:

✓ Design is approved by stakeholders
✓ Layout feels right
✓ Information hierarchy is clear
✓ All interactions are marked
✓ You understand what needs to be built
✓ You're ready to start coding

**Don't move to Phase 2 if**:
- You're still unsure about the layout
- You haven't shown it to stakeholders
- Design keeps changing
- You're exploring multiple options

Keep iterating in Phase 1 until design is solid.

## Phase 1 Success Criteria

You've done Phase 1 well when:

✓ Design is clear and understandable
✓ All sections and interactions are marked
✓ Information hierarchy is obvious
✓ Stakeholders approve the design
✓ You have a clear picture of what to build
✓ Layout works for target screen sizes
✓ You're confident moving to implementation

---

# Phase 2: Implementation

**Note**: Phase 2 content is separate. When you're ready to implement:
- Ask for "implementation guidance" or "code patterns"
- Request HTML structure
- Request CSS approach
- Request React components
- Reference design tokens
- See references/html-css-patterns.md, react-patterns.md, design-tokens.md

---

# Quick Decision Guide

| Situation | Use Phase 1 | Use Phase 2 |
|-----------|------------|-----------|
| Exploring a new feature | ✅ YES | No |
| Getting stakeholder feedback | ✅ YES | No |
| Iterating on layouts | ✅ YES | No |
| Deciding between options | ✅ YES | No |
| Validating design before coding | ✅ YES | No |
| Need HTML structure | No | ✅ YES |
| Need CSS approach | No | ✅ YES |
| Need React components | No | ✅ YES |
| Design is approved & ready to code | No | ✅ YES |
| Building the final product | No | ✅ YES |

---

# Workflow Examples

## Example 1: Design Exploration Only
```
You: "Create 3 different layouts for a dashboard"
Claude: [Shows 3 ASCII mockups]
You: "I like Option 2. Can you make the sidebar narrower?"
Claude: [Adjusted mockup]
You: "Perfect! I'll move forward with this."
→ Design exploration complete. Ready for Phase 2 when needed.
```

## Example 2: Full Workflow
```
You: "Design a product listing page"
Claude: [Shows ASCII mockup]
You: "Looks great! Now show me the HTML structure"
Claude: [Moves to Phase 2, provides HTML]
You: "Perfect! Show me the React code"
Claude: [Provides React components]
→ From design to code in one flow.
```

## Example 3: Multiple Iterations
```
You: "Create 3 options for a user profile page"
Claude: [Shows 3 mockups]
You: "I like A and C together. Can you combine them?"
Claude: [Shows combined mockup]
You: "Can the stats be higher up?"
Claude: [Adjusted mockup]
You: "Great! Does this work for mobile?"
Claude: [Shows mobile version]
You: "Perfect, let's code it"
→ Design iteration then implementation.
```

---

# Phase 1 vs Phase 2 Comparison

| Aspect | Phase 1 (Design) | Phase 2 (Implementation) |
|--------|-----------------|--------------------------|
| **Focus** | Layouts, hierarchy, interactions | HTML, CSS, React |
| **Output** | ASCII mockups | Code and patterns |
| **Timeline** | Minutes | Hours |
| **Feedback** | Design feedback | Technical feedback |
| **Iteration** | Easy (text changes) | Harder (code changes) |
| **Stakeholders** | Product, design | Engineering |
| **Decision** | "Does this layout work?" | "How do we build this?" |

---

# Getting Started

## Using Phase 1 Only
1. Describe your interface
2. Claude creates ASCII mockups
3. You iterate and refine
4. Get stakeholder approval
5. Done! (Or move to Phase 2 when ready)

## Using Both Phases
1. Describe your interface
2. Claude creates ASCII mockups (Phase 1)
3. You iterate and refine
4. Get approval
5. Ask for implementation code (Phase 2)
6. Claude provides patterns and structure
7. You build the application

## Tips
- Start with Phase 1 for every feature
- Don't skip design exploration
- Get stakeholder feedback early
- Iterate in Phase 1 before coding
- Move to Phase 2 only when design is solid
