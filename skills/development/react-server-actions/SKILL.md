---
name: react-server-actions
description: Implement React Server Actions in Next.js 14+ for secure, progressively enhanced form handling and server mutations without API routes. Use when handling form submissions, performing server-side mutations, implementing progressive enhancement, creating actions that work without JavaScript, validating data on the server, revalidating cached data after mutations, handling file uploads server-side, implementing optimistic UI updates, or building forms that gracefully degrade without client-side JavaScript.
---

# React Server Actions - Form Handling

## When to use this skill

- Handling form submissions in Next.js 14+ applications
- Performing server-side data mutations without API routes
- Implementing progressive enhancement for forms
- Creating actions that work without client-side JavaScript
- Validating form data securely on the server
- Revalidating Next.js cache after data mutations
- Handling file uploads with server-side processing
- Implementing optimistic UI updates with useOptimistic
- Building accessible forms with server-first architecture
- Integrating with database operations directly
- Managing form state with useFormState hook
- Creating secure mutations with server-only code

## When to use this skill

- Implementing forms, mutations in Next.js App Router.
- When working on related tasks or features
- During development that requires this expertise

**Use when**: Implementing forms, mutations in Next.js App Router.

## Server Action
\`\`\`typescript
'use server';

export async function createPost(formData: FormData) {
  const title = formData.get('title');
  await db.post.create({ data: { title } });
  revalidatePath('/posts');
}
\`\`\`

## Resources
- [Server Actions](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations)
