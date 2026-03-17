---
name: cfn-automatic-memory-persistence
description: "Automatic, structured persistence of agent outputs to SQLite database. Use when tracking agent outputs across CFN Loop workflows, persisting confidence scores, or querying agent execution history."
version: 1.0.0
tags: [memory, persistence, sqlite, auto, agent-tracking]
---

# Automatic Memory Persistence Skill

## Overview
This skill provides automatic, structured persistence of agent outputs to a SQLite database, ensuring consistent memory tracking across CFN Loop workflows.

## Key Components
- `persist-agent-output.sh`: Primary script for saving agent outputs
- `query-agent-history.sh`: Query and retrieve past agent outputs
- `test-memory-persistence.sh`: Validation test suite

## Memory Schema
```json
{
  "agent/[agent-id]/output/[task-id]": {
    "output": "Raw agent output text",
    "confidence": 0.85,
    "iteration": 1,
    "timestamp": "2025-10-20T15:30:00Z",
    "parsed_data": null
  }
}
```

## Integration Points
- Loop 3 output processing
- Loop 2 output processing
- Product Owner decision parsing

## Usage Examples

### Persist Agent Output
```bash
./persist-agent-output.sh \
  "task_authentication_v1" \  # Task ID
  "backend-dev" \             # Agent ID
  "Implemented JWT auth" \    # Output
  0.85 \                      # Confidence
  1                           # Iteration
```

### Query Agent History
```bash
# Get last 5 outputs for a specific agent
./query-agent-history.sh "backend-dev" "" 5

# Get outputs for a specific task
./query-agent-history.sh "backend-dev" "task_authentication_v1"
```

## Security & Performance
- ACL Level 1 (Read-only access)
- Indexed by tags for fast retrieval
- Minimal performance overhead
- Escaped and normalized inputs

## Testing
Run comprehensive tests:
```bash
./test-memory-persistence.sh
```

## Sprint 7 Insights
- **Confidence**: 0.95
- **Priority**: 9
- Provides robust, zero-configuration memory tracking
- Eliminates manual output saving
- Supports multi-iteration workflows

## Best Practices
- Always use script for output persistence
- Do not modify SQLite database directly
- Use query script for retrieval
- Add structured parsing for complex outputs