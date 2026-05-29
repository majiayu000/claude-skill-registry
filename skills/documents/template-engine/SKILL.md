---
name: template-engine
description: Load, validate, and populate templates consistently across frameworks. Use when relevant to the task.
---

# template-engine

Load, validate, and populate templates consistently across frameworks.

## Triggers

- "create from template [name]"
- "instantiate [template]"
- "new [artifact-type] from template"
- "use template [name]"
- "scaffold [artifact]"

## Purpose

This skill provides a unified template instantiation engine that:
- Locates templates across project, framework, and installation locations
- Parses template structure and placeholders
- Gathers required inputs from context or prompts
- Populates and validates instantiated artifacts
- Integrates with artifact-metadata for tracking

## Behavior

When triggered, this skill:

1. **Locates template**:
   - Search project templates first (`.aiwg/templates/`)
   - Search active framework templates
   - Search AIWG installation templates
   - Return first match or list similar templates

2. **Parses template**:
   - Extract placeholders (`{{variable}}`, `{variable}`)
   - Identify required vs optional sections
   - Detect conditional blocks
   - Build input requirements list

3. **Gathers inputs**:
   - Check context for matching values
   - Prompt for missing required values
   - Apply defaults for optional values

4. **Instantiates template**:
   - Replace all placeholders
   - Evaluate conditional sections
   - Process loops/repeating sections
   - Format output

5. **Validates output**:
   - Check all placeholders replaced
   - Validate structure
   - Create metadata (via artifact-metadata skill)

6. **Saves artifact**:
   - Write to appropriate location
   - Update artifact index

## Template Discovery Order

```
1. .aiwg/templates/{template-name}.md
2. .aiwg/templates/{category}/{template-name}.md
3. {framework}/templates/{category}/{template-name}.md
4. ~/.local/share/ai-writing-guide/.../{template-name}.md
```

## Template Syntax

### Basic Placeholders

```markdown
# {{project_name}} Architecture Document

**Author**: {{author}}
**Date**: {{date}}
**Version**: {{version|default:0.1.0}}
```

### Conditional Sections

```markdown
{{#if has_database}}
## Database Design

{{database_description}}
{{/if}}
```

### Loops/Repeating Sections

```markdown
## Components

{{#each components}}
### {{name}}

{{description}}

- **Owner**: {{owner}}
- **Dependencies**: {{dependencies}}
{{/each}}
```

### Includes

```markdown
{{> common/header.md}}

## Content

{{> partials/component-table.md}}
```

### Computed Values

```markdown
**Generated**: {{now|format:YYYY-MM-DD}}
**ID**: {{artifact_type}}-{{sequence|pad:3}}
```

## Configuration

### Template Metadata

Each template can have a `.meta.yaml` file:

```yaml
name: software-architecture-document
description: Template for Software Architecture Documents
category: architecture
version: 1.0.0

variables:
  - name: project_name
    required: true
    description: Name of the project

  - name: author
    required: true
    description: Document author

  - name: version
    required: false
    default: "0.1.0"
    description: Document version

  - name: components
    required: false
    type: array
    description: List of system components

sections:
  - name: overview
    required: true
  - name: database
    required: false
    condition: has_database

output:
  location: .aiwg/architecture/
  filename: "{{project_name|kebab}}-sad.md"
```

## Usage Examples

### Basic Template Instantiation

```
User: "Create SAD from template"

Skill executes:
1. Find: sdlc-complete/templates/analysis-design/software-architecture-doc-template.md
2. Parse: Extract placeholders (project_name, author, etc.)
3. Gather: Prompt for required values
4. Instantiate: Replace placeholders
5. Save: .aiwg/architecture/myproject-sad.md
6. Metadata: Create .aiwg/architecture/myproject-sad.metadata.json
```

### With Context

```
User: "New test plan from template for authentication module"

Context provides:
- project_name: "MyProject"
- module: "authentication"
- author: from git config

Skill uses context values, prompts for remaining.
```

### List Available Templates

```
User: "What templates are available?"

Skill returns:
Architecture:
  - software-architecture-doc-template
  - adr-template
  - api-contract-template

Requirements:
  - use-case-spec-template
  - user-story-template
  - supplementary-spec-template

Testing:
  - test-plan-template
  - test-case-template
  - test-strategy-template
```

### Template with Components

```
User: "Create component diagram from template with 3 components"

Skill prompts:
- Component 1 name? "API Gateway"
- Component 1 description? "External API interface"
- Component 2 name? "Auth Service"
...

Output includes all components in repeating section.
```

## CLI Usage

```bash
# Instantiate template
python template_engine.py --template software-architecture-doc-template

# With variables
python template_engine.py --template sad \
  --var project_name="MyProject" \
  --var author="John Doe"

# Interactive mode
python template_engine.py --template test-plan --interactive

# List templates
python template_engine.py --list
python template_engine.py --list --category architecture

# Validate template
python template_engine.py --validate --template custom-template.md

# Preview without saving
python template_engine.py --template sad --preview

# Specify output location
python template_engine.py --template sad --output .aiwg/architecture/custom-name.md
```

## Template Categories

### SDLC Framework Templates

| Category | Templates |
|----------|-----------|
| requirements | use-case-spec, user-story, supplementary-spec, srs, glossary |
| architecture | sad, adr, api-contract, data-flow, database-design |
| testing | test-strategy, test-plan, test-cases, defect-card |
| security | threat-model, security-requirements, vulnerability-plan |
| deployment | deployment-plan, release-notes, support-runbook |
| management | iteration-plan, risk-list, project-status |

### MMK Framework Templates

| Category | Templates |
|----------|-----------|
| intake | campaign-intake, audience-profile, brand-brief |
| content | blog-post, case-study, whitepaper, newsletter |
| creative | creative-brief, asset-spec, design-system |
| email | email-campaign, email-sequence, nurture-workflow |
| analytics | kpi-dashboard, measurement-plan, campaign-report |

## Integration

This skill integrates with:
- `artifact-metadata`: Creates metadata for instantiated artifacts
- `artifact-orchestration`: Uses templates for artifact generation
- `project-awareness`: Gets context values from project state

## Error Handling

### Missing Template

```
Template 'nonexistent' not found.
Did you mean:
  - test-plan-template (testing)
  - deployment-plan-template (deployment)

Available templates: python template_engine.py --list
```

### Missing Required Variable

```
Missing required variable: project_name
Description: Name of the project
Please provide: --var project_name="value"
```

### Invalid Template Syntax

```
Template validation failed:
  Line 45: Unclosed conditional block {{#if has_database}}
  Line 67: Unknown variable {{unknwon_var}}
```

## References

- SDLC templates: `sdlc-complete/templates/`
- MMK templates: `media-marketing-kit/templates/`
- Template syntax: Handlebars-compatible subset
- Metadata schema: `schemas/template-meta.schema.json`
