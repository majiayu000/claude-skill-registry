---
name: astro-patterns
description: Astro best practices, routing patterns, component architecture, and static
  site generation techniques. Use when building Astro websites, setting up routing,
  designing component architecture, configuri
---

---
name: astro-patterns
description: Astro best practices, routing patterns, component architecture, and static site generation techniques. Use when building Astro websites, setting up routing, designing component architecture, configuring static site generation, optimizing build performance, implementing content strategies, or when user mentions Astro patterns, routing, component design, SSG, static sites, or Astro best practices.
allowed-tools: - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Astro Patterns

Comprehensive best practices, routing patterns, component architecture, and static site generation techniques for building high-performance Astro websites.

## Overview

This skill provides:
- File-based routing patterns and advanced routing configurations
- Component architecture following islands architecture principles
- Layout systems with nested layouts and slot patterns
- Content strategies for blogs, documentation, and marketing sites
- Static site generation optimization techniques
- Build performance tuning and bundle optimization
- SEO and performance best practices

## Setup Scripts

### Core Setup Scripts

1. **scripts/setup-routing.sh** - Initialize routing structure and conventions
2. **scripts/setup-components.sh** - Scaffold component directory structure
3. **scripts/setup-layouts.sh** - Create layout hierarchy
4. **scripts/validate-structure.sh** - Validate Astro project structure
5. **scripts/optimize-build.sh** - Apply build optimization configurations

### Utility Scripts

6. **scripts/generate-route.sh** - Generate new route with layouts
7. **scripts/generate-page.sh** - Create new page with best practices
8. **scripts/analyze-performance.sh** - Analyze build and runtime performance
9. **scripts/generate-sitemap.sh** - Generate sitemap configuration

## Templates

### Routing Templates

1. **templates/routing/basic-page.astro** - Standard page with layouts
2. **templates/routing/dynamic-route.astro** - Dynamic route with getStaticPaths
3. **templates/routing/api-endpoint.ts** - API endpoint handler
4. **templates/routing/middleware.ts** - Route middleware configuration
5. **templates/routing/redirect-config.ts** - Redirect rules
6. **templates/routing/404-page.astro** - Custom 404 error page

### Component Templates

7. **templates/components/base-component.astro** - Basic Astro component
8. **templates/components/island-wrapper.astro** - Framework component wrapper
9. **templates/components/slot-component.astro** - Component with named slots
10. **templates/components/props-component.astro** - Type-safe props pattern
11. **templates/components/async-component.astro** - Component with data fetching
12. **templates/components/component-collection.astro** - Reusable component set

### Layout Templates

13. **templates/layouts/base-layout.astro** - Root layout with SEO
14. **templates/layouts/nested-layout.astro** - Nested layout pattern
15. **templates/layouts/blog-layout.astro** - Blog post layout
16. **templates/layouts/docs-layout.astro** - Documentation layout
17. **templates/layouts/marketing-layout.astro** - Marketing page layout
18. **templates/layouts/layout-with-sidebar.astro** - Layout with navigation sidebar

### Content Templates

19. **templates/content/blog-post.md** - Blog post with frontmatter
20. **templates/content/documentation-page.md** - Docs page structure
21. **templates/content/landing-page.astro** - Landing page pattern
22. **templates/content/case-study.astro** - Case study template

### Build Templates

23. **templates/build/astro.config.ts** - Full Astro configuration
24. **templates/build/tsconfig.json** - TypeScript configuration
25. **templates/build/env.d.ts** - Environment types
26. **templates/build/image-optimization.ts** - Image optimization config

## Examples

1. **examples/basic-routing.md** - File-based routing examples
2. **examples/dynamic-routes.md** - Dynamic route patterns with getStaticPaths
3. **examples/component-architecture.md** - Component organization patterns
4. **examples/layout-hierarchy.md** - Nested layout examples
5. **examples/content-collections-usage.md** - Content collections integration
6. **examples/build-optimization.md** - Build performance techniques
7. **examples/seo-patterns.md** - SEO and metadata best practices
8. **examples/api-routes.md** - API endpoint patterns

## Instructions

### Phase 1: Project Structure Setup

1. **Validate Existing Structure**
   ```bash
   # Check project structure
   bash scripts/validate-structure.sh
   ```

2. **Setup Core Directories**
   ```bash
   # Initialize routing structure
   bash scripts/setup-routing.sh

   # Setup component architecture
   bash scripts/setup-components.sh

   # Create layout hierarchy
   bash scripts/setup-layouts.sh
   ```

3. **Configure Astro**
   - Read: templates/build/astro.config.ts
   - Configure integrations, output mode, build settings
   - Setup path aliases and base URL

### Phase 2: Routing Architecture

1. **File-Based Routing**
   - Read: examples/basic-routing.md
   - Follow directory structure conventions
   - Use index.astro for default routes
   - Name files with kebab-case

2. **Dynamic Routes**
   - Read: examples/dynamic-routes.md
   - Read: templates/routing/dynamic-route.astro
   - Implement getStaticPaths for SSG
   - Use [param] syntax for dynamic segments
   - Handle 404 cases with custom error pages

3. **Generate New Routes**
   ```bash
   # Create new route with scaffolding
   bash scripts/generate-route.sh /blog/[slug] --layout blog

   # Create standard page
   bash scripts/generate-page.sh /about --layout marketing
   ```

4. **API Endpoints**
   - Read: templates/routing/api-endpoint.ts
   - Read: examples/api-routes.md
   - Create endpoints in pages/api/
   - Return Response objects
   - Handle different HTTP methods

### Phase 3: Component Architecture

1. **Component Organization**
   - Read: examples/component-architecture.md
   - Structure: components/{common,layout,ui,features}
   - Use clear naming conventions
   - Separate presentational from container components

2. **Create Components**
   - Read: templates/components/base-component.astro
   - Read: templates/components/props-component.astro
   - Define TypeScript interfaces for props
   - Use slots for composition
   - Export component types

3. **Async Data Fetching**
   - Read: templates/components/async-component.astro
   - Fetch data in component frontmatter
   - Handle loading and error states
   - Cache responses when appropriate

4. **Islands Architecture**
   - Read: templates/components/island-wrapper.astro
   - Use framework components selectively
   - Apply appropriate client directives
   - Minimize client-side JavaScript

### Phase 4: Layout System

1. **Base Layout**
   - Read: templates/layouts/base-layout.astro
   - Include global styles, meta tags, scripts
   - Setup SEO defaults
   - Add accessibility features

2. **Nested Layouts**
   - Read: examples/layout-hierarchy.md
   - Read: templates/layouts/nested-layout.astro
   - Create layout chains: base → section → page
   - Use layout prop pattern
   - Pass data through layout hierarchy

3. **Content-Specific Layouts**
   - Read: templates/layouts/blog-layout.astro
   - Read: templates/layouts/docs-layout.astro
   - Create specialized layouts for content types
   - Add navigation, TOC, breadcrumbs
   - Include content metadata

### Phase 5: Content Strategy

1. **Content Collections**
   - Read: examples/content-collections-usage.md
   - Define schemas in src/content/config.ts
   - Use type-safe content queries
   - Implement content validation

2. **Blog Architecture**
   - Read: templates/content/blog-post.md
   - Setup blog collection with frontmatter
   - Create blog index with pagination
   - Add RSS feed generation
   - Implement tag/category filtering

3. **Documentation Sites**
   - Read: templates/content/documentation-page.md
   - Create hierarchical navigation
   - Add search functionality
   - Include code syntax highlighting
   - Generate table of contents

### Phase 6: Build Optimization

1. **Configure Build Settings**
   - Read: templates/build/astro.config.ts
   - Read: examples/build-optimization.md
   - Set output mode (static, server, hybrid)
   - Configure build splitting
   - Enable compression

2. **Apply Optimizations**
   ```bash
   # Run optimization script
   bash scripts/optimize-build.sh

   # Analyze performance
   bash scripts/analyze-performance.sh
   ```

3. **Image Optimization**
   - Read: templates/build/image-optimization.ts
   - Use Astro Image component
   - Configure image formats (WebP, AVIF)
   - Implement responsive images
   - Add lazy loading

4. **Bundle Optimization**
   - Analyze bundle sizes
   - Split vendor chunks
   - Implement code splitting
   - Minimize CSS and JavaScript
   - Remove unused dependencies

### Phase 7: SEO and Performance

1. **SEO Setup**
   - Read: examples/seo-patterns.md
   - Add meta tags to base layout
   - Generate sitemap and robots.txt
   - Implement structured data
   - Add Open Graph and Twitter cards

2. **Generate Sitemap**
   ```bash
   bash scripts/generate-sitemap.sh
   ```

3. **Performance Testing**
   - Test with Lighthouse
   - Verify Core Web Vitals
   - Check page load times
   - Validate accessibility scores

## Best Practices

### Routing

- **File Organization**: Group related routes in directories
- **Index Files**: Use index.astro for directory default pages
- **Dynamic Parameters**: Name params clearly: [postSlug] not [slug]
- **404 Handling**: Always provide custom 404.astro page
- **Redirects**: Use Astro redirects, not client-side navigation

### Component Design

- **Single Responsibility**: Each component does one thing well
- **Composition**: Use slots and props for flexibility
- **Type Safety**: Define TypeScript interfaces for all props
- **Async Loading**: Fetch data in component frontmatter
- **Minimal Client JS**: Keep components static by default

### Layout Architecture

- **Layout Hierarchy**: Base → Section → Page layouts
- **Consistent Structure**: All layouts extend base layout
- **Slot Usage**: Use named slots for flexible content areas
- **SEO in Base**: Put SEO defaults in base layout
- **Performance**: Avoid heavy computation in layouts

### Content Management

- **Content Collections**: Use for all structured content
- **Frontmatter Schema**: Define strict schemas for validation
- **Type Safety**: Generate TypeScript types from schemas
- **Markdown**: Use remark/rehype plugins for enhancements
- **Asset Management**: Store assets in src/ for optimization

### Build Performance

- **Static by Default**: Generate static HTML when possible
- **Code Splitting**: Split bundles by route
- **Image Optimization**: Always use Astro Image
- **Prefetching**: Prefetch critical routes
- **Caching**: Configure appropriate cache headers

### SEO

- **Semantic HTML**: Use proper heading hierarchy
- **Meta Tags**: Include title, description, OG tags
- **Sitemap**: Generate and submit to search engines
- **Structured Data**: Add JSON-LD for rich results
- **Performance**: Fast sites rank better

## Common Patterns

### Pattern 1: Dynamic Blog Route

```astro
---
// src/pages/blog/[slug].astro
import { getCollection } from 'astro:content';
import BlogLayout from '@/layouts/BlogLayout.astro';

export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map(post => ({
    params: { slug: post.slug }
    props: { post }
  }));
}

const { post } = Astro.props;
const { Content } = await post.render();
---

<BlogLayout title={post.data.title} description={post.data.description}>
  <Content />
</BlogLayout>
```

### Pattern 2: Nested Layout Chain

```astro
---
// src/layouts/BlogLayout.astro
import BaseLayout from './BaseLayout.astro';

interface Props {
  title: string;
  description: string;
}

const { title, description } = Astro.props;
---

<BaseLayout title={title} description={description}>
  <div class="blog-container">
    <aside class="sidebar">
      <!-- Blog sidebar -->
    </aside>
    <main class="content">
      <slot />
    </main>
  </div>
</BaseLayout>
```

### Pattern 3: Type-Safe Component Props

```astro
---
// src/components/Card.astro
export interface Props {
  title: string;
  description?: string;
  href?: string;
  variant?: 'default' | 'featured' | 'compact';
}

const {
  title
  description
  href
  variant = 'default'
} = Astro.props;
---

<div class={`card card-${variant}`}>
  <h3>{title}</h3>
  {description && <p>{description}</p>}
  {href && <a href={href}>Read more</a>}
</div>
```

### Pattern 4: API Endpoint

```typescript
// src/pages/api/posts.ts
import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

export const GET: APIRoute = async ({ request }) => {
  const posts = await getCollection('blog');

  return new Response(JSON.stringify(posts), {
    status: 200
    headers: {
      'Content-Type': 'application/json'
      'Cache-Control': 'public, max-age=3600'
    }
  });
};
```

### Pattern 5: Optimized Image Usage

```astro
---
import { Image } from 'astro:assets';
import heroImage from '@/assets/hero.jpg';
---

<Image
  src={heroImage}
  alt="Hero image"
  width={1200}
  height={600}
  format="webp"
  loading="lazy"
  quality={80}
/>
```

## Troubleshooting

### Routes Not Generating

**Problem**: Dynamic routes not building

**Solution**:
1. Check getStaticPaths returns array of {params, props}
2. Verify params match route file name: [slug].astro needs params.slug
3. Ensure all content is available at build time
4. Check for async issues in getStaticPaths

### Build Performance Issues

**Problem**: Slow build times

**Solution**:
1. Run: `bash scripts/analyze-performance.sh`
2. Check for unnecessary data fetching
3. Optimize images before importing
4. Review large dependencies
5. Enable build parallelization

### Component Not Rendering

**Problem**: Component shows blank or errors

**Solution**:
1. Check component imports use correct path aliases
2. Verify props interface matches usage
3. Check for SSR-incompatible code (window, document)
4. Review error messages in build output

### Layout Not Applied

**Problem**: Layout styles or structure missing

**Solution**:
1. Verify layout prop is passed correctly
2. Check layout file exports default component
3. Ensure base layout includes global styles
4. Review slot placement in layout chain

### SEO Tags Not Appearing

**Problem**: Meta tags missing from pages

**Solution**:
1. Check base layout includes SEO component
2. Verify props passed through layout hierarchy
3. Inspect generated HTML for meta tags
4. Ensure head slot is used correctly

## Related Skills

- **component-integration**: For React, MDX, and Tailwind integration
- **content-collections**: Deep dive into content management
- **performance-optimization**: Advanced performance tuning

## Requirements

- Node.js 18+
- Astro 4.0+
- TypeScript 5.0+
- Recommended: pnpm or yarn

---

**Plugin**: website-builder
**Version**: 1.0.0
