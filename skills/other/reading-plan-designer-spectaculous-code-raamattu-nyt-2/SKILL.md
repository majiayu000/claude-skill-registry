---
name: reading-plan-designer
description: |
  Design and implement Bible reading plans for the KR92 Bible Voice project.

  Use when:
  - Creating new reading plans (7-day, 30-day, yearly)
  - Adding daily readings to existing plans
  - Generating reading plan SQL migrations
  - Understanding the reading plan data model
  - Designing reading sequences (chronological, topical, book-based)
  - Validating reading reference formats

  Triggers: "reading plan", "lukusuunnitelma", "daily readings", "create plan", "add readings"
---

# Reading Plan Designer

Design Bible reading plans with proper data structure and daily reading assignments.

## CRITICAL: bible_schema Usage

**All reading plan tables and RPC functions reside in `bible_schema`, NOT `public`.**

### Supabase Client Queries

```typescript
// WRONG - looks in public schema, will fail
const { data } = await supabase.rpc("get_user_reading_plans", { ... });

// CORRECT - explicitly specify bible_schema
const { data } = await (supabase as any)
  .schema("bible_schema")
  .rpc("get_user_reading_plans", { ... });

// WRONG - table query without schema
const { data } = await supabase.from("reading_plans").select("*");

// CORRECT - with schema prefix
const { data } = await (supabase as any)
  .schema("bible_schema")
  .from("reading_plans")
  .select("*");
```

### SQL Migrations

Always prefix table names with `bible_schema.` in migrations:

```sql
-- WRONG
INSERT INTO reading_plans ...

-- CORRECT
INSERT INTO bible_schema.reading_plans ...
```

## Context Files (Read First)

- `Docs/context/db-schema-short.md` - Database tables overview
- `Docs/context/supabase-map.md` - RPC functions for reading plans

## Quick Start: Generate a Plan

Use the bundled script to auto-generate plans with SQL migrations:

```bash
# Single book plan
python scripts/fetch_reading_plan.py --generate --book John --days 21 --sql -o john.json

# New Testament in 90 days
python scripts/fetch_reading_plan.py --generate --sections NT --days 90 --sql -o nt90.json

# Full Bible in 365 days
python scripts/fetch_reading_plan.py --generate --sections OT+NT --days 365 --sql -o yearly.json

# Psalms in 30 days
python scripts/fetch_reading_plan.py --generate --book Psalms --days 30 --sql -o psalms30.json
```

The script outputs:
- JSON file with plan structure
- SQL migration file (with `--sql` flag)
- Summary with day count and reading blocks

## Database Schema

### reading_plans (bible_schema)
```sql
id UUID PRIMARY KEY
slug TEXT UNIQUE           -- URL-friendly identifier
name_fi TEXT NOT NULL      -- Finnish name
name_en TEXT               -- English name (optional)
description_fi TEXT        -- Finnish description
duration_days INTEGER      -- Total days in plan
is_active BOOLEAN          -- Show to users
sort_order INTEGER         -- Display order
```

### reading_plan_days (bible_schema)
```sql
id UUID PRIMARY KEY
plan_id UUID REFERENCES reading_plans(id)
day_number INTEGER         -- Day 1, 2, 3...
title TEXT                 -- Optional day title
readings JSONB             -- Array of ReadingReference
```

### ReadingReference Format (JSONB)
```typescript
interface ReadingReference {
  book: string;           // Finnish abbreviation: "Matt", "1. Moos", "Ps"
  chapter_start: number;  // Starting chapter
  chapter_end?: number;   // For chapter ranges (optional)
  verse_start?: number;   // Starting verse (optional, full chapter if omitted)
  verse_end?: number;     // Ending verse (optional)
}
```

## Manual Plan Creation

### Step 1: Create Plan

```sql
INSERT INTO bible_schema.reading_plans (
  id, slug, name_fi, name_en, description_fi, duration_days, is_active, sort_order
) VALUES (
  gen_random_uuid(),
  'gospel-of-john',
  'Johanneksen evankeliumi',
  'Gospel of John',
  'Lue Johanneksen evankeliumi 21 päivässä',
  21,
  true,
  10
);
```

### Step 2: Add Daily Readings

```sql
WITH plan AS (
  SELECT id FROM bible_schema.reading_plans WHERE slug = 'gospel-of-john'
)
INSERT INTO bible_schema.reading_plan_days (id, plan_id, day_number, title, readings)
SELECT gen_random_uuid(), plan.id, day_num, title, readings::jsonb
FROM plan, (VALUES
  (1, 'Sana tuli lihaksi', '[{"book": "Joh", "chapter_start": 1}]'),
  (2, 'Kaanan häät', '[{"book": "Joh", "chapter_start": 2}]'),
  (3, 'Nikodemos', '[{"book": "Joh", "chapter_start": 3}]')
  -- Continue for all days...
) AS days(day_num, title, readings);
```

## Reading Reference Examples

| Type | JSON | Result |
|------|------|--------|
| Single verse | `{"book": "Joh", "chapter_start": 3, "verse_start": 16, "verse_end": 16}` | John 3:16 |
| Verse range | `{"book": "Matt", "chapter_start": 5, "verse_start": 3, "verse_end": 12}` | Matthew 5:3-12 |
| Full chapter | `{"book": "Ps", "chapter_start": 23}` | Psalm 23 |
| Chapter range | `{"book": "1. Moos", "chapter_start": 1, "chapter_end": 3}` | Genesis 1-3 |

## Book Abbreviations

Common Finnish abbreviations:

| Book | Abbrev | | Book | Abbrev |
|------|--------|-|------|--------|
| Genesis | 1. Moos | | Matthew | Matt |
| Exodus | 2. Moos | | Mark | Mark |
| Psalms | Ps | | Luke | Luuk |
| Proverbs | Sananl | | John | Joh |
| Isaiah | Jes | | Acts | Ap. t. |
| Jeremiah | Jer | | Romans | Room |
| Daniel | Dan | | Revelation | Ilm |

Query all: `SELECT abbreviation_fi, name_fi FROM bible_schema.books`

## Reading Plan Patterns

| Pattern | Days | Focus | Example |
|---------|------|-------|---------|
| Topical Week | 7 | Theme passages | "Armon viikko" |
| Book Study | 21-30 | Single book | "Johanneksen evankeliumi" |
| Section | 90 | NT or OT | "Uusi testamentti" |
| Full Bible | 365 | Complete | "Raamattu vuodessa" |

## Frontend Integration

### Pages & Components

| Component | Location | Purpose |
|-----------|----------|---------|
| `ReadingPlansPage` | `pages/ReadingPlansPage.tsx` | Browse and join plans, tabs for active/completed |
| `ReadingPlanCard` | `components/reading-plans/` | Plan card with today's readings, quit button |
| `DailyReadingView` | `components/reading-plans/` | Day view with verses, nav, mark-as-read |
| `VerseSetReader` | `components/reader/` | Inline verse display with audio |

### Key Features (Jan 2026)

- **Verses shown by default** - No need to click "Näytä teksti"
- **Top navigation bar** - `[<] [Merkitse luetuksi] [>]` for easy day navigation
- **Verse badges** - Click to open day view (stays in reading plan context)
- **Quit button** - X button on active plans
- **Activity tracking** - Events logged to `user_activity_log`

### Hooks

| Hook | Purpose |
|------|---------|
| `useReadingPlans` | Data fetching, mutations (join, quit, mark complete) |
| `useReadingPlanDay` | Fetch specific day's readings |
| `useVerseSetFetcher` | Fetch verses for inline display |

### Utility Files

| File | Purpose |
|------|---------|
| `chapterVerseCounts.ts` | Static verse counts for accurate range calculations |
| `activityLogger.ts` | Logging reading plan events |

## RPC Functions

| Function | Purpose |
|----------|---------|
| `get_user_reading_plans` | Get user's plans with progress |
| `join_reading_plan` | Join a plan |
| `get_reading_plan_day` | Get day's readings |
| `mark_reading_day_complete` | Mark day complete |

## External Resources

For inspiration on reading plan structures:
- [Bible Study Tools](https://www.biblestudytools.com/bible-reading-plan/) - Various plan types
- [YouVersion](https://www.bible.com/reading-plans) - Popular reading plans
- [Blue Letter Bible](https://www.blueletterbible.org/dailyreading/) - Chronological plans

## Validation Checklist

- [ ] Book abbreviations valid (exist in bible_schema.books)
- [ ] Day numbers sequential (1, 2, 3...)
- [ ] duration_days matches actual day count
- [ ] readings JSONB is valid array format
- [ ] Finnish name and description provided

## Related Skills

| Situation | Delegate To |
|-----------|-------------|
| Database migrations | `supabase-migration-writer` |
| Bible verse lookups | `bible-lookup-helper` |
| Admin panel for plans | `admin-panel-builder` |
| Test the feature | `test-writer` |
