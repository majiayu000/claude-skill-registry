---
name: launch-planner
description: Helps transform app ideas into shippable MVPs using a ship-fast, validate-first philosophy. Use when the user wants to plan an MVP, scope features, generate PRDs, get product advice, create Claude Code starter prompts, or needs help staying focused on shipping rather than over-engineering. Tech stack is Nuxt 3 or 4, Supabase, and Vercel.
---

# Launch Planner

This skill helps you transform app ideas into shippable MVPs by applying lean product principles and preventing common mistakes that delay launches.

## Product Philosophy

**Ship fast, validate with real users, no feature creep.**

Every decision should optimize for getting something in front of users as quickly as possible. Features can always be added after validation, but time spent building unused features is gone forever.

## Tech Stack Defaults

Unless specified otherwise, use:
- **Frontend**: Nuxt 3 or 4 with Vue
- **Database**: Supabase
- **Deployment**: Vercel
- **Styling**: Tailwind CSS (if frontend engineering context is known)
- **UI Components**: shadcn/ui (if frontend engineering context is known)

## MVP Scoping Rules

### Core Principle: One Week Maximum

If any feature takes more than 1 week to build, it's not MVP-ready. Break it down or cut it.

### The Essential Features Test

For every proposed feature, ask:
1. **Does it serve the core user loop?** If removed, would the product still solve its main problem?
2. **Can we validate the idea without it?** Many features feel necessary but aren't required for validation.
3. **Is there a simpler version?** Look for the 20% solution that gives 80% of the value.

### What to Cut from MVP

Common features to **defer until after validation**:
- User authentication (unless core to the value prop)
- User profiles and settings
- Email notifications
- Admin dashboards
- Multiple user roles/permissions
- Social features (likes, comments, follows)
- Search functionality
- Advanced filters
- Payment integration (unless it's a paid product)
- Mobile apps (start with responsive web)
- Multiple languages/i18n

## Critical Questions Before Building

Ask these three questions before writing any code:

### 1. Who is this for?

Be specific. "Everyone" is not an answer. Define:
- **Specific persona**: Job title, situation, or demographic
- **Current behavior**: What do they do today without your product?
- **Example**: "Freelance designers who currently use Notion to track client projects"

### 2. What's the one problem it solves?

One sentence. One problem. Examples:
- ❌ "Helps people manage tasks and collaborate with teams" (too broad)
- ✅ "Lets remote teams see who's working on what right now" (specific)

### 3. How will I know if it works?

Define your success metric upfront:
- Number of signups?
- Daily active users?
- Tasks completed?
- Time saved?
- Money made?

Be specific and measurable. "People like it" is not measurable.

## Common Mistakes to Avoid

### Building Features Nobody Asked For

Wait for users to request features. Don't build based on "they'll probably want this."

**Pattern to recognize**: "We should add [feature] because users might need it later."
**Response**: "Let's wait until users actually ask for it."

### Over-Engineering

Don't build for scale you don't have. Don't add complexity for edge cases that may never happen.

**Pattern to recognize**: "What if we have millions of users?" when you have zero.
**Response**: "Let's solve problems we actually have, not hypothetical ones."

### Adding Auth Before Validation

Authentication is surprisingly time-consuming and doesn't help validate if people want your product.

**When to add auth**: After validating people want the product and use it repeatedly.
**How to validate without auth**: Use a single shared link, simple password, or localStorage.

### Perfecting the UI/UX

Ugly MVPs validate ideas just as well as beautiful ones. Polish is for retention, not validation.

**MVP standard**: Clean enough that people take it seriously. No more.

### Building Features Sequentially

Work in vertical slices (full user flow for one feature) not horizontal layers (all database tables, then all API routes, then all UI).

**Better approach**: One working feature end-to-end > three half-built features.

## Workflows

### Generate a PRD from an Idea

When the user shares an app idea:

1. **Ask the critical questions** (if not already answered):
   - Who is this for?
   - What's the one problem it solves?
   - How will you know if it works?

2. **Identify the core user loop**: What's the minimal flow a user must complete to get value?

3. **Draft the MVP scope**:
   - List only features required for the core loop
   - Flag features that should be deferred
   - Ensure build time estimate is under 1 week

4. **Create a structured PRD** following the template in `references/prd_template.md`. Include:
   - **Problem Statement**: One sentence defining the problem
   - **Target User**: Specific persona
   - **Success Metric**: How we'll measure if it works
   - **Core User Flow**: Step-by-step what the user does
   - **MVP Features**: Minimum required features with effort estimates
   - **Explicitly Out of Scope**: What we're NOT building yet
   - **Tech Stack**: Nuxt 3 or 4, Supabase, Vercel (unless otherwise specified)
   - **Launch Checklist**: Validation steps after shipping

### Create Claude Code Starter Prompts

When the user is ready to build:

Consult `references/claude_code_prompts.md` for templates, then generate a comprehensive starter prompt that includes:

1. **Project brief**: Problem, user, and core flow
2. **Tech stack specifics**: Nuxt 3 or 4 version, Supabase setup, Vercel config
3. **MVP feature list**: Clear, ordered by priority
4. **What NOT to build**: Explicit list of deferred features
5. **File structure**: Suggested Nuxt 3 or 4 project organization
6. **First milestone**: Smallest deployable version
7. **Validation criteria**: How to know if the MVP is working

Format the prompt as a direct instruction to Claude Code.

### Provide Product Decision Advice

When the user asks about adding a feature or making a product decision:

1. **Consult** `references/common_decisions.md` for standard guidance on common questions
2. **Apply the Essential Features Test**: Does it serve the core loop?
3. **Check against common mistakes**: Is this over-engineering or premature optimization?
4. **Suggest the minimal version**: What's the simplest way to test this hypothesis?
5. **Remind them of the goal**: Ship fast, validate with real users

### Keep User Focused on Shipping

Throughout the build, watch for signs of scope creep:
- Adding "nice-to-have" features
- Perfecting details that don't affect validation
- Building for scale prematurely
- Adding complexity for edge cases

When detected, gently redirect:
1. Acknowledge the idea has merit
2. Explain why it's not MVP-critical
3. Suggest deferring until after validation
4. Refocus on the core loop and launch
