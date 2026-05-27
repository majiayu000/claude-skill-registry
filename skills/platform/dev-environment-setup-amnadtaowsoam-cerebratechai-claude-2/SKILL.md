---
name: Development Environment Setup
description: Standardized development environment configuration including tools, IDE settings, and automation for consistent developer experience.
---

# Development Environment Setup

## Overview

Development Environment Setup ensures all developers have consistent, properly configured environments with the right tools, settings, and workflows.

**Core Principle**: "Automate environment setup. Developers should be coding, not configuring."

---

## 1. Required Tools Checklist

```markdown
# Developer Machine Setup Checklist

## Essential Tools
- [ ] **Git** (version control)
- [ ] **Node.js 18+** (runtime)
- [ ] **npm/pnpm/yarn** (package manager)
- [ ] **Docker Desktop** (containerization)
- [ ] **VS Code** (recommended IDE)
- [ ] **Postman/Insomnia** (API testing)

## Optional but Recommended
- [ ] **nvm** (Node version manager)
- [ ] **Homebrew** (macOS package manager)
- [ ] **Oh My Zsh** (terminal enhancement)
- [ ] **Fig** (terminal autocomplete)
```

---

## 2. Automated Setup Script

```bash
#!/bin/bash
# scripts/setup-dev-machine.sh

echo "🚀 Setting up development machine..."

# Detect OS
OS="$(uname -s)"

# Install Homebrew (macOS)
if [ "$OS" = "Darwin" ]; then
  if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  fi
fi

# Install Node.js via nvm
if ! command -v nvm &> /dev/null; then
  echo "Installing nvm..."
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
  export NVM_DIR="$HOME/.nvm"
  [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
fi

echo "Installing Node.js 18..."
nvm install 18
nvm use 18
nvm alias default 18

# Install global npm packages
echo "Installing global packages..."
npm install -g pnpm typescript ts-node nodemon

# Install Docker Desktop
if ! command -v docker &> /dev/null; then
  echo "⚠️  Please install Docker Desktop manually:"
  echo "   https://www.docker.com/products/docker-desktop"
fi

# Install VS Code (macOS)
if [ "$OS" = "Darwin" ]; then
  if ! command -v code &> /dev/null; then
    echo "Installing VS Code..."
    brew install --cask visual-studio-code
  fi
fi

# Install VS Code extensions
echo "Installing VS Code extensions..."
code --install-extension dbaeumer.vscode-eslint
code --install-extension esbenp.prettier-vscode
code --install-extension prisma.prisma
code --install-extension ms-azuretools.vscode-docker
code --install-extension eamodio.gitlens
code --install-extension github.copilot

# Setup Git
echo "Configuring Git..."
read -p "Enter your Git name: " git_name
read -p "Enter your Git email: " git_email
git config --global user.name "$git_name"
git config --global user.email "$git_email"
git config --global init.defaultBranch main
git config --global pull.rebase false

# Setup SSH key for GitHub
if [ ! -f ~/.ssh/id_ed25519 ]; then
  echo "Generating SSH key..."
  ssh-keygen -t ed25519 -C "$git_email" -f ~/.ssh/id_ed25519 -N ""
  eval "$(ssh-agent -s)"
  ssh-add ~/.ssh/id_ed25519
  
  echo "📋 Copy this SSH key to GitHub:"
  cat ~/.ssh/id_ed25519.pub
  echo ""
  echo "Add it here: https://github.com/settings/keys"
  read -p "Press enter when done..."
fi

echo "✅ Development machine setup complete!"
echo ""
echo "Next steps:"
echo "1. Clone repositories"
echo "2. Run project-specific setup: npm run setup"
echo "3. Start coding!"
```

---

## 3. VS Code Configuration

### Workspace Settings
```json
// .vscode/settings.json
{
  // Editor
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true,
    "source.organizeImports": true
  },
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.tabSize": 2,
  "editor.rulers": [80, 120],
  
  // Files
  "files.autoSave": "onFocusChange",
  "files.exclude": {
    "**/.git": true,
    "**/node_modules": true,
    "**/.next": true,
    "**/dist": true,
    "**/.turbo": true
  },
  
  // TypeScript
  "typescript.tsdk": "node_modules/typescript/lib",
  "typescript.enablePromptUseWorkspaceTsdk": true,
  
  // Formatting
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  
  // Terminal
  "terminal.integrated.defaultProfile.osx": "zsh",
  "terminal.integrated.fontSize": 13,
  
  // Git
  "git.autofetch": true,
  "git.confirmSync": false,
  
  // Search
  "search.exclude": {
    "**/node_modules": true,
    "**/dist": true,
    "**/.next": true
  }
}
```

### Recommended Extensions
```json
// .vscode/extensions.json
{
  "recommendations": [
    // Essential
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "ms-azuretools.vscode-docker",
    
    // TypeScript
    "prisma.prisma",
    "bradlc.vscode-tailwindcss",
    
    // Git
    "eamodio.gitlens",
    "github.vscode-pull-request-github",
    
    // Productivity
    "github.copilot",
    "usernamehw.errorlens",
    "christian-kohler.path-intellisense",
    "formulahendry.auto-rename-tag",
    
    // Testing
    "orta.vscode-jest",
    
    // Markdown
    "yzhang.markdown-all-in-one"
  ]
}
```

### Keyboard Shortcuts
```json
// .vscode/keybindings.json
[
  {
    "key": "cmd+shift+r",
    "command": "workbench.action.tasks.runTask",
    "args": "dev"
  },
  {
    "key": "cmd+shift+t",
    "command": "workbench.action.tasks.runTask",
    "args": "test"
  }
]
```

---

## 4. Git Configuration

```bash
# ~/.gitconfig

[user]
  name = Your Name
  email = your.email@company.com

[core]
  editor = code --wait
  autocrlf = input
  excludesfile = ~/.gitignore_global

[init]
  defaultBranch = main

[pull]
  rebase = false

[push]
  default = current
  autoSetupRemote = true

[alias]
  # Shortcuts
  st = status
  co = checkout
  br = branch
  ci = commit
  
  # Useful aliases
  lg = log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
  unstage = reset HEAD --
  last = log -1 HEAD
  
  # Cleanup
  cleanup = "!git branch --merged | grep -v '\\*\\|main\\|develop' | xargs -n 1 git branch -d"

[diff]
  tool = vscode

[difftool "vscode"]
  cmd = code --wait --diff $LOCAL $REMOTE

[merge]
  tool = vscode

[mergetool "vscode"]
  cmd = code --wait $MERGED
```

### Global .gitignore
```bash
# ~/.gitignore_global

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment
.env.local
.env.*.local

# Logs
*.log
npm-debug.log*
```

---

## 5. Shell Configuration

### Zsh Setup (Oh My Zsh)
```bash
# ~/.zshrc

# Oh My Zsh
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="robbyrussell"

plugins=(
  git
  node
  npm
  docker
  vscode
  zsh-autosuggestions
  zsh-syntax-highlighting
)

source $ZSH/oh-my-zsh.sh

# NVM
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Aliases
alias gs="git status"
alias gp="git pull"
alias gc="git commit"
alias gco="git checkout"
alias dev="npm run dev"
alias t="npm test"

# Auto-load .nvmrc
autoload -U add-zsh-hook
load-nvmrc() {
  if [[ -f .nvmrc && -r .nvmrc ]]; then
    nvm use
  fi
}
add-zsh-hook chpwd load-nvmrc
load-nvmrc
```

---

## 6. Docker Configuration

```yaml
# docker-compose.yml (for local development)
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: devpass
      POSTGRES_DB: myapp_dev
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U dev"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  mailhog:
    image: mailhog/mailhog
    ports:
      - "1025:1025"  # SMTP
      - "8025:8025"  # Web UI

volumes:
  postgres_data:
```

---

## 7. Environment Variables

```bash
# .env.example (committed to repo)

# Database
DATABASE_URL=postgresql://dev:devpass@localhost:5432/myapp_dev

# Redis
REDIS_URL=redis://localhost:6379

# API
API_PORT=3000
API_HOST=localhost

# Auth
JWT_SECRET=your-secret-key-here
SESSION_SECRET=your-session-secret

# Email (local)
SMTP_HOST=localhost
SMTP_PORT=1025

# Feature Flags
ENABLE_NEW_FEATURE=false

# External Services (use test keys)
STRIPE_KEY=sk_test_...
SENDGRID_API_KEY=SG.test...
```

---

## 8. IDE Snippets

```json
// .vscode/snippets.code-snippets
{
  "React Component": {
    "prefix": "rfc",
    "body": [
      "import React from 'react';",
      "",
      "interface ${1:ComponentName}Props {",
      "  $2",
      "}",
      "",
      "export const ${1:ComponentName}: React.FC<${1:ComponentName}Props> = (props) => {",
      "  return (",
      "    <div>",
      "      $0",
      "    </div>",
      "  );",
      "};",
      ""
    ],
    "description": "Create React functional component"
  },
  
  "API Route": {
    "prefix": "api",
    "body": [
      "import { Request, Response } from 'express';",
      "",
      "export async function ${1:handlerName}(req: Request, res: Response) {",
      "  try {",
      "    $0",
      "    res.json({ success: true });",
      "  } catch (error) {",
      "    res.status(500).json({ error: error.message });",
      "  }",
      "}",
      ""
    ],
    "description": "Create API route handler"
  }
}
```

---

## 9. Troubleshooting Common Setup Issues

```markdown
# Setup Troubleshooting

## Node version mismatch
\`\`\`bash
# Use .nvmrc
nvm use

# Or install specific version
nvm install 18
nvm use 18
\`\`\`

## Docker not starting
\`\`\`bash
# macOS: Restart Docker Desktop
# Check Docker is running
docker ps

# Reset Docker
docker system prune -a
\`\`\`

## VS Code extensions not working
\`\`\`bash
# Reload window
Cmd+Shift+P → "Reload Window"

# Reinstall extension
code --uninstall-extension <extension-id>
code --install-extension <extension-id>
\`\`\`

## Git SSH issues
\`\`\`bash
# Test SSH connection
ssh -T git@github.com

# Add SSH key to agent
ssh-add ~/.ssh/id_ed25519
\`\`\`
```

---

## 10. Development Environment Checklist

- [ ] **Automated Setup**: One-command machine setup script?
- [ ] **VS Code Config**: Workspace settings committed?
- [ ] **Extensions**: Recommended extensions documented?
- [ ] **Git Config**: Global gitconfig and gitignore?
- [ ] **Shell Config**: Zsh/Bash configuration with aliases?
- [ ] **Docker Compose**: Local services containerized?
- [ ] **Environment Variables**: .env.example provided?
- [ ] **Snippets**: Code snippets for common patterns?
- [ ] **Troubleshooting**: Common issues documented?
- [ ] **Documentation**: Setup guide in README?

---

## Related Skills
- `45-developer-experience/local-dev-standard`
- `45-developer-experience/onboarding-docs`
- `45-developer-experience/hot-reload-fast-feedback`
