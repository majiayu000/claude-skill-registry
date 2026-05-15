# Vertical Ticker Marquee (Effect #7)

Multi-column auto-scrolling card columns at varying speeds.

## HTML

```html
<div class="ticker-holder" id="ticker">
    <div class="ticker-column" data-speed="0.45">
        <div class="ticker-item">...</div>
        <div class="ticker-item">...</div>
    </div>
    <div class="ticker-column" data-speed="0.55">...</div>
    <div class="ticker-column" data-speed="0.50">...</div>
    <div class="ticker-column" data-speed="0.60">...</div>
    <div class="ticker-column" data-speed="0.48">...</div>
</div>
```

## CSS

```css
.ticker-holder {
    display: flex; gap: 5px;
    height: 600px;
    overflow: clip;
}

.ticker-column {
    flex: 1;
    display: flex; flex-direction: column; gap: 5px;
    will-change: transform;
}

.ticker-item { flex-shrink: 0; }
```

## JS Engine

```js
class TickerEngine {
    constructor(holder) {
        this.columns = [...holder.querySelectorAll('.ticker-column')].map(col => ({
            el: col,
            speed: parseFloat(col.dataset.speed) || 0.5,
            offset: 0
        }));
        this.paused = false;
        holder.addEventListener('mouseenter', () => this.paused = true);
        holder.addEventListener('mouseleave', () => this.paused = false);
        this.animate();
    }

    animate() {
        if (!this.paused) {
            this.columns.forEach(col => {
                col.offset -= col.speed;
                const first = col.el.children[0];
                if (first && col.offset < -(first.offsetHeight + 5)) {
                    col.offset += first.offsetHeight + 5;
                    col.el.appendChild(first);
                }
                col.el.style.transform = `translateY(${col.offset}px)`;
            });
        }
        requestAnimationFrame(() => this.animate());
    }
}
```

## Rules

- Speed variance: 10-30% between columns (e.g., 0.45, 0.50, 0.55, 0.60, 0.48)
- Infinite loop: move first child to end when scrolled out
- Pause on hover
- Clone items if fewer than needed to fill visible height
- `prefers-reduced-motion`: stop animation, show static grid
