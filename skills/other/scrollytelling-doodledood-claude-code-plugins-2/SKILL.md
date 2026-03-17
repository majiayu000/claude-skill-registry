---
name: scrollytelling
description: 'Implements scroll-driven storytelling experiences with pinned sections, progressive reveals, and scroll-linked animations. Use when asked to build scrollytelling, scroll-driven animations, parallax effects, narrative scroll experiences, or story-driven landing pages.'
---

# Scrollytelling Skill

Build scroll-driven narrative experiences that reveal content, trigger animations, and create immersive storytelling as users scroll.

## What is Scrollytelling?

**Definition**: "A storytelling format in which visual and textual elements appear or change as the reader scrolls through an online article." When readers scroll, something other than conventional document movement happens.

**Origin**: The New York Times' "Snow Fall: The Avalanche at Tunnel Creek" (2012), which won the 2013 Pulitzer Prize for Feature Writing.

**Why it works**: Scrollytelling exploits a fundamental psychological principle—humans crave control. Every scroll is a micro-commitment that increases engagement. Users control the pace, creating deeper connection than passive consumption.

**Measured impact**:
- 400% longer time-on-page vs static content
- 67% improvement in information recall
- 5x higher social sharing rates
- 25-40% improved conversion completion

## Core Principles

### 1. Story First, Technology Second

The biggest mistake is leading with technology instead of narrative. Scrollytelling should enhance the story, not showcase effects.

### 2. User Agency & Progressive Disclosure

Users control the pace. Information reveals gradually to maintain curiosity. This shifts from predetermined pacing to user-controlled narrative flow.

### 3. Sequential Structure

Unlike hierarchical web content, scrollytelling demands linear progression with clear narrative beats. Each section builds on the previous.

### 4. Meaningful Change

Every scroll-triggered effect must serve the narrative. Gratuitous animation distracts rather than enhances.

### 5. Restraint Over Spectacle

Not every section needs animation. Subtle transitions often work better than constant effects. The format should amplify the content's message, not fight it.

## The 5 Standard Techniques

Research analyzing 50 scrollytelling articles identified these core patterns:

| Technique | Description | Best For |
|-----------|-------------|----------|
| **Graphic Sequence** | Discrete visuals that change completely at scroll thresholds | Data visualizations, step-by-step explanations |
| **Animated Transition** | Smooth morphing between states | State changes, evolution over time |
| **Pan and Zoom** | Scroll controls which portion of a visual is visible | Maps, large images, spatial narratives |
| **Moviescroller** | Frame-by-frame progression creating video-like effects | Product showcases, 3D object reveals |
| **Show-and-Play** | Interactive elements activate at scroll waypoints | Multimedia, audio/video integration |

## Layout Patterns

### Pattern 1: Side-by-Side Sticky (Most Common)

The classic scrollytelling pattern: a graphic becomes "stuck" while narrative text scrolls alongside. When the narrative concludes, the graphic "unsticks."

```
┌─────────────────────────────────────┐
│  ┌──────────┐  ┌─────────────────┐  │
│  │  Text    │  │                 │  │
│  │  Step 1  │  │    STICKY       │  │
│  ├──────────┤  │    GRAPHIC      │  │
│  │  Text    │  │                 │  │
│  │  Step 2  │  │  (updates with  │  │
│  ├──────────┤  │   active step)  │  │
│  │  Text    │  │                 │  │
│  │  Step 3  │  │                 │  │
│  └──────────┘  └─────────────────┘  │
└─────────────────────────────────────┘
```

**When to use**: Data visualization stories, step-by-step explanations, educational content requiring persistent visual context.

**Implementation**: Use CSS `position: sticky` (not JavaScript scroll listeners) for better performance and graceful degradation.

### Pattern 2: Full-Width Sections

Content spans the entire viewport with section-based transitions.

**When to use**: Highly visual narratives, immersive brand storytelling, portfolio showcases, timeline-based stories.

### Pattern 3: Layered Parallax

Multiple visual layers (background, midground, foreground) move at different speeds to create depth.

**When to use**: Atmospheric storytelling, game/product launches, long-form narratives where depth adds emotional impact.

**Accessibility warning**: Parallax triggers vestibular disorders (dizziness, nausea, migraines). Always provide reduced-motion fallback; limit to one subtle parallax effect per page maximum.

### Pattern 4: Multi-Directional

Combines vertical scrolling with horizontal sections or sideways timelines.

**When to use**: Timeline-based content, visually-driven showcases, unconventional layouts where surprise enhances the message.

## When to Use Scrollytelling

**Good candidates**:
- Long-form journalism with multimedia
- Brand storytelling celebrating achievements
- Product pages showcasing features
- Chronological/historical content
- Complex narratives broken into digestible chunks
- High-consideration products needing depth

**Avoid when**:
- You lack strong visual assets
- You're tight on time/budget (good scrollytelling requires more investment)
- The story lacks distinct chronology
- Content is brief
- Performance is critical on low-end devices

## Discovery Questions

Before implementing, clarify with the user:

```
header: "Scrollytelling Pattern"
question: "What scrollytelling pattern fits your narrative?"
options:
  - "Pinned narrative - text changes while visual stays fixed (NYT, Pudding.cool style)"
  - "Progressive reveal - content fades in as you scroll down"
  - "Parallax depth - layers move at different speeds (requires reduced-motion fallback)"
  - "Step sequence - discrete sections with transitions between"
  - "Hybrid - multiple patterns combined"
```

```
header: "Tech Stack"
question: "What's your frontend setup?"
options:
  - "React + Tailwind"
  - "React + CSS-in-JS"
  - "Next.js"
  - "Vue"
  - "Vanilla JS"
  - "Other"
```

```
header: "Animation Approach"
question: "Animation library preference?"
options:
  - "CSS-only (scroll-timeline API, IntersectionObserver) - best performance"
  - "GSAP ScrollTrigger - most powerful, cross-browser"
  - "Framer Motion / Motion - React ecosystem"
  - "Lenis + custom - smooth scroll"
  - "No preference - recommend based on complexity"
```

## Technical Implementation (2025-2026)

### Technology Selection Guide

| Complexity | Recommendation | Bundle Size |
|------------|----------------|-------------|
| Simple reveals, progress bars | Native CSS scroll-timeline | 0 KB |
| Viewport-triggered effects | IntersectionObserver | 0 KB |
| Complex timelines, pinning | GSAP ScrollTrigger | ~23 KB |
| React projects | Motion (Framer Motion) | ~32 KB |
| Smooth scroll + effects | Lenis + GSAP | ~25 KB |

### CSS Scroll-Driven Animations (Native - 2025+)

**Browser support**:
- Chrome 115+: Full support (since July 2025)
- Safari 26+: Full support (since September 2025)
- Firefox: Requires flag (`layout.css.scroll-driven-animations.enabled`)

**Key properties**:
- `animation-timeline: scroll()` - links animation to scroll position
- `animation-timeline: view()` - links animation to element visibility
- `animation-range` - controls when animation starts/stops

**Example - View-triggered fade in**:
```css
@supports (animation-timeline: scroll()) {
  .reveal-on-scroll {
    animation: reveal linear both;
    animation-timeline: view();
    animation-range: entry 0% entry 100%;
  }

  @keyframes reveal {
    from {
      opacity: 0;
      transform: translateY(30px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
}
```

**Example - Scroll-linked progress bar**:
```css
.progress-bar {
  animation: grow linear;
  animation-timeline: scroll();
}

@keyframes grow {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}
```

**Performance benefit**: Tokopedia achieved 80% code reduction and CPU usage dropped from 50% to 2% by switching to native CSS scroll-driven animations.

### IntersectionObserver Pattern

For scroll-triggered effects without continuous scroll tracking:

```tsx
const RevealOnScroll = ({ children, delay = 0 }) => {
  const ref = useRef(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Check reduced motion preference
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      setIsVisible(true);
      return;
    }

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.disconnect();
        }
      },
      { threshold: 0.1, rootMargin: '-50px' }
    );

    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  return (
    <div
      ref={ref}
      style={{
        opacity: isVisible ? 1 : 0,
        transform: isVisible ? 'translateY(0)' : 'translateY(30px)',
        transition: `all 0.6s ease ${delay}ms`,
      }}
    >
      {children}
    </div>
  );
};
```

### GSAP ScrollTrigger (Complex Animations)

For pinned sections, timeline orchestration, and cross-browser reliability:

```tsx
const ScrollytellingSection = ({ steps }) => {
  const containerRef = useRef(null);
  const [activeStep, setActiveStep] = useState(0);

  useEffect(() => {
    // Check reduced motion preference
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      return;
    }

    const ctx = gsap.context(() => {
      steps.forEach((_, index) => {
        ScrollTrigger.create({
          trigger: `.step-${index}`,
          start: 'top center',
          end: 'bottom center',
          onEnter: () => setActiveStep(index),
          onEnterBack: () => setActiveStep(index),
        });
      });
    }, containerRef);

    return () => ctx.revert();
  }, [steps]);

  return (
    <section ref={containerRef} className="relative">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Text column - scrolls naturally */}
        <div className="space-y-[100vh]">
          {steps.map((step, i) => (
            <div
              key={i}
              className={`step-${i} min-h-screen flex items-center transition-opacity duration-300 ${
                activeStep === i ? 'opacity-100' : 'opacity-30'
              }`}
            >
              <div className="max-w-md">
                <h3 className="text-2xl font-bold mb-4">{step.title}</h3>
                <p className="text-lg">{step.description}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Visual column - sticky */}
        <div className="relative hidden md:block">
          <div className="sticky top-0 h-screen flex items-center justify-center">
            <StepVisual step={activeStep} data={steps[activeStep]} />
          </div>
        </div>
      </div>
    </section>
  );
};
```

### Motion (Framer Motion) for React

```tsx
import { motion, useScroll, useTransform } from 'motion/react';

const ScrollLinkedSection = () => {
  const ref = useRef(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ['start end', 'end start'],
  });

  const opacity = useTransform(scrollYProgress, [0, 0.5, 1], [0, 1, 0]);
  const scale = useTransform(scrollYProgress, [0, 0.5, 1], [0.8, 1, 0.8]);

  return (
    <section ref={ref} className="h-[200vh] relative">
      <motion.div
        className="sticky top-0 h-screen flex items-center justify-center"
        style={{ opacity, scale }}
      >
        <h2 className="text-6xl font-bold">Scroll-Linked Content</h2>
      </motion.div>
    </section>
  );
};
```

### Scroll Progress Hook

```tsx
const useScrollProgress = (ref) => {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    const updateProgress = () => {
      const rect = element.getBoundingClientRect();
      const windowHeight = window.innerHeight;

      // 0 when element top enters viewport, 1 when bottom exits
      const start = rect.top - windowHeight;
      const end = rect.bottom;
      const current = -start;
      const total = end - start;

      setProgress(Math.max(0, Math.min(1, current / total)));
    };

    window.addEventListener('scroll', updateProgress, { passive: true });
    updateProgress();
    return () => window.removeEventListener('scroll', updateProgress);
  }, [ref]);

  return progress;
};
```

## Accessibility Requirements

Accessibility is non-negotiable. Scrollytelling can trigger vestibular disorders and exclude keyboard/screen reader users if not implemented correctly.

### Critical WCAG Criteria

| Criterion | Requirement |
|-----------|-------------|
| **SC 2.2.2** | Auto-playing content >5 seconds needs pause/stop/hide controls |
| **SC 2.3.3** | User-triggered animations must be disableable |
| **SC 2.3.1** | No flashing more than 3 times per second |

### Reduced Motion Support (Mandatory)

**Always** respect user preferences:

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0s !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0s !important;
    scroll-behavior: auto !important;
  }
}
```

```tsx
const prefersReducedMotion = () =>
  window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// In components - check before animating
useEffect(() => {
  if (prefersReducedMotion()) {
    // Show content immediately, skip animations
    return;
  }
  // Set up animations
}, []);
```

### Safe Animation Guidelines

| Animation Type | Safety |
|----------------|--------|
| Fade in/out, under 0.5s | Safe |
| Simple transforms | Safe |
| Parallax scrolling | Triggers vestibular issues - always provide fallback |
| Swooping, zooming | Problematic - avoid or provide fallback |
| Looping animations | Cognitive overload - limit iterations |

**Keep effects small**: Animations affecting more than 1/3 of the viewport can overwhelm users.

### Keyboard Navigation

- Add `tabindex="0"` to scrollable areas
- Ensure focus follows scroll targets when using smooth scrolling
- Provide skip links to major sections
- No keyboard traps in scroll regions

### Screen Reader Considerations

- Use proper heading hierarchy (`<h1>` through `<h6>`)
- DOM order must match logical reading order
- Use ARIA live regions for dynamic content updates
- Ensure all content exists in DOM (even if visually hidden initially)

## Performance Best Practices

### Do

- Use `transform` and `opacity` for animations (GPU-accelerated)
- Add `will-change: transform` sparingly on animated elements
- Use `passive: true` on scroll listeners
- Use `position: sticky` over JS-based pinning
- Lazy load images/videos until needed
- Use single IntersectionObserver for multiple elements
- Test on real devices, not just desktop

### Don't

- Animate `width`, `height`, `top`, `left` (triggers layout recalculation)
- Use `will-change` excessively (increases memory usage)
- Create scroll listeners without cleanup
- Forget to handle reduced-motion preferences
- Use `overflow: hidden` on ancestors of sticky elements

### Performance Targets

- First Contentful Paint: under 2.5 seconds
- Maintain 60fps during scrolling
- Meet Core Web Vitals thresholds

## Mobile Considerations

Mobile users represent 60%+ of web traffic. Scrollytelling must work excellently on mobile or risk excluding the majority of users.

### Mobile-First Design Philosophy

**Start with mobile**: "Starting with mobile first forces you to pare down your experience to the nuts and bolts, leaving only the necessities. This refines and focuses the content." (The Pudding)

Design the core experience for mobile, then enhance for desktop—not the reverse. This approach:
- Forces essential-only content decisions
- Improves development efficiency
- Results in less code if desktop is functionally similar

### Viewport Units: vh vs svh vs dvh vs lvh

Mobile browsers toggle navigation bars during scrolling, breaking traditional `100vh` layouts.

| Unit | Definition | When To Use |
|------|------------|-------------|
| `vh` | Large viewport (browser UI hidden) | **Legacy fallback only** |
| `svh` | Small viewport (browser UI visible) | **Use for ~90% of layouts** (recommended) |
| `lvh` | Large viewport (browser UI hidden) | Modals/overlays maximizing space |
| `dvh` | Dynamic viewport (changes constantly) | **Use sparingly** - causes layout thrashing |

**Critical warning**: "I initially thought 'dynamic viewport units are the future' and used dvh for every element. This was a mistake. The constant layout shifts felt broken."

**Implementation pattern**:

```css
.full-height-section {
  height: 100vh;  /* Fallback for older browsers */
  height: 100svh; /* Modern solution - small viewport */
}

/* Progressive enhancement */
@supports (height: 100svh) {
  :root {
    --viewport-height: 100svh;
  }
}
```

**JavaScript alternative** (The Pudding's recommendation):

```javascript
function setViewportHeight() {
  const vh = window.innerHeight;
  document.documentElement.style.setProperty('--vh', `${vh}px`);
}

window.addEventListener('resize', setViewportHeight);
setViewportHeight();
```

```css
.section {
  height: calc(var(--vh) * 100);
}
```

### Touch Scroll Physics

**Momentum scrolling**: Content continues scrolling after touch release, decelerating naturally. iOS and Android have different friction curves—iOS feels more "flicky."

**Critical for iOS**:

```css
.scroll-container {
  overflow-y: auto;
  -webkit-overflow-scrolling: touch; /* iOS momentum - still needed for pre-iOS 13 */
}
```

**Performance note**: Scroll events fire at END of momentum on iOS, not during. Use IntersectionObserver instead of scroll listeners for step detection.

### Preventing Gesture Conflicts

**Pull-to-Refresh conflicts**:

```css
/* Disable PTR but keep bounce effects */
html {
  overscroll-behavior-y: contain;
}

/* Or disable completely */
html {
  overscroll-behavior-y: none;
}
```

**Scroll chaining in modals**:

```css
.modal-content {
  overflow-y: auto;
  overscroll-behavior: contain; /* Prevents scrolling parent when modal hits boundary */
}
```

**Horizontal swipe conflicts** (browser back/forward):

```css
.horizontal-carousel {
  touch-action: pan-y pinch-zoom; /* Allow vertical scroll & zoom, block horizontal */
}
```

### Passive Event Listeners

Chrome 56+ defaults touch listeners to passive for 60fps scrolling. Use passive listeners for monitoring, non-passive only when you must `preventDefault()`:

```javascript
// ✅ Monitoring scroll (passive - default, best performance)
document.addEventListener('touchstart', trackTouch, { passive: true });

// ⚠️ Only when you MUST prevent default (e.g., custom swipe)
carousel.addEventListener('touchmove', handleSwipe, { passive: false });
```

**Prefer CSS over JavaScript**:

```css
/* Better than JavaScript preventDefault */
.element {
  touch-action: pan-y pinch-zoom;
}
```

### Scroll Snap on Mobile

Scroll snap works well on mobile with `mandatory` (avoid `proximity` on touch devices):

```css
.scroll-container {
  scroll-snap-type: y mandatory;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

.section {
  scroll-snap-align: start;
  min-height: 100svh;
}

/* Accessibility */
@media (prefers-reduced-motion: reduce) {
  .scroll-container {
    scroll-snap-type: none;
    scroll-behavior: auto;
  }
}
```

**Warning**: Never use `mandatory` if content can overflow the viewport—users won't be able to scroll to see it.

### Touch Accessibility

**Minimum touch target sizes**:

| Standard | Size | When |
|----------|------|------|
| WCAG 2.5.8 (AA) | 24×24px | Minimum compliance |
| WCAG 2.5.5 (AAA) | 44×44px | **Best practice** |
| Apple iOS | 44×44pt | Recommended |
| Android | 48×48dp | Recommended |

**Expand touch area without changing visual size**:

```css
.small-button {
  width: 24px;
  height: 24px;
  padding: 10px; /* Creates 44×44px touch target */
}
```

**Always provide button alternatives for gesture-only actions**:

```html
<!-- Swipe to delete MUST have button alternative -->
<div class="item">
  <span>Content</span>
  <button aria-label="Delete">Delete</button>
</div>
```

### Browser-Specific Quirks

**iOS Safari**:

```css
/* Position sticky requires no overflow on ancestors */
.parent {
  /* overflow: hidden; ❌ Breaks sticky on iOS */
}

.sticky {
  position: -webkit-sticky; /* Prefix still needed */
  position: sticky;
  top: 0;
}
```

```css
/* Preventing body scroll in modals requires JavaScript on iOS */
/* CSS overflow: hidden doesn't work on body */
```

```javascript
// iOS modal scroll lock
function lockScroll() {
  document.body.style.position = 'fixed';
  document.body.style.top = `-${window.scrollY}px`;
}
```

**Chrome Android**:

```css
/* Disable pull-to-refresh */
body {
  overscroll-behavior-y: none;
}
```

### Responsive Layout Strategy

**Side-by-Side → Stacked pattern**:

```tsx
<div className="grid grid-cols-1 md:grid-cols-2 gap-8">
  {/* On mobile: stacked, full-width */}
  {/* On desktop: side-by-side sticky */}
  <div className="space-y-[50vh] md:space-y-[100vh]">
    {/* Text steps - shorter spacing on mobile */}
  </div>
  <div className="hidden md:block">
    {/* Sticky visual - hidden on mobile, shown on desktop */}
  </div>
</div>
```

**Synchronize CSS and JS breakpoints**:

```javascript
const breakpoint = '(min-width: 800px)';
const isDesktop = window.matchMedia(breakpoint).matches;

if (isDesktop) {
  initScrollama(); // Complex scrollytelling
} else {
  initStackedView(); // Simple stacked layout
}

// Listen for breakpoint changes
window.matchMedia(breakpoint).addEventListener('change', (e) => {
  if (e.matches) {
    initScrollama();
  } else {
    initStackedView();
  }
});
```

**Mobile alternative patterns**:
- Replace sticky graphics with inline graphics between text sections
- Use simpler reveal animations instead of complex parallax
- Stack static images with scroll-triggered captions
- Consider whether scrollytelling is even appropriate

### Mobile Performance Strategies

**Target: 60fps (16.7ms per frame)**

**Use hardware-accelerated properties only**:

```css
.animate {
  /* ✅ Good - GPU accelerated */
  transform: translateY(100px);
  opacity: 0.5;

  /* ❌ Bad - triggers layout recalculation */
  /* top: 100px; width: 200px; margin: 20px; */
}
```

**Use `will-change` sparingly**:

```css
/* Only on elements about to animate */
.about-to-animate {
  will-change: transform;
}

/* Remove when animation completes */
.animation-complete {
  will-change: auto;
}
```

**Warning**: Too many composited layers hurt mobile performance. Don't apply `will-change` to everything.

**Throttle scroll handlers with requestAnimationFrame**:

```javascript
let ticking = false;

window.addEventListener('scroll', () => {
  if (!ticking) {
    requestAnimationFrame(() => {
      updateAnimation();
      ticking = false;
    });
    ticking = true;
  }
}, { passive: true });
```

**Better: Use IntersectionObserver** (no scroll events):

```javascript
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      animateElement(entry.target);
    }
  });
});
```

### When to Simplify or Abandon Scrollytelling on Mobile

**Keep scrollytelling when**:
- Transitions are truly meaningful to the narrative
- Spatial movement or temporal change is core to understanding
- Performance targets can be met (60fps, <3s load)
- Testing shows mobile users successfully comprehend content

**Simplify scrollytelling when**:
- Performance is acceptable but animations aren't essential
- Some complexity is nice-to-have but not required
- Desktop experience is richer but mobile should be functional

**Abandon scrollytelling when**:
- Performance issues can't be resolved on mid-tier devices
- Mobile users are confused or frustrated in testing
- Development timeline doesn't allow proper optimization
- Content works just as well in simpler stacked format
- Animations are decorative, not meaningful

**"The most important reason to preserve scroll animations is if the transitions are truly meaningful, not just something to make it pop."** (The Pudding)

### Mobile Testing Checklist

**Device Coverage**:
- [ ] iPhone (latest 2 models) - Safari
- [ ] iPhone - Chrome
- [ ] iPad - Safari (portrait & landscape)
- [ ] Android flagship - Chrome
- [ ] Android mid-tier - Chrome (critical for performance)
- [ ] Tablet Android - Chrome

**Viewport Testing**:
- [ ] Address bar hide/show transitions smooth
- [ ] No layout jumping during scroll
- [ ] Fixed elements stay positioned correctly
- [ ] svh/dvh units behaving as expected

**Performance Testing**:
- [ ] 60fps maintained during scroll (use Chrome DevTools FPS meter)
- [ ] No janky animations
- [ ] Images lazy-load properly
- [ ] Memory doesn't leak on long sessions
- [ ] Test with CPU throttling (4x slowdown in DevTools)

**Interaction Testing**:
- [ ] Touch scrolling feels natural (momentum)
- [ ] No accidental interactions
- [ ] Pull-to-refresh disabled if needed
- [ ] Scroll chaining behaves correctly

**Accessibility Testing**:
- [ ] Works with reduced motion enabled
- [ ] Touch targets minimum 44×44px
- [ ] Button alternatives for all gestures
- [ ] Screen reader (VoiceOver/TalkBack) can navigate

**Critical**: Chrome DevTools mobile emulator does NOT accurately simulate browser UI behavior. Test on real devices or use BrowserStack/Sauce Labs

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **Scroll-jacking** | Overrides natural scroll, breaks accessibility | Preserve native scroll behavior |
| **Text-graphics conflict** | User can't read text while watching animation | Separate text and animated areas |
| **Animation overload** | Distracts from content, causes fatigue | Restraint—not every section needs effects |
| **No length indicator** | Users don't know commitment level | Add progress indicators |
| **Missing fallbacks** | Breaks for no-JS or reduced-motion users | Progressive enhancement |
| **Mobile neglect** | Excludes 60% of users | Mobile-first design |
| **Poor pacing** | Too fast or too slow content reveals | Test with real users |

## Implementation Workflow

1. **Understand the narrative** - What story are you telling? What's the sequence?
2. **Choose pattern** - Pinned, progressive, parallax, or hybrid?
3. **Plan accessibility** - How will reduced-motion users experience this?
4. **Select technology** - Native CSS, GSAP, Motion based on complexity
5. **Scaffold structure** - Build HTML/component structure first
6. **Add scroll mechanics** - Implement tracking (IntersectionObserver, ScrollTrigger, etc.)
7. **Wire animations** - Connect scroll state to visual changes
8. **Add reduced-motion fallbacks** - Content should work without animation
9. **Performance audit** - Check for jank, optimize
10. **Cross-device testing** - Mobile, tablet, desktop, different browsers
11. **Accessibility testing** - Keyboard nav, screen readers, reduced motion

## Output

After gathering requirements, implement the scrollytelling experience directly in the codebase. Provide:

1. Component structure with scroll tracking
2. Animation/transition logic with reduced-motion handling
3. Responsive adjustments (mobile-first)
4. Accessible fallbacks
5. Performance optimizations
6. Testing recommendations

## Notable Examples for Reference

- **NYT "Snow Fall"** - Origin story, multimedia integration
- **Pudding.cool** - Data journalism with audio-visual sync
- **National Geographic "Atlas of Moons"** - Educational, responsive design
- **BBC "Partition of India"** - Historical narrative with multimedia
- **Firewatch website** - Multi-layered parallax for atmosphere

## Sources

Research based on 100+ sources including EU Data Visualization Guide, MDN, GSAP documentation, W3C WCAG, A List Apart, Smashing Magazine, The Pudding, CSS-Tricks, and academic research on scrollytelling effectiveness.
