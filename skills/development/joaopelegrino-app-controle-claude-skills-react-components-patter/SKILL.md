---
name: react-components-patterns
scope: domain
target: organizador-base-conhecimento
description: |
  Comprehensive guide to React component patterns used in the Plataforma B2B de treinamento técnico corporativo educational platform. This skill covers functional components with hooks, composition patterns, state management, props flow, and error handling strategies essential for building maintainable React applications.

  Learn how to create reusable, testable components following React best practices while avoiding common antipatterns like prop drilling, unnecessary class components, and improper state management. The skill emphasizes composition over inheritance, unidirectional data flow, and separation of concerns.

  Real-world examples are taken directly from the project codebase, including CLearningSystem, BashLearningSystem, Breadcrumb, AreaCard, and FlashcardModal components. Each pattern is demonstrated with production code showing how architectural decisions were implemented in a 5,500+ line React application with 17 components.

  Key topics include functional components (vs class components), React Hooks (useState, useEffect, custom hooks), component composition strategies, props vs Context API decision-making, controlled components for forms, error boundaries for resilience, and testing patterns with Vitest and Testing Library.

  This skill is essential for understanding the system's component architecture, contributing new features, refactoring duplicated code (current 25% duplication target: <10%), and maintaining consistency across the 227-module educational platform. Includes troubleshooting guides for common React issues encountered during development.

keywords: |
  react, components, hooks, useState, useEffect, functional-components,
  composition, props, context-api, error-boundary, patterns, jsx,
  react-patterns, component-architecture, reusable-components

allowed-tools: |
  Read, Write, Edit, Grep, Glob, Bash
---

# React Components Patterns

> **Padrões de Componentes React para Plataforma B2B de treinamento técnico corporativo**
>
> **Versão:** 1.0.0
> **Última Atualização:** 2025-11-16
> **Target:** React 18.3.1 + Hooks
> **Projeto:** Plataforma B2B de treinamento técnico corporativo

---

## 📋 Índice

1. [Overview](#-overview)
2. [Quando Usar Esta Skill](#-quando-usar-esta-skill)
3. [Conceitos Fundamentais](#-conceitos-fundamentais)
4. [Padrões de Componentes](#-padrões-de-componentes)
5. [Exemplos Práticos do Projeto](#-exemplos-práticos-do-projeto)
6. [Antipadrões a Evitar](#-antipadrões-a-evitar)
7. [Troubleshooting](#-troubleshooting)
8. [Referências](#-referências)

---

## 🎯 Overview

Esta skill documenta todos os padrões de componentes React utilizados no **Plataforma B2B de treinamento técnico corporativo**, um sistema educacional com 17 componentes React, 227 módulos educacionais e 5 sistemas integrados de aprendizado.

**O que você vai aprender:**
- Como criar componentes funcionais reutilizáveis e testáveis
- Quando usar hooks vs. Context API vs. props drilling
- Padrões de composição (composition over inheritance)
- Estratégias de state management local
- Error boundaries e tratamento de erros
- Testes de componentes com Vitest e Testing Library

**Por que esta skill é importante:**
- ✅ **Consistência:** Garante que novos componentes seguem os mesmos padrões existentes
- ✅ **Manutenibilidade:** Reduz duplicação de código (meta: 25% → <10%)
- ✅ **Testabilidade:** Componentes funcionais são mais fáceis de testar
- ✅ **Performance:** Hooks permitem otimizações (useMemo, useCallback)
- ✅ **Escalabilidade:** Composição permite crescimento sustentável

---

## 📋 Quando Usar Esta Skill

### Cenário 1: Criando Novo Componente

**Situação:** Você precisa adicionar um novo componente (ex: `LessonCard`, `ProgressBar`, `QuizModal`)

**Use esta skill para:**
- Decidir entre functional component vs. class component (sempre functional!)
- Escolher hooks apropriados (useState, useEffect, custom hooks)
- Definir interface de props (destructuring, PropTypes/TypeScript)
- Estruturar JSX de forma legível e manutenível

**Exemplo de aplicação:**
```jsx
// ✅ Seguindo padrões da skill
function LessonCard({ title, duration, completed, onComplete, onClick }) {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div
      onClick={onClick}
      className="card"
    >
      <h3>{title}</h3>
      <span>{duration}</span>
      {completed && <span>✅</span>}
    </div>
  );
}
```

---

### Cenário 2: Refatorando Código Duplicado

**Situação:** Você identificou 5 componentes com lógica similar (ex: CLearningSystem, BashLearningSystem, RustLearningSystem)

**Use esta skill para:**
- Extrair lógica comum em hooks customizados
- Criar componentes genéricos (BaseLearningSystem)
- Aplicar composition patterns
- Reduzir de 800+ linhas duplicadas para componente reutilizável

**Exemplo de refatoração:**
```jsx
// ❌ Antes: 5 componentes com 800 linhas duplicadas
function CLearningSystem() {
  const [notes, setNotes] = useState('');
  const [progress, setProgress] = useState([]);
  // ... 160 linhas de lógica duplicada
}

// ✅ Depois: Hook customizado + componente genérico
function useCourseLogic(courseId) {
  const [notes, setNotes, saveStatus] = useAutoSaveNotes(courseId);
  const [progress, updateProgress] = useModuleProgress(courseId);
  return { notes, setNotes, saveStatus, progress, updateProgress };
}

function BaseLearningSystem({ courseId, courseData }) {
  const { notes, setNotes, progress, updateProgress } = useCourseLogic(courseId);
  // ... 40 linhas de lógica genérica
}
```

**Impacto:** Reduz manutenção de 5 arquivos para 1 componente + 2 hooks

---

### Cenário 3: Debugging Problemas de Estado

**Situação:** Componente re-renderiza infinitamente ou estado não atualiza corretamente

**Use esta skill para:**
- Entender fluxo unidirecional de dados (props down, events up)
- Diagnosticar problemas com useEffect dependencies
- Identificar mutações acidentais de estado
- Aplicar padrões de imutabilidade

**Exemplo de debug:**
```jsx
// ❌ Problema: Re-render infinito
useEffect(() => {
  setData(fetchData()); // ⚠️ Sem array de dependências!
});

// ✅ Solução: Dependências corretas
useEffect(() => {
  async function load() {
    const result = await fetchData();
    setData(result);
  }
  load();
}, []); // ✅ Roda apenas uma vez
```

---

## 💡 Conceitos Fundamentais

### 1. Functional Components com Hooks

**Princípio:** Sempre use functional components em vez de class components.

**Por quê:**
- ✅ Menos código boilerplate (sem constructor, bind)
- ✅ Hooks permitem reutilizar lógica (custom hooks)
- ✅ Mais fácil de testar (funções puras)
- ✅ Melhor suporte a TypeScript
- ✅ React team recomenda (class components legacy)

**Anatomia de um functional component:**

```jsx
import React, { useState, useEffect } from 'react';

/**
 * Card de área de estudo do Hub
 *
 * Props:
 * - titulo: string - Nome da área (ex: "Bash Shell Scripting")
 * - descricao: string - Descrição curta
 * - icone: string - Emoji representativo
 * - horas: number - Duração total em horas
 * - modulos: number - Quantidade de aulas
 * - onClick: function - Callback ao clicar
 */
function AreaCard({ titulo, descricao, icone, horas, modulos, onClick }) {
  // Estado local (se necessário)
  const [isHovered, setIsHovered] = useState(false);

  // Efeitos colaterais (se necessário)
  useEffect(() => {
    // Lógica que roda após render
    console.log(`AreaCard ${titulo} montado`);
  }, [titulo]); // Dependências

  // Event handlers
  const handleMouseEnter = () => setIsHovered(true);
  const handleMouseLeave = () => setIsHovered(false);

  // JSX Render
  return (
    <div
      onClick={onClick}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      className={`card ${isHovered ? 'card-hover' : ''}`}
    >
      <div className="card-header">
        <span className="icon">{icone}</span>
        <h3>{titulo}</h3>
      </div>

      <p className="description">{descricao}</p>

      <div className="meta">
        <span>📚 {modulos} aulas</span>
        <span>⏱️ {horas}h</span>
      </div>
    </div>
  );
}

export default AreaCard;
```

**Checklist de qualidade:**
- [ ] Usa function (não arrow function para componentes principais)
- [ ] Props destructured na assinatura
- [ ] Comentário JSDoc descrevendo props
- [ ] Event handlers com nomes descritivos (handleClick, handleChange)
- [ ] Hooks no topo do componente (antes de qualquer condicional)
- [ ] JSX legível (indentação correta, componentes pequenos)
- [ ] export default ao final

---

### 2. Composition Over Inheritance

**Princípio:** Componha componentes de partes menores, não herde de classes base.

**Por quê:**
- ✅ Mais flexível (mix and match)
- ✅ Menos acoplamento
- ✅ Reutilização via props e children
- ✅ Alinhado com filosofia React

**Exemplo Real: Breadcrumb Component**

```jsx
// ✅ Composition: Breadcrumb é composto de itens menores
function Breadcrumb({ items }) {
  return (
    <nav aria-label="Breadcrumb" className="breadcrumb">
      {items.map((item, index) => (
        <React.Fragment key={index}>
          <BreadcrumbItem {...item} />
          {index < items.length - 1 && <BreadcrumbSeparator />}
        </React.Fragment>
      ))}
    </nav>
  );
}

// Componente pequeno e reutilizável
function BreadcrumbItem({ label, icon, onClick, current }) {
  return (
    <button
      onClick={onClick}
      aria-current={current ? 'page' : undefined}
      className={`breadcrumb-item ${current ? 'current' : ''}`}
    >
      {icon && <span aria-hidden="true">{icon}</span>}
      {label}
    </button>
  );
}

// Separador visual
function BreadcrumbSeparator() {
  return <span aria-hidden="true" className="separator">›</span>;
}

// Uso no CLearningSystem
<Breadcrumb items={[
  { label: 'Hub', icon: '🏠', onClick: () => setView('hub') },
  { label: 'Curso de C', icon: '📖', onClick: () => setView('course') },
  { label: 'Aula 1.1', icon: '📝', current: true }
]} />
```

**Benefícios aplicados:**
- Breadcrumb testável independentemente
- BreadcrumbItem reutilizável em outros contextos
- Fácil adicionar novos tipos (BreadcrumbCollapse para mobile)

**Arquivo real:** `src/components/Breadcrumb.jsx:15-45`

---

### 3. Props vs. Context API

**Decisão:** Quando usar props drilling vs. Context API?

**Use Props quando:**
- ✅ Componente pai e filho próximos (1-2 níveis)
- ✅ Dados específicos de um componente
- ✅ Performance é crítica (props são mais rápidos)
- ✅ Relação clara parent → child

**Use Context API quando:**
- ✅ Dados globais (tema, usuário, idioma)
- ✅ Props drilling profundo (3+ níveis)
- ✅ Muitos componentes precisam do mesmo dado
- ✅ Evitar "prop tunneling"

**Exemplo Props (Caso Comum no Projeto):**

```jsx
// ✅ Props drilling aceitável (apenas 2 níveis)
function CLearningSystem() {
  const [selectedLesson, setSelectedLesson] = useState(null);

  return (
    <LessonList
      lessons={courseData.lessons}
      selectedId={selectedLesson?.id}
      onSelect={setSelectedLesson}
    />
  );
}

function LessonList({ lessons, selectedId, onSelect }) {
  return lessons.map(lesson => (
    <LessonItem
      key={lesson.id}
      lesson={lesson}
      isSelected={lesson.id === selectedId}
      onClick={() => onSelect(lesson)}
    />
  ));
}
```

**Exemplo Context (Planejado para Release 2.0):**

```jsx
// Context para tema (usado em 10+ componentes)
const ThemeContext = React.createContext('light');

function App() {
  const [theme, setTheme] = useState('light');

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      <Header />
      <MainContent />
      <Footer />
    </ThemeContext.Provider>
  );
}

// Qualquer componente profundo pode acessar
function ThemeToggle() {
  const { theme, setTheme } = useContext(ThemeContext);

  return (
    <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
      {theme === 'light' ? '🌙' : '☀️'}
    </button>
  );
}
```

**Regra prática:** Start with props, migrate to Context when passing through 3+ components.

---

### 4. Controlled vs. Uncontrolled Components

**Controlled:** React controla o estado do input (recomendado)

**Uncontrolled:** DOM controla o estado (usar apenas se necessário)

**Exemplo Controlled (Caderno de Notas):**

```jsx
function NotesView({ courseId }) {
  const [notes, setNotes, saveStatus] = useAutoSaveNotes(courseId);

  return (
    <textarea
      value={notes} // ✅ Controlled: React é source of truth
      onChange={(e) => setNotes(e.target.value)}
      placeholder="Suas anotações..."
    />
  );
}
```

**Arquivo real:** `src/components/CNotesView.jsx:45-60`

**Por que controlled:**
- ✅ Estado sempre sincronizado
- ✅ Fácil validar e formatar input
- ✅ Auto-save funciona out of the box
- ✅ Testável (pode setar valor programaticamente)

---

### 5. Error Boundaries

**Princípio:** Componentes não devem crashar a aplicação inteira.

**Implementação:**

```jsx
// ErrorBoundary.jsx
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
    // Futuramente: enviar para Sentry
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary">
          <h2>⚠️ Algo deu errado</h2>
          <p>{this.state.error?.message}</p>
          <button onClick={() => window.location.reload()}>
            Recarregar Página
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

// Uso no SistemaEducacionalCompleto
function App() {
  return (
    <ErrorBoundary>
      <HubView />
    </ErrorBoundary>
  );
}
```

**Arquivo real:** `src/components/ErrorBoundary.jsx:1-40`

**Nota:** Error boundaries **devem ser class components** (única exceção à regra functional-first)

---

## 🏗️ Padrões de Componentes

### Padrão 1: Presentational vs. Container

**Presentational (Dumb):** Apenas UI, recebe tudo via props

```jsx
// ✅ Presentational: apenas renderiza
function AreaCard({ titulo, icone, onClick }) {
  return (
    <div onClick={onClick} className="card">
      <span>{icone}</span>
      <h3>{titulo}</h3>
    </div>
  );
}
```

**Container (Smart):** Gerencia estado e lógica

```jsx
// ✅ Container: gerencia dados e lógica
function HubView() {
  const [areas, setAreas] = useState(studyAreas);
  const [filter, setFilter] = useState('');

  const filteredAreas = areas.filter(a =>
    a.titulo.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div>
      <input
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        placeholder="Buscar área..."
      />
      {filteredAreas.map(area => (
        <AreaCard key={area.id} {...area} onClick={() => navigate(area.id)} />
      ))}
    </div>
  );
}
```

**Arquivo real:** `src/components/HubView.jsx:30-80`

**Benefício:** Presentational components são mais testáveis e reutilizáveis

---

### Padrão 2: Render Props (Avançado)

**Uso:** Compartilhar lógica entre componentes via função render

```jsx
// Componente que gerencia mouse position
function MouseTracker({ render }) {
  const [position, setPosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMove = (e) => setPosition({ x: e.clientX, y: e.clientY });
    window.addEventListener('mousemove', handleMove);
    return () => window.removeEventListener('mousemove', handleMove);
  }, []);

  return render(position);
}

// Uso
<MouseTracker render={({ x, y }) => (
  <p>Mouse em: {x}, {y}</p>
)} />
```

**Nota:** Padrão avançado, não usado atualmente no projeto (hooks são preferidos)

---

### Padrão 3: Higher-Order Components (HOC)

**Definição:** Função que recebe componente e retorna novo componente

```jsx
// HOC para adicionar loading state
function withLoading(Component) {
  return function WithLoadingComponent({ isLoading, ...props }) {
    if (isLoading) {
      return <div className="spinner">Carregando...</div>;
    }
    return <Component {...props} />;
  };
}

// Uso
const LessonListWithLoading = withLoading(LessonList);

<LessonListWithLoading
  isLoading={loading}
  lessons={lessons}
/>
```

**Nota:** HOCs são legado, hooks customizados são preferidos

---

## 🔧 Exemplos Práticos do Projeto

### Exemplo 1: AreaCard (Componente Mais Simples)

**Localização:** `src/components/AreaCard.jsx`

**Responsabilidade:** Card clicável de área de estudo no Hub

**Código completo:**

```jsx
function AreaCard({
  titulo,
  descricao,
  icone,
  horas,
  modulos,
  onClick
}) {
  return (
    <div
      onClick={onClick}
      className="
        bg-white rounded-lg p-6 shadow-lg
        hover:shadow-xl transition-shadow cursor-pointer
        border border-gray-200
      "
    >
      <div className="flex items-center gap-3 mb-3">
        <span className="text-4xl">{icone}</span>
        <h3 className="text-xl font-bold text-gray-800">{titulo}</h3>
      </div>

      <p className="text-gray-600 mb-4 line-clamp-2">{descricao}</p>

      <div className="flex gap-4 text-sm text-gray-500">
        <span>📚 {modulos} aulas</span>
        <span>⏱️ {horas}h</span>
      </div>
    </div>
  );
}

export default AreaCard;
```

**Análise do padrão:**
- ✅ Functional component puro (sem estado)
- ✅ Props destructured
- ✅ Tailwind classes inline
- ✅ Acessibilidade implícita (div clicável com onClick)
- ✅ Feedback visual (hover, transition)

**Uso no HubView:**

```jsx
<AreaCard
  titulo="Bash Shell Scripting"
  descricao="Domine o terminal"
  icone="💻"
  horas={16}
  modulos={16}
  onClick={() => setCurrentView('bash')}
/>
```

**Arquivo real:** `src/components/AreaCard.jsx:1-35`

---

### Exemplo 2: Breadcrumb (Componente com Estado e Acessibilidade)

**Localização:** `src/components/Breadcrumb.jsx`

**Responsabilidade:** Navegação hierárquica (Hub > Curso > Aula)

**Features:**
- ✅ WCAG 2.1 AA compliant
- ✅ Responsivo (colapsa em mobile)
- ✅ Sticky (sempre visível)
- ✅ Clicável (navegação entre níveis)

**Código (simplificado):**

```jsx
function Breadcrumb({ items }) {
  return (
    <nav
      aria-label="Breadcrumb"
      className="sticky top-0 z-10 bg-white shadow-md px-6 py-3"
    >
      <ol className="flex items-center gap-2">
        {items.map((item, index) => (
          <React.Fragment key={index}>
            <li>
              <button
                onClick={item.onClick}
                aria-current={item.current ? 'page' : undefined}
                className={`
                  flex items-center gap-2 px-3 py-1 rounded
                  ${item.current
                    ? 'bg-blue-100 text-blue-700 font-semibold'
                    : 'hover:bg-gray-100 text-gray-600'
                  }
                `}
              >
                {item.icon && <span aria-hidden="true">{item.icon}</span>}
                {item.label}
              </button>
            </li>

            {index < items.length - 1 && (
              <li aria-hidden="true" className="text-gray-400">
                ›
              </li>
            )}
          </React.Fragment>
        ))}
      </ol>
    </nav>
  );
}
```

**Arquivo real:** `src/components/Breadcrumb.jsx:1-95`

**Padrões aplicados:**
- ✅ Composition (Breadcrumb + BreadcrumbItem)
- ✅ Acessibilidade (aria-label, aria-current, semantic HTML)
- ✅ Responsividade (classes Tailwind)
- ✅ State management via props (items array)

**Validação US-061:** 13/13 critérios de aceite completos ✅

---

### Exemplo 3: CLearningSystem (Componente Complexo com Estado)

**Localização:** `src/components/CLearningSystem.jsx`

**Responsabilidade:** Sistema completo de aprendizado do Curso de C

**Estado gerenciado:**
- `currentView`: 'course' | 'lesson' | 'notes'
- `selectedLesson`: Lesson | null
- `completedLessons`: string[]
- `showFlashcards`: boolean

**Estrutura (simplificada):**

```jsx
function CLearningSystem({ onBack }) {
  // Estado de navegação
  const [currentView, setCurrentView] = useState('course');
  const [selectedLesson, setSelectedLesson] = useState(null);

  // Estado de progresso
  const [completedLessons, setCompletedLessons] = useState([]);

  // Estado de modals
  const [showFlashcards, setShowFlashcards] = useState(false);

  // Carregar progresso do localStorage ao montar
  useEffect(() => {
    const saved = localStorage.getItem('plataforma-b2b_progress_c');
    if (saved) {
      const { completedLessons } = JSON.parse(saved);
      setCompletedLessons(completedLessons);
    }
  }, []);

  // Handler de conclusão de aula
  const handleCompleteLesson = (lessonId) => {
    if (completedLessons.includes(lessonId)) return;

    const newCompleted = [...completedLessons, lessonId];
    setCompletedLessons(newCompleted);

    localStorage.setItem('plataforma-b2b_progress_c', JSON.stringify({
      completedLessons: newCompleted,
      lastUpdated: Date.now()
    }));
  };

  // Render condicional baseado em currentView
  if (currentView === 'notes') {
    return <CNotesView onBack={() => setCurrentView('course')} />;
  }

  if (currentView === 'lesson' && selectedLesson) {
    return (
      <div>
        <Breadcrumb items={[
          { label: 'Hub', icon: '🏠', onClick: onBack },
          { label: 'Curso de C', icon: '📖', onClick: () => setCurrentView('course') },
          { label: selectedLesson.title, icon: '📝', current: true }
        ]} />
        <LessonContent lesson={selectedLesson} />
        <button onClick={() => handleCompleteLesson(selectedLesson.id)}>
          ✅ Marcar como Concluída
        </button>
      </div>
    );
  }

  // View padrão: lista de aulas
  return (
    <div>
      <Breadcrumb items={[
        { label: 'Hub', icon: '🏠', onClick: onBack },
        { label: 'Curso de C', icon: '📖', current: true }
      ]} />

      <button onClick={() => setCurrentView('notes')}>
        📖 Estudar
      </button>

      <button onClick={() => setShowFlashcards(true)}>
        🎴 Flash Cards
      </button>

      {cCourseData.sections.map(section => (
        <Section key={section.sectionTitle}>
          <h2>{section.sectionTitle}</h2>
          {section.modules.map(lesson => (
            <LessonItem
              key={lesson.id}
              lesson={lesson}
              completed={completedLessons.includes(lesson.id)}
              onClick={() => {
                setSelectedLesson(lesson);
                setCurrentView('lesson');
              }}
            />
          ))}
        </Section>
      ))}

      {showFlashcards && (
        <FlashcardModal
          cards={cCourseData.flashcards}
          onClose={() => setShowFlashcards(false)}
        />
      )}
    </div>
  );
}
```

**Arquivo real:** `src/components/CLearningSystem.jsx:1-450`

**Padrões aplicados:**
- ✅ Multiple useState hooks (separação de concerns)
- ✅ useEffect para side effects (localStorage)
- ✅ Controlled components (estado sempre sincronizado)
- ✅ Conditional rendering (view switching)
- ✅ Event handlers descritivos
- ✅ Props drilling (onBack callback)

**Oportunidade de refatoração (US-043):**
- Extrair `useAutoSaveNotes` hook
- Extrair `useModuleProgress` hook
- Criar `BaseLearningSystem` componente genérico
- Reduzir 800 linhas duplicadas nos 5 sistemas

---

## ❌ Antipadrões a Evitar

### 1. Class Components (Exceto Error Boundaries)

**❌ Não fazer:**
```jsx
class AreaCard extends React.Component {
  constructor(props) {
    super(props);
    this.handleClick = this.handleClick.bind(this); // ⚠️ Boilerplate
  }

  handleClick() {
    this.props.onClick();
  }

  render() {
    return <div onClick={this.handleClick}>{this.props.titulo}</div>;
  }
}
```

**✅ Fazer:**
```jsx
function AreaCard({ titulo, onClick }) {
  return <div onClick={onClick}>{titulo}</div>;
}
```

**Por quê:** Functional components são mais simples, testáveis e alinhados com React moderno.

---

### 2. Mutação Direta de Estado

**❌ Não fazer:**
```jsx
const [lessons, setLessons] = useState([]);

// ⚠️ Mutação direta
lessons.push(newLesson);
setLessons(lessons); // React pode não detectar mudança!
```

**✅ Fazer:**
```jsx
// ✅ Imutabilidade
setLessons([...lessons, newLesson]);
// ou
setLessons(prev => [...prev, newLesson]);
```

**Por quê:** React depende de referências para detectar mudanças. Mutação direta quebra isso.

---

### 3. useEffect sem Array de Dependências

**❌ Não fazer:**
```jsx
useEffect(() => {
  fetchData(); // ⚠️ Roda em todo render!
});
```

**✅ Fazer:**
```jsx
useEffect(() => {
  fetchData();
}, []); // ✅ Roda apenas uma vez (mount)

// Ou com dependências
useEffect(() => {
  fetchData(courseId);
}, [courseId]); // ✅ Roda quando courseId muda
```

**Por quê:** Sem array de dependências, effect roda em todo render (performance ruim).

---

### 4. Props Drilling Excessivo

**❌ Não fazer:**
```jsx
// 5 níveis de props drilling!
<App user={user}>
  <Layout user={user}>
    <Sidebar user={user}>
      <Menu user={user}>
        <UserInfo user={user} />
      </Menu>
    </Sidebar>
  </Layout>
</App>
```

**✅ Fazer:**
```jsx
// Context API para dados globais
const UserContext = createContext();

<UserContext.Provider value={user}>
  <App>
    <Layout>
      <Sidebar>
        <Menu>
          <UserInfo /> {/* acessa via useContext */}
        </Menu>
      </Sidebar>
    </Layout>
  </App>
</UserContext.Provider>
```

**Por quê:** Props drilling profundo é difícil de manter. Context é melhor para dados globais.

---

### 5. Inline Functions em Props (Performance)

**❌ Evitar em listas grandes:**
```jsx
{lessons.map(lesson => (
  <LessonItem
    key={lesson.id}
    onClick={() => handleClick(lesson.id)} // ⚠️ Nova função a cada render
  />
))}
```

**✅ Fazer (se performance crítica):**
```jsx
const handleLessonClick = useCallback((lessonId) => {
  // lógica
}, []);

{lessons.map(lesson => (
  <LessonItem
    key={lesson.id}
    onClick={handleLessonClick}
    lessonId={lesson.id}
  />
))}
```

**Por quê:** Inline functions criam nova referência a cada render, podem causar re-renders desnecessários.

**Nota:** No projeto atual (227 módulos), performance ainda OK. Otimizar quando necessário.

---

## 🚨 Troubleshooting

### Problema 1: "Cannot read property 'map' of undefined"

**Sintoma:**
```
Uncaught TypeError: Cannot read property 'map' of undefined
    at CLearningSystem.jsx:45
```

**Causa:** Array de dados ainda não carregado quando componente tenta renderizar.

**Solução:**
```jsx
// ❌ Erro
function LessonList({ lessons }) {
  return lessons.map(lesson => <LessonItem {...lesson} />);
}

// ✅ Solução: Early return ou default value
function LessonList({ lessons = [] }) {
  if (!lessons || lessons.length === 0) {
    return <p>Nenhuma aula disponível</p>;
  }

  return lessons.map(lesson => <LessonItem {...lesson} />);
}
```

**Arquivo:** Problema comum em `CLearningSystem.jsx:90`, `BashLearningSystem.jsx:85`

---

### Problema 2: "Warning: Each child in a list should have a unique key prop"

**Sintoma:**
```
Warning: Each child in a list should have a unique "key" prop.
```

**Causa:** Esqueceu de adicionar prop `key` ao mapear array.

**Solução:**
```jsx
// ❌ Erro
{lessons.map(lesson => (
  <LessonItem title={lesson.title} />
))}

// ✅ Solução: Usar ID único
{lessons.map(lesson => (
  <LessonItem key={lesson.id} title={lesson.title} />
))}

// ⚠️ Evitar usar index (exceto se lista estática)
{lessons.map((lesson, index) => (
  <LessonItem key={index} {...lesson} /> // OK apenas se lista não muda
))}
```

---

### Problema 3: "Maximum update depth exceeded"

**Sintoma:**
```
Error: Maximum update depth exceeded. This can happen when a component
repeatedly calls setState inside componentWillUpdate or componentDidUpdate.
```

**Causa:** useEffect sem dependências corretas causando loop infinito.

**Solução:**
```jsx
// ❌ Loop infinito
useEffect(() => {
  setData(data + 1); // ⚠️ Atualiza data, que causa re-render, que roda effect novamente
});

// ✅ Solução 1: Array de dependências vazio
useEffect(() => {
  setData(1);
}, []); // Roda apenas uma vez

// ✅ Solução 2: Dependências corretas
useEffect(() => {
  if (shouldUpdate) {
    setData(newValue);
  }
}, [shouldUpdate]); // Roda apenas quando shouldUpdate muda
```

---

### Problema 4: Estado não atualiza imediatamente

**Sintoma:**
```jsx
const [count, setCount] = useState(0);

const handleClick = () => {
  setCount(count + 1);
  console.log(count); // ⚠️ Ainda mostra valor antigo!
};
```

**Causa:** setState é assíncrono. Valor atualizado só disponível no próximo render.

**Solução:**
```jsx
// ✅ Usar functional update se depende do valor anterior
const handleClick = () => {
  setCount(prev => {
    console.log(prev); // Valor mais recente
    return prev + 1;
  });
};

// ✅ Ou usar useEffect para reagir a mudanças
useEffect(() => {
  console.log('Count atualizado:', count);
}, [count]);
```

---

### Problema 5: Component re-renderiza muitas vezes

**Sintoma:** Performance ruim, componente renderiza 10+ vezes por interação.

**Diagnóstico:** Usar React DevTools Profiler.

**Causas comuns:**
1. Inline functions em props (criar nova função a cada render)
2. Objetos/arrays criados inline em props
3. Context que muda frequentemente

**Soluções:**

```jsx
// ❌ Causa re-renders
function Parent() {
  return <Child config={{ foo: 'bar' }} />; // ⚠️ Novo objeto a cada render
}

// ✅ Solução: useMemo para valores computados
function Parent() {
  const config = useMemo(() => ({ foo: 'bar' }), []);
  return <Child config={config} />;
}

// ✅ Solução: React.memo para componentes puros
const Child = React.memo(function Child({ config }) {
  return <div>{config.foo}</div>;
});
```

**Arquivo útil:** `.claude/skills/vite-build-optimization/` para análise de bundle

---

## 📚 Referências

### Skills Relacionadas

- **[component-refactor](../component-refactor/SKILL.md)** - Padrões de refatoração para reduzir duplicação
- **[react-hooks-custom](../react-hooks-custom/SKILL.md)** - Criação de hooks customizados
- **[system-state-management](../system-state-management/SKILL.md)** - State management avançado
- **[testing-strategy-vitest](../testing-strategy-vitest/SKILL.md)** - Testes de componentes React

### Documentação Técnica

- **[docs/tecnico/architecture/01-visao-geral-arquitetura.md](../../docs/tecnico/architecture/01-visao-geral-arquitetura.md)** - Arquitetura completa (4 camadas)
- **[docs/conceitual/01-visao-geral/00-definicoes-principais.md](../../docs/conceitual/01-visao-geral/00-definicoes-principais.md)** - Glossário e nomenclatura

### Código Real do Projeto

**Componentes Exemplares:**
- `src/components/AreaCard.jsx` - Componente simples e puro
- `src/components/Breadcrumb.jsx` - Acessibilidade e composição
- `src/components/CLearningSystem.jsx` - Componente complexo com estado
- `src/components/ErrorBoundary.jsx` - Error handling

**Hooks Customizados (Planejados):**
- `src/hooks/useAutoSaveNotes.js` - Auto-save para notas
- `src/hooks/useModuleProgress.js` - Progresso de aulas

### Recursos Externos

- **[React Docs - Components and Props](https://react.dev/learn/components-and-props)**
- **[React Docs - Hooks](https://react.dev/reference/react)**
- **[React Patterns](https://reactpatterns.com/)** - Catálogo de padrões
- **[Kent C. Dodds - Application State Management](https://kentcdodds.com/blog/application-state-management-with-react)** - Props vs Context

---

## 📝 Arquivos Auxiliares

Esta skill possui 3 arquivos auxiliares detalhados:

1. **[functional-components.md](./auxiliary/functional-components.md)** - Guia completo de functional components
2. **[hooks-guide.md](./auxiliary/hooks-guide.md)** - useState, useEffect, custom hooks em profundidade
3. **[composition-patterns.md](./auxiliary/composition-patterns.md)** - Padrões avançados de composição

---

**📍 Você está em:** `.claude/skills/react-components-patterns/SKILL.md`
**📅 Criado em:** 2025-11-16
**👤 Mantido por:** João Pelegrino + Claude Code
**🎯 Uso:** Referência para criar e manter componentes React no projeto
**🔄 Última auditoria:** 2025-11-16
**📊 Auto-discovery score:** TBD (testar após criação)
