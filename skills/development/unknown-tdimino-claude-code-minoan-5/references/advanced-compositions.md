# Advanced Compositions

Composite animation patterns observed on ConductorAI.com that combine multiple base modes. Use these when building custom `--mode full-page` layouts or freeform compositions beyond the standard 8 modes.

## 1. Workflow / Decision Tree Graph

Animated flowchart showing an agentic pipeline with nodes, status badges, and dashed connection lines. Simulates a live orchestration system.

### State Machine

```
         ┌─────────────┐
         │ TARGET DOCS  │ ◆ COMPLETE
         └──────┬───────┘
           ┌────┴────┐
     ┌─────┴──────┐  ┌──────┴──────┐
     │ IDENTIFY   │  │ FIND AND    │
     │ SECTIONS   │  │ REPLACE     │
     │ [ACTION]   │  │ [ENTITY]    │
     │◆ COMPLETE  │  │◆ PROCESSING │
     └─────┬──────┘  └─────────────┘
           │
     ┌─────┴──────┐
     │   CREATE    │
     └─────┬──────┘
     ┌─────┴──────────┐
     │ ENTER REQUEST…  │
     └────────────────┘
```

### DOM Structure

```html
<div class="wf-graph" aria-label="Workflow pipeline">
  <div class="wf-node wf-node--root" data-status="complete">
    <span class="wf-badge wf-badge--complete">COMPLETE</span>
    <div class="wf-node-body">TARGET DOCUMENTS &gt;&gt;&gt;</div>
  </div>
  <svg class="wf-lines" aria-hidden="true">
    <!-- Dashed connection lines rendered via SVG -->
  </svg>
  <div class="wf-children">
    <div class="wf-node" data-status="complete">
      <span class="wf-badge wf-badge--complete">COMPLETE</span>
      <div class="wf-node-body">IDENTIFY NON COMPLIANT SECTIONS [ACTION]</div>
    </div>
    <div class="wf-node" data-status="processing">
      <span class="wf-badge wf-badge--processing">PROCESSING</span>
      <div class="wf-node-body">FIND AND REPLACE ENTITY [ENTITY NAME]</div>
    </div>
  </div>
  <div class="wf-node wf-node--input">
    <span class="wf-badge wf-badge--create">CREATE</span>
    <div class="wf-input-field">|ENTER YOUR REQUEST...</div>
  </div>
</div>
```

### CSS

```css
.wf-graph {
  position: relative;
  font-family: var(--cm-font-mono);
  font-size: var(--cm-mono-size);
}

.wf-node {
  background: var(--cm-surface);
  border: 1px solid var(--cm-border);
  padding: 1rem 1.25rem;
  position: relative;
}

.wf-badge {
  position: absolute;
  top: -0.625rem;
  right: 1rem;
  padding: 0.125rem 0.5rem;
  font-size: 0.625rem;
  letter-spacing: 0.06em;
  border: 1px solid;
}

.wf-badge--complete {
  color: var(--cm-success);
  border-color: var(--cm-success);
  background: var(--cm-bg);
}

.wf-badge--processing {
  color: var(--cm-warning);
  border-color: var(--cm-warning);
  background: var(--cm-bg);
}

.wf-badge--create {
  color: var(--cm-text-40);
  border-color: var(--cm-border);
  background: var(--cm-bg);
}

.wf-lines line {
  stroke: var(--cm-brand);
  stroke-width: 1;
  stroke-dasharray: 4 4;
}

.wf-dot {
  fill: var(--cm-brand);
  r: 3;
}
```

### Connection Lines (SVG)

```javascript
function drawConnection(svg, fromEl, toEl) {
  const svgRect = svg.getBoundingClientRect();
  const from = fromEl.getBoundingClientRect();
  const to = toEl.getBoundingClientRect();

  const x1 = from.left + from.width / 2 - svgRect.left;
  const y1 = from.bottom - svgRect.top;
  const x2 = to.left + to.width / 2 - svgRect.left;
  const y2 = to.top - svgRect.top;

  const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
  line.setAttribute('x1', x1);
  line.setAttribute('y1', y1);
  line.setAttribute('x2', x2);
  line.setAttribute('y2', y2);
  svg.appendChild(line);

  [x1, y1, x2, y2].forEach((pos, i) => {
    const dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    dot.setAttribute('cx', i < 2 ? x1 : x2);
    dot.setAttribute('cy', i < 2 ? y1 : y2);
    dot.classList.add('wf-dot');
    svg.appendChild(dot);
  });
}
```

### Animation Choreography

Nodes reveal with stagger, then badges animate in, then connection lines draw with `stroke-dashoffset` transition:

```javascript
const STAGGER = 400;

function animateGraph(nodes, lines, badges) {
  nodes.forEach((node, i) => {
    node.style.opacity = '0';
    node.style.transform = 'translateY(8px)';
    setTimeout(() => {
      node.style.transition = 'opacity 420ms var(--cm-ease-out-cubic), transform 420ms var(--cm-ease-out-cubic)';
      node.style.opacity = '1';
      node.style.transform = 'none';
    }, i * STAGGER);
  });

  const lineDelay = nodes.length * STAGGER;
  lines.forEach(line => {
    const len = line.getTotalLength();
    line.style.strokeDasharray = len;
    line.style.strokeDashoffset = len;
    setTimeout(() => {
      line.style.transition = `stroke-dashoffset 600ms var(--cm-ease-out-cubic)`;
      line.style.strokeDashoffset = '0';
    }, lineDelay);
  });

  const badgeDelay = lineDelay + 600;
  badges.forEach((badge, i) => {
    badge.style.opacity = '0';
    setTimeout(() => {
      badge.style.transition = 'opacity 300ms ease';
      badge.style.opacity = '1';
    }, badgeDelay + i * 200);
  });
}
```

## 2. Multi-Agent Review Composition

Multiple document panels processed simultaneously by named agents. Each panel has an agent label badge and shows different review activity. Dashed lines connect agents to documents, simulating handoffs.

### Agent Badge

```css
.agent-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.25rem 0.625rem;
  font-family: var(--cm-font-mono);
  font-size: 0.625rem;
  letter-spacing: 0.06em;
  background: var(--cm-bg);
  border: 1px solid var(--cm-border);
}

.agent-badge::before {
  content: '';
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--cm-success);
}

.agent-badge[data-status="processing"]::before {
  background: var(--cm-warning);
}
```

### Document Panel Variants

Three visual variants observed on the platform page:

```css
/* Variant 1: Text lines with highlight bar */
.doc-panel--text .doc-line {
  height: 0.5rem;
  background: var(--cm-border-subtle);
  border-radius: 2px;
  margin-bottom: 0.375rem;
}

.doc-panel--text .doc-line.is-highlight {
  background: var(--cm-brand-20);
}

/* Variant 2: Text lines with blue annotation dots */
.doc-panel--annotated .doc-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--cm-brand);
  position: absolute;
}

/* Variant 3: Checklist with checkboxes */
.doc-panel--checklist .check-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.doc-panel--checklist .check-box {
  width: 14px;
  height: 14px;
  border: 1.5px solid var(--cm-brand);
  border-radius: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.doc-panel--checklist .check-box.is-checked {
  background: var(--cm-brand);
}

.doc-panel--checklist .check-box.is-checked::after {
  content: '';
  width: 4px;
  height: 7px;
  border: solid var(--cm-bg);
  border-width: 0 1.5px 1.5px 0;
  transform: rotate(45deg);
}
```

### Choreography

Panels reveal with stagger, then agent badges appear, then checklist items check off sequentially:

```javascript
function animateAgentReview(panels, checkboxes) {
  panels.forEach((panel, i) => {
    panel.style.opacity = '0';
    panel.style.transform = 'translateY(10px)';
    setTimeout(() => {
      panel.style.transition = 'opacity 420ms var(--cm-ease-out-cubic), transform 420ms var(--cm-ease-out-cubic)';
      panel.style.opacity = '1';
      panel.style.transform = 'none';
    }, i * 300);
  });

  const checkDelay = panels.length * 300 + 800;
  checkboxes.forEach((box, i) => {
    setTimeout(() => {
      box.classList.add('is-checked');
    }, checkDelay + i * 600);
  });
}
```

## 3. Reviewer Sidebar / Annotation Thread

A vertical list of reviewer comments alongside a document panel. Mixes human reviewers and AI bots, each with a name, annotation text, and check status. Simulates a collaborative review interface.

### State Machine

```
PENDING ──→ REVIEWING ──→ APPROVED
  ☐           ◌            ✓
```

### DOM Structure

```html
<div class="review-thread">
  <div class="review-comment" data-reviewer="bot" data-status="approved">
    <div class="review-comment-header">
      <span class="reviewer-name">REVIEW BOT</span>
      <span class="reviewer-check is-checked" aria-label="Approved"></span>
    </div>
    <p class="reviewer-note">Matches language used in ESIGN Act</p>
  </div>
  <div class="review-comment" data-reviewer="human" data-status="approved">
    <div class="review-comment-header">
      <span class="reviewer-name">ADAM T.</span>
      <span class="reviewer-check is-checked" aria-label="Approved"></span>
    </div>
    <p class="reviewer-note">Terminology aligns with federal definition</p>
  </div>
  <div class="review-comment" data-reviewer="human" data-status="pending">
    <div class="review-comment-header">
      <span class="reviewer-name">JAMES N.</span>
      <span class="reviewer-check" aria-label="Pending"></span>
    </div>
    <p class="reviewer-note">Replace informal terminology</p>
  </div>
  <div class="review-comment" data-reviewer="bot" data-status="reviewing">
    <div class="review-comment-header">
      <span class="reviewer-name">REVIEW BOT</span>
      <span class="reviewer-check" aria-label="Processing"></span>
    </div>
    <p class="reviewer-note">Processing...</p>
  </div>
</div>
```

### CSS

```css
.review-thread {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.review-comment {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 0.5rem 0.75rem;
  border-bottom: 1px solid var(--cm-border-subtle);
}

.review-comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.reviewer-name {
  font-family: var(--cm-font-mono);
  font-size: var(--cm-mono-size);
  font-weight: 600;
  color: var(--cm-brand);
}

.reviewer-note {
  font-family: var(--cm-font);
  font-size: var(--cm-mono-size);
  color: var(--cm-text-70);
  line-height: 1.4;
}

.reviewer-check {
  width: 16px;
  height: 16px;
  border: 1.5px solid var(--cm-border);
  border-radius: 2px;
}

.reviewer-check.is-checked {
  background: var(--cm-brand);
  border-color: var(--cm-brand);
  position: relative;
}

.reviewer-check.is-checked::after {
  content: '';
  position: absolute;
  left: 4px;
  top: 1px;
  width: 4px;
  height: 8px;
  border: solid var(--cm-bg);
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}
```

### Animation

Comments reveal with stagger. Pending items transition to approved one by one with checkbox check animation:

```javascript
function animateReviewThread(comments) {
  comments.forEach((comment, i) => {
    comment.style.opacity = '0';
    comment.style.transform = 'translateX(10px)';
    setTimeout(() => {
      comment.style.transition = 'opacity 300ms ease, transform 300ms ease';
      comment.style.opacity = '1';
      comment.style.transform = 'none';
    }, i * 200);
  });

  const pending = [...document.querySelectorAll('.review-comment[data-status="pending"]')];
  const startDelay = comments.length * 200 + 1200;

  pending.forEach((comment, i) => {
    setTimeout(() => {
      const check = comment.querySelector('.reviewer-check');
      check.classList.add('is-checked');
      comment.dataset.status = 'approved';
    }, startDelay + i * 800);
  });
}
```

## 4. Search Input Simulation

A fake search field that types a query, submits, then shows status badges and metric responses. Combines typewriter effect with status badge animation.

### DOM Structure

```html
<div class="search-sim">
  <div class="search-input-row">
    <input class="search-field" type="text" readonly aria-label="Search query">
    <button class="search-submit" aria-label="Submit search">
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
        <path d="M1 7h12M8 2l5 5-5 5" stroke="currentColor" stroke-width="1.5"/>
      </svg>
    </button>
  </div>
  <div class="search-badges" aria-live="polite">
    <span class="search-badge search-badge--submitted" hidden>QUERY SUBMITTED</span>
    <span class="search-badge search-badge--match" hidden>6M CONFIDENCE MATCH</span>
  </div>
</div>
```

### CSS

```css
.search-field {
  flex: 1;
  background: var(--cm-bg);
  border: 1px solid var(--cm-border);
  padding: 0.5rem 0.75rem;
  font-family: var(--cm-font-mono);
  font-size: var(--cm-mono-size);
  color: var(--cm-text);
  caret-color: var(--cm-brand);
}

.search-submit {
  background: var(--cm-brand);
  color: var(--cm-brand-text);
  border: none;
  padding: 0.5rem 0.75rem;
  cursor: pointer;
}

.search-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.25rem 0.625rem;
  font-family: var(--cm-font-mono);
  font-size: 0.625rem;
  letter-spacing: 0.06em;
  border: 1px solid var(--cm-border);
  color: var(--cm-text-70);
}

.search-badge::before {
  content: '';
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.search-badge--submitted::before { background: var(--cm-brand); }
.search-badge--match::before { background: var(--cm-success); }
```

### Choreography

Reuses typewriter internals. After typing completes, submit button pulses, then badges appear with stagger:

```javascript
const QUERY = 'FIND "ANTHONY K.M.", REVIEW...';
const TYPE_SPEED = 45;
const TYPE_VARIANCE = 18;

function animateSearch(field, submitBtn, badges) {
  let i = 0;

  function typeNext() {
    if (i < QUERY.length) {
      field.value += QUERY[i];
      i++;
      setTimeout(typeNext, TYPE_SPEED + Math.random() * TYPE_VARIANCE);
    } else {
      setTimeout(() => {
        submitBtn.style.transform = 'scale(0.95)';
        setTimeout(() => {
          submitBtn.style.transform = 'none';
          showBadges(badges);
        }, 150);
      }, 400);
    }
  }

  typeNext();
}

function showBadges(badges) {
  badges.forEach((badge, i) => {
    setTimeout(() => {
      badge.hidden = false;
      badge.style.opacity = '0';
      requestAnimationFrame(() => {
        badge.style.transition = 'opacity 300ms ease';
        badge.style.opacity = '1';
      });
    }, i * 400);
  });
}
```

## 5. Comparison Bar Chart

Two vertical bars side by side — a short "before" bar and a tall branded "after" bar — with an annotation arrow showing the multiplier. Used for metric callouts on case study pages.

### DOM Structure

```html
<div class="comparison-chart" aria-label="10x improvement in compliance capacity">
  <div class="comparison-bar comparison-bar--before">
    <div class="comparison-fill" style="--bar-height: 20%"></div>
    <span class="comparison-label">MANUAL COMPLIANCE CAPACITY</span>
  </div>
  <div class="comparison-annotation" aria-hidden="true">
    <span class="comparison-arrow"></span>
    <span class="comparison-multiplier">10x</span>
  </div>
  <div class="comparison-bar comparison-bar--after">
    <div class="comparison-fill" style="--bar-height: 100%"></div>
    <span class="comparison-label">AUTOMATED COMPLIANCE CAPACITY WITH CONDUCTOR AI</span>
  </div>
</div>
```

### CSS

```css
.comparison-chart {
  display: flex;
  align-items: flex-end;
  gap: 1.5rem;
  height: 20rem;
}

.comparison-bar {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  flex: 1;
}

.comparison-fill {
  width: 100%;
  height: var(--bar-height);
  transition: height 1200ms var(--cm-ease-out-cubic);
}

.comparison-bar--before .comparison-fill {
  background: var(--cm-border);
}

.comparison-bar--after .comparison-fill {
  background: var(--cm-brand);
}

.comparison-label {
  font-family: var(--cm-font-mono);
  font-size: 0.625rem;
  color: var(--cm-text-40);
  text-align: center;
  margin-top: 0.75rem;
  letter-spacing: 0.06em;
}

.comparison-annotation {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: var(--cm-text-40);
  font-family: var(--cm-font-mono);
  font-size: var(--cm-mono-size);
}

.comparison-arrow {
  display: block;
  width: 1px;
  height: 6rem;
  background: var(--cm-text-20);
  position: relative;
}

.comparison-arrow::before,
.comparison-arrow::after {
  content: '';
  position: absolute;
  left: -3px;
  border: 4px solid transparent;
}

.comparison-arrow::before {
  top: 0;
  border-bottom-color: var(--cm-text-20);
}

.comparison-arrow::after {
  bottom: 0;
  border-top-color: var(--cm-text-20);
}
```

### Animation

Bars grow from zero height on IntersectionObserver trigger:

```javascript
function animateComparison(chart) {
  const fills = chart.querySelectorAll('.comparison-fill');
  const multiplier = chart.querySelector('.comparison-multiplier');

  fills.forEach(fill => {
    fill.style.height = '0%';
  });

  if (multiplier) {
    multiplier.style.opacity = '0';
  }

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        requestAnimationFrame(() => {
          fills.forEach(fill => {
            fill.style.height = fill.style.getPropertyValue('--bar-height');
          });
        });

        if (multiplier) {
          setTimeout(() => {
            multiplier.style.transition = 'opacity 400ms ease';
            multiplier.style.opacity = '1';
          }, 800);
        }

        observer.disconnect();
      }
    });
  }, { threshold: 0.3 });

  observer.observe(chart);
}
```

## 6. Dot-Matrix Number Display

Large hero metrics rendered in a pixelated/dashed-outline style that evokes a data dashboard. Numbers like "330", ">90%", "98%" appear as retro dot-matrix numerals rather than standard font glyphs.

### Technique: SVG Text with Dashed Stroke

```css
.dot-matrix-number {
  font-family: var(--cm-font-mono);
  font-size: clamp(4rem, 8vw + 1rem, 8rem);
  font-weight: 700;
  fill: none;
  stroke: var(--cm-brand);
  stroke-width: 2;
  stroke-dasharray: 3 3;
  paint-order: stroke;
}
```

### DOM Structure

```html
<div class="metric-callout">
  <svg class="metric-svg" viewBox="0 0 300 100" aria-hidden="true">
    <text class="dot-matrix-number" x="50%" y="75%" text-anchor="middle">330</text>
  </svg>
  <span class="sr-only">330</span>
  <span class="metric-label">HOURS SAVED AT A RECENT EXERCISE</span>
</div>
```

### CSS

```css
.metric-callout {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.metric-svg {
  width: 100%;
  max-width: 20rem;
}

.metric-label {
  font-family: var(--cm-font-mono);
  font-size: var(--cm-mono-size);
  color: var(--cm-text-40);
  letter-spacing: 0.06em;
  text-align: center;
}
```

### Animation: Counting + Stroke Draw

```javascript
function animateMetric(svgText, targetValue, duration) {
  const isPercent = targetValue.includes('%');
  const prefix = targetValue.startsWith('>') ? '>' : '';
  const numericTarget = parseInt(targetValue.replace(/[^0-9]/g, ''), 10);
  const suffix = isPercent ? '%' : '';

  let start = null;

  function tick(now) {
    if (!start) start = now;
    const t = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - t, 3);
    const current = Math.round(numericTarget * eased);
    svgText.textContent = prefix + current + suffix;

    if (t < 1) {
      requestAnimationFrame(tick);
    }
  }

  requestAnimationFrame(tick);
}
```

## Decorative Framing: Corner Brackets

Observed framing nearly every section and card on the site. Purely decorative — use `aria-hidden="true"`.

```css
.bracket-frame {
  position: relative;
}

.bracket-frame::before,
.bracket-frame::after {
  content: '';
  position: absolute;
  width: 12px;
  height: 12px;
  border-color: var(--cm-border);
  border-style: solid;
  pointer-events: none;
}

.bracket-frame::before {
  top: 0;
  left: 0;
  border-width: 1px 0 0 1px;
}

.bracket-frame::after {
  bottom: 0;
  right: 0;
  border-width: 0 1px 1px 0;
}
```

For all four corners, add a wrapper element:

```html
<div class="bracket-frame" aria-hidden="true">
  <span class="bracket-tl"></span>
  <span class="bracket-br"></span>
</div>
```

```css
.bracket-tl { top: 0; right: 0; border-width: 1px 1px 0 0; }
.bracket-br { bottom: 0; left: 0; border-width: 0 0 1px 1px; }
```

## Composition Guidance

These patterns are designed to be combined with the base 8 modes:

| Advanced Pattern | Combines With | Example |
|-----------------|---------------|---------|
| Workflow graph | Terminal + progress | Pipeline dashboard with live node status |
| Multi-agent review | File review + stagger | Parallel document processing display |
| Reviewer sidebar | File review | Collaborative review interface |
| Search input sim | Typewriter + terminal | Search-driven investigation demo |
| Comparison bar | Stagger reveal | Case study metrics section |
| Dot-matrix number | Stagger reveal | Hero metrics with counting animation |
| Corner brackets | All patterns | Section framing (add to any panel) |

When composing, follow the full-page template's pattern: each section gets its own IntersectionObserver trigger, visibility API integration applies to the entire page's animation loops, and all `--cm-*` tokens propagate through.
