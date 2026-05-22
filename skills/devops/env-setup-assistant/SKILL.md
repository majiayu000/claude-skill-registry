---
name: env-setup-assistant
description: Expert guide for setting up development environments including IDE configuration, tooling, dependencies, and developer onboarding. Use when bootstrapping new projects or standardizing team environments.
---

# Environment Setup Assistant Skill

## Overview

This skill helps you create reproducible, developer-friendly environments. Covers IDE configuration, tool installation, dependency management, onboarding documentation, and cross-platform compatibility.

## Environment Setup Philosophy

### Principles
1. **One command setup**: New developers should run one command
2. **Reproducible**: Same environment everywhere
3. **Documented**: Clear instructions for edge cases
4. **Versioned**: Lock tool and dependency versions

### Goals
- **DO**: Automate everything possible
- **DO**: Detect and report issues early
- **DO**: Support multiple platforms (macOS, Linux, Windows)
- **DON'T**: Assume global installations
- **DON'T**: Require manual steps without documentation

## Project Setup Script

### Comprehensive Setup Script

```bash
#!/bin/bash
# scripts/setup.sh

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# ===================
# Check Prerequisites
# ===================
check_command() {
    if ! command -v "$1" &> /dev/null; then
        log_error "$1 is not installed"
        return 1
    fi
    log_info "$1 found: $(command -v $1)"
    return 0
}

check_prerequisites() {
    log_info "Checking prerequisites..."

    local missing=0

    check_command "node" || missing=$((missing + 1))
    check_command "npm" || missing=$((missing + 1))
    check_command "git" || missing=$((missing + 1))

    # Check Node version
    local node_version=$(node -v | cut -d'v' -f2)
    local required_version="18.0.0"
    if ! [ "$(printf '%s\n' "$required_version" "$node_version" | sort -V | head -n1)" = "$required_version" ]; then
        log_error "Node.js version must be >= $required_version (found: $node_version)"
        missing=$((missing + 1))
    fi

    if [ $missing -gt 0 ]; then
        log_error "$missing prerequisite(s) missing"
        echo ""
        echo "Install missing tools:"
        echo "  - Node.js: https://nodejs.org/ or 'nvm install 20'"
        echo "  - Git: https://git-scm.com/"
        exit 1
    fi

    log_info "All prerequisites met!"
}

# ===================
# Environment Setup
# ===================
setup_env() {
    log_info "Setting up environment..."

    if [ ! -f .env ]; then
        if [ -f .env.example ]; then
            cp .env.example .env
            log_info "Created .env from .env.example"
            log_warn "Please update .env with your values"
        else
            log_error "No .env.example found"
            exit 1
        fi
    else
        log_info ".env already exists"
    fi
}

# ===================
# Install Dependencies
# ===================
install_dependencies() {
    log_info "Installing dependencies..."

    npm ci

    log_info "Dependencies installed!"
}

# ===================
# Setup Git Hooks
# ===================
setup_git_hooks() {
    log_info "Setting up Git hooks..."

    npx husky install 2>/dev/null || log_warn "Husky not configured"

    log_info "Git hooks configured!"
}

# ===================
# Database Setup
# ===================
setup_database() {
    log_info "Setting up database..."

    # Check if database is running
    if ! pg_isready -h localhost -p 5432 &>/dev/null; then
        log_warn "PostgreSQL not running on localhost:5432"
        log_info "Start with: docker-compose up -d db"
        return
    fi

    # Run migrations
    npm run db:migrate 2>/dev/null || log_warn "No migrations to run"

    # Seed data (development only)
    if [ "$NODE_ENV" != "production" ]; then
        npm run db:seed 2>/dev/null || log_warn "No seed script found"
    fi

    log_info "Database setup complete!"
}

# ===================
# Verify Setup
# ===================
verify_setup() {
    log_info "Verifying setup..."

    # Type check
    npm run typecheck 2>/dev/null && log_info "TypeScript: OK" || log_warn "TypeScript check failed"

    # Lint
    npm run lint 2>/dev/null && log_info "Linting: OK" || log_warn "Linting issues found"

    # Build test
    npm run build 2>/dev/null && log_info "Build: OK" || log_error "Build failed"
}

# ===================
# Main
# ===================
main() {
    echo ""
    echo "================================"
    echo "  Project Setup"
    echo "================================"
    echo ""

    check_prerequisites
    echo ""

    setup_env
    echo ""

    install_dependencies
    echo ""

    setup_git_hooks
    echo ""

    setup_database
    echo ""

    verify_setup
    echo ""

    echo "================================"
    echo "  Setup Complete!"
    echo "================================"
    echo ""
    echo "Next steps:"
    echo "  1. Update .env with your values"
    echo "  2. Start development: npm run dev"
    echo "  3. Open http://localhost:3000"
    echo ""
}

main "$@"
```

## Version Management

### .nvmrc / .node-version

```
20.10.0
```

### Tool Versions (asdf)

```ini
# .tool-versions
nodejs 20.10.0
pnpm 8.12.0
python 3.11.6
```

### Volta Configuration

```json
// package.json
{
  "volta": {
    "node": "20.10.0",
    "npm": "10.2.5"
  }
}
```

## IDE Configuration

### VSCode Settings

```json
// .vscode/settings.json
{
  // Editor
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit",
    "source.organizeImports": "explicit"
  },
  "editor.tabSize": 2,
  "editor.insertSpaces": true,
  "editor.rulers": [80, 120],

  // Files
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  "files.exclude": {
    "**/.git": true,
    "**/node_modules": true,
    "**/.next": true
  },

  // TypeScript
  "typescript.preferences.importModuleSpecifier": "relative",
  "typescript.updateImportsOnFileMove.enabled": "always",
  "typescript.tsdk": "node_modules/typescript/lib",

  // Tailwind
  "tailwindCSS.experimental.classRegex": [
    ["cva\\(([^)]*)\\)", "[\"'`]([^\"'`]*).*?[\"'`]"],
    ["cn\\(([^)]*)\\)", "[\"'`]([^\"'`]*).*?[\"'`]"]
  ],

  // ESLint
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    "typescript",
    "typescriptreact"
  ],

  // Prettier
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

### VSCode Extensions

```json
// .vscode/extensions.json
{
  "recommendations": [
    // Essential
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "bradlc.vscode-tailwindcss",

    // TypeScript
    "ms-vscode.vscode-typescript-next",
    "yoavbls.pretty-ts-errors",

    // React/Next.js
    "dsznajder.es7-react-js-snippets",
    "formulahendry.auto-rename-tag",

    // Git
    "eamodio.gitlens",
    "mhutchie.git-graph",

    // Productivity
    "streetsidesoftware.code-spell-checker",
    "usernamehw.errorlens",
    "christian-kohler.path-intellisense",

    // Theme (optional)
    "GitHub.github-vscode-theme"
  ],
  "unwantedRecommendations": []
}
```

### VSCode Launch Configuration

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Next.js: debug server-side",
      "type": "node",
      "request": "attach",
      "port": 9229,
      "skipFiles": ["<node_internals>/**"]
    },
    {
      "name": "Next.js: debug client-side",
      "type": "chrome",
      "request": "launch",
      "url": "http://localhost:3000"
    },
    {
      "name": "Next.js: debug full stack",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/node_modules/.bin/next",
      "args": ["dev"],
      "cwd": "${workspaceFolder}",
      "console": "integratedTerminal"
    },
    {
      "name": "Jest: current file",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/node_modules/.bin/jest",
      "args": [
        "${fileBasename}",
        "--config",
        "jest.config.js",
        "--runInBand"
      ],
      "console": "integratedTerminal"
    }
  ]
}
```

## EditorConfig

```ini
# .editorconfig
root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.md]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab
```

## Git Configuration

### .gitattributes

```gitattributes
# .gitattributes

# Auto detect text files
* text=auto eol=lf

# Documents
*.md text
*.txt text

# Source code
*.js text
*.jsx text
*.ts text
*.tsx text
*.css text
*.scss text
*.html text
*.json text
*.yaml text
*.yml text

# Docker
Dockerfile text

# Shell
*.sh text eol=lf

# Windows
*.bat text eol=crlf

# Binary
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
*.woff binary
*.woff2 binary
*.ttf binary
*.eot binary
*.pdf binary
```

### Pre-commit Hooks (Husky + lint-staged)

```json
// package.json
{
  "scripts": {
    "prepare": "husky install"
  },
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md,yml,yaml}": [
      "prettier --write"
    ]
  }
}
```

```bash
# .husky/pre-commit
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

npx lint-staged
```

```bash
# .husky/commit-msg
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

npx --no-install commitlint --edit "$1"
```

## Onboarding Documentation

### CONTRIBUTING.md Template

```markdown
# Contributing Guide

## Getting Started

### Prerequisites

- Node.js 20+ ([install](https://nodejs.org/) or `nvm install 20`)
- pnpm 8+ (`npm install -g pnpm`)
- Docker Desktop ([install](https://docker.com/products/docker-desktop))
- Git ([install](https://git-scm.com/))

### Quick Start

```bash
# Clone the repository
git clone https://github.com/org/project.git
cd project

# Run setup script
./scripts/setup.sh

# Start development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

### Manual Setup

If the setup script doesn't work:

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```

3. **Start services**
   ```bash
   docker-compose up -d
   ```

4. **Run migrations**
   ```bash
   npm run db:migrate
   ```

## Development Workflow

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `chore/description` - Maintenance
- `docs/description` - Documentation

### Commit Messages

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Pull Requests

1. Create a branch from `main`
2. Make your changes
3. Run tests: `npm test`
4. Run linting: `npm run lint`
5. Create PR against `main`

## Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run test` | Run tests |
| `npm run lint` | Run linting |
| `npm run typecheck` | Run TypeScript checks |

## Architecture

[Brief overview of project structure]

## Getting Help

- Check existing [issues](https://github.com/org/project/issues)
- Ask in #dev-help Slack channel
- Reach out to @maintainer
```

### Developer Onboarding Checklist

```markdown
# New Developer Onboarding

## Day 1 - Environment Setup

- [ ] Clone repository
- [ ] Run setup script
- [ ] Verify development server starts
- [ ] Install IDE extensions
- [ ] Join Slack channels: #dev, #dev-help

## Day 1 - Access

- [ ] GitHub repository access
- [ ] Vercel team access
- [ ] Supabase project access
- [ ] 1Password vault access
- [ ] Figma access

## Week 1 - Understanding

- [ ] Read CONTRIBUTING.md
- [ ] Review project architecture
- [ ] Complete starter task
- [ ] Pair with team member

## Helpful Links

- [Project Documentation](./docs/)
- [Design System](https://figma.com/...)
- [API Documentation](./docs/api/)
```

## Cross-Platform Compatibility

### Platform Detection Script

```bash
# scripts/detect-platform.sh
#!/bin/bash

detect_os() {
    case "$(uname -s)" in
        Darwin)
            echo "macos"
            ;;
        Linux)
            echo "linux"
            ;;
        CYGWIN*|MINGW*|MSYS*)
            echo "windows"
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

detect_arch() {
    case "$(uname -m)" in
        x86_64)
            echo "amd64"
            ;;
        arm64|aarch64)
            echo "arm64"
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

OS=$(detect_os)
ARCH=$(detect_arch)

echo "Detected: $OS ($ARCH)"
```

### Windows PowerShell Setup

```powershell
# scripts/setup.ps1

Write-Host "Setting up development environment..." -ForegroundColor Green

# Check Node.js
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "Node.js not found. Please install from https://nodejs.org/" -ForegroundColor Red
    exit 1
}

$nodeVersion = node -v
Write-Host "Node.js version: $nodeVersion" -ForegroundColor Cyan

# Copy environment file
if (-not (Test-Path .env)) {
    if (Test-Path .env.example) {
        Copy-Item .env.example .env
        Write-Host "Created .env from .env.example" -ForegroundColor Yellow
    }
}

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Green
npm ci

# Setup complete
Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "Run 'npm run dev' to start development server" -ForegroundColor Cyan
```

## Environment Checklist

### Project Setup
- [ ] Setup script works on macOS, Linux, Windows
- [ ] Prerequisites documented with versions
- [ ] Environment variables documented
- [ ] IDE configuration committed
- [ ] Git hooks configured

### Developer Experience
- [ ] One command setup
- [ ] Clear error messages
- [ ] Onboarding documentation
- [ ] Helpful npm scripts
- [ ] Debug configurations

### Code Quality
- [ ] ESLint configured
- [ ] Prettier configured
- [ ] TypeScript strict mode
- [ ] Pre-commit hooks
- [ ] Editor integration

## When to Use This Skill

Invoke this skill when:
- Starting a new project
- Onboarding new developers
- Standardizing team environments
- Troubleshooting development setup issues
- Creating setup automation
- Configuring IDE settings
- Setting up cross-platform development
