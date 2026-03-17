---
name: user-story-mapping
description: Visualizing user journeys and slicing deliverables into releases.
role: prod-pm
triggers:
  - story map
  - user journey
  - release slice
  - backbone
  - mvp
---

# user-story-mapping Skill

This skill guides the creation of a 2D map of user needs (The Backbone) vs details (The Body) to scope releases.

## 1. The Matrix (Backbone vs Body)
- **X-Axis (Backbone)**: The narrative flow. "User Signs Up" -> "Searches Product" -> "Adds to Cart" -> "Checks Out".
- **Y-Axis (Priority)**: Depth of implementation.
  - *Slice 1 (MVP)*: "Sign up via Email".
  - *Slice 2 (v1.1)*: "Sign up via Google".
  - *Slice 3 (v2)*: "Sign up via SSO".

## 2. Process
1.  **Define the Persona**: Who are we mapping for?
2.  **Map the Steps (Activities)**: High-level goals (e.g., "Manage Profile").
3.  **Break into Tasks**: Concrete actions (e.g., "Upload Avatar").
4.  **Slice Lines**: Draw horizontal lines to define Release 1, Release 2, Release 3.

## 3. Output Format
Use `templates/product/USER_STORY_MAP_TEMPLATE.md` to document the outcome.

## 4. The "Walking Skeleton" Strategy
- **Goal**: Implement a tiny slice of the *entire* backbone first.
- **Why**: Proves end-to-end connectivity (Frontend -> Backend -> DB) in Week 1.
- **Example**: "User clicks Buy -> DB records order -> Payment Stubbed -> Email Sent".

## 5. Prioritization Rules (MoSCoW)
- **Must Have**: Without this, it doesn't work.
- **Should Have**: Important constraints (Performance, key features).
- **Could Have**: Delightful add-ons.
- **Won't Have**: Out of scope for now.
