---
name: generate-api-route
description: Generate Next.js API route handler with repository integration, error handling, and TypeScript types. Use when creating new API endpoints for meals, supplements, profile, analytics, or other resources.
allowed-tools: Read, Write, Glob, Grep
---

# Generate API Route

Generate a complete Next.js App Router API endpoint following Health Tracker 9000 patterns.

## Usage

When user requests to create a new API endpoint, ask for:

1. **Resource name** (e.g., "water-intake", "sleep-log", "weight-tracking")
2. **HTTP methods needed** (GET, POST, DELETE, PUT, etc.)
3. **Whether daily summary recalculation is needed** (yes for health data, no for reference data)
4. **Special validation** or business logic needed

## Implementation Pattern

Based on `src/app/api/meals/route.ts` pattern.

### File Structure

Create file: `src/app/api/{resource-name}/route.ts`

```typescript
import { NextResponse } from 'next/server';
import { ResourceRepository } from '@/lib/database/repositories/resourceRepository';
import { DailySummaryRepository } from '@/lib/database/repositories/dailySummaryRepository';
import { ProfileRepository } from '@/lib/database/repositories/profileRepository';
import { calculateHealthScore } from '@/lib/utils/healthScoring';
import { getDatabase } from '@/lib/database/connection';

export async function POST(request: Request) {
  const resourceRepo = new ResourceRepository();
  const summaryRepo = new DailySummaryRepository();

  try {
    const body = await request.json();
    const { date, ...otherFields } = body;

    const newRecord = resourceRepo.addResource({
      date,
      ...otherFields,
    });

    // Update daily summary if this is health-related data
    const summary = await summaryRepo.getDailySummary(date);
    if (summary) {
      const profileRepo = new ProfileRepository();
      const targets = profileRepo.calculateNutritionalTargets();

      const records = resourceRepo.getResourcesByDate(date);
      const dailyTotals = summaryRepo.calculateDailyTotals(records, summary.supplements);

      const scoreBreakdown = calculateHealthScore(dailyTotals, targets, {
        ...summary,
        records,
        totalNutrition: dailyTotals,
      });

      summaryRepo.saveDailySummary({
        date,
        totalNutrition: dailyTotals,
        healthScore: scoreBreakdown.total,
      });
    }

    return NextResponse.json(newRecord);
  } catch (error: any) {
    console.error('API Error:', error);
    return NextResponse.json({ error: error.message || 'Internal Server Error' }, { status: 500 });
  }
}

export async function DELETE(request: Request) {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');

  if (!id) return NextResponse.json({ error: 'ID required' }, { status: 400 });

  const resourceRepo = new ResourceRepository();
  const summaryRepo = new DailySummaryRepository();

  try {
    // Get date before deleting to update summary
    const stmt = getDatabase().prepare('SELECT date FROM table_name WHERE id = ?');
    const row = stmt.get(id) as any;
    const date = row?.date;

    resourceRepo.deleteResource(id);

    if (date) {
      const summary = await summaryRepo.getDailySummary(date);
      if (summary) {
        const profileRepo = new ProfileRepository();
        const targets = profileRepo.calculateNutritionalTargets();

        const records = resourceRepo.getResourcesByDate(date);
        const dailyTotals = summaryRepo.calculateDailyTotals(records, summary.supplements);

        const scoreBreakdown = calculateHealthScore(dailyTotals, targets, {
          ...summary,
          records,
          totalNutrition: dailyTotals,
        });

        summaryRepo.saveDailySummary({
          date,
          totalNutrition: dailyTotals,
          healthScore: scoreBreakdown.total,
        });
      }
    }

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}
```

## Key Conventions

- Use `NextResponse.json()` for all responses
- Always include try-catch with `console.error('API Error:', error)`
- Return proper HTTP status codes (400 for bad request, 500 for errors)
- Repository instances created at top of each handler
- Daily summary updates for date-based health data only
- DELETE endpoint should get date before deleting to update summary
- Use `getDatabase().prepare()` for raw SQL when needed

## Steps

1. Ask user for resource name, HTTP methods, and whether daily summary recalculation needed
2. Create directory: `src/app/api/{resource-name}/`
3. Create file: `route.ts` in that directory
4. Generate imports based on methods needed
5. Generate handlers for requested HTTP methods
6. Add daily summary recalculation if health-related data
7. Format with Prettier (project uses Prettier)

## Implementation Checklist

- [ ] Resource repository imported correctly
- [ ] Error handling with try-catch wrapper
- [ ] Daily summary updated (if applicable)
- [ ] Proper HTTP status codes
- [ ] ID validation in DELETE
- [ ] JSON response formatting
