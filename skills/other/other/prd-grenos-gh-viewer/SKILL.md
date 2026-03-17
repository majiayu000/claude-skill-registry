---
name: prd
description: 'Generate a Product Requirements Document (PRD) for a new feature. Use when planning a feature, starting a new project, or when asked to create a PRD. Triggers on: create a prd, write prd for, plan this feature, requirements for, spec out.'
---

# PRD Generator

Create detailed Product Requirements Documents that are clear, actionable, and suitable for implementation. This creates a **markdown PRD** that a product manager would write.

---

## The Job

1. Receive a feature description from the user
2. Ask 3-5 essential clarifying questions (with lettered options)
3. Generate a structured PRD based on answers
4. Save to `tasks/prd-[feature-name].md`

**Important:** Do NOT start implementing. Just create the PRD.

---

## Step 1: Clarifying Questions

Ask only critical questions where the initial prompt is ambiguous. Focus on:

- **Problem/Goal:** What problem does this solve?
- **Core Functionality:** What are the key actions?
- **Scope/Boundaries:** What should it NOT do?
- **Success Criteria:** How do we know it's done?

### Format Questions Like This:

```
1. What is the primary goal of this feature?
   A. Improve user onboarding experience
   B. Increase user retention
   C. Reduce support burden
   D. Other: [please specify]

2. Who is the target user?
   A. New users only
   B. Existing users only
   C. All users
   D. Admin users only

3. What is the scope?
   A. Minimal viable version
   B. Full-featured implementation
   C. Just the backend/API
   D. Just the UI
```

This lets users respond with "1A, 2C, 3B" for quick iteration.

---

## Step 2: PRD Structure

Generate the PRD with these sections:

### 1. Introduction/Overview

Brief description of the feature and the problem it solves.

### 2. Goals

Specific, measurable objectives (bullet list).

### 3. User Stories

Each story needs:

- **Title:** Short descriptive name
- **Description:** "As a [user], I want [feature] so that [benefit]"
- **Acceptance Criteria:** Verifiable checklist of what "done" means

Each story should be small enough to implement in one focused session.

**Format:**

```markdown
### US-001: [Title]

**Description:** As a [user], I want [feature] so that [benefit].

**Acceptance Criteria:**

- [ ] Specific verifiable criterion
- [ ] Another criterion
- [ ] Typecheck passes
```

**Important:**

- Acceptance criteria must be verifiable, not vague
- "Works correctly" is BAD
- "Button shows confirmation dialog before deleting" is GOOD
- Always include "Typecheck passes" for every story

### 4. Functional Requirements

Numbered list of specific functionalities:

- "FR-1: The system must allow users to..."
- "FR-2: When a user clicks X, the system must..."

Be explicit and unambiguous.

### 5. Non-Goals (Out of Scope)

What this feature will NOT include. Critical for managing scope.

### 6. Design Considerations (Optional)

- UI/UX requirements
- Link to mockups if available
- Relevant existing components to reuse

### 7. Technical Considerations (Optional)

- Known constraints or dependencies
- Integration points with existing systems
- Performance requirements

### 8. Success Metrics

How will success be measured?

- "Reduce time to complete X by 50%"
- "Increase conversion rate by 10%"

### 9. Open Questions

Remaining questions or areas needing clarification.

---

## Project-Specific Guidance (BYB React)

When writing PRDs for this codebase, consider:

### File Structure

- Types → `/types/`
- Stores → `/stores/`
- Hooks → `/hooks/` or `/screens/[Flow]/[Screen]/hooks/`
- Components → `/components/` or feature-specific
- Screens → `/screens/[Flow]/[Screen]/`
- Constants → `/constants/`
- Utilities → `/utils/`
- Translations → `/i18n/languages/en.json`

### Code Standards to Reference

- Use custom `Heading` and `Text` from `@/components`
- All user-facing strings must use `t()` for i18n
- Use Tamagui components with theme tokens
- Import from `tamagui` not `@tamagui/stacks`

---

## Writing for Junior Developers / AI Agents

The PRD reader may be a junior developer or AI agent. Therefore:

- Be explicit and unambiguous
- Avoid jargon or explain it
- Provide enough detail to understand purpose and core logic
- Number requirements for easy reference
- Use concrete examples where helpful

---

## Output

- **Format:** Markdown (`.md`)
- **Location:** `tasks/`
- **Filename:** `prd-[feature-name].md` (kebab-case)

---

## Example PRD

```markdown
# PRD: Favorites Feature

## Introduction

Add the ability for users to favorite workout tracks so they can quickly access their preferred workouts. Favorites will be stored in Firestore and synced across devices.

## Goals

- Allow users to mark tracks as favorites with a single tap
- Persist favorites to cloud for cross-device sync
- Display a dedicated favorites section for quick access
- Provide visual feedback when favoriting/unfavoriting

## User Stories

### US-001: Create Favorite type definitions

**Description:** As a developer, I need TypeScript types for favorites so the feature is type-safe.

**Acceptance Criteria:**

- [ ] Create `types/Favorite.ts` with Favorite interface
- [ ] Include fields: id, odTid, odUserId, favoritedAt
- [ ] Export FavoriteStoreState type for Zustand store
- [ ] Typecheck passes

### US-002: Create useFavoritesStore Zustand store

**Description:** As a developer, I need a store to manage favorites state.

**Acceptance Criteria:**

- [ ] Create `stores/useFavoritesStore.ts`
- [ ] State: favorites array, isLoading boolean
- [ ] Actions: addFavorite, removeFavorite, setFavorites, clearFavorites
- [ ] Persist to AsyncStorage for offline access
- [ ] Typecheck passes

### US-003: Create FavoriteButton component

**Description:** As a user, I want a button to toggle favorites on tracks.

**Acceptance Criteria:**

- [ ] Create `components/FavoriteButton.tsx`
- [ ] Props: trackId, size (sm/md/lg)
- [ ] Shows filled heart when favorited, outline when not
- [ ] Animates on press
- [ ] Uses theme colors
- [ ] Typecheck passes

### US-004: Add i18n translations for favorites

**Description:** As a user, I want favorites UI text in my language.

**Acceptance Criteria:**

- [ ] Add 'Favorites' key to en.json
- [ ] Add 'Add to Favorites' key
- [ ] Add 'Remove from Favorites' key
- [ ] Add 'No favorites yet' key
- [ ] Typecheck passes

### US-005: Integrate FavoriteButton into TrackCard

**Description:** As a user, I want to favorite tracks from the track list.

**Acceptance Criteria:**

- [ ] Import FavoriteButton into TrackCard component
- [ ] Position button in top-right corner of card
- [ ] Connect to useFavoritesStore
- [ ] Typecheck passes

## Functional Requirements

- FR-1: Users can tap a heart icon to favorite/unfavorite a track
- FR-2: Favorites persist across app sessions via AsyncStorage
- FR-3: Favorites sync to Firestore when online
- FR-4: FavoriteButton shows loading state during sync
- FR-5: Favorites count visible in profile section

## Non-Goals

- No favorites for individual exercises (only tracks)
- No favorites sharing with other users
- No favorites limit
- No favorites organization/folders

## Technical Considerations

- Use optimistic updates for immediate UI feedback
- Sync to Firestore `users/{userId}/favorites` collection
- Handle offline gracefully with AsyncStorage cache
- Consider React Query for server state

## Success Metrics

- Users can favorite a track in under 2 taps
- Favorites persist correctly across sessions
- No performance impact on track list rendering

## Open Questions

- Should favorites appear in a dedicated tab or section?
- Should we show "recently favorited" vs "all favorites"?
```

---

## After Creating PRD

Tell the user:

```
PRD saved to tasks/prd-[feature-name].md

Next steps:
1. Review the PRD and make any adjustments
2. When ready, say "convert to ralph" or use /ralph to convert it to prd.json
3. Then run: cd ralph-cc && ./ralph.sh
```

---

## Checklist

Before saving the PRD:

- [ ] Asked clarifying questions with lettered options
- [ ] Incorporated user's answers
- [ ] User stories are small and specific
- [ ] Acceptance criteria are verifiable (not vague)
- [ ] "Typecheck passes" included in every story
- [ ] Functional requirements are numbered and unambiguous
- [ ] Non-goals section defines clear boundaries
- [ ] Saved to `tasks/prd-[feature-name].md`
