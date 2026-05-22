---
name: docs-updater
description: Expert assistant for keeping documentation synchronized with code changes in the KR92 Bible Voice project. Use when updating API docs, maintaining architecture diagrams, syncing README, updating CLAUDE.MD, or generating documentation from code.
---

# Docs Updater

## Capabilities
- Update API docs when schemas change
- Maintain architecture diagrams
- Sync README with actual features
- Ensure CLAUDE.MD stays current
- Generate documentation from code

## Documentation Files

| File | Purpose | Update When |
|------|---------|-------------|
| `CLAUDE.MD` | AI context doc | Major architecture changes |
| `README.md` | Project overview | Feature changes, setup changes |
| `Docs/01-PRD.md` | Product requirements | Vision or scope changes |
| `Docs/02-DESIGN.md` | Architecture | System design changes |
| `Docs/03-API.md` | API contracts | Database/RPC/Edge Function changes |
| `Docs/04-DEV-WORKFLOW.md` | Dev process | Workflow or CI/CD changes |
| `Docs/05-DEV.md` | Bible lookups | RPC function changes |
| `Docs/06-AI-ARCHITECTURE.md` | AI system | AI feature or prompt changes |
| `Docs/07-ADMIN-GUIDE.md` | Admin panel | Admin feature changes |
| `Docs/08-WIDGET.md` | Widget docs | Widget API or features changes |

## Usage Examples

### Example 1: Update API Docs After Schema Change
**User:** "I added a new table 'user_study_plans'. Update the docs."

**Assistant:**

Update `Docs/03-API.md`:
```markdown
### User Data Tables (public)
| Table | Primary Key | Notes |
|-------|-------------|-------|
| `profiles` | `id` (UUID) | User profiles with preferences |
| `bookmarks` | `id` (UUID) | User bookmarks (RLS enabled) |
| `highlights` | `id` (UUID) | User highlights with color (RLS enabled) |
| `user_study_plans` | `id` (UUID) | **NEW** User-created Bible study plans (RLS enabled) |
| ... | ... | ... |

### User Data

**NEW** Study Plans:
\`\`\`sql
-- Get user's study plans
get_user_study_plans(p_user_id)

-- Create study plan
create_study_plan(p_title, p_description, p_duration_days)

-- Add chapter to plan
add_plan_chapter(p_plan_id, p_book_name, p_chapter_number, p_day_number)
\`\`\`
```

Update `Docs/02-DESIGN.md`:
```markdown
### User Data Tables (public)
\`\`\`sql
profiles(id, user_id, display_name, email, audio_enabled)
bookmarks(id, user_id, verse_id, osis, chapter_id)
highlights(id, user_id, verse_id, color, tags)
user_study_plans(id, user_id, title, description, duration_days, created_at)  # NEW
plan_chapters(id, plan_id, book_name, chapter_number, day_number, completed)  # NEW
\`\`\`
```

Update `CLAUDE.MD`:
```markdown
### Database Schemas

**public** - User data and application tables:
- `profiles`, `user_roles`, `bookmarks`, `highlights`
- `user_study_plans`, `plan_chapters` # NEW - Bible study planning
- ...
```

### Example 2: Document New RPC Function
**User:** "Created RPC function `search_user_content(query, user_id)`. Document it."

**Assistant:**

Add to `Docs/03-API.md`:
```markdown
### User Content Search

**NEW** Search across user's bookmarks, highlights, and notes:
\`\`\`sql
search_user_content(p_query TEXT, p_user_id UUID DEFAULT auth.uid(), p_limit INT DEFAULT 50)
→ [{
  content_type TEXT,           -- 'bookmark', 'highlight', 'note'
  verse_id UUID,
  osis TEXT,
  verse_text TEXT,
  note_text TEXT,              -- NULL for bookmarks/highlights
  highlight_color TEXT,        -- NULL for bookmarks/notes
  created_at TIMESTAMPTZ,
  rank REAL                    -- Full-text search rank
}]
\`\`\`

**TypeScript:**
\`\`\`typescript
const { data } = await supabase.rpc('search_user_content', {
  p_query: 'grace faith',
  p_limit: 20
});
\`\`\`
```

Add to `Docs/05-DEV.md`:
```markdown
### search_user_content — Search User Content

\`\`\`sql
SELECT * FROM public.search_user_content(
  p_query := 'grace',
  p_user_id := auth.uid(),
  p_limit := 50
);
\`\`\`

**Returns:** Combined results from bookmarks, highlights, and notes with full-text search ranking.
```

### Example 3: Update Architecture Diagram
**User:** "Added new Edge Function 'generate-study-plan'. Update architecture docs."

**Assistant:**

Update `Docs/02-DESIGN.md`:
```markdown
### Edge Functions

Location: `supabase/functions/`

| Function | Auth | Purpose |
|----------|------|---------|
| `ai-orchestrator` | JWT | Central AI routing with usage logging |
| `translate-search-term` | Public | FI↔EN term translation for search |
| `generate-study-plan` | JWT | **NEW** AI-powered study plan generation |
| `generate-audio` | JWT | ElevenLabs TTS generation |
| ... | ... | ... |
```

Update architecture diagram:
```markdown
## AI Integration Flow

\`\`\`
1. User requests study plan
       │
       ▼
2. Frontend calls Edge Function
       │
       ▼
3. Edge Function:
   ├── Fetch feature config (vendor/model)
   ├── Fetch prompt template from DB
   ├── Render prompt with user preferences
   ├── Call AI provider
   ├── Parse structured study plan
   ├── Save to database
   ├── Log usage to ai_usage_logs
   └── Return plan to user
       │
       ▼
4. Frontend displays plan with chapters
\`\`\`
```

### Example 4: Sync README with Features
**User:** "Audio feature now supports playback speed control. Update README."

**Assistant:**

Update `README.md`:
```markdown
## Key Features

- Multi-version Bible reader (KR92/STLK 2017, 1933/38, KJV with Strong's)
- Full-text search and Strong's Concordance lookup
- AI-powered search term translation (Finnish ↔ English)
- AI summaries and contextual analysis
- Topic explorer with cross-references
- Audio Bible with ElevenLabs TTS **← Updated**
  - **NEW:** Playback speed control (0.5x - 2.0x)
  - **NEW:** Skip forward/backward 10 seconds
  - Chapter-by-chapter playback with verse sync
- User accounts with bookmarks and highlights
...
```

### Example 5: Generate API Documentation from Code
**User:** "Generate API documentation for the new Edge Function"

**Assistant:**

Create documentation from Edge Function code:
```typescript
// supabase/functions/generate-study-plan/index.ts

/**
 * Generate Study Plan Edge Function
 *
 * Creates an AI-powered Bible study plan based on user preferences.
 *
 * @endpoint POST /functions/v1/generate-study-plan
 * @auth JWT required
 *
 * @request
 * {
 *   duration_days: number,      // Plan duration (7-90 days)
 *   focus_topic?: string,        // Optional topic focus
 *   books?: string[],           // Optional book preferences
 *   daily_chapters?: number     // Chapters per day (1-5)
 * }
 *
 * @response
 * {
 *   success: boolean,
 *   plan: {
 *     id: string,
 *     title: string,
 *     description: string,
 *     duration_days: number,
 *     chapters: [{
 *       day_number: number,
 *       book_name: string,
 *       chapter_number: number,
 *       reason: string            // AI-generated explanation
 *     }]
 *   },
 *   metadata: {
 *     model: string,
 *     latencyMs: number,
 *     tokens: number
 *   }
 * }
 *
 * @example
 * const { data } = await supabase.functions.invoke('generate-study-plan', {
 *   body: {
 *     duration_days: 30,
 *     focus_topic: 'grace',
 *     daily_chapters: 2
 *   }
 * });
 */
```

Generate markdown documentation:
```markdown
## Edge Function: generate-study-plan

**Endpoint:** `POST /functions/v1/generate-study-plan`
**Authentication:** JWT required
**Purpose:** Generate AI-powered Bible study plans

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `duration_days` | number | Yes | Plan duration (7-90 days) |
| `focus_topic` | string | No | Optional topic focus |
| `books` | string[] | No | Optional book preferences |
| `daily_chapters` | number | No | Chapters per day (1-5, default: 2) |

### Response

\`\`\`json
{
  "success": true,
  "plan": {
    "id": "uuid",
    "title": "30-Day Grace Study",
    "description": "AI-generated study plan focusing on grace",
    "duration_days": 30,
    "chapters": [
      {
        "day_number": 1,
        "book_name": "Romans",
        "chapter_number": 3,
        "reason": "Introduces foundational concepts of grace"
      }
    ]
  },
  "metadata": {
    "model": "google/gemini-2.5-flash",
    "latencyMs": 2341,
    "tokens": 1523
  }
}
\`\`\`

### Usage Example

\`\`\`typescript
const { data, error } = await supabase.functions.invoke('generate-study-plan', {
  body: {
    duration_days: 30,
    focus_topic: 'grace',
    daily_chapters: 2
  }
});

if (error) throw error;
console.log('Generated plan:', data.plan);
\`\`\`
```

## Documentation Checklist

When making changes, update docs in this order:

### 1. Code Changes
- [ ] Write code
- [ ] Add JSDoc/comments
- [ ] Add TypeScript types

### 2. API Documentation (if applicable)
- [ ] Update `Docs/03-API.md` with new tables/functions
- [ ] Add request/response examples
- [ ] Document error cases

### 3. Architecture Documentation (if applicable)
- [ ] Update `Docs/02-DESIGN.md` with architectural changes
- [ ] Update diagrams
- [ ] Document new patterns

### 4. Usage Documentation
- [ ] Update relevant guide (`05-DEV.md`, `06-AI-ARCHITECTURE.md`, etc.)
- [ ] Add usage examples
- [ ] Update best practices

### 5. User-Facing Documentation
- [ ] Update `README.md` for feature changes
- [ ] Update `Docs/07-ADMIN-GUIDE.md` for admin features
- [ ] Update `Docs/08-WIDGET.md` for widget changes

### 6. AI Context
- [ ] Update `CLAUDE.MD` for major changes
- [ ] Keep schema reference current
- [ ] Update common patterns

## Documentation Quality Standards

### Good Documentation
- ✅ Clear and concise
- ✅ Includes examples
- ✅ Explains the "why" not just "what"
- ✅ Up-to-date with code
- ✅ Covers error cases
- ✅ Uses consistent formatting

### Bad Documentation
- ❌ Outdated information
- ❌ No examples
- ❌ Vague descriptions
- ❌ Missing error handling
- ❌ Inconsistent formatting
- ❌ Missing type information

## Automation Opportunities

Create documentation generation scripts:
```typescript
// scripts/generate-api-docs.ts
// Reads database schema and generates API documentation

import { createClient } from '@supabase/supabase-js';

async function generateTableDocs() {
  const supabase = createClient(url, key);

  const { data: tables } = await supabase
    .from('information_schema.tables')
    .select('table_name, table_schema');

  // Generate markdown for each table
  // ...
}
```

## Related Documentation
All documentation files are interconnected - changes often need updates across multiple files.
