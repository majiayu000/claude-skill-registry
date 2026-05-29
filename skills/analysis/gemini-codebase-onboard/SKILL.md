---
name: gemini-codebase-onboard
description: Use Gemini CLI's 1M token context to understand entire codebases in one pass. Full architecture mapping, pattern discovery, and onboarding documentation.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TodoWrite
x-version: 1.0.0
x-category: platforms
x-tags:
  - gemini
  - codebase-analysis
  - architecture
  - multi-model
  - onboarding
x-author: context-cascade
x-verix-description: |
  [assert|neutral] gemini-codebase-onboard skill for megacontext analysis [ground:given] [conf:0.95] [state:confirmed]
---

<!-- S0 META-IDENTITY -->

# Gemini Codebase Onboard Skill



---

## LIBRARY-FIRST PROTOCOL (MANDATORY)

**Before writing ANY code, you MUST check:**

### Step 1: Library Catalog
- Location: `.claude/library/catalog.json`
- If match >70%: REUSE or ADAPT

### Step 2: Patterns Guide
- Location: `.claude/docs/inventories/LIBRARY-PATTERNS-GUIDE.md`
- If pattern exists: FOLLOW documented approach

### Step 3: Existing Projects
- Location: `D:\Projects\*`
- If found: EXTRACT and adapt

### Decision Matrix
| Match | Action |
|-------|--------|
| Library >90% | REUSE directly |
| Library 70-90% | ADAPT minimally |
| Pattern exists | FOLLOW pattern |
| In project | EXTRACT |
| No match | BUILD (add to library after) |

---

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

## Purpose

Use Gemini CLI's massive 1 million token context window to analyze entire codebases in a single pass. Generate architecture maps, pattern documentation, and onboarding guides.

## When to Use This Skill

- Onboarding to a new codebase
- Understanding full system architecture
- Mapping dependencies across all files
- Finding patterns and anti-patterns
- Migration planning (need full context)
- Security audits requiring full codebase awareness
- Refactoring impact analysis

## When NOT to Use This Skill

- Working with single file (use Claude directly)
- Complex reasoning tasks (Claude is better)
- Writing new features (Gemini gets stuck in loops)
- Iterative refinement (use Codex)

## Workflow

### Phase 1: Megacontext Load

```bash
# Load entire codebase
./scripts/multi-model/gemini-yolo.sh "Analyze architecture" task-id megacontext

# Via delegate.sh
./scripts/multi-model/delegate.sh gemini "Map full architecture" --all-files

# Direct Gemini
bash -lc "gemini --all-files 'Analyze entire codebase and document architecture'"
```

### Phase 2: Analysis Queries

Common analysis patterns:
- Architecture overview
- Dependency mapping
- Pattern identification
- Security scanning
- Migration assessment

### Phase 3: Documentation Generation

1. Gemini produces findings
2. Claude synthesizes into documentation
3. Store in project for future reference

## Context Window Specs

| Metric | Value |
|--------|-------|
| Capacity | 1 million tokens |
| Equivalent | ~1,500 pages |
| Lines of Code | ~30,000 LOC |
| Best for | Projects under 30K LOC |

## Success Criteria

- Full architecture understood
- Key patterns documented
- Dependencies mapped
- Onboarding guide created

## Example Usage

### Example 1: New Project Onboarding

```text
User: "I just joined this team, help me understand the codebase"

Gemini Analysis:
bash -lc "gemini --all-files 'Create comprehensive onboarding guide including:
1. High-level architecture
2. Key components and their responsibilities
3. Data flow between components
4. Configuration and environment setup
5. Common patterns used'"

Output:
- Architecture: Microservices with API gateway
- Key Services: auth, users, orders, notifications
- Patterns: Repository pattern, Event-driven
- Setup: Docker Compose with 4 services
```

### Example 2: Refactoring Impact Analysis

```text
User: "What would break if we rename User to Account?"

Gemini Analysis:
bash -lc "gemini --all-files 'Identify all files affected by renaming User to Account'"

Output:
- 47 files with direct User references
- 12 database migrations needed
- 8 API endpoints returning User data
- 15 frontend components
- 3 background jobs
```

### Example 3: Security Audit

```text
User: "Find all places handling sensitive data"

Gemini Analysis:
bash -lc "gemini --all-files 'Security audit: Find all PII handling, auth patterns, and potential vulnerabilities'"

Output:
- PII fields: 12 database columns
- Auth: JWT with refresh tokens
- Concerns: 3 endpoints missing auth middleware
- Logging: 2 instances of sensitive data in logs
```

## Query Patterns

### Architecture Documentation
```
gemini --all-files "Document the full system architecture with component interactions"
```

### Dependency Mapping
```
gemini --all-files "Create a dependency graph showing how all modules relate"
```

### Pattern Analysis
```
gemini --all-files "Identify all design patterns used and assess consistency"
```

### API Documentation
```
gemini --all-files "Document all API endpoints with their request/response formats"
```

## Integration with Meta-Loop

```
META-LOOP PROPOSE PHASE:
    |
    +---> gemini-codebase-onboard
    |         |
    |         +---> Gemini: Load entire codebase (--all-files)
    |         +---> Gemini: Analyze architecture
    |         +---> Gemini: Identify impact areas
    |
    +---> Claude: Synthesize into plan
    |
    +---> Continue to IMPLEMENT phase
```

## Memory Integration

Results stored at:
- Key: `multi-model/gemini/onboard/{project}/{task_id}`
- Tags: WHO=gemini-megacontext, WHY=codebase-analysis
- Contains: Architecture map, patterns, dependencies

## Limitations

Based on real developer feedback:
- May generate errors in analysis (missing XML tags)
- Can get stuck in loops trying to fix mistakes
- Switches to Flash model after 5 minutes (Flash is weaker)
- Slower than Claude for complex reasoning
- Not great for implementation tasks

## Strengths

- Breadth of analysis is excellent
- Can summarize entire folders effectively
- Great for onboarding and auditing
- Powerful for architectural understanding

## Related Skills

- `multi-model-discovery`: Find existing solutions
- `gemini-research`: Current info research
- `codex-iterative-fix`: After understanding, for implementation
- `documentation`: Generate docs from analysis

<!-- S4 SUCCESS CRITERIA -->

## Verification Checklist

- [ ] Entire codebase loaded
- [ ] Architecture documented
- [ ] Key patterns identified
- [ ] Dependencies mapped
- [ ] Onboarding guide created
- [ ] Memory-MCP updated

<!-- PROMISE -->

[commit|confident] <promise>GEMINI_CODEBASE_ONBOARD_COMPLETE</promise>
