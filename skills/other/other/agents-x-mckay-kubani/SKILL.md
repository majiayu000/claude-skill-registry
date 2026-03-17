---
name: agents
description: Manage and develop AI agents using kubani CLI. Use for checking agent health, versions, deployment status, running tests, evaluations, and managing Nexus proactive background missions.
---

# AI Agents Management

Manage AI agents using the kubani CLI and cluster tools.

## Quick Commands

```bash
# Create a new agent automatically (NEW!)
kubani agent draft --name my-agent --description "..."

# Check agent creation status
kubani agent status my-agent

# List all agents with status
kubani agents list

# Run agent locally with hot-reload
kubani run k8s-monitor --hot-reload

# Run agent tests
kubani test k8s-monitor

# Run evaluation suite
kubani eval k8s-monitor

# View execution traces
kubani trace k8s-monitor

# Start observability dashboard
kubani dashboard
```

## Nexus Proactive Missions

The Nexus agent supports background missions — scheduled, autonomous tasks that run without user interaction. Missions are dispatched by the `NexusHeartbeatWorkflow` Temporal Schedule (every 1 minute) and executed as bounded `run_mission_agent_turn` activities.

### Mission Management

```bash
# Register the heartbeat Temporal Schedule (run once on cluster setup)
python -c "
from kubani.nexus.orchestrator.worker import register_heartbeat_schedule
import asyncio
asyncio.run(register_heartbeat_schedule())
"

# Apply the missions DB schema migration
kubectl apply -f infrastructure/gitops/apps/nexus/missions-migration-job.yaml

# View active missions
psql $NEXUS_DATABASE_URL -c "SELECT id, title, status, schedule, next_run_at FROM nexus_missions WHERE status='active';"

# View recent mission runs
psql $NEXUS_DATABASE_URL -c "SELECT mission_id, status, tool_calls_made, found_anomaly, duration_ms FROM nexus_mission_runs ORDER BY started_at DESC LIMIT 20;"

# Pause the heartbeat schedule (stops all missions)
temporal schedule pause --schedule-id nexus-heartbeat

# Resume the heartbeat schedule
temporal schedule unpause --schedule-id nexus-heartbeat
```

### Mission Policies

| Policy | Allowed MCP Servers | Use Case |
|---|---|---|
| `nexus` | memory, skills, fetch | Safe missions (research, summarisation) |
| `nexus-proactive` | + kubernetes, discord, temporal | Cluster monitoring missions |

Destructive operations in `nexus-proactive` (delete, scale, exec) require HITL approval.

## Arguments

- `agent-name`: Optional specific agent name for detailed info

## Instructions

### List All Agents

```bash
cd /home/al/git/kubani
echo "=== AI Agents ==="
echo ""

for earthfile in agents/*/Earthfile; do
    agent_dir=$(dirname "$earthfile")
    agent_name=$(basename "$agent_dir")
    [ "$agent_name" = "core" ] && continue

    # Get version from pyproject.toml
    version=$(grep '^version = ' "$agent_dir/pyproject.toml" | sed 's/version = "\(.*\)"/\1/')

    # Get deployed image
    deployed=$(KUBECONFIG=/home/al/.kube/config kubectl get deploy $agent_name -n ai-agents -o jsonpath='{.spec.template.spec.containers[0].image}' 2>/dev/null || echo "not deployed")

    # Get pod status
    status=$(KUBECONFIG=/home/al/.kube/config kubectl get pods -n ai-agents -l app.kubernetes.io/name=$agent_name -o jsonpath='{.items[0].status.phase}' 2>/dev/null || echo "unknown")

    echo "$agent_name"
    echo "  Source version: $version"
    echo "  Deployed image: $deployed"
    echo "  Pod status: $status"
    echo ""
done
```

### Development Workflow

Use kubani for agent development:

```bash
# Initialize configuration (one-time)
kubani init

# Run agent with hot-reload
kubani run k8s-monitor --hot-reload

# Run with mock services (for offline development)
kubani run k8s-monitor --mock-mcp --mock-redis

# Run tests
kubani test k8s-monitor --coverage

# Run evaluation suite
kubani eval k8s-monitor

# Run specific evaluation layer
kubani eval k8s-monitor --layer llm
```

### Detailed Agent Info

For a specific agent, show detailed information:

```bash
AGENT_NAME="k8s-monitor"

# Pod details
KUBECONFIG=/home/al/.kube/config kubectl get pods -n ai-agents -l app.kubernetes.io/name=$AGENT_NAME -o wide

# Recent logs
KUBECONFIG=/home/al/.kube/config kubectl logs -n ai-agents -l app.kubernetes.io/name=$AGENT_NAME --tail=20

# Recent deployment history
git log --oneline -5 gitops/apps/ai-agents/$AGENT_NAME/deployment.yaml

# View traces
kubani trace $AGENT_NAME --last 10

# View metrics
kubani metrics $AGENT_NAME
```

### Build and Deploy

```bash
# Build agent container
kubani build k8s-monitor

# Deploy to cluster
kubani deploy k8s-monitor

# Rollback deployment
kubani deploy k8s-monitor --rollback
```

### Create New Agent

```bash
# Create from default template
kubani new my-agent

# Create with federated template
kubani new my-agent --template federated
```

## Framework

The `kubani/framework/` package provides shared functionality:

```bash
# Key modules:
# - config.py: Unified configuration system
# - events/: Event bus with hybrid event types
# - mcp/: MCP client
# - llm.py: LLM integration
# - registry/: Service registry
```

## Architecture

```
kubani/
├── framework/                # Core framework
│   ├── config.py            # Unified configuration
│   ├── events/              # Event bus (hybrid types)
│   ├── mcp/                 # MCP client
│   └── registry/            # Service registry
├── agents/                   # Reusable agent implementations
│   ├── _base/               # Base agent class (KubaniAgent)
│   ├── critic/              # Execution evaluation (learning)
│   ├── reflection/          # Cross-agent insights (learning)
│   ├── skill_synthesizer/   # Skill proposal (learning)
│   ├── event_classifier/    # Event classification
│   ├── remediator/          # Remediation actions
│   └── ...                  # Other specialized agents
├── syndicates/               # Multi-agent orchestration
│   ├── _base/               # Base syndicate class
│   ├── k8s_monitor/         # Kubernetes monitoring
│   ├── news_digest/         # News aggregation
│   └── learning_system/     # Continuous learning (Critic + Reflection + Synthesizer)
├── nexus/                    # Nexus agent (always-on, proactive)
│   ├── orchestrator/        # Temporal workflows and activities
│   │   ├── workflow.py      # NexusOrchestratorWorkflow (proactive_mission signal)
│   │   ├── heartbeat_workflow.py  # NexusHeartbeatWorkflow (cron dispatcher)
│   │   ├── activities.py    # run_agent_turn, run_mission_agent_turn
│   │   └── worker.py        # Worker + register_heartbeat_schedule
│   ├── missions/            # Mission CRUD, scheduler, activities
│   ├── models/              # NexusMission, NexusMissionRun models
│   └── tools/               # MCP clients (policy-aware), security
└── mcp/servers/              # MCP server implementations
```

## Learning System

The continuous learning system runs as a syndicate (`kubani/syndicates/learning_system/`):

```python
from kubani.syndicates.learning_system import LearningSystemSyndicate
from kubani.agents.critic import CriticAgent
from kubani.agents.reflection import ReflectionAgent
from kubani.agents.skill_synthesizer import SkillSynthesizerAgent

# Run the full learning system
syndicate = LearningSystemSyndicate()
await syndicate.start()
```
