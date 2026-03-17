---
name: managing-content
description: Integrates Headless CMS (Sanity, Strapi, Contentful) to manage dynamic content. Generates schemas, connects APIs, and builds type-safe frontend fetchers.
---

# Content Manager (CMS)

## When to use this skill
- When the user needs a "Blog", "Portfolio", "E-commerce Product List", or "Team Page".
- When the user asks to "connect Sanity/Strapi".
- When content needs to be editable by non-developers.

## Workflow
1.  **Selection**: Choose the CMS logic.
    - **Sanity.io**: (Cloud) Real-time, multi-user, hosted. Best for teams/rich-text heavy sites.
    - **Keystatic**: (Local) Git-based. Free, simple, no-hosting. Best for solo devs.
    - **Custom Firebase**: (DIY) Build your own Admin Panel on Firestore. Best if you want 100% UI control and already use Firebase Auth.
2.  **Modeling**: Define the content structure.
    - *Keystatic*: `keystatic.config.ts`.
    - *Sanity*: `sanity/schemaTypes`.
    - *Firebase*: Define TypeScript Interfaces models (e.g., `interface Post { ... }`).
3.  **Integration**:
    - *Firebase*: Use `getDocs(collection(db, "posts"))`.

## Instructions

### 1. The Local Route (Keystatic)
Perfect for "Hardcoded but Editable".
1.  **Setup**: Install `@keystatic/core` and `@keystatic/next`.
2.  **Config**: Create `keystatic.config.ts`.
    ```typescript
    export default config({
      storage: { kind: 'local' },
      collections: {
        posts: collection({
          label: 'Posts',
          slugField: 'title',
          schema: {
            title: fields.slug({ name: { label: 'Title' } }),
            content: fields.document({ label: 'Content' }),
          },
          path: 'content/posts/*',
        }),
      },
    });
    ```

### 2. The Cloud Route (Sanity)
Always separate schemas into small files in `sanity/schemaTypes/`.

### 3. The DIY Route (Firebase)
Use the `managing-databases` skill to build the Admin Dashboard.
- **Auth**: Restrict `/admin` to your `uid`.
- **Storage**: Use Firebase Storage for image uploads.
- **Rich Text**: You must install a library like Tiptap or Quill manually.
```javascript
// post.ts
export default {
  name: 'post',
  type: 'document',
  fields: [
    { name: 'title', type: 'string' },
    { name: 'image', type: 'image' }
  ]
}
```

### 2. The Fetching Layer
Create a `lib/sanity.ts` or `services/cms.ts`.
- **Type Safety**: Use tools like `sanity-typegen` to ensure TypeScript knows your schema.
- **Caching**: Use `fetch(url, { next: { revalidate: 60 } })` for ISR.

### 3. Rich Text Rendering
Never dump raw HTML. Use `PortableText` (Sanity) or `ReactMarkdown` to render safe, styled content.

## Self-Correction Checklist
- "Did I add the API keys to `.env`?" -> Never hardcode tokens.
- "Is the dataset public or private?" -> specific read settings.
