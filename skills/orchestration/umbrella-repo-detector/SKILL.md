---
name: umbrella-repo-detector
description: Detects multi-repo architecture patterns (frontend/backend/shared) from user prompts and guides umbrella setup. Use when working with multiple repositories, microservices architecture, or projects with separate FE/BE/Shared libraries. Helps configure SpecWeave for multi-repo coordination.
---

# Umbrella Multi-Repo Architecture Detector

## When This Skill Activates

Activates when user describes:
- Multiple repos: "3 repos", "frontend repo", "backend repo", "shared library"
- Architecture patterns: "monorepo with services", "microservices", "multi-repo"
- Explicit splits: "FE/BE/Shared", "frontend/backend/common"
- GitHub URLs for multiple repositories

## My Role

When I detect a multi-repo architecture in the user's prompt:

1. **Acknowledge the architecture** with detected repos
2. **Explain project-scoped user stories** (US-FE-*, US-BE-*, US-SHARED-*)
3. **Guide the init flow** for proper setup
4. **Route to PM agent** with multi-repo context

## Detection Patterns

| Pattern | Example | Detected As |
|---------|---------|-------------|
| Repo count | "3 repos", "multiple repos" | Multi-repo intent |
| Frontend repo | "Frontend repo", "UI repo", "web app" | Type: frontend, Prefix: FE |
| Backend repo | "Backend API repo", "server", "API" | Type: backend, Prefix: BE |
| Shared repo | "Shared library", "common types" | Type: shared, Prefix: SHARED |
| Mobile repo | "Mobile app", "iOS/Android" | Type: mobile, Prefix: MOBILE |
| Infra repo | "Infrastructure", "Terraform" | Type: infrastructure, Prefix: INFRA |

## Project-Scoped User Stories

When user describes multi-repo, user stories MUST be prefixed:

```markdown
## Instead of (generic):
US-001: User Registration
US-002: Registration API
US-003: Validation Schema

## Generate (project-scoped):
US-FE-001: User Registration Form
  - Related repo: frontend
  - Keywords: form, UI, validation display

US-BE-001: Registration API Endpoint
  - Related repo: backend
  - Keywords: API, endpoint, database

US-SHARED-001: Registration Validation Schema
  - Related repo: shared
  - Keywords: validator, schema, types
```

## Cross-Cutting User Stories

For features that span multiple repos, use cross-project tagging:

```markdown
US-AUTH-001: OAuth Integration
  - Tags: ["cross-project", "frontend", "backend"]
  - Creates linked issues in: FE repo, BE repo
  - Child stories:
    - US-FE-002: OAuth Login Button (frontend)
    - US-BE-002: OAuth Token Validation (backend)
```

## Setup Flow Guidance

When multi-repo detected, guide user through options:

### Option 1: Clone from GitHub (Recommended)
```
You have existing repos? Let's clone them:
1. Provide GitHub URLs (comma-separated or one per line)
2. Each repo gets its own .specweave/ configuration
3. Each repo syncs to its own GitHub issues
```

### Option 2: Create New Repos
```
Creating fresh repos:
1. I'll create repos on GitHub for you
2. Each gets initialized with .specweave/
3. External tool sync configured per repo
```

### Option 3: Initialize Local Folders
```
Have local folders already?
1. Point me to each folder
2. I'll initialize .specweave/ in each
3. Configure external tools per repo
```

## Umbrella Repo Structure

```
umbrella-project/                 # Optional parent repo
├── .specweave/
│   ├── config.json              # umbrella config with childRepos[]
│   └── docs/                    # High-level PRD, roadmap only
│
├── my-app-fe/                   # Frontend repo (cloned/created)
│   └── .specweave/
│       ├── config.json          # sync → my-app-fe GitHub issues
│       └── increments/
│           └── 0001-feature/
│               └── spec.md      # Only US-FE-* stories
│
├── my-app-be/                   # Backend repo (cloned/created)
│   └── .specweave/
│       └── ...                  # sync → my-app-be GitHub issues
│
└── my-app-shared/               # Shared repo (cloned/created)
    └── .specweave/
        └── ...                  # sync → my-app-shared GitHub issues
```

## Project ID Strategy

**CRITICAL**: The `id` field MUST match your canonical source name - no arbitrary abbreviations!

| Scenario | ID Source | Example |
|----------|-----------|---------|
| **1:1 Repo Mapping** | Exact repo name | `sw-qr-menu-fe` |
| **JIRA Project** | Project key (lowercase) | `WEBAPP` → `webapp` |
| **ADO Project** | Project name (kebab-case) | `Frontend Team` → `frontend-team` |
| **Area Path** | Last segment (kebab-case) | `Product\Web` → `web` |

```
✅ CORRECT: id matches repo name
   id: "sw-qr-menu-fe"
   path: "./sw-qr-menu-fe"
   githubUrl: "https://github.com/user/sw-qr-menu-fe"

❌ WRONG: arbitrary abbreviation
   id: "fe"              ← What if you have 2 frontend repos?
   path: "./sw-qr-menu-fe"
```

**Note**: The `prefix` (for user stories like `US-FE-001`) can be short even if `id` is long:
- `id: "sw-qr-menu-fe"` (full repo name)
- `prefix: "FE"` (short, for user story IDs)

## Config Example

**Parent umbrella config** (`.specweave/config.json`):
```json
{
  "umbrella": {
    "enabled": true,
    "childRepos": [
      {
        "id": "sw-qr-menu-fe",
        "path": "./sw-qr-menu-fe",
        "prefix": "FE",
        "githubUrl": "https://github.com/myorg/sw-qr-menu-fe"
      },
      {
        "id": "sw-qr-menu-be",
        "path": "./sw-qr-menu-be",
        "prefix": "BE",
        "githubUrl": "https://github.com/myorg/sw-qr-menu-be"
      },
      {
        "id": "sw-qr-menu-shared",
        "path": "./sw-qr-menu-shared",
        "prefix": "SHARED",
        "githubUrl": "https://github.com/myorg/sw-qr-menu-shared"
      }
    ]
  }
}
```

**JIRA-based project** (when JIRA is source of truth):
```json
{
  "umbrella": {
    "enabled": true,
    "childRepos": [
      {
        "id": "webapp",
        "path": "./frontend",
        "prefix": "WEBAPP",
        "jiraProject": "WEBAPP",
        "githubUrl": "https://github.com/myorg/frontend"
      }
    ]
  }
}
```

**Child repo config** (`sw-qr-menu-fe/.specweave/config.json`):
```json
{
  "project": {
    "name": "QR Menu Frontend",
    "prefix": "FE"
  },
  "sync": {
    "activeProfile": "github",
    "profiles": {
      "github": {
        "provider": "github",
        "config": {
          "owner": "myorg",
          "repo": "sw-qr-menu-fe"
        }
      }
    }
  }
}
```

## Response Template

When I detect multi-repo intent, respond:

```
I detected a **multi-repo architecture** in your description:

**Detected Repos:**
- Frontend (prefix: FE) - [matched keywords]
- Backend (prefix: BE) - [matched keywords]
- Shared (prefix: SHARED) - [matched keywords]

**User Story Format:**
User stories will be project-scoped:
- `US-FE-001`: Frontend stories
- `US-BE-001`: Backend stories
- `US-SHARED-001`: Shared library stories

**Setup Options:**
1. **Clone from GitHub** - Provide URLs, I'll clone and initialize each
2. **Create new repos** - I'll create on GitHub and initialize
3. **Initialize local folders** - Point to existing folders

Which would you like to do?
```

## Keywords for Story Routing

| Keywords | Routes To | Prefix |
|----------|-----------|--------|
| UI, component, page, form, view, theme, drag-drop, builder | Frontend | FE |
| API, endpoint, CRUD, webhook, notification, analytics | Backend | BE |
| schema, validator, types, utilities, localization | Shared | SHARED |
| iOS, Android, mobile, push notification | Mobile | MOBILE |
| Terraform, K8s, Docker, CI/CD | Infrastructure | INFRA |

## Saving Changes Across Repos

Use `/sw:save` to commit and push changes across all repos at once:

```bash
# Save all repos with same commit message
/sw:save "feat: Add user authentication"

# Preview what would happen
/sw:save --dry-run

# Save specific repos only
/sw:save "fix: Bug fixes" --repos frontend,backend
```

**Features:**
- **Auto-discovers nested repos** - Scans `repositories/`, `packages/`, `services/`, `apps/`, `libs/` for `.git` directories (up to 4 levels deep)
- Auto-detects repos with changes
- Sets up remotes if missing (prompts for URL or uses umbrella config)
- Commits with same message to all repos
- Pushes to origin
- Skips repos with no changes

**Auto-Discovery (No Config Required):**
Even without umbrella config, `/sw:save` automatically finds all nested repos:
```
my-project/
├── repositories/
│   ├── frontend/.git    # ← Auto-discovered
│   ├── backend/.git     # ← Auto-discovered
│   └── shared/.git      # ← Auto-discovered
└── .git                 # ← Parent repo included
```
All 4 repos will be committed and pushed with a single `/sw:save` command!

## Important Notes

1. **Each repo is independent** - Own `.specweave/`, own increments, own external tool sync
2. **Parent repo is optional** - Can have umbrella config or just independent repos
3. **User stories MUST have project prefix** - Never generate generic `US-001` in multi-repo mode
4. **Cross-project stories get special handling** - Tagged and linked across repos
5. **Use `/sw:save`** - Single command to save changes across all repos
