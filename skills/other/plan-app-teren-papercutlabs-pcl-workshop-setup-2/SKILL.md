---
name: plan-app
description: "MANDATORY INVOCATION: This skill MUST be invoked for building workshop apps. Guides the full flow from idea to deployed app: interview, screen flows, decomposition into sub-agents, parallel build, and merge. Trigger for: :plan-app macro, building an app, app planning, workshop app build."
---

# Plan App

Build a complete app in ~2 hours through guided planning and parallel sub-agent execution.

## Flow (MANDATORY - IN ORDER)

Complete each phase before moving to the next. Read the reference file at the START of each phase.

### Phase 1: INTERVIEW
**Read:** `reference/01-interview.md`
**When:** Immediately after skill invoked
**Goal:** Understand what they want to build, who uses it, core use cases
**Done when:** You have clear app concept and can describe it back to them

### Phase 2: SCREEN FLOWS
**Read:** `reference/02-screen-flows.md`
**When:** Interview complete
**Goal:** Create wireframes + user journeys (combined, not separate)
**Done when:** Participant approves the screen flows

### Phase 3: DECOMPOSITION
**Read:** `reference/03-decomposition.md`
**When:** Screen flows approved
**Goal:** Split work into Foundation + Feature agents
**Done when:** Sub-agent MD files written to `/docs/agents/`

### Phase 4: DISPATCH
**Read:** `reference/04-dispatch.md`
**When:** MD files ready
**Goal:** Run Foundation agent, then feature agents in parallel (same repo, file ownership prevents conflicts)
**Done when:** All sub-agents have returned

### Phase 5: TESTING
**Read:** `reference/05-testing.md`
**When:** All sub-agents complete
**Goal:** Automated verification + user testing
**Done when:** All checks pass, user confirms it works

### Phase 6: DEPLOY
**Read:** `reference/06-deploy.md`
**When:** Testing complete
**Goal:** Deploy to Vercel
**Done when:** App running on Vercel with live URL

## Project Location

Create the project folder in the current working directory. Use a slugified version of the app name:
- "Campaign Archive" → `./campaign-archive/`
- "Team Wiki" → `./team-wiki/`

Do not ask the user where to put it. Just create it in the current directory.

## Hard Limits

Enforce these during interview. If app exceeds limits, help them cut scope.

- **Max 4 screens**
- **Max 2 tables**
- **Max 2 external APIs**

## Tech Stack (Non-negotiable)

Do not offer choices. These are prescribed:

- **Framework:** Next.js (App Router)
- **Database:** Supabase (via Vercel integration)
- **UI:** ShadCN
- **Auth:** Supabase Auth with email/password (if needed)
- **Hosting:** Vercel

## Planning Outputs

All written to `/docs/` in the project:

| File | Contents |
|------|----------|
| `/docs/screen-flows.md` | Wireframes + user journeys (approved by participant) |
| `/docs/agents/foundation.md` | Foundation agent brief |
| `/docs/agents/feature-*.md` | Feature agent briefs (one per feature) |