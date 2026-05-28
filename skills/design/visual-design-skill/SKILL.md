---
document_name: "visual-design.skill.md"
location: ".claude/skills/visual-design.skill.md"
codebook_id: "CB-SKILL-VISUALDES-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for visual design work"
skill_metadata:
  category: "design"
  complexity: "intermediate"
  estimated_time: "varies"
  prerequisites:
    - "Design fundamentals"
    - "Design tools"
category: "skills"
status: "active"
tags:
  - "skill"
  - "design"
  - "visual"
  - "ui"
ai_parser_instructions: |
  This skill defines procedures for visual design.
  Used by UI Designer agent.
---

# Visual Design Skill

=== PURPOSE ===

Procedures for creating visual designs and mockups.

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(ui-designer) @ref(CB-AGENT-UIDESIGN-001) | Primary skill for visual work |

=== PROCEDURE: Design Process ===

**Steps:**
1. Review requirements and user flows
2. Reference design system foundations
3. Create low-fidelity wireframes
4. Iterate to high-fidelity mockups
5. Define states and interactions
6. Document specifications
7. Handoff to development

=== PROCEDURE: Layout Principles ===

**Grid System:**
```
Desktop (1200px+):
- 12 column grid
- 72px columns
- 24px gutters
- 80px margins

Tablet (768px-1199px):
- 8 column grid
- 24px gutters
- 32px margins

Mobile (< 768px):
- 4 column grid
- 16px gutters
- 16px margins
```

**Visual Hierarchy:**
1. **Size** - Larger = more important
2. **Color** - Bold/saturated = attention
3. **Contrast** - High contrast = emphasis
4. **Position** - Top-left reads first (LTR)
5. **Whitespace** - Isolation = importance

=== PROCEDURE: Color Usage ===

**Semantic Application:**
| Context | Color | Opacity |
|---------|-------|---------|
| Primary action | primary-500 | 100% |
| Secondary action | gray-100 | 100% |
| Destructive action | error | 100% |
| Disabled state | any | 50% |
| Hover state | +10% darker | 100% |
| Active state | +20% darker | 100% |

**Background Layers:**
```
Layer 0 (Page): gray-50
Layer 1 (Card): white
Layer 2 (Elevated): white + shadow-md
Layer 3 (Modal): white + shadow-xl
```

=== PROCEDURE: Typography Application ===

**Content Hierarchy:**
```
Page Title:     4xl, bold, gray-900
Section Title:  2xl, semibold, gray-900
Subsection:     xl, semibold, gray-900
Body:           base, regular, gray-700
Caption:        sm, regular, gray-500
Label:          sm, medium, gray-600
```

**Line Length:**
- Optimal: 50-75 characters
- Maximum: 85 characters
- Minimum: 45 characters

=== PROCEDURE: Spacing Application ===

**Component Internal Spacing:**
| Component | Padding |
|-----------|---------|
| Button | 16px horizontal, 8px vertical |
| Input | 12px |
| Card | 16px (mobile), 24px (desktop) |
| Modal | 24px |

**Layout Spacing:**
| Element | Margin |
|---------|--------|
| Between sections | 48px |
| Between cards | 24px |
| Between form fields | 16px |
| Between paragraphs | 16px |

=== PROCEDURE: Icon Design ===

**Icon Guidelines:**
- Size: 16px, 20px, 24px (standard)
- Stroke: 1.5px or 2px
- Corner radius: Match system (usually 2px)
- Style: Consistent (outlined OR filled)

**Icon Grid:**
```
┌────────────────────┐
│                    │
│    ┌──────────┐    │  24x24 canvas
│    │   SAFE   │    │  20x20 safe area
│    │   AREA   │    │  2px padding
│    └──────────┘    │
│                    │
└────────────────────┘
```

=== PROCEDURE: State Design ===

**Interactive States:**
| State | Visual Treatment |
|-------|------------------|
| Default | Base styling |
| Hover | Darker background or underline |
| Focus | Focus ring (2px, primary-500) |
| Active | Darker than hover, slight scale |
| Disabled | 50% opacity, no cursor |
| Loading | Spinner or skeleton |

**Form States:**
| State | Visual Treatment |
|-------|------------------|
| Empty | Placeholder text, gray-400 |
| Filled | Value text, gray-900 |
| Valid | Green border/icon |
| Invalid | Red border, error message |
| Focused | Primary border, glow |

=== PROCEDURE: Responsive Design ===

**Breakpoints:**
| Name | Min Width | Max Width |
|------|-----------|-----------|
| mobile | 0 | 767px |
| tablet | 768px | 1023px |
| desktop | 1024px | 1279px |
| wide | 1280px | ∞ |

**Responsive Patterns:**
- Stack (horizontal → vertical)
- Hide/Show (hide less important)
- Adapt (change component variant)
- Overflow (scroll container)

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(design-system) | System context |
| @skill(design-tokens) | Token usage |
