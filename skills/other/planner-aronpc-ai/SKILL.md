---
name: planner
description: >-
  Cria planos estruturados para features, refatorações e investigações. Use quando precisar planejar uma implementação, definir tasks e subtasks, ou organizar o trabalho antes de começar a codar.
compatibility: Qualquer projeto
metadata:
  author: aronpc
  version: 1.0.0
  category: planning
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
---

# planner

## Resumo
Cria planos de implementação estruturados com workflows para feature, refactor, investigation e migration.

## Skills Relacionadas

| Skill | Quando usar junto |
|-------|-------------------|
| `spec` | Para usar specs como source de requisitos |
| `sprint` | Para usar sprints como source de tarefas |
| `coder` | Para executar o plano criado |
| `qa` | Para validar a qualidade da implementação |
| `architecture` | Para definir arquitetura no plano |

## Quando usar

Use esta skill quando precisar:
- Planejar a implementação de uma nova feature
- Estruturar um refactoring complexo
- Investigar um bug ou comportamento inesperado
- Planejar uma migration de dados ou infraestrutura
- Criar planos de implementação acionáveis

**Não use para:**
- Tarefas triviais (use o workflow "simple")
- Análise de codebase sem objetivo de implementação
- Planejamento estratégico de produto (use roadmap-strategy)

---

## Workflow Types

Escolha o workflow apropriado baseado no tipo de tarefa:

| Workflow | Quando usar | Exemplos |
|----------|-------------|----------|
| `feature` | Nova funcionalidade | Adicionar autenticação OAuth, criar dashboard |
| `refactor` | Melhorar código existente | Extrair componentes, renomear módulos |
| `investigation` | Entender/debugar | Bug investigation, performance analysis |
| `migration` | Mover dados/infra | Database migration, framework upgrade |
| `simple` | Tarefas diretas | Fix typo, atualizar config |

### Feature Workflow
Para novas funcionalidades que adicionam valor ao produto:
1. Analise requisitos e dependências
2. Design da solução (API, componentes, fluxo)
3. Implementação por camadas (backend → frontend)
4. Testes e validação
5. Documentação

### Refactor Workflow
Para melhorias de código sem mudança de comportamento:
1. Identifique o que será refatorado
2. Garanta testes existentes passando
3. Faça mudanças incrementais
4. Rode testes após cada mudança
5. Valide comportamento inalterado

### Investigation Workflow
Para bugs ou comportamentos inesperados:
1. Defina o problema claramente
2. Colete evidências (logs, stack traces)
3. Forme hipóteses
4. Teste hipóteses sistematicamente
5. Documente causa raiz e solução

### Migration Workflow
Para migrações de dados ou infraestrutura:
1. Mapeie estado atual → estado desejado
2. Identifique dependências e riscos
3. Crie plano de rollback
4. Execute em fases
5. Valide cada fase

### Simple Workflow
Para tarefas triviais:
1. Entenda a mudança
2. Implemente
3. Verifique
4. Commit

---

## Estrutura do Plano

O plano de implementação segue esta estrutura JSON:

```json
{
  "spec_id": "spec-001",
  "workflow_type": "feature",
  "phases": [
    {
      "id": 0,
      "name": "Pre-Planning",
      "subtasks": [
        {
          "id": "st-0-1",
          "title": "Load context",
          "status": "pending"
        }
      ]
    }
  ],
  "verification_strategy": {
    "type": "command",
    "command": "npm test"
  }
}
```

### Fases do Plano

| Fase | Nome | Objetivo |
|------|------|----------|
| 0 | Pre-Planning | Carregar contexto, entender requisitos |
| 1 | Analysis | Analisar codebase, identificar arquivos |
| 2 | Design | Design da solução, estrutura |
| 3 | Implementation | Implementação principal |
| 4 | Testing | Testes unitários, integração |
| 5 | Review | Code review, ajustes |
| 6 | Integration | Merge, deployment |
| 7 | Verification | Validação final |

### Estrutura de Subtasks

Cada subtask deve ter:
- `id`: Identificador único (st-fase-numero)
- `title`: Título descritivo e acionável
- `description`: Detalhes da tarefa (opcional)
- `status`: pending | in_progress | completed | blocked
- `verification`: Como verificar conclusão (opcional)
- `files`: Arquivos relacionados (opcional)

---

## Verification Strategy

Cada plano deve incluir uma estratégia de verificação. Veja `references/verification-types.md` para detalhes.

| Tipo | Quando usar | Exemplo |
|------|-------------|---------|
| `command` | Testes, builds | `npm test`, `make build` |
| `api` | APIs REST/GraphQL | `curl localhost:3000/api/health` |
| `browser` | UI web | Puppeteer, screenshots |
| `e2e` | Fluxos completos | Playwright, Cypress |
| `manual` | Verificação humana | Code review, UX testing |
| `none` | Não verificável automaticamente | Documentação |

---

## Pre-Planning Checklist

Antes de criar o plano, verifique:

- [ ] Li e entendi a spec/task
- [ ] Identifiquei o workflow type apropriado
- [ ] Selecionei a verification strategy
- [ ] Mapeei arquivos que serão modificados
- [ ] Identifiquei dependências
- [ ] Avaliei riscos e complexidade
- [ ] Defini critérios de sucesso

---

## Exemplo de Plano

```json
{
  "spec_id": "spec-add-oauth",
  "workflow_type": "feature",
  "phases": [
    {
      "id": 0,
      "name": "Pre-Planning",
      "subtasks": [
        {"id": "st-0-1", "title": "Load spec and understand requirements", "status": "pending"},
        {"id": "st-0-2", "title": "Review existing auth implementation", "status": "pending"}
      ]
    },
    {
      "id": 1,
      "name": "Analysis",
      "subtasks": [
        {"id": "st-1-1", "title": "Identify files to modify", "status": "pending"},
        {"id": "st-1-2", "title": "Check OAuth provider docs", "status": "pending"}
      ]
    },
    {
      "id": 3,
      "name": "Implementation",
      "subtasks": [
        {"id": "st-3-1", "title": "Add OAuth provider config", "status": "pending", "files": ["src/auth/config.ts"]},
        {"id": "st-3-2", "title": "Create OAuth callback handler", "status": "pending", "files": ["src/auth/oauth.ts"]},
        {"id": "st-3-3", "title": "Update login UI", "status": "pending", "files": ["src/components/Login.tsx"]}
      ]
    },
    {
      "id": 4,
      "name": "Testing",
      "subtasks": [
        {"id": "st-4-1", "title": "Add OAuth unit tests", "status": "pending"},
        {"id": "st-4-2", "title": "Test OAuth flow manually", "status": "pending"}
      ]
    }
  ],
  "verification_strategy": {
    "type": "browser",
    "steps": ["Navigate to login", "Click OAuth button", "Verify redirect", "Verify login success"]
  }
}
```

---

## Referências

- `references/verification-types.md` - Tipos de verificação detalhados
- `references/workflow-patterns.md` - Padrões de workflow
- `references/plan-structure.md` - Schema JSON completo
