---
name: Endpoint Generator
description: Generator สำหรับสร้าง API endpoint พร้อม controller, service, repository, validation, tests และ documentation โดยอัตโนมัติ
---

# Endpoint Generator

## Overview

Generator สำหรับสร้าง API endpoint พร้อม controller, service, repository, types, validation, และ tests โดยอัตโนมัติ ลดเวลาในการเขียน boilerplate code

## Why This Matters

- **Speed**: สร้าง CRUD endpoints ในไม่กี่วินาที
- **Consistency**: ทุก endpoint มี pattern เดียวกัน
- **Completeness**: ไม่ลืม validation, error handling
- **Testability**: Tests scaffold มาด้วย

---

## Endpoint Types

### CRUD Operations
```
CREATE: POST /users
READ:   GET /users, GET /users/:id
UPDATE: PUT /users/:id, PATCH /users/:id
DELETE: DELETE /users/:id
```

### Custom Actions
```
POST /users/:id/activate
POST /users/:id/reset-password
GET /users/:id/orders
```

### Batch Operations
```
POST /users/bulk-create
PUT /users/bulk-update
DELETE /users/bulk-delete
```

---

## Generated Files

### File Structure
```
src/api/users/
├── users.controller.ts    # Request handling
├── users.service.ts       # Business logic
├── users.repository.ts    # Data access
├── users.types.ts         # TypeScript types
├── users.validation.ts    # Input validation
├── users.routes.ts        # Route definitions
└── users.openapi.yaml     # API documentation

tests/api/users/
├── users.controller.test.ts
├── users.service.test.ts
└── users.integration.test.ts
```

---

## Quick Start

### Generate Full CRUD
```bash
npx generate-endpoint users --crud

# Output:
✓ Generated users.controller.ts
✓ Generated users.service.ts
✓ Generated users.repository.ts
✓ Generated users.validation.ts
✓ Generated users.routes.ts
✓ Generated tests
```

### Generate Specific Operations
```bash
npx generate-endpoint users --operations create,read,update
```

### Generate from Schema
```bash
npx generate-endpoint --from-schema prisma/schema.prisma --model User
```

---

## Generated Code Examples

### Controller
```typescript
// users.controller.ts
import { Request, Response } from 'express';
import { UsersService } from './users.service';
import { validateCreateUser } from './users.validation';

export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  async create(req: Request, res: Response) {
    const data = validateCreateUser(req.body);
    const user = await this.usersService.create(data);
    return res.status(201).json({ data: user });
  }

  async findAll(req: Request, res: Response) {
    const users = await this.usersService.findAll(req.query);
    return res.json({ data: users });
  }

  async findOne(req: Request, res: Response) {
    const user = await this.usersService.findOne(req.params.id);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    return res.json({ data: user });
  }
}
```

### Service
```typescript
// users.service.ts
import { UsersRepository } from './users.repository';
import { CreateUserDto, UpdateUserDto } from './users.types';

export class UsersService {
  constructor(private readonly repository: UsersRepository) {}

  async create(data: CreateUserDto) {
    return this.repository.create(data);
  }

  async findAll(query: any) {
    return this.repository.findAll(query);
  }

  async findOne(id: string) {
    return this.repository.findById(id);
  }

  async update(id: string, data: UpdateUserDto) {
    return this.repository.update(id, data);
  }

  async delete(id: string) {
    return this.repository.delete(id);
  }
}
```

### Validation
```typescript
// users.validation.ts
import { z } from 'zod';

export const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  password: z.string().min(8),
});

export const updateUserSchema = createUserSchema.partial();

export type CreateUserDto = z.infer<typeof createUserSchema>;
export type UpdateUserDto = z.infer<typeof updateUserSchema>;

export function validateCreateUser(data: unknown): CreateUserDto {
  return createUserSchema.parse(data);
}
```

### Routes
```typescript
// users.routes.ts
import { Router } from 'express';
import { UsersController } from './users.controller';
import { authenticate } from '../../middleware/auth';

const router = Router();
const controller = new UsersController();

router.post('/', authenticate, controller.create);
router.get('/', authenticate, controller.findAll);
router.get('/:id', authenticate, controller.findOne);
router.put('/:id', authenticate, controller.update);
router.delete('/:id', authenticate, controller.delete);

export default router;
```

---

## OpenAPI Generation

### Generated Spec
```yaml
# users.openapi.yaml
paths:
  /users:
    post:
      summary: Create user
      tags: [Users]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserDto'
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          description: Validation error

components:
  schemas:
    CreateUserDto:
      type: object
      required: [email, name, password]
      properties:
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 1
          maxLength: 100
        password:
          type: string
          minLength: 8
```

---

## Test Generation

### Unit Tests
```typescript
// users.controller.test.ts
describe('UsersController', () => {
  let controller: UsersController;
  let mockService: jest.Mocked<UsersService>;

  beforeEach(() => {
    mockService = {
      create: jest.fn(),
      findAll: jest.fn(),
      findOne: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
    } as any;
    controller = new UsersController(mockService);
  });

  describe('create', () => {
    it('should create user with valid data', async () => {
      const userData = { 
        email: 'test@example.com', 
        name: 'Test',
        password: 'password123'
      };
      mockService.create.mockResolvedValue({ id: '1', ...userData });

      const req = { body: userData } as any;
      const res = {
        status: jest.fn().mockReturnThis(),
        json: jest.fn()
      } as any;

      await controller.create(req, res);

      expect(mockService.create).toHaveBeenCalledWith(userData);
      expect(res.status).toHaveBeenCalledWith(201);
    });

    it('should return 400 on validation error', async () => {
      const invalidData = { email: 'invalid' };
      
      await expect(
        controller.create({ body: invalidData } as any, {} as any)
      ).rejects.toThrow();
    });
  });
});
```

### Integration Tests
```typescript
// users.integration.test.ts
import request from 'supertest';
import app from '../../app';

describe('Users API', () => {
  describe('POST /users', () => {
    it('should create user', async () => {
      const response = await request(app)
        .post('/users')
        .send({
          email: 'test@example.com',
          name: 'Test User',
          password: 'password123'
        })
        .expect(201);

      expect(response.body.data).toHaveProperty('id');
      expect(response.body.data.email).toBe('test@example.com');
    });
  });
});
```

---

## Customization

### Custom Templates
```typescript
// templates/controller.template.ts
export const controllerTemplate = (entityName: string) => `
import { Request, Response } from 'express';
import { ${entityName}Service } from './${entityName.toLowerCase()}.service';

export class ${entityName}Controller {
  constructor(private readonly service: ${entityName}Service) {}

  // Generated methods...
}
`;
```

### Hooks
```typescript
// generator.config.ts
export default {
  hooks: {
    beforeGenerate: (context) => {
      console.log('Generating', context.entityName);
    },
    afterGenerate: (context, files) => {
      console.log('Generated', files.length, 'files');
    }
  }
};
```

---

## Best Practices

### 1. Start from Schema
```bash
# Generate from Prisma schema
npx generate-endpoint --from-schema prisma/schema.prisma --model User

# Ensures types match database
```

### 2. Include Middleware
```typescript
// Auto-attach common middleware
router.post('/', 
  authenticate,      // Auth
  rateLimit,         // Rate limiting
  validateRequest,   // Validation
  controller.create
);
```

### 3. Generate Tests
```bash
# Always generate tests
npx generate-endpoint users --crud --tests

# Saves time, ensures coverage
```

### 4. Version API
```typescript
// Generate with versioning
npx generate-endpoint users --version v1

// Output: src/api/v1/users/
```

---

## Summary

**Endpoint Generator:** สร้าง API endpoints อัตโนมัติ

**Generated Files:**
- Controller (request handling)
- Service (business logic)
- Repository (data access)
- Validation (input validation)
- Routes (route definitions)
- Tests (unit + integration)
- OpenAPI (documentation)

**Benefits:**
- 10x faster than manual
- Consistent patterns
- Complete with tests
- No missing validation

**Usage:**
```bash
npx generate-endpoint users --crud
```
