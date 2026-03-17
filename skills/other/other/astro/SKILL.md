---
name: astro
description: >
  Astro v5 patterns, component structure, and best practices. 
  Trigger: When creating/modifying Astro files (.astro), configuring Astro, or working with Astro-specific features.
license: Apache-2.0
metadata:
  author: prowler-cloud
  version: "1.0"
  scope: [root]
  auto_invoke:
    - "Creating/modifying Astro files (.astro)"
    - "Configuring Astro"
    - "Working with file-based routing"
    - "Implementing Astro Islands"
---

## When to Use

- Creating or modifying `.astro` files (pages, layouts, components)
- Setting up Astro configuration
- Working with Astro's file-based routing
- Implementing Astro Islands (client-side components)
- Integrating frameworks in Astro (React, Vue, Svelte, etc.)

## Critical Patterns

### File Structure

```
src/
├── layouts/          # Base layouts wrapping pages
│   └── BaseLayout.astro
├── pages/            # File-based routing (index.astro, about.astro)
├── components/       # Reusable components
│   ├── ui/           # Generic UI components (Button, Card)
│   ├── layout/       # Layout components (Header, Footer)
│   ├── sections/     # Page sections (Hero, Services)
│   └── islands/      # Interactive client-side components
└── styles/           # Global CSS
```

### Component Anatomy (.astro)

```astro
---
// 1. Frontmatter script (runs at build time)
import { SomeComponent } from './components/SomeComponent.astro';
import type { CollectionEntry } from 'astro:content';

// Props interface
interface Props {
  title: string;
  items?: Array<string>;
}

const { title, items = [] } = Astro.props;
const timestamp = new Date().toISOString();
---

<!-- 2. HTML/JSX template -->
<html>
  <head>
    <title>{title}</title>
  </head>
  <body>
    <SomeComponent />
    <p>Generated at: {timestamp}</p>
    <ul>
      {items.map(item => <li>{item}</li>)}
    </ul>
  </body>
</html>

<!-- 3. Client-side scripts (scoped) -->
<script>
  // Runs in browser when component mounts
  console.log('Component loaded');
</script>
```

### Astro Islands (Client-Side Interactivity)

```astro
---
// islands/InteractiveComponent.astro
---

<div id="counter">
  <button data-action="decrement">-</button>
  <span>0</span>
  <button data-action="increment">+</button>
</div>

<script define:vars={{ initialValue: 0 }}>
  let count = initialValue;
  
  document.getElementById('counter').addEventListener('click', (e) => {
    const btn = e.target.closest('button');
    if (!btn) return;
    
    count += btn.dataset.action === 'increment' ? 1 : -1;
    btn.parentElement.querySelector('span').textContent = count;
  });
</script>
```

### Pass Props to Slots

```astro
---
// components/Card.astro
interface Props {
  title: string;
  variant?: 'default' | 'primary';
}

const { title, variant = 'default' } = Astro.props;
---

<div class={`card card-${variant}`}>
  <h2 class="card-title">{title}</h2>
  <slot />
  <slot name="footer" />
</div>

<style>
  .card {
    border: 1px solid #ccc;
    padding: 1rem;
    border-radius: 0.5rem;
  }
  .card-primary {
    border-color: #3b82f6;
    background: #eff6ff;
  }
</style>

<!-- Usage -->
---
import Card from '../components/Card.astro';
---

<Card title="Welcome" variant="primary">
  <p>This is the main content.</p>
  <p slot="footer">Footer content</p>
</Card>
```

### Static vs Dynamic Imports

```astro
---
// BAD: Always imports entire library
import { HeavyComponent } from './components/HeavyComponent.astro';

// GOOD: Dynamic import with client:* directives
<HeavyComponent client:load />

// Directives: client:load, client:idle, client:visible, client:media
---
```

### Content Collections

```astro
---
// src/content/config.ts
import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  schema: z.object({
    title: z.string(),
    date: z.date(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };
---

// Usage in page
---
import { getCollection } from 'astro:content';

const posts = await getCollection('blog');
---

<ul>
  {posts.map(post => (
    <li>
      <a href={`/blog/${post.slug}`}>
        {post.data.title}
      </a>
    </li>
  ))}
</ul>
```

### TypeScript in Astro

```astro
---
// Always type props
interface Props {
  title: string;
  count?: number;
}

const { count = 0 } = Astro.props;

// Use Astro.slots API
const hasDefaultSlot = await Astro.slots.has('default');

// Access runtime data
const url = new URL(Astro.url.pathname, Astro.site);
---
```

### Styling Conventions

```astro
---
// Use Tailwind classes for layout and spacing
// Use scoped <style> for component-specific styles
---

<div class="container mx-auto p-4">
  <h1 class="text-2xl font-bold">Title</h1>
</div>

<style>
  h1 {
    /* Component-specific styles only */
  }
</style>
```

## Code Examples

### Page Component

```astro
---
// src/pages/about.astro
import BaseLayout from '../layouts/BaseLayout.astro';

const title = 'About Us';
---

<BaseLayout title={title}>
  <main class="max-w-4xl mx-auto py-12">
    <h1 class="text-4xl font-bold mb-6">{title}</h1>
    <p class="text-lg">Learn about our mission...</p>
  </main>
</BaseLayout>
```

### Layout Component

```astro
---
// src/layouts/BaseLayout.astro
interface Props {
  title: string;
  description?: string;
}

const { title, description = 'Default description' } = Astro.props;
const canonicalURL = new URL(Astro.url.pathname, Astro.site);
---

<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width" />
    <link rel="canonical" href={canonicalURL} />
    <meta name="description" content={description} />
    <title>{title}</title>
  </head>
  <body>
    <slot />
  </body>
</html>
```

### Island Component with State

```astro
---
// src/components/islands/ContactForm.astro
---

<form id="contact-form">
  <input type="text" name="name" placeholder="Name" required />
  <input type="email" name="email" placeholder="Email" required />
  <textarea name="message" placeholder="Message" required></textarea>
  <button type="submit">Send</button>
</form>

<script>
  const form = document.getElementById('contact-form');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    // Handle submission
  });
</script>
```

## Commands

```bash
# Development
pnpm run dev              # Start dev server

# Build
pnpm run build            # Build for production
pnpm run preview          # Preview production build

# Astro CLI
pnpm run astro check      # Type checking
pnpm run astro add        # Add integrations

# Create new page/component
# Follow file structure conventions
```

## Resources

- **Templates**: See [assets/](assets/) for Astro component templates
- **Astro Docs**: https://docs.astro.build
- **Content Collections**: https://docs.astro.build/en/guides/content-collections/
- **Islands Architecture**: https://docs.astro.build/en/concepts/islands/
