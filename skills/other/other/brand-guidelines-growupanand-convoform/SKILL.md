---
name: resend-brand
description: Use when creating Resend marketing materials, documents, presentations, or visual content. Triggers for Resend brand, Resend style, or Resend visual identity requests.
metadata:
  author: resend
  version: "1.0.0"
---

# Resend Brand Guidelines

## Core Colors

| Name         | Hex       |
| ------------ | --------- |
| Resend Black | `#000000` |
| Resend White | `#FDFDFD` |

### Semantic Colors

| Scale | Background  | Foreground  | Usage                                       |
| ----- | ----------- | ----------- | ------------------------------------------- |
| Gray  | `#16171AEB` | `#FDFEFFA6` | Structure, hierarchy, and subtle separation |
| Red   | `#FF173F2D` | `#FF9592`   | Critical states and irreversible actions    |
| Amber | `#FA820022` | `#FFCA16`   | Caution and pending states                  |
| Green | `#22FF991E` | `#46FEA5D4` | Success and completion                      |
| Blue  | `#0077FF3A` | `#70B8FF`   | Interactive and informational elements      |

## Typography

| Font                       | Role                                    |
| -------------------------- | --------------------------------------- |
| **Domaine Display Narrow** | Display headlines (never in product UI) |
| **Favorit**                | Headings & titles                       |
| **Inter**                  | Body text                               |
| **CommitMono**             | Code                                    |

### Typography Rules

- Use **sentence case** everywhere (headings, buttons, labels, navigation)
- Never use the Domaine font in bold
- Never use monospace for titles or body copy
- Never replace brand fonts with alternatives

### Typography Scale

**Display**
| Style | Font | Size/Line | Letter Spacing |
|-------|------|-----------|----------------|
| display/large | Domaine Display Narrow | 96/96 | -0.96px |
| title | Resend Favorit | 60/64 | -2.8px |
| small | Domaine Display Narrow | 72/72 | -0.77px |

**Body**
| Style | Font | Weight | Size/Line |
|-------|------|--------|-----------|
| xlarge | Resend Favorit | Regular | 24/32 |
| large | Inter | Regular/Medium | 18/28 |
| medium | Inter | Regular/Medium/Semi Bold | 16/24 |
| small | Inter | Regular | 14/20 |
| code | CommitMono | Regular | 14/20 |

## Logo

**Wordmark**

- `https://cdn.resend.com/brand/resend-wordmark-white.svg`
- `https://cdn.resend.com/brand/resend-wordmark-white.png`
- `https://cdn.resend.com/brand/resend-wordmark-black.svg`
- `https://cdn.resend.com/brand/resend-wordmark-black.png`

**Lettermark**

- `https://cdn.resend.com/brand/resend-icon-white.svg`
- `https://cdn.resend.com/brand/resend-icon-white.png`
- `https://cdn.resend.com/brand/resend-icon-black.svg`
- `https://cdn.resend.com/brand/resend-icon-black.png`

### Clearspace

Minimum clear space = 1/2 cap height on all sides

### Minimum Size

- Preferred: 24px height
- Extreme cases: 16px height minimum

### Logo Restrictions

Never: rotate, apply effects, outline, slant/stretch, use multiple colors, use low resolution, combine symbol+wordmark, modify proportions

## Cube Element

Secondary brand symbol. Never use as: primary logo, navigation element, or with modified geometry/colors.

## Gradients

| Name            | Value                                                                                                    |
| --------------- | -------------------------------------------------------------------------------------------------------- |
| Font gradient   | `linear-gradient(97deg, #ffffff 30%, rgba(255,255,255,0.50) 100%)`                                       |
| Smooth gradient | `linear-gradient(96deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.10) 100%)`                         |
| Border          | `linear-gradient(180deg, rgba(255,255,255,0.10) 0%, rgba(255,255,255,0.05) 100%)`                        |
| Rainbow border  | `linear-gradient(90deg, rgba(2,252,239,0.44) 0%, rgba(255,181,43,0.44) 50%, rgba(160,43,254,0.44) 100%)` |

## Effects

| Name       | Value                         |
| ---------- | ----------------------------- |
| Glass blur | `backdrop-filter: blur(25px)` |

## Textures

- **Noise**: Hero backgrounds, atmospheric depth
  `https://resend.com/static/product-pages/noise.png`

## Backgrounds

Brand wallpapers available at: https://resend.com/wallpapers

## Layout Patterns

| Name                 | Description                                                           |
| -------------------- | --------------------------------------------------------------------- |
| Right Object Scene   | Small label top-left, title top-left (2 lines), 3D object right       |
| Interface Scene      | Label top-left, title bottom-left (2 lines), UI screenshot background |
| Text Only Scene      | Title top-left, 3D abstract scene fills background                    |
| Text Only Background | Large title centered, subtle texture/gradient background              |
| Text Only Subtle     | Small centered text (2 lines), minimal dark background                |
| Big Number           | Large display number centered (Domaine), small label below            |

**Common patterns:**

- Label/category always small, top-left or top-center
- Titles use 2-line breaks for rhythm
- Titles are never longer than 3 lines.
- Objects positioned right, left, or as full background
- Dark backgrounds with subtle depth

## Design Principles

1. Dark-first design philosophy
2. Sharp contrast between black and light
3. Precision and focus over decoration
4. Accent colors communicate state, not style
5. Simple, stable, intentional forms
