---
name: vitest-runner
description: Execute JavaScript/TypeScript tests with Vitest, supporting coverage, watch mode, and parallel execution. Use for JS/TS test automation.
tools: Read, Write, Bash
---

# Vitest Runner Skill

## Purpose

Single responsibility: Execute and manage Vitest test suites with proper configuration, coverage reporting, and failure analysis. (BP-4)

## Grounding Checkpoint (Archetype 1 Mitigation)

Before executing, VERIFY:

- [ ] Node.js installed and version appropriate
- [ ] package.json exists with vitest dependency
- [ ] Test files exist (*.test.ts, *.spec.ts)
- [ ] vitest.config.ts or vite.config.ts present (optional)

**DO NOT run tests without verifying node_modules installed.**

## Uncertainty Escalation (Archetype 2 Mitigation)

ASK USER instead of guessing when:

- Multiple test configurations detected
- Coverage threshold unclear
- Watch mode vs single run
- Specific test patterns needed

**NEVER modify test configurations without user approval.**

## Context Scope (Archetype 3 Mitigation)

| Context Type | Included | Excluded |
|--------------|----------|----------|
| RELEVANT | Test files, vitest config, package.json | Application logic |
| PERIPHERAL | Coverage reports, test utilities | Build configs |
| DISTRACTOR | Deployment configs | Other frameworks |

## Workflow Steps

### Step 1: Environment Check (Grounding)

```bash
# Verify Node.js
node --version
npm --version

# Check vitest installed
npx vitest --version || npm install -D vitest

# List test files
find . -name "*.test.ts" -o -name "*.spec.ts" | grep -v node_modules | head -20
```

### Step 2: Discover Tests

```bash
# Show test collection
npx vitest --run --reporter=verbose --passWithNoTests 2>&1 | head -50

# List test files
npx vitest list
```

### Step 3: Execute Tests

**Basic execution:**
```bash
npx vitest run
```

**With coverage:**
```bash
npx vitest run --coverage
```

**Specific file or pattern:**
```bash
npx vitest run src/utils.test.ts
npx vitest run --grep "authentication"
```

**Watch mode:**
```bash
npx vitest --watch
```

**Parallel execution:**
```bash
npx vitest run --pool threads --poolOptions.threads.maxThreads 4
```

### Step 4: Analyze Results

```bash
# Verbose output with failures
npx vitest run --reporter=verbose 2>&1 | tee test_results.txt

# Extract failures
grep -E "^FAIL|AssertionError|Error:" test_results.txt

# Coverage summary
npx vitest run --coverage --coverage.reporter=text-summary
```

## Recovery Protocol (Archetype 4 Mitigation)

On error:

1. **PAUSE** - Capture test output
2. **DIAGNOSE** - Check error type:
   - `Cannot find module` → Check imports, tsconfig paths
   - `SyntaxError` → Check TypeScript compilation
   - `Timeout` → Increase timeout or check async handling
   - `ENOENT` → Check file paths, fixtures
3. **ADAPT** - Adjust test selection or configuration
4. **RETRY** - With narrower scope (max 3 attempts)
5. **ESCALATE** - Report failures with context

## Checkpoint Support

State saved to: `.aiwg/working/checkpoints/vitest-runner/`

```
checkpoints/vitest-runner/
├── test_collection.json     # Discovered tests
├── test_results.json        # Last run results
├── coverage_report.json     # Coverage data
└── failure_analysis.md      # Failure diagnostics
```

## Common Vitest Options

| Option | Purpose |
|--------|---------|
| `--run` | Single run (no watch) |
| `--watch` | Watch mode |
| `--coverage` | Generate coverage |
| `--reporter=verbose` | Detailed output |
| `--grep "pattern"` | Filter tests |
| `--bail` | Stop on first failure |
| `--update` | Update snapshots |
| `--ui` | Open UI |

## Configuration Templates

**vitest.config.ts:**
```typescript
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    include: ['**/*.{test,spec}.{js,ts}'],
    exclude: ['node_modules', 'dist'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'json'],
      exclude: ['node_modules/', 'test/']
    },
    globals: true,
    environment: 'node'
  }
})
```

## References

- Vitest documentation: https://vitest.dev/
- REF-001: Production-Grade Agentic Workflows (BP-4 single responsibility)
- REF-002: LLM Failure Modes (Archetype 1 grounding)
