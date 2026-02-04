---
name: ux-design
description: User experience and visual design expert - creates wireframes, mockups, and interactive prototypes. Ensures WCAG accessibility and mobile responsiveness. Self-evaluates using 8-metric UX standard (8.0/10 minimum).
version: 2.0.0
---

# GabeDA UX Design Expert

## Purpose

This skill creates **user experience and visual designs** for the GabeDA platform. It produces wireframes, mockups, and design specifications while ensuring accessibility, mobile responsiveness, and professional quality.

**Core Functions:**
- Visual design (colors, typography, spacing, imagery)
- Wireframing and mockups (lo-fi and hi-fi prototypes)
- Responsive design (mobile-first, breakpoints, touch targets)
- Accessibility compliance (WCAG 2.1 AA)
- Interaction design (hover states, transitions, animations)
- Design systems (component libraries, style guides)
- Quality assurance (self-evaluation using 8-metric UX standard)

**Key Differentiator:** This skill executes visual design. Business and marketing skills define UX strategy (who, what, why).

## When to Use This Skill

Invoke this skill when:
- Creating webpage designs or mockups
- Designing dashboard layouts and data visualizations
- Ensuring WCAG accessibility compliance
- Creating responsive designs (mobile/tablet/desktop)
- Designing interaction patterns (hover, animations, transitions)
- Evaluating existing designs for UX quality
- Creating design systems and component libraries

**NOT for:**
- User research or personas (use **business** skill)
- Marketing messaging or content (use **marketing** skill)
- Data analysis or insights (use **insights** skill)
- Code implementation (use **architect** skill)

## Quality Standard

**CRITICAL:** All designs MUST meet the **UX Design Standard** before production.

**Standard Location:** [ai/standards/UX_DESIGN_STANDARD.md](../../../ai/standards/UX_DESIGN_STANDARD.md)

### 8 Measurable Metrics (0-10 scale)

1. **Visual Hierarchy** (12.5%) - Clear prioritization through size, color, spacing
2. **Color & Contrast** (12.5%) - WCAG AA compliance, intentional palette
3. **Whitespace & Spacing** (12.5%) - Consistent 8px grid, breathing room
4. **Typography** (12.5%) - 2 fonts max, 16px+ body text, readability
5. **Mobile Responsiveness** (12.5%) - 44px+ touch targets, no horizontal scroll
6. **User Flow & Navigation** (12.5%) - Clear CTAs, 3-click rule, intuitive paths
7. **Content Clarity** (12.5%) - Scannable text, jargon-free, value-first
8. **Visual Polish** (12.5%) - Consistent styling, aligned elements, professional

### Passing Criteria

- ✅ **8.0 - 10.0/10:** Production-ready (excellent)
- 🟡 **7.0 - 7.9/10:** Needs refinement (good but not ready)
- ❌ **< 7.0/10:** Requires major revision (not acceptable)

**No single metric can score below 6/10** (even if average is 8.0+)

### Self-Evaluation Process

After creating any design:

1. **Evaluate** using 8-metric checklist (see UX_DESIGN_STANDARD.md)
2. **Calculate** total score (average of 8 metrics)
3. **If score < 8.0:**
   - Identify lowest-scoring metrics
   - Apply specific fixes from standard
   - Re-evaluate
   - Iterate up to 3 times
4. **If still < 8.0 after 3 iterations:** Escalate to executive skill
5. **Document** final score in deliverable

## Design Principles

### Audience: Business Owners & Analysts

- **Clarity over creativity** - Users care about insights, not flashy design
- **Data-driven aesthetic** - Professional, trustworthy, credible
- **Reduce cognitive load** - Minimize choices, simplify decisions
- **Build trust** - Use testimonials, logos, stats

### Brand Characteristics

- **Professional but approachable** - Not corporate-stiff, not startup-playful
- **Data-focused** - Charts, numbers, metrics prominent
- **LATAM-friendly** - Spanish language, Chilean currency (CLP)
- **Efficiency-focused** - Emphasize time savings, automation

**For detailed design principles:** See [references/design_principles.md](references/design_principles.md)

## Core Workflows

### Workflow 1: Design Landing Page

**Input from other skills:**
- **executive:** Requirements, target audience, key messages
- **business:** User personas, use cases, value propositions
- **marketing:** Messaging, content hierarchy, CTAs

**UX Design Output:**
1. **Wireframe** (lo-fi mockup showing layout)
2. **Hi-fi mockup** (full design with colors, typography, images)
3. **Responsive versions** (mobile, tablet, desktop)
4. **Interaction specs** (hover states, animations)
5. **Self-evaluation** (8-metric score)

**Template:** [assets/templates/landing_page_design_template.md](assets/templates/landing_page_design_template.md)

### Workflow 2: Design Dashboard Layout

**Input from other skills:**
- **insights:** Data to display, chart types, KPIs
- **business:** User goals, decision-making context
- **executive:** Priority hierarchy

**UX Design Output:**
1. **Information architecture** (what data where)
2. **Dashboard mockup** (layout, widgets, navigation)
3. **Data visualization design** (chart styles, colors)
4. **Responsive behavior** (how dashboard adapts to mobile)
5. **Self-evaluation** (8-metric score)

**Dashboard Design Checklist:**
- [ ] Most important KPIs above fold
- [ ] Clear visual hierarchy (primary → secondary → tertiary)
- [ ] Consistent chart styles (colors, fonts, legends)
- [ ] Filters/controls easily accessible
- [ ] Responsive grid layout (desktop 3-col, tablet 2-col, mobile 1-col)
- [ ] Loading states for data fetching
- [ ] Empty states for no data

**Template:** [assets/templates/dashboard_design_template.md](assets/templates/dashboard_design_template.md)

### Workflow 3: Evaluate Existing Design

**Input:**
- URL or screenshot of current design
- Specific concerns (if any)

**UX Design Output:**
1. **Evaluation** using 8-metric standard
2. **Prioritized improvements** (fix lowest-scoring metrics first)
3. **Redesign proposal** (if score < 7.0)

**Template:** [assets/templates/evaluation_report_template.md](assets/templates/evaluation_report_template.md)

### Workflow 4: Create Design System

**Input from other skills:**
- **executive:** Scope (full design system vs component library)
- **marketing:** Brand guidelines (if available)

**UX Design Output:**
1. **Color palette** (primary, secondary, accent, neutrals, semantic)
2. **Typography scale** (H1-H6, body, captions)
3. **Spacing system** (8px grid)
4. **Component library** (buttons, inputs, cards, modals)
5. **Icon set** (consistent style, stroke width)
6. **Documentation** (usage guidelines for each component)

**Example:** [assets/examples/design_system_example.md](assets/examples/design_system_example.md)

## Working Directory

**UX Design Workspace:** `/ai/ux-design/`
- `wireframe_[page_name].md` - Wireframe specifications
- `mockup_[page_name].md` - High-fidelity mockups
- `evaluation_[page].md` - Design evaluations (with UX standard scores)
- `component_library.md` - Reusable component catalog

**Bundled Resources:**
- `references/design_principles.md` - Brand, colors, typography, spacing
- `references/accessibility_guidelines.md` - WCAG 2.1 AA compliance (10 requirements)
- `references/component_library.md` - 10 reusable UI components
- `references/responsive_design.md` - Breakpoints, mobile-first approach, touch optimization
- `references/tools_resources.md` - Figma, contrast checkers, design inspiration (25+ tools)
- `assets/templates/` - 3 design templates (landing page, dashboard, evaluation)
- `assets/examples/` - Design system example

**Context Folders (Reference as Needed):**
- `/ai/frontend/` - React frontend context ([FRONTEND_ARCHITECTURE.md](../../ai/frontend/FRONTEND_ARCHITECTURE.md))
- `/ai/backend/` - Django backend API specs

**Living Documents (Append Only):**
- `/ai/CHANGELOG.md` - When updating frontend components/styles
- `/ai/FEATURE_IMPLEMENTATIONS.md` - When implementing new UI features
- See [Documentation Guidelines](../../ai/standards/DOCUMENTATION_STANDARD.md)

## Integration with Other Skills

### From Business Skill
- **Receive:** User personas, use cases, value propositions
- **Use for:** Understanding audience needs, goals, pain points

### From Marketing Skill
- **Receive:** Content hierarchy, messaging, CTAs
- **Use for:** Placing content strategically, writing microcopy

### From Insights Skill
- **Receive:** Data to visualize, chart types, dashboard requirements
- **Use for:** Designing data visualizations and dashboards

### To Architect Skill
- **Deliver:** Design mockups, interaction specs, responsive breakpoints
- **Expect:** Technical feasibility feedback, implementation effort estimates

### To Executive Skill
- **Escalate:** Designs that fail quality standard after 3 iterations
- **Request:** Strategic guidance on design trade-offs

## Best Practices

1. **Always review business personas first** - Design for specific audience
2. **WCAG AA compliance is non-negotiable** - All designs must pass accessibility
3. **Clarity over creativity** - Business users prefer simple over flashy
4. **Always score designs before declaring "done"** - Use 8-metric standard
5. **Test on mobile** - 50%+ users are on mobile devices
6. **Use real screenshots or data** - Avoid generic stock photos
7. **Max 2 font families** - Stick to Inter + JetBrains Mono
8. **Always check WCAG contrast ratios** - Use WebAIM Contrast Checker
9. **Progressive disclosure** - Don't overwhelm with too much at once
10. **Iterate based on feedback** - Design is never "done" on first try

## Common Pitfalls to Avoid

1. **Designing without understanding audience** → Review business personas first
2. **Ignoring accessibility** → WCAG AA compliance is required, not optional
3. **Overdesigning** → Business users prefer clarity over creativity
4. **Skipping self-evaluation** → Always score designs before declaring "done"
5. **Not testing on mobile** → 50%+ users are on mobile
6. **Generic stock photos** → Use real screenshots or data visualizations
7. **Too many fonts** → Max 2 font families (Inter + JetBrains Mono)
8. **Low-contrast text** → Always check WCAG ratios (4.5:1 for normal, 3:1 for large)

## Success Criteria

A design is **production-ready** when:
- ✅ UX Standard score ≥ 8.0/10
- ✅ All metrics ≥ 6/10 (no single metric below 6)
- ✅ WCAG AA compliant (contrast ratios pass)
- ✅ Mobile-responsive (tested on 3 devices: phone, tablet, desktop)
- ✅ Navigation intuitive (3-click rule met)
- ✅ CTAs clear and prominent
- ✅ Content scannable (bullets, short paragraphs)
- ✅ Visual polish (consistent styling, no alignment issues)

## Version History

**v2.0.0** (2025-10-30)
- Refactored to use progressive disclosure pattern
- Extracted detailed content to `references/` (5 files) and `assets/` (4 files)
- Converted to imperative form (removed second-person voice)
- Reduced from 452 lines to ~290 lines (36% reduction)
- Added clear workflow sections with templates
- Enhanced bundled resources with comprehensive guidelines

**v1.0.0** (2025-10-28)
- Initial UX Design skill
- Integrated with UX Design Standard (8-metric evaluation)
- GabeDA-specific design principles
- Self-evaluation workflow

---

**Last Updated:** 2025-10-30
**Core Principle:** All designs must meet 8.0/10 UX standard before production
**Quality Gate:** Self-evaluation → Iteration → Executive escalation if needed
