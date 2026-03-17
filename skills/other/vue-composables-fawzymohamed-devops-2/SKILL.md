---
name: vue-composables
description: Patterns for Vue 3 composables with localStorage persistence in Nuxt 4. Activate when creating composables, working with useProgress, useQuiz, useCertificate, or localStorage.
---

# Vue Composables Patterns (Nuxt 4)

## Activation Triggers
- Creating new composables in `app/composables/` directory
- Working with reactive state management
- Implementing localStorage persistence
- Building useProgress, useQuiz, or useCertificate

## Nuxt 4 Composables Location

```
app/
└── composables/
    ├── useProgress.ts
    ├── useQuiz.ts
    └── useCertificate.ts
```

## Composable Structure Template

```typescript
// app/composables/useExample.ts
import { ref, computed, readonly } from 'vue'

export function useExample() {
  // Private state
  const _state = ref<StateType>(initialValue)

  // Computed values
  const derivedValue = computed(() => {
    return _state.value.something
  })

  // Actions
  function doSomething(param: ParamType) {
    _state.value = // update logic
  }

  // Return public API
  return {
    state: readonly(_state),  // Prevent external mutation
    derivedValue,
    doSomething
  }
}
```

## useProgress Implementation

```typescript
// app/composables/useProgress.ts
import type { UserProgress, SubtopicProgress } from '~/data/types'

const STORAGE_KEY = 'devops-lms-progress'

export function useProgress() {
  // Use useState for cross-component reactivity (SSR-safe)
  const progress = useState<UserProgress>('user-progress', () => {
    return loadFromStorage() ?? createDefaultProgress()
  })

  // Load from localStorage (client-side only)
  function loadFromStorage(): UserProgress | null {
    if (typeof window === 'undefined') return null
    try {
      const stored = localStorage.getItem(STORAGE_KEY)
      return stored ? JSON.parse(stored) : null
    } catch (e) {
      console.warn('Failed to load progress from localStorage', e)
      return null
    }
  }

  // Create default progress structure
  function createDefaultProgress(): UserProgress {
    return {
      startedAt: new Date().toISOString(),
      phases: {}
    }
  }

  // Save to localStorage
  function saveToStorage() {
    if (typeof window === 'undefined') return
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(progress.value))
    } catch (e) {
      console.warn('Failed to save progress to localStorage', e)
    }
  }

  // Ensure nested structure exists
  function ensureStructure(phaseId: string, topicId: string) {
    if (!progress.value.phases[phaseId]) {
      progress.value.phases[phaseId] = { topics: {} }
    }
    if (!progress.value.phases[phaseId].topics[topicId]) {
      progress.value.phases[phaseId].topics[topicId] = { subtopics: {} }
    }
  }

  // Mark a subtopic as complete
  function markComplete(phaseId: string, topicId: string, subtopicId: string) {
    ensureStructure(phaseId, topicId)
    
    progress.value.phases[phaseId].topics[topicId].subtopics[subtopicId] = {
      completed: true,
      completedAt: new Date().toISOString(),
      quizScore: null
    }
    
    saveToStorage()
  }

  // Record quiz score
  function recordQuizScore(
    phaseId: string, 
    topicId: string, 
    subtopicId: string, 
    score: number
  ) {
    ensureStructure(phaseId, topicId)
    
    const subtopic = progress.value.phases[phaseId].topics[topicId].subtopics[subtopicId]
    if (subtopic) {
      subtopic.quizScore = score
      subtopic.quizCompletedAt = new Date().toISOString()
    } else {
      progress.value.phases[phaseId].topics[topicId].subtopics[subtopicId] = {
        completed: false,
        completedAt: null,
        quizScore: score,
        quizCompletedAt: new Date().toISOString()
      }
    }
    
    saveToStorage()
  }

  // Check if specific item is complete
  function isComplete(phaseId: string, topicId?: string, subtopicId?: string): boolean {
    if (!topicId) {
      // Check entire phase
      const phase = progress.value.phases[phaseId]
      if (!phase) return false
      // Would need roadmap data to check all topics
      return false
    }
    
    if (!subtopicId) {
      // Check entire topic
      const topic = progress.value.phases[phaseId]?.topics[topicId]
      if (!topic) return false
      // Would need roadmap data to check all subtopics
      return false
    }
    
    // Check specific subtopic
    return !!progress.value.phases[phaseId]?.topics[topicId]?.subtopics[subtopicId]?.completed
  }

  // Get completion count
  function getCompletedCount(): number {
    let count = 0
    for (const phase of Object.values(progress.value.phases)) {
      for (const topic of Object.values(phase.topics)) {
        for (const subtopic of Object.values(topic.subtopics)) {
          if (subtopic.completed) count++
        }
      }
    }
    return count
  }

  // Export/Import for data portability
  function exportProgress(): string {
    return JSON.stringify(progress.value, null, 2)
  }

  function importProgress(data: string) {
    try {
      const parsed = JSON.parse(data) as UserProgress
      progress.value = parsed
      saveToStorage()
      return true
    } catch {
      return false
    }
  }

  // Reset all progress
  function resetProgress() {
    progress.value = createDefaultProgress()
    saveToStorage()
  }

  return {
    progress: readonly(progress),
    markComplete,
    recordQuizScore,
    isComplete,
    getCompletedCount,
    exportProgress,
    importProgress,
    resetProgress
  }
}
```

## useQuiz Implementation

```typescript
// app/composables/useQuiz.ts
import type { Quiz, QuizQuestion, QuizAnswer } from '~/data/types'

export function useQuiz(quiz: Ref<Quiz> | Quiz) {
  const quizData = isRef(quiz) ? quiz : ref(quiz)
  
  const currentIndex = ref(0)
  const answers = ref<QuizAnswer[]>([])
  const isComplete = ref(false)
  const score = ref(0)

  const currentQuestion = computed(() => 
    quizData.value.questions[currentIndex.value]
  )
  
  const totalQuestions = computed(() => 
    quizData.value.questions.length
  )
  
  const isLastQuestion = computed(() => 
    currentIndex.value === totalQuestions.value - 1
  )
  
  const isFirstQuestion = computed(() => 
    currentIndex.value === 0
  )

  const passed = computed(() => 
    score.value >= quizData.value.passingScore
  )

  function submitAnswer(selected: string | string[] | boolean) {
    answers.value[currentIndex.value] = {
      questionIndex: currentIndex.value,
      selected
    }
  }

  function nextQuestion() {
    if (!isLastQuestion.value) {
      currentIndex.value++
    }
  }

  function previousQuestion() {
    if (!isFirstQuestion.value) {
      currentIndex.value--
    }
  }

  function goToQuestion(index: number) {
    if (index >= 0 && index < totalQuestions.value) {
      currentIndex.value = index
    }
  }

  function finishQuiz() {
    score.value = calculateScore()
    isComplete.value = true
  }

  function calculateScore(): number {
    let correct = 0
    
    answers.value.forEach((answer, index) => {
      const question = quizData.value.questions[index]
      if (isAnswerCorrect(answer, question)) {
        correct++
      }
    })
    
    return Math.round((correct / totalQuestions.value) * 100)
  }

  function isAnswerCorrect(answer: QuizAnswer, question: QuizQuestion): boolean {
    if (!answer) return false
    
    switch (question.type) {
      case 'single':
        return answer.selected === question.correctAnswer
      
      case 'multiple':
        const selected = answer.selected as string[]
        const correct = question.correctAnswers!
        return (
          selected.length === correct.length &&
          selected.every(s => correct.includes(s))
        )
      
      case 'true-false':
        return answer.selected === question.correctAnswer
      
      default:
        return false
    }
  }

  function getAnswerForQuestion(index: number): QuizAnswer | undefined {
    return answers.value[index]
  }

  function reset() {
    currentIndex.value = 0
    answers.value = []
    isComplete.value = false
    score.value = 0
  }

  return {
    // State (readonly)
    currentIndex: readonly(currentIndex),
    currentQuestion,
    totalQuestions,
    isLastQuestion,
    isFirstQuestion,
    answers: readonly(answers),
    isComplete: readonly(isComplete),
    score: readonly(score),
    passed,
    
    // Actions
    submitAnswer,
    nextQuestion,
    previousQuestion,
    goToQuestion,
    finishQuiz,
    getAnswerForQuestion,
    reset
  }
}
```

## useCertificate Implementation

```typescript
// app/composables/useCertificate.ts
import type { CertificateData } from '~/data/types'

export function useCertificate() {
  const isGenerating = ref(false)
  const error = ref<string | null>(null)

  function generateCertificateId(): string {
    const timestamp = Date.now().toString(36)
    const random = Math.random().toString(36).substring(2, 8)
    return `DEVOPS-${timestamp}-${random}`.toUpperCase()
  }

  function calculateTotalHours(completedLessons: number): number {
    // Assuming average 15 minutes per lesson
    return Math.round((completedLessons * 15) / 60)
  }

  async function generatePDF(data: CertificateData): Promise<Blob | null> {
    if (typeof window === 'undefined') return null
    
    isGenerating.value = true
    error.value = null
    
    try {
      // Dynamic imports for client-side only
      const [{ default: html2canvas }, { default: jsPDF }] = await Promise.all([
        import('html2canvas'),
        import('jspdf')
      ])
      
      const element = document.getElementById('certificate-preview')
      if (!element) {
        throw new Error('Certificate element not found')
      }
      
      const canvas = await html2canvas(element, {
        scale: 2,
        backgroundColor: '#1f2937'
      })
      
      const imgData = canvas.toDataURL('image/png')
      const pdf = new jsPDF({
        orientation: 'landscape',
        unit: 'mm',
        format: 'a4'
      })
      
      const imgWidth = 297 // A4 landscape width
      const imgHeight = (canvas.height * imgWidth) / canvas.width
      
      pdf.addImage(imgData, 'PNG', 0, 0, imgWidth, imgHeight)
      
      return pdf.output('blob')
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to generate PDF'
      return null
    } finally {
      isGenerating.value = false
    }
  }

  async function downloadCertificate(data: CertificateData) {
    const blob = await generatePDF(data)
    if (!blob) return
    
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `DevOps-Certificate-${data.certificateId}.pdf`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  return {
    isGenerating: readonly(isGenerating),
    error: readonly(error),
    generateCertificateId,
    calculateTotalHours,
    generatePDF,
    downloadCertificate
  }
}
```

## SSR Compatibility Patterns

```typescript
// Always check for window/client-side
function useClientSideFeature() {
  const isClient = ref(false)
  
  onMounted(() => {
    isClient.value = true
    // Now safe to access localStorage, window, etc.
  })
  
  return { isClient }
}

// Use useState for SSR-safe shared state
const sharedState = useState('key', () => defaultValue)

// Use useAsyncData for data fetching
const { data } = await useAsyncData('key', () => fetchData())

// Lazy load client-only modules
const loadClientLib = async () => {
  if (typeof window === 'undefined') return null
  const lib = await import('client-only-lib')
  return lib
}
```

## Best Practices

1. **Always use `readonly()` for exposed state** - Prevents accidental mutations
2. **Check `typeof window` before localStorage** - Prevents SSR errors  
3. **Use `useState` for cross-component state** - Nuxt's SSR-safe alternative to global refs
4. **Wrap localStorage in try/catch** - Handles quota errors and private browsing
5. **Provide TypeScript types for all returns** - Better DX and error catching
6. **Use `isRef` to handle both ref and raw values** - More flexible composable APIs
7. **Dynamic imports for browser-only libs** - html2canvas, jsPDF, etc.
