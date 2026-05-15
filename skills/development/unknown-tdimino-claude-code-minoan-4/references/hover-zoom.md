# Hover Image Zoom (Effect #6)

Scale reveal with overflow clipping on product/collection cards.

## HTML

```html
<div class="zoom-container">
    <img class="zoom-base" src="..." alt="..." loading="lazy" decoding="async">
    <div class="zoom-overlay"></div>
</div>
```

## CSS

```css
.zoom-container {
    position: relative;
    overflow: clip;
    border-radius: inherit;
}

.zoom-overlay {
    position: absolute; inset: 0;
    opacity: 0;
    transform: scale(1.2);
    transition: opacity 0.8s var(--grn-spring-smooth),
                transform 0.8s var(--grn-spring-smooth);
    pointer-events: none;
}

.zoom-container:hover .zoom-overlay {
    opacity: 1;
    transform: scale(1);
}
```

## Rules

- `overflow: clip` over `overflow: hidden` — clip doesn't create a new scroll container
- Initial `pointer-events: none` on overlay — otherwise hidden element captures clicks
- `border-radius: inherit` for container-matched rounding
- Image sizing: `object-fit: cover; width: 100%; height: 100%`

## Scale Values

| Scale | Effect |
|-------|--------|
| 1.1-1.2 | Mild zoom (default) |
| 1.3-1.4 | Medium zoom |
| 2.0-5.0 | Extreme zoom (for small thumbnails) |
