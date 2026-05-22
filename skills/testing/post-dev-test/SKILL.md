---
name: post-dev-test
description: Post-development test completion. Analyzes developed features from context, checks integration/e2e test coverage, writes missing tests. Use after feature-dev, before /precommit.
allowed-tools: Read, Grep, Glob, Write, Bash
---

# Post-Dev Test Skill

## Trigger

- Keywords: add tests, integration test, e2e test, test coverage, post dev test

## When to Use

- After completing feature development, before /precommit
- Want to ensure new features have sufficient integration/e2e coverage
- Unit tests exist, but higher-level tests are missing

## Key Rule: Must Execute on Changes

**Even if test coverage looks complete, tests must be executed whenever there are code changes.**

| Scenario                     | Action                               |
| ---------------------------- | ------------------------------------ |
| Code changes exist           | Must execute related integration/e2e |
| Tests exist and are complete | Still execute to confirm no regression |
| Tests missing or insufficient| Write then execute                   |
| Pure doc/comment changes     | Can skip                             |

**Reason**: Test coverage does not equal tests passing. Existing tests may fail due to code changes.

## When NOT to Use

- Only need unit tests (use `/codex-test-gen`)
- Review existing tests (use `/codex-test-review`)
- Still in development (complete `/feature-dev` flow first)

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│ Phase 1: Analyze Context                                        │
├─────────────────────────────────────────────────────────────────┤
│ 1. From conversation history: what feature was developed?       │
│ 2. Identify involved Service / Provider / Controller            │
│ 3. List core flows and API endpoints                            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ Phase 2: Check Existing Test Coverage                           │
├─────────────────────────────────────────────────────────────────┤
│ 1. Search test/integration/ for related tests                   │
│ 2. Search test/e2e/ for related tests                           │
│ 3. Assess coverage gaps                                         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ Phase 3: Determine Test Strategy                                │
├─────────────────────────────────────────────────────────────────┤
│ ┌──────────────┬────────────────────────────────────────────┐   │
│ │ Change Type  │ Test Requirement                           │   │
│ ├──────────────┼────────────────────────────────────────────┤   │
│ │ New API      │ Integration test (Controller + Service)    │   │
│ │ New Service  │ Integration test (Service layer)           │   │
│ │ Cross-svc    │ E2E test (complete flow)                   │   │
│ │ DB operation │ Integration test (actual DB)               │   │
│ │ External API │ Integration test (mock external)           │   │
│ └──────────────┴────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ Phase 4: Write Tests                                            │
├─────────────────────────────────────────────────────────────────┤
│ 1. Reference existing test patterns                             │
│ 2. Use {FRAMEWORK_MOCK_LIB} createApp / createRequester        │
│ 3. Follow TEST_ENV environment variable conventions             │
│ 4. Write to corresponding directory                             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ Phase 5: Execute Verification                                   │
├─────────────────────────────────────────────────────────────────┤
│ 1. Execute newly added tests                                    │
│ 2. Confirm passing                                              │
│ 3. Report results                                               │
└─────────────────────────────────────────────────────────────────┘
```

## Test File Conventions

| Type        | Directory           | Naming                                 | Env Variable           |
| ----------- | ------------------- | -------------------------------------- | ---------------------- |
| Integration | `test/integration/` | `*.integration.test.ts` or `*.test.ts` | `TEST_ENV=integration` |
| E2E         | `test/e2e/`         | `*.e2e.test.ts` or `*.test.ts`         | `TEST_ENV=e2e`         |

## Test Template

```typescript
import { Application, Framework } from '{FRAMEWORK_WEB}';
import { close, createApp } from '{FRAMEWORK_MOCK_LIB}';
import { ITestRequester, createRequester } from '../../createRequester';
import { TestEnvironment, onlyIf } from '../../helper/test-env';

const describeIntegration = onlyIf([
  TestEnvironment.INTEGRATION,
  TestEnvironment.E2E,
]);

describeIntegration('Feature Integration Tests', () => {
  let app: Application;
  let request: ITestRequester;

  beforeAll(async () => {
    app = await createApp<Framework>();
    request = await createRequester(app);
  });

  afterAll(async () => {
    await close(app);
  });

  describe('Scenario: ...', () => {
    it('should ...', async () => {
      // Arrange
      // Act
      // Assert
    });
  });
});
```

## Verification

- [ ] Test files in correct directory
- [ ] Using correct TEST_ENV condition
- [ ] Tests can run independently
- [ ] Covers main flow + error scenarios

## Execute Tests

```bash
# Execute single integration test
TEST_ENV=integration yarn jest test/integration/path/to/test.ts

# Execute single e2e test
TEST_ENV=e2e yarn jest test/e2e/path/to/test.ts
```

## Examples

```
Input: (User Authentication feature developed in conversation)
Phase 1: Identify ActiveAssetsWeeklyService, ActiveAssetsCacheService involved
Phase 2: Search test/e2e/auth/ -> found missing login test
Phase 3: Decide to write E2E test (cross-service flow)
Phase 4: Write active-assets-weekly.e2e.test.ts
Phase 5: Execute test and verify passing
```

```
Input: (New API endpoint developed in conversation)
Phase 1: Identify Controller + Service
Phase 2: Search test/integration/controller/ -> no corresponding test
Phase 3: Decide to write Integration test
Phase 4: Write new-feature.integration.test.ts
Phase 5: Execute test and verify passing
```

## References

- `references/test-patterns.md` - Existing test pattern reference
