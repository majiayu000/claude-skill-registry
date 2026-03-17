---
name: Naming & Folder Conventions
description: Conventions for naming files, folders, variables, functions, types, tests, and configs to keep a codebase predictable, searchable, and consistent
---

# Naming & Folder Conventions

## Overview

มาตรฐาน naming conventions สำหรับ files, folders, variables, และ functions ที่ทำให้ codebase predictable และ searchable ลดเวลาในการหา และลดความสับสน

## Why This Matters

- **Predictability**: Guess ได้ว่าไฟล์ชื่ออะไร อยู่ไหน
- **Searchability**: Find/grep ได้ง่าย
- **Consistency**: ทุกคนใช้ pattern เดียวกัน
- **Maintainability**: เข้าใจ code จาก naming

---

## Core Concepts

### 1. File Naming

- ใช้ casing ตามชนิดไฟล์: `PascalCase.tsx` (components), `camelCase.ts` (utilities), `kebab-case.ts` (scripts/configs)
- suffix ที่สื่อบทบาท: `*.service.ts`, `*.controller.ts`, `*.repository.ts`, `*.middleware.ts`, `*.dto.ts`, `*.types.ts`
- หลีกเลี่ยงชื่อกว้าง: `helpers.ts`, `utils.ts`, `data.ts` (แยกให้เฉพาะเจาะจง)

### 2. Folder Naming

- โฟลเดอร์ระดับ “feature/entity” ใช้ plural เช่น `users/`, `orders/`
- โฟลเดอร์ “cross-cutting collections” ใช้ plural เช่น `utils/`, `types/`, `constants/`
- จำกัดความลึก (เช่นไม่เกิน 4 levels) และห้ามตั้ง `misc/`, `stuff/`

### 3. Variable Naming

- `camelCase` สำหรับตัวแปรทั่วไป, `SCREAMING_SNAKE_CASE` สำหรับ constants
- boolean ใช้ prefix: `is/has/can/should`
- หลีกเลี่ยงตัวย่อที่ไม่เป็นมาตรฐาน; ชื่อควรสื่อ domain (`billingCycle`, `invoiceId`)

### 4. Function Naming

- ใช้ verb + object: `getUserById`, `createOrder`, `validateEmail`
- แยกคำให้ชัดเจนเมื่อมี side effects: `enqueueEmail`, `persistInvoice`, `publishEvent`
- หลีกเลี่ยง `process`, `handle`, `doThing` ถ้าไม่บอกความหมายจริง

### 5. Type/Interface Naming

- `PascalCase` สำหรับ types/interfaces/enums
- suffix แบบมาตรฐาน: `UserDto`, `CreateOrderRequest`, `PaymentResponse`
- ระวัง prefix `I` (optional) ให้เลือกแนวเดียวทั้ง repo

### 6. Test File Naming

- mirror path ของ source และใช้ `.test.ts` (unit) / `.spec.ts` (integration) ตามที่ทีมกำหนด
- ใช้ชื่อ describe/it แบบ “what/when/expect” เพื่อให้ output อ่านง่าย

### 7. Config File Naming

- config ที่ root ใช้ชื่อมาตรฐาน: `.env.example`, `tsconfig.json`, `eslint.config.*`, `jest.config.*`
- configs แบบ env-specific ให้ชัด: `config/default.ts`, `config/production.ts`

### 8. Documentation Naming

- ใช้ `README.md` ในระดับ repo และในโฟลเดอร์ใหญ่ที่จำเป็น
- ADR ใช้รูปแบบ `docs/adr/NNN-title.md` (ลำดับ + ชื่อสั้น)
- runbooks ใช้ `docs/runbooks/<topic>.md` และมี `INDEX.md` รวม

## Quick Start

```markdown
# Rules (short):
# - Avoid generic names (helpers, misc, data)
# - Use role suffixes (*.service.ts, *.controller.ts, *.repository.ts)
# - camelCase for code, PascalCase for types, UPPER_CASE for constants
# - Mirror source path in tests (tests/ mirrors src/)
```

## Production Checklist

- [ ] Naming convention documented
- [ ] Enforced via linter
- [ ] Team trained on conventions
- [ ] Reviewed in code reviews
- [ ] Auto-fix where possible

## File Naming Conventions

```
TypeScript/JavaScript:
├── PascalCase.tsx       # React components
├── camelCase.ts         # Utilities, services
├── kebab-case.ts        # Config, scripts
├── UPPERCASE.md         # Documentation

Suffixes:
├── *.service.ts         # Service classes
├── *.controller.ts      # API controllers
├── *.repository.ts      # Data access
├── *.middleware.ts      # Middleware
├── *.dto.ts             # Data transfer objects
├── *.types.ts           # Type definitions
├── *.test.ts            # Unit tests
├── *.spec.ts            # Integration tests
├── *.e2e.ts             # End-to-end tests
├── *.mock.ts            # Mock implementations
├── *.config.ts          # Configuration
├── *.constants.ts       # Constants
```

## Folder Naming Conventions

```
Structure:
src/
├── api/                 # Singular domain folders
├── domain/
│   ├── users/          # Feature/entity folders
│   ├── orders/
│   └── products/
├── infrastructure/
├── shared/
│   ├── utils/          # Utility folders
│   ├── types/
│   └── constants/
└── __tests__/           # Test folders (double underscore)

Rules:
- Use kebab-case for folders
- Singular for domains (user not users)
- Plural for collections (utils, types)
- Max 4 levels deep
- No generic names (helpers, misc, stuff)
```

## Variable & Function Naming

```typescript
// Variables: camelCase
const userId = 'user123';
const isActive = true;
const userList = [];

// Constants: SCREAMING_SNAKE_CASE
const MAX_RETRY_COUNT = 3;
const API_BASE_URL = 'https://api.example.com';

// Functions: camelCase with verb prefix
function getUserById(id: string) {}
function createUser(data: UserInput) {}
function validateEmail(email: string) {}
function handleUserUpdate(event: Event) {}

// Boolean: is/has/can/should prefix
function isValid(input: string) {}
function hasPermission(user: User) {}
function canDelete(item: Item) {}

// Async: consider suffix
function fetchUserAsync() {}
function getUserPromise() {}
```

## Type & Interface Naming

```typescript
// Interfaces: PascalCase with 'I' prefix (optional)
interface User {}
interface IUserRepository {}  // Optional I prefix

// Types: PascalCase
type UserId = string;
type UserRole = 'admin' | 'user';

// Enums: PascalCase, members SCREAMING_SNAKE_CASE
enum UserStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  PENDING = 'pending',
}

// DTOs: PascalCase with Dto suffix
interface CreateUserDto {}
interface UpdateUserDto {}

// Response/Request types
interface GetUserResponse {}
interface CreateUserRequest {}
```

## Test Naming

```typescript
// Test files: mirror source path
// src/services/UserService.ts
// → tests/services/UserService.test.ts

// Test names: describe what, when, expect
describe('UserService', () => {
  describe('createUser', () => {
    it('should create user when valid data provided', () => {});
    it('should throw error when email invalid', () => {});
    it('should hash password before saving', () => {});
  });
});

// Test helpers: .mock.ts, .fixture.ts
// tests/__mocks__/UserService.mock.ts
// tests/__fixtures__/users.fixture.ts
```

## Anti-patterns

| Bad | Good | Why |
|-----|------|-----|
| `data.ts` | `users.ts` | Generic = confusing |
| `helpers.ts` | `string-utils.ts` | Vague = hard to find |
| `index.ts` (many) | `users.service.ts` | Barrel = debugging nightmare |
| `get()` | `getUserById()` | No context |
| `temp_var` | `processingQueue` | Meaningless |
| `MyClass2` | `ExtendedMyClass` | Numbers = code smell |

## Enforcement

```json
// .eslintrc.js
{
  "rules": {
    "@typescript-eslint/naming-convention": [
      "error",
      { "selector": "variable", "format": ["camelCase", "UPPER_CASE"] },
      { "selector": "function", "format": ["camelCase"] },
      { "selector": "typeLike", "format": ["PascalCase"] }
    ]
  }
}
```

## Integration Points

- ESLint/Prettier configs
- Pre-commit hooks
- Code review checklists
- IDE snippets

## Further Reading

- [Naming Cheatsheet](https://github.com/kettanaito/naming-cheatsheet)
- [Clean Code Naming](https://cleancoders.com/episode/clean-code-episode-2)
