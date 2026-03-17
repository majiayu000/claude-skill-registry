---
name: web-components
description: Web Component patterns for Oh My Brand! frontend interactivity. Custom element lifecycle, attribute observation, event handling, and accessibility. Use when writing view.ts files.
metadata:
  author: Wesley Smits
  version: "1.0.0"
---

# Web Components

Web Component patterns for frontend interactivity in the Oh My Brand! WordPress FSE theme.

---

## When to Use

- Adding frontend interactivity to blocks (carousels, accordions, lightboxes)
- Creating reusable interactive components
- Handling user interactions (clicks, keyboard, touch)
- Managing component state on the frontend

---

## Reference Files

| File | Purpose |
|------|---------|
| [OmbGalleryCarousel.ts](references/OmbGalleryCarousel.ts) | Full Web Component example (~200 lines) |
| [view.ts](../block-scaffolds/references/view.ts) | Web Component scaffold |

---

## Custom Element Structure

```typescript
class OmbGalleryCarousel extends HTMLElement {
    static observedAttributes = ['visible-images'];

    #gallery: HTMLElement | null = null;
    #items: NodeListOf<HTMLElement> | null = null;
    #currentIndex = 0;

    connectedCallback(): void {
        this.#readAttributes();
        this.#queryElements();
        this.#bindEvents();
        this.#initialize();
    }

    disconnectedCallback(): void {
        this.#unbindEvents();
    }

    attributeChangedCallback(
        name: string,
        oldValue: string | null,
        newValue: string | null
    ): void {
        if (oldValue === newValue) return;
        // Handle attribute change
    }
}

if (!customElements.get('omb-gallery-carousel')) {
    customElements.define('omb-gallery-carousel', OmbGalleryCarousel);
}
```

See [OmbGalleryCarousel.ts](references/OmbGalleryCarousel.ts) for the complete implementation.

---

## Lifecycle Methods

### connectedCallback

Called when element is added to the DOM:

```typescript
connectedCallback(): void {
    this.#readAttributes();    // 1. Read attributes
    this.#queryElements();      // 2. Query child elements
    this.#bindEvents();         // 3. Bind events
    this.#initialize();         // 4. Initialize state
}
```

### disconnectedCallback

Called when element is removed from the DOM:

```typescript
disconnectedCallback(): void {
    this.#unbindEvents();
    if (this.#animationFrame) cancelAnimationFrame(this.#animationFrame);
    if (this.#debounceTimer) clearTimeout(this.#debounceTimer);
}
```

### attributeChangedCallback

Called when observed attribute changes:

```typescript
static observedAttributes = ['visible-images', 'autoplay'];

attributeChangedCallback(
    name: string,
    oldValue: string | null,
    newValue: string | null
): void {
    if (oldValue === newValue) return;

    switch (name) {
        case 'visible-images':
            this.#visibleImages = newValue ? parseInt(newValue, 10) : 3;
            this.#updateLayout();
            break;
        case 'autoplay':
            newValue !== null ? this.#startAutoplay() : this.#stopAutoplay();
            break;
    }
}
```

---

## Attribute Handling

### Boolean Attributes

```typescript
const hasAutoplay = this.hasAttribute('autoplay');
this.setAttribute('loading', '');     // Add
this.removeAttribute('loading');       // Remove
this.toggleAttribute('loading');       // Toggle
```

### Value Attributes

```typescript
const value = this.getAttribute('visible-images');
const parsed = value ? parseInt(value, 10) : 3;
this.setAttribute('visible-images', '4');
```

### Data Attributes

```typescript
const config = JSON.parse(this.dataset.config || '{}');
this.dataset.state = 'loading';
```

---

## Event Handling

### Arrow Function Methods

Use arrow functions to preserve `this` context:

```typescript
class OmbComponent extends HTMLElement {
    #handleClick = (event: MouseEvent): void => {
        event.preventDefault();
        this.#doSomething();
    };

    #bindEvents(): void {
        this.addEventListener('click', this.#handleClick);
    }

    #unbindEvents(): void {
        this.removeEventListener('click', this.#handleClick);
    }
}
```

### Custom Events

```typescript
this.dispatchEvent(
    new CustomEvent('omb-gallery:slide-change', {
        bubbles: true,
        detail: { index: this.#currentIndex, total: this.#items?.length ?? 0 },
    })
);
```

### Event Delegation

```typescript
#handleContainerClick = (event: MouseEvent): void => {
    const target = event.target as HTMLElement;
    const item = target.closest('[data-gallery-item]');
    if (item) this.#handleItemClick(item as HTMLElement);
};
```

---

## DOM Queries

### Query and Cache Elements

```typescript
#queryElements(): void {
    this.#container = this.querySelector('[data-container]');
    this.#items = this.querySelectorAll('[data-item]');
    this.#button = this.querySelector('button') as HTMLButtonElement | null;
}
```

### Null Safety

```typescript
// Guard clause
if (!this.#container) return;

// Optional chaining
this.#button?.click();

// Nullish coalescing
const count = this.#items?.length ?? 0;
```

---

## Accessibility

### Live Regions

```typescript
#announce(): void {
    if (!this.#liveRegion) return;
    this.#liveRegion.textContent = `Showing image ${this.#currentIndex + 1} of ${this.#items?.length}`;
}
```

### Keyboard Navigation

```typescript
#handleKeydown = (event: KeyboardEvent): void => {
    switch (event.key) {
        case 'ArrowLeft':
        case 'ArrowUp':
            event.preventDefault();
            this.#navigatePrevious();
            break;
        case 'ArrowRight':
        case 'ArrowDown':
            event.preventDefault();
            this.#navigateNext();
            break;
        case 'Escape':
            event.preventDefault();
            this.#close();
            break;
    }
};
```

### Focus Management

```typescript
#open(): void {
    this.#previousFocus = document.activeElement as HTMLElement;
    this.#dialog?.showModal();
    this.#dialog?.querySelector<HTMLElement>('button')?.focus();
}

#close(): void {
    this.#dialog?.close();
    this.#previousFocus?.focus();
}
```

### Reduced Motion

```typescript
#shouldReduceMotion(): boolean {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

#scrollToIndex(): void {
    const behavior = this.#shouldReduceMotion() ? 'auto' : 'smooth';
    this.#gallery?.scrollTo({ left: scrollLeft, behavior });
}
```

---

## Registration

### Guard Against Re-registration

```typescript
if (!customElements.get('omb-gallery-carousel')) {
    customElements.define('omb-gallery-carousel', OmbGalleryCarousel);
}
```

### Naming Convention

| Pattern | Example |
|---------|---------|
| Tag name | `omb-{block-name}` |
| Class name | `Omb{BlockName}` |

Examples:
- `omb-gallery-carousel` → `OmbGalleryCarousel`
- `omb-faq-accordion` → `OmbFaqAccordion`

---

## Related Skills

- [typescript-standards](../typescript-standards/SKILL.md) - TypeScript conventions
- [html-standards](../html-standards/SKILL.md) - HTML accessibility
- [vitest-testing](../vitest-testing/SKILL.md) - Testing Web Components
- [native-block-development](../native-block-development/SKILL.md) - Block structure
- [block-scaffolds](../block-scaffolds/SKILL.md) - Web Component template

---

## References

- [MDN Web Components](https://developer.mozilla.org/en-US/docs/Web/Web_Components)
- [Custom Elements Spec](https://html.spec.whatwg.org/multipage/custom-elements.html)
- [Web Components Best Practices](https://web.dev/custom-elements-best-practices/)
