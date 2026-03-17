---
name: content-collections
description: Content Collections TypeScript-first build tool for Markdown/MDX content. Use for blogs, docs, content sites with Vite + React, MDX components, type-safe Zod schemas, Contentlayer migration, or encountering TypeScript import errors, path alias issues, collection validation errors.

  Keywords: content-collections, @content-collections/core, @content-collections/vite,
  @content-collections/mdx, MDX, markdown, Zod schema validation, type-safe content,
  frontmatter, compileMDX, defineCollection, defineConfig, Vite plugin, tsconfig paths,
  .content-collections/generated, MDXContent component, rehype plugins, remark plugins,
  content schema, document transform, allPosts import, static site generation,
  blog setup, documentation, Cloudflare Workers static assets, content validation errors,
  module not found content-collections, path alias not working, MDX type errors,
  transform function async, collection not updating
license: MIT
---

# Content Collections

**Status**: Production Ready ✅
**Last Updated**: 2025-11-07
**Dependencies**: None
**Latest Versions**: @content-collections/core@0.12.0, @content-collections/vite@0.2.7, zod@3.23.8

---

## What is Content Collections?

Content Collections transforms local content files (Markdown/MDX) into **type-safe TypeScript data** with automatic validation at build time.

**Problem it solves**: Manual content parsing, lack of type safety, runtime errors from invalid frontmatter.

**How it works**:
1. Define collections in `content-collections.ts` (name, directory, Zod schema)
2. CLI/plugin scans filesystem, parses frontmatter, validates against schema
3. Generates TypeScript modules in `.content-collections/generated/`
4. Import collections: `import { allPosts } from "content-collections"`

**Perfect for**: Blogs, documentation sites, content-heavy apps with Cloudflare Workers, Vite, Next.js.

---

## Quick Start (5 Minutes)

### 1. Install Dependencies

```bash
# Bun (recommended)
bun add -d @content-collections/core @content-collections/vite zod

# npm
npm install -D @content-collections/core @content-collections/vite zod

# pnpm
pnpm add -D @content-collections/core @content-collections/vite zod
```

### 2. Configure TypeScript Path Alias

Add to `tsconfig.json`:

```json
{
  "compilerOptions": {
    "paths": {
      "content-collections": ["./.content-collections/generated"]
    }
  }
}
```

###

 3. Configure Vite Plugin

Add to `vite.config.ts`:

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import contentCollections from "@content-collections/vite";

export default defineConfig({
  plugins: [
    react(),
    contentCollections(), // MUST come after react()
  ],
});
```

### 4. Update .gitignore

```
.content-collections/
```

### 5. Create Collection Config

Create `content-collections.ts` in project root:

```typescript
import { defineCollection, defineConfig } from "@content-collections/core";
import { z } from "zod";

const posts = defineCollection({
  name: "posts",
  directory: "content/posts",
  include: "*.md",
  schema: z.object({
    title: z.string(),
    date: z.string(),
    description: z.string(),
    content: z.string(),
  }),
});

export default defineConfig({
  collections: [posts],
});
```

### 6. Create Content Directory

```bash
mkdir -p content/posts
```

Create `content/posts/first-post.md`:

```markdown
---
title: My First Post
date: 2025-11-07
description: Introduction to Content Collections
---

# My First Post

Content goes here...
```

### 7. Import and Use

```typescript
import { allPosts } from "content-collections";

console.log(allPosts); // Fully typed!
```

**Result**: Type-safe content with autocomplete, validation, and HMR.

---

## Critical Rules

### ✅ Always Do:

1. **Add path alias to tsconfig.json** - Required for imports to work
2. **Add .content-collections to .gitignore** - Generated files shouldn't be committed
3. **Use Standard Schema validators** - Zod, Valibot, ArkType supported
4. **Include `content` field in schema** - Required for frontmatter parsing
5. **Await compileMDX in transforms** - MDX compilation is async
6. **Put contentCollections() after react() in Vite** - Plugin order matters

### ❌ Never Do:

1. **Commit .content-collections directory** - Always generated, never committed
2. **Use non-standard validators** - Must support StandardSchema spec
3. **Forget to restart dev server after config changes** - Required for new collections
4. **Use sync transforms with async operations** - Transform must be async
5. **Double-wrap path alias** - Use `content-collections` not `./content-collections`
6. **Import from wrong package** - `@content-collections/core` for config, `content-collections` for data

---

## Known Issues Prevention

### Issue #1: Module not found: 'content-collections'

**Error**: `Cannot find module 'content-collections' or its corresponding type declarations`

**Why it happens**: Missing TypeScript path alias configuration.

**Prevention**:

Add to `tsconfig.json`:
```json
{
  "compilerOptions": {
    "paths": {
      "content-collections": ["./.content-collections/generated"]
    }
  }
}
```

Restart TypeScript server in VS Code: `Cmd+Shift+P` → "TypeScript: Restart TS Server"

**Source**: Common user error

---

### Issue #2: Vite Constant Restart Loop

**Error**: Dev server continuously restarts, infinite loop.

**Why it happens**: Vite watching `.content-collections` directory changes, which triggers regeneration.

**Prevention**:

1. Add to `.gitignore`:
```
.content-collections/
```

2. Add to `vite.config.ts` (if still happening):
```typescript
export default defineConfig({
  server: {
    watch: {
      ignored: ["**/.content-collections/**"],
    },
  },
});
```

**Source**: GitHub Issue #591 (TanStack Start)

---

### Issue #3: Transform Types Not Reflected

**Error**: TypeScript types don't match transformed documents.

**Why it happens**: TypeScript doesn't automatically infer transform function return type.

**Prevention**:

Explicitly type your transform return:

```typescript
const posts = defineCollection({
  name: "posts",
  // ... schema
  transform: (post): PostWithSlug => ({ // Type the return!
    ...post,
    slug: post._meta.path.replace(/\.md$/, ""),
  }),
});

type PostWithSlug = {
  // ... schema fields
  slug: string;
};
```

**Source**: GitHub Issue #396

---

### Issues #4-8: Advanced Troubleshooting

Additional issues covered in `references/advanced-troubleshooting.md`:

| Issue | Error | Quick Fix |
|-------|-------|-----------|
| #4 | Collection not updating | Verify glob pattern, restart dev server |
| #5 | MDX/Shiki errors | Use compatible versions (shiki ^1.0.0) |
| #6 | MDX path aliases fail | Use relative paths in MDX imports |
| #7 | Unclear validation errors | Add custom Zod error messages |
| #8 | Ctrl+C doesn't stop | Use `kill -9` or separate watch command |

---

## Configuration Patterns

| Pattern | Use Case | Template |
|---------|----------|----------|
| **Basic Blog** | Single collection, Markdown only | `templates/content-collections.ts` |
| **Multi-Collection** | Posts + Docs, nested folders | `templates/content-collections-multi.ts` |
| **Transform Functions** | Computed fields (slug, readingTime) | See `references/transform-cookbook.md` |
| **MDX + React** | Syntax highlighting, React components | `templates/content-collections-mdx.ts` |

For detailed schema patterns (dates, tags, validation), load `references/schema-patterns.md`.

---

## React Component Integration

### Using Collections in React

```tsx
import { allPosts } from "content-collections";

export function BlogList() {
  return (
    <ul>
      {allPosts.map((post) => (
        <li key={post._meta.path}>
          <h2>{post.title}</h2>
          <p>{post.description}</p>
          <time>{post.date}</time>
        </li>
      ))}
    </ul>
  );
}
```

---

### Rendering MDX Content

```tsx
import { MDXContent } from "@content-collections/mdx/react";

export function BlogPost({ post }: { post: { mdx: string } }) {
  return (
    <article>
      <MDXContent code={post.mdx} />
    </article>
  );
}
```

---

## Cloudflare Workers Deployment

Content Collections is **perfect for Cloudflare Workers** (build-time only, no runtime filesystem). Use template `templates/wrangler.toml` for config.

**Pattern**: `vite build` → `wrangler deploy` (Vite plugin handles content-collections automatically)

For detailed deployment guide, load `references/deployment-guide.md`.

---

## Bundled Resources

### Templates (9 copy-paste files)
`content-collections.ts`, `content-collections-multi.ts`, `content-collections-mdx.ts`, `tsconfig.json`, `vite.config.ts`, `BlogList.tsx`, `BlogPost.tsx`, `blog-post.md`, `wrangler.toml`

### Scripts
`init-content-collections.sh` - One-command automated setup

---

## Dependencies

### Required

```json
{
  "devDependencies": {
    "@content-collections/core": "^0.12.0",
    "@content-collections/vite": "^0.2.7",
    "zod": "^3.23.8"
  }
}
```

### Optional (MDX)

```json
{
  "devDependencies": {
    "@content-collections/markdown": "^0.1.4",
    "@content-collections/mdx": "^0.2.2",
    "shiki": "^1.0.0"
  }
}
```

---

## Official Documentation

- **Official Site**: https://www.content-collections.dev
- **Documentation**: https://www.content-collections.dev/docs
- **GitHub**: https://github.com/sdorra/content-collections
- **Vite Plugin**: https://www.content-collections.dev/docs/vite
- **MDX Integration**: https://www.content-collections.dev/docs/mdx

---

## Package Versions (Verified 2025-11-07)

| Package | Version | Status |
|---------|---------|--------|
| @content-collections/core | 0.12.0 | ✅ Latest stable |
| @content-collections/vite | 0.2.7 | ✅ Latest stable |
| @content-collections/mdx | 0.2.2 | ✅ Latest stable |
| @content-collections/markdown | 0.1.4 | ✅ Latest stable |
| zod | 3.23.8 | ✅ Latest stable |

---

## Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| TypeScript can't find module | Add path alias to `tsconfig.json`, restart TS server |
| Vite keeps restarting | Add `.content-collections/` to `.gitignore` |
| Changes not reflecting | Restart dev server, verify glob pattern |
| MDX compilation errors | Check Shiki version compatibility |
| Validation errors unclear | Add custom Zod error messages |

---

## When to Load References

| Reference | Load When... |
|-----------|--------------|
| `schema-patterns.md` | Setting up complex schemas, date validation, optional fields |
| `transform-cookbook.md` | Adding computed fields, async transforms, slugs |
| `mdx-components.md` | Integrating React components in MDX, syntax highlighting |
| `deployment-guide.md` | Deploying to Cloudflare Workers or other platforms |
| `advanced-troubleshooting.md` | Issues #4-8 (file watching, path aliases, process hanging) |

---

## Complete Setup Checklist

- [ ] Installed `@content-collections/core` and `@content-collections/vite`
- [ ] Installed `zod` for schema validation
- [ ] Added path alias to `tsconfig.json`
- [ ] Added `contentCollections()` to `vite.config.ts` (after react())
- [ ] Added `.content-collections/` to `.gitignore`
- [ ] Created `content-collections.ts` in project root
- [ ] Created content directory (e.g., `content/posts/`)
- [ ] Defined collection with Zod schema
- [ ] Created first content file with frontmatter
- [ ] Imported collection in React component
- [ ] Verified types work (autocomplete)
- [ ] Tested hot reloading (change content file)

