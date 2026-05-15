# Lottie Orchestration

Lottie player setup, responsive variants, scroll-synced playback, and configuration patterns.

## Player Setup

### CDN Options

```html
<!-- dotlottie-player (recommended, smaller) -->
<script src="https://unpkg.com/@dotlottie/dotlottie-player@2/dist/dotlottie-player.js"></script>

<!-- lottie-web (full API control) -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.12.2/lottie.min.js"></script>
```

### Declarative (data attributes)

Webflow-style pattern — good for simple autoplay/loop:

```html
<div class="lottie-animation"
     data-animation-type="lottie"
     data-src="https://example.com/animation.json"
     data-loop="1"
     data-direction="1"
     data-autoplay="1"
     data-renderer="svg"
     data-duration="7.96"
     data-loading="eager">
</div>
```

Initialization:
```javascript
document.querySelectorAll('[data-animation-type="lottie"]').forEach(el => {
  lottie.loadAnimation({
    container: el,
    renderer: el.dataset.renderer || 'svg',
    loop: el.dataset.loop === '1' || el.dataset.loop === 'true',
    autoplay: el.dataset.autoplay === '1',
    path: el.dataset.src
  });
});
```

### Programmatic Control

```javascript
const anim = lottie.loadAnimation({
  container: element,
  renderer: 'svg',
  loop: true,
  autoplay: false,
  path: 'animation.json'
});

anim.play();
anim.pause();
anim.stop();
anim.setSpeed(1.5);
anim.goToAndPlay(30, true);  // frame 30
anim.goToAndStop(0, true);   // first frame
anim.setDirection(-1);        // reverse
anim.totalFrames;             // read-only
anim.currentFrame;            // read-only
```

## Responsive Variants

Desktop/tablet/mobile containers with separate Lottie sources:

```html
<div class="lottie-responsive">
  <div class="slot-desktop">
    <div data-animation-type="lottie" data-src="feature-desktop.json"
         data-loop="1" data-autoplay="1" data-renderer="svg"></div>
  </div>
  <div class="slot-tablet">
    <div data-animation-type="lottie" data-src="feature-tablet.json"
         data-loop="1" data-autoplay="1" data-renderer="svg"></div>
  </div>
  <div class="slot-mobile">
    <div data-animation-type="lottie" data-src="feature-mobile.json"
         data-loop="1" data-autoplay="1" data-renderer="svg"></div>
  </div>
</div>
```

```css
.slot-desktop { display: block; }
.slot-tablet  { display: none; }
.slot-mobile  { display: none; }

@media (max-width: 991px) {
  .slot-desktop { display: none; }
  .slot-tablet  { display: block; }
}

@media (max-width: 767px) {
  .slot-tablet { display: none; }
  .slot-mobile { display: block; }
}
```

## Viewport-Triggered Playback

Play only when visible:

```javascript
function initViewportLottie(container) {
  const anim = lottie.loadAnimation({
    container,
    renderer: 'svg',
    loop: true,
    autoplay: false,
    path: container.dataset.src
  });

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) anim.play();
      else anim.pause();
    });
  }, { threshold: 0.3 });

  observer.observe(container);
  return anim;
}
```

## Scroll-Synced Playback

Scrub animation based on scroll position:

```javascript
function scrubLottie(anim, triggerElement) {
  function tick() {
    const rect = triggerElement.getBoundingClientRect();
    const viewH = window.innerHeight;
    const progress = 1 - (rect.top / viewH);
    const clamped = Math.max(0, Math.min(1, progress));
    const frame = Math.round(clamped * (anim.totalFrames - 1));
    anim.goToAndStop(frame, true);
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}
```

## Duration Reference (from ConductorAI)

| Animation | Duration | Loop |
|-----------|----------|------|
| Icon animations | 3–4s | yes |
| Feature demos | 6–10s | yes |
| Hero animation | 8s | yes |
| CTA background | 9.5s | yes |
| Decorative lines | 1–3s | yes |
| One-shot reveals | 3–5s | no |

## Renderer Choice

- `svg` — crisp at all sizes, accessible DOM, good for icons and UI
- `canvas` — better for complex animations with many layers, lower memory
- `html` — limited, use only if SVG isn't supported

Default to `svg` for marketing pages.

## Reduced Motion

Show first frame only:
```javascript
if (reducedMotion) {
  anim.goToAndStop(0, true);
  return;
}
```

Or hide animation entirely and show a static image:
```css
@media (prefers-reduced-motion: reduce) {
  .lottie-animation { display: none; }
  .lottie-fallback { display: block; }
}
```
