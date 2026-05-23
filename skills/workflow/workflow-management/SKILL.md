---
name: workflow-management
description: Create, debug, or modify Vercel WDK workflows for data updates and social media posting in the web application. Use when adding new automated jobs, fixing workflow errors, or updating scheduling logic.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
---

# Workflow Management Skill

This skill helps you work with Vercel WDK (Workflow Development Kit) workflows in `apps/web/src/workflows/`.

## When to Use This Skill

- Adding new scheduled workflows for data fetching
- Debugging workflow execution errors
- Modifying existing workflow schedules or logic
- Integrating new data sources into the update pipeline
- Adding new social media posting workflows

## Workflow Architecture

The project uses Vercel WDK workflows with the following structure:

```
apps/web/src/workflows/
├── cars.ts              # Car registration data workflow
├── coe.ts               # COE bidding data workflow
├── deregistrations.ts   # Deregistration data workflow
├── regenerate-post.ts   # Blog post regeneration workflow
└── shared.ts            # Shared workflow steps (social media, cache)
```

## Key Patterns

### 1. Workflow Definition

Workflows are defined using Vercel WDK directives:

```typescript
import { fetch } from "workflow";

export async function carsWorkflow(payload: CarsWorkflowPayload) {
  "use workflow";

  // Enable WDK's durable fetch for AI SDK
  globalThis.fetch = fetch;

  // Step 1: Process data
  const result = await processCarsData();

  // Step 2: Revalidate cache
  await revalidateCarsCache(month, year);

  // Step 3: Generate blog post
  const post = await generateCarsPost(data, month);

  return { postId: post.postId };
}

async function processCarsData(): Promise<UpdaterResult> {
  "use step";
  // Processing logic - each step is durable and can retry
  return await updateCars();
}
```

### 2. Scheduling Workflows

Workflows are triggered via Vercel Cron schedules configured in `apps/web/vercel.json`:

```json
{
  "crons": [
    { "path": "/api/workflows/cars", "schedule": "0 10 * * *" },
    { "path": "/api/workflows/coe", "schedule": "0 10 * * *" },
    { "path": "/api/workflows/deregistrations", "schedule": "0 10 * * *" }
  ]
}
```

### 3. API Route Integration

API routes trigger workflows using WDK's `start()` function:

```typescript
import { start } from "workflow/api";
import { carsWorkflow } from "@web/workflows/cars";

export async function POST(request: Request) {
  const payload = await request.json();
  const run = await start(carsWorkflow, [payload]);
  return Response.json({ message: "Workflow started", runId: run.runId });
}
```

### 4. Shared Steps

Common operations are extracted to `shared.ts`:

```typescript
export async function publishToSocialMedia(title: string, link: string) {
  "use step";
  await socialMediaManager.publishToAll({ message: `📰 ${title}`, link });
}

export async function revalidatePostsCache() {
  "use step";
  revalidateTag("posts:list", "max");
}
```

### 5. Error Handling

Steps automatically retry on failure. For custom error handling:

```typescript
async function processData() {
  "use step";
  try {
    const result = await updateData();
    return result;
  } catch (error) {
    console.error("Step failed:", error);
    throw error; // Re-throw for automatic retry
  }
}
```

## Common Tasks

### Adding a New Workflow

1. Create workflow file in `apps/web/src/workflows/`
2. Define workflow function with `"use workflow"` directive
3. Break logic into steps using `"use step"` directive
4. Create API route in `apps/web/src/app/api/workflows/`
5. Add Vercel Cron schedule if needed in `vercel.json`
6. Add tests for workflow logic

### Debugging Workflow Failures

1. Check Vercel dashboard for workflow execution logs
2. Review function logs in Vercel
3. Verify environment variables are set correctly
4. Test workflow locally using development server
5. Check database connectivity and Redis availability

### Modifying Existing Workflows

1. Read existing workflow implementation
2. Identify which step needs modification
3. Update step logic while maintaining error handling
4. Test changes locally
5. Deploy and monitor execution

## Environment Variables

Workflows typically need:
- `DATABASE_URL` - PostgreSQL connection
- `UPSTASH_REDIS_REST_URL` / `UPSTASH_REDIS_REST_TOKEN` - Redis
- Service-specific tokens (Discord webhook, Twitter API, etc.)

## Testing Workflows

Run workflow tests:
```bash
pnpm -F @sgcarstrends/web test -- src/workflows
```

Test individual workflow locally:
```bash
# Start dev server
pnpm dev

# Trigger workflow via HTTP
curl -X POST http://localhost:3000/api/workflows/cars
```

## References

- Vercel WDK Documentation: https://vercel.com/docs/workflow-kit
- Related files:
  - `apps/web/src/app/api/workflows/` - Workflow route handlers
  - `apps/web/src/config/platforms.ts` - Social media configuration
  - `apps/web/vercel.json` - Vercel Cron schedules
  - `apps/web/CLAUDE.md` - Web application documentation

## Best Practices

1. **Idempotency**: Ensure workflows can safely retry without duplicating data
2. **Step Granularity**: Break workflows into small, focused steps with `"use step"`
3. **Durable Fetch**: Set `globalThis.fetch = fetch` for AI SDK calls
4. **Logging**: Add comprehensive logging for debugging
5. **Testing**: Write unit tests for workflow logic
6. **Monitoring**: Track workflow execution in Vercel dashboard
