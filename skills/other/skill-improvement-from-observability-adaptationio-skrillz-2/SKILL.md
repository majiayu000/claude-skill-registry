---
name: skill-improvement-from-observability
description: Complete feedback loop from observability insights to skill updates. Use when analyzing enhanced telemetry patterns and automatically improving skills.
---

# Skill Improvement from Observability

**The Self-Improvement Loop**: Enhanced Telemetry → Pattern Analysis → Skill Updates → Better Performance

## Data Source

Primary: `{job="claude_code_enhanced"}` in Loki (from enhanced-telemetry hooks)

## Workflow

### 1. Collect Observability Insights

Use observability-analyzer with enhanced telemetry:
```logql
# Session analytics
{job="claude_code_enhanced", event_type="session_end"} | json

# Error patterns
{job="claude_code_enhanced", event_type="tool_result", status="error"} | json

# Tool sequences
{job="claude_code_enhanced", event_type="tool_call"} | json

# Prompt patterns
{job="claude_code_enhanced", event_type="user_prompt"} | json
```

### 2. Run Pattern Detection

Use observability-pattern-detector operations:
- `detect-failures` → Error patterns by tool
- `detect-tool-sequences` → Inefficient tool chains
- `detect-conversation-patterns` → User behavior insights
- `detect-context-issues` → Context management problems
- `detect-waste` → Redundant operations

### 3. Extract Actionable Patterns

Filter high-impact issues from enhanced telemetry:

**Error Analysis**:
```logql
sum by (tool, error_type) (count_over_time({job="claude_code_enhanced", event_type="tool_result", status="error"} | json [7d]))
```

**Tool Inefficiency**:
```logql
# Repeated Read→Read patterns (waste)
{job="claude_code_enhanced", event_type="tool_call"} | json | previous_tool="Read" and tool_name="Read"
```

**Context Issues**:
```logql
# Auto compaction frequency
count_over_time({job="claude_code_enhanced", event_type="context_compact", trigger="auto"} [7d])
```

### 4. Map Patterns to Skills

| Pattern | Likely Skill | Action |
|---------|--------------|--------|
| Bash command errors | bash-related skills | Add existence checks |
| File not found | file operation skills | Add path validation |
| Repeated Glob→Read | search skills | Optimize file discovery |
| High context usage | context-heavy skills | Add chunking |
| Many debugging prompts | core skills | Improve error messages |

### 5. Generate Improvement Recommendations

Based on enhanced telemetry patterns:

```json
{
  "improvement": {
    "pattern": "File not found errors",
    "occurrences": 45,
    "source_query": "{job=\"claude_code_enhanced\", event_type=\"tool_result\", status=\"error\"} | json | error_type=~\".*not found.*\"",
    "affected_skills": ["file-operations"],
    "recommendation": "Add file existence check before Read/Edit operations",
    "implementation": "Add pathlib.Path(file).exists() check",
    "priority": "high",
    "expected_impact": "Reduce errors by 80%"
  }
}
```

### 6. Track Effectiveness

After improvements deployed, measure:

```logql
# Before vs After error rates
sum(count_over_time({job="claude_code_enhanced", event_type="tool_result", status="error"} | json [7d]))

# Tool success rate improvement
sum(count_over_time({job="claude_code_enhanced", event_type="tool_result", status="success"} | json [7d])) /
sum(count_over_time({job="claude_code_enhanced", event_type="tool_result"} | json [7d]))
```

## Example Improvement Flows

### Flow 1: Error Reduction
```
Telemetry: "npm not found" × 45 in tool_result errors
    ↓
Pattern: Bash tool failures with npm commands
    ↓
Recommendation: Add npm availability check
    ↓
skill-updater applies changes
    ↓
Telemetry tracks: npm errors = 0 after deployment
    ↓
Result: ✅ 100% reduction
```

### Flow 2: Context Optimization
```
Telemetry: Auto-compaction triggered 12 times in 7 days
    ↓
Pattern: Large file reads accumulating tokens
    ↓
Recommendation: Add file chunking for large reads
    ↓
skill-updater applies changes
    ↓
Telemetry tracks: Auto-compactions = 2 after deployment
    ↓
Result: ✅ 83% reduction
```

### Flow 3: Tool Sequence Optimization
```
Telemetry: Glob→Read→Glob→Read pattern 89 times
    ↓
Pattern: Redundant file discovery
    ↓
Recommendation: Cache glob results within session
    ↓
skill-updater applies changes
    ↓
Telemetry tracks: Redundant glob reduced by 70%
    ↓
Result: ✅ Faster file operations
```

## Key Queries for Improvement Analysis

### High-Impact Errors
```logql
topk(10, sum by (tool, error_type) (count_over_time({job="claude_code_enhanced", event_type="tool_result", status="error"} | json [7d])))
```

### Session Quality Issues
```logql
# High error sessions
{job="claude_code_enhanced", event_type="session_end"} | json | error_count > 5

# Low productivity sessions (high turns, few tool calls)
{job="claude_code_enhanced", event_type="session_end"} | json | turn_count > 20 and tools_used < 5
```

### Tool Efficiency
```logql
# Tool usage distribution
sum by (tool) (count_over_time({job="claude_code_enhanced", event_type="tool_call"} | json [7d]))

# Error rate by tool
sum by (tool) (count_over_time({job="claude_code_enhanced", event_type="tool_result", status="error"} | json [7d])) /
sum by (tool) (count_over_time({job="claude_code_enhanced", event_type="tool_result"} | json [7d]))
```

### User Behavior Insights
```logql
# Prompt pattern trends
sum by (pattern) (count_over_time({job="claude_code_enhanced", event_type="user_prompt"} | json [7d]))

# Debugging frequency (indicates pain points)
count_over_time({job="claude_code_enhanced", event_type="user_prompt", pattern="debugging"} [7d])
```

## Integration with Ecosystem

Uses existing skills:
- **observability-analyzer**: Query enhanced telemetry data
- **observability-pattern-detector**: Detect improvement patterns
- **skill-updater**: Apply safe improvements
- **review-multi**: Validate changes
- **skill-tester**: Regression testing
- **enhanced-telemetry**: Source of all observability data

## Safety Classification

**Auto-Apply Safe**:
- ✅ Adding existence checks
- ✅ Adding error handling
- ✅ Improving error messages
- ✅ Updating documentation
- ✅ Adding validation

**Require Review**:
- ❌ Changing core logic
- ❌ Modifying APIs
- ❌ Removing functionality
- ❌ Changing data structures

## Effectiveness Metrics

Track improvement success:
```logql
# Calculate error reduction percentage
(before_errors - after_errors) / before_errors * 100

# Track pattern elimination
count_over_time({job="claude_code_enhanced"} | json | <pattern_filter> [7d])
```

Report format:
```json
{
  "improvement_id": "file-existence-check",
  "deployed": "2025-11-27",
  "before_errors": 45,
  "after_errors": 2,
  "reduction_percent": 95.6,
  "status": "successful"
}
```
