---
name: design-system-planning
description: Plan design systems - component libraries, design tokens, documentation strategies, versioning, governance, and adoption frameworks.
allowed-tools: Read, Glob, Grep, Task
---

# Design System Planning

Plan and architect design systems for consistent, scalable user interfaces.

## MANDATORY: Skill Loading First

Before answering ANY design system question:

2. Use established design system methodology (Nathan Curtis, Brad Frost)
3. Base all guidance on validated design system practices

## Design System Foundations

### What's in a Design System

| Layer | Purpose | Examples |
|-------|---------|----------|
| **Design Tokens** | Primitive values | Colors, spacing, typography |
| **Core Components** | Building blocks | Button, Input, Card |
| **Patterns** | Component combinations | Form, Navigation, Modal |
| **Templates** | Page layouts | Dashboard, Detail page |
| **Guidelines** | Usage documentation | When to use, accessibility |
| **Tooling** | Development support | Storybook, linting, testing |

### Atomic Design Methodology

```text
Atoms → Molecules → Organisms → Templates → Pages

Atoms:       Button, Input, Icon, Label
Molecules:   Form Field (Label + Input + Error)
Organisms:   Login Form (Fields + Button + Links)
Templates:   Auth Page Layout
Pages:       Login Page (Template + Real Content)
```

## Design Tokens

### Token Architecture

```text
├── Global Tokens (Primitives)
│   ├── colors.blue.500: "#3B82F6"
│   ├── spacing.4: "16px"
│   └── font.size.base: "16px"
│
├── Semantic Tokens (Aliases)
│   ├── color.text.primary: colors.gray.900
│   ├── color.background.surface: colors.white
│   └── spacing.component.padding: spacing.4
│
└── Component Tokens (Specific)
    ├── button.background.default: color.primary.main
    ├── button.padding.horizontal: spacing.4
    └── card.border.radius: radius.medium
```

### Token Implementation (.NET/CSS)

```csharp
// Token generation for .NET projects
public class DesignTokens
{
    public static class Colors
    {
        public static class Primary
        {
            public const string Main = "#3B82F6";
            public const string Light = "#60A5FA";
            public const string Dark = "#1D4ED8";
            public const string Contrast = "#FFFFFF";
        }

        public static class Semantic
        {
            public const string TextPrimary = "#111827";
            public const string TextSecondary = "#6B7280";
            public const string BackgroundSurface = "#FFFFFF";
            public const string BackgroundPage = "#F3F4F6";
            public const string BorderDefault = "#E5E7EB";
        }

        public static class Status
        {
            public const string Success = "#10B981";
            public const string Warning = "#F59E0B";
            public const string Error = "#EF4444";
            public const string Info = "#3B82F6";
        }
    }

    public static class Spacing
    {
        public const string Xs = "4px";
        public const string Sm = "8px";
        public const string Md = "16px";
        public const string Lg = "24px";
        public const string Xl = "32px";
        public const string Xxl = "48px";
    }

    public static class Typography
    {
        public static class FontSize
        {
            public const string Xs = "12px";
            public const string Sm = "14px";
            public const string Base = "16px";
            public const string Lg = "18px";
            public const string Xl = "20px";
            public const string Xxl = "24px";
            public const string Xxxl = "30px";
        }

        public static class FontWeight
        {
            public const string Normal = "400";
            public const string Medium = "500";
            public const string Semibold = "600";
            public const string Bold = "700";
        }

        public static class LineHeight
        {
            public const string Tight = "1.25";
            public const string Normal = "1.5";
            public const string Relaxed = "1.75";
        }
    }

    public static class Radius
    {
        public const string None = "0";
        public const string Sm = "2px";
        public const string Default = "4px";
        public const string Md = "6px";
        public const string Lg = "8px";
        public const string Xl = "12px";
        public const string Full = "9999px";
    }

    public static class Shadow
    {
        public const string Sm = "0 1px 2px 0 rgb(0 0 0 / 0.05)";
        public const string Default = "0 1px 3px 0 rgb(0 0 0 / 0.1)";
        public const string Md = "0 4px 6px -1px rgb(0 0 0 / 0.1)";
        public const string Lg = "0 10px 15px -3px rgb(0 0 0 / 0.1)";
    }
}
```

```css
/* CSS Custom Properties from tokens */
:root {
    /* Colors - Primitives */
    --color-blue-50: #EFF6FF;
    --color-blue-500: #3B82F6;
    --color-blue-600: #2563EB;
    --color-blue-700: #1D4ED8;

    /* Colors - Semantic */
    --color-primary-main: var(--color-blue-500);
    --color-primary-hover: var(--color-blue-600);
    --color-text-primary: var(--color-gray-900);
    --color-background-surface: var(--color-white);

    /* Spacing */
    --spacing-1: 4px;
    --spacing-2: 8px;
    --spacing-4: 16px;
    --spacing-6: 24px;
    --spacing-8: 32px;

    /* Typography */
    --font-size-sm: 14px;
    --font-size-base: 16px;
    --font-size-lg: 18px;
    --font-weight-medium: 500;
    --font-weight-bold: 700;
    --line-height-normal: 1.5;

    /* Component Tokens */
    --button-padding-x: var(--spacing-4);
    --button-padding-y: var(--spacing-2);
    --button-border-radius: var(--radius-md);
    --card-padding: var(--spacing-4);
    --input-height: 40px;
}
```

## Component Documentation

### Component Specification Template

````markdown
# Button Component

## Overview
Primary action trigger for user interactions.

## Anatomy
```

┌─────────────────────────────────────┐
│  [Icon]  Label Text  [Icon]         │
│                                     │
│  ← padding-x →     ← padding-x →    │
└─────────────────────────────────────┘

```

## Variants

| Variant | Use Case |
|---------|----------|
| Primary | Main actions, CTAs |
| Secondary | Alternative actions |
| Tertiary | Low-emphasis actions |
| Destructive | Dangerous/irreversible actions |

## States
- Default
- Hover
- Active/Pressed
- Focus
- Disabled
- Loading

## Sizes
| Size | Height | Font Size | Icon Size |
|------|--------|-----------|-----------|
| Small | 32px | 14px | 16px |
| Medium | 40px | 16px | 20px |
| Large | 48px | 18px | 24px |

## Props/API

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| variant | enum | primary | Visual style |
| size | enum | medium | Button size |
| disabled | boolean | false | Disabled state |
| loading | boolean | false | Loading state |
| iconLeft | ReactNode | - | Left icon |
| iconRight | ReactNode | - | Right icon |
| fullWidth | boolean | false | Full container width |

## Accessibility
- Use `<button>` element for actions
- Ensure visible focus state
- Minimum touch target: 44x44px
- Provide aria-label if icon-only
- Use aria-busy for loading state

## Do's and Don'ts

### Do
✓ Use verb-based labels ("Save", "Submit")
✓ Limit to one primary button per view
✓ Maintain sufficient contrast

### Don't
✗ Use vague labels ("Click here")
✗ Disable without explanation
✗ Use for navigation (use Link)

## Examples

### Basic Usage
```razor
<Button variant="primary">Save Changes</Button>
```

### With Icons

```razor
<Button variant="secondary" iconLeft="@Icons.Plus">
    Add Item
</Button>
```

### Loading State

```razor
<Button loading="@isSubmitting" disabled="@isSubmitting">
    @(isSubmitting ? "Saving..." : "Save")
</Button>
```

## Related Components

- ButtonGroup - Grouping related buttons
- IconButton - Icon-only buttons
- Link - For navigation

````

### Blazor Component Implementation

```csharp
@namespace DesignSystem.Components

<button
    type="@Type"
    class="@ComputedClass"
    disabled="@(Disabled || Loading)"
    aria-busy="@Loading.ToString().ToLower()"
    @onclick="HandleClick"
    @attributes="AdditionalAttributes">

    @if (Loading)
    {
        <span class="btn-spinner" aria-hidden="true"></span>
        <span class="visually-hidden">Loading</span>
    }

    @if (IconLeft is not null && !Loading)
    {
        <span class="btn-icon btn-icon-left" aria-hidden="true">
            @IconLeft
        </span>
    }

    <span class="btn-label">@ChildContent</span>

    @if (IconRight is not null)
    {
        <span class="btn-icon btn-icon-right" aria-hidden="true">
            @IconRight
        </span>
    }
</button>

@code {
    [Parameter] public RenderFragment? ChildContent { get; set; }
    [Parameter] public ButtonVariant Variant { get; set; } = ButtonVariant.Primary;
    [Parameter] public ButtonSize Size { get; set; } = ButtonSize.Medium;
    [Parameter] public bool Disabled { get; set; }
    [Parameter] public bool Loading { get; set; }
    [Parameter] public bool FullWidth { get; set; }
    [Parameter] public RenderFragment? IconLeft { get; set; }
    [Parameter] public RenderFragment? IconRight { get; set; }
    [Parameter] public string Type { get; set; } = "button";
    [Parameter] public EventCallback<MouseEventArgs> OnClick { get; set; }
    [Parameter(CaptureUnmatchedValues = true)]
    public Dictionary<string, object>? AdditionalAttributes { get; set; }

    private string ComputedClass => new CssBuilder("btn")
        .AddClass($"btn-{Variant.ToString().ToLower()}")
        .AddClass($"btn-{Size.ToString().ToLower()}")
        .AddClass("btn-full-width", FullWidth)
        .AddClass("btn-loading", Loading)
        .AddClass("btn-disabled", Disabled)
        .Build();

    private async Task HandleClick(MouseEventArgs args)
    {
        if (!Disabled && !Loading)
        {
            await OnClick.InvokeAsync(args);
        }
    }
}
```

## Design System Maturity Model

### Maturity Levels

| Level | Characteristics | Focus |
|-------|-----------------|-------|
| **1. Inconsistent** | No shared language, silos | Identify patterns |
| **2. Foundation** | Tokens, basic components | Establish core library |
| **3. Documented** | Guidelines, Storybook | Document patterns |
| **4. Integrated** | CI/CD, versioning | Scale adoption |
| **5. Evolved** | Governance, contributions | Continuous improvement |

### Maturity Assessment

```csharp
public class DesignSystemMaturity
{
    public record MaturityScore(
        int Foundations,      // Tokens, primitives
        int Components,       // Component coverage
        int Documentation,    // Guidelines, examples
        int Tooling,          // Dev tools, testing
        int Governance,       // Process, contribution
        int Adoption          // Team usage
    )
    {
        public decimal OverallScore => (Foundations + Components + Documentation +
            Tooling + Governance + Adoption) / 6m;

        public MaturityLevel Level => OverallScore switch
        {
            >= 4.5m => MaturityLevel.Evolved,
            >= 3.5m => MaturityLevel.Integrated,
            >= 2.5m => MaturityLevel.Documented,
            >= 1.5m => MaturityLevel.Foundation,
            _ => MaturityLevel.Inconsistent
        };
    }

    public enum MaturityLevel
    {
        Inconsistent = 1,
        Foundation = 2,
        Documented = 3,
        Integrated = 4,
        Evolved = 5
    }
}
```

## Versioning Strategy

### Semantic Versioning for Design Systems

```text
MAJOR.MINOR.PATCH

MAJOR: Breaking changes (renamed tokens, removed components)
MINOR: New features (new components, new variants)
PATCH: Bug fixes (visual fixes, docs updates)
```

### Change Categories

| Category | Version Impact | Example |
|----------|----------------|---------|
| New component | Minor | Add DatePicker |
| New variant | Minor | Add "ghost" button |
| Token rename | Major | `color-primary` → `color-brand` |
| Token value change | Minor or Patch | Adjust blue shade |
| API change | Major | Rename prop |
| Bug fix | Patch | Fix focus ring |
| Deprecation | Minor | Deprecate v1 API |
| Removal | Major | Remove deprecated API |

### Changelog Template

```markdown
# Changelog

## [2.0.0] - 2025-01-15

### ⚠️ Breaking Changes
- **tokens**: Renamed `color-primary-*` to `color-brand-*`
- **Button**: Removed `type` prop, use `variant` instead

### 🚀 Added
- **DatePicker**: New date picker component
- **Button**: Added `ghost` variant
- **tokens**: Added dark mode tokens

### 🔧 Changed
- **Card**: Updated padding to use new spacing tokens
- **Input**: Improved focus ring visibility

### 🐛 Fixed
- **Modal**: Fixed focus trap for keyboard navigation
- **Select**: Fixed dropdown positioning in scrollable containers

### 📚 Documentation
- Added migration guide from v1 to v2
- New accessibility guidelines section

### ⚠️ Deprecated
- **Button**: `primary` variant renamed to `brand` (removal in v3)
```

## Governance Model

### Contribution Workflow

```text
1. Proposal → 2. Review → 3. Design → 4. Build → 5. Document → 6. Release

Proposal:    Submit RFC with use case and requirements
Review:      Design system team evaluates fit
Design:      Create specs, get design approval
Build:       Implement with tests
Document:    Write guidelines, examples
Release:     Version, publish, communicate
```

### RFC Template

```markdown
# RFC: [Component/Feature Name]

## Summary
Brief description of the proposed change.

## Motivation
Why is this needed? What problem does it solve?

## Use Cases
1. [Use case 1]
2. [Use case 2]

## Proposed Solution
### Design
[Screenshots, Figma links]

### API
[Props, tokens, usage examples]

### Accessibility
[WCAG considerations]

## Alternatives Considered
[Other approaches and why they were rejected]

## Open Questions
[Unresolved decisions]

## Adoption Strategy
[How will teams migrate/adopt]
```

### Decision Log

```csharp
public class DesignDecision
{
    public required string Id { get; init; }
    public required string Title { get; init; }
    public required DateOnly Date { get; init; }
    public required string Context { get; init; }
    public required string Decision { get; init; }
    public required string Rationale { get; init; }
    public required List<string> Alternatives { get; init; }
    public required DecisionStatus Status { get; init; }
    public List<string> Supersedes { get; init; } = [];
    public string? SupersededBy { get; init; }
}

public enum DecisionStatus
{
    Proposed,
    Accepted,
    Superseded,
    Deprecated
}
```

## Design-to-Code Workflow

### Figma to Code Pipeline

```text
Figma Design
    ↓
Token Export (Figma Tokens plugin)
    ↓
Token Transformation (Style Dictionary)
    ↓
Generated CSS/Code
    ↓
Component Implementation
    ↓
Storybook Stories
    ↓
Visual Regression Tests
    ↓
Published Package
```

### Token Transformation Config

```json
// style-dictionary.config.json
{
  "source": ["tokens/**/*.json"],
  "platforms": {
    "css": {
      "transformGroup": "css",
      "buildPath": "dist/css/",
      "files": [{
        "destination": "tokens.css",
        "format": "css/variables"
      }]
    },
    "scss": {
      "transformGroup": "scss",
      "buildPath": "dist/scss/",
      "files": [{
        "destination": "_tokens.scss",
        "format": "scss/variables"
      }]
    },
    "csharp": {
      "transformGroup": "csharp",
      "buildPath": "dist/csharp/",
      "files": [{
        "destination": "DesignTokens.cs",
        "format": "csharp/class"
      }]
    }
  }
}
```

## Adoption Metrics

### Tracking Adoption

| Metric | What to Measure | Target |
|--------|-----------------|--------|
| **Coverage** | % of UI using DS components | >80% |
| **Adoption** | Teams actively using DS | 100% |
| **Contribution** | PRs from consuming teams | Growing |
| **Support** | Questions, issues filed | Decreasing |
| **Consistency** | Design audit score | >90% |

```csharp
public class AdoptionMetrics
{
    public required decimal ComponentCoverage { get; init; }
    public required int TeamsAdopted { get; init; }
    public required int TotalTeams { get; init; }
    public required int ContributionsPastQuarter { get; init; }
    public required int OpenIssues { get; init; }
    public required decimal ConsistencyScore { get; init; }

    public decimal AdoptionRate => TeamsAdopted / (decimal)TotalTeams * 100;
}
```

## Checklist: Design System Planning

### Strategy

- [ ] Goals and success metrics defined
- [ ] Target audience identified
- [ ] Scope determined (which products)
- [ ] Team and governance established
- [ ] Tech stack decided

### Foundation

- [ ] Design tokens defined
- [ ] Color system established
- [ ] Typography scale set
- [ ] Spacing system created
- [ ] Grid system defined

### Components

- [ ] Component audit completed
- [ ] Priority components identified
- [ ] Component specs created
- [ ] Accessibility requirements defined
- [ ] Implementation approach decided

### Documentation

- [ ] Documentation platform chosen
- [ ] Component documentation template
- [ ] Usage guidelines written
- [ ] Example code provided
- [ ] Contribution guide created

### Tooling

- [ ] Design tool integration (Figma)
- [ ] Storybook or equivalent
- [ ] Visual regression testing
- [ ] Linting rules
- [ ] CI/CD pipeline

### Governance

- [ ] Versioning strategy
- [ ] Release process
- [ ] RFC/proposal process
- [ ] Support model
- [ ] Feedback channels

## Related Skills

- `accessibility-planning` - Accessible components
- `prototype-strategy` - Prototyping with design system
- `heuristic-evaluation` - Evaluating consistency
- `information-architecture` - Navigation patterns
