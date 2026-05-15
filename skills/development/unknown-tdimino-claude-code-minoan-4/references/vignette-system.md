# Vignette Overlay System (Effect #2)

4 absolutely-positioned divs creating a cinematic frame around content. Always pair with shader canvas.

## HTML Structure

```html
<div class="vignette vignette--top"></div>
<div class="vignette vignette--bottom"></div>
<div class="vignette vignette--left"></div>
<div class="vignette vignette--right"></div>
```

## CSS

```css
.vignette {
    position: fixed;
    z-index: 2;
    pointer-events: none;
}

.vignette--top {
    inset: 0 0 auto 0;
    height: 30%;
    background: linear-gradient(0deg, transparent 0%, var(--grn-surface) 100%);
}

.vignette--bottom {
    inset: auto 0 0 0;
    height: 30%;
    background: linear-gradient(180deg, transparent 0%, var(--grn-surface) 100%);
}

.vignette--left {
    inset: 0 auto 0 0;
    width: 20%;
    background: linear-gradient(270deg, transparent 0%, var(--grn-surface) 100%);
}

.vignette--right {
    inset: 0 0 0 auto;
    width: 20%;
    background: linear-gradient(90deg, transparent 0%, var(--grn-surface) 100%);
}
```

## Critical Rules

- Vignette color MUST match `--grn-surface` exactly — mismatched colors create visible seams
- Always `pointer-events: none` — vignette must not block content interaction
- Always `position: fixed` + `z-index: 2` — sits above shader canvas (z:1), below content (z:10)
- Top/bottom: 30% height. Left/right: 20% width. Adjust for intensity.

## CSS Mask Alternative

For fading content at bottom of scrollable containers:

```css
.fade-bottom {
    mask: linear-gradient(0deg, rgba(0,0,0,0) 0%, rgb(0,0,0) 24%);
}
```

## When to Use

- Always with shader canvas — prevents content bleeding into shader
- Optional without shader — creates cinematic depth on dark surfaces
