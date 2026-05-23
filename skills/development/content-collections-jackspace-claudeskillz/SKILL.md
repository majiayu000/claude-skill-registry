---
name: content-collections
description: |
  Production-tested setup for Content Collections - a TypeScript-first build tool that transforms
  local content files (Markdown/MDX) into type-safe data collections with automatic validation.

  Use when: building blogs, documentation sites, or content-heavy applications with Vite + React,
  setting up MDX content with React components, implementing type-safe content schemas with Zod,
  migrating from Contentlayer, or encountering TypeScript import errors with content collections.

  Covers: Vite plugin setup, tsconfig path aliases, collection schemas with Zod validation,
  MDX compilation with compileMDX, transform functions for computed properties, rehype/remark plugins,
  React component integration with MDXContent, Cloudflare Workers deployment, and production build optimization.

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

### Issue #4: Collection Not Updating on File Change

**Error**: New content files not appearing in collection.

**Why it happens**: Glob pattern doesn't match, or dev server needs restart.

**Prevention**:

1. Verify glob pattern matches your files:
```typescript
include: "*.md"        // Only root files
include: "**/*.md"     // All nested files
include: "posts/*.md"  // Only posts/ folder
```

2. Restart dev server after adding new files outside watched patterns
3. Check file actually saved (watch for editor issues)

**Source**: Common user error

---

### Issue #5: MDX Type Errors with Shiki

**Error**: `esbuild errors with shiki langAlias` or compilation failures.

**Why it happens**: Version incompatibility between Shiki and Content Collections.

**Prevention**:

Use compatible versions:

```json
{
  "devDependencies": {
    "@content-collections/mdx": "^0.2.2",
    "shiki": "^1.0.0"
  }
}
```

Check official compatibility matrix in docs before upgrading Shiki.

**Source**: GitHub Issue #598 (Next.js 15)

---

### Issue #6: Custom Path Aliases in MDX Imports Fail

**Error**: MDX imports with `@` alias don't resolve.

**Why it happens**: MDX compiler doesn't respect tsconfig path aliases.

**Prevention**:

Use relative paths in MDX imports:

```mdx
<!-- ❌ Won't work -->
import Component from "@/components/Component"

<!-- ✅ Works -->
import Component from "../../components/Component"
```

Or configure files appender (advanced, see references/transform-cookbook.md).

**Source**: GitHub Issue #547

---

### Issue #7: Unclear Validation Error Messages

**Error**: Cryptic Zod validation errors like "Expected string, received undefined".

**Why it happens**: Zod errors aren't formatted for content context.

**Prevention**:

Add custom error messages to schema:

```typescript
schema: z.object({
  title: z.string({
    required_error: "Title is required in frontmatter",
    invalid_type_error: "Title must be a string",
  }),
  date: z.string().refine(
    (val) => !isNaN(Date.parse(val)),
    "Date must be valid ISO date (YYYY-MM-DD)"
  ),
})
```

**Source**: GitHub Issue #403

---

### Issue #8: Ctrl+C Doesn't Stop Process

**Error**: Dev process hangs on exit, requires `kill -9`.

**Why it happens**: File watcher not cleaning up properly.

**Prevention**:

This is a known issue with the watcher. Workarounds:

1. Use `kill -9 <pid>` when it hangs
2. Use `content-collections watch` separately (not plugin) for more control
3. Add cleanup handler in `vite.config.ts` (advanced)

**Source**: GitHub Issue #546

---

## Configuration Patterns

### Basic Blog Collection

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
    tags: z.array(z.string()).optional(),
    content: z.string(),
  }),
});

export default defineConfig({
  collections: [posts],
});
```

---

### Multi-Collection Setup

```typescript
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

const docs = defineCollection({
  name: "docs",
  directory: "content/docs",
  include: "**/*.md", // Nested folders
  schema: z.object({
    title: z.string(),
    category: z.string(),
    order: z.number().optional(),
    content: z.string(),
  }),
});

export default defineConfig({
  collections: [posts, docs],
});
```

---

### Transform Functions (Computed Fields)

```typescript
const posts = defineCollection({
  name: "posts",
  directory: "content/posts",
  include: "*.md",
  schema: z.object({
    title: z.string(),
    date: z.string(),
    content: z.string(),
  }),
  transform: (post) => ({
    ...post,
    slug: post._meta.path.replace(/\.md$/, ""),
    readingTime: Math.ceil(post.content.split(/\s+/).length / 200),
    year: new Date(post.date).getFullYear(),
  }),
});
```

---

### MDX with React Components

```typescript
import { compileMDX } from "@content-collections/mdx";

const posts = defineCollection({
  name: "posts",
  directory: "content/posts",
  include: "*.mdx",
  schema: z.object({
    title: z.string(),
    date: z.string(),
    content: z.string(),
  }),
  transform: async (post) => {
    const mdx = await compileMDX(post.content, {
      syntaxHighlighter: "shiki",
      shikiOptions: {
        theme: "github-dark",
      },
    });

    return {
      ...post,
      mdx,
      slug: post._meta.path.replace(/\.mdx$/, ""),
    };
  },
});
```

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

Content Collections is **perfect for Cloudflare Workers** because:
- Build-time only (no runtime filesystem access)
- Outputs static JavaScript modules
- No Node.js dependencies in generated code

### Deployment Pattern

```
Local Dev → content-collections build → vite build → wrangler deploy
```

### wrangler.toml

```toml
name = "my-content-site"
compatibility_date = "2025-11-07"

[assets]
directory = "./dist"
binding = "ASSETS"
```

### Build Script

`package.json`:
```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "deploy": "pnpm build && wrangler deploy"
  }
}
```

**Note**: Vite plugin handles `content-collections build` automatically!

---

## Using Bundled Resources

### Templates (templates/)

Copy-paste ready configuration files:

- `content-collections.ts` - Basic blog setup
- `content-collections-multi.ts` - Multiple collections
- `content-collections-mdx.ts` - MDX with syntax highlighting
- `tsconfig.json` - Complete TypeScript config
- `vite.config.ts` - Vite plugin setup
- `blog-post.md` - Example content file
- `BlogList.tsx` - React list component
- `BlogPost.tsx` - React MDX render component
- `wrangler.toml` - Cloudflare Workers config

### References (references/)

Deep-dive documentation for advanced topics:

- `schema-patterns.md` - Common Zod schema patterns
- `transform-cookbook.md` - Transform function recipes
- `mdx-components.md` - MDX + React integration
- `deployment-guide.md` - Cloudflare Workers setup

**When to load**: Claude should load these when you need advanced patterns beyond basic setup.

### Scripts (scripts/)

- `init-content-collections.sh` - One-command automated setup

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

## Troubleshooting

### Problem: TypeScript can't find 'content-collections'

**Solution**: Add path alias to `tsconfig.json`, restart TS server.

---

### Problem: Vite keeps restarting

**Solution**: Add `.content-collections/` to `.gitignore` and Vite watch ignore.

---

### Problem: Changes not reflecting

**Solution**: Restart dev server, verify glob pattern, check file saved.

---

### Problem: MDX compilation errors

**Solution**: Check Shiki version compatibility, verify MDX syntax.

---

### Problem: Validation errors unclear

**Solution**: Add custom error messages to Zod schema.

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

---

**Questions? Issues?**

1. Check `references/` directory for deep dives
2. Verify path alias in tsconfig.json
3. Check Vite plugin order (after react())
4. Review known issues above
5. Check official docs: https://www.content-collections.dev/docs
