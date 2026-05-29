---
name: 'signal-capture'
description: 'Detect and capture technical preferences, naming conventions, and architectural practices from user messages into Packmind standards. Trigger when user prescribes HOW to code through direct statements (e.g., "Use snake_case for columns", "Always use async/await") or suggestive patterns like questions ("Could we use X instead?"), code review feedback ("This would be clearer with X"), and comparative statements ("Use X instead of Y"). Does NOT trigger for feature requests, bug reports, or general implementation tasks without coding preferences.'
---

# Signal Capture Workflow

This skill helps detect technical preferences in user messages and captures them systematically in `.claude/signal-capture.yaml` for integration into coding standards.

## TRIGGER CHECKLIST - Read This First

**TRIGGER THIS SKILL IMMEDIATELY WHEN THE USER:**

- [ ] States a naming convention ("All interfaces should start with I")
- [ ] Prescribes a code structure ("Always use async/await")
- [ ] Suggests an alternative ("Could we use X instead?")
- [ ] Gives code review feedback implying a pattern ("This would be clearer with X")
- [ ] Makes a comparative statement ("Use X instead of Y", "Prefer X over Y")
- [ ] References a principle that needs clarification ("follow KISS", "apply DRY")
- [ ] Requests removal of a rule ("Remove the rule about X")

**TRIGGER AS SOON AS YOU DETECT THE PREFERENCE** - don't wait until the end of your response. Ask for validation immediately.

**MANDATORY MESSAGE CHECK:**
For every user message, ask yourself: "Is the user telling me HOW to code?" If yes → trigger this skill.

## Failure Example - When This Skill SHOULD Have Been Triggered

```
User: "Could we just ensure that standardFile exists instead of using optional chaining?"

AI: [Detects this is a suggestive pattern indicating a preference]
AI: [Implements the change but FORGETS to capture the preference as a rule] ❌

CORRECT BEHAVIOR:
AI: [Detects suggestive pattern]
AI: [Immediately triggers skill]
AI: [Asks user: "I detected a technical preference. Add this rule to tests-redaction?"]
AI: [If approved, logs to .claude/signal-capture.yaml]
AI: [Continues with the implementation]
```

## When to Trigger

**TRIGGER CONDITIONS** - User prescribes HOW to code:

- Naming conventions: "All interfaces should start with I", "Use snake_case for columns"
- Code structure directives: "Wrap emojis for accessibility", "Always use async/await", "Don't use class components"
- Pattern enforcement: "Use composition over inheritance", "Prefer functional programming"
- Principle references in tasks: "follow KISS", "apply DRY principle", "respect SOLID", "use React best practices", "follow clean code", "apply separation of concerns"
  **Note:** These require a clarification step (see "Clarification for Abstract Principles" below)
- Removal/updates: "Remove the rule about X", "We no longer need Y convention"
- Formatting rules: "Always add JSDoc comments", "Use single quotes"
- **Suggestive patterns (indicating preferences):**
  - Questions suggesting alternatives: "Could we use X instead?", "Should we prefer Y?", "Why not do Z?", "What about using X here?"
  - Comparative statements: "Use X instead of Y", "Prefer X over Y", "Replace X with Y", "Let's switch from X to Y"
  - Code review feedback implying patterns: "This would be clearer with X", "Better to use Y", "It's more maintainable if we X"
  - Context-specific suggestions revealing general practices: "Let's ensure X exists rather than Y" (implies: prefer X pattern over Y pattern)

**NON-TRIGGER CONDITIONS** - User asks WHAT to build or fix (without HOW):

- Feature requests without principles: "Add a search feature", "Create a new component"
- Bug reports: "This function is broken", "Fix the error on line 10"
- Questions: "How does this work?", "What's the best approach?"
- Implementation tasks without standards: "Implement the login page", "Add error handling"

⚠️ **EXCEPTION:** If any of the above includes principle references (KISS, DRY, SOLID, best practices), it BECOMES a trigger. Ask for specific rules before proceeding.

## Workflow

### Step 1: Detection

When a technical preference is detected in the user's message:

1. Identify the specific coding rule or convention being stated
2. Determine which existing standard it belongs to (or if a new standard is needed)
3. Classify the operation type: ADDED (new rule), UPDATED (modifying existing rule), or DELETED (removing old rule)

### Step 2: Ask for Validation

Present the detected preference to the user for approval:

> I detected a technical preference. Add this rule to **[STANDARD_NAME]**?
>
> Proposed rule: _"[REFORMULATED_RULE]"_

**Format guidelines for the proposed rule:**

- Start with a verb (imperative mood)
- Be concise and clear
- Focus on the "what" and "why" not implementation details
- Example: "Prefix interfaces with I to distinguish them from types"

Wait for user approval before proceeding. If user refuses, continue with the original task without updating standards.

### Clarification for Abstract Principles

When the user references abstract principles (KISS, DRY, SOLID, best practices) without explicit rules, ask for specifics before capturing:

> I noticed you mentioned [PRINCIPLE]. To capture this as a standard, could you specify concrete rules? For example:
>
> - [Suggest 2-3 specific rules relevant to the context]
>
> Which rules would you like to add, or type "skip" to continue without capturing.

This applies to:

- KISS, DRY, SOLID, YAGNI principles
- "Best practices" without specifics
- "Clean code" without specifics
- Framework conventions without explicit rules

**Language Independence:** Signal detection works regardless of the input language. Common principle names (KISS, DRY, SOLID) are universal. For localized terms, recognize equivalents like:

- FR: "bonnes pratiques", "principes de conception"
- ES: "buenas prácticas", "principios de diseño"

### Step 3: Log to `.claude/signal-capture.yaml`

If approved, append the change to `.claude/signal-capture.yaml`:

```yaml
- newRule: '<rule text>' # omit this field for DELETED operations
  oldRule: '<previous text>' # required for UPDATED and DELETED operations
  operation: ADDED | UPDATED | DELETED
  standard: '<short-name>' # e.g., typescript-code-standards, tests-redaction
  date: '<ISO date>' # e.g., 2025-12-19
  sourceFile: '<file path where signal was captured>' # file being worked on when rule was captured
  language: '<language>' # omit for DELETED operations
  goodExample: | # omit for DELETED operations
    <valid code example>
  badExample: | # omit for DELETED operations
    <invalid code example>
```

**YAML Logging Rules:**

1. **Operations:**
   - `ADDED`: New rule being added (requires: newRule, standard, date, sourceFile, language, goodExample, badExample)
   - `UPDATED`: Existing rule being modified (requires: newRule, oldRule, standard, date, sourceFile, language, goodExample, badExample)
   - `DELETED`: Rule being removed (requires: oldRule, standard, date, sourceFile)

2. **Examples:**
   - Always include meaningful, realistic code examples
   - Good example shows the correct way following the rule
   - Bad example shows what NOT to do (violating the rule)
   - Examples should be concise but illustrative
   - Use proper code formatting with appropriate language syntax

3. **Standard Names:**
   - Use existing standard names when applicable
   - Common standards: `typescript-code-standards`, `tests-redaction`, `changelog`, `api-design`, `react-patterns`
   - Use kebab-case for new standard names

4. **Source File:**
   - Include the file path where the preference was mentioned or where it will be applied
   - If no specific file, use the project root or most relevant path

### Step 4: Confirmation

After logging, confirm to the user:

> Rule logged to `.claude/signal-capture.yaml` for the **[STANDARD_NAME]** standard.

Then continue with the original task.

## Important Guidelines

1. **Only add if not already covered**: Check if the rule is already captured in existing standards before proposing to add it
2. **Keep wording concise**: Rules should be clear and actionable, not verbose
3. **Always include meaningful examples**: Both good and bad examples must be realistic and helpful
4. **Don't interrupt flow**: Signal capture should be quick and non-intrusive to the main task
5. **Be precise about operation type**: Distinguish clearly between ADDED, UPDATED, and DELETED operations

## Example Scenarios

### Example 1: Adding a New Rule

**User message:** "All API response types should have a 'data' property wrapper"

**Detection:** New architectural practice detected

**Validation prompt:**

> I detected a technical preference. Add this rule to **api-design**?
>
> Proposed rule: _"Wrap all API responses in a data property for consistency"_

**If approved, log:**

```yaml
- newRule: 'Wrap all API responses in a data property for consistency'
  operation: ADDED
  standard: 'api-design'
  date: '2025-12-19'
  sourceFile: 'src/api/users.ts'
  language: 'TYPESCRIPT'
  goodExample: |
    return {
      data: { users: [...] },
      meta: { total: 100 }
    }
  badExample: |
    return {
      users: [...],
      total: 100
    }
```

### Example 2: Updating an Existing Rule

**User message:** "Actually, let's update our interface naming - only prefix public interfaces with I, not internal ones"

**Detection:** Modification to existing naming convention

**Validation prompt:**

> I detected a technical preference. Update the rule in **typescript-code-standards**?
>
> Old rule: _"Prefix interfaces with I"_
> New rule: _"Prefix public interfaces with I (internal interfaces don't need prefix)"_

**If approved, log:**

```yaml
- newRule: "Prefix public interfaces with I (internal interfaces don't need prefix)"
  oldRule: 'Prefix interfaces with I'
  operation: UPDATED
  standard: 'typescript-code-standards'
  date: '2025-12-19'
  sourceFile: 'src/types/user.ts'
  language: 'TYPESCRIPT'
  goodExample: |
    // Public
    export interface IUserService { }

    // Internal
    interface UserCache { }
  badExample: |
    // Public
    export interface UserService { }

    // Internal
    interface IUserCache { }
```

### Example 3: Removing a Rule

**User message:** "Remove the rule about using JSDoc comments everywhere, it's too verbose"

**Detection:** Rule removal requested

**Validation prompt:**

> I detected a request to remove a rule from **typescript-code-standards**?
>
> Rule to remove: _"Add JSDoc comments to all exported functions"_

**If approved, log:**

```yaml
- oldRule: 'Add JSDoc comments to all exported functions'
  operation: DELETED
  standard: 'typescript-code-standards'
  date: '2025-12-19'
  sourceFile: 'CLAUDE.md'
```

### Example 4: Suggestive Pattern (Code Review Feedback)

**User message:** "Could we just ensure that standardFile and recipeFile exist instead of those optional chaining?"

**Detection:** Suggestive pattern revealing a testing practice preference (use assertions instead of optional chaining for test data setup)

**Validation prompt:**

> I detected a technical preference. Add this rule to **tests-redaction**?
>
> Proposed rule: _"Use assert to verify test data exists in beforeEach setup rather than optional chaining in test assertions for clearer failure messages and type narrowing"_

**If approved, log:**

```yaml
- newRule: 'Use assert to verify test data exists in beforeEach setup rather than optional chaining in test assertions for clearer failure messages and type narrowing'
  operation: ADDED
  standard: 'tests-redaction'
  date: '2026-01-08'
  sourceFile: 'packages/integration-tests/src/coding-agents-deployments/claude-deployment.spec.ts'
  language: 'TYPESCRIPT'
  goodExample: |
    let recipeFile: FileModification;

    beforeEach(() => {
      const found = files.find(f => f.path.startsWith('.claude/'));
      assert(found, 'Recipe file should exist');
      recipeFile = found;
    });

    it('includes content', () => {
      expect(recipeFile.content).toContain('---');
    });
  badExample: |
    let recipeFile: FileModification | undefined;

    beforeEach(() => {
      recipeFile = files.find(f => f.path.startsWith('.claude/'));
    });

    it('includes content', () => {
      expect(recipeFile?.content).toContain('---');
    });
```

## Integration with Main Task

Signal capture should happen seamlessly:

1. Detect the preference in the user's message
2. Quickly validate with the user
3. Log if approved
4. Continue with the main task without significant disruption

The goal is to build a knowledge base of coding preferences over time without interrupting the development flow.

---

**REMEMBER:** This skill is MANDATORY when users express technical preferences. Unlike other capture skills, this one requires user validation before logging. When you detect a preference, you MUST ask for approval - don't skip this step. Every captured preference helps build a comprehensive knowledge base of coding standards.