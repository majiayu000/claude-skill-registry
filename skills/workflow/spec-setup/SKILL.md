---
name: spec-setup
description: Initialize project-level state and configure specs via interactive questionnaire using cli-explore-agent
argument-hint: "[--regenerate] [--skip-specs] [--reset]"
allowed-tools: spawn_agent, wait, send_input, close_agent, AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep
---

# Workflow Spec Setup Command

## Overview

Initialize `.workflow/project-tech.json` and `.ccw/specs/*.md` with comprehensive project understanding by delegating analysis to **cli-explore-agent**, then interactively configure project guidelines through a multi-round questionnaire.

**Dual File System**:
- `project-tech.json`: Auto-generated technical analysis (stack, architecture, components)
- `specs/*.md`: User-maintained rules and constraints (created and populated interactively)

**Design Principle**: Questions are dynamically generated based on the project's tech stack, architecture, and patterns -- not generic boilerplate.

**Note**: This command may be called by other workflow commands. Upon completion, return immediately to continue the calling workflow without interrupting the task flow.

## Usage

```bash
$spec-setup                 # Initialize (skip if exists)
$spec-setup --regenerate    # Force regeneration of project-tech.json
$spec-setup --skip-specs    # Initialize project-tech only, skip spec initialization and questionnaire
$spec-setup --reset         # Reset specs content before questionnaire
```

## Execution Process

```
Input Parsing:
   |- Parse --regenerate flag -> regenerate = true | false
   |- Parse --skip-specs flag -> skipSpecs = true | false
   +- Parse --reset flag -> reset = true | false

Decision:
   |- BOTH_EXIST + no --regenerate + no --reset -> Exit: "Already initialized"
   |- EXISTS + --regenerate -> Backup existing -> Continue analysis
   |- EXISTS + --reset -> Reset specs, keep project-tech -> Skip to questionnaire
   +- NOT_FOUND -> Continue full flow

Full Flow:
   |- Step 1: Parse input and check existing state
   |- Step 2: Get project metadata (name, root)
   |- Step 3: Invoke cli-explore-agent (subagent)
   |   |- Structural scan (get_modules_by_depth.sh, find, wc)
   |   |- Semantic analysis (Gemini CLI)
   |   |- Synthesis and merge
   |   +- Write .workflow/project-tech.json
   |- Step 4: Initialize Spec System (if not --skip-specs)
   |   |- Check if specs/*.md exist
   |   |- If NOT_FOUND -> Run ccw spec init
   |   +- Run ccw spec rebuild
   |- Step 5: Multi-Round Interactive Questionnaire (if not --skip-specs)
   |   |- Check if guidelines already populated -> Ask: "Append / Reset / Cancel"
   |   |- Load project context from project-tech.json
   |   |- Round 1: Coding Conventions (coding_style, naming_patterns)
   |   |- Round 2: File & Documentation Conventions (file_structure, documentation)
   |   |- Round 3: Architecture & Tech Constraints (architecture, tech_stack)
   |   |- Round 4: Performance & Security Constraints (performance, security)
   |   +- Round 5: Quality Rules (quality_rules)
   |- Step 6: Write specs/*.md (if not --skip-specs)
   +- Step 7: Display Summary

Output:
   |- .workflow/project-tech.json (+ .backup if regenerate)
   +- .ccw/specs/*.md (scaffold or configured, unless --skip-specs)
```

## Implementation

### Step 1: Parse Input and Check Existing State

**Parse flags**:
```javascript
const regenerate = $ARGUMENTS.includes('--regenerate')
const skipSpecs = $ARGUMENTS.includes('--skip-specs')
const reset = $ARGUMENTS.includes('--reset')
```

**Check existing state**:

```bash
bash(test -f .workflow/project-tech.json && echo "TECH_EXISTS" || echo "TECH_NOT_FOUND")
bash(test -f .ccw/specs/coding-conventions.md && echo "SPECS_EXISTS" || echo "SPECS_NOT_FOUND")
```

**If BOTH_EXIST and no --regenerate and no --reset**: Exit early
```
Project already initialized:
- Tech analysis: .workflow/project-tech.json
- Guidelines: .ccw/specs/*.md

Use $spec-setup --regenerate to rebuild tech analysis
Use $spec-setup --reset to reconfigure guidelines
Use $spec-add to add individual rules
Use $workflow-status --project to view state
```

### Step 2: Get Project Metadata

```bash
bash(basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)")
bash(git rev-parse --show-toplevel 2>/dev/null || pwd)
bash(mkdir -p .workflow)
```

### Step 3: Invoke cli-explore-agent (Subagent)

**For --regenerate**: Backup and preserve existing data
```bash
bash(cp .workflow/project-tech.json .workflow/project-tech.json.backup)
```

**Delegate analysis to subagent**:

```javascript
let exploreAgent = null

try {
  exploreAgent = spawn_agent({
    message: `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS (Agent Execute)
1. **Read role definition**: ~/.codex/agents/cli-explore-agent.md (MUST read first)
2. Read: .workflow/project-tech.json (if exists, for --regenerate)

---

Analyze project for workflow initialization and generate .workflow/project-tech.json.

## MANDATORY FIRST STEPS
1. Execute: cat ~/.ccw/workflows/cli-templates/schemas/project-tech-schema.json (get schema reference)
2. Execute: ccw tool exec get_modules_by_depth '{}' (get project structure)

## Task
Generate complete project-tech.json following the schema structure:
- project_name: "${projectName}"
- initialized_at: ISO 8601 timestamp
- overview: {
    description: "Brief project description",
    technology_stack: {
      languages: [{name, file_count, primary}],
      frameworks: ["string"],
      build_tools: ["string"],
      test_frameworks: ["string"]
    },
    architecture: {style, layers: [], patterns: []},
    key_components: [{name, path, description, importance}]
  }
- features: []
- development_index: ${regenerate ? 'preserve from backup' : '{feature: [], enhancement: [], bugfix: [], refactor: [], docs: []}'}
- statistics: ${regenerate ? 'preserve from backup' : '{total_features: 0, total_sessions: 0, last_updated: ISO timestamp}'}
- _metadata: {initialized_by: "cli-explore-agent", analysis_timestamp: ISO timestamp, analysis_mode: "deep-scan"}

## Analysis Requirements

**Technology Stack**:
- Languages: File counts, mark primary
- Frameworks: From package.json, requirements.txt, go.mod, etc.
- Build tools: npm, cargo, maven, webpack, vite
- Test frameworks: jest, pytest, go test, junit

**Architecture**:
- Style: MVC, microservices, layered (from structure & imports)
- Layers: presentation, business-logic, data-access
- Patterns: singleton, factory, repository
- Key components: 5-10 modules {name, path, description, importance}

## Execution
1. Structural scan: get_modules_by_depth.sh, find, wc -l
2. Semantic analysis: Gemini for patterns/architecture
3. Synthesis: Merge findings
4. ${regenerate ? 'Merge with preserved development_index and statistics from .workflow/project-tech.json.backup' : ''}
5. Write JSON: Write('.workflow/project-tech.json', jsonContent)
6. Report: Return brief completion summary

Project root: ${projectRoot}
`
  })

  // Wait for completion
  const result = wait({ ids: [exploreAgent], timeout_ms: 600000 })

  if (result.timed_out) {
    send_input({ id: exploreAgent, message: 'Complete analysis now and write project-tech.json.' })
    const retry = wait({ ids: [exploreAgent], timeout_ms: 300000 })
    if (retry.timed_out) throw new Error('Agent timeout')
  }

} finally {
  if (exploreAgent) close_agent({ id: exploreAgent })
}
```

### Step 4: Initialize Spec System (if not --skip-specs)

```javascript
// Skip spec initialization if --skip-specs flag is provided
if (!skipSpecs) {
  // Initialize spec system if not already initialized
  const specsCheck = Bash('test -f .ccw/specs/coding-conventions.md && echo EXISTS || echo NOT_FOUND')
  if (specsCheck.includes('NOT_FOUND')) {
    console.log('Initializing spec system...')
    Bash('ccw spec init')
    Bash('ccw spec rebuild')
  }
} else {
  console.log('Skipping spec initialization and questionnaire (--skip-specs)')
}
```

If `--skip-specs` is provided, skip directly to Step 7 (Display Summary) with limited output.

### Step 5: Multi-Round Interactive Questionnaire (if not --skip-specs)

#### Step 5.0: Check Existing Guidelines

If guidelines already have content, ask the user how to proceed:

```javascript
// Check if specs already have content via ccw spec list
const specsList = Bash('ccw spec list --json 2>/dev/null || echo "{}"')
const specsData = JSON.parse(specsList)
const isPopulated = (specsData.total || 0) > 5  // More than seed docs

if (isPopulated && !reset) {
  const mode = ASK_USER([
    {
      id: "mode", type: "select",
      prompt: "Project guidelines already contain entries. How would you like to proceed?",
      options: [
        { label: "Append", description: "Keep existing entries and add new ones from the wizard" },
        { label: "Reset", description: "Clear all existing entries and start fresh" },
        { label: "Cancel", description: "Exit without changes" }
      ],
      default: "Append"
    }
  ])  // BLOCKS (wait for user response)

  // If Cancel -> exit
  // If Reset -> clear all arrays before proceeding
  // If Append -> keep existing, wizard adds to them
}

// If --reset flag was provided, clear existing entries before proceeding
if (reset) {
  // Reset specs content
  console.log('Resetting existing guidelines...')
}
```

#### Step 5.1: Load Project Context

```javascript
// Load project context via ccw spec load for planning context
const projectContext = Bash('ccw spec load --category planning 2>/dev/null || echo "{}"')
const specData = JSON.parse(projectContext)

// Extract key info from loaded specs for generating smart questions
const languages = specData.overview?.technology_stack?.languages || []
const primaryLang = languages.find(l => l.primary)?.name || languages[0]?.name || 'Unknown'
const frameworks = specData.overview?.technology_stack?.frameworks || []
const testFrameworks = specData.overview?.technology_stack?.test_frameworks || []
const archStyle = specData.overview?.architecture?.style || 'Unknown'
const archPatterns = specData.overview?.architecture?.patterns || []
const buildTools = specData.overview?.technology_stack?.build_tools || []
```

#### Step 5.2: Multi-Round Questionnaire

Each round uses `ASK_USER` with project-aware options. The user can always select "Other" to provide custom input.

**CRITICAL**: After each round, collect the user's answers and convert them into guideline entries. Do NOT batch all rounds -- process each round's answers before proceeding to the next.

---

##### Round 1: Coding Conventions

Generate options dynamically based on detected language/framework:

```javascript
// Build language-specific coding style options
const codingStyleOptions = []

if (['TypeScript', 'JavaScript'].includes(primaryLang)) {
  codingStyleOptions.push(
    { label: "Strict TypeScript", description: "Use strict mode, no 'any' type, explicit return types for public APIs" },
    { label: "Functional style", description: "Prefer pure functions, immutability, avoid class-based patterns where possible" },
    { label: "Const over let", description: "Always use const; only use let when reassignment is truly needed" }
  )
} else if (primaryLang === 'Python') {
  codingStyleOptions.push(
    { label: "Type hints", description: "Use type hints for all function signatures and class attributes" },
    { label: "Functional style", description: "Prefer pure functions, list comprehensions, avoid mutable state" },
    { label: "PEP 8 strict", description: "Strict PEP 8 compliance with max line length 88 (Black formatter)" }
  )
} else if (primaryLang === 'Go') {
  codingStyleOptions.push(
    { label: "Error wrapping", description: "Always wrap errors with context using fmt.Errorf with %w" },
    { label: "Interface first", description: "Define interfaces at the consumer side, not the provider" },
    { label: "Table-driven tests", description: "Use table-driven test pattern for all unit tests" }
  )
}
// Add universal options
codingStyleOptions.push(
  { label: "Early returns", description: "Prefer early returns / guard clauses over deep nesting" }
)

// Round 1: Coding Conventions
const round1 = ASK_USER([
  {
    id: "coding_style", type: "multi-select",
    prompt: `Your project uses ${primaryLang}. Which coding style conventions do you follow?`,
    options: codingStyleOptions.slice(0, 4) // Max 4 options
  },
  {
    id: "naming", type: "multi-select",
    prompt: `What naming conventions does your ${primaryLang} project use?`,
    options: [
      { label: "camelCase variables", description: "Variables and functions use camelCase (e.g., getUserName)" },
      { label: "PascalCase types", description: "Classes, interfaces, type aliases use PascalCase (e.g., UserService)" },
      { label: "UPPER_SNAKE constants", description: "Constants use UPPER_SNAKE_CASE (e.g., MAX_RETRIES)" },
      { label: "Prefix interfaces", description: "Prefix interfaces with 'I' (e.g., IUserService)" }
    ]
  }
])  // BLOCKS (wait for user response)
```

**Process Round 1 answers** -> add to `conventions.coding_style` and `conventions.naming_patterns` arrays.

---

##### Round 2: File Structure & Documentation

```javascript
// Round 2: File Structure & Documentation
const round2 = ASK_USER([
  {
    id: "file_structure", type: "multi-select",
    prompt: `Your project has a ${archStyle} architecture. What file organization rules apply?`,
    options: [
      { label: "Co-located tests", description: "Test files live next to source files (e.g., foo.ts + foo.test.ts)" },
      { label: "Separate test dir", description: "Tests in a dedicated __tests__ or tests/ directory" },
      { label: "One export per file", description: "Each file exports a single main component/class/function" },
      { label: "Index barrels", description: "Use index.ts barrel files for clean imports from directories" }
    ]
  },
  {
    id: "documentation", type: "multi-select",
    prompt: "What documentation standards does your project follow?",
    options: [
      { label: "JSDoc/docstring public APIs", description: "All public functions and classes must have JSDoc/docstrings" },
      { label: "README per module", description: "Each major module/package has its own README" },
      { label: "Inline comments for why", description: "Comments explain 'why', not 'what' -- code should be self-documenting" },
      { label: "No comment requirement", description: "Code should be self-explanatory; comments only for non-obvious logic" }
    ]
  }
])  // BLOCKS (wait for user response)
```

**Process Round 2 answers** -> add to `conventions.file_structure` and `conventions.documentation`.

---

##### Round 3: Architecture & Tech Stack Constraints

```javascript
// Build architecture-specific options
const archOptions = []

if (archStyle.toLowerCase().includes('monolith')) {
  archOptions.push(
    { label: "No circular deps", description: "Modules must not have circular dependencies" },
    { label: "Layer boundaries", description: "Strict layer separation: UI -> Service -> Data (no skipping layers)" }
  )
} else if (archStyle.toLowerCase().includes('microservice')) {
  archOptions.push(
    { label: "Service isolation", description: "Services must not share databases or internal state" },
    { label: "API contracts", description: "All inter-service communication through versioned API contracts" }
  )
}
archOptions.push(
  { label: "Stateless services", description: "Service/business logic must be stateless (state in DB/cache only)" },
  { label: "Dependency injection", description: "Use dependency injection for testability, no hardcoded dependencies" }
)

// Round 3: Architecture & Tech Stack Constraints
const round3 = ASK_USER([
  {
    id: "architecture", type: "multi-select",
    prompt: `Your ${archStyle} architecture uses ${archPatterns.join(', ') || 'various'} patterns. What architecture constraints apply?`,
    options: archOptions.slice(0, 4)
  },
  {
    id: "tech_stack", type: "multi-select",
    prompt: `Tech stack: ${frameworks.join(', ')}. What technology constraints apply?`,
    options: [
      { label: "No new deps without review", description: "Adding new dependencies requires explicit justification and review" },
      { label: "Pin dependency versions", description: "All dependencies must use exact versions, not ranges" },
      { label: "Prefer native APIs", description: "Use built-in/native APIs over third-party libraries when possible" },
      { label: "Framework conventions", description: `Follow official ${frameworks[0] || 'framework'} conventions and best practices` }
    ]
  }
])  // BLOCKS (wait for user response)
```

**Process Round 3 answers** -> add to `constraints.architecture` and `constraints.tech_stack`.

---

##### Round 4: Performance & Security Constraints

```javascript
// Round 4: Performance & Security Constraints
const round4 = ASK_USER([
  {
    id: "performance", type: "multi-select",
    prompt: "What performance requirements does your project have?",
    options: [
      { label: "API response time", description: "API endpoints must respond within 200ms (p95)" },
      { label: "Bundle size limit", description: "Frontend bundle size must stay under 500KB gzipped" },
      { label: "Lazy loading", description: "Large modules/routes must use lazy loading / code splitting" },
      { label: "No N+1 queries", description: "Database access must avoid N+1 query patterns" }
    ]
  },
  {
    id: "security", type: "multi-select",
    prompt: "What security requirements does your project enforce?",
    options: [
      { label: "Input sanitization", description: "All user input must be validated and sanitized before use" },
      { label: "No secrets in code", description: "No API keys, passwords, or tokens in source code -- use env vars" },
      { label: "Auth on all endpoints", description: "All API endpoints require authentication unless explicitly public" },
      { label: "Parameterized queries", description: "All database queries must use parameterized/prepared statements" }
    ]
  }
])  // BLOCKS (wait for user response)
```

**Process Round 4 answers** -> add to `constraints.performance` and `constraints.security`.

---

##### Round 5: Quality Rules

```javascript
// Round 5: Quality Rules
const round5 = ASK_USER([
  {
    id: "quality", type: "multi-select",
    prompt: `Testing with ${testFrameworks.join(', ') || 'your test framework'}. What quality rules apply?`,
    options: [
      { label: "Min test coverage", description: "Minimum 80% code coverage for new code; no merging below threshold" },
      { label: "No skipped tests", description: "Tests must not be skipped (.skip/.only) in committed code" },
      { label: "Lint must pass", description: "All code must pass linter checks before commit (enforced by pre-commit)" },
      { label: "Type check must pass", description: "Full type checking (tsc --noEmit) must pass with zero errors" }
    ]
  }
])  // BLOCKS (wait for user response)
```

**Process Round 5 answers** -> add to `quality_rules` array as `{ rule, scope, enforced_by }` objects.

### Step 6: Write specs/*.md (if not --skip-specs)

For each category of collected answers, append rules to the corresponding spec MD file. Each spec file uses YAML frontmatter with `readMode`, `priority`, `category`, and `keywords`.

**Category Assignment**: Based on the round and question type:
- Round 1-2 (conventions): `category: general` (applies to all stages)
- Round 3 (architecture/tech): `category: planning` (planning phase)
- Round 4 (performance/security): `category: execution` (implementation phase)
- Round 5 (quality): `category: execution` (testing phase)

```javascript
// Helper: append rules to a spec MD file with category support
// Uses .ccw/specs/ directory (same as frontend/backend spec-index-builder)
function appendRulesToSpecFile(filePath, rules, defaultCategory = 'general') {
  if (rules.length === 0) return

  // Ensure .ccw/specs/ directory exists
  const specDir = path.dirname(filePath)
  if (!fs.existsSync(specDir)) {
    fs.mkdirSync(specDir, { recursive: true })
  }

  // Check if file exists
  if (!file_exists(filePath)) {
    // Create file with frontmatter including category
    const frontmatter = `---
title: ${filePath.includes('conventions') ? 'Coding Conventions' : filePath.includes('constraints') ? 'Architecture Constraints' : 'Quality Rules'}
readMode: optional
priority: medium
category: ${defaultCategory}
scope: project
dimension: specs
keywords: [${defaultCategory}, ${filePath.includes('conventions') ? 'convention' : filePath.includes('constraints') ? 'constraint' : 'quality'}]
---

# ${filePath.includes('conventions') ? 'Coding Conventions' : filePath.includes('constraints') ? 'Architecture Constraints' : 'Quality Rules'}

`
    Write(filePath, frontmatter)
  }

  const existing = Read(filePath)
  // Append new rules as markdown list items after existing content
  const newContent = existing.trimEnd() + '\n' + rules.map(r => `- ${r}`).join('\n') + '\n'
  Write(filePath, newContent)
}

// Write conventions (general category) - use .ccw/specs/ (same as frontend/backend)
appendRulesToSpecFile('.ccw/specs/coding-conventions.md',
  [...newCodingStyle, ...newNamingPatterns, ...newFileStructure, ...newDocumentation],
  'general')

// Write constraints (planning category)
appendRulesToSpecFile('.ccw/specs/architecture-constraints.md',
  [...newArchitecture, ...newTechStack, ...newPerformance, ...newSecurity],
  'planning')

// Write quality rules (execution category)
if (newQualityRules.length > 0) {
  const qualityPath = '.ccw/specs/quality-rules.md'
  if (!file_exists(qualityPath)) {
    Write(qualityPath, `---
title: Quality Rules
readMode: required
priority: high
category: execution
scope: project
dimension: specs
keywords: [execution, quality, testing, coverage, lint]
---

# Quality Rules

`)
  }
  appendRulesToSpecFile(qualityPath,
    newQualityRules.map(q => `${q.rule} (scope: ${q.scope}, enforced by: ${q.enforced_by})`),
    'execution')
}

// Rebuild spec index after writing
Bash('ccw spec rebuild')
```

#### Answer Processing Rules

When converting user selections to guideline entries:

1. **Selected option** -> Use the option's `description` as the guideline string (it's more precise than the label)
2. **"Other" with custom text** -> Use the user's text directly as the guideline string
3. **Deduplication** -> Skip entries that already exist in the guidelines (exact string match)
4. **Quality rules** -> Convert to `{ rule: description, scope: "all", enforced_by: "code-review" }` format

### Step 7: Display Summary

```javascript
const projectTech = JSON.parse(Read('.workflow/project-tech.json'));

if (skipSpecs) {
  // Minimal summary for --skip-specs mode
  console.log(`
Project initialized successfully (tech analysis only)

## Project Overview
Name: ${projectTech.project_name}
Description: ${projectTech.overview.description}

### Technology Stack
Languages: ${projectTech.overview.technology_stack.languages.map(l => l.name).join(', ')}
Frameworks: ${projectTech.overview.technology_stack.frameworks.join(', ')}

### Architecture
Style: ${projectTech.overview.architecture.style}
Components: ${projectTech.overview.key_components.length} core modules

---
Files created:
- Tech analysis: .workflow/project-tech.json
- Specs: (skipped via --skip-specs)
${regenerate ? '- Backup: .workflow/project-tech.json.backup' : ''}

Next steps:
- Use $spec-setup (without --skip-specs) to configure guidelines
- Use $spec-add to create individual specs
- Use $workflow-plan to start planning
`);
} else {
  // Full summary with guidelines stats
  const countConventions = newCodingStyle.length + newNamingPatterns.length
    + newFileStructure.length + newDocumentation.length
  const countConstraints = newArchitecture.length + newTechStack.length
    + newPerformance.length + newSecurity.length
  const countQuality = newQualityRules.length

  // Get updated spec list
  const specsList = Bash('ccw spec list --json 2>/dev/null || echo "{}"')

  console.log(`
Project initialized and guidelines configured

## Project Overview
Name: ${projectTech.project_name}
Description: ${projectTech.overview.description}

### Technology Stack
Languages: ${projectTech.overview.technology_stack.languages.map(l => l.name).join(', ')}
Frameworks: ${projectTech.overview.technology_stack.frameworks.join(', ')}

### Architecture
Style: ${projectTech.overview.architecture.style}
Components: ${projectTech.overview.key_components.length} core modules

### Guidelines Summary
- Conventions: ${countConventions} rules added to coding-conventions.md
- Constraints: ${countConstraints} rules added to architecture-constraints.md
- Quality rules: ${countQuality} rules added to quality-rules.md

Spec index rebuilt. Use \`ccw spec list\` to view all specs.

---
Files created:
- Tech analysis: .workflow/project-tech.json
- Specs: .ccw/specs/ (configured)
${regenerate ? '- Backup: .workflow/project-tech.json.backup' : ''}

Next steps:
- Use $spec-add to add individual rules later
- Specs are auto-loaded via hook on each prompt
- Use $workflow-plan to start planning
`);
}
```

## Error Handling

| Situation | Action |
|-----------|--------|
| **Agent Failure** | Fall back to basic initialization with placeholder overview |
| **Missing Tools** | Agent uses Qwen fallback or bash-only |
| **Empty Project** | Create minimal JSON with all gaps identified |
| **No project-tech.json** (when --reset without prior init) | Run full flow from Step 2 |
| **User cancels mid-wizard** | Save whatever was collected so far (partial is better than nothing) |
| **File write failure** | Report error, suggest manual edit |

## Related Commands

- `$spec-add` - Interactive wizard to create individual specs with scope selection
- `$session-sync` - Quick-sync session work to specs and project-tech
- `$workflow-plan` - Start planning with initialized project context
- `$workflow-status --project` - View project state and guidelines
