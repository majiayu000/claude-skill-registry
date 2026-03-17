---
# ═══════════════════════════════════════════════════════════════════════════
# SKILL: Core Development
# Version: 2.0.0 | Updated: 2025-01
# ═══════════════════════════════════════════════════════════════════════════
name: core-development
description: Master core development paths - Frontend, Backend, Full Stack, DevOps. Atomic skill for learning sequences and technology stack recommendations.

# ACTIVATION TRIGGERS
triggers:
  - frontend
  - backend
  - full-stack
  - fullstack
  - devops
  - web development

# SKILL PARAMETERS
parameters:
  path:
    type: string
    enum: [frontend, backend, fullstack, devops]
    required: true
    description: Target development path
  level:
    type: string
    enum: [beginner, intermediate, advanced]
    required: false
    default: beginner

# OUTPUT SPECIFICATION
outputs:
  learning_path:
    type: array
    description: Ordered learning sequence
  tech_stack:
    type: object
    description: Recommended technologies
  timeline:
    type: string
    description: Estimated learning duration

# RELIABILITY
retry:
  max_attempts: 3
  backoff: exponential
  initial_delay_ms: 1000

# OBSERVABILITY
observability:
  log_level: info
  metrics: [invocation_count, success_rate]

# PREREQUISITES
prerequisites:
  - programming-basics
  - git-basics

level: intermediate

sasmp_version: "1.3.0"
bonded_agent: 01-core-paths
bond_type: PRIMARY_BOND
---

# Core Development Skill

## Quick Reference

| Path | Duration | Entry Point | Exit Point |
|------|----------|-------------|------------|
| **Frontend** | 3-6 mo | HTML/CSS | React/Vue + Testing |
| **Backend** | 6-12 mo | Language | API + DB + Deploy |
| **Full Stack** | 9-15 mo | Frontend | Full app + DevOps |
| **DevOps** | 12-24 mo | Linux | K8s + IaC + CI/CD |

---

## Learning Paths

### Frontend
```
[1] HTML5 + CSS3 (2-3 wk)
 │
 ▼
[2] JavaScript ES6+ (4-6 wk)
 │
 ▼
[3] React 19 / Vue 3 (4-6 wk)
 │
 ▼
[4] State + Testing (2-4 wk)
 │
 ▼
[5] Deploy + CI/CD (1-2 wk)
```

**2025 Stack:** TypeScript + React 19 + Tailwind v4 + Vite + Vitest

---

### Backend
```
[1] Python or JavaScript (4-6 wk)
 │
 ▼
[2] Framework: FastAPI / NestJS (4-6 wk)
 │
 ▼
[3] Database: PostgreSQL (3-4 wk)
 │
 ▼
[4] APIs + Auth (3-4 wk)
 │
 ▼
[5] Testing + Deploy (2-4 wk)
```

**2025 Stack:** Python + FastAPI + PostgreSQL + Redis + Docker

---

### Full Stack
```
[1] Frontend Mastery (3-4 mo)
 │
 ▼
[2] Backend Mastery (4-6 mo)
 │
 ▼
[3] Integration + DevOps (2-4 mo)
```

**2025 Stack:** Next.js 15 + PostgreSQL + Vercel

---

### DevOps
```
[1] Linux + Bash (4-6 wk)
 │
 ▼
[2] Docker (2-3 wk)
 │
 ▼
[3] Kubernetes (6-8 wk)
 │
 ▼
[4] Cloud: AWS/GCP (8-12 wk)
 │
 ▼
[5] Terraform + CI/CD (4-6 wk)
```

**2025 Stack:** Docker + Kubernetes + Terraform + GitHub Actions

---

## Technology Matrix

| Component | Frontend | Backend | Full Stack | DevOps |
|-----------|----------|---------|------------|--------|
| **Language** | TypeScript | Python/JS | TypeScript | Bash/Python |
| **Framework** | React 19 | FastAPI | Next.js 15 | - |
| **Styling** | Tailwind | - | Tailwind | - |
| **Database** | - | PostgreSQL | PostgreSQL | - |
| **Testing** | Vitest | pytest | Playwright | - |
| **Deploy** | Vercel | Docker | Vercel | K8s |

---

## Troubleshooting Decision Tree

```
Which path should I choose?
├─► Like visual/creative work? → Frontend
├─► Prefer logic/algorithms? → Backend
├─► Want to build complete products? → Full Stack
└─► Love automation/infrastructure? → DevOps

Stuck in tutorial hell?
├─► Stop watching, start building
├─► Pick ONE project and finish it
├─► 70% building, 30% learning
└─► Deploy something live today

Can't find a job?
├─► Portfolio too weak? → Build 3 real projects
├─► No GitHub activity? → Contribute to open source
├─► Resume weak? → Add measurable achievements
└─► No network? → Join communities, attend meetups
```

---

## Common Failure Modes

| Symptom | Root Cause | Recovery Action |
|---------|------------|-----------------|
| Analysis paralysis | Too many options | Pick popular stack, start today |
| Outdated learning | Using old resources | Check resource date (must be 2024+) |
| Impostor syndrome | Comparing to experts | Focus on daily improvement |
| Burnout | Too fast, too much | 1-2 hours/day consistently |

---

## Validation Checklist

Before marking path complete:
- [ ] Can build project from scratch without tutorial
- [ ] Understand WHY, not just HOW
- [ ] Have 3+ portfolio projects deployed
- [ ] Can explain concepts to others
- [ ] Passed technical interview questions

---

## Next Actions

Run `/learn` for personalized guidance on your chosen path.
