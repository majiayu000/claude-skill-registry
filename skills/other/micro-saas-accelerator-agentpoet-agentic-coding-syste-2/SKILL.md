---
name: Micro-SaaS Accelerator
description: Rapidly build and launch micro-SaaS applications with best practices, monetization, and deployment
triggers:
  - "micro-saas"
  - "saas mvp"
  - "launch saas"
  - "build saas"
  - "saas accelerator"
---

# Micro-SaaS Accelerator Skill

Rapidly build, launch, and scale micro-SaaS applications following proven patterns and best practices.

## What is a Micro-SaaS?

A **micro-SaaS** is a small, focused Software-as-a-Service business that:
- Solves ONE specific problem extremely well
- Can be built and maintained by 1-5 people
- Targets a niche audience
- Generates $1K-$50K MRR
- Requires minimal ongoing maintenance

## Core Capabilities

- MVP development (ship in 2-4 weeks)
- Authentication & user management
- Payment integration (Stripe/LemonSqueezy)
- Database schema design for SaaS
- Landing page & onboarding flows
- Usage tracking & analytics
- Email notifications
- API development
- Multi-tenancy setup
- Deployment & CI/CD

## Proven Tech Stack

### Frontend
```typescript
Next.js 14+ (App Router)
  + TypeScript
  + Tailwind CSS
  + shadcn/ui components
  + Framer Motion (animations)
```

### Backend & Database
```typescript
Supabase
  + PostgreSQL (database)
  + Auth (built-in)
  + Row Level Security (RLS)
  + Realtime subscriptions
  + Storage (files)
```

### Payments
```typescript
Stripe or LemonSqueezy
  + Checkout sessions
  + Webhooks
  + Subscription management
  + Customer portal
```

### Deployment
```bash
Vercel (frontend + API routes)
  + Automatic deployments
  + Preview environments
  + Edge functions
  + Analytics
```

## Rapid MVP Development Process

### Week 1: Foundation
```bash
Day 1-2: Project Setup
- Initialize Next.js 14 project
- Configure Supabase project
- Set up database schema
- Configure authentication

Day 3-4: Core Feature
- Implement main value proposition
- Build essential UI components
- Connect frontend to backend
- Add basic error handling

Day 5-7: User Flow
- Landing page
- Sign up/sign in
- Onboarding flow
- Dashboard layout
```

### Week 2: Polish & Launch
```bash
Day 8-10: Monetization
- Stripe integration
- Subscription plans
- Payment webhooks
- Customer portal

Day 11-13: Essential Features
- Usage limits enforcement
- Email notifications
- User settings
- Basic analytics

Day 14: Launch Prep
- Production deployment
- Domain setup
- Basic documentation
- Launch checklist completion
```

## Database Schema Pattern

### Core SaaS Tables
```sql
-- Users (managed by Supabase Auth)
-- Just extend with profile data

-- User profiles
CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id),
  email TEXT,
  full_name TEXT,
  avatar_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Subscriptions
CREATE TABLE subscriptions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id),
  stripe_customer_id TEXT UNIQUE,
  stripe_subscription_id TEXT UNIQUE,
  status TEXT NOT NULL, -- 'active', 'canceled', 'past_due'
  plan_id TEXT NOT NULL, -- 'free', 'pro', 'enterprise'
  current_period_end TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Usage tracking
CREATE TABLE usage (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id),
  resource_type TEXT NOT NULL,
  amount INTEGER DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Main resource (replace with your core entity)
CREATE TABLE resources (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id),
  title TEXT NOT NULL,
  content JSONB,
  status TEXT DEFAULT 'active',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS on ALL tables
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE usage ENABLE ROW LEVEL SECURITY;
ALTER TABLE resources ENABLE ROW LEVEL SECURITY;

-- Basic RLS policies
CREATE POLICY "Users can view own profile"
  ON profiles FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE
  USING (auth.uid() = id);

-- Repeat for other tables...
```

## Authentication Setup

### Supabase Auth Configuration
```typescript
// lib/supabase.ts
import { createClientComponentClient } from '@supabase/auth-helpers-nextjs'

export const supabase = createClientComponentClient()

// Protected route middleware
// middleware.ts
import { createMiddlewareClient } from '@supabase/auth-helpers-nextjs'
import { NextResponse } from 'next/server'

export async function middleware(req) {
  const res = NextResponse.next()
  const supabase = createMiddlewareClient({ req, res })
  const { data: { session } } = await supabase.auth.getSession()

  if (!session && req.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', req.url))
  }

  return res
}
```

## Payment Integration

### Stripe Setup (Recommended)
```typescript
// lib/stripe.ts
import Stripe from 'stripe'

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2023-10-16',
})

// API route: /api/create-checkout
export async function POST(req: Request) {
  const { priceId, userId } = await req.json()

  const session = await stripe.checkout.sessions.create({
    mode: 'subscription',
    payment_method_types: ['card'],
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${process.env.NEXT_PUBLIC_URL}/dashboard?success=true`,
    cancel_url: `${process.env.NEXT_PUBLIC_URL}/pricing?canceled=true`,
    client_reference_id: userId,
  })

  return Response.json({ url: session.url })
}

// API route: /api/webhooks/stripe
export async function POST(req: Request) {
  const sig = req.headers.get('stripe-signature')!
  const body = await req.text()

  const event = stripe.webhooks.constructEvent(
    body,
    sig,
    process.env.STRIPE_WEBHOOK_SECRET!
  )

  switch (event.type) {
    case 'checkout.session.completed':
      // Create subscription record
      break
    case 'customer.subscription.updated':
      // Update subscription status
      break
    case 'customer.subscription.deleted':
      // Cancel subscription
      break
  }

  return Response.json({ received: true })
}
```

## Usage Limits Enforcement

### Check and Enforce Limits
```typescript
// lib/usage-limits.ts
const PLAN_LIMITS = {
  free: { resources: 5, api_calls: 100 },
  pro: { resources: 100, api_calls: 10000 },
  enterprise: { resources: -1, api_calls: -1 }, // unlimited
}

export async function checkUsageLimit(
  userId: string,
  resourceType: string
) {
  // Get user's current plan
  const { data: subscription } = await supabase
    .from('subscriptions')
    .select('plan_id')
    .eq('user_id', userId)
    .single()

  const plan = subscription?.plan_id || 'free'

  // Count current usage
  const { count } = await supabase
    .from('usage')
    .select('*', { count: 'exact', head: true })
    .eq('user_id', userId)
    .eq('resource_type', resourceType)

  const limit = PLAN_LIMITS[plan][resourceType]

  if (limit === -1) return true // unlimited

  return count < limit
}

// Usage in API routes
export async function POST(req: Request) {
  const { userId } = await getSession(req)

  const canCreate = await checkUsageLimit(userId, 'resources')

  if (!canCreate) {
    return Response.json(
      { error: 'Usage limit reached. Upgrade to create more.' },
      { status: 403 }
    )
  }

  // Create resource...
}
```

## Landing Page Essentials

### Hero Section Template
```typescript
// app/page.tsx
export default function LandingPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-5xl font-bold text-center">
        {/* Clear, benefit-focused headline */}
        Transform X into Y in Minutes
      </h1>

      <p className="text-xl text-gray-600 mt-4 max-w-2xl text-center">
        {/* One-sentence explanation of what it does */}
        The fastest way to [achieve outcome] without [pain point]
      </p>

      <div className="flex gap-4 mt-8">
        <button className="px-8 py-3 bg-blue-600 text-white rounded-lg">
          Start Free Trial
        </button>
        <button className="px-8 py-3 border border-gray-300 rounded-lg">
          View Demo
        </button>
      </div>

      {/* Social proof */}
      <p className="text-sm text-gray-500 mt-8">
        Join 1,000+ users who love [Product]
      </p>
    </div>
  )
}
```

### Pricing Section
```typescript
const PLANS = [
  {
    name: 'Free',
    price: '$0',
    features: [
      '5 resources',
      '100 API calls/month',
      'Basic support',
    ],
  },
  {
    name: 'Pro',
    price: '$19',
    features: [
      '100 resources',
      '10,000 API calls/month',
      'Priority support',
      'Advanced features',
    ],
    popular: true,
  },
  {
    name: 'Enterprise',
    price: 'Custom',
    features: [
      'Unlimited resources',
      'Unlimited API calls',
      'Dedicated support',
      'Custom integrations',
    ],
  },
]
```

## Email Notifications

### Setup with Resend (Recommended)
```typescript
// lib/email.ts
import { Resend } from 'resend'

const resend = new Resend(process.env.RESEND_API_KEY)

export async function sendWelcomeEmail(email: string, name: string) {
  await resend.emails.send({
    from: 'onboarding@yourdomain.com',
    to: email,
    subject: 'Welcome to [Product]!',
    html: `
      <h1>Welcome, ${name}!</h1>
      <p>Thanks for signing up. Here's how to get started...</p>
    `,
  })
}

// Trigger on user signup
// Trigger on subscription created
// Trigger on usage limit reached
```

## Analytics & Monitoring

### Essential Metrics to Track
```typescript
// Track these events:
- User signups
- Trial starts
- Trial to paid conversions
- Feature usage
- Churn events
- Support requests
- Error rates

// Use:
- Vercel Analytics (built-in)
- PostHog (self-hosted)
- Plausible (privacy-focused)
```

## Launch Checklist

### Pre-Launch
- [ ] Core feature fully functional
- [ ] Authentication working
- [ ] Payments integrated and tested
- [ ] RLS policies on all tables
- [ ] Error handling implemented
- [ ] Loading states added
- [ ] Mobile responsive
- [ ] Basic SEO (title, description, OG tags)
- [ ] Terms of Service & Privacy Policy
- [ ] Email notifications working

### Launch Day
- [ ] Deploy to production
- [ ] Custom domain configured
- [ ] SSL certificate active
- [ ] Analytics tracking
- [ ] Monitoring/alerts setup
- [ ] Stripe webhook endpoint verified
- [ ] Test full signup → payment flow
- [ ] Create launch post (Twitter, HN, etc.)

### Post-Launch (Week 1)
- [ ] Monitor error logs daily
- [ ] Respond to user feedback
- [ ] Fix critical bugs within 24h
- [ ] Track key metrics
- [ ] Send welcome emails
- [ ] Engage with early users

## Common SaaS Patterns

### Freemium Model
```
Free Plan → Limited features/usage
  ↓
Pro Plan → Unlock full features
  ↓
Enterprise → Custom pricing/support
```

### Usage-Based Pricing
```
Track usage → Calculate bill
  ↓
Charge per unit (API calls, storage, etc.)
  ↓
Real-time usage display
```

### Seat-Based Pricing
```
Per user pricing
  ↓
Team management
  ↓
Invitation system
```

## Security Best Practices

### Critical Checklist
- [ ] Environment variables never committed
- [ ] RLS enabled on ALL database tables
- [ ] API routes validate auth tokens
- [ ] Input validation on all forms
- [ ] SQL injection prevention (use parameterized queries)
- [ ] CORS configured correctly
- [ ] Rate limiting on API routes
- [ ] Webhook signature verification
- [ ] Sensitive operations require re-authentication
- [ ] User data encrypted at rest

## Performance Optimization

### Must-Do Optimizations
```typescript
// 1. Image optimization
import Image from 'next/image'
<Image src={url} alt="..." width={500} height={300} />

// 2. Database query optimization
// Use indexes on frequently queried columns
CREATE INDEX idx_user_id ON resources(user_id);

// 3. API response caching
export const revalidate = 60 // Cache for 60 seconds

// 4. Use React Server Components
// Keep client components minimal

// 5. Lazy load heavy components
const HeavyComponent = dynamic(() => import('./HeavyComponent'))
```

## Deployment Process

### Vercel Deployment (Recommended)
```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Link project
vercel link

# 3. Set environment variables
vercel env add SUPABASE_URL
vercel env add SUPABASE_ANON_KEY
vercel env add STRIPE_SECRET_KEY
vercel env add STRIPE_WEBHOOK_SECRET

# 4. Deploy
vercel --prod
```

### Environment Variables Needed
```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# Stripe
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=

# App
NEXT_PUBLIC_URL=https://yourdomain.com

# Email (optional)
RESEND_API_KEY=
```

## Scaling Considerations

### When to Scale
```
< 1,000 users: Don't optimize, just ship
1K - 10K users: Basic optimization (caching, indexes)
10K - 100K users: Database optimization, CDN
100K+ users: Consider dedicated infrastructure
```

### Cost Management
```typescript
Free Tiers to Use:
- Vercel: 100GB bandwidth
- Supabase: 500MB database, 2GB bandwidth
- Stripe: No monthly fee, just transaction %
- Resend: 3,000 emails/month

Expected Costs (at 1,000 users):
- Hosting: $0-20/month
- Database: $0-25/month
- Email: $0-10/month
- Total: $0-55/month
```

## Marketing & Growth

### Launch Platforms
1. **Product Hunt**: Best for B2B tools, Wednesday launches
2. **Hacker News**: Show HN posts, technical products
3. **Twitter/X**: Build in public, share progress
4. **Reddit**: Niche subreddits (be helpful, not spammy)
5. **Indie Hackers**: Community of builders

### Content Strategy
```
Week 1: Launch announcement
Week 2-4: Tutorial content, use cases
Month 2+: SEO content, case studies
```

## Common Mistakes to Avoid

1. **Building too many features**: Ship core feature first
2. **Perfect design obsession**: Good enough is good enough for MVP
3. **No monetization**: Add payments from day 1
4. **Ignoring feedback**: Talk to users daily
5. **Over-engineering**: Use proven tech, not experimental
6. **No marketing**: Build audience while building product
7. **Forgetting analytics**: Can't improve what you don't measure

## Success Metrics

### MVP Success (First 30 Days)
- [ ] 100+ signups
- [ ] 10+ paying customers
- [ ] $500+ MRR
- [ ] <5% churn rate
- [ ] Product-market fit signals

### Growth Phase (Months 2-6)
- [ ] 1,000+ signups
- [ ] 50+ paying customers
- [ ] $2,500+ MRR
- [ ] Positive unit economics
- [ ] Organic growth starting

## Resources & Tools

### Essential Reading
- "The Mom Test" - Customer interviews
- "Traction" - Marketing channels
- "Zero to Sold" - Building & selling SaaS

### Useful Tools
- Excalidraw - Architecture diagrams
- Figma - UI design (optional)
- Linear - Issue tracking
- Plausible - Analytics
- Statuspage - Uptime monitoring

---

**Remember**: Ship fast, iterate based on feedback, and focus on solving ONE problem extremely well!

**Motto**: "Working software > Perfect software"
