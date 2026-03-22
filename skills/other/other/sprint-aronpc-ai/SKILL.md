---
name: sprint
description: >-
  Gerencia sprints de desenvolvimento com brainstorm interativo, tracking e tarefas. Use quando precisar criar sprints, planejar iterações, atualizar progresso, ou gerenciar tarefas de desenvolvimento.
compatibility: Projetos Laravel
metadata:
  author: aronpc
  version: 1.0.0
  category: planning
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# sprint

## Resumo
Gerencia sprints de desenvolvimento com brainstorm interativo, tracking e documentação automática.

## Skills Relacionadas

| Skill | Quando usar junto |
|-------|-------------------|
| `spec` | Para criar specs técnicas das features do sprint |
| `planner` | Para planejamento técnico com phases e subtasks |
| `coder` | Para executar as tarefas do sprint |
| `issues` | Para converter issues em tarefas de sprint |
| `qa` | Para validar entregas antes de fechar o sprint |
| `workflow` | Para commits e branches do sprint |

## Quando usar

Use esta skill sempre que trabalhar com:
- **Criar novos sprints** → Inicia brainstorm interativo (negócio, arquitetura, dados)
- Atualizar status de sprints existentes
- Executar tarefas de um sprint
- Documentar casos de uso e cenários de teste
- Manter o arquivo `sprints/tracking.md`
- Validar estrutura e nomenclatura de sprints
- Documentar implementações e progresso
- Brainstorming e refinamento de ideias para sprints

## Comportamento Interativo

Ao criar um novo sprint, esta skill:
1. **FAZ PERGUNTAS** sobre negócio, dados, arquitetura, UX (uma por vez)
2. **APRESENTA PROPOSTA** estruturada antes de criar
3. **INTEGRA COM OUTRAS SKILLS** (laravel-architecture, pest-testing, etc.)
4. **CRIA SPRINT COMPLETO** com todos os detalhes técnicos

Não crie sprints sem antes fazer o brainstorm!

## Execução Natural de Sprints

### Prompt: Executar Tarefa de Sprint

Use este prompt automaticamente quando o usuário pedir para executar algo relacionado a um sprint existente:

```
Você está ajudando o usuário a executar tarefas de um sprint. Sua tarefa é TRABALHAR na tarefa E ATUALIZAR o sprint automaticamente.

## CONTEXTO

- Tarefa solicitada: [descrição do que o usuário pediu]
- Sprints existentes: [listar sprints encontrados em sprints/]
- Commit mais recente: [mostrar último commit]

## SUA TAREFA

1. Primeiro, encontre o sprint ativo (status "Em Andamento 🚧") ou o último sprint modificado
2. Leia o arquivo do sprint completo
3. Execute a tarefa solicitada pelo usuário
4. **CRÍTICO**: Após completar a tarefa, ATUALIZE o arquivo do sprint:
   - Marque [x] na tarefa correspondente que foi completada
   - Se era a última tarefa pendente, mude status para "Concluído ✅" e adicione data de conclusão
   - Se ainda há tarefas pendentes mas estava como "Planejado", mude para "Em Andamento 🚧"
5. Salve o arquivo atualizado

## IMPORTANTE

- Sempre atualize o sprint após executar qualquer tarefa
- Não peça confirmação - a atualização é automática
- Use o formato de data AAAA-MM-DD
- Preserve todo o resto do conteúdo do sprint

## EXEMPLO

Se o usuário pediu "criar a migration de usuários" e isso é a tarefa "- [ ] Criar migration de usuários" no sprint 001:
1. Execute: php artisan make:migration create_users_table
2. Abra sprints/001-nome.md
3. Mude "- [ ] Criar migration de usuários" para "- [x] Criar migration de usuários"
4. Se era a última tarefa: mude status para "Concluído ✅" e adicione "**Data Fim**: 2026-02-13"
5. Salve e informe o usuário que o sprint foi atualizado
```

### Prompt: Iniciar Sprint

Use quando o usuário começar a trabalhar em um sprint planejado:

```
O usuário está começando a trabalhar em um sprint. ATUALIZE o status automaticamente.

## CONTEXTO

- Sprint sendo iniciado: [nome do arquivo]
- Status atual: [deve ser "Planejado"]

## SUA TAREFA

1. Abra o arquivo do sprint
2. Mude "**Status**: Planejado 📋" para "**Status**: Em Andamento 🚧"
3. Adicione "**Data Início**: [data de hoje em AAAA-MM-DD]" abaixo da linha de status
4. Salve o arquivo
5. Informe o usuário que o sprint foi iniciado

Não peça confirmação - faça automaticamente.
```

### Prompt: Finalizar Sprint

Use quando todas as tarefas de um sprint forem completadas:

```
O usuário completou todas as tarefas de um sprint. FINALIZE o sprint automaticamente.

## CONTEXTO

- Sprint sendo finalizado: [nome do arquivo]
- Status atual: [deve ser "Em Andamento"]

## SUA TAREFA

1. Abra o arquivo do sprint
2. Verifique que TODAS as tarefas estão marcadas como [x]
3. Mude "**Status**: Em Andamento 🚧" para "**Status**: Concluído ✅"
4. Adicione "**Data Fim**: [data de hoje em AAAA-MM-DD]" (se não existir)
5. Salve o arquivo
6. ATUALIZE sprints/tracking.md com o novo status
7. Sugira commit: "git add sprints/[arquivo] sprints/tracking.md && git commit -m 'Complete: sprint [nome]'"

Não peça confirmação - faça automaticamente.
```

### Prompt: Pausar Sprint

Use quando o usuário precisar pausar um sprint em andamento:

```
O usuário está pausando um sprint. ATUALIZE o status automaticamente.

## CONTEXTO

- Sprint sendo pausado: [nome do arquivo]
- Motivo: [bloqueio externo, dependência, etc.]
- Status atual: [deve ser "Em Andamento"]

## SUA TAREFA

1. Abra o arquivo do sprint
2. Mude "**Status**: Em Andamento 🚧" para "**Status**: Pausado ⏸️"
3. Adicione seção "## Bloqueios" se não existir e documente o motivo
4. Adicione "**Data Pausa**: [data de hoje em AAAA-MM-DD]"
5. Salve o arquivo
6. ATUALIZE sprints/tracking.md

Não peça confirmação - faça automaticamente.
```

### Prompt: Retomar Sprint

Use quando o usuário retomar um sprint pausado:

```
O usuário está retomando um sprint pausado. ATUALIZE o status automaticamente.

## CONTEXTO

- Sprint sendo retomado: [nome do arquivo]
- Status atual: [deve ser "Pausado"]

## SUA TAREFA

1. Abra o arquivo do sprint
2. Mude "**Status**: Pausado ⏸️" para "**Status**: Em Andamento 🚧"
3. Remova ou atualize bloqueios resolvidos
4. Adicione "**Data Retomada**: [data de hoje em AAAA-MM-DD]"
5. Salve o arquivo
6. ATUALIZE sprints/tracking.md

Não peça confirmação - faça automaticamente.
```

> Para prompts adicionais (Adicionar Tarefa, Listar Sprints, Dividir Sprint, Clonar Sprint, Retrospectiva, Criar Sprint Interativo, Refinamento, Casos de Uso, Bloqueios, Detalhar Técnico, Relatório), veja `references/prompts-avancados.md`.

## Brainstorming de Sprints

**NOTA**: Ao criar um novo sprint, o brainstorm é automático e interativo (ver `references/prompts-avancados.md` para o prompt completo de criação interativa).

Use esta seção para **refinar** sprints existentes ou fazer brainstorm manual.

### Ask (uma de cada vez)

- **Goal**: Qual resultado os usuários devem alcançar?
- **Domain**: Quais contextos ou pacotes estão envolvidos?
- **Data**: Novos modelos/relacionamentos? Queries necessárias?
- **Interfaces**: HTTP/API/CLI? Inputs/outputs necessários? Authz?
- **Side-effects**: Email, storage, filas, sistemas externos?
- **Performance**: Throughput, latência, paginação, riscos N+1?
- **Observability**: Logs, métricas, eventos, tratamento de falhas?
- **Testing**: Ponto de entrada TDD, fixtures/factories, casos de borda?
- **Environment**: Sail ou host? Disponibilidade de DB/cache/mail/storage?

### Propose

Apresente um design de 200–300 palavras, cobrindo:
- Rotas/contratos, validação, DTOs/transformers
- Services (ports+adapters, strategies/pipelines)
- Mudanças de modelo de dados e migrations
- Jobs/events/listeners onde relevante
- Estratégia de testes (feature/unit), factories e seeds
- Quality gates e plano de rollout

### Prepare Next Steps

Sugerir um plano de implementação breve; então use `laravel:writing-plans` para formalizar.

## Casos de Uso

Casos de uso descrevem como um usuário interage com o sistema para alcançar um objetivo específico. Eles conectam **requisitos** → **implementação** → **testes**.

Para estrutura completa, exemplos, boas práticas e mapeamento para testes, veja `references/templates.md`.

## Estrutura de Sprints

### Diretório Base

Todos os sprints são mantidos em `sprints/`:
- `sprints/tracking.md` - Visão geral e rastreamento de todos os sprints
- `sprints/XXX-nome-do-sprint.md` - Documentação individual de cada sprint

### Nomenclatura de Arquivos

- **Tracking**: `sprints/tracking.md`
- **Sprint individual**: `sprints/XXX-nome-curto.md`
  - `XXX`: Número sequencial de 3 dígitos (001, 002, 003...)
  - `nome-curto`: Nome em kebab-case, descritivo

## Status de Sprints

| Status | Descrição |
|--------|-----------|
| **Planejado** 📋 | Sprint planejado, aguardando início |
| **Em Andamento** 🚧 | Sprint em execução ativa |
| **Pausado** ⏸️ | Sprint temporariamente suspenso (bloqueio externo) |
| **Em Revisão** 👀 | Sprint em code review ou QA |
| **Concluído** ✅ | Sprint finalizado e implementado |
| **Arquivado** 📦 | Sprint antigo/obsoleto, mantido para histórico |
| **Cancelado** ❌ | Sprint cancelado |

## Metadados de Sprints

### Campos Recomendados

```markdown
## Metadados
- **Prioridade**: 🔴 Alta / 🟡 Média / 🟢 Baixa
- **Complexidade**: X pontos ou X horas estimadas
- **Tags**: feature, bugfix, refactor, chore, infra, docs
- **Depende de**: [000-outro-sprint.md]
- **Branch Git**: feature/sprint-XXX-nome
- **Stakeholder**: @responsável
- **Sprint relacionado**: [YYY-sprint-relacionado.md]
```

Para tabelas completas de tags e prioridades, veja `references/templates.md`.

## Criar Novo Sprint

Ao criar um novo sprint, INICIE UM BRAINSTORM INTERATIVO. Veja `references/prompts-avancados.md` para o prompt completo de criação interativa com fases de Descoberta, Proposta, Confirmação e Criação.

Após o brainstorm, use os templates de `references/templates.md` (Template Padrão ou Template com Blueprint).

### CRITÉRIOS DE QUALIDADE

Antes de finalizar, verifique:
- [ ] O nome do sprint é descritivo (kebab-case)
- [ ] O número de sprint tem 3 dígitos com zero à esquerda quando necessário
- [ ] A descrição explica claramente o objetivo
- [ ] Os requisitos são claros e mensuráveis
- [ ] Cada requisito funcional tem um caso de uso correspondente
- [ ] Casos de uso seguem a estrutura: Como/Quero/Para Que
- [ ] Cada caso de uso tem cenário principal + alternativos + exceções
- [ ] Regras de negócio estão documentadas
- [ ] **Estrutura de dados documentada** (models, migrations, relacionamentos)
- [ ] **API endpoints com contratos** (se aplicável)
- [ ] **Telas/componentes descritos** (se frontend)
- [ ] **Fluxos de integração mapeados** (se complexo)
- [ ] **Exemplos de testes fornecidos**
- [ ] Há mapeamento de casos de uso para testes
- [ ] As tarefas são específicas e acionáveis
- [ ] Há dependências documentadas
- [ ] Testes planejados
- [ ] Formatação correta e consistente

## Filament Blueprint Integration

### Quando usar Blueprint com Sprints

Use Filament Blueprint quando o sprint envolver:
- Múltiplas tabelas/relacionamentos
- Formulários complexos
- Recursos Filament (Resources, Widgets, etc.)
- Estruturas de banco de dados com múltiplas migrations

### Estrutura com Blueprint

```
sprints/
├── XXX-nome-do-sprint.md          ← Documentação do sprint
└── blueprints/                         ← Planos Blueprint (dentro do sprint!)
    └── XXX-nome-do-sprint/
        ├── blueprint.yaml
        ├── migrations/
        └── resources/
            └── Resources/
```

Para o template completo de sprint com Blueprint, veja `references/templates.md`.

## Atualizar Tracking

### Prompt: Atualizar Tracking após Mudanças

Use este prompt quando o usuário modificar sprints e precisar atualizar o tracking:

```
Você é um assistente de gerenciamento de sprints. Sua tarefa é ATUALIZAR o arquivo `sprints/tracking.md` com as mudanças feitas nos sprints.

## CONTEXTO

- Sprints modificados: [listar arquivos .md modificados]
- Último commit: [hash ou mensagem do commit]
- Status atual de cada sprint: [listar status]

## SUA TAREFA

1. Ler o arquivo `sprints/tracking.md` atual
2. Para cada sprint modificado:
   - Extrair: nome, status, data início, data fim, descrição
   - Verificar se já existe entrada no tracking.md
   - Se existir: ATUALIZAR a entrada (status, datas)
   - Se não existir: ADICIONAR nova entrada no formato correto
3. Garantir que todas as linhas da tabela mantenham o formato
4. Salvar o arquivo atualizado

## FORMATO DA TABELA (mantenha este padrão)

| Sprint | Status | Data Início | Data Fim | Descrição |
|--------|--------|-------------|----------|-----------|
| [001-nome](sprints/001-nome.md) | **Status** emoji | data-início | data-fim | Descrição breve |

## STATUS E EMOJIS PERMITIDOS

- **Planejado** 📋
- **Em Andamento** 🚧
- **Pausado** ⏸️
- **Em Revisão** 👀
- **Concluído** ✅
- **Arquivado** 📦
- **Cancelado** ❌

## IMPORTANTE

- Preserve a formatação da tabela
- As datas devem estar no formato AAAA-MM-DD
```

## Convenções

- Usar kebab-case para nomes de arquivos
- Usar português brasileiro para documentação
- Ser descritivo na descrição dos sprints
- Marcar status com emojis para identificação rápida
- Atualizar `tracking.md` sempre que modificar sprints
- **Sempre atualizar o sprint após executar tarefas** - isso é automático
