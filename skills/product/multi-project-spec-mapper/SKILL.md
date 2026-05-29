---
name: multi-project-spec-mapper
description: Intelligent multi-project specification splitting and organization. Analyzes user stories to map them to correct projects (FE, BE, MOBILE, INFRA) based on content, tech stack, and component architecture. Creates project-specific folder structure and splits monolithic specs. Activates for multi-project JIRA/GitHub setups, brownfield projects with multiple teams, microservices architecture. Keywords: multi-project, project mapping, spec splitting, JIRA projects, multiple projects, microservices, FE/BE/MOBILE split, intelligent classification.
---

# Multi-Project Spec Mapper - Intelligent Project Organization

**Purpose**: Automatically detect multiple projects in SpecWeave setup, analyze user stories to map them to the correct project (FE, BE, MOBILE, INFRA), and organize specs into project-specific folders with proper JIRA/GitHub sync.

**When to Use**:
- User has multiple JIRA projects configured (e.g., FE, BE, MOBILE)
- User has multiple GitHub repos to sync
- Brownfield projects with multiple teams/services
- Microservices architecture with separate frontend/backend/mobile codebases
- Need to split monolithic spec into project-specific specs

**Key Capabilities**:
1. ✅ **Intelligent Project Detection** - Analyze config.json to detect multi-project setup
2. ✅ **User Story Classification** - Map user stories to projects based on keywords, tech stack, components
3. ✅ **Spec Splitting** - Split monolithic specs into project-specific files
4. ✅ **Folder Organization** - Create `specs/FE/`, `specs/BE/`, `specs/MOBILE/` structure
5. ✅ **JIRA Item Type Mapping** - Suggest Epic/Story/Task hierarchy based on scope
6. ✅ **Bidirectional Sync** - Configure hooks for GitHub/JIRA sync per project

---

## How It Works

### Step 1: Detect Multi-Project Setup

**Check config.json** for:
```json
{
  "sync": {
    "profiles": {
      "jira-default": {
        "provider": "jira",
        "config": {
          "domain": "company.atlassian.net",
          "projects": ["FE", "BE", "MOBILE"]  // ← Multiple projects!
        }
      }
    }
  }
}
```

**If multiple projects found** → Activate multi-project mode

---

### Step 2: Analyze User Stories

For each user story, analyze:
- **Keywords**: "UI", "chart", "API", "mobile", "database", "deployment"
- **Tech Stack**: "React", "Node.js", "React Native", "PostgreSQL", "Kubernetes"
- **Components**: "component", "service", "screen", "controller", "pipeline"

**Example**:
```
US-001: Log a Workout (Web UI)
→ Keywords: "UI", "web", "chart"
→ Tech: "React"
→ Project: FE (90% confidence)

US-002: View Workout History (API)
→ Keywords: "API", "endpoint", "database"
→ Tech: "Node.js", "PostgreSQL"
→ Project: BE (95% confidence)

US-005: Cross-Platform Data Sync (Mobile)
→ Keywords: "mobile", "offline", "sync"
→ Tech: "React Native"
→ Project: MOBILE (100% confidence)
```

---

### Step 3: Create Project-Specific Specs

**Folder Structure**:
```
.specweave/docs/internal/specs/
├── FE/
│   ├── spec-0001-fitness-tracker-web.md
│   └── README.md
├── BE/
│   ├── spec-0001-fitness-tracker-api.md
│   └── README.md
├── MOBILE/
│   ├── spec-0001-fitness-tracker-mobile.md
│   └── README.md
└── SHARED/
    ├── spec-0001-fitness-tracker-shared.md  (cross-cutting concerns)
    └── README.md
```

**spec.md YAML Frontmatter (v0.31.0+ MANDATORY)**:

```yaml
# For 1-level structure (projects only)
---
increment: 0001-fitness-tracker-web
project: FE                      # REQUIRED
title: "Fitness Tracker Web UI"
status: planned
---

# For 2-level structure (projects + boards)
---
increment: 0001-fitness-tracker-web
project: acme-corp               # REQUIRED
board: digital-operations        # REQUIRED for 2-level
title: "Fitness Tracker Web UI"
status: planned
---
```

**Detection**: Use `detectStructureLevel()` from `src/utils/structure-level-detector.ts`

**Each spec contains**:
- YAML frontmatter with `project:` (and `board:` for 2-level) fields - MANDATORY
- User stories mapped to that project
- Project-specific acceptance criteria
- Links to shared infrastructure/requirements

---

### Step 4: JIRA Sync with Project Mapping

**Hierarchical JIRA Structure**:
```
JIRA Project: FE
├── Epic: Fitness Tracker Web UI (SPEC-0001)
│   ├── Story: US-001: Log a Workout
│   │   ├── Task: T-001: Create Workout Form Component
│   │   ├── Task: T-002: Implement Exercise Search
│   │   └── Task: T-003: Add Set Logging UI
│   └── Story: US-004: Track Progress with Charts
│       ├── Task: T-010: Integrate Recharts Library
│       └── Task: T-011: Create Chart Components

JIRA Project: BE
├── Epic: Fitness Tracker API Backend (SPEC-0001)
│   ├── Story: US-002: View Workout History (API)
│   │   ├── Task: T-004: Create GET /api/workouts Endpoint
│   │   ├── Task: T-005: Implement Filtering Logic
│   │   └── Task: T-006: Add Pagination
│   └── Story: US-003: Manage Exercise Library (API)
│       ├── Task: T-007: Create Exercise CRUD Endpoints
│       └── Task: T-008: Implement Search

JIRA Project: MOBILE
├── Epic: Fitness Tracker Mobile App (SPEC-0001)
    └── Story: US-005: Cross-Platform Data Sync
        ├── Task: T-012: Implement Offline Mode (AsyncStorage)
        ├── Task: T-013: Create Sync Queue
        └── Task: T-014: Handle Conflict Resolution
```

---

### Step 5: Configure Bidirectional Sync

**GitHub Hooks** (`.specweave/config.json`):
```json
{
  "hooks": {
    "post_task_completion": {
      "sync_living_docs": true,
      "external_tracker_sync": true
    }
  },
  "sync": {
    "enabled": true,
    "activeProfile": "jira-default",
    "settings": {
      "autoCreateIssue": true,
      "syncDirection": "bidirectional",
      "projectMapping": {
        "FE": {
          "jiraProject": "FE",
          "jiraBoards": [123],
          "githubRepo": "company/frontend-web"
        },
        "BE": {
          "jiraProject": "BE",
          "jiraBoards": [456],
          "githubRepo": "company/backend-api"
        },
        "MOBILE": {
          "jiraProject": "MOBILE",
          "jiraBoards": [789],
          "githubRepo": "company/mobile-app"
        }
      }
    }
  }
}
```

---

## Project Mapping Rules

### Frontend (FE)

**Keywords**:
- UI/UX: button, form, input, page, view, screen, modal, dropdown
- Visualization: chart, graph, dashboard, widget
- Styling: CSS, theme, dark mode, responsive
- State: Redux, Zustand, context, state management

**Tech Stack**:
- React, Vue, Angular, Next.js, Svelte
- TypeScript, JavaScript
- Tailwind, Material-UI, Chakra, Ant Design
- Recharts, D3, Chart.js

**Components**:
- Component, hook, context, provider, page, layout

**Confidence**: 30%+ for primary match

---

### Backend (BE)

**Keywords**:
- API: endpoint, REST, GraphQL, route
- Database: query, migration, schema, model
- Auth: authentication, JWT, session, token
- Processing: queue, job, worker, cron, batch

**Tech Stack**:
- Node.js (Express, Fastify, NestJS)
- Python (FastAPI, Django, Flask)
- Java (Spring Boot), .NET (ASP.NET)
- PostgreSQL, MySQL, MongoDB, Redis

**Components**:
- Controller, service, repository, middleware, handler

**Confidence**: 30%+ for primary match

---

### Mobile (MOBILE)

**Keywords**:
- Mobile: native, iOS, Android, cross-platform
- Device: camera, GPS, push notification, offline
- Navigation: tab bar, drawer, stack, screen transition
- Storage: AsyncStorage, local database

**Tech Stack**:
- React Native, Expo, Flutter
- Swift, Kotlin
- React Navigation

**Components**:
- Screen, navigator, bottom-sheet, drawer

**Exclude**: "web" keyword (penalty)

**Confidence**: 30%+ for primary match

---

### Infrastructure (INFRA)

**Keywords**:
- DevOps: deployment, CI/CD, Docker, Kubernetes
- Monitoring: logging, metrics, alerting, SLO
- Security: SSL, TLS, firewall, VPC
- Scalability: load balancing, CDN, backup

**Tech Stack**:
- AWS, Azure, GCP
- Kubernetes, Docker, Terraform
- Jenkins, GitHub Actions, GitLab CI
- Prometheus, Grafana, Datadog

**Components**:
- Pipeline, manifest, Helm chart, Terraform module

**Confidence**: 30%+ for primary match

---

## JIRA Item Type Hierarchy

**Epic** (> 13 story points):
- Large feature area spanning multiple stories
- Example: "Fitness Tracker MVP" (29 story points total)

**Story** (3-13 story points):
- Standard user story with clear value
- Example: "US-001: Log a Workout" (8 story points)

**Task** (1-2 story points):
- Small implementation task
- Example: "T-001: Create Workout Form Component" (2 story points)

**Subtask** (< 1 story point):
- Granular work item
- Example: "Create POST /api/workouts endpoint" (0.5 story points)

---

## Usage Examples

### Example 1: Fitness Tracker (Multi-Project)

**Input**: Monolithic spec with 35 user stories

**Detection**:
```
✓ Multi-project setup detected:
  - FE (Frontend Web)
  - BE (Backend API)
  - MOBILE (React Native)
```

**Classification**:
```
Analyzing 35 user stories...
✓ US-001: Log a Workout → FE (90% confidence: React, UI, chart)
✓ US-002: View Workout History → BE (95% confidence: API, database, query)
✓ US-004: Track Progress with Charts → FE (100% confidence: Recharts, visualization)
✓ US-005: Cross-Platform Data Sync → MOBILE (100% confidence: React Native, offline)

Project Distribution:
- FE: 12 user stories (34%)
- BE: 15 user stories (43%)
- MOBILE: 6 user stories (17%)
- SHARED: 2 user stories (6%)
```

**Output**:
```
Creating project-specific specs...
✓ specs/FE/spec-0001-fitness-tracker-web.md (12 user stories)
✓ specs/BE/spec-0001-fitness-tracker-api.md (15 user stories)
✓ specs/MOBILE/spec-0001-fitness-tracker-mobile.md (6 user stories)
✓ specs/SHARED/spec-0001-fitness-tracker-shared.md (2 user stories)

JIRA Sync Configuration:
✓ FE → JIRA Project FE (Board 123)
✓ BE → JIRA Project BE (Board 456)
✓ MOBILE → JIRA Project MOBILE (Board 789)
```

---

### Example 2: Microservices E-Commerce

**Input**: Spec for multi-service platform

**Detection**:
```
✓ Multi-project setup detected:
  - FRONTEND (Web storefront)
  - PRODUCT-SVC (Product service)
  - ORDER-SVC (Order service)
  - PAYMENT-SVC (Payment service)
  - INFRA (Kubernetes + monitoring)
```

**Classification**:
```
Analyzing 50 user stories...
✓ US-010: Product Catalog UI → FRONTEND (95%)
✓ US-011: Product Search API → PRODUCT-SVC (100%)
✓ US-020: Shopping Cart → ORDER-SVC (90%)
✓ US-030: Stripe Integration → PAYMENT-SVC (100%)
✓ US-040: Kubernetes Deployment → INFRA (100%)

Project Distribution:
- FRONTEND: 15 user stories
- PRODUCT-SVC: 12 user stories
- ORDER-SVC: 10 user stories
- PAYMENT-SVC: 8 user stories
- INFRA: 5 user stories
```

---

## Configuration

**Enable Multi-Project Mode** in `.specweave/config.json`:
```json
{
  "multiProject": {
    "enabled": true,
    "autoDetect": true,
    "customRules": {
      "FE": {
        "keywords": ["react", "ui", "chart"],
        "techStack": ["react", "typescript", "recharts"],
        "confidenceThreshold": 0.3
      }
    }
  }
}
```

---

## Related Skills

- **spec-generator**: Creates comprehensive specs (uses this skill for multi-project splitting)
- **increment-planner**: Plans increments (uses this skill to assign work to projects)
- **jira-sync**: Syncs to JIRA (uses project mappings from this skill)
- **github-sync**: Syncs to GitHub (uses project mappings from this skill)

---

## Version History

- **v1.0.0** (0.14.0): Initial release with intelligent project mapping
- Based on: Increment 0020-multi-project-intelligent-sync
