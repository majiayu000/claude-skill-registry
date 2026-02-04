---
name: self-validating-example
description: Example skill demonstrating self-validating REST API generation with automatic test execution. Use as a template for creating skills with pre-tool-use validation hooks. Validates Node.js environment and dependencies before generating endpoints.
user-invocable: false
hooks:
  pre_tool_use:
    - validate: file_exists
      path: package.json
      error: "Must be in a Node.js project"
    - validate: dependency
      package: express
      error: "Express must be installed: npm install express"
  post_tool_use:
    - validate: tests_pass
      command: npm test -- --testPathPattern="$OUTPUT"
      max_retries: 3
    - validate: lint
      command: npm run lint -- $OUTPUT
      auto_fix: true
    - validate: types
      command: npx tsc --noEmit $OUTPUT
---

# Self-Validating API Endpoint Generator

You are generating a REST API endpoint with **automatic validation**.

## How Self-Validation Works

```
┌──────────────────────────────────────────────────────────────┐
│  YOUR CODE WILL BE AUTOMATICALLY VALIDATED                   │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. PRE-CHECK: Verify project has Express installed          │
│                                                              │
│  2. GENERATE: You create the endpoint + tests                │
│                                                              │
│  3. VALIDATE (automatic):                                    │
│     ├─ npm test → Must pass                                  │
│     ├─ npm run lint → Auto-fixed if needed                   │
│     └─ tsc --noEmit → Must type-check                        │
│                                                              │
│  4. If validation fails:                                     │
│     └─ You get feedback and retry (max 3 times)              │
│                                                              │
│  5. If still failing after 3 attempts:                       │
│     └─ Pause for human review                                │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Required Outputs

### 1. API Endpoint (`src/routes/[name].ts`)

```typescript
import { Router, Request, Response } from 'express';

const router = Router();

// GET /api/[name]
router.get('/', async (req: Request, res: Response) => {
  // Implementation
});

// POST /api/[name]
router.post('/', async (req: Request, res: Response) => {
  // Implementation with validation
});

export default router;
```

### 2. Test File (`src/routes/[name].test.ts`) - REQUIRED!

```typescript
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import request from 'supertest';
import app from '../app';

describe('[Name] API', () => {
  describe('GET /api/[name]', () => {
    it('should return 200 with data', async () => {
      const res = await request(app).get('/api/[name]');
      expect(res.status).toBe(200);
      expect(res.body).toBeDefined();
    });
  });

  describe('POST /api/[name]', () => {
    it('should create resource with valid data', async () => {
      const res = await request(app)
        .post('/api/[name]')
        .send({ /* valid data */ });
      expect(res.status).toBe(201);
    });

    it('should return 400 for invalid data', async () => {
      const res = await request(app)
        .post('/api/[name]')
        .send({ /* invalid data */ });
      expect(res.status).toBe(400);
    });
  });
});
```

## Validation Criteria

| Check | Command | Required |
|-------|---------|----------|
| Tests pass | `npm test -- --testPathPattern="$OUTPUT"` | ✅ Yes |
| Lint clean | `npm run lint -- $OUTPUT` | ✅ Yes (auto-fix) |
| Types valid | `npx tsc --noEmit $OUTPUT` | ✅ Yes |

## Self-Healing Behavior

If tests fail, you will receive:
1. The test output showing which tests failed
2. A request to fix the failing tests
3. Another attempt (up to 3 total)

**Example failure feedback:**
```
🔴 VALIDATION FAILED (attempt 1/3)

Test Results:
  ✗ GET /api/users should return 200 with data
    Expected: 200
    Received: 404

Please fix the route handler and regenerate.
```

## Important Notes

1. **Always generate tests** - The skill will NOT complete without passing tests
2. **Use proper types** - TypeScript errors block completion
3. **Follow lint rules** - Auto-fixed but avoid common issues
4. **Handle edge cases** - Test both success and error paths

## Project-Specific Learnings

**Before starting work, check for project-specific learnings:**

```bash
# Check if skill memory exists for this skill
cat .specweave/skill-memories/self-validating-example.md 2>/dev/null || echo "No project learnings yet"
```

Project learnings are automatically captured by the reflection system when corrections or patterns are identified during development. These learnings help you understand project-specific conventions and past decisions.

