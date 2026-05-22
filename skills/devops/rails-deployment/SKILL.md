---
name: rails-deployment
description: Deploy Rails applications to production using Kamal, Docker, and modern deployment strategies. Covers zero-downtime deployments, environment management, database migrations, SSL/TLS, and production configurations.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Rails Deployment with Kamal

Deploy Rails 8 applications to production using Kamal for zero-downtime Docker deployments. Covers Kamal configuration, Docker setup, environment secrets, database migrations, SSL certificates, and production best practices.

<when-to-use>
- Setting up new Rails application for production deployment
- Deploying with Kamal to VPS (DigitalOcean, Hetzner, AWS EC2)
- Configuring Docker for Rails applications
- Managing environment variables and secrets
- Running database migrations in production
- Setting up zero-downtime deployments
- Configuring SSL/TLS certificates
- Managing multiple environments (staging, production)
</when-to-use>

<benefits>
- **Zero-Downtime** - Rolling deployments with health checks
- **Simple Setup** - SSH-based deployment, no complex orchestration
- **Docker Native** - Consistent environments from dev to production
- **Built-in SSL** - Automatic Let's Encrypt certificate management
- **Fast Deployments** - Optimized Docker layer caching
- **Rollback Support** - Easy rollback to previous versions
- **Multi-Server** - Deploy to multiple servers with load balancing
</benefits>

<verification-checklist>
Before deploying to production:
- ✅ Kamal configuration file (config/deploy.yml) properly configured
- ✅ Dockerfile optimized with multi-stage build
- ✅ Environment secrets set up (.env, Rails credentials)
- ✅ Database configured and migrations ready
- ✅ SSL certificates configured (Let's Encrypt or custom)
- ✅ Health check endpoint responding
- ✅ Asset precompilation working in Docker
- ✅ Background jobs (Solid Queue) configured
- ✅ Monitoring and logging set up
</verification-checklist>

<standards>
- Use Kamal for deployments (included in Rails 8)
- Multi-stage Dockerfile for optimized images
- Store secrets in Rails credentials or environment variables
- Run database migrations before deployment with --skip-push
- Use health checks for zero-downtime deployments
- Configure SSL with Let's Encrypt or custom certificates
- Set up log aggregation (stdout/stderr)
- Use Docker registry for image caching (Docker Hub, GitHub Container Registry)
- Configure proper resource limits in Docker
- Monitor application health and performance
</standards>

---

## Kamal Overview

Kamal (formerly MRSK) is a deployment tool for Rails 8 that uses Docker and SSH to deploy applications to any server. No Kubernetes, no complex orchestration - just simple, reliable deployments.

**Key Features:**
- Zero-downtime deployments with health checks
- Automatic SSL with Let's Encrypt
- Multi-server deployments
- Rolling restarts
- Easy rollbacks
- Built-in load balancing with Traefik

---

## Quick Start

### 1. Install Kamal

```bash
# Kamal comes with Rails 8
gem install kamal

# Verify installation
kamal version
```

### 2. Initialize Kamal

```bash
# Generate Kamal configuration files
kamal init

# Creates:
# - config/deploy.yml        # Main configuration
# - .env.erb                  # Environment template
# - .kamal/                   # Kamal directory
```

### 3. Configure Server

```yaml
# config/deploy.yml
service: my-blog-app
image: your-username/my-blog-app

servers:
  web:
    hosts:
      - 192.168.1.100  # Your server IP
    labels:
      traefik.http.routers.my-blog-app.rule: Host(`example.com`)
      traefik.http.routers.my-blog-app-secure.entrypoints: websecure
      traefik.http.routers.my-blog-app-secure.rule: Host(`example.com`)
      traefik.http.routers.my-blog-app-secure.tls: true
      traefik.http.routers.my-blog-app-secure.tls.certresolver: letsencrypt

registry:
  username: your-username
  password:
    - KAMAL_REGISTRY_PASSWORD

env:
  secret:
    - RAILS_MASTER_KEY
  clear:
    RAILS_ENV: production
    RAILS_LOG_TO_STDOUT: true

builder:
  multiarch: false
```

### 4. Setup Server

```bash
# Install Docker on remote server
kamal server bootstrap

# Verify setup
kamal setup
```

### 5. Deploy

```bash
# First deployment
kamal deploy

# Subsequent deployments
kamal deploy
```

---

## Code Examples & Patterns

For detailed deployment patterns and examples, see **[examples.md](examples.md)**.

### Pattern Categories

**examples.md contains:**
- **Kamal Configuration** - Complete deploy.yml examples for various setups
- **Docker Configuration** - Multi-stage Dockerfile optimization
- **Environment Management** - Secrets, credentials, environment variables
- **Database Migrations** - Safe migration strategies in production
- **SSL/TLS Setup** - Let's Encrypt and custom certificates
- **Multi-Server Deployment** - Load balancing across servers
- **Background Jobs** - Deploying Solid Queue workers
- **Health Checks** - Endpoint configuration for zero-downtime
- **Rollback Procedures** - Recovering from failed deployments
- **Monitoring & Logging** - Production observability setup
- **CI/CD Integration** - GitHub Actions deployment workflows

Refer to examples.md for complete code examples.

---

## Kamal Commands

### Deployment Commands

```bash
# Initial setup (first time only)
kamal setup

# Deploy application
kamal deploy

# Deploy without building new image
kamal deploy --skip-push

# Run migrations before deployment
kamal deploy --skip-push
kamal app exec "bin/rails db:migrate"
```

### Application Management

```bash
# Restart application
kamal app restart

# Stop application
kamal app stop

# Start application
kamal app start

# View application logs
kamal app logs -f

# Execute command in container
kamal app exec "bin/rails console"
kamal app exec "bin/rails db:migrate:status"
```

### Rollback

```bash
# List versions
kamal app version

# Rollback to previous version
kamal rollback [VERSION]
```

### Server Management

```bash
# SSH into server
kamal app exec --interactive bash

# View Docker containers
kamal app containers

# View server details
kamal server details
```

---

## Dockerfile for Rails

### Multi-Stage Dockerfile

Rails 8 includes an optimized Dockerfile by default:

```dockerfile
# Dockerfile (Rails 8 default, optimized)
ARG RUBY_VERSION=3.4.7
FROM ruby:$RUBY_VERSION-slim AS base

WORKDIR /rails

RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y \
    curl libjemalloc2 libvips sqlite3 && \
    rm -rf /var/lib/apt/lists /var/cache/apt/archives

ENV RAILS_ENV="production" \
    BUNDLE_DEPLOYMENT="1" \
    BUNDLE_PATH="/usr/local/bundle" \
    BUNDLE_WITHOUT="development:test"

FROM base AS build

RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y \
    build-essential git pkg-config && \
    rm -rf /var/lib/apt/lists /var/cache/apt/archives

COPY Gemfile Gemfile.lock ./
RUN bundle install && \
    rm -rf ~/.bundle/ "${BUNDLE_PATH}"/ruby/*/cache "${BUNDLE_PATH}"/ruby/*/bundler/gems/*/.git

COPY . .

RUN bundle exec bootsnap precompile --gemfile app/ lib/
RUN ./bin/rails assets:precompile

FROM base

COPY --from=build "${BUNDLE_PATH}" "${BUNDLE_PATH}"
COPY --from=build /rails /rails

RUN groupadd --system --gid 1000 rails && \
    useradd rails --uid 1000 --gid 1000 --create-home --shell /bin/bash && \
    chown -R 1000:1000 db log storage tmp
USER 1000:1000

ENTRYPOINT ["/rails/bin/docker-entrypoint"]

EXPOSE 3000
CMD ["./bin/thrust", "./bin/rails", "server"]
```

---

## Environment Management

### Rails Credentials

```bash
# Edit production credentials
EDITOR=nano rails credentials:edit --environment production

# Generates config/credentials/production.yml.enc
# and config/credentials/production.key
```

```yaml
# config/credentials/production.yml.enc (encrypted)
secret_key_base: <generated>
database:
  password: <db_password>
smtp:
  username: <smtp_user>
  password: <smtp_pass>
```

### Environment Variables

```ruby
# .env (not committed to git, for local deployment)
KAMAL_REGISTRY_PASSWORD=<docker_hub_password>
RAILS_MASTER_KEY=<from config/credentials/production.key>
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

---

## Database Migrations

### Safe Migration Strategy

```bash
# 1. Deploy without running migrations
kamal deploy --skip-push

# 2. Run migrations separately
kamal app exec "bin/rails db:migrate"

# 3. Restart application
kamal app restart
```

### Pre-Deployment Checks

```bash
# Check migration status before deploying
kamal app exec "bin/rails db:migrate:status"

# Run migrations in a transaction
kamal app exec "bin/rails db:migrate"

# Verify migration success
kamal app exec "bin/rails db:version"
```

---

<testing>

## Testing Deployment

### Local Docker Testing

```bash
# Build Docker image locally
docker build -t my-app .

# Run container locally
docker run -p 3000:3000 \
  -e RAILS_MASTER_KEY=<key> \
  -e DATABASE_URL=<url> \
  my-app

# Test in browser
open http://localhost:3000
```

### Staging Environment

```yaml
# config/deploy.staging.yml
service: my-blog-app-staging
image: your-username/my-blog-app

servers:
  web:
    hosts:
      - staging.example.com

env:
  secret:
    - RAILS_MASTER_KEY
  clear:
    RAILS_ENV: staging
```

```bash
# Deploy to staging
kamal deploy -c config/deploy.staging.yml
```

</testing>

---

<related-skills>
- rails-models - Database setup and migrations
- rails-jobs - Background job configuration for production
- rails-api - API deployment considerations
- rails-debugging - Production debugging and monitoring
</related-skills>

<resources>

**Official Documentation:**
- [Kamal Documentation](https://kamal-deploy.org/) - Official Kamal guide
- [Docker Documentation](https://docs.docker.com/) - Docker reference
- [Rails Deployment Guide](https://guides.rubyonrails.org/configuring.html#running-in-production) - Rails production config

**Deployment Platforms:**
- [DigitalOcean](https://www.digitalocean.com/) - Simple VPS hosting
- [Hetzner](https://www.hetzner.com/) - Cost-effective VPS
- [AWS EC2](https://aws.amazon.com/ec2/) - Scalable cloud hosting

**Monitoring & Logging:**
- [AppSignal](https://appsignal.com/) - Rails monitoring
- [Sentry](https://sentry.io/) - Error tracking
- [Lograge](https://github.com/roidrage/lograge) - Structured logging

**CI/CD:**
- [GitHub Actions](https://github.com/features/actions) - CI/CD automation
- [Kamal GitHub Action](https://github.com/basecamp/kamal) - Official action

</resources>
