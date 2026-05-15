# Terminal Display Patterns

Terminal-style status blocks with timestamps, dot-leader fills, progress labels, and search result counters.

## Status Typing with Progress Sync

Status items type sequentially, each synced with a progress bar increment.

### Timing Constants

| Constant | Default | Notes |
|----------|---------|-------|
| `TYPE_SPEED` | 45 | Base ms per character |
| `TYPE_VARIANCE` | 18 | Random variance |
| `DELETE_SPEED` | 24 | Ms per delete character |
| `HOLD_FULL_MS` | 2400 | Hold after typing complete |
| `HOLD_EMPTY_MS` | 160 | Hold after deleting |
| `PROGRESS_STEP_DURATION` | 450 | Ms per progress step |
| `LINGER_CREEP_PERCENT` | 5 | Extra % padding per step |

### Status Item Cleanup

```javascript
function cleanStatusText(text) {
  return text
    .replace(/^\s*\d+\s*\/\s*/i, '')   // strip "001 /" prefix
    .replace(/\s*>{2,}\s*$/g, '')       // strip trailing ">>>"
    .trim();
}
```

### Sequential Status Typing

```javascript
async function runStatusSequence(items, textEl, progressBar, percentEl) {
  const totalSteps = items.length;

  for (let i = 0; i < totalSteps; i++) {
    const item = items[i];

    // Type the status text
    for (let c = 1; c <= item.length; c++) {
      textEl.textContent = item.slice(0, c);
      await wait(TYPE_SPEED + Math.random() * TYPE_VARIANCE);
    }

    // Update progress
    const percent = Math.min(100, ((i + 1) / totalSteps) * 100);
    progressBar.style.width = percent + '%';
    percentEl.textContent = Math.round(percent) + '%';

    await wait(HOLD_FULL_MS);

    // Delete before next item (except last)
    if (i < totalSteps - 1) {
      for (let c = item.length - 1; c >= 0; c--) {
        textEl.textContent = item.slice(0, c);
        await wait(DELETE_SPEED);
      }
      await wait(HOLD_EMPTY_MS);
    }
  }
}
```

## Timestamp Column

```css
.terminal-timestamp {
  font-family: var(--cm-font-mono);
  font-size: var(--cm-mono-size);
  color: var(--cm-text-40);
  flex: 0 0 auto;
}
```

Formats:
- Predetermined: `[10:14:02]`, `[10:14:31]`, etc.
- Real-time: `new Date().toLocaleTimeString('en-US', { hour12: false })`

## Dot-Leader Fill

Same technique as progress-simulation-patterns.md — dynamic dot count based on container width.

```html
<div class="terminal-row">
  <span class="terminal-timestamp">[10:14:02]</span>
  <span class="terminal-dots"></span>
  <span class="terminal-label">QUERY_RECEIVED</span>
</div>
```

```css
.terminal-row {
  display: flex;
  align-items: baseline;
  font-family: var(--cm-font-mono);
  font-size: var(--cm-mono-size);
  padding: 0.25rem 0;
}
.terminal-dots {
  flex: 1 1 auto;
  min-width: 0;
  overflow: hidden;
  white-space: nowrap;
  color: var(--cm-text-20);
}
.terminal-label {
  flex: 0 0 auto;
  color: var(--cm-text-70);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
```

## Search Result Counter

Animated number counting from 0 to target, with label.

```javascript
function animateCounter(el, target, durationMs, label) {
  const start = performance.now();

  function tick(now) {
    const t = Math.min(1, (now - start) / durationMs);
    const eased = 1 - Math.pow(1 - t, 3); // easeOutCubic
    const value = Math.round(target * eased);
    el.textContent = `${Intl.NumberFormat('en-US').format(value)}..${label}`;

    if (t < 1) requestAnimationFrame(tick);
    else el.textContent = `${Intl.NumberFormat('en-US').format(target)}..${label}`;
  }

  requestAnimationFrame(tick);
}
```

Display format:
```
1,234..........matches found
2,356..SIMILAR
```

Two counters running independently:
```javascript
animateCounter(matchesEl, 1234, 3000, 'MATCHES');
animateCounter(similarEl, 2356, 3500, 'SIMILAR');
```

## Full Terminal Block Layout

```css
.terminal-block {
  background: var(--cm-surface);
  border: 1px solid var(--cm-border-subtle);
  border-radius: 0.75rem;
  padding: 1.5rem;
  font-family: var(--cm-font-mono);
}

.terminal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--cm-border-subtle);
  margin-bottom: 1rem;
}

.terminal-status-text {
  color: var(--cm-brand);
}

.terminal-results {
  display: flex;
  gap: 2rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--cm-border-subtle);
}

.result-value {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--cm-text);
}

.result-label {
  font-size: var(--cm-mono-size);
  color: var(--cm-text-40);
  text-transform: uppercase;
}
```

## Reduced Motion

Show final state with all items visible:
```javascript
if (reducedMotion) {
  textEl.textContent = items[items.length - 1];
  progressBar.style.width = '100%';
  percentEl.textContent = '100%';
  matchesEl.textContent = `${formatNumber(1234)}..MATCHES`;
  similarEl.textContent = `${formatNumber(2356)}..SIMILAR`;
  return;
}
```
