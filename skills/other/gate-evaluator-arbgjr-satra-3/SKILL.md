---
name: gate-evaluator
description: |
  Avalia quality gates entre fases do SDLC. Verifica artefatos obrigatorios,
  criterios de qualidade, e aprovacoes necessarias antes de permitir transicao.
  Use quando: transicao entre fases, verificacao manual de gate, auditoria de qualidade.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
user-invocable: false
---

# Gate Evaluator Skill

## Proposito

Esta skill avalia se um projeto atende aos criterios de qualidade para avancar
de uma fase do SDLC para a proxima. Cada gate tem:

1. **Artefatos obrigatorios** - Documentos, codigo, testes que devem existir
2. **Criterios de qualidade** - Metricas minimas que devem ser atendidas
3. **Aprovacoes** - Roles que devem aprovar a transicao

## Gates Disponiveis

| Gate | De | Para | Criterios Principais |
|------|-----|------|---------------------|
| Gate 0 | Preparacao | Descoberta | Compliance validado, escopo definido |
| Gate 1 | Descoberta | Requisitos | Fontes oficiais registradas, RAG pronto |
| Gate 2 | Requisitos | Arquitetura | Requisitos testaveis, NFRs definidos |
| Gate 3 | Arquitetura | Planejamento | ADRs completos, ameacas mitigadas |
| Gate 4 | Planejamento | Implementacao | Plano executavel, dependencias resolvidas |
| Gate 5 | Implementacao | Qualidade | Build verde, cobertura minima |
| Gate 6 | Qualidade | Release | Qualidade validada, seguranca ok |
| Gate 7 | Release | Operacao | Deploy seguro, rollback validado |

## Referencias de Padroes

Os gates validam conformidade com:
- `.docs/engineering-playbook/manual-desenvolvimento/qualidade.md` - Criterios de qualidade
- `.docs/engineering-playbook/manual-desenvolvimento/testes.md` - Requisitos de teste
- `.docs/engineering-playbook/stacks/devops/security.md` - Requisitos de seguranca

## Como Usar

### Avaliar um Gate

```python
# Via orchestrator
gate_result = evaluate_gate(
    from_phase=2,
    to_phase=3,
    project_context={
        "artifacts": [...],
        "approvals": [...]
    }
)
```

### Verificar Artefato Especifico

```python
artifact_check = check_artifact(
    artifact_type="requirements_document",
    path="docs/requirements.md"
)
```

### Obter Criterios de um Gate

```python
criteria = get_gate_criteria(gate_number=3)
```

## Formato de Avaliacao

### Input

```yaml
evaluate_gate:
  from_phase: number (0-7)
  to_phase: number (1-8)
  project_context:
    project_id: string
    artifacts:
      - type: string
        path: string
        created_at: datetime
        author: string
    approvals:
      - approver: string
        role: string
        approved_at: datetime
        scope: string
    metrics:
      test_coverage: float
      code_quality_score: float
      security_issues: number
```

### Output

```yaml
gate_result:
  gate_name: string
  from_phase: number
  to_phase: number

  passed: boolean
  score: float (0.0 - 1.0)

  artifact_checks:
    - artifact_type: string
      required: boolean
      present: boolean
      valid: boolean
      issues: list[string]

  quality_checks:
    - name: string
      threshold: number
      actual: number
      passed: boolean

  approval_checks:
    - role: string
      required: boolean
      approved: boolean
      approver: string

  blockers:
    - type: [artifact | quality | approval]
      description: string
      severity: [critical | high | medium]
      remediation: string

  recommendations:
    - string

  can_proceed: boolean
  human_approval_required: boolean
  escalation_reason: string
```

## Definicoes de Gate

Os arquivos de gate estao em `gates/` e seguem este formato:

```yaml
# gates/phase-2-to-3.yml
gate_name: requirements_to_architecture
from_phase: 2
to_phase: 3
description: "Transicao de Requisitos para Arquitetura"

required_artifacts:
  - type: requirements_document
    description: "Documento de requisitos completo"
    validation:
      - has_acceptance_criteria: true
      - stakeholder_approved: true
    path_pattern: "docs/requirements*.md"

  - type: user_stories
    description: "User stories com criterios de aceite"
    validation:
      - count_minimum: 1
      - has_priority: true
      - has_acceptance_criteria: true
    path_pattern: "docs/stories/*.md"

  - type: nfr_document
    description: "Requisitos nao funcionais"
    validation:
      - has_performance_requirements: true
      - has_security_requirements: true
    path_pattern: "docs/nfr*.md"

quality_checks:
  - name: requirements_completeness
    metric: completeness_score
    threshold: 0.8
    comparison: greater_or_equal

  - name: ambiguity_score
    metric: ambiguity_index
    threshold: 0.2
    comparison: less_or_equal

  - name: testability_score
    metric: testability_index
    threshold: 0.7
    comparison: greater_or_equal

human_approval:
  required: true
  roles:
    - product_owner
    - tech_lead
  timeout_hours: 24
  escalation_path:
    - engineering_manager
    - vp_engineering

gate_conditions:
  - all_artifacts_present: true
  - all_quality_checks_passed: true
  - required_approvals_obtained: true
```

## Checklists de Validacao

### Checklist de Artefato

```yaml
# checklists/artifact-checklist.yml
artifact_validation:
  requirements_document:
    structure:
      - has_title: true
      - has_version: true
      - has_author: true
      - has_date: true
    content:
      - has_problem_statement: true
      - has_proposed_solution: true
      - has_acceptance_criteria: true
      - has_stakeholder_approval: true
    format:
      - is_markdown: true
      - no_broken_links: true
      - images_have_alt_text: true
```

## Scripts de Validacao

### validate_gate.py

```python
#!/usr/bin/env python3
"""
Valida um gate do SDLC.
Uso: python validate_gate.py --from-phase 2 --to-phase 3 --project-dir /path/to/project
"""
import argparse
import yaml
from pathlib import Path

def load_gate_definition(from_phase: int, to_phase: int) -> dict:
    gate_file = Path(__file__).parent / f"gates/phase-{from_phase}-to-{to_phase}.yml"
    if not gate_file.exists():
        raise FileNotFoundError(f"Gate definition not found: {gate_file}")
    with open(gate_file) as f:
        return yaml.safe_load(f)

def check_artifacts(gate_def: dict, project_dir: Path) -> list:
    results = []
    for artifact in gate_def.get("required_artifacts", []):
        pattern = artifact.get("path_pattern", "*")
        matches = list(project_dir.glob(pattern))
        results.append({
            "type": artifact["type"],
            "required": True,
            "present": len(matches) > 0,
            "paths": [str(p) for p in matches],
            "issues": [] if matches else [f"Artifact not found: {pattern}"]
        })
    return results

def check_quality(gate_def: dict, metrics: dict) -> list:
    results = []
    for check in gate_def.get("quality_checks", []):
        metric_name = check["metric"]
        threshold = check["threshold"]
        comparison = check.get("comparison", "greater_or_equal")
        actual = metrics.get(metric_name, 0)

        if comparison == "greater_or_equal":
            passed = actual >= threshold
        elif comparison == "less_or_equal":
            passed = actual <= threshold
        else:
            passed = actual == threshold

        results.append({
            "name": check["name"],
            "threshold": threshold,
            "actual": actual,
            "passed": passed
        })
    return results

def evaluate_gate(from_phase: int, to_phase: int, project_dir: str, metrics: dict = None) -> dict:
    gate_def = load_gate_definition(from_phase, to_phase)
    project_path = Path(project_dir)
    metrics = metrics or {}

    artifact_results = check_artifacts(gate_def, project_path)
    quality_results = check_quality(gate_def, metrics)

    all_artifacts_present = all(a["present"] for a in artifact_results)
    all_quality_passed = all(q["passed"] for q in quality_results)

    passed = all_artifacts_present and all_quality_passed
    score = (
        sum(1 for a in artifact_results if a["present"]) / max(len(artifact_results), 1) * 0.5 +
        sum(1 for q in quality_results if q["passed"]) / max(len(quality_results), 1) * 0.5
    )

    blockers = []
    for a in artifact_results:
        if not a["present"]:
            blockers.append({
                "type": "artifact",
                "description": f"Missing artifact: {a['type']}",
                "severity": "critical",
                "remediation": f"Create {a['type']} matching pattern"
            })

    for q in quality_results:
        if not q["passed"]:
            blockers.append({
                "type": "quality",
                "description": f"Failed quality check: {q['name']}",
                "severity": "high",
                "remediation": f"Improve {q['name']} from {q['actual']} to {q['threshold']}"
            })

    return {
        "gate_name": gate_def["gate_name"],
        "from_phase": from_phase,
        "to_phase": to_phase,
        "passed": passed,
        "score": score,
        "artifact_checks": artifact_results,
        "quality_checks": quality_results,
        "blockers": blockers,
        "can_proceed": passed,
        "human_approval_required": gate_def.get("human_approval", {}).get("required", False)
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate SDLC gate")
    parser.add_argument("--from-phase", type=int, required=True)
    parser.add_argument("--to-phase", type=int, required=True)
    parser.add_argument("--project-dir", type=str, required=True)
    args = parser.parse_args()

    result = evaluate_gate(args.from_phase, args.to_phase, args.project_dir)
    print(yaml.dump(result, default_flow_style=False))
```

## Pontos de Pesquisa

Para melhorar esta skill:
- "quality gates CI/CD best practices 2025"
- "automated quality assurance software development"
- "DORA metrics quality gates"
