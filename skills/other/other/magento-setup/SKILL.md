---
name: magento-setup
description: Set up a Magento 2 Open Source project — installation, Composer setup, system requirements verification, and initial configuration. Use when starting a new Magento project or setting up a development environment.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
disable-model-invocation: true
---

# Magento 2 Project Setup

## Before writing code

1. **Fetch system requirements**: Fetch `https://experienceleague.adobe.com/en/docs/commerce-operations/installation-guide/system-requirements` for current PHP, MySQL, OpenSearch, Redis, and Varnish versions
2. **Fetch installation guide**: Web-search `site:experienceleague.adobe.com commerce installation guide` for step-by-step setup
3. **Check latest version**: Web-search `magento open source latest version release` for the current GA release

## What This Skill Does

Guides through complete Magento 2 environment setup:

1. **Verify system requirements** — PHP version, required extensions, MySQL/MariaDB, OpenSearch, Redis, Composer
2. **Install via Composer** — `composer create-project` from `repo.magento.com`
3. **Configure services** — database, search engine, cache backend, session storage
4. **Run installer** — `bin/magento setup:install` with all required parameters
5. **Post-install** — cron setup, developer mode, sample data (optional)

## Supported Stack (Conceptual)

- **PHP**: 8.2+ (check docs for exact supported versions)
- **Database**: MySQL 8.0+ or MariaDB 10.6+
- **Search**: OpenSearch 2.12+ (Elasticsearch deprecated)
- **Cache/Session**: Redis 7.x or Valkey 8.x
- **HTTP Cache**: Varnish 7.x
- **Message Queue**: RabbitMQ 3.13+ (optional)
- **Web Server**: Nginx 1.24+ or Apache 2.4
- **Composer**: 2.x

## Required PHP Extensions

memory_limit >= 2GB, and extensions: bcmath, ctype, curl, dom, gd, hash, iconv, intl, mbstring, openssl, pdo_mysql, simplexml, soap, spl, xsl, zip, sodium, sockets.

## Installation Pattern

```bash
# 1. Create project
composer create-project --repository-url=https://repo.magento.com/ \
    magento/project-community-edition <install-dir>

# 2. Install (with all services configured)
bin/magento setup:install \
    --base-url=<url> \
    --db-host=<host> --db-name=<name> --db-user=<user> --db-password=<pass> \
    --search-engine=opensearch --opensearch-host=<host> --opensearch-port=9200 \
    --session-save=redis --session-save-redis-host=<host> \
    --cache-backend=redis --cache-backend-redis-server=<host> \
    --admin-firstname=<first> --admin-lastname=<last> \
    --admin-email=<email> --admin-user=<user> --admin-password=<pass>

# 3. Post-install
bin/magento deploy:mode:set developer
bin/magento cron:install
bin/magento setup:upgrade
bin/magento cache:flush
```

## Development Environment Options

- **Docker**: Warden, Mark Shust's Docker Config, DDEV
- **Local**: Native PHP/MySQL/Nginx stack
- **Cloud**: Adobe Commerce Cloud (paid), custom cloud setup

Fetch the installation guide for exact CLI flags, service configuration, and file permission setup before proceeding.
