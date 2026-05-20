---
name: mermaid
description: Guide for creating beautiful Mermaid diagrams with proper styling for GitHub markdown (dark/light mode compatible, no icons).
---

# Mermaid Diagram Skill

This skill provides guidance on creating beautiful, professional Mermaid diagrams that render correctly on GitHub and work well in both light and dark mode.

## Core Principles

1. **Use dark fills with light strokes** — Ensures readability in both light and dark mode
2. **Set subgraph fills to `none`** — Allows subgraphs to adapt to any background
3. **Use rounded shapes** — `([text])` for stadium shapes, `((text))` for circles
4. **No Font Awesome icons** — GitHub doesn't support `fa:fa-*` icons, they render as text
5. **Quote subgraph labels** — Use `subgraph Name["Label Text"]` syntax
6. **Define classDef styles at the top** — Keep all styling together for maintainability

## The Golden Rule: Dark Fills + Light Strokes

The key insight for dark/light mode compatibility:

```
classDef myStyle fill:#DARK_COLOUR,stroke:#LIGHT_COLOUR,stroke-width:2px,color:#fff
```

- **Fill**: Use a darker shade (the node background)
- **Stroke**: Use a lighter shade of the same colour family (the border)
- **Color**: Always `#fff` (white text on dark background)

This approach ensures nodes are readable regardless of the page background.

## GitHub-Compatible Template

This is the canonical template for GitHub-rendered Mermaid diagrams:

```mermaid
flowchart TD
    %% --- COLOUR PALETTE & STYLING ---
    %% Dark fills + light strokes = readable in both light and dark mode
    classDef user fill:#374151,stroke:#d1d5db,stroke-width:2px,color:#fff
    classDef primary fill:#5b21b6,stroke:#ddd6fe,stroke-width:2px,color:#fff
    classDef secondary fill:#1e40af,stroke:#bfdbfe,stroke-width:2px,color:#fff
    classDef accent fill:#c2410c,stroke:#fed7aa,stroke-width:2px,color:#fff
    classDef success fill:#047857,stroke:#a7f3d0,stroke-width:2px,color:#fff

    %% --- NODES ---
    User((User)):::user
    User --> Action(["Performs action"]):::user

    Action --> Primary

    subgraph Primary["Primary Component"]
        direction TB
        Step1(["Step 1"]):::primary
        Step2(["Step 2"]):::primary
        Step1 --> Step2
    end

    subgraph Secondary["Secondary Component"]
        direction TB
        Process(["Process"]):::secondary
    end

    Primary --> Secondary
    Secondary --> Output(["Output"]):::success

    %% --- SUBGRAPH STYLES ---
    %% fill:none allows subgraphs to adapt to any background
    style Primary fill:none,stroke:#8b5cf6,stroke-width:2px,stroke-dasharray:5 5,color:#8b5cf6
    style Secondary fill:none,stroke:#3b82f6,stroke-width:2px,color:#3b82f6
```

## Colour Pairing Examples

Choose any colours you like — just follow the dark fill + light stroke pattern:

| Fill (Dark) | Stroke (Light) | Result |
|-------------|----------------|--------|
| `#374151` | `#d1d5db` | Grey |
| `#5b21b6` | `#ddd6fe` | Purple |
| `#1e40af` | `#bfdbfe` | Blue |
| `#c2410c` | `#fed7aa` | Orange |
| `#047857` | `#a7f3d0` | Green |
| `#b91c1c` | `#fecaca` | Red |
| `#0f766e` | `#99f6e4` | Teal |

These are just examples. Use whatever colours suit your diagram — the principle is what matters.

## Subgraph Syntax

### ❌ WRONG — Causes parse error
```mermaid
subgraph MyGroup [Label With Spaces]
```

### ✅ CORRECT — Quote the label
```mermaid
subgraph MyGroup["Label With Spaces"]
```

## Node Shapes

### ❌ WRONG — Square brackets are harsh
```mermaid
A[Square Node]
```

### ✅ CORRECT — Use rounded shapes
```mermaid
A(["Stadium shape"])     %% Rounded ends - use for most nodes
B((Circle))              %% Circle - use for users/actors
C{{"Decision"}}          %% Hexagon for decisions
D[(Database)]            %% Cylinder for databases/storage
```

## Subgraph Styling

### ❌ WRONG — Coloured fills break in dark mode
```mermaid
style MySubgraph fill:#f0f9ff,stroke:#3182ce
```

### ✅ CORRECT — Transparent fills adapt to any background
```mermaid
style MySubgraph fill:none,stroke:#8b5cf6,stroke-width:2px,stroke-dasharray:5 5,color:#8b5cf6
```

**Key points:**
- `fill:none` makes the background transparent
- `stroke-dasharray:5 5` creates a dashed border (optional, looks clean)
- `color:#...` sets the subgraph label colour to match the border

## Link Styling

```mermaid
A --> B              %% Solid arrow
A -.-> B             %% Dashed arrow
A -.->|Label| B      %% Dashed arrow with label
A ==> B              %% Thick arrow
```

## Complete Example

```mermaid
flowchart TD
    classDef user fill:#374151,stroke:#d1d5db,stroke-width:2px,color:#fff
    classDef process fill:#5b21b6,stroke:#ddd6fe,stroke-width:2px,color:#fff
    classDef decision fill:#c2410c,stroke:#fed7aa,stroke-width:2px,color:#fff
    classDef success fill:#047857,stroke:#a7f3d0,stroke-width:2px,color:#fff

    User((User)):::user
    User --> Request(["Makes request"]):::user

    Request --> Process

    subgraph Process["Processing"]
        direction TB
        Validate(["Validate input"]):::process
        Execute(["Execute logic"]):::process
        Validate --> Execute
    end

    Execute --> Check{{"Success?"}}:::decision
    Check -->|Yes| Done(["Complete"]):::success
    Check -->|No| Request

    style Process fill:none,stroke:#8b5cf6,stroke-width:2px,stroke-dasharray:5 5,color:#8b5cf6
```

## Common Mistakes

### ❌ Font Awesome icons (GitHub doesn't support them)
```mermaid
A[fa:fa-user User]  %% Renders as literal text
```

### ❌ Light fills with dark text
```mermaid
classDef bad fill:#ffffff,stroke:#000000,color:#000000  %% Invisible in dark mode
```

### ❌ Coloured subgraph fills
```mermaid
style Sub fill:#e0f2fe  %% Looks different in light vs dark mode
```

### ❌ Unquoted subgraph labels with spaces
```mermaid
subgraph Sub [My Label]  %% Parse error!
```

## Quick Reference

```mermaid
flowchart TD
    %% 1. Define styles: dark fill + light stroke + white text
    classDef myStyle fill:#DARK,stroke:#LIGHT,stroke-width:2px,color:#fff

    %% 2. Use rounded shapes
    Node(["Text"]):::myStyle

    %% 3. Quote subgraph labels
    subgraph Sub["My Label"]
        Inner(["Inner"])
    end

    %% 4. Style subgraphs with fill:none
    style Sub fill:none,stroke:#COLOR,stroke-width:2px,color:#COLOR
```

## When to Use This Skill

Invoke this skill when creating:
- Architecture diagrams for PRs
- System flow documentation
- Data pipeline visualisations
- Process flowcharts
- Any diagram in GitHub markdown

## GitHub-Specific Notes

1. **No Font Awesome** — GitHub's Mermaid renderer doesn't support FA icons
2. **No HTML** — Can't use `<br>` or other HTML in node labels
3. **Quote labels with spaces** — `subgraph X["Label"]` not `subgraph X [Label]`
4. **Test locally** — Use [mermaid.live](https://mermaid.live) to preview before committing
