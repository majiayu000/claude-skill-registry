---
name: artifact-aggregator
description: Create tiered reports (micro/standard/comprehensive) based on task complexity. Tier 1 (200-500 words) for Level 1 tasks, Tier 2 (500-1500 words) for Level 2, Tier 3 (1500-5000 words) for Level 3 epics. Synthesizes agent outputs into concise, scannable reports without duplication. Uses density over volume, actionable over descriptive. Triggers ONLY after multi-agent completion (2+ agents) or complex investigations. NOT for single-agent trivial tasks.
---

# Artifact Aggregator

## Overview

Synthesize outputs from multiple agents or complex investigations into concise, actionable reports that preserve critical knowledge without duplication or verbosity. Transform scattered findings into structured artifacts that humans actually read and find useful.

## Core Principles

### 1. Density Over Volume
- **Goal**: Maximum insight per word
- ❌ **Bad**: "The backend agent implemented the authentication system. First, it created models. Then it created endpoints. Then it added tests."
- ✅ **Good**: "Auth system complete: JWT models (user.py:42), /auth/login endpoint (api/auth.py:28), 12 tests passing."

### 2. No Duplication
- **Rule**: Every fact stated exactly once
- If backend and frontend both touched User model, mention once with both contexts
- Consolidate overlapping findings across agents

### 3. Actionable Over Descriptive
- **Focus**: What can reader DO with this information
- ✅ **Good**: "Next: Add password reset flow (backend/app/api/auth.py)"
- ❌ **Bad**: "The password reset functionality is not yet implemented"

### 4. Structure Over Stream
- **Format**: Scannable hierarchy, not narrative prose
- Use headings, bullets, code blocks
- Enable quick navigation to relevant sections

## When to Use

Invoke this skill when:
- **Multi-agent completion**: 2+ agents finished, need consolidated report
- **Knowledge preservation**: Research findings valuable for future work
- **Handoff documentation**: Passing project to another developer/team
- **Final summaries**: Project phase complete, stakeholders need overview
- **Complex investigations**: Deep dives need distillation for consumption

**DO NOT use** when:
- Single agent completed trivial task (just report directly)
- Output is already structured and concise
- No new knowledge beyond what user already knows
- Immediate next action is obvious (just do it, don't document first)

## Report Tiers

Select appropriate report tier based on orchestration level and task complexity:

### Tier 1: Micro Report (Level 1 tasks)

**Target:** 200-500 words, 50-100 lines
**Use for:** Single-agent delegations, simple tasks
**Time to read:** Under 2 minutes

**Structure:**
```markdown
# {Task Name}

## What Changed
- {file:line} - {concise change description}
- {file:line} - {concise change description}

## Next Steps
1. {actionable item}
2. {actionable item}
```

**Quality gates:**
- ✅ No fluff or narrative
- ✅ All file references have line numbers
- ✅ Next steps are immediately actionable
- ✅ Total word count under 500

**Example:**
```markdown
# Add Pagination to Tasks Endpoint

## What Changed
- backend/app/api/tasks.py:45 - Added limit/offset query params
- backend/app/api/tasks.py:67 - Return total count in headers
- backend/tests/test_tasks.py:120 - Added pagination tests

## Next Steps
1. Update frontend TasksList to use pagination (frontend/components/TasksList.tsx)
2. Add pagination UI controls (previous/next buttons)

[Total: 82 words]
```

### Tier 2: Standard Report (Level 2 tasks)

**Target:** 500-1500 words, 100-400 lines
**Use for:** Multi-agent orchestrations, full-stack features
**Time to read:** 3-5 minutes

**Structure:**
```markdown
# {Feature Name}

## Summary
{2-3 sentences: what, why, status}

## Changes by Domain
### Backend
- {changes with file:line}

### Frontend
- {changes with file:line}

## Integration Points
{How components connect}

## Issues Encountered
{Problems and resolutions}

## Next Steps
1. {actionable with context}
2. {actionable with context}
```

**Quality gates:**
- ✅ Scannable in under 5 minutes
- ✅ Clear domain separation
- ✅ Integration points documented
- ✅ Issues with resolutions (not just listed)
- ✅ Total word count 500-1500

**Example:** See "Example 1: Concise Feature Report" in original Examples section

### Tier 3: Comprehensive Report (Level 3 tasks)

**Target:** 1500-5000 words, 400-1000 lines
**Use for:** Epic-level work, long-term investigations, handoff documentation
**Time to read:** 10-15 minutes

**Structure:**
```markdown
# {Epic/Investigation Name}

## Executive Summary
{High-level overview for stakeholders}

## Scope & Goals
{What was attempted and why}

## Architecture Overview
{System design, major components}

## Implementation Details
### Phase 1: {Name}
{Detailed changes}

### Phase 2: {Name}
{Detailed changes}

## Technical Decisions
{Key choices and rationale}

## Integration & Dependencies
{How systems connect, external deps}

## Testing & Validation
{Coverage, results, remaining gaps}

## Performance & Scalability
{Benchmarks, bottlenecks, optimizations}

## Issues & Resolutions
{Problems encountered, how solved}

## Migration & Deployment
{Rollout strategy, risks}

## Knowledge Transfer
{What team needs to know}

## Next Steps & Roadmap
{Prioritized actions with estimates}

## Appendix
{Supporting details, full diffs, extended context}
```

**Quality gates:**
- ✅ Comprehensive but scannable (good hierarchy)
- ✅ Executive summary for non-technical stakeholders
- ✅ Technical details for implementers
- ✅ Clear handoff information
- ✅ Total word count 1500-5000 (not more!)

**Example:** See ORCHESTRATION-SUMMARY.md from Knowledge System Redesign

## Tier Selection Guide

Use this decision tree:

```
What orchestration level?
├─ Level 0 → No report (direct execution)
├─ Level 1 → Tier 1 (Micro Report)
├─ Level 2 → Tier 2 (Standard Report)
└─ Level 3 → Tier 3 (Comprehensive Report)

OR

How many agents?
├─ 0-1 agents → Tier 1
├─ 2-4 agents → Tier 2
└─ 5+ agents → Tier 3

OR

Session duration?
├─ Under 1 hour → Tier 1
├─ 1 hour - 1 day → Tier 2
└─ Multi-day/week → Tier 3
```

## Report Structure (Flexible)

Adapt this flexible structure to context:

```markdown
# [Feature/Investigation Name]

## Summary
[2-3 sentences: What was done, outcome, status]

## Key Changes
### [Domain 1: e.g., Backend]
- [File:line] - [What changed and why]
- [File:line] - [What changed and why]

### [Domain 2: e.g., Frontend]
- [File:line] - [What changed and why]

## Findings
[Critical discoveries, architectural decisions, non-obvious insights]
- [Finding 1]: [Implication]
- [Finding 2]: [Implication]

## Integration Points
[How components connect, API contracts, shared dependencies]
- [Component A] → [Component B]: [via what]

## Issues & Blockers
[Current problems, workarounds, technical debt]
- [Issue]: [Impact] - [Resolution or next step]

## Next Steps
1. [Actionable task with file/context reference]
2. [Actionable task with file/context reference]

## Appendix (Optional)
[Supporting details, full diffs, extended context - only if needed]
```

## Aggregation Workflow

### Step 1: Collect Agent Outputs

Gather artifacts from all agents:
- **Code changes**: Files modified, functions added/changed
- **Decisions made**: Architecture choices, trade-offs
- **Blockers encountered**: Issues, workarounds
- **Integration points**: APIs, contracts, shared state
- **Tests**: Coverage, failing tests, edge cases

**Collection methods:**
- Agent final reports (if they provide structured output)
- Git diff analysis (what actually changed)
- Direct questioning (ask agent for specific info)

### Step 2: Deduplicate & Consolidate

Identify redundant information:

**Example - Before deduplication:**
```
Backend Agent: "Added User model with email field"
Frontend Agent: "Created UserType with email: string"
Testing Agent: "Verified email field in User model"
```

**After consolidation:**
```
User model (backend/app/models/user.py:24) with email field
└─ TypeScript type generated (frontend/types/user.ts:8)
└─ Validated in 3 tests (test_user_model.py:15,42,58)
```

**Consolidation strategies:**
1. **Entity-centric**: Group by what was changed (User model) not who changed it
2. **Layer folding**: Combine "created endpoint" + "added tests" into single entry with sub-items
3. **Reference compression**: File paths once, line numbers inline

### Step 3: Extract Key Findings

Surface non-obvious insights:

**What qualifies as "key finding":**
- ✅ Architectural decisions (chose JWT over sessions because...)
- ✅ Performance discoveries (pagination required, initial load too slow)
- ✅ Technical constraints (WebSocket requires separate port on nginx)
- ✅ Security implications (tokens stored in httpOnly cookies)
- ❌ Obvious facts (FastAPI uses async/await)
- ❌ Implementation details already in code (function signature)

**Format:**
```markdown
## Findings

**JWT Implementation**: Used httpOnly cookies (not localStorage) for XSS protection.
Refresh tokens stored in separate cookie with longer expiry (7 days vs 30min access tokens).

**Database Schema**: User.role field added as enum (admin/user/guest). Migration
includes backfill for existing users (defaults to 'user').

**API Contract Change**: All endpoints now return ISO8601 timestamps (breaking change
from Unix timestamps). Frontend types updated, but mobile app needs notification.
```

### Step 4: Map Integration Points

Document how components connect:

**Integration point types:**
1. **API contracts**: Endpoint → Consumer(s)
2. **Type sharing**: Backend model → Frontend types
3. **Event flows**: Publisher → Subscribers
4. **Shared state**: Database tables, caches
5. **Dependencies**: Service A requires Service B

**Visualization:**
```markdown
## Integration Points

**Authentication Flow**:
POST /auth/login (api/auth.py:28)
  ↓ JWT token
React LoginForm (frontend/components/Login.tsx:42)
  ↓ Stores in cookie
Protected routes check via useAuth hook (frontend/hooks/useAuth.ts:18)

**WebSocket Notifications**:
Backend emits: NotificationEvent (websocket.py:56)
  → Frontend listens: useNotifications hook (hooks/useNotifications.ts:24)
  → Updates: NotificationBadge component (components/NotificationBadge.tsx:15)
```

### Step 5: Identify Actionable Next Steps

Convert blockers and TODO comments into concrete tasks:

**Transformation:**
```
Agent output: "Password reset not implemented yet"
↓
Next step: "Implement password reset flow:
  1. Add POST /auth/reset-password endpoint (backend/app/api/auth.py)
  2. Create ResetPasswordForm component (frontend/components/Auth/)
  3. Add email sending service integration"
```

**Prioritization:**
- **Critical**: Blockers preventing deployment
- **High**: Missing features from spec
- **Medium**: Tech debt, optimizations
- **Low**: Nice-to-haves, refactoring

### Step 6: Write Concisely

Apply compression techniques:

**Technique 1: File:line format**
```
❌ Verbose: "In the file backend/app/models/user.py, specifically at line 42,
we added a new field called 'role'"

✅ Concise: "Added User.role field (backend/app/models/user.py:42)"
```

**Technique 2: Bullets over paragraphs**
```
❌ Verbose: "The backend agent implemented three endpoints. The first endpoint was
for logging in users. The second endpoint was for logging out. The third endpoint
was for refreshing tokens."

✅ Concise:
- POST /auth/login - authenticate users
- POST /auth/logout - invalidate sessions
- POST /auth/refresh - renew access tokens
```

**Technique 3: Inline context**
```
❌ Verbose: "The NotificationBadge component was created. It shows a count of
unread notifications. It uses the useNotifications hook to get the data."

✅ Concise: "NotificationBadge (components/NotificationBadge.tsx:15) displays
unread count from useNotifications hook"
```

**Technique 4: Drop obvious**
```
❌ Includes obvious: "Created a React component using TypeScript with proper
type definitions and exported it as default"

✅ Drop obvious: "Created LoginForm component (components/Login.tsx)"
[TypeScript, proper types, default export are assumed]
```

## Report Types

### Type 1: Multi-Agent Feature Report

**Use case**: Full-stack feature implemented by multiple agents

**Structure:**
```markdown
# User Authentication Feature

## Summary
JWT-based auth implemented across backend (FastAPI) and frontend (React).
Login/logout functional, password reset pending.

## Key Changes
### Backend (fastapi-backend-expert)
- User.role field added (models/user.py:42)
- JWT service (services/auth.py:18-65)
- Auth endpoints: /login, /logout, /refresh (api/auth.py:28-92)
- 12 tests added (tests/test_auth.py)

### Frontend (React Frontend Expert (F1))
- LoginForm component (components/Login.tsx:15)
- useAuth hook (hooks/useAuth.ts:24)
- Token management (utils/auth.ts:10)
- Protected route HOC (components/ProtectedRoute.tsx:8)

## Integration
POST /auth/login → JWT token → stored in httpOnly cookie → useAuth hook reads
Protected routes use useAuth → if expired, redirect /login

## Next Steps
1. Implement password reset (backend endpoint + email integration)
2. Add "Remember me" option (extend refresh token expiry)
3. Mobile app notification (API timestamp format changed)
```

### Type 2: Research Findings Report

**Use case**: Investigation into codebase architecture or problem

**Structure:**
```markdown
# WebSocket Architecture Investigation

## Summary
Analyzed current WebSocket implementation to plan notification feature.
Found existing connection manager, but needs scaling improvements.

## Current State
- WebSocket server: backend/app/websocket.py:42
- Single connection per user (no connection pooling)
- Messages broadcast to all (no room/topic filtering)

## Findings
**Scaling Limitation**: Current design keeps all connections in memory (ConnectionManager dict).
Won't scale beyond ~1000 concurrent users. Need Redis pub/sub for horizontal scaling.

**Message Format**: Custom JSON structure, not standardized. Recommend adopting socket.io
protocol for easier client library integration.

**Error Handling**: Disconnects not properly cleaned up, causing memory leaks
(websocket.py:78 - TODO comment confirms).

## Recommendations
1. **Short-term**: Fix disconnect cleanup (critical, <1hr)
2. **Medium-term**: Add room-based filtering for notifications (1-2hrs)
3. **Long-term**: Migrate to Redis pub/sub + socket.io protocol (1 day)

## Integration Points
Frontend WebSocket client: frontend/hooks/useWebSocket.ts:24
Connects on app mount, auto-reconnects with exponential backoff
```

### Type 3: Handoff Documentation

**Use case**: Passing work to another developer

**Structure:**
```markdown
# Analysis System Implementation - Handoff

## What's Complete
✅ Provider/Agent models (models/analysis.py:12-89)
✅ AnalysisRun workflow (services/analysis_service.py:45)
✅ API endpoints: /analysis/run, /analysis/status (api/analysis.py:20-124)
✅ React dashboard: RunsTable, StatusBadge (dashboard/components/Analysis/)

## What's Pending
🟡 Proposal voting UI (spec complete, not implemented)
🟡 Background task for auto-retry failed runs (backend/tasks/analysis.py:TODO)
🔴 Performance: Runs query slow for >1000 entries (add index or pagination)

## Key Architectural Decisions
**Why async workflow**: Analysis runs can take 30+ seconds, so TaskIQ background
tasks prevent HTTP timeout. Status polled via /analysis/status endpoint.

**Why separate Proposal model**: Agents generate multiple proposals per run.
Keeping separate allows granular tracking and future proposal reuse.

## How to Continue
**Next priority**: Implement proposal voting
1. Add Vote model (models/analysis.py, follow Proposal pattern)
2. POST /analysis/proposals/{id}/vote endpoint
3. VotingCard component (copy ProposalCard structure)

**Files to read**:
- Architecture doc: docs/architecture/analysis-system.md
- Spec: .artifacts/analysis-system/spec.md
- Example run: seed_analysis_system.py (shows full workflow)
```

## Quality Checks

Before finalizing report, validate:

**Checklist:**
- [ ] **No duplication**: Each fact stated once
- [ ] **Scannable**: Can understand in 30-second skim
- [ ] **Actionable**: Next steps are clear and specific
- [ ] **Complete**: No critical info missing
- [ ] **Accurate**: File paths and line numbers correct
- [ ] **Concise**: No unnecessary words (target: <500 words for typical feature)

**Red flags:**
- Report > 1000 words (unless massive feature)
- Paragraphs > 3 sentences (break into bullets)
- Passive voice ("was implemented by" → "implemented")
- Vague next steps ("improve performance" → "add index on tasks.created_at")

## Anti-Patterns

- **Verbose narratives**: "First we did X, then we did Y, and finally..."
- **Duplicate listings**: Repeating same info in multiple sections
- **Obvious statements**: "We used TypeScript because it's typed JavaScript"
- **Missing file refs**: "Added new component" (which file?)
- **Vague next steps**: "Fix remaining issues" (which issues, where?)
- **Implementation details**: Including full function signatures in summary

## Examples

### Example 1: Concise Feature Report
```markdown
# Real-Time Notifications

## Summary
WebSocket notifications functional. Backend emits events, React displays badge with count.

## Changes
**Backend** (websocket.py:42): NotificationEvent emitter, /ws endpoint
**Frontend**:
- useNotifications hook (hooks/useNotifications.ts:24) - subscribes to ws://localhost:8000/ws
- NotificationBadge (components/NotificationBadge.tsx:15) - displays unread count

## Next
1. Add notification history modal (component + backend storage)
2. Mark-as-read functionality (PATCH /notifications/{id})

[Total: 82 words]
```

### Example 2: Research Findings (Dense)
```markdown
# Task Classification Performance Analysis

## Findings
**Current**: 850ms avg response time (classify endpoint)
**Bottleneck**: Pydantic AI initialization on every request (llm.py:34)

**Root cause**: No model caching. Each request:
1. Loads model weights (400ms)
2. Initializes agent (250ms)
3. Runs classification (200ms)

## Fix
Move model init to app startup (main.py lifespan context):
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.classifier = await init_classifier()  # Once at startup
    yield
```

**Expected**: 200ms avg (74% improvement)

[Total: 94 words, highly dense]
```

## Integration with Other Skills

- **parallel-coordinator**: Provides agent outputs to aggregate
- **Task Orchestrator**: Uses aggregator for final reports
- **Docs Expert (D2)**: May refine aggregated content for docs
- **Standalone**: Can aggregate any multi-source information

## Notes

- Prioritize density: every word must earn its place
- File:line references enable quick navigation
- Structure enables scanning (headings, bullets, code blocks)
- No duplication: consolidate overlapping findings
- Actionable next steps > descriptive status
- Target <500 words for typical feature reports
