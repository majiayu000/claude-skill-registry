---
name: spec-builder
description: Interactive specification builder for autonomous coding projects. Use when users have vague ideas, need help defining requirements, want to create project specs, or before running autonomous-master.
version: 1.0.0
category: autonomous-coding
layer: pre-orchestration
triggers:
  - "help me build"
  - "I want to create"
  - "build spec"
  - "spec builder"
  - "what should I build"
  - "help me define"
  - "project idea"
---

# Spec Builder

**Transforms vague ideas into detailed specifications for autonomous coding.**

Takes users through guided discovery to create complete, actionable specs ready for `autonomous start:`.

## Quick Start

### Start Spec Building
```
I want to build a todo app
```
or
```
build spec: project management tool
```
or
```
help me define what I want to build
```

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                      SPEC BUILDER FLOW                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  USER INPUT                                                      │
│  "I want to build something like Notion"                        │
│                         │                                        │
│                         ▼                                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  PHASE 1: DISCOVERY                                      │    │
│  │                                                          │    │
│  │  Q1: What type of application?                          │    │
│  │      → Workspace/productivity app                       │    │
│  │                                                          │    │
│  │  Q2: Who are the target users?                          │    │
│  │      → Teams and individuals                            │    │
│  │                                                          │    │
│  │  Q3: What are the 3-5 core features?                    │    │
│  │      → Pages, Editor, Collaboration, Search             │    │
│  │                                                          │    │
│  │  Q4: Any technology preferences?                        │    │
│  │      → Modern stack, real-time                          │    │
│  │                                                          │    │
│  │  Q5: Any constraints or requirements?                   │    │
│  │      → Must be self-hostable                            │    │
│  └─────────────────────────────────────────────────────────┘    │
│                         │                                        │
│                         ▼                                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  PHASE 2: ELABORATION                                    │    │
│  │                                                          │    │
│  │  For each core feature, expand:                         │    │
│  │  • Sub-features                                         │    │
│  │  • User stories                                         │    │
│  │  • Edge cases                                           │    │
│  │  • Integrations                                         │    │
│  │                                                          │    │
│  │  Pages:                                                  │    │
│  │  ├─ Hierarchical structure                              │    │
│  │  ├─ Page templates                                      │    │
│  │  ├─ Page sharing                                        │    │
│  │  └─ Page history/versioning                             │    │
│  └─────────────────────────────────────────────────────────┘    │
│                         │                                        │
│                         ▼                                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  PHASE 3: TECHNOLOGY RECOMMENDATION                      │    │
│  │                                                          │    │
│  │  Based on requirements, suggest:                        │    │
│  │  • Frontend: Next.js + TypeScript                       │    │
│  │  • Editor: Tiptap or Slate                              │    │
│  │  • Backend: Node.js + Prisma                            │    │
│  │  • Database: PostgreSQL                                 │    │
│  │  • Real-time: Socket.io or Liveblocks                   │    │
│  │  • Hosting: Vercel + Railway                            │    │
│  └─────────────────────────────────────────────────────────┘    │
│                         │                                        │
│                         ▼                                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  PHASE 4: SPECIFICATION OUTPUT                           │    │
│  │                                                          │    │
│  │  Generate complete spec ready for autonomous-master:    │    │
│  │                                                          │    │
│  │  ┌────────────────────────────────────────────────────┐ │    │
│  │  │ autonomous start: Build a collaborative workspace  │ │    │
│  │  │ application similar to Notion with:                │ │    │
│  │  │                                                    │ │    │
│  │  │ CORE FEATURES:                                     │ │    │
│  │  │ - Hierarchical pages with drag-and-drop           │ │    │
│  │  │ - Rich text editor with block-based content       │ │    │
│  │  │ - Real-time collaboration (multiple cursors)      │ │    │
│  │  │ - Full-text search across all content             │ │    │
│  │  │ - Sharing with granular permissions               │ │    │
│  │  │ ...                                               │ │    │
│  │  │                                                    │ │    │
│  │  │ TECHNOLOGY STACK:                                  │ │    │
│  │  │ - Next.js 14 with App Router                      │ │    │
│  │  │ - TypeScript                                       │ │    │
│  │  │ - Tiptap for rich text editor                     │ │    │
│  │  │ - Prisma + PostgreSQL                             │ │    │
│  │  │ - Socket.io for real-time                         │ │    │
│  │  └────────────────────────────────────────────────────┘ │    │
│  └─────────────────────────────────────────────────────────┘    │
│                         │                                        │
│                         ▼                                        │
│                  Ready for autonomous-master!                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Discovery Questions

### Core Questions (Always Asked)

| # | Question | Purpose |
|---|----------|---------|
| 1 | What type of application? | Categorize (web, mobile, API, etc.) |
| 2 | Who are the users? | Define audience and scale |
| 3 | What are 3-5 core features? | Identify must-haves |
| 4 | Technology preferences? | Constrain or open stack choices |
| 5 | Any constraints? | Budget, timeline, integrations |

### Follow-up Questions (Based on Answers)

| Trigger | Follow-up |
|---------|-----------|
| "authentication" mentioned | OAuth providers? SSO? MFA? |
| "payments" mentioned | Stripe? Subscriptions? One-time? |
| "real-time" mentioned | Chat? Notifications? Collaboration? |
| "mobile" mentioned | Native? PWA? React Native? |
| "API" mentioned | REST? GraphQL? Who consumes it? |

## Project Templates

Quick-start templates for common project types:

### SaaS Application
```
Template: saas
Includes:
- User auth with multi-tenancy
- Subscription billing
- Admin dashboard
- User settings
- API access
```

### E-Commerce
```
Template: ecommerce
Includes:
- Product catalog
- Shopping cart
- Checkout flow
- Order management
- Inventory tracking
```

### Social Platform
```
Template: social
Includes:
- User profiles
- Posts/content feed
- Likes/comments
- Follow system
- Notifications
```

### Internal Tool
```
Template: internal
Includes:
- SSO authentication
- Role-based access
- Data tables/CRUD
- Reports/dashboards
- Audit logging
```

## Usage Examples

### Example 1: Vague Idea
```
User: I want to build a todo app

Spec Builder: I'll help you define your todo app. Let me ask a few questions:

1. Who will use this? (personal, team, enterprise)
2. What makes it different from existing todo apps?
3. Any specific features you need? (recurring tasks, collaboration, etc.)
4. Web only or also mobile?

[After Q&A]

Generated Spec:
autonomous start: Build a collaborative task management app with:
- User authentication (email + Google OAuth)
- Personal and shared task lists
- Tasks with due dates, priorities, and labels
- Subtasks and checklists
- Recurring task support
- Real-time collaboration
- Mobile-responsive design
- Push notifications for due dates
Use Next.js, TypeScript, Prisma, PostgreSQL, and Tailwind CSS.
```

### Example 2: Clear Vision
```
User: build spec: Uber for dog walking

Spec Builder: Great concept! Let me clarify the specifics:

1. Two-sided marketplace (walkers + dog owners)?
2. Real-time tracking during walks?
3. Payment processing?
4. Scheduling (on-demand, recurring)?
5. Geographic scope?

[After Q&A]

Generated Spec:
autonomous start: Build an on-demand dog walking marketplace with:

DOG OWNER FEATURES:
- Registration with dog profiles
- Search nearby walkers with ratings
- Book on-demand or schedule recurring
- Real-time GPS tracking during walks
- In-app messaging with walkers
- Payment with saved cards
- Walk history and reports

WALKER FEATURES:
- Walker onboarding with background check
- Set availability and service area
- Accept/decline walk requests
- GPS tracking and walk logging
- Earnings dashboard
- Direct deposit payouts

ADMIN FEATURES:
- User management
- Dispute resolution
- Analytics dashboard

Use React Native (iOS + Android), Node.js, PostgreSQL,
Stripe Connect, Google Maps API, and Firebase for real-time.
```

## Integration with Autonomous-Master

After generating a spec:

```
┌─────────────────┐
│  SPEC-BUILDER   │
│                 │
│  [Generated     │
│   Spec]         │
└────────┬────────┘
         │
         │ Copy or auto-invoke
         ▼
┌─────────────────┐
│AUTONOMOUS-MASTER│
│                 │
│ autonomous      │
│ start: [spec]   │
└─────────────────┘
```

## Scripts

- `scripts/spec_builder.py` - Core discovery engine
- `scripts/question_engine.py` - Dynamic question generation
- `scripts/template_expander.py` - Template expansion
- `scripts/tech_recommender.py` - Technology recommendations
- `scripts/spec_formatter.py` - Format final specification

## References

- `references/QUESTION-BANK.md` - All discovery questions
- `references/TEMPLATES.md` - Project templates
- `references/TECH-STACKS.md` - Technology recommendations

## Templates

- `templates/saas.md` - SaaS application template
- `templates/ecommerce.md` - E-commerce template
- `templates/social.md` - Social platform template
- `templates/internal.md` - Internal tool template
