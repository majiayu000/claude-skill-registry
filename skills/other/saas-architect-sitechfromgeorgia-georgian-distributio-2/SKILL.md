---
name: saas-architect
description: Comprehensive SaaS architecture planner for Next.js + Supabase applications. Converts ideas into production-ready technical plans with database schemas, file structures, feature breakdowns, and week-by-week development roadmaps. Use when planning subscription-based applications, multi-tenant SaaS products, or building from idea to launch.
---

# SaaS Architect - Next.js + Supabase Edition

## Purpose

This skill transforms SaaS ideas into executable technical architectures optimized for Next.js 15 + Supabase stack. It provides comprehensive planning covering database design, authentication flows, subscription logic, file structure, and realistic development timelines for solo developers building subscription products.

## Core Philosophy

### 1. Subscription-First Architecture
- Design for recurring revenue from day one
- Plan for multiple pricing tiers
- Build upgrade/downgrade flows early
- Consider trial periods and grace periods

### 2. Multi-Tenant by Default
- Row Level Security (RLS) is mandatory
- Organizations/Teams structure built-in
- User roles and permissions from start
- Data isolation is non-negotiable

### 3. Next.js 15 + Supabase Optimized
- Use Server Components for data fetching
- Leverage Server Actions for mutations
- Utilize Supabase's built-in features (Auth, Storage, Realtime)
- Minimize custom backend code

### 4. Production-Ready from Start
- Security considerations upfront
- Scalability patterns built-in
- Monitoring and error tracking planned
- Deployment strategy defined

## How This Skill Works

### Phase 1: SaaS Product Definition

#### 1.1 Core Value Proposition
```markdown
**Product Name:** [Name]
**One-Line Pitch:** [What it does in one sentence]
**Target Market:** [Who pays for this]
**Primary Use Case:** [Main problem solved]
**Success Metric:** [How you measure value]
```

#### 1.2 Revenue Model
```markdown
**Pricing Strategy:** [Freemium / Trial / Pay-to-start]
**Tiers:** [How many pricing tiers]
**Key Differentiators:** [What makes higher tiers worth it]
**Billing Cycle:** [Monthly / Annual / Both]
```

**Example (Project Management SaaS):**
```markdown
**Product Name:** TaskFlow
**One-Line Pitch:** Project management for distributed teams with AI-powered task prioritization
**Target Market:** Remote teams, 10-50 employees, tech companies
**Primary Use Case:** Coordinate async work across timezones
**Success Metric:** Teams complete 30% more tasks on time

**Pricing Strategy:** Freemium with 14-day trial on paid plans
**Tiers:** 
  - Free: 1 project, 5 users, basic features
  - Pro ($29/mo): Unlimited projects, 25 users, AI features
  - Enterprise ($99/mo): Unlimited users, advanced integrations, priority support
**Key Differentiators:** 
  - Pro: AI task prioritization, integrations
  - Enterprise: SSO, custom workflows, dedicated support
**Billing Cycle:** Monthly + Annual (2 months free)
```

### Phase 2: Technical Architecture Planning

#### 2.1 Database Schema Design

The skill generates complete PostgreSQL schemas with RLS policies:

**Core Tables for Every SaaS:**

```sql
-- ============================================
-- USERS & AUTHENTICATION
-- ============================================
-- Note: Supabase Auth handles auth.users table
-- We extend it with profiles

CREATE TABLE profiles (
  id UUID REFERENCES auth.users PRIMARY KEY,
  email TEXT NOT NULL,
  full_name TEXT,
  avatar_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS Policies
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile"
  ON profiles FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE
  USING (auth.uid() = id);

-- ============================================
-- ORGANIZATIONS (Multi-Tenant Core)
-- ============================================
CREATE TABLE organizations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  logo_url TEXT,
  subscription_tier TEXT DEFAULT 'free',
  subscription_status TEXT DEFAULT 'active',
  trial_ends_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE organizations ENABLE ROW LEVEL SECURITY;

-- ============================================
-- ORGANIZATION MEMBERS (Team Management)
-- ============================================
CREATE TYPE member_role AS ENUM ('owner', 'admin', 'member');

CREATE TABLE organization_members (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  role member_role DEFAULT 'member',
  invited_by UUID REFERENCES auth.users(id),
  joined_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(organization_id, user_id)
);

ALTER TABLE organization_members ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Members can view own org members"
  ON organization_members FOR SELECT
  USING (
    organization_id IN (
      SELECT organization_id FROM organization_members 
      WHERE user_id = auth.uid()
    )
  );

-- ============================================
-- STRIPE INTEGRATION (Subscriptions)
-- ============================================
CREATE TABLE customers (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
  stripe_customer_id TEXT UNIQUE,
  email TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE products (
  id TEXT PRIMARY KEY, -- Stripe product ID
  active BOOLEAN DEFAULT true,
  name TEXT NOT NULL,
  description TEXT,
  image TEXT,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE prices (
  id TEXT PRIMARY KEY, -- Stripe price ID
  product_id TEXT REFERENCES products(id),
  active BOOLEAN DEFAULT true,
  currency TEXT DEFAULT 'usd',
  type TEXT CHECK (type IN ('one_time', 'recurring')),
  unit_amount BIGINT,
  interval TEXT CHECK (interval IN ('day', 'week', 'month', 'year')),
  interval_count INTEGER,
  trial_period_days INTEGER,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE subscriptions (
  id TEXT PRIMARY KEY, -- Stripe subscription ID
  organization_id UUID REFERENCES organizations(id),
  customer_id TEXT REFERENCES customers(stripe_customer_id),
  status TEXT NOT NULL,
  price_id TEXT REFERENCES prices(id),
  quantity INTEGER,
  cancel_at_period_end BOOLEAN DEFAULT false,
  current_period_start TIMESTAMPTZ,
  current_period_end TIMESTAMPTZ,
  trial_start TIMESTAMPTZ,
  trial_end TIMESTAMPTZ,
  canceled_at TIMESTAMPTZ,
  ended_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS for subscription data
ALTER TABLE customers ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Org owners can view own subscription"
  ON subscriptions FOR SELECT
  USING (
    organization_id IN (
      SELECT organization_id FROM organization_members 
      WHERE user_id = auth.uid() AND role IN ('owner', 'admin')
    )
  );

-- ============================================
-- FEATURE-SPECIFIC TABLES
-- ============================================
-- This section is customized based on your SaaS features
-- Example: Project Management SaaS

CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  status TEXT DEFAULT 'active',
  created_by UUID REFERENCES auth.users(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Org members can view org projects"
  ON projects FOR SELECT
  USING (
    organization_id IN (
      SELECT organization_id FROM organization_members 
      WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Org members can create projects"
  ON projects FOR INSERT
  WITH CHECK (
    organization_id IN (
      SELECT organization_id FROM organization_members 
      WHERE user_id = auth.uid()
    )
  );

CREATE TABLE tasks (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  description TEXT,
  status TEXT DEFAULT 'todo',
  priority TEXT DEFAULT 'medium',
  assigned_to UUID REFERENCES auth.users(id),
  due_date TIMESTAMPTZ,
  created_by UUID REFERENCES auth.users(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Org members can view org tasks"
  ON tasks FOR SELECT
  USING (
    project_id IN (
      SELECT id FROM projects 
      WHERE organization_id IN (
        SELECT organization_id FROM organization_members 
        WHERE user_id = auth.uid()
      )
    )
  );
```

#### 2.2 Next.js File Structure

The skill generates production-ready file structures:

```
your-saas-app/
├── app/
│   ├── (auth)/                          # Auth layout group
│   │   ├── login/
│   │   │   └── page.tsx                 # Login page
│   │   ├── signup/
│   │   │   └── page.tsx                 # Signup page
│   │   ├── forgot-password/
│   │   │   └── page.tsx
│   │   └── layout.tsx                   # Auth pages layout
│   │
│   ├── (dashboard)/                     # Protected dashboard routes
│   │   ├── layout.tsx                   # Dashboard shell (sidebar, nav)
│   │   ├── page.tsx                     # Dashboard home
│   │   │
│   │   ├── [orgSlug]/                   # Organization-specific routes
│   │   │   ├── projects/
│   │   │   │   ├── page.tsx             # Projects list
│   │   │   │   ├── [id]/
│   │   │   │   │   └── page.tsx         # Single project view
│   │   │   │   └── new/
│   │   │   │       └── page.tsx         # Create project
│   │   │   │
│   │   │   ├── tasks/
│   │   │   │   ├── page.tsx
│   │   │   │   └── [id]/page.tsx
│   │   │   │
│   │   │   ├── team/
│   │   │   │   ├── page.tsx             # Team members
│   │   │   │   └── invite/page.tsx      # Invite flow
│   │   │   │
│   │   │   └── settings/
│   │   │       ├── page.tsx             # Org settings
│   │   │       ├── billing/
│   │   │       │   └── page.tsx         # Subscription management
│   │   │       └── members/
│   │   │           └── page.tsx         # Member management
│   │   │
│   │   └── onboarding/                  # Post-signup onboarding
│   │       ├── page.tsx
│   │       └── create-org/page.tsx
│   │
│   ├── (marketing)/                     # Public pages
│   │   ├── page.tsx                     # Landing page
│   │   ├── pricing/
│   │   │   └── page.tsx                 # Pricing page
│   │   ├── about/
│   │   │   └── page.tsx
│   │   └── layout.tsx                   # Marketing layout
│   │
│   ├── api/                             # API routes
│   │   ├── stripe/
│   │   │   ├── checkout/
│   │   │   │   └── route.ts             # Create checkout session
│   │   │   ├── portal/
│   │   │   │   └── route.ts             # Customer portal
│   │   │   └── webhook/
│   │   │       └── route.ts             # Stripe webhooks
│   │   │
│   │   └── webhooks/
│   │       └── supabase/
│   │           └── route.ts             # Supabase webhooks
│   │
│   ├── globals.css
│   └── layout.tsx                       # Root layout
│
├── components/
│   ├── ui/                              # shadcn/ui components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── dialog.tsx
│   │   ├── dropdown-menu.tsx
│   │   ├── form.tsx
│   │   ├── input.tsx
│   │   ├── table.tsx
│   │   └── ...
│   │
│   ├── layouts/
│   │   ├── dashboard-shell.tsx          # Dashboard wrapper
│   │   ├── marketing-header.tsx
│   │   └── marketing-footer.tsx
│   │
│   ├── auth/
│   │   ├── login-form.tsx
│   │   ├── signup-form.tsx
│   │   └── auth-guard.tsx               # Protected route wrapper
│   │
│   ├── billing/
│   │   ├── pricing-card.tsx
│   │   ├── subscription-status.tsx
│   │   └── usage-meter.tsx
│   │
│   ├── organizations/
│   │   ├── org-switcher.tsx             # Switch between orgs
│   │   ├── org-selector.tsx
│   │   └── invite-member-dialog.tsx
│   │
│   └── features/                        # Feature-specific components
│       ├── projects/
│       │   ├── project-list.tsx
│       │   ├── project-card.tsx
│       │   └── create-project-dialog.tsx
│       └── tasks/
│           ├── task-list.tsx
│           ├── task-card.tsx
│           └── task-form.tsx
│
├── lib/
│   ├── supabase/
│   │   ├── client.ts                    # Browser client
│   │   ├── server.ts                    # Server client
│   │   ├── middleware.ts                # Auth middleware
│   │   └── types.ts                     # Generated types
│   │
│   ├── stripe/
│   │   ├── client.ts                    # Stripe initialization
│   │   ├── products.ts                  # Product/price helpers
│   │   └── webhooks.ts                  # Webhook handlers
│   │
│   ├── hooks/
│   │   ├── use-user.ts                  # Get current user
│   │   ├── use-organization.ts          # Get current org
│   │   ├── use-subscription.ts          # Get subscription status
│   │   └── use-permissions.ts           # Check user permissions
│   │
│   ├── actions/                         # Server Actions
│   │   ├── auth.actions.ts
│   │   ├── org.actions.ts
│   │   ├── subscription.actions.ts
│   │   └── features/
│   │       ├── projects.actions.ts
│   │       └── tasks.actions.ts
│   │
│   └── utils/
│       ├── permissions.ts               # Permission checking
│       ├── rate-limit.ts                # Rate limiting
│       └── errors.ts                    # Error handling
│
├── types/
│   ├── database.types.ts                # Generated from Supabase
│   ├── stripe.types.ts
│   └── app.types.ts
│
├── middleware.ts                        # Next.js middleware (auth)
├── .env.local
├── .env.example
├── next.config.js
├── package.json
├── tailwind.config.ts
└── tsconfig.json
```

### Phase 3: Feature Planning & Breakdown

The skill breaks down SaaS features into implementable chunks:

#### 3.1 Core SaaS Features (Must Have)

**Authentication & User Management**
```markdown
## Auth Flow
**User Stories:**
- As a user, I can sign up with email/password
- As a user, I can sign in with OAuth (Google, GitHub)
- As a user, I can reset my password
- As a user, I can update my profile

**Technical Implementation:**
- Supabase Auth handles all authentication
- Magic link email for password reset
- OAuth providers configured in Supabase dashboard
- Profile updates via Server Actions

**Acceptance Criteria:**
- [ ] Users can create accounts
- [ ] Email verification works
- [ ] Password reset flow functional
- [ ] OAuth providers work
- [ ] Sessions persist across refreshes
- [ ] Logout clears session

**Time Estimate:** 2-3 days
```

**Organization Management**
```markdown
## Multi-Tenant Organizations
**User Stories:**
- As a user, I can create an organization
- As an owner, I can invite team members
- As a member, I can accept invitations
- As an owner, I can manage member roles
- As a user, I can switch between organizations

**Technical Implementation:**
- Organizations table with RLS
- Invitation system via email
- Role-based access control (owner, admin, member)
- Organization switcher component
- Invites expire after 7 days

**Acceptance Criteria:**
- [ ] Users can create orgs with unique slugs
- [ ] Owners can invite via email
- [ ] Invites create pending records
- [ ] Members can accept/decline
- [ ] Role changes reflect immediately
- [ ] Users can switch orgs via dropdown

**Time Estimate:** 3-4 days
```

**Subscription & Billing**
```markdown
## Stripe Subscription Flow
**User Stories:**
- As a user, I can view pricing plans
- As an org owner, I can subscribe to a plan
- As an org owner, I can upgrade/downgrade
- As an org owner, I can manage billing
- As an org owner, I can cancel subscription

**Technical Implementation:**
- Stripe Checkout for subscriptions
- Webhook handler for subscription events
- Customer Portal for self-service billing
- Trial period (14 days)
- Graceful downgrade handling

**Acceptance Criteria:**
- [ ] Pricing page shows all plans
- [ ] Checkout flow works end-to-end
- [ ] Webhooks update subscription status
- [ ] Features respect subscription tier
- [ ] Portal allows plan changes
- [ ] Cancellation handles end of period

**Time Estimate:** 4-5 days
```

#### 3.2 Feature-Specific Planning

The skill generates custom feature breakdowns based on your SaaS:

**Example: Project Management Features**

```markdown
## Projects Feature
**User Stories:**
- As a member, I can view all org projects
- As a member, I can create new projects
- As a member, I can update project details
- As an admin, I can archive projects

**Database:**
- `projects` table with org relationship
- RLS policies for org-based access

**Components:**
- ProjectList (with search/filter)
- ProjectCard (preview)
- CreateProjectDialog (form)
- ProjectSettings (edit)

**API:**
- GET /api/projects?orgId=xxx
- POST /api/projects
- PATCH /api/projects/:id
- DELETE /api/projects/:id

**Time Estimate:** 3 days

## Tasks Feature
**User Stories:**
- As a member, I can create tasks in projects
- As a member, I can assign tasks
- As an assignee, I can update task status
- As a member, I can set due dates

**Database:**
- `tasks` table with project relationship
- Status enum (todo, in_progress, done)
- Priority enum (low, medium, high)

**Components:**
- TaskList (kanban or table view)
- TaskCard (draggable)
- CreateTaskDialog (form)
- TaskDetailView (modal)

**Time Estimate:** 3-4 days
```

### Phase 4: Development Roadmap

The skill generates realistic week-by-week plans:

#### Week 1: Foundation & Auth
```markdown
## Days 1-2: Project Setup
**Tasks:**
- [ ] Create Next.js 15 project with TypeScript
- [ ] Install dependencies (Supabase, Stripe, shadcn/ui, Zod)
- [ ] Set up Supabase project
- [ ] Configure environment variables
- [ ] Set up database schema (run SQL)
- [ ] Configure RLS policies
- [ ] Generate TypeScript types from database

**Deliverable:** Empty project with database ready

## Days 3-4: Authentication
**Tasks:**
- [ ] Implement Supabase Auth
- [ ] Create login/signup pages
- [ ] Add OAuth providers (Google, GitHub)
- [ ] Build auth middleware
- [ ] Create protected route wrapper
- [ ] Add password reset flow
- [ ] Style auth pages with shadcn/ui

**Deliverable:** Working authentication system

## Day 5: User Profiles
**Tasks:**
- [ ] Create profile page
- [ ] Implement profile update form
- [ ] Add avatar upload (Supabase Storage)
- [ ] Build user settings page

**Deliverable:** Users can manage profiles

## Weekend: Buffer
- Fix any blocking issues
- Test auth flows
- Start organization setup
```

#### Week 2: Organizations & Teams
```markdown
## Days 1-2: Organization Core
**Tasks:**
- [ ] Create org creation flow
- [ ] Build org switcher component
- [ ] Implement org slug validation
- [ ] Add org settings page
- [ ] Create org context/provider

**Deliverable:** Organizations functional

## Days 3-4: Team Management
**Tasks:**
- [ ] Build invitation system
- [ ] Create invite email templates
- [ ] Implement role management
- [ ] Add member list page
- [ ] Build invite acceptance flow

**Deliverable:** Team collaboration works

## Day 5: Polish
**Tasks:**
- [ ] Add loading states
- [ ] Improve error handling
- [ ] Add toast notifications
- [ ] Test org workflows

**Weekend:** Integration testing
```

#### Week 3: Stripe Integration
```markdown
## Days 1-2: Stripe Setup
**Tasks:**
- [ ] Set up Stripe account
- [ ] Create products and prices
- [ ] Implement webhook endpoint
- [ ] Test webhook locally (Stripe CLI)
- [ ] Add webhook handlers for key events

**Deliverable:** Stripe connected

## Days 3-4: Subscription Flow
**Tasks:**
- [ ] Build pricing page
- [ ] Implement checkout flow
- [ ] Create success/cancel pages
- [ ] Add subscription status indicator
- [ ] Implement Customer Portal link

**Deliverable:** Subscriptions work end-to-end

## Day 5: Feature Gates
**Tasks:**
- [ ] Add subscription checking middleware
- [ ] Implement usage limits per tier
- [ ] Build upgrade prompts
- [ ] Add billing page to dashboard

**Weekend:** Test all subscription scenarios
```

#### Week 4: Core Features
```markdown
## Days 1-3: Primary Feature (e.g., Projects)
**Tasks:**
- [ ] Build CRUD operations
- [ ] Create list/detail views
- [ ] Add search and filtering
- [ ] Implement Server Actions
- [ ] Add optimistic updates

**Deliverable:** Primary feature functional

## Days 4-5: Secondary Feature (e.g., Tasks)
**Tasks:**
- [ ] Build basic CRUD
- [ ] Create list view
- [ ] Add quick actions
- [ ] Implement status updates

**Weekend:** Feature testing and polish
```

#### Week 5: Polish & Launch Prep
```markdown
## Days 1-2: UX Polish
**Tasks:**
- [ ] Add loading skeletons
- [ ] Improve error messages
- [ ] Add empty states
- [ ] Implement toast notifications
- [ ] Add confirmation dialogs

## Days 3-4: Testing & Bugs
**Tasks:**
- [ ] Test all user flows
- [ ] Fix critical bugs
- [ ] Test mobile responsiveness
- [ ] Check cross-browser compatibility

## Day 5: Deploy
**Tasks:**
- [ ] Set up Vercel project
- [ ] Configure production environment variables
- [ ] Set up Stripe webhook in production
- [ ] Deploy to production
- [ ] Test production deployment

**Weekend:** Monitor, fix critical issues
```

### Phase 5: Security & Best Practices

The skill enforces security patterns:

#### 5.1 Row Level Security (RLS) Patterns

```sql
-- Pattern 1: User owns resource
CREATE POLICY "Users can only access own data"
  ON table_name FOR ALL
  USING (user_id = auth.uid());

-- Pattern 2: Org member access
CREATE POLICY "Org members can access org data"
  ON table_name FOR SELECT
  USING (
    organization_id IN (
      SELECT organization_id FROM organization_members 
      WHERE user_id = auth.uid()
    )
  );

-- Pattern 3: Role-based access
CREATE POLICY "Only admins can delete"
  ON table_name FOR DELETE
  USING (
    organization_id IN (
      SELECT organization_id FROM organization_members 
      WHERE user_id = auth.uid() 
      AND role IN ('owner', 'admin')
    )
  );

-- Pattern 4: Resource creator can update
CREATE POLICY "Creator can update"
  ON table_name FOR UPDATE
  USING (created_by = auth.uid());
```

#### 5.2 Server Action Security

```typescript
// lib/actions/secure-action.ts
import { createClient } from '@/lib/supabase/server';
import { redirect } from 'next/navigation';

export async function secureAction(
  handler: (userId: string, orgId: string) => Promise<any>
) {
  const supabase = await createClient();
  
  // 1. Verify authentication
  const { data: { user }, error } = await supabase.auth.getUser();
  
  if (error || !user) {
    redirect('/login');
  }
  
  // 2. Get current organization
  const { data: membership } = await supabase
    .from('organization_members')
    .select('organization_id')
    .eq('user_id', user.id)
    .single();
    
  if (!membership) {
    throw new Error('No organization access');
  }
  
  // 3. Execute handler with verified context
  return handler(user.id, membership.organization_id);
}

// Usage in Server Actions
export async function createProject(formData: FormData) {
  'use server';
  
  return secureAction(async (userId, orgId) => {
    const name = formData.get('name') as string;
    
    // Validation
    if (!name || name.length < 3) {
      return { error: 'Name must be at least 3 characters' };
    }
    
    // Database operation (RLS will further verify access)
    const supabase = await createClient();
    const { data, error } = await supabase
      .from('projects')
      .insert({
        name,
        organization_id: orgId,
        created_by: userId
      })
      .select()
      .single();
      
    if (error) {
      return { error: error.message };
    }
    
    return { data };
  });
}
```

#### 5.3 API Route Security

```typescript
// app/api/stripe/webhook/route.ts
import { headers } from 'next/headers';
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);
const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET!;

export async function POST(req: Request) {
  const body = await req.text();
  const signature = headers().get('stripe-signature');

  if (!signature) {
    return new Response('No signature', { status: 400 });
  }

  try {
    // Verify webhook signature
    const event = stripe.webhooks.constructEvent(
      body,
      signature,
      webhookSecret
    );

    // Handle different events
    switch (event.type) {
      case 'checkout.session.completed':
        await handleCheckoutComplete(event.data.object);
        break;
      case 'customer.subscription.updated':
        await handleSubscriptionUpdate(event.data.object);
        break;
      case 'customer.subscription.deleted':
        await handleSubscriptionCancel(event.data.object);
        break;
    }

    return new Response(JSON.stringify({ received: true }));
  } catch (err) {
    console.error('Webhook error:', err);
    return new Response('Webhook error', { status: 400 });
  }
}
```

### Phase 6: Deployment & Monitoring

#### 6.1 Environment Variables

```bash
# .env.example
# Supabase
NEXT_PUBLIC_SUPABASE_URL=your-project-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Stripe
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_xxx
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# App
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_APP_NAME=YourSaaS

# Email (optional)
RESEND_API_KEY=re_xxx
```

#### 6.2 Vercel Deployment Checklist

```markdown
## Pre-Deploy
- [ ] All environment variables set in Vercel
- [ ] Supabase RLS policies tested
- [ ] Stripe webhook URL configured for production
- [ ] Production Stripe keys configured
- [ ] Error tracking set up (Sentry)
- [ ] Analytics configured (PostHog, Plausible)

## Deploy
- [ ] Push to main branch
- [ ] Verify build succeeds
- [ ] Check production URL
- [ ] Test critical flows in production

## Post-Deploy
- [ ] Monitor error rates
- [ ] Check webhook delivery
- [ ] Verify subscription flows
- [ ] Test on mobile devices
```

## Output Format

When you request SaaS architecture planning, the skill provides:

```markdown
# [Your SaaS Name] - Technical Architecture Document

## Executive Summary
[2-3 paragraphs: what you're building, for whom, tech stack]

## Product Overview
**Name:** [Product Name]
**Target:** [Target Audience]
**Value Prop:** [One-liner]
**Revenue Model:** [Pricing strategy]

## Technical Stack
- **Frontend:** Next.js 15 (App Router) + TypeScript + Tailwind CSS
- **UI Components:** shadcn/ui
- **Backend:** Next.js Server Actions + API Routes
- **Database:** PostgreSQL (Supabase)
- **Auth:** Supabase Auth
- **Payments:** Stripe
- **Storage:** Supabase Storage
- **Hosting:** Vercel
- **Email:** Resend (optional)

## Database Architecture
[Complete SQL schema with RLS policies]

## File Structure
[Full Next.js directory structure]

## Feature Breakdown

### Core SaaS Features (Week 1-3)
[Authentication, Organizations, Subscriptions]

### Product Features (Week 4-6)
[Your specific features broken down]

## Development Roadmap
[Week-by-week plan with tasks and deliverables]

## Security Considerations
[RLS patterns, authentication flows, API security]

## Deployment Strategy
[Vercel setup, environment variables, monitoring]

## Success Metrics
- **Activation:** [First meaningful action]
- **Engagement:** [Regular usage indicator]
- **Retention:** [Return behavior]
- **Revenue:** [MRR growth targets]

## Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk 1] | [High/Med/Low] | [How to handle] |

## Next Steps
1. [First actionable task]
2. [Second task]
3. [Third task]
```

## How to Use This Skill

### Basic Usage
```
I need architecture for a SaaS product.

Use saas-architect skill.

Idea: [Your SaaS idea]
Target Users: [Who]
Pricing: [How you'll charge]
```

### Detailed Planning
```
Create complete SaaS architecture plan using saas-architect.

Product: [Detailed description]
Features: [List key features]
Timeline: [Launch target]
Constraints: [Any technical/business constraints]
```

### Feature-Specific Planning
```
I have existing SaaS, need to add [feature].

Use saas-architect to plan:
- Database changes needed
- File structure for feature
- Implementation steps
- Timeline estimate

Existing Stack: Next.js 15 + Supabase
```

## Integration with Development

### With Claude Code
After generating architecture, use with Claude Code:

```
Generate starter code for this SaaS architecture:

[Paste architecture document]

Start with:
1. Database schema (run SQL in Supabase)
2. Initial project structure
3. Auth implementation
4. Organization setup
```

### With Other Skills
**Recommended workflow:**

1. **idea-validator-pro** → Validate market fit
2. **saas-architect** → Technical planning
3. **modern-ui-designer** → Design system
4. **Claude Code** → Implementation
5. **code-quality-guardian** → Code review
6. **deployment-automation** → Launch

## Best Practices

### DO ✅
- **Start with Core SaaS Features**: Auth, Orgs, Subscriptions first
- **Use RLS Everywhere**: Never skip Row Level Security
- **Test Subscriptions Early**: Stripe webhooks are critical
- **Plan for Multi-Tenancy**: Even if starting single-tenant
- **Document Decisions**: Future you will thank you

### DON'T ❌
- **Skip RLS Policies**: Data leaks are catastrophic
- **Hardcode Stripe Keys**: Use environment variables
- **Ignore Webhook Testing**: Test webhooks locally first
- **Over-Engineer**: Start simple, scale later
- **Build Without Auth**: Start with authentication

## Common Scenarios

### Scenario 1: Freemium SaaS
```
Challenge: Need free tier with upgrade path
Solution: 
- Free tier with feature limits
- Trial period for paid plans
- Usage tracking in database
- Upgrade prompts in UI
```

### Scenario 2: Team Collaboration
```
Challenge: Multiple users per organization
Solution:
- Organization-based RLS
- Role-based permissions
- Invitation system
- Activity logging
```

### Scenario 3: Usage-Based Pricing
```
Challenge: Charge based on usage, not seats
Solution:
- Usage tracking table
- Metered billing with Stripe
- Usage dashboards
- Overage handling
```

## Technical Debt Prevention

### Phase 1 (Weeks 1-2): None Expected
Focus on getting foundation right.

### Phase 2 (Weeks 3-4): Monitor These
- Test coverage (aim for >70% on critical paths)
- Error handling consistency
- Loading state patterns

### Phase 3 (Weeks 5-6): Refactor Time
- Extract reusable hooks
- Consolidate similar components
- Optimize database queries
- Add missing indexes

## Launch Checklist

### Pre-Launch (1 Week Before)
- [ ] All core features working
- [ ] Mobile responsive tested
- [ ] Cross-browser tested
- [ ] Payment flow tested end-to-end
- [ ] Error tracking configured
- [ ] Analytics set up
- [ ] Terms of Service ready
- [ ] Privacy Policy ready
- [ ] Support email configured

### Launch Day
- [ ] Deploy to production
- [ ] Verify all webhooks working
- [ ] Test signup flow
- [ ] Test subscription flow
- [ ] Monitor error rates
- [ ] Check analytics tracking

### Post-Launch (First Week)
- [ ] Daily monitoring
- [ ] Fix critical bugs
- [ ] Gather user feedback
- [ ] Iterate on pain points

---

## Skill Metadata

**Version:** 1.0.0  
**Last Updated:** November 2025  
**Optimized For:** Next.js 15, Supabase, Stripe  
**Target:** Solo Developers building SaaS products  
**Output:** Complete technical architecture documentation  

---

**Key Insight**: Great SaaS architecture isn't about having every feature—it's about building the right foundation that scales. Focus on authentication, multi-tenancy, and subscriptions first. Everything else can iterate.
