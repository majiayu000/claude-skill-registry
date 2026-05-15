# Progress Simulation Patterns

Animated progress bar with document counter, dot-leader data rows, and processing indicator.

## Progress Bar Animation

### Constants

| Constant | Default | Notes |
|----------|---------|-------|
| `TOTAL_MS` | 6000 | Full animation duration |
| `START_PROGRESS` | 5 | Starting percentage |
| `END_PROGRESS` | 100 | Final percentage |

### Easing

```javascript
const easeOutCubic = t => 1 - Math.pow(1 - t, 3);
const clamp = (n, min, max) => Math.max(min, Math.min(max, n));
```

### rAF Tick Loop

```javascript
const start = performance.now();

function tick(now) {
  const rawT = clamp((now - start) / TOTAL_MS, 0, 1);
  const eased = easeOutCubic(rawT);
  const progressValue = START_PROGRESS + ((END_PROGRESS - START_PROGRESS) * eased);

  fillEl.style.width = progressValue + '%';
  percentEl.textContent = Math.round(progressValue) + '%';

  if (rawT < 1) requestAnimationFrame(tick);
  else onComplete();
}

requestAnimationFrame(tick);
```

## Document Counter

Counts from 0 to target alongside progress:

```javascript
const docValue = TARGET_DOC_COUNT * eased;
counterEl.textContent = `${Intl.NumberFormat('en-US').format(Math.round(docValue))} documents`;
```

## Dot-Leader Rows

### Layout

```css
.data-row {
  display: flex;
  align-items: baseline;
  width: 100%;
  gap: 0;
}
.data-time  { flex: 0 0 auto; }
.data-dots  { flex: 1 1 auto; min-width: 0; overflow: hidden; white-space: nowrap; }
.data-label { flex: 0 0 auto; text-transform: uppercase; }
```

### Dynamic Dot Fill

Measures container width, calculates how many dots fit:

```javascript
function measureDots(dotsEl) {
  dotsEl.textContent = '';
  const width = dotsEl.clientWidth;
  if (!width) return;

  const probe = document.createElement('span');
  probe.textContent = '.';
  probe.style.cssText = 'visibility:hidden;position:absolute;white-space:pre';
  probe.style.fontFamily = getComputedStyle(dotsEl).fontFamily;
  probe.style.fontSize = getComputedStyle(dotsEl).fontSize;
  document.body.appendChild(probe);
  const dotWidth = probe.getBoundingClientRect().width || 6;
  probe.remove();

  dotsEl.textContent = '.'.repeat(Math.max(0, Math.floor(width / dotWidth)));
}
```

Recalculate on resize (debounced 80ms):
```javascript
let resizeTimer = null;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(updateAllDots, 80);
});
```

## Staggered Row Reveals

Rows start hidden, reveal at staggered intervals:

```javascript
const ROW_STAGGER = [900, 1800, 2700, 3600];

rows.forEach(row => {
  row.classList.add('is-reveal');
  row.style.display = 'none';
});

rows.forEach((row, index) => {
  setTimeout(() => {
    row.style.display = 'flex';
    measureDots(row.querySelector('.data-dots'));
    requestAnimationFrame(() => row.classList.add('is-in'));
  }, ROW_STAGGER[index] || (index * 900));
});
```

CSS transitions:
```css
.data-row.is-reveal {
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 420ms ease, transform 420ms ease;
}
.data-row.is-reveal.is-in {
  opacity: 1;
  transform: translateY(0);
}
```

## Processing Dots

The one case where `setInterval` is acceptable — non-visual text state, not tied to rAF:

```javascript
let dotsCount = 0;
setInterval(() => {
  dotsCount = (dotsCount + 1) % 4;
  processingTextEl.textContent = 'PROCESSING' + '.'.repeat(dotsCount);
}, 420);
```

## Double-Init Guard

```javascript
if (root.dataset.progressInit === 'true') return;
root.dataset.progressInit = 'true';
```

## Reduced Motion

Show final state immediately:
```javascript
if (reducedMotion) {
  fillEl.style.width = '100%';
  percentEl.textContent = '100%';
  counterEl.textContent = `${formatNumber(TARGET_DOC_COUNT)} documents`;
  rows.forEach(row => { row.style.display = 'flex'; row.style.opacity = '1'; });
  return;
}
```
