---
name: agent-run
description: 'Tags: agents, execution, claude-api, orchestration, layer2'
---

# agent.run

**Version:** 0.1.0
**Status:** Active
**Tags:** agents, execution, claude-api, orchestration, layer2

## Overview

The `agent.run` skill executes registered Betty agents by orchestrating the complete agent lifecycle: loading manifests, generating Claude-friendly prompts, invoking the Claude API (or simulating), executing planned skills, and logging all results.

This skill is the primary execution engine for Betty agents, enabling them to operate in both **iterative** and **oneshot** reasoning modes. It handles the translation between agent manifests and Claude API calls, manages skill invocation, and provides comprehensive logging for auditability.

## Features

- ✅ Load agent manifests from path or agent name
- ✅ Generate Claude-optimized system prompts with capabilities and workflow patterns
- ✅ Optional Claude API integration (with mock fallback for development)
- ✅ Support for both iterative and oneshot reasoning modes
- ✅ Skill selection and execution orchestration
- ✅ Comprehensive execution logging to `agent_logs/<agent>_<timestamp>.json`
- ✅ Structured JSON output for programmatic integration
- ✅ Error handling with detailed diagnostics
- ✅ Validation of agent manifests and available skills

## Usage

### Command Line

```bash
# Execute agent by name
python skills/agent.run/agent_run.py api.designer

# Execute with task context
python skills/agent.run/agent_run.py api.designer "Design a REST API for user management"

# Execute from manifest path
python skills/agent.run/agent_run.py agents/api.designer/agent.yaml "Create authentication API"

# Execute without saving logs
python skills/agent.run/agent_run.py api.designer "Design API" --no-save-log
```

### As a Skill (Programmatic)

```python
import sys
import os
sys.path.insert(0, os.path.abspath("./"))

from skills.agent.run.agent_run import run_agent

# Execute agent
result = run_agent(
    agent_path="api.designer",
    task_context="Design a REST API for user management with authentication",
    save_log=True
)

if result["ok"]:
    print(f"Agent executed successfully!")
    print(f"Skills invoked: {result['details']['summary']['skills_executed']}")
    print(f"Log saved to: {result['details']['log_path']}")
else:
    print(f"Execution failed: {result['errors']}")
```

### Via Claude Code Plugin

```bash
# Using the Betty plugin command
/agent/run api.designer "Design authentication API"

# With full path
/agent/run agents/api.designer/agent.yaml "Create user management endpoints"
```

## Input Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `agent_path` | string | Yes | - | Path to agent.yaml or agent name (e.g., `api.designer`) |
| `task_context` | string | No | None | Task or query to provide to the agent |
| `save_log` | boolean | No | true | Whether to save execution log to disk |

## Output Schema

```json
{
  "ok": true,
  "status": "success",
  "timestamp": "2025-10-23T14:30:00Z",
  "errors": [],
  "details": {
    "timestamp": "2025-10-23T14:30:00Z",
    "agent": {
      "name": "api.designer",
      "version": "0.1.0",
      "description": "Design RESTful APIs...",
      "reasoning_mode": "iterative",
      "status": "active"
    },
    "task_context": "Design a REST API for user management",
    "prompt": "You are api.designer, a specialized Betty Framework agent...",
    "skills_available": [
      {
        "name": "api.define",
        "description": "Create OpenAPI specifications",
        "status": "active"
      }
    ],
    "missing_skills": [],
    "claude_response": {
      "analysis": "I will design a comprehensive user management API...",
      "skills_to_invoke": [
        {
          "skill": "api.define",
          "purpose": "Create initial OpenAPI spec",
          "inputs": {"guidelines": "zalando"},
          "order": 1
        }
      ],
      "reasoning": "Following API design workflow pattern"
    },
    "execution_results": [
      {
        "skill": "api.define",
        "purpose": "Create initial OpenAPI spec",
        "status": "simulated",
        "timestamp": "2025-10-23T14:30:05Z",
        "output": {
          "success": true,
          "note": "Simulated execution of api.define"
        }
      }
    ],
    "summary": {
      "skills_planned": 3,
      "skills_executed": 3,
      "success": true
    },
    "log_path": "/home/user/betty/agent_logs/api.designer_20251023_143000.json"
  }
}
```

## Reasoning Modes

### Oneshot Mode

In **oneshot** mode, the agent analyzes the complete task and plans all skill invocations upfront in a single pass. The execution follows the predetermined plan without dynamic adjustment.

**Best for:**
- Well-defined tasks with predictable workflows
- Tasks where all steps can be determined in advance
- Performance-critical scenarios requiring minimal API calls

**Example Agent:**
```yaml
name: api.generator
reasoning_mode: oneshot
workflow_pattern: |
  1. Define API structure
  2. Validate specification
  3. Generate models
```

### Iterative Mode

In **iterative** mode, the agent analyzes results after each skill invocation and dynamically determines the next steps. It can retry failed operations, adjust its approach based on feedback, or invoke additional skills as needed.

**Best for:**
- Complex tasks requiring adaptive decision-making
- Tasks with validation/refinement loops
- Scenarios where results influence subsequent steps

**Example Agent:**
```yaml
name: api.designer
reasoning_mode: iterative
workflow_pattern: |
  1. Analyze requirements
  2. Draft OpenAPI spec
  3. Validate (if fails, refine and retry)
  4. Generate models
```

## Examples

### Example 1: Execute API Designer

```bash
python skills/agent.run/agent_run.py api.designer \
  "Create a REST API for managing blog posts with CRUD operations"
```

**Output:**
```
================================================================================
AGENT EXECUTION: api.designer
================================================================================

Agent: api.designer v0.1.0
Mode: iterative
Status: active

Task: Create a REST API for managing blog posts with CRUD operations

--------------------------------------------------------------------------------
CLAUDE RESPONSE:
--------------------------------------------------------------------------------
{
  "analysis": "I will design a RESTful API following best practices...",
  "skills_to_invoke": [
    {
      "skill": "api.define",
      "purpose": "Create initial OpenAPI specification",
      "inputs": {"guidelines": "zalando", "format": "openapi-3.1"},
      "order": 1
    },
    {
      "skill": "api.validate",
      "purpose": "Validate the specification for compliance",
      "inputs": {"strict_mode": true},
      "order": 2
    }
  ]
}

--------------------------------------------------------------------------------
EXECUTION RESULTS:
--------------------------------------------------------------------------------

  ✓ api.define
    Purpose: Create initial OpenAPI specification
    Status: simulated

  ✓ api.validate
    Purpose: Validate the specification for compliance
    Status: simulated

📝 Log saved to: /home/user/betty/agent_logs/api.designer_20251023_143000.json

================================================================================
EXECUTION COMPLETE
================================================================================
```

### Example 2: Execute with Direct Path

```bash
python skills/agent.run/agent_run.py \
  agents/api.analyzer/agent.yaml \
  "Analyze this OpenAPI spec for compatibility issues"
```

### Example 3: Execute Without Logging

```bash
python skills/agent.run/agent_run.py api.designer \
  "Design authentication API" \
  --no-save-log
```

### Example 4: Programmatic Integration

```python
from skills.agent.run.agent_run import run_agent, load_agent_manifest

# Load and inspect agent before running
manifest = load_agent_manifest("api.designer")
print(f"Agent capabilities: {manifest['capabilities']}")

# Execute with custom context
result = run_agent(
    agent_path="api.designer",
    task_context="Design GraphQL API for e-commerce",
    save_log=True
)

if result["ok"]:
    # Access execution details
    claude_response = result["details"]["claude_response"]
    execution_results = result["details"]["execution_results"]

    print(f"Claude planned {len(claude_response['skills_to_invoke'])} skills")
    print(f"Executed {len(execution_results)} skills")

    # Check individual skill results
    for exec_result in execution_results:
        print(f"  - {exec_result['skill']}: {exec_result['status']}")
```

## Agent Manifest Requirements

For `agent.run` to successfully execute an agent, the agent manifest must include:

### Required Fields

```yaml
name: agent.name              # Must match pattern ^[a-z][a-z0-9._-]*$
version: 0.1.0                # Semantic version
description: "..."            # Clear description
capabilities:                 # List of capabilities
  - "Capability 1"
  - "Capability 2"
skills_available:            # List of Betty skills
  - skill.name.1
  - skill.name.2
reasoning_mode: iterative    # 'iterative' or 'oneshot'
```

### Recommended Fields

```yaml
workflow_pattern: |          # Recommended workflow steps
  1. Step 1
  2. Step 2
  3. Step 3

context_requirements:        # Optional context hints
  guidelines: string
  domain: string

error_handling:              # Error handling config
  max_retries: 3
  timeout_seconds: 300

status: active               # Agent status (draft/active/deprecated)
tags:                        # Categorization tags
  - tag1
  - tag2
```

## Claude API Integration

The skill supports both real Claude API calls and mock simulation:

### Real API Mode (Production)

Set the `ANTHROPIC_API_KEY` environment variable:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
python skills/agent.run/agent_run.py api.designer "Design API"
```

The skill will:
1. Detect the API key
2. Use the Anthropic Python SDK
3. Call Claude 3.5 Sonnet with the constructed prompt
4. Parse the structured JSON response
5. Execute the skills based on Claude's plan

### Mock Mode (Development)

Without an API key, the skill generates intelligent mock responses:

```bash
python skills/agent.run/agent_run.py api.designer "Design API"
```

The skill will:
1. Detect no API key
2. Generate plausible skill selections based on agent type
3. Simulate Claude's reasoning
4. Execute skills with simulated outputs

## Execution Logging

All agent executions are logged to `agent_logs/<agent>_<timestamp>.json` with:

- **Timestamp**: ISO 8601 UTC timestamp
- **Agent Info**: Name, version, description, mode, status
- **Task Context**: User-provided task or query
- **Prompt**: Complete Claude system prompt
- **Skills Available**: Registered skills with metadata
- **Missing Skills**: Skills referenced but not found
- **Claude Response**: Full API response or mock
- **Execution Results**: Output from each skill invocation
- **Summary**: Counts, success status, timing

### Log File Structure

```json
{
  "timestamp": "2025-10-23T14:30:00Z",
  "agent": { /* agent metadata */ },
  "task_context": "Design API for...",
  "prompt": "You are api.designer...",
  "skills_available": [ /* skill info */ ],
  "missing_skills": [],
  "claude_response": { /* Claude's plan */ },
  "execution_results": [ /* skill outputs */ ],
  "summary": {
    "skills_planned": 3,
    "skills_executed": 3,
    "success": true
  }
}
```

### Accessing Logs

```bash
# View latest log for an agent
cat agent_logs/api.designer_latest.json | jq '.'

# View specific execution
cat agent_logs/api.designer_20251023_143000.json | jq '.summary'

# List all logs for an agent
ls -lt agent_logs/api.designer_*.json
```

## Error Handling

### Common Errors

**Agent Not Found**
```json
{
  "ok": false,
  "status": "failed",
  "errors": ["Agent not found: my.agent"],
  "details": {
    "error": {
      "type": "BettyError",
      "message": "Agent not found: my.agent",
      "details": {
        "agent_path": "my.agent",
        "expected_path": "/home/user/betty/agents/my.agent/agent.yaml",
        "suggestion": "Use 'betty agent list' to see available agents"
      }
    }
  }
}
```

**Invalid Agent Manifest**
```json
{
  "ok": false,
  "errors": ["Agent manifest missing required fields: reasoning_mode, capabilities"],
  "details": {
    "error": {
      "type": "BettyError",
      "details": {
        "missing_fields": ["reasoning_mode", "capabilities"]
      }
    }
  }
}
```

**Skill Not Found**
- The execution continues but logs missing skills in `missing_skills` array
- Warning logged for each missing skill
- Agent may not function as intended if critical skills are missing

### Debugging Tips

1. **Check agent manifest**: Validate with `betty agent validate <agent_path>`
2. **Verify skills**: Ensure all `skills_available` are registered
3. **Review logs**: Check `agent_logs/<agent>_latest.json` for details
4. **Enable debug logging**: Set `BETTY_LOG_LEVEL=DEBUG`
5. **Test with mock mode**: Remove API key to test workflow logic

## Best Practices

### 1. Agent Design

- Define clear, specific capabilities in agent manifests
- Choose appropriate reasoning mode for the task complexity
- Provide detailed workflow patterns to guide Claude
- Include context requirements for optimal prompts

### 2. Task Context

- Provide specific, actionable task descriptions
- Include relevant domain context when needed
- Reference specific requirements or constraints
- Use examples to clarify ambiguous requests

### 3. Logging

- Keep logs enabled for production (default: `save_log=true`)
- Review logs regularly for debugging and auditing
- Archive old logs periodically to manage disk space
- Use log summaries to track agent performance

### 4. Error Recovery

- In iterative mode, agents can retry failed skills
- Review error details in logs for root cause analysis
- Validate agent manifests before deployment
- Test with mock mode before using real API calls

### 5. Performance

- Use oneshot mode for predictable, fast execution
- Cache agent manifests when running repeatedly
- Monitor Claude API usage and costs
- Consider skill execution time when designing workflows

## Integration with Betty Framework

### Skill Dependencies

`agent.run` depends on:
- **agent.define**: For creating agent manifests
- **Skill registry**: For validating available skills
- **Betty configuration**: For paths and settings

### Plugin Integration

The skill is registered in `plugin.yaml` as:
```yaml
- name: agent/run
  description: Execute a registered Betty agent
  handler:
    runtime: python
    script: skills/agent.run/agent_run.py
  parameters:
    - name: agent_path
      type: string
      required: true
```

This enables Claude Code to invoke agents directly:
```
User: "Run the API designer agent to create a user management API"
Claude: [Invokes /agent/run api.designer "create user management API"]
```

## Related Skills

- **agent.define** - Create and register new agent manifests
- **agent.validate** - Validate agent manifests before execution
- **run.agent** - Legacy simulation tool (read-only, no execution)
- **skill.define** - Register skills that agents can invoke
- **hook.simulate** - Test hooks before registration

## Changelog

### v0.1.0 (2025-10-23)
- Initial implementation
- Support for iterative and oneshot reasoning modes
- Claude API integration with mock fallback
- Execution logging to agent_logs/
- Comprehensive error handling
- CLI and programmatic interfaces
- Plugin integration for Claude Code

## Future Enhancements

Planned features for future versions:

- **v0.2.0**:
  - Real Claude API integration (currently mocked)
  - Skill execution (currently simulated)
  - Iterative feedback loops
  - Performance metrics

- **v0.3.0**:
  - Agent context persistence
  - Multi-agent orchestration
  - Streaming responses
  - Parallel skill execution

- **v0.4.0**:
  - Agent memory and learning
  - Custom LLM backends
  - Agent marketplace integration
  - A/B testing framework

## License

Part of the Betty Framework. See project LICENSE for details.

## Support

For issues, questions, or contributions:
- GitHub: [Betty Framework Repository]
- Documentation: `/docs/skills/agent.run.md`
- Examples: `/examples/agents/`
