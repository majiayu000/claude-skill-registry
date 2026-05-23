---
name: gemini-blog
description: Configure or debug LLM blog post generation using Vercel AI SDK and Google Gemini. Use when updating blog generation prompts, fixing AI integration issues, modifying content generation logic, or working with structured output schemas.
allowed-tools: Read, Edit, Grep, Glob, Bash
---

# Gemini Blog Generation Skill

Blog generation package: `packages/ai/`

## Architecture

```
packages/ai/
├── src/
│   ├── generate-post.ts    # 2-step generation (analysis → structured output)
│   ├── config.ts           # System instructions
│   ├── schemas.ts          # Zod schemas (postSchema, highlightSchema)
│   ├── tags.ts             # Tag constants (CARS_TAGS, COE_TAGS)
│   ├── hero-images.ts      # Hero image URLs
│   └── save-post.ts        # Post persistence with idempotency
```

### 2-Step Flow

1. **Step 1 (Analysis)**: `generateText()` + Code Execution Tool + Extended Thinking → Accurate calculations
2. **Step 2 (Generation)**: `generateObject()` + Zod schema → Type-safe structured output

## Key Functions

```typescript
// Standalone generation
import { generateBlogContent } from "@sgcarstrends/ai";

const { object } = await generateBlogContent({
  data: tokenisedData,     // Pipe-delimited data
  month: "October 2024",
  dataType: "cars",        // "cars" or "coe"
});

// object.title, object.excerpt, object.content, object.tags, object.highlights
```

## Schemas

```typescript
// postSchema
z.object({
  title: z.string().max(100),              // SEO title, max 60 chars preferred
  excerpt: z.string().max(500),            // Meta description, under 300 chars
  content: z.string(),                     // Markdown (no H1)
  tags: z.array(z.string()).min(1).max(10), // 3-5 tags, first is dataType
  highlights: z.array(highlightSchema),    // 3-6 key statistics
});

// highlightSchema
z.object({
  value: z.string(),   // "52.60%", "$125,000"
  label: z.string(),   // "Electric Vehicles Lead"
  detail: z.string(),  // "2,081 units registered"
});
```

## Tag Constants

```typescript
export const CARS_TAGS = ["Cars", "Registrations", "Fuel Types", "Market Trends", ...] as const;
export const COE_TAGS = ["COE", "Quota Premium", "1st Bidding Round", "PQP", ...] as const;
```

## Updating Prompts

Edit `packages/ai/src/config.ts`:
- `ANALYSIS_INSTRUCTIONS`: For calculation logic
- `GENERATION_INSTRUCTIONS`: For output format

## Debugging

**Low Quality Output:** Check Step 1 analysis logs, verify Code Execution Tool runs Python
**Schema Validation Errors:** Check Zod constraints (max lengths, array bounds)
**API Errors:** Verify `GOOGLE_GENERATIVE_AI_API_KEY`, check quota

## Environment Variables

```env
GOOGLE_GENERATIVE_AI_API_KEY=...    # Required
LANGFUSE_PUBLIC_KEY=pk-lf-...       # Optional telemetry
LANGFUSE_SECRET_KEY=sk-lf-...
```

## Best Practices

1. **Always use 2-step flow**: Separate analysis from generation
2. **Never skip Code Execution**: Required for accurate calculations
3. **Use tag constants**: Maintain vocabulary consistency
4. **Enable telemetry**: Track costs and quality

## References

- `packages/ai/CLAUDE.md` for full package documentation
- Vercel AI SDK: Use Context7 for latest docs
