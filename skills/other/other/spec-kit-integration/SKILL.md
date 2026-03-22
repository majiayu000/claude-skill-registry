---
name: spec-kit-integration
description: |
  Integracao com GitHub Spec Kit para Spec-Driven Development.
  Gera specs, technical plans e tasks usando templates padronizados.
  Use quando: criar specs, gerar technical plans, quebrar em tasks.
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
user-invocable: true
---

# Spec Kit Integration Skill

## Proposito

Esta skill integra o GitHub Spec Kit para habilitar Spec-Driven Development:

1. **Spec Creation** - Criar especificacoes usando template
2. **Technical Plan** - Gerar plano tecnico da spec
3. **Task Breakdown** - Quebrar plano em tasks executaveis
4. **Spec Analysis** - Validar qualidade da spec

## Pre-requisitos

```bash
# Instalar Specify CLI
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# Ou via pip
pip install git+https://github.com/github/spec-kit.git
```

## Comandos Disponiveis

### /spec-create

Cria uma nova spec usando o template:

```bash
specify init .
# ou
specify create feature-name
```

### /spec-plan

Gera technical plan de uma spec existente:

```bash
specify plan feature-name.spec.md
```

### /spec-tasks

Quebra o plan em tasks:

```bash
specify tasks feature-name.plan.md
```

### /spec-analyze

Valida qualidade da spec:

```bash
specify analyze feature-name.spec.md
```

## Templates

### Spec Template

```markdown
# Spec: {Feature Name}

## Overview
{Brief description of what this feature does}

## Problem Statement
{What problem does this solve?}

## Proposed Solution
{High-level description of the solution}

## Requirements

### Functional Requirements
- FR-001: {requirement}
- FR-002: {requirement}

### Non-Functional Requirements
- NFR-001: {requirement}

## Acceptance Criteria
- [ ] AC-001: {criterion}
- [ ] AC-002: {criterion}

## Out of Scope
- {item not included}

## Dependencies
- {dependency}

## Risks
- {risk}

## Open Questions
- {question}
```

### Technical Plan Template

```markdown
# Technical Plan: {Feature Name}

## Architecture Overview
{High-level architecture description}

## Components
### Component 1
- Responsibility: {description}
- Technology: {tech stack}
- Interfaces: {APIs, events}

## Data Model
{Entity relationships, schemas}

## API Design
{Endpoints, contracts}

## Security Considerations
{Authentication, authorization, data protection}

## Testing Strategy
{Unit, integration, e2e approach}

## Deployment Plan
{Rollout strategy, feature flags}

## Risks and Mitigations
| Risk | Mitigation |
|------|------------|
| {risk} | {mitigation} |
```

### Task Template

```markdown
# Task: {Task ID}

## Parent
- Spec: {spec-name}
- Plan: {plan-section}

## Description
{What needs to be done}

## Acceptance Criteria
- [ ] {criterion}

## Implementation Notes
{Technical details, considerations}

## Dependencies
- {blocking tasks}

## Estimate
{T-shirt size or story points}
```

## Fluxo de Uso

```
1. Criar Spec (/spec-create)
   - Preencher requisitos
   - Definir acceptance criteria
   - Validar com stakeholders

2. Gerar Technical Plan (/spec-plan)
   - Definir arquitetura
   - Detalhar componentes
   - Planejar testes

3. Quebrar em Tasks (/spec-tasks)
   - Tasks atomicas
   - Dependencias mapeadas
   - Estimativas

4. Implementar Tasks
   - @code-author implementa cada task
   - @code-reviewer valida
   - Marcar tasks completas

5. Validar Spec
   - Todos os ACs atendidos
   - Spec pode ser fechada
```

## Integracao com SDLC

| Fase SDLC | Artefato Spec Kit |
|-----------|-------------------|
| Fase 2 (Requisitos) | Spec |
| Fase 3 (Arquitetura) | Technical Plan |
| Fase 4 (Planejamento) | Tasks |
| Fase 5 (Implementacao) | Task execution |

## Validacao de Qualidade

```yaml
spec_quality_checks:
  completeness:
    - has_overview: required
    - has_problem_statement: required
    - has_proposed_solution: required
    - has_requirements: required
    - has_acceptance_criteria: required

  clarity:
    - no_ambiguous_terms: warning
    - measurable_criteria: required
    - testable_requirements: required

  structure:
    - follows_template: required
    - consistent_formatting: warning
    - linked_to_issues: optional
```

## Hooks de Validacao

```json
{
  "PreToolUse": [{
    "matcher": "Write(*.spec.md)",
    "hooks": [{
      "type": "command",
      "command": "specify analyze $TOOL_INPUT_FILE_PATH || true"
    }]
  }]
}
```

## Pontos de Pesquisa

Para melhorar:
- "spec-driven development best practices"
- "requirements documentation automation"
- "GitHub Spec Kit advanced usage"

## Referencias

- [GitHub Spec Kit](https://github.com/github/spec-kit)
- [Spec-Driven Development Blog](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
