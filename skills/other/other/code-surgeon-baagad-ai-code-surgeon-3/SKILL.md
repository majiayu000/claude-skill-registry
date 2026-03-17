---
name: code-surgeon-framework-detector
description: Use when analyzing a repository to detect primary framework, language, versions, and monorepo status for code-surgeon planning
---

# code-surgeon Framework Detector

## Overview

**framework-detector** is a sub-skill that scans a repository to identify the technology stack, frameworks, languages, and project structure.

**Core principle:** Quickly and accurately identify what technologies are in use so downstream planning can be framework-aware and language-specific.

---

## When to Use

This skill runs automatically as **Subagent 1B in Phase 1** of code-surgeon orchestration, in **parallel with Issue Analyzer**.

It's dispatched when you invoke:

```bash
/code-surgeon "GitHub issue URL or plain text requirement"
```

The main orchestrator automatically runs framework detection on your repository.

---

## What It Does

### Detection Strategy

Framework detector uses a **3-phase scanning approach**:

```
Phase 1: Language Detection (Fast)
  ├─ Scan directory for file extensions
  ├─ Count files by type (.js, .py, .go, .java, etc)
  ├─ Identify primary language
  └─ Time: <100ms

Phase 2: Framework Identification (Medium)
  ├─ Read package manager files (package.json, pyproject.toml, etc)
  ├─ Parse dependencies to identify frameworks
  ├─ Extract version numbers
  ├─ Detect secondary frameworks
  └─ Time: <200ms

Phase 3: Monorepo & Structure Detection (Variable)
  ├─ Look for workspace configs (lerna.json, turbo.json, etc)
  ├─ Identify monorepo structure if present
  ├─ Map workspace packages
  └─ Time: <200ms for monorepos, <50ms for single repos

Total Time: <500ms per repository
```

---

## File Scanning Order

Framework detector scans in this priority order (early exit when match found):

### JavaScript/TypeScript Ecosystem
```
1. package.json (primary indicator)
   ├─ Check: dependencies, devDependencies, peerDependencies
   ├─ Look for: react, vue, angular, svelte, next, gatsby, nuxt
   ├─ Extract: version field
   ├─ Detect type: if "type": "module" → ES modules
   └─ Framework example: "react": "^18.0.0" → React 18

2. tsconfig.json (if TypeScript)
   ├─ Indicates: TypeScript project
   ├─ Parse: compilerOptions.target (ES version)
   ├─ Check: jsx setting (React/Vue support)

3. Monorepo configs
   ├─ lerna.json → Lerna monorepo
   ├─ turbo.json → Turborepo
   ├─ pnpm-workspace.yaml → pnpm workspaces
   ├─ .npmrc → Package manager config
```

### Python Ecosystem
```
1. pyproject.toml (primary)
   ├─ [project] dependencies field
   ├─ Look for: django, fastapi, flask, sqlalchemy, pytest
   ├─ Extract: version field
   └─ Framework example: "django": "4.2.0"

2. requirements.txt (fallback)
   ├─ Parse: package==version lines
   ├─ Identify: Django==4.2.0, FastAPI==0.95.0

3. setup.py (legacy)
   ├─ Extract: install_requires, python_requires
```

### Go Ecosystem
```
1. go.mod (primary)
   ├─ Parse: require lines
   ├─ Look for: gorilla/mux, gin-gonic/gin, labstack/echo
   ├─ Extract: version (v1.0.0 format)
   ├─ Language: Go (obvious from go.mod)
   └─ Detect monorepo: go.work file

2. Monorepo: go.work
   ├─ Indicates: Go monorepo with workspaces
```

### Java Ecosystem
```
1. pom.xml (Maven)
   ├─ Parse: <dependencies><dependency> nodes
   ├─ Look for: spring-boot, junit, etc
   ├─ Extract: <version> tags

2. build.gradle (Gradle)
   ├─ Parse: dependencies block
   ├─ Look for: framework libraries

3. Monorepo: gradle.settings
   ├─ Indicates: Gradle multi-project build
```

### Other Languages
```
Ruby: Gemfile (+ Gemfile.lock)
Rust: Cargo.toml (+ workspaces)
C#: .csproj, .sln, .NET project files
Go: go.mod, go.work
```

---

## Framework Detection

Once language is identified, detect specific frameworks:

### JavaScript Frameworks
```
React:        "react" in package.json
Vue:          "vue" in package.json
Angular:      "@angular/core" in package.json
Svelte:       "svelte" in package.json
Next.js:      "next" in package.json OR pages/ directory
Gatsby:       "gatsby" in package.json
Nuxt:         "nuxt" in package.json
Express:      "express" in package.json (backend)
Node.js:      package.json with no framework (generic)
```

### Python Frameworks
```
Django:       "django" in pyproject.toml OR requirements.txt
FastAPI:      "fastapi" in pyproject.toml OR requirements.txt
Flask:        "flask" in pyproject.toml OR requirements.txt
SQLAlchemy:   "sqlalchemy" in dependencies
PyTest:       "pytest" in devDependencies
```

### Go Frameworks
```
Gin:          "github.com/gin-gonic/gin" in go.mod
Gorilla Mux:  "github.com/gorilla/mux" in go.mod
Echo:         "github.com/labstack/echo" in go.mod
```

**Version Detection:**
- JavaScript: Parse `"react": "^18.0.0"` → Extract "18.0.0"
- Python: Parse `django==4.2.0` → Extract "4.2.0"
- Go: Parse `github.com/gin-gonic/gin v1.0.0` → Extract "v1.0.0"

---

## Monorepo Detection

Detect monorepo structure and workspace configuration:

```
JavaScript/Node.js Monorepos:
  ✓ lerna.json         → Lerna monorepo (packages/)
  ✓ turbo.json         → Turborepo (apps/ + packages/)
  ✓ pnpm-workspace.yaml → pnpm workspaces
  ✓ yarn workspaces    → Check package.json "workspaces" field

Python Monorepos:
  ✓ Multiple pyproject.toml files in different directories
  ✓ setuptools_scm configuration

Go Monorepos:
  ✓ go.work file       → Go 1.18+ workspaces
  ✓ Multiple go.mod files in subdirectories

Java/Gradle:
  ✓ settings.gradle    → Gradle multi-project
  ✓ Multiple build.gradle files

Detection Algorithm:
1. Look for workspace config file
2. If found: is_monorepo = true
3. If not found: check for multiple package managers
   (if 2+ in different directories → is_monorepo = true)
4. List workspaces/packages if detected
```

---

## Output Format

```json
{
  "primary_language": "typescript" | "python" | "go" | "java" | "rust" | "ruby",
  "primary_framework": "React" | "Django" | "Express" | null,
  "frameworks": [
    {
      "name": "React",
      "version": "18.0.0",
      "language": "javascript",
      "category": "frontend"
    },
    {
      "name": "Express",
      "version": "4.18.0",
      "language": "javascript",
      "category": "backend"
    }
  ],
  "languages": [
    {
      "language": "javascript",
      "file_count": 145,
      "percentage": 60
    },
    {
      "language": "typescript",
      "file_count": 95,
      "percentage": 40
    }
  ],
  "is_monorepo": false,
  "monorepo_type": null | "lerna" | "turbo" | "pnpm" | "gradle" | "go-workspaces",
  "workspaces": [],
  "has_typescript": true,
  "has_testing": true,
  "has_documentation": true,
  "confidence": 0.95,
  "detection_details": {
    "package_manager": "npm",
    "package_file": "package.json",
    "files_scanned": 47,
    "detection_time_ms": 245
  }
}
```

---

## Error Handling

### Error Levels

```
CRITICAL (BLOCK):
  - Repository not found or inaccessible
  - Package manager files corrupted
  Recovery: User must fix repo access

HIGH (WARN):
  - No package manager files found (language unclear)
  - Conflicting framework versions
  Recovery: Assume generic framework, continue

MEDIUM (LOG):
  - Could not parse version number
  - Monorepo structure unclear
  Recovery: Use defaults, continue

LOW (INFO):
  - Secondary frameworks not detected
  - Type hints incomplete
  Recovery: Continue with detected info
```

### Common Failures

```
❌ "package.json not found"
→ Not a Node.js project OR missing package.json. Check file exists.

❌ "Could not parse version: ^18.0.0"
→ Extract only semantic version number (18.0.0), ignore symbols (^, ~, =)

❌ "Monorepo structure unclear"
→ Check for: lerna.json, turbo.json, go.work, pnpm-workspace.yaml

❌ "Conflicting frameworks: React and Vue both found"
→ Unlikely but possible. Use package.json version count to decide primary.
```

---

## Examples

### Example 1: React + Express Monorepo

**Repository Structure:**
```
project/
├── package.json (root, has workspaces)
├── turbo.json (Turborepo config)
├── apps/
│  ├── web/
│  │  └── package.json (React 18)
│  └── api/
│     └── package.json (Express 4.18)
└── packages/
   ├── types/
   │  └── package.json
```

**Output:**
```json
{
  "primary_language": "typescript",
  "primary_framework": "React",
  "frameworks": [
    {
      "name": "React",
      "version": "18.0.0",
      "language": "typescript",
      "category": "frontend"
    },
    {
      "name": "Express",
      "version": "4.18.0",
      "language": "typescript",
      "category": "backend"
    }
  ],
  "languages": [
    {
      "language": "typescript",
      "file_count": 240,
      "percentage": 85
    },
    {
      "language": "javascript",
      "file_count": 42,
      "percentage": 15
    }
  ],
  "is_monorepo": true,
  "monorepo_type": "turbo",
  "workspaces": ["apps/web", "apps/api", "packages/types"],
  "has_typescript": true,
  "has_testing": true,
  "has_documentation": true,
  "confidence": 0.98,
  "detection_details": {
    "package_manager": "npm",
    "package_file": "package.json",
    "files_scanned": 47,
    "detection_time_ms": 245
  }
}
```

### Example 2: Django + Python Single Repo

**Files:**
```
pyproject.toml (with django==4.2.0, djangorestframework==3.14.0)
requirements.txt (for production)
dev-requirements.txt (for testing)
manage.py
```

**Output:**
```json
{
  "primary_language": "python",
  "primary_framework": "Django",
  "frameworks": [
    {
      "name": "Django",
      "version": "4.2.0",
      "language": "python",
      "category": "backend"
    },
    {
      "name": "Django REST Framework",
      "version": "3.14.0",
      "language": "python",
      "category": "backend"
    }
  ],
  "languages": [
    {
      "language": "python",
      "file_count": 156,
      "percentage": 100
    }
  ],
  "is_monorepo": false,
  "monorepo_type": null,
  "workspaces": [],
  "has_typescript": false,
  "has_testing": true,
  "has_documentation": true,
  "confidence": 0.96,
  "detection_details": {
    "package_manager": "pip",
    "package_file": "pyproject.toml",
    "files_scanned": 156,
    "detection_time_ms": 180
  }
}
```

### Example 3: Multi-Framework Project (React + Django)

**Structure:**
```
frontend/
├── package.json (React 18)
└── ... (TypeScript, React files)

backend/
├── pyproject.toml (Django 4.2)
└── ... (Python files)

shared/
└── types/ (TypeScript type definitions)
```

**Output:**
```json
{
  "primary_language": "typescript",
  "primary_framework": "React",
  "frameworks": [
    {
      "name": "React",
      "version": "18.0.0",
      "language": "typescript",
      "category": "frontend"
    },
    {
      "name": "Django",
      "version": "4.2.0",
      "language": "python",
      "category": "backend"
    }
  ],
  "languages": [
    {
      "language": "typescript",
      "file_count": 145,
      "percentage": 55
    },
    {
      "language": "python",
      "file_count": 110,
      "percentage": 42
    },
    {
      "language": "javascript",
      "file_count": 8,
      "percentage": 3
    }
  ],
  "is_monorepo": false,
  "monorepo_type": null,
  "workspaces": [],
  "has_typescript": true,
  "has_testing": true,
  "has_documentation": true,
  "confidence": 0.94,
  "detection_details": {
    "package_manager": "multiple",
    "package_files": ["frontend/package.json", "backend/pyproject.toml"],
    "files_scanned": 263,
    "detection_time_ms": 320
  }
}
```

---

## Integration

### Input From

Main orchestrator (code-surgeon SKILL.md):
```
Calls: framework-detector subagent
Input: {
  repo_root: "/path/to/repository",
  timeout: 120000,  # 2 minutes
  expected_schema: "FrameworkDetection"
}
```

### Output To

Context Researcher (Phase 2):
```
Receives: {
  primary_language,
  frameworks[],
  is_monorepo,
  monorepo_type,
  workspaces
}

Used by: Context Researcher to:
  - Scope analysis to relevant languages
  - Apply framework-specific patterns
  - Understand monorepo structure
  - Guide file selection
```

### Data Contract

```typescript
interface FrameworkDetection {
  primary_language: string;
  primary_framework: string | null;
  frameworks: Array<{
    name: string;
    version: string;
    language: string;
    category: "frontend" | "backend" | "database" | "testing" | "utility";
  }>;
  languages: Array<{
    language: string;
    file_count: number;
    percentage: number;
  }>;
  is_monorepo: boolean;
  monorepo_type: "lerna" | "turbo" | "pnpm" | "gradle" | "go-workspaces" | null;
  workspaces: string[];
  has_typescript: boolean;
  has_testing: boolean;
  has_documentation: boolean;
  confidence: number;  // 0-1
  detection_details: {
    package_manager: string;
    package_file: string | null;
    files_scanned: number;
    detection_time_ms: number;
  };
}
```

---

## Performance Targets

```
Single Repository Scan:
  - Simple project (1 framework, no monorepo): <200ms
  - Complex project (multiple frameworks): <400ms
  - Large monorepo (50+ workspaces): <500ms
  - Maximum timeout: 2 minutes

Memory:
  - Single repo analysis: <5 MB
  - Monorepo with 100 packages: <20 MB

Accuracy:
  - Framework detection: 98%+ (compared to manual review)
  - Version extraction: 95%+ (some versions have non-standard formats)
  - Language detection: 99%+ (from file extensions)
```

---

## Testing

This skill is tested with:
- **5 JavaScript/TypeScript projects** (React, Vue, Angular, Svelte, plain Node)
- **5 Python projects** (Django, FastAPI, Flask, plain Python, mixed)
- **3 Go projects** (Gin, Gorilla, plain Go)
- **2 Java projects** (Maven, Gradle)
- **2 Monorepo projects** (Turborepo, Lerna)
- **3 Edge cases** (no framework detected, conflicting versions, missing files)

See TDD_TEST_SPECIFICATION.md for complete test cases.

---

## Common Mistakes

### ❌ Assuming package.json always has frameworks
Not all Node.js projects use frameworks. Some are utility libraries.
→ **Instead:** Check for actual framework packages, not just Node.js presence.

### ❌ Trusting version numbers without validation
Version formats vary: "^18.0.0", "~4.2", "latest", "1.0.0-beta"
→ **Instead:** Extract core version number, handle special cases gracefully.

### ❌ Failing on monorepo detection
Some monorepos don't have standard config files (custom setup).
→ **Instead:** Look for heuristics (multiple package.json in subdirs), continue with best guess.

### ❌ Missing secondary frameworks
A project might have React + GraphQL + Storybook
→ **Instead:** Scan all dependencies, not just primary framework.

---

