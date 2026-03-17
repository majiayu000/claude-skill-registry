---
name: multi-repo
version: 1.0.0
description: Multi-repository orchestration for coordinating atomic changes across dependent repositories. Tracks dependency graphs, coordinates cross-repo PRs, and detects breaking changes.
auto_activates:
  - "multiple repositories"
  - "cross-repo change"
  - "dependency graph"
  - "linked PRs"
  - "atomic cross-repo"
  - "breaking change detection"
explicit_triggers:
  - /amplihack:multi-repo
confirmation_required: false
token_budget: 2500
---

# Multi-Repository Orchestration Skill

## Purpose

Coordinate atomic changes across multiple repositories when features span repo boundaries. Track dependencies, manage linked PRs, and detect breaking changes before they propagate.

## When to Use This Skill

**USE FOR:**

- Changes that require coordinated updates across multiple repositories
- Managing repository dependency graphs
- Creating linked PRs that should merge together or in sequence
- Detecting breaking changes that affect dependent repositories
- Microservices or monorepo-alternative architectures

**AVOID FOR:**

- Single-repository changes (use default workflow)
- Forking/syncing operations (use git directly)
- Documentation-only changes
- Changes with no cross-repo dependencies

## Storage Location

All multi-repo data is stored in `.claude/data/multi-repo/`:

- `dependencies.yaml` - Repository dependency graph
- `linked-prs.yaml` - Currently active linked PR sets
- `breaking-changes.log` - History of detected breaking changes

## Dependency Graph Format

The dependency graph uses simple YAML:

```yaml
# .claude/data/multi-repo/dependencies.yaml
version: "1.0"
repositories:
  my-org/api-server:
    depends_on: []
    exposes:
      - type: api
        name: REST API v2
        contract: openapi.yaml

  my-org/web-client:
    depends_on:
      - repo: my-org/api-server
        type: api
        version: ">=2.0"
    exposes: []

  my-org/mobile-app:
    depends_on:
      - repo: my-org/api-server
        type: api
        version: ">=2.0"
    exposes: []
```

## Core Operations

### Operation 1: Initialize Dependency Graph

**When:** Setting up multi-repo tracking for the first time

**Process:**

1. Create `.claude/data/multi-repo/` directory if not exists
2. Create initial `dependencies.yaml` with current repository
3. Prompt for known dependencies (repos this one depends on)
4. Prompt for known dependents (repos that depend on this one)
5. Save and display the graph

**Command:** "Initialize multi-repo dependencies"

### Operation 2: Add Repository Dependency

**When:** Registering a new dependency relationship

**Process:**

1. Read current `dependencies.yaml`
2. Validate both repositories exist (via gh CLI)
3. Add dependency entry with type and version constraint
4. Update dependent repo's entry
5. Save changes

**Example:**

```
"Add dependency: my-org/web-client depends on my-org/api-server for REST API"
```

### Operation 3: Detect Breaking Changes

**When:** Before creating a PR that modifies a public interface

**Process:**

1. Identify changed files in current branch
2. Check if changes touch exposed contracts (API specs, schemas, exports)
3. Look up dependents in dependency graph
4. For each dependent:
   - Clone/fetch latest (use worktree if local)
   - Check if dependent uses affected interface
   - Report potential breakage
5. Generate impact report

**Output:**

```
Breaking Change Impact Report
=============================
Changed: my-org/api-server/openapi.yaml
  - Removed endpoint: DELETE /users/{id}
  - Modified field: User.email now required

Affected Dependents:
  - my-org/web-client (uses DELETE /users/{id})
  - my-org/mobile-app (no impact detected)

Recommendation: Coordinate changes with my-org/web-client
```

### Operation 4: Create Linked PRs

**When:** Making atomic changes across multiple repositories

**Process:**

1. User specifies the set of repos to update
2. For each repo in order (respecting dependency graph):
   - Create worktree or navigate to repo
   - Create feature branch with common prefix
   - Make changes
   - Create PR with links to other PRs in set
3. Track linked PRs in `linked-prs.yaml`
4. Add cross-references in PR descriptions

**Linked PR Format:**

```yaml
# .claude/data/multi-repo/linked-prs.yaml
linked_sets:
  - id: "auth-v2-migration"
    created: "2025-11-25T10:00:00Z"
    status: "pending"
    prs:
      - repo: my-org/api-server
        pr: 123
        status: "merged"
        merge_order: 1
      - repo: my-org/web-client
        pr: 456
        status: "approved"
        merge_order: 2
      - repo: my-org/mobile-app
        pr: 789
        status: "open"
        merge_order: 3
```

### Operation 5: Coordinate Merge Sequence

**When:** Merging a linked PR set

**Process:**

1. Read linked PR set from `linked-prs.yaml`
2. Verify all PRs are approved/ready
3. Merge in dependency order (upstream first)
4. Wait for CI to pass after each merge
5. Update linked-prs status
6. Report completion

**Merge Order Logic:**

1. Repos with no dependencies merge first
2. Repos with dependencies merge after their dependencies
3. Circular dependencies: Error (should not exist in healthy graph)

## Integration with Worktree Manager

When working across local repositories, leverage the worktree-manager agent:

1. For each local repo in dependency graph:
   - Use `git worktree add` to create isolated workspace
   - Worktrees go in `./worktrees/{repo-name}-{branch}/`
2. Make coordinated changes across worktrees
3. Commit and push from each worktree
4. Clean up worktrees after PRs merged

## Integration with PM Architect

For complex multi-repo projects:

1. Use backlog-curator to track cross-repo items
2. Use workstream-coordinator for multi-repo workstreams
3. Linked PRs map to single workstream items
4. Breaking change detection feeds into roadmap planning

## Philosophy Alignment

**Ruthless Simplicity:**

- YAML-based dependency graph (no database required)
- Leverage existing git and gh CLI tools
- Minimal skill surface area

**Zero-BS Implementation:**

- All operations are functional from day one
- No "planned" features - only what works now
- Breaking change detection actually checks code

**Modular Design:**

- Skill is self-contained
- Data stored in simple files
- Can be used independently or with PM Architect

## Examples

### Example 1: API Breaking Change

**Scenario:** Updating API endpoint signature

```
User: "I need to change the /users endpoint from GET to POST"

Skill Response:
1. Detected change to api-server/openapi.yaml
2. Scanned dependents:
   - web-client: Uses GET /users in 3 locations
   - mobile-app: Uses GET /users in 2 locations
3. Impact: HIGH - 5 usages across 2 repositories

Recommended approach:
1. Add POST /users endpoint (non-breaking)
2. Create linked PRs to update web-client and mobile-app
3. Deprecate GET /users with sunset date
4. Remove GET /users after clients migrate
```

### Example 2: Coordinated Feature Release

**Scenario:** New authentication flow spanning 3 repos

```
User: "Implement OAuth2 across api-server, web-client, and mobile-app"

Skill Response:
1. Created linked PR set: "oauth2-implementation"
2. Dependency order: api-server -> web-client, mobile-app (parallel)
3. Created branches:
   - api-server: feat/oauth2-backend
   - web-client: feat/oauth2-frontend
   - mobile-app: feat/oauth2-mobile
4. PRs created with cross-references:
   - api-server#123 (merge first)
   - web-client#456 (after #123)
   - mobile-app#789 (after #123)
```

## Limitations

- Dependency graph is per-workspace (not centralized)
- Requires gh CLI authenticated for PR operations
- Breaking change detection is heuristic (may miss runtime changes)
- Circular dependencies are not supported (and shouldn't exist)

## Success Criteria

- Changes across repos are coordinated atomically
- Breaking changes are detected before they cause production issues
- PRs merge in correct dependency order
- Teams have visibility into cross-repo impacts
