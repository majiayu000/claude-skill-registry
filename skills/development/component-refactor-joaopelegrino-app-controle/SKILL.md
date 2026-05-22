---
name: component-refactor
description: Guia refatoração de componentes React seguindo padrões do Ultrathink, reduzindo duplicação e criando componentes genéricos reutilizáveis
allowed-tools: [Read, Edit, Grep, Bash]
---

# Component Refactor Skill - Ultrathink

## Objetivo

Esta skill ativa automaticamente para ajudar na **refatoração inteligente de componentes React**, especialmente focada em:

- Eliminar duplicação de código (meta: reduzir de 25% para <10%)
- Criar componentes genéricos (ex: BaseLearningSystem)
- Extrair lógica comum em hooks customizados
- Padronizar estrutura de componentes

## Contexto do Projeto

### Problema Atual (Débito Técnico)

**Duplicação:** ~25% do código (~800 linhas)

**Componentes Duplicados:**

```
src/components/
├── BashLearningSystem.jsx      ← ~160 linhas (similar)
├── CLearningSystem.jsx          ← ~170 linhas (similar)
├── RustLearningSystem.jsx       ← ~165 linhas (similar)
├── VSCodeLearningSystem.jsx     ← ~150 linhas (similar)
└── ClaudeCodeLearningSystem.jsx ← ~155 linhas (similar)

Total: ~800 linhas com lógica repetida
```

**Padrões Comuns:**

1. **Estado:** progresso, notas, currentModule
2. **LocalStorage:** save/load de notas
3. **Layout:** header, vídeo, notas, fases/módulos
4. **Navegação:** voltar ao hub, abrir notas de módulo
5. **Progresso:** barra visual, percentual

### Solução Proposta (US-043)

Criar `BaseLearningSystem.jsx` - componente genérico com props:

```jsx
<BaseLearningSystem
  technology="Bash"
  title="Curso de Bash Shell Scripting"
  subtitle="Shell Scripting Robusto → Unix Tools → Pipelines"
  videoId="fAgz66M4aNc"
  videoStart={415}
  phases={bashPhases}
  modules={bashModules}
  flashCards={bashFlashCards}
  notesKey="bash-learning-notes"
  icon="🐚"
  onBack={() => setView('hub')}
  onOpenModule={(moduleId) => setView('module', moduleId)}
/>
```

## Padrões de Refatoração

### 1. Extrair Lógica Comum em Hooks

```jsx
// ❌ ANTES: Lógica repetida em cada componente
const [notes, setNotes] = useState('')
const [saveStatus, setSaveStatus] = useState('')

useEffect(() => {
  const saved = localStorage.getItem('bash-notes')
  if (saved) setNotes(saved)
}, [])

const handleNotesChange = (e) => {
  const value = e.target.value
  setNotes(value)
  localStorage.setItem('bash-notes', value)
  setSaveStatus('Salvo!')
  setTimeout(() => setSaveStatus(''), 2000)
}

// ✅ DEPOIS: Hook reutilizável
const [notes, handleNotesChange, saveStatus] = useAutoSaveNotes('bash')
```

**Criar:** `src/hooks/useAutoSaveNotes.js`

```jsx
export function useAutoSaveNotes(key) {
  const [notes, setNotes] = useState('')
  const [saveStatus, setSaveStatus] = useState('')

  useEffect(() => {
    const saved = localStorage.getItem(`${key}-learning-notes`)
    if (saved) setNotes(saved)
  }, [key])

  const handleChange = useCallback((e) => {
    const value = e.target.value
    setNotes(value)
    try {
      localStorage.setItem(`${key}-learning-notes`, value)
      setSaveStatus('Salvo!')
      setTimeout(() => setSaveStatus(''), 2000)
    } catch (error) {
      setSaveStatus('Erro ao salvar')
    }
  }, [key])

  return [notes, handleChange, saveStatus]
}
```

### 2. Extrair Gerenciamento de Progresso

```jsx
// ✅ Criar: src/hooks/useModuleProgress.js
export function useModuleProgress(key, totalModules) {
  const [completedModules, setCompletedModules] = useState(new Set())

  useEffect(() => {
    const saved = localStorage.getItem(`${key}-progress`)
    if (saved) {
      setCompletedModules(new Set(JSON.parse(saved)))
    }
  }, [key])

  const toggleModule = useCallback((moduleId) => {
    setCompletedModules(prev => {
      const newSet = new Set(prev)
      if (newSet.has(moduleId)) {
        newSet.delete(moduleId)
      } else {
        newSet.add(moduleId)
      }
      localStorage.setItem(`${key}-progress`, JSON.stringify([...newSet]))
      return newSet
    })
  }, [key])

  const progress = Math.round((completedModules.size / totalModules) * 100)

  return [completedModules, toggleModule, progress]
}
```

### 3. Componente Genérico BaseLearningSystem

**Estrutura Proposta:**

```jsx
// src/components/BaseLearningSystem.jsx
export function BaseLearningSystem({
  // Identificação
  technology,      // "Bash", "C", "Rust", etc.
  title,           // "Curso de Bash Shell Scripting"
  subtitle,        // "Shell Scripting Robusto → ..."
  icon,            // "🐚"

  // Conteúdo
  videoId,         // "fAgz66M4aNc"
  videoStart,      // 415 (segundos)
  sections,        // Array de seções/fases
  modules,         // Array de módulos/aulas

  // Dados
  flashCards,      // Array de flash cards
  notesKey,        // "bash" (para localStorage)

  // Callbacks
  onBack,          // () => setView('hub')
  onOpenModule,    // (moduleId) => setView('module', moduleId)
}) {
  // Hooks customizados
  const [notes, handleNotesChange, saveStatus] = useAutoSaveNotes(notesKey)
  const [completed, toggle, progress] = useModuleProgress(notesKey, modules.length)

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header com breadcrumb */}
      <header>
        <Breadcrumb items={[
          { label: 'Hub', onClick: onBack },
          { label: `Curso de ${technology}`, current: true }
        ]} />
        <button onClick={onBack}>← Voltar ao Hub</button>
        <h1>{title}</h1>
        <p>{subtitle}</p>
      </header>

      {/* Progresso */}
      <ProgressBar progress={progress} total={modules.length} />

      {/* Vídeo */}
      {videoId && (
        <VideoSection videoId={videoId} start={videoStart} />
      )}

      {/* Caderno de Notas */}
      <NotesSection
        notes={notes}
        onChange={handleNotesChange}
        status={saveStatus}
        placeholder={`Minhas anotações pessoais sobre ${technology}...`}
      />

      {/* Estrutura do Curso */}
      <CourseStructure
        sections={sections}
        modules={modules}
        completed={completed}
        onToggle={toggle}
        onOpenModule={onOpenModule}
      />
    </div>
  )
}
```

### 4. Subcomponentes Reutilizáveis

**Criar estrutura modular:**

```
src/components/shared/
├── Breadcrumb.jsx           # Navegação hierárquica
├── ProgressBar.jsx          # Barra de progresso visual
├── VideoSection.jsx         # Embed YouTube
├── NotesSection.jsx         # Caderno de notas com auto-save
├── CourseStructure.jsx      # Seções e aulas
├── ModuleCard.jsx           # Card de aula individual
└── FlashCardTrigger.jsx     # Botão "Praticar com Flash Cards"
```

## Estratégia de Refatoração

### Passo 1: Criar Hooks (Primeira Semana)

1. `useAutoSaveNotes.js` - Notas com auto-save
2. `useModuleProgress.js` - Progresso de módulos
3. `useLocalStorage.js` - Wrapper genérico localStorage

### Passo 2: Criar Subcomponentes (Segunda Semana)

1. `Breadcrumb.jsx` - US-061
2. `ProgressBar.jsx`
3. `VideoSection.jsx`
4. `NotesSection.jsx`
5. `CourseStructure.jsx`

### Passo 3: BaseLearningSystem (Terceira Semana)

1. Criar componente genérico
2. Migrar `BashLearningSystem` primeiro (piloto)
3. Testar extensivamente
4. Migrar demais sistemas

### Passo 4: Validação (Quarta Semana)

1. Testes unitários para hooks
2. Testes de integração para BaseLearningSystem
3. Validar funcionalidade idêntica
4. Remover código duplicado

## Checklist de Refatoração

Ao refatorar um componente:

- [ ] Identificar lógica duplicada
- [ ] Verificar se hook customizado já existe
- [ ] Extrair para hook se repetido 3+ vezes
- [ ] Criar subcomponente se bloco JSX > 50 linhas
- [ ] Props bem tipadas (considerar PropTypes ou TypeScript)
- [ ] Testes escritos antes de remover código antigo
- [ ] Validar que comportamento é idêntico
- [ ] Atualizar imports em todos os arquivos
- [ ] Remover código morto

## Métricas de Sucesso

| Métrica | Antes | Meta |
|---------|-------|------|
| Duplicação | 25% (~800 linhas) | <10% (~300 linhas) |
| Componentes LearningSystem | 5 × 160 linhas | 1 × 250 + 5 × 30 |
| Hooks Customizados | 0 | 3+ |
| Subcomponentes Shared | 1 (AreaCard) | 10+ |
| Linhas de Código | ~5.500 | ~4.700 |
| Manutenibilidade | 6/10 | 9/10 |

## Referências

- **PRODUCT-CENTRAL-DOCUMENT.md**: US-043 (Refatorar BaseLearningSystem)
- **ÉPICO 10**: Débito Técnico (linha 690-794)
- **Arquivos Afetados**:
  - `src/components/*LearningSystem.jsx` (5 arquivos)
  - `src/components/*NotesView.jsx` (5 arquivos)

## Comandos Úteis

```bash
# Analisar duplicação
npx jscpd src/components/

# Contar linhas por componente
wc -l src/components/*LearningSystem.jsx

# Encontrar padrões comuns
grep -r "useState.*completedModules" src/

# Identificar imports duplicados
grep -r "import.*useState" src/components/ | sort | uniq -c | sort -rn
```

## Ativação Automática

Esta skill ativa quando você:
- Refatora componentes React
- Cria hooks customizados
- Implementa US-043 (BaseLearningSystem)
- Trabalha com arquivos em `src/components/`
- Reduz duplicação de código
- Extrai lógica comum
