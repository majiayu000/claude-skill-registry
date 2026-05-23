---
name: create-pull-request
description: Create pull requests following project conventions. Use when: (1) creating a PR with gh pr create, (2) writing commit messages, (3) need branch naming guidance. Covers branch naming patterns, PR title/body format, and pre-commit checks.
---

# PR Creation Quick Reference

## Branch Naming

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/{description}` | `feature/impl-admin-example-api` |
| Bugfix | `fix/{description}` | `fix/example-creation-error` |
| Chore | `chore/{description}` | `chore/update-dependencies` |

## PR Title

Use English. Be concise and descriptive.

```
Implement AdminService.GetExample
Add validation for Example create API
Fix null pointer in tenant lookup
```

## PR Body Template

```markdown
## Proposed Changes

- Brief description of what was changed

## Implementation

{Verification details - curl commands, CLI output, or file changes}
```

## Implementation Section Examples

### API Endpoint

```markdown
## Implementation

### POST /admin/v1/tenants/{tenant_id}/examples

curl -X POST "http://localhost:8080/admin/v1/tenants/xxx/examples" \
    -H "Authorization: Bearer {token}" \
    -H "Content-Type: application/json" \
    -d '{"name": "Test", "description": "Test desc"}'

Response:
{"example": {"id": "xxx", "name": "Test", "created_at": "2025-01-01T00:00:00Z"}}
```

### Non-API Changes

```markdown
## Implementation

- Updated `internal/domain/model/example.go` with new validation
- Added unit tests in `example_test.go`
- Regenerated mocks with `make generate.mock`
```

## Pre-PR Checklist

```bash
make lint.go     # Must pass
make test        # Must pass
```

If applicable:
- `make migrate.up` - after DB changes
- `make generate.buf` - after proto changes
- `make generate.mock` - after repository interface changes

## Create PR Command

```bash
gh pr create --title "Implement feature" --body "$(cat <<'EOF'
## Proposed Changes

- Implemented new feature

## Implementation

{Details}
EOF
)"
```

## Important Notes

- Do NOT add AI attribution (no "Generated with Claude Code" or "Co-Authored-By: Claude")
- Keep commit messages and PR descriptions clean
- Run `self-review` skill before creating PR to catch issues early
