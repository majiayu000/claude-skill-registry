---
name: wordpress-sage-theme
description: WordPress theme development using Sage (roots/sage) framework. Use when creating, modifying, or debugging WordPress themes with Sage, including: (1) Creating new Sage themes from scratch, (2) Setting up Blade templates and components, (3) Configuring build tools (Vite, Bud), (4) Working with WordPress theme templates and hierarchy, (5) Implementing ACF fields integration, (6) Theme customization and asset management
---

# WordPress Sage Theme Development

## Overview

Sage is a WordPress theme framework by Roots that provides modern development practices including Blade templates, dependency management with Composer, and build tools with Vite/Bud.

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
