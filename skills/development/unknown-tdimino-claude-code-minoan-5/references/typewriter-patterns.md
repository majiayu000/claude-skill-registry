# Typewriter Patterns

Two variants: **hero-rotator** (word cycling in headlines) and **type-on** (terminal-style one-shot or looping text).

## Hero Rotator

Cycles through a list of words appended to a static base text. Cursor blinks between words.

### State Machine

```
START → TYPE_CHAR → (word complete?) → HOLD → DELETE_CHAR → (empty?) → NEXT_WORD → TYPE_CHAR
```

### Timing Constants

| Constant | Default | Notes |
|----------|---------|-------|
| `TYPE_MIN_MS` | 35 | Minimum ms per character |
| `TYPE_MAX_MS` | 65 | Maximum ms per character |
| `DELETE_MIN_MS` | 18 | Minimum ms per delete |
| `DELETE_MAX_MS` | 35 | Maximum ms per delete |
| `HOLD_MS` | 1100 | Hold complete word before deleting |
| `BETWEEN_WORDS_MS` | 180 | Pause between words |

Random per-character delay: `Math.floor(Math.random() * (max - min + 1)) + min`

### DOM Structure

```html
<h1 class="hero-heading hero-rotator">
  <span class="rotator-base">Accelerating</span>
  <span class="rotator-type__text">complex approvals</span>
  <span class="rotator-type__cursor" aria-hidden="true">|</span>
</h1>
```

JS restructures from initial markup:
```html
<h1 class="hero-heading hero-rotator">
  Accelerating
  <ul style="display:none">
    <li>complex approvals</li>
    <li>investigations</li>
  </ul>
</h1>
```

### CSS

```css
.hero-heading { white-space: nowrap; }

.rotator-type__text { color: var(--cm-brand); }

.rotator-type__cursor {
  color: var(--cm-text-40);
  font-weight: 300;
  animation: blink 530ms step-end infinite;
}

@keyframes blink { 50% { opacity: 0; } }
```

### Core Logic

```javascript
function tick() {
  const currentWord = items[wordIndex];
  if (!isDeleting) {
    charIndex += 1;
    text.textContent = currentWord.slice(0, charIndex);
    if (charIndex < currentWord.length) {
      timeoutId = setTimeout(tick, randomBetween(TYPE_MIN_MS, TYPE_MAX_MS));
    } else {
      isDeleting = true;
      timeoutId = setTimeout(tick, HOLD_MS);
    }
  } else {
    charIndex -= 1;
    text.textContent = currentWord.slice(0, Math.max(0, charIndex));
    if (charIndex > 0) {
      timeoutId = setTimeout(tick, randomBetween(DELETE_MIN_MS, DELETE_MAX_MS));
    } else {
      isDeleting = false;
      wordIndex = (wordIndex + 1) % items.length;
      timeoutId = setTimeout(tick, BETWEEN_WORDS_MS);
    }
  }
}
```

### Visibility API

```javascript
document.addEventListener('visibilitychange', () => {
  if (document.hidden) { pausedByVisibility = true; stop(); }
  else if (pausedByVisibility) { pausedByVisibility = false; start(); }
});
```

## Type-On Variant

One-shot or looping type effect for terminal/status text.

### Timing Constants

| Constant | Default | Notes |
|----------|---------|-------|
| `TYPE_SPEED` | 28 | Base ms per character |
| `TYPE_VARIANCE` | 20 | Random variance added |
| `DELETE_SPEED` | 18 | Ms per delete character |
| `HOLD_FULL_MS` | 1200 | Hold after typing complete |
| `HOLD_EMPTY_MS` | 300 | Hold after deleting before retype |

### DOM

Wraps original text content in span:
```html
<span class="type-on" data-loop="true">search initialization...</span>
<!-- becomes -->
<span class="type-on" data-loop="true">
  <span class="type-on-text">search i</span>
  <span class="type-on-cursor" aria-hidden="true">|</span>
</span>
```

### Core Logic (async/await)

```javascript
async function typeText(textEl, text) {
  for (let i = 1; i <= text.length; i++) {
    textEl.textContent = text.slice(0, i);
    await wait(TYPE_SPEED + Math.random() * TYPE_VARIANCE);
  }
}

async function deleteText(textEl) {
  const current = textEl.textContent;
  for (let i = current.length - 1; i >= 0; i--) {
    textEl.textContent = current.slice(0, i);
    await wait(DELETE_SPEED);
  }
}

async function run(wrapper, textEl, text, shouldLoop) {
  do {
    await typeText(textEl, text);
    await wait(HOLD_FULL_MS);
    if (!shouldLoop) break;
    await deleteText(textEl);
    await wait(HOLD_EMPTY_MS);
  } while (shouldLoop);
}
```

## Composition

Both variants on the same page: rotator in the hero heading, type-on in a terminal block below. Each initializes independently. Shared cursor keyframe.

## Reduced Motion

```javascript
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (reducedMotion) {
  text.textContent = items[0]; // show first word, no animation
  return;
}
```

CSS fallback:
```css
@media (prefers-reduced-motion: reduce) {
  .rotator-type__cursor, .type-on-cursor { animation: none; }
}
```
