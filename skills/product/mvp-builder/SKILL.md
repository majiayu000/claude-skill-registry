---
name: MVP Builder
description: Rapid MVP development and feature prioritization for fast product validation. Use when building minimum viable products, prioritizing features, validating ideas quickly, or when users need to ship products fast while avoiding over-engineering.
version: 1.0.0
---

# MVP Builder

Ship MVPs in 1-2 weeks, not months.

## Core Principle

**Start with the smallest thing that proves/disproves your riskiest assumption.**

MVP = Minimum **Viable** Product, not Minimum **Pretty** Product.

## MVP Feature Matrix

Categorize every feature idea using this matrix:

| Category         | Definition                           | Action                |
| ---------------- | ------------------------------------ | --------------------- |
| **P0**           | Must have for core value proposition | Build now             |
| **P1**           | Important but can wait for v1.1      | Ship after validation |
| **P2**           | Nice to have, delight features       | Ship v2+              |
| **Out of Scope** | Not needed for validation            | Defer indefinitely    |

### Example: Task Management MVP

**P0 (Week 1):**

- Create task with title/description
- Mark task complete
- View task list
- Basic authentication

**P1 (Post-validation):**

- Due dates, priorities, reminders

**P2 (Future):**

- Team collaboration, file attachments, mobile app

**Out of Scope:**

- Gantt charts, time tracking, integrations

## 5 MVP Patterns

### 1. Concierge MVP

**Definition:** Manually deliver the service before building automation

**When to use:** Core value is service delivery, not technology

**Examples:**

- Food delivery → Take orders via WhatsApp, deliver yourself
- AI copywriter → Manually write copy for customers
- Scheduling tool → Coordinate meetings via email

**Time:** 1-3 days | **Validates:** People want the service

---

### 2. Wizard of Oz MVP

**Definition:** Interface looks automated, but humans operate it behind the scenes

**When to use:** Automation is expensive/complex to build

**Examples:**

- Zapier early days → Manually created integrations
- AI chatbot → Human answers, customer thinks it's AI

**Time:** 1 week | **Validates:** Users engage with interface

---

### 3. Landing Page MVP

**Definition:** Explain the product + collect emails (no product yet)

**When to use:** Testing demand before building anything

**Examples:**

- Dropbox → Video showing concept
- Buffer → Landing page before code existed

**Time:** 1-2 days | **Validates:** People sign up for waitlist

---

### 4. Single-Feature MVP

**Definition:** One feature that solves one problem

**When to use:** One feature delivers 80% of value

**Examples:**

- Twitter → Just post 140-character updates
- Instagram → Just share photos with filters
- Stripe → Just accept credit card payments

**Time:** 1-2 weeks | **Validates:** People use the core feature

---

### 5. Piecemeal MVP

**Definition:** Combine existing tools instead of building custom

**When to use:** You can cobble together a solution with existing tools

**Examples:**

- Typeform + Airtable + Zapier + Stripe
- No-code tools: Webflow, Bubble, Retool

**Time:** 2-5 days | **Validates:** Workflow works end-to-end

## Tech Stack Decision Tree

```
Is this a web app?
├─ YES
│  ├─ Need real-time?
│  │  ├─ YES → Next.js + Supabase + WebSockets
│  │  └─ NO → Remix + PostgreSQL
│  └─ Simple CRUD? → Supabase + React
└─ NO
   ├─ Mobile app? → React Native + Expo
   ├─ API only? → Express + PostgreSQL
   ├─ Chrome extension? → Vanilla JS + Chrome APIs
   └─ CLI tool? → Node.js or Python
```

**Recommended MVP Stack:**

- **Frontend:** React + Vite or Next.js
- **Backend:** Supabase (Postgres + Auth + Storage) or Express.js
- **Styling:** Tailwind CSS + shadcn/ui
- **Hosting:** Vercel/Netlify (frontend) + Railway/Fly.io (backend)
- **Auth:** Clerk or Supabase Auth
- **Payments:** Stripe Checkout

**Speed-Focused Tools:**

- Supabase (backend in 10 min)
- Vercel v0 (UI generation)
- Clerk (auth in 5 min)
- Stripe Checkout (payments in 20 min)

## Anti-Patterns to Avoid

❌ **Building features "just in case"** → Build when 3+ users request
❌ **Perfect design before launch** → Ship functional, ugly is fine
❌ **Over-engineering architecture** → Monolith is fine for MVP
❌ **Custom authentication** → Use Clerk, Auth0, or Supabase Auth
❌ **Building admin panel first** → Use database GUI (Retool/Supabase)
❌ **Mobile app before web** → Web first, always
❌ **Scaling for 1M users** → Build for 10 users, scale when needed

## MVP Quality Standards

### Must Have ✅

- Core feature works end-to-end
- Basic auth (login/signup)
- Deploys without crashing
- Mobile-responsive (doesn't need to be beautiful)
- Basic error handling

### Can Skip ⏸️

- Perfect UI/UX
- Email notifications
- Advanced features
- Analytics dashboard
- Error monitoring (add after validation)
- Tests (add after product-market fit)

## Build Process

### Week 1: Build Core Feature

**Days 1-2: Design + Setup**

- Sketch 3 screens (paper/Figma)
- Set up repo + database (3-5 tables max)
- Deploy infrastructure

**Days 3-4: Build**

- Authentication (use library, don't build)
- Core feature (1 user flow only)
- Basic UI (use component library)

**Day 5: Polish + Deploy**

- Fix critical bugs
- Deploy to production
- Share with 5 friends for feedback

### Week 2: Validate

**Days 1-2: Iterate**

- Fix issues from Week 1 feedback
- Add 1-2 critical missing features

**Days 3-4: Get Users**

- Share on social media
- Post in relevant communities
- Email 20 people personally

**Day 5: Analyze & Decide**

- Did 10+ people sign up?
- Did 3+ people use it 3+ times?
- Are 1-2 people willing to pay?

**Decision Point:**

- ✅ Yes to above → Build P1 features
- ❌ No → Pivot or kill project

## Launch Checklist

**Pre-Launch (1 hour):**

- [ ] Core user flow works end-to-end
- [ ] Sign up + login works
- [ ] Deployed with HTTPS
- [ ] Privacy policy + ToS (use generator)

**Launch Day:**

- [ ] Post on Twitter/LinkedIn with screenshot
- [ ] Share in 3-5 relevant communities
- [ ] Email 20 people personally

**Week 1 Post-Launch:**

- [ ] Reply to every piece of feedback
- [ ] Fix critical bugs within 24 hours
- [ ] User interview with 3-5 early users

## Success Metrics

**MVP validation criteria:**

- **10+ signups** in first week
- **3+ people** use it 3+ times
- **1-2 people** willing to pay

**If you hit these:** You might have something. Build P1 features.

**If you don't:** Pivot or move on. Don't invest months in something nobody wants.

## Real MVP Examples

**Successful minimal starts:**

- **Airbnb:** Photos of their apartment + PayPal link
- **Stripe:** Just a form to collect card details
- **Dropbox:** Video demo before building product
- **Uber:** iPhone app in San Francisco only
- **Facebook:** Harvard students only, basic profiles

All started much smaller than you think.

## Related Resources

**Related Skills:**

- `product-strategist` - For validating product-market fit
- `frontend-builder` - For building the UI
- `api-designer` - For backend API design
- `deployment-advisor` - For deployment decisions
- `go-to-market-planner` - For launch strategy

**Related Patterns:**

- `META/DECISION-FRAMEWORK.md` - Platform selection decision tree

**Related Playbooks:**

- `PLAYBOOKS/build-mvp.md` - Step-by-step MVP build procedure (when created)

## Quick Reference

**For experienced users:**

- [ ] Identify riskiest assumption
- [ ] Choose MVP pattern (Concierge/Wizard/Landing/Single-Feature/Piecemeal)
- [ ] Categorize features (P0/P1/P2/Out of Scope)
- [ ] Build P0 only (1-2 weeks max)
- [ ] Ship ugly but functional
- [ ] Validate with 10+ users
- [ ] Decide: build P1 or pivot
