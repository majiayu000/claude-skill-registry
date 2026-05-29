---
name: Local Development Standard
description: Standardized local development environment setup ensuring consistency across team members and reducing "works on my machine" issues.
---

# Local Development Standard

## Overview

Local Development Standards define how developers set up and run projects on their machines, ensuring consistency, reproducibility, and minimal onboarding friction.

**Core Principle**: "New developers should be productive in under 30 minutes."

---

## 1. One-Command Setup

```bash
# The ideal: Single command to get started
npm run setup

# Or
make setup

# Or
./scripts/setup.sh
```

### Setup Script Example
```bash
#!/bin/bash
# scripts/setup.sh

echo "🚀 Setting up development environment..."

# Check prerequisites
command -v node >/dev/null 2>&1 || { echo "Node.js required"; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "Docker required"; exit 1; }

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Start Docker services
docker-compose up -d

# Run database migrations
npm run db:migrate

# Seed database
npm run db:seed

echo "✅ Setup complete! Run 'npm run dev' to start"
```

---

## 2. Environment Configuration

### .env.example
```bash
# .env.example - Committed to repo
DATABASE_URL=postgresql://localhost:5432/myapp_dev
REDIS_URL=redis://localhost:6379
API_KEY=your_api_key_here
NODE_ENV=development
```

### .env - Not committed
```bash
# .env - Local only, gitignored
DATABASE_URL=postgresql://localhost:5432/myapp_dev
REDIS_URL=redis://localhost:6379
API_KEY=actual_secret_key_12345
NODE_ENV=development
```

---

## 3. Docker Compose for Dependencies

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: myapp_dev
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: devpass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  mailhog:
    image: mailhog/mailhog
    ports:
      - "1025:1025"  # SMTP
      - "8025:8025"  # Web UI

volumes:
  postgres_data:
```

---

## 4. Package.json Scripts

```json
{
  "scripts": {
    "setup": "./scripts/setup.sh",
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "test": "jest",
    "test:watch": "jest --watch",
    "lint": "eslint .",
    "format": "prettier --write .",
    "type-check": "tsc --noEmit",
    "db:migrate": "prisma migrate dev",
    "db:seed": "prisma db seed",
    "db:reset": "prisma migrate reset",
    "docker:up": "docker-compose up -d",
    "docker:down": "docker-compose down"
  }
}
```

---

## 5. README Development Section

```markdown
## Development Setup

### Prerequisites
- Node.js 18+
- Docker Desktop
- Git

### Quick Start
\`\`\`bash
# Clone repository
git clone https://github.com/company/project.git
cd project

# Run setup
npm run setup

# Start development server
npm run dev
\`\`\`

### Available Commands
- `npm run dev` - Start development server
- `npm run test` - Run tests
- `npm run lint` - Lint code
- `npm run db:migrate` - Run database migrations

### Troubleshooting
- **Port 3000 already in use**: Run `lsof -ti:3000 | xargs kill`
- **Database connection failed**: Ensure Docker is running
```

---

## 6. VS Code Workspace Settings

```json
// .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "typescript.tsdk": "node_modules/typescript/lib",
  "files.exclude": {
    "**/.git": true,
    "**/node_modules": true,
    "**/.next": true
  }
}
```

### Recommended Extensions
```json
// .vscode/extensions.json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "prisma.prisma",
    "ms-azuretools.vscode-docker"
  ]
}
```

---

## 7. Hot Reload Configuration

### Next.js
```javascript
// next.config.js
module.exports = {
  reactStrictMode: true,
  webpack: (config) => {
    config.watchOptions = {
      poll: 1000,
      aggregateTimeout: 300,
    };
    return config;
  },
};
```

### Vite
```javascript
// vite.config.ts
export default defineConfig({
  server: {
    watch: {
      usePolling: true,
    },
    hmr: {
      overlay: true,
    },
  },
});
```

---

## 8. Local Development Checklist

- [ ] **One-Command Setup**: Can new devs start with single command?
- [ ] **.env.example**: Example environment file committed?
- [ ] **Docker Compose**: Dependencies containerized?
- [ ] **README**: Clear setup instructions?
- [ ] **VS Code Settings**: Workspace settings committed?
- [ ] **Hot Reload**: Fast feedback loop configured?
- [ ] **Seed Data**: Test data available for local dev?
- [ ] **Troubleshooting**: Common issues documented?

---

## Related Skills
* `45-developer-experience/onboarding-docs`
* `45-developer-experience/dev-environment-setup`
* `45-developer-experience/hot-reload-fast-feedback`
