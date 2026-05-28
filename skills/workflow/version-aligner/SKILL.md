---
name: version-aligner
description: Multi-repo version alignment - lockstep/independent/umbrella strategies, semver constraints, version conflict detection.
---

# Version Aligner

**Expertise**: Multi-repository version alignment, semantic versioning, version conflict detection, and compatibility validation.

## Core Capabilities

### 1. Semantic Versioning (Semver)

**Enforces semver rules**:

**Format**: `MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]`

**Version Bump Rules**:
```yaml
MAJOR (1.0.0 → 2.0.0):
  - Breaking changes (incompatible API)
  - Remove features
  - Change behavior of existing features
  Examples:
    - Remove deprecated endpoints
    - Change function signatures
    - Modify data formats

MINOR (1.0.0 → 1.1.0):
  - New features (backward compatible)
  - Add endpoints/functions
  - Deprecate (but don't remove) features
  Examples:
    - Add new API endpoints
    - Add optional parameters
    - New module exports

PATCH (1.0.0 → 1.0.1):
  - Bug fixes (no API changes)
  - Performance improvements
  - Documentation updates
  Examples:
    - Fix null pointer error
    - Optimize database query
    - Update README
```

**Pre-Release Tags**:
```yaml
# Alpha: Early development (unstable)
1.0.0-alpha.1, 1.0.0-alpha.2, ...

# Beta: Feature complete (testing)
1.0.0-beta.1, 1.0.0-beta.2, ...

# RC: Release candidate (near production)
1.0.0-rc.1, 1.0.0-rc.2, ...

# Final: Production release
1.0.0
```

### 2. Version Alignment Strategies

**Lockstep Versioning** (all repos share version):

```yaml
Strategy: Lockstep
Current State:
  - frontend: v2.5.0
  - backend: v2.5.0
  - api: v2.5.0
  - shared: v2.5.0

Proposed Bump: MAJOR (breaking change in API)
New State:
  - frontend: v3.0.0
  - backend: v3.0.0
  - api: v3.0.0
  - shared: v3.0.0

Rules:
  - ALL repos MUST bump together
  - Use highest bump type (if any repo needs MAJOR, all bump MAJOR)
  - Version always stays in sync
```

**Independent Versioning** (each repo has own version):

```yaml
Strategy: Independent
Current State:
  - frontend: v4.2.0
  - backend: v2.8.0
  - api: v3.1.0
  - shared: v1.5.0

Changes:
  - frontend: Bug fix → PATCH bump
  - backend: New feature → MINOR bump
  - api: No changes → No bump
  - shared: Breaking change → MAJOR bump

New State:
  - frontend: v4.2.1 (patch)
  - backend: v2.9.0 (minor)
  - api: v3.1.0 (unchanged)
  - shared: v2.0.0 (major)

Rules:
  - Each repo versions independently
  - Only bump repos with changes
  - Validate compatibility constraints
```

**Umbrella Versioning** (product version + service versions):

```yaml
Strategy: Umbrella
Product: v5.0.0 (umbrella)

Version Matrix:
  - frontend: v4.2.0
  - backend: v2.8.0
  - api: v3.1.0
  - shared: v1.5.0

Changes for Product v6.0.0:
  - frontend: v4.2.0 → v5.0.0 (major redesign)
  - backend: v2.8.0 → v2.9.0 (new endpoints)
  - api: v3.1.0 → v4.0.0 (breaking changes)
  - shared: v1.5.0 → v1.5.0 (no changes)

New Product: v6.0.0 (umbrella)
  - frontend: v5.0.0
  - backend: v2.9.0
  - api: v4.0.0
  - shared: v1.5.0

Rules:
  - Product version bumps for milestones
  - Services version independently
  - Track matrix in release-strategy.md
```

### 3. Conventional Commits Analysis

**Analyzes commits to suggest version bumps**:

**Commit Patterns**:
```bash
# MAJOR (breaking change)
feat!: remove legacy authentication
BREAKING CHANGE: Old auth endpoints removed

# MINOR (new feature)
feat: add real-time notifications
feat(api): add WebSocket support

# PATCH (bug fix)
fix: prevent null pointer in user service
fix(ui): correct button alignment
perf: optimize database queries

# No version bump
docs: update README
chore: upgrade dependencies
style: format code
refactor: extract helper function
test: add unit tests
```

**Version Bump Calculation**:
```bash
# Example commit history
git log v2.5.0..HEAD --oneline

feat!: remove deprecated endpoints       # BREAKING
feat: add dark mode toggle               # FEATURE
fix: prevent crash on logout             # BUGFIX
docs: update API documentation           # NO BUMP
chore: upgrade React to v18              # NO BUMP

# Analysis
Breaking changes: 1 → MAJOR bump (v2.5.0 → v3.0.0)
Features: 1 → Overridden by MAJOR
Bug fixes: 1 → Overridden by MAJOR

# Suggested: v2.5.0 → v3.0.0
```

### 4. Version Conflict Detection

**Detects incompatible versions**:

**Dependency Version Conflicts**:
```yaml
# Scenario: Two services depend on different versions of shared-lib

service-a:
  package.json: "shared-lib": "^2.0.0"
  Currently using: v2.0.0 ✓

service-b:
  package.json: "shared-lib": "^1.5.0"
  Currently using: v1.8.0 ✗

Conflict:
  - service-a requires shared-lib v2.x (breaking changes)
  - service-b still on shared-lib v1.x (outdated)
  - Cannot release until service-b upgrades

Resolution:
  1. Update service-b to "shared-lib": "^2.0.0"
  2. Test service-b with shared-lib v2.0.0
  3. Release service-b
  4. Then proceed with coordinated release
```

**API Contract Version Conflicts**:
```yaml
# Scenario: Frontend expects API v3, but backend provides v2

frontend:
  api-client: v3.0.0
  Expects: POST /api/v3/users (new endpoint)

backend:
  Current version: v2.8.0
  Provides: POST /api/v2/users (old endpoint)

Conflict:
  - Frontend expects v3 API
  - Backend hasn't released v3 yet
  - Deployment will fail

Resolution:
  1. Release backend v3.0.0 first (Wave 1)
  2. Verify API v3 endpoints work
  3. Then release frontend v5.0.0 (Wave 2)
```

### 5. Compatibility Validation

**Validates cross-repo compatibility**:

**Semver Range Checking**:
```typescript
// Example: Validate service-a can work with shared-lib versions

// service-a/package.json
{
  "dependencies": {
    "shared-lib": "^2.0.0"  // Allows 2.0.0 to <3.0.0
  }
}

// Validation
shared-lib v2.0.0 → Compatible ✓
shared-lib v2.5.0 → Compatible ✓
shared-lib v2.9.9 → Compatible ✓
shared-lib v3.0.0 → Incompatible ✗ (MAJOR change)
```

**API Contract Validation**:
```yaml
# OpenAPI spec comparison

api-gateway v2.8.0 (current):
  POST /api/v2/users:
    parameters:
      - name: email (required)
      - name: password (required)

api-gateway v3.0.0 (proposed):
  POST /api/v3/users:
    parameters:
      - name: email (required)
      - name: password (required)
      - name: phoneNumber (optional)  # NEW (backward compatible)

Compatibility:
  - New optional field → Minor version bump (v2.8.0 → v2.9.0) ✗
  - But route changed (/v2 → /v3) → Major version bump (v3.0.0) ✓
  - Verdict: v3.0.0 is correct ✓
```

### 6. Version Matrix Management

**Tracks versions for umbrella releases**:

**Version Matrix Document**:
```markdown
# Product Version Matrix

## v6.0.0 (Latest - 2025-01-15)
- frontend: v5.0.0
- backend: v2.9.0
- api-gateway: v4.0.0
- auth-service: v2.1.0
- user-service: v2.0.0
- order-service: v3.2.0
- shared-lib: v2.0.0
- database-schema: v12

## v5.0.0 (Previous - 2024-12-10)
- frontend: v4.2.0
- backend: v2.8.0
- api-gateway: v3.1.0
- auth-service: v2.0.0
- user-service: v1.8.0
- order-service: v3.1.0
- shared-lib: v1.5.0
- database-schema: v11

## Compatibility Matrix

| Product | Frontend | Backend | API Gateway | Shared Lib | Schema |
|---------|----------|---------|-------------|------------|--------|
| v6.0.0  | v5.0.0   | v2.9.0  | v4.0.0      | v2.0.0     | v12    |
| v5.0.0  | v4.2.0   | v2.8.0  | v3.1.0      | v1.5.0     | v11    |
| v4.0.0  | v3.5.0   | v2.5.0  | v2.8.0      | v1.2.0     | v10    |

## Breaking Changes

### v6.0.0
- API Gateway v3 → v4: Removed legacy /v2 endpoints
- Shared Lib v1 → v2: Changed authentication interface
- Schema v11 → v12: Added user_metadata table

### v5.0.0
- Frontend v4 → v5: React 16 → 18 (requires Node.js 18+)
- User Service v1 → v2: Changed user creation API
```

### 7. Automated Version Bumping

**Suggests and executes version bumps**:

**Interactive Version Bump**:
```bash
# Command
/sw-release:align

# Interactive prompts
? Which repositories to align?
  ◉ frontend (v4.2.0)
  ◉ backend (v2.8.0)
  ◉ api-gateway (v3.1.0)
  ◯ shared-lib (v2.0.0) - no changes

? Alignment strategy?
  ◯ Lockstep (all repos same version)
  ◉ Independent (bump changed repos only)
  ◯ Umbrella (product milestone)

# Analysis
Analyzing conventional commits since last release...

frontend (v4.2.0):
  - 12 commits since v4.2.0
  - Breaking changes: 1
  - Features: 3
  - Bug fixes: 5
  Suggested: v5.0.0 (MAJOR)

backend (v2.8.0):
  - 8 commits since v2.8.0
  - Features: 2
  - Bug fixes: 3
  Suggested: v2.9.0 (MINOR)

api-gateway (v3.1.0):
  - 15 commits since v3.1.0
  - Breaking changes: 2
  - Features: 4
  Suggested: v4.0.0 (MAJOR)

? Confirm version bumps?
  ◉ frontend: v4.2.0 → v5.0.0
  ◉ backend: v2.8.0 → v2.9.0
  ◉ api-gateway: v3.1.0 → v4.0.0

[Yes / No / Edit]
```

**Automated Execution**:
```bash
# Updates package.json
npm version major  # frontend
npm version minor  # backend
npm version major  # api-gateway

# Creates git tags
git tag v5.0.0 (frontend)
git tag v2.9.0 (backend)
git tag v4.0.0 (api-gateway)

# Updates CHANGELOG.md
# - Extracts commits since last tag
# - Groups by type (breaking, features, fixes)
# - Generates markdown

# Updates version matrix
# - Adds new product version row
# - Links to service versions
# - Documents breaking changes
```

## When to Use This Skill

**Ask me to**:

1. **Align versions across repos**:
   - "Align versions for all microservices"
   - "Sync versions before release"
   - "What versions should we bump to?"

2. **Detect version conflicts**:
   - "Check for version conflicts"
   - "Validate cross-repo compatibility"
   - "Are our dependencies aligned?"

3. **Suggest version bumps**:
   - "What version should we bump to?"
   - "Analyze commits for version bump"
   - "Calculate semver from commits"

4. **Manage version matrices**:
   - "Update version matrix"
   - "Show compatibility matrix"
   - "Track umbrella version history"

5. **Validate compatibility**:
   - "Can frontend v5.0.0 work with backend v2.8.0?"
   - "Check API contract compatibility"
   - "Validate dependency ranges"

## Best Practices

**Semver Discipline**:
- Never skip versions (v1.0.0 → v1.1.0, not v1.0.0 → v1.2.0)
- Use pre-release tags for testing (v1.0.0-rc.1)
- Document breaking changes clearly

**Dependency Management**:
- Pin major versions ("^2.0.0" not "*")
- Update dependencies regularly (avoid drift)
- Test compatibility before bumping

**Version Matrix**:
- Update after every product release
- Link to ADRs for breaking changes
- Track deprecation timelines

**Automation**:
- Use conventional commits (enables automated analysis)
- Automate changelog generation
- Validate versions in CI/CD

## Integration Points

**Release Strategy Advisor**:
- Reads alignment strategy from release-strategy.md
- Adapts to lockstep/independent/umbrella

**Release Coordinator**:
- Provides version bump suggestions
- Validates compatibility before release
- Updates version matrix post-release

**RC Manager**:
- Handles pre-release version tags
- Promotes RC to final version
- Tracks RC version history

**Brownfield Analyzer**:
- Detects existing version patterns
- Extracts current version matrix
- Suggests alignment improvements

## Example Workflows

### Independent Versioning

```bash
# 1. Analyze changes
/sw-release:align

# 2. Review suggested bumps
Frontend v4.2.0 → v5.0.0 (breaking changes)
Backend v2.8.0 → v2.9.0 (new features)
API v3.1.0 → v3.1.1 (bug fixes only)

# 3. Validate compatibility
✓ Frontend v5.0.0 compatible with Backend v2.8.0+
✓ Backend v2.9.0 compatible with API v3.1.0+
✗ Shared-lib v1.5.0 outdated (requires v2.0.0)

# 4. Fix blocking issues
Update Backend to use shared-lib v2.0.0

# 5. Execute version bumps
✓ All versions aligned
✓ Tags created
✓ Changelogs updated
```

### Umbrella Versioning

```bash
# 1. Create product release
/sw:increment "0040-product-v6-release"

# 2. Analyze component versions
Current umbrella: v5.0.0
Proposed: v6.0.0 (major milestone)

# 3. Review version matrix
Frontend: v4.2.0 → v5.0.0 (redesign)
Backend: v2.8.0 → v2.9.0 (new API)
API: v3.1.0 → v4.0.0 (breaking changes)
Shared: v1.5.0 → v2.0.0 (breaking changes)

# 4. Validate umbrella bump
Breaking changes detected → MAJOR bump correct ✓
Product v5.0.0 → v6.0.0 ✓

# 5. Update version matrix
.specweave/docs/internal/delivery/version-matrix.md updated ✓
```

## Commands Integration

Works with release commands:

- `/sw-release:align` - Interactive version alignment
- `/sw-release:validate-versions` - Check compatibility
- `/sw-release:bump <repo> <type>` - Bump specific repo
- `/sw-release:matrix` - Show version matrix

## Dependencies

**Required**:
- Git (version tags)
- Semver library (version parsing)
- SpecWeave core (living docs)

**Optional**:
- NPM (`npm version`) - Automated bumping
- Conventional Commits (commit analysis)
- GitHub CLI (`gh release`) - Release notes

## Output

**Creates/Updates**:
- `package.json` (version field)
- Git tags (v1.0.0, v2.0.0, etc.)
- `CHANGELOG.md` (release notes)
- `.specweave/docs/internal/delivery/version-matrix.md`
- Release strategy documentation

**Provides**:
- Version bump suggestions
- Compatibility validation report
- Version conflict detection
- Dependency graph
- Version history

---

**Remember**: Version alignment is critical for multi-repo architectures. Always:
- Follow semantic versioning strictly
- Validate compatibility before releasing
- Document breaking changes clearly
- Update version matrices regularly
- Automate where possible (conventional commits + semantic-release)

**Goal**: Consistent, predictable versioning across all repositories with clear compatibility guarantees.
