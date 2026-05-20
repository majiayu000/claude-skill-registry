---
name: build-feature
description: Implement a full-stack feature following an approved plan. Builds database layer, backend API, frontend components, and tests. Use after plan-feature has produced an approved implementation plan, or when you have a clear set of tasks to implement across the stack.
user-invokable: true
---

# Full-Stack Feature Implementation Workflow

Execute a full-stack feature implementation across database, backend, frontend, and testing layers. This skill follows the implementation plan produced by `/plan-feature` and builds all layers with integrated testing.

> [!CAUTION]
> **Scope boundary**: This skill implements code and commits it. It does **NOT** create pull requests, push to remote, run code reviews, or submit anything for merge. When implementation and commits are complete, **stop** and suggest the user run `/review-code` next. Do not proceed to PR creation — that is `/submit-pr`'s job.

## Step 1: Load Implementation Plan

Check for an implementation plan using the following priority:

> [!NOTE]
> GitHub issues created by `/plan-feature` are task-oriented work items — the decision record remains the authoritative source of council evaluations, rationale, and architectural context. When loading from an issue, always read the referenced decision record for full context.

### Option A: GitHub Issue (Primary)

If the user provides a GitHub issue number (e.g., `/build-feature 42` or `/build-feature #42`):

1. Fetch the issue details:

   ```bash
   gh issue view <number> --json title,body,labels,state,number
   ```

2. Validate the issue:
   - Confirm it has the `build-ready` label (warn if not — it may not have been through `/plan-feature` or may need further planning)
   - If the issue is closed, warn the user and ask whether to proceed

3. Parse the issue body to extract:
   - **Implementation Plan**: Task checkboxes organized by layer (Frontend, Backend, Database, Testing)
   - **Technical Context**: Architecture decisions, API contracts, schema changes
   - **Decision Record path**: Read the referenced decision record for full council context
   - **Feature Flag**: Flag name if applicable
   - **Success Metrics**: Measurable outcomes

4. Read the referenced decision record from the path specified in the issue for complete council rationale.

5. Signal work is in progress (see AGENTS.md "Label Management" for rules):

   ```bash
   # Single-developer constraint: only one issue should be in-progress at a time.
   # First, remove in-progress from any other issue that has it:
   gh issue list --label "in-progress" --state open --json number --jq '.[].number' | while read n; do
     gh issue edit "$n" --remove-label "in-progress"
   done

   gh issue edit <number> --add-label "in-progress"
   ```

6. Verify the issue is tracked on the [Product Roadmap]({PROJECT_BOARD_URL}) project board. If not, add it:

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

### Option B: Auto-Pick from Roadmap

If no issue number or description is given, automatically find the next `build-ready` ticket from the project roadmap:

1. **Determine the current phase.** Find the active milestone — the open milestone with the earliest due date that still has open issues:

   ```bash
   gh api repos/{OWNER}/{REPO}/milestones \
     --jq 'sort_by(.due_on) | map(select(.state == "open" and .open_issues > 0)) | .[0] | {title, number, due_on, open_issues}'
   ```

   If an issue already has the `in-progress` label, use its milestone instead:

   ```bash
   gh issue list --state open --label "in-progress" --json number,title,milestone --jq '.[0]'
   ```

2. **Fetch `build-ready` candidates.** List open issues in that milestone with the `build-ready` label, excluding any already labeled `in-progress`:

   ```bash
   gh issue list --state open --label "build-ready" --milestone "<milestone-title>" \
     --json number,title,labels \
     --jq '[.[] | select(.labels | map(.name) | index("in-progress") | not)]'
   ```

3. **Sort by project start date.** Fetch project items and match against candidates by issue number, then sort by the `start` field ascending:

   ```bash
   gh project item-list {PROJECT_NUMBER} --owner {OWNER} --format json --limit 200 | python3 -c "
   import json, sys
   data = json.load(sys.stdin)
   # <candidates> is a Python set literal of issue numbers, e.g., {22, 23, 10}
   candidates = <candidates>
   results = []
   for item in data.get('items', []):
       num = item.get('content', {}).get('number')
       if num in candidates:
           # Field is 'start', not 'startDate'
           start = item.get('start') or '9999-12-31'
           results.append((start, num, item.get('title', '')))
   results.sort()
   for start, num, title in results:
       display_start = start if start != '9999-12-31' else 'N/A'
       print(f'{display_start}\t#{num}\t{title}')
   "
   ```

   The first candidate (earliest `start` date) is the next ticket to work on. Issues without a `start` date sort last.

4. **If no candidates found**, fall through to Option C (Decision Record).

### CHECKPOINT: Present the recommended ticket and the full candidate list to the user.

Show a table of all `build-ready` candidates in the current phase, sorted by start date, with the top candidate highlighted as the recommendation:

| #     | Issue  | Title                   | Start Date     |
| ----- | ------ | ----------------------- | -------------- |
| **→** | **#N** | **Top candidate title** | **YYYY-MM-DD** |
| 2     | #N     | Other candidate         | YYYY-MM-DD     |

Ask the user to confirm:

- **(a)** Work on the recommended ticket
- **(b)** Pick a different ticket from the list (provide the issue number)
- **(c)** Skip auto-pick and describe what to build instead

If the user confirms a ticket, proceed with that issue number using the same flow as Option A (fetch full issue details, validate `build-ready`, extract plan, set `in-progress` label, etc.).

### Option C: Decision Record (Fallback)

If no issue number is given and no `build-ready` tickets are found on the roadmap:

1. Read the most recent decision record from `docs/decisions/` that matches the current feature
2. If no decision record exists, fall through to Option D

### Option D: User Description (Last Resort)

If no decision record exists, ask the user what to build.

> [!WARNING]
> No GitHub issue or decision record found. This means the planning pipeline (`/plan-feature`) was skipped — no council evaluation, no documented rationale, no structured task breakdown. Consider running `/plan-feature` first. Proceeding without a plan risks unreviewed architecture decisions.

### Extract Tasks

From the plan (regardless of source), identify:

- **Database changes**: Schema modifications, migrations, seed data
- **Backend tasks**: API endpoints, services, business logic
- **Frontend tasks**: Components, routing, state management, styling
- **Testing requirements**: Coverage goals, E2E scenarios, edge cases
- **Feature flag**: Whether to wrap behind a flag

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
git stash push -m "build-feature: stash before rebase"
git rebase origin/main
git stash pop
```

If the working tree is clean, rebase directly:

```bash
git rebase origin/main
```

## Step 2: Database Layer

If database changes are required:

1. Invoke `/database-design:postgresql` for schema design guidance

2. Design the Prisma schema changes:
   - Models with proper field types and defaults
   - Relations with referential integrity
   - Indexes for query performance
   - Constraints and validations
   - Enums where appropriate

3. Invoke `/database-migrations:sql-migrations` for migration best practices

### CHECKPOINT: Present the schema changes and migration plan to the user. Wait for approval before running.

4. Generate and apply the migration:
   ```bash
   pnpm db:migrate
   ```

## Step 3: Backend Implementation

Invoke `/backend-development:feature-development` for backend scaffolding guidance.

For each backend task from the plan:

### Types and Validation

- Define TypeScript interfaces for request/response types
- Create Zod schemas for runtime validation
- Export shared types for frontend consumption

### Service Layer

- Implement business logic in NestJS services
- Add proper error handling with typed exceptions
- Validate business rules and enforce invariants
- Keep services testable (dependency injection)

### API Layer

- Create tRPC procedures or NestJS controllers
- Wire up validation, auth guards, and rate limiting
- Return proper status codes and error formats

### Backend Tests

- Unit tests for services (mock dependencies)
- Integration tests for API endpoints
- Test validation, auth, and error handling

Run backend tests:

```bash
pnpm test
```

### CHECKPOINT: Present the API contract (endpoints, request/response types) to the user. Confirm the contract before building the frontend against it.

## Step 4: Frontend Implementation

For each frontend task from the plan:

### Component Creation

Invoke `/ui-design:create-component` for guided component creation with:

- Full TypeScript prop interfaces
- Tailwind CSS + shadcn/ui styling (invoke `/frontend-mobile-development:tailwind-design-system` for patterns)
- Keyboard navigation and ARIA attributes
- Responsive design
- Dark mode support (if applicable)

> [!NOTE]
> All user-visible text strings (headings, labels, descriptions, empty states, error messages, tooltips) must follow the **User-Facing Content Style** rules in `AGENTS.md`. No em dashes, no AI-slop vocabulary, no promotional inflation.

### State Management

If the feature requires client-side state:

- Invoke `/frontend-mobile-development:react-state-management` for state patterns
- Use React Query / tRPC hooks for server state
- Use local state (useState/useReducer) for UI state
- Use context or Zustand for shared client state

### Routing

If new pages or routes are needed:

- Add route definitions
- Create page components
- Add navigation links

### Content and SEO (for marketing or user-facing pages)

If this feature involves marketing pages, landing page copy, or product descriptions:

- Invoke `/seo-content-creation:seo-content-writer` for SEO content quality and E-E-A-T optimization
- Invoke `/content-marketing:content-marketer` for content strategy guidance
- Invoke `/accessibility-compliance:wcag-audit-patterns` alongside `/ui-design:accessibility-audit` for deeper WCAG compliance

### API Integration

- Wire components to backend via tRPC client or API hooks
- Handle loading states, error states, and empty states
- Add optimistic updates where appropriate

### Feature Flag (if applicable)

If the plan specifies a feature flag:

```typescript
const isEnabled = useFeatureFlag('FEATURE_NAME');
if (!isEnabled) return <ExistingComponent />;
return <NewFeature />;
```

### Frontend Tests

- Component render tests (React Testing Library)
- User interaction tests (click, type, submit)
- Integration tests with mocked API responses

### CHECKPOINT: Present the frontend implementation to the user. Describe what was built, show the component structure and key interactions.

## Step 5: End-to-End Testing

Write E2E test outlines for critical user flows:

- Happy path: User completes the main flow successfully
- Error path: User encounters validation errors, API failures
- Edge cases: Empty states, boundary conditions, concurrent actions

If E2E test infrastructure exists, implement the tests.

Run the full test suite:

```bash
pnpm test
```

Report coverage and any failures.

## Step 6: Self-Review

Before presenting to the user, perform a comprehensive self-review:

```bash
pnpm type-check      # No TypeScript errors
pnpm lint            # No linting violations
pnpm format:check    # No Prettier formatting issues
pnpm test            # All unit tests pass
pnpm test:smoke      # DI wiring and component tree render OK
```

If `format:check` fails, run `pnpm exec prettier --write` on the reported files before proceeding.

Check for:

- No hardcoded secrets or credentials
- Input validation on all user-facing inputs
- Proper error handling (no swallowed errors)
- Accessible components (ARIA, keyboard nav)
- No `any` types in TypeScript
- Proper loading and error states in UI

## Step 7: Update Documentation

If this feature changes how the project is set up, built, or run, update the relevant documentation **before committing**:

1. **README.md** — Update Quick Start, Running the Application, or Project Structure sections if the feature introduces new infrastructure, services, environment variables, or commands
2. **docs/DEVELOPMENT.md** — Update Prerequisites, Local Development Setup, Database Operations, or Troubleshooting sections as needed
3. **Makefile** — Add new targets for common operations (e.g., new Docker services, database commands)
4. **`.env.example` files** — Add new environment variables with clear descriptions and safe defaults
5. **`docs/INDEX.md`** — If any new files were added to `docs/`, add them to the appropriate table in the master documentation index

> [!IMPORTANT]
> A developer cloning the repo fresh must be able to get the project running by following README.md alone. If your feature adds a Docker service, database, new dev server, or environment variable, the docs MUST reflect it.

## Step 8: Commit

### CHECKPOINT: Present a complete summary to the user:

- Files created and modified (organized by layer)
- Database changes (if any)
- API endpoints added (if any)
- Components created (if any)
- Test results and coverage
- Any known limitations or deferred items

Wait for user approval before committing.

Create atomic, conventional commits. If the feature is small enough for one commit:

```
feat(<scope>): implement <feature-name>
```

If the feature is large, break into logical commits:

```
feat(db): add <model> schema and migration
feat(api): add <resource> endpoints
feat(web): add <feature> components and pages
test: add tests for <feature>
```

### Update GitHub Issue

If implementation was initiated from a GitHub issue:

1. Comment on it with progress:

   ```bash
   gh issue comment <number> --body "Implementation committed on branch \`<branch-name>\`. Proceeding to code review via \`/review-code\`."
   ```

> [!NOTE]
> Do **not** remove the `in-progress` label here. The label stays on the issue until it is closed (handled automatically by `.github/workflows/label-cleanup.yml`). This ensures the issue remains visibly in-progress through code review and PR submission.

## Step 9: Hand Off — STOP Here

> [!CAUTION]
> **This skill's work is done.** Do NOT proceed to create a pull request, push to remote, or run a code review. Those are separate skills with their own workflows and checkpoints.

Present the next step to the user:

- **Recommended**: Run `/review-code` for multi-perspective review before submitting
- **If more work remains**: Continue with remaining tasks from the implementation plan, then run `/review-code`
- **If UI-heavy**: Consider running `/ui-design:design-review` before code review

If working from a GitHub issue, remind the user:

- The PR should reference the issue with `Closes #<number>` so it auto-closes when merged
- `/submit-pr` will detect related issues from commit messages

**Do not push the branch, create a PR, or invoke `/submit-pr` from within this skill.**
