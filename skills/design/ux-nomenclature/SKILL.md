---
name: ux-nomenclature
description: Garante nomenclatura consistente seguindo o glossário do ÉPICO 12 (Arquitetura de Informação do Ultrathink)
allowed-tools: [Read, Edit, Grep]
---

# UX Nomenclature Skill - Ultrathink

## Objetivo

Esta skill ativa automaticamente quando você está trabalhando com nomenclatura de UI/UX no Ultrathink, garantindo **consistência absoluta** com o glossário definido no PRODUCT-CENTRAL-DOCUMENT.md (ÉPICO 12).

## Glossário Obrigatório

### ❌ Termos PROIBIDOS (Antigos)

- "Sistema de Aprendizado" → USE: **"Curso"**
- "Notas Rápidas" → USE: **"Meu Caderno de Notas"**
- "Módulo" → USE: **"Aula"**
- "FASE" → USE: **"Seção"**
- "Ver Notas" → USE: **"📖 Estudar"**
- "Notas de Aprendizado" → USE: **"Aula [número]: [título]"**
- "Conteúdo do Tópico" → USE: **"Subtópicos da Aula"**
- "Cronograma" (em contexto) → USE: **"Curso"**
- "Flash Cards [Tech]" (seção) → USE: **"Praticar com Flash Cards"**

### ✅ Hierarquia de Nomenclatura

```
NÍVEL 1: Hub de Aprendizado (sem mudanças)
NÍVEL 2: Curso de [Tecnologia]
  ├── Vídeo Principal do Curso
  ├── 📒 Meu Caderno de Notas
  └── Estrutura do Curso
      ├── Seção 1: [Nome]
      └── Seção 2: [Nome]
          └── Aula [número]: [Título]

NÍVEL 3: Aula [número]: [Título]
  ├── Subtópicos da Aula
  ├── Resumo do Conteúdo
  └── 💡 Praticar com Flash Cards

NÍVEL 4: Praticando: [Tecnologia] - [Seção]
```

### ✅ Botões de Navegação Padronizados

- Nível 2 → Nível 1: `← Voltar ao Hub`
- Nível 3 → Nível 2: `← Voltar ao Curso`
- Nível 4 → Nível 3: `✕ Fechar` (modal)

**Padrão:** SEMPRE usar `← Voltar ao [Nível Pai]`

### ✅ Placeholders e Textos de Ajuda

- Meu Caderno de Notas: `"Minhas anotações pessoais sobre [tecnologia]..."`
- Flash Cards: `"Revise os [conceitos/fundamentos/tópicos avançados]"`
- Contador de Cards: `"Card 1 de X"` (não "Cartão")

## Regras de Aplicação

### Ao Criar/Editar Componentes React:

1. **Sempre verificar** se nomenclatura está no glossário
2. **Substituir imediatamente** termos antigos por novos
3. **Alertar** se encontrar terminologia inconsistente
4. **Sugerir** nomenclatura correta baseada no contexto

### Ao Revisar Pull Requests:

1. **Bloquear** se usar termos proibidos
2. **Validar** que botões seguem padrão de navegação
3. **Confirmar** que breadcrumb usa formato correto

### Ao Gerar Código:

```jsx
// ❌ ERRADO
<h1>Sistema de Aprendizado Bash</h1>
<button>Ver Notas</button>
<h3>Notas Rápidas</h3>

// ✅ CORRETO
<h1>Curso de Bash Shell Scripting</h1>
<button>📖 Estudar</button>
<h3>📒 Meu Caderno de Notas</h3>
```

## Sistemas Afetados

Esta nomenclatura aplica-se a **TODOS** os 5 sistemas integrados:

- `BashLearningSystem.jsx` / `BashNotesView.jsx`
- `CLearningSystem.jsx` / `CNotesView.jsx`
- `RustLearningSystem.jsx` / `RustNotesView.jsx`
- `VSCodeLearningSystem.jsx` / `VSCodeNotesView.jsx`
- `ClaudeCodeLearningSystem.jsx` / `ClaudeCodeNotesView.jsx`

## Arquivos de Dados

Também validar nomenclatura em:

- `src/data/bashLearningData.js`
- `src/data/cLearningData.js`
- `src/data/rustLearningData.js`
- `src/data/vscodeLearningData.js`
- `src/data/claudeCodeLearningData.js`
- `src/data/studyAreas.js`

## Comandos Úteis

```bash
# Encontrar usos de termos antigos
grep -r "Sistema de Aprendizado" src/
grep -r "Ver Notas" src/
grep -r "Notas Rápidas" src/
grep -r "FASE [0-9]" src/

# Validar nomenclatura consistente
grep -r "Curso de" src/components/
grep -r "Meu Caderno de Notas" src/components/
grep -r "Estudar" src/components/
```

## Ativação Automática

Esta skill ativa quando você:
- Edita componentes React (*.jsx)
- Modifica arquivos de dados (*.js em src/data/)
- Refatora nomenclatura de UI
- Implementa US-060, US-061, US-062, US-063
- Trabalha com breadcrumb ou navegação
- Revisa código de sistemas de aprendizado

## Referências

- **PRODUCT-CENTRAL-DOCUMENT.md**: ÉPICO 12 (linhas 877-1373)
- **User Stories**: US-060 (Refatorar Nomenclatura), US-063 (Unificar Conceito de Notas)
- **Glossário Completo**: Tabela com 9 termos (linha 994-1006)
