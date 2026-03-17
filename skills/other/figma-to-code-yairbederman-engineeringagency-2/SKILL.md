---
name: figma-to-code
description: Translate Figma designs into production-ready code with pixel-perfect accuracy. Use when implementing UI from Figma mockups.
---

# Figma to Code

Structured workflow for translating Figma designs into production-ready code with pixel-perfect accuracy.

## When to Use

- Implementing new UI from Figma designs
- Converting design mockups to React/Next.js components
- Extracting design tokens from Figma
- Design handoff automation

## Prerequisites

- Access to Figma file via MCP or design tokens export
- Target component library defined (React, Vue, etc.)
- Design system tokens available

## Workflow

### Phase 1: Design Analysis

1. **Identify Components**
   - List all unique UI elements
   - Map to existing component library
   - Identify new components needed

2. **Extract Design Tokens**
   ```json
   {
     "colors": {
       "primary": "#3B82F6",
       "secondary": "#10B981"
     },
     "typography": {
       "heading": { "font": "Inter", "size": "24px", "weight": 600 },
       "body": { "font": "Inter", "size": "16px", "weight": 400 }
     },
     "spacing": {
       "xs": "4px",
       "sm": "8px",
       "md": "16px",
       "lg": "24px"
     }
   }
   ```

3. **Document Measurements**
   - Widths, heights, padding, margins
   - Border radii, shadows
   - Responsive breakpoints

### Phase 2: Component Mapping

| Figma Layer | Component | Props |
|-------------|-----------|-------|
| Button/Primary | `<Button variant="primary">` | size, disabled |
| Input/Text | `<Input type="text">` | placeholder, error |
| Card/Default | `<Card>` | elevation, clickable |

### Phase 3: Implementation

1. **Create Component Structure**
   ```tsx
   // Component from Figma
   interface Props {
     // Props derived from Figma variants
   }
   
   export const Component = ({ ...props }: Props) => {
     return (
       <div className={styles.container}>
         {/* Match Figma layer hierarchy */}
       </div>
     )
   }
   ```

2. **Apply Styles**
   - Use design tokens, not magic numbers
   - Match Figma spacing exactly
   - Implement responsive variants

3. **Handle States**
   - Default, hover, active, disabled
   - Loading states
   - Error states

### Phase 4: Verification

1. **Visual Comparison**
   - Overlay implementation on Figma design
   - Check pixel alignment
   - Verify colors match tokens

2. **Responsive Check**
   - Test all breakpoints
   - Verify mobile layout

3. **Interaction Check**
   - All states work correctly
   - Animations match spec

## Best Practices

### DO

- ✅ Use design tokens from Figma
- ✅ Match component hierarchy to Figma layers
- ✅ Implement all states shown in design
- ✅ Test at exact Figma frame sizes
- ✅ Document deviations from design

### DON'T

- ❌ Eyeball measurements
- ❌ Use magic numbers for spacing
- ❌ Ignore design variants
- ❌ Skip responsive testing
- ❌ Forget hover/active states

## Output Checklist

Before marking implementation complete:

- [ ] All design tokens extracted
- [ ] Components match Figma hierarchy
- [ ] Spacing matches design exactly
- [ ] Colors use token values
- [ ] Typography matches font specs
- [ ] All states implemented
- [ ] Responsive breakpoints work
- [ ] Visual diff shows < 1% deviation
