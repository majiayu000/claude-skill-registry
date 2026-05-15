# Composability

## Layer Stack

```
Layer 0  z-index: 0    Body background (--grn-bg)
Layer 1  z-index: 1    Shader gradient canvas (position: fixed)
Layer 2  z-index: 2    Vignette overlay (position: fixed, pointer-events: none)
Layer 3  z-index: 3    Grid pattern overlay (position: fixed, pointer-events: none)
Layer 4  z-index: 10   Content sections (position: relative)
Layer 5  z-index: 100  Glassmorphism nav (position: fixed)
```

## Composition Recipes

| Recipe | Effects | Template |
|--------|---------|----------|
| Cinematic Hero | #1 shader + #2 vignette + #8 glassmorphism + #16 clamp typo | `hero-section.html` |
| Dark Showcase | #10 bento + #3 shadows + #6 hover zoom + #11 CTAs | `bento-showcase.html` |
| Scrolling Ticker | #7 ticker + #4 smooth scroll + #11 CTAs + #2 vignette | `ticker-landing.html` |
| Full Grainient | All 16 effects | `dark-page.html` |
| Minimal Dark | #13 borders + #16 typography + #15 scrollbar | CSS-only, no JS |

## Performance Budget

| Component | Frame Cost |
|-----------|-----------|
| CSS effects (vignette, shadows, borders) | 0ms JS |
| Smooth scroll | ~0.5ms/frame |
| Ticker marquee | ~0.3ms/frame |
| Shader gradient | ~1-3ms/frame |
| Spring animations | ~0.1ms/event |
| **Total** | **<8ms for 120fps** |

## Rules

- One shader canvas per page max
- Vignette always accompanies shader canvas
- Glassmorphism nav always at z-index: 100
- Content sections use relative positioning above fixed layers
- Grid overlay is optional — omit on content-heavy pages
- Smooth scroll initializes once, not per section
