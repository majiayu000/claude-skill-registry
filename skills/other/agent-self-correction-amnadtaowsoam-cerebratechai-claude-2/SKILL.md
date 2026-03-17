---
name: Agent Self-Correction
description: AI agent self-correction mechanisms: error detection, validation loops, recovery strategies, confidence scoring, and iterative refinement
---

# Agent Self-Correction

## Overview

AI agent self-correction mechanisms enable agents to detect errors, validate outputs, and automatically recover from failures. This includes validation loops, confidence scoring, iterative refinement, and recovery strategies to improve reliability.

## Why This Matters

- **Reliability**: Agents แก้ error ได้เองโดยไม่ต้อง human intervention
- **Quality**: Output มีคุณภาพสูงขึ้น
- **Trust**: Users มั่นใจในผลลัพธ์ที่ได้
- **Efficiency**: ลด retry loops ที่ไม่จำเป็น

---

## Core Concepts

### 1. Error Detection

```typescript
interface ErrorDetection {
  type: 'syntax' | 'semantic' | 'logic' | 'format'
  severity: 'low' | 'medium' | 'high' | 'critical'
  message: string
  location?: string
}

class ErrorDetector {
  detectErrors(output: string, context: any): ErrorDetection[] {
    const errors: ErrorDetection[] = []

    // Syntax errors
    errors.push(...this.detectSyntaxErrors(output))

    // Semantic errors
    errors.push(...this.detectSemanticErrors(output, context))

    // Logic errors
    errors.push(...this.detectLogicErrors(output, context))

    // Format errors
    errors.push(...this.detectFormatErrors(output, context))

    return errors
  }

  private detectSyntaxErrors(output: string): ErrorDetection[] {
    const errors: ErrorDetection[] = []

    // Check for unclosed brackets
    const openBrackets = (output.match(/\(/g) || []).length
    const closeBrackets = (output.match(/\)/g) || []).length
    if (openBrackets !== closeBrackets) {
      errors.push({
        type: 'syntax',
        severity: 'high',
        message: 'Unclosed brackets detected',
      })
    }

    // Check for unclosed quotes
    const quotes = output.match(/"/g)
    if (quotes && quotes.length % 2 !== 0) {
      errors.push({
        type: 'syntax',
        severity: 'high',
        message: 'Unclosed quotes detected',
      })
    }

    return errors
  }

  private detectSemanticErrors(output: string, context: any): ErrorDetection[] {
    const errors: ErrorDetection[] = []

    // Check for hallucinations (if context provided)
    if (context.facts) {
      const outputFacts = this.extractFacts(output)
      for (const fact of outputFacts) {
        if (!context.facts.includes(fact)) {
          errors.push({
            type: 'semantic',
            severity: 'medium',
            message: `Potential hallucination: "${fact}" not in context`,
          })
        }
      }
    }

    return errors
  }

  private detectLogicErrors(output: string, context: any): ErrorDetection[] {
    const errors: ErrorDetection[] = []

    // Check for contradictions
    const statements = this.extractStatements(output)
    for (let i = 0; i < statements.length; i++) {
      for (let j = i + 1; j < statements.length; j++) {
        if (this.areContradictory(statements[i], statements[j])) {
          errors.push({
            type: 'logic',
            severity: 'high',
            message: 'Contradictory statements detected',
          })
        }
      }
    }

    return errors
  }

  private detectFormatErrors(output: string, context: any): ErrorDetection[] {
    const errors: ErrorDetection[] = []

    // Check if JSON is valid when expected
    if (context.expectedFormat === 'json') {
      try {
        JSON.parse(output)
      } catch (e) {
        errors.push({
          type: 'format',
          severity: 'critical',
          message: 'Invalid JSON output',
        })
      }
    }

    return errors
  }

  private extractFacts(text: string): string[] {
    // Extract factual statements
    return []
  }

  private extractStatements(text: string): string[] {
    // Extract logical statements
    return []
  }

  private areContradictory(a: string, b: string): boolean {
    // Check if two statements contradict
    return false
  }
}
```

### 2. Validation Loops

```typescript
interface ValidationResult {
  isValid: boolean
  errors: string[]
  warnings: string[]
  confidence: number
}

class ValidationLoop {
  private maxIterations: number = 3
  private confidenceThreshold: number = 0.8

  async executeWithValidation<T>(
    task: () => Promise<T>,
    validator: (result: T) => ValidationResult,
    corrector: (result: T, errors: string[]) => Promise<T>
  ): Promise<T> {
    let result = await task()
    let iteration = 0

    while (iteration < this.maxIterations) {
      const validation = validator(result)

      if (validation.isValid && validation.confidence >= this.confidenceThreshold) {
        return result
      }

      console.log(`Iteration ${iteration + 1}: Validation failed`)
      console.log('Errors:', validation.errors)
      console.log('Warnings:', validation.warnings)
      console.log('Confidence:', validation.confidence)

      // Correct the result
      result = await corrector(result, validation.errors)
      iteration++
    }

    throw new Error(`Validation failed after ${this.maxIterations} iterations`)
  }
}

// Usage
const loop = new ValidationLoop()

const result = await loop.executeWithValidation(
  // Task: Generate code
  async () => {
    return await llm.generate('Write a function to sort an array')
  },
  // Validator: Check code quality
  (code: string) => {
    const errors: string[] = []
    const warnings: string[] = []
    let confidence = 1.0

    // Check for syntax errors
    try {
      // Validate syntax
    } catch (e) {
      errors.push('Syntax error')
      confidence -= 0.5
    }

    // Check for best practices
    if (!code.includes('error handling')) {
      warnings.push('Missing error handling')
      confidence -= 0.1
    }

    return {
      isValid: errors.length === 0,
      errors,
      warnings,
      confidence,
    }
  },
  // Corrector: Fix issues
  async (code: string, errors: string[]) => {
    const prompt = `Fix the following issues in this code:
Code: ${code}
Issues: ${errors.join(', ')}
Return the corrected code only.`
    return await llm.generate(prompt)
  }
)
```

### 3. Confidence Scoring

```typescript
interface ConfidenceMetrics {
  overall: number
  components: {
    syntax: number
    semantic: number
    logic: number
    completeness: number
  }
  reasoning: string[]
}

class ConfidenceScorer {
  calculateConfidence(output: string, context: any): ConfidenceMetrics {
    const components = {
      syntax: this.scoreSyntax(output),
      semantic: this.scoreSemantic(output, context),
      logic: this.scoreLogic(output, context),
      completeness: this.scoreCompleteness(output, context),
    }

    const overall = (
      components.syntax * 0.2 +
      components.semantic * 0.3 +
      components.logic * 0.3 +
      components.completeness * 0.2
    )

    const reasoning = this.generateReasoning(components)

    return { overall, components, reasoning }
  }

  private scoreSyntax(output: string): number {
    let score = 1.0

    // Check for balanced brackets
    const brackets = output.match(/[(){}\[\]]/g) || []
    let balance = 0
    for (const bracket of brackets) {
      if (['(', '{', '['].includes(bracket)) {
        balance++
      } else {
        balance--
      }
      if (balance < 0) {
        score -= 0.3
      }
    }
    if (balance !== 0) {
      score -= 0.3
    }

    // Check for proper punctuation
    if (output.endsWith('.') || output.endsWith(',')) {
      score += 0.1
    }

    return Math.max(0, Math.min(1, score))
  }

  private scoreSemantic(output: string, context: any): number {
    let score = 1.0

    // Check for consistency with context
    if (context.keywords) {
      const outputKeywords = output.toLowerCase().split(/\s+/)
      const matchedKeywords = context.keywords.filter((k: string) =>
        outputKeywords.includes(k.toLowerCase())
      )
      score = matchedKeywords.length / context.keywords.length
    }

    return score
  }

  private scoreLogic(output: string, context: any): number {
    let score = 1.0

    // Check for logical flow
    const sentences = output.split(/[.!?]/).filter(s => s.trim())
    if (sentences.length < 2) {
      score -= 0.2
    }

    // Check for contradictions
    // (implementation depends on domain)

    return Math.max(0, Math.min(1, score))
  }

  private scoreCompleteness(output: string, context: any): number {
    let score = 1.0

    // Check if all required elements are present
    if (context.requiredElements) {
      const present = context.requiredElements.filter((e: string) =>
        output.includes(e)
      )
      score = present.length / context.requiredElements.length
    }

    // Check output length
    if (context.minLength && output.length < context.minLength) {
      score -= 0.3
    }
    if (context.maxLength && output.length > context.maxLength) {
      score -= 0.3
    }

    return Math.max(0, Math.min(1, score))
  }

  private generateReasoning(components: any): string[] {
    const reasoning: string[] = []

    if (components.syntax < 0.8) {
      reasoning.push('Syntax issues detected')
    }
    if (components.semantic < 0.8) {
      reasoning.push('Semantic inconsistencies found')
    }
    if (components.logic < 0.8) {
      reasoning.push('Logical flow could be improved')
    }
    if (components.completeness < 0.8) {
      reasoning.push('Response may be incomplete')
    }

    return reasoning
  }
}
```

### 4. Recovery Strategies

```typescript
interface RecoveryStrategy {
  name: string
  canHandle: (error: Error) => boolean
  recover: (error: Error, context: any) => Promise<any>
}

class RecoveryManager {
  private strategies: RecoveryStrategy[] = []

  addStrategy(strategy: RecoveryStrategy): void {
    this.strategies.push(strategy)
  }

  async recover(error: Error, context: any): Promise<any> {
    for (const strategy of this.strategies) {
      if (strategy.canHandle(error)) {
        console.log(`Applying recovery strategy: ${strategy.name}`)
        return await strategy.recover(error, context)
      }
    }

    throw new Error(`No recovery strategy found for error: ${error.message}`)
  }
}

// Common recovery strategies
const recoveryManager = new RecoveryManager()

// Retry strategy
recoveryManager.addStrategy({
  name: 'retry',
  canHandle: (error) => error instanceof NetworkError,
  recover: async (error, context) => {
    await sleep(1000) // Exponential backoff
    return context.task()
  },
})

// Fallback strategy
recoveryManager.addStrategy({
  name: 'fallback',
  canHandle: (error) => error instanceof APIError,
  recover: async (error, context) => {
    return context.fallbackValue
  },
})

// Rephrase strategy
recoveryManager.addStrategy({
  name: 'rephrase',
  canHandle: (error) => error instanceof ValidationError,
  recover: async (error, context) => {
    const rephrased = await llm.generate(
      `Rephrase this request to be clearer: ${context.originalRequest}`
    )
    return await context.task(rephrased)
  },
})

// Simplify strategy
recoveryManager.addStrategy({
  name: 'simplify',
  canHandle: (error) => error instanceof ComplexityError,
  recover: async (error, context) => {
    const simplified = await llm.generate(
      `Simplify this request: ${context.originalRequest}`
    )
    return await context.task(simplified)
  },
})
```

### 5. Iterative Refinement

```typescript
class IterativeRefiner {
  private maxIterations: number = 5
  private improvementThreshold: number = 0.1

  async refine<T>(
    initial: T,
    evaluator: (item: T) => number,
    refiner: (item: T, feedback: string) => Promise<T>
  ): Promise<T> {
    let current = initial
    let currentScore = evaluator(current)
    let iteration = 0

    while (iteration < this.maxIterations) {
      const feedback = this.generateFeedback(current, currentScore)
      const refined = await refiner(current, feedback)
      const refinedScore = evaluator(refined)

      const improvement = (refinedScore - currentScore) / currentScore

      console.log(`Iteration ${iteration + 1}:`)
      console.log(`  Current score: ${currentScore}`)
      console.log(`  Refined score: ${refinedScore}`)
      console.log(`  Improvement: ${(improvement * 100).toFixed(2)}%`)

      if (improvement < this.improvementThreshold) {
        console.log('Improvement below threshold, stopping')
        break
      }

      current = refined
      currentScore = refinedScore
      iteration++
    }

    return current
  }

  private generateFeedback<T>(item: T, score: number): string {
    const feedback: string[] = []

    if (score < 0.5) {
      feedback.push('Significant improvements needed')
    } else if (score < 0.8) {
      feedback.push('Moderate improvements needed')
    } else {
      feedback.push('Minor improvements possible')
    }

    // Add specific feedback based on item type
    // (implementation depends on domain)

    return feedback.join('. ')
  }
}

// Usage
const refiner = new IterativeRefiner()

const refinedCode = await refiner.refine(
  initialCode,
  // Evaluator: Code quality score
  (code: string) => {
    let score = 1.0

    // Check for error handling
    if (code.includes('try') && code.includes('catch')) {
      score += 0.2
    }

    // Check for comments
    if (code.includes('//') || code.includes('/*')) {
      score += 0.1
    }

    // Check for tests
    if (code.includes('test') || code.includes('spec')) {
      score += 0.1
    }

    return Math.min(1, score)
  },
  // Refiner: Improve code
  async (code: string, feedback: string) => {
    const prompt = `Improve this code based on feedback:
Code: ${code}
Feedback: ${feedback}
Return the improved code only.`
    return await llm.generate(prompt)
  }
)
```

### 6. Self-Reflection

```typescript
interface ReflectionResult {
  success: boolean
  confidence: number
  issues: string[]
  improvements: string[]
}

class SelfReflectiveAgent {
  async execute(task: string): Promise<string> {
    // Execute task
    const output = await this.generateOutput(task)

    // Reflect on output
    const reflection = await this.reflect(output, task)

    // If issues found, refine
    if (!reflection.success || reflection.confidence < 0.8) {
      console.log('Self-reflection detected issues, refining...')
      return await this.refine(output, reflection.issues)
    }

    return output
  }

  private async generateOutput(task: string): Promise<string> {
    // Generate initial output
    return await llm.generate(task)
  }

  private async reflect(output: string, task: string): Promise<ReflectionResult> {
    const prompt = `Reflect on this output for the given task:
Task: ${task}
Output: ${output}

Evaluate:
1. Does the output address the task?
2. Is the output complete?
3. Is the output accurate?
4. Are there any issues?

Return JSON with: success, confidence, issues, improvements`

    const reflection = await llm.generate(prompt)
    return JSON.parse(reflection)
  }

  private async refine(output: string, issues: string[]): Promise<string> {
    const prompt = `Refine this output to address the following issues:
Output: ${output}
Issues: ${issues.join(', ')}

Return the refined output only.`
    return await llm.generate(prompt)
  }
}
```

## Quick Start

```typescript
// 1. Set up error detection
const detector = new ErrorDetector()

// 2. Set up validation loop
const loop = new ValidationLoop()

// 3. Execute with self-correction
const result = await loop.executeWithValidation(
  () => llm.generate(task),
  (output) => {
    const errors = detector.detectErrors(output, context)
    return {
      isValid: errors.length === 0,
      errors: errors.map(e => e.message),
      warnings: [],
      confidence: 1.0 - (errors.length * 0.2),
    }
  },
  (output, errors) => llm.generate(`Fix: ${errors.join(', ')}\nOutput: ${output}`)
)
```

## Production Checklist

- [ ] Error detection implemented
- [ ] Validation loops configured
- [ ] Confidence scoring enabled
- [ ] Recovery strategies defined
- [ ] Iterative refinement active
- [ ] Self-reflection enabled
- [ ] Monitoring/logging in place
- [ ] Fallback mechanisms defined

## Anti-patterns

1. **No error detection**: ไม่ตรวจสอบผลลัพธ์
2. **Infinite loops**: Validation loops ไม่มี max iterations
3. **Over-correction**: แก้ปัญหาจนเกินไป
4. **No fallback**: ไม่มี strategy สำรองเมื่อ recovery ล้มเหลว
5. **Ignoring confidence**: ไม่สนใจ confidence scores

## Integration Points

- LLM APIs
- Monitoring systems
- Logging frameworks
- Alerting systems
- Feedback loops

## Further Reading

- [Self-Correction in LLMs](https://arxiv.org/abs/2303.05198)
- [Chain of Thought Prompting](https://arxiv.org/abs/2201.11903)
- [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)
- [Self-Consistency](https://arxiv.org/abs/2203.11171)
