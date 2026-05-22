---
name: rails-devops
description: DevOps and infrastructure specialist for Rails applications. Use when setting up Docker, CI/CD pipelines, deployment configurations, monitoring, logging, or production optimizations. Covers GitHub Actions, Docker, Kubernetes, and cloud platforms.
---

# Rails DevOps Specialist

Deploy and operate Rails applications with confidence.

## When to Use This Skill

- Docker containerization
- CI/CD pipeline setup (GitHub Actions, GitLab CI)
- Production configuration and optimization
- Database backups and migrations
- Monitoring and logging setup
- Security hardening
- Performance tuning
- Cloud deployment (AWS, Heroku, Render, Fly.io)
- Kubernetes configuration

## Docker Setup

### Production Dockerfile

```dockerfile
# Dockerfile
FROM ruby:3.3.0-alpine AS builder

# Install build dependencies
RUN apk add --no-cache \
    build-base \
    postgresql-dev \
    git \
    nodejs \
    yarn \
    tzdata

WORKDIR /app

# Install gems
COPY Gemfile Gemfile.lock ./
RUN bundle config set --local deployment 'true' && \
    bundle config set --local without 'development test' && \
    bundle install -j4 --retry 3

# Install node packages
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile --production

# Copy application
COPY . .

# Precompile assets
RUN SECRET_KEY_BASE=dummy bundle exec rails assets:precompile

# Final stage
FROM ruby:3.3.0-alpine

RUN apk add --no-cache \
    postgresql-client \
    tzdata \
    curl

WORKDIR /app

# Copy built artifacts
COPY --from=builder /usr/local/bundle /usr/local/bundle
COPY --from=builder /app /app

# Create user
RUN addgroup -g 1000 rails && \
    adduser -D -u 1000 -G rails rails && \
    chown -R rails:rails /app

USER rails

EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s \
  CMD curl -f http://localhost:3000/health || exit 1

CMD ["bundle", "exec", "puma", "-C", "config/puma.rb"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.9'

services:
  web:
    build: .
    command: bundle exec puma -C config/puma.rb
    ports:
      - "3000:3000"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      DATABASE_URL: postgres://postgres:password@db:5432/myapp_production
      REDIS_URL: redis://redis:6379/0
      RAILS_ENV: production
      SECRET_KEY_BASE: ${SECRET_KEY_BASE}
    env_file:
      - .env.production
    volumes:
      - ./storage:/app/storage
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: password
      POSTGRES_DB: myapp_production
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
    restart: unless-stopped

  solid_queue:
    build: .
    command: bundle exec rake solid_queue:start
    depends_on:
      - db
      - redis
    environment:
      DATABASE_URL: postgres://postgres:password@db:5432/myapp_production
      REDIS_URL: redis://redis:6379/0
      RAILS_ENV: production
    env_file:
      - .env.production
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

## CI/CD with GitHub Actions

### Complete CI Pipeline

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  RUBY_VERSION: '3.3.0'
  NODE_VERSION: '20'
  POSTGRES_VERSION: '15'

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: myapp_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: ${{ env.RUBY_VERSION }}
          bundler-cache: true

      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'yarn'

      - name: Install dependencies
        run: |
          bundle install --jobs 4 --retry 3
          yarn install --frozen-lockfile

      - name: Setup database
        env:
          RAILS_ENV: test
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/myapp_test
        run: |
          bundle exec rails db:create db:schema:load

      - name: Run RuboCop
        run: bundle exec rubocop --parallel

      - name: Run ERB Lint
        run: bundle exec erblint --lint-all

      - name: Run Brakeman
        run: bundle exec brakeman --no-pager --quiet

      - name: Run Bundler Audit
        run: bundle exec bundle-audit check --update

      - name: Run RSpec
        env:
          RAILS_ENV: test
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/myapp_test
          REDIS_URL: redis://localhost:6379/0
        run: |
          bundle exec rspec --format progress --format RspecJunitFormatter --out tmp/rspec.xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        if: always()
        with:
          files: ./coverage/coverage.xml

      - name: Upload test results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: test-results
          path: tmp/rspec.xml

  build:
    runs-on: ubuntu-latest
    needs: test

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ github.ref == 'refs/heads/main' }}
          tags: |
            myapp/web:latest
            myapp/web:${{ github.sha }}
          cache-from: type=registry,ref=myapp/web:buildcache
          cache-to: type=registry,ref=myapp/web:buildcache,mode=max

  deploy:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'

    steps:
      - name: Deploy to production
        run: |
          # Add your deployment command here
          echo "Deploying to production..."
```

## Production Configuration

### Environment Variables

```bash
# .env.production
RAILS_ENV=production
RAILS_LOG_TO_STDOUT=true
RAILS_SERVE_STATIC_FILES=true

# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname
DATABASE_POOL=5

# Redis
REDIS_URL=redis://redis:6379/0

# App
SECRET_KEY_BASE=your-secret-key-here
RAILS_MAX_THREADS=5
WEB_CONCURRENCY=2

# Assets
ASSET_HOST=https://cdn.example.com

# Email
SMTP_ADDRESS=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=your-sendgrid-api-key

# Monitoring
SENTRY_DSN=https://your-sentry-dsn
NEW_RELIC_LICENSE_KEY=your-newrelic-key
```

### Puma Configuration

```ruby
# config/puma.rb
max_threads_count = ENV.fetch("RAILS_MAX_THREADS", 5)
min_threads_count = ENV.fetch("RAILS_MIN_THREADS", max_threads_count)
threads min_threads_count, max_threads_count

worker_timeout 3600 if ENV.fetch("RAILS_ENV", "development") == "development"

port ENV.fetch("PORT", 3000)
environment ENV.fetch("RAILS_ENV", "development")

pidfile ENV.fetch("PIDFILE", "tmp/pids/server.pid")

workers ENV.fetch("WEB_CONCURRENCY", 2)

preload_app!

before_fork do
  ActiveRecord::Base.connection_pool.disconnect! if defined?(ActiveRecord)
end

on_worker_boot do
  ActiveRecord::Base.establish_connection if defined?(ActiveRecord)
end

plugin :tmp_restart
```

### Database Configuration

```yaml
# config/database.yml
production:
  <<: *default
  url: <%= ENV['DATABASE_URL'] %>
  pool: <%= ENV.fetch("RAILS_MAX_THREADS", 5) %>
  timeout: 5000
  reaping_frequency: 10
  connect_timeout: 2
  checkout_timeout: 5
  variables:
    statement_timeout: 30000  # 30 seconds
    lock_timeout: 5000        # 5 seconds
```

## Monitoring & Logging

### Structured Logging

```ruby
# config/environments/production.rb
config.log_level = :info
config.log_tags = [:request_id]

# JSON logging
config.logger = ActiveSupport::Logger.new(STDOUT)
config.logger.formatter = proc do |severity, time, progname, msg|
  {
    severity: severity,
    time: time.iso8601(3),
    progname: progname,
    message: msg,
    pid: Process.pid,
    host: Socket.gethostname
  }.to_json + "\n"
end
```

### Application Monitoring

```ruby
# config/initializers/sentry.rb
Sentry.init do |config|
  config.dsn = ENV['SENTRY_DSN']
  config.breadcrumbs_logger = [:active_support_logger, :http_logger]
  config.traces_sample_rate = 0.1
  config.profiles_sample_rate = 0.1

  config.before_send = lambda do |event, hint|
    # Filter sensitive data
    event.request.data.delete(:password) if event.request&.data
    event
  end
end
```

### Health Check Endpoint

```ruby
# app/controllers/health_controller.rb
class HealthController < ApplicationController
  skip_before_action :authenticate_user!

  def show
    checks = {
      database: database_check,
      redis: redis_check,
      disk_space: disk_space_check
    }

    if checks.values.all? { |status| status == :ok }
      render json: { status: 'ok', checks: checks }, status: :ok
    else
      render json: { status: 'error', checks: checks }, status: :service_unavailable
    end
  end

  private

  def database_check
    ActiveRecord::Base.connection.execute('SELECT 1')
    :ok
  rescue
    :error
  end

  def redis_check
    Redis.current.ping == 'PONG' ? :ok : :error
  rescue
    :error
  end

  def disk_space_check
    stat = Sys::Filesystem.stat('/')
    percent_used = (1 - stat.blocks_available.to_f / stat.blocks) * 100

    percent_used < 90 ? :ok : :warning
  rescue
    :error
  end
end
```

## Database Management

### Backup Script

```bash
#!/bin/bash
# bin/backup_database

set -e

BACKUP_DIR="/backups/postgresql"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/myapp_$DATE.sql.gz"

# Create backup
pg_dump $DATABASE_URL | gzip > $BACKUP_FILE

# Upload to S3
aws s3 cp $BACKUP_FILE s3://my-backups/database/

# Keep only last 30 days locally
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete

echo "Backup completed: $BACKUP_FILE"
```

### Migration Strategy

```bash
#!/bin/bash
# bin/deploy

set -e

echo "==> Running database migrations..."
bundle exec rails db:migrate

if [ $? -ne 0 ]; then
  echo "Migration failed! Rolling back..."
  bundle exec rails db:rollback
  exit 1
fi

echo "==> Precompiling assets..."
bundle exec rails assets:precompile

echo "==> Restarting application..."
if [ -f tmp/pids/server.pid ]; then
  kill -USR2 $(cat tmp/pids/server.pid)
else
  bundle exec pumactl restart
fi

echo "==> Deployment complete!"
```

## Security

### SSL/TLS Configuration

```ruby
# config/environments/production.rb
config.force_ssl = true
config.ssl_options = {
  hsts: {
    subdomains: true,
    preload: true,
    expires: 1.year
  },
  secure_cookies: true
}
```

### Rate Limiting

```ruby
# Gemfile
gem 'rack-attack'

# config/initializers/rack_attack.rb
class Rack::Attack
  # Rate limit by IP
  throttle('req/ip', limit: 300, period: 5.minutes) do |req|
    req.ip
  end

  # Protect login endpoint
  throttle('logins/ip', limit: 5, period: 20.seconds) do |req|
    req.ip if req.path == '/login' && req.post?
  end

  # Block suspicious requests
  blocklist('block bad actors') do |req|
    Rack::Attack::Allow2Ban.filter(req.ip, maxretry: 5, findtime: 10.minutes, bantime: 1.hour) do
      req.path.include?('admin') && req.get?
    end
  end
end
```

## Performance Optimization

### Database Connection Pooling

```ruby
# config/puma.rb
workers Integer(ENV.fetch("WEB_CONCURRENCY", 2))
threads_count = Integer(ENV.fetch("RAILS_MAX_THREADS", 5))

on_worker_boot do
  ActiveRecord::Base.establish_connection(
    ENV['DATABASE_URL'],
    pool: threads_count
  )
end
```

### CDN Configuration

```ruby
# config/environments/production.rb
config.action_controller.asset_host = ENV['ASSET_HOST']
config.action_controller.perform_caching = true

config.cache_store = :redis_cache_store, {
  url: ENV['REDIS_URL'],
  expires_in: 1.day,
  namespace: 'cache',
  pool_size: ENV.fetch("RAILS_MAX_THREADS", 5),
  pool_timeout: 5
}
```

## Deployment Platforms

### Heroku

```yaml
# app.json
{
  "name": "myapp",
  "stack": "heroku-22",
  "buildpacks": [
    { "url": "heroku/ruby" },
    { "url": "heroku/nodejs" }
  ],
  "addons": [
    "heroku-postgresql:standard-0",
    "heroku-redis:premium-0"
  ],
  "env": {
    "RAILS_ENV": { "value": "production" },
    "RACK_ENV": { "value": "production" }
  }
}
```

### Fly.io

```toml
# fly.toml
app = "myapp"
primary_region = "sjc"

[build]
  dockerfile = "Dockerfile"

[env]
  RAILS_ENV = "production"
  RACK_ENV = "production"

[[services]]
  internal_port = 3000
  protocol = "tcp"

  [[services.ports]]
    handlers = ["http"]
    port = 80
    force_https = true

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443

  [services.concurrency]
    type = "connections"
    hard_limit = 1000
    soft_limit = 800

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 512
```

## Best Practices

### ✅ Do

- Use Docker for consistent environments
- Implement comprehensive monitoring
- Set up automated backups
- Use environment variables for config
- Enable SSL/TLS in production
- Implement rate limiting
- Monitor application performance
- Set up proper logging
- Test deployment process in staging
- Document runbooks for common issues

### ❌ Don't

- Commit secrets to version control
- Skip database backups
- Deploy without testing
- Ignore security warnings
- Run migrations without backups
- Use root user in containers
- Expose debug endpoints in production
- Skip health checks
- Deploy during peak hours

---

**Remember**: Production environments require careful planning, monitoring, and incident response procedures. Always have rollback plans and test in staging first.

For detailed examples, see `devops-reference.md`.
