# File Review Patterns

A list of files progresses through states (Unreviewed → Processing → Reviewed) with staggered timing, simulating a document review workflow.

## State Machine

```
UNREVIEWED ──→ PROCESSING ──→ REVIEWED
(gray dot)    (blue+spinner)  (green dot)
"Ready"       "Reviewing"     "Reviewed"
"Unreviewed"                  "Done"
```

One-directional transitions. Each file transitions independently with staggered start times.

## DOM Structure

```html
<div class="file-list">
  <!-- Template rows (hidden, cloned per file) -->
  <div class="file-item template" data-state="reviewed" style="display:none">
    <div class="file-icon"><!-- SVG --></div>
    <div class="file-name"></div>
    <div class="file-ext"></div>
    <div class="file-status">Done</div>
    <div class="file-review-status">
      <div class="review-dot is-reviewed"></div>
      <span>Reviewed</span>
    </div>
  </div>
  <div class="file-item template" data-state="processing" style="display:none">
    <div class="file-icon"><!-- SVG --></div>
    <div class="file-name"></div>
    <div class="file-ext"></div>
    <div class="file-status">Processing</div>
    <div class="file-review-status">
      <div class="review-dot is-processing"></div>
      <span>Reviewing</span>
    </div>
  </div>
  <div class="file-item template" data-state="unreviewed" style="display:none">
    <div class="file-icon"><!-- SVG --></div>
    <div class="file-name"></div>
    <div class="file-ext"></div>
    <div class="file-status">Ready</div>
    <div class="file-review-status">
      <div class="review-dot"></div>
      <span>Unreviewed</span>
    </div>
  </div>
</div>
```

## SVG File Icon

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="12" height="15" viewBox="0 0 12 15" fill="none">
  <path opacity="0.4" d="M3.5 5.5H8.5M3.5 7.5H8.5M3.5 9.5H8.5M0.5 0.5H8.5L11.5 3.5V14.5H0.5V0.5Z"
        stroke="currentColor"/>
</svg>
```

## Template Cloning

```javascript
function parseExt(filename) {
  const match = filename.match(/(\.[a-z0-9]+)$/i);
  return match ? match[1] : '';
}

function stripIds(el) {
  el.removeAttribute('id');
  el.querySelectorAll('[id]').forEach(n => n.removeAttribute('id'));
  return el;
}

function createRow(template, filename) {
  const row = stripIds(template.cloneNode(true));
  row.classList.remove('template');
  row.style.display = '';
  row.querySelector('.file-name').textContent = filename;
  row.querySelector('.file-ext').textContent = parseExt(filename);
  return row;
}
```

## Status Indicators

```css
.review-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--cm-text-40);
}

.review-dot.is-reviewed {
  background: var(--cm-success);
}

.review-dot.is-processing {
  background: var(--cm-brand);
  animation: pulse 1.2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

## Transition Choreography

```javascript
const PROCESS_DURATION = 2000;
const STAGGER_DELAY = 800;

function animateReview(files, container) {
  const templates = {
    unreviewed: container.querySelector('[data-state="unreviewed"]'),
    processing: container.querySelector('[data-state="processing"]'),
    reviewed:   container.querySelector('[data-state="reviewed"]')
  };

  const rows = files.map(filename => {
    const row = createRow(templates.unreviewed, filename);
    row.style.opacity = '0';
    row.style.transform = 'translateY(5px)';
    container.appendChild(row);
    return { el: row, filename, state: 'unreviewed' };
  });

  // Reveal all rows with stagger
  rows.forEach((r, i) => {
    setTimeout(() => {
      r.el.style.transition = 'opacity 300ms ease, transform 300ms ease';
      r.el.style.opacity = '1';
      r.el.style.transform = 'none';
    }, i * 200);
  });

  // Transition each file through states
  rows.forEach((r, i) => {
    const startDelay = 1000 + (i * STAGGER_DELAY);

    // → processing
    setTimeout(() => {
      transitionState(r, templates.processing, container);
    }, startDelay);

    // → reviewed
    setTimeout(() => {
      transitionState(r, templates.reviewed, container);
    }, startDelay + PROCESS_DURATION);
  });
}

function transitionState(rowData, template, container) {
  const newRow = createRow(template, rowData.filename);
  newRow.style.opacity = '0';
  rowData.el.style.transition = 'opacity 200ms ease';
  rowData.el.style.opacity = '0';

  setTimeout(() => {
    container.replaceChild(newRow, rowData.el);
    rowData.el = newRow;
    requestAnimationFrame(() => {
      newRow.style.transition = 'opacity 200ms ease';
      newRow.style.opacity = '1';
    });
  }, 200);
}
```

## Reduced Motion

Show all files in reviewed state immediately:
```javascript
if (reducedMotion) {
  files.forEach(filename => {
    const row = createRow(templates.reviewed, filename);
    container.appendChild(row);
  });
  return;
}
```
