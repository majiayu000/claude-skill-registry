---
name: openapi-toolkit-mistralai-dart
description: 'Automates updating mistralai_dart when Mistral AI OpenAPI spec changes.
  Fetches latest spec, compares against current, generates changelogs and prioritized
  implementation plans. Use for: (1) Checking'
---

---
name: openapi-toolkit-mistralai-dart
description: Automates updating mistralai_dart when Mistral AI OpenAPI spec changes. Fetches latest spec, compares against current, generates changelogs and prioritized implementation plans. Use for: (1) Checking for API updates, (2) Generating implementation plans for spec changes, (3) Creating new models/endpoints from spec, (4) Syncing local spec with upstream. Triggers: "update api", "sync openapi", "new endpoints", "api changes", "check for updates", "update spec", "api version", "fetch spec", "compare spec", "what changed in the api", "implementation plan".
---

# OpenAPI Toolkit (mistralai_dart)

Uses shared scripts from [openapi-toolkit](../../shared/openapi-toolkit/README.md).

## Prerequisites

- `MISTRAL_API_KEY` environment variable set (for integration tests)
- Working directory: Repository root

## Quick Start

```bash
# Fetch latest spec
python3 .claude/shared/openapi-toolkit/scripts/fetch_spec.py \
  --config-dir .claude/skills/openapi-toolkit-mistralai-dart/config

# Analyze changes (create mode for new package)
python3 .claude/shared/openapi-toolkit/scripts/analyze_changes.py \
  --config-dir .claude/skills/openapi-toolkit-mistralai-dart/config \
  --mode create /tmp/openapi-toolkit-mistralai-dart/latest-main.json \
  --plan-out /tmp/implementation-plan.md

# Analyze changes (update mode for existing package)
python3 .claude/shared/openapi-toolkit/scripts/analyze_changes.py \
  --config-dir .claude/skills/openapi-toolkit-mistralai-dart/config \
  packages/mistralai_dart/specs/openapi.json /tmp/openapi-toolkit-mistralai-dart/latest-main.json \
  --format all --changelog-out /tmp/changelog.md --plan-out /tmp/plan.md

# Verify implementation
python3 .claude/shared/openapi-toolkit/scripts/verify_exports.py \
  --config-dir .claude/skills/openapi-toolkit-mistralai-dart/config

python3 .claude/shared/openapi-toolkit/scripts/verify_model_properties.py \
  --config-dir .claude/skills/openapi-toolkit-mistralai-dart/config
```

## Package-Specific References

- [Package Guide](references/package-guide.md)
- [Implementation Patterns](references/implementation-patterns.md)
- [Review Checklist](references/REVIEW_CHECKLIST.md)

## External References

- [Official Mistral API Documentation](https://docs.mistral.ai/api/)
- [Official Mistral TypeScript SDK](https://github.com/mistralai/client-ts)
- [Mistral OpenAPI Spec](https://docs.mistral.ai/openapi.yaml)
