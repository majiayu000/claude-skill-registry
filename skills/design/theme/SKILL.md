---
name: theme
description: Generates SCSS theme files in src/theme/ including vars.scss, shadow.scss, and index.scss with sample variables and mixins for styling.
---

# Theme Skill

## Purpose
- Generate SCSS theme files with variables and mixins.
- Add few sample SCSS variables as example in variables file.
- Add a few sample mixins as example in mixins file.
- Create an index.scss file that will forward the variables file. For example:
  ```scss
  @forward './vars';
  ```

## Output
Create the files:
- `src/theme/vars.scss`
- `src/theme/shadow.scss`
- `src/theme/index.scss`

## ⚠️ CRITICAL: Use Modern Sass Module System

**MUST follow current Sass best practices as documented in official Sass documentation**

### Example of Implementation Pattern
**In `src/theme/index.scss`** - Use `@forward` to re-export variables:
```scss
@forward './vars';
@forward './shadow';
```

**In components (App.vue, etc.)** - Use `@use` to import theme:
```scss
<style lang="scss">
@use '@/theme/' as *;

.my-component {
  color: $primary-color; // Variables from theme are now available
}
</style>
```

### Verification
After generating theme files:
- Run build and check console output for any deprecation warnings
- If deprecation warnings appear, consult official Sass documentation for current patterns
- Ensure the implementation follows the `@forward`/`@use` pattern shown in examples

## Notes
- `vars.scss` provides comprehensive design system variables
- `shadow.scss` provides Material Design-inspired shadow mixins (0dp to 24dp)
- Forward/use pattern enables clean imports in components
- Use with `@use '@/theme/' as *;` in components
- Shadow mixins reference `$global-black` from vars.scss
- The `index.scss` file acts as a barrel export using `@forward`
