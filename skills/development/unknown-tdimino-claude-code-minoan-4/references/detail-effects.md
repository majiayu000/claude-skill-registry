# Detail Effects (Effects #12-16)

## SVG Gradient Icons (#12)

```html
<svg width="20" height="20" viewBox="0 0 20 20" fill="none" role="presentation">
    <defs>
        <linearGradient id="gold-grad" x1="0.209" x2="0.791" y1="0" y2="1">
            <stop offset="0" stop-color="#FFF9E7"/>
            <stop offset="1" stop-color="#BA8B4D"/>
        </linearGradient>
    </defs>
    <path d="M10 2L12.5 7.5L18 8.5L14 12.5L15 18L10 15.5L5 18L6 12.5L2 8.5L7.5 7.5L10 2Z" fill="url(#gold-grad)"/>
</svg>
```

Lime gradient: stops `#AADB1F` → `#C2F13C`, x1="0.608" x2="0.392" y1="1" y2="0".

Always: `role="presentation"`, `display: block`.

## Inset Border System (#13)

```css
/* Single-side inset border via box-shadow */
.card-border { box-shadow: inset 0 -1px 0 0 var(--grn-border); }

/* Full inset border */
.card-border-full { box-shadow: inset 0 0 0 1px var(--grn-border-subtle); }
```

Not standard CSS `border` — avoids box model changes.

## Grid Pattern Overlay (#14)

```css
.grid-overlay {
    position: fixed; inset: 0; z-index: 3;
    pointer-events: none;
    background-image:
        repeating-linear-gradient(0deg, var(--grn-accent-20) 0, var(--grn-accent-20) 1px, transparent 1px, transparent 100px),
        repeating-linear-gradient(90deg, var(--grn-accent-20) 0, var(--grn-accent-20) 1px, transparent 1px, transparent 100px);
}
```

Very subtle — opacity 0.1-0.2. Optional on content-heavy pages.

## Custom Scrollbar (#15)

```css
/* Webkit */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--grn-text-20); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--grn-text-40); }

/* Firefox */
html { scrollbar-width: thin; scrollbar-color: var(--grn-text-20) transparent; }
```

Always include both. Default scrollbar breaks the dark aesthetic.

## Responsive Clamp Typography (#16)

```css
/* Hero */       font-size: clamp(32px, 4vw + 1rem, 6vw);     line-height: 1.1;
/* Subheading */ font-size: clamp(20px, 2vw + 0.5rem, 3vw);   line-height: 1.3;
/* Body */       font-size: clamp(16px, 1vw + 1rem, 1.1vw);   line-height: 1.5;
/* Display */    font-size: clamp(48px, 6vw + 2rem, 100px);    line-height: 1.0;
```

Font weights: 400 (body), 500 (headings), 600 (emphasis/buttons).

Always: `-webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale;`
