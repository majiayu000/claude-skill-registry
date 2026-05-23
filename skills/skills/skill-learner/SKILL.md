---
name: skill-learner
description: Post-commit skill that reviews completed work, identifies reusable patterns, and creates/enhances skills for continual learning. Auto-executes after commits to build organizational knowledge.
version: 1.0.0
category: workspace-hub
type: skill
trigger: post-commit
auto_execute: true
capabilities:
  - commit_analysis
  - pattern_extraction
  - skill_identification
  - skill_enhancement
  - knowledge_synthesis
  - continual_learning
tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
related_skills:
  - skill-creator
  - session-start-routine
  - repo-readiness
---

# Skill Learner

> Automatically analyze completed work, extract reusable patterns, and create/enhance skills for continual organizational learning.

## Quick Start

```bash
# Manual trigger after commit
/skill-learner

# Auto-triggers after:
# - git commit (via post-commit hook)
# - Task completion
# - Feature implementation

# Review learning
cat .claude/skill-learning-log.md
```

## When to Use

**AUTO-EXECUTES (via hook):**
- After every git commit
- After task completion
- After feature implementation
- After bug fixes with significant patterns
- After refactoring work

**MANUAL TRIGGER:**
- To analyze recent work history
- To review learning opportunities
- To create skills from existing patterns
- After completing a project phase
- During knowledge capture sessions

## Prerequisites

- Git repository with commit history
- Access to committed files and diffs
- (Optional) Skills directory for new skill creation
- (Optional) Internet for pattern research

## Overview

The skill-learner performs post-commit analysis to identify reusable patterns, common workflows, and valuable techniques from completed work. It automatically creates new skills or enhances existing ones, ensuring continuous organizational learning.

### What It Analyzes

1. **Commit Content**: Files changed, code added, patterns used
2. **Commit Message**: Task description, context, intent
3. **Work Patterns**: Repeated workflows, common operations
4. **Problem Solutions**: How bugs were fixed, how features were built
5. **Tool Usage**: Libraries, frameworks, techniques employed
6. **Documentation**: Comments, docs added, conventions followed

### Output

Generates:
- Pattern analysis report
- Skill creation recommendations
- Enhanced existing skills
- Learning log with insights
- Knowledge base entries

## Core Operations

### 1. Commit Analysis

**Analyzes Last Commit:**
```bash
# Extract commit metadata
COMMIT_HASH=$(git rev-parse HEAD)
COMMIT_MSG=$(git log -1 --pretty=%B)
COMMIT_AUTHOR=$(git log -1 --pretty=%an)
COMMIT_DATE=$(git log -1 --pretty=%ai)

# Get changed files
git diff-tree --no-commit-id --name-only -r HEAD

# Get diff content
git diff HEAD^ HEAD
```

**Example Analysis:**
```markdown
## Commit Analysis

**Commit**: a1b2c3d4
**Message**: Add interactive NPV calculator with Plotly visualization
**Author**: Developer
**Date**: 2026-01-07 14:30:00

### Files Changed (12)
- src/modules/npv/calculator.py (new)
- src/modules/npv/visualizer.py (new)
- src/modules/npv/__init__.py (new)
- tests/unit/test_npv_calculator.py (new)
- config/input/npv_analysis.yaml (new)
- scripts/run_npv_analysis.sh (new)
- docs/npv_calculator.md (new)
- ... 5 more files

### Code Additions
- Lines added: 847
- Lines removed: 23
- Net change: +824

### Technologies Used
- Plotly for interactive visualization
- Pandas for data handling
- NumPy for NPV calculations
- pytest for testing
```

### 2. Pattern Extraction

**Identifies Reusable Patterns:**

**Pattern Types:**
```markdown
1. **Workflow Patterns**
   - YAML config → Script execution → HTML report
   - Data load → Process → Validate → Visualize → Save

2. **Code Patterns**
   - Interactive plotting with Plotly
   - CSV data loading with relative paths
   - Modular calculator structure
   - TDD test-first approach

3. **Tool Patterns**
   - UV environment management
   - Bash script execution
   - YAML configuration files
   - Plotly visualization

4. **Problem-Solving Patterns**
   - NPV calculation with multiple discount rates
   - Handling missing data gracefully
   - Interactive parameter adjustment
   - Real-time visualization updates
```

**Example Extraction:**
```markdown
## Pattern: Interactive Financial Calculator

### Problem Solved
Need to calculate NPV with multiple scenarios and visualize results interactively.

### Solution Pattern
1. YAML configuration with parameters
2. Python calculator module
3. Plotly visualization
4. Bash execution wrapper
5. HTML report generation

### Reusability Score: 95/100
- Applicable to: IRR, ROI, payback period, sensitivity analysis
- Generic enough: Yes
- Well-documented: Yes
- Tested: Yes (85% coverage)
```

### 3. Skill Identification

**Determines Skill Creation Need:**

**Decision Matrix:**
```
CREATE NEW SKILL if:
✓ Pattern used 3+ times across commits
✓ Workflow is complex (5+ steps)
✓ Domain-specific knowledge required
✓ Significant time savings (>30 min per use)
✓ No existing skill covers it

ENHANCE EXISTING SKILL if:
✓ Pattern similar to existing skill
✓ New technique for known problem
✓ Updated best practices
✓ New tool/library version
✓ Improved approach discovered

SKIP if:
✗ One-time solution
✗ Trivial pattern (<3 steps)
✗ Already well-covered
✗ Repository-specific only
```

**Example Decision:**
```markdown
## Skill Decision: NPV Calculator

### Analysis
- **Frequency**: Used 5 times in last month
- **Complexity**: 8-step workflow
- **Domain Knowledge**: Financial engineering
- **Time Savings**: ~2 hours per use
- **Existing Skills**: None for financial calculators

### Recommendation: CREATE NEW SKILL
**Skill Name**: financial-calculator-builder
**Category**: development/finance
**Priority**: High

**Rationale**:
- High reusability across energy economic analysis
- Complex enough to warrant skill documentation
- Significant time savings
- Establishes pattern for future financial tools
```

### 4. Skill Creation

**Automatically Creates Skills:**

**Creation Process:**
```bash
1. Generate skill name from pattern
2. Extract workflow steps
3. Create SKILL.md with template
4. Document code examples
5. Add usage instructions
6. Link related skills
7. Update skills README
8. Commit new skill
```

**Example Skill Created:**
```markdown
---
name: financial-calculator-builder
description: Build interactive financial calculators (NPV, IRR, ROI) with Plotly visualization, YAML configuration, and HTML reporting.
version: 1.0.0
category: development/finance
created_from: commit a1b2c3d4
pattern_source: npv_calculator implementation
---

# Financial Calculator Builder

> Create interactive financial analysis tools with visualization and reporting.

## Quick Start

```bash
# Create NPV calculator
/financial-calculator-builder npv

# Create IRR calculator
/financial-calculator-builder irr

# Custom calculator
/financial-calculator-builder custom --config config/calc.yaml
```

## Pattern

1. Define calculation in YAML config
2. Implement calculator class
3. Add Plotly visualization
4. Create bash execution wrapper
5. Generate HTML report
6. Write tests (TDD)

[... full skill documentation ...]
```

### 5. Skill Enhancement

**Updates Existing Skills:**

**Enhancement Types:**
```markdown
1. **Version Updates**
   - New tool versions (Plotly 5.17 → 5.18)
   - Updated APIs
   - Deprecated method replacements

2. **Best Practice Improvements**
   - Better error handling
   - Performance optimizations
   - Security enhancements

3. **New Examples**
   - Additional use cases
   - Real-world implementations
   - Edge case handling

4. **Integration Points**
   - New tool integrations
   - Cross-skill workflows
   - Automation hooks
```

**Example Enhancement:**
```markdown
## Enhancement: plotly-visualization skill

### Commit: a1b2c3d4
### Pattern Found: Multi-scenario NPV visualization

### Enhancement Applied:
Added section "Financial Visualizations" to plotly-visualization skill:

**New Example: Multi-Scenario Analysis**
```python
import plotly.graph_objects as go

# Create multi-scenario NPV plot
fig = go.Figure()

for scenario in scenarios:
    fig.add_trace(go.Scatter(
        x=scenario['years'],
        y=scenario['npv'],
        name=scenario['name'],
        mode='lines+markers'
    ))

fig.update_layout(
    title='NPV Analysis: Multiple Scenarios',
    xaxis_title='Year',
    yaxis_title='Net Present Value ($M)'
)
```

**Version**: 1.2.0 → 1.3.0
**Reason**: Added financial visualization patterns
```

### 6. Knowledge Synthesis

**Builds Organizational Knowledge:**

**Knowledge Base Structure:**
```
.claude/knowledge/
├── patterns/
│   ├── financial-calculations.md
│   ├── interactive-visualization.md
│   └── data-pipelines.md
├── techniques/
│   ├── npv-calculation.md
│   ├── scenario-analysis.md
│   └── sensitivity-testing.md
└── lessons/
    ├── 2026-01-07-npv-calculator.md
    └── ...
```

**Example Knowledge Entry:**
```markdown
# Pattern: Interactive Financial Calculator

**Discovered**: 2026-01-07 (commit a1b2c3d4)
**Category**: Financial Engineering
**Reusability**: High

## Problem
Need to perform financial calculations (NPV, IRR, ROI) with:
- Multiple scenarios
- Interactive parameter adjustment
- Visual comparison
- Exportable reports

## Solution Pattern

### 1. Configuration (YAML)
```yaml
calculation:
  type: npv
  discount_rates: [0.05, 0.08, 0.10, 0.12]
  cash_flows: data/cash_flows.csv
  scenarios:
    - base
    - optimistic
    - pessimistic
```

### 2. Calculator Module (Python)
```python
class NPVCalculator:
    def calculate(self, cash_flows, discount_rate):
        return np.npv(discount_rate, cash_flows)

    def multi_scenario(self, scenarios, rates):
        results = {}
        for scenario in scenarios:
            for rate in rates:
                npv = self.calculate(scenario.cash_flows, rate)
                results[(scenario.name, rate)] = npv
        return results
```

### 3. Visualization (Plotly)
Interactive multi-scenario comparison with hover tooltips.

### 4. Execution (Bash)
```bash
./scripts/run_npv_analysis.sh config/npv.yaml
```

## Lessons Learned
1. YAML configuration makes calculators flexible
2. Plotly enables interactive scenario exploration
3. Modular design allows easy extension to other metrics
4. TDD catches calculation errors early

## Applications
- ✅ NPV Calculator (implemented)
- 🔲 IRR Calculator (recommended)
- 🔲 ROI Calculator (recommended)
- 🔲 Payback Period Calculator (recommended)
- 🔲 Sensitivity Analysis Tool (high value)

## Related Skills
- financial-calculator-builder (created)
- plotly-visualization (enhanced)
- yaml-workflow-executor (existing)
```

## Learning Log

**Maintains Continuous Learning Record:**

**Log Format:**
```markdown
# Skill Learning Log

## 2026-01-07

### Commit: a1b2c3d4 - NPV Calculator Implementation

**Patterns Extracted**: 3
- Interactive financial calculator
- Multi-scenario analysis
- YAML-driven calculations

**Skills Created**: 1
- financial-calculator-builder (v1.0.0)

**Skills Enhanced**: 2
- plotly-visualization (v1.2.0 → v1.3.0)
  - Added financial visualization examples
- yaml-workflow-executor (v2.1.0 → v2.1.1)
  - Added financial config examples

**Knowledge Added**: 1
- patterns/interactive-financial-calculator.md

**Reusability Score**: 95/100
**Time Savings**: ~2 hours per future use
**Learning Value**: High - establishes financial tool pattern

---

## 2026-01-06

### Commit: e5f6g7h8 - Marine Safety Data Processor

**Patterns Extracted**: 2
- CSV data validation
- Safety incident categorization

**Skills Enhanced**: 1
- data-pipeline-processor (v3.0.0 → v3.1.0)
  - Added safety data validation patterns

**Knowledge Added**: 1
- techniques/safety-data-validation.md

**Reusability Score**: 75/100
**Time Savings**: ~1 hour per future use
**Learning Value**: Medium - domain-specific but valuable

---
```

## Execution Checklist

**Pre-Analysis:**
- [ ] Git repository is valid
- [ ] At least one commit exists
- [ ] Access to skills directory
- [ ] Access to knowledge base

**Analysis Phase:**
- [ ] Extract commit metadata
- [ ] Analyze changed files
- [ ] Review code diff
- [ ] Identify patterns used
- [ ] Assess reusability

**Decision Phase:**
- [ ] Check for existing similar skills
- [ ] Calculate reusability score
- [ ] Determine create vs enhance vs skip
- [ ] Prioritize recommendations

**Action Phase:**
- [ ] Create new skills (if warranted)
- [ ] Enhance existing skills
- [ ] Update knowledge base
- [ ] Append to learning log
- [ ] Commit skill changes

**Post-Analysis:**
- [ ] Report generation
- [ ] Metrics tracking
- [ ] User notification (optional)

## Hook Integration

### Post-Commit Hook

**Hook Configuration:**
```bash
# .claude/hooks/post-commit.sh
#!/bin/bash
# Auto-execute skill learning after commits

REPO_PATH="$(pwd)"
SKILL_PATH="${HOME}/.claude/skills/workspace-hub/skill-learner"

# Allow bypassing skill learning
if [ "${SKIP_SKILL_LEARNING:-0}" = "1" ]; then
    echo "Skill learning skipped (SKIP_SKILL_LEARNING=1)"
    exit 0
fi

# Only run on significant commits
LINES_CHANGED=$(git diff HEAD^ HEAD --shortstat | grep -oE '[0-9]+ insertion' | grep -oE '[0-9]+' || echo 0)

if [ "$LINES_CHANGED" -lt 50 ]; then
    echo "Small commit (<50 lines), skipping skill learning"
    exit 0
fi

# Run skill learning
echo "Analyzing commit for learning opportunities..."
"$SKILL_PATH/analyze_commit.sh" "$REPO_PATH"

exit 0
```

**Trigger Conditions:**
- After git commit (>50 lines changed)
- After task completion
- After feature merges
- Manual trigger via `/skill-learner`

**Bypass Hook:**
```bash
# Skip learning for trivial commits
SKIP_SKILL_LEARNING=1 git commit -m "Fix typo"

# Or disable temporarily
mv .claude/hooks/post-commit.sh .claude/hooks/post-commit.sh.disabled
```

## Automation Scripts

### 1. Commit Analyzer

**Location:** `analyze_commit.sh`

```bash
#!/bin/bash
# Analyze recent commit for learning opportunities

REPO_PATH="${1:-.}"
COMMIT_HASH="${2:-HEAD}"

# Extract commit info
analyze_commit() {
    echo "Analyzing commit: $COMMIT_HASH"

    # Get commit metadata
    local msg=$(git log -1 --pretty=%B $COMMIT_HASH)
    local author=$(git log -1 --pretty=%an $COMMIT_HASH)
    local date=$(git log -1 --pretty=%ai $COMMIT_HASH)

    # Get changed files
    local files=$(git diff-tree --no-commit-id --name-only -r $COMMIT_HASH)

    # Analyze patterns
    extract_patterns "$files"

    # Make skill decisions
    decide_skill_actions

    # Generate report
    generate_learning_report
}

# Extract reusable patterns
extract_patterns() {
    local files="$1"

    # Check for workflow patterns
    if echo "$files" | grep -q "config/input/.*\.yaml"; then
        echo "Pattern: YAML-driven workflow"
    fi

    if echo "$files" | grep -q "scripts/.*\.sh"; then
        echo "Pattern: Bash execution script"
    fi

    # Check for code patterns
    if git diff $COMMIT_HASH^ $COMMIT_HASH | grep -q "import plotly"; then
        echo "Pattern: Plotly visualization"
    fi

    # More pattern detection...
}

# Decide whether to create/enhance skills
decide_skill_actions() {
    # Reusability scoring
    local score=0

    # Check commit history for similar patterns
    local pattern_count=$(git log --all --grep="similar pattern" | wc -l)
    if [ $pattern_count -ge 3 ]; then
        ((score += 30))
    fi

    # Check code complexity
    local lines_added=$(git diff $COMMIT_HASH^ $COMMIT_HASH --shortstat | grep -oE '[0-9]+ insertion' | grep -oE '[0-9]+')
    if [ $lines_added -gt 100 ]; then
        ((score += 20))
    fi

    # Decision
    if [ $score -ge 70 ]; then
        echo "Recommendation: CREATE NEW SKILL"
    elif [ $score -ge 40 ]; then
        echo "Recommendation: ENHANCE EXISTING SKILL"
    else
        echo "Recommendation: SKIP (low reusability)"
    fi
}

# Generate learning report
generate_learning_report() {
    local report_file=".claude/learning-reports/$(date +%Y-%m-%d)-$COMMIT_HASH.md"
    mkdir -p "$(dirname "$report_file")"

    {
        echo "# Learning Report"
        echo "**Commit**: $COMMIT_HASH"
        echo "**Date**: $(date)"
        echo ""
        echo "## Patterns Extracted"
        # ... pattern details ...
        echo ""
        echo "## Recommendations"
        # ... recommendations ...
    } > "$report_file"

    echo "Learning report saved: $report_file"
}

main "$@"
```

### 2. Skill Creator (from Pattern)

**Location:** `create_skill_from_pattern.sh`

```bash
#!/bin/bash
# Create new skill from extracted pattern

PATTERN_NAME="$1"
CATEGORY="${2:-development}"
SOURCE_COMMIT="$3"

# Generate skill from template
generate_skill() {
    local skill_dir="${HOME}/.claude/skills/${CATEGORY}/${PATTERN_NAME}"
    mkdir -p "$skill_dir"

    # Create SKILL.md
    cat > "${skill_dir}/SKILL.md" << EOF
---
name: ${PATTERN_NAME}
description: Auto-generated skill from commit pattern
version: 1.0.0
category: ${CATEGORY}
created_from: ${SOURCE_COMMIT}
---

# ${PATTERN_NAME^} Skill

> Auto-generated from repeated commit pattern

## Pattern Source

**Commit**: ${SOURCE_COMMIT}
**Extracted**: $(date)

[... skill template ...]
EOF

    echo "Skill created: $skill_dir"
}

generate_skill
```

### 3. Bulk Learning Analysis

**Analyzes Recent Commit History:**

```bash
#!/bin/bash
# Analyze last N commits for learning opportunities

REPO_PATH="${1:-.}"
COMMIT_COUNT="${2:-10}"

echo "Analyzing last $COMMIT_COUNT commits..."

for commit in $(git log -n $COMMIT_COUNT --pretty=%H); do
    echo "Commit: $commit"
    ./analyze_commit.sh "$REPO_PATH" "$commit"
    echo ""
done

# Generate aggregate report
echo "Generating aggregate learning report..."
./generate_aggregate_report.sh
```

## Error Handling

### No Patterns Found

```
ℹ️ Info: No reusable patterns detected in commit

Reason: Commit too small or repository-specific changes

Action: No skills created, logged for future pattern detection
```

### Skill Already Exists

```
⚠️ Warning: Skill 'financial-calculator-builder' already exists

Action Options:
1. Enhance existing skill (recommended)
2. Create variant skill (e.g., 'financial-calculator-builder-v2')
3. Skip creation

Recommendation: ENHANCE
```

### Invalid Pattern

```
❌ Error: Pattern extraction failed

Reason: Unable to identify coherent workflow or technique

Action: Manual review required - see .claude/learning-reports/error-*.md
```

### Skills Directory Not Found

```
⚠️ Warning: Skills directory not accessible

Location Expected: ~/.claude/skills/ or .claude/skills/

Action: Create skills directory or configure SKILLS_PATH
```

## Metrics & Success Criteria

### Learning Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Patterns Extracted/Week | 5-10 | Count from learning log |
| Skills Created/Month | 2-5 | New skills in directory |
| Skills Enhanced/Month | 5-10 | Version bumps recorded |
| Reusability Score Avg | > 70 | Average across patterns |
| Time Savings | > 10 hrs/month | Estimated from usage |

### Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Pattern Accuracy | > 90% | Correct pattern identification |
| Skill Usefulness | > 80% | Skills used after creation |
| Enhancement Value | > 70% | Enhanced skills improve workflow |
| False Positives | < 10% | Incorrect skill creation rate |

### Adoption Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Hook Installation | 100% repos | Track per repo |
| Learning Log Size | Growing | Lines in log |
| Knowledge Base Growth | +10 entries/month | Count entries |
| Skill Library Size | +3-5 skills/month | Total skills |

## Integration Points

### With Session Start Routine

```bash
# Review recent learning at session start
/session-start-routine

# Includes:
# - Recent patterns extracted
# - Skills created/enhanced
# - Learning opportunities
```

### With Skill Creator

```bash
# Manual skill creation uses patterns
/skill-creator new-feature

# Skill learner provides:
# - Similar existing patterns
# - Related skills
# - Best practices from learning log
```

### With Repo Sync

```bash
# Learning across all repos
./bulk_learning_analysis.sh

# Aggregate patterns from entire workspace
```

## Best Practices

### 1. Review Learning Log Regularly

```bash
# Weekly review
cat .claude/skill-learning-log.md | head -100

# Identify high-value patterns
grep "Reusability Score: 9" .claude/skill-learning-log.md
```

### 2. Refine Patterns

```bash
# If pattern is too specific, generalize
# If pattern is too generic, specialize
# Document edge cases
```

### 3. Link Related Knowledge

```bash
# Cross-reference skills
# Update related documentation
# Share patterns across teams
```

### 4. Validate Skill Usefulness

```bash
# Track skill usage
# Deprecate unused skills
# Enhance frequently-used skills
```

## Related Skills

- [skill-creator](../../builders/skill-creator/SKILL.md) - Manual skill creation
- [session-start-routine](../../meta/session-start-routine/SKILL.md) - Session initialization
- [repo-readiness](../repo-readiness/SKILL.md) - Repository preparation
- [compliance-check](../compliance-check/SKILL.md) - Standards validation

## References

- [Skill Template](../../../../templates/SKILL_TEMPLATE_v2.md)
- [Pattern Library](../../../../.claude/knowledge/patterns/)
- [Learning Framework](../../../../docs/modules/ai/LEARNING_FRAMEWORK.md)

---

## Version History

- **1.0.0** (2026-01-07): Initial release - post-commit skill learning with pattern extraction, skill creation/enhancement, knowledge synthesis, auto-hook integration, learning log, metrics tracking, and continual learning capabilities
