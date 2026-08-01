---
name: openapi-toolkit-googleai-dart
description: 'Automates updating googleai_dart when Google AI OpenAPI spec changes.
  Fetches latest spec, compares against current, generates changelogs and prioritized
  implementation plans. Use for: (1) Checking fo'
---

---
name: openapi-toolkit-googleai-dart
description: Automates updating googleai_dart when Google AI OpenAPI spec changes. Fetches latest spec, compares against current, generates changelogs and prioritized implementation plans. Use for: (1) Checking for API updates, (2) Generating implementation plans for spec changes, (3) Creating new models/endpoints from spec, (4) Syncing local spec with upstream. Triggers: "update api", "sync openapi", "new endpoints", "api changes", "check for updates", "update spec", "api version", "fetch spec", "compare spec", "what changed in the api", "implementation plan".
---

# OpenAPI Toolkit (googleai_dart)

Uses shared scripts from [openapi-toolkit](../../shared/openapi-toolkit/README.md) with googleai_dart-specific configuration.

## Prerequisites

- `GEMINI_API_KEY` or `GOOGLE_AI_API_KEY` environment variable set
- Working directory: Repository root
- Python 3

## Spec Registry

| Spec | Description | Auth Required |
|------|-------------|---------------|
| `main` | Core Gemini API (generation, embeddings, files, models, etc.) | Yes |
| `interactions` | Experimental Interactions API (server-side state, agents) | No |

## Workflow

### 1. Fetch Latest Specs

```bash
# Fetch all specs + auto-discover new ones
python3 .claude/shared/openapi-toolkit/scripts/fetch_spec.py \
  --config-dir .claude/skills/openapi-toolkit-googleai-dart/config

# Fetch specific spec only
python3 .claude/shared/openapi-toolkit/scripts/fetch_spec.py \
  --config-dir .claude/skills/openapi-toolkit-googleai-dart/config --spec main
```

Output: `/tmp/openapi-toolkit-googleai-dart/latest-main.json`, `/tmp/openapi-toolkit-googleai-dart/latest-interactions.json`

### 2. Analyze Changes

```bash
python3 .claude/shared/openapi-toolkit/scripts/analyze_changes.py \
  --config-dir .claude/skills/openapi-toolkit-googleai-dart/config \
  packages/googleai_dart/specs/openapi.json /tmp/openapi-toolkit-googleai-dart/latest-main.json \
  --format all \
  --changelog-out /tmp/openapi-toolkit-googleai-dart/changelog-main.md \
  --plan-out /tmp/openapi-toolkit-googleai-dart/plan-main.md
```

Generates:
- `changelog-main.md` - Human-readable change summary
- `plan-main.md` - Prioritized implementation plan (P0-P4)

### 3. Implement Changes

Before implementing, read `references/implementation-patterns.md` for:
- Model class structure and conventions
- Enum naming patterns
- JSON serialization patterns
- Test patterns and PR templates

Use templates from `../../shared/openapi-toolkit/assets/`:
- `model_template.dart` - Model class structure
- `enum_template.dart` - Enum type structure
- `test_template.dart` - Unit test structure
- `example_template.dart` - Example file structure

### 3.5 Update Documentation (MANDATORY)

Before running the review checklist, update all documentation:

1. **README.md** - Add/update:
   - New resources to Features section
   - New resources to API Coverage section
   - New example references in Examples section

2. **example/** - Create/update:
   - `{feature}_example.dart` for each new resource

3. **CHANGELOG.md** - Add entry for new features/changes

### 4. Review & Validate (MANDATORY)

Perform the four-pass review documented in `references/REVIEW_CHECKLIST.md`:

```bash
# Pass 2: Barrel file verification
python3 .claude/shared/openapi-toolkit/scripts/verify_exports.py \
  --config-dir .claude/skills/openapi-toolkit-googleai-dart/config

# Pass 3: Documentation completeness
python3 .claude/shared/openapi-toolkit/scripts/verify_readme.py \
  --config-dir .claude/skills/openapi-toolkit-googleai-dart/config
python3 .claude/shared/openapi-toolkit/scripts/verify_examples.py \
  --config-dir .claude/skills/openapi-toolkit-googleai-dart/config
python3 .claude/shared/openapi-toolkit/scripts/verify_readme_code.py \
  --config-dir .claude/skills/openapi-toolkit-googleai-dart/config

# Pass 4: Property-level verification
python3 .claude/shared/openapi-toolkit/scripts/verify_model_properties.py \
  --config-dir .claude/skills/openapi-toolkit-googleai-dart/config

# Dart quality checks (run from packages/googleai_dart)
cd packages/googleai_dart && dart analyze --fatal-infos && dart format --set-exit-if-changed . && dart test test/unit/
```

**Pass 4 is critical** - catches missing properties in parent models (e.g., `Tool`, `Candidate`).

### 5. Finalize

```bash
# Copy fetched specs to persisted locations
cp /tmp/openapi-toolkit-googleai-dart/latest-main.json packages/googleai_dart/specs/openapi.json
cp /tmp/openapi-toolkit-googleai-dart/latest-interactions.json packages/googleai_dart/specs/openapi-interactions.json

# Run quality checks (from packages/googleai_dart)
cd packages/googleai_dart && dart test && dart analyze && dart format --set-exit-if-changed .
```

## Package-Specific References

- [Package Guide](references/package-guide.md) - Package structure, naming conventions
- [Implementation Patterns](references/implementation-patterns.md) - Model conventions, serialization patterns
- [Review Checklist](references/REVIEW_CHECKLIST.md) - Four-pass validation process

## Troubleshooting

- **API key error**: Export `GEMINI_API_KEY` or `GOOGLE_AI_API_KEY`
- **Network errors**: Check connectivity; retry after a few seconds
- **No changes detected**: Summary shows all zeros; no action needed
- **New specs discovered**: Add them to `config/specs.json` and re-run
