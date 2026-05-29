---
name: learning-path-patterns
scope: domain
target: ultrathink-educational-platform
description: |
  Comprehensive guide to Learning Path patterns for the Ultrathink educational platform. This skill covers the conceptual difference between Study Areas (courses) and Proposed Paths (sequences of courses), data modeling, UI/UX patterns, and implementation guidelines.

  Learn how to structure Learning Paths correctly: a Proposed Path is NOT a container of loose flashcards, but a curated sequence of Study Areas (courses). Each path references existing courses with metadata like order, availability status, and estimated hours.

  Real-world examples are taken from the Hub MVP implementation (US-044), including caminhoExemploData.js, HubView.jsx, and LearningPathView.jsx. The skill demonstrates the reference pattern used for "Desenvolvedor Backend" path that sequences Bash, Linux, Docker, and DevOps courses.

  Key topics include data schema design (cursos array with ordem, areaId, disponivel flags), computed properties (getters for statistics), navigation patterns (path -> course -> lesson), availability states (disponivel: true/false with badges), and how to add new paths without duplicating course data.

  This skill is essential for implementing new Learning Paths, maintaining the Hub MVP pattern, scaling to multiple paths, and ensuring UI/UX consistency across the educational platform. Includes the correct mental model for Course vs Path separation.

keywords: |
  learning-path, trilha, caminho-proposto, area-de-estudo, curso, navegacao,
  hub, educacional, sequencia, cursos, disponibilidade, ordem, mvp,
  composite-pattern, entity-reference, data-modeling

allowed-tools: |
  Read, Write, Edit, Grep, Glob, Bash
---

# Learning Path Patterns

> **Padrao de Trilhas de Aprendizado para Sistema Educacional Corporativo**
>
> **Versao:** 1.0.0
> **Ultima Atualizacao:** 2025-11-22
> **Target:** Hub MVP (US-044)
> **Projeto:** Ultrathink - Plataforma B2B de Treinamento Tecnico

---

## Indice

1. [Overview](#-overview)
2. [Conceito Fundamental: Curso vs Caminho](#-conceito-fundamental-curso-vs-caminho)
3. [Schema de Dados](#-schema-de-dados)
4. [Padroes de UI/UX](#-padroes-de-uiux)
5. [Implementacao de Referencia](#-implementacao-de-referencia)
6. [Como Adicionar Novos Caminhos](#-como-adicionar-novos-caminhos)
7. [Antipadroes a Evitar](#-antipadroes-a-evitar)
8. [Exemplos do Projeto](#-exemplos-do-projeto)
9. [Referencias](#-referencias)

---

## Overview

Esta skill documenta o **padrao correto** para modelar e implementar **Caminhos de Aprendizado** (Learning Paths) no sistema Ultrathink.

**O que voce vai aprender:**
- Diferenca entre Area de Estudo (curso) e Caminho Proposto (trilha)
- Como estruturar dados para caminhos escalavel
- Padroes de UI para mostrar disponibilidade de cursos
- Navegacao correta: Hub -> Caminho -> Curso -> Aula
- Como adicionar novos caminhos sem duplicar dados

**Por que esta skill e importante:**
- **Clareza conceitual:** Evita confusao entre curso e trilha
- **Escalabilidade:** Mesmo curso pode estar em multiplos caminhos
- **Manutencao:** Atualizar curso atualiza todas as trilhas
- **UX consistente:** Usuario entende hierarquia intuitivamente
- **MVP focus:** Mostra apenas conteudo padronizado

**Contexto da US-044:**
O Hub anterior mostrava 13 areas + flashcards soltos em "Caminhos".
A US-044 simplificou para MVP: 1 Area (Bash) + 1 Caminho correto (sequencia de cursos).

---

## Conceito Fundamental: Curso vs Caminho

### ERRADO (antes da US-044)

```
Caminho de Aprendizado = Container de Flashcards
  - Flashcard 1: "O que e variavel?"
  - Flashcard 2: "Sintaxe de loop"
  - ...

Problema: Mistura conceitos, nao referencia cursos reais
```

### CORRETO (depois da US-044)

```
Area de Estudo (Curso):
  - Entidade autocontida
  - Tem: video, modulos, notas, flashcards
  - Exemplo: Bash, C, Rust

Caminho Proposto (Trilha):
  - Sequencia ordenada de CURSOS
  - Referencia Areas de Estudo existentes (ou planejadas)
  - Exemplo: "Desenvolvedor Backend" = Bash -> Linux -> Docker -> DevOps
```

### Analogia do Design Pattern

**Composite vs Entity Reference:**

```
Entity (Area de Estudo):
{
  id: "bash",
  name: "Bash Shell Scripting",
  modules: 16,
  hours: 32,
  flashcards: [...],     // Dados REAIS aqui
  sections: [...]        // Conteudo REAL aqui
}

Composite (Caminho Proposto):
{
  id: "backend-developer",
  name: "Desenvolvedor Backend",
  cursos: [
    { areaId: "bash", ordem: 1, disponivel: true },   // REFERENCIA
    { areaId: "linux", ordem: 2, disponivel: false }, // REFERENCIA
    { areaId: "docker", ordem: 3, disponivel: false } // REFERENCIA
  ]
}
```

**Beneficio:** Se `bash` for atualizado (mais modulos, novos flashcards), TODOS os caminhos que referenciam `bash` refletem automaticamente.

---

## Schema de Dados

### Schema de Caminho Proposto (caminhoExemploData.js)

```javascript
export const caminhoExemplo = {
  // Identificacao
  id: 'backend-developer',
  name: 'Desenvolvedor Backend',
  icon: 'trilha',
  description: 'Caminho proposto para dominar desenvolvimento backend...',
  badge: 'exemplo',  // 'exemplo' | 'popular' | 'novo' | null

  // Sequencia ordenada de cursos (REFERENCIAS, nao dados duplicados)
  cursos: [
    {
      ordem: 1,                      // Posicao na sequencia
      areaId: 'bash',               // Referencia a studyAreas.js
      nome: 'Bash Shell Scripting', // Display name (pode ser diferente)
      icone: 'terminal',
      descricao: 'Fundamentos de linha de comando...',
      modules: 16,                   // Estatisticas (sync com Area)
      hours: 32,
      disponivel: true,              // Clicavel ou nao
      destaque: 'Padrao de referencia' // Badge especial (opcional)
    },
    {
      ordem: 2,
      areaId: 'linux',
      nome: 'Linux Fundamentals',
      icone: 'linux',
      descricao: 'Sistema operacional, administracao...',
      modules: 12,
      hours: 24,
      disponivel: false,             // "Em breve" badge
      destaque: null
    }
    // ... mais cursos
  ],

  // Estatisticas calculadas (getters)
  get totalCursos() { return this.cursos.length; },
  get cursosDisponiveis() { return this.cursos.filter(c => c.disponivel).length; },
  get totalModules() { return this.cursos.reduce((sum, c) => sum + c.modules, 0); },
  get totalHours() { return this.cursos.reduce((sum, c) => sum + c.hours, 0); },
  get modulesDisponiveis() {
    return this.cursos.filter(c => c.disponivel).reduce((sum, c) => sum + c.modules, 0);
  },
  get hoursDisponiveis() {
    return this.cursos.filter(c => c.disponivel).reduce((sum, c) => sum + c.hours, 0);
  }
};

// Exportar dicionario de caminhos
export const caminhosPropostos = {
  'backend-developer': caminhoExemplo
};
```

### Schema de Area de Estudo (studyAreas.js)

```javascript
export const studyAreas = [
  {
    name: "Bash",
    icon: "terminal",
    description: "Shell scripting, automacao e linha de comando",
    modules: 16,
    hours: 32,
    badge: "Integrado",        // Status do sistema integrado
    hasIntegratedApp: true,    // Tem LearningSystem dedicado
    key: "bash",               // ID para navegacao
    flashcards: [...]          // Flashcards REAIS
  }
];
```

**Regra de Ouro:**
- `studyAreas.js` contem dados REAIS (flashcards, metricas)
- `caminhoExemploData.js` contem REFERENCIAS + metadados de ordenacao

---

## Padroes de UI/UX

### Padrao 1: Card de Caminho no Hub

```jsx
// HubView.jsx - Secao de Caminhos Propostos
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {Object.values(caminhosPropostos).map(caminho => (
    <div
      key={caminho.id}
      onClick={() => openLearningPath(caminho.id)}
      className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-xl p-6
                 shadow-lg hover:shadow-xl cursor-pointer transition-all"
    >
      <div className="flex items-center gap-3 mb-3">
        <span className="text-2xl">{caminho.icon}</span>
        <h3 className="text-lg font-bold text-slate-800">{caminho.name}</h3>
        {caminho.badge && (
          <span className="px-2 py-0.5 bg-purple-100 text-purple-600
                          text-xs rounded-full">{caminho.badge}</span>
        )}
      </div>
      <p className="text-slate-600 text-sm mb-4">{caminho.description}</p>

      {/* Estatisticas */}
      <div className="flex gap-4 text-sm text-slate-500">
        <span>{caminho.totalCursos} cursos</span>
        <span>{caminho.totalModules} modulos</span>
        <span>{caminho.totalHours}h</span>
      </div>
    </div>
  ))}
</div>
```

### Padrao 2: Lista de Cursos no LearningPathView

```jsx
// LearningPathView.jsx - Mostrar sequencia de cursos
<div className="space-y-4">
  {path.cursos.map((curso, index) => (
    <div
      key={curso.areaId}
      onClick={() => curso.disponivel && navigateToCourse(curso.areaId)}
      className={`
        flex items-center gap-4 p-4 rounded-lg border-2 transition-all
        ${curso.disponivel
          ? 'border-green-200 bg-green-50 hover:border-green-400 cursor-pointer'
          : 'border-slate-200 bg-slate-50 cursor-not-allowed opacity-60'}
      `}
    >
      {/* Numero da ordem */}
      <div className={`
        w-8 h-8 rounded-full flex items-center justify-center font-bold
        ${curso.disponivel ? 'bg-green-500 text-white' : 'bg-slate-300 text-slate-600'}
      `}>
        {curso.ordem}
      </div>

      {/* Info do curso */}
      <div className="flex-1">
        <div className="flex items-center gap-2">
          <span>{curso.icone}</span>
          <span className="font-medium">{curso.nome}</span>

          {/* Badge de disponibilidade */}
          {curso.disponivel ? (
            <span className="px-2 py-0.5 bg-green-100 text-green-700
                            text-xs rounded-full">Disponivel</span>
          ) : (
            <span className="px-2 py-0.5 bg-slate-100 text-slate-500
                            text-xs rounded-full">Em breve</span>
          )}

          {/* Destaque especial */}
          {curso.destaque && (
            <span className="px-2 py-0.5 bg-purple-100 text-purple-600
                            text-xs rounded-full">{curso.destaque}</span>
          )}
        </div>
        <p className="text-sm text-slate-600 mt-1">{curso.descricao}</p>
      </div>

      {/* Metricas */}
      <div className="text-right text-sm text-slate-500">
        <div>{curso.modules} modulos</div>
        <div>{curso.hours}h</div>
      </div>

      {/* Seta se disponivel */}
      {curso.disponivel && (
        <ChevronRight className="w-5 h-5 text-green-500" />
      )}
    </div>
  ))}
</div>
```

### Padrao 3: Navegacao do Breadcrumb

```
Hub > Caminho: Desenvolvedor Backend
Hub > Caminho: Desenvolvedor Backend > Bash (curso)
Hub > Caminho: Desenvolvedor Backend > Bash > Aula 1.1
```

**Implementacao:**
```jsx
// Breadcrumb para LearningPathView
<nav className="flex items-center gap-2 text-sm text-slate-600 mb-6">
  <button onClick={() => setCurrentView('hub')} className="hover:text-purple-600">
    Hub
  </button>
  <ChevronRight className="w-4 h-4" />
  <span className="text-slate-800 font-medium">
    Caminho: {path.name}
  </span>
</nav>
```

---

## Implementacao de Referencia

### Arquivo: src/data/caminhoExemploData.js

```javascript
/**
 * Caminho de Aprendizado Exemplo
 *
 * Este arquivo define o modelo correto para "Caminhos Propostos".
 *
 * CONCEITO:
 * - Caminho Proposto = sequencia ordenada de CURSOS (Areas de Estudo)
 * - NAO e um container de flashcards soltos
 * - Cada curso referencia uma Area de Estudo existente (ou planejada)
 * - Cursos tem ordem, disponibilidade e sao clicaveis quando disponiveis
 *
 * PADRAO:
 * - Baseado no modelo Bash (bashLearningData.js) que e a referencia
 * - Cada curso tem: ordem, areaId, nome, descricao, modules, hours, disponivel
 *
 * @see docs/backlog/ROADMAP.md - US-044
 */

export const caminhoExemplo = {
  id: 'backend-developer',
  name: 'Desenvolvedor Backend',
  icon: 'trilha',
  description: 'Caminho proposto para dominar desenvolvimento backend...',
  badge: 'exemplo',

  cursos: [
    {
      ordem: 1,
      areaId: 'bash',
      nome: 'Bash Shell Scripting',
      icone: 'terminal',
      descricao: 'Fundamentos de linha de comando, automacao e scripting robusto',
      modules: 16,
      hours: 32,
      disponivel: true,
      destaque: 'Padrao de referencia'
    },
    // ... mais cursos
  ],

  // Getters para estatisticas
  get totalCursos() { return this.cursos.length; },
  get cursosDisponiveis() { return this.cursos.filter(c => c.disponivel).length; },
  get totalModules() { return this.cursos.reduce((sum, c) => sum + c.modules, 0); },
  get totalHours() { return this.cursos.reduce((sum, c) => sum + c.hours, 0); }
};

export const caminhosPropostos = {
  'backend-developer': caminhoExemplo
};

export default caminhoExemplo;
```

### Arquivo: src/components/LearningPathView.jsx (Essencia)

```jsx
import { caminhosPropostos } from '../data/caminhoExemploData';

export function LearningPathView({ pathId, onBack, onCourseClick }) {
  const path = caminhosPropostos[pathId];

  if (!path) {
    return <div>Caminho nao encontrado</div>;
  }

  const handleCourseClick = (curso) => {
    if (curso.disponivel) {
      onCourseClick(curso.areaId);  // Navega para /curso/:areaId
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* Breadcrumb */}
      <nav>Hub > Caminho: {path.name}</nav>

      {/* Header */}
      <h1>{path.icon} {path.name}</h1>
      <p>{path.description}</p>

      {/* Stats */}
      <div>
        {path.cursosDisponiveis}/{path.totalCursos} cursos disponiveis |
        {path.modulesDisponiveis}/{path.totalModules} modulos |
        {path.hoursDisponiveis}h/{path.totalHours}h
      </div>

      {/* Lista de cursos */}
      {path.cursos.map(curso => (
        <CursoCard
          key={curso.areaId}
          curso={curso}
          onClick={() => handleCourseClick(curso)}
        />
      ))}
    </div>
  );
}
```

---

## Como Adicionar Novos Caminhos

### Passo 1: Definir o Caminho no caminhoExemploData.js

```javascript
export const caminhoFrontend = {
  id: 'frontend-developer',
  name: 'Desenvolvedor Frontend',
  icon: 'frontend',
  description: 'Domine as tecnologias do frontend moderno',
  badge: 'novo',

  cursos: [
    { ordem: 1, areaId: 'html-css', nome: 'HTML & CSS', disponivel: false, ... },
    { ordem: 2, areaId: 'javascript', nome: 'JavaScript', disponivel: false, ... },
    { ordem: 3, areaId: 'react', nome: 'React', disponivel: false, ... },
    { ordem: 4, areaId: 'vscode', nome: 'VSCode & Ferramentas', disponivel: true, ... }
  ],

  get totalCursos() { return this.cursos.length; },
  // ... outros getters
};

// Adicionar ao dicionario
export const caminhosPropostos = {
  'backend-developer': caminhoExemplo,
  'frontend-developer': caminhoFrontend  // NOVO
};
```

### Passo 2: Criar Areas de Estudo referenciadas (se nao existirem)

Se `html-css` nao existe em `studyAreas.js`, adicionar:

```javascript
// studyAreas.js
{
  name: "HTML & CSS",
  icon: "html",
  description: "Fundamentos da web",
  modules: 10,
  hours: 20,
  badge: null,             // Nao tem sistema integrado ainda
  hasIntegratedApp: false,
  key: "html-css",
  flashcards: []
}
```

### Passo 3: (Opcional) Criar LearningSystem para cursos disponiveis

Se quiser habilitar navegacao para o curso, criar:
- `HtmlCssLearningSystem.jsx`
- `htmlCssLearningData.js`

E marcar `disponivel: true` no caminho.

---

## Antipadroes a Evitar

### 1. Duplicar Dados de Curso no Caminho

**ERRADO:**
```javascript
cursos: [
  {
    areaId: 'bash',
    flashcards: [  // DUPLICADO!
      { front: "...", back: "..." }
    ],
    sections: [...]  // DUPLICADO!
  }
]
```

**CORRETO:**
```javascript
cursos: [
  {
    areaId: 'bash',  // REFERENCIA - flashcards estao em studyAreas.js
    modules: 16,     // Apenas metadados de exibicao
    hours: 32
  }
]
```

### 2. Misturar Flashcards Soltos no Caminho

**ERRADO:**
```javascript
caminhoBackend = {
  name: "Backend",
  flashcards: [  // Flashcards NAO pertencem a caminho!
    { front: "O que e REST?", back: "..." }
  ]
}
```

**CORRETO:**
```javascript
// Flashcards pertencem a CURSOS (studyAreas.js)
caminhoBackend = {
  name: "Backend",
  cursos: [
    { areaId: 'api-rest', ... }  // API REST tem seus proprios flashcards
  ]
}
```

### 3. Hardcoded Availability

**ERRADO:**
```jsx
// Verificar se curso esta disponivel via logica complexa
{studyAreas.find(a => a.key === curso.areaId)?.hasIntegratedApp && (
  <button>Acessar</button>
)}
```

**CORRETO:**
```javascript
// Declarativo no schema
{ areaId: 'bash', disponivel: true }  // Explicito

// No componente, simples:
{curso.disponivel && <button>Acessar</button>}
```

### 4. Ordem Implicita via Array Index

**ERRADO:**
```javascript
cursos: ['bash', 'linux', 'docker']  // Ordem implicita, fragil
```

**CORRETO:**
```javascript
cursos: [
  { ordem: 1, areaId: 'bash' },
  { ordem: 2, areaId: 'linux' },
  { ordem: 3, areaId: 'docker' }
]
```

---

## Exemplos do Projeto

### Arquivo Real: src/data/caminhoExemploData.js

**Localizacao:** `src/data/caminhoExemploData.js:1-109`

Este arquivo e o modelo de referencia implementado na US-044.

### Arquivo Real: src/components/LearningPathView.jsx

**Localizacao:** `src/components/LearningPathView.jsx`

Renderiza a lista de cursos do caminho com estados de disponibilidade.

### Arquivo Real: src/components/HubView.jsx

**Localizacao:** `src/components/HubView.jsx`

Mostra cards de Caminhos Propostos e Areas de Estudo.

### Navegacao Implementada

```
Rota           | Componente         | Props
---------------|-------------------|------------------------
/              | HubView            | studyAreas, caminhosPropostos
/trilha/:id    | LearningPathView   | pathId, onCourseClick
/curso/:id     | *LearningSystem    | courseId
/curso/:id/aula/:aulaId | *NotesView | moduleId
```

---

## Referencias

### Skills Relacionadas

- **[ultrathink-arch](../ultrathink-arch/SKILL.md)** - Arquitetura geral do sistema
- **[ux-nomenclature](../ux-nomenclature/SKILL.md)** - Glossario de termos (Caminho vs Trilha)
- **[component-refactor](../component-refactor/SKILL.md)** - Refatoracao de componentes

### Documentacao Tecnica

- **[ROADMAP.md](../../docs/backlog/ROADMAP.md)** - US-044 (Hub MVP Simplificado)
- **[docs/tecnico/architecture/](../../docs/tecnico/architecture/)** - Arquitetura detalhada

### Codigo Real do Projeto

**Implementacao de Referencia (US-044):**
- `src/data/caminhoExemploData.js:1-109` - Schema de caminho
- `src/data/studyAreas.js` - Areas de estudo (MVP: apenas Bash)
- `src/components/HubView.jsx` - Hub com caminhos
- `src/components/LearningPathView.jsx` - Lista de cursos do caminho
- `src/components/SistemaEducacionalCompleto.jsx` - Integracao

---

**Voce esta em:** `.claude/skills/learning-path-patterns/SKILL.md`
**Criado em:** 2025-11-22
**Mantido por:** Joao Pelegrino + Claude Code
**Uso:** Referencia para implementar e escalar Caminhos de Aprendizado
**Ultima auditoria:** 2025-11-22
**Desbloqueia:** Novos caminhos, escala do Hub, consistencia UX
