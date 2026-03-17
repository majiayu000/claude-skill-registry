---
name: ux-prototyping
description: Create interactive single-file HTML prototypes for UX validation. Use when the user asks to create a prototype, mockup, or interactive wireframe based on specs/architecture/ux.md or any UX specification. Triggers include requests like "create a prototype", "build a prototype from the UX spec", "make an interactive mockup", "prototype the user flow", or "validate the UX".
---

# UX Prototyping Skill

Create single-file HTML prototypes focused on validating user flows, interaction patterns, and information architecture. Prioritize UX fidelity over visual polish.

## Workflow

1. **Read the UX spec** at `specs/architecture/ux.md` (or user-specified path)
2. **Identify core flows** - Extract user journeys, screens, states, and interactions
3. **Build prototype** - Create single HTML file with all screens and interactions
4. **Output** - Save to `/mnt/user-data/outputs/prototype.html`

## Prototype Structure

Generate a single HTML file containing:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[App Name] - UX Prototype</title>
  <style>/* All CSS inline */</style>
</head>
<body>
  <!-- All screens as sections -->
  <!-- Navigation/state management -->
  <script>/* All JS inline */</script>
</body>
</html>
```

## Core Principles

### UX First, UI Second
- **Do**: Implement all user flows, states, transitions, error states, empty states
- **Do**: Make interactions feel responsive and logical
- **Do**: Show realistic data and content hierarchy
- **Defer**: Pixel-perfect styling, animations, brand colors (use clean defaults)

### Screen Management Pattern
Implement screens as `<section>` elements with `data-screen` attributes:

```javascript
function showScreen(screenId) {
  document.querySelectorAll('[data-screen]').forEach(s => s.hidden = true);
  document.querySelector(`[data-screen="${screenId}"]`).hidden = false;
}
```

### State Management Pattern
Use a simple state object:

```javascript
const state = { currentScreen: 'home', user: null, data: [] };
function setState(updates) { Object.assign(state, updates); render(); }
```

## Essential UX Elements

### 1. User Flows
- Primary task completion paths
- Alternative/secondary flows  
- Error recovery flows

### 2. Screen States
- **Empty** - First-time user, no data
- **Loading** - Skeleton or spinner
- **Error** - Network/validation errors
- **Success** - Confirmations
- **Partial** - Some data loaded

### 3. Interactions
- Form inputs with validation
- Button states (hover/active/disabled)
- Screen navigation
- Modal/overlay behaviors

## Base Styles

```css
* { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg: #f8fafc; --surface: #fff; --text: #1e293b;
  --text-muted: #64748b; --primary: #3b82f6; --border: #e2e8f0;
  --success: #22c55e; --error: #ef4444; --radius: 8px;
}
body { font-family: system-ui, sans-serif; background: var(--bg); color: var(--text); }
[data-screen] { display: none; }
[data-screen].active { display: block; }
.card { background: var(--surface); border-radius: var(--radius); padding: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.btn { padding: 0.625rem 1.25rem; border-radius: var(--radius); font-weight: 500; cursor: pointer; border: none; }
.btn-primary { background: var(--primary); color: white; }
.btn-primary:hover { background: #2563eb; }
.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }
.input { width: 100%; padding: 0.625rem; border: 1px solid var(--border); border-radius: var(--radius); }
.input:focus { outline: none; border-color: var(--primary); }
.container { max-width: 480px; margin: 0 auto; padding: 1rem; }
.stack > * + * { margin-top: 1rem; }
.empty-state { text-align: center; padding: 3rem; color: var(--text-muted); }
.error-msg { color: var(--error); font-size: 0.875rem; }
```

## Validation Checklist

Before delivering, verify:
- [ ] All screens from spec implemented
- [ ] Primary flow completable end-to-end
- [ ] Empty/error/loading states shown
- [ ] Navigation works correctly
- [ ] Interactive elements have feedback
- [ ] Responsive on mobile viewport

## Output

Save to `/mnt/user-data/outputs/prototype.html` (or descriptive name like `prototype-onboarding.html`).
