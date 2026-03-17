---
name: lit-component
description: Guide for developing Lit web components in the Common UI v2 system (@commontools/ui/v2). Use when creating or modifying ct- prefixed components, implementing theme integration, working with Cell abstractions, or building reactive UI components that integrate with the Common Tools runtime.
---

# Lit Component Development for Common UI

This skill provides guidance for developing Lit web components within the Common UI v2 component library (`packages/ui/src/v2`).

## When to Use This Skill

Use this skill when:
- Creating new `ct-` prefixed components in the UI package
- Modifying existing Common UI v2 components
- Implementing theme-aware components
- Integrating components with Cell abstractions from the runtime
- Building reactive components for pattern/recipe UIs
- Debugging component lifecycle or reactivity issues

## Core Philosophy

Common UI is inspired by SwiftUI and emphasizes:

1. **Default Configuration Works**: Components should work together with minimal configuration
2. **Composition Over Control**: Emphasize composing components rather than granular styling
3. **Adaptive to User Preferences**: Respect system preferences and theme settings (theme is ambient context, not explicit props)
4. **Reactive Binding Model**: Integration with FRP-style Cell abstractions from the runtime
5. **Progressive Enhancement**: Components work with plain values but enhance with Cells for reactivity
6. **Separation of Concerns**: Presentation components, theme-aware inputs, Cell-aware state, runtime-integrated operations

## Quick Start Pattern

### 1. Choose Component Category

Identify which category the component falls into:

- **Layout**: Arranges other components (vstack, hstack, screen)
- **Visual**: Displays styled content (separator, skeleton, label)
- **Input**: Captures user interaction (button, input, checkbox)
- **Complex/Integrated**: Deep runtime integration with Cells (render, code-editor, outliner)

**Complexity spectrum:** Components range from pure presentation (no runtime) to deeply integrated (Cell operations, pattern execution, backlink resolution). Choose the simplest pattern that meets requirements.

See `references/component-patterns.md` for detailed patterns for each category and `references/advanced-patterns.md` for complex integration patterns.

### 2. Create Component Files

Create the component directory structure:

```
packages/ui/src/v2/components/ct-component-name/
├── ct-component-name.ts    # Component implementation
├── index.ts                # Export and registration
└── styles.ts               # Optional: for complex components
```

### 3. Implement Component

Basic template:

```typescript
import { css, html } from "lit";
import { BaseElement } from "../../core/base-element.ts";

export class CTComponentName extends BaseElement {
  static override styles = [
    BaseElement.baseStyles,
    css`
      :host {
        display: block;
        box-sizing: border-box;
      }

      *,
      *::before,
      *::after {
        box-sizing: inherit;
      }
    `,
  ];

  static override properties = {
    // Define reactive properties
  };

  constructor() {
    super();
    // Set defaults
  }

  override render() {
    return html`<!-- component template -->`;
  }
}

globalThis.customElements.define("ct-component-name", CTComponentName);
```

### 4. Create Index File

```typescript
import { CTComponentName } from "./ct-component-name.ts";

if (!customElements.get("ct-component-name")) {
  customElements.define("ct-component-name", CTComponentName);
}

export { CTComponentName };
export type { /* exported types */ };
```

## Theme Integration

For components that need to consume theme (input and complex components):

```typescript
import { consume } from "@lit/context";
import { property } from "lit/decorators.js";
import {
  applyThemeToElement,
  type CTTheme,
  defaultTheme,
  themeContext,
} from "../theme-context.ts";

export class MyComponent extends BaseElement {
  @consume({ context: themeContext, subscribe: true })
  @property({ attribute: false })
  declare theme?: CTTheme;

  override firstUpdated(changed: Map<string | number | symbol, unknown>) {
    super.firstUpdated(changed);
    this._updateThemeProperties();
  }

  override updated(changed: Map<string | number | symbol, unknown>) {
    super.updated(changed);
    if (changed.has("theme")) {
      this._updateThemeProperties();
    }
  }

  private _updateThemeProperties() {
    const currentTheme = this.theme || defaultTheme;
    applyThemeToElement(this, currentTheme);
  }
}
```

Then use theme CSS variables with fallbacks:

```css
.button {
  background-color: var(
    --ct-theme-color-primary,
    var(--ct-color-primary, #3b82f6)
  );
  border-radius: var(
    --ct-theme-border-radius,
    var(--ct-border-radius-md, 0.375rem)
  );
  font-family: var(--ct-theme-font-family, inherit);
}
```

**Complete theme reference:** See `references/theme-system.md` for all available CSS variables and helper functions.

## Cell Integration

For components that work with reactive runtime data:

```typescript
import { property } from "lit/decorators.js";
import type { Cell } from "@commontools/runner";
import { isCell } from "@commontools/runner";

export class MyComponent extends BaseElement {
  @property({ attribute: false })
  declare cell: Cell<MyDataType>;

  private _unsubscribe: (() => void) | null = null;

  override updated(changedProperties: Map<string, any>) {
    super.updated(changedProperties);

    if (changedProperties.has("cell")) {
      // Clean up previous subscription
      if (this._unsubscribe) {
        this._unsubscribe();
        this._unsubscribe = null;
      }

      // Subscribe to new Cell
      if (this.cell && isCell(this.cell)) {
        this._unsubscribe = this.cell.sink(() => {
          this.requestUpdate();
        });
      }
    }
  }

  override disconnectedCallback() {
    super.disconnectedCallback();
    if (this._unsubscribe) {
      this._unsubscribe();
      this._unsubscribe = null;
    }
  }

  override render() {
    if (!this.cell) return html``;

    const value = this.cell.get();
    return html`<div>${value}</div>`;
  }
}
```

**Complete Cell patterns:** See `references/cell-integration.md` for:
- Subscription management
- Nested property access with `.key()`
- Array cell manipulation
- Transaction-based mutations
- Finding cells by equality

## Reactive Controllers

For reusable component behaviors, use reactive controllers. Example: `InputTimingController` for debouncing/throttling:

```typescript
import { InputTimingController } from "../../core/input-timing-controller.ts";

export class CTInput extends BaseElement {
  @property()
  timingStrategy: "immediate" | "debounce" | "throttle" | "blur" = "debounce";

  @property()
  timingDelay: number = 500;

  private inputTiming = new InputTimingController(this, {
    strategy: this.timingStrategy,
    delay: this.timingDelay,
  });

  private handleInput(event: Event) {
    const value = (event.target as HTMLInputElement).value;

    this.inputTiming.schedule(() => {
      this.emit("ct-change", { value });
    });
  }
}
```

## Common Patterns

### Event Emission

Use the `emit()` helper from `BaseElement`:

```typescript
private handleChange(newValue: string) {
  this.emit("ct-change", { value: newValue });
}
```

Events are automatically `bubbles: true` and `composed: true`.

### Dynamic Classes

Use `classMap` for conditional classes:

```typescript
import { classMap } from "lit/directives/class-map.js";

const classes = {
  button: true,
  [this.variant]: true,
  disabled: this.disabled,
};

return html`<button class="${classMap(classes)}">...</button>`;
```

### List Rendering

Use `repeat` directive with stable keys:

```typescript
import { repeat } from "lit/directives/repeat.js";

return html`
  ${repeat(
    items,
    (item) => item.id,  // stable key
    (item) => html`<div>${item.title}</div>`
  )}
`;
```

## Testing

Colocate tests with components:

```typescript
// ct-button.test.ts
import { describe, it } from "@std/testing/bdd";
import { expect } from "@std/expect";
import { CTButton } from "./ct-button.ts";

describe("CTButton", () => {
  it("should be defined", () => {
    expect(CTButton).toBeDefined();
  });

  it("should have default properties", () => {
    const element = new CTButton();
    expect(element.variant).toBe("primary");
  });
});
```

Run with: `deno task test` (includes required flags)

## Package Structure

Components are exported from `@commontools/ui/v2`:

```typescript
// packages/ui/src/v2/index.ts
export { CTButton } from "./components/ct-button/index.ts";
export type { ButtonVariant } from "./components/ct-button/index.ts";
```

## Reference Documentation

Load these references as needed for detailed guidance:

- **`references/component-patterns.md`** - Detailed patterns for each component category, file structure, type safety, styling conventions, event handling, and lifecycle methods
- **`references/theme-system.md`** - Theme philosophy, `ct-theme` provider, CTTheme interface, CSS variables, and theming patterns
- **`references/cell-integration.md`** - Comprehensive Cell integration patterns including subscriptions, mutations, array handling, and common pitfalls
- **`references/advanced-patterns.md`** - Advanced architectural patterns revealed by complex components: context provision, third-party integration, reactive controllers, path-based operations, diff-based rendering, and progressive enhancement

## Key Conventions

1. **Always extend `BaseElement`** - Provides `emit()` helper and base CSS variables
2. **Include box-sizing reset** - Ensures consistent layout behavior
3. **Use `attribute: false`** for objects/arrays/Cells - Prevents serialization errors
4. **Prefix custom events with `ct-`** - Namespace convention
5. **Export types separately** - Use `export type { ... }`
6. **Clean up subscriptions** - Always unsubscribe in `disconnectedCallback()`
7. **Use transactions for Cell mutations** - Never mutate cells directly
8. **Provide CSS variable fallbacks** - Components should work without theme context
9. **Document with JSDoc** - Include `@element`, `@attr`, `@fires`, `@example`
10. **Run tests with `deno task test`** - Not plain `deno test`

## Common Pitfalls to Avoid

- ❌ Forgetting to clean up Cell subscriptions (causes memory leaks)
- ❌ Mutating Cells without transactions (breaks reactivity)
- ❌ Using array index as key in `repeat()` (breaks reactivity)
- ❌ Missing box-sizing reset (causes layout issues)
- ❌ Not providing CSS variable fallbacks (breaks without theme)
- ❌ Using `attribute: true` for objects/arrays (serialization errors)
- ❌ Skipping `super` calls in lifecycle methods (breaks base functionality)

## Architecture Patterns to Study

Study these components to understand architectural patterns:

**Basic patterns:**
- **Simple visual:** `ct-separator` - Minimal component, CSS parts, ARIA
- **Layout:** `ct-vstack` - Flexbox abstraction, utility classes with `classMap`
- **Themed input:** `ct-button` - Theme consumption, event emission, variants

**Advanced patterns:**
- **Context provider:** `ct-theme` - Ambient configuration with `@provide`, `display: contents`, reactive Cell subscriptions
- **Runtime rendering:** `ct-render` - Recipe loading, UI extraction, lifecycle management
- **Third-party integration:** `ct-code-editor` - CodeMirror lifecycle, Compartments, bidirectional sync, CellController
- **Tree operations:** `ct-outliner` - Path-based operations, diff-based rendering, keyboard commands, MentionController

Each component reveals deeper patterns - study them not just for API but for architectural principles.
