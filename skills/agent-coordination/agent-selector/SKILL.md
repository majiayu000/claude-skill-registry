---
skill_name: agent-selector
activation_code: AGENT_SELECTOR_V1
version: 1.0.0
phase: 5.5
prerequisites:
  - PRD with Section 8 (Technical Architecture)
  - PHASE5_COMPLETE signal
outputs:
  - .claude/agent-config.json
  - .claude/agents/ directory
description: |
  Selects and configures agents from the agents repo based on PRD tech stack.
  Runs after task decomposition, before specification generation.
---

# Agent Selector Skill

## Activation

Triggered after Phase 5 (Task Decomposition) completes:

```
[ACTIVATE:AGENT_SELECTOR_V1]
```

## Purpose

Analyze PRD to determine optimal agent selection for the project.

## Execution Flow

### Step 1: Extract Tech Stack from PRD

Read PRD Section 8 (Technical Architecture) and identify:

```yaml
languages:
  - primary: TypeScript
  - secondary: Python

frameworks:
  - frontend: Next.js, React
  - backend: FastAPI

databases:
  - primary: PostgreSQL
  - graph: Neo4j

infrastructure:
  - cloud: AWS
  - containers: Docker, Kubernetes
  - iac: Terraform

special_domains:
  - ml: false
  - blockchain: false
  - gaming: false
  - spatial: false
```

### Step 2: Map to Agents

Use the agent mapping table:

| Tech | Agent |
|------|-------|
| TypeScript | `typescript-pro` |
| Python | `python-pro` |
| Next.js | `nextjs-expert` |
| React | `reactjs-expert` |
| FastAPI | `python-pro` (covers FastAPI) |
| PostgreSQL | `sql-pro` |
| Neo4j | `neo4j-expert` |
| AWS | `aws-expert` |
| Docker | `docker-expert` |
| Kubernetes | `kubernetes-expert` |
| Terraform | `terraform-expert` |

### Step 3: Determine Security Level

From PRD Section 11 (Security Requirements):

| Level | Additional Agents |
|-------|-------------------|
| Standard | `security-auditor` |
| High | `security-auditor`, `penetration-tester` |
| Compliance | `security-auditor`, `compliance-checker` |
| Financial | All security + `compliance-checker` |

### Step 4: Check Scale Requirements

From PRD Section 6 (Non-Functional Requirements):

| Requirement | Additional Agents |
|-------------|-------------------|
| High Performance | `performance-engineer`, `cache-expert` |
| Large Data | `data-engineer`, `database-optimizer` |
| Real-time | `performance-engineer` |

### Step 5: Generate agent-config.json

```json
{
  "version": "1.0.0",
  "source": {
    "local": "agents/",
    "upstream_repo": "https://github.com/turbobeest/agents",
    "note": "Agents bundled locally"
  },
  "agents": {
    "core": {
      "include": [
        "orchestration-intelligence/core-orchestration/orchestrator",
        "orchestration-intelligence/planning-assignment/planning-agent",
        "orchestration-intelligence/quality-control/validation-depth-controller"
      ]
    },
    "auditors": {
      "include": [
        "infrastructure-security/security-compliance/security-auditor",
        "development-architecture/system-architecture/architect-reviewer"
      ]
    },
    "tech-stack": {
      "languages": ["typescript-pro", "python-pro"],
      "frameworks": ["nextjs-expert", "reactjs-expert"],
      "databases": ["sql-pro", "neo4j-expert"],
      "infrastructure": ["aws-expert", "docker-expert", "kubernetes-expert"]
    }
  },
  "phase-gates": {
    "4": ["security-auditor"],
    "8": ["architect-reviewer", "security-auditor"],
    "11": ["security-auditor"]
  }
}
```

### Step 6: Present to User

```
╔═══════════════════════════════════════════════════════════════════════╗
║                         AGENT SELECTION                                ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  Based on your PRD, I recommend the following agents:                 ║
║                                                                        ║
║  CORE (always included):                                              ║
║    • orchestrator         - Pipeline coordination                      ║
║    • planning-agent       - Task planning                              ║
║    • validation-controller - Quality gates                             ║
║                                                                        ║
║  LANGUAGES:                                                            ║
║    • typescript-pro       - TypeScript expertise                       ║
║    • python-pro           - Python/FastAPI expertise                   ║
║                                                                        ║
║  FRAMEWORKS:                                                           ║
║    • nextjs-expert        - Next.js patterns                           ║
║    • reactjs-expert       - React best practices                       ║
║                                                                        ║
║  DATABASES:                                                            ║
║    • sql-pro              - PostgreSQL optimization                    ║
║    • neo4j-expert         - Graph database patterns                    ║
║                                                                        ║
║  INFRASTRUCTURE:                                                       ║
║    • aws-expert           - AWS services                               ║
║    • docker-expert        - Containerization                           ║
║    • kubernetes-expert    - K8s deployment                             ║
║                                                                        ║
║  AUDITORS (phase gates):                                               ║
║    • security-auditor     - Required: Phase 4, 8, 11                   ║
║    • architect-reviewer   - Required: Phase 8                          ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║  [A] Accept  [C] Customize  [S] Skip agents                           ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### Step 7: Sync Agents

On acceptance (agents are bundled locally in `agents/`):

```bash
./scripts/pull-agents.sh --config .claude/agent-config.json
```

### Step 8: Emit Signal

```
[SIGNAL:AGENTS_CONFIGURED]
[ACTIVATE:SPEC_GEN_V1]
```

## Agent Invention

If during any phase, specialized expertise is needed:

1. **Detect Gap**: Skill recognizes missing expertise
2. **Propose Agent**: Generate agent definition

```markdown
---
name: websocket-expert
domain: realtime
role: expert
model: sonnet
description: Real-time WebSocket communication specialist.
tools:
  - Read
  - Write
  - Edit
  - Bash
---

You are an expert in WebSocket and real-time communication...
```

3. **Save**: Write to `.claude/agents/custom/websocket-expert.md`
4. **Register**: Update agent-config.json
5. **Offer Contribution**:

```
New agent created: websocket-expert

Would you like to contribute this agent to the upstream community repo?
[Y] Yes - create PR to turbobeest/agents (upstream)
[N] No - keep local only
```

## Completion

Outputs:
- `.claude/agent-config.json` — Configuration
- `.claude/agents/` — Downloaded agents
- `.claude/.signals/AGENTS_CONFIGURED.json` — Signal

Next phase: Specification (Phase 6)
