# Lenis-Style Smooth Scroll (Effect #4)

Inertial wheel/touch scrolling with lerp interpolation. Vanilla JS, no dependencies.

## Implementation

```js
class SmoothScroll {
    constructor({ lerp = 0.1 } = {}) {
        this.lerp = lerp;
        this.targetY = window.scrollY;
        this.currentY = window.scrollY;
        this.running = false;

        window.addEventListener('wheel', (e) => {
            e.preventDefault();
            this.targetY = Math.max(0,
                Math.min(this.targetY + e.deltaY,
                    document.body.scrollHeight - window.innerHeight));
            if (!this.running) {
                this.running = true;
                this.animate();
            }
        }, { passive: false });
    }

    animate() {
        this.currentY += (this.targetY - this.currentY) * this.lerp;
        window.scrollTo(0, this.currentY);
        if (Math.abs(this.targetY - this.currentY) > 0.5) {
            requestAnimationFrame(() => this.animate());
        } else {
            this.running = false;
        }
    }
}
```

## Lerp Function

```
current + (target - current) * factor
```

- `lerp: 0.05` — very smooth, laggy feel
- `lerp: 0.1` — grainient default, balanced
- `lerp: 0.15` — responsive, less smoothing

## CSS Requirements

```css
html.lenis { height: auto; }
```

## Iframe Handling

Set `pointer-events: none` on iframes during scroll to prevent event capture.

## prefers-reduced-motion

```js
if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    // Skip smooth scroll — use native behavior
} else {
    new SmoothScroll({ lerp: 0.1 });
}
```

## Why Not `scroll-behavior: smooth`

No inertia, no lerp control, no touch normalization, no stop/start API.
