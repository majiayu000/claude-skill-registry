---
name: project-context
category: context
version: 1.0.0
description: NodeJS-Starter-V1 specific knowledge
priority: 2
---

# Project Context Skill

Project-specific knowledge for NodeJS-Starter-V1.

## Technology Stack

### Frontend
- **Framework**: Next.js 15 (App Router)
- **UI Library**: React 19
- **Styling**: Tailwind v4
- **Components**: shadcn/ui
- **Icons**: AI-generated custom (NO Lucide)

### Backend
- **Framework**: FastAPI (Python 3.12)
- **Agents**: LangGraph
- **Validation**: Pydantic
- **Async**: asyncio

### Database
- **Platform**: Supabase
- **Database**: PostgreSQL
- **Vectors**: pgvector
- **Auth**: Row Level Security (RLS)

### Tooling
- **Monorepo**: Turborepo + pnpm workspaces
- **Package Manager**: pnpm 9+
- **Node**: 20+
- **Python**: 3.12+

## Architecture Patterns

### Monorepo Structure
```
apps/
  web/          # Next.js frontend
  backend/      # FastAPI backend
packages/
  shared/       # Shared types
  config/       # Shared configs
```

### Layer Separation
```
Frontend: Components → Hooks → API Routes → Services
Backend:  API → Agents → Tools → Graphs → State
Database: Tables → RLS → Functions → Triggers
```

**Rule**: No cross-layer imports

### Verification-First
- Prove It Works
- Honest Failure Reporting
- No Assumptions
- Root Cause First
- One Fix at a Time

## Key Systems

### Agent Orchestration
- Master orchestrator coordinates subagents
- Independent verification (no self-attestation)
- Context partitioning for token efficiency

### Tool Registry
- Advanced tool search
- Programmatic calling
- Dependency resolution

### Long-Running Agents
- Multi-session via progress files
- State persistence
- Resume capability

### Memory System
- Vector-based (pgvector)
- Persistent knowledge
- Domain-specific memory

## Australian Context

- **Language**: en-AU (always)
- **Currency**: AUD
- **Locations**: Brisbane (primary), Sydney, Melbourne
- **Regulations**: Privacy Act 1988, WCAG 2.1 AA

## Design System

- **Aesthetic**: 2025-2026 modern (Bento, glassmorphism)
- **NO Lucide icons**: AI-generated custom only
- **Primary Color**: #0D9488 (teal)
- **Shadows**: Soft colored (never pure black)

## Commands

```bash
# Development
pnpm dev                          # All services
pnpm dev --filter=web             # Frontend only

# Database
supabase start && supabase db push

# Quality
pnpm turbo run type-check lint test

# Pre-PR
pnpm turbo run type-check lint test && echo "✅ Ready"
```

## Migrations

8 total migrations in `supabase/migrations/`:
1. init - UUID, triggers
2. auth_schema - profiles, RLS
3. enable_pgvector - vectors
4. state_tables - conversations, tasks
5. audit_evidence - verification
6. copywriting_consistency - business data
7. agent_runs_realtime - real-time status
8. domain_memory - persistent memory

## Never

- Use American spelling
- Use Lucide icons
- Skip verification
- Cross layer boundaries
- Self-verify own work
