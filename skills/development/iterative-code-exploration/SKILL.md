---
name: iterative-code-exploration
description: Progressive context retrieval pattern for understanding unfamiliar codebases through iterative refinement
license: MIT
metadata:
  source: affaan-m/everything-claude-code
  adapted-by: ai-skills
  category: code-exploration
---

# Iterative Code Exploration

A systematic pattern for progressively exploring and understanding unfamiliar codebases through iterative context refinement.

## The Problem

When working with new codebases, you often don't know:
- Which files contain relevant code
- What patterns and conventions exist
- What terminology the project uses
- How components interact

Standard approaches fail:
- **Read everything**: Time-consuming and overwhelming
- **Guess locations**: Often misses critical context
- **Ask broad questions**: Returns too much irrelevant information

## The Solution: 4-Phase Iterative Loop

```
┌─────────────────────────────────────────────┐
│                                             │
│   ┌──────────┐      ┌──────────┐            │
│   │ DISCOVER │─────▶│ EVALUATE │            │
│   └──────────┘      └──────────┘            │
│        ▲                  │                 │
│        │                  ▼                 │
│   ┌──────────┐      ┌──────────┐            │
│   │   LOOP   │◀─────│  REFINE  │            │
│   └──────────┘      └──────────┘            │
│                                             │
│        Max 3-4 cycles, then synthesize      │
└─────────────────────────────────────────────┘
```

### Phase 1: DISCOVER

Start with broad exploration:

```bash
# Find entry points
find . -name "main.*" -o -name "index.*" -o -name "app.*" | head -20

# Discover project structure
tree -L 3 -I 'node_modules|dist|build'

# Find configuration
find . -name "*.config.*" -o -name "package.json" -o -name "*.toml"

# Identify key patterns
grep -r "export class" --include="*.ts" src/ | head -20
grep -r "def " --include="*.py" . | head -20
```

Document initial findings:
- Project type (web app, library, service, etc.)
- Tech stack (languages, frameworks)
- Architecture hints (monorepo, microservices, etc.)

### Phase 2: EVALUATE

Assess discovered files for relevance:

```bash
# Read high-value files
cat README.md
cat ARCHITECTURE.md 2>/dev/null
cat docs/overview.md 2>/dev/null

# Check package manifests
cat package.json | jq '.dependencies, .scripts'
cat Cargo.toml 2>/dev/null
cat requirements.txt 2>/dev/null
```

**Scoring Criteria:**
- **Critical (★★★)**: Entry points, core logic, main configs
- **Important (★★)**: Utilities, shared components, types
- **Supporting (★)**: Tests, docs, examples
- **Noise (-)**: Generated files, vendored code

### Phase 3: REFINE

Focus on specific areas identified as relevant:

```bash
# Dive into specific modules
ls -la src/core/
cat src/core/index.ts

# Trace dependencies
grep -r "import.*from.*core" --include="*.ts" src/ | head -20

# Find related patterns
grep -A 5 -B 5 "class UserService" src/**/*.ts

# Check tests for usage examples
find . -name "*.test.*" -o -name "*.spec.*" | head -10
```

Build mental model:
- How components connect
- What patterns are used consistently
- Where similar functionality lives

### Phase 4: LOOP

Decision point - do you need more context?

**Continue if:**
- Key functionality still unclear
- Dependencies not fully traced
- Patterns inconsistent or confusing

**Stop if:**
- Core logic understood
- Can explain main flows
- Ready to make changes confidently

## Practical Workflow

### For Feature Implementation

1. **Discover**: Find similar existing features
   ```bash
   grep -r "feature-name" src/
   find . -name "*feature*"
   ```

2. **Evaluate**: Review implementation patterns
   ```bash
   cat src/features/similar-feature/index.ts
   ```

3. **Refine**: Check tests and edge cases
   ```bash
   cat src/features/similar-feature/*.test.ts
   ```

4. **Loop**: Trace dependencies until clear

### For Bug Fixing

1. **Discover**: Locate error origin
   ```bash
   grep -r "error message" src/
   git log -S "error message"
   ```

2. **Evaluate**: Understand surrounding context
   ```bash
   cat path/to/file.ts | grep -A 20 -B 20 "error location"
   ```

3. **Refine**: Check call sites and callers
   ```bash
   grep -r "functionName" --include="*.ts" src/
   ```

4. **Loop**: Expand context as needed

### For Refactoring

1. **Discover**: Map current structure
   ```bash
   find src/ -name "*.ts" | xargs wc -l | sort -n
   grep -r "class\|interface" --include="*.ts" src/ | wc -l
   ```

2. **Evaluate**: Identify coupling points
   ```bash
   grep -r "import.*from.*module" src/ | cut -d: -f2 | sort | uniq -c | sort -rn
   ```

3. **Refine**: Find all usages
   ```bash
   grep -r "ComponentName" --include="*.ts" src/
   ```

4. **Loop**: Ensure all references found

## Output Template

After each loop iteration, document:

```markdown
## Iteration N

**Query**: What I was looking for
**Found**: X files, Y patterns, Z components
**Relevance**: High/Medium/Low with reasons
**Gaps**: What's still unclear
**Next**: What to explore in next iteration

**Key Files**:
- path/to/file.ts - Core implementation (★★★)
- path/to/other.ts - Supporting utility (★★)

**Mental Model Update**:
- New understanding of X
- Connection between Y and Z
- Pattern: Description
```

## Integration Points

Complements:
- **knowledge-architecture**: For documenting discoveries
- **second-brain-librarian**: For saving exploration notes
- **project-orchestration**: For planning exploration strategy
- **testing-patterns**: For learning through tests

## Tips

- Start wide, then narrow focus
- Document assumptions to validate
- Use tests as documentation
- Follow imports/exports
- Check git history for context
- Look for comments explaining "why"
