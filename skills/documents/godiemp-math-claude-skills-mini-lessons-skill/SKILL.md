---
name: mini-lessons
description: Create interactive mini-lessons for the PAES math curriculum. Use when the user wants to add a new lesson, create lesson content, or implement lesson steps.
---

# Mini-Lessons Creation Skill

This skill guides you through creating world-class interactive mini-lessons for the PAES mathematics curriculum. Each lesson follows a 6-step pedagogical structure designed to maximize learning.

## When to Use This Skill

Invoke this skill when:
- User asks to "create a new lesson" or "add a mini-lesson"
- User wants to implement a specific topic from the curriculum
- User needs help with lesson step components
- User asks about lesson structure or patterns

---

# NOMENCLATURA: Niveles de Competencia vs Niveles Escolares

**IMPORTANTE**: El sistema usa DOS tipos de códigos que se parecen pero significan cosas diferentes:

## M1 y M2: Niveles de Competencia PAES

Los códigos **M1** y **M2** representan los dos niveles de competencia del examen PAES:

| Código | Nombre | Descripción |
|--------|--------|-------------|
| **M1** | Competencia Matemática 1 | Nivel básico - contenidos fundamentales |
| **M2** | Competencia Matemática 2 | Nivel avanzado - contenidos más complejos |

**Se usan en:**
- IDs de lecciones: `m1-alg-001-a`, `m2-geo-001-a`
- Campo `level` en registros: `level: 'M1'`
- Carpetas de componentes: `components/lessons/m1/`, `components/lessons/m2/`
- Unidades temáticas: `M1-ALG-001`, `M2-NUM-003`

## 1M, 2M, 3M, 4M: Niveles Escolares (Grados)

Los códigos **1M, 2M, 3M, 4M** representan los años de enseñanza media:

| Código | Grado Escolar | Equivalente |
|--------|---------------|-------------|
| **1M** | 1° Medio | 9th grade / Freshman |
| **2M** | 2° Medio | 10th grade / Sophomore |
| **3M** | 3° Medio | 11th grade / Junior |
| **4M** | 4° Medio | 12th grade / Senior |

**Se usan en:**
- Códigos MINEDUC: `MA1M-OA-03` (OA de 1° Medio)
- Campo `grade` en mapeos: `grade: '1M'`

## Relación entre ambos sistemas

Una lección de **Competencia M1** puede cubrir contenidos de **varios grados escolares**:

```
Lección: m1-alg-001-a (Competencia M1)
├── minEducOA: ['MA1M-OA-03']  → Cubre OA de 1° Medio
└── minEducOA: ['MA2M-OA-01']  → También puede cubrir OA de 2° Medio
```

## Formato de códigos MINEDUC

```
MA1M-OA-03
│││  │  └── Número de Objetivo de Aprendizaje
│││  └───── OA = Objetivo de Aprendizaje
│└└──────── 1M = 1° Medio (grado escolar)
└────────── MA = Matemáticas
```

Otros formatos:
- `MA2M-OA-XX` → 2° Medio
- `FG-MATE-3M-OAC-XX` → 3° Medio (Formación General)
- `FG-MATE-4M-OAC-XX` → 4° Medio (Formación General)

---

# STEP 0: IDENTIFY THE SUBJECT

**Before anything else, identify which mathematical subject the lesson covers:**

```
┌─────────────────────────────────────────────────────────────┐
│  📐 ÁLGEBRA (Algebra)                                       │
│  Variables, equations, expressions, factoring               │
│  → Read: .claude/skills/mini-lessons/subjects/algebra-patterns.md │
├─────────────────────────────────────────────────────────────┤
│  🔢 NÚMEROS (Numbers)                                       │
│  Fractions, percentages, decimals, operations               │
│  → Read: .claude/skills/mini-lessons/subjects/numbers-patterns.md │
├─────────────────────────────────────────────────────────────┤
│  📏 GEOMETRÍA (Geometry)                                    │
│  Shapes, areas, perimeters, theorems                        │
│  → Read: .claude/skills/mini-lessons/subjects/geometry-patterns.md │
├─────────────────────────────────────────────────────────────┤
│  🎲 PROBABILIDAD (Probability & Statistics)                 │
│  Probability, data, counting, graphs                        │
│  → Read: .claude/skills/mini-lessons/subjects/probability-patterns.md │
└─────────────────────────────────────────────────────────────┘
```

**Each subject has distinct patterns for hooks, explore steps, and explain steps.**
Read the subject-specific guide BEFORE proceeding to Phase 1.

**Subject Selection Guide:**
→ `.claude/skills/mini-lessons/subjects/README.md`

---

# THREE-STEP WORKFLOW

Creating a mini-lesson requires THREE steps:

```
┌─────────────────────────────────────────────────────────────┐
│  STEP 0: IDENTIFY SUBJECT                                   │
│  ─────────────────────────────────────────────────────────  │
│  Determine if this is Álgebra, Números, Geometría, or       │
│  Probabilidad. Read the subject-specific pattern guide.     │
│                                                             │
│  Read: .claude/skills/mini-lessons/subjects/README.md       │
│  Read: .claude/skills/mini-lessons/subjects/{subject}-patterns.md │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  PHASE 1: DEEP THINKING (Pedagogical Design)                │
│  ─────────────────────────────────────────────────────────  │
│  Use extended thinking to complete pedagogical design       │
│  BEFORE writing any code. Apply subject-specific patterns.  │
│                                                             │
│  Read: .claude/skills/mini-lessons/pedagogical-design.md    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  PHASE 2: IMPLEMENTATION (Error-Free Execution)             │
│  ─────────────────────────────────────────────────────────  │
│  Follow the 5 Critical Rules and create all files.          │
│  Use subject-specific templates and patterns.               │
│                                                             │
│  Read: .claude/skills/mini-lessons/anti-patterns.md         │
│  Read: .claude/skills/mini-lessons/step-templates.md        │
└─────────────────────────────────────────────────────────────┘
```

---

# PHASE 1: DEEP THINKING (Summary)

**MANDATORY**: Before writing ANY code, use extended thinking to complete:

1. **Learning Objective Analysis** - What concept, prerequisites, misconceptions?
2. **ZPD Analysis** - Scaffolding strategy from current ability to learning edge
3. **Lesson Narrative Arc** - Cognitive AND emotional journey for all 6 steps
4. **Real-World Hook Design** - Culturally relevant, genuinely puzzling scenario
5. **Multiple Representations** - Visual, symbolic, verbal, kinesthetic, numeric

**For detailed frameworks and templates, read:**
→ `.claude/skills/mini-lessons/pedagogical-design.md`

---

# PHASE 2: IMPLEMENTATION

## The 6-Step Structure

| Step | File Name | Type in Registry | Purpose | Required |
|------|-----------|------------------|---------|----------|
| 1 | `Step1Hook.tsx` | `hook` | Engage with real-world scenario | Yes |
| 2 | `Step2Explore.tsx` | `explore` | Interactive discovery of patterns | Yes |
| 3 | `Step3Explain.tsx` | `explain` | Theory with tabbed interface | Optional |
| 4 | `Step4Classify.tsx` | `explore` | Classification exercises | Yes |
| 5 | `Step5Practice.tsx` | `practice` | Guided problem-solving | Yes |
| 6 | `Step6Verify.tsx` | `verify` | Checkpoint quiz (3/4 to pass) | Yes |

> **Important: Step Types vs File Names**
>
> The TypeScript types define 5 step types: `'hook' | 'explore' | 'explain' | 'practice' | 'verify'`
>
> Component files are named `Step4Classify.tsx` but the **step type** in the lesson registration
> must use `type: 'explore'` (since 'classify' is not a valid type). The step `id` can be 'classify'.
>
> ```typescript
> // CORRECT registration - id is 'classify', type is 'explore'
> { id: 'classify', type: 'explore', title: 'Clasifica las Expresiones' }
> ```

### 5-Step Lessons (Variation)

Some lessons skip Step3Explain when theory is integrated into exploration:

```
components/lessons/m1/{lesson-slug}/
  ├─ Step1Hook.tsx
  ├─ Step2Explore.tsx      # Contains embedded theory
  ├─ Step3Classify.tsx     # Replaces Step4, numbered Step3
  ├─ Step4Practice.tsx     # Replaces Step5, numbered Step4
  ├─ Step5Verify.tsx       # Replaces Step6, numbered Step5
  └─ index.ts
```

**When to use 5-step:**
- Geometry lessons where visual exploration IS the explanation
- Simple concepts that don't need separate theory step
- Example: `area-paralelogramos-trapecios`

### Step1Hook: Multi-Phase Pattern (Recommended)

80%+ of lessons use the 4-phase hook pattern. This is the PRIMARY approach:

```
┌──────────────────────────────────────────────────────────────┐
│ Phase 1: SCENARIO                                            │
│ Present real-world situation with visual (emoji, SVG, image) │
│ "Don Pedro tiene una frutería..."                            │
│ [Explorar →]                                                 │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│ Phase 2: QUESTION                                            │
│ Pose the puzzle with multiple-choice options                 │
│ Show options A, B, C, D                                      │
│ [Verificar]                                                  │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│ Phase 3: REVEAL                                              │
│ Show if correct/incorrect with brief feedback                │
│ "¡Correcto!" or "¡Casi!"                                     │
│ (auto-advance after 1.5s)                                    │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│ Phase 4: RESULT                                              │
│ Bridge to the math concept                                   │
│ "Esto es exactamente lo que hacemos con..."                  │
│ [Descubrir el patrón →]                                      │
└──────────────────────────────────────────────────────────────┘
```

**Implementation:**
```typescript
type Phase = 'scenario' | 'question' | 'reveal' | 'result';
const [phase, setPhase] = useState<Phase>('scenario');
```

### Step3Explain: Pattern Decision Tree

Choose the right pattern for your Explain step:

```
                    ┌─────────────────────────────────────┐
                    │ Does the content have multiple      │
                    │ PARALLEL concepts that can be       │
                    │ explored in any order?              │
                    └───────────────┬─────────────────────┘
                                    │
               ┌────────────────────┴────────────────────┐
               │                                         │
              YES                                       NO
               │                                         │
               ▼                                         ▼
    ┌──────────────────────┐              ┌──────────────────────┐
    │ Use TABBED Interface │              │ Use PHASE-BASED      │
    │                      │              │ Navigation           │
    │ • Factor Numérico    │              │                      │
    │ • Factor Variable    │              │ • Definition → Method│
    │ • Factor Combinado   │              │ • Method → Formula   │
    │ • Tips               │              │ • Formula → Tips     │
    │                      │              │                      │
    │ User can jump to any │              │ Content builds on    │
    │ tab in any order     │              │ previous phase       │
    └──────────────────────┘              └──────────────────────┘
```

**Examples:**
- **Tabbed**: Factor Común (4 types), Productos Notables (4 formulas)
- **Phase-based**: MCM/MCD (definition → method → formula), Ecuaciones Lineales

### Acceptable Variations

While the patterns above are preferred, these variations are also acceptable:

1. **Phase-based Step3Explain**: For linear content, back/forward navigation is valid
   - See `anti-patterns.md` → "Valid Alternative Patterns"

2. **Custom Step6Verify**: When questions need embedded charts/diagrams
   - Must document why CheckpointQuiz isn't sufficient

3. **5-Step Pipeline**: Some geometry lessons skip Step3Explain
   - Only for lessons where theory is integrated into exploration

### Custom Step File Names

While the standard naming is `Step2Explore.tsx`, you can use descriptive names to clarify the step's purpose. **43 of 48 lessons use custom names.** The step number must match the progression.

**Common custom names:**
```
Step2ExploreMultiples.tsx    # Múltiplos lesson
Step2ExploreDice.tsx         # Probabilidad with dice
Step2FractionBars.tsx        # Fracciones visualization
Step3Proof.tsx               # Teorema Pitágoras
Step4Comparison.tsx          # Comparing numbers
Step5ExploreTiles.tsx        # MCD with tile visualization
Step5AbsoluteValue.tsx       # Valor absoluto exploration
```

**Rules for custom names:**
1. **Keep step number prefix** - `Step2...`, `Step3...`, etc.
2. **Be descriptive** - Name describes the activity or content
3. **Update index.ts exports** - Match the actual file names
4. **Match lesson registry** - The `id` in steps array should align

**Example index.ts with custom names:**
```typescript
export { default as Step1Hook } from './Step1Hook';
export { default as Step2ExploreMultiples } from './Step2ExploreMultiples';
export { default as Step3Explain } from './Step3Explain';
export { default as Step4Practice } from './Step4Practice';
export { default as Step5ExploreSynchronization } from './Step5ExploreSynchronization';
export { default as Step6Verify } from './Step6Verify';
```

## File Organization

```
app/lessons/m1/{lesson-slug}/
  └─ page.tsx                    # Main lesson page

components/lessons/m1/{lesson-slug}/
  ├─ Step1Hook.tsx
  ├─ Step2Explore.tsx
  ├─ Step3Explain.tsx
  ├─ Step4Classify.tsx
  ├─ Step5Practice.tsx
  ├─ Step6Verify.tsx
  └─ index.ts                    # Barrel exports

lib/lessons/lessons/{subject}.ts  # Lesson registry
```

---

## 5 CRITICAL IMPLEMENTATION RULES

These rules are NON-NEGOTIABLE. Violating them creates broken lessons.

### RULE 1: isActive Check (MANDATORY)

```typescript
export default function StepN({ onComplete, isActive }: LessonStepProps) {
  const [state, setState] = useState(...);

  if (!isActive) return null;  // THIS LINE IS MANDATORY

  return <div>...</div>;
}
```

### RULE 2: onComplete Call (MANDATORY)

```typescript
<button onClick={onComplete}>Continuar</button>
```

Every step MUST call `onComplete` when finished.

### RULE 3: Tips INSIDE Tabs (Step3Explain)

Tips MUST be inside a dedicated "Tips" tab, NOT as a standalone section.

```typescript
// 1. Include 'tips' in TabId type
type TabId = 'formula1' | 'formula2' | 'tips';

// 2. Conditional rendering
{activeTab === 'tips' ? (
  <TipsContent />
) : (
  <FormulaContent />
)}
```

**CANONICAL EXAMPLE**: `components/lessons/m1/factor-comun/Step3Explain.tsx`

### RULE 4: CheckpointQuiz for Step6 (MANDATORY)

```typescript
import { CheckpointQuiz, CheckpointQuestion } from '@/components/lessons/shared';

const QUESTIONS: CheckpointQuestion[] = [
  {
    id: 'q1',
    question: '¿Pregunta?',
    options: ['A', 'B', 'C', 'D'],
    correctAnswer: 0,
    explanation: 'Explicación.',
  },
  // 3-4 questions total
];

export default function Step6Verify({ onComplete, isActive }: LessonStepProps) {
  return (
    <CheckpointQuiz
      onComplete={onComplete}
      isActive={isActive}
      questions={QUESTIONS}
      requiredCorrect={3}
      successMessage="¡Excelente!"
    />
  );
}
```

### RULE 5: Dark Mode Classes (MANDATORY)

```typescript
// CORRECT
<div className="bg-blue-50 dark:bg-blue-900/30 text-gray-700 dark:text-gray-300">

// WRONG - missing dark: variants
<div className="bg-blue-50 text-gray-700">
```

---

## Anti-Pattern Detection

Before completing, verify NO anti-patterns exist.

**Read the full anti-pattern guide:**
→ `.claude/skills/mini-lessons/anti-patterns.md`

**Quick Checks:**
- [ ] Search for "Tips" - must be inside `{activeTab === 'tips' ? ...}`
- [ ] Search for `if (!isActive) return null;` - must exist in ALL steps
- [ ] Step6Verify should be ~30-40 lines (using CheckpointQuiz)
- [ ] Search for `bg-` - must have `dark:` variant

---

## Step Templates

For complete code templates with placeholders, read:
→ `.claude/skills/mini-lessons/step-templates.md`

---

## Lesson Registration

Add to `lib/lessons/lessons/{subject}.ts`:

```typescript
{
  id: 'm1-xxx-001-x',
  slug: 'lesson-slug',
  title: 'Título de la Lección',
  description: 'Descripción breve.',
  level: 'M1',
  subject: 'álgebra',  // 'números' | 'álgebra' | 'geometría' | 'probabilidad'
  thematicUnit: 'M1-XXX-001',
  skills: ['skill-1', 'skill-2'],
  estimatedMinutes: 14,
  minEducOA: ['MA1M-OA-03'],  // MINEDUC Learning Objectives
  steps: [
    { id: 'hook', type: 'hook', title: 'Título del Hook' },
    { id: 'explore', type: 'explore', title: 'Descubre el Patrón' },
    { id: 'explain', type: 'explain', title: 'La Teoría' },
    { id: 'classify', type: 'explore', title: 'Clasifica' },  // Note: type is 'explore'
    { id: 'practice', type: 'practice', title: 'Practica' },
    { id: 'verify', type: 'verify', title: 'Checkpoint' },
  ],
},
```

### minEducOA Field

The `minEducOA` field maps lessons to Chile's official MINEDUC Learning Objectives (Objetivos de Aprendizaje). This enables:
- Curriculum alignment tracking
- Teacher lesson planning
- PAES coverage analysis

**Common M1 codes:**

| Code | Area |
|------|------|
| `MA1M-OA-01` | Operaciones con números enteros y racionales |
| `MA1M-OA-02` | Potencias y raíces |
| `MA1M-OA-03` | Expresiones algebraicas y factorización |
| `MA1M-OA-04` | Ecuaciones e inecuaciones |
| `MA1M-OA-05` | Proporcionalidad y porcentajes |
| `MA1M-OA-06` | Geometría: perímetros, áreas, volúmenes |
| `MA1M-OA-07` | Transformaciones geométricas |
| `MA1M-OA-08` | Probabilidad y estadística |

**For complete OA reference, see:** `.claude/skills/mini-lessons/reference.md`

---

## Page Component Template

```typescript
'use client';

import { useRouter } from 'next/navigation';
import { LessonShell } from '@/components/lessons/shared';
import { getLessonBySlug } from '@/lib/lessons/types';
import {
  Step1Hook, Step2Explore, Step3Explain,
  Step4Classify, Step5Practice, Step6Verify,
} from '@/components/lessons/m1/{lesson-slug}';

const LESSON_SLUG = '{lesson-slug}';

export default function LessonPage() {
  const router = useRouter();
  const lesson = getLessonBySlug(LESSON_SLUG);

  if (!lesson) {
    return <div className="min-h-screen flex items-center justify-center">
      <p className="text-gray-500">Lección no encontrada</p>
    </div>;
  }

  return (
    <LessonShell
      lesson={lesson}
      onComplete={() => router.push('/mini-lessons')}
      onExit={() => router.push('/mini-lessons')}
    >
      {({ currentStep, completeStep }) => {
        const steps = [
          <Step1Hook key="1" onComplete={completeStep} isActive={currentStep === 0} />,
          <Step2Explore key="2" onComplete={completeStep} isActive={currentStep === 1} />,
          <Step3Explain key="3" onComplete={completeStep} isActive={currentStep === 2} />,
          <Step4Classify key="4" onComplete={completeStep} isActive={currentStep === 3} />,
          <Step5Practice key="5" onComplete={completeStep} isActive={currentStep === 4} />,
          <Step6Verify key="6" onComplete={completeStep} isActive={currentStep === 5} />,
        ];
        return steps[currentStep] || null;
      }}
    </LessonShell>
  );
}
```

---

## Index Exports

```typescript
// components/lessons/m1/{lesson-slug}/index.ts
export { default as Step1Hook } from './Step1Hook';
export { default as Step2Explore } from './Step2Explore';
export { default as Step3Explain } from './Step3Explain';
export { default as Step4Classify } from './Step4Classify';
export { default as Step5Practice } from './Step5Practice';
export { default as Step6Verify } from './Step6Verify';
```

---

## Quality Gates

All gates must pass before completion.

### Gate 1: Pedagogical Quality
- [ ] Hook uses real-world scenario (not abstract math)
- [ ] Explore has discovery BEFORE explanation
- [ ] Explain has Tips INSIDE tabs
- [ ] Progressive difficulty curve
- [ ] All text in Spanish
- [ ] Growth mindset language ("¡Casi!" not "Incorrecto")

### Gate 2: Technical Compliance
- [ ] All 6 step components created
- [ ] index.ts exports all steps
- [ ] page.tsx uses LessonShell
- [ ] Lesson registered in lib/lessons/lessons/{subject}.ts
- [ ] No TypeScript errors
- [ ] No lint errors

### Gate 3: Implementation Rules
- [ ] **RULE 1**: isActive check in ALL steps
- [ ] **RULE 2**: onComplete called in ALL steps
- [ ] **RULE 3**: Tips inside tabs (Step3)
- [ ] **RULE 4**: CheckpointQuiz used (Step6)
- [ ] **RULE 5**: Dark mode classes on ALL colors

### Gate 4: Content Quality
- [ ] Checkpoint questions test ALL steps
- [ ] Explanations are clear and step-by-step
- [ ] Hints are genuinely helpful
- [ ] Duration is 12-17 minutes

---

## Quick Reference

**For detailed reference materials, read:**
→ `.claude/skills/mini-lessons/reference.md`

**For pedagogical design guidance (Phase 1 planning), read:**
→ `.claude/skills/mini-lessons/pedagogical-design.md`

### Exemplar Lessons (Study These)
- `components/lessons/m1/factor-comun/` - Best Tips-in-tabs pattern
- `components/lessons/m1/terminos-semejantes/` - Best hook design
- `components/lessons/m1/figuras-compuestas/` - Best visual exploration

### DO NOT Copy
- `components/lessons/m1/productos-notables-cubos/Step3Explain.tsx` - Tips outside tabs

### Shared Components
Import from `@/components/lessons/shared`:
- `LessonShell` - Lesson page wrapper
- `CheckpointQuiz` - Step 6 verify (ALWAYS use)
- `Celebration` - Success animations
- `NumberLine` - Number visualization (Números)
- `BarChart`, `PieChart` - Data visualization (Probabilidad)
- `FrequencyTable` - Frequency tables with tally marks (Probabilidad)
- `FactorGrid` - Divisor/factor visualization (Números)
- `VennDiagram` - Set theory diagrams (Probabilidad)

**For full component props, see:** `.claude/skills/mini-lessons/reference.md`

---

## Mini-Lesson Toolbox

Composable hooks and primitives to build Step4/Step5 faster while keeping full control.

**For full documentation, read:**
→ `.claude/skills/mini-lessons/toolbox.md`

### Quick Reference

**Hooks** (`@/hooks/lessons`):
- `useMultipleChoice` - State for multiple-choice sequences
- `useHintToggle` - Toggle hint visibility

**Primitives** (`@/components/lessons/primitives`):
- `ProgressDots` - Progress indicator dots
- `FeedbackPanel` - Correct/incorrect feedback
- `OptionButton` - Answer option with states
- `HintPanel` - Collapsible hint
- `ActionButton` - Primary action button
- `ResultsSummary` - End-of-step results

**Colors** (`@/lib/lessons/styles`):
- `colors.feedback`, `colors.option`, `colors.progressDot`, `colors.gradient`, `colors.hint`

### Canonical Examples

- `components/lessons/m1/completar-cuadrado/Step4Classify.tsx`
- `components/lessons/m1/completar-cuadrado/Step5Practice.tsx`

---

## Final Checklist

- [ ] Phase 1 thinking completed
- [ ] All 6 step components created
- [ ] index.ts exports all steps
- [ ] page.tsx with LessonShell
- [ ] Lesson registered in types
- [ ] All 5 rules verified
- [ ] No anti-patterns
- [ ] All quality gates passed
- [ ] Spanish throughout
- [ ] No errors
