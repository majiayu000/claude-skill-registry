---
name: css-native
description: Use when implementing Disney's 12 animation principles with pure CSS animations and transitions
---

# CSS Native Animation Principles

Implement all 12 Disney animation principles using CSS animations, transitions, and transforms.

## 1. Squash and Stretch

```css
@keyframes squash-stretch {
  0%, 100% { transform: scaleX(1) scaleY(1); }
  50% { transform: scaleX(1.2) scaleY(0.8); }
}
.ball { animation: squash-stretch 0.3s ease-in-out; }
```

## 2. Anticipation

```css
@keyframes anticipate-jump {
  0% { transform: translateY(0); }
  20% { transform: translateY(10px) scaleY(0.9); } /* wind up */
  100% { transform: translateY(-100px); }
}
```

## 3. Staging

```css
.hero { z-index: 10; filter: none; }
.background { z-index: 1; filter: blur(2px); opacity: 0.7; }
```

## 4. Straight Ahead / Pose to Pose

```css
/* Pose to pose - define keyframes explicitly */
@keyframes walk-cycle {
  0% { background-position: 0 0; }
  25% { background-position: -100px 0; }
  50% { background-position: -200px 0; }
  75% { background-position: -300px 0; }
  100% { background-position: -400px 0; }
}
```

## 5. Follow Through and Overlapping Action

```css
.character { animation: move 0.5s ease-out; }
.hair { animation: move 0.5s ease-out 0.05s; } /* slight delay */
.cape { animation: move 0.5s ease-out 0.1s; }
```

## 6. Slow In and Slow Out

```css
.element {
  transition: transform 0.4s cubic-bezier(0.42, 0, 0.58, 1);
}
/* Or use: ease-in-out, ease-in, ease-out */
```

## 7. Arc

```css
@keyframes arc-motion {
  0% { transform: translate(0, 0); }
  50% { transform: translate(100px, -80px); }
  100% { transform: translate(200px, 0); }
}
/* Use offset-path for true arcs */
.element { offset-path: path('M0,100 Q100,0 200,100'); }
```

## 8. Secondary Action

```css
.button:hover {
  transform: scale(1.05);
}
.button:hover .icon {
  animation: wiggle 0.3s ease-in-out;
}
```

## 9. Timing

```css
.fast { animation-duration: 0.15s; }
.normal { animation-duration: 0.3s; }
.slow { animation-duration: 0.6s; }
.dramatic { animation-duration: 1.2s; }
```

## 10. Exaggeration

```css
@keyframes exaggerated-bounce {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-150px) scale(0.8, 1.3); }
}
```

## 11. Solid Drawing

```css
.element {
  transform-style: preserve-3d;
  perspective: 1000px;
}
.face { transform: rotateY(20deg); }
```

## 12. Appeal

```css
.appealing {
  border-radius: 50%;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
}
.appealing:hover {
  transform: scale(1.02);
  box-shadow: 0 8px 30px rgba(0,0,0,0.15);
}
```

## Timing Reference

| Action | Duration |
|--------|----------|
| Micro-interaction | 100-200ms |
| Button feedback | 150-300ms |
| Page transitions | 300-500ms |
| Complex animations | 500-1000ms |

## Key CSS Properties

- `animation` / `@keyframes`
- `transition`
- `transform`
- `offset-path` (motion paths)
- `animation-timing-function`
- `animation-delay`
