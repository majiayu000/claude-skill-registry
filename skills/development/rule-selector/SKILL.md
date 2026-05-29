---
name: rule-selector
description: Analyzes project tech stack and recommends optimal rule configuration. Detects frameworks from package.json, requirements.txt, go.mod, and other config files. Generates custom manifest.yaml profiles for your specific stack.
context:fork: true
allowed-tools: read, glob, grep, search
min_required_version: 1.0.0
compatible_versions: '^1.0.0'
---

# Rule Selector

Intelligently detects your tech stack and configures optimal coding rules.

## When to Use

- Setting up rules for a new project
- Onboarding to an existing codebase
- Updating rules after adding new dependencies
- Auditing rule configuration for optimization
- Generating team-specific rule profiles

## Instructions

### Step 1: Detect Project Type

Scan for configuration files to identify the tech stack:

```bash
# Check for package managers and configs
ls -la package.json requirements.txt go.mod Cargo.toml pom.xml build.gradle composer.json Gemfile

# Check for framework-specific files
ls -la next.config.* nuxt.config.* angular.json svelte.config.* astro.config.*
```

### Step 2: Parse Dependencies

Extract framework and library information:

**Node.js/JavaScript Projects:**

```bash
# Parse package.json for key dependencies
cat package.json | jq '.dependencies + .devDependencies | keys[]' | grep -E "react|next|vue|angular|svelte"
```

**Python Projects:**

```bash
# Parse requirements.txt or pyproject.toml
cat requirements.txt | grep -E "fastapi|django|flask|pytorch|tensorflow"
```

**Go Projects:**

```bash
# Parse go.mod
cat go.mod | grep -E "gin|echo|fiber|chi"
```

### Step 3: Load Rule Index

Load the rule index to discover all available rules dynamically:

- @.claude/context/rule-index.json

The index contains metadata for all 1,081+ rules with technology mappings.

**Version Compatibility Check** (CRITICAL):

Before using the rule index, verify version compatibility:

```javascript
// Load and validate index version
const ruleIndex = JSON.parse(await fs.readFile('.claude/context/rule-index.json', 'utf-8'));
const indexVersion = ruleIndex.version || '0.0.0';
const minRequired = '1.0.0'; // From skill frontmatter

if (!isVersionCompatible(indexVersion, minRequired)) {
  console.warn(`
⚠️  RULE INDEX VERSION MISMATCH
   Current index version: ${indexVersion}
   Required version: ${minRequired}+

   The rule index may be outdated. Please regenerate it:

   Command: pnpm index-rules
   Or:      node scripts/generate-rule-index.mjs

   This ensures all rules are discoverable by the skill.
  `);

  // Offer to regenerate automatically
  const shouldRegenerate = await promptUser('Regenerate rule index now? (y/n)');
  if (shouldRegenerate) {
    await execAsync('pnpm index-rules');
    // Reload index after regeneration
    ruleIndex = JSON.parse(await fs.readFile('.claude/context/rule-index.json', 'utf-8'));
  }
}

// Helper function for semantic version comparison
function isVersionCompatible(current, required) {
  const [cMajor, cMinor, cPatch] = current.split('.').map(Number);
  const [rMajor, rMinor, rPatch] = required.split('.').map(Number);

  // Major version must match (breaking changes)
  if (cMajor !== rMajor) return false;

  // Minor version must be >= required (new features are backward compatible)
  if (cMinor < rMinor) return false;

  // Patch version doesn't matter for compatibility
  return true;
}
```

**When to Increment Index Version**:

Update the version in `scripts/generate-rule-index.mjs` when:

| Change Type       | Version Bump            | Example                                                         |
| ----------------- | ----------------------- | --------------------------------------------------------------- |
| **Major (X.0.0)** | Breaking schema changes | Renamed `technology_map` to `tech_index`, removed `rules` array |
| **Minor (1.X.0)** | New rules added         | Added 50 new rules, new technology categories                   |
| **Minor (1.X.0)** | Rule paths changed      | Moved rules from `.claude/archive/` to `.claude/rules-library/` |
| **Minor (1.X.0)** | New metadata fields     | Added `templates` or `validation_blocks` to rule metadata       |
| **Patch (1.0.X)** | Bug fixes only          | Fixed technology detection, corrected metadata parsing          |
| **Patch (1.0.X)** | Re-indexing             | Re-ran index generation without content changes                 |

**Version History**:

- **1.1.0**: Added versioning metadata, schema_version, and increment guide
- **1.0.0**: Initial release with master rules and library rules support

**Fallback Strategy (CRITICAL for drop-in reliability):**

If `.claude/context/rule-index.json` is missing or cannot be loaded:

1. **Attempt to load pre-built index** (should exist in repo):
   - Check if file exists at `.claude/context/rule-index.json`
   - If exists, load it (pre-built index includes common stacks)

2. **If pre-built index missing, fall back to direct directory scan**:
   - Scan `.claude/rules-master/` directory directly
   - Scan `.claude/rules-library/` (formerly archive) directory directly
   - Build temporary index in memory from discovered rules
   - Continue with rule selection using temporary index
   - Log fallback in reasoning: "Used directory scan fallback - rule-index.json not found"

3. **Never fail** - Always provide rule recommendations even if index is missing

**Empty Directory Handling:**

If no configuration files are detected (package.json, requirements.txt, go.mod, etc.):

1. **Detect empty state**:
   - Check for common config files: `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle`, `composer.json`, `Gemfile`
   - Check for framework configs: `next.config.*`, `nuxt.config.*`, `angular.json`, `svelte.config.*`, `astro.config.*`
   - If none found: Empty directory detected

2. **Prompt user with Quick Pick list for common stacks**:

   ```
   "No configuration files detected. Please select your intended stack:

   **Quick Pick (Common Stacks):**
   1. Next.js - Full-stack React framework with App Router
   2. Python API - FastAPI/Django REST API service
   3. Go Service - Go microservice or API
   4. React SPA - React single-page application
   5. TypeScript App - TypeScript application
   6. Vue.js App - Vue.js application
   7. Other - Describe your stack using keywords

   Or describe your stack using one of these keywords:

   **Supported Stack Keywords:**
   - `nextjs-app` - Next.js application
   - `react-spa` - React single-page application
   - `fastapi-backend` - FastAPI backend service
   - `django-backend` - Django backend service
   - `go-microservice` - Go microservice
   - `python-api` - Python API service
   - `typescript-app` - TypeScript application
   - `vue-app` - Vue.js application
   - `angular-app` - Angular application
   - `nodejs-api` - Node.js API service
   - `mobile-react-native` - React Native mobile app
   - `mobile-flutter` - Flutter mobile app

   **Or describe your stack in natural language:**
   - Example: 'React with Python backend'
   - Example: 'Next.js TypeScript with PostgreSQL'
   - Example: 'Go microservices'
   - Example: 'Python FastAPI with MongoDB'
   "
   ```

3. **Parse user description**:
   - Extract technologies from user input
   - Map to rule categories using technology keywords
   - Generate profile based on parsed technologies
   - **If user uses a Stack Keyword**: Map directly to corresponding rules (e.g., `nextjs-app` → Next.js + TypeScript + React rules)

4. **Generate manifest.yaml**:
   - Use parsed technologies to select rules
   - Create stack profile with selected rules
   - Document that profile was generated from user description

## Supported Stack Keywords

When prompting users in empty directory scenarios, suggest these keywords for better rule mapping:

| Keyword               | Description                   | Maps To Rules                        |
| --------------------- | ----------------------------- | ------------------------------------ |
| `nextjs-app`          | Next.js application           | Next.js, React, TypeScript, Tailwind |
| `react-spa`           | React single-page application | React, TypeScript, JavaScript        |
| `fastapi-backend`     | FastAPI backend service       | FastAPI, Python, Pydantic            |
| `django-backend`      | Django backend service        | Django, Python                       |
| `go-microservice`     | Go microservice               | Go, Golang                           |
| `python-api`          | Python API service            | Python, FastAPI/Django               |
| `typescript-app`      | TypeScript application        | TypeScript, JavaScript               |
| `vue-app`             | Vue.js application            | Vue, TypeScript, JavaScript          |
| `angular-app`         | Angular application           | Angular, TypeScript                  |
| `nodejs-api`          | Node.js API service           | Node.js, Express, TypeScript         |
| `mobile-react-native` | React Native mobile app       | React Native, TypeScript             |
| `mobile-flutter`      | Flutter mobile app            | Flutter, Dart                        |

**Usage**: When user provides a keyword, map directly to corresponding technology rules. For natural language descriptions, extract technologies and map to rules.

### Step 4: Map Technologies to Rules

For each detected technology, query the index's `technology_map`:

```javascript
// Pseudocode
const detectedTech = ['nextjs', 'react', 'typescript', 'tailwind'];
const recommendedRules = [];

detectedTech.forEach(tech => {
  const rules = index.technology_map[tech] || [];
  recommendedRules.push(...rules);
});

// Prioritize master rules over library rules
const masterRules = recommendedRules.filter(r => r.type === 'master');
const libraryRules = recommendedRules.filter(r => r.type === 'library');
```

**Technology Mapping**:

- Detected technologies from Step 2 → Query `index.technology_map[tech]`
- Get all rules for each technology
- Prioritize master rules (from `.claude/rules-master/`)
- Supplement with library rules (from `.claude/rules-library/`, formerly archive)

### Step 5: Generate Stack Profile

Create a custom profile in manifest.yaml using rules from the index:

```yaml
# Generated stack profile for: my-nextjs-app
# Rules discovered from rule index
stack_profiles:
  my-nextjs-app:
    # Auto-detected: Next.js 14 + TypeScript + Tailwind + Prisma
    include:
      # Master rules (from index, type: "master")
      - '.claude/rules-master/TECH_STACK_NEXTJS.md'
      - '.claude/rules-master/PROTOCOL_ENGINEERING.md'

      # Library rules (from index, type: "library", formerly archive)
      # Selected based on technology_map queries
      - '.claude/rules-library/nextjs.mdc'
      - '.claude/rules-library/typescript.mdc'
      - '.claude/rules-library/react.mdc'
      - '.claude/rules-library/tailwind.mdc'
      - '.claude/rules-library/vitest-unit-testing-cursorrules-prompt-file/**/*.mdc'

    exclude:
      # Exclude rules for technologies NOT detected
      # Query index.technology_map for all technologies
      # Exclude rules not matching detected stack
      - '.claude/rules-library/angular-*/**'
      - '.claude/rules-library/vue-*/**'
      - '.claude/rules-library/python-*/**'
      - '.claude/rules-library/go-*/**'
      - '.claude/rules-library/swift-*/**'
      - '.claude/rules-library/android-*/**'

    # Priority order (master rules first)
    priority:
      - TECH_STACK_NEXTJS # Master rule (highest priority)
      - PROTOCOL_ENGINEERING # Master rule (universal)
      - nextjs # Library rule (framework-specific)
      - typescript # Library rule (language)

    metadata:
      generated: '2025-11-29'
      generated_by: 'rule-selector (index-based)'
      detected_stack:
        - 'next@14.0.0'
        - 'react@18.2.0'
        - 'typescript@5.3.0'
        - 'tailwindcss@3.4.0'
        - '@prisma/client@5.7.0'
      rules_source: 'rule-index.json'
      total_rules_available: 1081
      rules_selected: 7
```

## Detection Patterns

### Frontend Detection

```yaml
# React Ecosystem
react_detection:
  signals:
    - package.json: "react", "react-dom"
  variants:
    next: "next" in dependencies
    gatsby: "gatsby" in dependencies
    remix: "@remix-run" in dependencies
    vite_react: "vite" + "@vitejs/plugin-react"
  rules:
    base: ["react.mdc"]
    next: ["nextjs.mdc", "nextjs-app-router-*"]
    gatsby: ["gatsby-*"]

# Vue Ecosystem
vue_detection:
  signals:
    - package.json: "vue"
  variants:
    nuxt: "nuxt" in dependencies
    vue3: version >= 3.0
  rules:
    base: ["vue.mdc"]
    nuxt: ["vue3-nuxt-3-*"]
    vue3: ["vue3-composition-api-*"]

# Angular Ecosystem
angular_detection:
  signals:
    - package.json: "@angular/core"
    - angular.json exists
  rules: ["angular-typescript-*"]

# Svelte Ecosystem
svelte_detection:
  signals:
    - package.json: "svelte"
  variants:
    sveltekit: "@sveltejs/kit" in dependencies
  rules:
    base: ["svelte.mdc"]
    sveltekit: ["sveltekit-*"]
```

### Backend Detection

```yaml
# Python Ecosystem
python_detection:
  signals:
    - requirements.txt exists
    - pyproject.toml exists
    - "*.py" files present
  variants:
    fastapi: "fastapi" in requirements
    django: "django" in requirements
    flask: "flask" in requirements
    ml: "pytorch" or "tensorflow" in requirements
  rules:
    base: ["python.mdc"]
    fastapi: ["fastapi.mdc", "python-fastapi-*"]
    django: ["python-django-*"]
    ml: ["python-llm-ml-workflow-*"]

# Node.js Backend
node_backend_detection:
  signals:
    - package.json: "express" or "fastify" or "nestjs"
  rules: ["node-express.mdc", "javascript-*"]

# Go Backend
go_detection:
  signals:
    - go.mod exists
    - "*.go" files present
  rules: ["go-*", "backend-scalability-*"]
```

### Testing Detection

```yaml
testing_detection:
  e2e:
    cypress: ['cypress-e2e-testing-*', 'cypress-api-testing-*']
    playwright: ['playwright-e2e-testing-*', 'playwright-api-testing-*']
  unit:
    jest: ['jest-unit-testing-*']
    vitest: ['vitest-unit-testing-*']
    pytest: ['python-*'] # Python testing included in python rules
  bdd:
    cucumber: ['gherkin-*']
```

## Output Formats

### Format 1: Manifest Update (default)

Generates updated `.claude/rules/manifest.yaml`:

```yaml
# AUTO-GENERATED by rule-selector skill
# Project: my-nextjs-app
# Generated: 2025-11-29T10:00:00Z

stack_profiles:
  # ... generated profile ...

loading_policy:
  max_rules_files: 5 # Increased for comprehensive stack
  selection: 'most_relevant'
  auto_detect: true
```

### Format 2: Recommendation Report

```markdown
## Rule Selection Report

**Project**: /path/to/my-nextjs-app
**Scan Date**: 2025-11-29

### Detected Stack

| Category  | Technology   | Version | Confidence |
| --------- | ------------ | ------- | ---------- |
| Framework | Next.js      | 14.0.0  | High       |
| Language  | TypeScript   | 5.3.0   | High       |
| Styling   | Tailwind CSS | 3.4.0   | High       |
| Database  | Prisma       | 5.7.0   | High       |
| Testing   | Vitest       | 1.0.0   | High       |

### Recommended Rules

**Primary Rules** (always load):

1. `nextjs.mdc` - Next.js App Router best practices
2. `typescript.mdc` - TypeScript coding standards
3. `react.mdc` - React component patterns

**Secondary Rules** (load when relevant): 4. `tailwind.mdc` - Tailwind CSS conventions 5. `clean-code.mdc` - Universal code quality

**Testing Rules** (load during test tasks): 6. `vitest-unit-testing-*` - Unit testing patterns

### Rules NOT Recommended

These rules are excluded as irrelevant to your stack:

- `angular-*` (No Angular detected)
- `vue-*` (No Vue detected)
- `python-*` (No Python detected)
- `cypress-*` (Playwright detected instead)

### Optimization Suggestions

1. **Context Budget**: Your stack needs ~5 rule files. Current limit is 3.
   → Recommend increasing `max_rules_files` to 5

2. **Missing Coverage**: No accessibility rules detected.
   → Consider adding `accessibility-guidelines.mdc`

3. **Duplicate Coverage**: Both `nextjs.mdc` and `react.mdc` cover components.
   → `nextjs.mdc` takes priority for Next.js projects
```

### Format 3: JSON (for automation)

```json
{
  "project_path": "/path/to/my-nextjs-app",
  "scan_timestamp": "2025-11-29T10:00:00Z",
  "detected_stack": {
    "framework": { "name": "nextjs", "version": "14.0.0", "confidence": 0.95 },
    "language": { "name": "typescript", "version": "5.3.0", "confidence": 1.0 },
    "styling": { "name": "tailwindcss", "version": "3.4.0", "confidence": 0.9 },
    "testing": { "name": "vitest", "version": "1.0.0", "confidence": 0.85 }
  },
  "recommended_rules": {
    "primary": ["nextjs.mdc", "typescript.mdc", "react.mdc"],
    "secondary": ["tailwind.mdc", "clean-code.mdc"],
    "testing": ["vitest-unit-testing-cursorrules-prompt-file"]
  },
  "excluded_rules": ["angular-*", "vue-*", "python-*"],
  "manifest_updates": {
    "stack_profile_name": "my-nextjs-app",
    "include_patterns": ["..."],
    "exclude_patterns": ["..."]
  }
}
```

## Quick Commands

```
# Auto-detect and show recommendations
/select-rules

# Auto-detect and update manifest.yaml
/select-rules --apply

# Detect for specific directory
/select-rules --path ./packages/web

# Generate JSON output
/select-rules --format json

# Show what rules would be excluded
/select-rules --show-excluded

# Force re-detection (ignore cached)
/select-rules --fresh
```

## Integration with Project Setup

### New Project Workflow

```
1. User creates new project
2. Run: /select-rules --apply
3. Skill detects stack from package.json
4. Generates optimized manifest.yaml
5. Rules auto-load on next Claude session
```

### Monorepo Support

For monorepos with multiple packages:

```yaml
stack_profiles:
  monorepo_web:
    root: 'packages/web'
    include: ['nextjs-*', 'react-*']

  monorepo_api:
    root: 'packages/api'
    include: ['fastapi-*', 'python-*']

  monorepo_shared:
    root: 'packages/shared'
    include: ['typescript.mdc', 'clean-code.mdc']
```

## Version Checking

### Overview

The rule-selector skill relies on the rule index (`.claude/context/rule-index.json`) for dynamic rule discovery. To ensure compatibility, the skill validates the index version before use.

### Version Compatibility Rules

**Semantic Versioning** (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes to index structure (must match exactly)
- **MINOR**: New features/rules added (backward compatible, skill requires minimum)
- **PATCH**: Bug fixes and re-indexing (always compatible)

**Compatibility Check**:

```javascript
// Skill requires: 1.2.0
// Index version: 1.3.0 ✅ Compatible (same major, higher minor)
// Index version: 1.1.0 ❌ Incompatible (lower minor version)
// Index version: 2.0.0 ❌ Incompatible (different major version)
```

### Automatic Version Validation

When the skill loads the rule index, it automatically:

1. **Checks version compatibility** against `min_required_version` in frontmatter
2. **Warns if outdated** with clear instructions to regenerate
3. **Offers auto-regeneration** (if running in interactive mode)
4. **Falls back gracefully** to directory scanning if index is severely outdated

### Warning Message Format

When version mismatch is detected:

```
⚠️  RULE INDEX VERSION MISMATCH
   Current index version: 1.0.0
   Required version: 1.2.0+

   The rule index may be outdated. Please regenerate it:

   Command: pnpm index-rules
   Or:      node scripts/generate-rule-index.mjs

   This ensures all rules are discoverable by the skill.
```

### Regeneration Commands

**Standard Regeneration** (updates index with all current rules):

```bash
pnpm index-rules
```

**Manual Regeneration** (if pnpm not available):

```bash
node scripts/generate-rule-index.mjs
```

**Prebuilt Index** (lightweight, common stacks only):

```bash
pnpm index-rules:prebuilt
```

### When to Regenerate

Regenerate the rule index when:

| Scenario                     | Reason                                | Command            |
| ---------------------------- | ------------------------------------- | ------------------ |
| **Added new rules**          | New rules won't be discoverable       | `pnpm index-rules` |
| **Moved rule files**         | Paths in index are stale              | `pnpm index-rules` |
| **Updated rule metadata**    | Descriptions/technologies changed     | `pnpm index-rules` |
| **Version mismatch warning** | Skill requires newer index            | `pnpm index-rules` |
| **After git pull**           | Other developers may have added rules | `pnpm index-rules` |
| **Index file deleted**       | Need to recreate from scratch         | `pnpm index-rules` |

### Version Increment Guide for Maintainers

When updating `scripts/generate-rule-index.mjs`, increment version as follows:

**Major Version (X.0.0)** - Breaking Changes:

```javascript
// Example: Renamed field
const index = {
  version: '2.0.0', // Breaking: renamed 'technology_map' to 'tech_index'
  tech_index: techMap, // <- Renamed from 'technology_map'
  rules: allRules,
};
```

**Minor Version (1.X.0)** - New Features (Backward Compatible):

```javascript
// Example: New metadata field
const index = {
  version: '1.2.0', // Minor: added 'templates' metadata
  rules: allRules.map(rule => ({
    ...rule,
    templates: extractTemplates(rule.path), // <- New field
  })),
  technology_map: techMap,
};
```

**Patch Version (1.0.X)** - Bug Fixes:

```javascript
// Example: Fixed technology detection bug
function extractTechnologies(filePath, content) {
  // Fixed: Now correctly detects 'nextjs' from 'next.js'
  const normalized = tech === 'next.js' ? 'nextjs' : tech;
  return normalized;
}
// Version: 1.0.1 (patch bump for bug fix)
```

### Self-Healing Index

If a requested rule is not found in the index, the skill will:

1. **Log the missing rule** with file path
2. **Suggest regeneration** via `pnpm index-rules`
3. **Offer auto-regeneration** (if running interactively)
4. **Fall back to directory scan** (if index regeneration fails)

This ensures the skill remains functional even with stale or missing indexes.

### Testing Version Compatibility

**Test Scenario 1: Current Index**

```bash
# Check current index version
cat .claude/context/rule-index.json | jq '.version'
# Output: "1.1.0"

# Check skill requirements
cat .claude/skills/rule-selector/SKILL.md | grep min_required_version
# Output: min_required_version: 1.0.0

# Result: ✅ Compatible (1.1.0 >= 1.0.0)
```

**Test Scenario 2: Outdated Index**

```bash
# Simulate outdated index (edit version to 0.9.0)
# Run skill - should show warning and offer regeneration
```

## Best Practices

1. **Run on Setup**: Always run rule-selector when starting a new project
2. **Update Periodically**: Re-run after major dependency changes
3. **Review Exclusions**: Check excluded rules to ensure nothing important is missed
4. **Customize Priorities**: Adjust rule priority based on team preferences
5. **Document Decisions**: Keep notes on why certain rules were included/excluded
6. **Keep Index Fresh**: Regenerate index after adding/moving rules (`pnpm index-rules`)
7. **Check Version Compatibility**: Validate index version matches skill requirements
