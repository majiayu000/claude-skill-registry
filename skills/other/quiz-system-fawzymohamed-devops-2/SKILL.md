---
name: quiz-system
description: Knowledge for implementing the LMS quiz system with Nuxt UI. Activate when working with quiz components, question types, scoring, or quiz-related composables.
---

# Quiz System Implementation

## Activation Triggers
- Creating quiz components
- Working with question types
- Implementing scoring logic
- Building QuizContainer, QuizQuestion, QuizResults

## TypeScript Interfaces

```typescript
// app/data/types.ts

export interface QuizQuestion {
  question: string
  type: 'single' | 'multiple' | 'true-false'
  options?: string[]
  correctAnswer?: string | boolean
  correctAnswers?: string[]
  explanation: string
}

export interface Quiz {
  passingScore: number  // Percentage (0-100)
  questions: QuizQuestion[]
}

export interface QuizAnswer {
  questionIndex: number
  selected: string | string[] | boolean
}

export interface QuizState {
  currentIndex: number
  answers: QuizAnswer[]
  isComplete: boolean
  score: number
  passed: boolean
}
```

## Question Types in Markdown

### Single Choice
```yaml
- question: "Which command lists files in Linux?"
  type: single
  options: ["ls", "cd", "pwd", "rm"]
  correctAnswer: "ls"
  explanation: "The 'ls' command lists directory contents."
```

### Multiple Choice
```yaml
- question: "Which are valid Linux distributions? (Select all)"
  type: multiple
  options: ["Ubuntu", "Windows Server", "Fedora", "macOS", "Debian"]
  correctAnswers: ["Ubuntu", "Fedora", "Debian"]
  explanation: "Ubuntu, Fedora, and Debian are Linux distributions."
```

### True/False
```yaml
- question: "Git is a distributed version control system."
  type: true-false
  correctAnswer: true
  explanation: "Git is indeed a distributed VCS."
```

## Component Implementation

### QuizContainer.vue

```vue
<script setup lang="ts">
import type { Quiz } from '~/data/types'

const props = defineProps<{
  quiz: Quiz
}>()

const emit = defineEmits<{
  (e: 'complete', score: number, passed: boolean): void
}>()

const {
  currentQuestion,
  currentIndex,
  totalQuestions,
  isLastQuestion,
  isFirstQuestion,
  isComplete,
  score,
  passed,
  answers,
  submitAnswer,
  nextQuestion,
  previousQuestion,
  finishQuiz,
  getAnswerForQuestion,
  reset
} = useQuiz(props.quiz)

// Track selected answer for current question
const selectedAnswer = ref<string | string[] | boolean | null>(null)

// Initialize selected from previous answers
watch(currentIndex, (newIndex) => {
  const previous = getAnswerForQuestion(newIndex)
  selectedAnswer.value = previous?.selected ?? null
}, { immediate: true })

function handleNext() {
  if (selectedAnswer.value !== null) {
    submitAnswer(selectedAnswer.value)
  }
  
  if (isLastQuestion.value) {
    finishQuiz()
    emit('complete', score.value, passed.value)
  } else {
    nextQuestion()
    selectedAnswer.value = null
  }
}

function handleRetry() {
  reset()
  selectedAnswer.value = null
}
</script>

<template>
  <UCard>
    <!-- Quiz Header -->
    <template #header>
      <div class="flex items-center justify-between">
        <h3 class="font-semibold">Quiz</h3>
        <UBadge variant="soft">
          Question {{ currentIndex + 1 }} of {{ totalQuestions }}
        </UBadge>
      </div>
      <UProgress 
        :value="((currentIndex + 1) / totalQuestions) * 100" 
        class="mt-3"
        size="sm"
      />
    </template>

    <!-- Question (Active Quiz) -->
    <div v-if="!isComplete">
      <QuizQuestion
        :question="currentQuestion"
        v-model="selectedAnswer"
      />
    </div>

    <!-- Results -->
    <QuizResults
      v-else
      :score="score"
      :passed="passed"
      :passing-score="quiz.passingScore"
      :questions="quiz.questions"
      :answers="answers"
    />

    <!-- Footer Actions -->
    <template #footer>
      <div class="flex justify-between">
        <UButton
          v-if="!isComplete"
          variant="outline"
          :disabled="isFirstQuestion"
          @click="previousQuestion"
          class="cursor-pointer"
        >
          <UIcon name="i-heroicons-arrow-left" class="w-4 h-4 mr-2" />
          Previous
        </UButton>
        <div v-else />

        <UButton
          v-if="!isComplete"
          :disabled="selectedAnswer === null"
          @click="handleNext"
          class="cursor-pointer"
        >
          {{ isLastQuestion ? 'Finish Quiz' : 'Next' }}
          <UIcon name="i-heroicons-arrow-right" class="w-4 h-4 ml-2" />
        </UButton>
        
        <UButton
          v-else
          @click="handleRetry"
          class="cursor-pointer"
        >
          <UIcon name="i-heroicons-arrow-path" class="w-4 h-4 mr-2" />
          Try Again
        </UButton>
      </div>
    </template>
  </UCard>
</template>
```

### QuizQuestion.vue

```vue
<script setup lang="ts">
import type { QuizQuestion } from '~/data/types'

const props = defineProps<{
  question: QuizQuestion
}>()

const model = defineModel<string | string[] | boolean | null>()

// For multiple choice, manage array
const multipleSelected = computed({
  get: () => (model.value as string[]) || [],
  set: (val) => { model.value = val }
})

function toggleMultiple(option: string) {
  const current = [...multipleSelected.value]
  const index = current.indexOf(option)
  if (index > -1) {
    current.splice(index, 1)
  } else {
    current.push(option)
  }
  multipleSelected.value = current
}

function isSelected(option: string): boolean {
  if (props.question.type === 'multiple') {
    return multipleSelected.value.includes(option)
  }
  return model.value === option
}
</script>

<template>
  <div class="space-y-6">
    <!-- Question Text -->
    <h4 class="text-lg font-medium text-gray-100">
      {{ question.question }}
    </h4>

    <!-- Single Choice Options -->
    <div v-if="question.type === 'single'" class="space-y-3">
      <div
        v-for="option in question.options"
        :key="option"
        class="flex items-center gap-3 p-4 rounded-lg border cursor-pointer transition-all"
        :class="[
          model === option 
            ? 'border-primary-500 bg-primary-500/10' 
            : 'border-gray-700 hover:border-gray-600'
        ]"
        @click="model = option"
      >
        <div 
          class="w-5 h-5 rounded-full border-2 flex items-center justify-center flex-shrink-0"
          :class="model === option ? 'border-primary-500' : 'border-gray-600'"
        >
          <div 
            v-if="model === option" 
            class="w-2.5 h-2.5 rounded-full bg-primary-500"
          />
        </div>
        <span class="text-gray-200">{{ option }}</span>
      </div>
    </div>

    <!-- Multiple Choice Options -->
    <div v-else-if="question.type === 'multiple'" class="space-y-3">
      <p class="text-sm text-gray-400">Select all that apply</p>
      <div
        v-for="option in question.options"
        :key="option"
        class="flex items-center gap-3 p-4 rounded-lg border cursor-pointer transition-all"
        :class="[
          isSelected(option)
            ? 'border-primary-500 bg-primary-500/10' 
            : 'border-gray-700 hover:border-gray-600'
        ]"
        @click="toggleMultiple(option)"
      >
        <UCheckbox 
          :model-value="isSelected(option)"
          @update:model-value="toggleMultiple(option)"
        />
        <span class="text-gray-200">{{ option }}</span>
      </div>
    </div>

    <!-- True/False Options -->
    <div v-else-if="question.type === 'true-false'" class="flex gap-4">
      <UButton
        :variant="model === true ? 'solid' : 'outline'"
        :color="model === true ? 'success' : 'secondary'"
        size="lg"
        class="flex-1 cursor-pointer"
        @click="model = true"
      >
        <UIcon name="i-heroicons-check" class="w-5 h-5 mr-2" />
        True
      </UButton>
      <UButton
        :variant="model === false ? 'solid' : 'outline'"
        :color="model === false ? 'error' : 'secondary'"
        size="lg"
        class="flex-1 cursor-pointer"
        @click="model = false"
      >
        <UIcon name="i-heroicons-x-mark" class="w-5 h-5 mr-2" />
        False
      </UButton>
    </div>
  </div>
</template>
```

### QuizResults.vue

```vue
<script setup lang="ts">
import type { QuizQuestion, QuizAnswer } from '~/data/types'

const props = defineProps<{
  score: number
  passed: boolean
  passingScore: number
  questions: QuizQuestion[]
  answers: QuizAnswer[]
}>()

function getAnswerStatus(index: number): 'correct' | 'incorrect' | 'unanswered' {
  const answer = props.answers[index]
  const question = props.questions[index]
  
  if (!answer) return 'unanswered'
  
  if (question.type === 'multiple') {
    const selected = answer.selected as string[]
    const correct = question.correctAnswers!
    const isCorrect = selected.length === correct.length && 
      selected.every(s => correct.includes(s))
    return isCorrect ? 'correct' : 'incorrect'
  }
  
  return answer.selected === question.correctAnswer ? 'correct' : 'incorrect'
}
</script>

<template>
  <div class="space-y-6">
    <!-- Score Display -->
    <div class="text-center py-6">
      <div 
        class="inline-flex items-center justify-center w-24 h-24 rounded-full mb-4"
        :class="passed ? 'bg-success-500/20' : 'bg-error-500/20'"
      >
        <span 
          class="text-3xl font-bold"
          :class="passed ? 'text-success-500' : 'text-error-500'"
        >
          {{ score }}%
        </span>
      </div>
      
      <h3 class="text-xl font-semibold mb-2">
        {{ passed ? 'Congratulations!' : 'Keep Learning!' }}
      </h3>
      
      <p class="text-gray-400">
        {{ passed 
          ? 'You passed the quiz!' 
          : `You need ${passingScore}% to pass. Try again!` 
        }}
      </p>
    </div>

    <!-- Question Review -->
    <div class="space-y-4">
      <h4 class="font-medium text-gray-300">Review Your Answers</h4>
      
      <div 
        v-for="(question, index) in questions" 
        :key="index"
        class="p-4 rounded-lg border"
        :class="[
          getAnswerStatus(index) === 'correct' 
            ? 'border-success-500/50 bg-success-500/5' 
            : 'border-error-500/50 bg-error-500/5'
        ]"
      >
        <div class="flex items-start gap-3">
          <UIcon 
            :name="getAnswerStatus(index) === 'correct' 
              ? 'i-heroicons-check-circle-solid' 
              : 'i-heroicons-x-circle-solid'"
            class="w-5 h-5 flex-shrink-0 mt-0.5"
            :class="getAnswerStatus(index) === 'correct' 
              ? 'text-success-500' 
              : 'text-error-500'"
          />
          <div class="flex-1 min-w-0">
            <p class="font-medium text-gray-200 mb-2">{{ question.question }}</p>
            
            <p class="text-sm text-gray-400">
              Your answer: 
              <span :class="getAnswerStatus(index) === 'correct' ? 'text-success-400' : 'text-error-400'">
                {{ answers[index]?.selected ?? 'Not answered' }}
              </span>
            </p>
            
            <p v-if="getAnswerStatus(index) !== 'correct'" class="text-sm text-gray-400">
              Correct answer: 
              <span class="text-success-400">
                {{ question.type === 'multiple' 
                  ? question.correctAnswers?.join(', ') 
                  : question.correctAnswer 
                }}
              </span>
            </p>
            
            <p class="text-sm text-gray-500 mt-2 italic">
              {{ question.explanation }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
```

## Scoring Logic

```typescript
function calculateScore(answers: QuizAnswer[], questions: QuizQuestion[]): number {
  let correctCount = 0
  
  answers.forEach((answer, index) => {
    const question = questions[index]
    if (!answer) return
    
    switch (question.type) {
      case 'single':
        if (answer.selected === question.correctAnswer) {
          correctCount++
        }
        break
        
      case 'multiple':
        const selected = answer.selected as string[]
        const correct = question.correctAnswers!
        // All selected must match exactly
        if (
          selected.length === correct.length &&
          selected.every(s => correct.includes(s))
        ) {
          correctCount++
        }
        break
        
      case 'true-false':
        if (answer.selected === question.correctAnswer) {
          correctCount++
        }
        break
    }
  })
  
  return Math.round((correctCount / questions.length) * 100)
}
```

## Quiz Writing Guidelines

### CRITICAL: Content Alignment Rule

**Quiz questions MUST only test concepts explicitly covered in the lesson content.**

Before writing any quiz question:
1. ✅ Verify the concept is mentioned in the lesson text
2. ✅ Ensure the question can be answered using lesson content alone
3. ❌ Never assume knowledge of topics not covered in this specific lesson
4. ❌ Never test related concepts that "should" be known but aren't in the lesson
5. 💡 If a concept would make a good question but isn't in the lesson, add it to the lesson first

**Example of violation:** A lesson about "Design & Architecture" that doesn't mention SOLID principles should NOT have a quiz question about the Open/Closed Principle.

### Question Count Guidelines

**Dynamic question count (3-7 per lesson)** - Based on difficulty and lesson length:
| Difficulty | Est. Minutes | Questions |
|------------|--------------|-----------|
| beginner | 5-10 | 3 |
| beginner | 11-15 | 4 |
| beginner | 16+ | 5 |
| intermediate | 5-10 | 4 |
| intermediate | 11-15 | 5 |
| intermediate | 16+ | 6 |
| advanced | 5-15 | 5 |
| advanced | 16-20 | 6 |
| advanced | 21+ | 7 |

### Additional Guidelines

1. **Mix question types** - Single choice, multiple choice, true/false
2. **Test understanding, not memorization** - "Why" questions, not just "What"
3. **Provide clear explanations** - Help learners understand correct answers
4. **70% passing score** - Standard threshold
5. **Avoid trick questions** - Be straightforward and fair
6. **Natural variation** - Vary ±1 question to avoid identical counts across lessons
