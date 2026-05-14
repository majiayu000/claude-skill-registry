# Animation Patterns

CSS and GSAP animation recipes for HTML slide presentations. All patterns include timing, easing, and accessibility considerations.

## CSS Animation Recipes

### Staggered List Reveal

Reveal list items one by one with staggered delay:

```css
.stagger-list li {
  opacity: 0;
  transform: translateY(15px);
  transition: all 0.5s var(--ease-out-expo);
}
.stagger-list.visible li:nth-child(1) { transition-delay: 0s; }
.stagger-list.visible li:nth-child(2) { transition-delay: 0.08s; }
.stagger-list.visible li:nth-child(3) { transition-delay: 0.16s; }
.stagger-list.visible li:nth-child(4) { transition-delay: 0.24s; }
.stagger-list.visible li:nth-child(5) { transition-delay: 0.32s; }
.stagger-list.visible li:nth-child(6) { transition-delay: 0.40s; }
.stagger-list.visible li {
  opacity: 1;
  transform: translateY(0);
}
```

### Card Grid Pop-In

Cards scale in from 0.8 with rotation:

```css
.card-pop {
  opacity: 0;
  transform: scale(0.8) rotate(-2deg);
  transition: all 0.6s var(--ease-out-expo);
}
.card-pop.visible {
  opacity: 1;
  transform: scale(1) rotate(0deg);
}
```

### Gradient Background Animation

Subtle background movement:

```css
.gradient-bg {
  background: linear-gradient(-45deg, var(--bg-primary), var(--bg-secondary), var(--accent), var(--bg-primary));
  background-size: 400% 400%;
  animation: gradientShift 15s ease infinite;
}
@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
```

### Counter Animation

Animate numbers counting up (requires JS):

```javascript
function animateCounter(element, target, duration = 2000) {
  const start = 0;
  const startTime = performance.now();
  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
    element.textContent = Math.floor(eased * target).toLocaleString();
    if (progress < 1) requestAnimationFrame(update);
    else element.textContent = target.toLocaleString();
  }
  requestAnimationFrame(update);
}
```

### Typewriter Effect

```css
.typewriter {
  overflow: hidden;
  white-space: nowrap;
  border-right: 2px solid var(--accent);
  animation: typing 2s steps(40) 0.5s forwards, blink 0.7s step-end infinite;
  width: 0;
}
@keyframes typing { to { width: 100%; } }
@keyframes blink { 50% { border-color: transparent; } }
```

### Parallax Layers

```css
.parallax-container {
  position: relative;
  overflow: hidden;
}
.parallax-bg {
  position: absolute;
  top: -10%;
  left: -5%;
  width: 110%;
  height: 120%;
  transition: transform 0.1s linear;
}
```

```javascript
// Move background based on scroll position
document.addEventListener('scroll', () => {
  const bg = document.querySelector('.parallax-bg');
  if (bg) {
    const scrolled = window.scrollY;
    bg.style.transform = `translateY(${scrolled * 0.3}px)`;
  }
});
```

## GSAP Animation Recipes

Load GSAP from CDN:
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
```

### Timeline Slide Entrance

```javascript
function animateSlideEntrance(slideEl) {
  const tl = gsap.timeline();
  const title = slideEl.querySelector('.slide-title');
  const items = slideEl.querySelectorAll('.reveal');

  tl.from(title, { y: 30, opacity: 0, duration: 0.6, ease: 'expo.out' })
    .from(items, { y: 20, opacity: 0, duration: 0.5, stagger: 0.1, ease: 'expo.out' }, '-=0.3');

  return tl;
}
```

### Spring-Based Card Animation

```javascript
gsap.from('.card', {
  scale: 0.8,
  opacity: 0,
  duration: 0.8,
  stagger: 0.15,
  ease: 'elastic.out(1, 0.5)',
  scrollTrigger: { trigger: '.card-grid', start: 'top 80%' }
});
```

### Text Split Animation

```javascript
// Split heading into characters
const heading = document.querySelector('.split-heading');
heading.innerHTML = heading.textContent.split('').map(char =>
  `<span style="display:inline-block">${char === ' ' ? '&nbsp;' : char}</span>`
).join('');

gsap.from('.split-heading span', {
  y: 60,
  opacity: 0,
  rotateX: -90,
  stagger: 0.03,
  duration: 0.6,
  ease: 'back.out(1.7)'
});
```

### Morphing Number Counter

```javascript
gsap.to('.metric-number', {
  textContent: 300000,
  duration: 2,
  ease: 'power2.out',
  snap: { textContent: 1 },
  onUpdate: function() {
    this.targets()[0].textContent = Math.floor(this.targets()[0].textContent).toLocaleString();
  }
});
```

### Responsive Animation with matchMedia

```javascript
gsap.matchMedia().add({
  isDesktop: '(min-width: 800px)',
  isMobile: '(max-width: 799px)',
  reduceMotion: '(prefers-reduced-motion: reduce)'
}, (context) => {
  let { isDesktop, reduceMotion } = context.conditions;

  if (reduceMotion) return; // Skip all animations

  gsap.from('.slide-title', {
    y: isDesktop ? 40 : 20,
    opacity: 0,
    duration: isDesktop ? 0.8 : 0.5,
    ease: 'expo.out'
  });
});
```

## GSAP Advanced Patterns

### Timeline with Position Parameter

```javascript
function animateSlideIn(slideEl) {
  const tl = gsap.timeline({ defaults: { ease: 'expo.out' } });
  tl.from(slideEl.querySelector('.slide-title'), { y: 40, opacity: 0, duration: 0.7 })
    .from(slideEl.querySelector('.slide-subtitle'), { y: 30, opacity: 0, duration: 0.5 }, '<0.2')
    .from(slideEl.querySelectorAll('.reveal'), { y: 20, opacity: 0, stagger: 0.08, duration: 0.5 }, '<0.15');
  return tl;
}
```

The `"<0.2"` position parameter means "0.2s after the START of the previous tween" — creating overlapping, choreographed entrances instead of sequential waits. This keeps motion flowing naturally rather than waiting for each step to complete.

### SplitText Headline Reveal

```javascript
// Using GSAP SplitText plugin (or manual word split)
function splitReveal(selector) {
  const el = document.querySelector(selector);
  const words = el.textContent.split(' ');
  el.innerHTML = words.map(w => `<span class="word" style="display:inline-block;overflow:hidden"><span class="word-inner" style="display:inline-block">${w}</span></span>`).join(' ');
  return gsap.from(`${selector} .word-inner`, {
    yPercent: 110,
    duration: 0.8,
    stagger: 0.04,
    ease: 'expo.out'
  });
}
```

Each word clips behind its wrapper during reveal — creates the cinematic "rising text" effect where words appear to slide up from below while staying perfectly clipped.

### ScrollTrigger Slide Navigation

```javascript
// Pin each slide and transition on scroll
gsap.utils.toArray('.slide').forEach((slide, i) => {
  ScrollTrigger.create({
    trigger: slide,
    start: 'top top',
    pin: true,
    pinSpacing: true,
    onEnter: () => animateSlideIn(slide),
    onEnterBack: () => animateSlideIn(slide)
  });
});
```

Pins each slide in the viewport while allowing scrolling to trigger animations. Re-animates when scrolling back up (onEnterBack) for a smooth, reversible experience.

### Reusable animateSlide Template

```javascript
function animateSlide(slide, options = {}) {
  const { mood = 'professional' } = options;
  const config = {
    professional: { duration: 0.5, stagger: 0.06, ease: 'power2.out' },
    playful:      { duration: 0.7, stagger: 0.1,  ease: 'back.out(1.7)' },
    cinematic:    { duration: 1.2, stagger: 0.15, ease: 'power1.inOut' },
    energetic:    { duration: 0.4, stagger: 0.08, ease: 'back.out(2)' }
  };
  const c = config[mood] || config.professional;
  const tl = gsap.timeline({ defaults: { ease: c.ease, duration: c.duration } });
  const title = slide.querySelector('.slide-title');
  const items = slide.querySelectorAll('.reveal, .reveal-scale, .reveal-left');
  if (title) tl.from(title, { y: 40, opacity: 0 });
  if (items.length) tl.from(items, { y: 20, opacity: 0, stagger: c.stagger }, '<0.2');
  return tl;
}
```

A reusable template that adapts animation character based on presentation mood. Pass different mood options to get professional, playful, cinematic, or energetic timing without duplicating animation logic.

## Spring Physics Timing (Remotion-Inspired)

Translate Remotion spring configurations to GSAP easing equivalents. Spring physics creates natural, organic motion that feels responsive:

- **Smooth** (damping: 200) → `gsap.to(el, { ease: 'power3.out', duration: 0.8 })` — heavily damped, no overshoot. Settled, refined motion.
- **Snappy** (damping: 20) → `gsap.to(el, { ease: 'back.out(1.2)', duration: 0.5 })` — slight overshoot then settle. Quick with anticipation.
- **Bouncy** (damping: 8) → `gsap.to(el, { ease: 'elastic.out(1, 0.4)', duration: 1.0 })` — visible oscillation. Playful and energetic.
- **Heavy** (mass: 5) → increase `duration` by 2-3x for weighty, deliberate movement. Feels substantial.

| Remotion Spring | GSAP Equivalent | Duration | Character |
|----------------|-----------------|----------|-----------|
| smooth (damping: 200) | power3.out | 0.6-0.8s | Settled, no bounce |
| snappy (damping: 20) | back.out(1.2) | 0.4-0.6s | Quick with overshoot |
| bouncy (damping: 8) | elastic.out(1, 0.4) | 0.8-1.2s | Playful oscillation |
| heavy (mass: 5) | power2.inOut (2x duration) | 1.5-2.0s | Deliberate, weighty |

## Timing Guidelines by Mood

| Mood | Duration | Easing | Stagger |
|------|----------|--------|---------|
| Playful | 400-600ms | `back.out(1.7)` or `elastic.out(1, 0.5)` | 0.1-0.15s |
| Professional | 200-300ms | `power2.out` or `expo.out` | 0.05-0.08s |
| Cinematic | 800-1500ms | `power1.inOut` or `sine.inOut` | 0.15-0.25s |
| Technical | 150-250ms | `power3.out` | 0.03-0.05s |
| Energetic | 300-500ms | `back.out(2)` | 0.08-0.12s |

## Accessibility

Always wrap animation code in a reduced-motion check:

```javascript
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (!prefersReducedMotion) {
  // Run animations
} else {
  // Make all elements visible immediately
  document.querySelectorAll('.reveal, .reveal-scale, .reveal-left, .reveal-blur')
    .forEach(el => el.classList.add('visible'));
}
```
