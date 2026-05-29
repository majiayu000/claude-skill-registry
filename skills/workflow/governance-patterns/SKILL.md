---
name: governance-patterns
description: Follow these patterns when implementing governance operations (copy, branch, transfer, promote, merge) in OptAIC. Covers artifact handling, RBAC mutations, lineage tracking, and activity emission.
---

# Governance Patterns

Guide for implementing resource governance operations with proper artifact management, RBAC mutations, and lineage tracking.

## When to Use

Apply when:
- Implementing copy/branch/transfer/promote/merge operations
- Managing resource artifacts (files, data, code)
- Mutating RBAC bindings during governance operations
- Tracking lineage and provenance of resources
- Building approval workflows for promotions

## Core Components

### ArtifactManager (`libs/core/artifacts.py`)

Manages file artifacts stored at `{DATA_DIR}/artifacts/{artifact_ref}/`.

```python
from libs.core.artifacts import ArtifactManager

manager = ArtifactManager(data_dir=data_dir)

# Create empty artifact
artifact_ref = manager.create_artifact()

# Copy artifact (for branch/promote)
new_ref = manager.copy_artifact(source_ref)

# File operations
manager.write_file(artifact_ref, "model.pkl", model_bytes)
content = manager.read_file(artifact_ref, "model.pkl")
files = manager.list_files(artifact_ref)
```

### GovernanceService (`libs/core/governance.py`)

Orchestrates governance operations with RBAC mutations.

```python
from libs.core.governance import GovernanceService

service = GovernanceService(artifact_manager=manager)

# Copy (reference only)
result = await service.copy_resource(session, actor, source_id=src, target_parent_id=parent)

# Branch (with file copy)
result = await service.branch_resource(session, actor, source_id=src, target_parent_id=parent)

# Transfer ownership
result = await service.transfer_resource(session, actor, resource_id=res, target_owner_id=owner)

# Promote to team
result = await service.promote_resource(session, actor, source_id=src, target_space_id=space, team_principal_id=team)

# Merge branch
result = await service.merge_resource(session, actor, source_id=branch, target_id=ancestor)
```

## Governance Operations

### Copy (Reference)

- **Artifact**: Same `artifact_ref` (no file copy)
- **RBAC**: No changes - user keeps existing role
- **Lineage**: Creates `copy_of` edge
- **Use Case**: Referencing shared definitions

### Branch

- **Artifact**: New `artifact_ref` with copied files
- **RBAC**: Actor=owner, source_owner=viewer
- **Lineage**: Creates `branch_of` edge
- **Use Case**: Personal modifications of official resources

### Transfer

- **Artifact**: Same `artifact_ref` (ownership change only)
- **RBAC**: Target=owner, previous=viewer
- **Lineage**: Creates `transferred_from` edge
- **Use Case**: Handing off resources to another user

### Promote

- **Artifact**: New `artifact_ref` with copied files
- **RBAC**: Team=owner, promoter=delegator
- **Lineage**: Creates `promoted_from` edge
- **Use Case**: Publishing personal work to team official

### Merge

- **Artifact**: Branch artifact replaces ancestor artifact
- **RBAC**: No changes (ancestor RBAC preserved)
- **Lineage**: Creates `merged_from` edge
- **Use Case**: Incorporating branch changes back to official

## RBAC Templates

Templates define role binding mutations for operations.

```python
template = RbacTemplate(
    name="branch",
    policy={
        "bindings": [
            {"principal": "actor_id", "role": "owner"},
            {"principal": "source_owner_id", "role": "viewer"},
        ],
        "revocations": []  # Optional role revocations
    }
)
```

Context variables for templates:
- `actor_id`: User performing the operation
- `source_owner_id`: Original owner of source resource
- `target_owner_id`: New owner for transfer
- `team_id`: Team principal for promote

## Lineage Edge Types

| Edge Type | Meaning |
|-----------|---------|
| `copy_of` | Resource references same artifact |
| `branch_of` | Resource is a branch with copied files |
| `transferred_from` | Ownership was transferred |
| `promoted_from` | Promoted to team space |
| `merged_from` | Branch merged back to ancestor |
| `derived_from` | General derivation (legacy) |

## API Endpoints

All endpoints at `/governance/resources/{resource_id}/`:

```
POST /copy      - Copy by reference
POST /branch    - Branch with file copy
POST /transfer  - Transfer ownership
POST /promote   - Promote to team
POST /merge     - Merge branch
GET  /lineage   - Query lineage chain
```

## Activity Actions

Governance operations emit these activities:

```
resource.copied      resource.branched
resource.transferred resource.promoted
resource.merged
```

## Database Schema

### Resource Table
- `artifact_ref`: UUID reference to artifact folder

### ResourceEdge Table
- `edge_type`: Type of relationship
- `created_by_principal_id`: Who created the edge

See [references/schema.md](references/schema.md) for details.

## Testing

```python
@pytest.fixture
def governance_service(artifact_manager):
    return GovernanceService(artifact_manager=artifact_manager)

async def test_branch_creates_new_artifact(governance_service, db_session):
    result = await governance_service.branch_resource(...)
    assert result["artifact_ref"] != source.artifact_ref
```

See [references/testing.md](references/testing.md) for patterns.

## Reference Files

- [Schema Details](references/schema.md) - Database schema for governance
- [Testing Patterns](references/testing.md) - How to test governance operations
- [RBAC Templates](references/rbac-templates.md) - Template definitions
