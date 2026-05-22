---
name: ci-cd-github
description: GitHub Actions CI/CD workflows for testing, building, and deploying. Use this skill when creating or modifying GitHub Actions workflows, debugging CI failures, or setting up automated pipelines.
---

# CI/CD GitHub Actions Skill

This skill provides guidance for managing GitHub Actions CI/CD workflows in the Family Plan project.

## Existing Workflows

| Workflow | File | Trigger | Purpose |
|----------|------|---------|---------|
| PHPUnit Tests | `.github/workflows/phpunit.yml` | Push/PR | Backend unit & integration tests |
| Playwright Tests | `.github/workflows/playwright.yml` | Push/PR | Frontend E2E tests |
| Mobile Tests | `.github/workflows/mobile.yml` | Push/PR | React Native tests |
| Docker Publish | `.github/workflows/docker-publish.yml` | Release | Build & push Docker images |

## Workflow Structure

### Basic PHP Test Workflow

```yaml
# .github/workflows/phpunit.yml
name: PHPUnit Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: app
          POSTGRES_PASSWORD: "!ChangeMe!"
          POSTGRES_DB: app_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.3'
          extensions: pdo_pgsql, intl
          coverage: xdebug

      - name: Get Composer Cache Directory
        id: composer-cache
        run: echo "dir=$(composer config cache-files-dir)" >> $GITHUB_OUTPUT

      - name: Cache Composer dependencies
        uses: actions/cache@v4
        with:
          path: ${{ steps.composer-cache.outputs.dir }}
          key: ${{ runner.os }}-composer-${{ hashFiles('**/composer.lock') }}
          restore-keys: ${{ runner.os }}-composer-

      - name: Install dependencies
        run: composer install --prefer-dist --no-progress

      - name: Create database schema
        run: |
          php bin/console doctrine:database:create --env=test --if-not-exists
          php bin/console doctrine:migrations:migrate --env=test --no-interaction
        env:
          DATABASE_URL: postgresql://app:!ChangeMe!@localhost:5432/app_test

      - name: Run PHPUnit
        run: vendor/bin/phpunit --coverage-clover coverage.xml
        env:
          DATABASE_URL: postgresql://app:!ChangeMe!@localhost:5432/app_test

      - name: Upload coverage report
        uses: codecov/codecov-action@v4
        with:
          files: coverage.xml
          fail_ci_if_error: false
```

### Behat Acceptance Tests

```yaml
# .github/workflows/behat.yml
name: Behat Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  behat:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: app
          POSTGRES_PASSWORD: "!ChangeMe!"
          POSTGRES_DB: app_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.3'
          extensions: pdo_pgsql, intl

      - name: Install dependencies
        run: composer install --prefer-dist --no-progress

      - name: Setup database
        run: |
          php bin/console doctrine:database:create --env=test --if-not-exists
          php bin/console doctrine:migrations:migrate --env=test --no-interaction
        env:
          DATABASE_URL: postgresql://app:!ChangeMe!@localhost:5432/app_test

      - name: Start Symfony server
        run: |
          symfony server:start --no-tls -d
        env:
          DATABASE_URL: postgresql://app:!ChangeMe!@localhost:5432/app_test

      - name: Run Behat
        run: vendor/bin/behat --format=progress
        env:
          DATABASE_URL: postgresql://app:!ChangeMe!@localhost:5432/app_test
```

### Playwright E2E Tests

```yaml
# .github/workflows/playwright.yml
name: Playwright Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 30

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install dependencies
        working-directory: frontend
        run: npm ci

      - name: Install Playwright browsers
        working-directory: frontend
        run: npx playwright install --with-deps

      - name: Start backend (Docker)
        run: |
          docker compose up -d database php nginx
          docker compose exec -T php php bin/console doctrine:migrations:migrate --no-interaction
          sleep 10

      - name: Start frontend
        working-directory: frontend
        run: npm start &
        env:
          REACT_APP_API_URL: http://localhost:8080

      - name: Wait for frontend
        run: npx wait-on http://localhost:3000

      - name: Run Playwright tests
        working-directory: frontend
        run: npx playwright test

      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: frontend/playwright-report/
          retention-days: 30
```

### Mobile Tests (React Native)

```yaml
# .github/workflows/mobile.yml
name: Mobile Tests

on:
  push:
    branches: [main, develop]
    paths:
      - 'mobile/**'
  pull_request:
    branches: [main]
    paths:
      - 'mobile/**'

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: mobile/package-lock.json

      - name: Install dependencies
        working-directory: mobile
        run: npm ci

      - name: Run linter
        working-directory: mobile
        run: npm run lint

      - name: Run TypeScript check
        working-directory: mobile
        run: npx tsc --noEmit

      - name: Run tests
        working-directory: mobile
        run: npm test -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: mobile/coverage/lcov.info
          flags: mobile
```

### Code Quality Workflow

```yaml
# .github/workflows/quality.yml
name: Code Quality

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  php-quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.3'
          tools: phpstan, php-cs-fixer

      - name: Install dependencies
        run: composer install --prefer-dist --no-progress

      - name: Run PHP-CS-Fixer
        run: vendor/bin/php-cs-fixer fix --dry-run --diff

      - name: Run PHPStan
        run: vendor/bin/phpstan analyse src tests --level=8

  frontend-quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install dependencies
        working-directory: frontend
        run: npm ci

      - name: Run ESLint
        working-directory: frontend
        run: npm run lint
```

## Matrix Testing

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        php-version: ['8.2', '8.3']
        postgres-version: ['15', '16']
      fail-fast: false

    services:
      postgres:
        image: postgres:${{ matrix.postgres-version }}-alpine
        # ...

    steps:
      - uses: shivammathur/setup-php@v2
        with:
          php-version: ${{ matrix.php-version }}
```

## Caching Strategies

```yaml
# Composer cache
- uses: actions/cache@v4
  with:
    path: vendor
    key: ${{ runner.os }}-composer-${{ hashFiles('**/composer.lock') }}
    restore-keys: ${{ runner.os }}-composer-

# NPM cache
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: ${{ runner.os }}-node-

# Playwright browsers cache
- uses: actions/cache@v4
  with:
    path: ~/.cache/ms-playwright
    key: ${{ runner.os }}-playwright-${{ hashFiles('**/package-lock.json') }}
```

## Secrets Management

Required secrets in GitHub repository settings:

| Secret | Description |
|--------|-------------|
| `CODECOV_TOKEN` | Codecov upload token |
| `DOCKER_USERNAME` | Docker Hub username |
| `DOCKER_PASSWORD` | Docker Hub password/token |

```yaml
- name: Login to Docker Hub
  uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKER_USERNAME }}
    password: ${{ secrets.DOCKER_PASSWORD }}
```

## Debugging CI Failures

### Common Issues

1. **Database connection failures**
   - Check service health check options
   - Verify DATABASE_URL environment variable
   - Ensure migrations run before tests

2. **Playwright failures**
   - Check if backend is fully ready before tests
   - Use `wait-on` for frontend readiness
   - Review screenshots/videos in artifacts

3. **Cache misses**
   - Verify cache key patterns
   - Check if lock files are committed

### Debug Steps

```yaml
- name: Debug info
  run: |
    php -v
    composer --version
    env | grep -E '^(DATABASE|APP)' | sort
```

## Best Practices

1. **Use job dependencies** - `needs: [build]` for sequential jobs
2. **Cache dependencies** - Faster builds with proper caching
3. **Upload artifacts** - Save test reports and screenshots
4. **Use matrix builds** - Test multiple PHP/Node versions
5. **Set timeouts** - Prevent hanging jobs
6. **Use reusable workflows** - DRY workflow definitions
7. **Branch protection** - Require CI to pass before merge
