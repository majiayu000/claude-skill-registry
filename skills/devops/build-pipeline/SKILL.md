---
name: build-pipeline
description: Execute complete build pipeline with dead code detection, formatting, linting, type checking, testing, and production build. Use when the user mentions building, running the full pipeline, checking code quality, or preparing for deployment. Auto-triggers on phrases like "build the project", "run all checks", "prepare for production", or "validate code quality".
allowed-tools: Bash(bun*)
---

# Project Build Pipeline

Execute a comprehensive build pipeline with fail-fast behavior for the Tetris project.

## Pipeline Steps (6 stages)

1. **Dead Code Detection** (`bun run knip`) - Identify unused code, exports, and dependencies
2. **Code Formatting** (`bun run format`) - Apply consistent code style via Biome
3. **Linting** (`bun run lint`) - Perform code quality checks and import optimization
4. **Type Checking** (`bun run typecheck`) - Validate TypeScript type safety
5. **Testing** (`bun test`) - Execute all test suites (160+ tests)
6. **Production Build** (`bun run build`) - Create optimized production bundle

## Execution

```bash
# Execute full pipeline with fail-fast behavior
bun run knip && \
bun run format && \
bun run lint && \
bun run typecheck && \
bun test && \
bun run build
```

The pipeline uses `&&` operator to ensure immediate termination upon any step failure.

## Pipeline Rationale

1. **knip (first)**: Detect unused code early to reduce processing time
2. **format (second)**: Ensure consistent code style before quality checks
3. **lint (third)**: Check code quality on properly formatted code
4. **typecheck (fourth)**: Verify type safety after code structure validation
5. **test (fifth)**: Confirm functionality with comprehensive test suite
6. **build (last)**: Generate production bundle only when all gates pass

## When This Skill Activates

- "Build the project"
- "Run all checks"
- "Prepare for production"
- "Validate code quality"
- "Execute the full pipeline"
- "Check if everything is ready to deploy"
