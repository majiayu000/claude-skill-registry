---
name: vibery-manager
description: Unified management for Vibery monorepo (templates, kits, CLI, website). Use /template, /kit, /sync, /publish, /deploy commands.
version: 1.4.0
---

# Vibery Manager

Unified workflow for managing the Vibery monorepo.

## Available Commands

| Command                          | Description                                       |
| -------------------------------- | ------------------------------------------------- |
| `/template create <type> <name>` | Create new template (agent, command, skill, etc.) |
| `/template list [--type TYPE]`   | List all templates                                |
| `/template pull <source>`        | Pull from git repo or local path                  |
| `/kit create <name>`             | Create new kit scaffold                           |
| `/kit add <kit> <item>`          | Add template/skill to kit                         |
| `/kit remove <kit> <item>`       | Remove item from kit                              |
| `/kit list [kit-name]`           | List kits or kit contents                         |
| `/sync`                          | Sync templates + generate manifest                |
| `/publish`                       | Push to GitHub (templates repo)                   |
| `/deploy`                        | Alias for `/sync` + `/publish` (one command)      |

## Architecture

```
vibery-studio/templates (GitHub)     ← Single source of truth
├── agents/*.md
├── commands/*.md
├── skills/*/
├── mcps/*.json
├── hooks/*.json
├── settings/*.json
├── registry.json                    ← Template catalog
└── templates-manifest.json          ← File listing (no API needed)

vibe-templates/ (local)
├── templates/                       ← Maps to vibery-studio/templates
├── cli/                             ← npm package "vibery"
├── stacks/                          ← Kits
└── website/                         ← kits.vibery.app
```

## How CLI Fetches Templates (No Rate Limits)

1. CLI fetches `templates-manifest.json` via raw GitHub URL
2. Manifest lists all files per template type
3. CLI downloads files via raw URLs (no GitHub API = no rate limits)
4. Fallback to bundled templates if network fails

**Key**: Raw GitHub URLs (`raw.githubusercontent.com`) have NO rate limits.

## Deployment Flow

**Add new template (no CLI publish needed):**

```bash
# 1. Create template
/template create agent my-new-agent

# 2. Sync + generate manifest
/sync

# 3. Push to GitHub
/publish

# Done! npx vibery install my-new-agent works immediately
```

**What `/sync` does:**

1. Runs `node scripts/sync-all.js` (registry + website data)
2. Runs `node cli/scripts/generate-templates-manifest.js` (manifest)
3. Copies manifest to templates/

**What `/publish` does:**

1. `cd templates && git add . && git commit && git push`

**CLI auto-fetches** from GitHub raw URLs (no npm publish needed for template updates).

## Quick Workflow

### Create Template

```bash
/template create agent security-auditor
# Or manually:
echo "---
name: my-agent
description: What it does
---
# Content" > templates/agents/my-agent.md
```

### Create Kit

```bash
/kit create backend-stack
/kit add backend-stack databases
/kit add backend-stack api-security
```

### Deploy Everything

```bash
/deploy         # One command: sync + push to GitHub + deploy website
```

## Script Locations

| Script                                                   | Purpose                          |
| -------------------------------------------------------- | -------------------------------- |
| `scripts/sync-all.js`                                    | Templates → CLI + website        |
| `cli/scripts/generate-templates-manifest.js`             | Generate templates-manifest.json |
| `.claude/skills/vibery-manager/scripts/manage.py`        | Kit management + kit sync        |
| `.claude/skills/vibery-manager/scripts/validate-kits.py` | Validate kit structures          |

## Deployment Targets

| Target      | URL/Package             | Update Method             |
| ----------- | ----------------------- | ------------------------- |
| **GitHub**  | vibery-studio/templates | `/publish` → git push     |
| **CLI**     | `npx vibery`            | Auto-fetches from GitHub  |
| **Website** | https://kits.vibery.app | Separate deploy if needed |

**Note**: CLI npm package only needs update for CODE changes, not template updates.

## Generated Files

| Source        | Output                              | Used By             |
| ------------- | ----------------------------------- | ------------------- |
| `templates/*` | `templates/templates-manifest.json` | CLI (remote fetch)  |
| `templates/*` | `templates/registry.json`           | CLI (template list) |
| `templates/*` | `website/src/data/templates.json`   | Website             |
| `stacks/*`    | `website/src/data/kits.json`        | Website             |
| `stacks/*`    | `cli/kits.json`                     | CLI                 |

## Workflow Examples (Multi-Context Prompts)

### Example 1: Create New Kit

**Context 1 - Plan:**

```
I want to create a "devops-essentials" kit with Docker, CI/CD, and monitoring templates.
What agents and skills should I include?
```

**Context 2 - Execute:**

```
/kit create devops-essentials
/kit add devops-essentials docker-pro
/kit add devops-essentials ci-cd-automation
/kit add devops-essentials monitoring-setup
```

**Context 3 - Deploy:**

```
/deploy
```

---

### Example 2: Add Template + Update Kit

**Context 1 - Create template:**

```
Create an agent for Kubernetes deployment optimization.
Save it as templates/agents/k8s-optimizer.md
```

**Context 2 - Add to existing kit:**

```
/kit add devops-essentials k8s-optimizer
```

**Context 3 - Deploy:**

```
/deploy
```

---

### Example 3: Pull External Templates + Bundle

**Context 1 - Import:**

```
/template pull https://github.com/someone/awesome-agents
```

**Context 2 - Create bundle:**

```
/kit create imported-stack
/kit add imported-stack agent-from-pull-1
/kit add imported-stack agent-from-pull-2
```

**Context 3 - Deploy:**

```
/deploy
```

---

### Example 4: Quick Single Template

```bash
/template create agent payment-gateway-pro
# ... edit the template ...
/deploy
```

---

### Daily Workflow Summary

| Step           | Command                             | Notes                             |
| -------------- | ----------------------------------- | --------------------------------- |
| 1. Create/edit | `/template create` or `/kit create` |                                   |
| 2. Add items   | `/kit add <kit> <item>`             |                                   |
| 3. Validate    | `python scripts/validate-kits.py`   | Optional                          |
| 4. Sync        | `/sync`                             | JS for templates, Python for kits |
| 5. Deploy      | `/publish`                          | Build + Cloudflare                |

## Troubleshooting

### Templates empty on website

```bash
node scripts/sync-all.js   # Use JS, not Python!
cd website && npm run build
npx wrangler pages deploy dist --project-name=vibery-kits
```

### Kit validation errors

```bash
python .claude/skills/vibery-manager/scripts/validate-kits.py
```
