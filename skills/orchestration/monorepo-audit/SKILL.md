---
name: monorepo-audit
description: File-to-agent mapping and manifest generation for composite monorepo audits. Provides dynamic discovery of all config agents, generates structured audit manifests with priority-ordered spawn instructions, and handles library vs consumer repo exclusions. Use when performing root-level composite audits that scan repository for all config files and coordinate parallel agent execution across 26+ config domains.
---

# Monorepo Composite Audit Skill

This skill provides the file-to-agent mapping and manifest generation for composite monorepo audits.

## Purpose

Enable monorepo-setup-agent to perform **composite audits** that:

1. Scan repository root for all config files
2. Map each file to its specialized audit agent
3. Generate exact spawn instructions for /ms
4. Consolidate results from all audit agents

---

## Repository Detection

**Use `/skill scope-check` to discover repositories.** The skill scans `/mnt/f/code/`, reads `package.json` files, and classifies repos as library or consumer based on `metasaver.applicationType`.

---

## Core Concept: Agent Manifest

The skill outputs a **structured manifest** that tells /ms exactly which agents to spawn:

```typescript
interface AuditManifest {
  mode: "audit";
  targetPath: string;
  repoType: "library" | "consumer";
  agents: AgentInstruction[];
  excludedPaths: string[];
  totalFiles: number;
}

interface AgentInstruction {
  agent: string; // Agent name from settings.json
  file: string; // Target file/directory to audit
  priority: "critical" | "high" | "medium" | "low";
  taskDescription: string; // Exact description for Task tool
  taskPrompt: string; // Exact prompt for Task tool
}
```

## File-to-Agent Mapping

### Root Configuration Files

| File/Directory                     | Agent                   | Priority | Notes                  |
| ---------------------------------- | ----------------------- | -------- | ---------------------- |
| `turbo.json`                       | turbo-config-agent      | critical | Turborepo pipeline     |
| `package.json`                     | root-package-json-agent | critical | Root package scripts   |
| `pnpm-workspace.yaml`              | pnpm-workspace-agent    | critical | Workspace globs        |
| `tsconfig.json`                    | typescript-agent        | high     | Root TypeScript config |
| `eslint.config.js` or `.eslintrc*` | eslint-agent            | high     | Linting rules          |
| `.prettierrc*`                     | prettier-agent          | high     | Formatting rules       |
| `.editorconfig`                    | editorconfig-agent      | medium   | Editor consistency     |
| `commitlint.config.js`             | commitlint-agent        | high     | Commit validation      |
| `.husky/`                          | husky-agent             | high     | Git hooks              |
| `.github/workflows/`               | github-workflow-agent   | high     | CI/CD pipelines        |
| `.nvmrc`                           | nvmrc-agent             | medium   | Node version           |
| `.vscode/`                         | vscode-agent            | medium   | VS Code settings       |
| `docker-compose.yml`               | docker-compose-agent    | medium   | Dev services           |
| `.dockerignore`                    | dockerignore-agent      | low      | Docker exclusions      |
| `.env.example`                     | env-example-agent       | medium   | Environment template   |
| `.npmrc.template`                  | npmrc-template-agent    | medium   | NPM registry config    |
| `scripts/`                         | scripts-agent           | medium   | Setup scripts          |
| `README.md`                        | readme-agent            | low      | Documentation          |
| `nodemon.json`                     | nodemon-agent           | low      | Dev server config      |
| `vitest.config.ts`                 | vitest-agent            | medium   | Test configuration     |
| `vite.config.ts`                   | vite-agent              | medium   | Build configuration    |
| `tailwind.config.js`               | tailwind-agent          | medium   | CSS framework          |
| `postcss.config.js`                | postcss-agent           | low      | CSS processing         |

### Excluded Paths (Not Audited by Root Agents)

**Consumer Repos (metasaver-com, resume-builder, rugby-crm):**

- `apps/` - Application packages (have own configs)
- `packages/` - Shared libraries (have own configs)
- `services/` - Backend services (have own configs)
- `node_modules/` - Dependencies
- `dist/`, `build/`, `.turbo/`, `.next/` - Build outputs

**Library Repos (multi-mono):**

- `components/` - Shared components
- `config/` - Shared configs (source of truth)
- `packages/` - Published packages
- `node_modules/` - Dependencies
- `dist/`, `build/` - Build outputs

## Discovery Algorithm

**CRITICAL: Always use DYNAMIC DISCOVERY - ensure you scan actual agent directories, not hardcoded lists!**

The Project Manager MUST scan the actual agent directories to discover all available agents:

```bash
# STEP 1: Scan .claude/agents/config/ directories dynamically
find .claude/agents/config -type f -name "*-agent.md" | sort

# This will discover ALL agents, including any newly added ones:
.claude/agents/config/build-tools/docker-compose-agent.md
.claude/agents/config/build-tools/dockerignore-agent.md
.claude/agents/config/build-tools/pnpm-workspace-agent.md
.claude/agents/config/build-tools/postcss-agent.md
.claude/agents/config/build-tools/tailwind-agent.md
.claude/agents/config/build-tools/turbo-config-agent.md
.claude/agents/config/build-tools/vite-agent.md
.claude/agents/config/build-tools/vitest-agent.md
.claude/agents/config/code-quality/editorconfig-agent.md
.claude/agents/config/code-quality/eslint-agent.md
.claude/agents/config/code-quality/prettier-agent.md
.claude/agents/config/version-control/commitlint-agent.md
.claude/agents/config/version-control/gitattributes-agent.md
.claude/agents/config/version-control/github-workflow-agent.md
.claude/agents/config/version-control/gitignore-agent.md
.claude/agents/config/version-control/husky-agent.md
.claude/agents/config/workspace/claude-md-agent.md        # <- NEW!
.claude/agents/config/workspace/env-example-agent.md
.claude/agents/config/workspace/nodemon-agent.md
.claude/agents/config/workspace/npmrc-template-agent.md
.claude/agents/config/workspace/nvmrc-agent.md
.claude/agents/config/workspace/readme-agent.md
.claude/agents/config/workspace/root-package-json-agent.md
.claude/agents/config/workspace/scripts-agent.md
.claude/agents/config/workspace/typescript-agent.md
.claude/agents/config/workspace/vscode-agent.md

TOTAL: 26 config agents (self-discovering, always accurate)
```

**The Project Manager uses DYNAMIC DISCOVERY:**

1. **SCAN directories** - `Glob(".claude/agents/config/**/*-agent.md")`
2. Extract agent names from file paths
3. Group by category (directory name)
4. Batch into waves of 10 (Claude Code max)
5. Spawn all discovered agents with audit instructions
6. Consolidate results

```typescript
// DYNAMIC DISCOVERY - The ONLY source of truth
async function discoverConfigAgents(repoPath: string): Promise<string[]> {
  // Use Glob tool to find ALL agent files
  const agentFiles = await Glob(".claude/agents/config/**/*-agent.md");

  // Extract agent names from file paths
  const agents = agentFiles.map((filePath) => {
    const fileName = filePath.split("/").pop(); // e.g., "claude-md-agent.md"
    return fileName.replace(".md", ""); // e.g., "claude-md-agent"
  });

  console.log(`DISCOVERED ${agents.length} config agents`);
  return agents;
}

// Group by category for reporting
function groupAgentsByCategory(agentFiles: string[]): Record<string, string[]> {
  const categories: Record<string, string[]> = {};

  for (const filePath of agentFiles) {
    // Extract: .claude/agents/config/CATEGORY/agent-name.md
    const parts = filePath.split("/");
    const category = parts[parts.length - 2]; // e.g., "workspace"
    const agentName = parts[parts.length - 1].replace(".md", "");

    if (!categories[category]) {
      categories[category] = [];
    }
    categories[category].push(agentName);
  }

  return categories;
}

// Example output:
// {
//   "build-tools": ["docker-compose-agent", "dockerignore-agent", ...],
//   "code-quality": ["editorconfig-agent", "eslint-agent", "prettier-agent"],
//   "version-control": ["commitlint-agent", "gitattributes-agent", ...],
//   "workspace": ["claude-md-agent", "env-example-agent", "nodemon-agent", ...]
// }

async function discoverAuditTargets(repoPath: string): Promise<AuditManifest> {
  const repoType = detectRepoType(repoPath);
  const agents: AgentInstruction[] = [];

  // Get ALL config agents from categories
  const allAgents: string[] = [];
  for (const category of Object.keys(CONFIG_AGENT_CATEGORIES)) {
    allAgents.push(...CONFIG_AGENT_CATEGORIES[category]);
  }

  console.log(`Found ${allAgents.length} config agents to spawn`);

  // Each agent audits its specific domain
  for (const agentName of allAgents) {
    agents.push({
      agent: agentName,
      priority: getAgentPriority(agentName),
      taskDescription: `Audit ${agentName.replace("-agent", "")} config`,
      taskPrompt: `Audit ${repoPath} for ${agentName.replace("-agent", "")} compliance. Report violations and recommendations.`,
    });
  }

  return {
    mode: "audit",
    targetPath: repoPath,
    repoType: repoType,
    agents: agents,
    totalAgents: allAgents.length,
    excludedPaths: getExcludedPaths(repoType),
  };
}

function getAgentPriority(agentName: string): string {
  const criticalAgents = [
    "turbo-config-agent",
    "pnpm-workspace-agent",
    "root-package-json-agent",
  ];
  const highAgents = [
    "typescript-agent",
    "eslint-agent",
    "prettier-agent",
    "husky-agent",
    "commitlint-agent",
    "github-workflow-agent",
  ];
  const lowAgents = [
    "readme-agent",
    "nodemon-agent",
    "dockerignore-agent",
    "postcss-agent",
  ];

  if (criticalAgents.includes(agentName)) return "critical";
  if (highAgents.includes(agentName)) return "high";
  if (lowAgents.includes(agentName)) return "low";
  return "medium";
}

function getExcludedPaths(repoType: string): string[] {
  if (repoType === "library") {
    return [
      "components/",
      "config/",
      "packages/",
      "node_modules/",
      "dist/",
      "build/",
    ];
  } else {
    return [
      "apps/",
      "packages/",
      "services/",
      "node_modules/",
      "dist/",
      "build/",
      ".turbo/",
      ".next/",
    ];
  }
}
```

**Important:** The discovery agent MUST always run `find .claude/agents -type f -name "*.md"` BEFORE generating the manifest to ensure it discovers what agents are available in the current directory structure.

## Manifest Output Format

The monorepo-setup-agent returns this **exact format** for /ms to execute:

```markdown
## Audit Manifest for /mnt/f/code/resume-builder

**Repository Type:** consumer
**Total Audit Agents:** 15

### Critical Priority (3 agents)

1. Task("turbo-config-agent", "Audit /mnt/f/code/resume-builder/turbo.json for MetaSaver standards")
2. Task("root-package-json-agent", "Audit /mnt/f/code/resume-builder/package.json for MetaSaver standards")
3. Task("pnpm-workspace-agent", "Audit /mnt/f/code/resume-builder/pnpm-workspace.yaml for MetaSaver standards")

### High Priority (5 agents)

4. Task("typescript-agent", "Audit /mnt/f/code/resume-builder/tsconfig.json for MetaSaver standards")
5. Task("eslint-agent", "Audit /mnt/f/code/resume-builder/eslint.config.js for MetaSaver standards")
6. Task("prettier-agent", "Audit /mnt/f/code/resume-builder/.prettierrc.json for MetaSaver standards")
7. Task("commitlint-agent", "Audit /mnt/f/code/resume-builder/commitlint.config.js for MetaSaver standards")
8. Task("husky-agent", "Audit /mnt/f/code/resume-builder/.husky for MetaSaver standards")

### Medium Priority (5 agents)

9. Task("editorconfig-agent", "Audit /mnt/f/code/resume-builder/.editorconfig for MetaSaver standards")
10. Task("nvmrc-agent", "Audit /mnt/f/code/resume-builder/.nvmrc for MetaSaver standards")
11. Task("vscode-agent", "Audit /mnt/f/code/resume-builder/.vscode for MetaSaver standards")
12. Task("env-example-agent", "Audit /mnt/f/code/resume-builder/.env.example for MetaSaver standards")
13. Task("scripts-agent", "Audit /mnt/f/code/resume-builder/scripts for MetaSaver standards")

### Low Priority (2 agents)

14. Task("dockerignore-agent", "Audit /mnt/f/code/resume-builder/.dockerignore for MetaSaver standards")
15. Task("readme-agent", "Audit /mnt/f/code/resume-builder/README.md for MetaSaver standards")

**Excluded Paths:** apps/, packages/, services/, node_modules/, dist/, build/, .turbo/, .next/

**Spawn Strategy:** All agents can run in PARALLEL (no dependencies between root config audits)
```

## Integration with /ms Workflow

### Phase 1: Discovery

```bash
/ms "Composite audit of resume-builder monorepo"

# /ms spawns monorepo-setup-agent in discovery mode
Task("monorepo-setup-agent", "
  MODE: audit-discovery
  TARGET: /mnt/f/code/resume-builder

  Scan the repository root and generate an audit manifest.
  Use the monorepo-audit skill to map files to agents.
  Return the exact Task calls needed for Phase 2.
  Only discover what needs auditing - do not execute audits.
")
```

### Phase 2: Execution

```bash
# /ms reads manifest from Phase 1 and spawns all agents in ONE message
Task("turbo-config-agent", "Audit /mnt/f/code/resume-builder/turbo.json...")
Task("root-package-json-agent", "Audit /mnt/f/code/resume-builder/package.json...")
Task("pnpm-workspace-agent", "Audit /mnt/f/code/resume-builder/pnpm-workspace.yaml...")
# ... all 15 agents in parallel
```

### Phase 3: Consolidation

```bash
# /ms spawns monorepo-setup-agent with all results
Task("monorepo-setup-agent", "
  MODE: audit-consolidate
  TARGET: /mnt/f/code/resume-builder

  Consolidate these audit results:

  turbo-config-agent: [results]
  root-package-json-agent: [results]
  ...

  Provide unified audit report with:
  - Total violations by priority
  - Pass/fail status per config
  - Top recommendations
")
```

## Best Practices

1. **Scan before spawning** - Always discover what exists first
2. **Parallel execution** - Root configs have no dependencies
3. **Priority ordering** - Critical configs first in manifest
4. **Exclude workspace packages** - They have their own configs
5. **Exact prompts** - Manifest provides copy-paste Task calls
6. **Consistent format** - Same manifest structure for all repos
7. **Library vs Consumer** - Different exclusions based on repo type

## Example: Multi-Repo Composite Audit

```bash
/ms "Composite audit of all 4 MetaSaver monorepos"

# Phase 1: Spawn 4 monorepo-setup-agents for discovery
Task("monorepo-setup-agent", "MODE: audit-discovery, TARGET: /mnt/f/code/resume-builder")
Task("monorepo-setup-agent", "MODE: audit-discovery, TARGET: /mnt/f/code/multi-mono")
Task("monorepo-setup-agent", "MODE: audit-discovery, TARGET: /mnt/f/code/rugby-crm")
Task("monorepo-setup-agent", "MODE: audit-discovery, TARGET: /mnt/f/code/metasaver-com")

# Each returns manifest of ~15 agents
# Total agents needed: ~60 (but run max 10 at a time)

# Phase 2: Execute in batches of 10
# Phase 3: Consolidate all results
```

## Integration with Existing Skills

This skill integrates with:

- `/skill audit-workflow` - Uses bi-directional comparison
- `/skill remediation-options` - Offers conform/update/ignore for violations
- Repository type provided via `scope` parameter. If not provided, use `/skill scope-check`

The monorepo-audit skill is the **orchestration layer** that coordinates all other audit skills.
