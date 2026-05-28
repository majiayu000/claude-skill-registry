---
name: Rugged Utility
description: LivestockAI's design philosophy for field-ready, farmer-friendly UI
---

# Rugged Utility

LivestockAI is built for farmers in the field - often on dusty phones with cracked screens, under bright sunlight, with dirty hands. Every UI decision prioritizes **usability over aesthetics**.

## Touch Targets

All interactive elements MUST meet minimum sizes:

| Element           | Minimum Size    | Rationale             |
| ----------------- | --------------- | --------------------- |
| Buttons           | 48px height     | Fat finger friendly   |
| Action Grid items | 64px × 64px     | Field use with gloves |
| Form inputs       | 44px height     | Easy tap targets      |
| List items        | 48px row height | Scrollable lists      |
| Icon buttons      | 44px × 44px     | Toolbar actions       |

## Signal Palette

| Color        | CSS Variable    | Usage                               |
| ------------ | --------------- | ----------------------------------- |
| Forest Green | `--success`     | Growth, revenue, healthy batches    |
| Amber        | `--warning`     | Alerts, low stock, attention needed |
| Red          | `--destructive` | Mortality, losses, critical issues  |
| Neutral      | `--muted`       | Data, secondary information         |
| Primary      | `--primary`     | Actions, CTAs (Emerald brand)       |

## Health Pulse Card

Color-coded status at a glance:

```
┌─────────────────────────────────────────────┐
│ 🟢 ON TRACK                                  │
│ Mortality: 2.1% • FCR: 1.8 • Weight: 1.2kg  │
└─────────────────────────────────────────────┘
```

States:

- 🟢 **Green**: All metrics within targets
- 🟡 **Amber**: One metric needs attention
- 🔴 **Red**: Critical - immediate action required

## Action Grid

High-frequency actions as large touch targets:

```
┌──────────┬──────────┬──────────┐
│   🍗     │    💀    │    💰    │
│  Feed    │  Death   │   Sale   │
├──────────┼──────────┼──────────┤
│   ⚖️     │    💉    │    💧    │
│  Weigh   │   Vax    │  Water   │
└──────────┴──────────┴──────────┘
```

- 2×3 or 3×2 grid depending on screen
- Icons + labels always visible
- Each cell minimum 64px × 64px

## Typography

| Element    | Size | Weight   | Usage               |
| ---------- | ---- | -------- | ------------------- |
| Page title | 24px | Bold     | Route headers       |
| Card title | 18px | Semibold | Card headers        |
| Body       | 16px | Regular  | Content             |
| Caption    | 14px | Regular  | Secondary text      |
| Label      | 12px | Medium   | Form labels, badges |

## Error States

```
┌─────────────────────────────────────────────┐
│ ⚠️ Failed to save feed record               │
│                                              │
│ Check your connection and try again.         │
│                                              │
│ [Retry]                      [Save Offline]  │
└─────────────────────────────────────────────┘
```

- Clear error message
- Actionable recovery options
- Offline fallback when applicable

## Related Skills

- `batch-centric-design` - Batch-focused UI patterns
- `offline-first` - Offline indicators
