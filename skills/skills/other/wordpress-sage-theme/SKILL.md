---
name: wordpress-sage-theme
description: 'Provides WordPress theme development patterns using Sage (roots/sage) framework. Use when creating, modifying, or debugging WordPress themes with Sage, including (1): creating new Sage themes from scratch, (2): setting up Blade templates and components, (3): configuring build tools (Vite, Bud), (4): working with WordPress theme templates and hierarchy, (5): implementing ACF fields integration, (6): theme customization and asset management.'
allowed-tools: Read, Write, Bash, Glob, Grep
---

# WordPress Sage Theme Development

## Overview

Sage is a WordPress theme framework by Roots that provides modern development practices including Blade templates, dependency management with Composer, and build tools with Vite/Bud.

## When to Use

Use this skill when working with WordPress theme development using the Sage (Roots) framework. Specific scenarios include:

- Creating new Sage themes from scratch or from composer templates
- Setting up Blade templates, layouts, and reusable components
- Configuring build tools (Bud/Vite) for asset compilation
- Working with WordPress template hierarchy in Blade format
- Integrating Advanced Custom Fields (ACF) with Blade templates
- Debugging theme rendering or asset loading issues
- Optimizing theme performance and following best practices

## Instructions

1. **Theme Setup**: Use `composer create-project roots/sage` to create new themes
2. **Blade Templates**: Place templates in `resources/views/` following WordPress hierarchy
3. **Components**: Create reusable components in `resources/views/components/`
4. **Build**: Run `npm install` and `npm run dev` for development, `npm run build` for production
5. **ACF Integration**: Use `get_field()` and `have_rows()` directives in Blade templates
6. **Asset Management**: Configure Bud entry points in `bud.config.js`
7. **Output Escape**: Always escape output with `{{ }}` or WordPress escape functions

## Examples

**Create a new Sage theme:**
```bash
composer create-project roots/sage my-theme
cd my-theme
npm install && composer install
npm run dev
```

**Blade page template:**
```blade
@extends('layouts.app')

@section('content')
  <main class="content">
    <h1>{{ the_title() }}</h1>
    <div class="entry-content">
      {{ the_content() }}
    </div>
  </main>
@endsection
```

**ACF flexible content in Blade:**
```blade
@if (have_rows('flexible_content'))
  @while (have_rows('flexible_content'))
    @php the_row() @endphp
    @switch(get_row_layout())
      @case('hero_section')
        @include('components.hero')
        @break
    @endswitch
  @endwhile
@endif
```

## Quick Start

### Creating a New Sage Theme

**Prerequisites**: PHP 8.0+, Node.js 18+, Composer

```bash
# Create new Sage theme
wp scaffold theme-theme my-theme --theme_name="My Theme" --author="Your Name" --activate

# Or install Sage directly via Composer
composer create-project roots/sage my-theme
cd my-theme

# Install dependencies
npm install
composer install

# Build for development
npm run dev

# Build for production
npm run build
```

### Directory Structure

```
resources/
├── views/           # Blade templates
│   ├── layouts/     # Base layouts (app.blade.php)
│   ├── components/  # Reusable components
│   └── partials/    # Template partials
├── styles/          # CSS/SASS files
│   └── main.scss    # Main stylesheet
└── scripts/         # JavaScript files
    └── main.js      # Main JavaScript
```

## Blade Templates

### Layouts

**Base Layout** (`resources/views/layouts/app.blade.php`):

```blade
<!DOCTYPE html>
<html {{ site_html_language_attributes() }}>
  <head>
    {{ wp_head() }}
  </head>
  <body {{ body_class() }}>
    @yield('content')
    {{ wp_footer() }}
  </body>
</html>
```

### Template Hierarchy Mapping

| WordPress Template | Sage Blade File |
|-------------------|-----------------|
| front-page.php | `views/front-page.blade.php` |
| single.php | `views/single.blade.php` |
| page.php | `views/page.blade.php` |
| archive.php | `views/archive.blade.php` |
| index.php | `views/index.blade.php` |

**Example Page Template** (`resources/views/page.blade.php`):

```blade
@extends('layouts.app')

@section('content')
  <main class="content">
    <h1>{{ the_title() }}</h1>
    <div class="entry-content">
      {{ the_content() }}
    </div>
  </main>
@endsection
```

### Components

**Reusable Button Component** (`resources/views/components/button.blade.php`):

```blade
@props(['url' => '#', 'text' => 'Click', 'variant' => 'primary'])

<a href="{{ $url }}" class="btn btn-{{ $variant }}">
  {{ $text }}
</a>
```

**Usage**:

```blade
<x-button url="/contact" text="Contact Us" variant="secondary" />
```

## ACF Integration

### Displaying ACF Fields

**Basic Field**:

```blade
@while(the_post())
  <h1>{{ get_field('hero_title') ?? the_title() }}</h1>
  <p>{{ get_field('hero_description') }}</p>
@endwhile
```

**Flexible Content**:

```blade
@if (have_rows('flexible_content'))
  @while (have_rows('flexible_content'))
    @php the_row() @endphp

    @switch(get_row_layout())
      @case('hero_section')
        @include('components.hero')
        @break

      @case('features_grid')
        @include('components.features-grid')
        @break
    @endswitch
  @endwhile
@endif
```

**Repeater Field**:

```blade
@if (have_rows('testimonials'))
  <div class="testimonials">
    @while (have_rows('testimonials'))
      @php the_row() @endphp
      <blockquote>
        <p>{{ get_sub_field('testimonial_text') }}</p>
        <cite>{{ get_sub_field('author_name') }}</cite>
      </blockquote>
    @endwhile
  </div>
@endif
```

## Build Configuration (Bud)

### Tailwind CSS Setup

**Install Tailwind**:

```bash
npm install -D tailwindcss
npx tailwindcss init -p
```

**Configure** (`bud.config.js`):

```js
export default async (app) => {
  app
    .entry({
      app: ['@/scripts/main.js', '@styles/main.css'],
      editor: ['@scripts/editor.js', '@styles/editor.css'],
    })
    .assets('images', 'fonts')
    .tailwind()
    .runtime()
};
```

**Tailwind CSS** (`resources/styles/main.css`):

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer components {
  .btn {
    @apply px-4 py-2 rounded font-semibold transition;
  }

  .btn-primary {
    @apply bg-blue-600 text-white hover:bg-blue-700;
  }
}
```

## Advanced Patterns

### Conditional Logic

```blade
@if (is_front_page())
  @include('components.hero')
@elseif (is_singular('post'))
  @include('components.post-meta')
@endif
```

### Custom Queries

```blade
@php
  $args = [
    'post_type' => 'service',
    'posts_per_page' => 6,
  ];
  $query = new WP_Query($args);
@endphp

@if ($query->have_posts())
  @while ($query->have_posts())
    @php $query->the_post() @endphp
    <article>
      <h2>{{ the_title() }}</h2>
    </article>
  @endwhile
  @php wp_reset_postdata() @endphp
@endif
```

### Theme Customization

**functions.php additions**:

```php
// Custom image sizes
add_image_size('hero-lg', 1920, 1080, true);

// Custom post types
add_action('init', function() {
  register_post_type('service', [
    'label' => 'Services',
    'public' => true,
    'has_archive' => true,
    'supports' => ['title', 'editor', 'thumbnail'],
  ]);
});
```

## References

- **Sage Documentation**: See [SAGE.md](references/SAGE.md) for complete framework reference
- **Blade Templates**: See [BLADE.md](references/BLADE.md) for advanced Blade patterns
- **Bud Configuration**: See [BUD.md](references/BUD.md) for build tool configuration
- **ACF Integration**: See [ACF.md](references/ACF.md) for ACF field examples

## Troubleshooting

**Build issues**:
```bash
# Clear cache
npm run clean

# Rebuild
rm -rf node_modules public
npm install
npm run build
```

**Blade not compiling**: Check `public/manifest.json` exists after build

**AC fields not showing**: Verify field names match exactly (case-sensitive)

## Best Practices

### Blade Template Organization

- **Use components for reusable UI elements**: Create blade components in `resources/views/components/` for buttons, cards, and other repeated elements
- **Keep layouts minimal**: Base layouts should only contain structural HTML; delegate styling to components
- **Leverage Blade directives**: Use `@include`, `@each`, and `@component` for better code organization
- **Avoid inline PHP**: Use `@php` blocks sparingly; move complex logic to Composers or service classes

### ACF Field Management

- **Group related fields**: Use ACF field groups to organize fields logically by content type
- **Use field keys for references**: When referencing fields programmatically, use field keys (e.g., `field_12345678`) for reliability
- **Implement fallback values**: Always provide default values for optional fields to prevent empty output
- **Cache expensive queries**: Use WordPress transients for complex ACF queries on high-traffic pages

### Asset Management

- **Use Bud for asset compilation**: Let Bud handle versioning and optimization instead of manual asset management
- **Minimize HTTP requests**: Combine CSS/JS files where appropriate using Bud's entry points
- **Optimize images**: Use WordPress image sizes and lazy loading; consider WebP conversion
- **Cache busting**: Bud automatically handles cache busting via manifest.json

### Code Organization

- **Use Composers for data**: Move data retrieval logic from templates to Sage Composers (`app/View/Composers/`)
- **Separate concerns**: Keep business logic in service classes, presentation in Blade templates
- **Follow WordPress coding standards**: Maintain consistency with WordPress PHP coding standards
- **Use type declarations**: PHP 8.0+ allows typed properties and arguments for better code quality

### Security Considerations

- **Escape all output**: Use `{{ }}` (Blade auto-escapes) or WordPress functions like `esc_html()`, `esc_url()`
- **Validate ACF input**: Sanitize and validate custom field inputs on the backend
- **Nonce verification**: Always verify nonces for form submissions
- **Capability checks**: Use `current_user_can()` before privileged operations

## Constraints and Warnings

### Version Requirements

- **PHP 8.0+ required**: Sage 10 requires PHP 8.0 or higher; earlier versions are not supported
- **Node.js 18+ required**: Build tools require modern Node.js; older versions may cause compilation errors
- **WordPress 6.0+ recommended**: While Sage works with WordPress 5.x, version 6.0+ is recommended for full feature support
- **Composer required**: Dependency management requires Composer; manual installation is not supported

### Build Tool Limitations

- **Hot reload limitations**: Bud's hot reload may not work correctly with some WordPress multisite configurations
- **Production builds required for testing**: Some features work differently in development vs production; always test with `npm run build` before deployment
- **Manifest.json dependency**: Theme relies on `public/manifest.json`; missing this file breaks asset loading

### Common Pitfalls

- **Template hierarchy confusion**: Sage uses Blade files but follows WordPress template hierarchy; ensure file names match WordPress expectations
- **Direct file access**: Do not access Blade files directly via URL; they must be rendered through WordPress
- **Plugin conflicts**: Some caching and security plugins may interfere with Bud's hot reload or asset serving
- **Theme updates**: Updating Sage via Composer may overwrite customizations; use child themes for extensive modifications

### Performance Considerations

- **ACF Repeater performance**: Large repeater fields can impact page load; consider pagination or alternative storage for large datasets
- **Blade compilation overhead**: First load after cache clear compiles all templates; use OPcache in production
- **Asset bundle size**: Monitor compiled asset sizes; large bundles affect page load performance
- **Database queries**: Use Query Monitor plugin to identify and optimize expensive queries in theme templates

### Deployment Constraints

- **Build step required**: Production deployments must run `npm run build`; raw source files cannot be served
- **Environment-specific configuration**: Bud configuration may need adjustment for different deployment environments
- **File permissions**: Ensure `public/` directory is writable during builds; incorrect permissions cause build failures
