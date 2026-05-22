---
name: ai-structured-output
description: Generate type-safe AI content using Gemini structured output with Zod validation and Code Execution Tool. Use when building AI generation functions that need guaranteed output format.
allowed-tools: Read, Edit, Write, Grep, Glob
---

# AI Structured Output Patterns

This skill documents patterns for generating type-safe, validated AI content using Google Gemini with Vercel AI SDK.

## When to Use This Skill

- Generating structured content (blog posts, reports, summaries) with guaranteed format
- Need type-safe LLM output with TypeScript inference
- Preventing hallucinations in data analysis through code execution
- Creating reusable AI generation functions for workflows
- Building multi-step AI pipelines with separate analysis and generation phases

## Architecture Overview

The recommended architecture uses a **2-step generation flow**:

```
Step 1: Analysis (Accuracy)          Step 2: Structured Output (Presentation)
┌─────────────────────────────┐     ┌─────────────────────────────┐
│ generateText()              │     │ generateObject()            │
│ + Code Execution Tool       │ ──▶ │ + Zod Schema               │
│ + Extended Thinking         │     │ + Field Descriptions        │
│ = Accurate calculations     │     │ = Type-safe output          │
└─────────────────────────────┘     └─────────────────────────────┘
```

**Why 2 steps?**
- Step 1 focuses on **accuracy**: Code execution prevents calculation errors
- Step 2 focuses on **format**: Zod schema ensures consistent structure
- Separation allows optimisation: extended thinking only where needed

## 2-Step Generation Implementation

### Complete Example

```typescript
import { google } from "@ai-sdk/google";
import { generateText, generateObject } from "ai";
import { z } from "zod";

// Define output schema with field descriptions
const outputSchema = z.object({
  title: z.string().max(100).describe("SEO-optimised title, max 60 chars preferred"),
  excerpt: z.string().max(500).describe("2-3 sentence summary for meta description"),
  content: z.string().describe("Full markdown content without H1 title"),
  tags: z.array(z.string()).min(1).max(10).describe("3-5 category tags in Title Case"),
  highlights: z.array(z.object({
    value: z.string().describe('Metric value, e.g. "52.60%", "$125,000"'),
    label: z.string().describe('Short label, e.g. "Electric Vehicles Lead"'),
    detail: z.string().describe('Context, e.g. "2,081 units registered"'),
  })).min(3).max(10).describe("3-6 key statistics for visual display"),
});

type GeneratedOutput = z.infer<typeof outputSchema>;

export async function generate2Step(data: string): Promise<GeneratedOutput> {
  // STEP 1: Analysis with Code Execution
  const analysisResult = await generateText({
    model: google("gemini-2.5-flash"),
    system: ANALYSIS_INSTRUCTIONS,
    tools: { code_execution: google.tools.codeExecution({}) },
    prompt: `Analyse this data:\n${data}\n\nProvide detailed analysis with accurate calculations.`,
    providerOptions: {
      google: {
        thinkingConfig: {
          thinkingBudget: -1,  // Unlimited thinking for complex analysis
        },
      },
    },
  });

  // STEP 2: Structured Output Generation
  const { object } = await generateObject({
    model: google("gemini-2.5-flash"),
    schema: outputSchema,
    system: GENERATION_INSTRUCTIONS,
    prompt: `Based on this analysis:\n\n${analysisResult.text}\n\nGenerate the structured output.`,
  });

  return object;  // Fully typed!
}
```

## Code Execution Tool

The Code Execution Tool is **critical** for preventing hallucinations in data analysis.

### Configuration

```typescript
tools: { code_execution: google.tools.codeExecution({}) }
```

### Why It Matters

| Without Code Execution | With Code Execution |
|------------------------|---------------------|
| LLM guesses calculations | Python executes actual math |
| Plausible but wrong numbers | Verified accurate results |
| Cannot validate data | Can parse and validate input |
| Unreliable for financial data | Safe for market analysis |

### When to Use

- **Always use** for: calculations, aggregations, percentages, comparisons
- **Skip** for: creative writing, summaries, opinion pieces
- **Use in Step 1 only**: Code execution is for analysis, not generation

### Example: Data Analysis with Code Execution

```typescript
const analysisResult = await generateText({
  model: google("gemini-2.5-flash"),
  tools: { code_execution: google.tools.codeExecution({}) },
  system: `You are a data analyst. Use Python code execution for ALL calculations.
Never estimate or guess numbers. Execute code to:
- Parse the input data
- Calculate totals and percentages
- Compare values and trends
- Validate data consistency`,
  prompt: `Analyse this sales data:\n${pipeDelimitedData}`,
});
```

## Extended Thinking Configuration

Extended thinking improves analysis quality but increases latency. Use selectively.

### Configuration

```typescript
providerOptions: {
  google: {
    thinkingConfig: {
      thinkingBudget: -1,  // -1 = unlimited, or set specific token budget
    },
  },
}
```

### When to Use

| Step | Extended Thinking | Reason |
|------|-------------------|--------|
| Analysis (Step 1) | YES | Complex reasoning, data patterns |
| Generation (Step 2) | NO | Speed matters, schema guides output |

### Example: Selective Extended Thinking

```typescript
// Step 1: WITH extended thinking (complex analysis)
const analysis = await generateText({
  model: google("gemini-2.5-flash"),
  tools: { code_execution: google.tools.codeExecution({}) },
  providerOptions: {
    google: {
      thinkingConfig: { thinkingBudget: -1 },
    },
  },
  prompt: analysisPrompt,
});

// Step 2: WITHOUT extended thinking (faster generation)
const { object } = await generateObject({
  model: google("gemini-2.5-flash"),
  schema: outputSchema,
  prompt: generationPrompt,
  // No thinkingConfig = faster response
});
```

## Zod Schema Design Patterns

### Field Descriptions

Use `.describe()` to guide LLM output:

```typescript
const schema = z.object({
  // Constraints + description = better output
  title: z.string()
    .max(100)
    .describe("SEO title, max 60 chars preferred, include main keyword"),

  // Array bounds prevent over/under generation
  tags: z.array(z.string())
    .min(3)
    .max(5)
    .describe("Category tags in Title Case, first tag is primary category"),

  // Nested objects with descriptions
  author: z.object({
    name: z.string().describe("Full name"),
    role: z.string().describe("Job title or role"),
  }).describe("Content author information"),
});
```

### Type Inference

```typescript
// Infer TypeScript type from schema
type Output = z.infer<typeof schema>;

// Use in function signatures
async function generate(): Promise<Output> {
  const { object } = await generateObject({
    model: google("gemini-2.5-flash"),
    schema,
    prompt: "...",
  });
  return object;  // Typed as Output
}
```

### Common Patterns

```typescript
// Optional fields with defaults
z.string().optional().default("Unknown")

// Enum-like constraints
z.enum(["draft", "published", "archived"])

// Numeric constraints
z.number().min(0).max(100).describe("Percentage value 0-100")

// Date strings
z.string().describe("ISO 8601 date string, e.g. 2024-01-15")

// Markdown content
z.string().describe("Markdown formatted content, use ## for sections")
```

## Tag Constants Pattern

Use controlled vocabulary for consistent categorisation:

```typescript
// Define constants with as const
export const CATEGORY_TAGS = [
  "Technology",
  "Business",
  "Finance",
  "Market Analysis",
  "Monthly Update",
] as const;

// Extract type from constants
export type CategoryTag = (typeof CATEGORY_TAGS)[number];

// Use in schema
const schema = z.object({
  tags: z.array(z.enum(CATEGORY_TAGS))
    .min(1)
    .max(5)
    .describe("Select from predefined categories"),
});
```

### Multiple Category Sets

```typescript
export const CARS_TAGS = [
  "Cars", "Registrations", "Fuel Types", "Vehicle Types",
  "Monthly Update", "New Registration", "Market Trends",
] as const;

export const COE_TAGS = [
  "COE", "Quota Premium", "1st Bidding Round", "2nd Bidding Round",
  "Monthly Update", "PQP",
] as const;

// Type union
export type DataTag = (typeof CARS_TAGS)[number] | (typeof COE_TAGS)[number];
```

## System Instruction Separation

Separate instructions for analysis vs generation:

```typescript
// Analysis instructions focus on accuracy
const ANALYSIS_INSTRUCTIONS = `You are a data analyst.
Use Python code execution for ALL calculations.
Never estimate or guess numbers.

Required analysis:
1. Parse the pipe-delimited input data
2. Calculate totals, percentages, and changes
3. Identify top performers and trends
4. Compare with previous periods if available

Output: Detailed analysis with verified numbers.`;

// Generation instructions focus on format
const GENERATION_INSTRUCTIONS = `You are a content writer.
Transform the analysis into structured output.

Requirements:
- Title: SEO-optimised, max 60 characters
- Excerpt: 2-3 sentences, under 300 characters
- Content: Markdown without H1, 500-700 words
- Tags: 3-5 from the allowed vocabulary
- Highlights: 3-6 key statistics with value/label/detail

Tone: Professional, accessible, data-driven.`;
```

## Telemetry Integration

Track generation performance with Langfuse:

```typescript
import { generateText, generateObject } from "ai";

// Step 1: Analysis telemetry
const analysisResult = await generateText({
  model: google("gemini-2.5-flash"),
  tools: { code_execution: google.tools.codeExecution({}) },
  prompt: analysisPrompt,
  experimental_telemetry: {
    isEnabled: true,
    functionId: "content-analysis/cars",
    metadata: {
      step: "analysis",
      dataType: "cars",
      month: "2024-01",
      tags: ["cars", "2024-01", "analysis"],
    },
  },
});

// Step 2: Generation telemetry
const { object } = await generateObject({
  model: google("gemini-2.5-flash"),
  schema: outputSchema,
  prompt: generationPrompt,
  experimental_telemetry: {
    isEnabled: true,
    functionId: "content-generation/cars",
    metadata: {
      step: "generation",
      dataType: "cars",
      month: "2024-01",
      tags: ["cars", "2024-01", "generation"],
    },
  },
});
```

### Langfuse Setup

```typescript
// instrumentation.ts
import { registerOTel } from "@vercel/otel";
import { LangfuseExporter } from "@langfuse/otel";

export function startTracing() {
  registerOTel({
    serviceName: "ai-generation",
    traceExporter: new LangfuseExporter({
      publicKey: process.env.LANGFUSE_PUBLIC_KEY,
      secretKey: process.env.LANGFUSE_SECRET_KEY,
      baseUrl: process.env.LANGFUSE_HOST,
    }),
  });
}

export async function shutdownTracing() {
  // Flush pending traces before exit
  await new Promise((resolve) => setTimeout(resolve, 1000));
}
```

## Function Patterns

### Standalone Function (No Workflow)

```typescript
export interface GenerateParams {
  data: string;
  month: string;
  dataType: "cars" | "coe";
}

export interface GenerateResult {
  object: GeneratedOutput;
  usage: { inputTokens: number; outputTokens: number; totalTokens: number };
  response: { id: string; modelId: string; timestamp: Date };
}

export async function generateContent(
  params: GenerateParams
): Promise<GenerateResult> {
  startTracing();

  try {
    // Step 1: Analysis
    const analysis = await generateText({ /* ... */ });

    // Step 2: Generation
    const { object, usage, response } = await generateObject({ /* ... */ });

    return { object, usage, response };
  } finally {
    await shutdownTracing();
  }
}
```

### Workflow-Aware Wrapper

```typescript
import type { WorkflowContext } from "@upstash/workflow";

export async function generateInWorkflow(
  context: WorkflowContext,
  params: GenerateParams
): Promise<GenerateResult> {
  // Use workflow context for step orchestration
  const result = await context.run("generate-content", async () => {
    return generateContent(params);
  });

  // Additional workflow steps
  await context.run("save-to-database", async () => {
    await saveToDatabase(result);
  });

  await context.run("invalidate-cache", async () => {
    await revalidateTag("content:list");
  });

  return result;
}
```

## Error Handling

```typescript
import { APIError } from "@ai-sdk/google";

export async function generateWithRetry(
  params: GenerateParams,
  maxRetries = 3
): Promise<GenerateResult> {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await generateContent(params);
    } catch (error) {
      if (error instanceof APIError) {
        // Handle rate limits
        if (error.status === 429 && attempt < maxRetries) {
          await new Promise(r => setTimeout(r, 2000 * attempt));
          continue;
        }
        // Handle quota exceeded
        if (error.status === 403) {
          throw new Error("API quota exceeded. Check billing.");
        }
      }
      throw error;
    }
  }
  throw new Error("Max retries exceeded");
}
```

## Environment Variables

Required:
```bash
GOOGLE_GENERATIVE_AI_API_KEY=...  # Google AI API key
```

Optional (for telemetry):
```bash
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

## Best Practices

1. **Always use 2-step flow** for data-driven content
2. **Use Code Execution Tool** for any calculations
3. **Enable extended thinking** for analysis step only
4. **Add .describe()** to all schema fields
5. **Use tag constants** for controlled vocabulary
6. **Separate instructions** for analysis vs generation
7. **Enable telemetry** from the start
8. **Handle errors** with retries for rate limits

## Related Skills

- `gemini-blog` - Blog-specific generation patterns
- `schema-design` - Database schema for persisting generated content
- `workflow-management` - QStash workflow integration
- `redis-cache` - Caching generated content

## Reference Files

- `packages/ai/src/generate-post.ts` - 2-step flow implementation
- `packages/ai/src/schemas.ts` - Zod schema patterns
- `packages/ai/src/tags.ts` - Tag constants
- `packages/ai/src/config.ts` - System instructions
- `packages/ai/src/instrumentation.ts` - Langfuse setup
