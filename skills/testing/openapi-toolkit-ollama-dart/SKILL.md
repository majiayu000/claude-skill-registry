---
name: openapi-toolkit-ollama-dart
description: 'Automates updating ollama_dart when Ollama OpenAPI spec changes. Fetches
  latest spec, compares against current, generates changelogs and prioritized implementation
  plans. Use for: (1) Checking for API'
---

---
name: openapi-toolkit-ollama-dart
description: Automates updating ollama_dart when Ollama OpenAPI spec changes. Fetches latest spec, compares against current, generates changelogs and prioritized implementation plans. Use for: (1) Checking for API updates, (2) Generating implementation plans for spec changes, (3) Creating new models/endpoints from spec, (4) Syncing local spec with upstream. Triggers: "update api", "sync openapi", "new endpoints", "api changes", "check for updates", "update spec", "api version", "fetch spec", "compare spec", "what changed in the api", "implementation plan".
---

# OpenAPI Toolkit (ollama_dart)

Uses shared scripts from [openapi-toolkit](../../shared/openapi-toolkit/README.md).

## Prerequisites

- Working directory: Repository root

## Quick Start

```bash
# Fetch latest spec
python3 .claude/shared/openapi-toolkit/scripts/fetch_spec.py \
  --config-dir .claude/skills/openapi-toolkit-ollama-dart/config

# Analyze changes (create mode for new package)
python3 .claude/shared/openapi-toolkit/scripts/analyze_changes.py \
  --config-dir .claude/skills/openapi-toolkit-ollama-dart/config \
  --mode create /tmp/openapi-toolkit-ollama-dart/latest-main.json \
  --plan-out /tmp/implementation-plan.md

# Analyze changes (update mode for existing package)
python3 .claude/shared/openapi-toolkit/scripts/analyze_changes.py \
  --config-dir .claude/skills/openapi-toolkit-ollama-dart/config \
  packages/ollama_dart/specs/openapi.json /tmp/openapi-toolkit-ollama-dart/latest-main.json \
  --format all --changelog-out /tmp/changelog.md --plan-out /tmp/plan.md

# Verify implementation
python3 .claude/shared/openapi-toolkit/scripts/verify_exports.py \
  --config-dir .claude/skills/openapi-toolkit-ollama-dart/config

python3 .claude/shared/openapi-toolkit/scripts/verify_model_properties.py \
  --config-dir .claude/skills/openapi-toolkit-ollama-dart/config
```

## Package-Specific References

- [Package Guide](references/package-guide.md)
- [Implementation Patterns](references/implementation-patterns.md)
- [Review Checklist](references/REVIEW_CHECKLIST.md)

## External References

- [Official Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Official Ollama JS Client](https://github.com/ollama/ollama-js)
- [Ollama OpenAPI Spec](https://raw.githubusercontent.com/ollama/ollama/refs/heads/main/docs/openapi.yaml)
