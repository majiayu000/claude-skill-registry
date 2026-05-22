---
name: document-project
description: Generate comprehensive architecture documentation automatically from existing codebase analysis. This skill should be used when working with brownfield projects or updating outdated documentation.
acceptance:
  - documentation_generated: "All three documentation files created (architecture.md, standards.md, patterns.md)"
  - confidence_sufficient: "Overall confidence score ≥70% across all analyzed sections"
  - review_checklist_created: "Human review checklist generated identifying low-confidence areas"
  - configuration_updated: "Project configuration updated with documentation paths and brownfield flag"
inputs:
  codebase_path:
    type: string
    required: true
    description: "Path to codebase to analyze (e.g., src/)"
  existing_docs_mode:
    type: enum
    values: ["merge", "replace", "supplement"]
    default: "merge"
    description: "How to handle existing documentation"
  include_tests:
    type: boolean
    default: true
    description: "Include test file analysis in documentation"
  max_files:
    type: number
    default: 1000
    description: "Maximum files to analyze (safety limit)"
outputs:
  documentation_files:
    type: object
    description: "Paths to generated documentation files"
  confidence_score:
    type: number
    description: "Overall confidence score (0-100%)"
  review_checklist:
    type: string
    description: "Path to human review checklist file"
  analysis_summary:
    type: object
    description: "Summary of analysis (files analyzed, patterns found, etc.)"
telemetry:
  emit: "skill.document-project.completed"
  track:
    - project_name
    - codebase_path
    - duration_ms
    - files_analyzed
    - lines_analyzed
    - confidence_score
    - patterns_identified
---

# Brownfield Project Documentation Generator

Generate comprehensive architecture documentation automatically by analyzing existing codebase structure, patterns, and conventions.

## Purpose

Analyze an existing codebase and generate three comprehensive documentation files:
1. **architecture.md** - Project structure, tech stack, data models, API specifications
2. **standards.md** - Coding standards, best practices, discovered conventions
3. **patterns.md** - Design patterns, architectural patterns, common conventions

This enables BMAD Enhanced to work with brownfield projects by reverse-engineering architecture from code.

## When to Use This Skill

This skill should be used when:
- Starting BMAD Enhanced with existing project (brownfield onboarding)
- Architecture documentation is outdated or missing
- Need to discover implicit patterns and conventions
- Onboarding to unfamiliar codebase

This skill should NOT be used when:
- Greenfield projects (write docs from scratch instead)
- Project already has current, comprehensive documentation
- Codebase >500K lines (too complex for automated analysis)
- Project has no clear structure

## Project Type Support

**Well-Supported Languages:**
- ✅ Node.js/TypeScript (excellent support)
- ✅ Python (good support)
- ✅ Go (good support)
- ✅ Java/Kotlin (good support)
- ✅ Rust (good support)

**Basic Support:**
- ⚠️ PHP, Ruby, C#/.NET (basic support)

**Optimal Codebase Size:** 10K-100K lines
- Smaller: May lack sufficient patterns to analyze
- Larger: Analysis may be too slow or complex

## Sequential Documentation Generation

Execute steps in order - each builds on previous analysis:

### Step 0: Configuration and Validation

**Purpose:** Verify project is suitable for automated documentation.

**Actions:**

1. **Load config** from `.claude/config.yaml` (codebasePath, existingDocs, includeTests, maxFiles)
2. **Validate structure:** Check path exists, identify languages, count files/lines, verify size (10K-100K recommended)
3. **Check existing docs:** Ask how to handle (merge/replace/supplement)
4. **Get confirmation:** Show summary (path, language, file count, lines, estimated time), ask to proceed

**See:** `references/templates.md#step-0-configuration-and-validation-output` for complete formats

**Halt if:**
- Codebase path not found
- No recognizable project structure
- Codebase too large (>500K lines)
- Unsupported language
- User declines to proceed

**Output:** Validation confirmation (project type, lines, existing docs mode, scope, ready status)

**Reference:** See [validation-criteria.md](references/validation-criteria.md) for detailed validation rules.

---

### Step 1: Analyze Project Structure

**Purpose:** Map file organization and module structure.

**Actions:**

1. **Scan directory structure:** Identify main dirs, detect patterns (feature vs type), note nesting
2. **Analyze file organization:** Files per dir, naming conventions, size distribution, co-location patterns
3. **Detect project type:** Backend API / Frontend App / Full-Stack / Library / Monorepo (based on directory structure)
4. **Map relationships:** Analyze imports, build dependency graph, identify core modules, detect circular dependencies

**Output:** Project structure analysis with type, organization, directory structure (dirs + file counts + line counts), key patterns

**See:** `references/templates.md#step-1-codebase-analysis-output` for complete format

**Reference:** See [analysis-techniques.md](references/analysis-techniques.md) for detailed analysis methods.

---

### Step 2: Analyze Technology Stack

**Purpose:** Identify languages, frameworks, and dependencies.

**Actions:**

1. Read package configuration:
   - **Node.js:** package.json
   - **Python:** requirements.txt, pyproject.toml
   - **Go:** go.mod
   - **Java:** pom.xml, build.gradle
   - **Rust:** Cargo.toml

2. Extract dependencies and identify frameworks:
   - Backend: Express, Django, Spring Boot, etc.
   - Frontend: React, Vue, Angular, etc.
   - Database: Prisma, TypeORM, SQLAlchemy, etc.
   - Testing: Jest, Pytest, JUnit, etc.

3. Detect runtime/platform:
   - Node.js/Python/JDK version
   - Database type (PostgreSQL, MySQL, MongoDB)

**Output:** Tech stack summary (runtime, backend/frontend frameworks, key libraries, testing tools, versions, confidence score)

**See:** `references/templates.md#step-2-technology-stack-analysis` for complete format

---

### Step 3: Extract Data Models and Schemas

**Purpose:** Document data structures and validation rules.

**Actions:**

1. Locate data model files:
   - Prisma schema: `prisma/schema.prisma`
   - TypeScript interfaces: `src/types/*.ts`, `src/models/*.ts`
   - Database migrations: `prisma/migrations/`, `migrations/`
   - Validation schemas: Zod, Yup, Joi schemas

2. Parse data models and extract validation rules

3. Analyze relationships:
   - One-to-many, many-to-many
   - Foreign keys and constraints

4. Detect data flow:
   - Request → Validation → Service → Repository → Database
   - Response transformation (DTOs)

**Output:** Data models summary (models with fields/types/constraints, validation rules, relationships, confidence score)

**See:** `references/templates.md#complete-architecture-md-template` for data model format

**Reference:** See [analysis-techniques.md](references/analysis-techniques.md) for model extraction patterns.

---

### Step 4: Analyze API Patterns

**Purpose:** Document API structure and conventions.

**Actions:**

1. Locate API definitions:
   - Express routes: `src/routes/**/*.ts`
   - Controllers: `src/controllers/**/*.ts`
   - OpenAPI/Swagger spec (if exists)
   - GraphQL schemas (if exists)

2. Extract endpoints and analyze request/response patterns:
   - Request validation (middleware)
   - Error response format
   - Success response format
   - Status codes used

3. Identify authentication:
   - JWT tokens, session-based, API keys, OAuth

4. Detect rate limiting and other middleware

**Output:** API specs summary (base URL, authentication type/headers/expiry, error/success response formats, confidence score)

**See:** `references/templates.md#complete-architecture-md-template` for API specification format

---

### Step 5: Extract Coding Standards and Patterns

**Purpose:** Document implicit conventions and best practices.

**Actions:**

1. Analyze code style:
   - Read `.eslintrc`, `.prettierrc`, `tsconfig.json`
   - Detect: indentation, quotes, semicolons
   - Naming conventions: variables, functions, classes, files

2. Identify architectural patterns:
   - Design patterns: Repository, Factory, Strategy
   - Architectural style: Layered, Clean, Hexagonal

3. Extract error handling patterns:
   - Error classes
   - Centralized error handling
   - Logging patterns

4. Detect testing patterns:
   - Test organization
   - Mocking strategy
   - Test data management

**Output:**
```
Coding Standards:

Code Style:
- Indentation: 2 spaces
- Quotes: Single quotes
- Naming: camelCase (variables), PascalCase (classes), kebab-case (files)

Architectural Patterns:
1. Layered Architecture
   - Routes (presentation layer)
   - Services (business logic layer)
   - Repositories (data access layer)

2. Dependency Injection
3. Repository Pattern

Error Handling:
- Custom error classes (AppError, ValidationError)
- Centralized error handling middleware
- Never expose stack traces to clients

Confidence: High (90%)
```

**Reference:** See [pattern-detection.md](references/pattern-detection.md) for pattern identification techniques.

---

### Step 6: Generate Architecture Documentation

**Purpose:** Create comprehensive architecture.md from findings.

**Actions:**

1. Load architecture template structure

2. Populate sections with analyzed data from Steps 1-5:
   - Overview, tech stack, project structure
   - Data models, API specifications
   - Include confidence scores where applicable
   - Add source file references

3. Generate diagrams (optional):
   - Mermaid diagrams for architecture layers
   - Data model ERD
   - API endpoint map

4. Add human review notes for medium/low confidence sections

5. Write documentation file:
   - Create `docs/architecture.md`
   - Or merge with existing docs if "merge" mode selected

**Output:**
```
✓ Architecture documentation generated
✓ File: docs/architecture.md (2,450 lines)
✓ Sections: 12
✓ Overall confidence: 85%
✓ Human review items: 5
```

**Reference:** See [documentation-templates.md](references/documentation-templates.md) for template structures.

---

### Step 7: Generate Standards Documentation

**Purpose:** Create standards.md from discovered patterns.

**Actions:**

1. Extract standards from code analysis:
   - Security standards (from security practices)
   - Testing standards (from test patterns)
   - Code quality standards (from ESLint rules)
   - Performance standards (from observed patterns)

2. Document best practices:
   - Observed consistently across codebase
   - Mark as "discovered" vs "recommended"

3. Create standards document with examples and consistency scores

**Output:**
```
✓ Standards documentation generated
✓ File: docs/standards.md (850 lines)
✓ Standards extracted: 18
✓ Consistency scores: 75-100%
```

---

### Step 8: Generate Patterns Documentation

**Purpose:** Document discovered design patterns and conventions.

**Actions:**

1. Extract design patterns:
   - Repository, Factory, Strategy, Middleware patterns

2. Document usage examples:
   - Show code examples of each pattern
   - Explain when to use
   - Link to existing implementations

3. Identify anti-patterns:
   - Code smells detected
   - Inconsistencies
   - Technical debt

4. Create patterns document

**Output:**
```
✓ Patterns documentation generated
✓ File: docs/patterns.md (620 lines)
✓ Patterns identified: 8
✓ Anti-patterns noted: 3
```

**Reference:** See [pattern-detection.md](references/pattern-detection.md) for pattern documentation templates.

---

### Step 9: Validation and Confidence Scoring

**Purpose:** Score accuracy and identify areas needing human review.

**Actions:**

1. **Calculate confidence:** Score each section (tech stack, structure, data models, API, standards) and compute overall
2. **Identify low-confidence areas:** Find sections <70%, conflicting patterns, missing info
3. **Generate review checklist:** List high/medium priority items needing human verification
4. **Create validation report**

**Output:** Validation summary (overall confidence %, high/medium priority review item counts)

**See:** `references/templates.md#review-checklist-template` and `references/confidence-scoring.md` for formats

**Reference:** See [confidence-scoring.md](references/confidence-scoring.md) for scoring guidelines.

---

### Step 10: Summary and Next Steps

**Purpose:** Provide user with clear summary and action items.

**Actions:**

1. **Generate summary report:** Project name, duration, files analyzed, confidence, generated docs (paths + line counts), key findings (type, arch, tech stack, test coverage), next steps
2. **Create review checklist file:** `docs/REVIEW_CHECKLIST.md`
3. **Update config:** Set brownfield flag, doc paths, documented=true
4. **Prompt next action:** Review items, create task spec, run index-docs, or exit

**Output:** Summary confirmation (report generated, checklist created, config updated, ready status)

**See:** `references/templates.md` for complete summary formats

---

## Confidence Scoring Guidelines

**High (85-100%):** Explicit in code/config, consistent patterns, no conflicts | **Medium (70-84%):** Inferred from patterns, some inconsistencies, needs validation | **Low (<70%):** Missing/unclear info, conflicts, high uncertainty, MUST review

**See:** `references/confidence-scoring.md` for detailed scoring methodology

---

## Limitations

**Cannot:** Understand business logic without context, document deployment infrastructure, capture tribal knowledge, understand legacy decisions, document external integrations perfectly

**Requires:** Readable structured codebase, standard organization, supported language/framework, 10K-100K lines (optimal)

## Best Practices

Run periodically (every 3-6 months) | Always review low-confidence sections | Supplement with manual docs (business context, deployment) | Use as starting point, enhance with team input

## Integration with Planning Workflow

**Brownfield:** document-project → index-docs → create-task-spec (use generated docs) | **Greenfield:** Write docs manually first | **Brownfield:** Generate from code, then refine

## References

Detailed documentation in `references/`:

- **templates.md**: All output formats, complete architecture/standards/patterns templates, analysis summaries, review checklists, error templates
- **analysis-techniques.md**: Analysis methods for structure, tech stack, models, APIs, patterns
- **pattern-detection.md**: Pattern identification and documentation techniques
- **documentation-templates.md**: Templates for architecture, standards, patterns docs
- **confidence-scoring.md**: Confidence calculation methodology and validation criteria
- **validation-criteria.md**: Project validation rules and sizing guidelines
