---
name: prompt-creation
description: Create context prompts for AI assistants in JSON or markdown frontmatter. Enforces mandatory context gathering (10 questions), validates schema compliance, ensures token efficiency. All content must be in English. Two types: technology-stack (project config) or behavioral (assistant persona). Trigger: When creating context prompts for AI assistants or documenting project configuration.
skills:
  - critical-partner
  - conventions
  - english-writing
---

# Prompt Creation Skill

## Purpose

Create standardized context prompts for AI assistants in `prompts/` directory. Two types: technology-stack (project config with versions/policies) or behavioral (assistant persona/rules). Enforces context gathering, validates schema compliance, ensures token efficiency. Uses JSON or markdown frontmatter format.

---

## When to Use

Use this skill when:

- Creating context prompts for AI assistants
- Defining technology stack configuration for projects
- Documenting behavioral rules for AI assistant personas
- Setting up language processing or communication guidelines

Don't use this skill for:

- Creating agent definitions (use agent-creation instead)
- Creating skills (use skill-creation instead)
- Modifying existing prompts without full context gathering

---

## English Writing

All generated code, documentation, comments, and prompt content must follow the [english-writing](../english-writing/SKILL.md) skill. Do not duplicate these rules here.

---

## Critical Patterns

### Pattern 1: Frontmatter vs Markdown Body (CRITICAL STRUCTURE)

**MANDATORY RULE**: Frontmatter for metadata ONLY, markdown body for all content/examples.

```markdown
---
# ✅ CORRECT: Frontmatter = metadata only (4-6 fields max)
name: english-practice
type: behavioral
description: English language teacher and technical writing coach
priority: high
---

# English Practice Prompt

## Overview

{Detailed explanation HERE in markdown}

## Persona

**Role**: English language teacher and technical writing coach

**Traits**:

- Patient with explanations
- Encouraging but precise
- Detail-oriented

## General Rules

1. Use only ASCII apostrophes (') and hyphens (-)
2. Never provide literal translations
3. Always explain corrections

## Instruction Types

### Practice Mode

**Behavior**: Review technical English text

**Rules**:

- Provide corrections with explanations
- Offer learning tips

### Translate Mode

**Behavior**: Translate Spanish to English

**Rules**:

- Never translate literally
- Explain phrasal verbs and idioms

## Examples

### Example 1: Status Update

**Input**: "Ayer termine el feature"

**Output**: "Yesterday I finished the feature"

**Explanation**: Past tense correction, article usage
```

```markdown
# ❌ WRONG: Content in frontmatter (bloated, hard to read)

---

name: english-practice
type: behavioral
persona:
role: Teacher
traits: - Patient - Encouraging
general_rules:

- Use ASCII apostrophes
- Never translate literally
  instruction_types:
  practice:
  behavior: Review text
  rules: - Provide corrections - Offer tips
  translate:
  behavior: Translate
  examples:
- input: "..."
  output: "..."

---

# (Empty or minimal markdown body)
```

**Why this matters**:

- Frontmatter = machine-readable metadata (name, type, priority)
- Markdown body = human-readable content (rules, examples, guidelines)
- Token efficiency: Markdown is more concise than nested YAML
- Readability: Prose > nested dictionaries

### Pattern 2: Mandatory Minimal Frontmatter

**MAXIMUM 4-6 FIELDS**: Only metadata, no content.

**Allowed Fields** (pick 4-6 only):

```yaml
---
name: prompt-identifier
type: behavioral | technology-stack
description: Single-line purpose statement
context: When and why to use this prompt
priority: low | medium | high
tags: [optional, comma-separated]
---
```

**PROHIBITED in Frontmatter** (move to markdown body):

- ❌ `persona:` with nested role/traits
- ❌ `general_rules:` with lists
- ❌ `instruction_types:` with nested behaviors
- ❌ `examples:` with nested input/output
- ❌ `evaluation_criteria:` with nested scoring
- ❌ `guidelines:` with nested sections
- ❌ Any content that users read (only metadata allowed)

**Validation**:

- Frontmatter < 10 lines total
- No nested objects beyond 1 level
- No arrays with >3 simple strings
- All prose, examples, rules in markdown body

### Pattern 3: Mandatory Context Gathering (10 Questions)

**CRITICAL**: NEVER create a prompt without gathering context first.

**Technology Stack Prompts - Ask:**

1. Project name? (filename)
2. Technologies used? (languages, frameworks, libraries + versions)
3. Key architectural patterns? (SSG, SPA, microservices)
4. Version constraints or compatibility requirements?
5. Core policies or conventions? (strict typing, accessibility)
6. Performance targets or optimization requirements?
7. Build tools or development environment?
8. Integration points or external dependencies?
9. Warnings or common pitfalls?
10. Examples needed? (patterns, configurations)

**Behavioral Prompts - Ask:**

1. Primary objective? (what should assistant help with?)
2. Persona to adopt? (teacher, reviewer, translator)
3. Core behavioral rules? (always/never do X)
4. Instruction types supported? (commands, modes, prefixes)
5. Default tone or communication style?
6. Language processing rules? (output language, translation)
7. Communication guidelines? (tone, structure, formatting)
8. Evaluation criteria? (accuracy, clarity, constructiveness)
9. Runtime behaviors? (missing context, version conflicts)
10. Examples needed? (Jira tickets, commit messages, translations)

```bash
# ❌ WRONG: Skip context gathering
Create English practice prompt
# [Agent creates generic prompt]

# ✅ CORRECT: Gather context first
What is the primary objective?
What persona should the assistant adopt?
# [After gathering 10 answers, create prompt]
```

### Pattern 4: Use Template from assets/

**CRITICAL**: Follow template structure exactly.

**Template Path**: `skills/prompt-creation/assets/PROMPT-TEMPLATE.md`

```bash
# Copy template to prompts directory
cp skills/prompt-creation/assets/PROMPT-TEMPLATE.md prompts/{prompt-name}.md

# Fill placeholders: {prompt-name}, {type}, {description}, etc.
```

**Structure Enforcement**:

1. **Frontmatter**: 4-6 metadata fields only (name, type, description, context, priority)
2. **Markdown Body**: All content organized in sections
   - Overview/Purpose
   - Persona (if behavioral)
   - General Rules
   - Instruction Types/Modes
   - Examples (with explanations)
   - Guidelines
   - Decision Tree (if complex)
   - Related Skills/Prompts
   - References

**Validation**: Generated prompt matches template structure (minimal frontmatter + structured markdown body)

### Pattern 5: Choose Prompt Type and Naming

**Two types:**

1. **technology-stack**: Project configuration
   - Naming: `{project-name}.md` (e.g., `sbd.md`, `usn.md`)
   - Contains: stack, policies, versioning, warnings, examples
   - Frontmatter: name, type, description, context

2. **behavioral**: Assistant persona/rules
   - Naming: `{behavior-name}.md` (e.g., `english-practice.md`)
   - Contains: persona, modes, rules, examples
   - Frontmatter: name, type, description, priority

### Pattern 6: Token Efficiency

**Principle**: Minimal frontmatter + concise markdown body = fewer tokens.

**Apply**:

- Use markdown lists/tables instead of nested YAML objects
- Examples in code blocks with explanations (not YAML dictionaries)
- Decision trees as markdown flowcharts (not nested YAML)
- Omit empty fields entirely (don't include `general_rules: []`)
- No redundant metadata (if it's in description, don't repeat elsewhere)

**Example (token-efficient structure)**:

```markdown
---
name: example-prompt
type: behavioral
description: Quick task handler with validation
priority: medium
---

# Example Prompt

## Rules

1. Always validate input format
2. Provide clear error messages
3. Use standard output formats

## Examples

### Valid Input

\`\`\`
Input: "Create user profile"
Output: Profile created with default settings (ID: usr_001)
\`\`\`

### Invalid Input

\`\`\`
Input: "xyz123"
Output: Error - Invalid command format. Expected: "verb + object"
\`\`\`
```

**Comparison (YAML vs Markdown)**:

```yaml
# ❌ WRONG: 15 tokens for one rule in frontmatter
general_rules:
  - rule: "Always validate input"
    explanation: "Check format before processing"

# ✅ CORRECT: 8 tokens for same rule in markdown body
## Rules
1. Always validate input (check format before processing)
```

### Pattern 7: Validate Against Schema

**Schema Path**: `skills/prompt-creation/assets/frontmatter-schema.json`

**Validation**:

- All required fields present (name, type, description)
- Field types correct (string, array, object)
- Enum values valid (type must be "behavioral" or "technology-stack")
- **Frontmatter < 10 lines total**
- **No nested objects beyond 1 level deep**
- **No arrays with >3 simple strings**

```bash
# Validate frontmatter structure
cat prompts/my-prompt.md | yq eval '.frontmatter' - | \
  yq eval-all '.' skills/prompt-creation/assets/frontmatter-schema.json -
```

### Pattern 8: Markdown Frontmatter (REQUIRED)

```markdown
---
name: project-name
type: tech-stack
stack:
  languages:
    - TypeScript 5.x
policies:
  - Strict typing required
---

# Additional markdown content if needed
```

JSON format available but markdown frontmatter preferred (more readable, same validation).

---

## Decision Tree

```
New prompt needed?
├─ [STEP 1] Gather Context
│   ├─ Technology stack? → Ask 10 tech questions (Pattern 3)
│   └─ Behavioral rules? → Ask 10 behavioral questions (Pattern 3)
│
├─ [STEP 2] Choose Structure Format
│   └─ REQUIRED: Markdown frontmatter with minimal metadata
│       ├─ Frontmatter: 4-6 fields ONLY (name, type, description, context/priority)
│       └─ Body: All rules, examples, persona in markdown sections
│
├─ [STEP 3] Choose Prompt Type & Naming
│   ├─ technology-stack? → {project-name}.md (e.g., sbd.md)
│   └─ behavioral? → {behavior-name}.md (e.g., english-practice.md)
│
├─ [STEP 4] Copy & Fill Template
│   ├─ Copy assets/PROMPT-TEMPLATE.md to prompts/{name}.md
│   ├─ Fill frontmatter: name, type, description, context/priority
│   └─ Fill markdown body: Overview, Rules, Examples, Persona, etc.
│
├─ [STEP 5] Validate Structure
│   ├─ Frontmatter < 10 lines? ✅
│   ├─ No nested YAML objects? ✅
│   ├─ All content in markdown body? ✅
│   └─ Schema validation passes? ✅
│
└─ [STEP 6] Review & Deliver
    ├─ Token efficiency check (Pattern 6)
    ├─ critical-partner review (optional)
    └─ Deliver to user with usage instructions
```

**Critical Checkpoints**:

- ⚠️ **STOP if**: User provides incomplete context → Ask clarifying questions first
- ⚠️ **REJECT if**: Frontmatter has >10 lines or nested objects → Move to markdown body
- ⚠️ **VALIDATE**: Must follow template structure exactly (Pattern 4)

---

## Edge Cases

### Case 1: User Provides Incomplete Context

```
# ❌ WRONG: Proceed anyway
User: "Create a prompt for my React project"
Agent: [Creates generic React prompt]

# ✅ CORRECT: Ask remaining questions
User: "Create a prompt for my React project"
Agent: "I need more context. Please answer:
1. What is the project name?
2. What React version?
3. What other libraries? (state management, UI, routing)
4. Any strict policies? (TypeScript, accessibility)
# ... (ask all 10 questions)
```

### Case 2: Conflicting Technology Versions

```yaml
# ❌ WRONG: Ignore conflicts
stack:
  frameworks:
    - React 18.x
  libraries:
    - react-router-dom 5.x  # Incompatible with React 18

# ✅ CORRECT: Flag compatibility issues
# Agent warns: "React Router 5 is incompatible with React 18. Use v6+"
stack:
  frameworks:
    - React 18.x
  libraries:
    - react-router-dom 6.x
warnings:
  - React Router must be v6+ for React 18 compatibility
```

### Case 3: Behavioral Prompt Without Clear Persona

```yaml
# ❌ WRONG: Vague persona
persona:
  role: Helper
  traits:
    - Nice

# ✅ CORRECT: Specific persona with actionable traits
persona:
  role: English teacher and technical writing coach
  traits:
    - Patient with explanations
    - Encouraging but precise with corrections
    - Detail-oriented in grammar feedback
```

### Case 4: Empty or Redundant Fields

```yaml
# ❌ WRONG: Include empty fields
warnings: []
examples: {}
optional_field: null

# ✅ CORRECT: Omit entirely (saves tokens)
# (no warnings, examples, or optional_field at all)
```

---

## Step-by-Step Workflow

### Step 1: Gather Context

**CRITICAL**: See [Pattern 1: Mandatory Context Gathering](#pattern-1-mandatory-context-gathering-10-questions) above.

Ask all 10 questions for the prompt type. Do not proceed without sufficient context.

---

### Step 2: Copy Template

See [Pattern 2: Use Template from assets/](#pattern-2-use-template-from-assets).

```bash
cp skills/prompt-creation/assets/PROMPT-TEMPLATE.md prompts/{prompt-name}.md
```

---

### Step 3: Determine Type and Name

See [Pattern 3: Choose Prompt Type and Naming](#pattern-3-choose-prompt-type-and-naming).

- Technology stack: `{project-name}.md` (type: `tech-stack`)
- Behavioral: `{behavior-name}.md` (type: `behavioral`)

---

### Step 4: Fill Template

Replace placeholders:

- `{prompt-name}`: Prompt identifier
- `{technology-stack | behavioral}`: Select type
- `{description}`: Brief purpose
- All section-specific placeholders

See [Examples](#examples) section below for complete templates.

---

### Step 5: Validate Structure

**CRITICAL VALIDATION**: Ensure minimal frontmatter + markdown body structure.

**Compliance Checklist:**

**Frontmatter Requirements:**

- [ ] Frontmatter < 10 lines total
- [ ] Only 4-6 metadata fields (name, type, description, context/priority, optional tags)
- [ ] No nested objects beyond 1 level (e.g., no `persona.role.traits`)
- [ ] No arrays with >3 simple strings in frontmatter
- [ ] YAML syntax valid (use `- item`, not `[]`)
- [ ] Empty fields omitted entirely (no `rules: []`)

**Markdown Body Requirements:**

- [ ] All prose content in markdown sections (not frontmatter)
- [ ] All examples in markdown code blocks (not YAML dictionaries)
- [ ] All rules/guidelines in markdown lists (not YAML arrays in frontmatter)
- [ ] Persona traits in markdown section (not `persona:` in frontmatter)
- [ ] Instruction types/modes as markdown headings (not `instruction_types:` in frontmatter)

**File Structure:**

- [ ] File created in `prompts/` directory
- [ ] Correct naming convention: `{behavior-name}.md` or `{project-name}.md`
- [ ] Follows template structure from `assets/PROMPT-TEMPLATE.md`
- [ ] Validates against `assets/frontmatter-schema.json`

**Quality Checks:**

- [ ] Token efficiency applied (Pattern 6: markdown > YAML)
- [ ] Examples included with clear context
- [ ] Reviewed by critical-partner (recommended for complex prompts)

---

## Examples

### Example 1: Technology Stack Prompt (CORRECT Structure)

**Filename**: `prompts/sbd.md`

````markdown
---
name: sbd
type: technology-stack
description: SBD web application stack configuration with strict typing and MUI patterns
context: Apply when working on SBD project codebase
---

# SBD Stack Configuration

## Overview

Web application for supply business distribution using React + TypeScript + MUI.

## Technology Stack

### Languages

- TypeScript 5.6.2
- JavaScript (ES2020+ for legacy modules)

### Frameworks

- React 18.3.1 (with Hooks)
- Webpack 5 (bundler)

### Libraries

- MUI 5.15.14 (Material-UI component library)
- Redux Toolkit 2.5.1 (state management + RTK Query)
- AG Grid 32.0.0 (data tables)
- Formik + Yup (forms + validation)

## Policies

1. **Strict Typing**: No `any` type allowed - use `unknown` or proper types
2. **MUI Components**: Prefer MUI over custom HTML for UI consistency
3. **Accessibility**: WCAG 2.1 AA compliance required (ARIA, keyboard nav)
4. **Redux Patterns**: Use RTK Query for data fetching, no legacy Redux

## Versioning

```json
{
  "typescript": ">=5.0.0 <6.0.0",
  "react": ">=18.0.0 <19.0.0",
  "@mui/material": ">=5.0.0 <6.0.0"
}
```
````

## Warnings

⚠️ **Avoid**:

- Legacy Redux patterns (createStore, thunks without RTK)
- Custom HTML when MUI equivalent exists
- Skipping accessibility attributes

✅ **Test**:

- Keyboard navigation on all interactive elements
- Screen reader compatibility (NVDA, JAWS)

````

### Example 2: Behavioral Prompt (CORRECT Structure)

**Filename**: `prompts/english-practice.md`

```markdown
---
name: english-practice
type: behavioral
description: English language teacher and technical writing coach for software developers
priority: high
---

# English Practice Prompt

## Overview

Help users practice technical English writing in software development contexts. Focus on grammar, punctuation, and natural phrasing.

## Persona

**Role**: English language teacher and technical writing coach

**Traits**:
- Patient with explanations
- Encouraging but precise with corrections
- Detail-oriented in grammar and punctuation
- Focused on natural, idiomatic English

## General Rules

1. **Punctuation**: Use only ASCII apostrophes (`'`) and hyphens (`-`), never curly quotes
2. **Explanations**: Always explain why a correction is needed
3. **Translations**: Never translate literally - use natural English phrasing
4. **Consistency**: Ensure punctuation and capitalization consistency

## Instruction Types

### Practice Mode

**Prefix**: `practice:`

**Behavior**: Review and correct English text with detailed feedback

**Rules**:
- Provide corrected version first
- Explain each correction with reasoning
- Offer learning tips for common mistakes
- Focus on technical vocabulary usage

**Example**:
````

User: "practice: Ayer termine el feature de authentication"
Assistant:
✅ Corrected: "Yesterday I finished the authentication feature"

Corrections:

1. "termine" → "finished" (past tense in English)
2. "el feature" → "the feature" (article in English)
3. "authentication" → correct technical term

```

### Translate Mode

**Prefix**: `translate:`

**Behavior**: Translate Spanish to natural English

**Rules**:
- Never translate word-by-word - use natural English
- Explain phrasal verbs and idioms
- Provide context for technical terms
- Suggest alternative phrasings when applicable

**Example**:
```

User: "translate: Este bug se presenta cuando el usuario intenta iniciar sesión"
Assistant:
✅ Translation: "This bug occurs when the user attempts to log in"

Notes:

- "se presenta" → "occurs" (not "presents itself" - unnatural)
- "iniciar sesión" → "log in" (standard tech term, not "start session")

```

## Evaluation Criteria

When reviewing text, check:
1. Grammar correctness (tense, subject-verb agreement)
2. Punctuation consistency (commas, periods, apostrophes)
3. Natural phrasing (idioms, common expressions)
4. Technical vocabulary accuracy
5. Clarity and conciseness

## Output Format

1. Corrected text (if applicable)
2. Detailed explanation of corrections
3. Learning tips or alternatives
4. Encouragement and next steps
```

---

## 🔍 Self-Check Protocol (For AI Agents)

**Before completing prompt creation, verify you have:**

### 1. Context Gathering

- [ ] Asked all 10 questions for prompt type (tech-stack or behavioral)
- [ ] Received sufficient answers (not vague or incomplete)
- [ ] Clarified ambiguous responses
- [ ] Confirmed prompt type matches user intent

### 2. Structure & Format (CRITICAL)

- [ ] **Frontmatter < 10 lines** (only metadata: name, type, description, context/priority)
- [ ] **No nested YAML objects in frontmatter** (e.g., no `persona.role`, `instruction_types.practice`)
- [ ] **All content in markdown body** (rules, examples, persona traits, instruction types)
- [ ] Copied template structure from `assets/PROMPT-TEMPLATE.md`
- [ ] Chosen correct naming convention (`{behavior}.md` or `{project}.md`)
- [ ] Replaced all placeholders with actual content
- [ ] Omitted empty fields entirely (no `rules: []` or `examples: {}`)

### 3. Content Quality

- [ ] Technology versions specified (if tech-stack)
- [ ] Persona is specific and actionable (if behavioral) - **in markdown section**
- [ ] Policies/rules are clear and enforceable - **in markdown lists**
- [ ] Examples included with explanations - **in markdown code blocks**
- [ ] Token-efficient (markdown > YAML for content)

### 4. Validation & Review

- [ ] YAML syntax validated (only for minimal frontmatter)
- [ ] Schema validation passed (`assets/frontmatter-schema.json`)
- [ ] Structure matches template exactly
- [ ] Critical-partner review (recommended for complex prompts)

**Confidence check:**

1. Is frontmatter truly minimal (< 10 lines, no nested objects)?
2. Is all prose content in markdown body (not YAML)?
3. Would this prompt be easy to read and maintain?
4. Does this provide sufficient context for AI assistants?

**If you answered NO to any:** Refactor structure (move content to markdown) or gather more context before finalizing.

**For complete validation:** See [Validation Checklist](#validation-checklist) below.

---

## Validation Checklist

**Before finalizing any prompt:**

### Frontmatter Structure

- [ ] Frontmatter < 10 lines total
- [ ] Only 4-6 metadata fields (name, type, description, context/priority, tags optional)
- [ ] No nested objects in frontmatter (e.g., no `persona.role`, `stack.languages.list`)
- [ ] No arrays with >3 simple strings in frontmatter
- [ ] YAML syntax valid (use `- item`, not `[]`)
- [ ] Empty fields omitted entirely

### Markdown Body Structure

- [ ] All rules/policies in markdown lists (## Rules section)
- [ ] All examples in markdown code blocks (## Examples section)
- [ ] Persona traits in markdown section (## Persona, not `persona:` in frontmatter)
- [ ] Instruction types as markdown headings (### Practice Mode, not `instruction_types:` YAML)
- [ ] Guidelines in markdown prose (## Guidelines section)

### File & Naming

- [ ] File created in `prompts/` directory
- [ ] Correct naming: `{behavior-name}.md` or `{project-name}.md`
- [ ] Type matches content (behavioral vs technology-stack)

### Content Quality

- [ ] Context gathered (answered 10 questions for prompt type)
- [ ] Template structure followed from `assets/PROMPT-TEMPLATE.md`
- [ ] Technology versions specified (if tech-stack)
- [ ] Examples included with explanations
- [ ] Token-efficient (markdown > YAML for content)

### Technical Validation

- [ ] Validates against `assets/frontmatter-schema.json`
- [ ] Critical-partner review completed (recommended for complex prompts)

---

## Quick Reference

| Aspect      | Technology Stack            | Behavioral                        |
| ----------- | --------------------------- | --------------------------------- |
| Type        | `tech-stack`                | `behavioral`                      |
| Naming      | `{project}.md`              | `{behavior}.md`                   |
| Key Fields  | stack, policies, versioning | objective, persona, general_rules |
| Examples    | `sbd.md`, `usn.md`          | `english-practice.md`             |
| Context Q's | 10 tech questions           | 10 behavioral questions           |

---

## References

- [agent-creation](../agent-creation/SKILL.md): Creating agent definitions
- [skill-creation](../skill-creation/SKILL.md): Creating skill definitions
- [critical-partner](../critical-partner/SKILL.md): Review and validation
- [conventions](../conventions/SKILL.md): General coding conventions
- [humanizer](../humanizer/SKILL.md): Empathy, clarity, and human-centric communication patterns for prompts and assistants
