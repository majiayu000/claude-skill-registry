# 9-Layer Box Shadow System (Effect #3)

Deep multi-layer shadows for "floating card" elevation on dark backgrounds.

## Lime Glow Variant (Featured Cards)

```css
box-shadow:
    inset 0px 0.5px 0.5px 0px rgb(255,255,255),       /* inner highlight */
    0px 70px 30px 0px rgba(0,0,0,0.05),                /* far ambient */
    0px 40px 25px 0px rgba(0,0,0,0.25),                /* mid ambient */
    0px 20px 20px 0px rgba(0,0,0,0.25),                /* near ambient */
    0px 5px 10px 0px rgba(0,0,0,0.35),                 /* contact shadow */
    0px 0px 0px 0.7px rgba(0,0,0,0.35),                /* border ring */
    0px -5px 30px 0px var(--grn-accent-20),             /* glow UP */
    0px -1px 3px 0px var(--grn-accent-20),              /* glow tight */
    0px 1px 0px 2px var(--grn-accent-20);               /* glow bottom */
```

## White Glow Variant

Replace accent glow layers with `rgba(255,255,255,0.08)`.

## CTA Inset Glow

```css
box-shadow: inset 0 0 3px white, 0 0 40px var(--grn-accent-20);
```

## Simple Inset Border

```css
box-shadow: inset 0 0 0 1px var(--grn-border-subtle);
```

## Anatomy

| Layer | Role |
|-------|------|
| 1 (inset) | Inner highlight — subtle white edge |
| 2-5 | Ambient shadows at increasing distance |
| 6 | Border ring — thin dark outline |
| 7-9 | Colored glow (up, tight, bottom) |

## Rules

- Minimum 4 layers — fewer looks flat on dark backgrounds
- On pure black (#000), shadows are invisible unless colored
- Use `will-change: transform` on shadowed elements for GPU compositing
- Avoid on >20 elements simultaneously — performance cost
