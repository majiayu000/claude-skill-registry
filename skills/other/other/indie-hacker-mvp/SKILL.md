---
name: Indie Hacker MVP Development
description: Fast MVP shipping patterns for indie hackers - ruthless prioritization, lean development
version: 1.0.0
author: AI Skills Community
tags: [indie-hacker, mvp, lean, startup, shipping]
---

# Indie Hacker MVP Development

Ship fast, validate fast, iterate based on feedback. This skill guides rapid MVP development.

## Core Philosophy

1. **Speed over Perfection**: Ship something functional, not polished
2. **Ruthless MVP Focus**: 1-3 features maximum for v1
3. **Validate Before Building**: Talk to users, don't assume
4. **Revenue First**: Build what people will pay for

## Instructions

### The MVP Checklist

Before writing code, answer these:
- [ ] Can I describe the core value in one sentence?
- [ ] Have I talked to at least 3 potential users?
- [ ] What's the ONE feature that solves the core problem?
- [ ] Can I ship in 2 weeks or less?
- [ ] How will I know if it's working? (metrics)

### Development Priorities

**DO:**
- Use existing tools (Clerk for auth, Convex for backend)
- Copy proven UI patterns (don't reinvent)
- Ship daily, get feedback weekly
- Use feature flags for experimental features
- Write tests only for critical paths

**DON'T:**
- Build admin dashboards before you have users
- Add "nice to have" features
- Optimize before you have traffic
- Build custom solutions for solved problems
- Spend time on perfect code architecture

### The 2-Week Sprint Template

**Week 1:**
- Day 1-2: Core feature implementation
- Day 3-4: Basic UI (functional, not beautiful)
- Day 5: Integration and testing

**Week 2:**
- Day 1-2: Polish critical user flows
- Day 3: Deploy to production
- Day 4: Share with 10 potential users
- Day 5: Collect feedback, prioritize v2

### Lean Tech Stack Recommendations

```
Frontend: React + Vite (fast dev server)
Backend: Convex (zero-config, real-time)
Auth: Clerk (5-minute setup)
UI: Shadcn/ui (copy-paste components)
Deployment: Vercel (push to deploy)
```

### User Feedback Script

After someone uses your MVP, ask:
1. "What did you expect to happen?"
2. "What actually happened?"
3. "Would you pay $X/month for this?"
4. "What's missing that would make you use this daily?"

## Examples

### Good MVP Scope
```
"Users can submit a lead form, and automatically receive
a personalized response email within 30 seconds."
```

### Bad MVP Scope (Too Big)
```
"Users can submit leads, get auto-responses, view analytics
dashboard, set up custom workflows, integrate with CRM,
manage team permissions, and export reports."
```

## Best Practices

1. **Launch embarrassingly early** - If you're not embarrassed, you waited too long
2. **Manual before automation** - Do things that don't scale initially
3. **Talk to users weekly** - Schedule recurring user calls
4. **Metrics from day 1** - Track signups, activation, retention
5. **One channel focus** - Master one acquisition channel before expanding

## Anti-Patterns to Avoid

- ❌ Building features no one asked for
- ❌ Premature optimization
- ❌ Perfect code before product-market fit
- ❌ Building for imaginary scale
- ❌ Spending weeks on landing page design

## Quick Decision Framework

When unsure, ask:
1. "Will this help me get 10 paying users?"
2. "Can I validate this with a manual process first?"
3. "What's the simplest version of this feature?"

If the answer to #1 is no, don't build it yet.
