---
name: Issue Logging During Ralph Execution
description: >-
  Provides guidance for systematically logging issues during Ralph autonomous execution.
  Use when: (1) Any problem occurs during task execution, (2) Manual intervention is required,
  (3) Workflows don't work as expected, (4) Quality gates fail or require workarounds.
---

# Issue Logging During Ralph Execution

This skill provides structured guidance for logging issues that occur during Ralph autonomous execution, ensuring comprehensive data for revise reports.

## When to Log Issues

**Always log when:**
- Quality gates fail
- Manual intervention is required
- A task step is confusing or unclear
- Skills don't execute as expected
- Configuration is missing or incorrect
- External tools/services fail
- Workflows have bugs or broken instructions

**Log even if resolved:**
- You found a workaround
- The issue was temporary
- You manually fixed something
- The problem was environmental

## Issue Categories

### Ralph Systems
- Core execution engine problems
- Quality gate configuration issues
- Beads integration failures
- Performance bottlenecks
- State management problems

### Workflows & Process
- Unclear or broken instructions
- Missing workflow steps
- Process flow problems
- Coordination failures
- Resource gathering issues

### Code Rules & Documentation
- Missing validation rules
- Documentation inconsistencies
- Template problems
- Reference documentation gaps
- API documentation issues

### Skills & Prompts
- Skill execution failures
- Prompt clarity problems
- Error handling gaps
- Integration issues between skills
- Missing edge case handling

### Infrastructure & Tooling
- Missing dependencies
- Environment configuration problems
- CLI command failures
- File system issues
- External service problems

## Logging Format

**Required Fields:**
```json
{
  "timestamp": "2026-01-10T14:30:00Z",
  "category": "ralph_systems",
  "severity": "medium",
  "title": "Quality gate configuration incorrect",
  "description": "The lint command in quality-gates.json was using 'eslint' but project uses 'npm run lint'",
  "symptoms": "Command not found error when running quality gates",
  "workaround": "Manually updated the quality-gates.json file to use correct command",
  "context": "Executing Task 2: Add TypeScript types, quality gate stage"
}
```

**Severity Guidelines:**
- **Critical:** Blocks execution completely, data loss risk
- **High:** Significant manual intervention required
- **Medium:** Workaround needed, slows progress
- **Low:** Minor inconvenience, cosmetic issue

## Common Scenarios & Examples

### Quality Gate Failures
```json
{
  "timestamp": "2026-01-10T15:45:00Z",
  "category": "ralph_systems", 
  "severity": "high",
  "title": "TypeScript quality gate fails with module resolution error",
  "description": "tsc command fails due to missing path mapping in tsconfig.json",
  "symptoms": "error TS2307: Cannot find module '@types/node'",
  "workaround": "Manually installed missing types package and re-ran typecheck",
  "context": "Task 3 quality gate validation"
}
```

### Workflow Confusion
```json
{
  "timestamp": "2026-01-10T16:20:00Z",
  "category": "workflows_process",
  "severity": "medium", 
  "title": "Unclear instruction in skill execution",
  "description": "Step 2 of database-migration skill says 'configure connection' but doesn't specify which config file",
  "symptoms": "Spent 15 minutes searching for correct config location",
  "workaround": "Found config in .env file after checking multiple locations",
  "context": "Executing skill: database-migration"
}
```

### Missing Infrastructure
```json
{
  "timestamp": "2026-01-10T17:10:00Z",
  "category": "infrastructure_tooling",
  "severity": "high",
  "title": "Required CLI tool not installed",
  "description": "Skill requires 'jq' for JSON processing but tool not available in environment",
  "symptoms": "Command not found: jq",
  "workaround": "Rewrote JSON processing using native shell commands",
  "context": "Skill execution: json-config-parser"
}
```

## Integration with Execution Loop

**Where to add logging:**
1. **Before task execution:** Log if task setup fails
2. **During skill execution:** Log when skills don't work as expected
3. **Quality gate stage:** Log all failures and manual interventions
4. **State management:** Log when Beads operations fail
5. **After task completion:** Log if success required unusual steps

**Logging Implementation:**
- Append to `revise-issues.json` in execution output directory
- Use `.devagent/plugins/ralph/output/revise-issues.json` as the canonical example
- Use atomic writes to prevent corruption
- Include timestamps for chronological analysis
- Validate JSON structure before writing

## Error Handling for Logging

**If logging fails:**
- Don't let logging failures stop execution
- Fallback to simple Beads comment with issue summary
- Note logging failure in task comments
- Continue with primary execution objectives

**Best Practices:**
- Log immediately when issues occur
- Include enough context for later analysis
- Be specific about what went wrong
- Document successful workarounds
- Log even small issues that might indicate patterns