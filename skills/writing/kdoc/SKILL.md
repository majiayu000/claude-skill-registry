---
name: kdoc
description: Write concise KDoc documentation for Kotlin classes and functions. Use when user wants to add KDoc to Kotlin files. Focuses on short summaries without version info or variable docs.
allowed-tools:
  - Read
  - Edit
  - Glob
  - Grep
---

# KDoc Documentation Writer

Write short, concise KDoc documentation for Kotlin files focusing on class and function summaries only.

## Rules

1. **Class/Interface/Object KDoc**
   - Single sentence describing purpose
   - No `@author`, `@version`, `@since`, or other metadata
   - No `@property` for class properties

2. **Function KDoc**
   - One-liner summary of what function does
   - `@param` only if parameter purpose isn't obvious from name
   - `@return` only if return value needs clarification
   - Skip `@throws` unless critical for API consumers

3. **DO NOT Document**
   - Variables/properties (neither class nor local)
   - Private functions (unless complex logic)
   - Getters/setters
   - Obvious functions (e.g., `fun getId(): String`)
   - Companion object members

4. **Style**
   - Start with verb (Returns, Creates, Handles, Processes)
   - No period at end of single-line KDoc
   - Max 80 chars per line
   - Use `/** ... */` format

## Examples

### Class KDoc
```kotlin
/** Manages game session state and lifecycle */
class GameManager { ... }

/** Handles user authentication via OAuth and email */
interface AuthService { ... }
```

### Function KDoc
```kotlin
/** Loads questions from remote API and caches locally */
suspend fun loadQuestions(): List<Question>

/** @param difficulty Filter questions by difficulty level */
fun getQuestionsByDifficulty(difficulty: Difficulty): List<Question>

/**
 * Validates answer and updates score
 * @return true if answer correct
 */
fun submitAnswer(questionId: String, answer: String): Boolean
```

### Skip These
```kotlin
// NO KDoc needed
private fun calculateInternalScore(): Int
val currentScore: Int
fun getUsername(): String
companion object { const val TAG = "Game" }
```

## Workflow

1. Read target Kotlin file
2. Identify public classes, interfaces, objects
3. Identify public/internal functions needing docs
4. Write minimal KDoc using Edit tool
5. Skip variables, private members, obvious code
