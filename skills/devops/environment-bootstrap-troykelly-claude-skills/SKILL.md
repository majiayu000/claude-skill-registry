---
name: environment-bootstrap
description: Use for development environment setup - create and maintain init scripts, run smoke tests, ensure consistent environment across sessions
allowed-tools:
  - Bash
  - Read
  - Write
model: opus
---

# Environment Bootstrap

## Overview

Set up and maintain consistent development environments.

**Core principle:** Every session should start with a known-good environment.

**Announce at start:** "I'm using environment-bootstrap to set up the development environment."

## When to Use

| Situation | Action |
|-----------|--------|
| First clone of repository | Create init script |
| Starting new session | Run init script |
| After pulling changes | Re-run init if deps changed |
| Environment seems broken | Run init to reset |

## The Init Script

### Location

```
project/
├── scripts/
│   └── init.sh    ← Standard location
├── package.json
└── ...
```

### Template

```bash
#!/usr/bin/env bash
set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=== Development Environment Bootstrap ==="
echo ""

# Step 1: Check prerequisites
echo "Checking prerequisites..."

check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo -e "${RED}ERROR: $1 is required but not installed${NC}"
        exit 1
    fi
    echo -e "  ${GREEN}✓${NC} $1 found"
}

check_command node
check_command pnpm
check_command git
check_command gh

# Check Node version
REQUIRED_NODE="18"
CURRENT_NODE=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$CURRENT_NODE" -lt "$REQUIRED_NODE" ]; then
    echo -e "${RED}ERROR: Node $REQUIRED_NODE+ required, found $CURRENT_NODE${NC}"
    exit 1
fi
echo -e "  ${GREEN}✓${NC} Node version OK ($CURRENT_NODE)"

# Check gh authentication
if ! gh auth status &> /dev/null; then
    echo -e "${RED}ERROR: gh CLI not authenticated. Run 'gh auth login'${NC}"
    exit 1
fi
echo -e "  ${GREEN}✓${NC} GitHub CLI authenticated"

echo ""

# Step 2: Install dependencies
echo "Installing dependencies..."
pnpm install --frozen-lockfile --silent
echo -e "${GREEN}✓${NC} Dependencies installed"
echo ""

# Step 3: Environment setup
echo "Setting up environment..."
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${YELLOW}!${NC} Created .env from .env.example - review and update values"
    else
        echo -e "${YELLOW}!${NC} No .env file and no .env.example found"
    fi
else
    echo -e "  ${GREEN}✓${NC} .env exists"
fi
echo ""

# Step 4: Build
echo "Building project..."
pnpm build --silent
echo -e "${GREEN}✓${NC} Build successful"
echo ""

# Step 5: Run tests
echo "Running tests..."
if pnpm test --silent; then
    echo -e "${GREEN}✓${NC} Tests passed"
else
    echo -e "${RED}✗${NC} Tests failed - environment may have issues"
    exit 1
fi
echo ""

# Step 6: Start development services (if docker-compose exists)
if [ -f "docker-compose.yml" ] || [ -f "docker-compose.yaml" ]; then
    echo "Starting development services..."
    docker-compose up -d

    echo "Waiting for services to be ready..."
    sleep 5

    # Verify postgres (if defined)
    if docker-compose config --services 2>/dev/null | grep -q "postgres"; then
        if docker-compose ps postgres 2>/dev/null | grep -q "Up"; then
            echo -e "${GREEN}✓${NC} postgres ready"
        else
            echo -e "${RED}✗${NC} postgres failed to start"
        fi
    fi

    # Verify redis (if defined)
    if docker-compose config --services 2>/dev/null | grep -q "redis"; then
        if docker-compose ps redis 2>/dev/null | grep -q "Up"; then
            echo -e "${GREEN}✓${NC} redis ready"
        else
            echo -e "${RED}✗${NC} redis failed to start"
        fi
    fi

    echo ""
fi

# Step 7: Start development server (optional)
if [ "${START_DEV_SERVER:-false}" = "true" ]; then
    echo "Starting development server..."
    pnpm dev &
    DEV_PID=$!

    # Wait for server to be ready
    sleep 5

    # Smoke test (IPv6-first: try [::1] before falling back to 127.0.0.1)
    if curl -sf http://[::1]:3000/health > /dev/null; then
        echo -e "${GREEN}✓${NC} Development server running on IPv6 (PID: $DEV_PID)"
    elif curl -sf http://127.0.0.1:3000/health > /dev/null; then
        echo -e "${YELLOW}!${NC} Development server running on IPv4 legacy (PID: $DEV_PID)"
    else
        echo -e "${RED}✗${NC} Development server not responding"
        kill $DEV_PID 2>/dev/null
        exit 1
    fi
fi

echo ""
echo -e "${GREEN}=== Environment Ready ===${NC}"
echo ""
echo "Next steps:"
echo "  pnpm dev    - Start development server"
echo "  pnpm test   - Run tests"
echo "  pnpm build  - Build for production"
```

### Making Executable

```bash
chmod +x scripts/init.sh
```

## Running the Init Script

### Standard Run

```bash
./scripts/init.sh
```

### With Dev Server

```bash
START_DEV_SERVER=true ./scripts/init.sh
```

### After Pulling Changes

```bash
git pull origin main
./scripts/init.sh
```

## Smoke Test

After environment setup, verify basic functionality:

### What to Test

| Test | How | Pass Criteria |
|------|-----|---------------|
| Build | `pnpm build` | No errors |
| Tests | `pnpm test` | All pass |
| Dev server | `pnpm dev` | Server starts |
| Health check | `curl http://[::1]:3000/health` | 200 OK (IPv6-first) |
| Basic flow | Run E2E test | Passes |

### Smoke Test Script

```bash
#!/usr/bin/env bash
# scripts/smoke-test.sh

set -euo pipefail

echo "Running smoke tests..."

# Start dev server
pnpm dev &
DEV_PID=$!
sleep 10

# Health check (IPv6-first, fallback to IPv4 legacy)
if curl -sf http://[::1]:3000/health > /dev/null; then
    echo "Health check passed (IPv6)"
elif curl -sf http://127.0.0.1:3000/health > /dev/null; then
    echo "Health check passed (IPv4 legacy)"
else
    echo "Health check failed"
    kill $DEV_PID
    exit 1
fi

# Basic E2E (if available)
if [ -f "tests/smoke.test.ts" ]; then
    pnpm test:e2e tests/smoke.test.ts
fi

# Clean up
kill $DEV_PID

echo "Smoke tests passed"
```

## Environment Documentation

### README Section

```markdown
## Development Setup

### Prerequisites

- Node.js 18+
- pnpm 8+
- GitHub CLI (`gh`) authenticated

### Quick Start

```bash
# Clone repository
git clone https://github.com/owner/repo.git
cd repo

# Run setup
./scripts/init.sh

# Start development
pnpm dev
```

### Environment Variables

Copy `.env.example` to `.env` and update:

| Variable | Description | Required |
|----------|-------------|----------|
| DATABASE_URL | PostgreSQL connection string | Yes |
| JWT_SECRET | Secret for signing tokens | Yes |
| API_KEY | External API key | No |
```

## Maintaining Init Scripts

### When to Update

Update the init script when:

- New prerequisite added
- New environment variable needed
- Build process changes
- New verification step needed

### Version in Commit

When updating init script:

```bash
git add scripts/init.sh
git commit -m "chore: Update init script for [change]"
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| "command not found" | Install missing prerequisite |
| "permission denied" | `chmod +x scripts/init.sh` |
| "node version" | Use nvm: `nvm use 18` |
| "pnpm install failed" | Delete node_modules, try again |
| "build failed" | Check for type errors, missing deps |

### Reset Environment

When environment is in unknown state:

```bash
# Nuclear option
rm -rf node_modules dist .cache .next
pnpm store prune
./scripts/init.sh
```

## Checklist

Init script should:

- [ ] Check all prerequisites
- [ ] Verify correct versions
- [ ] Install dependencies
- [ ] Set up environment files
- [ ] Run build
- [ ] Run tests
- [ ] Start development services (if docker-compose exists)
- [ ] Verify services are ready (postgres, redis, etc.)
- [ ] Optionally start dev server
- [ ] Verify server responds (if started)
- [ ] Print clear success/failure

Environment documentation should:

- [ ] List prerequisites
- [ ] Explain quick start
- [ ] Document env variables
- [ ] Explain common issues

## Integration

This skill is called by:
- `session-start` - Beginning of each session
- `error-recovery` - Resetting environment

This skill ensures:
- Consistent development environment
- Quick session startup
- Early detection of environment issues
