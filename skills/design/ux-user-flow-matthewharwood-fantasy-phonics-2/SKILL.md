---
name: ux-user-flow
description: Navigation and user flow patterns including routing, state management, progressive disclosure, and game progression. Use when designing multi-step flows, game phases, or navigation structures. (project)
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# UX User Flow Skill

Navigation architecture and user journey patterns for single-page game applications. This skill covers routing, state-driven UI, and progressive disclosure.

## State-Based Routing

### Game State Machine

```javascript
const GAME_STATES = {
  loading: 'game-loading',
  playing: 'game-playing',
  paused: 'game-paused',
  complete: 'game-complete',
  menu: 'game-menu'
};

class GameRouter {
  #state = GAME_STATES.loading;

  get state() {
    return this.#state;
  }

  set state(newState) {
    const oldState = this.#state;
    this.#state = newState;

    document.body.dataset.state = newState;

    this.dispatchEvent(new CustomEvent('state-change', {
      detail: { from: oldState, to: newState }
    }));
  }
}
```

### CSS State Display

```css
/* Hide all views by default */
[data-view] {
  display: none;
}

/* Show view matching state */
[data-state="game-loading"] [data-view="loading"],
[data-state="game-playing"] [data-view="playing"],
[data-state="game-menu"] [data-view="menu"] {
  display: block;
}
```

### URL Hash Routing

```javascript
class HashRouter {
  constructor() {
    window.addEventListener('hashchange', () => this.#handleRoute());
    this.#handleRoute();
  }

  #handleRoute() {
    const hash = window.location.hash.slice(1) || 'home';
    this.dispatchEvent(new CustomEvent('route', {
      detail: { route: hash }
    }));
  }

  navigate(route) {
    window.location.hash = route;
  }
}
```

## Game Phase Navigation

### Phase Progression

```javascript
const PHASES = ['word', 'collision', 'mutation', 'story'];

class PhaseManager {
  #currentPhase = 'word';
  #completedPhases = new Set();

  get currentPhase() {
    return this.#currentPhase;
  }

  canAccess(phase) {
    const index = PHASES.indexOf(phase);
    if (index === 0) return true;
    const prevPhase = PHASES[index - 1];
    return this.#completedPhases.has(prevPhase);
  }

  completePhase(phase) {
    this.#completedPhases.add(phase);
    const nextIndex = PHASES.indexOf(phase) + 1;
    if (nextIndex < PHASES.length) {
      this.#currentPhase = PHASES[nextIndex];
    }
  }
}
```

### Phase Indicator UI

```html
<phase-indicator
  phases="word,collision,mutation,story"
  current="word">
</phase-indicator>
```

## Multi-Step Flows

### Wizard Pattern

Steps are stored as direct references during construction - NO querySelector:

```javascript
class StepWizard extends HTMLElement {
  #steps = [];  // Direct element references
  #currentStep = 0;

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });

    // Build steps during construction, store direct references
    const stepData = ['Step 1', 'Step 2', 'Step 3'];
    stepData.forEach(title => {
      const step = document.createElement('div');
      step.className = 'step';
      step.setAttribute('part', 'step');
      step.textContent = title;
      this.#steps.push(step);  // Store direct reference
      this.shadowRoot.appendChild(step);
    });

    this.#updateView();
  }

  connectedCallback() {
    this.addEventListener('click', this);
    this.addEventListener('keydown', this);
  }

  disconnectedCallback() {
    this.removeEventListener('click', this);
    this.removeEventListener('keydown', this);
  }

  handleEvent(e) {
    // Handle navigation via events
  }

  next() {
    if (this.#currentStep < this.#steps.length - 1) {
      this.#currentStep++;
      this.#updateView();
    }
  }

  previous() {
    if (this.#currentStep > 0) {
      this.#currentStep--;
      this.#updateView();
    }
  }

  #updateView() {
    // Use direct references - never querySelector
    this.#steps.forEach((step, i) => {
      step.hidden = i !== this.#currentStep;
      step.setAttribute('aria-current', i === this.#currentStep ? 'step' : 'false');
    });
  }
}

customElements.define('step-wizard', StepWizard);
```

### Progress Tracking

```html
<ol class="step-progress" aria-label="Progress">
  <li data-status="complete">Create Account</li>
  <li data-status="current" aria-current="step">Choose Avatar</li>
  <li data-status="pending">Start Game</li>
</ol>
```

## Progressive Disclosure

### Reveal on Interaction

```javascript
class ExpandableSection extends HTMLElement {
  handleEvent(e) {
    if (e.type === 'click') {
      const expanded = this.getAttribute('aria-expanded') === 'true';
      this.setAttribute('aria-expanded', !expanded);
      this.#content.hidden = expanded;
    }
  }
}
```

### Conditional Rendering

```javascript
render() {
  // Only show advanced options when enabled
  if (this.#showAdvanced) {
    this.#advancedSection.hidden = false;
  }

  // Unlock features based on progress
  this.#lockedFeatures.forEach(feature => {
    const isUnlocked = this.#progress >= feature.requiredProgress;
    feature.element.toggleAttribute('locked', !isUnlocked);
    feature.element.setAttribute('aria-disabled', !isUnlocked);
  });
}
```

### Just-in-Time Help

```javascript
#showHintIfNeeded() {
  const attempts = this.#failedAttempts;
  if (attempts >= 3) {
    this.#showHint('mild');
  }
  if (attempts >= 5) {
    this.#showHint('strong');
  }
}
```

## Menu Navigation

### Keyboard Navigation

```javascript
handleEvent(e) {
  if (e.type === 'keydown') {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        this.#focusNext();
        break;
      case 'ArrowUp':
        e.preventDefault();
        this.#focusPrevious();
        break;
      case 'Home':
        e.preventDefault();
        this.#focusFirst();
        break;
      case 'End':
        e.preventDefault();
        this.#focusLast();
        break;
      case 'Escape':
        this.close();
        break;
    }
  }
}
```

### Menu Structure

```html
<nav aria-label="Game menu">
  <ul role="menu">
    <li role="none">
      <button role="menuitem" aria-current="page">Word Phase</button>
    </li>
    <li role="none">
      <button role="menuitem">Collision Phase</button>
    </li>
    <li role="none">
      <button role="menuitem" aria-disabled="true">Story Phase</button>
    </li>
  </ul>
</nav>
```

## View Transitions

### Crossfade Views

```css
[data-view] {
  opacity: 0;
  transition: opacity 0.2s ease;
  pointer-events: none;
}

[data-view].active {
  opacity: 1;
  pointer-events: auto;
}
```

### Slide Transitions

```css
[data-view] {
  transform: translateX(100%);
  transition: transform 0.3s ease;
}

[data-view].active {
  transform: translateX(0);
}

[data-view].exiting {
  transform: translateX(-100%);
}
```

## Focus Management

### On View Change

Store focus target references during construction - NO querySelector:

```javascript
class ViewRouter extends HTMLElement {
  #views = new Map();       // view name -> { element, focusTarget }
  #currentView = null;

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });

    // Build views during construction
    const viewConfigs = [
      { name: 'home', title: 'Home' },
      { name: 'game', title: 'Game' },
      { name: 'settings', title: 'Settings' }
    ];

    viewConfigs.forEach(config => {
      const view = document.createElement('div');
      view.className = 'view';
      view.setAttribute('data-view', config.name);

      // Create and store focus target reference
      const heading = document.createElement('h1');
      heading.textContent = config.title;
      heading.setAttribute('tabindex', '-1');  // Focusable but not in tab order
      view.appendChild(heading);

      // Store both view and focus target as direct references
      this.#views.set(config.name, {
        element: view,
        focusTarget: heading  // Direct reference for focus
      });

      this.shadowRoot.appendChild(view);
    });
  }

  #navigateTo(viewName) {
    // Hide current view
    if (this.#currentView) {
      this.#currentView.element.hidden = true;
    }

    // Show new view
    const view = this.#views.get(viewName);
    if (view) {
      view.element.hidden = false;
      this.#currentView = view;

      // Focus using direct reference - NO querySelector
      view.focusTarget?.focus();
    }
  }
}
```

### Skip Links

```html
<a href="#main-game" class="skip-link">Skip to game</a>
<a href="#word-list" class="skip-link">Skip to word list</a>
```

## History Management

### Browser Back/Forward

```javascript
class HistoryManager {
  pushState(state, title, url) {
    history.pushState(state, title, url);
  }

  connectedCallback() {
    window.addEventListener('popstate', (e) => {
      if (e.state) {
        this.#restoreState(e.state);
      }
    });
  }

  #restoreState(state) {
    this.dispatchEvent(new CustomEvent('history-navigate', {
      detail: state
    }));
  }
}
```

## Game Progression Patterns

### Save Points

```javascript
async saveProgress() {
  const progress = {
    phase: this.#currentPhase,
    completedWords: Array.from(this.#completedWords),
    score: this.#score,
    timestamp: Date.now()
  };

  await this.#storage.set('progress', progress);
}

async loadProgress() {
  const progress = await this.#storage.get('progress');
  if (progress) {
    this.#restoreProgress(progress);
  }
}
```

### Session Continuity

```javascript
connectedCallback() {
  // Check for saved session
  this.#checkSavedSession();
}

#checkSavedSession() {
  const saved = this.#storage.get('session');
  if (saved) {
    this.#showResumePrompt(saved);
  }
}

#showResumePrompt(session) {
  this.dispatchEvent(new CustomEvent('resume-available', {
    detail: {
      phase: session.phase,
      progress: session.progress
    }
  }));
}
```

## Error Recovery

### Graceful Degradation

```javascript
async #loadPhase(phase) {
  try {
    const data = await this.#fetchPhaseData(phase);
    this.#renderPhase(data);
  } catch (error) {
    this.#showErrorRecovery({
      message: 'Failed to load phase',
      retry: () => this.#loadPhase(phase),
      fallback: () => this.#loadOfflineData(phase)
    });
  }
}
```

### Offline Support

```javascript
if (!navigator.onLine) {
  this.#showOfflineMode();
  this.#loadCachedContent();
}

window.addEventListener('online', () => {
  this.#syncProgress();
  this.#showOnlineMode();
});
```
