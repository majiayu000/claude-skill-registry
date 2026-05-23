---
name: vendix-backend
description: >
  NestJS patterns for Vendix backend API.
  Trigger: When editing files in apps/backend/, creating modules, or working with Prisma.
license: MIT
metadata:
  author: vendix
  version: "1.0"
---

## When to Use

Use this skill when:
- Creating NestJS modules, controllers, or services
- Adding API endpoints
- Working with Prisma in the backend
- Implementing business logic

## Critical Patterns

### Pattern 1: Module Structure

All features MUST follow this structure:

```
apps/backend/src/features/
└── my-feature/
    ├── my-feature.module.ts
    ├── my-feature.controller.ts
    ├── my-feature.service.ts
    ├── dto/
    │   ├── create-my-feature.dto.ts
    │   └── update-my-feature.dto.ts
    └── entities/
        └── my-feature.entity.ts
```

### Pattern 2: Controller Pattern

Controllers handle HTTP requests and delegate to services:

```typescript
import { Controller, Get, Post, Body, Param, HttpStatus } from '@nestjs/common';
import { MyFeatureService } from './my-feature.service';
import { CreateMyFeatureDto } from './dto/create-my-feature.dto';

@Controller('my-feature')
export class MyFeatureController {
  constructor(private readonly myFeatureService: MyFeatureService) {}

  @Get()
  async findAll() {
    return this.myFeatureService.findAll();
  }

  @Get(':id')
  async findOne(@Param('id') id: string) {
    return this.myFeatureService.findOne(id);
  }

  @Post()
  async create(@Body() createDto: CreateMyFeatureDto) {
    return this.myFeatureService.create(createDto);
  }
}
```

### Pattern 3: Service with Prisma

Services use Prisma for database operations:

```typescript
import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { CreateMyFeatureDto } from './dto/create-my-feature.dto';

@Injectable()
export class MyFeatureService {
  constructor(private prisma: PrismaService) {}

  async findAll() {
    return this.prisma.myFeature.findMany();
  }

  async findOne(id: string) {
    return this.prisma.myFeature.findUnique({ where: { id } });
  }

  async create(createDto: CreateMyFeatureDto) {
    return this.prisma.myFeature.create({ data: createDto });
  }

  async update(id: string, updateDto: UpdateMyFeatureDto) {
    return this.prisma.myFeature.update({
      where: { id },
      data: updateDto,
    });
  }

  async remove(id: string) {
    return this.prisma.myFeature.delete({ where: { id } });
  }
}
```

### Pattern 4: DTO Validation with class-validator

```typescript
import { IsString, IsNotEmpty, IsEmail, MinLength } from 'class-validator';

export class CreateUserDto {
  @IsString()
  @IsNotEmpty()
  name: string;

  @IsEmail()
  email: string;

  @IsString()
  @MinLength(8)
  password: string;
}
```

### Pattern 5: Module Registration

```typescript
import { Module } from '@nestjs/common';
import { MyFeatureController } from './my-feature.controller';
import { MyFeatureService } from './my-feature.service';
import { PrismaModule } from '../../prisma/prisma.module';

@Module({
  imports: [PrismaModule],
  controllers: [MyFeatureController],
  providers: [MyFeatureService],
  exports: [MyFeatureService],
})
export class MyFeatureModule {}
```

## Decision Tree

```
Creating a new feature?
├── Create feature folder under src/features/
├── Generate module, controller, service
├── Create DTOs for validation
├── Add Prisma methods in service
└── Register module in app.module.ts

Adding API endpoint?
├── Add route handler in controller
├── Implement business logic in service
├── Use Prisma for database operations
└── Create/update DTOs for validation

Adding authentication?
├── Use JWT guards
├── Create auth module
├── Implement passport strategies
└── Protect routes with @UseGuards()
```

## Code Examples

### Example 1: Complete CRUD Module

```typescript
// items.module.ts
import { Module } from '@nestjs/common';
import { ItemsController } from './items.controller';
import { ItemsService } from './items.service';
import { PrismaModule } from '../prisma/prisma.module';

@Module({
  imports: [PrismaModule],
  controllers: [ItemsController],
  providers: [ItemsService],
  exports: [ItemsService],
})
export class ItemsModule {}

// items.controller.ts
import { Controller, Get, Post, Put, Delete, Param, Body } from '@nestjs/common';
import { ItemsService } from './items.service';
import { CreateItemDto } from './dto/create-item.dto';

@Controller('items')
export class ItemsController {
  constructor(private readonly itemsService: ItemsService) {}

  @Get()
  findAll() {
    return this.itemsService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.itemsService.findOne(id);
  }

  @Post()
  create(@Body() createItemDto: CreateItemDto) {
    return this.itemsService.create(createItemDto);
  }
}

// items.service.ts
import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class ItemsService {
  constructor(private prisma: PrismaService) {}

  findAll() {
    return this.prisma.item.findMany();
  }

  findOne(id: string) {
    return this.prisma.item.findUnique({ where: { id } });
  }

  create(createItemDto: CreateItemDto) {
    return this.prisma.item.create({ data: createItemDto });
  }
}
```

### Example 2: Using Prisma with Relations

```typescript
// Find with relations
async findOneWithDetails(id: string) {
  return this.prisma.order.findUnique({
    where: { id },
    include: {
      items: true,
      customer: true,
    },
  });
}

// Find with filtering
async findActiveOrders() {
  return this.prisma.order.findMany({
    where: { status: 'ACTIVE' },
    include: { items: true },
  });
}
```

### Example 3: Exception Handling

```typescript
import { NotFoundException, ForbiddenException } from '@nestjs/common';

async remove(id: string) {
  const item = await this.prisma.item.findUnique({ where: { id } });

  if (!item) {
    throw new NotFoundException(`Item with ID ${id} not found`);
  }

  // Check permissions
  if (item.userId !== currentUser.id) {
    throw new ForbiddenException('You do not have permission');
  }

  return this.prisma.item.delete({ where: { id } });
}
```

## Commands

```bash
# Generate new module
cd apps/backend
nest g module features/my-feature
nest g controller features/my-feature
nest g service features/my-feature

# Run backend in development
npm run start:dev -w apps/backend

# Run backend in production mode
npm run start:prod -w apps/backend

# Run tests
npm run test -w apps/backend

# Run e2e tests
npm run test:e2e -w apps/backend

# Prisma migrations
npm run prisma migrate dev -w apps/backend
npm run prisma migrate deploy -w apps/backend

# Open Prisma Studio
npm run prisma studio -w apps/backend
```

## Resources

- **Backend**: See [apps/backend/doc/](../../../apps/backend/doc/) for detailed docs
- **Prisma**: See [skills/vendix-prisma/SKILL.md](../vendix-prisma/SKILL.md)
- **NestJS Docs**: https://docs.nestjs.com
