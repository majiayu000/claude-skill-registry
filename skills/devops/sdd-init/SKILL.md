---
name: sdd-init
description: "Initialize Spec-Driven Development context — detects tech stack, conventions, architecture patterns, and bootstraps persistence backends. Triggers on 'sdd-init', 'init sdd', 'setup sdd', 'initialize sdd', 'setup project', 'initialize project context'. Creates/updates docs/specs/architecture.md & ontology.md (Constitution), and populates knowledge-graph.json."
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, AskUserQuestion
---

# SDD Init Skill

Initialize Spec-Driven Development (SDD) in the current project. Detects tech stack, conventions, architecture patterns, and bootstraps all persistence backends (Constitution + Knowledge Graph).

## When to Use

**Trigger phrases:**
- "sdd-init", "init sdd", "setup sdd"
- "initialize sdd", "setup project", "initialize project context"
- "bootstrap sdd", "start sdd"
- "detect project stack", "detect tech stack"

## Workflow

```
1. Detect Project Context
   ├── Scan tech stack (languages, frameworks, tools)
   ├── Identify conventions (folder structure, patterns, configs)
   └── Detect architecture (monolith, microservices, serverless)

2. Bootstrap Constitution
   ├── Check if docs/specs/architecture.md exists
   ├── If missing → ask user to create with constitution skill
   └── If exists → show current state

3. Bootstrap Knowledge Graph
   ├── Check if docs/specs/knowledge-graph.json exists
   ├── Create with initial discoveries (stack, patterns, conventions)
   └── Link to Constitution

4. Return Structured Result
   └── status, executive_summary, artifacts, next_recommended
```

## Phase 1: Detect Project Context

### 1.1 Scan Tech Stack

Detect the primary language and framework:

```bash
# Detect language (priority order)
ls *.go *.rs *.ts *.js *.py *.java *.cs *.rb *.php *.cpp *.c 2>/dev/null | head -1

# Detect framework/type
ls package.json pyproject.toml Cargo.toml go.mod pom.xml *.csproj Gemfile composer.json 2>/dev/null

# Detect project type
ls -la src/ lib/ app/ cmd/ internal/ pkg/ services/ 2>/dev/null
```

### 1.2 Identify Conventions

Scan for existing patterns:

```bash
# Folder structure
find . -maxdepth 2 -type d -name "src" -o -name "lib" -o -name "app" -o -name "cmd" | head -10

# Config files
ls -la *.yaml *.yml *.toml *.json *.env* Makefile 2>/dev/null

# Testing patterns
find . -name "*_test.*" -o -name "test_*.py" -o -name "*_test.go" -o -name "*.spec.ts" 2>/dev/null | head -10

# Build system
ls Makefile Dockerfile docker-compose*.yml *.mk 2>/dev/null

# CI/CD
ls .github/workflows/ .gitlab-ci.yml .circleci/ 2>/dev/null
```

### 1.3 Detect Architecture Style

Analyze project structure for architectural patterns:

```bash
# Microservices vs Monolith
ls services/ microservices/ cmd/ api/ internal/ 2>/dev/null

# Serverless
ls functions/ lambda/ handlers/ 2>/dev/null

# Layered architecture
ls controllers/ services/ repositories/ models/ 2>/dev/null

# Hexagonal/Ports & Adapters
ls ports/ adapters/ domain/ infrastructure/ 2>/dev/null
```

## Phase 2: Bootstrap Constitution

### 2.1 Check Existence

```bash
# Check if Constitution files exist
[ -f docs/specs/architecture.md ] && echo "architecture:exists" || echo "architecture:missing"
[ -f docs/specs/ontology.md ] && echo "ontology:exists" || echo "ontology:missing"
```

### 2.2 If Missing → Ask User

Use `AskUserQuestion` to prompt:

> The Constitution files (architecture.md, ontology.md) don't exist yet.
> 
> **Option 1:** Create both (Recommended) - Sets up architectural DNA and domain language
> **Option 2:** Create architecture.md only
> **Option 3:** Create ontology.md only  
> **Option 4:** Skip for now - I'll detect context but skip Constitution

If user chooses option 1-3, delegate to `/developer-kit-specs:constitution create` with the detected context.

### 2.3 If Exists → Show Current State

Read and display current Constitution files with detected context as comparison.

## Phase 3: Bootstrap Knowledge Graph

### 3.1 Check Existence

```bash
# Check if KG exists
ls docs/specs/knowledge-graph.json 2>/dev/null
```

### 3.2 Create/Update KG

Create or update `docs/specs/knowledge-graph.json` with initial discoveries:

```json
{
  "metadata": {
    "spec_id": "project-init",
    "version": "1.0.0",
    "created": "{{ISO_DATE}}",
    "project": "{{PROJECT_NAME}}",
    "type": "initial-discovery"
  },
  "context": {
    "workingDirectory": "{{PWD}}",
    "projectName": "{{PROJECT_NAME}}"
  },
  "stack": {
    "primaryLanguage": "{{DETECTED_LANGUAGE}}",
    "framework": "{{DETECTED_FRAMEWORK}}",
    "buildSystem": "{{DETECTED_BUILD_SYSTEM}}"
  },
  "conventions": {
    "folderStructure": ["{{FOLDERS}}"],
    "namingPatterns": ["{{PATTERNS}}"],
    "configFiles": ["{{CONFIGS}}"],
    "testingPattern": "{{TESTING_PATTERN}}"
  },
  "architecture": {
    "style": "{{MONOLITH|MICROSERVICE|SERVERLESS|LAYERED|HEXAGONAL}}",
    "layers": ["{{LAYERS}}"],
    "patterns": ["{{ARCHITECTURAL_PATTERNS}}"]
  },
  "references": {
    "constitution": "docs/specs/architecture.md",
    "ontology": "docs/specs/ontology.md"
  },
  "source": "sdd-init"
}
```

### 3.3 Validation

After creating KG, validate it exists and has valid JSON:

```bash
# Validate KG
cat docs/specs/knowledge-graph.json | python3 -m json.tool > /dev/null && echo "KG:valid" || echo "KG:invalid"
```

## Phase 4: Return Structured Result

Return a JSON object with:

```json
{
  "status": "success|partial|skipped",
  "executive_summary": "Brief description of what was detected and initialized",
  "artifacts": [
    {
      "path": "docs/specs/architecture.md",
      "action": "created|existing|skipped",
      "summary": "What this file contains"
    },
    {
      "path": "docs/specs/ontology.md",
      "action": "created|existing|skipped", 
      "summary": "What this file contains"
    },
    {
      "path": "docs/specs/knowledge-graph.json",
      "action": "created|updated",
      "summary": "What was discovered and stored"
    }
  ],
  "next_recommended": [
    "Review Constitution if just created",
    "Run brainstorm to start first spec",
    "Check knowledge-graph.json for detected patterns"
  ]
}
```

## Output Format

Display result in a structured format:

```
══════════════════════════════════════════════════
SDD Init — {{PROJECT_NAME}}
══════════════════════════════════════════════════

STATUS: {{status}}

TECH STACK DETECTED:
  Language: {{language}}
  Framework: {{framework}}
  Build: {{build_system}}

ARCHITECTURE:
  Style: {{architecture_style}}
  Patterns: {{patterns}}

ARTIFACTS:
  ✓ Constitution (architecture.md) — {{status}}
  ✓ Constitution (ontology.md) — {{status}}
  ✓ Knowledge Graph — {{status}}

NEXT STEPS:
  {{next_recommended}}

══════════════════════════════════════════════════
```

## Integration with Other Skills

| Skill | Integration Point |
|-------|-------------------|
| `constitution` | Created/updated by sdd-init if missing |
| `knowledge-graph` | Populated by sdd-init with initial discoveries |
| `brainstorm` | Should read Constitution before starting |
| `spec-to-tasks` | Should validate against KG and Constitution |
| `task-implementation` | Should check KG for existing patterns |

## Constraints and Warnings

- **Read-only detection** — Does NOT modify source code
- **Non-destructive** — Only creates new files, never overwrites existing content
- **Permission check** — Warn if docs/specs/ cannot be created
- **Backup KG** — If updating existing KG, preserve existing data

## Error Handling

| Error | Recovery |
|-------|----------|
| Cannot create docs/specs/ | Ask user to create directory manually |
| KG JSON invalid | Show error, keep raw file, suggest validation |
| Constitution delegate fails | Fall back to inline creation with template |