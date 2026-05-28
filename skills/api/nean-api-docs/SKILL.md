---
name: nean-api-docs
description: Generate and serve OpenAPI documentation from NestJS decorators.
argument-hint: "[--serve] [--export <path>]"
allowed-tools: Bash, Write, Read, Glob, Grep
---

## Purpose
Generate and serve OpenAPI (Swagger) documentation using @nestjs/swagger decorators.

## Arguments
- `--serve` — Ensure Swagger UI is available at `/api/docs`
- `--export <path>` — Export OpenAPI spec to file (default: `openapi.json`)
- (no args) — Audit endpoints for missing documentation

## What gets created/updated

```
apps/api/src/
├── main.ts                     # Swagger setup (if not present)
└── modules/**/
    └── *.controller.ts         # API decorators added
    
openapi.json                    # Generated spec (if --export)
```

## How it works

NestJS Swagger reads decorators from:
1. **Controllers** — `@ApiTags`, `@ApiOperation`, `@ApiResponse`
2. **DTOs** — `@ApiProperty` from class-validator decorators
3. **Parameters** — `@ApiParam`, `@ApiQuery`, `@ApiBody`

## Decorator conventions

### Controller decorators
```typescript
@Controller('users')
@ApiTags('users')
@UseGuards(JwtAuthGuard)
@ApiBearerAuth()
export class UsersController {
  @Get()
  @ApiOperation({ summary: 'List all users' })
  @ApiPaginatedResponse(UserResponseDto)
  findAll(@Query() query: PaginationDto) {}

  @Get(':id')
  @ApiOperation({ summary: 'Get user by ID' })
  @ApiResponse({ status: 200, type: UserResponseDto })
  @ApiResponse({ status: 404, description: 'User not found' })
  findOne(@Param('id', ParseUUIDPipe) id: string) {}

  @Post()
  @ApiOperation({ summary: 'Create new user' })
  @ApiCreatedResponse({ type: UserResponseDto })
  @ApiBadRequestResponse({ description: 'Validation failed' })
  create(@Body() dto: CreateUserDto) {}
}
```

### DTO decorators
```typescript
export class CreateUserDto {
  @ApiProperty({ 
    description: 'User email address',
    example: 'user@example.com' 
  })
  @IsEmail()
  email: string;

  @ApiProperty({ 
    description: 'Display name',
    minLength: 1,
    maxLength: 100 
  })
  @IsString()
  @MinLength(1)
  @MaxLength(100)
  name: string;

  @ApiPropertyOptional({ 
    description: 'Profile bio',
    default: '' 
  })
  @IsOptional()
  @IsString()
  bio?: string;
}
```

## Swagger setup (main.ts)

```typescript
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Swagger configuration
  const config = new DocumentBuilder()
    .setTitle('My API')
    .setDescription('API documentation')
    .setVersion('1.0')
    .addBearerAuth()
    .addTag('health', 'Health check endpoints')
    .addTag('auth', 'Authentication endpoints')
    .addTag('users', 'User management')
    .build();

  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs', app, document, {
    swaggerOptions: {
      persistAuthorization: true,
    },
  });

  await app.listen(3000);
}
```

## Swagger UI

When configured, Swagger UI is available at `/api/docs`:
- Interactive API explorer
- Try-it-out functionality (with auth)
- Schema visualization
- Download OpenAPI spec

## Audit checklist

When auditing documentation:
- [ ] All controllers have `@ApiTags`
- [ ] All endpoints have `@ApiOperation` with summary
- [ ] All response codes documented with `@ApiResponse`
- [ ] All DTOs have `@ApiProperty` decorators
- [ ] Examples provided for complex types
- [ ] Auth requirements documented (`@ApiBearerAuth`)
- [ ] Error responses documented

## Workflow
1. Ensure @nestjs/swagger is installed
2. Configure Swagger in main.ts
3. Audit controllers for missing decorators
4. Add decorators as needed
5. Verify documentation at /api/docs

## Output
- Endpoints documented count
- Missing documentation warnings
- Spec file location (if exported)

## Reference
For setup and customization, see `reference/nean-api-docs-reference.md`
