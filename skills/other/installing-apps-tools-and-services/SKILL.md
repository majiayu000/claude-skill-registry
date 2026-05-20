---
name: installing-apps-tools-and-services
description: "Use this skill when installing applications, packages, tools, or services on the system. Handles Python (uv), Node/JS/TS (bun), Docker containers, and GitHub-sourced installations with mise-managed tools and ecosystem integration patterns."
---

# Installing Apps and Packages

Comprehensive guide for installing applications, packages, and services following Jarad's ecosystem patterns and tool preferences.

## When to Use This Skill

Trigger this skill when:

- Installing Python applications or packages (CLI tools, libraries, services)
- Installing Node.js/JavaScript/TypeScript applications or packages
- Setting up containerized applications with Docker Compose
- Cloning and installing GitHub-sourced projects
- Integrating new tools into the existing ecosystem (proxy network, traefik, shared databases)
- Configuring applications to work with mise-managed tooling
- Setting up application secrets and environment variables

## General Workflow

### 1. Gather Data on Install Target

**Inspect Current Host:**

```bash
# Check OS and architecture
uname -a
lsb_release -a
arch

# Check mise-managed tools
mise ls --current

# Check available databases/services
systemctl status postgresql redis neo4j qdrant

# Check Docker network
docker network ls | grep proxy
```

**Key Information to Note:**

- OS: Ubuntu/Debian-based Linux
- Architecture: x86_64
- Package managers: uv (Python), bun (Node), mise (version management)
- Native services: PostgreSQL, Redis
- Docker network: `proxy` (system-wide Traefik network)
- Domain conventions: `*.delo.sh` for services

### 2. Gather Data on Thing Being Installed

**Use Official Channels:**

- Check main GitHub repository (README, installation docs)
- Review official documentation site
- Examine release notes and installation guides
- Look for Docker Compose examples if applicable
- Check for .env.example or configuration templates

**Critical Questions:**

- What runtime does it require? (Python, Node, Rust, Go?)
- Is it a CLI tool, library, or service?
- Does it need a database? (Can we use native Postgres/Redis?)
- Does it expose HTTP endpoints? (Needs Traefik integration?)
- What secrets/API keys does it need? (Check ~/.config/zshyzsh/secrets.zsh)

### 3. Determine Installation Method

**Decision Tree:**

```
Is it available in the mise registry?
├─ Yes? → mise install <package> #easy peasy done!

Is it Python-based?
├─ CLI tool → uv tool install
├─ Library → uv pip install -g
└─ Service → Docker or uv pip install -g

Is it Node/JS/TS-based?
├─ CLI tool → bun install -g or bunx (one-offs)
├─ Library → bun add
└─ Service → Docker or native bun

Is it containerized?
└─ Follow Docker/Containerized Workflow

Is it from GitHub?
└─ Clone to ~/code and apply appropriate install method
```

## Python Applications

### Core Principles

**ALWAYS use `uv` as the package tool**

- Prefer global installs over venv
- Use mise-managed `uv` and `python`
- End goal: invoke as `someApp`, not `uv run someApp`
- Preferred bin path: `~/.local/bin`

### Installation Patterns

**CLI Tools:**

```bash
# Use uv tool install for CLI tools
uv tool install <package-name>

# Verify installation
which <tool-name>
<tool-name> --version
```

**Example - Installing ruff:**

```bash
# Install globally as CLI tool
uv tool install ruff

# Verify
ruff --version
```

**Libraries/Packages:**

```bash
# Use uv sync first if pyproject allows
uv sync

# Use global install instead of pip install
uv pip install -g <package-name>

# If docs say "pip install -r requirements.txt", translate to:
uv pip install -r requirements.txt
```

**Services (Python-based):**

For services like FastAPI apps, Agno agents, etc.:

```bash
# Clone to ~/code if from GitHub
cd ~/code
gh repo clone <repo-url>
cd <project-name>

# Install dependencies globally or in project
uv sync

# Or use project-specific environment
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### Tool Replacements

**Replace these commands:**

- `pip install` → `uv pip install -g`
- `pipx install` → `uv tool install`
- `python -m venv` → `uv venv` (if venv needed)

### Mise Integration

**Ensure mise manages Python and uv:**

```bash
# Check current versions
mise ls --current

# Install/update if needed
mise use python@latest uv@latest -g

# Verify
which python
which uv

# Explicitly invoke
mise x -- uv --version
mise x python@3.12 -- python --version
```

## Node/JavaScript/TypeScript Applications

### Core Principles

**Prefer `bun` over `npm`**

- Use mise-managed bun/nodejs
- Use globally installed tools
- Use latest bun/nodejs versions
- OK to use `npx` or `bunx` for one-off commands

### Installation Patterns

**CLI Tools:**

```bash
# Global installation with bun
bun install -g <package-name>

# Verify
which <tool-name>
<tool-name> --version
```

**Example - Installing typescript:**

```bash
# Install globally
bun install -g typescript

# Verify
tsc --version
```

**One-off Commands:**

```bash
# Use bunx for one-time executions
bunx create-react-app my-app
bunx prettier --write .
```

**Project Dependencies:**

```bash
# For project-specific packages
cd ~/code/<project-name>
bun install
bun add <package-name>
```

### Mise Integration

**Ensure mise manages bun/node:**

```bash
# Install/update globally
mise use bun@latest -g
mise use node@latest -g

# Verify
which bun
which node
bun --version
node --version
```

## GitHub-Sourced Installations

### Core Principle

**Always clone into `~/code`**

### Workflow

```bash
# 1. Clone to standard location
cd ~/code
git clone <repo-url>
cd <project-name>

# 2. Initialize with iMi (optional, if it's a project you'll develop)
imi init

# 3. Apply appropriate installation method based on type
# - Python: uv pip install -g -r requirements.txt
# - Node: bun install
# - Rust: cargo install --path .
# - Go: go install
```

**Example - Installing a Python CLI from GitHub:**

```bash
cd ~/code
git clone https://github.com/user/awesome-tool
cd awesome-tool

# Install as tool
uv tool install .

# Or if it has requirements
uv pip install -g -r requirements.txt
uv pip install -g .
```

## Docker/Containerized Installations

### Core Principles

**Ecosystem Integration:**

1. Modify compose files to fit Docker container ecosystem
2. Avoid common port conflicts (3000, 8080, etc.)
3. Use system-wide `proxy` network for Traefik integration
4. Connect to native services (Postgres, Redis, Neo4j, Qdrant)
5. Use simple, common-sense subdomains (\*.delo.sh)

### Workflow

#### 1. Examine and Modify Compose File

**Critical Modifications:**

```yaml
# docker-compose.yml

services:
  app:
    image: awesome-app:latest
    container_name: awesome-app # Simple slug, no numbers/postfixes
    restart: unless-stopped
    networks:
      - proxy # System-wide network
    environment:
      # Use native databases
      - DATABASE_URL=postgresql://user:pass@host.docker.internal:5432/dbname
      - REDIS_URL=redis://host.docker.internal:6379
      - QDRANT_URL=http://host.docker.internal:6333
    labels:
      # Traefik configuration
      - "traefik.enable=true"
      - "traefik.http.routers.awesome-app.rule=Host(`awesome.delo.sh`)"
      - "traefik.http.routers.awesome-app.entrypoints=websecure"
      - "traefik.http.routers.awesome-app.tls.certresolver=letsencrypt"
      - "traefik.http.services.awesome-app.loadbalancer.server.port=8000"

networks:
  proxy:
    external: true
```

**Port Management:**

- Avoid exposing ports directly unless necessary
- Use Traefik labels for HTTP/HTTPS access
- If port exposure needed, choose random non-privileged port (e.g., 8473, 9234)
- Never use common ports: 3000, 8000, 8080, 5000, etc.

**Database Integration:**

```yaml
# DON'T add separate database services
services:
  postgres:  # ❌ Don't do this
    image: postgres:16
    ...

# DO connect to native instances
environment:
  # ✅ Use host.docker.internal
  - DATABASE_URL=postgresql://user:pass@host.docker.internal:5432/dbname
  - REDIS_URL=redis://host.docker.internal:6379
```

#### 2. Create .env File

**Resolve Secrets:**

1. Check provided .env.example or README
2. Cross-reference with system secrets: `~/.config/zshyzsh/secrets.zsh`
3. Generate new secrets if needed (API keys, passwords, etc.)

```bash
# Example .env file
DATABASE_URL=postgresql://delorenj:${POSTGRES_PASSWORD}@host.docker.internal:5432/awesome_app
REDIS_URL=redis://host.docker.internal:6379
SECRET_KEY=${AWESOME_APP_SECRET_KEY}  # From secrets.zsh
API_KEY=${OPENAI_API_KEY}  # From secrets.zsh
```

**Common Secret Locations:**

- OpenAI: `$OPENAI_API_KEY`
- Anthropic: `$ANTHROPIC_API_KEY`
- GitHub: `$GITHUB_TOKEN`
- Database: `$POSTGRES_PASSWORD`

#### 3. Build and Deploy

```bash
# Production build preferred
docker compose build --no-cache

# Deploy with proper restart policy
docker compose up -d

# Verify
docker compose ps
docker compose logs -f
```

**Container Naming:**

- Use simple slugs: `awesome-app`, not `awesome-app-1` or `awesome-app_container`
- Set `container_name` explicitly in compose file
- Restart policy: `unless-stopped` is usually sufficient

**Lock Down Configuration:**

For production deployments, create custom image and push to Docker Hub:

```bash
# Build custom image
docker build -t delorenj/awesome-app:latest .

# Push to Docker Hub
docker push delorenj/awesome-app:latest

# Update compose to use locked image
services:
  app:
    image: delorenj/awesome-app:latest
```

### Traefik Integration Patterns

**Basic HTTP Service:**

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.app.rule=Host(`app.delo.sh`)"
  - "traefik.http.routers.app.entrypoints=websecure"
  - "traefik.http.routers.app.tls.certresolver=letsencrypt"
```

**Service with Path Prefix:**

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.app.rule=Host(`delo.sh`) && PathPrefix(`/app`)"
  - "traefik.http.middlewares.app-strip.stripprefix.prefixes=/app"
  - "traefik.http.routers.app.middlewares=app-strip"
```

**WebSocket Support:**

```yaml
labels:
  - "traefik.http.routers.app.rule=Host(`ws.delo.sh`)"
  - "traefik.http.services.app.loadbalancer.server.port=8080"
```

### Database Setup

**Create Database (if needed):**

```bash
# Connect to native Postgres
psql -U delorenj -d postgres

# Create database
CREATE DATABASE awesome_app;

# Create user if needed
CREATE USER awesome_app WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE awesome_app TO awesome_app;
```

**Initialize Schema:**

```bash
# If app has migrations
docker compose exec app python manage.py migrate

# Or run SQL files
psql -U delorenj -d awesome_app -f schema.sql
```

## Post-Installation Verification

### Check Tool Availability

```bash
# For CLI tools
which <tool-name>
<tool-name> --version

# For Python packages
python -c "import <package>"

# For Node packages
node -e "require('<package>')"

# For Docker services
docker compose ps
curl http://localhost:<port>/health
curl https://app.delo.sh/health
```

### Verify Mise Integration

```bash
# List all mise-managed tools
mise ls --current

# Verify PATH includes mise bins
echo $PATH | grep mise
```

### Verify Service Integration

```bash
# Test database connection
psql -U delorenj -d awesome_app -c "SELECT 1"

# Test Redis connection
redis-cli ping

# Test Traefik routing
curl -I https://app.delo.sh
```

## Common Patterns

### Pattern: Installing Python MCP Server

```bash
# 1. Clone to ~/code
cd ~/code
git clone https://github.com/user/mcp-server
cd mcp-server

# 2. Install globally
uv pip install -g .

# 3. Verify
which mcp-server
mcp-server --version

# 4. Configure in Claude Code
# Add to claude_desktop_config.json
```

### Pattern: Installing Node CLI Tool

```bash
# 1. Install globally with bun
bun install -g awesome-cli

# 2. Verify
which awesome-cli
awesome-cli --version

# 3. Add to mise if version pinning needed
mise use awesome-cli@latest -g
```

### Pattern: Docker Service with Native Database

```bash
# 1. Create project structure
cd ~/docker/trunk-main/stacks/ai
mkdir awesome-service
cd awesome-service

# 2. Create compose file
cat > docker-compose.yml << 'EOF'
services:
  awesome:
    image: awesome/service:latest
    container_name: awesome-service
    restart: unless-stopped
    networks:
      - proxy
    environment:
      - DATABASE_URL=postgresql://delorenj:${POSTGRES_PASSWORD}@host.docker.internal:5432/awesome
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.awesome.rule=Host(`awesome.delo.sh`)"
      - "traefik.http.routers.awesome.entrypoints=websecure"
      - "traefik.http.routers.awesome.tls.certresolver=letsencrypt"

networks:
  proxy:
    external: true
EOF

# 3. Create .env from secrets
cat > .env << 'EOF'
POSTGRES_PASSWORD=<from secrets.zsh>
OPENAI_API_KEY=<from secrets.zsh>
EOF

# 4. Create database
psql -U delorenj -d postgres -c "CREATE DATABASE awesome"

# 5. Deploy
docker compose up -d

# 6. Verify
docker compose logs -f
curl https://awesome.delo.sh/health
```

## Troubleshooting

### Tool Not Found After Installation

```bash
# Check if installed
uv tool list
bun pm ls -g

# Check PATH
echo $PATH | grep -E '(\.local/bin|mise)'

# Verify mise activation
mise doctor

# Reinstall if needed
uv tool uninstall <tool>
uv tool install <tool>
```

### Docker Service Won't Start

```bash
# Check logs
docker compose logs

# Verify network exists
docker network ls | grep proxy

# Test database connectivity
docker compose exec app psql $DATABASE_URL -c "SELECT 1"

# Check port conflicts
ss -tulpn | grep :<port>
```

### Traefik Routing Issues

```bash
# Check Traefik dashboard
# (Access via configured dashboard URL)

# Verify labels are applied
docker inspect <container> | grep traefik

# Test DNS resolution
nslookup app.delo.sh

# Check certificate
curl -I https://app.delo.sh
```

## Quick Reference

### Installation Commands by Type

| Type           | Install Command                | Example                      |
| -------------- | ------------------------------ | ---------------------------- |
| Python CLI     | `uv tool install <pkg>`        | `uv tool install ruff`       |
| Python lib     | `uv pip install -g <pkg>`      | `uv pip install -g requests` |
| Node CLI       | `bun install -g <pkg>`         | `bun install -g typescript`  |
| Node one-off   | `bunx <cmd>`                   | `bunx prettier --write .`    |
| GitHub repo    | `cd ~/code && git clone <url>` | Clone then apply above       |
| Docker service | `docker compose up -d`         | With ecosystem mods          |

### Key File Locations

- Secrets: `~/.config/zshyzsh/secrets.zsh`
- Docker stacks: `~/docker/trunk-main/stacks/`
- Code repos: `~/code/`
- Mise config: `~/.config/mise/config.toml`
- Local bins: `~/.local/bin/`

### Essential Checks

```bash
# Before installing
mise ls --current
which python uv bun node
docker network ls | grep proxy

# After installing
which <tool>
<tool> --version
mise doctor

# For Docker services
docker compose ps
docker compose logs
curl https://app.delo.sh/health
```

## Resources

### references/

- `docker-compose-patterns.md` - Common Docker Compose configurations
- `traefik-labels-reference.md` - Traefik label patterns
- `native-service-connection.md` - Connecting to native Postgres/Redis/Qdrant

### scripts/

- `install-python-cli.sh` - Template for Python CLI installation
- `install-node-cli.sh` - Template for Node CLI installation
- `setup-docker-service.sh` - Template for Docker service setup

### assets/

- `docker-compose.template.yml` - Standard compose file template
- `.env.template` - Standard .env template
- `traefik-labels.yml` - Common Traefik label configurations

## See Also

- `ecosystem-patterns` skill - Overall ecosystem architecture and conventions
- `mise-task-managing` skill - Managing mise tasks and tool versions
- Docker Compose patterns in ecosystem-patterns/references/
