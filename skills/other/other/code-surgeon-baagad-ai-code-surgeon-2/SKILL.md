---
name: code-surgeon-context-researcher
description: Use when analyzing a codebase to select relevant files, build dependency maps, and extract architectural patterns for informed implementation planning
---

# code-surgeon Context Researcher

## Overview

**context-researcher** is the most complex sub-skill. It receives requirements and framework information, then performs deep codebase analysis to select relevant files, understand dependencies, and extract team conventions.

**Core principle:** Transform a requirement into deeply-understood codebase context that enables precise, informed implementation planning.

---

## When to Use

This skill runs in **Phase 2** of code-surgeon orchestration, after Issue Analyzer and Framework Detector complete.

**Input from:**
- Issue Analyzer: `{issue_type, requirements[], file_hints}`
- Framework Detector: `{primary_language, frameworks[], is_monorepo}`
- Main Orchestrator: `{repo_root, depth_mode}`

**Output to:**
- Implementation Planner (Phase 3)

---

## The Challenge

Context Researcher must answer: **"What in this codebase is relevant to this requirement?"**

For a 500K line codebase:
- ❌ Can't load all files (token explosion)
- ❌ Can't parse full AST (too slow, 100+ seconds)
- ❌ Can't guess blindly (might miss critical code)
- ✅ Must intelligently select relevant files
- ✅ Must understand file relationships
- ✅ Must respect token budget
- ✅ Must complete in <5 minutes

---

## Analysis Pipeline

### Step 1: Preparation (30 seconds)

```
Inputs received:
  - issue_type: "feature" | "bug" | "refactor" | "perf" | "docs"
  - requirements: ["Add JWT refresh", "Implement sliding expiration", ...]
  - file_hints: ["src/auth", "src/api"]
  - primary_language: "typescript"
  - frameworks: [{React, Express, TypeScript}, ...]
  - is_monorepo: false
  - depth_mode: "standard" (60K tokens available)

Initialize:
  - Token budget: 60K tokens
  - Reserved: 10K tokens (for later phases)
  - Available for analysis: 50K tokens
  - Scanning starts...
```

### Step 2: File Discovery (1 minute)

**Tier 1: Direct Impact Files** (Always include)
```
Find files matching:
  1. Mentioned in file_hints (src/auth, src/api, etc.)
  2. Match issue keywords (auth → *auth*.ts, etc.)
  3. Core framework files (src/index.ts, src/app.ts, etc.)
  4. Related test files (src/**/*.test.ts, tests/**)

Example for "Add JWT refresh":
  ✓ src/auth/authContext.tsx
  ✓ src/auth/jwt.ts (if exists)
  ✓ src/api/auth.ts
  ✓ src/types/auth.d.ts
  ✓ tests/auth/*.test.ts
  ✓ .env.example

Result: 10-20 files (Tier 1)
Token estimate: ~15K tokens
```

**Tier 2: Dependent Files** (Smart selection)
```
For each Tier 1 file, find:
  1. Files that IMPORT this file (reverse dependencies)
  2. Files THIS file imports (forward dependencies)
  3. TEST files for this module

Algorithm per Tier 1 file:
  IF file exports public API (auth context):
    INCLUDE all files that import it (export is used)
  ELSE IF file is internal utility:
    INCLUDE only direct callers

Confidence heuristic:
  - Files in same directory: High priority
  - Files in parent/sibling directories: Medium
  - Files in distant directories: Low priority

Example for authContext.tsx:
  ✓ src/pages/login.tsx (imports useAuth)
  ✓ src/components/ProtectedRoute.tsx
  ✓ src/components/UserProfile.tsx
  ~ src/services/api.ts (might use auth)

Result: 15-30 files (Tier 2)
Token estimate: ~20K tokens
```

**Tier 3: Pattern Files** (Selective)
```
Find architectural patterns to follow:
  1. Look for similar implementations in codebase
  2. Find error handling examples
  3. Find framework-specific patterns

Examples:
  - "How do other services handle async?"
  - "What's the pattern for API error responses?"
  - "How are React hooks organized?"

Result: 3-5 files (Tier 3)
Token estimate: ~5K tokens
```

### Step 3: Dependency Mapping (1 minute)

**Build Lightweight Graph** (No full AST parsing)
```
For each selected file:
  1. Extract imports using regex
  2. Extract exports using regex
  3. Build relationship map

Strategy:
  ❌ NOT: Full AST parsing (too slow)
  ❌ NOT: Call graph analysis (too complex)
  ✅ YES: Regex-based import/export detection
  ✅ YES: Direct file relationships
  ✅ YES: Dependency count and direction

Output structure:
  {
    "src/auth/authContext.tsx": {
      "imports": ["src/types/auth", "src/utils/token"],
      "exported": ["useAuth", "AuthProvider"],
      "imported_by": ["src/pages/login.tsx", "src/components/ProtectedRoute.tsx"],
      "impact": "high"  # if >5 files depend on it
    }
  }
```

### Step 4: Pattern Extraction (1 minute)

**Identify Architectural Patterns**
```
Scan selected files for patterns:

Pattern 1: Hook Pattern (React)
  Look for: "export const useXxx = () => {"
  Extract: Hook signature, return type, dependencies

Pattern 2: Service Pattern (Backend)
  Look for: "class XxxService" or "export const xxxService"
  Extract: Methods, async operations

Pattern 3: Error Handling Pattern
  Look for: "try { } catch (error) {"
  Extract: Error types, recovery strategies

Pattern 4: Typing Pattern
  Look for: "interface Xxx {" or "type Xxx ="
  Extract: Type structure, required vs optional

Pattern 5: API Pattern
  Look for: "router.get/post/put/delete"
  Extract: Endpoint structure, request/response types
```

### Step 5: Team Conventions Extraction (30 seconds)

**Load & Parse Team Guidelines**
```
Read: .claude/team-guidelines.md (if exists)
Extract:
  - Coding style rules
  - Architecture patterns required
  - Naming conventions
  - Error handling requirements
  - Testing requirements
  - Security requirements

Create rules map:
  {
    "typescript": {
      "strict_mode": true,
      "no_any": true,
      "interface_over_type": true
    },
    "react": {
      "use_hooks": true,
      "use_context_api": true,
      "functional_components_only": true
    },
    "security": {
      "require_auth_check": true,
      "validate_all_input": true
    }
  }
```

### Step 6: Content Extraction (2 minutes)

**Smart Content Extraction** (Respecting token budget)
```
For each selected file:

IF file < 300 lines:
  INCLUDE full content (cheap tokens)

ELSE IF file 300-1000 lines:
  EXTRACT:
    - File header + imports
    - Function signatures (1 line each)
    - Key implementations (50-line context windows)
    - Test examples
  SKIP: Loop internals, temporary variables

ELSE IF file 1000-5000 lines:
  EXTRACT:
    - File header
    - Relevant function signatures
    - Related implementations (20-30 lines)
  SKIP: Most implementation details

ELSE (file > 5000 lines):
  EXTRACT ONLY:
    - File header
    - Function names and signatures
    - Most relevant implementation (10-15 lines)
```

### Step 7: Caching for Performance (30 seconds)

**Cache Analysis Results**
```
Save to: .claude/planning/cache/
Files cached:
  - file-structure-<hash>.json
    {files: [...], modification_time, file_sizes}

  - dependency-graph-<hash>.json
    {imports/exports per file, impact levels}

  - patterns-<hash>.json
    {patterns found, locations}

Cache validity:
  - File structure: Valid until files added/deleted (git detects)
  - Dependency graph: Valid 1 day or until imports change
  - Patterns: Valid 1 week (stable architectural decisions)

Next request reuses:
  - File structure (2K token savings)
  - Dependency graph (3K token savings)
  - Patterns (3K token savings)
  → 25-30% token reduction on repeat requests
```

---

## Output Format

```json
{
  "files_selected": [
    {
      "path": "src/auth/authContext.tsx",
      "tier": 1,
      "size_bytes": 3400,
      "relevance": "critical",
      "reason": "Directly implements useAuth mentioned in requirement"
    },
    {
      "path": "src/pages/login.tsx",
      "tier": 2,
      "size_bytes": 2100,
      "relevance": "high",
      "reason": "Imports useAuth, needs JWT refresh integration"
    }
  ],
  "file_count": {
    "tier_1": 12,
    "tier_2": 18,
    "tier_3": 5,
    "total": 35
  },
  "dependency_graph": {
    "src/auth/authContext.tsx": {
      "imports": ["src/types/auth", "src/utils/token"],
      "exported": ["useAuth", "AuthProvider"],
      "imported_by": ["src/pages/login.tsx", "src/components/ProtectedRoute.tsx"],
      "impact": "high"
    }
  },
  "patterns_found": [
    {
      "name": "React Hook Pattern",
      "example_file": "src/hooks/useLocalStorage.ts",
      "description": "Custom hooks using useState + useEffect + useCallback",
      "location": "src/hooks/**/*.ts"
    },
    {
      "name": "Service Singleton Pattern",
      "example_file": "src/services/api.ts",
      "description": "Services as singletons with static getInstance()",
      "location": "src/services/**/*.ts"
    }
  ],
  "team_conventions": [
    "Use TypeScript strict mode (no 'any')",
    "Prefer interfaces over types",
    "All async code must have error boundaries",
    "Use Context API for state (not Redux)",
    "All exported types documented with JSDoc"
  ],
  "token_analysis": {
    "tier_1_tokens": 15000,
    "tier_2_tokens": 20000,
    "tier_3_tokens": 5000,
    "total_used": 40000,
    "budget_remaining": 20000,
    "cache_savings": "25% (7.5K tokens saved from cache)"
  },
  "cache_status": {
    "file_structure_cached": true,
    "dependency_graph_cached": false,
    "patterns_cached": true,
    "cache_created": "2025-02-12T13:15:00Z"
  },
  "analysis_metadata": {
    "depth_mode": "standard",
    "files_scanned": 235,
    "duration_seconds": 285,
    "primary_language": "typescript",
    "is_monorepo": false
  }
}
```

---

## Depth Modes

### QUICK Mode (30K tokens)
```
File selection:
  - Tier 1 files ONLY
  - No Tier 2 filtering (include all imports/importers)
  - No Tier 3 patterns

Content extraction:
  - Function signatures only
  - Skip implementations

Dependency graph:
  - Direct relationships only (1 level)

Patterns:
  - Skip pattern extraction

Result:
  - 10-15 files selected
  - ~25K tokens used
  - 5K tokens buffer
  - Accuracy: ~85% (might miss dependencies)
```

### STANDARD Mode (60K tokens) ← Default
```
File selection:
  - Tier 1: All direct impact files
  - Tier 2: Smart filtered (relevant imports/importers)
  - Tier 3: Top 3-5 patterns

Content extraction:
  - Headers + signatures
  - Key implementations (50-line context windows)

Dependency graph:
  - Full graph with impact scoring

Patterns:
  - Extract 3-5 key architectural patterns

Result:
  - 35-45 files selected
  - ~50K tokens used
  - 10K tokens buffer
  - Accuracy: ~95% (good coverage)
```

### DEEP Mode (90K tokens)
```
File selection:
  - Tier 1: All files
  - Tier 2: All related files (no filtering)
  - Tier 3: All patterns + examples

Content extraction:
  - Full content for files < 500 lines
  - Detailed extracts for larger files

Dependency graph:
  - Full bidirectional graph
  - Call relationships where detectable

Patterns:
  - Extract ALL patterns found
  - Include counter-examples

Result:
  - 50-70 files selected
  - ~80K tokens used
  - 10K tokens buffer
  - Accuracy: ~99% (comprehensive coverage)
```

---

## Error Handling

### Scenarios

```
CRITICAL (BLOCK):
  - Repository path not found
  - Package manager files corrupted
  Recovery: User must fix repo access

HIGH (WARN):
  - Too many files selected (would exceed token budget)
  - Circular import detected
  Recovery: Auto-switch to QUICK mode

MEDIUM (LOG):
  - Pattern detection incomplete
  - Dependency graph partial
  Recovery: Continue with what's found

LOW (INFO):
  - File extraction partially successful
  - Cache miss (first time analysis)
  Recovery: Continue normally
```

---

## Performance Targets

```
Analysis time:
  - QUICK: <2 minutes
  - STANDARD: <5 minutes
  - DEEP: <10 minutes

Memory usage:
  - Single analysis: <50 MB
  - Including cache: <200 MB

Accuracy:
  - File selection: 95%+ match with manual review
  - Dependency mapping: 90%+ accuracy
  - Pattern extraction: 85%+ accuracy
  - Token estimation: ±10% accuracy
```

---

## Examples

### Example 1: React + Node Monolith

**Issue:** "Add JWT token refresh mechanism"
**Depth:** STANDARD

**Analysis Output:**
```
Tier 1 (Direct Impact):
  ✓ src/auth/authContext.tsx (useAuth implementation)
  ✓ src/auth/jwt.ts (JWT utilities)
  ✓ src/api/auth.ts (auth endpoints)
  ✓ src/types/auth.d.ts (types)
  ✓ tests/auth/*.test.ts

Tier 2 (Dependent Files):
  ✓ src/pages/login.tsx (uses useAuth)
  ✓ src/components/ProtectedRoute.tsx (auth check)
  ✓ src/services/api.ts (makes API calls)
  ✓ src/middleware/auth.ts (server-side auth)

Patterns Found:
  1. React Hook Pattern (useAuth usage)
  2. Service Singleton Pattern (API service)
  3. Error Handling Pattern (try/catch blocks)

Teams Conventions:
  - No 'any' types in TypeScript
  - All async code needs error handling
  - Use Context API for state
```

### Example 2: Django REST API

**Issue:** "Fix database N+1 query in user endpoint"
**Depth:** STANDARD

**Analysis Output:**
```
Tier 1 (Direct Impact):
  ✓ myapp/views.py (user endpoint)
  ✓ myapp/models.py (User model)
  ✓ myapp/serializers.py (serialization)
  ✓ tests/test_users.py

Tier 2 (Related Files):
  ✓ myapp/permissions.py (auth checks)
  ✓ myapp/filters.py (filtering logic)
  ~ myapp/pagination.py (pagination)

Patterns Found:
  1. Django Model Pattern (ORM usage)
  2. Serializer Pattern (DRF patterns)
  3. Query Optimization Pattern (select_related/prefetch_related)

Team Conventions:
  - Use Django ORM, no raw SQL
  - All views must have permission checks
  - Use DRF serializers for all APIs
```

---

## Integration

### Input Contract
```typescript
interface ContextResearcherInput {
  issue_type: "feature" | "bug" | "refactor" | "performance" | "docs";
  requirements: string[];
  file_hints: string[];
  primary_language: string;
  frameworks: Array<{name, version, language, category}>;
  is_monorepo: boolean;
  repo_root: string;
  depth_mode: "quick" | "standard" | "deep";
  timeout_seconds: 300;  // 5 minutes max
}
```

### Output Contract
```typescript
interface ContextResearcherOutput {
  files_selected: Array<{
    path: string;
    tier: 1 | 2 | 3;
    size_bytes: number;
    relevance: "critical" | "high" | "medium" | "low";
    reason: string;
  }>;
  file_count: {
    tier_1: number;
    tier_2: number;
    tier_3: number;
    total: number;
  };
  dependency_graph: Record<string, {
    imports: string[];
    exported: string[];
    imported_by: string[];
    impact: "critical" | "high" | "medium" | "low";
  }>;
  patterns_found: Array<{
    name: string;
    example_file: string;
    description: string;
    location: string;
  }>;
  team_conventions: string[];
  token_analysis: {
    tier_1_tokens: number;
    tier_2_tokens: number;
    tier_3_tokens: number;
    total_used: number;
    budget_remaining: number;
    cache_savings: string;
  };
  cache_status: {
    file_structure_cached: boolean;
    dependency_graph_cached: boolean;
    patterns_cached: boolean;
    cache_created: string;
  };
  analysis_metadata: {
    depth_mode: string;
    files_scanned: number;
    duration_seconds: number;
    primary_language: string;
    is_monorepo: boolean;
  };
}
```

---

## Key Algorithms

### File Selection Algorithm
```
FOR EACH requirement:
  1. Extract keywords (auth, login, database, etc.)
  2. Find files matching keywords
  3. Find files in matching directories
  4. Rank by relevance
  5. Include top matches as Tier 1

FOR EACH Tier 1 file:
  1. Extract imports (forward dependencies)
  2. Find files that import this file (reverse deps)
  3. Rank by relationship strength
  4. Include high-confidence matches as Tier 2

FOR ENTIRE selection:
  1. Find similar implementations (patterns)
  2. Find test files
  3. Find config files
  4. Include as Tier 3

APPLY token budget:
  IF total tokens > budget:
    REMOVE lowest-confidence Tier 2 files
    REMOVE all Tier 3 except top 3
```

### Dependency Detection (Regex-based)
```
JavaScript/TypeScript:
  Pattern: import .* from ['"]([^'"]+)['"]
  Pattern: export (const|function|class) (\w+)

Python:
  Pattern: from .* import .*
  Pattern: import .*
  Pattern: def .* or class .*

Go:
  Pattern: import .*
  Pattern: func .* or type .* struct

Java:
  Pattern: import .*;
  Pattern: public .* class .*
```

---

## Testing

This skill is tested with:
- 3 JavaScript/TypeScript projects (sizes: 200, 500, 1000+ files)
- 2 Python projects (Django, FastAPI)
- 1 Go project (Gin)
- 2 Monorepo projects (Turborepo, Lerna)
- Various issue types (feature, bug, refactor, perf)
- All 3 depth modes
- Cache validation (cold start vs. warm)

---

## Common Mistakes

### ❌ Trying to analyze everything
"If I include all files, I'll be comprehensive!" → Token explosion, no time for planning.
→ **Instead:** Intelligently select relevant files, trust the filtering.

### ❌ Parsing full AST
"I need to understand every function call!" → Too slow (100+ seconds), too expensive.
→ **Instead:** Use lightweight regex for imports/exports, accept 90% accuracy.

### ❌ Ignoring team guidelines
"The code will speak for itself!" → Generates code that violates team standards.
→ **Instead:** Always read `.claude/team-guidelines.md`, enforce conventions.

### ❌ Skipping pattern extraction
"I'll invent new patterns!" → Code looks different from rest of codebase.
→ **Instead:** Extract existing patterns, ensure consistency.

---

