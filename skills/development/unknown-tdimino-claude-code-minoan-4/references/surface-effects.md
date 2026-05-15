# Surface Effects (Effects #8-11)

## Glassmorphism (#8)

3 blur tiers:

```css
/* Light — subtle overlays */
.glass-light {
    backdrop-filter: var(--grn-blur-light);  /* blur(5px) */
    background: rgba(0, 0, 0, 0.4);
}

/* Medium — panels */
.glass-medium {
    backdrop-filter: var(--grn-blur-medium);  /* blur(10px) */
    background: rgba(0, 0, 0, 0.6);
}

/* Heavy — navigation */
.glass-heavy {
    backdrop-filter: var(--grn-blur-heavy);  /* blur(20px) */
    background: rgba(0, 0, 0, 0.7);
    border-bottom: 1px solid var(--grn-border-subtle);
}
```

Critical: background MUST be semi-transparent or blur is invisible on dark.

## 3D Perspective Card Flip (#9)

```css
.perspective-container { perspective: 1200px; overflow: visible; }

.flip-card {
    will-change: transform;
    transform: rotateY(90deg);
    transition: transform 0.8s var(--grn-spring-smooth);
}
.flip-card.active { transform: rotateY(0); }
```

Stagger cards with `translateY` offsets (10-30px each).

Critical: `overflow: visible` on container — clip breaks 3D rotation.

## Bento Grid (#10)

```css
.bento-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
}

.bento-card {
    background: var(--grn-surface);
    border-radius: 20px;
    padding: 28px;
    box-shadow: inset 0 0 0 1px var(--grn-border-subtle);
}

.bento-card--span2 { grid-column: span 2; }
.bento-card--tall { grid-row: span 2; }
```

Responsive: collapse to `grid-template-columns: 1fr` on mobile.

## Gradient CTAs (#11)

```css
.btn-primary {
    padding: 12px 28px;
    font-weight: 600; color: #000;
    border: none; border-radius: 50px;
    background: linear-gradient(180deg, #EBFFB4, var(--grn-accent));
    box-shadow: inset 0 0 3px white, 0 0 40px var(--grn-accent-20);
    transition: filter 0.4s var(--grn-spring-snappy),
                transform 0.4s var(--grn-spring-snappy);
}
.btn-primary:hover { filter: brightness(1.1); transform: scale(1.03); }
.btn-primary:active { transform: scale(0.98); }

.btn-secondary {
    padding: 12px 28px;
    font-weight: 500; color: var(--grn-text);
    background: transparent;
    border: 1px solid var(--grn-border);
    border-radius: 50px;
}
.btn-secondary:hover { background-color: var(--grn-text-10); }
```
