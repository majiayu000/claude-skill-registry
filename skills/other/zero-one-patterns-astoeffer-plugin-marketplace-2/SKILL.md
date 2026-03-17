---
name: zero-one-theme-patterns
description: UIkit patterns and Zero One theme customization for Kirby CMS. Use when styling components with UIkit, customizing the Zero One theme, or building responsive layouts.
---

# Zero One Theme Patterns

UIkit 3 patterns and Zero One theme customizations for Cloodle's Kirby CMS frontend.

## When to Use This Skill

- Building UI components with UIkit
- Customizing Zero One theme variables
- Creating responsive layouts
- Styling cards, buttons, and forms

## Quick Reference

See [reference.md](reference.md) for complete patterns.

## UIkit Essentials

### Layout Grid
```html
<div class="uk-container">
    <div class="uk-grid" uk-grid>
        <div class="uk-width-1-2@m">Content</div>
    </div>
</div>
```

### Cards
```html
<div class="uk-card uk-card-default uk-card-body">
    <h3 class="uk-card-title">Title</h3>
    <p>Content</p>
</div>
```

## Zero One Variables

```scss
$global-primary-background: #6e66cc;
$global-border-radius: 12px;
$base-body-font-family: "Outfit", sans-serif;
```

## Template Pattern

```php
<?php snippet('header') ?>
<main class="uk-section">
    <div class="uk-container">
        <?= $page->text()->toBlocks() ?>
    </div>
</main>
<?php snippet('footer') ?>
```
