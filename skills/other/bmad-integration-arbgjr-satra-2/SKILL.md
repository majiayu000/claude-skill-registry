---
name: bmad-integration
description: |
  Integracao com BMAD Method para escala adaptativa e workflows guiados.
  Detecta nivel de complexidade e ajusta agentes automaticamente.
  Use quando: iniciar workflow, detectar complexidade, mapear agentes BMAD.
allowed-tools:
  - Read
  - Bash
  - Glob
user-invocable: false
---

# BMAD Integration Skill

## Proposito

Esta skill integra conceitos do BMAD Method para:

1. **Escala Adaptativa** - Detectar nivel de complexidade (0-3)
2. **Workflow Mapping** - Mapear workflows BMAD para agentes locais
3. **Role Alignment** - Alinhar roles BMAD com agentes do SDLC

## BMAD Overview

BMAD Method oferece:
- 21 agentes especializados
- 50+ workflows guiados
- 3 modulos: BMM (core), BMB (builder), CIS (criativo)
- Escala adaptativa Level 0-4

## Escala Adaptativa

### Level 0 - Quick Flow
```yaml
trigger:
  - bug fix
  - typo
  - hotfix
  - small change
  - patch

agents: [code-author, code-reviewer]
skip_phases: [0, 1, 2, 3, 4]
estimated_time: "~5 min"
human_approval: false
```

### Level 1 - Feature
```yaml
trigger:
  - new feature in existing service
  - enhancement
  - improvement
  - minor change

agents:
  - requirements-analyst
  - code-author
  - test-author
  - code-reviewer
skip_phases: [0, 1, 3]
estimated_time: "~15-30 min"
human_approval: false
```

### Level 2 - Product/Service
```yaml
trigger:
  - new product
  - new service
  - new integration
  - major feature
  - new domain

agents: "ALL"
skip_phases: []
estimated_time: "~1-4 hours"
human_approval: true
approval_gates: [phase-2-to-3, phase-6-to-7]
```

### Level 3 - Enterprise
```yaml
trigger:
  - compliance requirement
  - multi-team effort
  - critical system
  - security sensitive
  - high risk

agents: "ALL"
skip_phases: []
estimated_time: "variable"
human_approval: true
approval_gates: "ALL"
extra_requirements:
  - compliance_review
  - security_review
  - architecture_review
  - legal_review
```

## Role Mapping

| BMAD Role | Nosso Agente | Fase |
|-----------|--------------|------|
| Discovery Agent | domain-researcher | 1 |
| Product Manager | product-owner | 2 |
| Requirements Agent | requirements-analyst | 2 |
| UX Designer | ux-writer | 2 |
| Architect | system-architect | 3 |
| Data Architect | data-architect | 3 |
| Security Expert | threat-modeler | 3 |
| Scrum Master | delivery-planner | 4 |
| Developer | code-author | 5 |
| Code Reviewer | code-reviewer | 5 |
| Test Engineer | test-author | 5 |
| QA Expert | qa-analyst | 6 |
| DevOps | cicd-engineer | 7 |
| SRE | observability-engineer | 8 |

## Deteccao de Complexidade

### Algoritmo

```python
def detect_complexity(request: str, context: dict) -> int:
    """Detecta nivel de complexidade baseado na request."""

    # Keywords por nivel
    level_0_keywords = [
        "fix", "typo", "bug", "hotfix", "patch",
        "corrigir", "ajustar", "pequeno"
    ]

    level_1_keywords = [
        "feature", "enhancement", "add", "improve",
        "funcionalidade", "melhoria", "adicionar"
    ]

    level_2_keywords = [
        "new service", "new product", "integration",
        "novo servico", "novo produto", "integracao"
    ]

    level_3_keywords = [
        "compliance", "security", "critical", "multi-team",
        "enterprise", "audit", "gdpr", "lgpd", "pci"
    ]

    request_lower = request.lower()

    # Verificar level 3 primeiro (mais restritivo)
    if any(kw in request_lower for kw in level_3_keywords):
        return 3

    if any(kw in request_lower for kw in level_2_keywords):
        return 2

    if any(kw in request_lower for kw in level_1_keywords):
        return 1

    # Verificar contexto
    if context.get("affected_services", 0) >= 3:
        return 3

    if context.get("new_service", False):
        return 2

    if context.get("existing_service", True):
        return 1

    # Default: feature
    return 1
```

## Workflow Templates

### Quick Flow (Level 0)

```yaml
workflow: quick_flow
steps:
  - agent: code-author
    action: implement_fix
    validation: compile_check

  - agent: code-reviewer
    action: quick_review
    validation: no_blockers

  - action: commit_and_push
    validation: ci_pass
```

### Feature Flow (Level 1)

```yaml
workflow: feature_flow
steps:
  - phase: 2
    agent: requirements-analyst
    action: clarify_requirements
    output: user_story

  - phase: 5
    agents: [code-author, test-author]
    action: implement_with_tests
    output: [code, tests]

  - phase: 5
    agent: code-reviewer
    action: review
    validation: approved

  - phase: 6
    agent: qa-analyst
    action: validate
    validation: quality_ok
```

### Full SDLC (Level 2)

```yaml
workflow: full_sdlc
steps:
  - phase: 0
    agents: [intake-analyst, compliance-guardian]
    gate: phase-0-to-1

  - phase: 1
    agents: [domain-researcher, rag-curator]
    gate: phase-1-to-2

  - phase: 2
    agents: [product-owner, requirements-analyst]
    output: spec
    gate: phase-2-to-3

  - phase: 3
    agents: [system-architect, adr-author, threat-modeler]
    output: [architecture, adrs, threat_model]
    gate: phase-3-to-4

  # ... continua para todas as fases
```

## Integracao

### Com orchestrator

O orchestrator usa bmad-integration para:
1. Detectar nivel na entrada
2. Selecionar workflow apropriado
3. Configurar gates necessarios
4. Definir aprovacoes humanas

### Com gate-evaluator

Complexidade afeta rigor dos gates:
- Level 0-1: Gates simplificados
- Level 2: Gates padrao
- Level 3: Gates estendidos + extra reviews

## Scripts

### detect_level.py

```python
#!/usr/bin/env python3
"""Detecta nivel de complexidade de uma request."""
import sys
import json

def detect_level(request: str) -> dict:
    # Implementacao do algoritmo
    level = 1  # default

    keywords = {
        0: ["fix", "bug", "typo", "hotfix"],
        1: ["feature", "add", "improve"],
        2: ["new service", "integration", "new product"],
        3: ["compliance", "security", "critical", "multi-team"]
    }

    request_lower = request.lower()

    for lvl in [3, 2, 1, 0]:
        if any(kw in request_lower for kw in keywords[lvl]):
            level = lvl
            break

    return {
        "level": level,
        "workflow": ["quick_flow", "feature_flow", "full_sdlc", "enterprise_flow"][level],
        "human_approval": level >= 2,
        "estimated_time": ["~5min", "~15min", "~1-4h", "variable"][level]
    }

if __name__ == "__main__":
    request = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    result = detect_level(request)
    print(json.dumps(result, indent=2))
```

## Pontos de Pesquisa

Para melhorar:
- [BMAD Method GitHub](https://github.com/bmad-code-org/BMAD-METHOD)
- "adaptive software development workflows"
- "complexity detection in software projects"

## Referencias

- [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD)
- BMAD Documentation
