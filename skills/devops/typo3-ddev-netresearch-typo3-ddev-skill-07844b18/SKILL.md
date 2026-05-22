---
name: typo3-ddev
description: "Agent Skill: DDEV setup for TYPO3 extension development. Use when setting up local dev environment or multi-version testing (11.5/12.4/13.4/14.0). By Netresearch."
---

# TYPO3 DDEV Setup Skill

Automates DDEV environment for TYPO3 extension development with multi-version testing.

## When to Use

- Setting up DDEV for a TYPO3 extension project
- Testing extension across multiple TYPO3 versions
- Quick development environment spin-up

## Container Priority

**Always check for existing containers first:**

1. Check `.ddev/` exists → use `ddev exec`
2. Check `docker-compose.yml` exists → use `docker compose exec`
3. Only use system tools if no container environment

> **Critical**: Use the project's configured PHP version, not system PHP.

## Quick Start

```bash
scripts/validate-prerequisites.sh    # Check Docker, DDEV
ddev start
ddev install-all                     # All versions (11/12/13/14)
ddev install-v13                     # Single version
```

## Access URLs

| Environment | URL |
|-------------|-----|
| TYPO3 v13 | `https://v13.{sitename}.ddev.site/typo3/` |
| Docs | `https://docs.{sitename}.ddev.site/` |

**Credentials**: admin / Joh316!

## Generated Files

Copy templates from `assets/templates/` to project's `.ddev/`:

```
.ddev/
├── config.yaml
├── docker-compose.web.yaml
├── apache/apache-site.conf
├── index.html.netresearch.template  (for netresearch/* packages)
├── index.html.typo3.template        (for all other packages)
└── commands/web/install-v{11,12,13,14}
```

## Optional Commands

```bash
ddev generate-makefile    # Creates make up/test/lint/ci
ddev generate-index       # Overview dashboard
ddev docs                 # Render Documentation/*.rst
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Database exists | `ddev mysql -e "DROP DATABASE v13; CREATE DATABASE v13;"` |
| Extension not appearing | `ddev exec -d /var/www/html/v13 vendor/bin/typo3 cache:flush` |

## References

| Topic | File |
|-------|------|
| Prerequisites | `references/prerequisites-validation.md` |
| Quick start | `references/quickstart.md` |
| Advanced options | `references/advanced-options.md` |
| Landing page templates | `references/index-page-generation.md` |
| Windows fixes | `references/windows-fixes.md` |
| Troubleshooting | `references/troubleshooting.md` |
| PHP version management | `references/0003-php-version-management.md` |

---

> **Contributing:** https://github.com/netresearch/typo3-ddev-skill
