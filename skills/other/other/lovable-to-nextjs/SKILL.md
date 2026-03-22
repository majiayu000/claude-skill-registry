---
name: lovable-to-nextjs
description: >
  Convert Lovable/Vite React projects to Next.js App Router with static export for GitHub Pages.
  Handles full project restructuring: routing, SEO (metadata, OpenGraph, JSON-LD), sitemap,
  GitHub Actions CI/CD pipeline, data/ folder as file-based CMS, and proper 'use client' boundaries.
  Use this skill whenever the user mentions converting a Vite project to Next.js, migrating from
  Lovable to Next.js, restructuring a React SPA for static export, setting up a Next.js site with
  SEO and GitHub Pages deployment, or wants to turn a Vite/React project into a production-ready
  static Next.js site. Also trigger when the user has a Lovable-generated project and wants better
  SEO, performance, or deployment setup.
---

# Lovable/Vite to Next.js Converter

Convert Lovable (Vite + React) projects into production-ready Next.js static sites with excellent SEO,
a file-based CMS pattern using `data/`, and GitHub Pages deployment.

## Package manager: yarn classic (v1) only

Use yarn classic (v1.22.x) exclusively. Never use npm. All commands, scripts, and CI pipelines must use yarn.
- `yarn install` (not npm install)
- `yarn add` (not npm install package)
- `yarn build` (not npm run build)
- `yarn create next-app` (not npx create-next-app) for scaffolding
- `npx shadcn@latest` is the only exception — shadcn CLI has no `yarn create` equivalent
- CI: `yarn install --frozen-lockfile`

Important: yarn classic does NOT have `yarn dlx`. Use `yarn create <name>` for `create-*` packages,
and `npx` only when there is no yarn alternative (like shadcn CLI).

## Why this approach matters

Lovable generates Vite + React SPAs with client-side routing (react-router-dom). These work fine for
interactive apps but are terrible for SEO — search engines see an empty HTML shell. By converting to
Next.js with static export, every page becomes a real HTML file with proper metadata, structured data,
and sitemap entries. The site stays fully static (no server needed) but gains all the SEO benefits.

The key insight: **pages should be server components** (no 'use client'). Only interactive leaf components
(navbars, carousels, forms) need 'use client'. This is critical because static export generates HTML at
build time — if a page is a client component, its content won't be in the initial HTML.

## Pre-conversion checklist

Before starting, read the Vite project to understand:
1. **Routing** — Check `src/App.tsx` or router config for all routes and their components
2. **Components** — Map which components exist and their dependencies
3. **Data** — Identify hardcoded content that should move to `data/` files
4. **Assets** — Find images, fonts, and static files in `src/assets/`
5. **Dependencies** — Check package.json for what to keep vs replace
6. **Styling** — Confirm Tailwind CSS setup and copy HSL CSS variables from `index.css`

## Conversion steps

### Step 1: Scaffold with create-next-app

Always start by scaffolding a real Next.js project. This ensures all dependencies are compatible
and correctly resolved. Never try to manually write a package.json from scratch — that leads to
version mismatches and missing peer dependencies.

```bash
yarn create next-app <project-name> --typescript --tailwind --eslint --app --src-dir --no-import-alias --yes
```

**IMPORTANT:** Do NOT use `@latest` suffix (e.g. `yarn create next-app@latest`) — it fails on
yarn classic with "is not recognized as an internal or external command". Just `yarn create next-app`.

The `--yes` flag skips interactive prompts (like React Compiler). With yarn classic, `yarn create`
automatically downloads and runs the `create-next-app` package.

### Step 2: Downgrade Tailwind v4 to v3 and set up postcss

As of 2025+, `create-next-app` scaffolds with Tailwind v4 and `@tailwindcss/postcss`. Lovable projects
and shadcn/ui use Tailwind v3 with HSL CSS variables and `tailwind.config.ts`. Tailwind v4 uses a
completely different config system (CSS-based, oklch colors) that is incompatible with this pattern.

**You must downgrade before running shadcn init**, otherwise shadcn will generate oklch-based globals.css
that won't work with the Lovable project's HSL design tokens.

```bash
# Remove Tailwind v4 postcss plugin
yarn remove @tailwindcss/postcss

# Install Tailwind v3 + required plugins
yarn add -D tailwindcss@3 postcss autoprefixer tailwindcss-animate
```

Then create `tailwind.config.ts` (the scaffold won't have one since v4 uses CSS config)
and replace `postcss.config.mjs` to use `tailwindcss` + `autoprefixer` instead of `@tailwindcss/postcss`.
See `references/config-templates.md` for both files.

### Step 3: Initialize shadcn/ui and copy components from Lovable

**CRITICAL:** Do NOT use `npx shadcn@latest add` to install UI components. The latest shadcn CLI (v4)
generates components using `@base-ui/react` which look completely different from the Lovable versions
(different imports, styles, sizes, no `asChild` prop). The converted site will NOT look identical to
the original if you use the generated components.

**The correct approach:**

1. Run `npx shadcn@latest init -y --defaults` — this only creates `components.json` and `lib/utils.ts`
2. Copy the entire `components/ui/` folder from the Lovable project into `src/components/ui/`
3. Install all `@radix-ui/*` dependencies that the copied components need

```bash
# Step 1: shadcn init only (creates components.json + lib/utils.ts)
npx shadcn@latest init -y --defaults

# Step 2: Copy components from Lovable project
cp -r ../lovable-project/src/components/ui/* src/components/ui/

# Step 3: Install radix dependencies used by the Lovable components
# Check the Lovable project's package.json for all @radix-ui/* packages and install them:
yarn add @radix-ui/react-slot @radix-ui/react-accordion @radix-ui/react-dialog \
  @radix-ui/react-dropdown-menu @radix-ui/react-popover @radix-ui/react-tabs \
  @radix-ui/react-tooltip @radix-ui/react-toast @radix-ui/react-select \
  @radix-ui/react-checkbox @radix-ui/react-switch @radix-ui/react-label \
  @radix-ui/react-separator @radix-ui/react-scroll-area @radix-ui/react-avatar \
  @radix-ui/react-progress @radix-ui/react-radio-group @radix-ui/react-toggle \
  @radix-ui/react-toggle-group @radix-ui/react-collapsible @radix-ui/react-hover-card \
  @radix-ui/react-navigation-menu @radix-ui/react-menubar @radix-ui/react-context-menu \
  @radix-ui/react-alert-dialog @radix-ui/react-aspect-ratio @radix-ui/react-slider
# (only install the ones actually used — check the Lovable project's package.json)

# Step 4: Install other dependencies
yarn add next-sitemap lucide-react sonner class-variance-authority clsx tailwind-merge nextjs-toploader
# Add any project-specific deps (framer-motion, recharts, etc.)
```

**After shadcn init:** The generated `globals.css` will have shadcn's default oklch/tw-animate-css
format. You MUST replace it entirely with the Lovable project's HSL CSS variables using the
`@tailwind base/components/utilities` directives (Tailwind v3 syntax). Copy the `:root` and `.dark`
variables from the original `src/index.css`. See `references/config-templates.md` for the structure.

### Step 4: Configure for static export

Edit the generated `next.config.ts` for static export:

```typescript
const nextConfig: NextConfig = {
  output: "export",
  distDir: 'dist',
  images: { unoptimized: true },
  reactStrictMode: true,
  typescript: { ignoreBuildErrors: true },
  poweredByHeader: false,
};
```

**Do NOT include `eslint: { ignoreDuringBuilds: true }`.** This option was removed in Next.js 16+
and will cause a build warning or error.

Add sitemap scripts to package.json:
```json
{
  "sitemap": "next-sitemap --config next-sitemap.config.cjs",
  "postbuild": "yarn sitemap"
}
```

### Step 5: Set up the project structure

Organize the src/ folder following this convention:

```
src/
├── app/
│   ├── layout.tsx          # Root layout (server component)
│   ├── page.tsx            # Home page (server component)
│   ├── globals.css         # Tailwind v3 + HSL design tokens
│   ├── not-found.tsx       # 404 page
│   └── [route]/
│       └── page.tsx        # Each route becomes a folder
├── components/
│   ├── layout/             # Navbar, Footer (use client)
│   ├── sections/           # Page sections
│   └── ui/                 # shadcn/ui components
├── data/                   # JSON content files (file-based CMS)
├── lib/
│   ├── utils.ts            # cn() helper
│   └── schema.tsx          # JSON-LD structured data + SchemaMarkup component
├── hooks/                  # Custom React hooks
└── types/                  # TypeScript types
```

**IMPORTANT:** `schema.tsx` must use `.tsx` extension, not `.ts`, because it contains JSX
(the SchemaMarkup component). Using `.ts` will cause a Turbopack parse error during build.

Also create these at root level:
```
.github/workflows/deploy.yml    # GitHub Actions pipeline
next-sitemap.config.cjs         # Sitemap configuration
public/.nojekyll                # Required for GitHub Pages
public/images/                  # Static images (moved from src/assets/)
```

### Step 6: Move assets to public/

Vite projects import images from `src/assets/` using ES module imports (`import heroImg from "@/assets/hero.jpg"`).
Next.js static export doesn't support this pattern.

Move all images from `src/assets/` to `public/images/` and reference them with string paths:

```typescript
// Vite (BEFORE):
import heroImg from "@/assets/hero-amazon.jpg";
<img src={heroImg} alt="..." />

// Next.js (AFTER):
<img src="/images/hero-amazon.jpg" alt="..." />
```

Remove all `import ... from "@/assets/..."` statements. Use plain `<img>` tags with `/images/` paths.
Do NOT use `next/image` `<Image>` component — it requires server-side optimization which doesn't work
with `output: "export"`.

### Step 7: Convert routing

Replace react-router-dom routes with file-based routing:

| Vite (react-router-dom) | Next.js (App Router) |
|---|---|
| `<Route path="/" element={<Home />} />` | `src/app/page.tsx` |
| `<Route path="/about" element={<About />} />` | `src/app/about/page.tsx` |
| `<Route path="/blog/:slug" element={<Post />} />` | `src/app/blog/[slug]/page.tsx` |
| `<Route path="*" element={<NotFound />} />` | `src/app/not-found.tsx` |

For dynamic routes, add `generateStaticParams`:
```typescript
export async function generateStaticParams() {
  return posts.map((post) => ({ slug: post.slug }));
}
```

**Dynamic route params are async in Next.js 15+.** Both `generateMetadata` and page components
receive `params` as a `Promise`:
```typescript
export default async function Page({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  // ...
}
```

Remove all react-router-dom imports and dependencies (useNavigate, useParams, Link, Navigate, etc.).
Replace with Next.js equivalents:
- `Link` from `next/link`
- `usePathname` from `next/navigation` (only in client components)
- `notFound()` from `next/navigation` (instead of `<Navigate to="..." />`)
- Remove `<BrowserRouter>`, `<Routes>`, `<Route>` wrappers entirely

### Step 8: Extract content to data/ folder

Move hardcoded content from components into `src/data/` JSON files. This creates a
file-based CMS where content changes don't require touching component code.

**Pattern:** One JSON file per content type:
```
src/data/
├── site.json          # Site-wide config (name, url, description, social links)
├── navigation.json    # Menu items
├── features.json      # Product features
├── testimonials.json  # User testimonials
├── pricing.json       # Pricing plans
├── faq.json           # FAQ entries
└── team.json          # Team members (if applicable)
```

**site.json example:**
```json
{
  "name": "My Product",
  "url": "https://myproduct.com",
  "description": "Short description for SEO",
  "locale": "pt-BR",
  "social": {
    "twitter": "@myproduct",
    "github": "https://github.com/myproduct"
  },
  "analytics": {
    "gtmId": "GTM-XXXXXXX",
    "gaId": "G-XXXXXXXXXX"
  }
}
```

Import data in server components:
```typescript
import siteData from '@/data/site.json';
import features from '@/data/features.json';
```

### Step 9: Implement SEO

This is where the conversion really pays off. Read `references/seo-templates.md` for complete examples.

**Root layout metadata** — Set defaults that apply to all pages:
- `metadataBase` with the site URL
- `title` with `default` and `template` pattern (`%s | Site Name`)
- `description`, `keywords`, `authors`, `creator`, `publisher`
- `robots` with googleBot directives
- `openGraph` with type, locale, url, siteName
- `twitter` card configuration
- `alternates.canonical`

**Per-page metadata** — Override defaults on each page:
```typescript
export const metadata: Metadata = {
  title: "Features - My Product",
  description: "Page-specific description",
  openGraph: { /* page-specific OG */ },
};
```

**JSON-LD structured data** — Create `src/lib/schema.tsx` (must be .tsx!) with schemas:
- WebSite schema (every site)
- Organization or Person schema
- BreadcrumbList for navigation
- FAQPage if there's an FAQ section
- SoftwareApplication if it's an app landing page
- Product if it's a product page

Render with a SchemaMarkup component:
```typescript
export function SchemaMarkup({ schema }: { schema: object | object[] }) {
  const data = Array.isArray(schema) ? schema : [schema];
  return (
    <>
      {data.map((s, i) => (
        <script
          key={i}
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(s) }}
        />
      ))}
    </>
  );
}
```

### Step 10: Handle 'use client' correctly

This is the most important architectural decision. The rule is simple but crucial:

**Pages (`page.tsx`) should NEVER have 'use client'.**

Pages are server components that generate static HTML. If you put 'use client' on a page,
its content won't be pre-rendered — you'll get the same empty-shell problem as the Vite SPA.

**What needs 'use client':**
- Components with `useState`, `useEffect`, `useRef`
- Components with event handlers (onClick, onChange)
- Components using browser APIs (window, document)
- Components using hooks from libraries (usePathname, useIsMobile)
- Navbar with mobile menu toggle
- Carousels, accordions, tabs with state
- Form components

**What stays as server components:**
- All `page.tsx` files
- `layout.tsx` (root layout)
- Pure display components (Hero sections, static cards)
- Components that only receive and render props
- SchemaMarkup component

**The boundary pattern:** Create a client component wrapper that receives server-rendered content:
```typescript
// sections/Features.tsx (server component)
export function Features() {
  const features = featuresData; // imported from data/
  return (
    <section>
      <h2>Features</h2>
      <FeaturesGrid features={features} /> {/* client if interactive */}
    </section>
  );
}
```

If a section component from Lovable uses only simple animations (Framer Motion) or state,
extract it as a client component in `components/sections/` and import it from the page.
The page itself stays server-rendered.

### Step 11: Set up sitemap and robots.txt

Use `next-sitemap` for automatic generation. See `references/config-templates.md` for the full config.

Key points:
- Set `siteUrl` to the actual production URL
- Use `transform` to assign priorities (homepage = 1.0, main pages = 0.9, etc.)
- Generate robots.txt automatically
- Run via `postbuild` script

### Step 12: Set up GitHub Actions

Create `.github/workflows/deploy.yml`. See `references/config-templates.md` for the full template.

The pipeline:
1. Triggers on push to `main`
2. Installs dependencies with `yarn install --frozen-lockfile`
3. Builds the static site (`yarn build`, which auto-runs `postbuild` for sitemap)
4. Uploads `dist/` as GitHub Pages artifact
5. Deploys to GitHub Pages

### Step 13: Final verification

After conversion, verify:
1. `yarn build` completes without errors
2. The `dist/` folder contains HTML files for every route
3. Each HTML file has proper `<title>`, `<meta>` tags in the source
4. No page.tsx files have 'use client'
5. `sitemap.xml` and `robots.txt` are generated in `dist/`
6. All internal links use `<Link>` from `next/link`
7. Images use `<img>` tags (not next/image with optimization, since it's static)
8. The `.nojekyll` file exists in `public/`
9. JSON-LD structured data present in HTML source (`application/ld+json`)

## Common pitfalls (lessons learned)

1. **`yarn create next-app@latest` fails** — Remove `@latest`. Yarn classic can't handle the suffix.
2. **Tailwind v4 vs v3** — Scaffold comes with Tailwind v4 + `@tailwindcss/postcss`. Must downgrade
   to v3 BEFORE running `shadcn init`, otherwise globals.css gets oklch colors incompatible with
   Lovable's HSL variables.
3. **`eslint` in next.config.ts** — Removed in Next.js 16. Don't include it or you get warnings/errors.
4. **schema.ts parse error** — Any file with JSX (like SchemaMarkup component) MUST use `.tsx` extension.
   Turbopack will fail with "Expected a semicolon" if JSX is in a `.ts` file.
5. **Asset imports** — Vite's `import img from "@/assets/..."` doesn't work in Next.js static export.
   Move to `public/images/` and use string paths.
6. **Dynamic params are Promise** — In Next.js 15+, `params` in page components and `generateMetadata`
   is `Promise<{ slug: string }>` — must `await params` before use.
7. **shadcn overwrites globals.css** — After `shadcn init`, the globals.css will have Tailwind v4 syntax
   (`@import "tailwindcss"`, oklch colors). Replace it entirely with Tailwind v3 directives and the
   project's original HSL CSS variables.
8. **Don't manually write package.json** — Always scaffold with `create-next-app`, then modify.
   Manual package.json leads to missing peer deps and incorrect package names.
9. **shadcn v4 components are visually incompatible with Lovable** — The latest `shadcn@latest` generates
   completely different components using `@base-ui/react` instead of `@radix-ui/*`. Button, Card, Badge,
   Input, Select — ALL of them look different (wrong sizes, missing `asChild`, different variant styles).
   **NEVER use `npx shadcn@latest add` to install components.** Instead, copy the entire `components/ui/`
   folder directly from the Lovable project, then install the `@radix-ui/*` packages from the Lovable
   project's package.json. Only use `npx shadcn@latest init` (for `components.json` + `lib/utils.ts`).

## Common Lovable patterns and how to convert them

**Lovable query setup (QueryClientProvider):**
Create `src/app/providers.tsx` with 'use client' and wrap children in layout.

**Lovable toast setup (sonner/shadcn):**
Import Toaster components in the root layout (they're client components but used inside a server layout).

**Lovable shadcn/ui components:**
Never use `npx shadcn@latest add` — it generates incompatible v4 components using `@base-ui/react`.
Copy the entire `components/ui/` folder from the Lovable project and install all `@radix-ui/*` packages
from the Lovable project's package.json. This ensures the converted site looks identical to the original.

**Lovable custom hooks:**
Move to `src/hooks/`. Add 'use client' if they use browser APIs.

**Lovable `src/assets/` images:**
Move to `public/images/`. Replace all `import img from "@/assets/..."` with `<img src="/images/..." />`.

## File reference

For complete template files (configs, layout, deploy workflow, sitemap config, etc.),
read `references/config-templates.md`.

For complete SEO templates (metadata patterns, JSON-LD schemas, SchemaMarkup component),
read `references/seo-templates.md`.
