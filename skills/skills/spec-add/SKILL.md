---
name: spec-add
description: Add specs, conventions, constraints, or learnings to project guidelines interactively or automatically
argument-hint: "[-y|--yes] [--type <convention|constraint|learning>] [--category <category>] [--dimension <specs|personal>] [--scope <global|project>] [--interactive] \"rule text\""
allowed-tools: AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep
---

# Spec Add Command

## Overview

Unified command for adding specs one at a time. Supports both interactive wizard mode and direct CLI mode.

**Key Features**:
- Supports both project specs and personal specs
- Scope selection (global vs project) for personal specs
- Category-based organization for workflow stages
- Interactive wizard mode with smart defaults
- Direct CLI mode with auto-detection of type and category
- Auto-confirm mode (`-y`/`--yes`) for scripted usage

## Use Cases

1. **During Session**: Capture important decisions as they're made
2. **After Session**: Reflect on lessons learned before archiving
3. **Proactive**: Add team conventions or architectural rules
4. **Interactive**: Guided wizard for adding rules with full control over dimension, scope, and category

## Usage

```bash
$spec-add                                                     # Interactive wizard (all prompts)
$spec-add --interactive                                       # Explicit interactive wizard
$spec-add "Use async/await instead of callbacks"              # Direct mode (auto-detect type)
$spec-add -y "No direct DB access" --type constraint          # Auto-confirm, skip confirmation
$spec-add --scope global --dimension personal                 # Create global personal spec (interactive)
$spec-add --dimension specs --category exploration            # Project spec in exploration category (interactive)
$spec-add "Cache invalidation requires event sourcing" --type learning --category architecture
```

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `rule` | string | Yes (unless `--interactive`) | - | The rule, convention, or insight to add |
| `--type` | enum | No | auto-detect | Type: `convention`, `constraint`, `learning` |
| `--category` | string | No | auto-detect / `general` | Category for organization (see categories below) |
| `--dimension` | enum | No | Interactive | `specs` (project) or `personal` |
| `--scope` | enum | No | `project` | `global` or `project` (only for personal dimension) |
| `--interactive` | flag | No | - | Launch full guided wizard for adding rules |
| `-y` / `--yes` | flag | No | - | Auto-categorize and add without confirmation |

### Type Categories

**convention** - Coding style preferences (goes to `conventions` section)
- Subcategories: `coding_style`, `naming_patterns`, `file_structure`, `documentation`

**constraint** - Hard rules that must not be violated (goes to `constraints` section)
- Subcategories: `architecture`, `tech_stack`, `performance`, `security`

**learning** - Session-specific insights (goes to `learnings` array)
- Subcategories: `architecture`, `performance`, `security`, `testing`, `process`, `other`

### Workflow Stage Categories (for `--category`)

| Category | Use Case | Example Rules |
|----------|----------|---------------|
| `general` | Applies to all stages | "Use TypeScript strict mode" |
| `exploration` | Code exploration, debugging | "Always trace the call stack before modifying" |
| `planning` | Task planning, requirements | "Break down tasks into 2-hour chunks" |
| `execution` | Implementation, testing | "Run tests after each file modification" |

## Execution Process

```
Input Parsing:
   |- Parse: rule text (positional argument, optional if --interactive)
   |- Parse: --type (convention|constraint|learning)
   |- Parse: --category (subcategory)
   |- Parse: --dimension (specs|personal)
   |- Parse: --scope (global|project)
   |- Parse: --interactive (flag)
   +- Parse: -y / --yes (flag)

Step 1: Parse Input

Step 2: Determine Mode
   |- If --interactive OR no rule text -> Full Interactive Wizard (Path A)
   +- If rule text provided -> Direct Mode (Path B)

Path A: Interactive Wizard
   |- Step A1: Ask dimension (if not specified)
   |- Step A2: Ask scope (if personal + scope not specified)
   |- Step A3: Ask category (if not specified)
   |- Step A4: Ask type (convention|constraint|learning)
   |- Step A5: Ask content (rule text)
   +- Continue to Step 3

Path B: Direct Mode
   |- Step B1: Auto-detect type (if not specified) using detectType()
   |- Step B2: Auto-detect category (if not specified) using detectCategory()
   |- Step B3: Default dimension to 'specs' if not specified
   +- Continue to Step 3

Step 3: Determine Target File
   |- specs dimension -> .ccw/specs/coding-conventions.md or architecture-constraints.md
   +- personal dimension -> ~/.ccw/personal/ or .ccw/personal/

Step 4: Validate and Write Spec
   |- Ensure target directory and file exist
   |- Check for duplicates
   |- Append rule to appropriate section
   +- Run ccw spec rebuild

Step 5: Display Confirmation
   +- If -y/--yes: Minimal output
   +- Otherwise: Full confirmation with location details
```

## Implementation

### Step 1: Parse Input

```javascript
// Parse arguments
const args = "$ARGUMENTS"
const argsLower = args.toLowerCase()

// Extract flags
const AUTO_YES = argsLower.includes('--yes') || argsLower.includes('-y')
const isInteractive = argsLower.includes('--interactive')

// Extract named parameters
const hasType = argsLower.includes('--type')
const hasCategory = argsLower.includes('--category')
const hasDimension = argsLower.includes('--dimension')
const hasScope = argsLower.includes('--scope')

let type = hasType ? args.match(/--type\s+(\w+)/i)?.[1]?.toLowerCase() : null
let category = hasCategory ? args.match(/--category\s+(\w+)/i)?.[1]?.toLowerCase() : null
let dimension = hasDimension ? args.match(/--dimension\s+(\w+)/i)?.[1]?.toLowerCase() : null
let scope = hasScope ? args.match(/--scope\s+(\w+)/i)?.[1]?.toLowerCase() : null

// Extract rule text (everything before flags, or quoted string)
let ruleText = args
  .replace(/--type\s+\w+/gi, '')
  .replace(/--category\s+\w+/gi, '')
  .replace(/--dimension\s+\w+/gi, '')
  .replace(/--scope\s+\w+/gi, '')
  .replace(/--interactive/gi, '')
  .replace(/--yes/gi, '')
  .replace(/-y\b/gi, '')
  .replace(/^["']|["']$/g, '')
  .trim()

// Validate values
if (scope && !['global', 'project'].includes(scope)) {
  console.log("Invalid scope. Use 'global' or 'project'.")
  return
}
if (dimension && !['specs', 'personal'].includes(dimension)) {
  console.log("Invalid dimension. Use 'specs' or 'personal'.")
  return
}
if (type && !['convention', 'constraint', 'learning'].includes(type)) {
  console.log("Invalid type. Use 'convention', 'constraint', or 'learning'.")
  return
}
if (category) {
  const validCategories = [
    'general', 'exploration', 'planning', 'execution',
    'coding_style', 'naming_patterns', 'file_structure', 'documentation',
    'architecture', 'tech_stack', 'performance', 'security',
    'testing', 'process', 'other'
  ]
  if (!validCategories.includes(category)) {
    console.log(`Invalid category. Valid categories: ${validCategories.join(', ')}`)
    return
  }
}
```

### Step 2: Determine Mode

```javascript
const useInteractiveWizard = isInteractive || !ruleText
```

### Path A: Interactive Wizard

```javascript
if (useInteractiveWizard) {

  // --- Step A1: Ask dimension (if not specified) ---
  if (!dimension) {
    if (AUTO_YES) {
      dimension = 'specs'  // Default to project specs in auto mode
    } else {
      const dimensionAnswer = ASK_USER([
        {
          id: "dimension", type: "select",
          prompt: "What type of spec do you want to create?",
          options: [
            { label: "Project Spec", description: "Coding conventions, constraints, quality rules for this project (stored in .ccw/specs/)" },
            { label: "Personal Spec", description: "Personal preferences and constraints that follow you across projects (stored in ~/.ccw/specs/personal/ or .ccw/specs/personal/)" }
          ]
        }
      ])  // BLOCKS (wait for user response)
      dimension = dimensionAnswer.dimension === "Project Spec" ? "specs" : "personal"
    }
  }

  // --- Step A2: Ask scope (if personal + scope not specified) ---
  if (dimension === 'personal' && !scope) {
    if (AUTO_YES) {
      scope = 'project'  // Default to project scope in auto mode
    } else {
      const scopeAnswer = ASK_USER([
        {
          id: "scope", type: "select",
          prompt: "Where should this personal spec be stored?",
          options: [
            { label: "Global (Recommended)", description: "Apply to ALL projects (~/.ccw/specs/personal/)" },
            { label: "Project-only", description: "Apply only to this project (.ccw/specs/personal/)" }
          ]
        }
      ])  // BLOCKS (wait for user response)
      scope = scopeAnswer.scope.includes("Global") ? "global" : "project"
    }
  }

  // --- Step A3: Ask category (if not specified) ---
  if (!category) {
    if (AUTO_YES) {
      category = 'general'  // Default to general in auto mode
    } else {
      const categoryAnswer = ASK_USER([
        {
          id: "category", type: "select",
          prompt: "Which workflow stage does this spec apply to?",
          options: [
            { label: "General (Recommended)", description: "Applies to all stages (default)" },
            { label: "Exploration", description: "Code exploration, analysis, debugging" },
            { label: "Planning", description: "Task planning, requirements gathering" },
            { label: "Execution", description: "Implementation, testing, deployment" }
          ]
        }
      ])  // BLOCKS (wait for user response)
      const categoryLabel = categoryAnswer.category
      category = categoryLabel.includes("General") ? "general"
        : categoryLabel.includes("Exploration") ? "exploration"
        : categoryLabel.includes("Planning") ? "planning"
        : "execution"
    }
  }

  // --- Step A4: Ask type (if not specified) ---
  if (!type) {
    if (AUTO_YES) {
      type = 'convention'  // Default to convention in auto mode
    } else {
      const typeAnswer = ASK_USER([
        {
          id: "type", type: "select",
          prompt: "What type of rule is this?",
          options: [
            { label: "Convention", description: "Coding style preference (e.g., use functional components)" },
            { label: "Constraint", description: "Hard rule that must not be violated (e.g., no direct DB access)" },
            { label: "Learning", description: "Insight or lesson learned (e.g., cache invalidation needs events)" }
          ]
        }
      ])  // BLOCKS (wait for user response)
      const typeLabel = typeAnswer.type
      type = typeLabel.includes("Convention") ? "convention"
        : typeLabel.includes("Constraint") ? "constraint"
        : "learning"
    }
  }

  // --- Step A5: Ask content (rule text) ---
  if (!ruleText) {
    if (AUTO_YES) {
      console.log("Error: Rule text is required in auto mode. Provide rule text as argument.")
      return
    }
    const contentAnswer = ASK_USER([
      {
        id: "content", type: "text",
        prompt: "Enter the rule or guideline text:"
      }
    ])  // BLOCKS (wait for user response)
    ruleText = contentAnswer.content
  }

}
```

### Path B: Direct Mode

**Auto-detect type if not specified**:

```javascript
function detectType(ruleText) {
  const text = ruleText.toLowerCase();

  // Constraint indicators
  if (/\b(no|never|must not|forbidden|prohibited|always must)\b/.test(text)) {
    return 'constraint';
  }

  // Learning indicators
  if (/\b(learned|discovered|realized|found that|turns out)\b/.test(text)) {
    return 'learning';
  }

  // Default to convention
  return 'convention';
}

function detectCategory(ruleText, type) {
  const text = ruleText.toLowerCase();

  if (type === 'constraint' || type === 'learning') {
    if (/\b(architecture|layer|module|dependency|circular)\b/.test(text)) return 'architecture';
    if (/\b(security|auth|permission|sanitize|xss|sql)\b/.test(text)) return 'security';
    if (/\b(performance|cache|lazy|async|sync|slow)\b/.test(text)) return 'performance';
    if (/\b(test|coverage|mock|stub)\b/.test(text)) return 'testing';
  }

  if (type === 'convention') {
    if (/\b(name|naming|prefix|suffix|camel|pascal)\b/.test(text)) return 'naming_patterns';
    if (/\b(file|folder|directory|structure|organize)\b/.test(text)) return 'file_structure';
    if (/\b(doc|comment|jsdoc|readme)\b/.test(text)) return 'documentation';
    return 'coding_style';
  }

  return type === 'constraint' ? 'tech_stack' : 'other';
}

if (!useInteractiveWizard) {
  if (!type) {
    type = detectType(ruleText)
  }
  if (!category) {
    category = detectCategory(ruleText, type)
  }
  if (!dimension) {
    dimension = 'specs'  // Default to project specs in direct mode
  }
}
```

### Step 3: Ensure Guidelines File Exists

**Uses .ccw/specs/ directory (same as frontend/backend spec-index-builder)**

```bash
bash(test -f .ccw/specs/coding-conventions.md && echo "EXISTS" || echo "NOT_FOUND")
```

**If NOT_FOUND**, initialize spec system:

```bash
Bash('ccw spec init')
Bash('ccw spec rebuild')
```

### Step 4: Determine Target File

```javascript
const path = require('path')
const os = require('os')

const isConvention = type === 'convention'
const isConstraint = type === 'constraint'
const isLearning = type === 'learning'

let targetFile
let targetDir

if (dimension === 'specs') {
  // Project specs - use .ccw/specs/ (same as frontend/backend spec-index-builder)
  targetDir = '.ccw/specs'
  if (isConstraint) {
    targetFile = path.join(targetDir, 'architecture-constraints.md')
  } else {
    targetFile = path.join(targetDir, 'coding-conventions.md')
  }
} else {
  // Personal specs - use .ccw/personal/ (same as backend spec-index-builder)
  if (scope === 'global') {
    targetDir = path.join(os.homedir(), '.ccw', 'personal')
  } else {
    targetDir = path.join('.ccw', 'personal')
  }

  // Create type-based filename
  const typePrefix = isConstraint ? 'constraints' : isLearning ? 'learnings' : 'conventions'
  targetFile = path.join(targetDir, `${typePrefix}.md`)
}
```

### Step 5: Build Entry

```javascript
function buildEntry(rule, type, category, sessionId) {
  if (type === 'learning') {
    return {
      date: new Date().toISOString().split('T')[0],
      session_id: sessionId || null,
      insight: rule,
      category: category,
      context: null
    };
  }

  // For conventions and constraints, just return the rule string
  return rule;
}
```

### Step 6: Write Spec

```javascript
const fs = require('fs')

// Ensure directory exists
if (!fs.existsSync(targetDir)) {
  fs.mkdirSync(targetDir, { recursive: true })
}

// Check if file exists
const fileExists = fs.existsSync(targetFile)

if (!fileExists) {
  // Create new file with frontmatter
  const frontmatter = `---
title: ${dimension === 'specs' ? 'Project' : 'Personal'} ${isConstraint ? 'Constraints' : isLearning ? 'Learnings' : 'Conventions'}
readMode: optional
priority: medium
category: ${category}
scope: ${dimension === 'personal' ? scope : 'project'}
dimension: ${dimension}
keywords: [${category}, ${isConstraint ? 'constraint' : isLearning ? 'learning' : 'convention'}]
---

# ${dimension === 'specs' ? 'Project' : 'Personal'} ${isConstraint ? 'Constraints' : isLearning ? 'Learnings' : 'Conventions'}

`
  fs.writeFileSync(targetFile, frontmatter, 'utf8')
}

// Read existing content
let content = fs.readFileSync(targetFile, 'utf8')

// Deduplicate: skip if rule text already exists in the file
if (content.includes(ruleText)) {
  console.log(`
Rule already exists in ${targetFile}
Text: "${ruleText}"
`)
  return
}

// Format the new rule based on type
let newRule
if (isLearning) {
  const entry = buildEntry(ruleText, type, category)
  newRule = `- [learning/${category}] ${entry.insight} (${entry.date})`
} else {
  newRule = `- [${category}] ${ruleText}`
}

// Append the rule
content = content.trimEnd() + '\n' + newRule + '\n'
fs.writeFileSync(targetFile, content, 'utf8')

// Rebuild spec index
Bash('ccw spec rebuild')
```

### Step 7: Display Confirmation

**If `-y`/`--yes` (auto mode)**:
```
Spec added: [${type}/${category}] "${ruleText}" -> ${targetFile}
```

**Otherwise (full confirmation)**:
```
Spec created successfully

Dimension: ${dimension}
Scope: ${dimension === 'personal' ? scope : 'project'}
Category: ${category}
Type: ${type}
Rule: "${ruleText}"

Location: ${targetFile}

Use 'ccw spec list' to view all specs
Use 'ccw spec load --category ${category}' to load specs by category
```

## Target File Resolution

### Project Specs (dimension: specs)
```
.ccw/specs/
|- coding-conventions.md       <- conventions, learnings
|- architecture-constraints.md <- constraints
+- quality-rules.md            <- quality rules
```

### Personal Specs (dimension: personal)
```
# Global (~/.ccw/personal/)
~/.ccw/personal/
|- conventions.md              <- personal conventions (all projects)
|- constraints.md              <- personal constraints (all projects)
+- learnings.md                <- personal learnings (all projects)

# Project-local (.ccw/personal/)
.ccw/personal/
|- conventions.md              <- personal conventions (this project only)
|- constraints.md              <- personal constraints (this project only)
+- learnings.md                <- personal learnings (this project only)
```

## Examples

### Interactive Wizard
```bash
$spec-add --interactive
# Prompts for: dimension -> scope (if personal) -> category -> type -> content
```

### Add a Convention (Direct)
```bash
$spec-add "Use async/await instead of callbacks" --type convention --category coding_style
```

Result in `.ccw/specs/coding-conventions.md`:
```markdown
- [coding_style] Use async/await instead of callbacks
```

### Add an Architectural Constraint (Direct)
```bash
$spec-add "No direct DB access from controllers" --type constraint --category architecture
```

Result in `.ccw/specs/architecture-constraints.md`:
```markdown
- [architecture] No direct DB access from controllers
```

### Capture a Learning (Direct, Auto-detect)
```bash
$spec-add "Cache invalidation requires event sourcing for consistency" --type learning
```

Result in `.ccw/specs/coding-conventions.md`:
```markdown
- [learning/architecture] Cache invalidation requires event sourcing for consistency (2026-03-06)
```

### Auto-confirm Mode
```bash
$spec-add -y "No direct DB access from controllers" --type constraint
# Auto-detects category as 'architecture', writes without confirmation prompt
```

### Personal Spec (Global)
```bash
$spec-add --scope global --dimension personal --type convention "Prefer descriptive variable names"
```

Result in `~/.ccw/personal/conventions.md`:
```markdown
- [general] Prefer descriptive variable names
```

### Personal Spec (Project)
```bash
$spec-add --scope project --dimension personal --type constraint "No ORM in this project"
```

Result in `.ccw/personal/constraints.md`:
```markdown
- [general] No ORM in this project
```

## Error Handling

- **Duplicate Rule**: Warn and skip if exact rule text already exists in target file
- **Invalid Category**: Suggest valid categories for the type
- **Invalid Scope**: Exit with error - must be 'global' or 'project'
- **Invalid Dimension**: Exit with error - must be 'specs' or 'personal'
- **Invalid Type**: Exit with error - must be 'convention', 'constraint', or 'learning'
- **File not writable**: Check permissions, suggest manual creation
- **Invalid path**: Exit with error message
- **File Corruption**: Backup existing file before modification

## Related Commands

- `$spec-setup` - Initialize project with specs scaffold
- `$session-sync` - Quick-sync session work to specs and project-tech
- `$workflow-session-start` - Start a session
- `$workflow-session-complete` - Complete session (prompts for learnings)
- `ccw spec list` - View all specs
- `ccw spec load --category <cat>` - Load filtered specs
- `ccw spec rebuild` - Rebuild spec index
