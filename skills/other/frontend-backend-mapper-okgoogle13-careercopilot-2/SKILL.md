---
name: frontend-backend-mapper
description: "Analyzes and maps frontend API calls to backend endpoints. Detects missing endpoints, unused endpoints, and integration gaps. Optional: trace complete data flows to database and design tokens. Related: api-contract-validator for detailed type analysis."
---

# Frontend-Backend Mapper Workflow

This skill analyzes the integration between frontend API services and backend endpoints to ensure complete coverage. It can optionally trace complete data flows including database operations and design token usage.

## Workflow Steps

1. **Scan frontend API services:**
   - Read all files in `frontend/src/api/*.ts`
   - Extract API call patterns:
     - Function names (e.g., `generateKscResponses`)
     - HTTP methods (GET, POST, PUT, DELETE)
     - URL paths (e.g., `/api/v1/ksc/generate`)
     - Request/response TypeScript interfaces
   - Build frontend API inventory

2. **Scan backend endpoints:**
   - Read all files in `backend/app/api/endpoints/*.py`
   - Extract route definitions:
     - Route decorators (`@router.post`, `@router.get`)
     - URL paths
     - Request/response Pydantic models
     - Function names
   - Build backend endpoint inventory

3. **Perform integration analysis:**
   - Match frontend calls to backend endpoints
   - Identify ✅ **MAPPED** integrations (frontend ↔ backend)
   - Identify ❌ **MISSING BACKEND** endpoints (frontend calls with no backend)
   - Identify ❌ **UNUSED BACKEND** endpoints (backend routes with no frontend)
   - Identify ⚠️ **TYPE MISMATCHES** (field name inconsistencies, type differences)

4. **Analyze Genkit flow integration:**
   - Read `backend/app/genkit_flows/*.py`
   - Map backend endpoints to Genkit flows
   - Track complete data flow: Component → Service → Endpoint → Flow

5. **[OPTIONAL] Trace database operations:**
   - Read `backend/app/core/firestore_cache.py` and Firestore collection usage
   - Map backend endpoints to Firestore collections they read/write
   - Document data persistence flow: Endpoint → Collection → Cache strategy
   - Identify missing database operations (endpoints without data persistence)
   - Only included when `--include-database` flag is used

6. **[OPTIONAL] Map design token usage:**
   - Read `frontend/src/theme/tokens.json` and CSS token definitions
   - Scan components in `frontend/src/components/**/*.tsx`
   - Identify which components use design tokens vs hardcoded values
   - Document token application flow: Token → CSS Variable → Component
   - Flag components not using the M3 token system
   - Only included when `--include-design-tokens` flag is used

7. **Generate mapping report:**
   - Create `docs/INTEGRATION_MAP.md` with:
     - Complete integration matrix
     - Missing endpoint list with priority
     - Unused endpoint list for cleanup
     - Type mismatch warnings
     - Integration health score
     - Recommendations for fixes
     - [OPTIONAL] Database persistence flow (with `--include-database`)
     - [OPTIONAL] Design token coverage report (with `--include-design-tokens`)

8. **Generate visual diagrams:**
   - Create Mermaid diagram showing:
     - Frontend components → API services
     - API services → Backend endpoints
     - Backend endpoints → Genkit flows
     - Missing connections highlighted
     - [OPTIONAL] Add Firestore collection connections (with `--include-database`)
     - [OPTIONAL] Add design token flow (with `--include-design-tokens`)

9. **Report findings:**
   - Display summary statistics
   - Show critical issues (missing required endpoints)
   - List improvement opportunities
   - Provide action items

## Analysis Output Structure

### Integration Map Report

```markdown
# Frontend-Backend Integration Map

Generated: 2025-01-06T12:00:00Z

## Summary Statistics

- Total Frontend API Functions: 45
- Total Backend Endpoints: 38
- Mapped Integrations: 35 (✅ 77.8%)
- Missing Backend Endpoints: 10 (❌ 22.2%)
- Unused Backend Endpoints: 3 (⚠️ 6.7%)
- Type Mismatches: 5 (⚠️ 11.1%)

## Integration Health Score: 78/100

### ✅ MAPPED INTEGRATIONS (35)

| Frontend Function        | HTTP Method | Backend Endpoint             | Genkit Flow           |
| ------------------------ | ----------- | ---------------------------- | --------------------- |
| `generateKscResponses()` | POST        | `/api/v1/ksc/generate`       | `generateKscResponse` |
| `getAtsScore()`          | POST        | `/api/v1/analysis/ats-score` | `atsScoring`          |
| ...                      |

### ❌ MISSING BACKEND ENDPOINTS (10)

| Frontend Function    | Expected Endpoint            | Priority | Impact         |
| -------------------- | ---------------------------- | -------- | -------------- |
| `sendWelcomeEmail()` | POST `/api/v1/email/welcome` | HIGH     | Broken feature |
| `getUserAnalytics()` | GET `/api/v1/analytics/user` | MEDIUM   | Missing data   |
| ...                  |

### ❌ UNUSED BACKEND ENDPOINTS (3)

| Endpoint                           | Last Used | Recommendation       |
| ---------------------------------- | --------- | -------------------- |
| GET `/api/v1/admin/legacy-reports` | Never     | Consider deprecating |
| ...                                |

### ⚠️ TYPE MISMATCHES (5)

| Integration                     | Issue                                                                              | Fix                |
| ------------------------------- | ---------------------------------------------------------------------------------- | ------------------ |
| `analysisService.getAtsScore()` | Frontend uses `resumeText` (camelCase), backend expects `resume_text` (snake_case) | Standardize casing |
| ...                             |
```

### Visual Diagram

The skill generates a Mermaid flowchart:

```mermaid
graph LR
    A[KscGeneratorPage] -->|calls| B[aiServices.generateKscResponses]
    B -->|POST /api/v1/ksc/generate| C[ksc/generate endpoint]
    C -->|invokes| D[generateKscResponse flow]
    D -->|caches via| E[Firestore Cache]

    F[AnalysisPage] -->|calls| G[analysisService.getAtsScore]
    G -.->|MISSING| H[/api/v1/analysis/ats-score]

    style H fill:#ff6b6b,stroke:#ff0000
```

## Template Variables

- `{{FRONTEND_SERVICES}}`: List of frontend API service files
- `{{BACKEND_ENDPOINTS}}`: List of backend endpoint files
- `{{MAPPED_COUNT}}`: Number of mapped integrations
- `{{MISSING_COUNT}}`: Number of missing backend endpoints
- `{{UNUSED_COUNT}}`: Number of unused backend endpoints
- `{{MISMATCH_COUNT}}`: Number of type mismatches
- `{{HEALTH_SCORE}}`: Overall integration health percentage
- `{{DIAGRAM}}`: Mermaid diagram code

## Usage Tips

- Run this skill after significant frontend or backend changes
- Use before major releases to catch integration issues
- Generate integration map for new team members
- Track integration health over time
- Prioritize missing endpoints by usage frequency
- Use `--include-database` to trace complete data flows to Firestore
- Use `--include-design-tokens` to audit component token compliance
- Use both flags for comprehensive fullstack documentation
