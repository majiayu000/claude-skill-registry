---
name: 'packmind-create-standard'
description: "Guide for creating coding standards via the Packmind CLI. This skill should be used when users want to create a new coding standard (or add rules to an existing standard) that captures team conventions, best practices, or coding guidelines for distribution to CoPilot."
license: 'Complete terms in LICENSE.txt'
---

# Standard Creator

This skill provides a complete walkthrough for creating coding standards via the Packmind CLI.

## About Coding Standards

Coding standards are collections of rules that capture team conventions, best practices, and coding guidelines. They help maintain consistency across codebases and enable CoPilot to follow your team's specific practices.

### What Standards Provide

1. **Consistent code style** - Rules that enforce naming conventions, formatting, and structure
2. **Best practices** - Guidelines for error handling, testing, security, and performance
3. **Domain knowledge** - Company-specific patterns, architectural decisions, and business logic
4. **Code examples** - Positive/negative examples that demonstrate correct vs incorrect usage

### Standard Structure

Every standard consists of:

```
{
  "name": "Standard Name",
  "description": "What the standard covers and why",
  "summary": "One-sentence description of when to apply the rules (optional)",
  "scope": "Where/when the standard applies (e.g., 'TypeScript files', 'React components')",
  "rules": [
    {
      "content": "Rule description starting with action verb",
      "examples": {
        "positive": "Valid code example",
        "negative": "Invalid code example",
        "language": "TYPESCRIPT"
      }
    }
  ]
}
```

**Note**: The Packmind CLI currently requires the `scope` field. The `summary` field is used in other workflows (like MCP) but not yet supported by the CLI.

#### Understanding `scope` vs `summary`

- **`scope`** (required by CLI): **WHERE** the standard applies - file patterns, technologies, specific locations
  - Examples: `"TypeScript test files (*.spec.ts, *.test.ts)"`, `"React functional components"`
- **`summary`** (optional, not yet CLI-supported): **WHEN/WHY** to apply - high-level purpose and trigger condition
  - Examples: `"Apply when writing tests to ensure consistency"`, `"Use when handling user data for privacy compliance"`

## Prerequisites

Before creating a standard, verify that packmind-cli is available:

Check if packmind-cli is installed:

```bash
packmind-cli --version
```

If not available, install it:

```bash
npm install -g @packmind/cli
```

Then login to Packmind:

```bash
packmind-cli login
```

## Standard Creation Process

To create a standard, follow this process in order, skipping steps only if there is a clear reason why they are not applicable.

### Step 1: Clarify the Request

Gather essential information before drafting the standard.

#### Clarification Flow

Study the user's request and identify critical gaps. The number of questions should match the request clarity:
- **1-2 questions** when the request is well-defined (clear scope, specific examples, detailed context)
- **3-5 questions** when the context is unclear or the request is vague

**Examples of focused questions:**
- "Which service or file shows the expected pattern?"
- "Is there an existing doc or rule we must stay aligned with?"
- "What specific aspect matters most (mocking guidelines, naming conventions, assertion style)?"

Introduce questions with a simple phrase about needing clarification, then list as bullet points—no numbering, no category headers.

#### Repository Access Guardrail

**Do not open or scan repository files unless the user explicitly points to them** (provides file paths or requests project-wide review). If source references are needed, ask the user to supply them.

#### What to Capture

Take brief notes on:
- Title or slug (if mentioned)
- Scope guardrails
- Key references
- Expected outcomes

Keep notes concise—just enough to unlock drafting.

### Step 2: Draft Rules

Transform the understanding into concrete rules. **Do not add examples yet** - examples will be added in Step 3.

#### Draft Creation (Rules Only)

1. Create a draft markdown file in `.packmind/standards/_drafts/` (create the folder if missing) using filename `<slug>-draft.md` (lowercase with hyphens)
2. Initial draft structure:
   - `# <Standard Title>`
   - Context paragraph explaining when/why to apply the standard
   - Optional **Key References** list citing files or authoritative sources
   - `## Rules` as bullet points following the Rule Writing Guidelines below
   - **DO NOT include examples yet** - examples will be added in Phase 2

#### Rule Writing Guidelines

Each rule should follow these format requirements:

1. **Start with an action verb** - Use imperative form (e.g., "Use", "Avoid", "Prefer", "Include")
2. **Be concise** - Max ~25 words per rule
3. **Be specific and actionable** - Avoid vague guidance
4. **Focus on one concept** - One rule per convention

##### Avoid Rationale Phrases

Rules describe **WHAT** to do, not **WHY**. Strip justifications and benefits—let examples demonstrate value.

**Common fluff patterns to remove:**
- "to improve/provide/ensure..." (benefit phrases)
- "while maintaining/preserving..." (secondary concerns)
- "for better/enhanced..." (quality claims)
- "and enable/allow..." (future benefits)

**Bad (includes rationale):**
> Document props with JSDoc comments to provide IDE intellisense and improve developer experience.

**Good (action only):**
> Document component props with JSDoc comments (`/** ... */`) describing purpose, expected values, and defaults.

##### Rule Splitting

If a rule addresses 2+ distinct concerns, **proactively split** it into separate rules:

**Bad (too broad):**
> Create centralized color constants in dedicated files for consistent palettes, using semantic naming based on purpose rather than specific color values.

**Good (split into focused rules):**
- Define color constants in `theme/colors.ts` using semantic names (e.g., `primary`, `error`)
- Use semantic color tokens instead of literal hex values in components

##### Inline Examples in Rules

Inline examples (code, paths, patterns) within the rule content are **optional**. Only include them when they clarify something not obvious from the rule text.

**Types of useful inline examples:**
- Code syntax: `const`, `async/await`, `/** ... */`
- File paths: `infra/repositories/`, `domain/entities/`
- Naming patterns: `.spec.ts`, `I{Name}` prefix

**Good rules with inline examples:**
- "Use const instead of let for variables that are never reassigned"
- "Prefix interface names with I (e.g., `IUserService`)"
- "Place repository implementations in `infra/repositories/`"

**Good rules without inline examples:**
- "Name root describe block after the class or function under test"
- "Run linting before committing changes"
- "Keep business logic out of controllers"

**Bad rules:**
- "Write good code" (too vague)
- "Use const and prefix interfaces with I" (multiple concepts)
- "Don't use var" (no positive guidance)

#### Draft Summary

After saving the draft file, write a concise summary that captures:
- One sentence summarizing the standard's purpose
- A bullet list of all rules (each rule ~22 words max, imperative form, with inline code if helpful)

Then proceed directly to Step 3.

### Step 3: Add Examples

Add illustrative examples to each rule in the draft file.

#### Examples Creation

1. Open the existing draft file and add examples to each rule:
   - `### Positive Example` showing the compliant approach
   - `### Negative Example` highlighting the anti-pattern to avoid
   - Annotate every code block with its language (e.g., `typescript`, `sql`, `javascript`)
   - Keep examples concise and focused on demonstrating the specific rule
2. If a rule doesn't benefit from code examples (e.g., process or organizational rules), skip examples for that rule

#### Examples Guidelines

- Examples should be realistic and directly relevant to this codebase
- Each example should clearly demonstrate why the rule matters
- Keep code snippets minimal—only include what's necessary to illustrate the point

Valid language values for code blocks:
- TYPESCRIPT, TYPESCRIPT_TSX
- JAVASCRIPT, JAVASCRIPT_JSX
- PYTHON, JAVA, GO, RUST, CSHARP
- PHP, RUBY, KOTLIN, SWIFT, SQL
- HTML, CSS, SCSS, YAML, JSON
- MARKDOWN, BASH, GENERIC

Then proceed directly to Step 4.

### Step 4: Creating the Playbook File

Create a JSON playbook file named `<standard-name>.playbook.json` based on the draft content:

```json
{
  "name": "Your Standard Name",
  "description": "A clear description of what this standard covers, why it exists, and what problems it solves.",
  "scope": "Where this standard applies (e.g., 'TypeScript files', 'React components', '*.spec.ts test files')",
  "rules": [
    {
      "content": "First rule starting with action verb"
    },
    {
      "content": "Second rule with examples",
      "examples": {
        "positive": "const x = getValue();",
        "negative": "let x = getValue();",
        "language": "TYPESCRIPT"
      }
    }
  ]
}
```

#### Playbook Requirements

- **name**: Non-empty string
- **description**: Non-empty string explaining purpose
- **scope**: Non-empty string describing applicability
- **rules**: Array with at least one rule
- **rules[].content**: Non-empty string starting with action verb (max ~25 words)
- **rules[].examples** (optional): If provided, must include positive, negative, and language

#### Valid Language Values

TYPESCRIPT, TYPESCRIPT_TSX, JAVASCRIPT, JAVASCRIPT_JSX, PYTHON, JAVA, GO, RUST, CSHARP, PHP, RUBY, KOTLIN, SWIFT, SQL, HTML, CSS, SCSS, YAML, JSON, MARKDOWN, BASH, GENERIC

### Step 5: Review Before Submission

**Before running the CLI command**, you MUST get explicit user approval:

1. **Display a formatted recap** of the playbook content:

```
---
Name: <standard name>

Description: <description>

Scope: <scope>

Rules:

1. <rule content>
   - ✅ <positive example>
   - ❌ <negative example>
2. <rule content>
   - ✅ <positive example>
   - ❌ <negative example>
...
---
```

2. **Provide the file path** to the playbook JSON file so users can open and edit it directly if needed.

3. Ask: **"Here is the standard that will be created on Packmind. The playbook file is at `<path>` if you want to review or edit it. Do you approve?"**

4. **Wait for explicit user confirmation** before proceeding to Step 6.

5. If the user requests changes, go back to earlier steps to make adjustments.

### Step 6: Confirm and Submit

1. **Re-read the playbook file** from disk to capture any user edits.

2. **Compare with the original content** you created in Step 4.

3. **If changes were detected**:
   - Display the formatted recap again (same format as Step 5)
   - Ask: **"The file was modified. Here is the updated content that will be sent. Do you confirm?"**
   - **Wait for explicit confirmation** before proceeding.

4. **If no changes**: Proceed directly to submission.

5. Run the packmind-cli command:

```bash
packmind-cli standards create <path-to-playbook.json>
```

Example:
```bash
packmind-cli standards create ./typescript-conventions.playbook.json
```

Expected output on success:
```
packmind-cli Standard "Your Standard Name" created successfully (ID: <uuid>)
```

#### Troubleshooting

**"Not logged in" error:**
```bash
packmind-cli login
```

**"Failed to resolve global space" error:**
- Verify your API key is valid
- Check network connectivity to Packmind server

**JSON validation errors:**
- Ensure all required fields are present
- Verify JSON syntax is valid (use a JSON validator)
- Check that rules array has at least one entry

### Step 7: Cleanup

After the standard is **successfully created**, delete the temporary files:

1. Delete the playbook JSON file (e.g., `<standard-name>.playbook.json`)
2. Delete the draft markdown file in `.packmind/standards/_drafts/` if it exists

**Only clean up on success** - if the CLI command fails, keep the files so the user can retry.

## Complete Example

Here's a complete example creating a TypeScript testing standard:

**File: testing-conventions.playbook.json**
```json
{
  "name": "TypeScript Testing Conventions",
  "description": "Enforce consistent testing patterns in TypeScript test files to improve readability, maintainability, and reliability of the test suite.",
  "scope": "TypeScript test files (*.spec.ts, *.test.ts)",
  "rules": [
    {
      "content": "Use descriptive test names that explain the expected behavior",
      "examples": {
        "positive": "it('returns empty array when no items match filter')",
        "negative": "it('test filter')",
        "language": "TYPESCRIPT"
      }
    },
    {
      "content": "Follow Arrange-Act-Assert pattern in test structure",
      "examples": {
        "positive": "const input = createInput();\nconst result = processInput(input);\nexpect(result).toEqual(expected);",
        "negative": "expect(processInput(createInput())).toEqual(expected);",
        "language": "TYPESCRIPT"
      }
    },
    {
      "content": "Use one assertion per test for better error isolation",
      "examples": {
        "positive": "it('validates name', () => { expect(result.name).toBe('test'); });\nit('validates age', () => { expect(result.age).toBe(25); });",
        "negative": "it('validates user', () => { expect(result.name).toBe('test'); expect(result.age).toBe(25); });",
        "language": "TYPESCRIPT"
      }
    },
    {
      "content": "Avoid using 'should' at the start of test names - use assertive verb-first naming"
    }
  ]
}
```

**Creating the standard:**
```bash
packmind-cli standards create testing-conventions.playbook.json
```

## Quick Reference

| Field             | Required    | Description                              |
| ----------------- | ----------- | ---------------------------------------- |
| name              | Yes         | Standard name                            |
| description       | Yes         | What and why                             |
| summary           | No          | One-sentence (not yet supported by CLI)  |
| scope             | Yes (CLI)   | Where it applies                         |
| rules             | Yes         | At least one rule                        |
| rules[].content   | Yes         | Rule text (verb-first, max ~25 words)    |
| rules[].examples  | No          | Code examples                            |
| examples.positive | If examples | Valid code                               |
| examples.negative | If examples | Invalid code                             |
| examples.language | If examples | Language ID                              |
