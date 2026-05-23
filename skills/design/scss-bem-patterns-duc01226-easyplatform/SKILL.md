---
name: scss-bem-patterns
description: Use when editing SCSS or CSS files (.scss, .css) or HTML templates with styling. Provides BEM naming convention, SCSS structure, theming patterns, and responsive design rules for EasyPlatform frontend styling.
---

# SCSS & BEM Styling Patterns

When implementing styles in EasyPlatform, follow these patterns exactly.

## Full Pattern Reference

See the complete styling guide: [scss-styling-guide.md](docs/claude/scss-styling-guide.md)

## BEM Naming Convention (MANDATORY)

Every UI element MUST have a BEM class, even without special styling.

### Structure

- **Block:** `user-list` - Standalone component
- **Element:** `user-list__header` - Part of a block
- **Modifier:** `--primary --small` - Variation (separate class)

### Example

```html
<div class="user-list">
    <div class="user-list__header">
        <h1 class="user-list__title">Users</h1>
    </div>
    <div class="user-list__content">
        @for (user of vm.users; track user.id) {
            <div class="user-list__item">
                <span class="user-list__item-name">{{ user.name }}</span>
                <button class="user-list__btn --primary --small">Edit</button>
            </div>
        }
    </div>
</div>
```

### SCSS Structure

```scss
.user-list {
    // Block styles
    display: flex;
    flex-direction: column;

    &__header {
        // Element styles
        padding: var(--spacing-md);
    }

    &__title {
        font-size: var(--font-size-lg);
    }

    &__item {
        display: flex;
        align-items: center;

        &-name {
            flex: 1;
        }
    }

    &__btn {
        // Base button styles

        &.--primary {
            background: var(--color-primary);
        }

        &.--small {
            padding: var(--spacing-xs);
        }
    }
}
```

## Critical Rules

1. **Every element needs a BEM class** - No anonymous divs/spans
2. **Modifiers are separate classes** - Use `class="btn --primary"` not `class="btn--primary"`
3. **Use CSS variables** - `var(--spacing-md)` not hardcoded values
4. **Component scoping** - Each component has its own block name
5. **No global styles** - All styles scoped to BEM blocks

## Anti-Patterns

```scss
// ❌ Anonymous elements
<div><span>Text</span></div>

// ✅ BEM classes on everything
<div class="card"><span class="card__text">Text</span></div>

// ❌ Modifier attached to base class
.btn--primary { }

// ✅ Modifier as separate class
.btn.--primary { }

// ❌ Hardcoded values
padding: 16px;

// ✅ CSS variables
padding: var(--spacing-md);

// ❌ Deep nesting
.header .nav .menu .item .link { }

// ✅ BEM flat structure
.header__nav-link { }
```

## Theming

```scss
// Use design tokens from design system
@use '@libs/share-styles/themes' as themes;

.component {
    color: var(--text-primary);
    background: var(--bg-surface);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-sm);
}
```

## Responsive Design

```scss
.component {
    padding: var(--spacing-sm);

    @media (min-width: 768px) {
        padding: var(--spacing-md);
    }

    @media (min-width: 1024px) {
        padding: var(--spacing-lg);
    }
}
```

## Detailed Instructions

For task-specific guidance, also reference:

- [scss-styling.instructions.md](instructions/scss-styling.instructions.md) - Complete SCSS guide
- [FrontendDesignSystem.md](docs/design-system/FrontendDesignSystem.md) - Design tokens
