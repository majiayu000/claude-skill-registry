---
name: dom-apis
description: DOM manipulation and browser APIs including element selection, events, storage, fetch, and modern Web APIs.
sasmp_version: "1.3.0"
bonded_agent: 05-dom-browser-apis
bond_type: PRIMARY_BOND

# Production-Grade Configuration
skill_type: reference
response_format: code_first
max_tokens: 1500

parameter_validation:
  required: [topic]
  optional: [api_type]

retry_logic:
  on_ambiguity: ask_clarification
  fallback: show_common_apis

observability:
  entry_log: "DOM APIs skill activated"
  exit_log: "DOM reference provided"
---

# DOM & Browser APIs Skill

## Quick Reference Card

### Element Selection
```javascript
// Modern (preferred)
document.querySelector('#id');
document.querySelector('.class');
document.querySelectorAll('div.item');

// Scoped
container.querySelector('.child');

// Cache references
const els = {
  form: document.querySelector('#form'),
  input: document.querySelector('#input'),
  btn: document.querySelector('#btn')
};
```

### DOM Manipulation
```javascript
// Safe text (XSS-safe)
el.textContent = userInput;

// Create elements (safest)
const div = document.createElement('div');
div.className = 'card';
div.textContent = title;
parent.appendChild(div);

// Batch updates (performance)
const fragment = document.createDocumentFragment();
items.forEach(item => {
  const li = document.createElement('li');
  li.textContent = item;
  fragment.appendChild(li);
});
list.appendChild(fragment);
```

### Event Handling
```javascript
// Event delegation (best practice)
list.addEventListener('click', (e) => {
  if (e.target.matches('.delete')) {
    e.target.closest('li').remove();
  }
});

// Options
el.addEventListener('click', handler, {
  once: true,      // Remove after first call
  passive: true,   // Never preventDefault
  capture: false   // Bubbling phase
});

// Cleanup with AbortController
const controller = new AbortController();
el.addEventListener('click', handler, { signal: controller.signal });
controller.abort(); // Remove listener
```

### Storage APIs
```javascript
// LocalStorage (persistent)
localStorage.setItem('key', JSON.stringify(data));
const data = JSON.parse(localStorage.getItem('key'));

// SessionStorage (tab-only)
sessionStorage.setItem('token', value);

// Safe wrapper
const storage = {
  get: (k, def = null) => {
    try { return JSON.parse(localStorage.getItem(k)) ?? def; }
    catch { return def; }
  },
  set: (k, v) => localStorage.setItem(k, JSON.stringify(v))
};
```

### Fetch API
```javascript
// GET
const res = await fetch('/api/data');
const data = await res.json();

// POST
await fetch('/api/data', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(data)
});

// With error handling
async function fetchJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}
```

### Modern Web APIs
```javascript
// Intersection Observer (lazy loading)
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.src = e.target.dataset.src;
      observer.unobserve(e.target);
    }
  });
});
document.querySelectorAll('img[data-src]').forEach(img => {
  observer.observe(img);
});

// Clipboard
await navigator.clipboard.writeText(text);

// Geolocation
navigator.geolocation.getCurrentPosition(
  pos => console.log(pos.coords),
  err => console.error(err)
);
```

## Troubleshooting

### Common Issues

| Problem | Symptom | Fix |
|---------|---------|-----|
| Element not found | `null` returned | Check if DOM loaded |
| Event not firing | Handler not called | Verify selector/delegation |
| XSS vulnerability | Script execution | Use `textContent` |
| Memory leak | Growing memory | Remove listeners |

### Debug Checklist
```javascript
// 1. Verify element exists
const el = document.querySelector('#id');
console.assert(el, 'Element not found');

// 2. Check event target
el.addEventListener('click', (e) => {
  console.log('target:', e.target);
  console.log('currentTarget:', e.currentTarget);
});

// 3. Monitor DOM changes
new MutationObserver(console.log)
  .observe(el, { childList: true, subtree: true });
```

## Production Patterns

### Form Handling
```javascript
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(form));

  try {
    btn.disabled = true;
    await submitData(data);
    form.reset();
  } catch (err) {
    showError(err.message);
  } finally {
    btn.disabled = false;
  }
});
```

### Debounced Input
```javascript
const debouncedSearch = debounce(async (query) => {
  const results = await search(query);
  renderResults(results);
}, 300);

input.addEventListener('input', (e) => {
  debouncedSearch(e.target.value);
});
```

## Related

- **Agent 05**: DOM & Browser APIs (detailed learning)
- **Skill: asynchronous**: Fetch and promises
- **Skill: ecosystem**: Framework alternatives
