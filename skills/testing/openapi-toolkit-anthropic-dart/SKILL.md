---
name: openapi-toolkit-anthropic-dart
description: 'Automates updating anthropic_sdk_dart when Anthropic OpenAPI spec changes.
  Fetches latest spec, compares against current, generates changelogs and prioritized
  implementation plans. Use for: (1) Checki'
---

---
name: openapi-toolkit-anthropic-dart
description: Automates updating anthropic_sdk_dart when Anthropic OpenAPI spec changes. Fetches latest spec, compares against current, generates changelogs and prioritized implementation plans. Use for: (1) Checking for API updates, (2) Generating implementation plans for spec changes, (3) Creating new models/endpoints from spec, (4) Syncing local spec with upstream. Triggers: "update api", "sync openapi", "new endpoints", "api changes", "check for updates", "update spec", "api version", "fetch spec", "compare spec", "what changed in the api", "implementation plan".
---

# OpenAPI Toolkit (anthropic_sdk_dart)

Uses shared scripts from [openapi-toolkit](../../shared/openapi-toolkit/README.md).

## Prerequisites

- `ANTHROPIC_API_KEY` environment variable set (for integration tests)
- Working directory: Repository root

## Quick Start

```bash
# Fetch latest spec
python3 .claude/shared/openapi-toolkit/scripts/fetch_spec.py \
  --config-dir .claude/skills/openapi-toolkit-anthropic-dart/config

# Analyze changes (create mode for new package)
python3 .claude/shared/openapi-toolkit/scripts/analyze_changes.py \
  --config-dir .claude/skills/openapi-toolkit-anthropic-dart/config \
  --mode create /tmp/openapi-toolkit-anthropic-dart/latest-main.yaml \
  --plan-out /tmp/implementation-plan.md

# Analyze changes (update mode for existing package)
python3 .claude/shared/openapi-toolkit/scripts/analyze_changes.py \
  --config-dir .claude/skills/openapi-toolkit-anthropic-dart/config \
  packages/anthropic_sdk_dart/specs/openapi.yaml /tmp/openapi-toolkit-anthropic-dart/latest-main.yaml \
  --format all --changelog-out /tmp/changelog.md --plan-out /tmp/plan.md

# Verify implementation
python3 .claude/shared/openapi-toolkit/scripts/verify_exports.py \
  --config-dir .claude/skills/openapi-toolkit-anthropic-dart/config

python3 .claude/shared/openapi-toolkit/scripts/verify_model_properties.py \
  --config-dir .claude/skills/openapi-toolkit-anthropic-dart/config
```

## Package-Specific References

- [Package Guide](references/package-guide.md)
- [Implementation Patterns](references/implementation-patterns.md)
- [Review Checklist](references/REVIEW_CHECKLIST.md)

## External References

- [Official Anthropic API Documentation](https://docs.anthropic.com/en/api)
- [Official Anthropic TypeScript SDK](https://github.com/anthropics/anthropic-sdk-typescript)
- [Anthropic OpenAPI Spec](https://storage.googleapis.com/stainless-sdk-openapi-specs/anthropic%2Fanthropic-a49e89deec4e00d1da490808099d66e2001531b12d8666a7f5d0b496f760440d.yml)
