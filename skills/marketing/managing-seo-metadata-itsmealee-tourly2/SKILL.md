---
name: managing-seo-metadata
description: Strategies for dynamic SEO using Next.js Metadata API. Use to generate social share cards and search-engine-friendly titles for tours.
---

# SEO and Metadata Strategy

## When to use this skill
- Any page intended for public discovery (Tours, Destinations, Blog).
- Creating dynamic OpenGraph (OG) images for social media sharing.

## Workflow
- [ ] Use `export const metadata` for static pages.
- [ ] Use `export async function generateMetadata` for dynamic routes (`tours/[id]`).
- [ ] Fetch the tour data inside `generateMetadata` to populate tags.

## Example (Dynamic Metadata)
```typescript
export async function generateMetadata({ params }): Promise<Metadata> {
    const { id } = await params;
    const tour = await TourService.getById(id);

    return {
        title: `${tour.title} | Tourly`,
        description: tour.description.substring(0, 160),
        openGraph: {
            images: [tour.images[0]],
        },
    };
}
```

## Instructions
- **Memoization**: Next.js automatically deduplicates fetch requests between `generateMetadata` and your Page component.
- **Defaults**: Set a global `title.template` in `root layout.tsx` (e.g., `%s | Tourly`).
- **Canonical**: Always include `canonical` URLs to prevent duplicate content issues.
