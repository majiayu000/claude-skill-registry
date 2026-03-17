---
name: when-managing-multiple-repos-use-github-multi-repo
description: Multi-repository coordination, synchronization, and architecture management with AI swarm orchestration. Coordinates repo-architect, code-analyzer, and coordinator agents across multiple repositories to maintain consistency, propagate changes, manage dependencies, and ensure architectural alignment. Handles monorepo-to-multi-repo migrations, cross-repo refactoring, and synchronized releases. Use when managing microservices, multi-package ecosystems, or coordinating changes across related repositories.
agents:
  - repo-architect
  - code-analyzer
  - hierarchical-coordinator
  - cicd-engineer
topology: hierarchical
mcp_tools:
  - mcp__claude-flow__swarm_init
  - mcp__claude-flow__agent_spawn
  - mcp__claude-flow__task_orchestrate
  - mcp__flow-nexus__github_repo_analyze
---

# GitHub Multi-Repository Management Skill

## Overview

Orchestrate complex operations across multiple related GitHub repositories with intelligent agent coordination. This skill enables consistent architecture enforcement, synchronized dependency updates, cross-repo refactoring, and coordinated releases for microservices, multi-package ecosystems, and distributed system architectures.

## When to Use This Skill

Activate this skill when managing microservices architectures spanning multiple repositories, coordinating changes across frontend/backend/infrastructure repos, migrating from monorepo to multi-repo structure, propagating breaking changes across dependent repositories, maintaining consistent coding standards across teams, synchronizing releases for multi-package systems, or enforcing architectural patterns across an organization.

Use for both small-scale coordination (2-5 repos) and large-scale orchestration (10+ repositories), one-time migrations or ongoing maintenance, and establishing governance for multi-repo ecosystems.

## Agent Coordination Architecture

### Swarm Topology

Initialize a **hierarchical topology** with a coordinator agent managing specialized worker agents. Hierarchical structure enables centralized decision-making for consistency while delegating specialized tasks to expert agents.

```bash
# Initialize hierarchical swarm for multi-repo coordination
npx claude-flow@alpha swarm init --topology hierarchical --max-agents 8 --strategy adaptive
```

### Specialized Agent Roles

**Hierarchical Coordinator** (`hierarchical-coordinator`): Top-level orchestrator that maintains global view of all repositories, makes architectural decisions, coordinates cross-repo operations, and ensures consistency. Acts as the single source of truth for multi-repo strategy.

**Repository Architect** (`repo-architect`): Analyzes repository structures, defines architectural patterns, creates dependency graphs, identifies coupling issues, and designs migration strategies. Maintains the architectural vision across repositories.

**Code Analyzer** (`code-analyzer`): Scans codebases for patterns, dependencies, and inconsistencies. Identifies code duplication across repos, tracks API contracts, and validates architectural compliance.

**CI/CD Engineer** (`cicd-engineer`): Manages build pipelines, deployment workflows, and release orchestration. Coordinates continuous integration across repositories and handles versioning strategies.

**Worker Agents** (spawned dynamically): Execute repository-specific tasks such as refactoring, testing, documentation updates, and dependency bumps. Scaled based on number of target repositories.

## Multi-Repository Workflows (SOP)

### Workflow 1: Cross-Repository Change Propagation

Propagate breaking changes, API updates, or architectural patterns across multiple repositories.

**Phase 1: Impact Analysis**

**Step 1.1: Initialize Hierarchical Coordination**

```bash
# Set up hierarchical swarm
mcp__claude-flow__swarm_init topology=hierarchical maxAgents=8 strategy=adaptive

# Spawn coordinator and specialists
mcp__claude-flow__agent_spawn type=coordinator name=hierarchical-coordinator
mcp__claude-flow__agent_spawn type=analyst name=repo-architect
mcp__claude-flow__agent_spawn type=analyst name=code-analyzer
mcp__claude-flow__agent_spawn type=coder name=cicd-engineer
```

**Step 1.2: Analyze Repository Dependencies**

Use `scripts/repo-graph.sh` to build dependency graph:

```bash
# Generate dependency graph across all repositories
bash scripts/repo-graph.sh build-graph \
  --repos "repo1,repo2,repo3" \
  --output "references/dependency-graph.dot"
```

Visualize the dependency graph to identify impact scope:

```bash
# Render graph visualization
dot -Tpng references/dependency-graph.dot -o dependency-graph.png
```

**Step 1.3: Identify Affected Repositories**

Launch coordinator to analyze impact:

```plaintext
Task("Hierarchical Coordinator", "
  Analyze the impact of <CHANGE_DESCRIPTION> across all repositories:

  1. Review dependency graph at references/dependency-graph.dot
  2. Identify direct dependents (repositories importing affected code)
  3. Identify transitive dependents (downstream consumers)
  4. Categorize changes by risk level (breaking/compatible/enhancement)
  5. Create propagation strategy with sequencing

  Store impact analysis in memory: multi-repo/impact-analysis
  Use scripts/repo-graph.sh for dependency traversal
  Run hooks: npx claude-flow@alpha hooks pre-task --description 'impact analysis'
", "hierarchical-coordinator")
```

**Phase 2: Parallel Repository Updates**

Execute coordinated updates across all affected repositories.

**Step 2.1: Spawn Worker Agents per Repository**

For each affected repository, spawn a dedicated worker agent:

```plaintext
Task("Worker: Repository 1", "
  Apply changes to repository <REPO_1>:

  1. Clone repository: bash scripts/multi-repo.sh clone <REPO_1>
  2. Create feature branch: change-propagation-<DATE>
  3. Apply code changes based on coordinator strategy
  4. Update tests to reflect new API contracts
  5. Validate build passes: npm test / cargo test
  6. Commit changes with standardized message
  7. Push branch and create draft PR

  Store results in memory: multi-repo/updates/<REPO_1>
  Run hooks for coordination
", "coder")

Task("Worker: Repository 2", "
  Apply changes to repository <REPO_2>:
  [Same steps as above, tailored to REPO_2]

  Store results in memory: multi-repo/updates/<REPO_2>
", "coder")

# Spawn additional workers for each repository
# All workers execute in parallel
```

**Step 2.2: Coordinate Test Execution**

After all workers complete, test repositories together:

```plaintext
Task("CI/CD Engineer", "
  Validate changes across all repositories:

  1. Set up integration test environment
  2. Build all modified repositories in dependency order
  3. Run integration tests with new versions
  4. Check for breaking changes in API contracts
  5. Validate performance hasn't degraded

  Use scripts/integration-test.sh for orchestration
  Store test results in memory: multi-repo/test-results
", "cicd-engineer")
```

**Phase 3: Synchronized Release**

Coordinate pull request creation and merging across repositories.

**Step 3.1: Create Pull Requests**

Generate PRs for all repositories simultaneously:

```bash
# Create PRs across all repos
bash scripts/multi-repo.sh create-prs \
  --repos "repo1,repo2,repo3" \
  --title "Propagate: <CHANGE_DESCRIPTION>" \
  --body-template "references/pr-template.md" \
  --labels "multi-repo-sync,automated"
```

**Step 3.2: Coordinate Review and Merge**

Track PR status and coordinate merging in dependency order:

```plaintext
Task("Hierarchical Coordinator", "
  Coordinate PR review and merge process:

  1. Monitor PR status using scripts/multi-repo.sh pr-status
  2. Ensure PRs are reviewed in dependency order
  3. Merge upstream dependencies first (libraries, shared code)
  4. Wait for CI to pass on each merge
  5. Merge downstream consumers after dependencies released
  6. Verify no build breaks in dependency chain

  Use scripts/multi-repo.sh merge-sequence for ordering
  Store merge sequence in memory: multi-repo/merge-plan
", "hierarchical-coordinator")
```

**Step 3.3: Tag and Release**

Create coordinated releases across repositories:

```bash
# Execute synchronized releases
bash scripts/multi-repo.sh synchronized-release \
  --repos "repo1,repo2,repo3" \
  --version-strategy "minor" \
  --release-notes-dir "references/release-notes"
```

### Workflow 2: Monorepo to Multi-Repo Migration

Migrate a monolithic repository into multiple focused repositories while preserving history.

**Phase 1: Architecture Planning**

**Step 1.1: Analyze Monorepo Structure**

```plaintext
Task("Repository Architect", "
  Analyze monorepo structure and design migration strategy:

  1. Map directory structure and module boundaries
  2. Identify logical separation points (services, packages, layers)
  3. Analyze import/dependency patterns using scripts/analyze-deps.sh
  4. Detect circular dependencies that need refactoring
  5. Create proposed repository structure
  6. Design shared library strategy for common code

  Reference references/migration-best-practices.md
  Store architecture plan in memory: multi-repo/migration-plan
", "repo-architect")
```

**Step 1.2: Generate Dependency Graph**

Create comprehensive dependency visualization:

```bash
# Analyze monorepo dependencies
bash scripts/analyze-deps.sh \
  --monorepo-path <PATH> \
  --output references/monorepo-dependencies.json

# Generate split recommendations
bash scripts/repo-graph.sh recommend-split \
  --deps references/monorepo-dependencies.json \
  --output references/split-strategy.md
```

**Phase 2: Repository Creation and History Preservation**

**Step 2.1: Create Target Repositories**

```bash
# Create new repositories with proper structure
bash scripts/multi-repo.sh create-repos \
  --org <ORGANIZATION> \
  --repos-config references/new-repos.json \
  --template "references/repo-template"
```

**Step 2.2: Extract Code with History**

For each target repository, extract relevant code while preserving Git history:

```bash
# Extract subdirectory with full history
bash scripts/migration.sh extract-with-history \
  --source <MONOREPO_PATH> \
  --subdirectory <SUBDIR> \
  --target-repo <NEW_REPO> \
  --preserve-authors true
```

**Step 2.3: Refactor Cross-Repository Dependencies**

```plaintext
Task("Code Analyzer", "
  Refactor dependencies for multi-repo structure:

  1. Identify hard-coded paths that need updating
  2. Convert internal imports to package dependencies
  3. Extract shared code to common library repository
  4. Update build configurations for new structure
  5. Generate package.json / Cargo.toml with correct dependencies

  Use scripts/refactor-imports.sh for automated conversion
  Store refactoring changes in memory: multi-repo/refactoring
", "code-analyzer")
```

**Phase 3: Validation and Cutover**

**Step 3.1: Parallel Build Validation**

Ensure all new repositories build independently:

```plaintext
Task("CI/CD Engineer", "
  Validate all new repositories build and test successfully:

  1. Set up CI pipelines for each new repository
  2. Configure dependency resolution (npm registry, cargo)
  3. Run full test suites in each repository
  4. Validate integration between repositories
  5. Compare test results with monorepo baseline

  Use scripts/validate-migration.sh
  Store validation results in memory: multi-repo/validation
", "cicd-engineer")
```

**Step 3.2: Gradual Migration Plan**

Create phased cutover strategy:

```bash
# Generate migration timeline
bash scripts/migration.sh create-timeline \
  --repos references/new-repos.json \
  --risk-assessment references/risk-analysis.md \
  --output references/migration-timeline.md
```

### Workflow 3: Architectural Pattern Enforcement

Ensure consistent architectural patterns across all repositories.

**Phase 1: Pattern Definition**

**Step 1.1: Define Architectural Standards**

Create comprehensive architecture documentation in `references/architecture-standards.md` covering:
- Directory structure conventions
- Module organization patterns
- API design guidelines
- Testing strategies
- Documentation requirements
- CI/CD pipeline standards

**Step 1.2: Create Enforcement Rules**

Define linting rules and validation checks in `references/enforcement-rules.json`:
- Static analysis rules
- Dependency policy (allowed/forbidden packages)
- File naming conventions
- Code complexity thresholds
- Test coverage minimums

**Phase 2: Compliance Scanning**

**Step 2.1: Scan All Repositories**

```plaintext
Task("Code Analyzer", "
  Scan all repositories for architectural compliance:

  1. Clone all repositories: bash scripts/multi-repo.sh clone-all
  2. Run architectural linting: bash scripts/arch-lint.sh --config references/enforcement-rules.json
  3. Generate compliance report for each repository
  4. Identify violations by severity (critical/high/medium/low)
  5. Create prioritized remediation plan

  Store compliance reports in memory: multi-repo/compliance
", "code-analyzer")
```

**Step 2.2: Automated Remediation**

For common violations, generate automated fixes:

```bash
# Apply automated fixes where safe
bash scripts/auto-fix-violations.sh \
  --repos-dir <CLONED_REPOS> \
  --rules references/enforcement-rules.json \
  --create-prs true
```

**Phase 3: Continuous Monitoring**

**Step 3.1: Set Up Compliance Tracking**

```bash
# Create dashboard for ongoing monitoring
bash scripts/compliance-dashboard.sh setup \
  --repos references/repo-list.txt \
  --rules references/enforcement-rules.json \
  --output-dir compliance-dashboard
```

**Step 3.2: Automated Alerts**

Configure alerts for architectural violations:

```bash
# Set up GitHub Actions for compliance checks
bash scripts/setup-compliance-ci.sh \
  --repos references/repo-list.txt \
  --workflow-template references/compliance-workflow.yml
```

## MCP Tool Integration

### Repository Analysis

```bash
# Analyze each repository's structure and quality
mcp__flow-nexus__github_repo_analyze repo=<owner/repo1> analysis_type=code_quality
mcp__flow-nexus__github_repo_analyze repo=<owner/repo2> analysis_type=performance
mcp__flow-nexus__github_repo_analyze repo=<owner/repo3> analysis_type=security
```

### Swarm Orchestration

```bash
# Monitor multi-repo operation progress
mcp__claude-flow__swarm_status verbose=true

# Track task completion across repositories
mcp__claude-flow__task_status detailed=true

# Get performance metrics
mcp__claude-flow__agent_metrics metric=performance
```

## Best Practices

**Hierarchical Coordination**: Always use a single coordinator agent to maintain consistency and make global decisions. Worker agents handle repository-specific tasks but report to coordinator.

**Dependency-Order Execution**: Respect dependency graphs when applying changes. Update upstream dependencies before downstream consumers to avoid build breaks.

**Atomic Operations**: Group related changes across repositories into single coordinated operations. Use draft PRs and synchronized merges to maintain atomicity.

**History Preservation**: When migrating or refactoring, preserve Git history. Use `git filter-branch` or `git subtree` to maintain commit provenance.

**Testing Integration**: Always test repositories together after multi-repo changes. Individual repository tests may pass while integration fails.

**Rollback Strategy**: Maintain ability to rollback changes across all repositories. Use Git tags and release branches to enable coordinated rollback.

**Communication**: Keep stakeholders informed of multi-repo operations. Use consistent PR descriptions, labels, and commit messages across repositories.

## Error Handling

**Partial Failure Recovery**: If some repositories update successfully while others fail, coordinate rollback or forward-fix strategy based on dependency relationships.

**Merge Conflict Resolution**: For cross-repo conflicts, use coordinator to determine resolution strategy. Prioritize maintaining API contracts and build stability.

**Network Failures**: Implement retry logic with exponential backoff for GitHub API calls. Cache repository metadata to reduce API dependencies.

**Circular Dependency Detection**: If circular dependencies detected during analysis, coordinator must create refactoring plan to break cycles before migration proceeds.

## References

- `references/architecture-standards.md` - Organizational architecture patterns
- `references/enforcement-rules.json` - Automated compliance rules
- `references/migration-best-practices.md` - Repository migration guidelines
- `references/pr-template.md` - Standardized PR description template
- `references/repo-template/` - Template structure for new repositories
- `scripts/multi-repo.sh` - Multi-repository operation utilities
- `scripts/repo-graph.sh` - Dependency graph analysis
- `scripts/migration.sh` - Monorepo migration tools
- `scripts/analyze-deps.sh` - Dependency analysis
- `scripts/arch-lint.sh` - Architectural linting
- `scripts/integration-test.sh` - Cross-repo integration testing
