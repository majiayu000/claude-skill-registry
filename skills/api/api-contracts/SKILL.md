---
name: API Contracts Generator
description: Génère des contrats API cohérents entre Frontend (Next.js) et Backend (NestJS) avec types synchronisés, validation standardisée et error handling uniforme. À utiliser lors de la création d'APIs, DTOs, types frontend/backend, ou quand l'utilisateur mentionne "API", "DTO", "types", "contract", "validation", "frontend-backend", "synchronisation".
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# API Contracts Generator

## 🎯 Mission

Garantir une **communication parfaite** entre Frontend (Next.js) et Backend (NestJS) via des contrats API cohérents, types synchronisés et validation standardisée.

## 🏗️ Philosophie des API Contracts

### Le Problème

Dans un projet full-stack, les erreurs de communication Frontend ↔ Backend sont fréquentes :
- ❌ Types incohérents (backend attend `clubId`, frontend envoie `id`)
- ❌ Validations divergentes (backend accepte 100 chars, frontend 50)
- ❌ Erreurs non standardisées (format différent selon l'endpoint)
- ❌ Documentation obsolète (Swagger non à jour)

### La Solution : API Contracts

Un **API Contract** définit le contrat entre frontend et backend :
- ✅ **DTOs Backend** : Structure des requêtes/réponses avec validation
- ✅ **Types Frontend** : TypeScript synchronisés avec le backend
- ✅ **Validation cohérente** : Mêmes règles backend et frontend
- ✅ **Error format standard** : Format uniforme pour toutes les erreurs
- ✅ **Documentation auto** : Swagger généré depuis le code

### Architecture de Communication

```
Frontend (Next.js)
  ↓ Server Action (avec types)
  ↓ Validation Zod
  ↓ fetch/axios
Backend (NestJS)
  ↓ Controller (avec DTOs)
  ↓ Validation class-validator
  ↓ Handler (CQRS)
  ↓ Response DTO
  ↑ JSON Response
Frontend (Next.js)
  ↑ Typed Response
  ↑ UI Update
```

## 📦 1. Backend DTOs (NestJS)

### Request DTOs (Input)

Les **Request DTOs** définissent la structure des données **envoyées par le frontend**.

#### Template Request DTO

```typescript
// volley-app-backend/src/club-management/presentation/dtos/create-club.dto.ts

import { IsString, IsNotEmpty, IsOptional, MaxLength, MinLength } from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class CreateClubDto {
  @ApiProperty({
    description: 'Club name',
    example: 'Volley Club Paris',
    minLength: 3,
    maxLength: 100,
  })
  @IsString()
  @IsNotEmpty()
  @MinLength(3)
  @MaxLength(100)
  readonly name: string;

  @ApiPropertyOptional({
    description: 'Club description',
    example: 'Best volleyball club in Paris',
    maxLength: 500,
  })
  @IsString()
  @IsOptional()
  @MaxLength(500)
  readonly description?: string;
}
```

**Règles pour Request DTOs** :
- ✅ Validation avec `class-validator` (IsString, IsNotEmpty, etc.)
- ✅ Swagger decorators `@ApiProperty` pour documentation
- ✅ `readonly` pour immutabilité
- ✅ Types primitifs (string, number, boolean, Date)
- ✅ Exemples dans Swagger (`example`)
- ❌ **JAMAIS** de logique métier (seulement validation)

### Response DTOs (Output)

Les **Response DTOs** définissent la structure des données **retournées par le backend**.

#### Template Response DTO

```typescript
// volley-app-backend/src/club-management/presentation/dtos/club-detail.dto.ts

import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class OwnerDto {
  @ApiProperty({ example: 'user-123' })
  id: string;

  @ApiProperty({ example: 'John Doe' })
  name: string;

  @ApiProperty({ example: 'john@example.com' })
  email: string;
}

export class SubscriptionDto {
  @ApiProperty({ example: 'FREE', enum: ['FREE', 'PRO', 'UNLIMITED'] })
  plan: string;

  @ApiProperty({ example: 'ACTIVE', enum: ['ACTIVE', 'INACTIVE', 'EXPIRED'] })
  status: string;

  @ApiProperty({ example: 1 })
  maxTeams: number;

  @ApiProperty({ example: 0 })
  currentTeamsCount: number;
}

export class ClubDetailDto {
  @ApiProperty({ example: 'club-123' })
  id: string;

  @ApiProperty({ example: 'Volley Club Paris' })
  name: string;

  @ApiPropertyOptional({ example: 'Best club in Paris' })
  description?: string;

  @ApiProperty({ type: OwnerDto })
  owner: OwnerDto;

  @ApiProperty({ type: SubscriptionDto })
  subscription: SubscriptionDto;

  @ApiProperty({ example: 15 })
  membersCount: number;

  @ApiProperty({ example: '2024-01-01T00:00:00.000Z' })
  createdAt: Date;
}
```

**Règles pour Response DTOs** :
- ✅ Swagger decorators pour documentation complète
- ✅ Nested DTOs pour relations (OwnerDto, SubscriptionDto)
- ✅ Exemples réalistes
- ✅ Enum values documentés
- ✅ Types primitifs + nested objects
- ❌ **JAMAIS** d'entités domain brutes (utiliser des mappers)

### Pagination DTO (Standard)

```typescript
// volley-app-backend/src/shared/dtos/pagination.dto.ts

import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { Type } from 'class-transformer';
import { IsInt, IsOptional, Max, Min } from 'class-validator';

export class PaginationQueryDto {
  @ApiPropertyOptional({ default: 1, minimum: 1 })
  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  page?: number = 1;

  @ApiPropertyOptional({ default: 10, minimum: 1, maximum: 100 })
  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  @Max(100)
  limit?: number = 10;
}

export class PaginationMetaDto {
  @ApiProperty({ example: 1 })
  page: number;

  @ApiProperty({ example: 10 })
  limit: number;

  @ApiProperty({ example: 50 })
  total: number;

  @ApiProperty({ example: 5 })
  totalPages: number;
}

export class PaginatedResponseDto<T> {
  @ApiProperty({ isArray: true })
  data: T[];

  @ApiProperty({ type: PaginationMetaDto })
  meta: PaginationMetaDto;
}
```

### Controller Integration

```typescript
// volley-app-backend/src/club-management/presentation/controllers/clubs.controller.ts

import { Controller, Post, Get, Body, Param, Query, UseGuards } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiBearerAuth } from '@nestjs/swagger';
import { JwtAuthGuard } from '../../auth/guards/jwt-auth.guard';
import { CreateClubDto } from '../dtos/create-club.dto';
import { ClubDetailDto } from '../dtos/club-detail.dto';
import { ClubListDto } from '../dtos/club-list.dto';
import { PaginationQueryDto, PaginatedResponseDto } from '../../shared/dtos/pagination.dto';
import { CreateClubHandler } from '../../application/commands/create-club/create-club.handler';
import { GetClubHandler } from '../../application/queries/get-club/get-club.handler';
import { ListClubsHandler } from '../../application/queries/list-clubs/list-clubs.handler';

@ApiTags('Clubs')
@ApiBearerAuth()
@Controller('clubs')
@UseGuards(JwtAuthGuard)
export class ClubsController {
  constructor(
    private readonly createClubHandler: CreateClubHandler,
    private readonly getClubHandler: GetClubHandler,
    private readonly listClubsHandler: ListClubsHandler,
  ) {}

  @Post()
  @ApiOperation({ summary: 'Create a new club' })
  @ApiResponse({ status: 201, description: 'Club created', type: String })
  @ApiResponse({ status: 400, description: 'Validation error' })
  async create(@Body() dto: CreateClubDto): Promise<{ id: string }> {
    const command = new CreateClubCommand(dto.name, dto.description, 'current-user-id');
    const id = await this.createClubHandler.execute(command);
    return { id };
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get club details' })
  @ApiResponse({ status: 200, description: 'Club found', type: ClubDetailDto })
  @ApiResponse({ status: 404, description: 'Club not found' })
  async findOne(@Param('id') id: string): Promise<ClubDetailDto> {
    const query = new GetClubQuery(id);
    return this.getClubHandler.execute(query);
  }

  @Get()
  @ApiOperation({ summary: 'List clubs with pagination' })
  @ApiResponse({ status: 200, description: 'Clubs list', type: PaginatedResponseDto })
  async findAll(@Query() pagination: PaginationQueryDto): Promise<PaginatedResponseDto<ClubListDto>> {
    const query = new ListClubsQuery(pagination.page, pagination.limit);
    return this.listClubsHandler.execute(query);
  }
}
```

## 🎨 2. Frontend Types (Next.js)

### Stratégie de Synchronisation

**Option 1 : Générer les types depuis Swagger** (Recommandé)
```bash
# Install openapi-typescript
npm install --save-dev openapi-typescript

# Generate types from backend Swagger
npx openapi-typescript http://localhost:3000/api-json -o src/types/api.ts
```

**Option 2 : Partager les types (Monorepo)**
```typescript
// shared/types/club.types.ts (partagé entre frontend et backend)
export interface CreateClubInput {
  name: string;
  description?: string;
}

export interface ClubDetail {
  id: string;
  name: string;
  description?: string;
  owner: {
    id: string;
    name: string;
    email: string;
  };
  subscription: {
    plan: string;
    status: string;
    maxTeams: number;
    currentTeamsCount: number;
  };
  membersCount: number;
  createdAt: Date;
}
```

**Option 3 : Dupliquer les types manuellement** (Moins recommandé)
```typescript
// volley-app-frontend/src/features/club-management/types/club.types.ts

// Dupliqué depuis backend CreateClubDto
export interface CreateClubInput {
  name: string;
  description?: string;
}

// Dupliqué depuis backend ClubDetailDto
export interface ClubDetail {
  id: string;
  name: string;
  description?: string;
  owner: {
    id: string;
    name: string;
    email: string;
  };
  subscription: {
    plan: string;
    status: string;
    maxTeams: number;
    currentTeamsCount: number;
  };
  membersCount: number;
  createdAt: Date;
}
```

### Validation Frontend avec Zod

```typescript
// volley-app-frontend/src/features/club-management/schemas/club.schema.ts

import { z } from 'zod';

// Schema SYNCHRONISÉ avec backend CreateClubDto
export const createClubSchema = z.object({
  name: z
    .string()
    .min(3, 'Le nom doit contenir au moins 3 caractères')
    .max(100, 'Le nom ne peut pas dépasser 100 caractères'),
  description: z
    .string()
    .max(500, 'La description ne peut pas dépasser 500 caractères')
    .optional(),
});

export type CreateClubInput = z.infer<typeof createClubSchema>;
```

**CRITIQUE** : Les règles de validation Zod doivent **EXACTEMENT** correspondre aux règles backend (class-validator).

## 🔗 3. Server Actions (Frontend → Backend)

### Template Server Action

```typescript
// volley-app-frontend/src/features/club-management/actions/create-club.action.ts
'use server';

import { revalidatePath } from 'next/cache';
import { createClubSchema, CreateClubInput } from '../schemas/club.schema';
import { clubsApi } from '../api/clubs.api';

export async function createClubAction(input: CreateClubInput) {
  try {
    // 1. Validate input (frontend validation)
    const validated = createClubSchema.parse(input);

    // 2. Call backend API
    const response = await clubsApi.create(validated);

    // 3. Revalidate cache
    revalidatePath('/dashboard/coach');

    // 4. Return success
    return {
      success: true as const,
      data: response,
    };
  } catch (error) {
    // 5. Handle errors
    if (error instanceof z.ZodError) {
      return {
        success: false as const,
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Données invalides',
          details: error.errors,
        },
      };
    }

    return {
      success: false as const,
      error: {
        code: 'UNKNOWN_ERROR',
        message: error.message || 'Une erreur est survenue',
      },
    };
  }
}

// Type du retour
export type CreateClubResult =
  | { success: true; data: { id: string } }
  | { success: false; error: { code: string; message: string; details?: any } };
```

### API Client

```typescript
// volley-app-frontend/src/features/club-management/api/clubs.api.ts

import { CreateClubInput, ClubDetail, ClubList } from '../types/club.types';
import { PaginatedResponse } from '@/types/api.types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3000';

export const clubsApi = {
  async create(input: CreateClubInput): Promise<{ id: string }> {
    const response = await fetch(`${API_BASE_URL}/clubs`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${getToken()}`, // Helper to get JWT
      },
      body: JSON.stringify(input),
    });

    if (!response.ok) {
      throw await handleApiError(response);
    }

    return response.json();
  },

  async getById(id: string): Promise<ClubDetail> {
    const response = await fetch(`${API_BASE_URL}/clubs/${id}`, {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    });

    if (!response.ok) {
      throw await handleApiError(response);
    }

    return response.json();
  },

  async list(page: number = 1, limit: number = 10): Promise<PaginatedResponse<ClubList>> {
    const response = await fetch(
      `${API_BASE_URL}/clubs?page=${page}&limit=${limit}`,
      {
        headers: {
          Authorization: `Bearer ${getToken()}`,
        },
      },
    );

    if (!response.ok) {
      throw await handleApiError(response);
    }

    return response.json();
  },
};

// Helper functions
function getToken(): string {
  // Get JWT from cookies or localStorage
  return '';
}

async function handleApiError(response: Response): Promise<Error> {
  const error = await response.json();
  return new ApiError(error.code, error.message, error.details);
}

class ApiError extends Error {
  constructor(
    public code: string,
    message: string,
    public details?: any,
  ) {
    super(message);
    this.name = 'ApiError';
  }
}
```

## ⚠️ 4. Error Handling Standard

### Backend Error Format

```typescript
// volley-app-backend/src/shared/filters/http-exception.filter.ts

import { ExceptionFilter, Catch, ArgumentsHost, HttpException, HttpStatus } from '@nestjs/common';
import { Response } from 'express';

export interface ErrorResponse {
  code: string;
  message: string;
  details?: any;
  timestamp: string;
  path: string;
}

@Catch()
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest();

    let status = HttpStatus.INTERNAL_SERVER_ERROR;
    let errorResponse: ErrorResponse = {
      code: 'INTERNAL_SERVER_ERROR',
      message: 'Une erreur interne est survenue',
      timestamp: new Date().toISOString(),
      path: request.url,
    };

    if (exception instanceof HttpException) {
      status = exception.getStatus();
      const exceptionResponse = exception.getResponse();

      if (typeof exceptionResponse === 'object') {
        errorResponse = {
          ...errorResponse,
          ...(exceptionResponse as any),
        };
      } else {
        errorResponse.message = exceptionResponse as string;
      }
    }

    response.status(status).json(errorResponse);
  }
}
```

### Frontend Error Handling

```typescript
// volley-app-frontend/src/lib/api-error.ts

export class ApiError extends Error {
  constructor(
    public code: string,
    message: string,
    public details?: any,
    public status?: number,
  ) {
    super(message);
    this.name = 'ApiError';
  }

  static fromResponse(response: any): ApiError {
    return new ApiError(
      response.code || 'UNKNOWN_ERROR',
      response.message || 'Une erreur est survenue',
      response.details,
      response.status,
    );
  }

  // User-friendly messages
  getUserMessage(): string {
    const messages: Record<string, string> = {
      VALIDATION_ERROR: 'Les données fournies sont invalides',
      NOT_FOUND: 'La ressource demandée n\'existe pas',
      UNAUTHORIZED: 'Vous devez être connecté pour effectuer cette action',
      FORBIDDEN: 'Vous n\'avez pas les permissions nécessaires',
      INTERNAL_SERVER_ERROR: 'Une erreur interne est survenue. Veuillez réessayer.',
    };

    return messages[this.code] || this.message;
  }
}
```

## ✅ 5. Checklist API Contract

### Backend (NestJS)
- [ ] Request DTOs avec validation class-validator
- [ ] Response DTOs avec Swagger decorators
- [ ] Exemples réalistes dans Swagger
- [ ] Error handling standardisé
- [ ] Pagination DTO pour listes
- [ ] Swagger activé et accessible (`/api`)

### Frontend (Next.js)
- [ ] Types synchronisés avec backend (OpenAPI ou partagés)
- [ ] Validation Zod cohérente avec backend
- [ ] Server Actions avec types
- [ ] API client avec types
- [ ] Error handling standardisé
- [ ] Messages d'erreur traduits pour UI

### Synchronisation
- [ ] Script de génération des types (si OpenAPI)
- [ ] CI/CD vérifie la synchronisation
- [ ] Documentation Swagger à jour
- [ ] Types partagés si monorepo

## 🎓 Exemple Complet : CreateClub Flow

### 1. Backend DTO

```typescript
// backend/src/club-management/presentation/dtos/create-club.dto.ts
export class CreateClubDto {
  @IsString()
  @MinLength(3)
  @MaxLength(100)
  readonly name: string;

  @IsString()
  @IsOptional()
  @MaxLength(500)
  readonly description?: string;
}
```

### 2. Frontend Schema (Zod)

```typescript
// frontend/src/features/club-management/schemas/club.schema.ts
export const createClubSchema = z.object({
  name: z.string().min(3).max(100),
  description: z.string().max(500).optional(),
});
```

### 3. Server Action

```typescript
// frontend/src/features/club-management/actions/create-club.action.ts
export async function createClubAction(input: CreateClubInput) {
  const validated = createClubSchema.parse(input); // Frontend validation
  const response = await clubsApi.create(validated); // Backend call
  revalidatePath('/dashboard/coach');
  return { success: true, data: response };
}
```

### 4. Component Usage

```typescript
// frontend/src/features/club-management/components/ClubCreationForm.tsx
'use client';

import { useTransition } from 'react';
import { createClubAction } from '../actions/create-club.action';

export function ClubCreationForm() {
  const [isPending, startTransition] = useTransition();

  const handleSubmit = async (formData: FormData) => {
    startTransition(async () => {
      const result = await createClubAction({
        name: formData.get('name') as string,
        description: formData.get('description') as string,
      });

      if (result.success) {
        router.push(`/clubs/${result.data.id}`);
      } else {
        setError(result.error.message);
      }
    });
  };

  return <form action={handleSubmit}>...</form>;
}
```

## 🚨 Erreurs Courantes à Éviter

1. ❌ **Types incohérents**
   - ✅ FAIRE : Générer types frontend depuis Swagger ou partager
   - ❌ NE PAS FAIRE : Dupliquer manuellement sans synchronisation

2. ❌ **Validations divergentes**
   - ✅ FAIRE : Même règles backend (class-validator) et frontend (Zod)
   - ❌ NE PAS FAIRE : Backend max=100, Frontend max=50

3. ❌ **Erreurs non standardisées**
   - ✅ FAIRE : Format uniforme `{ code, message, details }`
   - ❌ NE PAS FAIRE : Formats différents selon l'endpoint

4. ❌ **Swagger obsolète**
   - ✅ FAIRE : Swagger généré automatiquement depuis les DTOs
   - ❌ NE PAS FAIRE : Documentation manuelle non synchronisée

5. ❌ **Server Actions avec logique métier**
   - ✅ FAIRE : Server Actions = orchestration mince (appel API + cache)
   - ❌ NE PAS FAIRE : Logique métier dans Server Actions

## 📚 Skills Complémentaires

Pour aller plus loin :
- **server-actions** : Patterns Server Actions Next.js détaillés
- **ddd-bounded-context** : Architecture backend DDD
- **cqrs-command-query** : Commands/Queries pour APIs

---

**Rappel** : La **synchronisation parfaite** Frontend ↔ Backend garantit une communication sans bugs et une expérience développeur optimale.
