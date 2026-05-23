---
name: ralph
description: "Convert PRDs to prd.json format for the Ralph autonomous agent system. Use when you have an existing PRD and need to convert it to Ralph's JSON format. Triggers on: convert to ralph, convert this prd, turn this into ralph format, create prd.json, ralph json, run ralph on this."
---

# Ralph PRD Converter

Converts existing markdown PRDs to the `prd.json` format that Ralph uses for autonomous execution.

---

## The Job

1. Read the PRD from `tasks/prd-[feature-name].md` (or ask user which PRD)
2. Convert user stories to properly-sized JSON entries
3. Validate story sizing and dependencies
4. Save to `ralph-cc/prd.json`

---

## Story Size: The Number One Rule

> **Each story must be completable in ONE Ralph iteration (one context window).**

Ralph spawns a fresh Claude Code instance per iteration with no memory of previous work. If a story is too big, Claude runs out of context before finishing and produces broken code.

### Right-sized stories (GOOD):

- Add a TypeScript type/interface
- Create a single component
- Add a Zustand store
- Create a custom hook
- Add translations to i18n
- Update a configuration file

### Too big (SPLIT THESE):

- "Build the entire feature" → Split into: types, store, hooks, components, screen
- "Add authentication" → Split into: types, store, hook, UI components, routes
- "Create a dashboard" → Split into: types, data hooks, individual cards, layout

### Rule of Thumb

If you cannot describe the change in 2-3 sentences, it is too big.

---

## Story Ordering: Dependencies First

Stories execute in priority order. Earlier stories must NOT depend on later ones.

**Correct order:**

1. Types/Interfaces (no dependencies)
2. Constants/Configuration
3. Utilities/Helpers
4. Stores (depends on types)
5. Hooks (depends on stores)
6. UI Components (depends on hooks)
7. Screens (depends on components)
8. Integration (wiring everything together)

**Wrong order:**

1. UI component (depends on store that doesn't exist yet)
2. Store (should come first!)

---

## Output Format

```json
{
  "project": "BYB React",
  "branchName": "ralph/[feature-name-kebab-case]",
  "description": "[Feature description from PRD]",
  "userStories": [
    {
      "id": "US-001",
      "title": "[Story title]",
      "description": "As a [user], I want [feature] so that [benefit]",
      "acceptanceCriteria": ["Criterion 1", "Criterion 2", "Typecheck passes"],
      "priority": 1,
      "passes": false,
      "notes": ""
    }
  ]
}
```

---

## Acceptance Criteria: Must Be Verifiable

Each criterion must be something Ralph can CHECK, not something vague.

### Good criteria (verifiable):

- "Create `types/Feature.ts` with Feature interface"
- "Add `useFeatureStore` to `/stores` with state and actions"
- "Component shows loading skeleton when isLoading is true"
- "Typecheck passes"

### Bad criteria (vague):

- "Works correctly"
- "User can do X easily"
- "Good UX"
- "Handles edge cases"

### Always include:

```
"Typecheck passes"
```

---

## Conversion Rules

1. **Each user story becomes one JSON entry**
2. **IDs**: Sequential (US-001, US-002, etc.)
3. **Priority**: Based on dependency order (1 = first to execute)
4. **All stories**: `passes: false` and empty `notes`
5. **branchName**: Derive from feature name, kebab-case, prefixed with `ralph/`
6. **Always add**: "Typecheck passes" to every story's acceptance criteria

---

## Splitting Large Stories

If a PRD has stories that are too big, split them:

**Original:**

> "US-003: Create favorites feature UI"

**Split into:**

```json
{
  "id": "US-003",
  "title": "Create FavoriteButton component",
  "acceptanceCriteria": [
    "Create components/FavoriteButton.tsx",
    "Props: trackId, isFavorite, onToggle",
    "Shows heart icon with fill/outline states",
    "Typecheck passes"
  ],
  "priority": 3
},
{
  "id": "US-004",
  "title": "Create FavoritesList component",
  "acceptanceCriteria": [
    "Create components/FavoritesList.tsx",
    "Renders list of favorited tracks",
    "Shows empty state when no favorites",
    "Typecheck passes"
  ],
  "priority": 4
},
{
  "id": "US-005",
  "title": "Integrate FavoriteButton into TrackCard",
  "acceptanceCriteria": [
    "Import FavoriteButton into TrackCard",
    "Connect to useFavoritesStore",
    "Position in top-right of card",
    "Typecheck passes"
  ],
  "priority": 5
}
```

---

## Archiving Previous Runs

**Before writing a new prd.json, check if there's an existing one from a different feature:**

1. Read current `ralph-cc/prd.json` if it exists
2. Check if `branchName` differs from the new feature
3. If different AND `ralph-cc/progress.txt` has content:
   - Create archive folder: `ralph-cc/archive/YYYY-MM-DD-feature-name/`
   - Copy current `prd.json` and `progress.txt` to archive
   - Reset `progress.txt` with fresh header

**Note:** The `ralph.sh` script handles this automatically, but if manually updating between runs, archive first.

---

## Example Conversion

### Input (from tasks/prd-favorites.md):

```markdown
### US-001: Create Favorite type definitions

**Description:** As a developer, I need TypeScript types for favorites.

**Acceptance Criteria:**

- [ ] Create types/Favorite.ts with Favorite interface
- [ ] Include fields: id, odTid, favoritedAt
- [ ] Typecheck passes

### US-002: Create useFavoritesStore

**Description:** As a developer, I need a store to manage favorites.

**Acceptance Criteria:**

- [ ] Create stores/useFavoritesStore.ts
- [ ] State: favorites array, isLoading
- [ ] Actions: addFavorite, removeFavorite
- [ ] Typecheck passes
```

### Output (ralph-cc/prd.json):

```json
{
  "project": "BYB React",
  "branchName": "ralph/favorites",
  "description": "Add ability for users to favorite workout tracks",
  "userStories": [
    {
      "id": "US-001",
      "title": "Create Favorite type definitions",
      "description": "As a developer, I need TypeScript types for favorites so the feature is type-safe.",
      "acceptanceCriteria": [
        "Create types/Favorite.ts with Favorite interface",
        "Include fields: id, odTid, favoritedAt",
        "Typecheck passes"
      ],
      "priority": 1,
      "passes": false,
      "notes": ""
    },
    {
      "id": "US-002",
      "title": "Create useFavoritesStore Zustand store",
      "description": "As a developer, I need a store to manage favorites state.",
      "acceptanceCriteria": [
        "Create stores/useFavoritesStore.ts",
        "State: favorites array, isLoading boolean",
        "Actions: addFavorite, removeFavorite, setFavorites",
        "Typecheck passes"
      ],
      "priority": 2,
      "passes": false,
      "notes": ""
    }
  ]
}
```

---

## After Converting

Tell the user:

```
PRD converted and saved to ralph-cc/prd.json

Branch: ralph/[feature-name]
Stories: [X] total
Estimated iterations: [X]

To run Ralph:
  cd ralph-cc && ./ralph.sh

To monitor progress:
  - Watch terminal output
  - Check ralph-cc/progress.txt for learnings
  - Review git commits as they're created
```

---

## Checklist Before Saving

- [ ] Each story completable in ONE iteration (small enough)?
- [ ] Stories ordered by dependency (types → stores → hooks → UI)?
- [ ] Every story has "Typecheck passes" as criterion?
- [ ] Acceptance criteria are verifiable (not vague)?
- [ ] No story depends on a later story?
- [ ] Branch name is kebab-case with `ralph/` prefix?
- [ ] Previous run archived (if different feature)?

---

## If No PRD Exists

If the user says "convert to ralph" but no PRD exists in `tasks/`:

1. Ask which feature they want to convert
2. If they describe a feature, suggest using `/prd` first:

```
No PRD found in tasks/. Would you like me to:

A. Create a PRD first (recommended) - I'll ask clarifying questions and generate tasks/prd-[feature].md
B. Create prd.json directly from your description (skip the markdown PRD step)

For complex features, option A is recommended as it produces better-structured user stories.
```
