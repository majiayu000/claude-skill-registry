---
name: nixtla-prd-to-code
description: "Transform PRD documents into actionable implementation tasks with TodoWrite integration. Use when planning development work, converting requirements to tasks, or creating implementation roadmaps. Trigger with 'PRD to tasks', 'plan implementation from PRD', or 'create task list'."
allowed-tools: "Read,Write,Glob,TodoWrite"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
---

# Nixtla PRD to Code

Transform Product Requirements Documents into comprehensive implementation task lists with automatic TodoWrite integration for seamless development planning.

## Overview

This skill bridges the gap between requirements and code:

- **Parse PRDs**: Extract functional requirements, non-functional requirements, and technical specifications
- **Identify dependencies**: Detect task dependencies and ordering constraints
- **Generate task lists**: Create detailed, prioritized implementation tasks
- **TodoWrite integration**: Automatically populate Claude's todo list
- **Track progress**: Maintain clear roadmap from idea to working code

## Prerequisites

**Required**:
- Python 3.8+
- PRD documents in standardized format (Overview, Functional Requirements, Technical Spec)
- Access to TodoWrite tool in conversation context

**Optional**:
- `pyyaml`: For YAML task list export (install via `pip install pyyaml`)

## Instructions

### Step 1: Identify PRD Document

Locate the PRD file to transform:
```bash
ls 000-docs/000a-planned-plugins/*/02-PRD.md
```

### Step 2: Parse PRD

Execute the PRD parser to extract requirements:
```bash
python {baseDir}/scripts/parse_prd.py \
    --prd 000-docs/000a-planned-plugins/implemented/nixtla-roi-calculator/02-PRD.md \
    --output tasks.json
```

### Step 3: Review Generated Tasks

The script generates a structured task list with:
- Task titles and descriptions
- Priority levels (P0, P1, P2)
- Dependencies between tasks
- Estimated complexity
- Implementation notes

### Step 4: Populate TodoWrite

Automatically populate Claude's todo list:
```bash
python {baseDir}/scripts/parse_prd.py \
    --prd 000-docs/000a-planned-plugins/implemented/nixtla-roi-calculator/02-PRD.md \
    --populate-todo
```

### Step 5: Begin Implementation

Follow the generated task list, marking items complete as work progresses.

## Output

- **tasks.json**: Structured task list in JSON format
- **tasks.yaml**: Human-readable task list (if pyyaml installed)
- **implementation_plan.md**: Markdown checklist for manual tracking
- **TodoWrite integration**: Automatic task population in conversation

## Error Handling

1. **Error**: `PRD file not found`
   **Solution**: Verify PRD path, check `000-docs/000a-planned-plugins/` directory

2. **Error**: `Missing Functional Requirements section`
   **Solution**: Ensure PRD has `## Functional Requirements` heading with FR-X items

3. **Error**: `TodoWrite tool not available`
   **Solution**: Skill can only populate todos in conversation context, not standalone script execution

4. **Error**: `Invalid PRD format`
   **Solution**: PRD must have standard sections: Overview, Goals, Functional Requirements, Technical Spec

5. **Error**: `Circular dependency detected`
   **Solution**: Review task dependencies, ensure no circular references (Task A → Task B → Task A)

## Examples

### Example 1: Parse ROI Calculator PRD

```bash
python {baseDir}/scripts/parse_prd.py \
    --prd 000-docs/000a-planned-plugins/implemented/nixtla-roi-calculator/02-PRD.md \
    --output roi_tasks.json \
    --verbose
```

**Generated tasks.json**:
```json
{
  "tasks": [
    {
      "id": "roi-001",
      "title": "Implement cost input collection",
      "description": "Build input form for infrastructure costs, forecasting volume, team composition",
      "priority": "P0",
      "dependencies": [],
      "complexity": "medium",
      "functional_requirement": "FR-1"
    },
    {
      "id": "roi-002",
      "title": "Build ROI calculation engine",
      "description": "5-year TCO calculation for build vs. buy scenarios",
      "priority": "P0",
      "dependencies": ["roi-001"],
      "complexity": "high",
      "functional_requirement": "FR-2"
    }
  ]
}
```

### Example 2: Auto-Populate TodoWrite

When used in conversation context:

```python
# In Claude Code conversation
from parse_prd import PRDParser

parser = PRDParser('000-docs/000a-planned-plugins/implemented/nixtla-roi-calculator/02-PRD.md')
tasks = parser.extract_tasks()

# Automatically populates TodoWrite
for task in tasks:
    TodoWrite(content=task['title'], activeForm=f"Working on {task['title']}", status="pending")
```

### Example 3: Generate Markdown Checklist

```bash
python {baseDir}/scripts/parse_prd.py \
    --prd 000-docs/000a-planned-plugins/implemented/nixtla-forecast-explainer/02-PRD.md \
    --output-format markdown \
    --output implementation_plan.md
```

**Generated implementation_plan.md**:
```markdown
# Nixtla Forecast Explainer - Implementation Plan

## Phase 1: Core Infrastructure (P0)
- [ ] Set up project structure and dependencies
- [ ] Create MCP server scaffold
- [ ] Implement SHAP explainability integration

## Phase 2: Feature Development (P0)
- [ ] Build feature importance calculation
- [ ] Implement counterfactual analysis
- [ ] Add time-based contribution decomposition

## Phase 3: Visualization (P1)
- [ ] Generate waterfall charts
- [ ] Create interactive dashboards
- [ ] Export to PDF reports
```

### Example 4: Batch Process Multiple PRDs

```bash
for prd in 000-docs/000a-planned-plugins/*/02-PRD.md; do
    plugin_name=$(basename $(dirname "$prd"))
    python {baseDir}/scripts/parse_prd.py \
        --prd "$prd" \
        --output "009-temp-data/task-plans/${plugin_name}_tasks.json"
done
```

## Resources

- **PRD Standard**: `000-docs/000a-planned-plugins/README.md` (PRD structure specification)
- **TodoWrite Documentation**: Use `AskUserQuestion` to learn about TodoWrite tool capabilities
- **Task Management**: Beads (`bd` CLI) for advanced task tracking

**Related Skills**:
- `nixtla-plugin-scaffolder`: Generate plugin structure from PRD
- `nixtla-demo-generator`: Create Jupyter demos for implementation
- `nixtla-test-generator`: Build test suites from PRD requirements

**Scripts**:
- `{baseDir}/scripts/parse_prd.py`: Main PRD parsing and task generation script
- `{baseDir}/assets/templates/task_template.json`: Task structure template
