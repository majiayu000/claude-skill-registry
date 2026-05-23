---
name: meta-configuracao-evolucao
description: Automatiza processo de pesquisa de documentação oficial, extração de melhores práticas e aplicação no projeto Ultrathink através de skills/agents/hooks
allowed-tools: [WebSearch, WebFetch, Read, Write, Edit, Bash, Grep]
---

# Meta-Configuração e Evolução Skill

## Objetivo

Esta é uma **skill meta** que automatiza o ciclo completo de:

1. 🔍 **Research**: Buscar documentação oficial de tecnologias
2. 📚 **Learning**: Extrair padrões, exemplos e melhores práticas
3. 🛠️ **Implementation**: Criar skills/agents/hooks customizados
4. 📝 **Documentation**: Documentar conhecimento adquirido

## Quando Esta Skill Ativa

Ativa automaticamente quando você precisa:

- Integrar nova tecnologia ao Ultrathink
- Atualizar configurações baseado em nova versão
- Implementar padrão da indústria
- Criar skills/agents para novo domínio
- Automatizar workflow recorrente

## Processo Automatizado (6 Etapas)

### Etapa 1: Identificar Necessidade

**Gatilhos:**
- Usuário solicita integração de tecnologia
- Nova versão de dependência lançada
- Padrão emergente na comunidade
- Débito técnico identificado

**Ações:**
- Definir escopo da pesquisa
- Listar fontes oficiais
- Priorizar documentação

### Etapa 2: Web Research

**Estratégia de Busca:**

```bash
# 1. Busca geral
WebSearch("Nome da Tecnologia official documentation 2025")

# 2. Busca específica
WebSearch("Nome da Tecnologia best practices patterns examples")

# 3. Busca de casos de uso
WebSearch("Nome da Tecnologia React integration tutorial")
```

**Fontes Priorizadas:**
1. **Documentação Oficial** (docs.*, *.dev)
2. **GitHub Repos Oficiais** (README, wiki, examples/)
3. **Blog Oficial** (release notes, announcements)
4. **Community Hubs** (Dev.to, Medium autores verificados)
5. **Stack Overflow** (respostas aceitas com +100 votos)

**Informações a Extrair:**
- Estrutura de arquivos recomendada
- Padrões de código (code style guides)
- Exemplos práticos (working code)
- Melhores práticas (best practices)
- Configurações comuns (setup guides)
- Pitfalls conhecidos (common mistakes)
- Integrações (com stack existente)

### Etapa 3: Análise e Síntese

**Processar Informação:**

```javascript
// Template mental
const knowledge = {
  technology: "Nome",
  version: "X.Y.Z",

  // Conceitos-chave
  coreConcepts: [
    { name: "Conceito 1", description: "...", importance: "high" },
    { name: "Conceito 2", description: "...", importance: "medium" }
  ],

  // Padrões de código
  patterns: [
    {
      name: "Pattern Name",
      problem: "O que resolve",
      solution: "Como resolver",
      example: "// código"
    }
  ],

  // Integração com stack atual
  integration: {
    react: "Como integrar com React",
    vite: "Configuração Vite necessária",
    tailwind: "Classes Tailwind relevantes"
  },

  // Pitfalls
  pitfalls: [
    { mistake: "Erro comum", solution: "Como evitar" }
  ]
}
```

### Etapa 4: Decisão de Aplicação

**Matriz de Decisão:**

| Aplicação | Quando Usar | Exemplo |
|-----------|-------------|---------|
| **Skill** | Conhecimento que ativa automaticamente por contexto | ux-nomenclature, component-refactor |
| **Agent** | Tarefa complexa com múltiplos passos | ux-refactor-agent, test-generator-agent |
| **Hook** | Automação de evento específico | PostToolUse para formatar código |
| **Slash Command** | Comando manual recorrente | /test, /deploy, /fix |
| **MCP Server** | Integração externa com protocolo | chrome-devtools, playwright |

**Critérios de Escolha:**

```
Skill:
  ✅ Conhecimento declarativo
  ✅ Ativa por contexto (automático)
  ✅ Sem lógica complexa
  ✅ Consulta rápida

Agent:
  ✅ Múltiplos passos
  ✅ Lógica condicional
  ✅ System prompt extenso
  ✅ Context window isolado

Hook:
  ✅ Reação a evento
  ✅ Automação shell command
  ✅ Pode bloquear ação
  ✅ Transformação de input

Slash Command:
  ✅ Invocação manual
  ✅ Workflow definido
  ✅ Substitui comandos longos
```

### Etapa 5: Geração de Artefatos

#### 5.1 Criar Skill

**Estrutura:**

```markdown
---
name: tecnologia-nome
description: Descrição concisa do que a skill faz
allowed-tools: [Read, Edit, Grep, ...]
---

# Skill Title

## Objetivo
[O que esta skill faz]

## Conceitos-Chave
[Conhecimento extraído da documentação]

## Padrões de Código
[Exemplos práticos]

## Integração com Ultrathink
[Como usar no contexto do projeto]

## Comandos Úteis
[Comandos bash/grep para aplicar]

## Referências
[Links para docs oficiais]

## Ativação Automática
Esta skill ativa quando você:
- [Condição 1]
- [Condição 2]
```

**Salvar em:** `.claude/skills/{tecnologia-nome}/SKILL.md`

#### 5.2 Criar Agent

**Estrutura:**

```markdown
# Agent Name

## System Prompt

You are a specialized agent for [task description].

### Expertise Areas
- [Area 1]
- [Area 2]

### Tools Available
- Read
- Edit
- Bash
- [outros]

### Workflow

1. **Step 1**: [Description]
   - Action: [what to do]
   - Output: [expected result]

2. **Step 2**: [Description]
   ...

### Quality Criteria

Your output must:
- [ ] Criterion 1
- [ ] Criterion 2

### Examples

[Provide 2-3 examples of input/output]

### Constraints

DO NOT:
- [Don't 1]
- [Don't 2]

ALWAYS:
- [Always 1]
- [Always 2]
```

**Salvar em:** `.claude/agents/{agent-name}.md`

#### 5.3 Criar Hook

**Estrutura (hooks.toml):**

```toml
[[PreToolUse]]
matcher = "Edit|Write"
name = "format-code"

  [[PreToolUse.hooks]]
  type = "command"
  command = '''
    # Hook logic here
    prettier --write "$FILE"
  '''
```

**Adicionar em:** `.claude/hooks.toml`

### Etapa 6: Documentação e Validação

**Criar Documento de Referência:**

```markdown
# [Tecnologia] Integration Guide - Ultrathink

## Overview
[O que foi integrado e por quê]

## Research Summary
- Official Docs: [link]
- Key Concepts: [list]
- Best Practices: [list]

## Implementation
### Skills Created
- [skill-name]: [description]

### Agents Created
- [agent-name]: [description]

### Hooks Added
- [hook-name]: [trigger] → [action]

## Usage Examples
[3-5 exemplos práticos]

## Testing
[Como validar que funciona]

## Maintenance
[Como manter atualizado]

## References
[Todos os links consultados]
```

**Salvar em:** `docs/integrations/{tecnologia}-integration.md`

## Templates Prontos

### Template: Nova Tecnologia

```bash
# Workflow completo
1. WebSearch("[Tech] official documentation best practices 2025")
2. WebFetch(docs_url, "Extract setup, patterns, examples")
3. Criar skill: .claude/skills/{tech}/SKILL.md
4. Testar: Implementar exemplo mínimo
5. Documentar: docs/integrations/{tech}-integration.md
```

### Template: Padrão de Código

```bash
# Quando aprender novo padrão
1. WebSearch("[Pattern Name] React TypeScript examples")
2. Extrair exemplos
3. Criar skill: .claude/skills/patterns/{pattern}/SKILL.md
4. Adicionar ao component-refactor skill
```

### Template: Automação

```bash
# Quando identificar tarefa repetitiva
1. Documentar workflow atual (passos manuais)
2. Decidir: Hook vs Slash Command vs Agent
3. Implementar solução
4. Testar 3x em cenários reais
5. Adicionar à documentação
```

## Checklist de Aplicação

Ao aplicar conhecimento externo:

### Research
- [ ] Documentação oficial consultada
- [ ] Exemplos práticos encontrados (3+)
- [ ] Melhores práticas identificadas
- [ ] Pitfalls conhecidos listados
- [ ] Integrações com stack validadas

### Implementation
- [ ] Tipo de artefato decidido (skill/agent/hook)
- [ ] Frontmatter correto (name, description, allowed-tools)
- [ ] Exemplos práticos incluídos
- [ ] Comandos úteis documentados
- [ ] Referências linkadas

### Validation
- [ ] Testado em cenário real
- [ ] Funciona conforme esperado
- [ ] Não quebra funcionalidades existentes
- [ ] Documentação criada
- [ ] Adicionado ao CLAUDE.md (se relevante)

### Maintenance
- [ ] Data da fonte documentada
- [ ] Versão da tecnologia especificada
- [ ] Plano de atualização definido

## Exemplos de Uso

### Exemplo 1: Integrar Nova Biblioteca UI

```bash
# 1. Research
WebSearch("Radix UI React components documentation 2025")
WebFetch("https://www.radix-ui.com/docs/primitives/overview/introduction",
  "Extract component patterns, accessibility features, integration with Tailwind")

# 2. Synthesize
- Radix UI fornece componentes acessíveis unstyled
- Integra nativamente com Tailwind
- Pattern: Composition over configuration

# 3. Apply
Criar: .claude/skills/radix-ui-integration/SKILL.md
Conteúdo:
  - Quando usar Radix vs componente custom
  - Como compor com Tailwind
  - Exemplos: Dropdown, Dialog, Tooltip
  - Acessibilidade automática (ARIA)

# 4. Validate
Implementar Dialog component com Radix
Testar acessibilidade (screen reader)
Validar integração Tailwind

# 5. Document
docs/integrations/radix-ui-integration.md
```

### Exemplo 2: Atualizar Padrão React

```bash
# 1. Research
WebSearch("React 18.3 new features hooks patterns 2025")
WebFetch("https://react.dev/blog", "Extract new patterns, deprecations")

# 2. Synthesize
- useTransition para UI não-bloqueante
- Automatic batching habilitado
- Concurrent features estáveis

# 3. Apply
Atualizar: .claude/skills/component-refactor/SKILL.md
Adicionar seção: "React 18.3 Patterns"
  - useTransition para filtros
  - useDeferredValue para buscas
  - Automatic batching (sem mudanças necessárias)

# 4. Validate
Refatorar SearchBar com useTransition
Medir performance (antes/depois)

# 5. Document
Atualizar CLAUDE.md seção "React Patterns"
```

### Exemplo 3: Criar Agent de Migração

```bash
# 1. Research (contexto interno)
Grep: Encontrar todos os *LearningSystem.jsx
Read: Analisar estrutura comum
Identificar: 800 linhas duplicadas

# 2. Synthesize
Pattern: Template Method
Solution: BaseLearningSystem + props

# 3. Apply
Criar: .claude/agents/learning-system-migrator.md
System Prompt:
  - Analisar componente atual
  - Extrair props necessárias
  - Gerar código BaseLearningSystem
  - Validar funcionalidade idêntica
  - Criar testes

# 4. Validate
Executar agent em BashLearningSystem
Comparar output (diff)
Rodar testes

# 5. Document
docs/agents/learning-system-migrator-guide.md
```

## Métricas de Sucesso

| Métrica | Meta | Como Medir |
|---------|------|------------|
| Tempo de Integração | -50% | Antes vs Depois desta skill |
| Qualidade do Código | Seguir padrões oficiais | Lint + Review |
| Documentação | 100% das integrações | docs/integrations/ |
| Reutilização | 3+ usos por skill | Logs de ativação |
| Manutenção | Atualizar <2h por tech | Tracking tempo |

## Evolução Contínua

Esta meta-skill deve ser atualizada quando:

- Anthropic lança nova feature (skills/agents/hooks)
- Novo padrão emerge na comunidade
- Feedback de uso identificar gap
- Tecnologia no stack evolui significativamente

**Processo de Atualização:**

1. Identificar mudança
2. Pesquisar nova documentação
3. Atualizar este SKILL.md
4. Aplicar em skills existentes
5. Validar retrocompatibilidade

## Comandos de Manutenção

```bash
# Listar todas as skills
ls -la .claude/skills/

# Ver última atualização de skill
stat -c '%y %n' .claude/skills/*/SKILL.md

# Buscar skills que referenciam tecnologia
grep -r "tecnologia-nome" .claude/skills/

# Validar frontmatter de todas skills
for skill in .claude/skills/*/SKILL.md; do
  echo "Checking $skill"
  head -5 "$skill" | grep -E "^(name|description|allowed-tools):"
done

# Contar linhas de todas as skills
wc -l .claude/skills/*/SKILL.md

# Encontrar skills órfãs (não usadas em 30 dias)
find .claude/skills/ -name "SKILL.md" -mtime +30
```

## Referências Meta

- **Anthropic Docs**: https://docs.claude.com/en/docs/claude-code
- **Hooks Guide**: https://code.claude.com/docs/en/hooks-guide
- **Skills Best Practices**: Community patterns
- **Agent Patterns**: alexop.dev full-stack guide

## Ativação Automática

Esta skill ativa quando você:
- Pesquisa documentação oficial
- Integra nova tecnologia
- Cria skills/agents/hooks
- Atualiza configurações do projeto
- Aplica conhecimento externo ao Ultrathink
- Automatiza processos recorrentes
- Evolui arquitetura do sistema
