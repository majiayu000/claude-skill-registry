---
name: plans-yankeeinlondon-adaptive-shell
description: 'This plan addresses two interconnected needs for the ~/.config/sh repository:'
---

# Testing Framework and Planning Skill Enhancement

**Date:** 2025-10-21

**Status:** Planning

## Overview

This plan addresses two interconnected needs for the `~/.config/sh` repository:

1. **Adapt the Planning Skill** - The `.claude/skills/planning/SKILL.md` was ported from a TypeScript project and needs updates to work with this bash scripting repository.

2. **Establish a Testing Framework** - Current tests in `tests/` rely heavily on manual visual inspection rather than boolean assertions. We need a robust, automated testing framework suitable for bash scripts.

## Current State Analysis

### Planning Skill Issues

The current planning skill has these considerations for our bash repo:

- References `pnpm test` and `pnpm test:types` (appropriate since we'll publish to npm)
- Discusses "type tests" which are primarily relevant to TypeScript
- References Vitest testing patterns (actually appropriate for our approach)
- Uses `tests/unit/WIP/` directory structure
- File naming conventions like `*.test.ts`
- TypeScript-specific test examples

### Current Testing Approach

We have three test files with varying quality:

1. **tests/color.sh** - Purely demonstrative, requires manual visual inspection
2. **tests/lists.sh** - Has boolean assertions with pass/fail tracking (good pattern)
3. **tests/file-deps.sh** - Most sophisticated, uses boolean checks and structured output

**Problems:**

- No unified test runner
- No standardized assertion library
- No aggregate pass/fail reporting
- No CI/CD integration capability
- Tests require manual execution and review

## Proposed Testing Framework

### Design Principles

1. **Leverage TypeScript Expertise** - Ken is a TypeScript expert, use Vitest
2. **Boolean Assertions** - All automated tests must have pass/fail checks
3. **Hybrid Approach** - TypeScript tests for automation, bash demos for visual testing
4. **Structured Output** - Support both human-readable and machine-parseable formats
5. **Exit Codes** - Proper exit codes for CI/CD integration
6. **npm Publishing Ready** - Aligned with eventual npm package distribution

### Framework Choice: Vitest

**Rationale:**

- **NPM Publishing** - Repo will likely be published to npm, so pnpm is already required
- **Expert Alignment** - Ken is TypeScript expert, leverage existing expertise
- **Superior Tooling** - Watch mode, UI, coverage reports, parallel execution
- **Bash Testing** - Easy to test bash scripts via `execSync()` from TypeScript
- **Best of Both Worlds** - Keep visual bash demos, add robust automated tests

### Hybrid Architecture

```txt
tests/
├── demos/              # Bash visual demos (manual testing)
│   ├── color-demo.sh   # Interactive color showcase
│   └── showcase.sh     # Feature demonstrations
├── helpers/            # TypeScript test utilities
│   └── bash.ts         # Helpers for testing bash from TS
├── lists.test.ts       # Automated Vitest tests
├── color.test.ts
├── file-deps.test.ts
└── WIP/                # In-progress tests (TDD workflow)
```

## Plan Phases

### Phase 0: Planning Skill Adaptation

**Goals:**

- Update planning skill for bash/TypeScript hybrid context
- Keep Vitest references (they're appropriate!)
- Add bash-specific testing patterns
- Preserve TDD methodology and phase-based approach

**Tasks:**

1. Update `.claude/skills/planning/SKILL.md`:
   - Keep TypeScript/Vitest examples (they're correct for our approach)
   - Add bash-specific testing patterns using bash helper
   - Update to reflect hybrid approach (TypeScript tests + bash source)
   - Clarify when to use demos vs automated tests
   - Keep start-position.ts reference (it works well)

2. Update test file naming conventions:
   - Automated tests: `*.test.ts`
   - Demo scripts: `*-demo.sh` or `showcase-*.sh`

3. Update directory structure recommendations:
   - `tests/` for automated tests
   - `tests/demos/` for visual demonstrations
   - `tests/WIP/` for in-progress work
   - `tests/helpers/` for TypeScript utilities

**Deliverables:**

- Updated `.claude/skills/planning/SKILL.md`
- Keep start-position.ts as-is (it's already TypeScript)

**No TDD Required** - This is documentation work

**Duration:** 1-2 hours

### Phase 1: Vitest Setup & Bash Test Helpers

**Goals:**

- Set up Vitest testing infrastructure
- Create bash helper utilities for testing bash from TypeScript
- Establish test patterns and conventions

**Tasks:**

1. **Package Setup:**
   - Create `package.json` with vitest dependency
   - Create `vitest.config.ts` configuration
   - Create `tsconfig.json` for test files
   - Add test scripts to package.json

2. **Bash Test Helper (`tests/helpers/bash.ts`):**

   ```typescript
   import { execSync } from 'child_process'

   export interface BashOptions {
     env?: Record<string, string>
     cwd?: string
   }

   /**
    * Execute bash script and return stdout
    */
   export function bash(script: string, options?: BashOptions): string {
     return execSync(script, {
       shell: '/bin/bash',
       encoding: 'utf-8',
       cwd: options?.cwd || process.cwd(),
       env: {
         ...process.env,
         ROOT: process.cwd(),
         ...options?.env
       }
     }).trim()
   }

   /**
    * Source a bash file and execute script
    */
   export function sourcedBash(file: string, script: string, options?: BashOptions): string {
     return bash(`source ${file} && ${script}`, options)
   }

   /**
    * Execute bash and return exit code
    */
   export function bashExitCode(script: string, options?: BashOptions): number {
     try {
       bash(script, options)
       return 0
     } catch (error: any) {
       return error.status || 1
     }
   }
   ```

3. **Example Test Pattern Documentation:**

   Create example in `tests/helpers/example.test.ts`:

   ```typescript
   import { describe, it, expect } from 'vitest'
   import { sourcedBash, bashExitCode } from './bash'

   describe('example: testing bash functions', () => {
     it('should test bash function output', () => {
       const result = sourcedBash('./utils/lists.sh', `
         items=("apple" "banana" "cherry")
         retain_prefixes_ref items "a" "b"
       `)

       expect(result).toContain('apple')
       expect(result).toContain('banana')
       expect(result).not.toContain('cherry')
     })

     it('should test bash function exit codes', () => {
       const exitCode = bashExitCode(`
         source ./utils/lists.sh
         items=("apple" "banana")
         list_contains_ref items "banana"
       `)

       expect(exitCode).toBe(0)
     })
   })
   ```

**TDD Approach:**

1. Create `tests/WIP/bash-helper.test.ts` to test the bash helper itself
2. Write tests for basic bash execution
3. Implement bash helper to pass tests
4. Write tests for sourced bash execution
5. Implement sourcedBash to pass tests
6. Move from WIP to `tests/helpers/bash.test.ts`

**Deliverables:**

- `package.json` with vitest and scripts
- `vitest.config.ts`
- `tsconfig.json`
- `tests/helpers/bash.ts`
- `tests/helpers/bash.test.ts` (tests for the helper)
- `tests/helpers/example.test.ts` (documentation example)

**Duration:** 2-3 hours

### Phase 2: Migrate Existing Tests to Vitest

**Goals:**

- Convert existing test files to Vitest
- Separate visual demos from automated tests
- Establish patterns for the rest of the codebase

**Tasks:**

1. **Migrate tests/lists.sh → tests/lists.test.ts:**
   - Convert all 8 tests to Vitest format
   - Use `sourcedBash()` helper
   - Keep all existing test logic and assertions
   - Remove manual pass/fail tracking (Vitest handles this)

2. **Migrate tests/file-deps.sh → tests/file-deps.test.ts:**
   - Keep JSON validation approach
   - Use Vitest's `expect().toMatchObject()` for JSON
   - Test both console and JSON output formats
   - Add tests for edge cases (empty dependencies, etc.)

3. **Convert tests/color.sh:**
   - Move to `tests/demos/color-demo.sh` (keep as visual demo)
   - Create `tests/color.test.ts` for automated tests:
     - Test `colorize()` function output structure
     - Test `rgb_text()` with known RGB values
     - Test color shortcut functions return non-empty strings
     - Test color variables are set correctly by `setup_colors()`

**TDD Approach:**

For each test file:

1. Create new test in `tests/WIP/MODULE.test.ts`
2. Write tests using Vitest and bash helper
3. Verify tests pass against existing functionality
4. If tests fail, determine if bug in source or test
5. Remove old bash test file (or move to demos/)
6. Move new test from WIP to `tests/`

**Deliverables:**

- `tests/lists.test.ts`
- `tests/file-deps.test.ts`
- `tests/color.test.ts`
- `tests/demos/color-demo.sh` (visual demo)

**Duration:** 2-3 hours

### Phase 3: Core Utilities Test Coverage

**Goals:**

- Add comprehensive test coverage for critical utility functions
- Focus on most-used functions first
- Aim for 80%+ coverage of exported functions
- Fix any bugs discovered during testing

**Priority Functions to Test:**

From `utils/` directory:

1. **utils/text.sh** - String manipulation functions (trim, uppercase, lowercase, etc.)
2. **utils/typeof.sh** - Type checking utilities (is_function, is_number, etc.)
3. **utils/filesystem.sh** - File operations (file_exists, dir_exists, etc.)
4. **utils/empty.sh** - Empty/null checking (is_empty, not_empty, etc.)
5. **utils/detection.sh** - System detection (get_os, get_shell, etc.)
6. **utils/errors.sh** - Error handling (panic, error, warn, etc.)

**TDD Approach:**

For each utility module:

1. Create `tests/WIP/MODULE.test.ts`
2. List all exported functions in the module
3. Write tests for each function:
   - Happy path (normal usage)
   - Edge cases (empty strings, null, undefined, boundaries)
   - Error cases (invalid input)
4. Run tests - many will fail initially (discovering bugs or behavior issues)
5. Fix bugs in source code OR clarify test expectations
6. Ensure all tests pass
7. Migrate test from WIP to `tests/MODULE.test.ts`

**Example Test Structure:**

```typescript
import { describe, it, expect } from 'vitest'
import { sourcedBash, bashExitCode } from './helpers/bash'

describe('text utilities', () => {
  describe('trim()', () => {
    it('should remove leading and trailing whitespace', () => {
      const result = sourcedBash('./utils/text.sh', `
        trim "  hello world  "
      `)
      expect(result).toBe('hello world')
    })

    it('should handle empty string', () => {
      const result = sourcedBash('./utils/text.sh', `trim ""`)
      expect(result).toBe('')
    })

    it('should handle string with only whitespace', () => {
      const result = sourcedBash('./utils/text.sh', `trim "   "`)
      expect(result).toBe('')
    })
  })

  describe('uppercase()', () => {
    it('should convert string to uppercase', () => {
      const result = sourcedBash('./utils/text.sh', `uppercase "hello"`)
      expect(result).toBe('HELLO')
    })

    it('should handle mixed case', () => {
      const result = sourcedBash('./utils/text.sh', `uppercase "HeLLo"`)
      expect(result).toBe('HELLO')
    })
  })
})
```

**Deliverables:**

- `tests/text.test.ts`
- `tests/typeof.test.ts`
- `tests/filesystem.test.ts`
- `tests/empty.test.ts`
- `tests/detection.test.ts`
- `tests/errors.test.ts`
- Bug fixes discovered during testing
- Documentation updates if function behavior is clarified

**Duration:** 4-6 hours

### Phase 4: Documentation and CI Integration

**Goals:**

- Document testing conventions and best practices
- Add CI/CD integration with GitHub Actions
- Create testing guidelines for contributors
- Set up useful npm scripts

**Tasks:**

1. **Create `tests/README.md`:**
   - How to run tests (`pnpm test`)
   - How to write tests using bash helper
   - Vitest commands reference:
     - `pnpm test` - run all tests once
     - `pnpm test:watch` - run in watch mode
     - `pnpm test:ui` - open Vitest UI
     - `pnpm test:coverage` - generate coverage report
   - Test writing patterns and examples
   - When to use demos vs automated tests
   - Best practices for testing bash from TypeScript

2. **Update `CLAUDE.md`:**
   - Add comprehensive testing section
   - Link to tests/README.md
   - Document TDD expectations
   - Include example of testing bash functions
   - Explain hybrid approach (demos + automated tests)

3. **Package.json scripts:**

   ```json
   {
     "scripts": {
       "test": "vitest run",
       "test:watch": "vitest",
       "test:ui": "vitest --ui",
       "test:coverage": "vitest run --coverage"
     },
     "devDependencies": {
       "vitest": "^latest",
       "@vitest/ui": "^latest",
       "@vitest/coverage-v8": "^latest",
       "typescript": "^latest"
     }
   }
   ```

4. **Create `.github/workflows/test.yml`:**

   ```yaml
   name: Tests

   on:
     push:
       branches: [ main ]
     pull_request:
       branches: [ main ]

   jobs:
     test:
       runs-on: ubuntu-latest

       steps:
         - uses: actions/checkout@v3

         - uses: pnpm/action-setup@v2
           with:
             version: 8

         - uses: actions/setup-node@v3
           with:
             node-version: '20'
             cache: 'pnpm'

         - run: pnpm install

         - run: pnpm test
   ```

5. **Add pre-commit hook example (`.git/hooks/pre-commit.example`):**

   ```bash
   #!/bin/bash
   # Run tests before committing
   pnpm test || exit 1
   ```

**Deliverables:**

- `tests/README.md`
- Updated `CLAUDE.md`
- Updated `package.json` with scripts
- `.github/workflows/test.yml`
- `.git/hooks/pre-commit.example`

**Duration:** 1-2 hours

## Testing Standards

### Test File Conventions

- **Automated tests:** `*.test.ts` in `tests/` directory
- **Demo scripts:** `*-demo.sh` or `showcase-*.sh` in `tests/demos/`
- **Helper utilities:** `*.ts` in `tests/helpers/`
- **Work in progress:** Use `tests/WIP/` during development

### Test Organization

```txt
tests/
├── demos/                 # Visual demonstration scripts
│   ├── color-demo.sh     # Interactive color showcase
│   └── showcase.sh       # General feature demonstrations
├── helpers/              # TypeScript test utilities
│   ├── bash.ts          # Bash execution helpers
│   ├── bash.test.ts     # Tests for bash helper
│   └── example.test.ts  # Example/documentation
├── WIP/                  # Work in progress (during TDD)
├── *.test.ts            # Automated test files
└── README.md            # Testing documentation
```

### Writing Tests

**Principles:**

1. **One behavior per test** - Each `it()` block tests a single thing
2. **Descriptive names** - Test names should explain what's being verified
3. **Arrange-Act-Assert** - Clear setup, execution, and verification
4. **Independence** - Tests should not depend on each other
5. **Cleanup** - Clean up any temporary files/state (use `beforeEach`/`afterEach`)

**Example Pattern:**

```typescript
import { describe, it, expect } from 'vitest'
import { sourcedBash } from './helpers/bash'

describe('function_name', () => {
  it('should handle empty input gracefully', () => {
    // Arrange
    const input = ""

    // Act
    const result = sourcedBash('./utils/module.sh', `
      function_name "${input}"
    `)

    // Assert
    expect(result).toBe('default_value')
  })

  it('should process normal input correctly', () => {
    const result = sourcedBash('./utils/module.sh', `
      function_name "test input"
    `)

    expect(result).toContain('test input')
  })
})
```

### Running Tests

```bash
# Install dependencies (first time)
pnpm install

# Run all tests
pnpm test

# Run tests in watch mode (auto-rerun on file changes)
pnpm test:watch

# Run tests with UI
pnpm test:ui

# Run tests with coverage report
pnpm test:coverage

# Run specific test file
pnpm test lists

# Run tests matching pattern
pnpm test --grep "retain_prefixes"
```

### When to Use Demos vs Automated Tests

**Use Demo Scripts (`tests/demos/`) when:**

- Visual inspection is required (e.g., color output)
- Interactive demonstration of features
- Showcasing functionality to users
- Manual testing during development

**Use Automated Tests (`tests/*.test.ts`) when:**

- Boolean pass/fail verification is possible
- Testing function behavior and logic
- CI/CD integration needed
- Regression testing required

## Open Questions

1. **Should we keep start-position.ts or rewrite in bash?**
   - **Decision:** Keep TypeScript - it works well and we're using TypeScript for tests anyway

2. **Should tests be in `tests/` or co-located with source?**
   - **Decision:** Keep centralized in `tests/` - cleaner separation for bash source files

3. **Do we need a WIP directory?**
   - **Decision:** Yes, essential for TDD workflow without breaking main test suite

4. **Coverage threshold?**
   - **Recommendation:** Start with 80% for core utils, can adjust based on what makes sense

## Success Criteria

### Phase 0 (Planning Skill)

- [ ] Planning skill updated for bash/TypeScript hybrid approach
- [ ] TypeScript/Vitest references kept and clarified
- [ ] Bash-specific testing patterns added
- [ ] Demo vs automated test guidance provided

### Phase 1 (Vitest Setup)

- [ ] package.json created with vitest dependencies
- [ ] vitest.config.ts and tsconfig.json configured
- [ ] Bash helper implemented and tested
- [ ] Example tests created as documentation
- [ ] All tests pass

### Phase 2 (Existing Tests)

- [ ] lists.test.ts migrated with all tests passing
- [ ] file-deps.test.ts migrated with all tests passing
- [ ] color.test.ts created for automated tests
- [ ] color-demo.sh moved to demos/ directory
- [ ] All tests passing, zero regressions

### Phase 3 (Coverage)

- [ ] Tests exist for 6 core utility modules
- [ ] Each exported function has at least one test
- [ ] 80%+ coverage of critical functions
- [ ] Any discovered bugs fixed
- [ ] All tests passing

### Phase 4 (Documentation)

- [ ] tests/README.md comprehensive and clear
- [ ] CLAUDE.md includes testing guidance
- [ ] GitHub Actions workflow functional
- [ ] Pre-commit hook example provided
- [ ] All npm scripts working correctly

## Timeline Estimate

- **Phase 0:** 1-2 hours (documentation)
- **Phase 1:** 2-3 hours (Vitest setup and bash helper)
- **Phase 2:** 2-3 hours (migrate existing tests)
- **Phase 3:** 4-6 hours (new test coverage)
- **Phase 4:** 1-2 hours (documentation and CI)

**Total:** 10-16 hours of focused work

## Next Steps

After approval of this plan:

1. Begin Phase 0 - Update planning skill documentation
2. Execute Phase 1 - Set up Vitest and create bash helper (with TDD)
3. Checkpoint after Phase 1 to review test patterns
4. Execute Phase 2 - Migrate existing tests
5. Execute Phase 3 - Add coverage for core utilities
6. Execute Phase 4 - Documentation and CI integration

## Benefits of This Approach

1. **Leverages Expertise** - Uses TypeScript, which Ken knows well
2. **NPM Ready** - Aligns with npm publishing plans
3. **Superior DX** - Watch mode, UI, coverage built-in
4. **Best of Both** - Visual demos + robust automation
5. **CI/CD Ready** - Proper exit codes, JSON output, GitHub Actions
6. **Maintainable** - Industry-standard tooling, familiar to contributors
