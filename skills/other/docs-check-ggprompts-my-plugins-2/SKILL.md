---
name: docs-check
description: "Documentation check checkpoint for conductor gates. Analyzes code changes to determine if documentation needs updating. Returns structured result with pass/fail status and documentation suggestions."
user-invocable: true
---

# Docs Check Checkpoint

Documentation checkpoint that verifies docs are up-to-date with code changes.

## What This Skill Does

1. Analyzes what changed in the code
2. Identifies documentation-relevant changes
3. Checks if corresponding docs exist and are current
4. Suggests documentation updates if needed
5. Writes result to checkpoint file

## Workflow

### Step 1: Get Changed Files

```bash
# For uncommitted changes
git diff --name-only HEAD
git diff --name-only --cached

# For branch diff
git diff --name-only main...HEAD
```

### Step 2: Categorize Changes

Identify what type of changes were made:

| Change Type | Documentation Impact |
|-------------|---------------------|
| New API endpoint | API docs needed |
| New CLI command | Usage docs needed |
| Config schema change | Config docs needed |
| Breaking change | Migration guide needed |
| New feature | README/feature docs |
| Bug fix | Usually no docs needed |
| Refactor (no API change) | No docs needed |

### Step 3: Check Existing Documentation

Look for docs that might need updates:

```bash
# Common doc locations
ls README.md CHANGELOG.md docs/ *.md 2>/dev/null

# API docs
ls docs/API.md docs/api/ swagger.yaml openapi.yaml 2>/dev/null

# Check if changed files have corresponding docs
# e.g., if routes/api.js changed, check docs/API.md
```

### Step 4: Analyze Documentation Gaps

For each significant change, check:

1. **API changes** - Is there API documentation? Does it cover new endpoints?
2. **Config changes** - Are new config options documented?
3. **Breaking changes** - Is there a migration guide?
4. **New features** - Is the feature documented for users?
5. **CHANGELOG** - Is there a changelog entry?

### Step 5: Create Structured Result

```json
{
  "checkpoint": "docs-check",
  "timestamp": "2026-01-19T12:00:00Z",
  "passed": true,
  "changes_analyzed": 5,
  "suggestions": [
    {
      "type": "api",
      "file": "docs/API.md",
      "message": "New endpoint POST /api/spawn should be documented",
      "priority": "high"
    },
    {
      "type": "changelog",
      "file": "CHANGELOG.md",
      "message": "Consider adding changelog entry for new feature",
      "priority": "medium"
    }
  ],
  "summary": "2 documentation suggestions. None are blocking."
}
```

**Result Fields:**
- `passed`: true if no critical documentation missing
- `changes_analyzed`: number of changed files analyzed
- `suggestions`: array of `{type, file, message, priority: "high"|"medium"|"low"}`
- `summary`: brief human-readable summary

### Step 6: Write Checkpoint File

```bash
mkdir -p .checkpoints
cat > .checkpoints/docs-check.json << 'EOF'
{
  "checkpoint": "docs-check",
  ...
}
EOF
```

## Decision Criteria

**Pass if:**
- No critical documentation gaps
- Minor suggestions are acceptable

**Fail if:**
- Breaking changes without migration guide
- New public API without documentation
- README claims features that don't exist

**Suggestion priorities:**
- `high`: Should be documented before merge
- `medium`: Should be documented soon
- `low`: Nice to have, not blocking

## Documentation Patterns to Check

### API Changes

If files like `routes/*.js`, `api/*.ts`, `endpoints/*` changed:
- Check `docs/API.md` or similar
- Look for OpenAPI/Swagger specs
- Verify new endpoints are documented

### Configuration Changes

If files like `config.js`, `.env.example`, `settings.json` changed:
- Check README configuration section
- Verify new options are documented
- Check for breaking config changes

### CLI Changes

If argument parsing or command files changed:
- Check `--help` output accuracy
- Verify README usage section
- Check man pages if applicable

### Breaking Changes

Indicators of breaking changes:
- Removed or renamed exports
- Changed function signatures
- Modified config schema
- Database migration files

### CHANGELOG

For any user-visible change:
- Should have CHANGELOG entry
- Entry should mention issue ID if applicable
- Breaking changes should be clearly marked

## Example Usage

When invoked as `/docs-check`:

```
Running Docs Check checkpoint...

Analyzing changed files...
Found 8 changed files:
- backend/routes/api.js (modified)
- backend/modules/spawn-handler.js (new)
- extension/hooks/useSpawn.ts (new)
- README.md (modified)
- docs/API.md (not modified)

Checking documentation coverage...

API changes detected:
- New endpoint: POST /api/spawn
- docs/API.md does not document this endpoint

New feature detected:
- Spawn functionality added
- README.md was updated (good!)

Result:
{
  "passed": true,
  "suggestions": [
    {
      "type": "api",
      "file": "docs/API.md",
      "message": "Document POST /api/spawn endpoint",
      "priority": "high"
    }
  ],
  "summary": "1 high-priority suggestion: API docs need update"
}

Checkpoint result written to .checkpoints/docs-check.json
```

## Files to Always Check

| Project Type | Doc Files |
|--------------|-----------|
| Node.js | `README.md`, `CHANGELOG.md`, `docs/`, `API.md` |
| Python | `README.md`, `docs/`, `CHANGELOG.md`, `*.rst` |
| Rust | `README.md`, `CHANGELOG.md`, `docs/` |
| Go | `README.md`, `doc.go`, `docs/` |

## Notes

- This checkpoint is advisory by default (suggestions don't block)
- For strict projects, configure to fail on high-priority suggestions
- Always check CHANGELOG for any user-visible changes
- Breaking changes MUST have documentation before merge
