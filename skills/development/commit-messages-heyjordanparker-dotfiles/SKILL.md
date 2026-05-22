---
name: commit-messages
description: MANDATORY when writing commit messages. Structures commits with type prefix, what+why body, and architectural file tree.
---

# Commit Messages

**This skill is mandatory.** Follow this format for all commits.

## Format

```
<type>: <subject - what changed, all changes summarized>

<what changed + why, combined naturally>

<additional context if multi-file or complex>:
- <change 1>
- <change 2>

<file tree>
├── path/to/modified.ts*   <- brief annotation
└── path/to/context.ts
```

## Anatomy

```
feat: add auto-migrations to deploy pipeline

Migrations now run automatically on every deploy via Trellis hook.
Safe because symlink switch happens AFTER migrations succeed.

deploy/
├── hooks/build-after.yml*    <- run migrations post-deploy
├── hooks/deploy-prepare.yml
└── docs/migrations.md*       <- design rules added
```

## Rules

1. **Type prefix:** `feat`, `fix`, `chore`, `refactor`, `docs`, `test`
2. **Subject:** lowercase after colon, <72 chars, summarizes all changes
3. **Body:** what+why woven together (not separate sections)
4. **File tree:** at end, show modified (*) and relevant context files
5. **No self-reference:** never "I", "we", "Claude"
6. **Bullets:** for multi-concern commits, group by area

## Examples

### Single-concern fix

```
fix: prevent cron ping pileup when requests take longer than interval

WordPress wp-cron.php uses ignore_user_abort(true), so PHP keeps
processing after client timeout. With 10s interval and 5s timeout,
requests piled up. Now skips ping if previous request is in flight.

app/
├── Services/CronPing.php*    <- added in-flight check
└── config/schedule.php       <- interval config lives here
```

### Multi-concern feature

```
feat: add Matomo configurator, 1Password secrets, and security hardening

Matomo:
- MatomoConfigurator with MaxMind GeoIP download
- Patches to remove newsletter and update nags

Secrets:
- 1Password integration via .vault_pass
- `bun secrets` command for local env vars

app/
├── Configurators/
│   └── MatomoConfigurator.php*   <- new configurator
├── Commands/SecretsCommand.php*  <- bun secrets
├── .vault_pass*                  <- 1Password integration
└── trellis/
    └── group_vars/all/vault.yml* <- encrypted secrets
```

### Minimal (trivial changes)

```
chore: update aws-sdk-php to fix security advisory

composer.lock*
```

## Anti-patterns

- `Completely turned off cors` → no type, no why
- `Fixed stuff` → vague
- `I added the feature` → self-reference
- No file tree for multi-file changes
