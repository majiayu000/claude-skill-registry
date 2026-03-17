---
name: alignment-workflow
description: |
  Workflow formal para coleta de consenso em decisões organizacionais (ODRs).
  Gerencia ciclo de vida de ODRs desde criação até aprovação.
  Use quando: coletar inputs, rastrear aprovações, escalar decisões.
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
user-invocable: false
version: "1.0.0"
---

# Alignment Workflow Skill

## Propósito

Esta skill implementa o workflow formal para coleta de consenso em Organizational Decision Records (ODRs), garantindo que todos os stakeholders relevantes sejam consultados antes de decisões críticas.

## Ciclo de Vida do ODR

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CICLO DE VIDA ODR                            │
└─────────────────────────────────────────────────────────────────────┘

  [Detectar]     [Criar]       [Coletar]     [Aprovar]    [Finalizar]
      │             │              │             │             │
      ▼             ▼              ▼             ▼             ▼
  ┌───────┐    ┌───────┐    ┌───────────┐  ┌───────────┐  ┌─────────┐
  │Trigger│───▶│ Draft │───▶│ Pending   │─▶│ Pending   │─▶│Approved │
  │       │    │       │    │ Input     │  │ Approval  │  │   or    │
  └───────┘    └───────┘    └───────────┘  └───────────┘  │Rejected │
                                 │              │         └─────────┘
                                 │              │              │
                              [timeout]     [timeout]          │
                                 │              │              ▼
                                 ▼              ▼         ┌─────────┐
                            [escalate]    [escalate]     │ ADRs    │
                                                         │derivados│
                                                         └─────────┘
```

## Estados do ODR

| Estado | Descrição | Ações Permitidas |
|--------|-----------|------------------|
| `draft` | Rascunho inicial | Editar, Adicionar alternativas |
| `pending_input` | Aguardando inputs de stakeholders | Fornecer input, Escalar |
| `pending_approval` | Inputs coletados, aguardando aprovação | Aprovar, Rejeitar, Revisar |
| `approved` | Decisão aprovada | Criar ADRs derivados |
| `rejected` | Decisão rejeitada | Arquivar, Reabrir |
| `superseded` | Substituída por outro ODR | - |

## Scripts Disponíveis

### consensus_manager.py

Gerencia o workflow de consenso.

```bash
# Transicionar ODR para próximo estado
python3 .claude/skills/alignment-workflow/scripts/consensus_manager.py \
  transition --odr ODR-001 --to pending_input

# Registrar input de stakeholder
python3 .claude/skills/alignment-workflow/scripts/consensus_manager.py \
  add-input --odr ODR-001 --stakeholder "CTO" --input "Prefiro build interno"

# Aprovar ODR
python3 .claude/skills/alignment-workflow/scripts/consensus_manager.py \
  approve --odr ODR-001 --approver "PM" --comment "Alinhado com estratégia"

# Verificar timeouts
python3 .claude/skills/alignment-workflow/scripts/consensus_manager.py \
  check-timeouts --project my-project
```

### escalation.py

Gerencia escalações de decisões.

```bash
# Escalar ODR
python3 .claude/skills/alignment-workflow/scripts/escalation.py \
  escalate --odr ODR-001 --reason "Timeout de input do CTO"

# Ver escalações pendentes
python3 .claude/skills/alignment-workflow/scripts/escalation.py \
  list --project my-project
```

## Regras de Timeout

| Situação | Timeout Padrão | Ação |
|----------|----------------|------|
| Input de stakeholder | 48h | Reminder após 24h, escalação após 48h |
| Aprovação | 72h | Reminder após 48h, escalação após 72h |
| Conflito entre inputs | 24h | Escalar para decision maker |

## Integração com Gates

### Phase 2→3 (Requirements → Architecture)

```yaml
gate_check:
  odr_required:
    - condition: "project.budget > 100000"
      category: "resource"
      status_required: "approved"
    - condition: "stakeholders.count >= 3"
      category: "business"
      status_required: "approved"
```

### Phase 3→4 (Architecture → Planning)

```yaml
gate_check:
  odr_required:
    - condition: "decisions.has_build_vs_buy"
      category: "strategic"
      status_required: "approved"
    - condition: "architecture.significant_tradeoffs"
      category: "business"
      status_required: "approved"
```

### Phase 6→7 (QA → Release)

```yaml
gate_check:
  odr_required:
    - condition: "scope.changed_after_planning"
      category: "scope"
      status_required: "approved"
```

## Templates de Comunicação

### Template: Solicitação de Input

```markdown
## 📋 Solicitação de Input - {odr_id}

**Decisão**: {title}
**Categoria**: {category}
**Deadline**: {deadline}

### Contexto
{business_context}

### Alternativas
{for alt in alternatives}
**{alt.id}. {alt.title}**
- ✅ Prós: {alt.pros}
- ❌ Contras: {alt.cons}
- 💰 Custo estimado: {alt.estimated_cost}
{/for}

### Sua Contribuição
Por favor, responda até **{deadline}**:

1. Qual alternativa você recomenda?
2. Há riscos não mapeados?
3. Quais trade-offs são aceitáveis?

---
*Use `/odr-input {odr_id} "Seu feedback"` para responder*
```

### Template: Reminder

```markdown
## ⏰ Reminder: Input Pendente - {odr_id}

Olá {stakeholder_name},

O prazo para seu input em **{title}** é amanhã.

- 📅 Deadline: {deadline}
- 📋 ODR: {odr_id}

Por favor, forneça sua contribuição o mais breve possível.

---
*Se não puder contribuir, avise para marcarmos como "waived"*
```

### Template: Escalação

```markdown
## 🚨 Escalação: ODR Sem Resposta - {odr_id}

**Atenção {decision_maker}**,

O ODR **{title}** não recebeu inputs necessários dentro do prazo.

### Stakeholders Pendentes
{for s in pending_stakeholders}
- {s.name} ({s.role}): Sem resposta desde {s.requested_at}
{/for}

### Impacto
A falta de input pode atrasar a decisão e impactar o cronograma do projeto.

### Ações Solicitadas
1. Contatar stakeholders diretamente
2. Ou marcar inputs como "waived" e prosseguir

---
*Deadline para resolução: {escalation_deadline}*
```

## Workflow: Coletar Consenso

```python
def collect_consensus(odr_id: str) -> dict:
    """
    Workflow completo para coletar consenso em um ODR.
    
    Returns:
        dict com status e resultados
    """
    odr = load_odr(odr_id)
    
    # 1. Validar que ODR está em estado válido
    if odr["status"] not in ["draft", "pending_input"]:
        return {"error": f"ODR em estado inválido: {odr['status']}"}
    
    # 2. Se draft, transicionar para pending_input
    if odr["status"] == "draft":
        odr = transition_odr(odr_id, "pending_input")
        send_input_requests(odr)
    
    # 3. Verificar inputs coletados
    consulted = odr["stakeholders"]["consulted"]
    pending = [s for s in consulted if s["input_status"] == "pending"]
    received = [s for s in consulted if s["input_status"] == "received"]
    waived = [s for s in consulted if s["input_status"] == "waived"]
    
    # 4. Se todos inputs coletados, transicionar para pending_approval
    if not pending:
        odr = transition_odr(odr_id, "pending_approval")
        notify_decision_maker(odr)
        return {
            "status": "pending_approval",
            "inputs_received": len(received),
            "inputs_waived": len(waived)
        }
    
    # 5. Verificar timeouts
    for stakeholder in pending:
        requested_at = datetime.fromisoformat(stakeholder.get("requested_at", ""))
        if datetime.now() - requested_at > timedelta(hours=48):
            # Escalar
            escalate_odr(odr_id, f"Timeout de input: {stakeholder['name']}")
    
    return {
        "status": "pending_input",
        "pending_inputs": len(pending),
        "received_inputs": len(received)
    }
```

## Workflow: Aprovar ODR

```python
def approve_odr(odr_id: str, approver: str, approved: bool, comment: str = "") -> dict:
    """
    Registra aprovação/rejeição de um ODR.
    
    Args:
        odr_id: ID do ODR
        approver: Nome do aprovador
        approved: True para aprovar, False para rejeitar
        comment: Comentário opcional
    
    Returns:
        dict com resultado
    """
    odr = load_odr(odr_id)
    
    # Validar estado
    if odr["status"] != "pending_approval":
        return {"error": f"ODR não está aguardando aprovação: {odr['status']}"}
    
    # Validar aprovador
    decision_maker = odr["stakeholders"]["decision_maker"]
    if approver.lower() != decision_maker["name"].lower():
        return {"error": f"Apenas {decision_maker['name']} pode aprovar este ODR"}
    
    # Registrar aprovação
    odr["approvals"].append({
        "stakeholder": approver,
        "approved": approved,
        "approved_at": datetime.now().isoformat(),
        "comments": comment
    })
    
    # Atualizar status
    new_status = "approved" if approved else "rejected"
    odr["status"] = new_status
    odr["updated_at"] = datetime.now().isoformat()
    
    # Salvar
    save_odr(odr)
    
    # Notificar stakeholders
    notify_stakeholders(odr, f"ODR {new_status}")
    
    # Se aprovado, sugerir criação de ADRs técnicos
    if approved:
        suggested_adrs = suggest_derived_adrs(odr)
        return {
            "status": new_status,
            "suggested_adrs": suggested_adrs
        }
    
    return {"status": new_status}
```

## Integração com GitHub

Quando ODRs são criados, podem gerar issues/discussions no GitHub:

```python
def sync_odr_to_github(odr_id: str) -> dict:
    """Sincroniza ODR com GitHub para visibilidade."""
    odr = load_odr(odr_id)
    
    # Criar issue para ODR
    issue = create_github_issue(
        title=f"[ODR] {odr['title']}",
        body=format_odr_for_github(odr),
        labels=["odr", f"category:{odr['metadata']['category']}"]
    )
    
    # Atualizar ODR com referência
    odr["relationships"]["github_issue"] = issue["number"]
    save_odr(odr)
    
    return {"github_issue": issue["number"]}
```

## Referências

- Agente: `.claude/agents/alignment-agent.md`
- Template ODR: `.agentic_sdlc/templates/odr-template.yml`
- Guia ADR vs ODR: `.docs/guides/adr-vs-odr.md`
- Issue #9: Implementar workflow de consenso
