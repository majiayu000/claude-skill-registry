---
name: documentation-sync-specialist
description: Automated documentation maintenance for Vigil Guard v2.0.0's documentation files. Use for syncing docs with code changes, version updates, API generation, cross-reference validation, 3-branch architecture docs, and documentation creation.
version: 2.0.0
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Documentation Synchronization Specialist (v2.0.0)

## Overview

Automated documentation maintenance for Vigil Guard's documentation files, ensuring consistency with v2.0.0 codebase changes, 3-branch architecture updates, and API modifications.

## When to Use This Skill

- Auto-updating docs after code changes
- Synchronizing version numbers across files
- Generating API.md from Express routes
- Flagging outdated documentation sections
- Maintaining cross-reference consistency
- Creating documentation for new features
- Documenting 3-branch architecture (v2.0.0)

## v2.0.0 Architecture Documentation

### Key Changes to Document

```yaml
v1.x → v2.0.0 Documentation Updates:

Architecture:
  - 40-node sequential → 24-node 3-branch parallel
  - 6-9 services → 11 Docker services
  - New branch services: heuristics-service, semantic-service

Configuration:
  - rules.config.json (829 lines) → REMOVED/merged
  - unified_config.json: 246 → 303 lines, v5.0.0
  - pii.conf: 247 → 361 lines

Testing:
  - 100+ tests → 8 E2E test files
  - New: arbiter-decision.test.js

New Concepts:
  - 3-Branch Detection (A:30%, B:35%, C:35%)
  - Arbiter v2 Decision Engine
  - Branch degradation handling
  - Weighted fusion scoring
```

### Documentation Structure

```
docs/
├── QUICKSTART.md              # 5-minute setup (v2.0.0)
├── USER_GUIDE.md              # Complete manual
├── API.md                     # REST API reference
├── ARCHITECTURE_v2.0.0.md     # 3-branch system architecture
├── DETECTION_CATEGORIES.md    # Patterns in unified_config.json
├── PII_DETECTION.md           # Dual-language PII
├── CLICKHOUSE_RETENTION.md    # Data lifecycle
├── CONFIGURATION.md           # Variable reference
├── AUTHENTICATION.md          # JWT + RBAC
├── SECURITY.md                # Best practices
├── DOCKER.md                  # 11 containers orchestration
├── GRAFANA_SETUP.md           # Dashboard setup
├── INSTALLATION.md            # Step-by-step
├── MAINTENANCE.md             # Operations
├── MIGRATION_v2.0.0.md        # v1.x → v2.0.0 upgrade
├── TROUBLESHOOTING.md         # Common issues
└── ... (additional files)
```

## Common Tasks

### Task 1: Version Number Update (v2.0.0)

**Trigger:** Version bump to v2.0.0

```bash
# Detect version change
OLD_VERSION="v1.8.1"
NEW_VERSION="v2.0.0"

# Update all references
find docs/ -name "*.md" -type f -exec sed -i '' "s/$OLD_VERSION/$NEW_VERSION/g" {} \;

# Files typically affected:
# - ARCHITECTURE_v1.8.1.md → rename to ARCHITECTURE_v2.0.0.md
# - USER_GUIDE.md (version references)
# - QUICKSTART.md (version in examples)
# - MIGRATION_v2.0.0.md (new file)
# - CLAUDE.md (version history)
```

**Automation:**
```yaml
on_version_bump:
  1. Grep all .md files for old version
  2. Replace with new version (v2.0.0)
  3. Rename ARCHITECTURE_v*.md if needed
  4. Create MIGRATION_v2.0.0.md from template
  5. Update CLAUDE.md version history
  6. Commit: "docs: update version references to v2.0.0"
```

### Task 2: 3-Branch Architecture Documentation

**New sections for ARCHITECTURE_v2.0.0.md:**

```markdown
## 3-Branch Parallel Detection Pipeline

### Overview
```
Input → Validator → 3-Branch Executor (PARALLEL)
                         ├── Branch A: Heuristics (:5005) - 30%
                         ├── Branch B: Semantic (:5006) - 35%
                         └── Branch C: LLM Guard (:8000) - 35%
                                    ↓
                    Arbiter v2 → Decision → PII → Output
```

### Branch Specifications

| Branch | Service | Port | Weight | Timeout | Function |
|--------|---------|------|--------|---------|----------|
| A | heuristics-service | 5005 | 30% | 1000ms | Pattern matching |
| B | semantic-service | 5006 | 35% | 2000ms | Embedding similarity |
| C | prompt-guard-api | 8000 | 35% | 3000ms | LLM validation |

### Arbiter v2 Decision Logic
- **BLOCK:** Weighted score >= 70
- **SANITIZE:** Weighted score 30-69
- **ALLOW:** Weighted score < 30
```

### Task 3: API Documentation Generation

**Trigger:** New endpoint added to Express backend

```typescript
// Source: services/web-ui/backend/src/server.ts
// New v2.0.0 endpoints:

// Branch health check
app.get('/api/health/branches', authMiddleware, branchHealthHandler);

// Branch analysis proxies
app.post('/api/analyze/heuristics', authMiddleware, heuristicsHandler);
app.post('/api/analyze/semantic', authMiddleware, semanticHandler);

// Branch metrics
app.get('/api/metrics/branches', authMiddleware, branchMetricsHandler);
```

**Generate API.md section:**
```markdown
## Branch Services API (v2.0.0)

### GET /api/health/branches
Check health status of all 3 branch detection services.

**Response:**
```json
{
  "branch_a": { "name": "Heuristics", "port": 5005, "healthy": true },
  "branch_b": { "name": "Semantic", "port": 5006, "healthy": true },
  "branch_c": { "name": "LLM Guard", "port": 8000, "healthy": true }
}
```

### POST /api/analyze/heuristics
Test heuristics service (Branch A) directly.

**Request:**
```json
{
  "text": "input to analyze",
  "request_id": "test-123"
}
```
```

### Task 4: Config Variable Documentation

**Trigger:** New variable added to variables.json

```json
// v2.0.0 new variables
{
  "name": "branch_a_weight",
  "key": "branch_a_weight",
  "type": "number",
  "default": 0.30,
  "description": "Heuristics branch weight in arbiter fusion (0.0-1.0)",
  "group": "3-Branch Detection"
},
{
  "name": "arbiter_block_threshold",
  "key": "arbiter_block_threshold",
  "type": "number",
  "default": 70,
  "description": "Minimum weighted score for BLOCK decision",
  "group": "3-Branch Detection"
}
```

### Task 5: Migration Guide (v1.x → v2.0.0)

**Template: `docs/MIGRATION_v2.0.0.md`**

```markdown
# Migration Guide: v1.8.1 → v2.0.0

## Breaking Changes
- [ ] Architecture: 40-node sequential → 24-node 3-branch parallel
- [ ] Config: rules.config.json removed (merged into unified_config.json)
- [ ] Services: 2 new containers (heuristics-service, semantic-service)
- [ ] ClickHouse schema: Add branch columns

## Database Migrations
```sql
-- Run in ClickHouse
ALTER TABLE n8n_logs.events_processed
  ADD COLUMN branch_a_score Float32 DEFAULT 0,
  ADD COLUMN branch_b_score Float32 DEFAULT 0,
  ADD COLUMN branch_c_score Float32 DEFAULT 0,
  ADD COLUMN arbiter_decision String DEFAULT '';
```

## Service Updates
```bash
# Pull new images
docker-compose pull

# Start new services
docker-compose up -d heuristics-service semantic-service
```

## Workflow Import
1. Export old workflow from n8n
2. Import: `services/workflow/workflows/Vigil Guard v2.0.0.json`
3. Verify 24 nodes visible

## Verification
- [ ] Branch health: `curl http://localhost/api/health/branches`
- [ ] Arbiter decision in logs: `SELECT arbiter_decision FROM events_processed LIMIT 1`
- [ ] All 11 services running: `./scripts/status.sh`
```

## Integration with Other Skills

### With workflow-json-architect:
```yaml
When: Workflow JSON modified (24 nodes)
Action:
  - Update ARCHITECTURE_v2.0.0.md (node descriptions)
  - Update USER_GUIDE.md (workflow examples)
  - Create MIGRATION.md if breaking changes
```

### With pattern-library-manager:
```yaml
When: New detection pattern added to unified_config.json
Action:
  - Update DETECTION_CATEGORIES.md (category list)
  - Update CONFIGURATION.md (new config variables)
  - Note: patterns now in unified_config.json v5.0.0
```

### With docker-vigil-orchestration:
```yaml
When: Docker configuration changed (11 services)
Action:
  - Update DOCKER.md (service descriptions)
  - Add heuristics-service (port 5005)
  - Add semantic-service (port 5006)
  - Update port reference table
```

### With express-api-developer:
```yaml
When: New API endpoint added
Action:
  - Regenerate API.md (routes table)
  - Add branch service endpoints (v2.0.0)
  - Update AUTHENTICATION.md (if auth required)
```

## Automation Workflows

### Workflow 1: On Code Change

```yaml
trigger: git commit
actions:
  1. Parse commit message for affected components
  2. Map components to documentation files
  3. Run freshness checks on affected docs
  4. Flag outdated sections
  5. Create PR with doc updates or TODO comments
```

### Workflow 2: Release Preparation (v2.0.0)

```yaml
trigger: Tag v2.0.0 created
actions:
  1. Update all version references to v2.0.0
  2. Generate CHANGELOG.md from commits
  3. Create MIGRATION_v2.0.0.md from template
  4. Update README.md badges
  5. Verify API.md matches server.ts routes
  6. Document 3-branch architecture
  7. Commit: "docs: prepare for v2.0.0 release"
```

## Metrics & KPIs

```yaml
success_metrics:
  update_lag: <5 minutes (from code change to doc update)
  version_consistency: 100% (no stale version references)
  broken_links: 0
  auto_update_rate: 95% (5% manual review)

v2.0.0_specific:
  3_branch_docs: Complete (architecture, API, migration)
  unified_config_docs: Updated (303 lines reference)
  test_docs: Updated (8 E2E files reference)
```

## Troubleshooting

### Issue: Docs out of sync with v2.0.0 code

**Diagnosis:**
```bash
# Check for old version references
grep -rn "v1\.[0-9]\+\.[0-9]\+" docs/ | grep -v "Binary"
grep -rn "rules.config.json" docs/  # Should be minimal
grep -rn "40-node\|40 node" docs/  # Should be 0
```

**Solution:**
```bash
# Update to v2.0.0
OLD="v1.8.1"
NEW="v2.0.0"
find docs/ -name "*.md" -exec sed -i '' "s/$OLD/$NEW/g" {} \;

# Remove rules.config.json references
# Replace with unified_config.json

# Update architecture references
# Replace "40-node" with "24-node 3-branch"
```

## Quick Reference

```bash
# Check version consistency
grep -rn "v[0-9]\+\.[0-9]\+\.[0-9]\+" docs/ | sort -u

# Validate links
./scripts/validate-doc-links.sh

# Generate API docs
./scripts/generate-api-docs.sh

# Sync config docs
./scripts/sync-config-docs.js
```

## Reference Files

### Documentation Sources
- Main docs: `docs/*.md`
- Service docs: `services/*/README.md`
- Root: `README.md`, `CONTRIBUTING.md`, `CLAUDE.md`

### v2.0.0 Key References
- Workflow: `services/workflow/workflows/Vigil Guard v2.0.0.json` (24 nodes)
- Config: `services/workflow/config/unified_config.json` (303 lines, v5.0.0)
- PII: `services/workflow/config/pii.conf` (361 lines)
- Tests: `services/workflow/tests/e2e/` (8 test files)

---

**Last Updated:** 2025-12-09
**Version:** v2.0.0
**Architecture:** 3-Branch Parallel Detection (24 nodes)
**Services:** 11 Docker containers
