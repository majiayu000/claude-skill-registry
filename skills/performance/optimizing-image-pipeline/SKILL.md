---
name: optimizing-image-pipeline
description: Advanced strategies for fast-loading images using next/image and Appwrite previews. Use to implement blur placeholders and avoid layout shifts.
---

# Image Optimization Pipeline

## When to use this skill
- Displaying large tour galleries.
- Implementing "Blur-up" loading effects for a premium feel.
- Reducing bandwidth usage on mobile.

## Workflow
- [ ] Use `next/image` for all non-decorative images.
- [ ] For Appwrite images, use `placeholder="blur"` and provide a `blurDataURL`.
- [ ] Use Appwrite's Preview API (`/storage/buckets/[ID]/files/[ID]/preview`) to request specific widths.

## Implementation Guide
```tsx
import Image from 'next/image';

export function TourImage({ fileId, alt }: { fileId: string, alt: string }) {
    const src = `https://cloud.appwrite.io/v1/storage/buckets/tours/files/${fileId}/preview?project=YOUR_ID&width=800`;
    
    return (
        <Image
            src={src}
            alt={alt}
            width={800}
            height={600}
            placeholder="blur"
            blurDataURL="data:image/png;base64,..." // Generate with a tool or placeholder lib
            className="rounded-xl object-cover"
        />
    );
}
```

## Instructions
- **Priority**: Add the `priority` attribute to images "above the fold" (e.g., Hero image).
- **Quality**: Use `quality={75}` or higher for travel photos to maintain clarity.
- **Placeholders**: Use a solid color or a generated blur hash for a better UX.
