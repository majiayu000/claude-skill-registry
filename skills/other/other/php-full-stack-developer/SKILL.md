---
name: php-full-stack-developer
description: A senior PHP/Laravel full-stack developer skill. Use for backend/frontend/DB/devops/CI work, debugging, refactors, migrations, API work, and anything that could affect security, data integrity, API contracts, performance, or deployment.
---

# PHP Full-Stack Developer (Senior)

## Trigger Conditions

Use this skill when:
- The user requests engineering work: backend/frontend/DB/devops/CI, debugging, refactors, migrations, API work.
- The work could affect security, data integrity, API contracts, performance, or deployment.
- There is uncertainty, contradictions, or multiple valid approaches.

## Prompting Principles (Senior Clarity)

- Start with **Pre-Flight**: define goal, acceptance criteria, risks, constraints, verification.
- Ask only the **minimum questions** that prevent expensive rework (auth/data/contracts/env).
- Prefer explicit contracts over "magic": payload shape, errors, pagination, idempotency.
- Prefer reversible changes and staged rollout for risky work.
- Always produce "How to test" steps.

## Stop-Work Rules (quick gates)

Stop and confirm with user if:
- Auth/authz rules are unclear for protected resources.
- DB change is destructive or constraints are unknown.
- API/UI contract change has unknown consumers.
- PHP/framework/DB versions are unknown for critical work.
- Rollback plan is missing for production changes.

## Laravel Specifics

### Deploy checklist (zero-downtime)
```bash
php artisan down --retry=60
git pull origin main
composer install --no-dev --optimize-autoloader
php artisan migrate --force
php artisan config:cache
php artisan route:cache
php artisan view:cache
php artisan queue:restart
php artisan up
```

### Common artisan commands
```bash
php artisan make:model ModelName -m        # Model + migration
php artisan make:controller NameController --resource
php artisan make:job ProcessSomething
php artisan make:event / make:listener
php artisan make:command CustomCommand
php artisan horizon:status
php artisan horizon:terminate
php artisan queue:work --queue=default,high
php artisan tinker
php artisan test --parallel
```

### Queue management
```bash
php artisan queue:work redis --queue=high,default --tries=3 --timeout=90
php artisan queue:failed
php artisan queue:retry all
php artisan queue:flush
```

### Database
```bash
php artisan migrate:status
php artisan migrate --pretend        # preview SQL
php artisan migrate:rollback --step=1
php artisan db:seed --class=UserSeeder
```

## Security Checklist

- Input validation: FormRequest classes, not inline
- SQL: Always Eloquent/query builder, never raw user input
- Auth: middleware groups, `can()` policies
- File uploads: validate MIME, store outside webroot
- Secrets: `.env` only, never in code or logs
- CORS: configured per-env
- Rate limiting: `throttle:` middleware on public APIs

## Performance Patterns

- N+1 queries: `with()` eager loading
- Cache heavy queries: `Cache::remember()`
- Queue slow work: anything > 500ms
- Pagination: `paginate()` not `get()` on large tables
- Indexes: add for all FK columns and frequent WHERE clauses

## Testing

```bash
php artisan test
php artisan test --filter TestClassName
php artisan test --parallel --processes=4
php artisan dusk                          # browser tests
php artisan dusk --filter CriticalTest
```
