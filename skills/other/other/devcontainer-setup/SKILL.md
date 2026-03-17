---
name: devcontainer-setup
description: Standardized DevContainer setup for Python3.13 development environments. Use when initializing a new project, adding DevContainer support, or standardizing tool versions across a team.
---

# DevContainer Setup

## Core Principle

**Environment as Code. Consistent, reproducible, and isolated.**

Development environments should be defined in code, version controlled, and identical for all team members. This eliminates "works on my machine" issues and streamlines onboarding.

---

**This skill defines the complete DevContainer setup. Follow it step by step. DO NOT add extensions, features, or configurations not explicitly listed in this skill.**

If you identify something the project might need beyond this skill:
1. **STOP** - Do not add it
2. **Ask** the user: "I think you might benefit from [X] because [reason]. Would you like me to add it?"
3. **Wait** for explicit user approval
4. Proceed only after "yes" confirmation

**Examples of things you must NOT add without asking:**
- Extra VS Code extensions
- Different base images
- Additional features beyond what's specified
- Custom configurations

**Trust the default.** This skill covers the common cases.

---

## When to Use

Use this skill when:
- Initializing a new project from scratch
- Adding DevContainer support to an existing project
- Standardizing tool versions (Python, Node, etc.) across the team
- Automating environment setup (extensions, dependencies)

**Supplementary docs (same directory as this skill):**
- `WEB_DEVELOPMENT.md` — Port forwarding, Vite/React issues in devcontainer
  - Read this file if user has web dev networking issues

---

## Step 0: Gather Requirements

**First, ask the user:**

"Do you want the **default setup** (recommended) or **advanced** (customize each option)?"
- **Default** → Record all variables as `yes`, skip to Step 1
- **Advanced** → Ask the detailed questions below

**⛔ STOP - Wait for user response before proceeding to Step 1.**

---

### Default Setup (Recommended)

Sets all options to `yes`:
```
[DOCKER]=yes, [GH_CLI]=yes, [NODE_FEATURE]=yes, [ENV_MODULE]=yes, [POSTCREATE]=yes
```

This gives you: Docker CLI, GitHub CLI, Node.js tooling, .env secrets management, and post-create automation.

**If user chose "Default": Execute Steps 1-7 immediately. DO NOT analyze the project, detect frameworks, or adapt the configuration. DO NOT read project files to customize. Follow the skill exactly as written.**

---

### Advanced Setup (Customize)

**Only if user chose "Advanced", ask these questions:**

"Do you need any of these additional tools?"
- **Docker CLI (build/run containers inside the dev container)** → Record `[DOCKER]=yes`
- **GitHub CLI (`gh`)** → Record `[GH_CLI]=yes`
- **Node.js runtime (npm)** with Python base → Record `[NODE_FEATURE]=yes`

"Do you want credential/secrets management via `.env`?"
- **Yes** → Record `[ENV_MODULE]=yes`
- **No** → Record `[ENV_MODULE]=no`

"Do you want post-create automation (install deps, run setup scripts)?"
- **Yes** → Record `[POSTCREATE]=yes`
- **No** → Record `[POSTCREATE]=no`

---

## Step 1: Create Directory Structure

```bash
mkdir -p .devcontainer
```

---

## Step 2: Create Dockerfile

```bash
cat > .devcontainer/Dockerfile << 'EOF'
ARG VARIANT="3.13-bookworm"
FROM mcr.microsoft.com/devcontainers/python:${VARIANT}

USER root
RUN pip install --no-cache-dir uv \
    && uv --version
USER vscode
EOF
```

---

## Step 3: Create devcontainer.json

### Base Configuration

Start with this minimal config:

```bash
cat > .devcontainer/devcontainer.json << 'EOF'
{
  "name": "Dev Container",
  "build": {
    "dockerfile": "Dockerfile",
    "context": "..",
    "args": {}
  },
  "remoteEnv": {
    "PYTHONPATH": "${containerWorkspaceFolder}/src:${containerWorkspaceFolder}"
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-toolsai.jupyter",
        "bierner.markdown-mermaid"
      ],
      "settings": {
        "editor.formatOnSave": true,
        "editor.bracketPairColorization.enabled": true,
        "editor.guides.bracketPairs": "active",
        "debug.allowBreakpointsEverywhere": true
      }
    }
  }
}
EOF
```



---

## Step 4: Add Features (If Needed)

**If any of [GH_CLI], [DOCKER], [NODE_FEATURE] = yes:**

Add a `features` block to `devcontainer.json`:

```jsonc
{
  "features": {
    // Always include git:
    "ghcr.io/devcontainers/features/git:1": {},
    
    // If [GH_CLI] = yes:
    "ghcr.io/devcontainers/features/github-cli:1": {},
    
    // If [DOCKER] = yes:
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    
    // If [NODE_FEATURE] = yes (Python base + Node runtime):
    "ghcr.io/devcontainers/features/node:1": { "version": "lts" }
  }
}
```

**Note:** The Python base image does NOT include Node.js. If the user needs npm for development scripts, you MUST add the Node feature.

---

## Step 5: Add .env Module (If [ENV_MODULE] = yes)

### Create .env.example:

```bash
cat > .devcontainer/.env.example << 'EOF'
GITHUB_USER=
GITHUB_TOKEN=
INSTALL_AZURE_CLI=false
EOF
```

### Create .gitignore for secrets:

```bash
echo ".env" >> .devcontainer/.gitignore
```

### Add to devcontainer.json:

Add these properties to the JSON:

```jsonc
{
  "initializeCommand": "touch .devcontainer/.env",
  "runArgs": ["--env-file", ".devcontainer/.env"]
}
```

---

## Step 6: Add postCreate Automation (If [POSTCREATE] = yes)

### Create postCreate.sh:

```bash
cat > .devcontainer/postCreate.sh << 'EOF'
#!/bin/bash
set -e

# Configure GitHub credentials if provided
if [ -n "${GITHUB_USER:-}" ] && [ -n "${GITHUB_TOKEN:-}" ]; then
  echo "Configuring GitHub credentials..."
  printf 'https://%s:%s@github.com\n' "$GITHUB_USER" "$GITHUB_TOKEN" >> "$HOME/.git-credentials"
  chmod 600 "$HOME/.git-credentials" || true
  git config --global credential.helper store
  git config --global credential.useHttpPath true
fi

# Install Azure CLI (optional)
if [ "${INSTALL_AZURE_CLI:-false}" = "true" ]; then
  echo "Installing Azure CLI..."
  curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash || echo "Azure CLI installation failed (non-blocking)"
else
  echo "Skipping Azure CLI (set INSTALL_AZURE_CLI=true to enable)"
fi

echo "postCreate done"
EOF
```

### Make executable:

```bash
chmod +x .devcontainer/postCreate.sh
```

### Add to devcontainer.json:

```jsonc
{
  "postCreateCommand": "bash .devcontainer/postCreate.sh"
}
```

---

## Step 7: Verify and Complete

**Run verification:**

```bash
# Check files exist
ls -la .devcontainer/

# Validate JSON syntax
cat .devcontainer/devcontainer.json | python3 -m json.tool > /dev/null && echo "JSON OK"

# Check script is executable (if created)
test -x .devcontainer/postCreate.sh && echo "postCreate.sh executable" || true
```

**Success criteria:**
- [ ] `.devcontainer/Dockerfile` exists
- [ ] `.devcontainer/devcontainer.json` is valid JSON
- [ ] Extensions match the runtime
- [ ] Features added based on user requirements
- [ ] postCreate.sh is executable (if used)

**Report to user:** "DevContainer created. Run 'Reopen in Container' from VS Code command palette."

---

## Quick Reference

```
Setup modes:
  Default (recommended): All options = yes
  Advanced:              Customize each option

Variables to capture:
  [DOCKER]        = yes | no
  [GH_CLI]        = yes | no
  [NODE_FEATURE]  = yes | no  (Node.js runtime: npm)
  [ENV_MODULE]    = yes | no
  [POSTCREATE]    = yes | no

Default setup (yes to all):
  .devcontainer/
  ├── Dockerfile
  ├── devcontainer.json   ← All features enabled
  ├── .env.example
  ├── .gitignore
  └── postCreate.sh

Minimal setup (advanced, all no):
  .devcontainer/
  ├── Dockerfile          ← Python base only
  └── devcontainer.json
```

---

## Decision Tree

```
User says "I want a DevContainer"
│
├─► Ask: "Default or Advanced?"
│
├─► If Default: Set all = yes, execute Steps 1-7
│
└─► If Advanced:
    ├─► Ask: "Docker inside?" → [DOCKER]
    ├─► Ask: "GitHub CLI?" → [GH_CLI]
    ├─► Ask: "Need Node.js tooling?" → [NODE_FEATURE]
    ├─► Ask: "Secrets via .env?" → [ENV_MODULE]
    ├─► Ask: "Post-create scripts?" → [POSTCREATE]
    └─► Execute Steps 1-7 based on recorded values
```
