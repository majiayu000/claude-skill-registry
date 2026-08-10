---
name: software-paas-hosting
description: Chooses PaaS compute hosting for apps, agents, bots, APIs, and workers. Use when picking Vercel, Fly.io, Railway, Render, Cloudflare, Deno, or container PaaS.
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.1"
last_validated: 2026-07-11
---

# PaaS Compute Hosting Selection

Use this skill to pick the right managed compute platform for an application, agent, or bot when you don't want to operate Kubernetes, EC2 fleets, or your own infrastructure.

This is a **selection skill**, not an implementation guide. If you already know the platform and need help building on it, hand off to the platform's docs or to `software-backend` / agent-stack skills.

## When To Use This Skill

- Picking where to deploy a Next.js / FastAPI / Node / Python app
- Choosing the compute substrate for an agent (Shape A triggered, Shape B bot, Shape C loop)
- Deciding between Vercel-style serverless, Fly.io-style always-on containers, and Cloudflare-style edge workers
- Evaluating "deploy-and-forget" platforms vs setting up your own infra
- Picking a host for a side-project, prototype, or production product without a platform team

## When NOT To Use This Skill

| Need | Use Instead |
|------|-------------|
| Managed data/auth platforms (Supabase, Convex, Firebase) | [`../software-baas-platforms/SKILL.md`](../software-baas-platforms/SKILL.md) |
| Kubernetes, Terraform, GitOps, self-managed clusters | [`../ops-devops-platform/SKILL.md`](../ops-devops-platform/SKILL.md) |
| Cost optimization across existing infra | [`../ops-cost-optimization/SKILL.md`](../ops-cost-optimization/SKILL.md) |
| Backend implementation defaults (REST, auth, queues, observability) | [`../software-backend/SKILL.md`](../software-backend/SKILL.md) |
| Always-on bot serving stack (FastAPI + Redis) | [`../ai-bot-builder/references/production-deployment.md`](../ai-bot-builder/references/production-deployment.md) |
| Voice bot deployment (SIP, media, recording) | [`../ai-voice-bots/references/production-deployment.md`](../ai-voice-bots/references/production-deployment.md) |
| Agent trigger integration | [`../ai-coding-agents-tasks/references/webhook-and-queue-triggers.md`](../ai-coding-agents-tasks/references/webhook-and-queue-triggers.md) |
| LLM inference cost and provider routing | [`../ai-llm-inference/SKILL.md`](../ai-llm-inference/SKILL.md) |

## Quick Reference

| Question | Read | Outcome |
|----------|------|---------|
| Which PaaS fits this workload? | [`references/platform-comparison.md`](references/platform-comparison.md) | Strengths, weaknesses, pricing model, lock-in profile for 8 platforms |
| Where should I host an agent / bot / loop? | [`references/agent-hosting-matrix.md`](references/agent-hosting-matrix.md) | Per-shape (A/B/C) reference architectures with concrete platform stacks |
| Which facts must be rechecked? | [`data/sources.json`](data/sources.json) | Primary docs for volatile limits, pricing, and beta platform features |

## Workflow

1. Classify the workload by statefulness: stateless request, stateful session, always-on worker, durable workflow, or media/voice.
2. Bound execution shape: max request duration, concurrency, WebSocket/SSE needs, queue semantics, cron cadence, and restart tolerance.
3. Choose the placement driver: near users, near data, compliance boundary, cost floor, or team familiarity.
4. Read [`references/platform-comparison.md`](references/platform-comparison.md) for 1-2 eligible platforms; reject ineligible options with a concrete reason.
5. For agents and bots, confirm the selection in [`references/agent-hosting-matrix.md`](references/agent-hosting-matrix.md).
6. Before giving current limits, queues, regions, free-tier, or pricing claims, verify against [`data/sources.json`](data/sources.json) and primary docs.
7. Hand off implementation details to the chosen platform docs plus `software-backend`, `software-baas-platforms`, or agent runtime skills.

## Fact-Checking

Treat PaaS limits, pricing, regions, managed database maturity, and beta/preview features as volatile. Verify before relying on:

- Vercel function duration (GA vs "extended max duration" beta), Queues beta status, Workflow, AI Gateway, Sandbox, Agent, and plan-level billing.
- Cloudflare Workers CPU time, subrequest caps (raised Feb 2026 — verify current free vs. paid default and configurable ceiling), wall-clock duration, Queue consumer retries, Durable Objects, Workflows, Vectorize, and AI Gateway.
- Deno Deploy vs Deploy Classic migration state (Classic and subhosting v1 are scheduled to shut down; treat the date as imminent and re-verify against the migration guide, not this document), supported regions, queue support, and framework/runtime compatibility.
- Fly.io Managed Postgres vs legacy Fly Postgres, Machines autostart/autostop behavior, regions, and support boundaries.
- Railway, Render, Northflank, and Koyeb plan limits, free-tier behavior, sleep/scale-to-zero semantics, and production support.
- Amazon Bedrock AgentCore Runtime duration, Memory/Gateway/Identity semantics, Registry preview state, pricing dimensions, and region/service availability.

## Three-Question Selection

Answer these three before reading deeper:

1. **Is the workload stateless per request, stateful per session, or always-running?**
   - Stateless → Vercel, Cloudflare Workers, Netlify, Deno Deploy
   - Stateful (sessions, WebSocket, long-held) → Fly.io, Railway, Render
   - Always-running (loops, daemons, cron-driven) → Fly.io Machines, Railway Workers, Render Background Workers, Inngest

2. **What's the max single-request duration?**
   - <30s CPU / short wall time → any platform
   - 30s–300s CPU → Cloudflare Workers Paid if configured, Vercel Fluid, Fly.io, Railway, Render
   - 300s–800s wall time → Vercel Pro/Enterprise Fluid Compute (800s is GA), Fly.io, Railway, Render
   - 800s–1800s → Vercel Pro/Enterprise "extended max duration" (30 min, beta as of mid-2026, select Node/Python runtimes only, incompatible with Secure Compute/Static IPs) or a container platform
   - 1800s+ or multi-hour → Fly.io Machines, container workers, Vercel Workflows (no fixed duration ceiling), or durable orchestration; not a single request-scoped function
   - Multi-step durable → wrap in Inngest / Trigger.dev / Temporal / Vercel Workflows regardless of host

3. **Does it need to be near users (edge) or near data (region)?**
   - Edge / low-latency first byte → Cloudflare Workers, Vercel Edge, Deno Deploy
   - Region / co-located with database → Fly.io (multi-region capable), Railway, Render

## Default Picks

| Workload | Default | Why |
|----------|---------|-----|
| Next.js product site / web app | **Vercel** | First-party support; AI SDK and AI Gateway baked in |
| Always-on Python/Node bot | **Fly.io** | Long-held connections, WebSocket, persistent state, no cold-start surprises |
| Triggered agent (webhook → run) | **Vercel + Inngest** or **Cloudflare Workers + Queues** | Idempotency + durable steps native to both |
| Autonomous loop (Shape C) | **Inngest on Vercel** or **Fly.io Machines** | Durable iteration + budget caps |
| Voice bot control plane | **Fly.io** (paired with LiveKit Cloud for media) | Persistent agent worker per call |
| Multi-tenant SaaS backend | **Fly.io** or **Railway** | Stateful, scales horizontally, owns Postgres |
| Edge AI (low-latency LLM proxy) | **Cloudflare Workers + AI Gateway** | Low-latency global request handling; verify CPU and subrequest limits |
| AWS enterprise agent | **AgentCore Runtime + Memory + Gateway** | Long sessions, framework choice, managed identity/tooling; verify pricing and regional support |
| Background workers and cron | **Render Background Workers**, **Railway Workers**, **Fly.io Machines** | Cheap, simple, always-on |

## Graduating From PaaS To Raw Cloud

PaaS is the right default until one of these becomes true; treat each as a concrete trigger, not a vague "we're big now" feeling:

| Signal | Why PaaS stops fitting |
|--------|-------------------------|
| Sustained monthly PaaS spend materially exceeds one platform-team engineer's fully-loaded cost | The math flips toward owning the infra; verify current spend against current salary bands rather than assuming a fixed dollar threshold |
| Compliance mandates a named cloud, region, or physical control (data residency, FedRAMP, sector-specific hosting rules) | No PaaS vendor can contractually satisfy a requirement it wasn't built for |
| Workload needs GPUs, custom kernels, specialized network hardware, or sub-millisecond determinism | PaaS compute is general-purpose; specialized silicon or latency floors need raw cloud or bare metal |
| Multi-region active-active with strong consistency guarantees | Most PaaS databases and compute are single-region-primary or eventually consistent by default |
| Platform-specific limits (duration, subrequests, memory, egress) are hit routinely, not as an edge case | Repeated limit-hugging is a sign the workload has outgrown the platform's target shape, not a config problem |

Migrate incrementally: keep the stateless front end on PaaS, move only the constrained workload (the GPU job, the compliance-scoped service) to raw cloud, and re-evaluate the rest only if the same pressure recurs elsewhere.

## Deploy-and-Forget Scope

| Removed by the platform | Still your responsibility |
|-------------------------|---------------------------|
| OS patching and kernel updates | Application correctness |
| Load balancer config | Schema migrations |
| TLS certificate management | Secret rotation |
| Autoscaling rules (sensible defaults) | Cost monitoring |
| Log aggregation | Provider failover (LLM / external APIs) |
| Health-check wiring | Domain-specific compliance (recording, audit logs) |
| Zero-downtime deploys | Backups and disaster recovery |
| Build pipeline (Dockerfile or buildpacks) | Billing alerts at the platform level |

## ASCII Flow

```text
workload + scale + statefulness
            │
            ▼
┌──────────────────────────────────┐
│  Three-Question Selection        │
│  (stateful? duration? edge?)     │
└────────────┬─────────────────────┘
             │
             ▼
┌──────────────────────────────────┐
│  references/platform-comparison  │
│  → pick 1–2 finalists            │
└────────────┬─────────────────────┘
             │
             ▼
┌──────────────────────────────────┐
│  references/agent-hosting-matrix │
│  → confirm against shape A/B/C   │
└────────────┬─────────────────────┘
             │
             ▼
┌──────────────────────────────────┐
│  Implementation handoff          │
│  → platform docs                 │
│  → software-backend defaults     │
│  → agent-runtime guides          │
└──────────────────────────────────┘
```

## Lock-in Discipline

| Rule | Why |
|------|-----|
| Use Dockerfile-based deploys | Buildpacks and platform-specific config tie you to the host |
| Keep data in external services (Supabase, Neon, Upstash, Cloudflare D1) | Data portability is the hardest part of a platform migration |
| Use portable secret stores (Doppler, Infisical, AWS Secrets Manager) | Platform-native env vars do not survive a migration |
| Avoid host-proprietary primitives unless they are load-bearing | Vercel Edge Config, Cloudflare Durable Objects — choose deliberately |
| Pin runtime versions in `package.json` / `Dockerfile` | A platform's default Node/Python upgrade can break silently |

## Cost Discipline

Default cost shape per platform:

| Platform | Free tier | Hobby paid tier | Production scaling |
|----------|-----------|-----------------|---------------------|
| Vercel | Free for non-commercial / prototype use | Pro is the usual production baseline | Function duration, bandwidth, seats, storage, AI products |
| Fly.io | Trial / usage credit varies | Pay-as-you-go | Machine size/count, bandwidth, volumes, Managed Postgres |
| Railway | Free/trial credits vary | Hobby for personal, Pro for teams | Resource usage, replicas, storage, egress |
| Render | Free web services may sleep | Paid instances for always-on | Instance count, databases, workers, bandwidth |
| Cloudflare Workers | Free request tier | Workers Paid for production limits | Requests, CPU, duration, storage products |
| Deno Deploy | Verify current plan | Usage-based / platform-specific | Region, build, and runtime limits |
| Northflank | Trial / free credits vary | Team/container plans | Container hours, add-ons, environments |
| Koyeb | Free instance is preview/hobby only | Instance-hour pricing | Instance type/count, bandwidth, regions |

Always set spend alerts at the billing platform level. The single most common surprise in PaaS bills is autoscale-driven egress on a misconfigured background job.

## Common Anti-Patterns

- Treating Vercel functions as always-on workers (they're stateless; use Fly.io or Render)
- Putting Postgres on the same Fly.io machine as the app (split for durability)
- Hosting voice agents on Vercel (no SIP/media; use LiveKit Cloud + Fly.io)
- Running a 6-hour autonomous loop in a single function (use durable orchestrator)
- Using a platform's in-cluster database without a migration plan
- Forgetting that "free tier" CPU is throttled — production workloads need the paid plan
- Deploying a multi-tenant bot to edge functions without per-tenant rate limits
- Holding a WebSocket on a Vercel function (it terminates; use Fly.io / Cloudflare Durable Objects)
- Treating Cloudflare's default 30s CPU limit as a wall-clock request limit; HTTP Workers can run longer while connected, but CPU, queue, cron, and Durable Object alarm limits still matter
- Using Vercel Queues as a mature queue without checking beta status, poison-message handling, and dead-letter requirements
- Assuming Deno Deploy Classic behavior still applies; Classic and subhosting v1 are on a hard shutdown date in July 2026 (imminent — treat any project still on Classic as an urgent migration, not a someday task), projects do not migrate automatically, and the new Deploy has different regions, APIs, and queue support
- Confusing legacy Fly Postgres guidance with Fly Managed Postgres; evaluate support, backups, HA, regions, and missing managed features explicitly
- Treating Koyeb's free instance as production-ready; it is explicitly scoped to testing/hobby use (single region, no worker services, no volumes, no custom scaling, scales to zero on idle) — not a beta feature, just a non-production tier
- Ignoring egress and subrequest fan-out costs: a background job that fans out to many external calls or streams large payloads through a serverless function is the most common runaway PaaS bill, independent of which platform is chosen
- Picking a platform by brand familiarity instead of the three-question selection; "we already use Vercel" is not a reason to force a stateful WebSocket workload onto stateless functions

## Navigation

- [`references/platform-comparison.md`](references/platform-comparison.md) — Vercel, Fly.io, Railway, Render, Cloudflare Workers + Durable Objects, Deno Deploy, Northflank, Koyeb
- [`references/agent-hosting-matrix.md`](references/agent-hosting-matrix.md) — Shape A/B/C → recommended PaaS and AWS stacks with reference architectures
- [`references/aws-bedrock-agentcore.md`](references/aws-bedrock-agentcore.md) — AWS-native agent runtime, memory, gateway, identity, observability, evaluation, policy, and registry choices
- [`data/sources.json`](data/sources.json) — primary documentation sources for volatile platform facts
- [`../software-baas-platforms/SKILL.md`](../software-baas-platforms/SKILL.md) — managed data/auth platforms (sibling skill)
- [`../ops-devops-platform/SKILL.md`](../ops-devops-platform/SKILL.md) — for K8s/self-managed substrate decisions
- [`../ai-coding-agents-tasks/SKILL.md`](../ai-coding-agents-tasks/SKILL.md) — agent task and trigger model
- [`../ai-agents/references/24-7-operating-model.md`](../ai-agents/references/24-7-operating-model.md) — SLOs and on-call once deployed
- [`../ai-agents/references/autonomous-loop-patterns.md`](../ai-agents/references/autonomous-loop-patterns.md) — Shape C loop drivers
- [`../ai-bot-builder/references/production-deployment.md`](../ai-bot-builder/references/production-deployment.md) — bot serving stack patterns
- [`../ai-voice-bots/references/production-deployment.md`](../ai-voice-bots/references/production-deployment.md) — voice deployment (LiveKit-paired)

## Related Skills

- [`../software-baas-platforms/SKILL.md`](../software-baas-platforms/SKILL.md) — data layer
- [`../software-backend/SKILL.md`](../software-backend/SKILL.md) — backend defaults
- [`../ops-devops-platform/SKILL.md`](../ops-devops-platform/SKILL.md) — when PaaS isn't enough
- [`../ops-cost-optimization/SKILL.md`](../ops-cost-optimization/SKILL.md) — cost governance
- [`../ai-llm-inference/SKILL.md`](../ai-llm-inference/SKILL.md) — LLM provider routing
- [`../software-workflow-automation/SKILL.md`](../software-workflow-automation/SKILL.md) — Inngest/Temporal durable substrate

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.
