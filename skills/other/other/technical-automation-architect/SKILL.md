---
name: technical-automation-architect
description: Design technical architecture and automation strategies for solo SaaS products. Use when selecting tech stacks, deciding build vs buy, or implementing AI automation to scale operations.
category: business
license: MIT
---

# When to Use This Skill

Use this skill when you need to:

- **Choose a tech stack** for your solo SaaS product
- **Decide build vs buy** for features and infrastructure
- **Implement AI automation** to multiply your effectiveness
- **Leverage managed services** instead of building from scratch
- **Use SaaS boilerplates** to accelerate development
- **Manage technical debt** strategically as solo founder
- **Scale to $1M ARR** as solo or tiny team

# Core Concepts

## "Boring Stack" Philosophy

**Use established technologies, not cutting-edge**:

**Why boring wins**:

- Faster development (you know the tools)
- Fewer bugs (battle-tested libraries)
- Easier hiring (common skills)
- Better resources (tutorials, help, solutions)
- Long-term maintainability (won't abandon you)

**The cost of new/shiny**:

- Learning curve: 2-3 months to become productive
- Unknown bugs and edge cases
- Sparse documentation and community
- Abandonment risk (if project dies)

**Principle**: Leverage existing skills over chasing new tech

## Build vs Buy: Leverage Everything

**The ruthless equation**: "Would you rather spend 3 months building
authentication or 3 months acquiring your first 100 customers?"

**Leverage (Buy)** for:

- Authentication (Auth0, Supabase Auth, Clerk)
- Payment processing (Stripe, Paddle)
- Email infrastructure (SendGrid, Resend, Postmark)
- User management frameworks
- Managed databases (RDS, Supabase, PlanetScale)
- Hosting (Vercel, Railway, Fly.io)

**Build** only:

- Your core differentiator (unique value proposition)
- Features where existing solutions don't fit
- Custom integrations that don't exist

**SaaS boilerplates**: Can significantly reduce setup time by prebuilding common
foundation pieces.

# Step-by-Step Architecture Process

## Phase 1: Stack Selection (Week 1)

**Choose technologies you already know**:

- Backend: Django, Rails, or Go (what you're proficient in)
- Frontend: React, NextJS, or HTMX (leverage existing skills)
- Database: PostgreSQL (battle-tested) or SQLite (start simple)
- Infrastructure: Managed services (don't self-host initially)

**Avoid**:

- New languages you'll need to learn
- Cutting-edge frameworks (use stable, mature tech)
- Complex architectures (microservices, K8s) until proven need

**Deliverable**: Tech stack decision document

## Phase 2: Build vs Buy Matrix (Week 2)

**List all components needed**:

- Authentication, payments, email, database, hosting, etc.

**For each component**:

- What managed services exist?
- Cost of managed service vs build time?
- Does it integrate well with chosen stack?
- What's the exit strategy if service fails?

**Decision criteria** (rules of thumb):

- Buy if: Managed service integration is clearly faster than custom build
- Buy if: Not core differentiator
- Build if: Core unique value prop
- Build if: Existing solutions don't fit use case

**Deliverable**: Build/buy decision matrix

## Phase 3: SaaS Boilerplate Evaluation (Week 3)

**Research boilerplates in your stack**:

- Django: ShipFast, SaaS Pegasus
- Rails: Jumpstart, Bullet Train
- NextJS: Supabase SaaS Kit, various Next.js starters

**Evaluation criteria**:

- Active maintenance (last commit within 3 months)
- Community size (stars, issues, discussions)
- Feature match (high overlap with your immediate roadmap)
- License terms (MIT vs paid)
- Tech stack alignment (your preferred tools)

**Decision**:

- Use boilerplate: If most foundational needs are covered and code quality is
  acceptable
- Build from scratch: If highly custom requirements

**Deliverable**: Boilerplate choice or scratch-build decision

## Phase 4: Automation Planning (Week 4)

**Identify automation opportunities**:

- Repetitive tasks (daily/weekly)
- Manual processes (customer onboarding, reporting)
- Communication (emails, notifications, updates)
- Operations (deployments, backups, monitoring)

**Automation tools**:

- No-code: Zapier, Make (n8n), Airtable
- Code: Scripts, GitHub Actions, cron jobs
- AI: Cursor, v0, Bolt for code generation
- Infrastructure: Terraform, Docker for reproducibility

**Deliverable**: Automation roadmap prioritized by ROI

# Common Mistakes

**Mistake 1: Choosing Shiny Over Familiar**

- **Problem**: Spend 3 months learning Rust when you know Python
- **Solution**: Use boring stack you're proficient in

**Mistake 2: Building Solved Problems**

- **Problem**: 3 months building auth from scratch
- **Solution**: Use Auth0/Supabase in 1 day, ship features

**Mistake 3: Over-Engineering Early**

- **Problem**: Microservices, K8s for MVP
- **Solution**: Monolith, managed hosting until proven need

**Mistake 4: No Automation Strategy**

- **Problem**: Manual everything, stuck in operations
- **Solution**: Automate high-frequency, low-judgment work early

**Mistake 5: Ignoring Technical Debt**

- **Problem**: Accumulate debt unconsciously, drowning in hacks
- **Solution**: Conscious trade-offs, scheduled repayment

# Success Metrics

**Technical Health Indicators** (directional targets):

| Metric                   | Warning         | Healthy           | Optimal           |
| ------------------------ | --------------- | ----------------- | ----------------- |
| **Dev velocity**         | <1 feature/week | 2-3 features/week | 4-5 features/week |
| **Downtime/month**       | >2 hours        | <30 minutes       | <5 minutes        |
| **Bugs per release**     | 5+              | 1-2               | 0-1               |
| **Deployment frequency** | Monthly         | Weekly            | Daily             |
| **Technical debt ratio** | >40%            | 20-30%            | <20%              |

**Red flags**:

- ❌ Taking 2+ weeks to ship simple features
- ❌ Constant production incidents
- ❌ Dreading code changes (fear of breaking things)
- ❌ Can't take time off (product breaks without you)

# Deep Dives

For comprehensive technical strategies, tools, and frameworks, see the
references:

**[references/stack-comparison.md](references/stack-comparison.md)**

- Django vs Rails vs Go comparison
- Frontend options: React vs NextJS vs HTMX
- Database choices: PostgreSQL vs SQLite vs MySQL
- Hosting infrastructure options
- Real-world stack examples from successful solo SaaS

**[references/managed-services.md](references/managed-services.md)**

- Authentication: Auth0, Supabase Auth, Clerk comparison
- Payments: Stripe vs Paddle configuration
- Email: SendGrid, Resend, Postmark setup
- Databases: RDS, Supabase, PlanetScale evaluation
- Cost-benefit calculations for each service

**[references/automation-checklist.md](references/automation-checklist.md)**

- 50+ automation opportunities identified
- No-code tools comparison (Zapier vs Make vs n8n)
- AI-assisted automation patterns for solo teams
- Developer productivity multipliers
- CI/CD pipeline templates

## Research Notes

This skill synthesizes findings from technical operations research:

**Primary Research**:

**Key Principles**:

- **Boring stack philosophy** - Established tech over shiny new tools
- **Leverage everything** - Solved problems shouldn't be rebuilt
- **Conscious technical debt** - Documented trade-offs, scheduled repayment
- **Ruthless automation** - Automate repetitive work to protect focus for core
  product and customer outcomes

**Recommended Stacks**:

- **Backend**: Django (Python), Rails (Ruby), Go + HTMX + SQLite
- **Frontend**: React + SWR, NextJS, or HTMX
- **Database**: PostgreSQL (production), SQLite (start)
- **Infrastructure**: Docker, Terraform, Kamal (simplified deployment)

**Build vs Buy Examples**:

- **Buy**: Auth, payments, email, hosting, user management
- **Build**: Core differentiator only
- **SaaS boilerplates**: Can reduce time-to-first-version for common app
  scaffolding

---

## Next Steps After Architecture Setup

Once your tech stack is chosen:

1. **Start building** - Use boilerplate or scratch-build
2. **Automate early** - CI/CD, deployments, backups
3. **Document decisions** - Why you chose X over Y
4. **Monitor tech debt** - Track ratio, schedule cleanup

Related skills:

- `systemization-documentation-expert` for SOPs and handoffs
- `customer-retention-optimizer` for onboarding and lifecycle automation

---

## Sources

- [DORA | DevOps Research and Assessment](https://dora.dev/)
- [The Twelve-Factor App](https://12factor.net/)
- [Auth0 Documentation](https://auth0.com/docs)
- [Supabase Auth Documentation](https://supabase.com/docs/guides/auth)
- [Stripe Documentation](https://docs.stripe.com/)
- [Vercel Documentation](https://vercel.com/docs)
- [Fly.io Docs](https://fly.io/docs)
