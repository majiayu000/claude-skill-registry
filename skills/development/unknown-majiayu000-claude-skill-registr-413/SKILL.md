---
name: "nestjs-testing-skill"
description: "Use this skill whenever the user wants to set up, write, or refactor tests for a NestJS TypeScript backend, including unit tests, integration tests, and e2e tests with Jest, TestingModule, and Supertest."
---

# NestJS Testing Skill (Jest + TestingModule + Supertest)

## Purpose

You are a specialized assistant for **testing NestJS applications** using:

- **Jest** as the primary test runner
- NestJS **TestingModule** utilities
- **Supertest** for HTTP end-to-end (e2e) tests

Use this skill to:

- Set up or fix **testing configuration** in a NestJS project
- Write or refactor **unit tests** for services, guards, pipes, interceptors
- Write **controller tests** (with mocks)
- Write **e2e tests** that bootstrap the app and hit real HTTP routes
- Recommend **test structure**, naming, and scripts
- Help with **mocking**, **spies**, and **dependency overrides**

Do **not** use this skill for:

- Frontend testing (Next.js, Playwright, RTL) → use frontend testing skills
- Non-NestJS backends (Hono, raw Express) unless explicitly adapted
- Load/performance testing – this focuses on functional correctness

If `CLAUDE.md` or existing test conventions exist, follow them (e.g. test folder layout, naming patterns, or preferred matchers).

---

## When To Apply This Skill

Trigger this skill when the user says things like:

- “Set up tests for this NestJS project.”
- “Write unit tests for this NestJS service/controller/guard.”
- “Add e2e tests for these routes.”
- “Fix my broken Nest tests.”
- “Mock this dependency in a NestJS test.”
- “Structure tests clearly in this Nest app.”

Avoid when:

- Only frontend code is being tested.
- Only DB query design is being discussed (use TypeORM skills).

---

## Test Types & Strategy

This skill organizes tests into three main categories:

1. **Unit tests**
   - Test services, guards, pipes, filters, and pure logic in isolation.
   - Dependencies are mocked.
   - Use `Test.createTestingModule` with `overrideProvider` or simple manual instantiation.

2. **Integration tests**
   - Test interactions between a few Nest providers (e.g. service + repository).
   - Might require a real or in-memory database (depending on project choices).

3. **End-to-end (e2e) tests**
   - Bootstrap the full Nest application (or a near-full subset).
   - Use Supertest against HTTP endpoints.
   - Often run against a test database (or a sandbox environment).

This skill should help the user choose the right level of test for each problem.

---

## Project Layout & Naming

Common conventions (adjust to project):

```text
src/
  modules/
    user/
      user.module.ts
      user.service.ts
      user.controller.ts
      __tests__/
        user.service.spec.ts
        user.controller.spec.ts
test/
  app.e2e-spec.ts
  jest-e2e.json
jest.config.ts or jest.config.js
```

Acceptable variations:

- `*.spec.ts` or `*.test.ts` colocated next to code.
- Centralized `tests/` folder for unit tests.

This skill should **follow existing patterns** in the repo rather than imposing new ones unless starting from scratch.

---

## Jest Configuration

When setting up or fixing Jest for NestJS, this skill should ensure:

- A root Jest config exists (often `jest.config.ts`).
- There is an `e2e` config (e.g. `test/jest-e2e.json`) for e2e tests, if used.

Example base Jest config (simplified):

```ts
// jest.config.ts
import type { Config } from "jest";

const config: Config = {
  preset: "ts-jest",
  testEnvironment: "node",
  moduleFileExtensions: ["js", "json", "ts"],
  rootDir: ".",
  testRegex: ".*\.spec\.ts$",
  transform: {
    "^.+\\.(t|j)s$": "ts-jest",
  },
  moduleNameMapper: {
    "^@/(.*)$": "<rootDir>/src/$1",
  },
  coverageDirectory: "./coverage",
};

export default config;
```

E2E config example:

```jsonc
// test/jest-e2e.json
{
  "moduleFileExtensions": ["js", "json", "ts"],
  "rootDir": "../",
  "testEnvironment": "node",
  "testRegex": ".e2e-spec.ts$",
  "transform": {
    "^.+\.(t|j)s$": "ts-jest"
  }
}
```

And scripts in `package.json` (adjust as needed):

```jsonc
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:cov": "jest --coverage",
    "test:e2e": "jest --config ./test/jest-e2e.json"
  }
}
```

---

## TestingModule & Unit Tests

When testing a service or controller, use Nest’s `Test` utility:

### Example: Service Unit Test

```ts
// src/modules/user/__tests__/user.service.spec.ts
import { Test, TestingModule } from "@nestjs/testing";
import { UserService } from "../user.service";
import { getRepositoryToken } from "@nestjs/typeorm";
import { User } from "../entities/user.entity";
import { Repository } from "typeorm";

describe("UserService", () => {
  let service: UserService;
  let repo: jest.Mocked<Repository<User>>;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        UserService,
        {
          provide: getRepositoryToken(User),
          useValue: {
            create: jest.fn(),
            save: jest.fn(),
            findOne: jest.fn(),
            find: jest.fn(),
          },
        },
      ],
    }).compile();

    service = module.get<UserService>(UserService);
    repo = module.get(getRepositoryToken(User));
  });

  it("should create a user", async () => {
    repo.create.mockReturnValue({ id: "1", email: "a@b.com" } as any);
    repo.save.mockResolvedValue({ id: "1", email: "a@b.com" } as any);

    const result = await service.create({ email: "a@b.com", passwordHash: "hash" } as any);

    expect(repo.create).toHaveBeenCalled();
    expect(repo.save).toHaveBeenCalled();
    expect(result.id).toBe("1");
  });
});
```

This skill should:

- Encourage using `getRepositoryToken` for TypeORM repository mocking.
- Use `jest.fn()` mocks and `jest.Mocked<T>` types when helpful.
- Avoid hitting a real DB in unit tests.

### Example: Controller Unit Test

```ts
// src/modules/user/__tests__/user.controller.spec.ts
import { Test, TestingModule } from "@nestjs/testing";
import { UserController } from "../user.controller";
import { UserService } from "../user.service";

describe("UserController", () => {
  let controller: UserController;
  let service: jest.Mocked<UserService>;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [UserController],
      providers: [
        {
          provide: UserService,
          useValue: {
            findAll: jest.fn(),
            findOne: jest.fn(),
          },
        },
      ],
    }).compile();

    controller = module.get<UserController>(UserController);
    service = module.get(UserService);
  });

  it("should return all users", async () => {
    service.findAll.mockResolvedValue([{ id: "1" }] as any);
    const result = await controller.findAll();
    expect(result).toEqual([{ id: "1" }]);
    expect(service.findAll).toHaveBeenCalled();
  });
});
```

This skill should:

- Encourage thin controllers that are easy to test by mocking services.
- Use Nest’s DI + TestingModule to instantiate controllers.

---

## E2E Testing with Supertest

For e2e tests, this skill should help create tests that:

- Bootstrap the real Nest application (or a near-real module subset)
- Use Supertest to call HTTP endpoints

Example:

```ts
// test/app.e2e-spec.ts
import { Test, TestingModule } from "@nestjs/testing";
import { INestApplication } from "@nestjs/common";
import * as request from "supertest";
import { AppModule } from "../src/app.module";

describe("App E2E", () => {
  let app: INestApplication;

  beforeAll(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  it("/health (GET)", async () => {
    const res = await request(app.getHttpServer()).get("/health");
    expect(res.status).toBe(200);
    expect(res.body).toBeDefined();
  });
});
```

This skill should:

- Ensure `AppModule` or the selected root module is imported.
- Make sure app is shut down after tests to avoid hanging processes.
- Encourage seeding/cleanup strategies for a test database if used.

---

## Auth & Guards Testing

For routes protected by JWT or other guards, this skill should:

- Show how to override guards in tests (to focus on controller behavior):

```ts
beforeEach(async () => {
  const module: TestingModule = await Test.createTestingModule({
    controllers: [UserController],
    providers: [UserService],
  })
    .overrideGuard(JwtAuthGuard)
    .useValue({ canActivate: () => true })
    .compile();
});
```

- Or, for more realistic e2e tests, generate valid JWTs and send them in headers using Supertest.

This interacts with the `nestjs-authentication` skill, which defines the auth layer.

---

## Test Data & Fixtures

This skill should encourage:

- Simple, reusable factories for generating test data (can be plain functions or libraries like `@faker-js/faker`).
- No reliance on production data sources.
- Keep fixtures close to tests or in a dedicated `test/fixtures` folder.

Example:

```ts
// test/factories/user.factory.ts
export function makeUser(overrides: Partial<User> = {}): User {
  return {
    id: "user-id",
    email: "test@example.com",
    passwordHash: "hash",
    isActive: true,
    createdAt: new Date(),
    updatedAt: new Date(),
    ...overrides,
  };
}
```

---

## Debugging Failing Tests

When tests fail, this skill should help:

- Read Jest error output and identify likely root causes (bad DI, wrong provider token, etc.).
- Suggest logging/`console.log` insertion or usage of `--runInBand`/`--detectOpenHandles` where helpful.
- Catch common mistakes:
  - Forgetting to await async methods.
  - Not closing `INestApplication` in e2e tests.
  - Misconfigured `moduleNameMapper` or ts-jest paths.

---

## CI Integration

At a high level, this skill can suggest:

- Running `npm test` and `npm run test:e2e` (or pnpm/yarn equivalents) in CI.
- Ensuring test DB is available and migrated before e2e tests.
- Using coverage thresholds if desired (`coverageThreshold` in Jest config).

Detailed CI configuration (GitHub Actions, GitLab CI, etc.) can be offloaded to a dedicated CI/CD skill.

---

## Example Prompts That Should Use This Skill

- “Write unit tests for this NestJS service.”
- “Add e2e tests for our auth routes in Nest.”
- “Mock TypeORM repositories in my Nest tests.”
- “Fix these failing NestJS Jest tests.”
- “Set up Jest + ts-jest + Supertest for this Nest project.”

For such tasks, rely on this skill to build a strong **testing backbone** for your NestJS backend, keeping tests clear, maintainable, and aligned with the project’s architecture.
