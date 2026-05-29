---
name: Pesquisa
description: Fase 1 - Research Protocol. Busca autonoma no codebase, consulta MCPs, mapeia arquivos e gera PRD.md. Aplica S.A.I.S (Solicitar + Analisar) e S.D.A inicial. NUNCA pergunta onde estao arquivos, sempre busca automaticamente.
---

# FASE 1: PESQUISA (RESEARCH PROTOCOL)

## Objetivo
Entender completamente o contexto da tarefa atraves de busca autonoma, sem perguntas sobre localizacao de arquivos.

---

## REGRA DE OURO: AUTONOMIA TOTAL

### NUNCA PERGUNTE:
- "Onde esta o modulo X?"
- "Em qual pasta fica o controller Y?"
- "Pode me mostrar a estrutura de Z?"
- "Qual arquivo contem a funcao W?"

### SEMPRE BUSQUE:
```bash
# Mapear estrutura geral
ls -la /home/runner/workspace

# Encontrar arquivos por nome
find . -name "*mataMata*" -type f

# Buscar por conteudo
grep -r "calcularSaldo" controllers/ routes/ services/

# Localizar padroes
grep -rn "app.post.*acerto" routes/

# Listar controllers
ls -la controllers/

# Ver imports de um modulo
grep -n "require\|import" public/js/fluxo-financeiro/core.js
```

---

## PROTOCOLO DE EXECUCAO

### PASSO 1: Compreender Requisito
**Input do usuario:** `[descricao da funcionalidade]`

**Perguntas validas (APENAS NEGOCIO):**
- "Quais regras de negocio especificas?"
- "Isso se aplica a todas as ligas ou e configuravel?"
- "Qual comportamento esperado em caso de erro?"

**Perguntas PROIBIDAS:**
- Localizacao de arquivos
- Estrutura de pastas
- Onde encontrar codigo

### PASSO 2: Mapear Contexto Automaticamente

#### 2.1 Identificar Modulo/Feature
```bash
# Buscar por palavras-chave da funcionalidade
grep -ri "[palavra-chave]" . --include="*.js" --include="*.html" | head -20
```

#### 2.2 Localizar Arquivos Backend
```bash
# Controllers relacionados
find controllers/ -name "*[palavra-chave]*"

# Models envolvidos
find models/ -name "*[palavra-chave]*"

# Routes afetadas
grep -rn "router\." routes/ | grep -i "[palavra-chave]"

# Services externos
find services/ -name "*.js" -exec grep -l "[palavra-chave]" {} \;
```

#### 2.3 Localizar Arquivos Frontend
```bash
# Modulos JS
find public/js -name "*[palavra-chave]*"
find public/participante/js/modules -name "*.js"

# Fragmentos HTML
find public/participante/fronts -name "*.html"

# CSS relacionado
grep -rn "[palavra-chave]" public/css/ public/participante/css/
```

### PASSO 3: Consultar Documentacao (MCP)

#### Quando Usar Context7 MCP
- Frameworks/libs oficiais (Express, Mongoose, Socket.io)
- Documentacao tecnica atualizada

#### Quando Usar Perplexity MCP
- APIs nao-documentadas (API Cartola FC)
- Bibliotecas brasileiras/nicho
- Noticias/eventos recentes

### PASSO 4: Ler Principios do Projeto
```bash
# OBRIGATORIO: Ler CLAUDE.md para contexto geral
cat CLAUDE.md
```

### PASSO 5: Aplicar S.A.I.S (Solicitar + Analisar)

#### 5.1 SOLICITAR arquivos identificados
- Ver arquivos completos (nao apenas snippets)
- Priorizar: Controllers > Routes > Models > Frontend

#### 5.2 ANALISAR linha por linha
- Entender fluxo de dados
- Identificar funcoes principais
- Mapear dependencias entre arquivos
- Verificar padroes de codigo

### PASSO 6: Mapear Dependencias (S.D.A Inicial)
```bash
# Quem importa este arquivo?
grep -r "require.*[nome-arquivo]" . --include="*.js"
grep -r "import.*[nome-arquivo]" . --include="*.js"

# Quais IDs/classes sao usados?
grep -r "#[id-elemento]\|.[classe-css]" . --include="*.html" --include="*.js"
```

---

## GERAR PRD.md

### Estrutura Obrigatoria
```markdown
# PRD - [Nome da Funcionalidade]

**Data:** [data atual]
**Autor:** Claude (Pesquisa Protocol)
**Status:** Draft

---

## Resumo Executivo
[1-2 paragrafos explicando O QUE precisa ser feito e POR QUE]

---

## Contexto e Analise

### Modulos Identificados
- **Backend:**
  - `controllers/[arquivo].js` - [Descricao]
  - `models/[arquivo].js` - [Estrutura de dados]
  - `routes/[arquivo].js` - [Endpoints]

- **Frontend:**
  - `public/js/[modulo]/[arquivo].js` - [Logica cliente]
  - `public/participante/fronts/[arquivo].html` - [Template]

### Dependencias Mapeadas
- [Arquivo A] importa [Arquivo B]
- [Funcao X] e usada por [Arquivo C, D]

### Padroes Existentes
- Similar a: [feature existente]
- Pode reutilizar: [componente/funcao]

---

## Solucao Proposta

### Abordagem Escolhida
[Explicar COMO resolver]

### Arquivos a Criar
1. `[path/novo-arquivo.js]` - [Proposito]

### Arquivos a Modificar
1. `[path/arquivo-existente.js]` - [O que mudar]

### Regras de Negocio
- [Regra 1]: [Descricao]
- [Regra 2]: [Descricao]

---

## Riscos e Consideracoes

### Impactos Previstos
- Positivo: [Beneficio]
- Atencao: [Ponto de cuidado]
- Risco: [Possivel problema]

### Multi-Tenant
- [ ] Validado isolamento liga_id

---

## Testes Necessarios

### Cenarios de Teste
1. [Cenario positivo]
2. [Cenario negativo]
3. [Edge case]

---

## Proximos Passos

1. Validar PRD
2. Gerar Spec: Executar `/spec` com este PRD
3. Implementar: Executar `/code` com Spec gerado

---

**Gerado por:** Pesquisa Protocol v1.0
```

### Onde Salvar
```bash
# Sempre em .claude/docs/
path=".claude/docs/PRD-[nome-tarefa-kebab-case].md"

# Exemplo:
# .claude/docs/PRD-notificacoes-push.md
# .claude/docs/PRD-export-pdf-extrato.md
```

---

## Checklist Final (Antes de Gerar PRD)

### Pesquisa Completa
- [ ] Busquei automaticamente todos os arquivos relacionados
- [ ] Li arquivos principais completamente
- [ ] Mapeei dependencias iniciais
- [ ] Consultei MCPs quando necessario
- [ ] Li CLAUDE.md do projeto

### Solucao Clara
- [ ] Entendi completamente o requisito
- [ ] Proposta baseada em codigo existente
- [ ] Reuso de patterns identificados
- [ ] Riscos mapeados

### PRD Estruturado
- [ ] Todas as secoes preenchidas
- [ ] Listas de arquivos precisas
- [ ] Regras de negocio documentadas
- [ ] Testes planejados

---

## Proxima Acao

```
PRD gerado com sucesso!

LIMPAR CONTEXTO:
1. Feche esta conversa
2. Abra nova conversa
3. Execute: /spec .claude/docs/PRD-[nome].md
```

---

**STATUS:** PESQUISA PROTOCOL - AUTONOMOUS & THOROUGH
**Versao:** 1.0 (High Senior Edition)
