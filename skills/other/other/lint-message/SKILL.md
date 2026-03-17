---
name: lint-message
description: "Use when writing ESLint rule error messages to educate developers effectively."
user-invocable: false
---

# Writing Effective ESLint Rule Messages

## Purpose

ESLint messages are the primary interface between our custom rules and the developers (including AI agents) who encounter them. A well-crafted message transforms a confusing lint error into a learning opportunity. Our rules often enforce non-intuitive concepts—extensibility patterns, maintainability principles, or guards against esoteric bugs—that junior developers and AI agents cannot infer from the error alone.

**Treat every ESLint message as a teaching moment.** The message should transfer the insight that motivated the rule's creation.

## Message Structure

Follow this pattern for comprehensive messages:

```text
[What's wrong] → [Why it matters] → [How to fix]
```

### 1. What's Wrong (Use Template Variables)

Use `{{handlebars}}` syntax to make the error specific to the user's code:

```typescript
// ❌ Generic
messages: {
  badNaming: 'Variable name is incorrect',
}

// ✅ Specific with context
messages: {
  badNaming: 'Boolean variable "{{name}}" lacks a descriptive prefix',
}
```

### 2. Why It Matters (The Teaching Moment)

This is the most critical part. Explain:

- The underlying principle being violated
- The real-world consequence of ignoring this rule
- The pitfall or bug this rule prevents

```typescript
// ❌ No explanation
messages: {
  noMemo: 'Add useMemo to this value',
}

// ✅ Explains the underlying concept
messages: {
  noMemo: 'Value "{{name}}" is recreated on every render, causing unnecessary re-renders in child components. Wrap in useMemo() to maintain referential stability.',
}
```

### 3. How to Fix (Actionable Guidance)

When the fix isn't obvious from the "why", include concrete guidance:

```typescript
// ✅ Includes fix guidance
messages: {
  missingPrefix: 'Boolean {{type}} "{{name}}" should use a prefix like "is", "has", "can", or "should" (e.g., "{{suggestedName}}") to signal its type at the call site and improve code readability.',
}
```

## Guiding Principles

### Assume No Prior Knowledge

Write as if the reader has never encountered this pattern before. Junior developers and AI agents lack the institutional knowledge that motivated the rule.

```typescript
// ❌ Assumes knowledge
messages: {
  error: 'Avoid object arrays in Firestore',
}

// ✅ Explains the concept
messages: {
  error: 'Arrays of objects in Firestore documents cannot be queried by field value and lead to full-document reads. Use a subcollection or map structure instead.',
}
```

### Explain the Esoteric Bug

Many rules exist to prevent bugs that have bitten the team repeatedly. Document this history in the message:

```typescript
// ❌ Just states the rule
messages: {
  noOverride: 'Do not call overridable methods in constructor',
}

// ✅ Explains the bug this prevents
messages: {
  noOverride: 'Calling "{{methodName}}" in the constructor is unsafe because subclasses may override it, and the subclass instance is not yet initialized when the parent constructor runs. This causes subtle bugs where overridden methods access uninitialized properties.',
}
```

### Verbose Is Acceptable

Unlike user-facing UI, lint messages can be long. Clarity trumps brevity:

```typescript
// ✅ Verbose but clear
messages: {
  preferParams: 'Access "{{paramName}}" via params.{{paramName}} instead of traversing {{traversalPath}}. The params object is type-safe, more readable, and avoids brittle reference traversal that breaks when document paths change.',
}
```

### Use Domain-Specific Language

When the rule enforces a team convention or architectural decision, name it:

```typescript
// ✅ References the pattern by name
messages: {
  useHandler: 'Firebase triggers should use DocumentChangeHandler types to ensure params are properly typed. See the handler pattern documentation.',
}
```

## Anti-Patterns to Avoid

### ❌ Tautological Messages

Messages that just restate the rule name without explanation:

```typescript
// Bad
messages: {
  error: 'This violates the no-circular-references rule',
}
```

### ❌ Imperative Without Justification

Commands without reasoning don't teach:

```typescript
// Bad
messages: {
  error: 'Use useCallback here',
}
```

### ❌ Overly Technical Without Context

AST jargon that doesn't help the developer understand:

```typescript
// Bad
messages: {
  error: 'CallExpression callee must not be MemberExpression with computed property',
}
```

## Example: Before and After

### Before (Minimal)

```typescript
messages: {
  missingBooleanPrefix:
    'Boolean {{type}} "{{name}}" should start with an approved prefix: {{prefixes}}',
}
```

### After (Educational)

```typescript
messages: {
  missingBooleanPrefix:
    'Boolean {{type}} "{{name}}" should start with a prefix like "is", "has", "can", or "should". ' +
    'Boolean prefixes make code self-documenting—readers immediately know {{name}} holds a true/false value without checking its declaration. ' +
    'Consider renaming to "is{{capitalizedName}}" or "has{{capitalizedName}}".',
}
```

## Checklist for New Rules

Before finalizing a rule's messages, verify:

- [ ] Does the message explain **why** this pattern is problematic?
- [ ] Would a junior developer understand the underlying concept after reading it?
- [ ] Would an AI agent be able to fix the issue correctly based on the message alone?
- [ ] Does it use `{{variables}}` to reference the specific code that triggered it?
- [ ] Does it suggest a concrete fix or alternative approach?
- [ ] Is it free of jargon that requires prior knowledge of this codebase?
