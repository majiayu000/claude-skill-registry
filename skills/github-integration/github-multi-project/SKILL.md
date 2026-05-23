---
name: github-multi-project
description: Expert at organizing specs and splitting tasks across multiple GitHub repositories for monorepo, polyrepo, and parent repo architectures. Use when managing specs across multiple repos, coordinating cross-repo work, or allocating tasks to different teams/repositories.
---

# GitHub Multi-Project Management Skill

Expert skill for managing SpecWeave projects across multiple GitHub repositories.

## Core Capabilities

### 1. Spec Organization
- Organizes specs in `.specweave/docs/internal/projects/{project-id}/` structure
- Maps increments to specific projects/repos
- Maintains traceability across repositories
- Handles cross-project dependencies

### 2. Task Splitting
When a SpecWeave increment spans multiple repositories:
- Analyzes tasks in `tasks.md`
- Identifies which tasks belong to which repo
- Creates repo-specific task lists
- Maintains cross-repo coordination

### 3. Repository Architectures

#### Single Repository
```
my-app/
├── .specweave/
│   └── docs/internal/projects/default/
└── src/
```

#### Multi-Repository (Polyrepo)
```
my-app-frontend/
├── .git
└── src/

my-app-backend/
├── .git
└── src/

my-app-shared/
├── .git
└── src/
```

#### Parent Repository Approach (Recommended for Multi-Repo)
```
my-app-parent/              # Parent repo with .specweave
├── .specweave/
│   └── docs/internal/projects/
│       ├── frontend/
│       ├── backend/
│       └── shared/
└── services/               # Implementation repos
    ├── frontend/
    ├── backend/
    └── shared/
```

#### Monorepo
```
my-app/
├── .specweave/
│   └── docs/internal/projects/
│       ├── frontend/
│       ├── backend/
│       └── shared/
└── packages/
    ├── frontend/
    ├── backend/
    └── shared/
```

## Task Splitting Examples

### Example 1: E-commerce Platform
**Increment**: Add shopping cart functionality

**Tasks split by repository**:

**Frontend (my-app-frontend)**:
- T-001: Create CartItem component
- T-002: Implement cart state management
- T-003: Add cart UI with add/remove buttons

**Backend (my-app-backend)**:
- T-004: Create cart database schema
- T-005: Implement cart API endpoints
- T-006: Add cart validation logic

**Shared (my-app-shared)**:
- T-007: Define cart TypeScript types
- T-008: Create cart utility functions

### Example 2: Microservices Architecture
**Increment**: Implement user notifications

**Tasks split by service**:

**User Service**:
- T-001: Add notification preferences to user profile
- T-002: Create preference API endpoints

**Notification Service**:
- T-003: Implement notification queue
- T-004: Create email sender
- T-005: Create push notification sender

**Gateway Service**:
- T-006: Add notification routes
- T-007: Implement rate limiting

## Commands

### Analyze Task Distribution
```typescript
// Analyze which tasks belong to which repository
function analyzeTaskDistribution(tasks: Task[]): Map<string, Task[]> {
  const distribution = new Map();

  for (const task of tasks) {
    const repo = detectRepository(task);
    if (!distribution.has(repo)) {
      distribution.set(repo, []);
    }
    distribution.get(repo).push(task);
  }

  return distribution;
}
```

### Create Repository-Specific Issues
```typescript
// Create GitHub issues in each repository
async function createRepoSpecificIssues(
  increment: Increment,
  distribution: Map<string, Task[]>
) {
  for (const [repo, tasks] of distribution) {
    const issue = await createGitHubIssue({
      repo,
      title: `[${increment.id}] ${increment.name} - ${repo}`,
      body: formatTasksAsChecklist(tasks),
      labels: ['specweave', 'increment', repo]
    });

    console.log(`Created issue #${issue.number} in ${repo}`);
  }
}
```

## Best Practices

### 1. Parent Repository Approach
**Recommended for multi-repo projects**:
- Central .specweave/ folder in parent repo
- Living docs sync to parent (single source of truth)
- Implementation repos stay clean
- Better for enterprise/multi-team projects

### 2. Task Naming Convention
```
T-{repo}-{number}: {description}
T-FE-001: Create user profile component
T-BE-001: Implement user API
T-SHARED-001: Define user types
```

### 3. Cross-Repository Dependencies
Mark dependencies clearly:
```
T-FE-002: Consume user API
  Dependencies: T-BE-001 (must complete first)
```

### 4. Spec Organization
```
.specweave/docs/internal/projects/
├── frontend/
│   └── specs/
│       ├── spec-001-user-interface.md
│       └── spec-002-cart-ui.md
├── backend/
│   └── specs/
│       ├── spec-001-api-design.md
│       └── spec-002-database.md
└── shared/
    └── specs/
        └── spec-001-types.md
```

## Integration with GitHub Projects

### Multi-Repo GitHub Project
Create a GitHub Project that spans multiple repositories:
1. Create project at organization level
2. Add issues from all repos
3. Use project boards for cross-repo coordination
4. Track overall increment progress

### Repository-Specific Projects
Each repository can have its own project:
- Frontend Project: UI tasks
- Backend Project: API tasks
- Shared Project: Common tasks

## Automation

### GitHub Actions Integration
```yaml
# .github/workflows/specweave-sync.yml
name: SpecWeave Multi-Repo Sync

on:
  workflow_dispatch:
  schedule:
    - cron: '0 */6 * * *' # Every 6 hours

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Sync to repositories
        run: |
          # Sync tasks to frontend repo
          gh issue create --repo myorg/frontend ...

          # Sync tasks to backend repo
          gh issue create --repo myorg/backend ...
```

## Error Handling

### Common Issues
1. **Repository not found**: Ensure repos exist and token has access
2. **Task ambiguity**: Use clear naming to indicate target repo
3. **Cross-repo conflicts**: Use parent repo as single source of truth
4. **Permission errors**: Token needs repo scope for all repositories

## Related Skills
- github-sync: Basic GitHub synchronization
- github-issue-tracker: Task-level tracking
- specweave:multi-project-spec-mapper: Intelligent spec splitting