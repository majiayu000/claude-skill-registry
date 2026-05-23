---
name: workflow
description: Load development methodology workflows. Supports agile, devops, vmodel, and kanban methodologies.
argument-hint: "<methodology> - Choose: agile, devops, vmodel, kanban"
---

# Development Workflow Loader

When invoked with `/workflow <methodology>`, load the corresponding workflow configuration.

## Supported Methodologies

### @agile (or /workflow agile)
**File**: `C:\.claude\workflows\agile-scrum.yaml`
**Quick Reference**: `C:\.claude\workflows\agile-scrum-quickref.yaml`

Use for: Product development teams, iterative delivery, customer-focused projects

**Includes**:
- Sprint planning templates
- User story format (As a... I want... So that...)
- Retrospective formats
- Daily standup structure
- Definition of Done/Ready

**Sub-shortcuts**:
- `@sprint` - Sprint context
- `@story` - User story template
- `@retro` - Retrospective format
- `@standup` - Daily standup format

### @devops (or /workflow devops)
**File**: `C:\.claude\workflows\devops-cicd.yaml`

Use for: Continuous delivery, automated deployments, infrastructure management

**Includes**:
- CI/CD pipeline templates
- Infrastructure as Code patterns
- Monitoring and observability setup
- GitOps workflows

**Sub-shortcuts**:
- `@pipeline` - CI/CD pipeline
- `@deploy` - Deployment patterns
- `@monitor` - Observability setup
- `@iac` - Infrastructure as Code

### @vmodel (or /workflow vmodel)
**File**: `C:\.claude\workflows\waterfall-vmodel.yaml`

Use for: Regulated industries, fixed-scope projects, compliance-heavy contexts

**Includes**:
- Phase gate definitions
- Traceability matrix templates
- SRS document template (`C:\.claude\workflows\templates\SRS-template.md`)
- Validation/Verification mapping

**Sub-shortcuts**:
- `@phase` - Phase management
- `@gate` - Quality gates
- `@trace` - Traceability matrix
- `@srs` - SRS document

### @kanban (or /workflow kanban)
**File**: `C:\.claude\workflows\kanban-flow.yaml`

Use for: Continuous flow delivery, support/maintenance teams, operations work

**Includes**:
- WIP limit recommendations
- Flow metrics (lead time, cycle time)
- Board configuration
- Service Level Expectations

**Sub-shortcuts**:
- `@wip` - WIP limits
- `@flow` - Flow metrics
- `@board` - Board management
- `@sle` - Service Level Expectations

## Usage
1. Load methodology: `/workflow agile`
2. Apply to project context
3. Combine with other configs: `@agile @dotnet @deploy:k8s`
