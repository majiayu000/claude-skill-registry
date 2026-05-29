---
name: logo-management
description: Manage car logo fetching, scraping, and Vercel Blob storage in the logos package. Use when adding new car brand logos, updating logo sources, debugging brand name normalization, managing Vercel Blob storage, or optimizing logo caching.
allowed-tools: Read, Edit, Bash, Grep, Glob
---

# Logo Management Skill

Logo package lives in `packages/logos/`.

```
packages/logos/
├── src/
│   ├── services/logo/     # fetch.ts, list.ts, download.ts
│   ├── infra/storage/     # Vercel Blob service
│   └── utils/normalize.ts # Brand name normalization
└── scripts/               # fetch-logos.ts, upload-to-blob.ts
```

## Brand Name Normalization

```typescript
// packages/logos/src/utils/normalize.ts
export function normalizeBrandName(brand: string): string {
  return brand.toLowerCase().trim()
    .replace(/\s+/g, "-")        // Spaces → hyphens
    .replace(/[^a-z0-9-]/g, "")  // Remove special chars
    .replace(/-+/g, "-");        // Dedupe hyphens
}

// Brand aliases for common variations
const BRAND_ALIASES: Record<string, string> = {
  "mercedes": "mercedes-benz",
  "vw": "volkswagen",
  "landrover": "land-rover",
};
```

## Logo Fetching

```typescript
// packages/logos/src/services/logo/fetch.ts
export async function getLogoUrl(brand: string): Promise<string | null> {
  const normalizedBrand = normalizeBrandName(brand);
  const cacheKey = `logo:url:${normalizedBrand}`;

  // Check Redis cache
  const cached = await redis.get<string>(cacheKey);
  if (cached) return cached;

  // Try different extensions
  for (const ext of ["svg", "png", "jpg"]) {
    const url = `${LOGO_CDN_BASE}/${normalizedBrand}.${ext}`;
    const response = await fetch(url, { method: "HEAD" });
    if (response.ok) {
      await redis.set(cacheKey, url, { ex: 7 * 24 * 60 * 60 });
      return url;
    }
  }
  return null;
}
```

## Vercel Blob Storage

```typescript
// packages/logos/src/infra/storage/blob.ts
import { put, list, del } from "@vercel/blob";

export class LogoBlobService {
  async upload(brand: string, file: Buffer): Promise<string> {
    const fileName = `logos/${normalizeBrandName(brand)}.png`;
    const blob = await put(fileName, file, { access: "public", addRandomSuffix: false });
    await redis.set(`logo:blob:${normalizeBrandName(brand)}`, blob.url, { ex: 7 * 24 * 60 * 60 });
    return blob.url;
  }

  async list(): Promise<string[]> {
    const { blobs } = await list({ prefix: "logos" });
    return blobs.map(blob => blob.url);
  }

  async delete(brand: string): Promise<void> {
    await del(`logos/${normalizeBrandName(brand)}.png`);
    await redis.del(`logo:blob:${normalizeBrandName(brand)}`);
  }
}
```

## Scripts

```bash
# Fetch logos from CDN
pnpm -F @sgcarstrends/logos fetch-logos

# Scrape logos from websites
pnpm -F @sgcarstrends/logos scrape-logos
```

## Usage in Apps

```typescript
// API route
import { getLogoUrl } from "@sgcarstrends/logos";

app.get("/logos/:brand", async (c) => {
  const logoUrl = await getLogoUrl(c.req.param("brand"));
  if (!logoUrl) return c.json({ error: "Logo not found" }, 404);
  return c.json({ logoUrl });
});

// React component
<Image src={logoUrl || "/images/logo-placeholder.png"} alt={`${brand} logo`} width={64} height={64} />
```

## Environment Variables

```env
BLOB_READ_WRITE_TOKEN=vercel_blob_token_here
```

## Best Practices

1. **Normalize Names**: Always normalize brand names before lookup
2. **Cache Aggressively**: Use multi-layer caching (memory → Redis → Blob)
3. **Fallbacks**: Provide placeholder for missing logos
4. **Batch Operations**: Use batch uploads for multiple logos

## References

- Vercel Blob: Use Context7 for latest docs
- `packages/logos/CLAUDE.md` for package details
