---
name: pattern-extractor
description: Extract coding patterns and conventions from repository source code. Use when analyzing codebase patterns, identifying architectural decisions, or preparing for skill generation.
metadata:
  phase: 2
  pipeline: assimilation
  version: 1.0.0
---

# Pattern Extractor

## Overview

Perform deep code analysis to extract recurring patterns, coding conventions, and architectural decisions. This is phase 2 of the assimilation pipeline—consuming scan-report.json and producing patterns.json.

---

## When to Use

Use this skill when:
- Analyzing a scanned repository for patterns
- Identifying architectural decisions in code
- Extracting conventions for skill generation
- Understanding how a codebase handles common concerns

---

## Input

**Required:** `.github/temp/scan-report.json` (from repo-scanner)

---

## Output

**File:** `.github/temp/patterns.json`

---

## Execution Steps

### Step 1: Validate Input

```bash
# Check scan-report.json exists
if [ ! -f ".github/temp/scan-report.json" ]; then
    echo "ERROR: scan-report.json not found. Run repo-scanner first."
    exit 1
fi
```

### Step 2: Load Scan Report

Read scan-report.json to understand:
- Language (determines grep patterns)
- Framework (provides hints for expected patterns)
- Domains (focus areas for analysis)
- Entry points (key files to analyze)

### Step 3: Define Pattern Categories

| Category | Description | What to Look For |
|----------|-------------|------------------|
| `architecture` | Design patterns, structure | Middleware, MVC, Factory, Singleton, Repository |
| `reliability` | Error handling, resilience | Try/catch, retry logic, circuit breaker, graceful degradation |
| `quality` | Testing, code quality | Test patterns, assertions, mocking, coverage |
| `security` | Auth, validation | Authentication, authorization, input validation, sanitization |
| `conventions` | Project-specific style | Naming patterns, file organization, coding style |

### Step 4: Run Semantic Grep

Use language-appropriate patterns to find code structures.

#### JavaScript/TypeScript Patterns

```bash
# Middleware pattern
grep -rn "middleware\|\.use(\|next()" --include="*.js" --include="*.ts"

# Factory pattern
grep -rn "create[A-Z]\|factory\|Factory" --include="*.js" --include="*.ts"

# Error handling
grep -rn "try.*{$\|\.catch(\|throw new" --include="*.js" --include="*.ts"

# Async patterns
grep -rn "async.*await\|Promise\.\|\.then(" --include="*.js" --include="*.ts"

# Dependency injection
grep -rn "constructor.*private\|@Inject\|inject(" --include="*.js" --include="*.ts"

# Event patterns
grep -rn "\.on(\|\.emit(\|EventEmitter\|addEventListener" --include="*.js" --include="*.ts"

# Repository/DAO pattern
grep -rn "Repository\|findById\|findAll\|save(" --include="*.js" --include="*.ts"
```

#### Python Patterns

```bash
# Decorator pattern
grep -rn "@.*def \|@staticmethod\|@classmethod\|@property" --include="*.py"

# Context manager
grep -rn "with.*as\|__enter__\|__exit__" --include="*.py"

# Error handling
grep -rn "try:\|except.*:\|raise " --include="*.py"

# Async patterns
grep -rn "async def\|await \|asyncio" --include="*.py"

# Dependency injection
grep -rn "@inject\|Depends(\|dependency" --include="*.py"
```

#### Go Patterns

```bash
# Interface pattern
grep -rn "type.*interface\|func.*\(.*\).*{" --include="*.go"

# Error handling
grep -rn "if err != nil\|return.*err\|errors\." --include="*.go"

# Middleware pattern
grep -rn "func.*Handler\|http\.Handler\|middleware" --include="*.go"
```

#### Rust Patterns

```bash
# Result/Error handling
grep -rn "Result<\|\.unwrap()\|\.expect(\|?" --include="*.rs"

# Trait implementations
grep -rn "impl.*for\|trait " --include="*.rs"

# Pattern matching
grep -rn "match.*{\|=>" --include="*.rs"
```

### Step 5: Analyze Key Files

Select max 20 files for deeper analysis:

1. Entry points from scan-report
2. Files in detected domains
3. Files with highest grep hit counts

For each file (max 10KB):
- Read content
- Identify patterns used
- Note line numbers for evidence

### Step 6: Calculate Confidence Scores

For each detected pattern, calculate:

```
confidence = (
    frequency     × 0.30 +    # In how many files? (0-1)
    consistency   × 0.30 +    # Same implementation? (0-1)
    documentation × 0.20 +    # Mentioned in docs? (0-1)
    external      × 0.20      # Known pattern? (0-1)
)
```

#### Scoring Rules

| Component | Score 1.0 | Score 0.5 | Score 0.0 |
|-----------|-----------|-----------|-----------|
| **Frequency** | Found in >50% of relevant files | Found in 20-50% | Found in <20% |
| **Consistency** | Same structure everywhere | Minor variations | Inconsistent |
| **Documentation** | Explicitly documented | Commented | No docs |
| **External** | GoF/known pattern | Common practice | Novel pattern |

### Step 7: Extract Conventions

Analyze code for project-specific conventions:

| Convention | How to Detect |
|------------|---------------|
| **Naming** | Analyze variable/function names: camelCase, snake_case, PascalCase |
| **File structure** | Analyze directory layout: by-type, by-feature, flat |
| **Import style** | Analyze imports: absolute, relative, barrel files |
| **Comment style** | Analyze comments: JSDoc, docstrings, inline |

### Step 8: Require Evidence

**MUST have ≥2 evidence locations** to include a pattern.

Evidence format: `"<file-path>:L<line-number>"`

Examples:
- `"src/middleware/auth.ts:L45"`
- `"lib/router/index.js:L120-L145"`

### Step 9: Generate Output

Create `.github/temp/patterns.json`:

```json
{
  "source": {
    "repo": "<repo-name>",
    "language": "<language>",
    "framework": "<framework>"
  },
  "patterns": [
    {
      "name": "<pattern-name>",
      "category": "<architecture|reliability|quality|security|conventions>",
      "confidence": 0.85,
      "scores": {
        "frequency": 0.9,
        "consistency": 0.8,
        "documentation": 0.7,
        "external": 1.0
      },
      "evidence": [
        "<file>:L<line>",
        "<file>:L<line>"
      ],
      "description": "<what the pattern does>",
      "keywords": ["<discovery-keyword>", "<another-keyword>"]
    }
  ],
  "conventions": {
    "naming": "<camelCase|snake_case|PascalCase|kebab-case>",
    "fileStructure": "<by-type|by-feature|flat|monorepo>",
    "importStyle": "<absolute|relative|barrel>",
    "commentStyle": "<jsdoc|docstring|inline|minimal>"
  },
  "metadata": {
    "extracted_at": "<ISO-timestamp>",
    "extractor_version": "1.0.0",
    "files_analyzed": <count>,
    "patterns_found": <count>
  }
}
```

### Step 10: Report Completion

```
✅ Pattern extraction complete
   Patterns found: <count>
   Categories: architecture(<n>), reliability(<n>), quality(<n>), security(<n>), conventions(<n>)
   Files analyzed: <count>
   
   Report: .github/temp/patterns.json
```

---

## Pattern Recognition Guide

### Architecture Patterns

| Pattern | Indicators | Example Evidence |
|---------|------------|------------------|
| **Middleware Chain** | `use()`, `next()`, ordered handlers | Express app.use(), Koa middleware |
| **MVC** | controllers/, models/, views/ dirs | Separate concerns by layer |
| **Factory** | `create*()` functions, `*Factory` classes | Object instantiation abstraction |
| **Repository** | `*Repository` classes, CRUD methods | Data access abstraction |
| **Singleton** | `getInstance()`, module-level instance | Single instance pattern |
| **Dependency Injection** | Constructor injection, `@Inject` | Inversion of control |

### Reliability Patterns

| Pattern | Indicators | Example Evidence |
|---------|------------|------------------|
| **Error-First Callback** | `(err, result) =>` | Node.js callback convention |
| **Try-Catch Wrapper** | Consistent error boundaries | Centralized error handling |
| **Retry Logic** | Loop with delay, attempt counter | Network request retry |
| **Circuit Breaker** | State tracking, failure threshold | Prevent cascade failures |
| **Graceful Degradation** | Fallback values, default behavior | Service unavailable handling |

### Quality Patterns

| Pattern | Indicators | Example Evidence |
|---------|------------|------------------|
| **Arrange-Act-Assert** | Test structure with sections | Test organization |
| **Mock/Stub** | `jest.mock()`, `sinon.stub()` | Test isolation |
| **Fixture Pattern** | Shared test data setup | Test data management |
| **Integration Test** | Real dependencies, E2E | Full stack testing |

### Security Patterns

| Pattern | Indicators | Example Evidence |
|---------|------------|------------------|
| **Input Validation** | Schema validation, sanitization | Prevent injection |
| **Authentication** | Login, token verification | Identity verification |
| **Authorization** | Role checks, permissions | Access control |
| **Rate Limiting** | Request counting, throttling | Abuse prevention |

---

## Error Handling

| Condition | Action |
|-----------|--------|
| scan-report.json not found | FAIL with error message |
| No patterns found | Produce empty patterns array, warn user |
| File read error | Skip file, log warning, continue |
| Confidence below 0.60 | Include but mark as low-confidence |

---

## Examples

### Example Output: Express.js API

```json
{
  "source": {
    "repo": "my-api",
    "language": "JavaScript",
    "framework": "Express.js"
  },
  "patterns": [
    {
      "name": "middleware-chain",
      "category": "architecture",
      "confidence": 0.92,
      "scores": {
        "frequency": 1.0,
        "consistency": 0.9,
        "documentation": 0.8,
        "external": 1.0
      },
      "evidence": [
        "src/app.js:L15",
        "src/app.js:L22",
        "src/middleware/auth.js:L8"
      ],
      "description": "Request flows through ordered middleware functions with next() chaining",
      "keywords": ["middleware", "request processing", "express", "chain"]
    },
    {
      "name": "error-first-callback",
      "category": "reliability",
      "confidence": 0.78,
      "scores": {
        "frequency": 0.7,
        "consistency": 0.8,
        "documentation": 0.6,
        "external": 1.0
      },
      "evidence": [
        "src/services/db.js:L34",
        "src/services/file.js:L12"
      ],
      "description": "Callbacks receive error as first parameter for consistent error handling",
      "keywords": ["callback", "error handling", "async", "node"]
    }
  ],
  "conventions": {
    "naming": "camelCase",
    "fileStructure": "by-type",
    "importStyle": "relative",
    "commentStyle": "jsdoc"
  },
  "metadata": {
    "extracted_at": "2026-01-25T11:00:00Z",
    "extractor_version": "1.0.0",
    "files_analyzed": 18,
    "patterns_found": 6
  }
}
```

---

## Conventions

✅ **Do:**
- Require ≥2 evidence locations for each pattern
- Calculate all four confidence components
- Include keywords for pattern discovery
- Use relative file paths in evidence

❌ **Don't:**
- Include patterns with only 1 evidence location
- Accept confidence scores outside 0.0-1.0
- Include repo-specific variable names in descriptions
- Skip the conventions section

---

## Related Skills

- [repo-scanner](../repo-scanner/SKILL.md) — Phase 1: Scan repository structure
- [skill-generator](../skill-generator/SKILL.md) — Phase 3: Generate skills from patterns
- [orchestrator](../orchestrator/SKILL.md) — Coordinates all phases
