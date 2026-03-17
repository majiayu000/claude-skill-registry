---
name: fullstack-spec
description: Bridge frontend features to backend implementation. Describe what you want in the UI, get specs for both frontend AND backend.
allowed-tools: Read, Write, Glob, Grep, Edit, Bash, mcp__memory__*
context: full
agent: general-purpose
model: claude-opus-4-5-20250514
---

# fullstack-spec

**The Frontend-to-Backend Bridge (Module-Aware)**

You describe a feature in plain language. This skill generates:
1. **Module identification** - Which backend module(s) are involved
2. **Interface contracts** - How modules communicate
3. **Frontend component spec** - What to build in the UI
4. **Backend module spec** - Which module handles what
5. **Database changes** - If new data is required
6. **Implementation instructions** - Step-by-step for Claude

## Core Principle: Modularity

**Every feature must respect module boundaries.**

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MODULAR ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  FRONTEND MODULES          MIDDLEWARE           BACKEND MODULES     │
│  (React/Next.js)           (API Layer)          (Python/Services)   │
│                                                                     │
│  ┌─────────────┐          ┌───────────┐        ┌─────────────────┐ │
│  │ UI Module   │ ───────▶ │ API Route │ ─────▶ │ Module 1:       │ │
│  │ (Component) │          │ (Contract)│        │ Ingestion       │ │
│  └─────────────┘          └───────────┘        ├─────────────────┤ │
│                                                │ Module 2:       │ │
│  ┌─────────────┐          ┌───────────┐        │ Graph Maint.    │ │
│  │ State       │ ◀─────── │ Response  │ ◀───── ├─────────────────┤ │
│  │ Management  │          │ Contract  │        │ Module 3:       │ │
│  └─────────────┘          └───────────┘        │ Output Engine   │ │
│                                                ├─────────────────┤ │
│  Interface contracts       Versioned APIs      │ Module 4:       │ │
│  between all layers        with schemas        │ AI Analysis     │ │
│                                                ├─────────────────┤ │
│                                                │ Module 5:       │ │
│                                                │ Human Decision  │ │
│                                                ├─────────────────┤ │
│                                                │ Module 6:       │ │
│                                                │ Trust & Audit   │ │
│                                                └─────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

## When To Use

- You've designed a UI feature but don't know what backend changes are needed
- You want to describe a feature and get the full technical spec
- Starting a new feature and want to plan both ends together
- Need to understand which MODULE a feature touches
- User mentions: "I want to add", "build a feature", "implement this UI", "frontend to backend"

## The Problem This Solves

```
BEFORE: "I added a button to the UI... now what does the backend need?"
        → Confusion about data flow, module boundaries, interface contracts

AFTER:  Describe feature → Get module mapping → Get interface contracts
        → Clear implementation path that respects modularity
```

## Workflow

### 1. Identify Which Modules Are Involved

**FIRST STEP: Map the feature to backend modules**

| Module | Responsibilities | Touch This If... |
|--------|------------------|------------------|
| **M1: Ingestion** | Fetch, parse, import legislation | Adding/updating legislation data |
| **M2: Graph Maintenance** | Amendments, versions, health | Changing graph structure, versioning |
| **M3: Output Engine** | Queries, validation, responses | Reading/querying data, API responses |
| **M4: AI Analysis** | LLM analysis, confidence scoring | AI-powered features, extraction |
| **M5: Human Decision** | Review queues, approvals | Human-in-loop workflows |
| **M6: Trust & Audit** | Provenance, audit trail | Any data changes requiring audit |

**Feature → Module Mapping Examples:**

| Feature | Modules Touched | Why |
|---------|-----------------|-----|
| "View obligation details" | M3 (Output) | Read-only query |
| "Edit obligation" | M3 + M5 + M6 | Output + Human Decision + Audit |
| "AI-suggest obligation" | M4 + M5 + M6 | AI Analysis + Human Approval + Audit |
| "Import new Act" | M1 + M2 + M6 | Ingestion + Graph + Audit |
| "Track changes over time" | M2 + M3 | Versioning + Query |

### 2. Understand the Feature

Ask these questions:

1. **What should the user be able to do?**
   - Action: "View", "Create", "Edit", "Delete", "Filter", "Search"
   - Object: What are they acting on? (obligations, schemes, evidence)

2. **Which modules does this touch?** (Use table above)
   - Read-only? → M3 Output Engine
   - Creates/modifies data? → Add M5 + M6
   - AI-involved? → Add M4

3. **Where does the data come from?**
   - Existing: Already in Neo4j/Supabase?
   - New: Needs new data model?
   - External: From an API?

4. **Who can do this?**
   - Public (no auth)
   - Authenticated user
   - Admin only (M5 workflow)

5. **What happens after?**
   - UI updates
   - Data changes → M6 audit
   - Notifications

### 2. Detect Project Context

Read the project's CLAUDE.md to understand:
- Tech stack (React/Next.js, Python/FastAPI, Node/Express)
- Database (Neo4j, Supabase, SQLite)
- API patterns (REST, GraphQL, tRPC)
- Existing API structure

For apex-governance:
```
Frontend: React + Vite
Backend: FastAPI (Python)
Database: Neo4j (graph) + SQLite (app state)
API: REST at /api/*
Auth: Clerk
```

For apex-lens:
```
Frontend: Next.js 16 (App Router)
Backend: API routes proxy to services
Database: Neo4j (via apex-helix) + Supabase
API: Next.js API routes → microservices
Auth: Supabase
```

### 3. Define Interface Contracts

**Every cross-module call needs a contract:**

```typescript
// Interface Contract Template
interface ModuleContract {
  // Input schema (what the caller sends)
  request: {
    schema: "module.operation.v1";
    data: RequestType;
  };

  // Output schema (what the module returns)
  response: {
    success: boolean;
    data?: ResponseType;
    error?: { code: string; message: string };
    metadata: {
      module: string;
      operation: string;
      timestamp: string;
      audit_id?: string;  // If M6 involved
    };
  };
}
```

**Contract between layers:**

```
┌─────────────────┐     Contract A     ┌─────────────────┐
│  FRONTEND       │ ◀───────────────▶ │  MIDDLEWARE     │
│  (React)        │  - Request DTO     │  (API Routes)   │
│                 │  - Response DTO    │                 │
└─────────────────┘  - Error codes     └────────┬────────┘
                                                │
                                         Contract B
                                                │
                     ┌──────────────────────────┼──────────────────────────┐
                     │                          ▼                          │
              ┌──────┴──────┐           ┌──────────────┐           ┌───────┴─────┐
              │ Module 3    │           │ Module 4     │           │ Module 6    │
              │ Output      │◀─────────▶│ AI Analysis  │◀─────────▶│ Audit       │
              └─────────────┘ Contract C└──────────────┘ Contract D└─────────────┘
```

### 4. Generate Fullstack Spec

Output a complete specification:

```markdown
# Feature Spec: [Feature Name]

## User Story
As a [role], I want to [action] so that [benefit].

## Module Impact Analysis

| Module | Impact | Changes Required |
|--------|--------|------------------|
| M3: Output | Primary | New query endpoint |
| M5: Human Decision | Secondary | Approval workflow |
| M6: Audit | Required | Audit logging |

## Data Flow Diagram (Module-Aware)

```
User Action → UI Component → API Contract → Module Router
                                               │
                            ┌──────────────────┼──────────────────┐
                            ▼                  ▼                  ▼
                      M3: Output         M4: AI (if needed)  M6: Audit
                            │                  │                  │
                            └──────────────────┴──────────────────┘
                                               │
                                               ▼
                                          Neo4j/DB
```

---

## FRONTEND SPEC (Modular)

### Frontend Module Structure

Frontend components should be organized by domain, not by type:

```
src/
├── modules/                    # Feature modules (domain-driven)
│   ├── obligations/            # Obligation feature module
│   │   ├── components/         # UI components for this module
│   │   │   ├── ObligationCard.tsx
│   │   │   └── ObligationList.tsx
│   │   ├── hooks/              # Data hooks for this module
│   │   │   └── useObligations.ts
│   │   ├── api/                # API contracts for this module
│   │   │   └── obligations.api.ts
│   │   └── index.ts            # Public exports only
│   ├── legislation/            # Legislation feature module
│   └── compliance/             # Compliance feature module
├── shared/                     # Cross-module shared code
│   ├── components/             # Design system components
│   ├── hooks/                  # Generic hooks
│   └── utils/                  # Utilities
└── app/                        # Next.js routes (thin, imports modules)
```

### Component: [ComponentName]

**Module:** `src/modules/[domain]/components/[ComponentName].tsx`

**Exports:** Only via module index (encapsulation)
```typescript
// src/modules/obligations/index.ts
export { ObligationCard } from './components/ObligationCard';
export { useObligations } from './hooks/useObligations';
// Internal components NOT exported
```

**Props:**
```typescript
interface [ComponentName]Props {
  // Props definition
}
```

**State:**
```typescript
// Local state
const [loading, setLoading] = useState(false);
const [error, setError] = useState<string | null>(null);
const [data, setData] = useState<DataType | null>(null);
```

**Data Fetching (via module hook):**
```typescript
// Use module-specific hook, not direct API call
import { useObligations } from '@/modules/obligations';

const { data, isLoading, error } = useObligations(id);
```

**User Interactions:**
| Interaction | Handler | Module API | Backend Module |
|-------------|---------|------------|----------------|
| Click button | handleAction() | obligations.api.ts | M3: Output |
| Submit form | handleSubmit() | obligations.api.ts | M3 + M5 + M6 |

**Design System:**
- [ ] Uses [Trustee/Saville] tokens
- [ ] Touch targets ≥44px
- [ ] Focus indicators visible

---

## MIDDLEWARE SPEC (API Layer)

### API Route Contract

**Location:** `src/app/api/[domain]/route.ts` (Next.js) or `main.py` (FastAPI)

**Purpose:** Route requests to correct backend module, enforce contracts

```typescript
// Middleware responsibility: Route to module, NOT implement logic
export async function POST(request: Request) {
  // 1. Validate request against contract schema
  const body = await validateRequest(RequestSchema, request);

  // 2. Check auth/permissions
  const user = await requireAuth(request);

  // 3. Route to appropriate MODULE (not implement here)
  const result = await moduleRouter.dispatch({
    module: 'M3_OUTPUT',  // or M4_AI, M5_HUMAN, etc.
    operation: 'query_obligations',
    payload: body,
    context: { user, audit: true }
  });

  // 4. Return standardized response
  return Response.json(result);
}
```

---

## BACKEND MODULE SPEC

### Module: [Module Name] (e.g., M3: Output Engine)

**Responsibility:** [Single responsibility from architecture doc]

**This module ONLY handles:**
- [Specific responsibility 1]
- [Specific responsibility 2]

**This module does NOT:**
- [What other modules handle]

### Module Interface

```python
# Each module exposes a standard interface
class OutputEngineModule:
    """
    Module 3: Output Engine
    Responsibility: Query processing, response building, guardrails
    """

    def handle(self, request: ModuleRequest) -> ModuleResponse:
        """
        Standard module entry point

        Input Contract:
          - operation: str (e.g., "query_obligations")
          - payload: dict (operation-specific)
          - context: dict (user, permissions, audit_id)

        Output Contract:
          - success: bool
          - data: dict (operation-specific)
          - metadata: dict (module, timestamp, etc.)
        """
        pass
```

### Operation: [operation_name]

**Module:** M[X]: [Module Name]

**Input Contract:**
```python
@dataclass
class QueryObligationsRequest:
    filters: dict
    pagination: PaginationParams
    include_relationships: bool = False
```

**Output Contract:**
```python
@dataclass
class QueryObligationsResponse:
    obligations: List[Obligation]
    total_count: int
    page: int
    has_more: bool
```

**Cross-Module Calls:** (if this operation calls other modules)
```
M3: Output → M6: Audit (log query for compliance)
M3: Output → M4: AI (if semantic search requested)
```

**Authorization:**
- Required role: [public/user/admin]
- Ownership check: [if applicable]

**Error Cases:**
| Condition | Error Code | Handling Module |
|-----------|------------|-----------------|
| Not found | NOT_FOUND | M3 (this module) |
| Unauthorized | UNAUTHORIZED | Middleware |
| Invalid input | VALIDATION_ERROR | Middleware |
| AI failure | AI_UNAVAILABLE | M4 (graceful degrade) |

---

## DATABASE CHANGES

### Neo4j (if graph data)

**New Node Type:** (if needed)
```cypher
(:NewNode {
  id: String,
  created_at: DateTime,
  // ...
})
```

**New Relationship:** (if needed)
```cypher
(:ExistingNode)-[:NEW_RELATIONSHIP {
  // properties
}]->(:OtherNode)
```

**Required Query:**
```cypher
// Query the frontend will need
MATCH (n:Node {id: $id})
RETURN n
```

### Supabase/SQLite (if app state)

**Table Changes:**
```sql
-- If new table needed
CREATE TABLE feature_table (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW()
);

-- If column needed
ALTER TABLE existing_table ADD COLUMN new_column TYPE;
```

---

## IMPLEMENTATION INSTRUCTIONS (Module-Aware)

### For Claude (Copy-Paste This)

```
CONTEXT:
- Project: [apex-governance/apex-lens]
- Feature: [Feature name]
- Modules Touched: [M3: Output, M5: Human Decision, M6: Audit]

MODULARITY REQUIREMENTS:
- Each module is independent - changes in one don't break others
- All cross-module calls use interface contracts
- Frontend modules mirror backend module boundaries

TASK (in order):
1. BACKEND MODULE: Add operation to [Module Name] at [path]
   - Define input/output contracts
   - Implement module logic ONLY (not API)
   - Add cross-module calls if needed

2. MIDDLEWARE: Add API route at [path]
   - Validate request against contract
   - Route to module (don't implement logic here)
   - Return standardized response

3. FRONTEND MODULE: Add to src/modules/[domain]/
   - Create hook that calls API
   - Create component that uses hook
   - Export only public interface

4. INTEGRATION: Wire module to page/layout
   - Import from module index only
   - Don't import internal module files

CONSTRAINTS:
- Modules communicate ONLY via contracts
- No direct database calls from middleware
- No business logic in API routes
- Frontend imports via module index only
- All changes logged to M6: Audit
```

### Step-by-Step (For Non-Coders, Module-Aware)

**Key principle: Build from the inside out (data → module → API → UI)**

1. **Identify modules**
   Ask Claude: "Which modules does [feature] touch?"
   → Get module list and responsibilities

2. **Build backend module operation**
   Tell Claude: "In Module [X], add operation [name] that [description]"
   Tell Claude: "Define input/output contracts for this operation"

3. **Add middleware route**
   Tell Claude: "Add API route /api/[path] that routes to Module [X]"
   Tell Claude: "The route should validate inputs, not implement logic"

4. **Create frontend module**
   Tell Claude: "Create hook use[Feature] in src/modules/[domain]/hooks/"
   Tell Claude: "Create component [Name] in src/modules/[domain]/components/"
   Tell Claude: "Export via src/modules/[domain]/index.ts"

5. **Wire to page**
   Tell Claude: "Import [Feature] from '@/modules/[domain]' and add to [page]"

6. **Test boundaries**
   Tell Claude: "Verify [feature] works if Module [Y] is unavailable"
   → This tests module independence
```

### 4. Apex-Specific Patterns

For apex-governance (Python FastAPI + React):

```
┌─────────────────────────────────────────────────────────────────────┐
│ APEX-GOVERNANCE FULLSTACK PATTERN                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  frontend/src/                    backend/                          │
│  ├── pages/                       ├── main.py (endpoints)           │
│  │   └── Feature.jsx              ├── persistence.py (SQLite)       │
│  ├── components/                  ├── database.py (Neo4j)           │
│  │   └── FeatureComponent.jsx     ├── models.py (Pydantic)          │
│  └── hooks/                       └── scoring.py (if compliance)    │
│      └── useFeature.js                                              │
│                                                                     │
│  Data Flow:                                                         │
│  Component → fetch('/api/...') → main.py → Neo4j/SQLite → Response  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

For apex-lens (Next.js + Services):

```
┌─────────────────────────────────────────────────────────────────────┐
│ APEX-LENS FULLSTACK PATTERN                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  src/                                                               │
│  ├── app/                         External Services:                │
│  │   └── api/                     ├── apex-helix (3001)             │
│  │       └── helix/               ├── apex-precedent (3002)         │
│  │           └── route.ts         └── apex-kestrel (3003)           │
│  ├── components/                                                    │
│  │   └── FeatureComponent.tsx                                       │
│  └── hooks/                                                         │
│      └── use-feature.ts (React Query)                               │
│                                                                     │
│  Data Flow:                                                         │
│  Component → useQuery → /api/helix/* → proxy → apex-helix → Neo4j   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 5. Example: Adding "Favourite Obligations" Feature (Module-Aware)

**User Request:** "I want users to be able to favourite obligations"

**Generated Spec:**

```markdown
# Feature Spec: Favourite Obligations

## User Story
As a trustee, I want to favourite obligations so that I can quickly access the ones most relevant to my scheme.

## Module Impact Analysis

| Module | Impact | Reason |
|--------|--------|--------|
| **M3: Output** | Primary | Query favourites, return with obligations |
| **M5: Human Decision** | None | No approval workflow needed |
| **M6: Audit** | Required | Log favourite actions for compliance |

**Modules NOT touched:**
- M1: Ingestion (not importing data)
- M2: Graph Maintenance (not modifying graph structure)
- M4: AI Analysis (no AI involved)

## Data Flow (Module-Aware)

```
User clicks star
       │
       ▼
┌─────────────────────┐     Contract A     ┌─────────────────────┐
│  FRONTEND MODULE    │ ─────────────────▶ │  MIDDLEWARE         │
│  src/modules/       │  POST /api/        │  API Route          │
│    favourites/      │  favourites        │  (validates only)   │
└─────────────────────┘                    └──────────┬──────────┘
                                                      │
                                               ┌──────┴──────┐
                                               ▼             ▼
                                         ┌──────────┐  ┌──────────┐
                                         │ M3:Output│  │ M6:Audit │
                                         │ (save)   │─▶│ (log)    │
                                         └──────────┘  └──────────┘
```

---

## FRONTEND MODULE SPEC

### Module: `src/modules/favourites/`

```
src/modules/favourites/
├── components/
│   └── FavouriteButton.tsx      # The star button
├── hooks/
│   └── useFavourites.ts         # Data fetching hook
├── api/
│   └── favourites.api.ts        # API contract definitions
└── index.ts                     # Public exports ONLY
```

**Public Exports (index.ts):**
```typescript
// ONLY export what other modules need
export { FavouriteButton } from './components/FavouriteButton';
export { useFavourites, useToggleFavourite } from './hooks/useFavourites';
export type { Favourite } from './api/favourites.api';
```

**API Contract (favourites.api.ts):**
```typescript
// Contract matches backend module interface
export interface ToggleFavouriteRequest {
  entity_type: 'obligation' | 'legislation' | 'definition';
  entity_id: string;
}

export interface ToggleFavouriteResponse {
  success: boolean;
  data: { favourited: boolean; favourite_id?: string };
  metadata: { module: 'M3_OUTPUT'; audit_id: string };
}
```

---

## MIDDLEWARE SPEC

### API Route: POST /api/favourites

**Location:** `src/app/api/favourites/route.ts`

**Responsibility:** Validate and route (NOT implement)

```typescript
import { moduleRouter } from '@/lib/module-router';
import { ToggleFavouriteRequest } from '@/modules/favourites';

export async function POST(request: Request) {
  // 1. Validate against contract
  const body = await validateRequest(ToggleFavouriteRequest, request);

  // 2. Auth check
  const user = await requireAuth(request);

  // 3. Route to M3: Output (NOT implement here)
  const result = await moduleRouter.dispatch({
    module: 'M3_OUTPUT',
    operation: 'toggle_favourite',
    payload: body,
    context: { user_id: user.id, audit: true }
  });

  return Response.json(result);
}
```

---

## BACKEND MODULE SPEC

### Module: M3 Output Engine

**Operation:** `toggle_favourite`

```python
# backend/modules/output_engine.py

class OutputEngineModule:

    def toggle_favourite(
        self,
        request: ToggleFavouriteRequest,
        context: RequestContext
    ) -> ToggleFavouriteResponse:
        """
        Module 3 operation: Toggle user favourite

        Cross-module calls:
        - M6: Audit → log the action
        """
        # 1. Check existing favourite
        existing = self.persistence.get_favourite(
            user_id=context.user_id,
            entity_type=request.entity_type,
            entity_id=request.entity_id
        )

        # 2. Toggle
        if existing:
            self.persistence.delete_favourite(existing.id)
            favourited = False
        else:
            fav = self.persistence.create_favourite(
                user_id=context.user_id,
                entity_type=request.entity_type,
                entity_id=request.entity_id
            )
            favourited = True

        # 3. Cross-module call to M6: Audit
        audit_id = self.audit_module.log_action(
            action='favourite_toggle',
            user_id=context.user_id,
            entity_type=request.entity_type,
            entity_id=request.entity_id,
            result=favourited
        )

        return ToggleFavouriteResponse(
            success=True,
            data={'favourited': favourited},
            metadata={'module': 'M3_OUTPUT', 'audit_id': audit_id}
        )
```

---

## DATABASE CHANGES

### SQLite (app state - NOT in Neo4j graph)

```sql
-- Favourites are user preferences, not graph data
CREATE TABLE IF NOT EXISTS favourites (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  entity_type TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(user_id, entity_type, entity_id)
);
```

**Why SQLite not Neo4j?**
- Favourites are USER state, not KNOWLEDGE state
- Keeps graph clean (separation of concerns)
- Faster for user-specific queries

---

## IMPLEMENTATION INSTRUCTIONS (For Claude)

```
CONTEXT:
- Project: apex-governance
- Feature: Favourite obligations
- Modules: M3 (Output), M6 (Audit)

ORDER OF IMPLEMENTATION:

1. BACKEND MODULE (M3: Output)
   - Add toggle_favourite operation to output_engine.py
   - Add cross-module call to M6 for audit logging
   - Define input/output dataclasses

2. DATABASE
   - Add favourites table to persistence.py
   - Add get_favourite, create_favourite, delete_favourite methods

3. MIDDLEWARE
   - Add POST /api/favourites route
   - Route to M3, don't implement logic

4. FRONTEND MODULE
   - Create src/modules/favourites/ directory
   - Add FavouriteButton component
   - Add useFavourites hook
   - Export via index.ts

5. INTEGRATION
   - Import FavouriteButton from '@/modules/favourites'
   - Add to ObligationCard

MODULARITY TEST:
- Feature should work if M4 (AI) module is unavailable
- Audit should log even if UI fails to update
```
```

## Model Preference

**opus** - Fullstack planning requires understanding entire system architecture

---
*Part of 45Black UI Expert Devstack*
*For non-coders: Describe what you want, get specs for frontend AND backend*
