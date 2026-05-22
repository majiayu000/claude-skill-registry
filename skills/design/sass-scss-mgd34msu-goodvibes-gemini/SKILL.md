---
name: sass-scss
description: Implements CSS preprocessing with Sass/SCSS using modules, mixins, functions, and nesting. Use when needing CSS preprocessing, design system variables, reusable mixins, or organizing large stylesheets.
---

# Sass/SCSS

CSS preprocessor with variables, nesting, mixins, and modules.

## Quick Start

**Install:**
```bash
npm install -D sass
```

**Create styles:**
```scss
// styles/variables.scss
$primary: #3b82f6;
$secondary: #6b7280;
$spacing: 16px;
$border-radius: 8px;

// styles/button.scss
@use 'variables' as *;

.button {
  padding: $spacing;
  border-radius: $border-radius;
  background: $primary;
  color: white;
  border: none;
  cursor: pointer;

  &:hover {
    background: darken($primary, 10%);
  }
}
```

## Module System

### @use - Import Modules

```scss
// _colors.scss
$primary: #3b82f6;
$secondary: #6b7280;

// styles.scss
@use 'colors';

.button {
  background: colors.$primary;
}

// Custom namespace
@use 'colors' as c;
.button {
  background: c.$primary;
}

// No namespace
@use 'colors' as *;
.button {
  background: $primary;
}
```

### @forward - Re-export Modules

```scss
// _tokens/_colors.scss
$primary: #3b82f6;
$secondary: #6b7280;

// _tokens/_spacing.scss
$sm: 8px;
$md: 16px;
$lg: 24px;

// _tokens/_index.scss
@forward 'colors';
@forward 'spacing';

// styles.scss
@use 'tokens';

.card {
  padding: tokens.$md;
  background: tokens.$primary;
}
```

### Configure Modules

```scss
// _library.scss
$border-radius: 4px !default;
$primary-color: blue !default;

@mixin button {
  border-radius: $border-radius;
  background: $primary-color;
}

// main.scss
@use 'library' with (
  $border-radius: 8px,
  $primary-color: #3b82f6
);

.button {
  @include library.button;
}
```

## Variables

```scss
// Basic variables
$font-stack: system-ui, -apple-system, sans-serif;
$primary: #3b82f6;
$spacing-unit: 8px;

// Maps
$colors: (
  'primary': #3b82f6,
  'secondary': #6b7280,
  'success': #10b981,
  'error': #ef4444,
);

// Access map values
.button {
  background: map-get($colors, 'primary');
}

// Default values
$border-radius: 8px !default;
```

## Nesting

```scss
.card {
  padding: 16px;
  background: white;

  // Nested selectors
  .title {
    font-size: 24px;
    margin-bottom: 8px;
  }

  .body {
    color: #6b7280;
  }

  // Parent selector (&)
  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  &.highlighted {
    border: 2px solid #3b82f6;
  }

  // Modifier pattern
  &--large {
    padding: 24px;
  }

  // Media queries
  @media (min-width: 768px) {
    padding: 24px;
  }
}
```

## Mixins

### Basic Mixins

```scss
@mixin flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

@mixin truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.container {
  @include flex-center;
}

.title {
  @include truncate;
}
```

### Mixins with Arguments

```scss
@mixin button($bg, $color: white) {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  background: $bg;
  color: $color;
  cursor: pointer;

  &:hover {
    background: darken($bg, 10%);
  }
}

.btn-primary {
  @include button(#3b82f6);
}

.btn-secondary {
  @include button(#e5e7eb, #1f2937);
}
```

### Content Blocks

```scss
@mixin media($breakpoint) {
  @if $breakpoint == 'sm' {
    @media (min-width: 640px) { @content; }
  } @else if $breakpoint == 'md' {
    @media (min-width: 768px) { @content; }
  } @else if $breakpoint == 'lg' {
    @media (min-width: 1024px) { @content; }
  }
}

.container {
  padding: 16px;

  @include media('md') {
    padding: 24px;
  }

  @include media('lg') {
    padding: 32px;
    max-width: 1200px;
  }
}
```

## Functions

### Built-in Functions

```scss
// Color functions
$base: #3b82f6;

.element {
  background: $base;
  border-color: darken($base, 20%);
  color: lighten($base, 40%);

  &:hover {
    background: adjust-hue($base, 15deg);
  }
}

// Math functions
.grid {
  width: percentage(1/3);  // 33.33333%
  margin: round(16.5px);   // 17px
  padding: min(16px, 2vw);
}

// String functions
$icon: 'arrow';
.icon-#{$icon} {
  content: quote($icon);
}

// List functions
$sizes: 8px, 16px, 24px, 32px;
.element {
  padding: nth($sizes, 2);  // 16px
  margin: list.append($sizes, 48px);
}
```

### Custom Functions

```scss
@function spacing($multiplier) {
  $base: 8px;
  @return $base * $multiplier;
}

@function rem($pixels) {
  @return #{$pixels / 16}rem;
}

.element {
  padding: spacing(2);     // 16px
  font-size: rem(18);      // 1.125rem
  margin: spacing(3);      // 24px
}
```

## Control Flow

### Conditionals

```scss
@mixin theme-colors($theme) {
  @if $theme == 'light' {
    background: white;
    color: #1f2937;
  } @else if $theme == 'dark' {
    background: #1f2937;
    color: white;
  } @else {
    @error "Unknown theme: #{$theme}";
  }
}
```

### Loops

```scss
// @for loop
@for $i from 1 through 5 {
  .mt-#{$i} {
    margin-top: $i * 8px;
  }
}

// @each loop
$colors: (
  'primary': #3b82f6,
  'secondary': #6b7280,
  'success': #10b981,
);

@each $name, $color in $colors {
  .bg-#{$name} {
    background: $color;
  }
  .text-#{$name} {
    color: $color;
  }
}

// @while loop
$i: 1;
@while $i <= 3 {
  .col-#{$i} {
    width: percentage($i / 12);
  }
  $i: $i + 1;
}
```

## Extend/Inheritance

```scss
%button-base {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
}

.btn-primary {
  @extend %button-base;
  background: #3b82f6;
  color: white;
}

.btn-secondary {
  @extend %button-base;
  background: #e5e7eb;
  color: #1f2937;
}
```

## File Organization

```
styles/
  _tokens/
    _colors.scss
    _spacing.scss
    _typography.scss
    _index.scss          # @forward all tokens
  _mixins/
    _breakpoints.scss
    _utilities.scss
    _index.scss
  components/
    _button.scss
    _card.scss
    _index.scss
  main.scss              # Entry point
```

```scss
// main.scss
@use 'tokens';
@use 'mixins';
@use 'components/button';
@use 'components/card';
```

## Built-in Modules

```scss
@use 'sass:math';
@use 'sass:string';
@use 'sass:list';
@use 'sass:map';
@use 'sass:color';

.element {
  width: math.div(100%, 3);
  padding: math.clamp(16px, 5vw, 32px);
}

$colors: map.merge($base-colors, $override-colors);
$updated: map.set($colors, 'primary', blue);
```

## Best Practices

1. **Use @use over @import** - @import is deprecated
2. **Prefix partials with _** - Indicates files for import only
3. **Keep nesting shallow** - Max 3-4 levels deep
4. **Use variables for design tokens** - Colors, spacing, typography
5. **Prefer mixins for complex patterns** - Functions for calculations

## Common Patterns

### Design Tokens

```scss
// _tokens.scss
$colors: (
  'primary-50': #eff6ff,
  'primary-500': #3b82f6,
  'primary-600': #2563eb,
);

$spacing: (
  'xs': 4px,
  'sm': 8px,
  'md': 16px,
  'lg': 24px,
  'xl': 32px,
);

@function color($name) {
  @return map-get($colors, $name);
}

@function space($size) {
  @return map-get($spacing, $size);
}
```

### Responsive Mixins

```scss
$breakpoints: (
  'sm': 640px,
  'md': 768px,
  'lg': 1024px,
  'xl': 1280px,
);

@mixin breakpoint($name) {
  $value: map-get($breakpoints, $name);
  @media (min-width: $value) {
    @content;
  }
}
```

## Reference Files

- [references/modules.md](references/modules.md) - Module system
- [references/mixins.md](references/mixins.md) - Common mixins
