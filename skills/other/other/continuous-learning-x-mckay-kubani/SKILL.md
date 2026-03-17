---
name: continuous-learning
description: Voyager-inspired continuous learning system with Critic Agent, Reflection Agent, and Discord-based approval workflow for skill proposals.
---

# Continuous Learning System

The continuous learning system enables agents to improve over time through automated analysis, pattern recognition, and skill synthesis.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Learning System                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   Critic    │───▶│ Reflection  │───▶│ Synthesizer │         │
│  │   Agent     │    │   Agent     │    │             │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│        │                  │                   │                 │
│        ▼                  ▼                   ▼                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Shared Memory System                        │   │
│  │  (Qdrant + Neo4j + Redis via Memory MCP)                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Discord Approval Workflow                   │   │
│  │  (Skill proposals → Team review → Auto-deploy)          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### Critic Agent

Evaluates agent executions and provides structured feedback:

```python
from kubani.agents.critic import CriticAgent

critic = CriticAgent()

# Evaluate recent executions (used by syndicate)
evaluations = await critic.evaluate_recent_executions(
    hours=24,
    agent_id="k8s-monitor",  # Optional filter
)

# Each evaluation contains:
# - overall_score: 0.0-1.0
# - success: bool
# - feedback: Detailed analysis
# - patterns_identified: Reusable patterns
```

### Reflection Agent

Synthesizes learnings across agents and identifies cross-cutting patterns:

```python
from kubani.agents.reflection import ReflectionAgent
from kubani.agents.reflection.models import ReflectionResult, InsightType

reflection = ReflectionAgent()
result: ReflectionResult = await reflection.reflect(
    time_window_hours=168,  # Look back 1 week
    min_evaluations=10,
)

# Returns ReflectionResult with:
# - patterns: List[ReflectionInsight] - Recurring patterns
# - anti_patterns: List[ReflectionInsight] - Things to avoid
# - best_practices: List[ReflectionInsight] - Recommended approaches
# - knowledge: List[ReflectionInsight] - Learned facts
# - skill_opportunities: List[ReflectionInsight] - Potential new skills
# - evaluations_analyzed: int
# - agents_analyzed: List[str]
```

### Skill Synthesizer Agent

Proposes new skills based on successful patterns:

```python
from kubani.agents.skill_synthesizer import SkillSynthesizerAgent

synthesizer = SkillSynthesizerAgent()
result = await synthesizer.synthesize_skills()

# Returns SynthesisResult with:
# - proposals_created: int
# - proposals_posted: int (sent to Discord for approval)
# - proposals: List[SkillProposal]
#   Each proposal has:
#   - skill_name: str
#   - skill_content: str (full SKILL.md content)
#   - confidence: float (0.0-1.0)
#   - supporting_evidence: List[str]
```

## Discord Approval Workflow

### Skill Proposals

When a skill is proposed, it's posted to Discord for review:

```
🆕 New Skill Proposal: k8s/oom-remediation

📋 Description:
Automated remediation for OOM killed pods including
memory analysis and scaling recommendations.

📊 Confidence: 0.87
📈 Based on: 12 successful executions

React to approve:
✅ Approve and deploy
❌ Reject
🔄 Request modifications
```

### Approval Flow

1. **Proposal Posted**: Skill proposal appears in `#learning-proposals`
2. **Team Review**: Team members review and react
3. **Threshold Met**: If ✅ reactions >= threshold, skill is approved
4. **Auto-Deploy**: Approved skills are automatically:
   - Added to the skills library
   - Synced to the registry
   - Available to all agents

### Configuration

```yaml
# config.yaml
learning:
  enabled: true
  critic_enabled: true
  reflection_enabled: true
  auto_approve_threshold: 0.95  # Auto-approve if confidence >= 0.95
  require_discord_approval: true
  min_examples_for_skill: 3
  approval_timeout_hours: 72

discord:
  learning_channel: "learning-proposals"
  approval_reactions:
    approve: "✅"
    reject: "❌"
    modify: "🔄"
  approval_threshold: 2  # Number of approvals needed
```

## Learning System Syndicate

The learning system runs as a syndicate that orchestrates the three agents:

```python
from kubani.syndicates.learning_system import LearningSystemSyndicate

# Run the full learning system
syndicate = LearningSystemSyndicate()
await syndicate.start()

# The syndicate runs three concurrent loops:
# - Critic evaluation (configurable interval, default hourly)
# - Reflection synthesis (configurable interval, default daily)
# - Skill synthesis (configurable interval, default weekly)

# Manual triggers are also available:
await syndicate.trigger_evaluation(agent_id="k8s-monitor")
await syndicate.trigger_reflection()
await syndicate.trigger_synthesis()
```

### Event Architecture

The learning system uses hybrid events:

```python
# Framework events (kubani/framework/events/types.py)
from kubani.framework.events import EventType
# EventType.AGENT_EXECUTION_COMPLETE - triggers learning

# Domain events (kubani/syndicates/learning_system/events.py)
EVALUATION_COMPLETE = "learning:evaluation_complete"
REFLECTION_COMPLETE = "learning:reflection_complete"
SKILL_PROPOSED = "learning:skill_proposed"
SKILL_APPROVED = "learning:skill_approved"
SKILL_REJECTED = "learning:skill_rejected"
```

## Memory Integration

### Storing Learnings via MCP

```python
from kubani.framework.mcp import get_mcp_client

client = get_mcp_client()

# Store a learning
await client.memory.store_learning(
    agent_id="k8s-monitor",
    learning_type="pattern",  # pattern, anti_pattern, insight, fact
    content="OOM kills in production often indicate need for VPA",
    confidence=0.85,
    context={"namespace": "production", "pod": "api-server"},
)
```

### Querying Learnings

```python
# Semantic search via MCP
results = await client.memory.search_learnings(
    query="kubernetes memory issues",
    agent_id="k8s-monitor",  # Optional filter
    limit=10,
)
```

## Commands

### View Learning Status

```bash
# View learning system status
kubani learning status

# View recent learnings
kubani learning list --agent k8s-monitor --last 24h

# View pending proposals
kubani learning proposals
```

### Trigger Learning Cycle

```bash
# Run critic evaluation manually
kubani learning evaluate --agent k8s-monitor

# Run reflection cycle
kubani learning reflect

# Propose skill from pattern
kubani learning propose --pattern pattern-123
```

### Manage Approvals

```bash
# List pending approvals
kubani learning approvals

# Approve a proposal (CLI fallback)
kubani learning approve --proposal proposal-456

# Reject a proposal
kubani learning reject --proposal proposal-456 --reason "Needs more examples"
```

## Best Practices

1. **Start with critic enabled** to collect execution data
2. **Review proposals carefully** before approving
3. **Set appropriate thresholds** for auto-approval
4. **Monitor the learning channel** for new proposals
5. **Provide feedback** on rejected proposals
6. **Track skill effectiveness** after deployment
7. **Periodically review** the knowledge graph

## Monitoring

View learning metrics in the dashboard:

```bash
kubani dashboard
# Navigate to: http://localhost:8080/learning
```

Dashboard shows:
- Learning rate over time
- Skill proposal success rate
- Pattern identification trends
- Knowledge graph visualization
- Agent improvement metrics
