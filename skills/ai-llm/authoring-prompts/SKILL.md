---
name: authoring-prompts
description: Invoke this skill first when authoring any AI agent instructions. Foundational principles for writing LLM instructions (skills, CLAUDE.md, rules, commands). Covers token economics, imperative language, formatting for LLM parsing, emphasis modifiers, terminology consistency, and common anti-patterns.
---

# Instruction Authoring Foundations

Core principles for writing instructions that LLMs execute efficiently and deterministically. Apply these principles across all instruction types: skills, CLAUDE.md files, rules, and slash commands.

## Token Economics

The context window is a shared resource. Challenge each piece of information: "Does Claude already know this?" Only add context Claude lacks. Assume Claude is already very smart.

Remove decorative language. No "please", "remember", "make sure", "it's important".

Use examples over explanations. One concrete before/after example teaches more than three paragraphs of description.

Prefer tables for structured data. Compress related information into scannable format.

## Determinism and Specificity

### Degrees of Freedom

Match specificity to task requirements.

**High freedom** (text instructions): Use when multiple approaches are valid. Medium freedom (pseudocode, parameterized scripts): Use when a preferred pattern exists. **Low freedom** (exact scripts, no parameters): Use when operations are fragile or consistency is critical.

### Zero Ambiguity

Every instruction must have exactly one interpretation.

Use explicit constraints, not suggestions. "Run `pytest tests/ --strict-markers`" not "Run tests with strict markers when appropriate."

Specify conditions completely. "Validate input at API boundaries" not "Validate input."

Eliminate hedge words: "consider", "try to", "when possible", "generally", "often".

### Deterministic Commands

Include all flags and arguments. `dotnet test --logger "console;verbosity=detailed"` not `dotnet test`.

Use absolute paths or precisely scoped paths. `/src/api/`, `src/**/*.ts`, not "the API code."

Specify tool versions when behavior differs. "Node.js 20+: use native fetch" not "Use fetch."

## Imperative Language Patterns

Use imperative form only. "Validate at boundaries" not "You should validate at boundaries."

Write direct commands in imperative mood.

Good: "Validate input at API boundaries"
Avoid: "You should consider validating input"

State what to do, not what not to do when possible.

Good: "Let exceptions propagate"
Avoid: "Do not catch exceptions unnecessarily"

### Specificity in Constraints

Be specific in prohibitions and requirements.

Good: "Do not implement retry logic in background jobs"
Avoid: "Avoid defensive patterns"

## Formatting for LLM Parsing

Use markdown structure that aids LLM understanding.

**Headings**: Establish context and scope. Content under a heading applies to that domain only.

**Lists**: Use only for discrete, parallel, independent items. Use prose when relationships between ideas matter.

**Code blocks**: For exact values, commands, identifiers, and patterns only.

**Tables**: For structured comparisons, reference data, or multi-dimensional information.

**Bold/Italic**: Use sparingly. If more than 10% of text is emphasized, nothing is emphasized.

**White space**: Use blank lines between paragraphs and sections for clarity. Aids parsing.

### Tables vs Lists vs Prose

**Tables**: Structured data with categories - types, priorities, mappings, decision matrices.

**Lists**: Discrete, parallel items - required packages, file paths, command flags.

**Prose**: Relationships and context - when to use one approach vs another, why a constraint exists.

## Emphasis and Terminology

### Emphasis Modifiers

Use MUST, MUST NOT, REQUIRED only for hard constraints where violation causes failure.

Do not use modifiers for preferences or defaults. If every instruction uses MUST, none stand out.

Bold only for hard constraints where violation causes failure. Avoid over-emphasis.

### Terminology Consistency

Choose one term per concept and use it throughout.

Good: Always "API endpoint"
Bad: Mix "API endpoint", "URL", "route", "path"

## Structural Optimization

Place critical constraints first. Most important information at top of file.

Use progressive specificity. Global rules first, then domain-specific, then file-specific.

Separate concerns cleanly. One section per topic. Do not mix testing rules with deployment procedures.

End sections decisively. No trailing "etc." or "and more."

## Common Anti-Patterns

### Language Anti-Patterns

Suggestion language:
- ❌ "Consider using async/await"
- ✓ "Use async/await for I/O operations"

Vague quantifiers:
- ❌ "Usually validate input"
- ✓ "Validate input at API boundaries"

Ambiguous conditionals:
- ❌ "Add logging when appropriate"
- ✓ "Log errors with stack traces. Omit logging for expected control flow."

Multiple options without default:
- ❌ "Use Jest, Vitest, or Mocha for testing"
- ✓ "Use Vitest for tests. Jest acceptable for legacy files."

### Structural Anti-Patterns

Burying critical constraints:
- ❌ Long preamble, then critical requirement in middle
- ✓ Critical requirement first, context after if needed

Over-emphasis:
- ❌ **Every** **other** **word** **bold**
- ✓ Bold only for hard constraints where violation causes failure

Lists as default:
- ❌ Everything formatted as bulleted list
- ✓ Lists for discrete items, prose for relationships

### Content Anti-Patterns

Repeating framework documentation:
- ❌ "React hooks let you use state and lifecycle in function components..."
- ✓ "Store form state in URL params, not local state"

Generic best practices:
- ❌ "Functions should be small and focused"
- ✓ "Limit API handlers to routing only. Move logic to services/"

Time-sensitive information:
- ❌ "Before August 2025, use legacy API"
- ✓ "Use v2 API at api.example.com/v2/"

Decorative content: Welcome messages, motivational statements, background history.

Hypothetical scenarios: "If we ever migrate to Postgres..." Address when actual, not hypothetical.

## Optimization Techniques

### Sentence Compression

Remove filler:
- Before: "You should make sure to always run the test suite before committing your changes"
- After: "Run `pytest` before committing"

Combine related instructions:
- Before: "Use TypeScript. Add type annotations. Enable strict mode."
- After: "Use TypeScript strict mode with explicit type annotations"

### Command Specification

Full specification:
```markdown
## Commands
- `pytest tests/ --strict-markers --cov=src --cov-report=html`: Run tests with coverage
- `dotnet build --configuration Release --no-restore`: Production build
- `npm run lint -- --fix`: Auto-fix linting issues
```

Not:
```markdown
## Commands
Run pytest to test. Use dotnet build for building. Lint with npm.
```
