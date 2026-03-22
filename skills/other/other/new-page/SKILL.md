---
name: new-page
description: Creates a new Astro page with the correct layout, dark mode support, and project conventions. Use when adding a new page or route to the site.
argument-hint: "<page-name> [--ssr]"
disable-model-invocation: true
---

Create a new page in the `src/pages/` directory following project conventions.

## Steps

1. Take the page name from the user's argument. If not provided, ask for one.
2. Determine the file path: `src/pages/<page-name>.astro` (or `src/pages/<page-name>/index.astro` for nested routes).
3. Check if `--ssr` was specified in the argument. Default is static (prerendered).
4. Create the page file:

**Static page (default):**

```astro
---
import Base from "../layouts/Base.astro";

export const prerender = true;
---

<Base title="<Page Title>" description="<page description>">
  <section class="mx-auto max-w-6xl px-4 pt-16 pb-20">
    <h1 class="text-3xl sm:text-4xl font-bold tracking-tight text-gray-900 dark:text-gray-100">
      <Page Title>
    </h1>
    <p class="mt-4 text-lg text-gray-600 dark:text-gray-400">
      Page description goes here.
    </p>
  </section>
</Base>
```

**SSR page (with `--ssr`):**

```astro
---
import Base from "../layouts/Base.astro";

const env = Astro.locals.runtime.env;
---

<Base title="<Page Title>" description="<page description>">
  <section class="mx-auto max-w-6xl px-4 pt-16 pb-20">
    <h1 class="text-3xl sm:text-4xl font-bold tracking-tight text-gray-900 dark:text-gray-100">
      <Page Title>
    </h1>
  </section>
</Base>
```

5. Adjust the layout import path based on file depth (e.g., `../../layouts/Base.astro` for nested pages).
6. Ask the user if they want to add a navigation link in `src/components/Header.astro`. If yes, add an entry to the `navLinks` array.
7. Tell the user:
   - The file was created
   - Static pages include `export const prerender = true`
   - SSR pages can access Cloudflare bindings via `Astro.locals.runtime.env`
   - Standard layout classes: `mx-auto max-w-6xl px-4 pt-16 pb-20`
