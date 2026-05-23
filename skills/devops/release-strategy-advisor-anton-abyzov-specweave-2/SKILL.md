---
name: release-strategy-advisor
description: Release strategy advisor - detects brownfield patterns (tags, CI/CD, changelogs), recommends versioning strategy based on architecture. Creates release-strategy.md.
---

# Release Strategy Advisor

**Expertise**: Release management strategy design, version alignment, brownfield release pattern detection, and living documentation of delivery processes.

## Core Capabilities

### 1. Brownfield Strategy Detection

**Analyzes existing projects to detect release patterns**:

**Git Analysis**:
- Version tags (v1.0.0, v2.1.0-rc.1, etc.)
- Tag patterns (semantic versioning, date-based, custom)
- Release branches (release/*, hotfix/*)
- Tag frequency and cadence

**CI/CD Detection**:
- GitHub Actions workflows (`.github/workflows/release.yml`)
- GitLab CI (`.gitlab-ci.yml`)
- Jenkins pipelines (`Jenkinsfile`)
- CircleCI config (`.circleci/config.yml`)
- Azure Pipelines (`azure-pipelines.yml`)

**Package Managers**:
- NPM: `package.json` (version, scripts: version/publish)
- Python: `setup.py`, `pyproject.toml`
- Java: `pom.xml`, `build.gradle`
- Go: `go.mod`
- Ruby: `*.gemspec`
- Rust: `Cargo.toml`

**Monorepo Tools**:
- Lerna (`lerna.json`)
- Nx (`nx.json`, `workspace.json`)
- Turborepo (`turbo.json`)
- Yarn Workspaces (`package.json` workspaces)
- Changesets (`.changeset/config.json`)

**Release Automation**:
- Semantic Release (`.releaserc`, `release.config.js`)
- Standard Version (`.versionrc`)
- Conventional Changelog
- Custom release scripts

### 2. Strategy Recommendation

**Suggests optimal strategy based on**:

**Project Architecture**:
- Single repository → Simple semver strategy
- Multi-repo (2-5 repos) → Coordinated or independent
- Multi-repo (5+ repos) → Umbrella versioning
- Monorepo → Workspace-based versioning
- Microservices → Service-level versioning

**Team Factors**:
- Small team (1-5) → Simple manual releases
- Medium team (5-20) → Semi-automated releases
- Large team (20+) → Fully automated releases

**Deployment Patterns**:
- Low frequency (<1/month) → Manual releases
- Medium frequency (1-4/month) → Semi-automated
- High frequency (daily/weekly) → Automated CI/CD
- Continuous deployment → Trunk-based + feature flags

**Dependencies**:
- No dependencies → Independent releases
- Weak coupling → Independent with coordination
- Strong coupling → Coordinated/lockstep releases
- Shared libraries → Umbrella versioning

### 3. Release Strategy Types

**Single Repo Strategies**:
```markdown
## Simple Semver
- One repository, one version
- Manual or automated bumps (patch/minor/major)
- GitHub releases + NPM/PyPI publish
- CHANGELOG.md maintenance
- Example: SpecWeave itself
```

**Multi-Repo Strategies**:
```markdown
## Coordinated Releases
- All repos share same version
- Release together (v1.0.0 across all)
- Synchronized CI/CD
- Example: Microservices with tight coupling

## Independent Releases
- Each repo has own version
- Release independently
- Example: service-a v2.1.0, service-b v1.5.0

## Umbrella Versioning
- Product version (v3.0.0) spans multiple repos
- Internal service versions tracked separately
- Example: "Product v3.0.0" contains:
  - frontend v2.5.0
  - backend v1.8.0
  - api v2.1.0
```

**Monorepo Strategies**:
```markdown
## Workspace-Based
- Lerna/Nx/Turborepo manage versions
- Independent package versions
- Changesets for semantic release
- Example: Babel, Jest

## Fixed Versioning
- All packages share same version
- Lerna --fixed mode
- Example: Angular packages
```

**Microservices Strategies**:
```markdown
## Service-Level Versioning
- Each service has own semantic version
- API contract versioning separate
- Rolling releases (deploy services independently)

## Coordinated Major Releases
- Independent minor/patch versions
- Coordinated major versions (breaking changes)
- Example: v2.x (service-a v2.3.0, service-b v2.1.0)
```

### 4. Release Candidate (RC) Management

**RC Patterns**:

**Pre-Release Tags**:
- `v1.0.0-rc.1`, `v1.0.0-rc.2` → `v1.0.0` (final)
- `v2.0.0-beta.1` → `v2.0.0-rc.1` → `v2.0.0`
- `v3.0.0-alpha.1` → `v3.0.0-beta.1` → `v3.0.0-rc.1` → `v3.0.0`

**Channel-Based**:
- Stable (production)
- Beta (pre-release testing)
- Alpha (early adopters)
- Canary (1% traffic, feature flags)

**Environment-Based**:
- Dev → Staging (RC) → Production (final)
- Feature branches → RC branch → Main branch

**RC Workflow**:
1. Create RC: `v1.0.0-rc.1`
2. Deploy to staging/beta channel
3. Testing & bug fixes (creates rc.2, rc.3, ...)
4. Validation complete → Promote RC to v1.0.0
5. Deploy to production

### 5. Living Documentation

**Creates release-strategy.md in**:

**Cross-Project** (applies to entire system):
```
.specweave/docs/internal/delivery/release-strategy.md
```

**Project-Specific** (multi-project mode):
```
.specweave/docs/internal/projects/{project-id}/delivery/release-strategy.md
```

**Document Structure**:
```markdown
# Release Strategy: {Product/Project Name}

## Current Strategy
- Type: Single-repo / Multi-repo / Monorepo / Microservices
- Versioning: Semantic / Date-based / Custom
- Alignment: Lockstep / Independent / Umbrella
- RC Process: Pre-release tags / Channels / Feature flags

## Repositories
- Repo A: {purpose, current version, release frequency}
- Repo B: {purpose, current version, release frequency}

## Version Alignment
- Major: Coordinated (breaking changes)
- Minor: Independent (new features)
- Patch: Independent (bug fixes)

## Release Candidate Workflow
1. Create RC tag: v1.0.0-rc.1
2. Deploy to staging
3. Testing phase (1 week)
4. Promote to production: v1.0.0

## CI/CD Integration
- GitHub Actions: .github/workflows/release.yml
- Automated: npm publish, Docker push, Deploy to K8s
- Manual gates: QA approval, stakeholder sign-off

## Changelog Management
- Tool: Conventional Changelog / Keep a Changelog
- Format: CHANGELOG.md (root or per-package)
- Automation: semantic-release / standard-version

## Hotfix Strategy
- Branch: hotfix/* from production tag
- Version: Patch bump (v1.0.1)
- Process: Fast-track testing, immediate deploy

## Release Checklist
- [ ] All tests passing
- [ ] Changelog updated
- [ ] Version bumped
- [ ] Git tag created
- [ ] GitHub release published
- [ ] Package published (NPM/PyPI/Docker)
- [ ] Deployment successful
- [ ] Documentation updated

## Metrics & Monitoring
- DORA Metrics: Deployment frequency, lead time, MTTR, change failure rate
- Release cadence: {weekly / bi-weekly / monthly}
- Hotfix frequency: {target <5% of releases}

## Decision History
- 2025-01-15: Adopted umbrella versioning (ADR-023)
- 2025-02-01: Introduced RC workflow (ADR-025)
- 2025-03-10: Migrated to semantic-release (ADR-028)
```

### 6. Integration with Brownfield Analyzer

**Automatic Strategy Detection** (when brownfield analyzer runs):

```bash
# Brownfield analyzer detects:
# 1. Repository structure (single/multi/monorepo)
# 2. Existing version tags
# 3. CI/CD configurations
# 4. Package manager configs
# 5. Release automation tools

# Then invokes release-strategy-advisor:
# - Analyze detected patterns
# - Classify release strategy
# - Document findings in release-strategy.md
# - Suggest improvements if needed
```

**Detection Output Example**:
```markdown
## Detected Release Strategy

**Type**: Multi-repo Independent Releases

**Evidence**:
- 3 repositories detected:
  - frontend: v2.5.0 (last release: 2025-01-10)
  - backend: v1.8.0 (last release: 2025-01-08)
  - shared: v1.2.0 (last release: 2024-12-15)

- Version alignment: None (independent)
- Release frequency: Weekly (frontend), Bi-weekly (backend), Monthly (shared)
- CI/CD: GitHub Actions with semantic-release
- Changelog: Conventional Changelog (auto-generated)

**Recommendations**:
1. Consider umbrella versioning for product releases
2. Add RC workflow for major versions
3. Align major versions for better API compatibility
```

## When to Use This Skill

**Ask me to**:

1. **Analyze existing release strategy**:
   - "What's our current release strategy?"
   - "Detect our versioning patterns"
   - "Analyze how we're releasing across repos"

2. **Recommend optimal strategy**:
   - "What release strategy should we use?"
   - "How should we version our microservices?"
   - "Should we use coordinated or independent releases?"

3. **Create release documentation**:
   - "Document our release process"
   - "Create release-strategy.md"
   - "Write down our versioning approach"

4. **Plan multi-repo releases**:
   - "How to coordinate releases across 5 repos?"
   - "Should we align versions?"
   - "What's the best RC workflow for us?"

5. **Brownfield integration**:
   - "Understand our existing release process"
   - "What release tools are we using?"
   - "Map our current deployment pipeline"

## Best Practices

**Version Alignment**:
- Lockstep: Use for tightly coupled services (shared breaking changes)
- Independent: Use for loosely coupled services (autonomous teams)
- Umbrella: Use for products with multiple independent modules

**RC Workflows**:
- Always use RC for major versions (breaking changes)
- Consider RC for minor versions if critical features
- Skip RC for patch versions (hotfixes) unless high risk

**Changelog Discipline**:
- Automate changelog generation (conventional commits)
- Manual curation for major releases (highlight key features)
- Link to GitHub issues/PRs for traceability

**Release Frequency**:
- High-risk changes: RC → staging → production (1-2 weeks)
- Low-risk changes: Direct to production (daily/weekly)
- Balance speed with stability (DORA metrics)

## Integration Points

**Brownfield Analyzer**:
- Detects existing patterns automatically
- Feeds data to release-strategy-advisor
- Creates baseline documentation

**Living Docs**:
- Stores strategy in delivery/ folder
- Updates on strategy changes
- Links to ADRs for decisions

**Multi-Project**:
- Different strategies per project
- Cross-project release coordination
- Shared release templates

**Increment Lifecycle**:
- Release increments span repositories
- Coordinated planning & execution
- Automated living docs sync

## Example Workflows

### Single-Repo Project (SpecWeave)

```bash
# 1. User asks for release strategy
"What release strategy should SpecWeave use?"

# 2. Advisor analyzes:
# - Single repo (GitHub: anton-abyzov/specweave)
# - NPM package
# - GitHub Actions for releases
# - Existing semver tags

# 3. Recommends:
# - Simple semver strategy
# - Automated releases via GitHub Actions
# - CHANGELOG.md maintenance
# - RC for major versions only

# 4. Creates:
# .specweave/docs/internal/delivery/release-strategy.md
```

### Multi-Repo Microservices

```bash
# 1. User asks for strategy
"How should we release our 5 microservices?"

# 2. Advisor analyzes:
# - 5 repos detected (user-service, order-service, ...)
# - Tight coupling (shared API contracts)
# - High deployment frequency (daily)

# 3. Recommends:
# - Umbrella versioning (product v1.0.0)
# - Independent service versions (service-a v2.3.0)
# - RC workflow for product major versions
# - Rolling releases for services

# 4. Creates:
# .specweave/docs/internal/delivery/release-strategy.md
# - Umbrella version matrix
# - Service version independence
# - RC workflow for product releases
```

### Monorepo (Lerna/Nx)

```bash
# 1. User asks for strategy
"How to version our Lerna monorepo?"

# 2. Advisor analyzes:
# - Monorepo with 12 packages
# - Lerna detected (lerna.json)
# - Changesets for versioning
# - Independent package releases

# 3. Recommends:
# - Independent versioning (Lerna independent mode)
# - Changesets for semantic release
# - Automated changelogs per package
# - Fixed versioning for core packages

# 4. Creates:
# .specweave/docs/internal/delivery/release-strategy.md
# - Lerna configuration explanation
# - Changesets workflow
# - Package grouping strategy
```

## Commands Integration

Works with release management commands:

- `/sw-release:init` - Analyze & recommend strategy
- `/sw-release:align` - Align versions across repos
- `/sw-release:rc` - Create release candidate
- `/sw-release:publish` - Execute release

## Dependencies

**Required**:
- Git (version tag analysis)
- SpecWeave core (living docs integration)

**Optional** (for detection):
- GitHub CLI (`gh`) - GitHub release detection
- NPM (`npm`) - NPM package detection
- Python (`python`) - Python package detection
- Lerna (`lerna`) - Monorepo detection
- Nx (`nx`) - Nx workspace detection

## Output

**Creates/Updates**:
- `.specweave/docs/internal/delivery/release-strategy.md` (cross-project)
- `.specweave/docs/internal/projects/{id}/delivery/release-strategy.md` (project-specific)

**Provides**:
- Current strategy analysis
- Recommended improvements
- RC workflow templates
- CI/CD integration guides
- Version alignment matrix
- Release checklist

---

**Remember**: Release strategy is a living document. Update it when:
- Architecture changes (new repos, services)
- Team size changes
- Deployment frequency changes
- Tooling changes (new CI/CD, monorepo tools)
- Lessons learned from releases

**Goal**: Clear, documented, repeatable release process that scales with your team and product.
