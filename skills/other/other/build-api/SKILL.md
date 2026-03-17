---
name: build-api
description: Build backend API endpoints, services, and database changes. Use for backend-only work like new API routes, business logic, database schema changes, or microservice patterns. Activates the Architecture Council for significant API decisions.
user-invokable: true
---

# Backend API Development Workflow

Build backend API endpoints, services, and database changes following NestJS patterns, Prisma schema design, and the project's clean architecture conventions.

> [!CAUTION]
> **Scope boundary**: This skill implements backend code and commits it. It does **NOT** create pull requests, push to remote, run code reviews, or submit anything for merge. When implementation and commits are complete, **stop** and suggest the user run `/review-code` next.

## Step 1: Define API Requirements

Ensure we are on a feature branch based on the latest `main`. Always fetch first:

```bash
git fetch origin main
```

If on `main`, create a new feature branch from the latest `origin/main`:

```bash
git checkout -b feature/<feature-slug> origin/main
```

If already on an existing feature branch, rebase it onto the latest `origin/main` to pick up any changes:

```bash
git status --porcelain
```

If the working tree is dirty, stash changes before rebasing:

```bash
git stash push -m "build-api: stash before rebase"
git rebase origin/main
git stash pop
```

If the working tree is clean, rebase directly:

```bash
git rebase origin/main
```

If the user provides a GitHub issue number (e.g., `/build-api 42` or `/build-api #42`), fetch the issue and signal work is in progress (see AGENTS.md "Label Management" for rules):

```bash
gh issue view <number> --json title,body,labels,state,number

# Single-developer constraint: only one issue should be in-progress at a time.
# First, remove in-progress from any other issue that has it:
gh issue list --label "in-progress" --state open --json number --jq '.[].number' | while read n; do
  gh issue edit "$n" --remove-label "in-progress"
done

gh issue edit <number> --add-label "in-progress"
```

Verify the issue is tracked on the [Product Roadmap]({PROJECT_BOARD_URL}) project board. If not, add it:

```bash
# --limit 200 covers the current board size; increase if the project grows beyond 200 items
EXISTING=$(gh project item-list {PROJECT_NUMBER} --owner {OWNER} --format json --limit 200 \
  | python3 -c "
import json, sys
data = json.load(sys.stdin)
for item in data.get('items', []):
    # <number> must be an integer literal, e.g., == 42, not == '42'
    if item.get('content', {}).get('number') == <number>:
        print(item['id'])
        break
")

if [ -z "$EXISTING" ]; then
  ITEM_ID=$(gh project item-add {PROJECT_NUMBER} --owner {OWNER} --url "https://github.com/{OWNER}/{REPO}/issues/<number>" --format json | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")
  echo "Warning: Issue #<number> was not on the project board. Added it now (item $ITEM_ID)."
fi
```

> [!WARNING]
> If the issue was missing from the project board, it may also be missing phase, size, and date fields. Check the project item and warn the user if fields are unset — this suggests the issue was created outside of `/plan-feature` or `/security-audit`, which are the skills that ensure board membership and field population.

Ask the user (or read from the decision record / issue body if `/plan-feature` was run first):

- What resource(s) or endpoint(s) are being created or modified?
- What operations are needed (CRUD, custom actions, queries)?
- Are there database schema changes?
- Is this a tRPC procedure or REST endpoint?
- Are there authentication or authorization requirements?

If a decision record exists in `docs/decisions/`, read it for the task breakdown.

## Step 2: Design API Contract

Invoke `/backend-development:api-design-principles` for API design guidance.

Design the full API contract:

- **Endpoint paths and HTTP methods** (REST) or **procedure names** (tRPC)
- **Request types**: Full TypeScript interfaces with all fields, optional/required markers
- **Response types**: Success responses, error responses, pagination if applicable
- **Validation rules**: Using Zod schemas for runtime validation
- **Error format**: Standardized error response structure
- **Auth requirements**: Which endpoints need authentication, role-based access

If this represents a **significant API decision** (new resource type, breaking change to existing API, new architectural pattern), activate the Architecture Council using `.claude/councils/architecture-council.md`:

> **Model Selection**: See the [Model Selection](../../README.md#model-selection) section in README.md for mapping agent model specs to Task tool parameters.

### Principal Engineer — consult: full-stack-orchestration

- **Vote**: Approve / Concern / Block
- **Rationale**: Architectural soundness, scalability, maintainability
- **Recommendations**: Patterns to follow, trade-offs to consider

### Platform Engineer — consult: cloud-infrastructure

- **Vote**: Approve / Concern / Block
- **Rationale**: Operational implications, deployment considerations
- **Recommendations**: Infrastructure concerns, monitoring needs

### Security Engineer — consult: security-scanning

- **Vote**: Approve / Concern / Block
- **Rationale**: Security risks, attack surface, compliance
- **Recommendations**: Security hardening steps, input validation

### Backend Specialist — consult: backend-development

- **Vote**: Approve / Concern / Block
- **Rationale**: API design quality, NestJS patterns, developer experience
- **Recommendations**: Implementation approach, ecosystem integration

### CHECKPOINT: Present the API contract (and Architecture Council evaluation if activated) to the user. Wait for approval before implementation begins.

## Step 3: Database Layer (if needed)

If schema changes are required:

1. Invoke `/database-design:postgresql` for PostgreSQL schema design guidance

2. Design the Prisma schema changes:
   - Model definitions with proper field types
   - Relations and foreign keys
   - Indexes for query performance
   - Unique constraints and validations
   - Enums where appropriate

3. Invoke `/database-migrations:sql-migrations` for migration generation guidance

### CHECKPOINT: Present the Prisma schema changes and migration plan to the user. Wait for approval before running the migration.

4. Generate and apply the migration:

   ```bash
   pnpm db:migrate
   ```

5. If seed data is needed, update the seed script.

## Step 4: Implement Backend

Follow NestJS patterns and `/backend-development:architecture-patterns` for clean architecture:

### Types and DTOs

- Define request/response TypeScript interfaces
- Create Zod validation schemas for runtime validation
- Export types for frontend consumption (via tRPC or shared packages)

### Repository / Data Access Layer

- Create or update Prisma queries
- Implement data access patterns (repository pattern if used)
- Add query optimization (select specific fields, use includes wisely)

### Service Layer

- Implement business logic in NestJS services
- Add input validation and business rule enforcement
- Handle error cases with typed exceptions
- Keep services testable (inject dependencies)

### Controller / Router Layer

- Create tRPC procedures or NestJS controllers
- Wire up validation, auth guards, and services
- Implement proper HTTP status codes (REST) or error codes (tRPC)
- Add rate limiting if needed for public endpoints

### Guards and Middleware

- Add authentication guards where required
- Add authorization checks (role-based or resource-based)
- Add request logging for debugging

Use `/javascript-typescript:typescript-advanced-types` for complex type scenarios (generics, conditional types, mapped types).

For performance-sensitive endpoints, invoke `/application-performance:performance-optimization` for API profiling and optimization patterns.

## Step 5: Write Tests

Following the QA Lead testing strategy:

### Unit Tests

- Test each service method in isolation
- Mock Prisma client and external dependencies
- Test business logic, validation rules, error handling
- Cover happy paths and edge cases

### Integration Tests

- Test endpoints against a real (test) database
- Verify request validation rejects bad input
- Verify authentication and authorization enforcement
- Test error responses for various failure modes

### Validation Tests

- Boundary conditions (empty strings, max lengths, special characters)
- Invalid input formats
- Missing required fields
- Type coercion and casting

Run tests and verify coverage:

```bash
pnpm test
```

Ensure coverage meets the >80% target.

## Step 6: Generate API Documentation

Invoke `/documentation-generation:openapi-spec-generation` to generate or update API documentation for the new endpoints.

If using tRPC, document the procedure signatures and usage examples.
If using REST, generate or update the OpenAPI/Swagger specification.

## Step 7: Self-Review

Before presenting to the user, verify:

```bash
pnpm type-check      # No TypeScript errors
pnpm lint            # No linting violations
pnpm format:check    # No Prettier formatting issues
pnpm test            # All unit tests pass
pnpm test:smoke      # DI container and HTTP pipeline boot OK
```

If `format:check` fails, run `pnpm exec prettier --write` on the reported files before proceeding.

Check for common issues:

- No hardcoded secrets or credentials
- Proper error handling (no swallowed errors)
- Input validation on all external-facing endpoints
- Proper use of TypeScript strict mode (no `any` types)

## Step 8: Update Documentation

If this API change alters how the project is set up, built, or run, update the relevant documentation **before committing**:

1. **README.md** — Update Quick Start, Running the Application, or Project Structure sections if the change introduces new infrastructure, services, environment variables, or commands
2. **docs/DEVELOPMENT.md** — Update Prerequisites, Local Development Setup, Database Operations, or Troubleshooting sections as needed
3. **Makefile** — Add new targets for common operations (e.g., new Docker services, database commands)
4. **`.env.example` files** — Add new environment variables with clear descriptions and safe defaults
5. **`docs/INDEX.md`** — If any new files were added to `docs/`, add them to the appropriate table in the master documentation index

> [!IMPORTANT]
> A developer cloning the repo fresh must be able to get the project running by following README.md alone. If your API change adds a Docker service, database, new environment variable, or external dependency, the docs MUST reflect it.

## Step 9: Commit

### CHECKPOINT: Present a summary of all changes — files modified, API contract implemented, test results, and documentation. Wait for user approval.

Commit with conventional commit format:

```
feat(api): add <resource> endpoints
```

Or if modifying existing endpoints:

```
feat(api): update <resource> with <change-description>
```

### Update GitHub Issue

If implementation was initiated from a GitHub issue:

1. Comment on it with progress:

   ```bash
   gh issue comment <number> --body "Implementation committed on branch \`<branch-name>\`. Proceeding to code review via \`/review-code\`."
   ```

> [!NOTE]
> Do **not** remove the `in-progress` label here. The label stays on the issue until it is closed (handled automatically by `.github/workflows/label-cleanup.yml`). This ensures the issue remains visibly in-progress through code review and PR submission.

## Step 10: Hand Off — STOP Here

> [!CAUTION]
> **This skill's work is done.** Do NOT proceed to create a pull request, push to remote, or run a code review. Those are separate skills with their own workflows and checkpoints.

Present the next step to the user:

- **Recommended**: Run `/review-code` for multi-perspective security and quality review before submitting
- **If more work remains**: Continue with remaining tasks, then run `/review-code`

If working from a GitHub issue, remind the user:

- The PR should reference the issue with `Closes #<number>` so it auto-closes when merged
- `/submit-pr` will detect related issues from commit messages

**Pipeline**: `/plan-feature` → `/build-feature` or **`/build-api`** → `/review-code` → `/submit-pr`

**Do not push the branch, create a PR, or invoke `/submit-pr` from within this skill.**
