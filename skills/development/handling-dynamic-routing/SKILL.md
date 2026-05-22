---
name: handling-dynamic-routing
description: Logic for Next.js 15 Dynamic Routes. Use when building pages like `tours/[id]`.
---

# Dynamic Routing Patterns

## When to use this skill
- Creating pages that depend on a parameter (slug, ID).
- Handling `params` in Next.js 15 Server Components.

## Workflow (Next.js 15)
- [ ] Define the folder: `app/tours/[id]/page.tsx`.
- [ ] Access `params` as a **Promise** (required in v15).
- [ ] Fetch data based on the resolved `id`.

## Implementation
```typescript
interface TourPageProps {
    params: Promise<{ id: string }>;
}

export default async function TourDetailsPage({ params }: TourPageProps) {
    const { id } = await params; // Await the promise
    const tour = await TourService.getById(id);
    
    return (
        <main>
            <h1>{tour.title}</h1>
            {/* ... */}
        </main>
    );
}
```

## Instructions
- **Metadata**: Await `params` in `generateMetadata` as well.
- **Loading**: Use `loading.tsx` in the directory for automatic fallback UI.
