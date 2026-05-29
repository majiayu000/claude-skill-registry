---
name: repo-readiness
description: Prepare any repository for new work by analyzing CLAUDE.md, file structure, mission/objectives, and establishing work readiness state. Auto-executes before new tasks to provide context.
version: 1.0.0
category: workspace-hub
type: skill
trigger: pre-task
auto_execute: true
capabilities:
  - claude_config_analysis
  - structure_assessment
  - mission_extraction
  - context_preparation
  - work_readiness_validation
tools:
  - Read
  - Glob
  - Grep
  - Bash
related_skills:
  - compliance-check
  - repo-sync
  - sparc-workflow
---

# Repository Readiness Skill

> Automatically prepare repositories for new work by analyzing configuration, structure, mission, and establishing complete work context.

## Quick Start

```bash
# Manual trigger
/repo-readiness

# Auto-triggers before:
# - New task execution
# - Feature development
# - SPARC workflow initiation
# - Agent assignment

# Direct check
./scripts/check_repo_readiness.sh <repo-name>
```

## When to Use

**AUTO-EXECUTES (via hook):**
- Before starting any new task in a repository
- When switching to a different repository
- Before SPARC specification phase
- Before agent assignment for new work

**MANUAL TRIGGER:**
- When repository context is unclear
- Before major refactoring
- After long breaks from a repository
- When onboarding to an existing project
- Before cross-repo coordination

## Prerequisites

- Repository is cloned locally
- Git is initialized
- Read access to repository files
- (Optional) Internet for external documentation lookup

## Overview

The repo-readiness skill performs comprehensive analysis of a repository to establish complete work context before executing any new tasks. It replaces manual context gathering with automated, systematic preparation.

### What It Analyzes

1. **Configuration**: CLAUDE.md, .claude/*, .agent-os/*
2. **Structure**: Directory organization, module architecture
3. **Mission**: Product vision, objectives, technical decisions
4. **State**: Git status, dependencies, environment setup
5. **Standards**: Compliance with workspace-hub standards
6. **Context**: Historical decisions, conventions, patterns

### Output

Generates a comprehensive readiness report with:
- Configuration summary
- Structure analysis
- Mission & objectives extraction
- Readiness assessment (✅ Ready / ⚠️ Needs Attention / ❌ Not Ready)
- Recommended actions
- Context for AI agents

## Core Operations

### 1. Configuration Analysis

**Analyzes:**
```
✓ Root CLAUDE.md
✓ .claude/CLAUDE.md (extended config)
✓ .claude.json (MCP settings)
✓ .mcp.json (MCP servers)
✓ .agent-os/ configuration
✓ Repository-specific rules
```

**Extracts:**
- Critical rules and constraints
- File organization standards
- Testing requirements
- AI agent guidelines
- Tool preferences (UV, pytest, etc.)
- Integration points

**Example Output:**
```markdown
## Configuration Summary

### CLAUDE.md Status: ✅ Found
- **Location**: /root/CLAUDE.md
- **Critical Rules**:
  - TDD mandatory
  - YAGNI principle
  - UV environment required
- **File Organization**: Modular structure enforced
- **Testing**: pytest with 80% coverage minimum
- **AI Guidelines**: Question before implementation

### Extended Config: ✅ Found (.claude/CLAUDE.md)
- SPARC methodology enabled
- MCP integration configured
- HTML reporting standards defined

### MCP Configuration: ✅ Found
- Active servers: claude-flow, browser-automation
- Tools available: 47 MCP tools
```

### 2. Structure Assessment

**Analyzes:**
```
✓ Directory organization
✓ Module architecture
✓ File naming conventions
✓ Test structure
✓ Documentation presence
✓ Script organization
```

**Checks Against:**
- FILE_ORGANIZATION_STANDARDS.md
- Repository best practices
- Module patterns
- Naming conventions

**Example Output:**
```markdown
## Structure Assessment

### Directory Organization: ✅ Compliant
```
repo/
├── src/              ✅ Present
│   └── modules/      ✅ Modular structure
├── tests/            ✅ Present
│   ├── unit/         ✅ Organized
│   └── integration/  ✅ Organized
├── docs/             ✅ Present
├── config/           ✅ Present
├── scripts/          ✅ Present
├── data/             ✅ Present
└── reports/          ✅ Present
```

### Module Architecture: ✅ Well-Organized
- **Modules Found**: 5
  - data_processor/
  - visualization/
  - analysis/
  - reporting/
  - utilities/

### Naming Conventions: ⚠️ Minor Issues
- ✅ Python files use snake_case
- ✅ Modules use lowercase
- ⚠️ 2 files need organization (see details)

### Test Coverage: ✅ Good
- Unit tests: 45 files
- Integration tests: 12 files
- Test coverage: 85% (target: 80%)
```

### 3. Mission & Objectives Extraction

**Sources:**
```
✓ .agent-os/product/mission.md
✓ .agent-os/product/tech-stack.md
✓ .agent-os/product/roadmap.md
✓ .agent-os/product/decisions.md
✓ README.md
✓ docs/OVERVIEW.md
```

**Extracts:**
- Project purpose and vision
- Key objectives
- Technical stack
- Architecture decisions
- Current roadmap
- Recent decisions

**Example Output:**
```markdown
## Mission & Objectives

### Project Purpose
Energy data analysis and visualization platform for offshore oil & gas operations.

### Key Objectives
1. Process BSEE production data with 99.9% accuracy
2. Generate interactive HTML reports with Plotly
3. NPV analysis for economic evaluation
4. Marine safety incident tracking
5. Support 10+ concurrent analysis workflows

### Technical Stack
- **Language**: Python 3.11+
- **Environment**: UV package manager
- **Testing**: pytest with 85% coverage
- **Visualization**: Plotly (interactive only)
- **Data**: Pandas, Polars
- **Reporting**: HTML with embedded plots

### Recent Decisions (Last 30 Days)
1. Migrated to UV from pip (2024-12-15)
2. Standardized on Plotly for all visualizations (2024-12-10)
3. Implemented SPARC workflow (2024-12-01)
```

### 4. State Assessment

**Checks:**
```
✓ Git status (clean/dirty)
✓ Branch information
✓ Remote status
✓ Dependencies installed
✓ Environment setup
✓ Recent commits
✓ Open issues/PRs
```

**Example Output:**
```markdown
## Repository State

### Git Status: ✅ Clean
- **Branch**: main
- **Commits ahead**: 0
- **Commits behind**: 0
- **Uncommitted changes**: None
- **Last commit**: 2024-12-20 14:23 - "Update NPV calculation logic"

### Environment: ✅ Ready
- UV environment: ✅ Detected (.venv/)
- Dependencies: ✅ Synchronized (pyproject.toml == uv.lock)
- Python version: ✅ 3.11.7

### Dependencies Status: ⚠️ 2 Updates Available
- plotly: 5.17.0 → 5.18.0 (minor)
- pandas: 2.1.3 → 2.1.4 (patch)
```

### 5. Standards Compliance

**Validates:**
```
✓ Logging standards
✓ Testing framework standards
✓ HTML reporting standards
✓ File organization standards
✓ Development workflow compliance
```

**Example Output:**
```markdown
## Standards Compliance

### Logging Standards: ✅ Compliant
- Standard format implemented
- Five log levels configured
- Rotation configured (10MB, 5 backups)

### Testing Standards: ✅ Compliant
- pytest configured
- Coverage threshold: 80% (current: 85%)
- Unit + integration tests present

### HTML Reporting: ✅ Compliant
- Interactive plots only (Plotly)
- CSV data with relative paths
- Reports in reports/ directory

### File Organization: ✅ Compliant
- Modular src/ structure
- Tests mirror source
- Documentation organized
```

### 6. Context Preparation

**Generates:**
```
✓ AI agent context summary
✓ Key conventions to follow
✓ Common patterns
✓ Recent changes
✓ Known issues
✓ Quick reference
```

**Example Output:**
```markdown
## AI Agent Context

### Key Conventions
- **Imports**: Use absolute imports from src/
- **Testing**: Write tests before implementation (TDD)
- **Data Loading**: Use relative paths from reports/
- **Error Handling**: Use custom exceptions in src/exceptions.py
- **Logging**: Use module-level logger = logging.getLogger(__name__)

### Common Patterns
1. **Data Pipeline**: load → validate → process → visualize → report
2. **Configuration**: YAML files in config/input/ directory
3. **Execution**: Bash scripts in scripts/ directory
4. **Reporting**: HTML with Plotly in reports/ directory

### Recent Changes (Last 7 Days)
- Refactored NPV calculation to support multiple discount rates
- Added new marine safety incident categorization
- Updated BSEE data extractor for 2024 format
- Enhanced error handling in data validation

### Known Issues
- Issue #42: Slow performance on files >100MB (workaround documented)
- Issue #38: Timezone handling in date parsing (fix in progress)

### Quick Reference
- Main entry point: `scripts/run_analysis.sh`
- Configuration: `config/input/<feature>.yaml`
- Documentation: `docs/README.md`
- Examples: `examples/`
```

## Readiness Assessment

### Overall Readiness Score

Calculated from:
- Configuration completeness (25%)
- Structure compliance (20%)
- Mission clarity (15%)
- State health (20%)
- Standards adherence (20%)

**Readiness Levels:**

```
✅ READY (90-100%)
   - All critical checks passed
   - Minor issues documented
   - Safe to proceed with new work

⚠️ NEEDS ATTENTION (70-89%)
   - Some issues need addressing
   - Can proceed with caution
   - Fix issues before major work

❌ NOT READY (<70%)
   - Critical issues present
   - Must resolve before proceeding
   - Blocks new work
```

### Example Assessment

```markdown
## Overall Readiness: ✅ READY (95%)

### Breakdown
- Configuration: ✅ 100% (All configs present and valid)
- Structure: ✅ 95% (2 minor file organization issues)
- Mission: ✅ 100% (Clear objectives and roadmap)
- State: ✅ 90% (2 dependency updates available)
- Standards: ✅ 95% (Full compliance, minor logging improvement)

### Recommended Actions
1. 📦 Update plotly to 5.18.0 (optional, minor version)
2. 📁 Organize 2 files in src/utilities/ into subfolders
3. 📝 Add logging to new marine_safety module (standard practice)

### Safe to Proceed: ✅ YES
All critical requirements met. Recommended actions can be addressed incrementally.
```

## Execution Checklist

**Pre-Check:**
- [ ] Repository path is valid
- [ ] Git repository initialized
- [ ] Read access to all files

**Analysis Phase:**
- [ ] Read CLAUDE.md (root and .claude/)
- [ ] Analyze directory structure
- [ ] Extract mission from .agent-os/
- [ ] Check git status
- [ ] Verify environment setup
- [ ] Validate standards compliance

**Reporting Phase:**
- [ ] Generate configuration summary
- [ ] Create structure assessment
- [ ] Extract mission & objectives
- [ ] Report repository state
- [ ] Calculate readiness score
- [ ] Provide recommended actions

**Post-Check:**
- [ ] Save readiness report to .claude/readiness-report.md
- [ ] Update repository context cache
- [ ] Provide summary to user or agent

## Hook Integration

### Pre-Task Hook

This skill auto-executes as a pre-task hook:

**Hook Configuration:**
```bash
# .claude/hooks/pre-task.sh
#!/bin/bash
# Auto-execute repo-readiness before any task

REPO_PATH="$(pwd)"
SKILL_PATH="$HOME/.claude/skills/workspace-hub/repo-readiness"

# Execute readiness check
"$SKILL_PATH/check_readiness.sh" "$REPO_PATH"

# Exit code determines if task can proceed
# 0 = Ready, 1 = Not ready (blocks task)
exit $?
```

**Trigger Conditions:**
- `/create-spec` command
- `/execute-tasks` command
- `/plan-product` command
- Any SPARC workflow phase
- Agent assignment via orchestrator

**Bypass Hook (when needed):**
```bash
# Force task execution even if not ready
SKIP_READINESS_CHECK=1 /execute-tasks "task description"
```

### Post-Task Hook (Optional)

Update readiness state after work:

```bash
# .claude/hooks/post-task.sh
#!/bin/bash
# Update readiness cache after task completion

REPO_PATH="$(pwd)"
TASK_ID="$1"

# Re-run readiness to update cache
"$HOME/.claude/skills/workspace-hub/repo-readiness/check_readiness.sh" "$REPO_PATH" --update-cache

# Log task completion
echo "$(date): Task $TASK_ID completed" >> .claude/task-history.log
```

## Automation Scripts

### 1. Check Readiness Script

**Location:** `.claude/skills/workspace-hub/repo-readiness/check_readiness.sh`

```bash
#!/bin/bash
# Repository Readiness Check Script

REPO_PATH="${1:-.}"
OUTPUT_FILE="${REPO_PATH}/.claude/readiness-report.md"

# Function: Check configuration
check_configuration() {
    local score=0

    # Check CLAUDE.md
    if [ -f "${REPO_PATH}/CLAUDE.md" ]; then
        echo "✅ Root CLAUDE.md found"
        ((score += 25))
    else
        echo "❌ Root CLAUDE.md missing"
    fi

    # Check extended config
    if [ -f "${REPO_PATH}/.claude/CLAUDE.md" ]; then
        echo "✅ Extended CLAUDE.md found"
        ((score += 25))
    fi

    # Check .agent-os
    if [ -d "${REPO_PATH}/.agent-os" ]; then
        echo "✅ Agent OS configuration found"
        ((score += 25))
    fi

    # Check MCP config
    if [ -f "${REPO_PATH}/.claude.json" ] || [ -f "${REPO_PATH}/.mcp.json" ]; then
        echo "✅ MCP configuration found"
        ((score += 25))
    fi

    echo "Configuration Score: ${score}/100"
    return $score
}

# Function: Check structure
check_structure() {
    local score=0
    local required_dirs=("src" "tests" "docs" "config" "scripts")

    for dir in "${required_dirs[@]}"; do
        if [ -d "${REPO_PATH}/${dir}" ]; then
            echo "✅ ${dir}/ present"
            ((score += 20))
        else
            echo "⚠️ ${dir}/ missing"
        fi
    done

    echo "Structure Score: ${score}/100"
    return $score
}

# Function: Check mission
check_mission() {
    local score=0

    if [ -f "${REPO_PATH}/.agent-os/product/mission.md" ]; then
        echo "✅ Mission defined"
        ((score += 50))
    fi

    if [ -f "${REPO_PATH}/.agent-os/product/roadmap.md" ]; then
        echo "✅ Roadmap defined"
        ((score += 50))
    fi

    echo "Mission Score: ${score}/100"
    return $score
}

# Function: Check state
check_state() {
    local score=0

    cd "$REPO_PATH" || exit 1

    # Check git status
    if git diff-index --quiet HEAD -- 2>/dev/null; then
        echo "✅ Git working directory clean"
        ((score += 50))
    else
        echo "⚠️ Uncommitted changes present"
        ((score += 25))
    fi

    # Check environment
    if [ -d ".venv" ] || [ -d "venv" ]; then
        echo "✅ Virtual environment detected"
        ((score += 50))
    fi

    echo "State Score: ${score}/100"
    return $score
}

# Main execution
main() {
    echo "========================================"
    echo "Repository Readiness Check"
    echo "Repository: ${REPO_PATH}"
    echo "Timestamp: $(date)"
    echo "========================================"
    echo ""

    # Run all checks
    check_configuration
    local config_score=$?

    check_structure
    local struct_score=$?

    check_mission
    local mission_score=$?

    check_state
    local state_score=$?

    # Calculate overall score
    local overall_score=$(( (config_score*25 + struct_score*20 + mission_score*15 + state_score*20) / 80 ))

    echo ""
    echo "========================================"
    echo "Overall Readiness: ${overall_score}%"

    if [ $overall_score -ge 90 ]; then
        echo "Status: ✅ READY"
        echo "========================================"
        return 0
    elif [ $overall_score -ge 70 ]; then
        echo "Status: ⚠️ NEEDS ATTENTION"
        echo "========================================"
        return 1
    else
        echo "Status: ❌ NOT READY"
        echo "========================================"
        return 2
    fi
}

main "$@"
```

### 2. Bulk Readiness Check

Check all repos in workspace:

```bash
#!/bin/bash
# Check readiness of all repositories in workspace-hub

WORKSPACE_ROOT="/mnt/github/workspace-hub"
READINESS_SCRIPT="$HOME/.claude/skills/workspace-hub/repo-readiness/check_readiness.sh"

# Get all repos from .gitignore
repos=$(grep -E "^[a-z].*/$" "${WORKSPACE_ROOT}/.gitignore" | sed 's/\///')

echo "Checking readiness of all repositories..."
echo ""

# Track results
ready_count=0
attention_count=0
not_ready_count=0

for repo in $repos; do
    repo_path="${WORKSPACE_ROOT}/${repo}"

    if [ -d "$repo_path" ]; then
        echo "Checking: $repo"

        if "$READINESS_SCRIPT" "$repo_path" > /dev/null 2>&1; then
            echo "  ✅ READY"
            ((ready_count++))
        else
            exit_code=$?
            if [ $exit_code -eq 1 ]; then
                echo "  ⚠️ NEEDS ATTENTION"
                ((attention_count++))
            else
                echo "  ❌ NOT READY"
                ((not_ready_count++))
            fi
        fi
    fi
done

echo ""
echo "Summary:"
echo "  Ready: $ready_count"
echo "  Needs Attention: $attention_count"
echo "  Not Ready: $not_ready_count"
```

## Error Handling

### Missing Configuration

**Error:** CLAUDE.md not found
```
❌ Critical: No CLAUDE.md found in repository root

Action Required:
1. Create CLAUDE.md with repository configuration
2. Use template from workspace-hub/templates/CLAUDE.md
3. Re-run readiness check

Quick Fix:
cp ~/workspace-hub/templates/CLAUDE.md ./CLAUDE.md
```

### Incomplete Structure

**Error:** Required directories missing
```
⚠️ Warning: Required directories missing
   Missing: tests/, docs/

Action Required:
1. Create missing directories
2. Follow FILE_ORGANIZATION_STANDARDS.md
3. Re-run readiness check

Quick Fix:
mkdir -p tests/{unit,integration} docs config scripts
```

### Unclear Mission

**Error:** No mission.md found
```
⚠️ Warning: Project mission not defined
   Missing: .agent-os/product/mission.md

Action Required:
1. Create .agent-os/product/mission.md
2. Define project purpose and objectives
3. Document technical decisions

Quick Fix:
mkdir -p .agent-os/product
cp ~/workspace-hub/templates/mission.md .agent-os/product/
```

### Dirty Git State

**Error:** Uncommitted changes present
```
⚠️ Warning: Repository has uncommitted changes
   Files modified: 5

Action Required:
1. Review uncommitted changes: git status
2. Commit changes: git add . && git commit -m "message"
3. Or stash: git stash
4. Re-run readiness check
```

### Environment Issues

**Error:** Virtual environment not found
```
⚠️ Warning: No virtual environment detected

Action Required:
1. Create UV environment: uv venv
2. Install dependencies: uv pip install -r requirements.txt
3. Activate environment: source .venv/bin/activate
4. Re-run readiness check
```

## Metrics & Success Criteria

### Performance Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Check Time | < 5 seconds | Time to complete all checks |
| Accuracy | > 95% | Correct readiness assessment |
| False Positives | < 5% | Incorrectly marked as ready |
| False Negatives | < 2% | Incorrectly marked as not ready |
| Cache Hit Rate | > 80% | Using cached readiness data |

### Coverage Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Repos with CLAUDE.md | 100% | Track per repo |
| Repos with mission.md | 100% | Track per repo |
| Structure compliance | > 95% | Average across repos |
| Standards adherence | > 90% | Average compliance score |

### Adoption Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Hook installation | 100% repos | Pre-task hook installed |
| Auto-execution rate | > 95% | Tasks with readiness check |
| Manual check usage | > 10/week | Explicit readiness checks |
| Issue detection | > 50% | Issues caught before work |

## Integration Points

### With SPARC Workflow

Readiness check before each SPARC phase:

```bash
# Before Specification
/repo-readiness → Analyze context → /create-spec

# Before Architecture
/repo-readiness → Verify structure → /sparc-architecture

# Before Implementation
/repo-readiness → Check environment → /execute-tasks
```

### With Compliance Check

Combined health validation:

```bash
# Readiness + compliance
/repo-readiness && /compliance-check

# Report both
./scripts/health-check.sh --full
```

### With Agent Orchestration

Provide context to agents:

```javascript
// Agent receives readiness report
{
  "task": "implement-feature-X",
  "repository": "digitalmodel",
  "readiness": {
    "status": "ready",
    "score": 95,
    "context": {
      "conventions": [...],
      "patterns": [...],
      "recent_changes": [...]
    }
  }
}
```

### With Repo Sync

Ensure readiness before bulk operations:

```bash
# Check readiness before sync
./scripts/repository_sync sync all --check-readiness
```

## Best Practices

### 1. Run Before Every New Task

```bash
# Always start with readiness check
/repo-readiness

# Then proceed with work
/create-spec "new feature"
```

### 2. Keep Configuration Updated

```bash
# Update CLAUDE.md when rules change
# Update mission.md when objectives change
# Update roadmap.md when priorities shift
```

### 3. Address Issues Promptly

```bash
# Don't ignore warnings
# Fix structural issues immediately
# Keep environment synchronized
```

### 4. Use Cache Wisely

```bash
# Cache valid for 1 hour by default
# Force refresh when configuration changes
/repo-readiness --force-refresh
```

### 5. Monitor Across All Repos

```bash
# Weekly bulk check
./scripts/bulk_readiness_check.sh > reports/readiness-$(date +%Y-%m-%d).txt

# Track trends
# Maintain >95% readiness across all repos
```

## Related Skills

- [compliance-check](../compliance-check/SKILL.md) - Standards validation
- [repo-sync](../repo-sync/SKILL.md) - Multi-repo management
- [sparc-workflow](../sparc-workflow/SKILL.md) - Development methodology
- [session-start-routine](../../meta/session-start-routine/SKILL.md) - Session initialization

## References

- [FILE_ORGANIZATION_STANDARDS.md](../../../docs/modules/standards/FILE_ORGANIZATION_STANDARDS.md)
- [AI_AGENT_GUIDELINES.md](../../../docs/modules/ai/AI_AGENT_GUIDELINES.md)
- [DEVELOPMENT_WORKFLOW.md](../../../docs/modules/workflow/DEVELOPMENT_WORKFLOW.md)
- [CLAUDE.md](../../../CLAUDE.md) - Root configuration template

---

## Version History

- **1.0.0** (2026-01-07): Initial release - comprehensive repository readiness skill with configuration analysis, structure assessment, mission extraction, state checking, standards compliance, auto-hook integration, bulk checking capabilities, error handling, and metrics tracking
