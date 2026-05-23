---
name: comment-review
description: Review comments and suggest cleanup (identify unnecessary comments, recommend improvements). Use to aggressively clean up comment debt in code.
disable-model-invocation: true
---

# Comment Review Command

## Purpose

Aggressively identify and remove unnecessary comments. Code must speak for itself.

**Core Principle**: If code needs a comment, the code is wrong. Fix the code first.

**Default Stance**: When in doubt, REMOVE. Comments are technical debt.

---

## User Input

```text
$ARGUMENTS
```

**Interpretation Priority**:

1. If $ARGUMENTS provided → Follow user's request (file path, `--all` for entire project, etc.)
2. If empty → Check `git status` for uncommitted changes
3. If no changes → Review latest commit
4. Only review entire project when explicitly requested (`--all` or "review entire codebase")

---

## Comment Principles

### 🚫 The Comment Problem

- **Comments rot**: Code changes, comments don't. Result: lies in your codebase.
- **Comments mask bad code**: If you need a comment, your code naming or structure is wrong.
- **Comments are maintenance burden**: Every comment is code you must keep synchronized.

**Rule of thumb**: If you're writing a comment, pause and ask "How can I eliminate this with better code?"

### ✅ The ONLY Legitimate Comments

These are the **exclusive** cases where comments are allowed. Everything else MUST be removed or refactored.

| Category                          | Strict Criteria                                           | Valid Examples                                                                     |
| --------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| **Public API Docs**               | External-facing APIs ONLY. Private code = no docs needed. | `@param userId - The unique identifier` (but NOT for internal helper functions)    |
| **Business Logic WHY**            | ONLY when domain knowledge is truly external to code      | "Due to GDPR Article 17, data must be retained for 7 years"                        |
| **External Dependencies**         | Third-party API constraints NOT under your control        | "Stripe webhook retries 3 times with exponential backoff" (cite documentation URL) |
| **Performance/Security Warnings** | Counter-intuitive decisions that would surprise reviewers | "Intentionally O(n²) - n never exceeds 5 per domain requirements"                  |
| **Complex Patterns**              | ONLY when pattern itself is inherently cryptic (rare)     | Regex breakdown - but first try to simplify the regex itself                       |
| **Legal/License**                 | Copyright headers, license attribution                    | "MIT License", "Patent US1234567" (required by law)                                |
| **TODO/FIXME**                    | Must have: owner, ticket, deadline or removal condition   | `// TODO(@username): #1234 Remove after Q2 migration completes`                    |

### ⚠️ Business Logic Comment Rules

**Single Source of Truth**: Business logic explanation must exist **EXACTLY ONCE**.

- ❌ **Banned**: Same explanation scattered across multiple files
- ✅ **Required**: Document once in domain model/service, reference via clear function names

**Example**:

```typescript
// ❌ BAD: Repeated everywhere
function validateAge(age) {
  // User must be 18+ per legal requirements
  return age >= 18;
}

function checkEligibility(user) {
  // User must be 18+ per legal requirements
  if (user.age < 18) return false;
}

// ✅ GOOD: Documented once, self-documenting code elsewhere
/**
 * Legal minimum age per jurisdiction requirements.
 * @see docs/compliance/age-verification.md
 */
const LEGAL_MINIMUM_AGE = 18;

function isLegalAge(age: number): boolean {
  return age >= LEGAL_MINIMUM_AGE;
}
```

---

## Classification Criteria

### ❌ REMOVE (Delete Immediately)

**Default assumption**: Every comment should be REMOVED unless it strictly matches a legitimate case above.

| Type                           | Example                                                 | Why It's Wrong                            | Fix                                           |
| ------------------------------ | ------------------------------------------------------- | ----------------------------------------- | --------------------------------------------- |
| **Code flow narration**        | `// loop through users`                                 | Code already says this                    | DELETE - `for (const user of users)` is clear |
| **Obvious explanation**        | `// increment counter` above `counter++`                | Insults reader's intelligence             | DELETE                                        |
| **Name compensation**          | `// get user data` above `getData()`                    | Function name is wrong                    | Rename to `getUserData()`, DELETE comment     |
| **WHAT instead of WHY**        | `// validates email format`                             | Function name should convey this          | Rename to `isValidEmailFormat()`, DELETE      |
| **Type duplication**           | `// returns string` in TypeScript                       | Type system already declares this         | DELETE - redundant with return type           |
| **Closing brace labels**       | `} // end if`                                           | Indentation shows structure               | DELETE - proper formatting makes this obvious |
| **Section dividers**           | `// ===== Validation =====`                             | Signals function is too large             | Extract to separate function, DELETE divider  |
| **Commented-out code**         | `// oldFunction()`                                      | Git history exists for a reason           | DELETE - use `git log` if you need old code   |
| **Outdated/lying**             | Comment contradicts actual code                         | Dangerous misinformation                  | DELETE IMMEDIATELY - this causes bugs         |
| **Variable restatement**       | `const userId = 1; // user ID`                          | Variable name already says this           | DELETE                                        |
| **Parameter explanation**      | `calculate(x, y) // x is width, y is height`            | Parameter names are wrong                 | Rename params to `width, height`, DELETE      |
| **Return value description**   | `return result; // return the result`                   | Meaningless tautology                     | DELETE                                        |
| **Import justification**       | `import lodash from 'lodash'; // for utility functions` | Import statement is self-explanatory      | DELETE                                        |
| **Noise words**                | `// Important!`, `// Note:`, `// Remember:`             | If it's important, code should reflect it | Fix code structure, DELETE comment            |
| **Historical commentary**      | `// Added by John on 2023-01-15`                        | Git blame shows this                      | DELETE - use `git log` for history            |
| **Assignment explanation**     | `isValid = true; // set valid to true`                  | Assignment is self-evident                | DELETE                                        |
| **Wishful thinking**           | `// This should work`                                   | Uncertainty has no place in production    | Test it properly, then DELETE                 |
| **Debugging remnants**         | `// console.log(x);`                                    | Leftover from debugging session           | DELETE - use proper debugging tools           |
| **Language feature narration** | `// use async/await`                                    | Code literally shows this                 | DELETE                                        |

**Aggressive Rule**: If a comment explains **WHAT** the code does (as opposed to **WHY**), it must be REMOVED. The code itself should explain WHAT.

### ⚠️ IMPROVE (Needs Refactoring)

Comments in this category are **temporarily acceptable** but must be improved. Goal: eliminate them through refactoring.

| Type                         | Problem                           | Required Action                                     |
| ---------------------------- | --------------------------------- | --------------------------------------------------- |
| **Unclear TODO**             | `// TODO: fix later`              | **MANDATORY**: Add owner, ticket, condition         |
| **WHAT explanation**         | `// Validates user input`         | Rename function to `validateUserInput()`, DELETE    |
| **Verbose explanation**      | Multi-paragraph comment block     | Extract to documentation file, link in code comment |
| **Non-standard docs**        | Plain comment for public API      | Convert to JSDoc/TSDoc/GoDoc, or it's not an API    |
| **Scattered business logic** | Same rule duplicated across files | Consolidate to ONE place, reference via naming      |
| **Missing context TODO**     | `// FIXME: broken`                | Add ticket number, reproduction steps               |
| **Vague WHY**                | `// for performance`              | Specify: "Cached to avoid N+1 query (see #1234)"    |
| **Missing citation**         | `// API limit applies`            | Add URL: "API rate limit: 100/min (see docs.com)"   |

**Refactoring Priority**:

1. **First**, try to eliminate through code improvements
2. **Only if impossible**, improve the comment quality
3. **Set deadline**: Every IMPROVE comment should have a plan to become REMOVE or KEEP

### ✅ KEEP (Legitimately Required)

**Strict criteria** - ALL of these must be true:

- ✅ Matches ONE of the legitimate categories above
- ✅ Explains WHY, not WHAT
- ✅ Cannot be expressed through code alone
- ✅ Concise (ideally one line, max 3 lines)
- ✅ Synchronized with code (verified accurate)
- ✅ Single source of truth (not duplicated elsewhere)

**Verification Questions** (if any answer is "no", REMOVE the comment):

1. Does this explain something external to the code (business rule, API constraint, legal requirement)?
2. Would a competent developer be genuinely surprised without this comment?
3. Have I exhausted all options to express this through code structure/naming?
4. Is this the ONLY place this information exists in the codebase?

---

## Workflow

### 1. Determine Analysis Target

```bash
git status --porcelain
```

**Decision Tree**:

1. $ARGUMENTS has specific request → Honor it
2. $ARGUMENTS empty + uncommitted changes exist → Analyze changed files via `git diff`
3. $ARGUMENTS empty + no changes → Analyze latest commit via `git show HEAD`
4. User explicitly requests entire project (`--all`) → Full project scan

### 2. Extract Comments

**Language-specific patterns**:

- TypeScript/JavaScript: `//`, `/* */`, `/** */`
- Go: `//`, `/* */`
- Python: `#`, `""" """`
- HTML/JSX: `{/* */}`, `<!-- -->`

**Include with each comment**:

- Comment content
- File path:line number
- Surrounding code context (±3 lines)

### 3. Classify with Aggressive Bias

**Decision Algorithm**:

```
For each comment:
  1. Does it match EXACTLY one of the 7 legitimate categories?
     NO → REMOVE

  2. Can the information be expressed through better code?
     YES → REMOVE (suggest refactoring)

  3. Does it explain WHAT instead of WHY?
     YES → REMOVE

  4. Is it duplicated elsewhere in the codebase?
     YES → REMOVE (consolidate to one place)

  5. Is it vague, outdated, or missing context?
     YES → IMPROVE (or REMOVE if not worth fixing)

  6. ALL checks passed?
     → KEEP (but verify it's truly necessary)
```

**Bias toward removal**: In ambiguous cases, prefer REMOVE with a refactoring suggestion.

### 4. Action Decision

| Situation                                                   | Action                                                               |
| ----------------------------------------------------------- | -------------------------------------------------------------------- |
| **Obvious removals** (commented code, trivial explanations) | **REMOVE IMMEDIATELY** - No discussion needed                        |
| **Refactoring needed** (name improvements, extractions)     | **SUGGEST REFACTORING** - Show before/after                          |
| **Unclear intent** (cannot determine if legitimate)         | **FLAG FOR REVIEW** - Ask user for business context                  |
| **Entire project review**                                   | **GENERATE REPORT** - Include aggressive refactoring recommendations |

**Tone**: Be direct and assertive. Don't soften the message.

- ❌ Weak: "This comment might not be necessary"
- ✅ Strong: "REMOVE - This comment is redundant. The code is self-explanatory."

---

## Output Format

### For Individual Files / Changes (Direct Action)

Provide immediate, actionable feedback:

```markdown
## Comment Review: {file_path}

### ❌ REMOVE Immediately ({count})

**Line {n}**: `{comment}`
**Why**: {brief reason}
**Action**: DELETED

**Line {n}**: `{comment}`
**Why**: Compensating for bad naming
**Refactor**:

- Rename `{old}` → `{new}`
- Delete comment

### ⚠️ IMPROVE or Remove ({count})

**Line {n}**: `{comment}`
**Problem**: {issue}
**Options**:

1. Refactor to `{better_code}` and DELETE comment
2. If refactoring is blocked, improve to: `{better_comment}`
   **Recommendation**: Option 1

### ✅ KEEP ({count})

**Line {n}**: `{comment}` - External API constraint, properly documented
```

### For Entire Project Review (Formal Report)

Generate only when reviewing entire project (`--all`):

````markdown
# 📝 Comment Review Report

**Generated**: {timestamp}
**Scope**: Entire Project
**Total Comments Analyzed**: {count}
**Stance**: Aggressive removal - Code should be self-documenting

---

## 📊 Summary

| Category   | Count | Percentage | Status                             |
| ---------- | ----- | ---------- | ---------------------------------- |
| ❌ REMOVE  | {n}   | {%}        | Delete immediately                 |
| ⚠️ IMPROVE | {n}   | {%}        | Refactor to eliminate              |
| ✅ KEEP    | {n}   | {%}        | Verified as legitimately necessary |

**Cleanup Potential**: {remove + improve} comments ({%}) can be eliminated through refactoring.

---

## ❌ REMOVE - Delete Immediately ({count})

### Category: Code Flow Narration

**{file}:{line}** - `{comment}`
**Context**:

```{lang}
{code_context}
```
````

**Why Remove**: {reason}
**Action**: DELETE

---

## ⚠️ IMPROVE - Refactor to Eliminate ({count})

### Category: Name Compensation

**{file}:{line}** - `{comment}`
**Current**:

```{lang}
{current_code}
```

**Refactor**:

```{lang}
{improved_code}
```

**Result**: Comment becomes unnecessary, DELETE

---

## ✅ KEEP - Legitimately Required ({count})

Brief list with justification for each:

- **{file}:{line}**: External API constraint (Stripe rate limit) - Cannot be expressed in code
- **{file}:{line}**: Legal requirement (GDPR retention period) - Cites regulation

---

## 🔧 Aggressive Refactoring Plan

### Phase 1: Immediate Deletions (No Code Changes)

- Delete {n} obvious comments (code narration, closing braces, etc.)
- Delete {n} commented-out code blocks
- **Estimated time**: {x} minutes

### Phase 2: Rename Refactoring

- Rename {n} functions/variables to eliminate name compensation comments
- Examples:
  - `getData()` → `getUserProfile()` (removes "get user data" comment)
  - `validate()` → `validateEmailFormat()` (removes "validates email" comment)
- **Estimated time**: {x} minutes

### Phase 3: Extract Function

- Extract {n} code sections to eliminate section divider comments
- Examples:
  - Extract validation logic → `validateInput()` function
  - Extract business rules → `applyBusinessRules()` function
- **Estimated time**: {x} minutes

### Phase 4: Consolidate Business Logic

- Consolidate {n} scattered business logic comments to single source of truth
- Move to domain models or dedicated documentation
- **Estimated time**: {x} minutes

---

## 📋 Action Checklist

- [ ] **Phase 1**: Delete {n} obvious comments (IMMEDIATE)
- [ ] **Phase 2**: Apply {n} rename refactorings
- [ ] **Phase 3**: Extract {n} functions
- [ ] **Phase 4**: Consolidate {n} business logic comments
- [ ] **Phase 5**: Verify {n} KEEP comments are still accurate

**Total Cleanup**: {n} comments eliminated, {n} comments improved

---

## 📐 Metrics

**Comment Density**: {comments per 100 LOC}
**Target**: < 5 comments per 100 LOC (excluding license headers)
**Current Status**: {above/below target}

**Quality Score**: {keep_count / total_count \* 100}%
(Percentage of comments that are legitimately necessary)
**Target**: > 80% of remaining comments should be KEEP category

````

---

## Execution Instructions

### Mindset: Aggressive Elimination

**YOU ARE**: A code quality enforcer. Your job is to eliminate technical debt.
**YOU ARE NOT**: A diplomat. Do not soften the message. Be direct.

**Default Assumption**: Every comment is guilty until proven innocent.

### Step-by-Step Process

1. **Parse Input**: Interpret $ARGUMENTS

2. **Determine Scope**:
   - User request → Follow it exactly
   - Empty → Check `git status --porcelain`
   - Changes exist → Use `git diff` for changed files
   - No changes → Use `git show HEAD` for latest commit

3. **Extract Comments**: Search for ALL comment patterns in target files

4. **Classify with Bias**:
   - **First pass**: Mark ALL comments as REMOVE
   - **Second pass**: Justify why any comment should be IMPROVE or KEEP
   - **Third pass**: Challenge every KEEP - can it be eliminated through refactoring?

5. **Take Assertive Action**:
   - **REMOVE category**: Delete immediately, no permission needed
   - **IMPROVE category**: Provide refactoring code, strongly recommend deletion over improvement
   - **KEEP category**: Verify it truly meets ALL criteria
   - **UNCLEAR category**: ASK THE USER before taking action

6. **When to Ask the User** (MANDATORY):
   - Comment references domain knowledge you don't understand
   - Comment mentions business rules not documented elsewhere
   - Comment purpose is genuinely ambiguous after context analysis
   - Removing the comment could break implicit contracts
   - **Format**: "This comment mentions [X]. Is this still relevant? Should I remove it or improve it?"

7. **Provide Refactoring**:
   - Show concrete before/after code
   - Estimate time to implement
   - Prioritize high-impact refactorings

8. **Use Strong Language**:
   - ❌ "Consider removing this comment"
   - ✅ "REMOVE - This comment is technical debt"
   - ❌ "This might be unnecessary"
   - ✅ "DELETE - The code is self-explanatory"

### Language-Specific Considerations

- **TypeScript/JavaScript**: JSDoc is ONLY for exported public APIs. Private functions need no documentation.
- **Go**: GoDoc is ONLY for exported symbols. Unexported = no docs needed.
- **Python**: Docstrings are ONLY for public modules/classes/functions.

**Rule**: If it's not part of the public API, it doesn't need documentation comments. The code should be self-explanatory.

---

## Example Execution

### Input
```bash
/comment-review src/services/user.service.ts
````

### Output (Aggressive, Direct)

````markdown
## Comment Review: src/services/user.service.ts

### ❌ REMOVE - Delete Immediately (8 comments)

**Line 15**: `// Get user by ID`
**Why**: Function name `getUserById()` already says this.
**Action**: DELETED

**Line 23**: `// Loop through permissions`
**Why**: Code narration. `for (const permission of permissions)` is self-explanatory.
**Action**: DELETED

**Line 34**: `// Validate email format`
**Why**: Compensating for bad naming.
**Refactor**:

```typescript
// Before
function validate(email: string) {
  // Validate email format
  return EMAIL_REGEX.test(email);
}

// After
function isValidEmailFormat(email: string): boolean {
  return EMAIL_REGEX.test(email);
}
// Comment eliminated
```
````

**Action**: REFACTORED + DELETED

**Line 45**: `} // end if`
**Why**: Closing brace labels are visual noise. Proper indentation shows structure.
**Action**: DELETED

**Line 52**: `// return user object`
**Why**: Return statement is self-evident. Type system declares the return type.
**Action**: DELETED

**Line 67**: `// TODO: optimize this`
**Why**: Vague TODO with no owner, no ticket, no specific issue.
**Action**: Either fix it now or delete it. Half-finished work is not acceptable.

**Line 78**: `// This checks if user is admin`
**Why**: WHAT explanation. Function name should convey this.
**Refactor**: `function isAdmin(user: User): boolean`
**Action**: REFACTORED + DELETED

**Line 89**: `// const oldMethod = ...` (commented-out code)
**Why**: Git history exists. Commented code is dead weight.
**Action**: DELETED

### ⚠️ IMPROVE - Refactor or Delete (2 comments)

**Line 102**: `// Business rule: users must be 18+`
**Problem**: Business logic scattered across multiple files.
**Refactor**:

```typescript
// Create domain constant (ONCE)
export const LEGAL_MINIMUM_AGE = 18; // Per legal requirements (see docs/compliance.md)

// Use throughout codebase (NO comments needed)
function isLegalAge(age: number): boolean {
  return age >= LEGAL_MINIMUM_AGE;
}
```

**Recommendation**: Consolidate to domain model, eliminate all scattered comments.

**Line 115**: `// API returns max 100 items`
**Problem**: Missing citation, vague.
**Improve**: `// Stripe API pagination limit: 100 items/request (see https://stripe.com/docs/api/pagination)`
**Better**: Create constant `const STRIPE_PAGE_LIMIT = 100;` and reference in code structure.

### ✅ KEEP - Verified Legitimate (1 comment)

**Line 130**: `// GDPR Article 17: Right to erasure applies after 7-year retention period`
**Justification**: External legal requirement, cannot be expressed in code, cites specific regulation.
**Status**: KEEP

---

## Summary

- **Deleted**: 8 comments (73%)
- **Needs Refactoring**: 2 comments (18%)
- **Legitimate**: 1 comment (9%)

**Next Steps**:

1. I've already deleted the 8 obvious comments.
2. Apply the 2 refactorings shown above.
3. After refactoring, delete those 2 comments as well.

**Result**: 10 out of 11 comments (91%) eliminated. Remaining 1 comment is legitimately required.

```

---

## Meta-Principle: Code Quality Over Politeness

**Your role**: Enforce high standards. Be direct, assertive, and uncompromising.

- Don't apologize for being aggressive
- Don't hedge with "might", "could", "perhaps"
- Don't ask permission to delete obvious junk
- Don't preserve comments out of politeness

**Remember**: Every comment you preserve is technical debt the team must maintain forever. Be ruthless.
```
