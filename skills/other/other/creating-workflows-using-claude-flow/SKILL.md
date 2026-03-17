---
name: creating-workflows-using-claude-flow
description: Use this skill when creating automated multi-phase workflows for development tasks using claude-flow orchestration. Implements patterns for implementation kickoff, verification, retry loops, and failure recovery.
---

# Creating Workflows Skill

Comprehensive guidance for building automated development workflows using claude-flow orchestration, multi-agent coordination, and intelligent verification systems.

## When to Use This Skill

This skill should be triggered when:

- Creating multi-phase development workflows (implementation + verification)
- Building automated CI/CD pipelines with intelligent agents
- Implementing retry loops with context injection
- Setting up verification steps with failure detection
- Orchestrating multiple agents for parallel/sequential task execution
- Creating workflows that need checkpoint recovery
- Implementing silent failure detection (processes that pretend to succeed)
- Building developer experience tooling with dry-run capabilities
- Documenting complex automated workflows
- Migrating manual processes to automated orchestration

## Key Concepts

### Shell Context Independence & jelmore Execution

**Critical Requirement**: Workflow scripts must not depend on interactive shell configuration.

**Why**: Shell aliases and functions don't propagate to subprocess environments (n8n workflows, cron jobs, systemd services).

#### jelmore: Convention-Based LLM Execution Primitive

**jelmore** provides a unified CLI for LLM invocations with shell context independence built-in. Use jelmore instead of calling LLM clients directly when building workflows.

**Why Use jelmore in Workflows**:

- ✅ Shell-context-free (no alias dependencies)
- ✅ Convention over configuration (auto-infer client/MCP servers)
- ✅ Detached Zellij sessions with immediate return
- ✅ Built-in iMi worktree integration
- ✅ Native Bloodbank event publishing
- ✅ Unified interface across all LLM clients

**Location**: `/home/delorenj/code/jelmore`

**Basic Usage in Workflows**:

```bash
# Instead of: npx claude-flow@alpha swarm "$objective" --claude
# Use jelmore with auto-inference:
uv run jelmore execute -p "$objective" --auto

# Instead of: gptme --model $KK "$task"
# Use jelmore with explicit client:
uv run jelmore execute -f task.md --client gptme --model-tier balanced

# For PR review workflows:
uv run jelmore execute --config pr-review.json --var PR_NUMBER=$pr_num --json
```

**Implementation Patterns**:

- Place scripts in `~/.local/bin/` with explicit PATH exports
- Replace aliases with direct command invocations or jelmore CLI
- Use jelmore for LLM invocations (inherits detached Zellij pattern)
- Return session identifiers immediately for observability

**See**:

- `ecosystem-patterns` skill - jelmore architecture and patterns
- `bloodbank-n8n-event-driven-workflows` skill - Event-driven integration
- `/home/delorenj/code/jelmore/CLI.md` - Complete CLI reference

### Multi-Phase Workflows

Workflows split into distinct phases with different execution strategies:

- **Phase 1 (Kickoff)**: Implementation via multi-agent orchestration (parallel execution)
- **Phase 2 (Verification)**: System state validation (sequential execution)
- **Phase N**: Additional phases as needed (testing, deployment, etc.)

### Retry Loops with Context Injection

When Phase 2 fails, retry Phase 1 with failure context:

- Append failure details to context string
- Increment attempt counter
- Enforce max retry limit
- Provide comprehensive failure summary on exhaustion

### Silent Failure Detection

Processes that don't properly report errors require explicit monitoring:

- Log pattern matching (success indicators)
- Error pattern matching (failure indicators)
- Timeout enforcement
- Background process monitoring

### Claude-Flow Integration

**Critical**: `claude-flow@alpha` v2.7.26+ does NOT support `workflow execute` command.

**Available Commands**:

- `swarm <objective>` - Multi-agent coordination with parallel execution
- `sparc <mode>` - SPARC methodology (spec, architect, tdd, integration)
- `stream-chain` - Chain multiple Claude instances with context preservation
- `agent <action>` - Agent management (spawn, list, terminate)

## Quick Reference

### 1. Basic Workflow Script Structure

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Parse CLI arguments
TASK_FILE="${PROJECT_ROOT}/TASK.md"
PHASE="all"
MAX_RETRIES=2
RETRY_ENABLED=true
DRY_RUN=false

# Parse flags (--task, --phase, --max-retries, --no-retry, --dry-run, --help)
# Implement usage() function
# Validate inputs
```

### 2. Phase 1: Implementation with jelmore (Recommended)

```bash
run_phase1() {
  local attempt=$1
  local context_override="${2:-$CONTEXT}"

  echo -e "${GREEN}Running Phase 1: Implementation${NC}"

  if [[ $attempt -gt 1 ]]; then
    echo -e "${BLUE}Retry attempt $((attempt - 1))/${MAX_RETRIES}${NC}"
  fi

  # jelmore execution with JSON output
  local jelmore_output
  jelmore_output=$(uv run jelmore execute \
    --file "$TASK_FILE" \
    --auto \
    --json 2>&1)

  local exit_code=$?

  # Parse jelmore response
  if [[ $exit_code -eq 0 ]]; then
    local session_name=$(echo "$jelmore_output" | jq -r '.session_name')
    local execution_id=$(echo "$jelmore_output" | jq -r '.execution_id')
    local log_path=$(echo "$jelmore_output" | jq -r '.log_path')

    echo -e "${GREEN}✓ Execution started${NC}"
    echo "  Session: $session_name"
    echo "  Execution ID: $execution_id"
    echo "  Logs: $log_path"
    echo ""
    echo "  Attach: zellij attach $session_name"

    # Store for later reference
    export JELMORE_SESSION="$session_name"
    export JELMORE_EXECUTION_ID="$execution_id"
    export JELMORE_LOG_PATH="$log_path"
  else
    echo -e "${RED}Error: jelmore execution failed${NC}"
    echo "$jelmore_output"
    return 1
  fi

  return 0
}
```

**Alternative: Phase 1 with Claude-Flow Swarm (Legacy Pattern)**

```bash
run_phase1_legacy() {
  local attempt=$1
  local context_override="${2:-$CONTEXT}"

  echo -e "${GREEN}Running Phase 1: Implementation${NC}"

  if [[ $attempt -gt 1 ]]; then
    echo -e "${BLUE}Retry attempt $((attempt - 1))/${MAX_RETRIES}${NC}"
  fi

  # Read task content
  local task_content
  if [[ -f "$TASK_FILE" ]]; then
    task_content=$(cat "$TASK_FILE")
  else
    echo -e "${RED}Error: Task file not found: $TASK_FILE${NC}"
    return 1
  fi

  # Build objective with context
  local objective="$task_content"
  if [[ -n "$context_override" ]]; then
    objective="$objective\n\nAdditional Context: $context_override"
  fi

  # Execute swarm (opens Claude Code CLI)
  npx claude-flow@alpha swarm "$objective" \
    --strategy development \
    --parallel \
    --max-agents 5 \
    --claude

  return $?
}
```

### 3. Phase 2: Verification with Silent Failure Detection

```bash
run_phase2() {
  echo -e "${GREEN}Running Phase 2: Verification${NC}"
  local phase2_failed=false

  # Step 1: Backend startup with log monitoring
  echo -e "${BLUE}[Step 1/N] Starting backend...${NC}"

  # Start process in background
  your_start_command > /tmp/backend.log 2>&1 &
  local backend_pid=$!

  # Watch logs for success indicator (30s timeout)
  local timeout=30
  local elapsed=0
  local backend_started=false

  while [[ $elapsed -lt $timeout ]]; do
    # Check for success pattern
    if grep -q "SUCCESS_PATTERN" /tmp/backend.log 2>/dev/null; then
      backend_started=true
      echo -e "${GREEN}✓ Backend started${NC}"
      break
    fi

    # Check for error patterns
    if grep -qi "error\|failed" /tmp/backend.log 2>/dev/null; then
      echo -e "${RED}✗ Backend errors detected${NC}"
      cat /tmp/backend.log
      phase2_failed=true
      break
    fi

    sleep 1
    elapsed=$((elapsed + 1))
  done

  if [[ "$backend_started" == "false" && "$phase2_failed" == "false" ]]; then
    echo -e "${RED}✗ Backend startup timed out${NC}"
    cat /tmp/backend.log
    phase2_failed=true
  fi

  if [[ "$phase2_failed" == "true" ]]; then
    return 1
  fi

  # Step 2: Additional verification steps
  # ...

  echo -e "${GREEN}✓ Phase 2 complete${NC}"
  return 0
}
```

### 4. Retry Loop Implementation

```bash
case "$PHASE" in
  all|*)
    ATTEMPT=1
    PHASE1_SUCCESS=false
    PHASE2_SUCCESS=false

    while [[ $ATTEMPT -le $((MAX_RETRIES + 1)) ]]; do
      echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
      echo -e "${YELLOW}Workflow Attempt ${ATTEMPT}/$((MAX_RETRIES + 1))${NC}"
      echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

      # Phase 1 with retry context
      RETRY_CONTEXT="$CONTEXT"
      if [[ $ATTEMPT -gt 1 ]]; then
        RETRY_CONTEXT="$CONTEXT | RETRY: Previous Phase 2 verification failed. Review logs and address failures."
      fi

      run_phase1 $ATTEMPT "$RETRY_CONTEXT"
      PHASE1_EXIT=$?

      if [[ $PHASE1_EXIT -ne 0 ]]; then
        echo -e "${RED}Phase 1 failed with exit code $PHASE1_EXIT${NC}"

        if [[ "$RETRY_ENABLED" == "false" || $ATTEMPT -gt $MAX_RETRIES ]]; then
          echo -e "${RED}No more retries. Exiting.${NC}"
          exit $PHASE1_EXIT
        fi

        ATTEMPT=$((ATTEMPT + 1))
        continue
      fi

      PHASE1_SUCCESS=true
      echo -e "${GREEN}✓ Phase 1 completed${NC}"

      # Phase 2
      run_phase2
      PHASE2_EXIT=$?

      if [[ $PHASE2_EXIT -ne 0 ]]; then
        if [[ $ATTEMPT -ge $((MAX_RETRIES + 1)) ]]; then
          # Exhausted retries - provide guidance
          echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
          echo -e "${YELLOW}Retry Summary:${NC}"
          echo "  Total attempts: $ATTEMPT"
          echo "  Phase 1: ${GREEN}✓ Success${NC}"
          echo "  Phase 2: ${RED}✗ Failed${NC}"
          echo -e "${BLUE}Next steps:${NC}"
          echo "  1. Review Phase 2 logs"
          echo "  2. Manually investigate failures"
          echo "  3. Run Phase 2 only: $0 --phase 2"
          echo "  4. Increase retries: $0 --max-retries 5"
          exit $PHASE2_EXIT
        fi

        echo -e "${BLUE}Phase 2 Failed - Triggering Retry${NC}"
        echo -e "${YELLOW}Looping back to Phase 1 with failure context...${NC}"
        ATTEMPT=$((ATTEMPT + 1))
        sleep 2
        continue
      fi

      # Success
      PHASE2_SUCCESS=true
      break
    done

    # Final status
    if [[ "$PHASE1_SUCCESS" == "true" && "$PHASE2_SUCCESS" == "true" ]]; then
      echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
      echo -e "${GREEN}✅ Workflow completed successfully${NC}"
      echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

      if [[ $ATTEMPT -gt 1 ]]; then
        echo -e "${BLUE}Success after $((ATTEMPT - 1)) retry attempt(s)${NC}"
      fi

      exit 0
    fi
    ;;
esac
```

### 5. Dry-Run Mode

```bash
if [[ "$DRY_RUN" == "true" ]]; then
  echo -e "${YELLOW}DRY RUN MODE${NC}"
  echo "Would execute Phase 1:"
  echo "  npx claude-flow@alpha swarm \"\$(cat $TASK_FILE)\" \\"
  echo "    --strategy development \\"
  echo "    --parallel \\"
  echo "    --max-agents 5 \\"
  echo "    --claude"
  echo ""
  echo "Would execute Phase 2:"
  echo "  1. Start backend (with log monitoring)"
  echo "  2. Build artifacts"
  echo "  3. Run verification checks"

  if [[ "$RETRY_ENABLED" == "true" ]]; then
    echo ""
    echo "Retry loop: Phase 2 failures retry Phase 1 (max $MAX_RETRIES attempts)"
  fi

  exit 0
fi
```

## Common Patterns

### Pattern 1: Backend/Service Startup Monitoring

**Problem**: Process managers (mise, pm2, etc.) often return success even when compilation fails.

**Solution**: Monitor logs for explicit success indicators.

```bash
# Start process
mise start > /tmp/service.log 2>&1 &

# Monitor for success pattern
while [[ $elapsed -lt $timeout ]]; do
  if grep -q "Accepted new IPC connection" /tmp/service.log; then
    echo "✓ Service started"
    break
  fi

  if grep -qi "error|compilation failed" /tmp/service.log; then
    echo "✗ Service failed"
    cat /tmp/service.log
    exit 1
  fi

  sleep 1
  elapsed=$((elapsed + 1))
done
```

### Pattern 2: File Validation After Build

**Problem**: Builds may appear successful but produce incomplete artifacts.

**Solution**: Explicitly verify required files exist.

```bash
required_files=(
  "dist/manifest.json"
  "dist/bundle.js"
  "dist/styles.css"
)

for file in "${required_files[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "✗ Required file missing: $file"
    exit 1
  fi
done

echo "✓ All artifacts present"
```

### Pattern 3: Manual Verification Prompts

**Problem**: Some verification steps can't be automated (UI testing, Chrome extension reload).

**Solution**: Provide clear instructions and wait for confirmation.

```bash
echo -e "${BLUE}[Step N/N] Manual Verification Required${NC}"
echo -e "${YELLOW}Please complete these steps:${NC}"
echo "  1. Open chrome://extensions"
echo "  2. Enable 'Developer mode'"
echo "  3. Find extension and click 'Reload'"
echo "  4. Test on target page"
echo ""
echo -e "${YELLOW}Press Enter when complete, or Ctrl+C to abort...${NC}"
read -r

echo -e "${GREEN}✓ Manual verification complete${NC}"
```

### Pattern 4: Context Injection on Retry

**Problem**: Retries without context repeat the same mistakes.

**Solution**: Append failure information to task context.

```bash
RETRY_CONTEXT="$CONTEXT"
if [[ $ATTEMPT -gt 1 ]]; then
  RETRY_CONTEXT="$CONTEXT | RETRY: Previous Phase 2 verification failed. Specific failure: $FAILURE_REASON. Review verification logs at $LOG_PATH and address these issues."
fi

run_phase1 $ATTEMPT "$RETRY_CONTEXT"
```

### Pattern 5: Comprehensive Error Reporting

**Problem**: Failures without guidance leave users stuck.

**Solution**: Provide actionable next steps on failure.

```bash
if [[ $MAX_RETRIES_EXHAUSTED == true ]]; then
  echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${YELLOW}Retry Summary:${NC}"
  echo "  Total attempts: $ATTEMPT"
  echo "  Phase 1 status: ${GREEN}✓ Success${NC}"
  echo "  Phase 2 status: ${RED}✗ Failed${NC}"
  echo ""
  echo -e "${BLUE}Next steps:${NC}"
  echo "  1. Review Phase 2 logs in $LOG_DIR"
  echo "  2. Check backend/service status: ps aux | grep service"
  echo "  3. Run Phase 2 only: $0 --phase 2"
  echo "  4. Increase retries: $0 --max-retries 5"
  echo "  5. Contact team if issue persists: #dev-support"
fi
```

## Documentation Patterns

### 1. Workflow Overview Document

Create a comprehensive markdown document (e.g., `workflow-name.md`) with:

- **Purpose**: What the workflow does
- **Phases**: Detailed breakdown of each phase
- **Trigger**: How to invoke the workflow
- **Inputs**: Required parameters and files
- **Outputs**: Generated artifacts and reports
- **Success Criteria**: How to verify completion
- **Failure Recovery**: Common issues and solutions
- **Manual Steps**: Any non-automated requirements

### 2. Quick Reference Cheat Sheet

Create a concise one-page reference (e.g., `QUICK-REFERENCE.md`) with:

- Common commands (full workflow, individual phases, dry-run)
- CLI flags and options
- Output file locations
- Troubleshooting commands
- Emergency procedures

### 3. README for Workflows Directory

Create `README.md` in workflows directory with:

- List of all available workflows
- When to use each workflow
- Quick start examples
- Common configuration options
- Links to detailed documentation

### 4. Implementation Report Template

After execution, generate report with:

- Workflow name and version
- Execution timestamp
- All phases executed with status
- Retry attempts (if any)
- Generated artifacts with paths
- Performance metrics (execution time, agent utilization)
- Next steps or recommendations

## CLI Argument Patterns

### Standard Flags

```bash
-t, --task FILE         Task specification file (default: TASK.md)
-c, --context STRING    Additional context for requirements
-p, --phase PHASE       Run specific phase only (1, 2, etc.)
-s, --skip-verification Skip Phase N verification
-r, --max-retries N     Max retry attempts on failure (default: 2)
--no-retry              Disable retry loop (fail immediately)
-d, --dry-run          Show what would be executed
-h, --help             Show help message
```

### Usage Function Template

```bash
usage() {
  cat <<EOF
Usage: $0 [options]

Execute the ${WORKFLOW_NAME} workflow

Phases:
  Phase 1: ${PHASE1_DESCRIPTION}
  Phase 2: ${PHASE2_DESCRIPTION}

Options:
  -t, --task FILE         Task specification file (default: TASK.md)
  -c, --context STRING    Additional context
  -p, --phase PHASE       Run specific phase (1 or 2)
  -r, --max-retries N     Max retries (default: 2)
  --no-retry              Disable retry loop
  -d, --dry-run          Preview without execution
  -h, --help             Show this message

Examples:
  # Full workflow with retry
  $0 --task TASK.md

  # Phase 1 only
  $0 --task TASK.md --phase 1

  # Disable retry
  $0 --task TASK.md --no-retry

  # Preview execution
  $0 --task TASK.md --dry-run

EOF
  exit 1
}
```

## Testing Strategies

### 1. Dry-Run Testing

Always implement and test dry-run mode:

```bash
./workflow-script.sh --dry-run
# Should show commands without executing
# Verify output matches expected execution plan
```

### 2. Individual Phase Testing

Test each phase independently:

```bash
# Test Phase 1 in isolation
./workflow-script.sh --task TASK.md --phase 1

# Test Phase 2 in isolation (requires Phase 1 artifacts)
./workflow-script.sh --phase 2
```

### 3. Retry Loop Testing

Test retry behavior with intentional failures:

```bash
# Modify Phase 2 to fail temporarily
# Run full workflow
./workflow-script.sh --task TASK.md

# Verify:
# - Phase 1 executes
# - Phase 2 fails
# - Phase 1 re-executes with failure context
# - Loop continues until max retries
# - Comprehensive failure summary appears
```

### 4. Silent Failure Detection Testing

Test failure detection:

```bash
# Modify backend to fail compilation
# Run workflow
./workflow-script.sh --task TASK.md --phase 2

# Verify:
# - Detects compilation errors in logs
# - Fails with clear error message
# - Shows relevant log excerpts
```

## Integration with Claude-Flow

### Swarm Command

Best for: Multi-agent implementation workflows

```bash
npx claude-flow@alpha swarm "$objective" \
  --strategy development \        # Options: research, development, testing, optimization
  --parallel \                    # Enable parallel execution (2.8-4.4x speedup)
  --max-agents 5 \               # Limit concurrent agents
  --claude                        # Open Claude Code CLI (default: built-in executor)
```

### SPARC Command

Best for: Structured development phases (spec, architect, tdd)

```bash
npx claude-flow@alpha sparc spec "$task"     # Requirements analysis
npx claude-flow@alpha sparc architect "$task" # System design
npx claude-flow@alpha sparc tdd "$task"      # Test-driven implementation
```

### Stream-Chain Command

Best for: Sequential workflows with context preservation

```bash
npx claude-flow@alpha stream-chain run \
  "analyze requirements" \
  "design architecture" \
  "implement solution"
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **workflow-script-template.sh** - Complete bash script template with all patterns
- **phase-patterns.md** - Common Phase 1/2/N implementation patterns
- **retry-strategies.md** - Retry loop configurations and failure handling
- **verification-patterns.md** - Silent failure detection and validation strategies
- **documentation-templates.md** - Markdown templates for workflow docs
- **cli-design.md** - CLI argument parsing and usage function patterns

Use these references when building new workflows.

## Working with This Skill

### For Beginners

Start with the template:

1. Copy `workflow-script-template.sh` from `assets/`
2. Customize Phase 1 (implementation) with your task
3. Customize Phase 2 (verification) with your checks
4. Test with `--dry-run` first
5. Run individual phases before full workflow

### For Intermediate Users

Implement patterns:

- Add retry loop with context injection
- Implement silent failure detection for your tools
- Add manual verification prompts where needed
- Create comprehensive documentation

### For Advanced Users

Optimize and extend:

- Add additional phases (testing, deployment, rollback)
- Implement checkpoint recovery between phases
- Add performance metrics collection
- Create reusable verification modules
- Integrate with CI/CD pipelines

## Common Pitfalls

### Pitfall 1: Using Non-Existent CLI Commands

**Problem**: Documentation may reference commands that don't exist in your version.

**Solution**: Always verify with `--help`:

```bash
npx claude-flow@alpha --help
npx claude-flow@alpha swarm --help
```

### Pitfall 2: Missing Failure Detection

**Problem**: Process returns success but actually failed.

**Solution**: Never trust exit codes alone. Monitor logs for explicit success patterns.

### Pitfall 3: Retrying Without Context

**Problem**: Retries repeat identical failures.

**Solution**: Always inject failure context into retry attempts.

### Pitfall 4: Poor Error Messages

**Problem**: Users don't know what to do when workflow fails.

**Solution**: Provide specific next steps, log locations, and troubleshooting commands.

### Pitfall 5: No Dry-Run Mode

**Problem**: Can't preview workflow without executing.

**Solution**: Always implement `--dry-run` mode that shows commands without running them.

## Resources

### In This Skill

- `references/` - Detailed pattern documentation
- `assets/` - Templates and examples
- `scripts/` - Helper utilities

### External

- Claude-Flow Documentation: https://github.com/ruvnet/claude-flow
- Bash Best Practices: https://mywiki.wooledge.org/BashGuide
- Mise Task Runner: https://mise.jdx.dev/tasks.html

## Notes

- This skill codifies patterns from real workflow implementations
- Always test dry-run mode before production use
- Retry loops should have reasonable limits (2-5 attempts max)
- Silent failure detection is critical for reliable automation
- Documentation is as important as the workflow itself
