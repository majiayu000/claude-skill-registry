---
name: platform-architecture
description: Conhecimento completo da arquitetura, padrões de código, estrutura de dados e convenções do sistema educacional Plataforma B2B de treinamento técnico corporativo
allowed-tools: [Read, Grep, Glob]
---

# Plataforma B2B de treinamento técnico corporativo Architecture Skill

## Objetivo

Esta skill ativa automaticamente para fornecer **conhecimento profundo** sobre a arquitetura do Plataforma B2B de treinamento técnico corporativo, ajudando em:

- Decisões arquiteturais consistentes
- Navegação rápida no código
- Entendimento de fluxos de dados
- Manutenção de padrões estabelecidos

## Arquitetura Geral

### Stack Tecnológica

```yaml
Frontend:
  Framework: React 18.3.1
  Build: Vite 5.4.19 (startup 295ms)
  Styling: Tailwind CSS 3.4.1
  Icons: Lucide React 0.344.0
  Markdown: React Markdown 10.1.0

Testing:
  Unit: Vitest 3.2.4 + Testing Library 16.3.0
  E2E: Playwright 1.56.1
  Coverage: ~5% (meta: 80%)

DevOps:
  Container: Docker + Nginx Alpine
  CI/CD: GitHub Actions
  MCP: Chrome DevTools + Playwright

Metrics:
  Components: 17
  Lines of Code: ~5.500
  Modules: 227 (50 C + 24 Rust + 16 Bash + 8 VSCode + 12 Claude Code + 117 outros)
  Flash Cards: 39
  Hours Content: 692h
```

### Estrutura de Diretórios

```
app-controle/
├── src/
│   ├── components/           # 17 componentes React
│   │   ├── SistemaEducacionalCompleto.jsx  # Root component
│   │   ├── HubView.jsx                     # Nível 1: Hub
│   │   ├── LearningPathView.jsx            # Caminhos de aprendizado
│   │   ├── FlashcardModal.jsx              # Modal 3D cards
│   │   │
│   │   ├── *LearningSystem.jsx (5x)        # Nível 2: Cursos
│   │   │   ├── BashLearningSystem.jsx
│   │   │   ├── CLearningSystem.jsx
│   │   │   ├── RustLearningSystem.jsx
│   │   │   ├── VSCodeLearningSystem.jsx
│   │   │   └── ClaudeCodeLearningSystem.jsx
│   │   │
│   │   ├── *NotesView.jsx (5x)             # Nível 3: Aulas
│   │   │   ├── BashNotesView.jsx
│   │   │   ├── CNotesView.jsx
│   │   │   ├── RustNotesView.jsx
│   │   │   ├── VSCodeNotesView.jsx
│   │   │   └── ClaudeCodeNotesView.jsx
│   │   │
│   │   └── shared/                         # Componentes reutilizáveis
│   │       ├── AreaCard.jsx
│   │       ├── CodeBlock.jsx
│   │       ├── ErrorBoundary.jsx
│   │       └── (Breadcrumb.jsx - futuro)
│   │
│   ├── data/                 # Dados estruturados (fonte da verdade)
│   │   ├── studyAreas.js                   # 13 áreas de estudo (MVP: apenas Bash ativo)
│   │   ├── caminhoExemploData.js           # Caminhos Propostos (trilhas de cursos)
│   │   ├── cLearningData.js                # 50 módulos C
│   │   ├── rustLearningData.js             # 24 módulos Rust
│   │   ├── bashLearningData.js             # 16 módulos Bash
│   │   ├── vscodeLearningData.js           # 8 módulos VSCode
│   │   └── claudeCodeLearningData.js       # 12 módulos Claude Code
│   │
│   ├── hooks/                # Hooks customizados (futuro)
│   │   ├── useAutoSaveNotes.js
│   │   ├── useModuleProgress.js
│   │   └── useLocalStorage.js
│   │
│   ├── utils/                # Utilitários
│   │   ├── helpers.js
│   │   └── debugLogger.js
│   │
│   └── tests/                # Testes automatizados
│       ├── setup.js
│       └── components/
│           └── AreaCard.test.jsx
│
├── .claude/                  # Configuração Claude Code
│   ├── commands/             # Slash commands
│   │   ├── test.md
│   │   ├── deploy.md
│   │   └── fix.md
│   ├── skills/               # Skills especializadas
│   │   ├── ux-nomenclature/
│   │   ├── component-refactor/
│   │   ├── breadcrumb-impl/
│   │   ├── platform-architecture/
│   │   ├── localStorage-patterns/
│   │   └── learning-path-patterns/
│   ├── agents/               # Agents especializados
│   ├── hooks.toml            # Hooks de automação
│   └── settings.local.json   # Configurações
│
├── screenshots/              # Evidências visuais
├── docs/                     # Documentação técnica
├── dist/                     # Build de produção
├── .mcp.json                 # MCP servers
├── docker-compose.yml
├── Dockerfile
├── nginx.conf
├── vite.config.js
└── PRODUCT-CENTRAL-DOCUMENT.md  # PRD + Backlog
```

## Hierarquia de Navegação (4 Níveis)

```
NÍVEL 1: Hub de Aprendizado
├── Estatísticas: 13 áreas, 39 cards, 227 módulos, 692h
├── Seção: Caminhos Propostos (1 caminho Rust)
└── Seção: Áreas de Estudo (13 cards)
    │
    └── Card "Bash" (clique)
        │
        NÍVEL 2: Curso de Bash Shell Scripting
        ├── Breadcrumb: Hub > Curso de Bash
        ├── Vídeo Principal (YouTube embed)
        ├── 📒 Meu Caderno de Notas (textarea + auto-save)
        └── Estrutura do Curso
            ├── Seção 1: Fundamentos (4 aulas)
            ├── Seção 2: Processamento (4 aulas)
            ├── Seção 3: Recursos Avançados (4 aulas)
            └── Seção 4: Ferramentas (4 aulas)
                │
                └── Aula 1.1 (clique em "📖 Estudar")
                    │
                    NÍVEL 3: Aula 1.1: Introdução ao Shell Scripting
                    ├── Breadcrumb: Hub > Bash > Aula 1.1
                    ├── Subtópicos da Aula (botões expandíveis)
                    ├── Resumo do Conteúdo (markdown)
                    └── 💡 Praticar com Flash Cards
                        │
                        └── (clique em "Começar Prática")
                            │
                            NÍVEL 4: Modal Flash Cards
                            ├── Breadcrumb: Hub > Bash > Praticando
                            ├── Card 3D (frente/verso)
                            ├── Navegação (anterior/próximo)
                            └── Contador (1/2)
```

## Modelo de Caminhos Propostos (US-044)

### Conceito Fundamental

**Area de Estudo (Curso):** Entidade autocontida com video, modulos, notas, flashcards.
**Caminho Proposto (Trilha):** Sequencia ordenada de CURSOS (referencias, nao dados duplicados).

```
Exemplo: "Desenvolvedor Backend"
  1. Bash Shell Scripting (disponivel)
  2. Linux Fundamentals (em breve)
  3. Docker & Containers (em breve)
  4. DevOps Essentials (em breve)
```

### Schema de Caminho (caminhoExemploData.js)

```javascript
export const caminhoExemplo = {
  id: 'backend-developer',
  name: 'Desenvolvedor Backend',
  icon: 'trilha',
  description: 'Caminho para dominar desenvolvimento backend',
  badge: 'exemplo',

  cursos: [
    {
      ordem: 1,
      areaId: 'bash',       // Referencia a studyAreas.js
      nome: 'Bash Shell Scripting',
      modules: 16,
      hours: 32,
      disponivel: true,     // Clicavel
      destaque: 'Padrao de referencia'
    },
    // ... mais cursos
  ],

  // Getters computados
  get totalCursos() { return this.cursos.length; },
  get cursosDisponiveis() { return this.cursos.filter(c => c.disponivel).length; }
};

export const caminhosPropostos = {
  'backend-developer': caminhoExemplo
};
```

### Navegacao de Caminhos

```
Hub (/)
  |-- Clica em Caminho "Desenvolvedor Backend"
  v
LearningPathView (/trilha/backend-developer)
  |-- Lista cursos na ordem
  |-- Cursos disponiveis: clicaveis (badge verde)
  |-- Cursos indisponiveis: desabilitados (badge "Em breve")
  |-- Clica em "Bash" (disponivel)
  v
BashLearningSystem (/curso/bash)
```

### Skill Relacionada

Para detalhes completos sobre Caminhos de Aprendizado, consulte:
**.claude/skills/learning-path-patterns/SKILL.md**

---

## Fluxo de Dados

### Estado Global (SistemaEducacionalCompleto.jsx)

```jsx
const [currentView, setCurrentView] = useState('hub')
// Valores possíveis:
// - 'hub'                    → HubView
// - 'learning-path'          → LearningPathView
// - 'bash'                   → BashLearningSystem
// - 'c'                      → CLearningSystem
// - 'rust'                   → RustLearningSystem
// - 'vscode'                 → VSCodeLearningSystem
// - 'claude-code'            → ClaudeCodeLearningSystem

const [selectedArea, setSelectedArea] = useState(null)
const [selectedPath, setSelectedPath] = useState(null)
const [selectedModule, setSelectedModule] = useState(null)
```

### LocalStorage Keys

```javascript
// Notas do usuário (editáveis)
'bash-learning-notes'
'c-learning-notes'
'rust-learning-notes'
'vscode-learning-notes'
'claude-code-learning-notes'

// Progresso de módulos (futuro - US-042)
'bash-progress'          // JSON: ["1.1", "1.2", ...]
'c-progress'
'rust-progress'
'vscode-progress'
'claude-code-progress'
```

### Props Drilling Pattern

```jsx
// HubView → SistemaEducacional
<HubView
  studyAreas={studyAreas}
  onAreaClick={(area) => setCurrentView(area.key)}
  onPathClick={(path) => {
    setSelectedPath(path)
    setCurrentView('learning-path')
  }}
/>

// BashLearningSystem → SistemaEducacional
<BashLearningSystem
  onBack={() => setCurrentView('hub')}
  onModuleClick={(module) => {
    setSelectedModule(module)
    setCurrentView('bash-notes')
  }}
/>

// BashNotesView → SistemaEducacional
<BashNotesView
  module={selectedModule}
  onBack={() => setCurrentView('bash')}
  onBackToHub={() => setCurrentView('hub')}
/>
```

## Padrões de Código

### Convenções de Nomenclatura

```javascript
// Componentes: PascalCase
HubView, BashLearningSystem, FlashcardModal

// Arquivos: camelCase
cLearningData.js, studyAreas.js

// Constantes: UPPER_SNAKE_CASE
const MAX_NOTES_SIZE = 50000

// Funções: camelCase
handleNotesChange, toggleModule

// CSS Classes: kebab-case ou Tailwind
breadcrumb-container, flex items-center
```

### Estrutura de Componente Padrão

```jsx
// 1. Imports
import React, { useState, useEffect } from 'react'
import { ChevronRight } from 'lucide-react'

// 2. Component
export function ComponentName({ prop1, prop2, onAction }) {
  // 3. Hooks
  const [state, setState] = useState(initialValue)
  useEffect(() => {
    // Side effects
  }, [dependencies])

  // 4. Event Handlers
  const handleClick = () => {
    // Logic
    onAction?.()
  }

  // 5. Render
  return (
    <div className="container">
      {/* JSX */}
    </div>
  )
}
```

### Estrutura de Dados (studyAreas.js)

```javascript
export const studyAreas = [
  {
    name: "Bash",
    icon: "🐚",
    description: "Shell scripting, automação e linha de comando",
    modules: 16,
    hours: 32,
    badge: "Integrado",           // "Integrado" | "Novo" | null
    hasIntegratedApp: true,
    key: "bash",
    flashcards: [
      {
        id: 1,
        category: "basics",
        front: "Como criar uma variável em Bash?",
        back: "VARIAVEL=\"valor\" (sem espaços ao redor do =)",
        code: "NAME=\"João\"\\necho $NAME"
      }
    ]
  }
]
```

### Estrutura de Módulos (bashLearningData.js)

```javascript
export const bashPhases = [
  {
    id: 1,
    title: "Seção 1: Fundamentos Shell Scripting",
    description: "História, filosofia software tools e scripts básicos",
    modules: [
      {
        id: "1.1",
        title: "Introdução ao Curso + História Unix/Linux",
        week: 1,
        date: "03/02/2025",
        deliverable: "Compreensão da história e contexto do shell scripting",
        topics: [
          {
            title: "Introdução ao Curso",
            content: "Objetivos e estrutura do curso"
          },
          {
            title: "História Unix/Linux",
            content: "Bell Labs, PDP-11 e evolução dos shells"
          }
        ]
      }
    ]
  }
]
```

## Padrões de Estilo (Tailwind)

### Cores Principais

```css
/* Gradientes */
bg-gradient-to-br from-purple-500 to-blue-500  /* Cards especiais */
bg-gradient-to-br from-slate-50 to-slate-100   /* Fundo geral */

/* Primárias */
text-purple-600, bg-purple-500  /* Ação principal */
text-blue-600, bg-blue-500      /* Links */
text-green-600, bg-green-500    /* Sucesso */
text-slate-600, bg-slate-100    /* Neutro */

/* Estados */
hover:bg-purple-700             /* Hover buttons */
focus:ring-2 focus:ring-purple-500  /* Focus estados */
```

### Spacing e Layout

```css
/* Containers */
max-w-7xl mx-auto px-4          /* Container principal */
max-w-4xl mx-auto               /* Container estreito */

/* Padding padrão */
p-6                             /* Cards */
p-4                             /* Sections */
py-3 px-4                       /* Buttons */

/* Grid */
grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6
```

### Componentes Comuns

```css
/* Card */
bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow

/* Button Primário */
bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 transition-colors

/* Input */
w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-purple-500
```

## Build e Deploy

### Comandos

```bash
npm run dev          # Dev server (porta 3000)
npm run build        # Build produção
npm run preview      # Preview build
npm test             # Testes Vitest
npm run test:ui      # Testes UI
npm run test:coverage # Cobertura

docker-compose up -d  # Container
docker-compose down   # Parar
```

### Vite Config

```javascript
// vite.config.js
export default {
  build: {
    sourcemap: false,          // Segurança
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,    // Remove console.log
        drop_debugger: true
      }
    },
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
          'ui-vendor': ['lucide-react', 'react-markdown']
        }
      }
    }
  }
}
```

## Débito Técnico Conhecido

### Alta Prioridade

1. **Duplicação de Código:** ~25% (800 linhas em *LearningSystem.jsx)
2. **Sem React Router:** Navegação via estado interno
3. **LocalStorage:** Sem tratamento de erros (QuotaExceededError)
4. **Progresso não persiste:** Reset ao recarregar

### Média Prioridade

5. **Cobertura de Testes:** 5% (meta: 80%)
6. **Sem TypeScript:** Projeto em JavaScript puro
7. **Acessibilidade:** Falta ARIA labels consistentes
8. **Bundle Size:** TBD (meta: <200KB)

## Roadmap

### Sprint 2.4 (Atual - ÉPICO 12)

- US-060: Refatorar Nomenclatura (13 pts)
- US-061: Implementar Breadcrumb (8 pts)
- US-062: Padronizar Botões (5 pts)
- US-063: Unificar Conceito de Notas (5 pts)

### Sprint 2.5

- US-064: Melhorar Hierarquia Visual (8 pts)
- US-065: Documentar Arquitetura (3 pts)

### Futuro (Release 2.0+)

- US-040: React Router (13 pts)
- US-041: Tratamento erros localStorage (5 pts)
- US-042: Persistir progresso (8 pts)
- US-043: BaseLearningSystem (21 pts)
- US-050: Dark mode (13 pts)

## Navegação Rápida

```bash
# Encontrar componente
find src/components -name "*Learning*.jsx"

# Ver estrutura de dados
cat src/data/studyAreas.js | grep "name:"

# Buscar uso de hook
grep -r "useState" src/components/

# Ver imports de componente
head -20 src/components/SistemaEducacionalCompleto.jsx

# Contar linhas de código
wc -l src/components/*.jsx

# Listar TODOs
grep -r "TODO" src/

# Ver dependências
cat package.json | jq .dependencies
```

## Referências Críticas

- **PRODUCT-CENTRAL-DOCUMENT.md**: Fonte única da verdade (PRD + Backlog)
- **CLAUDE.md**: Instruções para Claude Code
- **ARQUITETURA_E_PADROES.md**: Padrões técnicos
- **README.md**: Setup e uso básico
- **docs/MCP-CHROME-DEVTOOLS-*.md**: Guias MCP (3 docs)

## Ativação Automática

Esta skill ativa quando você:
- Precisa entender arquitetura do sistema
- Navega entre componentes
- Toma decisões de design
- Busca padrões estabelecidos
- Implementa novas features
- Refatora código existente
- Escreve documentação técnica
