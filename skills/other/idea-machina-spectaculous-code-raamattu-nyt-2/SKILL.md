---
name: idea-machina
description: |
  Expert assistant for developing the IdeaMachina app - an ideas-to-project pipeline with brainstorming, evaluation, shaping, translation, and "Continue to..." actions that convert ideas into projects, goals, workflows, or prompts.

  Use when:
  (1) Adding features to the idea-machina app (apps/idea-machina/)
  (2) Working with pm_ideas, pm_idea_tags, pm_idea_ratings, pm_projects tables
  (3) Implementing brainstorm, translate, or AI-assisted idea shaping
  (4) Implementing "Continue to..." workflows (project, goal, workflow, prompt)
  (5) Extending the ideas data layer, types, or UI components
  (6) Working with the idea lifecycle state machine (intake → shaping → evaluation → project)
  (7) Questions about idea-machina architecture, patterns, or data flow

  Triggers: "idea-machina", "ideas app", "pm_ideas", "idea management", "continue to project", "idea tags", "idea ratings", "brainstorm idea", "idea shaping", "idea evaluation", "IMIdeaCard", "IdeasStatsBar"
---

# IdeaMachina Development Guide

## App Location

```
apps/idea-machina/
├── src/
│   ├── pages/
│   │   ├── Index.tsx              # Prompts management (original)
│   │   ├── IdeasPage.tsx          # Ideas list: stats bar, tabs, single-column cards
│   │   ├── IdeaDetailPage.tsx     # Idea detail/edit view
│   │   └── ProjectsPage.tsx       # Projects CRUD
│   ├── components/
│   │   ├── ideas/                 # New Ohjaamo-style components
│   │   │   ├── config.ts          # STATUS_CONFIG: icons, colors, rings per status
│   │   │   ├── IdeasStatsBar.tsx   # Clickable stat cards (total + per-status)
│   │   │   ├── IMIdeaCard.tsx      # Rich full-width card with inline actions
│   │   │   └── IMIdeasCardList.tsx # List wrapper with loading/empty states
│   │   ├── ui/
│   │   │   └── dropdown-menu.tsx   # Radix dropdown-menu (local copy)
│   │   ├── IdeaForm.tsx           # Create/edit form with benefit + bilingual fields
│   │   ├── TagSelector.tsx        # Multi-select tags + TagChips display
│   │   ├── RatingStars.tsx        # 1-5 star input
│   │   ├── LanguageFieldTabs.tsx  # FI/EN tab switcher for bilingual fields
│   │   ├── ContinueDialog.tsx     # "Continue to..." actions
│   │   ├── BrainstormDialog.tsx   # AI brainstorm: develop/split/subideas
│   │   ├── AIPickupToggle.tsx     # AI pickup toggle + priority
│   │   └── AppHeader.tsx          # Navigation header
│   ├── lib/
│   │   ├── ideas.ts               # Data layer: CRUD, brainstorm, translate, stats
│   │   └── aiContext.ts           # AI phase history utilities (v2)
│   ├── types/
│   │   └── ideas.ts               # TypeScript interfaces + helpers
│   └── App.tsx                    # Routes
```

## Architecture Principles

1. **Monorepo**: Shared UI from `packages/ui/src/`, app-local components for IM-specific
2. **DB schema**: All tables in `ai_prompt` schema via `supabaseAiPrompt` client
3. **Data layer**: `lib/ideas.ts` for all Supabase operations, React Query for caching
4. **Bilingual**: All text fields have `_fi` / `_en` variants, `localizedField()` resolves
5. **Soft delete**: `deleted_at` column, never hard delete
6. **AI features**: Brainstorm (develop/split/subideas), translate (FI/EN), AI phase history

## Key Patterns

### Data Fetching (React Query)

```typescript
const { data: ideas } = useQuery({
  queryKey: ["ideas", filters],
  queryFn: () => listIdeas(filters),
});

const statusMutation = useMutation({
  mutationFn: ({ id, status }) => quickUpdateStatus(id, status),
  onSuccess: () => queryClient.invalidateQueries({ queryKey: ["ideas"] }),
});
```

### Bilingual Fields

Every text field has three variants: base, `_fi`, `_en`.

```typescript
// Resolve: prefer current lang, fallback to other, then base
const title = localizedField(i18n.language, idea.title_fi, idea.title_en, idea.title);
```

Form uses `LanguageFieldTabs` component for FI/EN tab input.

### Status Flow

Statuses: `new` → `nurturing` → `ready` → `converted` | `archived`

Inline quick-change buttons on each card. `quickUpdateStatus()` for direct DB update.

### "Continue to..." Actions

Ideas convert to: **Project** → `pm_projects` | **Goal** → `pm_goals` | **Workflow** → `workflows` | **Prompt** → `prompts` + `prompt_versions`

### AI Phase History (ai_context JSONB)

Append-only phase log stored in `idea.ai_context`. Utility: `lib/aiContext.ts`.

```typescript
import { normalizeAiContext, addPhase, getLatestPhase } from "../lib/aiContext";
// Types: AiPhase, IdeaAiContext, PromotedResource
// Phases: prepare, brainstorm, develop, split, subideas, translate
```

### Stats (Client-Side)

```typescript
const stats = computeIdeaStats(ideas); // { total, new, nurturing, ready, converted, archived }
```

## State Machine

Full lifecycle: see `Docs/idea-machina/IDEA-MACHINA-STATES.md`

```
IDEA_INTAKE → IDEA_SHAPING (enrich/enhance/decompose)
            → IDEA_EVALUATION (business/tech/risk agents)
            → PROJECT_COMMIT → GOAL_DRAFT → GOAL_POLISH
            → ROADMAP_PLANNING → WORKFLOW_DESIGN
            → EXECUTION → RESULT_EVALUATION → DELIVERY
            → MONITORING → LEARNING ↺ feeds back
```

Currently implemented: Intake, partial Shaping (brainstorm), Continue-to-Project.
Future: Evaluation agents, goal polishing, roadmap planning, execution/monitoring.

## References

- [Architecture Details](references/architecture.md) — Component hierarchy, data flow, query keys
- [DB Schema](references/db-schema.md) — Table structures, bilingual columns, RLS policies
- State machine: `Docs/idea-machina/IDEA-MACHINA-STATES.md`

## Common Tasks

### Add New Field to Ideas

1. Migration: `ALTER TABLE ai_prompt.pm_ideas ADD COLUMN ...` (+ `_fi`/`_en` variants)
2. Types: Update `PmIdea` and `IdeaFormData` in `types/ideas.ts`
3. Form: Add `LanguageFieldTabs` in `IdeaForm.tsx`
4. Card: Display in `IMIdeaCard.tsx`
5. Translate: Add to `TranslationResult` and `applyTranslation` in `lib/ideas.ts`

### Add New "Continue to..." Action

1. Types: Add payload interface in `types/ideas.ts`
2. Data: Add function in `lib/ideas.ts`
3. Dialog: Add option and form in `ContinueDialog.tsx`
4. Handlers: Wire up in `IdeasPage.tsx`

### Add New Tab/Filter

1. Tab: Add to `TabValue` type and `<Tabs>` in `IdeasPage.tsx`
2. Filter: Add client-side logic in `filteredIdeas` useMemo
3. Or add server-side filter param to `IdeaFilters` type and `listIdeas()`

### Implement Next State Machine Phase

1. Reference `Docs/idea-machina/IDEA-MACHINA-STATES.md` for transitions
2. Add status/state fields to DB if needed
3. Create components for the new phase UI
4. Add service functions in `lib/ideas.ts`
5. Wire into page with mutations and dialogs
