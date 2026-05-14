# HTML Slide Template

Complete boilerplate for a single-file HTML presentation with navigation, animations, and responsive viewport fitting.

## Full Boilerplate

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PRESENTATION_TITLE</title>

  <!-- Fonts (customize per style preset) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=HEADING_FONT:wght@400;700&family=BODY_FONT:wght@300;400;500;700&display=swap" rel="stylesheet">

  <!-- Optional: Prism.js for code highlighting -->
  <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet">

  <style>
    /* === THEME VARIABLES === */
    :root {
      --bg-primary: #0a0a0a;
      --bg-secondary: #1a1a1a;
      --text-primary: #ffffff;
      --text-secondary: #999999;
      --accent: #4a9eff;
      --accent-secondary: #ff6b6b;
      --font-heading: 'HEADING_FONT', sans-serif;
      --font-body: 'BODY_FONT', sans-serif;
      --title-size: clamp(2rem, 6vw, 5rem);
      --body-size: clamp(0.9rem, 2vw, 1.25rem);
      --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* === PASTE viewport-base.css CONTENTS HERE === */

    /* === PRESENTATION-SPECIFIC STYLES === */
    /* Add custom styles per preset and slide content */
  </style>
</head>
<body>

  <!-- === PROGRESS BAR === -->
  <div class="progress-bar" id="progress"></div>

  <!-- === SLIDE 1: TITLE === -->
  <section class="slide" id="slide-1">
    <div class="slide-content" style="text-align: center;">
      <h1 class="slide-title reveal">Presentation Title</h1>
      <p class="slide-subtitle reveal">Subtitle or tagline goes here</p>
      <p class="slide-caption reveal">Speaker Name — Event — Date</p>
    </div>
  </section>

  <!-- === SLIDE 2: CONTENT === -->
  <section class="slide" id="slide-2">
    <div class="slide-content">
      <h2 class="slide-title reveal">Section Heading</h2>
      <ul class="slide-body">
        <li class="reveal">First key point with supporting detail</li>
        <li class="reveal">Second key point with evidence</li>
        <li class="reveal">Third key point with example</li>
        <li class="reveal">Fourth key point with takeaway</li>
      </ul>
    </div>
  </section>

  <!-- === SLIDE 3: TWO-COLUMN === -->
  <section class="slide" id="slide-3">
    <div class="slide-content">
      <h2 class="slide-title reveal">Comparison Heading</h2>
      <div class="split-layout">
        <div class="reveal-left">
          <h3>Left Column</h3>
          <p class="slide-body">Content for the left side with explanation or image.</p>
        </div>
        <div class="reveal">
          <h3>Right Column</h3>
          <p class="slide-body">Content for the right side with comparison.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- === SLIDE 4: IMAGE FOCUS === -->
  <section class="slide" id="slide-4">
    <div class="slide-content" style="text-align: center;">
      <h2 class="slide-title reveal">Visual Showcase</h2>
      <img src="image.png" alt="Description" class="reveal-scale">
      <p class="slide-caption reveal">Image caption or source attribution</p>
    </div>
  </section>

  <!-- === SLIDE 5: CODE === -->
  <section class="slide" id="slide-5">
    <div class="slide-content">
      <h2 class="slide-title reveal">Code Example</h2>
      <pre class="code-block reveal"><code class="language-javascript">
// Example code here
function greet(name) {
  return `Hello, ${name}!`;
}
      </code></pre>
    </div>
  </section>

  <!-- === SLIDE 6: QUOTE === -->
  <section class="slide" id="slide-6">
    <div class="slide-content" style="text-align: center; max-width: 800px;">
      <blockquote class="reveal" style="font-size: clamp(1.2rem, 3vw, 2rem); font-style: italic; line-height: 1.4; color: var(--text-primary);">
        "A meaningful quote that reinforces the key message of the presentation."
      </blockquote>
      <p class="slide-caption reveal" style="margin-top: 1rem;">— Attribution, Role</p>
    </div>
  </section>

  <!-- === SLIDE 7: FEATURE GRID === -->
  <section class="slide" id="slide-7">
    <div class="slide-content">
      <h2 class="slide-title reveal" style="text-align: center;">Features</h2>
      <div class="grid-3" style="margin-top: 2rem;">
        <div class="card reveal">
          <h3 style="color: var(--accent); margin-bottom: 0.5rem;">Feature 1</h3>
          <p class="slide-body">Brief description of this feature and its benefit.</p>
        </div>
        <div class="card reveal">
          <h3 style="color: var(--accent); margin-bottom: 0.5rem;">Feature 2</h3>
          <p class="slide-body">Brief description of this feature and its benefit.</p>
        </div>
        <div class="card reveal">
          <h3 style="color: var(--accent); margin-bottom: 0.5rem;">Feature 3</h3>
          <p class="slide-body">Brief description of this feature and its benefit.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- === NAVIGATION DOTS === -->
  <nav class="nav" id="nav"></nav>

  <!-- === SCRIPTS === -->
  <!-- Optional: Prism.js -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-javascript.min.js"></script>

  <!-- Optional: Mermaid -->
  <!-- <script src="https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.9.0/mermaid.min.js"></script> -->

  <script>
    // === SLIDE NAVIGATION ===
    const slides = document.querySelectorAll('.slide');
    const nav = document.getElementById('nav');
    const progress = document.getElementById('progress');
    let currentSlide = 0;

    // Create nav dots
    slides.forEach((_, i) => {
      const dot = document.createElement('button');
      dot.className = 'nav-dot' + (i === 0 ? ' active' : '');
      dot.setAttribute('aria-label', `Go to slide ${i + 1}`);
      dot.onclick = () => goToSlide(i);
      nav.appendChild(dot);
    });

    function goToSlide(index) {
      if (index < 0 || index >= slides.length) return;
      currentSlide = index;
      slides[index].scrollIntoView({ behavior: 'smooth' });
      updateNav();
      triggerAnimations(index);
    }

    function updateNav() {
      document.querySelectorAll('.nav-dot').forEach((dot, i) => {
        dot.classList.toggle('active', i === currentSlide);
      });
      progress.style.width = ((currentSlide + 1) / slides.length * 100) + '%';
    }

    // === KEYBOARD NAVIGATION ===
    document.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') {
        e.preventDefault();
        goToSlide(currentSlide + 1);
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        e.preventDefault();
        goToSlide(currentSlide - 1);
      } else if (e.key === 'Home') {
        e.preventDefault();
        goToSlide(0);
      } else if (e.key === 'End') {
        e.preventDefault();
        goToSlide(slides.length - 1);
      }
    });

    // === TOUCH NAVIGATION ===
    let touchStartY = 0;
    document.addEventListener('touchstart', (e) => { touchStartY = e.touches[0].clientY; });
    document.addEventListener('touchend', (e) => {
      const diff = touchStartY - e.changedTouches[0].clientY;
      if (Math.abs(diff) > 50) {
        goToSlide(currentSlide + (diff > 0 ? 1 : -1));
      }
    });

    // === INTERSECTION OBSERVER FOR ANIMATIONS ===
    function triggerAnimations(slideIndex) {
      const slide = slides[slideIndex];
      slide.querySelectorAll('.reveal, .reveal-scale, .reveal-left, .reveal-blur').forEach((el, i) => {
        setTimeout(() => el.classList.add('visible'), i * 100);
      });
    }

    // Observer for scroll-based navigation
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const index = Array.from(slides).indexOf(entry.target);
          currentSlide = index;
          updateNav();
          triggerAnimations(index);
        }
      });
    }, { threshold: 0.5 });

    slides.forEach(slide => observer.observe(slide));

    // Trigger first slide animations
    triggerAnimations(0);

    // Optional: Initialize Mermaid
    // mermaid.initialize({ startOnLoad: true, theme: 'dark' });
  </script>
</body>
</html>
```

## Slide Type Templates

### Title Slide
```html
<section class="slide" style="text-align: center;">
  <div class="slide-content">
    <h1 class="slide-title reveal">Main Title</h1>
    <p class="slide-subtitle reveal">Subtitle or tagline</p>
    <p class="slide-caption reveal">Speaker — Event — Date</p>
  </div>
</section>
```

### Section Divider
```html
<section class="slide" style="background: var(--accent);">
  <div class="slide-content" style="text-align: center;">
    <h2 class="slide-title reveal" style="color: var(--bg-primary);">Section Title</h2>
  </div>
</section>
```

### Timeline
```html
<section class="slide">
  <div class="slide-content">
    <h2 class="slide-title reveal">Timeline</h2>
    <div style="display: flex; justify-content: space-between; margin-top: 2rem; position: relative;">
      <div style="position: absolute; top: 50%; left: 0; right: 0; height: 2px; background: var(--accent);"></div>
      <div class="reveal" style="text-align: center; z-index: 1;">
        <div style="width: 12px; height: 12px; border-radius: 50%; background: var(--accent); margin: 0 auto 0.5rem;"></div>
        <strong>2023</strong>
        <p class="slide-caption">Milestone 1</p>
      </div>
      <!-- Repeat for each milestone -->
    </div>
  </div>
</section>
```

### Metric Highlight
```html
<section class="slide">
  <div class="slide-content" style="text-align: center;">
    <h2 class="slide-title reveal">Key Metrics</h2>
    <div class="grid-3" style="margin-top: 2rem;">
      <div class="reveal">
        <div style="font-size: clamp(2rem, 5vw, 4rem); font-weight: 700; color: var(--accent);">300K+</div>
        <p class="slide-body">Users worldwide</p>
      </div>
      <!-- Repeat for each metric -->
    </div>
  </div>
</section>
```
