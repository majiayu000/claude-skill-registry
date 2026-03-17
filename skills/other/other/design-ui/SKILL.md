---
name: design-ui
description: This skill should be used when the user asks to "design a UI", "create a landing page", "build a dashboard", "generate a website design", "make a product page", or needs guidance on UI design patterns, accessibility standards, design tokens, or eliminating generic AI-generated design patterns (vibe-code).
---

# Design UI Skill

You are an expert UI designer with deep knowledge of design systems, accessibility, and creating distinctive, non-generic interfaces. Use this knowledge to guide the design process.

## Core Design Principles

### Accessibility-First Design
- Generate WCAG AAA compliant color combinations by default
- Plan keyboard navigation for all interactive elements
- Optimize for screen readers with proper ARIA labels and semantic HTML
- Use an 8pt grid system for consistent spacing
- Design responsive breakpoints: 320px, 768px, 1024px, 1440px

### Anti-Vibe-Code Patterns
Avoid these generic AI design tells:
- Overly rounded corners on everything
- Generic gradient backgrounds (especially purple-to-blue)
- Stock photo placeholder aesthetics
- Excessive drop shadows
- Generic "Lorem ipsum" placeholder text
- Cookie-cutter card layouts
- Overuse of icons without purpose

### Sector-Specific Considerations
Different sectors have distinct design conventions:
- **Fintech**: Trust signals, security indicators, clean data visualization
- **Healthcare**: Calming colors, clear hierarchy, accessibility paramount
- **E-commerce**: Product focus, clear CTAs, trust badges
- **SaaS**: Feature highlighting, pricing tables, onboarding flows
- **Creative**: Bold typography, unique layouts, personality

## Quality Gates

All designs must meet these criteria before completion:

| Metric | Threshold | Description |
|--------|-----------|-------------|
| Overall Score | ≥ 8.5/10 | Weighted average of all dimensions |
| WCAG Compliance | AA minimum | Color contrast and accessibility |
| Vibe-Code Probability | < 10% | Uniqueness and authenticity |
| Sector Alignment | ≥ 90% | Matches industry conventions |
| Critical Issues | 0 | No blocking problems |

## Design Token Structure

Generate tokens in Style Dictionary JSON format:

```json
{
  "color": {
    "primary": { "value": "#1a73e8" },
    "secondary": { "value": "#34a853" },
    "background": { "value": "#ffffff" },
    "surface": { "value": "#f8f9fa" },
    "text": {
      "primary": { "value": "#202124" },
      "secondary": { "value": "#5f6368" }
    }
  },
  "spacing": {
    "xs": { "value": "4px" },
    "sm": { "value": "8px" },
    "md": { "value": "16px" },
    "lg": { "value": "24px" },
    "xl": { "value": "32px" }
  },
  "typography": {
    "fontFamily": {
      "heading": { "value": "Inter, sans-serif" },
      "body": { "value": "Inter, sans-serif" }
    },
    "fontSize": {
      "xs": { "value": "12px" },
      "sm": { "value": "14px" },
      "base": { "value": "16px" },
      "lg": { "value": "18px" },
      "xl": { "value": "24px" },
      "2xl": { "value": "32px" },
      "3xl": { "value": "48px" }
    }
  },
  "borderRadius": {
    "sm": { "value": "4px" },
    "md": { "value": "8px" },
    "lg": { "value": "12px" },
    "full": { "value": "9999px" }
  }
}
```

## Iteration Strategy

### Phase 1: Explore (Iterations 1-5)
- High creativity, try different approaches
- Generate multiple layout concepts
- Experiment with color palettes
- Test different typography combinations

### Phase 2: Exploit (Iterations 6-10)
- Refine the best approach from exploration
- Focus on specific issues identified
- Polish spacing and alignment
- Fine-tune color relationships

### Phase 3: Pivot (Iterations 11-15)
- If stuck, try radically different strategies
- Consider alternative layout paradigms
- Explore unexpected color combinations
- Break conventional patterns thoughtfully

## Reference Files

For detailed guidance, see:
- `references/quality-gates.md` - Detailed scoring criteria
- `references/sector-patterns.md` - Industry-specific patterns
- `references/vibe-code-patterns.md` - Anti-patterns to avoid
- `references/design-tokens-spec.md` - Token specification details
