---
name: PHP Tooling
description: PHP ecosystem tooling, dependency management, and static analysis.
metadata:
  labels: [php, composer, toolchain, static-analysis]
  triggers:
    files: ['composer.json']
    keywords: [composer, lock, phpstan, xdebug]
---

# PHP Tooling

## **Priority: P2 (MEDIUM)**

## Structure

```text
project/
├── composer.json
├── phpstan.neon
└── .php-cs-fixer.php
```

## Implementation Guidelines

- **Composer Lock**: Commit `composer.lock` for environment parity.
- **PSR-4**: Strictly map namespaces to `src/` and `tests/`.
- **Static Analysis**: Integrate **PHPStan** (level 5+) in CI.
- **Linting**: Automate PSR-12 enforcement via **PHP CS Fixer**.
- **Debugging**: Use **Xdebug** for profiling; avoid `var_dump`.
- **Scripts**: Define `lint`, `analyze`, `test` in `composer.json`.

## Anti-Patterns

- **Manual Requires**: **No Manual Require**: Rely on Composer autoload.
- **Blind Updates**: **No Blind Updating**: Review `composer.lock` diffs.
- **Production Debug**: **No Prod Xdebug**: Disable debugging in live env.
- **Vendor Commits**: **No Vendor Check-in**: Exclude `vendor/` from git.

## Code

```json
{
  "autoload": {
    "psr-4": { "App\\": "src/" }
  },
  "scripts": {
    "analyze": "phpstan analyze"
  }
}
```
