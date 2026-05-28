---
name: idea-machina
description: |
  Expert assistant for developing the IdeaMachina app - an ideas management system with CRUD, tagging, ratings, and "Continue to..." actions that convert ideas into projects, goals, workflows, or prompts.

  Use when:
  (1) Adding features to the idea-machina app
  (2) Creating new pages or components in apps/idea-machina/
  (3) Working with pm_ideas, pm_idea_tags, pm_idea_ratings tables
  (4) Implementing "Continue to..." workflows (project, goal, workflow, prompt)
  (5) Extending the ideas data layer or types
  (6) Questions about idea-machina architecture or patterns

  Triggers: "idea-machina", "ideas app", "pm_ideas", "idea management", "continue to project", "idea tags", "idea ratings"
---

# IdeaMachina Development Guide

Expert guidance for extending the IdeaMachina app in the Raamattu Nyt monorepo.

## App Location

```
apps/idea-machina/
├── src/
│   ├── pages/
│   │   ├── Index.tsx           # Prompts management (original)
│   │   ├── IdeasPage.tsx       # Ideas list with filters
│   │   └── IdeaDetailPage.tsx  # Idea detail/edit view
│   ├── components/
│   │   ├── IdeaCard.tsx        # Card for list view
│   │   ├── IdeaForm.tsx        # Create/edit form
│   │   ├── IdeaFilters.tsx     # Status/tag/AI filters
│   │   ├── TagSelector.tsx     # Multi-select tags
│   │   ├── RatingStars.tsx     # 1-5 star input
│   │   ├── ContinueDialog.tsx  # "Continue to..." actions
│   │   └── AIPickupToggle.tsx  # AI pickup toggle + priority
│   ├── lib/
│   │   └── ideas.ts            # Data layer (CRUD, tags, ratings)
│   ├── types/
│   │   └── ideas.ts            # TypeScript interfaces
│   └── App.tsx                 # Routes
└── package.json
```

## Architecture Principles

1. **Monorepo patterns**: Shared UI from `packages/ui`, shared logic to `packages/*`
2. **DB schema**: All tables in `ai_prompt` schema
3. **Data layer**: Supabase client in `lib/ideas.ts`, React Query for state
4. **Soft delete**: Use `deleted_at` column, never hard delete
5. **RLS policies**: Owner can CRUD, authenticated can read

## Key Patterns

### Data Fetching (React Query)

```typescript
const { data: ideas } = useQuery({
  queryKey: ["ideas", filters],
  queryFn: () => listIdeas(filters),
});

const mutation = useMutation({
  mutationFn: createIdea,
  onSuccess: () => queryClient.invalidateQueries({ queryKey: ["ideas"] }),
});
```

### Type Transformations

DB uses `label`, UI uses `name` for tags:

```typescript
function transformTag(dbTag: PmIdeaTag): IdeaTag {
  return { ...dbTag, name: dbTag.label };
}
```

### "Continue to..." Actions

Ideas can convert to:
- **Project** → `pm_projects` (sets idea status to 'converted')
- **Goal** → `pm_goals` (links to existing project)
- **Workflow** → `workflows` (optional project link)
- **Prompt** → `prompts` + `prompt_versions`

## References

- [Architecture Details](references/architecture.md) - Full component hierarchy and data flow
- [DB Schema](references/db-schema.md) - Table structures and RLS policies
- PRD location: `/Docs/idea-machina/PRD.md` (when created)

## Development Workflow

1. **New feature**: Plan with brainstorming skill first
2. **DB changes**: Create migration in `supabase/migrations/`
3. **Types**: Update `src/types/ideas.ts`
4. **Data layer**: Add functions to `src/lib/ideas.ts`
5. **Components**: Build in `src/components/`
6. **Pages**: Add routes in `src/App.tsx`
7. **Tests**: Use test-writer skill
8. **Docs**: Update `/Docs/idea-machina/`

## Common Tasks

### Add New Field to Ideas

1. Migration: `ALTER TABLE ai_prompt.pm_ideas ADD COLUMN ...`
2. Types: Update `PmIdea` and `IdeaWithDetails`
3. Form: Add field to `IdeaForm.tsx`
4. Card: Display in `IdeaCard.tsx` if needed

### Add New "Continue to..." Action

1. Types: Add payload interface in `types/ideas.ts`
2. Data: Add function in `lib/ideas.ts`
3. Dialog: Add option and form in `ContinueDialog.tsx`
4. Handlers: Wire up in pages

### Add New Filter

1. State: Add filter state in `IdeasPage.tsx`
2. UI: Add control in `IdeaFilters.tsx`
3. Query: Pass to `listIdeas()` in query key
4. Data: Handle in `listIdeas()` function
