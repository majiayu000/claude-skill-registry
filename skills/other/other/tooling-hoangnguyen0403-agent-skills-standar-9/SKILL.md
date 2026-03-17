---
name: TypeScript Tooling
description: Development tools, linting, and build configuration for TypeScript projects.
metadata:
  labels: [tooling, typescript, eslint, prettier, testing]
  triggers:
    files: ['tsconfig.json', '.eslintrc.*', 'jest.config.*', 'package.json']
    keywords: [eslint, prettier, jest, vitest, build, compile, lint]
---

# TypeScript Tooling

## **Priority: P1 (OPERATIONAL)**

Essential tooling for TypeScript development and maintenance.

## Implementation Guidelines

- **Compiler**: `tsc` for CI. `ts-node`/`esbuild` for dev.
- **Lint**: ESLint + `@typescript-eslint`. Strict type checking.
- **Format**: Prettier (on save + commit).
- **Test**: Jest/Vitest > 80% coverage.
- **Build**: `tsup` (libs), Vite/Webpack (apps).
- **Check**: `tsc --noEmit` in CI.

## Anti-Patterns

- **No Disable**: Avoid `// eslint-disable`.
- **No Skip**: Avoid `skipLibCheck: true` if possible.
- **No Ignore**: Use `@ts-expect-error` > `@ts-ignore`.

## ESLint Configuration

### Strict Mode Requirement

**CRITICAL**: Every file in the project, including tests (`.spec.ts`), must adhere to strict type-checked rules. NEVER turn off `@typescript-eslint/no-explicit-any` or `no-unsafe-*` rules.

### Common Linting Issues & Solutions

#### Request Object Typing

**Problem**: Using `any` for Express request objects or creating duplicate inline interfaces.
**Solution**: Use the centralized interfaces in `src/common/interfaces/request.interface.ts`.

```typescript
import { RequestWithUser } from 'src/common/interfaces/request.interface';
```

#### Unused Parameters

**Problem**: Function parameters marked as unused by linter.
**Solution**: Prefix the parameter with an underscore (e.g., `_data`) or remove it. NEVER use `eslint-disable`.

#### Test Mock Typing

**Problem**: Jest mocks triggering unsafe type warnings when `expect.any()` or custom mocks are used.
**Solution**: Cast the mock or expectation using `as unknown as TargetType`.

```typescript
mockRepo.save.mockResolvedValue(result as unknown as User);
```

## Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitReturns": true,
    "noUnusedLocals": true
  }
}
```

## Reference & Examples

For testing configuration and CI/CD setup:
See [references/REFERENCE.md](references/REFERENCE.md).

## Related Topics

best-practices | language
