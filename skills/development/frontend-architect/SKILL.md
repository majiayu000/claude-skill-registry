---
name: frontend-architect
description: Frontend stack decisions, Cloudflare deployment patterns, component systems, and internal tools architecture. Use for framework selection, deployment strategy, design system bridging, shadcn setup. Activate on "frontend architecture", "tech stack", "Cloudflare Pages", "component library", "internal tools", "shadcn setup". NOT for writing CSS (use frontend-developer), design critique (use design-critic), or backend APIs.
allowed-tools: Read,Write,Edit,Bash,Glob,Grep,WebFetch,WebSearch
---

# Frontend Architect

Expert in frontend stack decisions, Cloudflare deployment, and bridging design systems to component implementations. Specializes in internal tools that expose prototypes to select users.

## When to Use

✅ **Use for**:
- Choosing between Next.js, Astro, Remix, etc.
- Setting up Cloudflare Pages/Workers
- Designing internal tool architectures
- Bridging design catalogs to component libraries
- Setting up shadcn/ui from scratch
- Feature flag and preview URL strategies

❌ **NOT for**:
- Writing CSS or component styling (use `frontend-developer`)
- Design assessment (use `design-critic`)
- Backend API design (use `api-architect`)
- Database decisions
- DevOps/CI beyond deployment

## Framework Selection Decision Tree

### Question 1: What's the Content Type?

| Content | Framework | Why |
|---------|-----------|-----|
| Mostly static, some interactivity | **Astro** | Islands architecture, minimal JS |
| Full-stack app, heavy interactivity | **Next.js** | RSC, API routes, ecosystem |
| Content-heavy with CMS | **Astro** or **Next.js** | Both have great CMS integrations |
| SPA with complex state | **React + Vite** | Faster builds, simpler mental model |
| Marketing/landing pages | **Astro** | Best performance, partial hydration |

### Question 2: Where's It Deployed?

| Platform | Best Fit | Considerations |
|----------|----------|----------------|
| Cloudflare Pages | Astro, Next.js (OpenNext) | Edge-first, workers integration |
| Vercel | Next.js | Native support, best DX |
| Netlify | Astro, SvelteKit | Strong Astro support |
| Self-hosted | Any | Control vs. maintenance tradeoff |

### Question 3: Team Experience?

| Team | Recommendation |
|------|----------------|
| React experts | Next.js or React + Vite |
| Vue/Nuxt background | Nuxt 3 |
| Performance obsessed | Astro or SolidStart |
| Content team involved | Astro with MDX |

## Cloudflare Pages Patterns

### Basic Setup

```bash
# Initialize with wrangler
npx wrangler pages project create my-project

# Link existing project
npx wrangler pages project list
```

### wrangler.toml Configuration

```toml
name = "my-project"
compatibility_date = "2026-01-31"
pages_build_output_dir = "out"  # or ".next" for Next.js

# Environment variables
[vars]
NEXT_PUBLIC_API_URL = "https://api.example.com"

# Secrets (set via wrangler secret)
# GITHUB_TOKEN, API_KEY, etc.

# KV namespace (for caching)
[[kv_namespaces]]
binding = "CACHE"
id = "abc123..."
```

### Preview Deployments

Every branch gets a preview URL:

```
Pattern: <branch>.<project>.pages.dev

Examples:
- main.my-project.pages.dev (production)
- feature-123.my-project.pages.dev (preview)
- staging.my-project.pages.dev (staging)
```

**Workflow**:
```bash
# Deploy preview manually
npx wrangler pages deploy out --project-name=my-project

# Or use GitHub integration
# Push to any branch → automatic preview URL
```

### Access Control (Internal Tools)

```toml
# In wrangler.toml or Cloudflare dashboard

# Cloudflare Access for auth
# Configure in dashboard: Access > Applications

# Patterns:
# - internal.example.com → Protected by Access
# - preview-*.pages.dev → Protected by Access
# - example.com → Public
```

### Feature Flags at Edge

```typescript
// src/middleware.ts (Next.js) or functions/_middleware.ts (Pages)

export async function onRequest(context: { request: Request; env: Env }) {
  const flags = await context.env.FLAGS.get('feature-flags', 'json');

  // Check user eligibility
  const email = context.request.headers.get('cf-access-authenticated-user-email');

  if (flags?.betaUsers?.includes(email)) {
    // Rewrite to beta version
    return context.env.ASSETS.fetch(
      new Request('https://beta.example.com' + new URL(context.request.url).pathname)
    );
  }

  return context.next();
}
```

## Internal Tools Architecture

For "prototypes/side ideas exposed as internal tools only a few users can see":

### Architecture Pattern

```
your-domain.com/           # Public production
├── internal/              # Cloudflare Access protected
│   ├── tool-1/           # Internal tool 1
│   ├── tool-2/           # Internal tool 2
│   └── experiments/      # Wild experiments
└── preview-*.pages.dev    # Branch previews (also protected)
```

### Access Levels

| Role | Access | Implementation |
|------|--------|----------------|
| Admin | All internal tools | Cloudflare Access group |
| Beta | Stable internal tools | Access group + feature flags |
| Public | Production only | Default |

### Monorepo Structure (Turborepo)

```
apps/
├── web/                   # Public site
├── internal/              # Internal tools (protected)
│   ├── admin/            # Admin dashboard
│   ├── prototype-1/      # Experiment
│   └── prototype-2/      # Another experiment
└── shared/               # Shared components

packages/
├── ui/                    # Design system
├── config/               # Shared configs
└── types/                # Shared types
```

### Quick Prototype Script

```bash
#!/bin/bash
# scripts/new-prototype.sh

NAME=$1
mkdir -p apps/internal/$NAME

cat > apps/internal/$NAME/package.json << EOF
{
  "name": "@internal/$NAME",
  "version": "0.0.1",
  "private": true,
  "scripts": {
    "dev": "next dev --port 3100",
    "build": "next build",
    "deploy": "wrangler pages deploy out --project-name=$NAME"
  }
}
EOF

echo "Created apps/internal/$NAME"
echo "Run: cd apps/internal/$NAME && pnpm dev"
```

## shadcn/ui Setup

### Initial Setup

```bash
# For Next.js
npx shadcn@latest init

# Interactive prompts:
# - Style: New York (more opinionated) or Default
# - Base color: Slate, Gray, Zinc, Neutral, Stone
# - CSS variables: Yes (recommended)
# - tailwind.config.js path: tailwind.config.js
# - components.json location: ./
# - Aliases: @/components, @/lib/utils
```

### components.json

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.js",
    "css": "app/globals.css",
    "baseColor": "slate",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils"
  }
}
```

### Adding Components

```bash
# Add specific components
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add dialog

# Add multiple at once
npx shadcn@latest add button card dialog input

# List available
npx shadcn@latest add --help
```

### Customization Pattern

```typescript
// components/ui/button.tsx (after shadcn generates it)

// Add your variants to the existing cva()
const buttonVariants = cva(
  "...", // existing base styles
  {
    variants: {
      variant: {
        default: "...",
        destructive: "...",
        // ADD YOUR CUSTOM VARIANTS
        neobrutalist: "border-3 border-black shadow-[4px_4px_0_#000] hover:shadow-[2px_2px_0_#000] active:shadow-none",
        ghost: "...",
      },
      size: {
        // existing sizes...
        // ADD YOUR CUSTOM SIZES
        jumbo: "h-14 px-10 text-lg",
      },
    },
  }
);
```

## Design System Bridging

Connect design catalog to component implementation:

### Pattern: Token → Tailwind → Component

```
design-catalog/color-palettes.json
          ↓
tailwind.config.js (extends theme.colors)
          ↓
components/ui/*.tsx (use Tailwind classes)
```

### Implementation

```typescript
// lib/design-catalog/loader.ts
import palettes from '@/design-catalog/color-palettes.json';

export function getDesignTokens(trendId: string) {
  const palette = palettes.palettes.find(p => p.trend === trendId);

  return {
    colors: Object.fromEntries(
      palette.colors.map(c => [c.name.toLowerCase().replace(' ', '-'), c.hex])
    ),
    // ... typography, spacing from other catalog files
  };
}

// scripts/generate-tailwind-theme.ts
import { getDesignTokens } from '../lib/design-catalog/loader';

const tokens = getDesignTokens('neobrutalism');
const tailwindTheme = {
  theme: {
    extend: {
      colors: tokens.colors,
    },
  },
};

fs.writeFileSync(
  'tailwind.config.generated.js',
  `module.exports = ${JSON.stringify(tailwindTheme, null, 2)}`
);
```

## Common Anti-Patterns

### Anti-Pattern: Premature Microservices

**Novice thinking**: "Let's split into 5 repos for cleanliness"

**Reality**: Coordination overhead kills velocity. Monorepo with clear boundaries is faster.

**Correct approach**: Start monorepo (Turborepo), split when you have dedicated teams per service.

---

### Anti-Pattern: Framework FOMO

**Novice thinking**: "Remix/SolidStart is hot, let's migrate"

**Reality**: Framework migrations are expensive. Stick with working stack unless there's a clear benefit.

**Correct approach**: Evaluate frameworks for NEW projects. Migrate existing only for compelling reasons (performance, developer experience, dead ecosystem).

---

### Anti-Pattern: Over-Engineering Internal Tools

**Novice thinking**: "Internal tool needs full CI/CD, comprehensive tests, perfect architecture"

**Reality**: Internal tools are for experimentation. Perfect is the enemy of shipped.

**Correct approach**: Ship fast, iterate. Add rigor when tool becomes critical. Internal tools are for learning what to build right.

---

### Anti-Pattern: Ignoring Edge Runtime Constraints

**Novice thinking**: "Just use any npm package on Cloudflare Workers"

**Reality**: Workers have no Node.js APIs. Many packages fail.

**Common failures**:
- `fs` → Use KV or R2
- `crypto` (Node) → Use Web Crypto API
- Heavy libraries → Bundle size limits

**Correct approach**: Check package compatibility. Use lightweight alternatives. Test in Workers environment early.

## Stack Recommendations by Use Case

### SaaS Dashboard

```
Framework: Next.js 14+ (App Router)
Styling: Tailwind + shadcn/ui
State: Zustand or Jotai
Data: TanStack Query + tRPC
Auth: NextAuth.js or Clerk
Deploy: Cloudflare Pages (OpenNext) or Vercel
```

### Marketing Site

```
Framework: Astro
Styling: Tailwind
CMS: Sanity, Contentful, or MDX
Deploy: Cloudflare Pages
Performance: Target 100 Lighthouse
```

### Internal Tool

```
Framework: Next.js (simpler) or React + Vite (faster builds)
Styling: Tailwind + shadcn/ui
Auth: Cloudflare Access
Deploy: Cloudflare Pages (protected)
Polish Level: 70% (ship fast)
```

### Design Showcase Gallery

```
Framework: Next.js 14+ or Astro
Styling: Tailwind + Custom CSS for showcase
Images: next/image or Astro Image
Gallery: Masonry grid, virtualized
Deploy: Cloudflare Pages
```

## Pairs With

- **design-critic**: Get design assessment before/after implementation
- **cloudflare-worker-dev**: For edge computing patterns
- **web-design-expert**: For design decisions
- **devops-automator**: For CI/CD beyond Cloudflare

## References

See `/references/` for detailed guides:
- `cloudflare-patterns.md` - Advanced Cloudflare Pages/Workers patterns
- `shadcn-customization.md` - Extending shadcn/ui components
- `internal-tools.md` - Patterns for prototype-to-internal pipelines
- `monorepo-setup.md` - Turborepo configuration for frontend apps
