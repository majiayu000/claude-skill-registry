# Anti-Patterns

Banned patterns with wrong/right code examples and rationale.

---

### 1. setInterval for Animation Frames

**Don't:**
```javascript
setInterval(() => {
  element.style.transform = `translateX(${x++}px)`;
}, 16);
```

**Do:**
```javascript
function tick(now) {
  const elapsed = now - start;
  element.style.transform = `translateX(${elapsed * speed}px)`;
  if (elapsed < duration) requestAnimationFrame(tick);
}
requestAnimationFrame(tick);
```

**Why:** `setInterval` doesn't sync with the display refresh rate, causes jank when the tab is inactive, and wastes CPU. `requestAnimationFrame` pauses automatically when hidden and fires at the optimal time for smooth 60fps.

**Exception:** `setInterval` is acceptable for non-visual state cycling (e.g., rotating "PROCESSING..." dots) where frame-perfect timing doesn't matter.

---

### 2. transition: all

**Don't:**
```css
.element { transition: all 300ms ease; }
```

**Do:**
```css
.element { transition: opacity 420ms ease, transform 420ms ease; }
```

**Why:** `transition: all` animates every property change, including layout-triggering ones like `width`, `padding`, `border`. It creates unpredictable animations and makes debugging impossible. Explicit property lists are predictable and performant.

---

### 3. Animate Layout Properties

**Don't:**
```javascript
element.style.width = newWidth + 'px';
element.style.top = newTop + 'px';
element.style.marginLeft = offset + 'px';
```

**Do:**
```javascript
element.style.transform = `translateX(${offset}px) scale(${scale})`;
element.style.opacity = value;
```

**Why:** `width`, `height`, `top`, `left`, `margin`, `padding` trigger layout recalculation (reflow) on every frame. `transform` and `opacity` are compositor-only properties — the browser animates them on the GPU without touching layout.

---

### 4. Hardcoded Stagger Delays

**Don't:**
```javascript
items[0].style.transitionDelay = '0ms';
items[1].style.transitionDelay = '200ms';
items[2].style.transitionDelay = '400ms';
```

**Do:**
```javascript
items.forEach((el, i) => {
  el.style.transitionDelay = `calc(${i} * var(--cm-stagger))`;
});
```

Or in CSS:
```css
.item { transition-delay: calc(var(--index) * var(--cm-stagger)); }
```

**Why:** Hardcoded values can't be adjusted globally. CSS custom properties make stagger configurable from one place and respect the pacing multiplier.

---

### 5. Missing prefers-reduced-motion

**Don't:**
```css
.element {
  animation: slide-in 600ms ease-out;
}
```

**Do:**
```css
.element {
  animation: slide-in 600ms ease-out;
}

@media (prefers-reduced-motion: reduce) {
  .element {
    animation: none;
    opacity: 1;
    transform: none;
  }
}
```

**Why:** Accessibility requirement. Motion can trigger vestibular disorders, migraines, and seizures. Every animated effect must show its final state immediately when reduced motion is preferred.

---

### 6. Animate Off-Screen Elements

**Don't:**
```javascript
// Animate everything on page load
document.querySelectorAll('.animate').forEach(el => {
  el.classList.add('animate-in');
});
```

**Do:**
```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('animate-in');
      observer.unobserve(e.target);
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.animate').forEach(el => observer.observe(el));
```

**Why:** Animating elements that aren't visible wastes GPU resources and can cause scrollbar jank. Use IntersectionObserver to trigger animation only when elements enter the viewport.

---

### 7. Date.now() in Animation Loops

**Don't:**
```javascript
const start = Date.now();
function tick() {
  const elapsed = Date.now() - start;
  // ...
  requestAnimationFrame(tick);
}
```

**Do:**
```javascript
function tick(now) {
  // `now` is from performance.now(), passed by rAF
  const elapsed = now - start;
  // ...
  requestAnimationFrame(tick);
}
const start = performance.now();
requestAnimationFrame(tick);
```

**Why:** `performance.now()` is monotonic (never goes backwards), has sub-millisecond precision, and is automatically passed as the first argument to `requestAnimationFrame` callbacks. `Date.now()` can jump when the system clock adjusts.

---

### 8. Permanent will-change

**Don't:**
```css
.element {
  will-change: transform, opacity;
}
```

**Do:**
```javascript
element.style.willChange = 'transform, opacity';
startAnimation(element, () => {
  element.style.willChange = '';
});
```

Or with CSS class:
```css
.will-animate { will-change: transform, opacity; }
```
```javascript
el.classList.add('will-animate');
el.addEventListener('transitionend', () => {
  el.classList.remove('will-animate');
}, { once: true });
```

**Why:** `will-change` creates a new compositor layer, consuming GPU memory. Left permanently, it wastes memory for every element — especially problematic on mobile. Add before animation, remove after completion.

---

### 9. Typing Effect Without Cursor

**Don't:**
```html
<span class="typing-text">complex approvals</span>
```

**Do:**
```html
<span class="typing-text">complex approvals</span>
<span class="typing-cursor" aria-hidden="true">|</span>
```

**Why:** The blinking cursor is what sells the illusion of someone typing. Without it, text appearing character-by-character looks like a rendering glitch. The cursor provides the visual metaphor.

---

### 10. Pure White Text in Dark Mode

**Don't:**
```css
.heading { color: #FFFFFF; }
```

**Do:**
```css
.heading { color: var(--cm-text); } /* #E8ECF4 */
```

**Why:** Pure white (#FFF) on dark backgrounds creates excessive contrast that strains the eyes. A slightly warm off-white reduces glare while maintaining readability. Use the `--cm-text` token.

---

### 11. Eager Lottie on Mobile Below Fold

**Don't:**
```html
<div data-animation-type="lottie" data-src="big.json"
     data-autoplay="1" data-loading="eager"></div>
```

**Do:**
```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      lottie.loadAnimation({
        container: e.target,
        path: e.target.dataset.src,
        autoplay: true
      });
      observer.unobserve(e.target);
    }
  });
}, { rootMargin: '200px' });
```

**Why:** Lottie JSON files can be 100KB+ and their SVG rendering is CPU-intensive. Loading and playing below-fold animations on mobile wastes bandwidth and battery. Use IntersectionObserver with rootMargin to preload slightly before visible.

---

### 12. Hardcoded File Extensions

**Don't:**
```javascript
if (filename.endsWith('.pdf')) ext = '.pdf';
else if (filename.endsWith('.xlsx')) ext = '.xlsx';
// ...
```

**Do:**
```javascript
const ext = (filename.match(/(\.[a-z0-9]+)$/i) || [''])[0];
```

**Why:** Hardcoding extensions means every new file type needs a code change. The regex pattern handles any extension automatically.
