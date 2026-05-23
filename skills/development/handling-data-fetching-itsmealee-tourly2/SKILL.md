---
name: handling-data-fetching
description: Strategy for fetching data using React Server Components (RSC) and managing cache. Use for initial page loads and SEO-optimized data.
---

# Data Fetching and Caching

## When to use this skill
- When building pages that need SEO (Tours, Details).
- When deciding between RSC and Client-side `useEffect`.

## Strategy
- **RSC (Default)**: Fetch data in Server Components for speed and SEO.
- **Client Fetching**: Use only for highly interactive, private, or real-time data.
- **No-store**: Use `cache: 'no-store'` or `dynamic = 'force-dynamic'` for frequently changing data (like live availability).

## Implementation (RSC)
```typescript
import { TourService } from '@/services/tours';

export default async function ToursPage() {
    const tours = await TourService.getAll();
    
    return (
        <div>
            {tours.documents.map(tour => <TourCard key={tour.$id} tour={tour} />)}
        </div>
    );
}
```

## Instructions
- **Type Safety**: Await findings and pass typed objects to child components.
- **Suspense**: Always wrap RSC data-fetching segments in `Suspense` for better UX.
