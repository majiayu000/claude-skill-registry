---
name: github-repo-architect
description: Repository structure optimization and multi-repo management with swarm coordination for scalable project architecture and development workflows. Use for structure analysis, template management, cross-repo synchronization, and architecture recommendations.
---

# GitHub Repository Architect Skill

## Overview

Repository structure optimization with swarm coordination. This skill handles repository structure analysis, template management, cross-repository synchronization, architecture recommendations, and development workflow optimization.

## Quick Start

```bash
# List repository structure
ls -la

# Search repositories in organization
gh repo list org --limit 20 --json name,description,languages

# Create new repository
gh repo create my-new-repo --public --description "Description"

# Clone repository
gh repo clone owner/repo

# View repository info
gh repo view owner/repo --json name,description,topics
```

## When to Use

- Analyzing repository structure for optimization
- Creating standardized project templates
- Cross-repository synchronization
- Architecture analysis and recommendations
- Multi-repo workflow coordination

## Core Capabilities

| Capability | Description |
|------------|-------------|
| Structure optimization | Best practices implementation |
| Multi-repo coordination | Cross-repo synchronization |
| Template management | Consistent project setup |
| Architecture analysis | Improvement recommendations |
| Workflow coordination | Development process optimization |

## Usage Examples

### 1. Repository Structure Analysis

```javascript
// Initialize architecture analysis swarm
mcp__claude-flow__swarm_init({ topology: "mesh", maxAgents: 4 })
mcp__claude-flow__agent_spawn({ type: "analyst", name: "Structure Analyzer" })
mcp__claude-flow__agent_spawn({ type: "architect", name: "Repository Architect" })
mcp__claude-flow__agent_spawn({ type: "optimizer", name: "Structure Optimizer" })
mcp__claude-flow__agent_spawn({ type: "coordinator", name: "Multi-Repo Coordinator" })

// Orchestrate structure optimization
mcp__claude-flow__task_orchestrate({
    task: "Analyze and optimize repository structure for scalability and maintainability",
    strategy: "adaptive",
    priority: "medium"
})
```

### 2. Analyze Current Structure

```bash
# List repository contents
ls -la

# Find all config files
find . -name "*.json" -o -name "*.yml" -o -name "*.yaml" | head -20

# Analyze package dependencies
cat package.json | jq '.dependencies, .devDependencies'

# Search for related repositories
gh search repos "language:typescript template architecture" \
  --limit 10 \
  --json fullName,description,stargazersCount \
  --sort stars
```

### 3. Create Repository Template

```bash
# Create template repository
gh repo create claude-project-template \
  --public \
  --description "Standardized template for Claude Code projects" \
  --template

# Clone and setup structure
gh repo clone owner/claude-project-template
cd claude-project-template

# Create directory structure
mkdir -p .claude/commands/{github,sparc,swarm}
mkdir -p src tests docs config

# Create core files
cat > package.json << 'EOF'
{
  "name": "claude-project-template",
  "version": "1.0.0",
  "description": "Claude Code project with ruv-swarm integration",
  "engines": { "node": ">=20.0.0" },
  "dependencies": {
    "ruv-swarm": "^1.0.11"
  }
}
EOF

cat > CLAUDE.md << 'EOF'
# Claude Code Configuration

## Quick Start
```bash
npx claude-flow init --sparc
npm install
npx claude-flow start --ui
```

## Features
- ruv-swarm integration
- SPARC development modes
- GitHub workflow automation
EOF

# Commit and push
git add -A
git commit -m "feat: Create standardized project template"
git push
```

### 4. Cross-Repository Synchronization

```bash
# List organization repositories
REPOS=$(gh repo list org --limit 100 --json name --jq '.[].name')

# Update common files across repositories
for repo in $REPOS; do
  echo "Updating $repo..."

  # Clone repo
  gh repo clone org/$repo /tmp/$repo -- --depth=1

  # Update workflow file
  mkdir -p /tmp/$repo/.github/workflows
  cat > /tmp/$repo/.github/workflows/ci.yml << 'EOF'
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with: { node-version: '20' }
      - run: npm install && npm test
EOF

  # Commit and create PR
  cd /tmp/$repo
  git checkout -b standardize-ci
  git add .github/workflows/ci.yml
  git commit -m "ci: Standardize CI workflow"
  git push origin standardize-ci
  gh pr create --title "ci: Standardize CI workflow" --body "Organization-wide standardization"

  cd -
  rm -rf /tmp/$repo
done
```

### 5. Batch Architecture Operations

```javascript
[Single Message - Repository Architecture Review]:
    // Initialize comprehensive architecture swarm
    mcp__claude-flow__swarm_init({ topology: "hierarchical", maxAgents: 6 })
    mcp__claude-flow__agent_spawn({ type: "architect", name: "Senior Architect" })
    mcp__claude-flow__agent_spawn({ type: "analyst", name: "Structure Analyst" })
    mcp__claude-flow__agent_spawn({ type: "optimizer", name: "Performance Optimizer" })
    mcp__claude-flow__agent_spawn({ type: "researcher", name: "Best Practices Researcher" })

    // Analyze current structures
    Bash("ls -la packages/claude-flow/")
    Bash("ls -la packages/ruv-swarm/")
    Read("packages/claude-flow/package.json")
    Read("packages/ruv-swarm/package.json")

    // Search for patterns
    Bash(`gh search repos "language:javascript monorepo" --limit 5 --json fullName,stargazersCount`)

    // Track architecture improvements
    TodoWrite({ todos: [
      { id: "arch-analysis", content: "Analyze current structure", status: "completed" },
      { id: "arch-research", content: "Research best practices", status: "completed" },
      { id: "arch-templates", content: "Create standardized templates", status: "pending" },
      { id: "arch-workflows", content: "Implement improved workflows", status: "pending" },
      { id: "arch-docs", content: "Document architecture decisions", status: "pending" }
    ]})

    // Store analysis results
    mcp__claude-flow__memory_usage({
        action: "store",
        key: "architecture/analysis/results",
        value: JSON.stringify({
            repositories_analyzed: ["claude-flow", "ruv-swarm"],
            optimization_areas: ["structure", "workflows", "templates"],
            recommendations: ["standardize_structure", "improve_workflows"]
        })
    })
```

## Architecture Patterns

### Monorepo Structure

```
project-root/
├── packages/
│   ├── package-a/
│   │   ├── src/
│   │   ├── .claude/
│   │   └── package.json
│   ├── package-b/
│   │   ├── src/
│   │   └── package.json
│   └── shared/
│       ├── types/
│       ├── utils/
│       └── config/
├── tools/
│   ├── build/
│   ├── test/
│   └── deploy/
├── docs/
│   ├── architecture/
│   ├── integration/
│   └── examples/
└── .github/
    ├── workflows/
    ├── templates/
    └── actions/
```

### Command Structure

```
.claude/
├── commands/
│   ├── github/
│   │   ├── github-modes.md
│   │   ├── pr-manager.md
│   │   └── issue-tracker.md
│   ├── sparc/
│   │   ├── sparc-modes.md
│   │   └── coder.md
│   └── swarm/
│       └── coordination.md
├── templates/
│   ├── issue.md
│   ├── pr.md
│   └── project.md
└── config.json
```

### Integration Pattern

```javascript
const integrationPattern = {
    packages: {
        "claude-flow": {
            role: "orchestration_layer",
            dependencies: ["ruv-swarm"],
            provides: ["CLI", "workflows", "commands"]
        },
        "ruv-swarm": {
            role: "coordination_engine",
            dependencies: [],
            provides: ["MCP_tools", "neural_networks", "memory"]
        }
    },
    communication: "MCP_protocol",
    coordination: "swarm_based",
    state_management: "persistent_memory"
}
```

## MCP Tool Integration

### Swarm Coordination

```javascript
mcp__claude-flow__swarm_init({
    topology: "mesh",
    maxAgents: 4,
    strategy: "adaptive"
})

mcp__claude-flow__agent_spawn({
    type: "architect",
    name: "Repository Architect",
    capabilities: ["structure-analysis", "pattern-recognition", "optimization"]
})
```

### Memory for Architecture State

```javascript
mcp__claude-flow__memory_usage({
    action: "store",
    key: "architecture/structure/analysis",
    namespace: "architecture",
    value: JSON.stringify({
        repositories: ["repo1", "repo2"],
        patterns_found: ["monorepo", "microservices"],
        recommendations: ["standardize", "consolidate"]
    })
})
```

## Best Practices

### 1. Structure Optimization
- Consistent directory organization across repositories
- Standardized configuration files and formats
- Clear separation of concerns and responsibilities
- Scalable architecture for future growth

### 2. Template Management
- Reusable project templates for consistency
- Standardized issue and PR templates
- Workflow templates for common operations
- Documentation templates for clarity

### 3. Multi-Repository Coordination
- Cross-repository dependency management
- Synchronized version and release management
- Consistent coding standards and practices
- Automated cross-repo validation

### 4. Documentation Architecture
- Comprehensive architecture documentation
- Clear integration guides and examples
- Maintainable and up-to-date documentation
- User-friendly onboarding materials

## Monitoring and Analysis

### Architecture Health Metrics
- Repository structure consistency score
- Documentation coverage percentage
- Cross-repository integration success rate
- Template adoption and usage statistics

### Automated Analysis
- Structure drift detection
- Best practices compliance checking
- Performance impact analysis
- Scalability assessment and recommendations

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| `github-multi-repo` | Cross-repo synchronization |
| `github-release-manager` | Coordinated releases |
| `sparc-workflow` | Architecture design |
| `agent-orchestration` | Multi-agent coordination |

---

## Version History

- **1.0.0** (2025-01-02): Initial release - converted from repo-architect agent
