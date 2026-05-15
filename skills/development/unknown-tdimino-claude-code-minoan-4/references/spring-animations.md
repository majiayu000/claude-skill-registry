# Spring Animations (Effect #5)

3 spring presets via CSS cubic-bezier approximations.

## Presets

| Name | CSS | Use Case |
|------|-----|----------|
| Snappy | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Buttons, tab nav, toggles |
| Smooth | `cubic-bezier(0.25, 1, 0.5, 1)` | Image zoom, gallery transitions |
| Subtle | `cubic-bezier(0.22, 1, 0.36, 1)` | Card reveals, hover states |

## CSS Custom Properties

```css
--grn-spring-snappy: cubic-bezier(0.34, 1.56, 0.64, 1);
--grn-spring-smooth: cubic-bezier(0.25, 1, 0.5, 1);
--grn-spring-subtle: cubic-bezier(0.22, 1, 0.36, 1);
```

## Usage

```css
.card {
    transition: transform 0.6s var(--grn-spring-snappy),
                opacity 0.6s var(--grn-spring-snappy);
}

.card:hover { transform: translateY(-4px); }
```

## Entry Animations

```css
.fade-up {
    opacity: 0; transform: translateY(24px);
    transition: opacity 0.8s var(--grn-spring-smooth),
                transform 0.8s var(--grn-spring-smooth);
}
.fade-up.visible { opacity: 1; transform: translateY(0); }
```

Trigger via IntersectionObserver:

```js
const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.1 });
document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));
```

## prefers-reduced-motion

```css
@media (prefers-reduced-motion: reduce) {
    .fade-up { opacity: 1; transform: none; transition: none; }
}
```
