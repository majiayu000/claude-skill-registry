# Flow Nexus Cloud Swarm Deployment SOP

```yaml
metadata:
  skill_name: when-deploying-cloud-swarm-use-flow-nexus-swarm
  version: 1.0.0
  category: platform-integration
  difficulty: advanced
  estimated_duration: 40-70 minutes
  trigger_patterns:
    - "deploy cloud swarm"
    - "flow nexus swarm"
    - "distributed workflow"
    - "event-driven agents"
    - "cloud agent coordination"
  dependencies:
    - flow-nexus MCP server
    - Claude Flow hooks
    - E2B account (optional)
  agents:
    - hierarchical-coordinator (swarm orchestrator)
    - flow-nexus-swarm (cloud platform manager)
    - adaptive-coordinator (dynamic optimization)
  success_criteria:
    - Swarm initialized successfully
    - Agents deployed to cloud
    - Workflows executing correctly
    - Performance metrics tracked
    - Auto-scaling functional
```

## Overview

Deploy cloud-based AI agent swarms with event-driven workflow automation using Flow Nexus platform. Supports hierarchical, mesh, ring, and star topologies with E2B sandbox distribution.

## Prerequisites

**Required:**
- Flow Nexus MCP server installed
- Flow Nexus account (authenticated)
- Basic understanding of swarm patterns

**Optional:**
- E2B API key for cloud sandboxes
- Anthropic API key for Claude Code
- Existing workflow definitions

**Verification:**
```bash
# Check Flow Nexus availability
npx flow-nexus@latest --version

# Verify authentication
mcp__flow-nexus__auth_status
```

## Agent Responsibilities

### hierarchical-coordinator (Swarm Orchestrator)
**Role:** Coordinate multi-level swarm hierarchy, manage agent lifecycles, optimize task distribution

**Expertise:**
- Hierarchical swarm patterns
- Task decomposition
- Agent coordination
- Resource allocation

**Output:** Swarm topology, agent assignments, coordination protocols

### flow-nexus-swarm (Cloud Platform Manager)
**Role:** Manage Flow Nexus platform integration, E2B sandbox deployment, cloud resources

**Expertise:**
- Flow Nexus platform APIs
- E2B sandbox management
- Cloud infrastructure
- Distributed systems

**Output:** Cloud deployment, sandbox configuration, resource management

### adaptive-coordinator (Dynamic Optimization)
**Role:** Monitor swarm performance, adapt topology, optimize resource usage dynamically

**Expertise:**
- Performance monitoring
- Dynamic optimization
- Resource management
- Adaptive algorithms

**Output:** Performance metrics, optimization recommendations, scaling policies

## Phase 1: Initialize Cloud Swarm

**Objective:** Initialize swarm with selected topology and agent configuration

**Evidence-Based Validation:**
- Swarm created successfully
- Topology configured correctly
- Swarm ID stored in memory
- Configuration validated

**hierarchical-coordinator Actions:**
```bash
# Pre-task coordination
npx claude-flow@alpha hooks pre-task --description "Initialize cloud swarm deployment"

# Restore session
npx claude-flow@alpha hooks session-restore --session-id "cloud-swarm-$(date +%s)"

# Create project structure
mkdir -p swarm/{config,agents,workflows,monitoring,docs}

# Design swarm topology
cat > swarm/config/topology.json << 'EOF'
{
  "topology": "hierarchical",
  "maxAgents": 8,
  "strategy": "adaptive",
  "roles": {
    "coordinator": {
      "count": 1,
      "capabilities": ["task_delegation", "monitoring", "optimization"]
    },
    "supervisor": {
      "count": 2,
      "capabilities": ["team_management", "task_execution", "reporting"]
    },
    "worker": {
      "count": 5,
      "capabilities": ["task_execution", "specialization"]
    }
  },
  "communication": {
    "protocol": "event-driven",
    "queue": "message-queue",
    "realtime": true
  }
}
EOF

# Post-edit hook
npx claude-flow@alpha hooks post-edit --file "swarm/config/topology.json" --memory-key "swarm/topology"
```

**flow-nexus-swarm Actions:**
```bash
# Initialize swarm on Flow Nexus platform
mcp__flow-nexus__swarm_init {
  "topology": "hierarchical",
  "maxAgents": 8,
  "strategy": "adaptive"
}

# Store swarm ID
SWARM_ID="[returned_swarm_id]"
npx claude-flow@alpha memory store --key "swarm/swarm-id" --value "$SWARM_ID"

# Get swarm status
mcp__flow-nexus__swarm_status { "swarm_id": "$SWARM_ID" }

# List available swarm templates
mcp__flow-nexus__swarm_templates_list {
  "category": "specialized",
  "includeStore": true
}

# Store swarm configuration
npx claude-flow@alpha memory store \
  --key "swarm/config" \
  --value "{\"swarm_id\": \"$SWARM_ID\", \"topology\": \"hierarchical\", \"max_agents\": 8, \"timestamp\": \"$(date -Iseconds)\"}"

# Notify initialization complete
npx claude-flow@alpha hooks notify --message "Cloud swarm initialized: $SWARM_ID"
```

**adaptive-coordinator Actions:**
```bash
# Create performance monitoring configuration
cat > swarm/monitoring/config.json << 'EOF'
{
  "metrics": {
    "swarm": ["agent_count", "task_throughput", "response_time"],
    "agents": ["utilization", "success_rate", "error_rate"],
    "resources": ["cpu_usage", "memory_usage", "network_io"]
  },
  "thresholds": {
    "high_utilization": 0.85,
    "low_utilization": 0.2,
    "max_response_time_ms": 5000,
    "max_error_rate": 0.05
  },
  "scaling": {
    "scale_up": {
      "trigger": "utilization > 0.85 for 5 minutes",
      "action": "add 2 agents"
    },
    "scale_down": {
      "trigger": "utilization < 0.2 for 10 minutes",
      "action": "remove 1 agent"
    }
  }
}
EOF

# Post-edit hook
npx claude-flow@alpha hooks post-edit --file "swarm/monitoring/config.json" --memory-key "swarm/monitoring-config"
```

**Success Criteria:**
- [ ] Swarm initialized on Flow Nexus
- [ ] Topology configured
- [ ] Monitoring setup created
- [ ] Configuration stored

**Memory Persistence:**
```bash
npx claude-flow@alpha memory store \
  --key "swarm/phase1-complete" \
  --value "{\"status\": \"complete\", \"swarm_id\": \"$SWARM_ID\", \"topology\": \"hierarchical\", \"timestamp\": \"$(date -Iseconds)\"}"
```

## Phase 2: Deploy Agents to Cloud

**Objective:** Deploy specialized agents to E2B sandboxes with role-specific configurations

**Evidence-Based Validation:**
- All agents deployed successfully
- Sandboxes running
- Agent capabilities configured
- Communication established

**hierarchical-coordinator Actions:**
```bash
# Define agent specifications
cat > swarm/agents/specifications.json << 'EOF'
{
  "coordinator": {
    "type": "coordinator",
    "capabilities": ["task_delegation", "monitoring", "optimization"],
    "resources": {
      "template": "nodejs",
      "memory": "2GB",
      "cpus": 2
    }
  },
  "supervisors": [
    {
      "type": "supervisor",
      "name": "supervisor-backend",
      "capabilities": ["backend_tasks", "database", "api"],
      "specialization": "backend"
    },
    {
      "type": "supervisor",
      "name": "supervisor-frontend",
      "capabilities": ["frontend_tasks", "ui", "testing"],
      "specialization": "frontend"
    }
  ],
  "workers": [
    {
      "type": "worker",
      "name": "worker-coder-1",
      "capabilities": ["coding", "implementation"],
      "specialization": "coder"
    },
    {
      "type": "worker",
      "name": "worker-coder-2",
      "capabilities": ["coding", "implementation"],
      "specialization": "coder"
    },
    {
      "type": "worker",
      "name": "worker-tester",
      "capabilities": ["testing", "validation"],
      "specialization": "tester"
    },
    {
      "type": "worker",
      "name": "worker-reviewer",
      "capabilities": ["code_review", "quality"],
      "specialization": "reviewer"
    },
    {
      "type": "worker",
      "name": "worker-docs",
      "capabilities": ["documentation", "writing"],
      "specialization": "documentation"
    }
  ]
}
EOF

# Post-edit hook
npx claude-flow@alpha hooks post-edit --file "swarm/agents/specifications.json" --memory-key "swarm/agent-specs"
```

**flow-nexus-swarm Actions:**
```bash
# Retrieve swarm ID
SWARM_ID=$(npx claude-flow@alpha memory retrieve --key "swarm/swarm-id" | jq -r '.value')

# Spawn coordinator agent
mcp__flow-nexus__agent_spawn {
  "type": "coordinator",
  "name": "coordinator-main",
  "capabilities": ["task_delegation", "monitoring", "optimization"]
}

COORDINATOR_ID="[returned_agent_id]"
npx claude-flow@alpha memory store --key "swarm/coordinator-id" --value "$COORDINATOR_ID"

# Spawn supervisor agents
for spec in "backend" "frontend"; do
  mcp__flow-nexus__agent_spawn {
    "type": "analyst",
    "name": "supervisor-$spec",
    "capabilities": ["team_management", "task_execution", "reporting"]
  }
done

# Spawn worker agents
for spec in "coder" "coder" "tester" "reviewer" "documentation"; do
  mcp__flow-nexus__agent_spawn {
    "type": "coder",
    "name": "worker-$spec",
    "capabilities": ["task_execution", "specialization"]
  }
done

# Get agent list
mcp__flow-nexus__agent_list { "filter": "all" }

# Store agent count
npx claude-flow@alpha memory store --key "swarm/agent-count" --value "8"

# Scale swarm if needed
mcp__flow-nexus__swarm_scale {
  "swarm_id": "$SWARM_ID",
  "target_agents": 8
}

# Notify deployment complete
npx claude-flow@alpha hooks notify --message "8 agents deployed to cloud sandboxes"
```

**adaptive-coordinator Actions:**
```bash
# Create agent monitoring script
cat > swarm/monitoring/monitor-agents.sh << 'EOF'
#!/bin/bash

SWARM_ID="${SWARM_ID:-$(npx claude-flow@alpha memory retrieve --key swarm/swarm-id | jq -r '.value')}"

echo "Monitoring swarm: $SWARM_ID"
echo "================================"

# Get agent metrics
mcp__flow-nexus__agent_metrics --agentId="all"

# Get swarm status
mcp__flow-nexus__swarm_status --swarm_id="$SWARM_ID"

# Check for performance issues
UTILIZATION=$(mcp__flow-nexus__agent_metrics | jq '.avg_utilization')
if (( $(echo "$UTILIZATION > 0.85" | bc -l) )); then
  echo "WARNING: High utilization detected ($UTILIZATION)"
  echo "Consider scaling up the swarm"
fi

echo "================================"
echo "Monitoring complete"
EOF

chmod +x swarm/monitoring/monitor-agents.sh

# Post-edit hook
npx claude-flow@alpha hooks post-edit --file "swarm/monitoring/monitor-agents.sh" --memory-key "swarm/monitor-script"
```

**Success Criteria:**
- [ ] Coordinator agent deployed
- [ ] Supervisor agents deployed (2)
- [ ] Worker agents deployed (5)
- [ ] Monitoring script created

**Memory Persistence:**
```bash
npx claude-flow@alpha memory store \
  --key "swarm/phase2-complete" \
  --value "{\"status\": \"complete\", \"agents_deployed\": 8, \"coordinator\": \"$COORDINATOR_ID\", \"timestamp\": \"$(date -Iseconds)\"}"
```

## Phase 3: Coordinate Workflows

**Objective:** Create event-driven workflows with agent coordination and task routing

**Evidence-Based Validation:**
- Workflows created successfully
- Tasks being executed
- Event-driven processing active
- Message queue operational

**hierarchical-coordinator Actions:**
```bash
# Design workflow structure
cat > swarm/workflows/main-workflow.json << 'EOF'
{
  "id": "main-workflow",
  "name": "Full-Stack Development Workflow",
  "description": "Coordinate backend and frontend development with testing",
  "steps": [
    {
      "id": "step1",
      "name": "Requirements Analysis",
      "agent": "coordinator",
      "action": "analyze_requirements",
      "output": "requirements_doc"
    },
    {
      "id": "step2",
      "name": "Backend Development",
      "agent": "supervisor-backend",
      "action": "coordinate_backend",
      "dependencies": ["step1"],
      "parallel": true,
      "subtasks": [
        {
          "name": "API Development",
          "agent": "worker-coder-1"
        },
        {
          "name": "Database Schema",
          "agent": "worker-coder-2"
        }
      ]
    },
    {
      "id": "step3",
      "name": "Frontend Development",
      "agent": "supervisor-frontend",
      "action": "coordinate_frontend",
      "dependencies": ["step1"],
      "parallel": true,
      "subtasks": [
        {
          "name": "UI Components",
          "agent": "worker-coder-1"
        }
      ]
    },
    {
      "id": "step4",
      "name": "Testing",
      "agent": "worker-tester",
      "action": "run_tests",
      "dependencies": ["step2", "step3"]
    },
    {
      "id": "step5",
      "name": "Code Review",
      "agent": "worker-reviewer",
      "action": "review_code",
      "dependencies": ["step4"]
    },
    {
      "id": "step6",
      "name": "Documentation",
      "agent": "worker-docs",
      "action": "generate_docs",
      "dependencies": ["step5"]
    }
  ],
  "triggers": [
    {
      "event": "pull_request_created",
      "action": "start_workflow"
    },
    {
      "event": "code_pushed",
      "action": "run_tests"
    }
  ]
}
EOF

# Post-edit hook
npx claude-flow@alpha hooks post-edit --file "swarm/workflows/main-workflow.json" --memory-key "swarm/workflow"
```

**flow-nexus-swarm Actions:**
```bash
# Create workflow on Flow Nexus
mcp__flow-nexus__workflow_create {
  "name": "Full-Stack Development Workflow",
  "description": "Coordinate backend and frontend development with testing",
  "steps": [
    {
      "name": "Requirements Analysis",
      "agent_type": "coordinator"
    },
    {
      "name": "Backend Development",
      "agent_type": "supervisor",
      "parallel": true
    },
    {
      "name": "Frontend Development",
      "agent_type": "supervisor",
      "parallel": true
    },
    {
      "name": "Testing",
      "agent_type": "worker"
    },
    {
      "name": "Code Review",
      "agent_type": "worker"
    },
    {
      "name": "Documentation",
      "agent_type": "worker"
    }
  ],
  "triggers": [
    { "event": "pull_request_created" },
    { "event": "code_pushed" }
  ],
  "priority": 8,
  "metadata": {
    "category": "development",
    "tags": ["fullstack", "automated"]
  }
}

# Store workflow ID
WORKFLOW_ID="[returned_workflow_id]"
npx claude-flow@alpha memory store --key "swarm/workflow-id" --value "$WORKFLOW_ID"

# Assign agents to workflow tasks
mcp__flow-nexus__workflow_agent_assign {
  "task_id": "backend_development",
  "agent_type": "analyst",
  "use_vector_similarity": true
}

# Execute workflow
mcp__flow-nexus__workflow_execute {
  "workflow_id": "$WORKFLOW_ID",
  "input_data": {
    "project": "fullstack-app",
    "requirements": "Build REST API with React frontend"
  },
  "async": true
}

# Store execution ID
EXECUTION_ID="[returned_execution_id]"
npx claude-flow@alpha memory store --key "swarm/execution-id" --value "$EXECUTION_ID"

# Notify workflow started
npx claude-flow@alpha hooks notify --message "Workflow executing: $WORKFLOW_ID"
```

**adaptive-coordinator Actions:**
```bash
# Create workflow monitoring script
cat > swarm/monitoring/monitor-workflow.sh << 'EOF'
#!/bin/bash

WORKFLOW_ID="${WORKFLOW_ID:-$(npx claude-flow@alpha memory retrieve --key swarm/workflow-id | jq -r '.value')}"

echo "Monitoring workflow: $WORKFLOW_ID"
echo "================================"

# Get workflow status
mcp__flow-nexus__workflow_status \
  --workflow_id="$WORKFLOW_ID" \
  --include_metrics=true

# Check queue status
mcp__flow-nexus__workflow_queue_status \
  --include_messages=true

# Get audit trail
mcp__flow-nexus__workflow_audit_trail \
  --workflow_id="$WORKFLOW_ID" \
  --limit=50

echo "================================"
EOF

chmod +x swarm/monitoring/monitor-workflow.sh

# Post-edit hook
npx claude-flow@alpha hooks post-edit --file "swarm/monitoring/monitor-workflow.sh" --memory-key "swarm/workflow-monitor"
```

**Success Criteria:**
- [ ] Workflow created on platform
- [ ] Agents assigned to tasks
- [ ] Workflow executing
- [ ] Monitoring scripts ready

**Memory Persistence:**
```bash
npx claude-flow@alpha memory store \
  --key "swarm/phase3-complete" \
  --value "{\"status\": \"complete\", \"workflow_id\": \"$WORKFLOW_ID\", \"execution_id\": \"$EXECUTION_ID\", \"timestamp\": \"$(date -Iseconds)\"}"
```

## Phase 4: Monitor Performance

**Objective:** Track swarm performance, collect metrics, identify bottlenecks

**Evidence-Based Validation:**
- Metrics being collected
- Performance within acceptable range
- No critical bottlenecks
- Dashboards accessible

**hierarchical-coordinator Actions:**
```bash
# Create performance analysis script
cat > swarm/monitoring/analyze-performance.sh << 'EOF'
#!/bin/bash

SWARM_ID="${SWARM_ID:-$(npx claude-flow@alpha memory retrieve --key swarm/swarm-id | jq -r '.value')}"

echo "Performance Analysis: $SWARM_ID"
echo "================================"

# Get agent metrics
echo "Agent Metrics:"
mcp__flow-nexus__agent_metrics --metric="all"

# Get workflow metrics
echo -e "\nWorkflow Metrics:"
mcp__flow-nexus__workflow_status --include_metrics=true

# Get system health
echo -e "\nSystem Health:"
mcp__flow-nexus__system_health

# Calculate summary
echo -e "\n================================"
echo "Performance Summary:"
echo "- Average agent utilization: [calculated]"
echo "- Workflow completion rate: [calculated]"
echo "- Average response time: [calculated]"
echo "- Error rate: [calculated]"
echo "================================"
EOF

chmod +x swarm/monitoring/analyze-performance.sh

# Post-edit hook
npx claude-flow@alpha hooks post-edit --file "swarm/monitoring/analyze-performance.sh" --memory-key "swarm/perf-analysis"
```

**flow-nexus-swarm Actions:**
```bash
# Get swarm metrics
SWARM_ID=$(npx claude-flow@alpha memory retrieve --key "swarm/swarm-id" | jq -r '.value')
mcp__flow-nexus__swarm_status {
  "swarm_id": "$SWARM_ID",
  "verbose": true
}

# Get detailed agent metrics
mcp__flow-nexus__agent_metrics { "metric": "all" }

# Get workflow status with metrics
WORKFLOW_ID=$(npx claude-flow@alpha memory retrieve --key "swarm/workflow-id" | jq -r '.value')
mcp__flow-nexus__workflow_status {
  "workflow_id": "$WORKFLOW_ID",
  "include_metrics": true
}

# Store performance metrics
npx claude-flow@alpha memory store \
  --key "swarm/performance-metrics" \
  --value "{\"avg_utilization\": 0.72, \"throughput_tps\": 12, \"avg_response_ms\": 2400, \"error_rate\": 0.02, \"timestamp\": \"$(date -Iseconds)\"}"
```

**adaptive-coordinator Actions:**
```bash
# Create performance report
cat > swarm/monitoring/performance-report.md << 'EOF'
# Swarm Performance Report

**Generated:** $(date -Iseconds)
**Swarm ID:** $SWARM_ID

## Swarm Metrics

- **Topology:** Hierarchical
- **Total Agents:** 8 (1 coordinator, 2 supervisors, 5 workers)
- **Active Workflows:** 1

## Performance Metrics

### Agent Utilization
- Average: 72%
- Coordinator: 85%
- Supervisors: 78%
- Workers: 68%

### Throughput
- Tasks per second: 12
- Tasks completed: [calculated]
- Tasks pending: [calculated]

### Response Time
- Average: 2.4s
- p50: 1.8s
- p95: 4.2s
- p99: 6.8s

### Error Rate
- Overall: 2%
- By agent type:
  - Coordinator: 0%
  - Supervisors: 1%
  - Workers: 3%

## Bottleneck Analysis

### Identified Issues
- Worker-coder-1 at 95% utilization (bottleneck)
- Message queue backlog: 23 tasks

### Recommendations
1. Scale up worker agents (+2)
2. Optimize task distribution algorithm
3. Increase message queue capacity
4. Consider specialized worker for high-load tasks

## Resource Usage

- CPU: 65% average
- Memory: 4.2GB / 16GB
- Network I/O: 120 Mbps

## Scaling Recommendations

Based on current metrics:
- **Immediate**: Add 1 worker agent
- **Short-term**: Optimize coordinator algorithm
- **Long-term**: Implement auto-scaling policies
EOF

# Post-edit hook
npx claude-flow@alpha hooks post-edit --file "swarm/monitoring/performance-report.md" --memory-key "swarm/perf-report"
```

**Success Criteria:**
- [ ] Metrics collected successfully
- [ ] Performance analyzed
- [ ] Bottlenecks identified
- [ ] Report generated

**Memory Persistence:**
```bash
npx claude-flow@alpha memory store \
  --key "swarm/phase4-complete" \
  --value "{\"status\": \"complete\", \"performance_good\": true, \"bottleneck_identified\": true, \"timestamp\": \"$(date -Iseconds)\"}"
```

## Phase 5: Scale and Optimize

**Objective:** Implement auto-scaling, optimize performance, adapt topology dynamically

**Evidence-Based Validation:**
- Scaling policies active
- Performance improved
- Auto-scaling working
- Optimization applied

**hierarchical-coordinator Actions:**
```bash
# Create scaling policy
cat > swarm/config/scaling-policy.json << 'EOF'
{
  "auto_scaling": {
    "enabled": true,
    "min_agents": 5,
    "max_agents": 15,
    "rules": [
      {
        "name": "scale_up_high_utilization",
        "condition": "avg_utilization > 0.80 for 5 minutes",
        "action": "add_agents",
        "count": 2,
        "cooldown": 300
      },
      {
        "name": "scale_down_low_utilization",
        "condition": "avg_utilization < 0.30 for 10 minutes",
        "action": "remove_agents",
        "count": 1,
        "cooldown": 600
      },
      {
        "name": "scale_up_queue_backlog",
        "condition": "queue_size > 50",
        "action": "add_agents",
        "count": 3,
        "cooldown": 180
      }
    ]
  },
  "optimization": {
    "task_distribution": "load_balanced",
    "agent_specialization": true,
    "dynamic_reassignment": true,
    "priority_queuing": true
  }
}
EOF

# Post-edit hook
npx claude-flow@alpha hooks post-edit --file "swarm/config/scaling-policy.json" --memory-key "swarm/scaling-policy"

# Post-task hook
npx claude-flow@alpha hooks post-task --task-id "cloud-swarm-deployment"
```

**flow-nexus-swarm Actions:**
```bash
# Scale swarm based on analysis
SWARM_ID=$(npx claude-flow@alpha memory retrieve --key "swarm/swarm-id" | jq -r '.value')
mcp__flow-nexus__swarm_scale {
  "swarm_id": "$SWARM_ID",
  "target_agents": 10
}

# Spawn additional worker agents
mcp__flow-nexus__agent_spawn {
  "type": "coder",
  "name": "worker-coder-3",
  "capabilities": ["task_execution", "specialization"]
}

mcp__flow-nexus__agent_spawn {
  "type": "coder",
  "name": "worker-coder-4",
  "capabilities": ["task_execution", "specialization"]
}

# Get updated swarm status
mcp__flow-nexus__swarm_status {
  "swarm_id": "$SWARM_ID",
  "verbose": true
}

# Store final configuration
npx claude-flow@alpha memory store \
  --key "swarm/final-config" \
  --value "{\"swarm_id\": \"$SWARM_ID\", \"agents\": 10, \"scaled\": true, \"timestamp\": \"$(date -Iseconds)\"}"
```

**adaptive-coordinator Actions:**
```bash
# Create auto-scaling monitor
cat > swarm/monitoring/auto-scale-monitor.sh << 'EOF'
#!/bin/bash

SWARM_ID="${SWARM_ID:-$(npx claude-flow@alpha memory retrieve --key swarm/swarm-id | jq -r '.value')}"

echo "Auto-Scaling Monitor: $SWARM_ID"
echo "================================"

while true; do
  # Get current metrics
  METRICS=$(mcp__flow-nexus__agent_metrics --metric="all")
  UTILIZATION=$(echo "$METRICS" | jq '.avg_utilization')
  AGENT_COUNT=$(mcp__flow-nexus__swarm_status --swarm_id="$SWARM_ID" | jq '.agent_count')

  echo "[$(date -Iseconds)] Utilization: $UTILIZATION, Agents: $AGENT_COUNT"

  # Check scaling conditions
  if (( $(echo "$UTILIZATION > 0.80" | bc -l) )); then
    echo "High utilization detected. Scaling up..."
    NEW_COUNT=$((AGENT_COUNT + 2))
    if [ $NEW_COUNT -le 15 ]; then
      mcp__flow-nexus__swarm_scale --swarm_id="$SWARM_ID" --target_agents=$NEW_COUNT
    fi
  elif (( $(echo "$UTILIZATION < 0.30" | bc -l) )); then
    echo "Low utilization detected. Scaling down..."
    NEW_COUNT=$((AGENT_COUNT - 1))
    if [ $NEW_COUNT -ge 5 ]; then
      mcp__flow-nexus__swarm_scale --swarm_id="$SWARM_ID" --target_agents=$NEW_COUNT
    fi
  fi

  sleep 300  # Check every 5 minutes
done
EOF

chmod +x swarm/monitoring/auto-scale-monitor.sh

# Create deployment summary
cat > swarm/docs/DEPLOYMENT-SUMMARY.md << 'EOF'
# Cloud Swarm Deployment Summary

**Deployment Date:** $(date -Iseconds)
**Swarm ID:** $SWARM_ID

## Configuration

- **Topology:** Hierarchical
- **Initial Agents:** 8
- **Final Agents:** 10
- **Auto-scaling:** Enabled (5-15 agents)

## Deployed Agents

### Coordinator
- coordinator-main: Task delegation, monitoring, optimization

### Supervisors
- supervisor-backend: Backend development coordination
- supervisor-frontend: Frontend development coordination

### Workers
- worker-coder-1, 2, 3, 4: Implementation
- worker-tester: Testing and validation
- worker-reviewer: Code review
- worker-docs: Documentation

## Workflows

- Full-Stack Development Workflow (executing)
- Event-driven processing enabled
- Message queue operational

## Performance

- Average utilization: 72%
- Throughput: 12 TPS
- Response time: 2.4s avg
- Error rate: 2%

## Monitoring

- Real-time metrics collection
- Auto-scaling monitor running
- Performance analysis available
- Audit trail active

## Next Steps

1. Monitor auto-scaling behavior
2. Optimize task distribution
3. Fine-tune performance thresholds
4. Add custom workflows as needed
5. Review and adjust scaling policies

## Access

- Swarm status: `mcp__flow-nexus__swarm_status`
- Agent metrics: `mcp__flow-nexus__agent_metrics`
- Workflow status: `mcp__flow-nexus__workflow_status`
- Performance: `./swarm/monitoring/analyze-performance.sh`
EOF

# Post-edit hooks
npx claude-flow@alpha hooks post-edit --file "swarm/monitoring/auto-scale-monitor.sh" --memory-key "swarm/auto-scale-monitor"
npx claude-flow@alpha hooks post-edit --file "swarm/docs/DEPLOYMENT-SUMMARY.md" --memory-key "swarm/summary"

# Session end hook
npx claude-flow@alpha hooks session-end --export-metrics true
```

**Success Criteria:**
- [ ] Swarm scaled to 10 agents
- [ ] Auto-scaling policies active
- [ ] Performance optimized
- [ ] Monitoring running
- [ ] Documentation complete

**Memory Persistence:**
```bash
npx claude-flow@alpha memory store \
  --key "swarm/phase5-complete" \
  --value "{\"status\": \"complete\", \"agents\": 10, \"auto_scaling\": true, \"optimized\": true, \"timestamp\": \"$(date -Iseconds)\"}"

# Final workflow summary
npx claude-flow@alpha memory store \
  --key "swarm/workflow-complete" \
  --value "{\"status\": \"success\", \"swarm_id\": \"$SWARM_ID\", \"agents\": 10, \"workflow_executing\": true, \"auto_scaling\": true, \"timestamp\": \"$(date -Iseconds)\"}"
```

## Workflow Summary

**Total Estimated Duration:** 40-70 minutes

**Phase Breakdown:**
1. Initialize Cloud Swarm: 5-10 minutes
2. Deploy Agents to Cloud: 10-15 minutes
3. Coordinate Workflows: 10-15 minutes
4. Monitor Performance: 10-15 minutes
5. Scale and Optimize: 5-15 minutes

**Key Deliverables:**
- Cloud swarm deployment
- 10 specialized agents
- Event-driven workflows
- Performance monitoring
- Auto-scaling system
- Complete documentation

## Evidence-Based Success Metrics

**Swarm Deployment:**
- Swarm initialized successfully
- All agents deployed (10)
- Topology configured correctly

**Workflows:**
- Workflow executing
- Event-driven processing active
- Task completion rate >90%

**Performance:**
- Average utilization 70-80%
- Response time <3s
- Error rate <5%
- Throughput >10 TPS

**Scaling:**
- Auto-scaling functional
- Scaling policies effective
- Performance improved after scaling

## Troubleshooting

**Swarm Initialization Failed:**
- Verify Flow Nexus authentication
- Check account credits
- Review topology configuration

**Agent Deployment Issues:**
- Check E2B sandbox availability
- Verify agent specifications
- Review resource limits

**Workflow Execution Errors:**
- Check agent assignments
- Verify task dependencies
- Review event triggers

**Performance Issues:**
- Analyze bottlenecks
- Scale up agents
- Optimize task distribution

**Auto-scaling Not Working:**
- Verify scaling policies
- Check metric thresholds
- Review cooldown periods

## Best Practices

1. **Topology Selection**: Choose based on task complexity
2. **Agent Specialization**: Assign clear roles
3. **Monitoring**: Track all metrics
4. **Scaling**: Start small, scale gradually
5. **Optimization**: Iterate based on metrics
6. **Documentation**: Keep updated
7. **Testing**: Validate workflows thoroughly
8. **Resources**: Monitor costs and usage

## References

- Flow Nexus Swarm API: https://flow-nexus.ruv.io/docs/swarm
- E2B Sandboxes: https://e2b.dev/docs
- Claude Flow: https://github.com/ruvnet/claude-flow
- Event-Driven Architecture: https://martinfowler.com/articles/201701-event-driven.html
