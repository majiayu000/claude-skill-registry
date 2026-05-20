---
name: planning-business
description: Business planning skill with Lean Canvas, milestone planning, and business model analysis. Use when users need to create or refine business plans.
---

# Planning Business

Business planning skill that guides users through structured business model creation. Supports adaptive question depth based on user experience profile.

## When to Use

- User wants to create or validate a business plan
- User needs a Lean Canvas for their product/startup
- User wants to refine an existing business model

## Phases

### Phase 1: Lean Canvas

Guides user through all 9 Lean Canvas blocks via AskUserQuestion prompts. Produces a structured one-page business model.

**Workflow:**

1. Check for adaptive profile from EPIC-072:
   - Read user profile for experience level (beginner/intermediate/advanced)
   - If missing profile or no profile found, default to intermediate question depth
   - Log warning for missing profile: "No adaptive profile found, defaulting to intermediate depth"
2. Check for existing `devforgeai/specs/business/business-plan/lean-canvas.md`:
   - If exists: Enter iteration mode (read, present, modify)
   - If not exists: Start fresh canvas workflow
3. Walk through 9 blocks in order, adapting question depth per profile
4. Write completed canvas to `devforgeai/specs/business/business-plan/lean-canvas.md`

**Adaptive Profile Fallback:**

When no adaptive profile exists or the profile is absent, the skill defaults to intermediate question depth. A warning is logged indicating the missing profile so the user is aware adaptation is unavailable. The full 9-block workflow completes without error regardless of profile availability.

**9 Lean Canvas Blocks (in order):**

1. Problem
2. Customer Segments
3. Unique Value Proposition
4. Solution
5. Channels
6. Revenue Streams
7. Cost Structure
8. Key Metrics
9. Unfair Advantage

**Output:** `devforgeai/specs/business/business-plan/lean-canvas.md`

**Reference:** For detailed workflow, adaptive question sets, and iteration support, see: [lean-canvas-workflow.md](references/lean-canvas-workflow.md)

### Phase 2: Milestone-Based Plan

*Future: STORY-532*

### Phase 3: Business Model Pattern Matching

*Future: STORY-533*

## User Interaction

All user interaction uses AskUserQuestion tool. No Bash-based prompts.

## Error Handling

- Missing output directory: Create `devforgeai/specs/business/business-plan/` before writing
- Corrupted existing canvas: Offer fresh start or abort via AskUserQuestion
- Unknown experience level in profile: Fall back to intermediate

## Success Criteria

- All 9 Lean Canvas blocks presented to user
- Output file written with user-provided content
- Adaptive depth applied based on profile (or fallback to intermediate)
- Existing canvas preserved during iteration mode
