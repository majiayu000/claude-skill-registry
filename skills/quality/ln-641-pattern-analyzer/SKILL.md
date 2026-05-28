---
name: ln-641-pattern-analyzer
description: L3 Worker. Analyzes single pattern implementation, calculates 4 scores (compliance, completeness, quality, implementation), identifies gaps and issues. Usually invoked by ln-640, can also analyze a specific pattern on user request.
---

# Pattern Analyzer

L3 Worker that analyzes a single architectural pattern against best practices and calculates 4 scores.

## Purpose & Scope
- Analyze ONE pattern per invocation (receives pattern name, locations, best practices from coordinator)
- Find all implementations in codebase (Glob/Grep)
- Validate implementation exists and works
- Calculate 4 scores: compliance, completeness, quality, implementation
- Identify gaps and issues with severity and effort estimates
- Return structured analysis result to coordinator

## Input (from ln-640 coordinator)
```
- pattern: string          # Pattern name (e.g., "Job Processing")
- locations: string[]      # Known file paths/directories
- adr_reference: string    # Path to related ADR (if exists)
- bestPractices: object    # Best practices from MCP Ref/Context7/WebSearch
```

## Workflow

### Phase 1: Find Implementations
```
# Use locations from coordinator + additional search
files = []
files.append(Glob(locations))

# Expand search using common_patterns.md grep patterns
IF pattern == "Job Processing":
  files.append(Grep("Queue|Worker|Job|Bull|BullMQ", "**/*.{ts,js,py}"))
IF pattern == "Event-Driven":
  files.append(Grep("EventEmitter|publish|subscribe|on\\(", "**/*.{ts,js,py}"))
# ... etc

deduplicate(files)
```

### Phase 2: Read and Analyze Code
```
FOR EACH file IN files (limit: 10 key files):
  Read(file)
  Extract:
    - Components implemented
    - Patterns used
    - Error handling approach
    - Logging/observability
    - Tests coverage
```

### Phase 3: Calculate 4 Scores

**Compliance Score (0-100):**
```
score = 0
IF follows industry standard (MADR, Nygard): +30
IF has ADR documentation: +20
IF consistent naming conventions: +15
IF follows tech stack conventions: +15
IF no anti-patterns detected: +20
```

**Completeness Score (0-100):**
```
score = 0
IF all required components present: +40
IF error handling implemented: +20
IF logging/observability: +15
IF tests exist: +15
IF documentation complete: +10
```

**Quality Score (0-100):**
```
score = 0
IF code readable (short methods, clear names): +25
IF maintainable (low complexity): +25
IF no code smells: +20
IF follows SOLID: +15
IF performance optimized: +15
```

**Implementation Score (0-100):**
```
score = 0
IF code exists and compiles: +30
IF used in production paths (not dead code): +25
IF no dead/unused implementations: +15
IF integrated with other patterns: +15
IF monitored/observable: +15
```

### Phase 4: Identify Issues and Gaps
```
issues = []
FOR EACH bestPractice IN bestPractices:
  IF NOT implemented:
    issues.append({
      severity: "HIGH" | "MEDIUM" | "LOW",
      category: "compliance" | "completeness" | "quality" | "implementation",
      issue: description,
      suggestion: how to fix,
      effort: estimate ("2h", "4h", "1d", "3d")
    })

gaps = {
  undocumented: aspects not in ADR,
  unimplemented: ADR decisions not in code
}

recommendations = [
  "Create ADR for X",
  "Update existing ADR with Y",
  "Refactor Z to match pattern"
]
```

### Phase 5: Return Result
```json
{
  "pattern": "Job Processing",
  "scores": {
    "compliance": 72,
    "completeness": 85,
    "quality": 68,
    "implementation": 90
  },
  "codeReferences": [
    "src/jobs/processor.ts",
    "src/workers/base.ts"
  ],
  "issues": [
    {
      "severity": "HIGH",
      "category": "quality",
      "issue": "No dead letter queue",
      "suggestion": "Add Bull DLQ configuration",
      "effort": "4h"
    }
  ],
  "gaps": {
    "undocumented": ["Error recovery strategy"],
    "unimplemented": ["Job prioritization from ADR"]
  },
  "recommendations": [
    "Create ADR for dead letter queue strategy"
  ]
}
```

## Critical Rules
- **One pattern only:** Analyze only the pattern passed by coordinator
- **Read before score:** Never score without reading actual code
- **Effort estimates:** Always provide realistic effort for each issue
- **Best practices comparison:** Use bestPractices from coordinator, not assumptions
- **Code references:** Always include file paths for findings

## Definition of Done
- All implementations found via Glob/Grep
- Key files read and analyzed
- 4 scores calculated with justification
- Issues identified with severity, category, suggestion, effort
- Gaps documented (undocumented, unimplemented)
- Recommendations provided
- Structured result returned to coordinator

## Reference Files
- Scoring rules: `../ln-640-pattern-evolution-auditor/references/scoring_rules.md`
- Common patterns: `../ln-640-pattern-evolution-auditor/references/common_patterns.md`

---
**Version:** 1.0.0
**Last Updated:** 2026-01-29
