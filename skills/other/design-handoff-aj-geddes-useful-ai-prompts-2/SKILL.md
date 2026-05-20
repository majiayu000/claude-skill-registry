---
name: design-handoff
description: Prepare designs for development handoff. Document specifications, interactions, and assets to enable efficient development and maintain design quality.
---

# Design Handoff

## Overview

Design handoff bridges design and development, ensuring developers have all information needed to implement designs accurately and efficiently.

## When to Use

- Before development starts
- Feature completion in design
- Component library updates
- Design system changes
- Iterative refinement handoff

## Instructions

### 1. **Design Documentation**

```yaml
Design Handoff Package:

Overview:
  - Feature description
  - User flows
  - Key interactions
  - Platform (web, iOS, Android)

Screens & Components:
  - All screen designs
  - Responsive variants (mobile, tablet, desktop)
  - All component states (default, hover, focus, disabled, error)
  - Dark mode variants (if applicable)

Specifications:
  - Typography (font, size, weight, line-height)
  - Spacing & layout (padding, margin, gaps)
  - Colors (hex values, opacity)
  - Shadows & elevations
  - Border radius
  - Animations & transitions

Interactions:
  - Click/tap behaviors
  - Hover states
  - Focus indicators
  - Loading states
  - Error states
  - Success states

Assets:
  - SVG/PNG icons (with color variants)
  - Illustrations
  - Background images
  - Logo files
  - All assets exported with specs

Accessibility:
  - ARIA attributes
  - Keyboard navigation
  - Color contrast ratios
  - Focus indicators
  - Alt text for images

Responsive Breakpoints:
  - Mobile (320px - 480px)
  - Tablet (768px - 1024px)
  - Desktop (1200px+)
  - Layout changes per breakpoint

---

## Design Specifications:

Typography Spec Example:
  Element: Primary Heading (h1)
  Font Family: Inter
  Font Size: 48px (desktop), 32px (tablet), 24px (mobile)
  Font Weight: 700 (bold)
  Line Height: 1.2 (57.6px)
  Letter Spacing: -0.02em
  Color: #1F2937

Color Spec Example:
  Primary Brand: #2196F3
  Contrast: 4.5:1 on white background
  RGB: rgb(33, 150, 243)
  Usage: Primary actions, links, focus indicators

Spacing Example:
  Container Padding: 32px (desktop), 24px (tablet), 16px (mobile)
  Section Gap: 48px (desktop), 32px (tablet), 24px (mobile)
  Component Spacing: 16px (default), 8px (compact), 24px (generous)
```

### 2. **Developer-Friendly Documentation**

```python
# Create developer-ready handoff docs

class DesignHandoff:
    def create_spec_document(self, design):
        """Generate comprehensive spec"""
        return {
            'title': design.name,
            'version': '1.0',
            'last_updated': 'January 15, 2025',
            'design_owner': 'Sarah Chen',
            'development_owner': 'John Smith',
            'status': 'Ready for development',

            'overview': {
                'description': 'What this feature does',
                'user_goal': 'What users accomplish',
                'success_criteria': 'How we measure success'
            },

            'components': [
                {
                    'name': 'Primary Button',
                    'states': ['default', 'hover', 'active', 'disabled', 'loading'],
                    'specs': {
                        'padding': '12px 24px',
                        'border_radius': '8px',
                        'font_size': '16px',
                        'font_weight': '600',
                        'min_height': '44px'
                    },
                    'colors': {
                        'default': '#2196F3',
                        'hover': '#1976D2',
                        'disabled': '#CCCCCC'
                    },
                    'figma_link': 'https://figma.com/...'
                }
            ],

            'interactions': [
                {
                    'trigger': 'Click primary button',
                    'action': 'Submit form',
                    'feedback': 'Button shows loading spinner',
                    'success': 'Navigate to success page',
                    'error': 'Show error message'
                }
            ]
        }

    def create_component_inventory(self, design):
        """List all components and variants"""
        return {
            'ui_components': {
                'buttons': ['Primary', 'Secondary', 'Outline', 'Text'],
                'inputs': ['Text', 'Email', 'Password', 'Search'],
                'selects': ['Dropdown', 'Autocomplete', 'Radio', 'Checkbox'],
                'feedback': ['Toast', 'Modal', 'Alert', 'Progress'],
                'navigation': ['Breadcrumb', 'Tabs', 'Drawer', 'Pagination']
            },
            'total_components': 50,
            'total_variants': 250
        }

    def export_assets(self, design):
        """Prepare optimized assets"""
        return {
            'exports': [
                {'name': 'icons-16.svg', 'size': '16x16px', 'format': 'SVG'},
                {'name': 'icons-24.svg', 'size': '24x24px', 'format': 'SVG'},
                {'name': 'icons-32.svg', 'size': '32x32px', 'format': 'SVG'},
                {'name': 'logo.svg', 'format': 'SVG', 'colors': ['primary', 'white', 'dark']},
                {'name': 'placeholder-image.png', 'size': '1200x800px', 'format': 'PNG'}
            ],
            'optimization': 'All assets compressed, SVGs minified',
            'storage': 'Cloud drive link shared with dev team'
        }
```

### 3. **Handoff Checklist**

```yaml
Design Handoff Checklist:

Before Handoff:
  [ ] All screens complete and reviewed
  [ ] All component states documented
  [ ] Responsive variants specified
  [ ] Dark mode variants created (if applicable)
  [ ] Accessibility review completed
  [ ] Animations documented with timings
  [ ] All interactions specified
  [ ] Spec document written
  [ ] Assets exported and optimized
  [ ] Design approved by product manager
  [ ] Design approved by tech lead

Documentation:
  [ ] Overview document written
  [ ] Component specs documented
  [ ] Responsive breakpoints specified
  [ ] Interaction flows documented
  [ ] Copy and labels finalized
  [ ] Error states documented
  [ ] Loading states documented
  [ ] Empty states documented
  [ ] Accessibility requirements listed
  [ ] Performance constraints noted

Assets:
  [ ] Icons exported (all sizes)
  [ ] Illustrations included
  [ ] Images optimized
  [ ] Color palette defined
  [ ] Typography specifications clear
  [ ] Spacing/grid defined
  [ ] Shadow definitions provided
  [ ] All assets organized

Testing:
  [ ] Designs reviewed on mobile device
  [ ] Interaction flows validated
  [ ] Contrast ratios verified
  [ ] Focus states visible
  [ ] Keyboard navigation planned

Handoff Meeting:
  [ ] Design rationale explained
  [ ] Technical constraints discussed
  [ ] Timeline and scope agreed
  [ ] Questions answered
  [ ] Next steps clarified
  [ ] Designer available for questions
```

### 4. **Design-Dev Collaboration**

```yaml
Best Practices for Handoff:

Communication:
  - Schedule kickoff meeting before starting dev
  - Designer available for questions (at least 4 hours/week)
  - Use shared design tool (Figma) as source of truth
  - Use design comments for clarifications
  - Regular sync meetings (weekly recommended)

Documentation:
  - Write specs for non-obvious designs
  - Include rationale for design decisions
  - Document edge cases
  - Link to design patterns
  - Reference design system

Flexibility:
  - Allow developer improvements for technical feasibility
  - Be open to implementation alternatives
  - Test implementations and iterate
  - Adjust for browser/device constraints
  - Accommodate performance needs

Process:
  1. Design complete → Share in Figma
  2. Dev reviews specs, asks questions
  3. Kickoff meeting to align
  4. Dev implements with designer review
  5. First implementation review
  6. Design polish phase
  7. Final sign-off

---

Common Handoff Issues & Solutions:

Issue: Missing responsive designs
Solution: Include tablet & mobile variants in handoff

Issue: Unclear interactions
Solution: Record prototype videos or create Figma flows

Issue: Vague color specifications
Solution: Export color palette with hex, RGB, and CSS variables

Issue: Missing edge cases
Solution: Document error, loading, and empty states

Issue: Disconnect during development
Solution: Plan regular sync meetings and code reviews
```

## Best Practices

### ✅ DO
- Create comprehensive documentation
- Export all assets and specifications
- Document every component state
- Include responsive variants
- Explain design decisions
- Provide developer-friendly specs
- Use shared design tools
- Schedule kickoff meeting
- Make yourself available for questions
- Review implementations and iterate

### ❌ DON'T
- Expect developers to guess
- Leave responsive design to chance
- Skip edge case documentation
- Use unclear specifications
- Disappear after handoff
- Change designs mid-development without notification
- Provide images instead of vector files
- Ignore technical constraints
- Miss performance considerations
- Skip accessibility in handoff

## Design Handoff Tips

- Use Figma for design-to-dev (auto-sizing, specs)
- Create component library in code alongside design
- Document design tokens (colors, typography, spacing)
- Record Figma walkthroughs for complex interactions
- Maintain design system as source of truth
