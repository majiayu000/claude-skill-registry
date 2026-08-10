---
name: ops-cost-optimization
description: "Audits SaaS/PaaS, cloud commitment, and AI/LLM costs across Vercel, Supabase, AWS, and Cloudflare. Use when analyzing bills, right-sizing plans, or buying commitments."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.1"
last_validated: 2026-07-11
---

# SaaS/PaaS Cost Optimization

Use this skill to audit, reduce, and monitor infrastructure and SaaS spending. Keep the output operational: cost breakdown, waste identification, optimization actions, and monitoring setup.

## Quick Reference

| Need | Starting Reference | Notes |
|------|--------------------|-------|
| audit Vercel bill | [references/vercel-cost-guide.md](references/vercel-cost-guide.md) | ISR, Functions, Fast Origin Transfer, Image Optimization |
| audit Supabase bill | [references/supabase-cost-guide.md](references/supabase-cost-guide.md) | compute, storage, bandwidth, Auth MAUs, Edge Functions |
| audit email costs | [references/resend-cost-guide.md](references/resend-cost-guide.md) | volume tiers, batch efficiency, domain warm-up |
| audit domain costs | [references/domain-registrar-cost-guide.md](references/domain-registrar-cost-guide.md) | GoDaddy vs Cloudflare vs Namecheap, transfer savings |
| audit payment processing | [references/stripe-cost-guide.md](references/stripe-cost-guide.md) | transaction fees, Radar, Billing, volume negotiation |
| audit AI API spend | [references/ai-api-cost-guide.md](references/ai-api-cost-guide.md) | Claude, GPT, prompt caching, batch API, model routing |
| audit CI/CD costs | [references/github-cicd-cost-guide.md](references/github-cicd-cost-guide.md) | Actions minutes, Copilot, Codespaces, hosting alternatives |
| audit monitoring costs | [references/monitoring-analytics-cost-guide.md](references/monitoring-analytics-cost-guide.md) | PostHog, Sentry, Datadog, free tier maximization |
| audit CDN/edge costs | [references/cloudflare-cost-guide.md](references/cloudflare-cost-guide.md) | Workers, R2, Pages, DNS, free tier scope |
| decide on AWS/GCP/Azure commitments or K8s cost allocation | [references/cloud-commitment-and-k8s-cost-guide.md](references/cloud-commitment-and-k8s-cost-guide.md) | Savings Plans vs RIs vs Spot, CUDs, Azure Reservations, when NOT to commit, OpenCost/Kubecost, GPU capacity |
| set up cost monitoring | [references/cost-monitoring-setup.md](references/cost-monitoring-setup.md) | budget alerts, review cadence, annual cost calendar, FOCUS normalization |
| track unit economics | [references/unit-economics-guide.md](references/unit-economics-guide.md) | cost per customer/feature/request, ARPC tracking, FOCUS standard |
| IaC cost guardrails in CI | [references/github-cicd-cost-guide.md](references/github-cicd-cost-guide.md) | Infracost PR diffs, budget-threshold merge gates |
| monthly cost review | [assets/monthly-cost-review-checklist.md](assets/monthly-cost-review-checklist.md) | reusable review template |
| automated cost audit from billing data | [agents/cost-auditor.md](agents/cost-auditor.md) | parses screenshots/API data, ranks top 5 cost drivers, outputs prioritized actions |

## Workflow

1. **inventory** — list all paid services, current plans, billing cycles, and monthly spend
2. **audit** — for each service: pull usage data, compare to plan limits, identify top cost drivers by dollar amount
3. **diagnose** — classify each cost line:
   - **necessary**: directly supports revenue or product function
   - **reducible**: supports function but can be lowered via architecture or configuration
   - **wasteful**: unused, over-provisioned, or cheaper alternative exists
4. **optimize** — load the platform-specific reference file and apply the highest-impact tactics first
5. **monitor** — set up budget alerts, usage dashboards, and a monthly review cadence using [references/cost-monitoring-setup.md](references/cost-monitoring-setup.md)

## ASCII Flow

```text
Cost concern or bill review
  -> Inventory paid services, owners, plans, cycles, and spend
  -> Rank cost lines by monthly dollar impact
  -> Classify each line
     +-- necessary -> protect and monitor
     +-- reducible -> tune architecture, usage, seats, or plan tier
     +-- wasteful -> cancel, consolidate, or downgrade
  -> Load platform guide for top drivers
  -> Apply highest-impact optimizations first
  -> Add budget alerts, dashboards, and monthly review cadence
```

## Decision Rules

- start with the highest-cost service and work down
- distinguish usage-based charges (optimizable) from flat subscriptions (right-size or cancel)
- check if the free tier covers actual usage before paying for a plan
- prefer architecture changes (caching, CDN, SSG, on-demand ISR) over plan upgrades
- compare annual vs monthly pricing — annual often saves 15-20%
- consolidate services when one platform covers multiple needs (e.g., Cloudflare for DNS + CDN + storage)
- never optimize a $2/month line before a $20/month line
- when in doubt, measure for one billing cycle before cutting
- never buy a commitment (Savings Plan, RI, CUD, Reservation) against usage that hasn't been stable for 4-6+ weeks, or during an active migration/re-platform — see [references/cloud-commitment-and-k8s-cost-guide.md](references/cloud-commitment-and-k8s-cost-guide.md#when-not-to-buy-a-commitment)
- separate zero-risk waste elimination from margin/durability trade-offs before cutting — a cut that reduces headroom or DR posture needs an explicit risk owner, not just a plan-tier downgrade
- weigh implementation and ongoing operational cost (engineer-time, new on-call burden) against savings before recommending a migration — a cheaper service that costs six weeks to adopt often doesn't pay back for a year

## Cost Categories

| Category | Examples | Optimization Lever |
|----------|----------|--------------------|
| compute | Vercel Functions, Supabase database, edge workers | reduce invocations, optimize cold starts, right-size memory |
| bandwidth | Fast Origin Transfer, database egress, CDN transfer | caching, compression, image optimization, SSG |
| storage | Supabase storage, R2, S3, blob stores | lifecycle policies, compression, deduplication |
| per-request | ISR writes/reads, API calls, email sends | batching, caching, debouncing, on-demand invalidation |
| subscriptions | Pro plans, seats, add-ons | right-size plan tier, remove unused seats/add-ons |
| transaction fees | Stripe processing, dispute fees | volume negotiation, reduce disputes, batch payouts |
| AI tokens | Claude API, OpenAI API, fine-tuning, self-hosted GPU inference | prompt caching, model routing, batch API, shorter prompts, spot/reserved GPU capacity |
| cloud commitments | AWS Savings Plans/RIs, GCP CUDs, Azure Reservations | commit only against a verified stable usage floor, layer flexible + rigid instruments, never commit mid-migration |
| K8s cluster cost | shared node pools, control plane, storage, load balancers | namespace/label cost allocation (OpenCost/Kubecost), request-vs-usage rightsizing |

## When to Use This Skill

- monthly bill is higher than expected and you want to find what's driving it
- launching new projects and want to forecast infrastructure costs
- comparing free tier vs paid tier for a service
- setting up cost alerts and budget monitoring
- annual cost review and plan right-sizing
- evaluating whether to switch or consolidate services
- deciding whether to buy a Savings Plan, Reserved Instance, or Committed Use Discount, and how much
- allocating shared Kubernetes cluster cost back to teams or features
- governing AI/LLM spend before a new model-backed feature ships

## Route Elsewhere

- company-level burn rate, runway, and financial operations -> `startup-operating-system`
- infrastructure architecture and platform design -> [ops-devops-platform](../ops-devops-platform/SKILL.md)
- choosing between managed backend platforms -> [software-baas-platforms](../software-baas-platforms/SKILL.md)
- AI API integration patterns (not cost) -> [software-ai-integration](../software-ai-integration/SKILL.md)
- payment system design (not cost) -> [software-payments](../software-payments/SKILL.md)

---

## Optimization Playbook

### Quick wins (do first)

- remove unused projects, environments, and preview deployments
- switch time-based ISR revalidation to on-demand revalidation
- enable image optimization and compression
- check for services still on paid plans but no longer used
- consolidate DNS to a provider that includes it free (Cloudflare)

### Architecture changes (do next)

- move static content to CDN or SSG to reduce function invocations
- add response caching at edge to reduce origin transfer
- batch API calls and email sends instead of per-request
- use prompt caching for repeated AI API calls
- implement connection pooling to reduce database compute

### Plan optimization (do quarterly)

- compare current usage against plan tier limits
- evaluate annual vs monthly billing
- check if usage has dropped below the free tier threshold
- negotiate volume pricing when crossing tier boundaries
- remove unused seats and add-ons

## Anti-Patterns

- optimizing $1 costs while ignoring $50 costs
- switching to a cheaper service without accounting for migration effort
- cutting costs that directly support revenue-generating features
- skipping monitoring setup — costs drift back up within months
- over-provisioning "just in case" without measuring actual usage
- paying for annual plans on services you might stop using

---

## Navigation

### Platform references

- [references/vercel-cost-guide.md](references/vercel-cost-guide.md)
- [references/supabase-cost-guide.md](references/supabase-cost-guide.md)
- [references/resend-cost-guide.md](references/resend-cost-guide.md)
- [references/domain-registrar-cost-guide.md](references/domain-registrar-cost-guide.md)
- [references/stripe-cost-guide.md](references/stripe-cost-guide.md)
- [references/ai-api-cost-guide.md](references/ai-api-cost-guide.md)
- [references/github-cicd-cost-guide.md](references/github-cicd-cost-guide.md)
- [references/monitoring-analytics-cost-guide.md](references/monitoring-analytics-cost-guide.md)
- [references/cloudflare-cost-guide.md](references/cloudflare-cost-guide.md)
- [references/cloud-commitment-and-k8s-cost-guide.md](references/cloud-commitment-and-k8s-cost-guide.md)

### Cross-platform

- [references/cost-monitoring-setup.md](references/cost-monitoring-setup.md)
- [references/unit-economics-guide.md](references/unit-economics-guide.md)
- [assets/monthly-cost-review-checklist.md](assets/monthly-cost-review-checklist.md)
- [data/sources.json](data/sources.json)

### Agents

- [agents/cost-auditor.md](agents/cost-auditor.md)

## Related Skills

- `startup-operating-system`
- [../ops-devops-platform/SKILL.md](../ops-devops-platform/SKILL.md)
- [../software-baas-platforms/SKILL.md](../software-baas-platforms/SKILL.md)
- [../software-payments/SKILL.md](../software-payments/SKILL.md)
- [../software-ai-integration/SKILL.md](../software-ai-integration/SKILL.md)

## Fact-Checking

- Verify current pricing, tier limits, and free-tier inclusions before final recommendations.
- Pricing changes frequently — prefer official pricing pages over cached knowledge.
- If web access is unavailable, mark pricing-sensitive guidance as unverified and include the official pricing URL from `data/sources.json`.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.

