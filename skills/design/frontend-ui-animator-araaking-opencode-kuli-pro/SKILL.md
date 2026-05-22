---
name: frontend-ui-animator
description: Analyze and implement purposeful UI animations for Next.js + Tailwind + React projects. Use when user asks to add animations, enhance UI motion, animate pages/components, or improve visual feedback. Triggers on "add animations", "animate UI", "motion design", "hover effects", "scroll animations", "page transitions", "micro-interactions".
---

# Frontend UI Animator

Implement purposeful, performant animations that enhance UX without overwhelming users. Focus on key moments: hero intros, hover feedback, content reveals, and navigation transitions.

## Core Philosophy

**"You don't need animations everywhere"** - Prioritize:

| Priority | Area | Purpose |
|----------|------|---------|
| 1 | Hero Intro | First impression, brand personality |
| 2 | Hover Interactions | Feedback, discoverability |
| 3 | Content Reveal | Guide attention, reduce cognitive load |
| 4 | Background Effects | Atmosphere, depth |
| 5 | Navigation Transitions | Spatial awareness, continuity |

## Workflow

Execute phases sequentially. Complete each before proceeding.

### Phase 1: Analyze

1. **Scan project structure** - Identify all pages in `app/` and components in `components/`
2. **Check existing setup** - Review `tailwind.config.ts` for existing animations/keyframes
3. **Identify animation candidates** - List components by priority category
4. **Document constraints** - Note installed animation libraries (framer-motion, etc.)

Output: Animation audit table. See `references/component-checklist.md`.

### Phase 2: Plan

1. **Map animations to components** - Assign specific animation patterns
2. **Determine triggers** - Load, scroll (intersection), hover, click
3. **Estimate effort** - Low (CSS only), Medium (hooks needed), High (library required)
4. **Propose phased rollout** - Quick wins first

Output: Implementation plan with component → animation mapping.

### Phase 3: Implement

1. **Extend Tailwind config** - Add keyframes and animation utilities
2. **Add reduced-motion support** - Accessibility first
3. **Create reusable hooks** - `useScrollReveal`, `useMousePosition` if needed
4. **Apply animations per component** - Follow patterns in `references/animation-patterns.md`

**Performance rules:**
```tsx
// ✅ DO: Use transforms and opacity only
transform: translateY(20px);
opacity: 0.5;
filter: blur(4px);

// ❌ DON'T: Animate layout properties
margin-top: 20px;
height: 100px;
width: 200px;
```

### Phase 4: Verify

1. Test in browser - Visual QA all animations
2. Test reduced-motion - Verify `prefers-reduced-motion` works
3. Check CLS - No layout shifts from animations
4. Performance audit - No jank on scroll animations

## Quick Reference

### Animation Triggers

| Trigger | Implementation |
|---------|----------------|
| Page load | CSS `animation` with `animation-delay` for stagger |
| Scroll into view | `IntersectionObserver` or `react-intersection-observer` |
| Hover | Tailwind `hover:` utilities or CSS `:hover` |
| Click/Tap | State-driven with `useState` |

### Common Patterns

**Staggered children:**
```tsx
{items.map((item, i) => (
  <div 
    key={item.id}
    style={{ animationDelay: `${i * 100}ms` }}
    className="animate-fade-slide-in"
  />
))}
```

**Scroll reveal hook:**
```tsx
const useScrollReveal = (threshold = 0.1) => {
  const ref = useRef<HTMLDivElement>(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => entry.isIntersecting && setIsVisible(true),
      { threshold }
    );
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, [threshold]);

  return { ref, isVisible };
};
```

**Usage:**
```tsx
const { ref, isVisible } = useScrollReveal();
<div ref={ref} className={isVisible ? 'animate-fade-in' : 'opacity-0'} />
```

## Resources

- **Animation patterns**: See `references/animation-patterns.md`
- **Audit template**: See `references/component-checklist.md`
- **Tailwind presets**: See `references/tailwind-presets.md`

## Technical Stack

- **CSS animations**: Default for simple effects
- **Tailwind utilities**: For hover states and basic animations
- **Framer Motion**: For complex orchestration, gestures, layout animations
- **GSAP**: For timeline-based sequences (if already installed)

## Accessibility (Required)

Always include in global CSS:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
  }
}
```
