---
name: lovable-brand-enforcer
description: "Enforce consistent brand identity across all Lovable UI generations with design tokens, component rules, typography scales, and interaction patterns."
homepage: https://lovable.dev
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"emoji":"🎯"}}
---

# Lovable Brand Enforcer

## Purpose

Ensure every Lovable UI generation adheres to a defined brand identity. Prevents visual drift across multiple generations by producing a complete design token system, component styling rules, typography scale, and interaction patterns. Use before or alongside any other Lovable skill to lock in consistency.

> **Platform context**: Lovable generates React + TypeScript + Tailwind CSS + shadcn/ui apps. Design tokens map to Tailwind's `tailwind.config.ts` and CSS custom properties in `index.css`. shadcn/ui theming uses HSL-based CSS variables.

## Inputs

| Parameter       | Required | Values                                           | Default              |
|-----------------|----------|--------------------------------------------------|----------------------|
| `brand_name`    | yes      | Any string                                       | —                    |
| `style`         | yes      | corporate, startup, creative, editorial, technical | —                    |
| `palette`       | no       | Comma-separated hex: primary,secondary,accent,neutral | Computed from style |
| `fonts`         | no       | Comma-separated: heading-font,body-font          | Computed from style  |
| `border_radius` | no       | Number in px                                     | Computed from style  |
| `spacing_unit`  | no       | Number in px                                     | 8                    |

## Workflow

### 1. Resolve Brand Parameters

For missing optional values, apply defaults based on `style`:

| Style      | Primary  | Secondary | Accent  | Neutral  | Heading Font     | Body Font         | Radius | Spacing |
|------------|----------|-----------|---------|----------|------------------|-------------------|--------|---------|
| corporate  | #1e3a5f  | #4a5568   | #3182ce | #f7fafc  | Inter            | Inter             | 4px    | 8px     |
| startup    | #6366f1  | #f1f5f9   | #f59e0b | #ffffff  | Satoshi          | Inter             | 8px    | 8px     |
| creative   | #7c3aed  | #f472b6   | #fbbf24 | #fafafa  | Clash Display    | Satoshi           | 16px   | 8px     |
| editorial  | #1a1a1a  | #6b7280   | #b45309 | #f9fafb  | Playfair Display | Source Serif Pro  | 0px    | 4px     |
| technical  | #0f172a  | #334155   | #06b6d4 | #f8fafc  | Geist Sans       | Geist Mono        | 6px    | 8px     |

### 2. Generate Design Token Block

Produce CSS custom properties that integrate with shadcn/ui's theming system. Instruct Lovable to add these to `src/index.css`:

```css
:root {
  /* Brand Colors (HSL for shadcn compatibility) */
  --brand-primary: {primary_hsl};
  --brand-secondary: {secondary_hsl};
  --brand-accent: {accent_hsl};

  /* Spacing Scale */
  --space-unit: {spacing_unit}px;
  --space-xs: calc(var(--space-unit) * 0.5);
  --space-sm: var(--space-unit);
  --space-md: calc(var(--space-unit) * 2);
  --space-lg: calc(var(--space-unit) * 3);
  --space-xl: calc(var(--space-unit) * 4);
  --space-2xl: calc(var(--space-unit) * 6);
  --space-section: calc(var(--space-unit) * 8);

  /* Border Radius */
  --radius-sm: calc({border_radius}px * 0.5);
  --radius-md: {border_radius}px;
  --radius-lg: calc({border_radius}px * 2);
  --radius-full: 9999px;

  /* Typography */
  --font-heading: '{heading_font}', system-ui, sans-serif;
  --font-body: '{body_font}', system-ui, sans-serif;
}
```

### 3. Define Typography Scale

Generate a type scale with consistent ratios:

| Token       | Size     | Weight | Line Height | Font           | Usage                        |
|-------------|----------|--------|-------------|----------------|------------------------------|
| `display`   | 3.5rem   | 700    | 1.1         | heading        | Hero headlines               |
| `h1`        | 2.5rem   | 700    | 1.2         | heading        | Page titles                  |
| `h2`        | 2rem     | 600    | 1.25        | heading        | Section headers              |
| `h3`        | 1.5rem   | 600    | 1.3         | heading        | Subsection headers           |
| `h4`        | 1.25rem  | 600    | 1.4         | heading        | Card titles                  |
| `body`      | 1rem     | 400    | 1.6         | body           | Paragraph text               |
| `body-sm`   | 0.875rem | 400    | 1.5         | body           | Secondary text               |
| `caption`   | 0.75rem  | 500    | 1.4         | body           | Labels, captions             |
| `overline`  | 0.75rem  | 600    | 1.4         | body           | Uppercase category labels    |

### 4. Define Component Styling Rules

For every shadcn/ui component used in the project, enforce consistent styling:

**Buttons**:
- Primary: `bg-{primary}`, white text, `border-radius: var(--radius-md)`, min-height 40px.
- Secondary: `bg-transparent`, `border: 1px solid {primary}`, `text-{primary}`.
- Ghost: `bg-transparent`, `text-{secondary}`, hover `bg-{neutral}`.
- All buttons: `font-weight: 500`, `padding: 8px 16px`, `transition: all 150ms ease-out`.

**Cards**:
- `border-radius: var(--radius-lg)`, `border: 1px solid {neutral-200}`, `padding: var(--space-md)`.
- Hover: slight lift with shadow increase (coordinated with animation-choreographer if installed).
- No nested cards.

**Inputs**:
- `border-radius: var(--radius-md)`, `border: 1px solid {neutral-300}`, height 40px.
- Focus: `ring-2 ring-{primary}`, border color changes to `{primary}`.
- Error: `ring-2 ring-red-500`, `border-color: red-500`.

**Navigation**:
- Active item: `text-{primary}`, left border accent or background highlight.
- Hover: `bg-{neutral-100}` or subtle opacity change.
- Consistent icon size: 20px.

### 5. Define Interaction Patterns

Standardize interaction behavior across the project:

- **Button press**: Scale to 0.98 on active (100ms). Return to 1.0 on release (150ms).
- **Link hover**: Color shift to `{primary}`. Underline animates in from left (200ms).
- **Card hover**: `translateY(-2px)` + shadow increase (200ms ease-out). Matches animation skill if combined.
- **Focus ring**: 2px solid `{primary}` at 50% opacity, 2px offset. Visible on `:focus-visible` only.
- **Toast notifications**: Consistent position (top-right), slide-in animation, brand-colored accent bar.
- **Loading states**: Skeleton placeholders use `{neutral-100}` base with `{neutral-200}` shimmer.

### 6. Generate Lovable Constraint Block

Compile all tokens, rules, and patterns into a single reusable prompt block. Format:

```
BRAND IDENTITY CONSTRAINTS — {brand_name}

DESIGN TOKENS:
[CSS custom properties block from step 2]

TYPOGRAPHY:
[Scale table from step 3]

COMPONENT RULES:
[Styling rules from step 4]

INTERACTION PATTERNS:
[Patterns from step 5]

ENFORCEMENT:
- All colors must use CSS custom properties, not hardcoded hex values.
- All spacing must use the spacing scale variables.
- All border-radius must use radius variables.
- Typography must follow the defined scale. No arbitrary font sizes.
- Every component must match the styling rules above.
```

## Output Format

A complete brand identity constraint block formatted as a Lovable prompt prefix. Includes CSS custom properties, typography scale, component rules, and interaction patterns. Ready to prepend to any Lovable generation or refinement prompt to enforce brand consistency.

## Guardrails

- All colors must be defined as CSS custom properties, never hardcoded hex throughout components.
- Typography must follow the defined scale. No arbitrary font sizes outside the scale.
- Spacing must use the spacing scale. No magic numbers in margin/padding.
- Border radius must use radius variables. No component-specific overrides.
- Component styling must be consistent — same component type looks the same everywhere.
- Custom fonts must be loaded via Google Fonts or local files. Never reference fonts without ensuring they are imported.
- Dark mode variants must maintain the same brand identity. Generate dark-mode token overrides when dark mode is requested.
- Never use generic Tailwind colors (red-500, blue-600) for brand elements. Use brand token colors.

## Failure Handling

| Problem | Follow-up Prompt |
|---------|-----------------|
| Visual drift between pages | "Apply the brand token CSS variables globally. Replace all hardcoded colors with var(--brand-*). Ensure every page imports the same index.css token block." |
| Inconsistent button styles | "Standardize all buttons: primary uses bg-{primary} with white text, secondary uses border-{primary} with transparent bg. All use radius var(--radius-md) and min-height 40px." |
| Typography mismatch | "Apply the typography scale. Hero = display (3.5rem/700), page titles = h1 (2.5rem/700), section headers = h2 (2rem/600). Body text = 1rem/400. No arbitrary sizes." |
| Wrong fonts loading | "Import {heading_font} and {body_font} from Google Fonts in index.html or via @import in index.css. Apply --font-heading to all headings, --font-body to body text." |
| Spacing inconsistency | "Use spacing scale only: xs=4px, sm=8px, md=16px, lg=24px, xl=32px. Replace arbitrary margin/padding values. Section gaps use space-section (64px)." |

## Examples

### Example 1: Startup SaaS Brand

**Input**: `brand_name=LaunchPad`, `style=startup`, `palette=#6366f1,#f1f5f9,#f59e0b,#ffffff`, `fonts=Satoshi,Inter`

**Lovable prompt prefix**:
```
BRAND IDENTITY — LaunchPad

All UI must follow these constraints:

COLORS: Primary #6366f1 (indigo), Secondary #f1f5f9 (light gray), Accent #f59e0b (amber), Neutral #ffffff. Use CSS custom properties --brand-primary, --brand-secondary, --brand-accent throughout. No hardcoded colors.

TYPOGRAPHY: Headings use Satoshi (import from CDN). Body uses Inter. Scale: display 3.5rem/700, h1 2.5rem/700, h2 2rem/600, h3 1.5rem/600, body 1rem/400, small 0.875rem/400.

SPACING: Base unit 8px. xs=4, sm=8, md=16, lg=24, xl=32, section=64. No magic numbers.

RADIUS: Base 8px. Buttons and inputs 8px. Cards 16px. Badges/pills 9999px.

COMPONENTS: Primary buttons indigo bg + white text. Cards have 1px neutral border + 16px radius + 16px padding. Inputs have 8px radius + 40px height. Focus rings 2px indigo at 50% opacity.

INTERACTIONS: Button press scales to 0.98. Cards lift 2px on hover. Link hover shifts to indigo. Loading uses gray skeleton shimmers.
```

### Example 2: Editorial Publication

**Input**: `brand_name=The Chronicle`, `style=editorial`

**Lovable prompt prefix**:
```
BRAND IDENTITY — The Chronicle

COLORS: Primary #1a1a1a (black), Secondary #6b7280 (gray), Accent #b45309 (amber-brown), Neutral #f9fafb. Elegant, restrained palette. Use CSS custom properties.

TYPOGRAPHY: Headings use Playfair Display (serif). Body uses Source Serif Pro. Scale: display 3.5rem/700, h1 2.5rem/700, body 1rem/400 with 1.6 line-height for readability.

SPACING: Base unit 4px for tighter editorial layouts. Generous vertical rhythm between paragraphs.

RADIUS: 0px everywhere. Sharp corners for editorial aesthetic.

COMPONENTS: Minimal button styles — text buttons with underline, dark fill for primary CTA only. Cards use horizontal rule separators instead of border boxes. Thin 0.5px borders where needed.
```

## Security & Privacy

This skill generates text prompts only. It does not access external endpoints, transmit data, or execute code. All output is prompt text intended for the Lovable.dev platform.

## Trust Statement

This skill contains no executable scripts. It produces Lovable-compatible brand constraint prompts. It does not access the filesystem, network, or any external service.
