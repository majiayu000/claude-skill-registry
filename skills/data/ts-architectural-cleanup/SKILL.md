---
complexity: very_high
confidence_boost:
  architectural_issues: 0.5
  code_quality_problems: 0.4
  duplicate_code: 0.6
  refactoring_needs: 0.4
dependencies:
- typescript
- vue
- pinia
- '@vue/runtime-core'
- vite
- '@babel/parser'
- '@babel/traverse'
description: COMPREHENSIVE architectural cleanup using AST analysis to detect duplicates,
  consolidate code patterns, and implement systematic refactoring strategies. Utilizes
  advanced AST parsing to identify structural issues and provides automated refactoring
  suggestions with safe transformation capabilities.
estimated_duration: 30-60 minutes
name: ts-architectural-cleanup
prerequisites:
- typescript ast
- code analysis
- refactoring patterns
- architecture principles
- babel ast parsing
skill_id: ts-architectural-cleanup
skill_name: TypeScript Architectural Cleanup Specialist
tags:
- typescript
- architectural
- cleanup
- duplicate
- refactoring
- ast
- code-quality
- consolidation
token_budget: 5000
triggers:
  contexts:
  - typescript
  - architecture
  - cleanup
  - refactoring
  - code quality
  - duplicate detection
  - ast analysis
  file_patterns:
  - src/**/*.ts
  - src/**/*.vue
  - tsconfig.json
  - package.json
  keywords:
  - duplicate
  - cleanup
  - architectural
  - refactor
  - consolidate
  - code quality
  - ast
  - pattern detection
  - duplicate method
  - duplicate function
  - duplicate interface
version: 1.0
---

# TypeScript Architectural Cleanup Specialist

This skill provides comprehensive architectural cleanup and duplicate detection using advanced AST analysis and systematic refactoring strategies.

## Quick Context
- **Complexity**: very_high
- **Duration**: 30-60 minutes
- **Dependencies**: typescript, vue, pinia, @vue/runtime-core, vite, @babel/parser, @babel/traverse

## Activation Triggers
- **Keywords**: duplicate, cleanup, architectural, refactor, consolidate, code quality
- **Files**: src/**/*.ts, src/**/*.vue, architectural files
- **Contexts**: typescript, architecture, cleanup, refactoring, duplicate detection

## 🚨 CRITICAL ARCHITECTURAL ISSUES

### **IMMEDIATE Cleanup Needs**
**CURRENT ARCHITECTURAL PROBLEMS:**
1. **17,393 occurrences of anti-patterns** across 3,614 files (research findings)
2. **Duplicate method declarations** causing compilation failures
3. **Inconsistent patterns** across similar components
4. **Code duplication** in calendar composables and utility functions
5. **Architectural inconsistencies** in store patterns and component structure

### **Why Architectural Cleanup is Critical:**
```
// PROBLEM: Duplicate methods causing compilation errors
const getTask = (taskId: string): Task | undefined => { /* ... */ }
const getTask = (taskId: string): Task | undefined => { /* ... */ }  // ❌ Duplicate

// CONSEQUENCE: Application fails to compile, confusing error messages
// Development experience suffers, onboarding becomes difficult
```

## Architectural Cleanup Process

### Phase 1: AST Analysis & Duplicate Detection (Critical)
```typescript
// AST-based duplicate detection system
interface DuplicateAnalysis {
  file: string
  duplicates: Array<{
    type: 'function' | 'class' | 'interface' | 'variable'
    name: string
    occurrences: Array<{
      line: number
      column: number
      signature: string
      confidence: number
    }>
    suggestedAction: 'remove' | 'merge' | 'refactor' | 'consolidate'
  }>
}

export class ArchitecturalAnalyzer {
  private astCache = new Map<string, ESTree.Program>()
  private duplicateThreshold = 0.8 // 80% similarity threshold

  async analyzeCodebase(): Promise<DuplicateAnalysis[]> {
    const files = await this.getTypeScriptFiles()
    const analyses: DuplicateAnalysis[] = []

    for (const file of files) {
      const analysis = await this.analyzeFile(file)
      analyses.push(analysis)
    }

    return analyses
  }

  private async analyzeFile(filePath: string): Promise<DuplicateAnalysis> {
    const ast = await this.parseFile(filePath)
    const duplicates = await this.detectDuplicates(ast)

    return {
      file: filePath,
      duplicates
    }
  }

  private async detectDuplicates(ast: ESTree.Program) {
    // Implementation using AST traversal
    // Detects duplicate functions, classes, interfaces, variables
  }
}
```

### Phase 2: Pattern Recognition & Consolidation (Critical)
```typescript
// Pattern recognition for architectural improvements
export interface CodePattern {
  name: string
  description: string
  detection: (ast: ESTree.Program) => boolean
  refactoring: (ast: ESTree.Program) => ESTree.Program
  priority: 'high' | 'medium' | 'low'
}

export class PatternRecognizer {
  private patterns: CodePattern[] = [
    {
      name: 'Duplicate Store Methods',
      description: 'Identifies duplicate methods in Pinia stores',
      detection: this.detectDuplicateStoreMethods,
      refactoring: this.consolidateStoreMethods,
      priority: 'high'
    },
    {
      name: 'Similar Component Logic',
      description: 'Finds similar logic patterns across Vue components',
      detection: this.detectSimilarComponentLogic,
      refactoring: this.extractComposable,
      priority: 'medium'
    },
    {
      name: 'Duplicate Utility Functions',
      description: 'Identifies duplicate utility functions',
      detection: this.detectDuplicateUtilities,
      refactoring: this.consolidateUtilities,
      priority: 'high'
    }
  ]

  async recognizePatterns(ast: ESTree.Program): Promise<CodePattern[]> {
    return this.patterns.filter(pattern => pattern.detection(ast))
  }
}
```

### Phase 3: Automated Refactoring Engine (Critical)
```typescript
// Safe automated refactoring with rollback capability
export class RefactoringEngine {
  private transformations: Map<string, (() => void)[]> = new Map()

  async applyRefactoring(
    filePath: string,
    transformation: (ast: ESTree.Program) => ESTree.Program
  ): Promise<{ success: boolean; rollback: () => void }> {
    const originalContent = await fs.readFile(filePath, 'utf8')
    const originalAST = await this.parseFile(filePath)

    try {
      const newAST = transformation(originalAST)
      const newContent = this.generateCode(newAST)

      // Create rollback point
      const rollback = () => fs.writeFile(filePath, originalContent)

      // Apply transformation
      await fs.writeFile(filePath, newContent)

      return { success: true, rollback }
    } catch (error) {
      console.error(`Refactoring failed for ${filePath}:`, error)
      return { success: false, rollback: () => {} }
    }
  }

  async batchRefactor(
    refactoringPlan: Array<{
      file: string
      transformation: (ast: ESTree.Program) => ESTree.Program
    }>
  ): Promise<{ successful: string[]; failed: string[] }> {
    const results = { successful: [], failed: [] }

    for (const plan of refactoringPlan) {
      const result = await this.applyRefactoring(plan.file, plan.transformation)

      if (result.success) {
        results.successful.push(plan.file)
      } else {
        results.failed.push(plan.file)
      }
    }

    return results
  }
}
```

### Phase 4: Duplicate Method Resolution (Critical)
```typescript
// Specialized duplicate method resolver
export class DuplicateMethodResolver {
  async resolveDuplicateMethods(filePath: string): Promise<void> {
    const content = await fs.readFile(filePath, 'utf8')
    const ast = await this.parseFile(content)

    const duplicateMethods = this.findDuplicateMethods(ast)

    for (const duplicate of duplicateMethods) {
      await this.resolveMethodDuplicate(filePath, duplicate)
    }
  }

  private findDuplicateMethods(ast: ESTree.Program) {
    const methodMap = new Map<string, ESTree.FunctionDeclaration[]>()

    // Traverse AST to find all method declarations
    traverse(ast, {
      FunctionDeclaration(path) {
        const methodName = path.node.id?.name
        if (methodName) {
          if (!methodMap.has(methodName)) {
            methodMap.set(methodName, [])
          }
          methodMap.get(methodName)!.push(path.node)
        }
      }
    })

    // Find methods with multiple declarations
    return Array.from(methodMap.entries())
      .filter(([, methods]) => methods.length > 1)
      .map(([name, methods]) => ({ name, methods }))
  }

  private async resolveMethodDuplicate(filePath: string, duplicate: { name: string; methods: any[] }) {
    const content = await fs.readFile(filePath, 'utf8')

    // Remove duplicate declarations, keep the first one
    const methodDeclarations = duplicate.methods
    const firstDeclaration = methodDeclarations[0]
    const duplicateDeclarations = methodDeclarations.slice(1)

    let updatedContent = content

    for (const duplicateDecl of duplicateDeclarations) {
      // Remove duplicate method declaration
      const start = duplicateDecl.start || 0
      const end = duplicateDecl.end || 0
      updatedContent = updatedContent.slice(0, start) + updatedContent.slice(end)
    }

    await fs.writeFile(filePath, updatedContent)
  }
}
```

### Phase 5: Code Quality Metrics & Validation (Critical)
```typescript
// Code quality measurement and improvement tracking
export interface CodeQualityMetrics {
  duplicateCount: number
  complexityScore: number
  maintainabilityIndex: number
  technicalDebt: number
  testCoverage: number
}

export class QualityAnalyzer {
  async analyzeCodebase(): Promise<CodeQualityMetrics> {
    const files = await this.getTypeScriptFiles()
    let totalDuplicates = 0
    let totalComplexity = 0

    for (const file of files) {
      const analysis = await this.analyzeFile(file)
      totalDuplicates += analysis.duplicates
      totalComplexity += analysis.complexity
    }

    return {
      duplicateCount: totalDuplicates,
      complexityScore: totalComplexity / files.length,
      maintainabilityIndex: this.calculateMaintainability(totalComplexity, files.length),
      technicalDebt: this.calculateTechnicalDebt(totalDuplicates, files.length),
      testCoverage: await this.calculateTestCoverage()
    }
  }

  private calculateMaintainability(complexity: number, fileCount: number): number {
    // Maintainability calculation based on complexity and file count
    const normalizedComplexity = complexity / fileCount
    return Math.max(0, 100 - (normalizedComplexity * 2))
  }

  private calculateTechnicalDebt(duplicates: number, fileCount: number): number {
    // Technical debt hours based on duplicates
    return (duplicates / fileCount) * 2 // 2 hours per duplicate per file
  }
}
```

## Implementation Strategies

### Strategy 1: Incremental Cleanup
```typescript
// Gradual cleanup with validation at each step
export class IncrementalCleanup {
  async cleanupIncrementally(): Promise<void> {
    const phases = [
      'duplicate-methods',
      'similar-components',
      'utility-consolidation',
      'store-patterns',
      'type-improvements'
    ]

    for (const phase of phases) {
      console.log(\`Starting cleanup phase: \${phase}\`)

      await this.executePhase(phase)
      await this.validatePhase(phase)

      console.log(\`Completed cleanup phase: \${phase}\`)
    }
  }

  private async executePhase(phase: string): Promise<void> {
    switch (phase) {
      case 'duplicate-methods':
        await this.cleanupDuplicateMethods()
        break
      case 'similar-components':
        await this.extractSimilarComponents()
        break
      // ... other phases
    }
  }

  private async validatePhase(phase: string): Promise<void> {
    // Run TypeScript compilation
    // Run tests
    // Verify functionality still works
    // Rollback if validation fails
  }
}
```

### Strategy 2: Safety-First Refactoring
```typescript
// Safety checks before any refactoring
export class SafeRefactoring {
  async safeRefactor(filePath: string, transformation: Function): Promise<boolean> {
    // Pre-refactoring checks
    const preChecks = await this.runPreChecks(filePath)
    if (!preChecks.passed) {
      console.error('Pre-refactoring checks failed:', preChecks.errors)
      return false
    }

    // Create backup
    const backup = await this.createBackup(filePath)

    try {
      // Apply refactoring
      await transformation(filePath)

      // Post-refactoring validation
      const postChecks = await this.runPostChecks(filePath)
      if (!postChecks.passed) {
        console.error('Post-refactoring checks failed:', postChecks.errors)
        await this.restoreBackup(backup)
        return false
      }

      return true
    } catch (error) {
      console.error('Refactoring failed:', error)
      await this.restoreBackup(backup)
      return false
    }
  }

  private async runPreChecks(filePath: string): Promise<{ passed: boolean; errors: string[] }> {
    const errors: string[] = []

    // Check if TypeScript compiles
    try {
      execSync('npx tsc --noEmit', { cwd: this.projectRoot })
    } catch (error) {
      errors.push('TypeScript compilation failed')
    }

    // Check if tests pass
    try {
      execSync('npm test', { cwd: this.projectRoot })
    } catch (error) {
      errors.push('Tests failed')
    }

    return {
      passed: errors.length === 0,
      errors
    }
  }
}
```

### Strategy 3: Pattern-Based Consolidation
```typescript
// Automated pattern detection and consolidation
export class PatternConsolidation {
  async consolidatePatterns(): Promise<void> {
    const patterns = await this.detectPatterns()

    for (const pattern of patterns) {
      await this.consolidatePattern(pattern)
    }
  }

  private async detectPatterns(): Promise<CodePattern[]> {
    return [
      {
        type: 'duplicate-composables',
        files: await this.findDuplicateComposables(),
        action: 'extract-to-shared-composable'
      },
      {
        type: 'similar-store-patterns',
        files: await this.findSimilarStorePatterns(),
        action: 'create-base-store'
      },
      {
        type: 'duplicate-utility-functions',
        files: await this.findDuplicateUtilities(),
        action: 'consolidate-in-utils'
      }
    ]
  }

  private async consolidatePattern(pattern: CodePattern): Promise<void> {
    switch (pattern.action) {
      case 'extract-to-shared-composable':
        await this.extractSharedComposable(pattern.files)
        break
      case 'create-base-store':
        await this.createBaseStore(pattern.files)
        break
      case 'consolidate-in-utils':
        await this.consolidateUtilities(pattern.files)
        break
    }
  }
}
```

## Expected Outcomes
After successful execution:
- ✅ **Zero Duplicate Declarations**: All duplicate methods, functions, and interfaces resolved
- ✅ **Consolidated Code**: Similar patterns extracted into reusable components
- ✅ **Improved Architecture**: Clean separation of concerns and consistent patterns
- ✅ **Better Maintainability**: Reduced complexity and improved code organization
- ✅ **Enhanced Quality**: Higher maintainability index and reduced technical debt

## Success Criteria
- [ ] All duplicate method declarations removed
- [ ] Similar component logic extracted into composables
- [ ] Utility functions consolidated
- [ ] Store patterns standardized
- [ ] Code quality metrics improved
- [ ] TypeScript compilation successful
- [ ] All tests pass

## Validation Commands
```bash
# TypeScript compilation check
npx tsc --noEmit --skipLibCheck

# Duplicate detection
npm run cleanup:duplicates

# Code quality analysis
npm run analyze:quality

# Full test suite
npm run test

# Development server validation
npm run dev
```

## Cleanup Monitoring
```typescript
// Real-time cleanup progress tracking
export class CleanupMonitor {
  trackProgress(phase: string, progress: number): void {
    console.log(\`Cleanup Progress - \${phase}: \${progress}%\`)
  }

  generateReport(): CleanupReport {
    return {
      duplicatesRemoved: this.duplicateCount,
      patternsConsolidated: this.patternCount,
      qualityImprovement: this.qualityScore,
      timeSaved: this.estimatedTimeSaved
    }
  }
}
```

---
**This skill provides comprehensive architectural cleanup that eliminates code duplication, consolidates patterns, and significantly improves code quality and maintainability.**

---

## MANDATORY USER VERIFICATION REQUIREMENT

### Policy: No Fix Claims Without User Confirmation

**CRITICAL**: Before claiming ANY issue, bug, or problem is "fixed", "resolved", "working", or "complete", the following verification protocol is MANDATORY:

#### Step 1: Technical Verification
- Run all relevant tests (build, type-check, unit tests)
- Verify no console errors
- Take screenshots/evidence of the fix

#### Step 2: User Verification Request
**REQUIRED**: Use the `AskUserQuestion` tool to explicitly ask the user to verify the fix:

```
"I've implemented [description of fix]. Before I mark this as complete, please verify:
1. [Specific thing to check #1]
2. [Specific thing to check #2]
3. Does this fix the issue you were experiencing?

Please confirm the fix works as expected, or let me know what's still not working."
```

#### Step 3: Wait for User Confirmation
- **DO NOT** proceed with claims of success until user responds
- **DO NOT** mark tasks as "completed" without user confirmation
- **DO NOT** use phrases like "fixed", "resolved", "working" without user verification

#### Step 4: Handle User Feedback
- If user confirms: Document the fix and mark as complete
- If user reports issues: Continue debugging, repeat verification cycle

### Prohibited Actions (Without User Verification)
- Claiming a bug is "fixed"
- Stating functionality is "working"
- Marking issues as "resolved"
- Declaring features as "complete"
- Any success claims about fixes

### Required Evidence Before User Verification Request
1. Technical tests passing
2. Visual confirmation via Playwright/screenshots
3. Specific test scenarios executed
4. Clear description of what was changed

**Remember: The user is the final authority on whether something is fixed. No exceptions.**
