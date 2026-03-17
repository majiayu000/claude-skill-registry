# parallel-dispatch

Generic parallel agent orchestration utility for launching multiple agents concurrently.

## Triggers

- "launch parallel [agents]"
- "concurrent review by [agents]"
- "multi-agent [task]"
- "parallel analysis"
- "dispatch agents"

## Purpose

This skill provides the foundational infrastructure for launching multiple agents in parallel, collecting their results, and handling timeouts. It is used by higher-level skills like `artifact-orchestration`, `review-synthesis`, and `gate-evaluation`.

## Behavior

When triggered, this skill:

1. **Parses agent configuration**:
   - Agent names (from built-in or custom)
   - Prompt templates for each agent
   - Shared context/artifact reference
   - Timeout settings

2. **Prepares agent-specific prompts**:
   - Loads prompt template per agent
   - Injects shared context (artifact path, requirements)
   - Adds output format requirements

3. **Launches agents in parallel**:
   - Uses single message with multiple Task tool calls
   - Each agent runs independently
   - No inter-agent communication during execution

4. **Collects results**:
   - Waits for all agents or timeout
   - Captures success/failure per agent
   - Structures results for downstream processing

5. **Returns consolidated results**:
   - Per-agent output
   - Execution metadata (duration, status)
   - Aggregated insights (if configured)

## Configuration Format

```yaml
dispatch:
  name: "artifact-review"
  timeout: 300  # seconds

  agents:
    - name: security-architect
      prompt: |
        Review the artifact at {artifact_path} for security concerns.
        Focus on: authentication, authorization, data protection, input validation.
        Output format: structured findings with severity ratings.

    - name: test-architect
      prompt: |
        Review the artifact at {artifact_path} for testability.
        Focus on: test coverage gaps, edge cases, integration points.
        Output format: test recommendations with priority.

    - name: requirements-analyst
      prompt: |
        Review the artifact at {artifact_path} for requirements traceability.
        Focus on: requirement coverage, gaps, conflicts.
        Output format: traceability assessment.

  context:
    artifact_path: ".aiwg/architecture/sad.md"
    requirements_path: ".aiwg/requirements/"

  result_format: structured  # or 'raw'
  aggregate: true  # combine findings
```

## Usage Examples

### Basic Parallel Review

```
User: "Launch parallel review of the SAD by security-architect, test-architect, and requirements-analyst"

Skill executes:
1. Loads SAD from .aiwg/architecture/
2. Prepares review prompts for each agent
3. Dispatches all three agents in single message
4. Collects reviews (timeout: 5 min)
5. Returns structured results
```

### Custom Agent Configuration

```
User: "Dispatch agents with config from .aiwg/config/review-config.yaml"

Skill executes:
1. Loads configuration file
2. Validates agent names exist
3. Prepares prompts from templates
4. Dispatches with configured timeout
5. Returns results in configured format
```

## Result Format

### Structured Results

```json
{
  "dispatch_id": "review-20251208-143022",
  "status": "completed",
  "duration_seconds": 127,
  "agents": {
    "security-architect": {
      "status": "success",
      "duration": 45,
      "output": {
        "findings": [...],
        "severity_summary": {...},
        "recommendations": [...]
      }
    },
    "test-architect": {
      "status": "success",
      "duration": 52,
      "output": {
        "coverage_gaps": [...],
        "test_recommendations": [...],
        "priority_order": [...]
      }
    },
    "requirements-analyst": {
      "status": "success",
      "duration": 38,
      "output": {
        "traced_requirements": [...],
        "gaps": [...],
        "conflicts": [...]
      }
    }
  },
  "aggregate": {
    "total_findings": 12,
    "critical_issues": 2,
    "recommendations": 8
  }
}
```

### Raw Results

```json
{
  "dispatch_id": "review-20251208-143022",
  "agents": {
    "security-architect": "Full text output from agent...",
    "test-architect": "Full text output from agent...",
    "requirements-analyst": "Full text output from agent..."
  }
}
```

## Error Handling

### Timeout Handling

```yaml
timeout_behavior:
  action: "partial"  # or "fail"
  # partial: return results from completed agents
  # fail: return error if any agent times out
```

### Agent Failure

```yaml
failure_behavior:
  action: "continue"  # or "abort"
  # continue: proceed with other agents
  # abort: stop all if one fails
  retry: 1  # retry failed agents once
```

## Built-in Agent Groups

For convenience, common agent combinations are pre-defined:

### Architecture Review Group
```yaml
group: architecture-review
agents:
  - security-architect
  - test-architect
  - requirements-analyst
  - technical-writer
```

### Security Review Group
```yaml
group: security-review
agents:
  - security-architect
  - security-auditor
  - privacy-officer
```

### Documentation Review Group
```yaml
group: documentation-review
agents:
  - technical-writer
  - requirements-analyst
  - domain-expert
```

### Marketing Review Group
```yaml
group: marketing-review
agents:
  - brand-guardian
  - legal-reviewer
  - quality-controller
  - accessibility-checker
```

## Integration

This skill is the foundation for:
- `artifact-orchestration` (SDLC)
- `gate-evaluation` (SDLC)
- `review-synthesis` (MMK)
- `brand-compliance` (MMK)

## CLI Usage

```bash
# Using Python script
python parallel_dispatcher.py --config review-config.yaml

# With inline agents
python parallel_dispatcher.py \
  --agents "security-architect,test-architect" \
  --artifact ".aiwg/architecture/sad.md" \
  --timeout 300

# List available groups
python parallel_dispatcher.py --list-groups

# Validate configuration
python parallel_dispatcher.py --config review-config.yaml --validate
```

## Performance Considerations

- **Optimal parallelism**: 3-5 agents per dispatch
- **Timeout guidance**: 2-5 minutes for document review
- **Memory**: Each agent has isolated context
- **Cost**: Parallel execution uses more tokens but reduces wall-clock time

## References

- Agent definitions: Framework `agents/` directories
- Configuration schema: `schemas/dispatch-config.schema.json`
- Result schema: `schemas/dispatch-result.schema.json`
