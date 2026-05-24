---
name: php-modernization
description: "Use when modernizing PHP code: PHP 8.1-8.5 features, PSR/PHP-FIG/PER-CS compliance, PHPStan/Rector/PHP-CS-Fixer/PHPat tooling, DTOs/enums/readonly/property hooks, type safety. Triggers: PHP modernization, type safety, PHPStan, Rector, PHP-CS-Fixer, enum, DTO, readonly, strict_types, property hooks, PHP 8.4, PHP 8.5."
license: "(MIT AND CC-BY-SA-4.0)"
compatibility: "Requires php 8.1+, composer."
metadata:
  version: "1.17.1"
  repository: "https://github.com/netresearch/php-modernization-skill"
  author: "Netresearch DTT GmbH"
allowed-tools:
  - "Bash(php:*)"
  - "Bash(composer:*)"
  - "Bash(uv:*)"
  - "Bash(vendor/bin/*)"
  - "Bash(.Build/bin/*)"
  - "Read"
  - "Write"
  - "Glob"
  - "Grep"
---

# PHP Modernization

## Agent contract

1. **Discover**: `uv run ${CLAUDE_SKILL_DIR}/scripts/introspect.py` (cheap), or `verify_php_project.py --summary` (full, with `agent_actions[]`).
2. **Drill**: `... --check PM-XX` per finding. Full output when triaging >3.
3. **Apply**: `uv run ${CLAUDE_SKILL_DIR}/scripts/modernize_loop.py --mode dry-run`. Review transcript before applying.
4. **References**: load on demand; do not pre-load.

## Reference routing

| Need | Read |
|---|---|
| PHP 8.0-8.3 baseline | `references/php8-features.md` |
| PHP 8.4 | `references/php-8.4.md` |
| PHP 8.5 | `references/php-8.5.md` |
| PSR / PER-CS | `references/psr-per-compliance.md` |
| PHPStan config | `references/phpstan-compliance.md` |
| Static analysis | `references/static-analysis-tools.md` |
| PHP-CS-Fixer deprecations | `references/php-cs-fixer-deprecations.md` |
| DTOs / VOs / inputs | `references/type-safety.md`, `references/request-dtos.md` |
| Adapter / registry | `references/adapter-registry-pattern.md` |
| Multi-version compat | `references/multi-version-adapters.md` |
| Symfony patterns | `references/symfony-patterns.md` |
| PSR-15 middleware | `references/psr15-middleware-architecture.md` |
| Doctrine edges | `references/doctrine-modernization-edges.md` |
| API Platform | `references/api-platform-edges.md` |
| Immutability | `references/immutability-boundaries.md` |
| Contracts & invariants | `references/contracts-and-invariants.md` |
| Mutation testing | `references/mutation-testing.md` |
| Migration planning | `references/migration-strategies.md` |
| PHPUnit 12→13, mock vs stub | `references/phpunit-modernization.md` |
| Multi-agent dispatch hazards | `references/multi-agent-pitfalls.md` |

## Hard guardrails

- Never apply `readonly` to Doctrine entities or mapped-superclasses (embeddables: see `references/doctrine-modernization-edges.md`).
- Never run Rector without `--dry-run`. Invoke `vendor/bin/rector` directly — composer script aliases can drop `--`-forwarded flags depending on configuration.
- Never raise PHPStan level without regenerating + committing the baseline. Shrink, never delete.
- Never apply blanket `final` to mock targets or extension points without confirmation.
- Never edit `@generated` files or files under `var/cache/`, `vendor/`, `node_modules/`, `.Build/`.
- Never `git checkout --` files outside your scope in shared trees — use `git stash` / `git diff`.
- Never trust a warm PHPStan cache after vendor change: `rm -rf /tmp/phpstan-* var/cache/phpstan` first.
- Never mass-substitute `createMock` → `createStub` — promote to `expects(...)->method(...)->with(...)`.

## Migration checklist

- [ ] `declare(strict_types=1)` everywhere
- [ ] `@PER-CS`, no deprecated aliases
- [ ] PHPStan ≥9 (`treatPhpDocTypesAsCertain: false`); 10 for new
- [ ] PHPat for layer boundaries
- [ ] Return + parameter types on all methods
- [ ] DTOs over arrays; backed enums over constants
- [ ] PSR interfaces in type-hints
- [ ] `#[Override]` (8.3+), `#[SensitiveParameter]` (8.2+), typed constants (8.3+)
- [ ] readonly on DTOs/VOs/events only
- [ ] Property hooks (8.4); `array_find/any/all` (8.4); pipe `|>` (8.5)
- [ ] PHPUnit 12+: stubs use `createStub`, mocks `createMock` + `expects` (no `self::any()` in 13)
- [ ] Rector `withComposerBased(symfony: true)` (per-version `SymfonySetList::SYMFONY_*` are `@deprecated`)
