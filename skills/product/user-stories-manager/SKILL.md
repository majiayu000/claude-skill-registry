---
name: "user-stories-manager"
description: "Manage user stories: create, list, update status, link migrations/tests, validate; use when working on features, tracking progress, or creating new stories (project)"
version: "1.0.0"
---

# User Stories Manager

Manage user stories for tracking feature development, linking code artifacts, and monitoring progress.

## Quick Commands

```bash
# List stories
./scripts/story-list.sh                    # All stories summary
./scripts/story-list.sh --status draft     # Filter by status
./scripts/story-list.sh --module invoices  # Filter by module

# Create new story
./scripts/story-create.sh "feature-name" --module admin-events

# Update story
./scripts/story-update.sh US-001 --status in-progress
./scripts/story-update.sh US-001 --priority high

# Link resources
./scripts/story-link.sh US-001 --migration 20251224_add_feature
./scripts/story-link.sh US-001 --test apps/web/__tests__/e2e/path/test.ts

# Validate
./scripts/story-validate.sh

# Statistics
./scripts/story-stats.sh
```

## Directory Structure

```
docs/user-stories/
├── {module}/                    # Module directories (18 total)
│   ├── US-{number}-{slug}.md   # Story files
│   └── _module.yml             # Optional module metadata
├── story-template.md           # Template for new stories
├── index.json                  # Auto-generated index
└── README.md                   # Documentation
```

## Story Format

Stories use markdown with YAML frontmatter:

```markdown
---
id: US-001
title: Dancer Registration
module: authentication
status: in-progress
priority: high
acceptance_criteria:
  - "User can register with email/password"
  - "Profile created in database"
migration_ids:
  - "20251115120000_add_dancer_profiles"
db_tables:
  - profiles
  - auth.users
test_files:
  - "apps/web/__tests__/e2e/auth/01-registration-flow.test.ts"
dependencies: []
created_at: 2025-11-15
updated_at: 2025-12-15
---

# User Story: Dancer Registration

## Context
...

## User Story Statement
**As a** dancer
**I want to** create an account
**So that** I can participate in events

## Acceptance Criteria
1. User can register with email/password
2. Profile created in database

## Technical Implementation
...
```

## Status Lifecycle

```
draft → in-progress → testing → done
```

| Status | Meaning | Requirements |
|--------|---------|--------------|
| **draft** | Being planned | None |
| **in-progress** | Active development | Must have acceptance_criteria |
| **testing** | Code complete, validating | Must have migration_ids, test_files |
| **done** | Fully complete | All linked migrations & tests exist |

## Frontmatter Fields

### Required
- **id**: Story identifier (e.g., "US-001")
- **title**: Human-readable title
- **module**: Module name
- **status**: draft, in-progress, testing, done
- **priority**: low, medium, high, critical
- **acceptance_criteria**: List of criteria

### Optional
- **assigned_to**: Developer email
- **migration_ids**: Linked migration IDs
- **db_tables**: Affected database tables
- **test_files**: Linked test file paths
- **dependencies**: Other story IDs
- **blockers**: Current blockers
- **notes**: Implementation notes
- **created_at**: Creation date
- **updated_at**: Last update date
- **completed_at**: Completion date

## Modules (18)

| Module | Stories | Description |
|--------|---------|-------------|
| authentication | US-001 | Registration, login |
| cast-management | US-002 | Cast workflows |
| communications | US-003 to US-007 | Emails, invitations |
| admin-events | US-008 to US-014 | Event management |
| dancer-experience | US-015 to US-019 | Dancer features |
| admin-productions | US-020 to US-021 | Production management |
| admin-cast-assignment | US-022 to US-029 | Cast assignment |
| admin-reporting | US-030 to US-032 | Reports, exports |
| invoices | US-033 to US-038 | Invoice system |
| hire-orders | US-039 to US-045 | Hire orders |
| clients | US-046 to US-048 | Client management |
| ai-chatbot | US-049 to US-052, US-059 | AI chatbot |
| venues | US-053 to US-054 | Venue management |
| reimbursements | US-055 to US-056 | Reimbursements |
| legal-compliance | US-057 | Legal documents |
| airtable-sync | US-058 | Airtable sync |
| payments | US-060 | Tipalti payments |
| repertoire | US-061+ | Repertoire management |

## Development Workflow

### Starting a Feature

1. Find or create a story:
   ```bash
   ./scripts/story-list.sh --status draft
   # or
   ./scripts/story-create.sh "new-feature" --module admin-events
   ```

2. Update status to in-progress:
   ```bash
   ./scripts/story-update.sh US-070 --status in-progress
   ```

3. As you implement, link resources:
   ```bash
   ./scripts/story-link.sh US-070 --migration 20251224_add_feature
   ./scripts/story-link.sh US-070 --test apps/web/__tests__/e2e/feature/test.ts
   ```

4. Mark complete when done:
   ```bash
   ./scripts/story-update.sh US-070 --status done
   ```

### Finding Stories

```bash
# What needs work?
./scripts/story-list.sh --status draft
./scripts/story-list.sh --status in-progress

# What's in a module?
./scripts/story-list.sh --module invoices

# High priority items
./scripts/story-list.sh --priority critical
./scripts/story-list.sh --priority high
```

## Validation

Stories are validated for:
- Valid frontmatter schema (Zod)
- Migration files exist
- Test files exist
- No duplicate IDs
- Acceptance criteria for non-draft stories
- Dependencies reference existing stories

Run validation:
```bash
./scripts/story-validate.sh
```

## Integration with @ballee/user-stories

The skill wraps the `@ballee/user-stories` package:

```typescript
import {
  getAllStories,
  getStoryById,
  getStoriesByModule,
  getStoriesByStatus,
  validateStoryCompleteness,
} from '@ballee/user-stories';
```

## Related Skills

- `wip-lifecycle-manager` - For multi-step implementation tracking
- `database-migration-manager` - For creating migrations
- `test-patterns` - For writing E2E tests
- `service-patterns` - For service layer implementation
