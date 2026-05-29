---
name: Repository Automation Scripts
description: Automated scripts for common repository tasks including setup, cleanup, dependency updates, and maintenance.
---

# Repository Automation Scripts

## Overview

Repository Automation Scripts are helper scripts that automate repetitive tasks, reduce manual errors, and improve developer productivity.

**Core Principle**: "If you do it more than twice, automate it."

---

## 1. Setup Script

```bash
#!/bin/bash
# scripts/setup.sh

set -e  # Exit on error

echo "🚀 Setting up development environment..."

# Check prerequisites
check_command() {
  if ! command -v $1 &> /dev/null; then
    echo "❌ $1 is required but not installed."
    exit 1
  fi
}

check_command node
check_command docker
check_command git

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Setup environment
if [ ! -f .env ]; then
  echo "📝 Creating .env from .env.example..."
  cp .env.example .env
fi

# Start Docker services
echo "🐳 Starting Docker services..."
docker-compose up -d

# Wait for database
echo "⏳ Waiting for database..."
sleep 5

# Run migrations
echo "🗄️  Running database migrations..."
npm run db:migrate

# Seed database
echo "🌱 Seeding database..."
npm run db:seed

echo "✅ Setup complete! Run 'npm run dev' to start"
```

---

## 2. Cleanup Script

```bash
#!/bin/bash
# scripts/cleanup.sh

echo "🧹 Cleaning up development environment..."

# Stop Docker containers
docker-compose down

# Remove node_modules
rm -rf node_modules

# Remove build artifacts
rm -rf .next dist build

# Remove logs
rm -rf logs/*.log

# Remove .env (optional)
read -p "Remove .env file? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  rm -f .env
fi

echo "✅ Cleanup complete!"
```

---

## 3. Dependency Update Script

```bash
#!/bin/bash
# scripts/update-deps.sh

echo "📦 Updating dependencies..."

# Update package.json
npx npm-check-updates -u

# Install updated dependencies
npm install

# Run tests
npm test

# If tests pass, commit
if [ $? -eq 0 ]; then
  git add package.json package-lock.json
  git commit -m "chore: update dependencies"
  echo "✅ Dependencies updated and committed"
else
  echo "❌ Tests failed. Please review changes."
  git checkout package.json package-lock.json
fi
```

---

## 4. Database Reset Script

```bash
#!/bin/bash
# scripts/db-reset.sh

echo "🗄️  Resetting database..."

# Confirm action
read -p "This will delete all data. Continue? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  exit 1
fi

# Reset database
npm run db:reset

# Seed with fresh data
npm run db:seed

echo "✅ Database reset complete!"
```

---

## 5. Code Generation Script

```bash
#!/bin/bash
# scripts/generate-component.sh

COMPONENT_NAME=$1

if [ -z "$COMPONENT_NAME" ]; then
  echo "Usage: ./scripts/generate-component.sh ComponentName"
  exit 1
fi

COMPONENT_DIR="src/components/$COMPONENT_NAME"

mkdir -p $COMPONENT_DIR

# Create component file
cat > $COMPONENT_DIR/$COMPONENT_NAME.tsx << EOF
import React from 'react';
import styles from './$COMPONENT_NAME.module.css';

interface ${COMPONENT_NAME}Props {
  // Add props here
}

export const $COMPONENT_NAME: React.FC<${COMPONENT_NAME}Props> = (props) => {
  return (
    <div className={styles.container}>
      <h1>$COMPONENT_NAME</h1>
    </div>
  );
};
EOF

# Create CSS module
cat > $COMPONENT_DIR/$COMPONENT_NAME.module.css << EOF
.container {
  /* Add styles here */
}
EOF

# Create test file
cat > $COMPONENT_DIR/$COMPONENT_NAME.test.tsx << EOF
import { render, screen } from '@testing-library/react';
import { $COMPONENT_NAME } from './$COMPONENT_NAME';

describe('$COMPONENT_NAME', () => {
  it('renders correctly', () => {
    render(<$COMPONENT_NAME />);
    expect(screen.getByText('$COMPONENT_NAME')).toBeInTheDocument();
  });
});
EOF

# Create index file
cat > $COMPONENT_DIR/index.ts << EOF
export { $COMPONENT_NAME } from './$COMPONENT_NAME';
EOF

echo "✅ Component $COMPONENT_NAME created at $COMPONENT_DIR"
```

---

## 6. Pre-push Validation Script

```bash
#!/bin/bash
# scripts/pre-push.sh

echo "🔍 Running pre-push checks..."

# Lint
echo "📝 Linting..."
npm run lint
if [ $? -ne 0 ]; then
  echo "❌ Linting failed"
  exit 1
fi

# Type check
echo "🔤 Type checking..."
npm run type-check
if [ $? -ne 0 ]; then
  echo "❌ Type check failed"
  exit 1
fi

# Tests
echo "🧪 Running tests..."
npm test
if [ $? -ne 0 ]; then
  echo "❌ Tests failed"
  exit 1
fi

echo "✅ All checks passed!"
```

---

## 7. Makefile for Common Tasks

```makefile
# Makefile

.PHONY: setup dev test lint clean

setup:
  @./scripts/setup.sh

dev:
  @npm run dev

test:
  @npm test

lint:
  @npm run lint
  @npm run type-check

clean:
  @./scripts/cleanup.sh

db-reset:
  @./scripts/db-reset.sh

update-deps:
  @./scripts/update-deps.sh

help:
  @echo "Available commands:"
  @echo "  make setup       - Setup development environment"
  @echo "  make dev         - Start development server"
  @echo "  make test        - Run tests"
  @echo "  make lint        - Run linting and type checking"
  @echo "  make clean       - Clean up environment"
  @echo "  make db-reset    - Reset database"
  @echo "  make update-deps - Update dependencies"
```

---

## 8. GitHub Actions Automation

```yaml
# .github/workflows/dependency-update.yml
name: Dependency Update

on:
  schedule:
    - cron: '0 0 * * 1'  # Every Monday
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Update dependencies
        run: ./scripts/update-deps.sh
      
      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v4
        with:
          title: 'chore: update dependencies'
          body: 'Automated dependency update'
          branch: 'chore/update-dependencies'
```

---

## 9. Repository Automation Checklist

- [ ] **Setup Script**: One-command environment setup?
- [ ] **Cleanup Script**: Easy cleanup of dev environment?
- [ ] **Update Script**: Automated dependency updates?
- [ ] **Code Generation**: Templates for common files?
- [ ] **Pre-push Checks**: Validation before pushing?
- [ ] **Makefile**: Common tasks documented?
- [ ] **Documentation**: Scripts documented in README?
- [ ] **Permissions**: Scripts executable (`chmod +x`)?

---

## Related Skills
- `45-developer-experience/local-dev-standard`
- `45-developer-experience/release-workflow`
