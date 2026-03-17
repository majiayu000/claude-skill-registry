---
name: validate-sdk
description: Validates TypeScript SDK code (build, types, lint, tests) in the sdk/ directory
user-invocable: true
---

# Validate SDK Skill

**CLAUDE: When this skill is invoked with `/validate-sdk`, run these commands in sequence:**
```bash
cd sdk && bun run build && bun run type-check && bun run lint && bun run test
```

## Purpose
Validates the TypeScript MCP client SDK for build integrity, type safety, lint compliance, and test correctness.

## Usage
```bash
/validate-sdk
```

## What It Validates

### Build Verification
```bash
cd sdk && bun run build
```
- Compiles TypeScript via esbuild
- Generates `dist/` output
- Validates module exports

### TypeScript Check
```bash
cd sdk && bun run type-check
```
- Validates type definitions
- Ensures generated types are valid
- Checks MCP protocol types

### ESLint
```bash
cd sdk && bun run lint
```
- Code style consistency
- TypeScript best practices
- Import validation

### Tests
```bash
cd sdk && bun run test
```
- Unit tests for SDK components
- Integration tests with server
- E2E protocol compliance

## Full Validation Command
```bash
cd sdk && bun run build && bun run type-check && bun run lint && bun run test
```

## Additional Commands

### Specific Test Categories
```bash
cd sdk && bun run test:unit           # Unit tests only
cd sdk && bun run test:integration    # Integration tests
cd sdk && bun run test:e2e            # End-to-end tests
cd sdk && bun run test:all            # All test categories
```

### Type Generation
```bash
cd sdk && bun run generate-types
```
Regenerates TypeScript types from Rust tool schemas.

### MCP Inspector
```bash
cd sdk && bun run inspect
```
Interactive debugging with MCP inspector.

## Success Criteria
- Build completes without errors
- All TypeScript types valid
- Zero ESLint violations
- All tests pass
- Generated types match Rust definitions

## Related Skills
- `generate-sdk-types` - Regenerate TypeScript types from Rust
- `test-mcp-compliance` - MCP protocol validation
