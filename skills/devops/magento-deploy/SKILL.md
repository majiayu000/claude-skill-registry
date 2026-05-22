---
name: magento-deploy
description: Deploy Magento 2 — deployment modes, static content deployment, DI compilation, CLI commands, zero-downtime strategies, and CI/CD pipeline setup. Use when preparing for production deployment or building deployment automation.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# Magento 2 Deployment & CLI

## Before writing code

**Fetch live docs**:
1. Fetch `https://experienceleague.adobe.com/en/docs/commerce-operations/configuration-guide/cli/set-mode` for deployment modes
2. Fetch `https://experienceleague.adobe.com/en/docs/commerce-operations/configuration-guide/cli/static-view/static-view-file-deployment` for static content deploy
3. Web-search `magento 2 zero downtime deployment` for zero-downtime strategies

## Deployment Modes

| Mode | Errors | Static Files | DI Compilation | Use Case |
|------|--------|-------------|----------------|----------|
| **Developer** | Displayed | Generated on demand | Automatic | Local development |
| **Production** | Logged only | Pre-deployed | Pre-compiled | Live site |
| **Default** | Not displayed | On demand | Not optimized | Initial install |

```bash
bin/magento deploy:mode:show
bin/magento deploy:mode:set production
bin/magento deploy:mode:set developer
```

## Production Deployment Steps

### Standard Sequence

```bash
# 1. Enable maintenance mode
bin/magento maintenance:enable

# 2. Pull latest code (git pull, composer install)
composer install --no-dev --optimize-autoloader

# 3. Run setup upgrade (applies db_schema changes and patches)
bin/magento setup:upgrade

# 4. Compile DI (generates interceptors, factories, proxies)
bin/magento setup:di:compile

# 5. Deploy static content (CSS, JS, images, templates)
bin/magento setup:static-content:deploy en_US --jobs=4

# 6. Flush cache
bin/magento cache:flush

# 7. Disable maintenance mode
bin/magento maintenance:disable
```

### Static Content Deploy Strategies

- **quick** — minimizes deployment time by reusing files across locales (default in 2.4+)
- **compact** — minimizes disk space
- **standard** — full deployment
- Flags: `--exclude-theme`, `--no-html-minify`, `--jobs=N` for parallelism

## Zero-Downtime Deployment

### Pipeline Deployment

Build and deploy on separate systems:
1. **Build server**: `setup:di:compile` + `setup:static-content:deploy`
2. **Transfer** artifacts to production
3. **Production**: `setup:upgrade --keep-generated` (no recompilation)

### Blue-Green Deployment

Two identical environments with load balancer switching:
- Native support since 2.4.4: `deployment/blue_green/enabled` in `app/etc/env.php`
- Deploy to inactive environment, test, switch traffic
- Instant rollback by switching back

### Symlink Switching

- Deploy to versioned directories (`releases/20260214/`)
- Switch `current` symlink to new release
- Shared directories for `var/`, `pub/media/`, `app/etc/env.php`
- Tools: Deployer (deployer.org), Capistrano, custom scripts

## Essential CLI Commands

### Module Management
```bash
bin/magento module:enable VendorName_ModuleName
bin/magento module:disable VendorName_ModuleName
bin/magento module:status
```

### Cache Management
```bash
bin/magento cache:clean          # Clean invalidated cache types
bin/magento cache:flush          # Flush all cache storage
bin/magento cache:status         # Show cache type status
bin/magento cache:enable <type>
bin/magento cache:disable <type>
```

### Indexer Management
```bash
bin/magento indexer:reindex
bin/magento indexer:status
bin/magento indexer:set-mode schedule
```

### Cron
```bash
bin/magento cron:run
bin/magento cron:install
```

### Admin
```bash
bin/magento admin:user:create
bin/magento admin:user:unlock <username>
```

### Development
```bash
bin/magento dev:profiler:enable
bin/magento dev:template-hints:enable
bin/magento setup:config:set --<option>=<value>
```

## CI/CD Pipeline Pattern

1. **Lint/Static Analysis**: PHP_CodeSniffer, PHPStan, Magento coding standard
2. **Unit Tests**: `vendor/bin/phpunit -c dev/tests/unit/phpunit.xml.dist`
3. **Build**: `composer install --no-dev`, `setup:di:compile`, `setup:static-content:deploy`
4. **Integration Tests** (optional, slow): against test database
5. **Deploy**: transfer artifacts, `setup:upgrade`, cache flush
6. **Smoke Test**: verify critical pages load

## Best Practices

- Never run `setup:di:compile` or `setup:static-content:deploy` on production during traffic
- Use pipeline deployment for zero-downtime
- Use `--jobs=N` for parallel static content deployment
- Automate deployment — manual steps are error-prone
- Always take database backups before `setup:upgrade`
- Test deployment on staging before production

Fetch the deployment documentation for exact CLI options, mode-switching requirements, and pipeline deployment configuration before deploying.
