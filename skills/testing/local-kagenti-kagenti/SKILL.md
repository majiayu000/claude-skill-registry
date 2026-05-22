---
name: local
description: Local development and testing workflows for Kagenti. Full test suites for Kind and HyperShift.
---

# Local Development Skills

Skills for local development and testing workflows.

## Available Sub-Skills

| Skill | Description |
|-------|-------------|
| `local:testing` | Detailed local testing guide with Kind |
| `local:full-test` | Full end-to-end test workflows |

## Quick Start

### Kind (Local Docker)

```bash
# Full test workflow
./.github/scripts/local-setup/kind-full-test.sh
```

### HyperShift (AWS)

```bash
# Full test workflow (keeps cluster)
./.github/scripts/local-setup/hypershift-full-test.sh --skip-cluster-destroy
```

## Show Services

```bash
# Show all deployed services and access URLs
./.github/scripts/local-setup/show-services.sh
```

## Development Cycle

1. Make code changes
2. Run `kind-full-test.sh` or individual scripts
3. Check logs with `kubectl logs`
4. Access UI at http://kagenti-ui.localtest.me:8080

## Related Documentation

- `.github/scripts/local-setup/README.md`
- `.github/scripts/kind/README.md`
