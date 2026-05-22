---
name: clean-architecture-frontend
description: Clean Architecture patterns for Next.js 16 frontend applications. Enforces strict layer separation (Domain, Application, Infrastructure, Delivery) with the Dependency Rule, ensuring business logic independence from frameworks. Use when designing scalable architecture, implementing use cases, separating concerns, or migrating to maintainable patterns.
---

# Clean Architecture for Frontend Development

Expert guidance for implementing Clean Architecture principles in Next.js 16 App Router projects with strict layer separation, dependency inversion, and framework-independent business logic.

---

## ⚠️ PRAGMATIC ARCHITECTURE: When NOT to Use Full Clean Architecture

> **YAGNI Principle:** You Ain't Gonna Need It. Apply Clean Architecture ONLY where complexity justifies it.

### Decision Matrix: Simple vs Full DDD

| Criteria           | Use SIMPLE Pattern   | Use FULL DDD                  |
| ------------------ | -------------------- | ----------------------------- |
| **Operation**      | Read-only CRUD       | Mutations with business rules |
| **Business Rules** | None/trivial         | Complex validation, state     |
| **Data Ownership** | Public data          | User-owned (requires auth)    |
| **Testability**    | Integration tests OK | Need unit tests on logic      |

### Simple Pattern Example (Characters)

```typescript
// ✅ SIMPLE: Direct Prisma queries for read-only public data
// app/_lib/repositories.ts
export async function findAllCharacters(limit = 50) {
  return prisma.character.findMany({ take: limit });
}

// app/characters/page.tsx
const characters = await findAllCharacters();
```

**Why Simple Here?**

- No business rules to enforce
- Public data (no auth needed)
- A UseCase would just be a pass-through wrapper

### Full DDD Example (Diary Entries)

```typescript
// ✅ FULL DDD: Mutations with business rules + auth + RLS
// app/_actions/diary.ts
export async function createDiaryEntry(...) {
  return withAuthenticatedRLS(prisma, async (tx, user) => {
    const useCase = UseCaseFactory.createCreateDiaryEntryUseCase();
    await useCase.execute(input, user.id);
  });
}
```

**Why Full DDD Here?**

- Business rules: character/location must exist
- User ownership: entries belong to users
- Authorization: RLS enforcement
- Testable: UseCase can be unit tested

### Reference: Architecture Decision Matrix

See [docs/ARCHITECTURE_DECISION_MATRIX.md](../../../docs/ARCHITECTURE_DECISION_MATRIX.md) for the complete decision guide including:

- Domain classification (Simple, Hybrid, Complex)
- Migration guidelines
- Anti-patterns to avoid

---

## When to Use This Skill

✅ **Primary Use Cases**

- "Implement Clean Architecture in Next.js"
- "Separate business logic from framework"
- "Create use cases and interactors"
- "Design independent domain layer"
- "Apply Dependency Rule"
- "Implement hexagonal architecture"
- "Design port and adapter pattern"

✅ **Secondary Use Cases**

- "Where should business rules go?"
- "How to make framework-independent code?"
- "Design repository interfaces"
- "Implement dependency injection"
- "Test business logic in isolation"
- "Migrate from monolithic structure"
- "Scale application architecture"

❌ **Do NOT use when**

- Simple static websites
- Quick prototypes without complex logic
- Pure marketing/landing pages
- Applications with minimal business rules
- **Simple CRUD without business logic** (use direct repository pattern)

---

## Core Principles of Clean Architecture

### The Dependency Rule

> **Source code dependencies must point only inward, toward higher-level policies.**

```
┌─────────────────────────────────────────┐
│         Delivery Layer (UI)             │ ← Frameworks, UI, HTTP
│  ┌───────────────────────────────────┐  │
│  │   Infrastructure Layer (Data)     │  │ ← DB, External APIs
│  │  ┌─────────────────────────────┐  │  │
│  │  │  Application Layer (Use Cases)│ │ │ ← Orchestration
│  │  │  ┌───────────────────────┐  │  │  │
│  │  │  │   Domain Layer        │  │  │  │ ← Business Rules
│  │  │  │   (Entities, VOs)     │  │  │  │
│  │  │  └───────────────────────┘  │  │  │
│  │  └─────────────────────────────┘  │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘

Dependencies flow INWARD ONLY:
Delivery → Infrastructure → Application → Domain
```

**Key Rules:**

1. **Inner layers** know nothing about outer layers
2. **Domain** is 100% framework-agnostic (no React, no Next.js)
3. **Application** defines interfaces, Infrastructure implements them
4. **Delivery** depends on everything, but everything else ignores it

### The Four Layers

#### 1. Domain Layer (Innermost)

**Purpose:** Pure business logic and rules

**Contains:**

- Entities (business objects)
- Value Objects (immutable data)
- Domain Services (complex business rules)
- Domain Events
- Business exceptions

**Characteristics:**

- Zero dependencies on frameworks
- No React, no Next.js, no Prisma
- Can be tested with pure TypeScript
- Portable to any framework

**Location:** `/core/domain/`

```typescript
// ✅ CORRECT - Pure domain entity
export class Episode {
  private constructor(
    public readonly id: number,
    public readonly title: string,
    public readonly season: number,
    public readonly episodeNumber: number,
    private _rating: number
  ) {
    this.validateRating(_rating);
  }

  static create(data: EpisodeData): Episode {
    return new Episode(
      data.id,
      data.title,
      data.season,
      data.episodeNumber,
      data.rating
    );
  }

  // Business rule: rating must be 1-5
  private validateRating(rating: number): void {
    if (rating < 1 || rating > 5) {
      throw new InvalidRatingError("Rating must be between 1 and 5");
    }
  }

  updateRating(newRating: number): Episode {
    this.validateRating(newRating);
    return new Episode(
      this.id,
      this.title,
      this.season,
      this.episodeNumber,
      newRating
    );
  }

  get isHighlyRated(): boolean {
    return this._rating >= 4;
  }
}

// ❌ WRONG - Domain depends on framework
import { prisma } from "@/app/_lib/prisma"; // NO!
export class Episode {
  async save() {
    await prisma.episode.update(...); // VIOLATION!
  }
}
```

#### 2. Application Layer (Use Cases)

**Purpose:** Orchestrate business logic for specific use cases

**Contains:**

- Use Cases / Interactors
- Application Services
- DTOs (Data Transfer Objects)
- Repository Interfaces (ports)
- Service Interfaces (ports)

**Characteristics:**

- Defines interfaces for Infrastructure layer
- Orchestrates Domain entities
- Framework-agnostic (but aware of application needs)
- Can import from Domain layer only

**Location:** `/core/application/`

```typescript
// ✅ CORRECT - Use case with interface dependency
import { Episode } from "@/core/domain/entities/Episode";
import { EpisodeRepository } from "@/core/application/ports/EpisodeRepository";

export class TrackEpisodeUseCase {
  constructor(private episodeRepository: EpisodeRepository) {}

  async execute(input: TrackEpisodeInput): Promise<TrackEpisodeOutput> {
    // 1. Fetch episode from repository (interface)
    const episode = await this.episodeRepository.findById(input.episodeId);
    if (!episode) {
      throw new EpisodeNotFoundError(input.episodeId);
    }

    // 2. Apply business rule (domain entity)
    const updatedEpisode = episode.updateRating(input.rating);

    // 3. Persist changes via repository (interface)
    await this.episodeRepository.save(updatedEpisode);

    // 4. Return DTO
    return {
      episodeId: updatedEpisode.id,
      newRating: updatedEpisode.rating,
    };
  }
}

// Interface (port) - defined in Application layer
export interface EpisodeRepository {
  findById(id: number): Promise<Episode | null>;
  save(episode: Episode): Promise<void>;
}

// ❌ WRONG - Use case depends on concrete implementation
import { PrismaEpisodeRepository } from "@/infrastructure/prisma"; // NO!
export class TrackEpisodeUseCase {
  async execute(input: TrackEpisodeInput) {
    const repo = new PrismaEpisodeRepository(); // VIOLATION!
    await repo.save(...);
  }
}
```

#### 3. Infrastructure Layer (Adapters)

**Purpose:** Implement interfaces defined by Application layer

**Contains:**

- Repository implementations (Prisma adapters)
- External service adapters (API clients)
- Database configurations
- Third-party integrations
- Mappers (Domain ↔ Database)

**Characteristics:**

- Implements Application interfaces
- Knows about Domain and Application layers
- Framework-specific code lives here
- Depends inward only

**Location:** `/infrastructure/`

```typescript
// ✅ CORRECT - Infrastructure implements Application interface
import { EpisodeRepository } from "@/core/application/ports/EpisodeRepository";
import { Episode } from "@/core/domain/entities/Episode";
import { prisma } from "@/app/_lib/prisma";

export class PrismaEpisodeRepository implements EpisodeRepository {
  async findById(id: number): Promise<Episode | null> {
    const record = await prisma.episode.findUnique({ where: { id } });
    if (!record) return null;

    // Map Prisma model to Domain entity
    return Episode.create({
      id: record.id,
      title: record.title,
      season: record.season,
      episodeNumber: record.episode_number,
      rating: record.rating,
    });
  }

  async save(episode: Episode): Promise<void> {
    await prisma.episode.update({
      where: { id: episode.id },
      data: {
        rating: episode.rating,
      },
    });
  }
}

// Mapper utility
export class EpisodePrismaMapper {
  static toDomain(record: PrismaEpisode): Episode {
    return Episode.create({
      id: record.id,
      title: record.title,
      season: record.season,
      episodeNumber: record.episode_number,
      rating: record.rating,
    });
  }

  static toPersistence(episode: Episode): PrismaEpisodeData {
    return {
      id: episode.id,
      title: episode.title,
      season: episode.season,
      episode_number: episode.episodeNumber,
      rating: episode.rating,
    };
  }
}
```

#### 4. Delivery Layer (UI/Controllers)

**Purpose:** Handle user interactions and presentation

**Contains:**

- Next.js App Router pages, layouts
- React Server/Client components
- Server Actions (as thin controllers)
- API routes
- Dependency injection/composition

**Characteristics:**

- Depends on all other layers
- Orchestrates use case execution
- Handles HTTP/UI concerns
- Provides dependencies to use cases

**Location:** `/app/`

```typescript
// ✅ CORRECT - Server Action as thin controller
"use server";

import { TrackEpisodeUseCase } from "@/core/application/use-cases/TrackEpisodeUseCase";
import { PrismaEpisodeRepository } from "@/infrastructure/prisma/EpisodeRepository";
import { revalidatePath } from "next/cache";

export async function trackEpisode(episodeId: number, rating: number) {
  // 1. Compose dependencies (Dependency Injection)
  const episodeRepository = new PrismaEpisodeRepository();
  const useCase = new TrackEpisodeUseCase(episodeRepository);

  // 2. Execute use case
  try {
    const result = await useCase.execute({ episodeId, rating });

    // 3. Handle framework-specific concerns
    revalidatePath(`/episodes/${episodeId}`);

    return { success: true, data: result };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// ✅ CORRECT - Page as composition layer
import { PrismaEpisodeRepository } from "@/infrastructure/prisma/EpisodeRepository";
import { GetEpisodeDetailsUseCase } from "@/core/application/use-cases/GetEpisodeDetailsUseCase";
import { EpisodeDetail } from "@/app/_components/EpisodeDetail";

export default async function EpisodePage({ params }: Props) {
  // Compose dependencies
  const repository = new PrismaEpisodeRepository();
  const useCase = new GetEpisodeDetailsUseCase(repository);

  // Execute use case
  const episode = await useCase.execute({ id: params.id });

  // Render UI
  return <EpisodeDetail episode={episode} />;
}
```

---

## Integration with Next.js 16 App Router

### Directory Structure

```
app/                          # Delivery Layer (Next.js)
  episodes/
    [id]/
      page.tsx               # Thin orchestration layer
      actions.ts             # Server Actions as controllers
  _components/               # Delivery-specific UI components
  _lib/                      # Framework utilities (auth, prisma)

core/                        # Business Logic (Framework-agnostic)
  domain/
    entities/
      Episode.ts             # Pure business object
      Character.ts
    value-objects/
      Rating.ts              # Immutable value with validation
      EmailAddress.ts
    services/
      EpisodeRatingService.ts # Complex domain rules
    exceptions/
      DomainException.ts
      InvalidRatingError.ts

  application/
    use-cases/
      TrackEpisodeUseCase.ts # Orchestrate episode tracking
      GetEpisodeDetailsUseCase.ts
    ports/                   # Interfaces (contracts)
      EpisodeRepository.ts   # Interface for data access
      NotificationService.ts # Interface for notifications
    dtos/
      TrackEpisodeInput.ts
      EpisodeDetailsOutput.ts

infrastructure/              # Adapters (Framework-specific)
  prisma/
    repositories/
      PrismaEpisodeRepository.ts # Implements EpisodeRepository
      PrismaCharacterRepository.ts
    mappers/
      EpisodeMapper.ts       # Domain ↔ Prisma conversion
  email/
    SendgridEmailService.ts  # Implements NotificationService
  cache/
    RedisCache.ts

prisma/
  schema.prisma              # Database schema

components/
  ui/                        # Shadcn UI primitives
```

### Use Case Execution Pattern

#### Step 1: Define Domain Entity

```typescript
// core/domain/entities/Episode.ts
export class Episode {
  private constructor(
    public readonly id: number,
    public readonly title: string,
    private _viewCount: number,
  ) {}

  static create(data: EpisodeData): Episode {
    return new Episode(data.id, data.title, data.viewCount ?? 0);
  }

  incrementViewCount(): Episode {
    return new Episode(this.id, this.title, this._viewCount + 1);
  }

  get viewCount(): number {
    return this._viewCount;
  }
}
```

#### Step 2: Define Repository Interface (Port)

```typescript
// core/application/ports/EpisodeRepository.ts
import { Episode } from "@/core/domain/entities/Episode";

export interface EpisodeRepository {
  findById(id: number): Promise<Episode | null>;
  save(episode: Episode): Promise<void>;
  findTrending(limit: number): Promise<Episode[]>;
}
```

#### Step 3: Implement Use Case

```typescript
// core/application/use-cases/IncrementEpisodeViewsUseCase.ts
import { Episode } from "@/core/domain/entities/Episode";
import { EpisodeRepository } from "@/core/application/ports/EpisodeRepository";

export class IncrementEpisodeViewsUseCase {
  constructor(private episodeRepository: EpisodeRepository) {}

  async execute(input: { episodeId: number }): Promise<void> {
    const episode = await this.episodeRepository.findById(input.episodeId);
    if (!episode) {
      throw new EpisodeNotFoundError(input.episodeId);
    }

    const updatedEpisode = episode.incrementViewCount();
    await this.episodeRepository.save(updatedEpisode);
  }
}
```

#### Step 4: Implement Repository Adapter

```typescript
// infrastructure/prisma/repositories/PrismaEpisodeRepository.ts
import { EpisodeRepository } from "@/core/application/ports/EpisodeRepository";
import { Episode } from "@/core/domain/entities/Episode";
import { prisma } from "@/app/_lib/prisma";
import { EpisodeMapper } from "../mappers/EpisodeMapper";

export class PrismaEpisodeRepository implements EpisodeRepository {
  async findById(id: number): Promise<Episode | null> {
    const record = await prisma.episode.findUnique({ where: { id } });
    return record ? EpisodeMapper.toDomain(record) : null;
  }

  async save(episode: Episode): Promise<void> {
    const data = EpisodeMapper.toPersistence(episode);
    await prisma.episode.update({
      where: { id: episode.id },
      data,
    });
  }

  async findTrending(limit: number): Promise<Episode[]> {
    const records = await prisma.episode.findMany({
      orderBy: { viewCount: "desc" },
      take: limit,
    });
    return records.map(EpisodeMapper.toDomain);
  }
}
```

#### Step 5: Execute from Delivery Layer

```typescript
// app/episodes/[id]/actions.ts
"use server";

import { IncrementEpisodeViewsUseCase } from "@/core/application/use-cases/IncrementEpisodeViewsUseCase";
import { PrismaEpisodeRepository } from "@/infrastructure/prisma/repositories/PrismaEpisodeRepository";

export async function incrementViews(episodeId: number) {
  const repository = new PrismaEpisodeRepository();
  const useCase = new IncrementEpisodeViewsUseCase(repository);

  await useCase.execute({ episodeId });
}
```

---

## Exception Handling in Clean Architecture

### Preserve Domain Exception Types Across Layers

**Critical Pattern:** Domain exceptions are part of your domain model. Never wrap them in generic `Error` as they flow through layers.

#### Domain Layer: Define Exceptions

```typescript
// core/domain/exceptions/DomainException.ts
export abstract class DomainException extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly timestamp: Date = new Date(),
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

// core/domain/exceptions/ValidationException.ts
export class ValidationException extends DomainException {
  constructor(
    message: string,
    public readonly field?: string,
    public readonly value?: unknown,
  ) {
    super(message, "VALIDATION_ERROR");
  }
}

// core/domain/exceptions/NotFoundException.ts
export class NotFoundException extends DomainException {
  constructor(
    public readonly entityType: string,
    public readonly entityId: string | number,
  ) {
    super(`${entityType} with id ${entityId} not found`, "NOT_FOUND");
  }
}
```

#### Application Layer: Throw Domain Exceptions

```typescript
// core/application/use-cases/TrackEpisodeUseCase.ts
import {
  ValidationException,
  NotFoundException,
} from "@/core/domain/exceptions";

export class TrackEpisodeUseCase {
  constructor(private episodeRepository: EpisodeRepository) {}

  async execute(input: { episodeId: number; rating: number }, userId: string) {
    // ✅ Throw domain exceptions for business rule violations
    if (!input.rating || input.rating < 1 || input.rating > 5) {
      throw new ValidationException(
        "Rating must be between 1 and 5",
        "rating",
        input.rating,
      );
    }

    const episode = await this.episodeRepository.findById(input.episodeId);
    if (!episode) {
      throw new NotFoundException("Episode", input.episodeId);
    }

    // ... business logic
  }
}
```

#### Delivery Layer: Preserve Exceptions (DO NOT WRAP)

```typescript
// app/_actions/episodes.ts
"use server";
import { withAuthenticatedRLS } from "@/app/_lib/prisma-rls";
import { UseCaseFactory } from "@/infrastructure/factories";
import {
  ValidationException,
  NotFoundException,
  DomainException,
} from "@/core/domain/exceptions";
import { revalidatePath } from "next/cache";

export async function trackEpisode(episodeId: number, rating: number) {
  return withAuthenticatedRLS(prisma, async (tx, user) => {
    try {
      const useCase = UseCaseFactory.createTrackEpisodeUseCase();
      await useCase.execute({ episodeId, rating }, user.id);

      revalidatePath(`/episodes/${episodeId}`);
      return { success: true };
    } catch (error) {
      // ✅ CORRECT: Preserve domain exception types
      if (error instanceof ValidationException) {
        throw error; // Client gets field, value, code
      }
      if (error instanceof NotFoundException) {
        throw error; // Client gets entityType, entityId
      }
      if (error instanceof DomainException) {
        throw error; // Catch-all for domain exceptions
      }
      if (error instanceof Error) {
        throw error; // Preserve standard errors
      }

      // Only truly unexpected errors get wrapped
      throw new Error("Failed to track episode");
    }
  });
}
```

#### ❌ Anti-Pattern: Wrapping Domain Exceptions

```typescript
// ❌ WRONG - Loses type information and metadata
catch (error) {
  if (error instanceof ValidationException) {
    throw new Error(error.message); // Lost field, value, code!
  }
  throw new Error("Failed");
}
```

**Why This is Wrong:**

- Loses exception type (client can't catch `ValidationException`)
- Loses metadata (field, value, code)
- Breaks type-safe error handling
- Makes debugging harder

#### ✅ Correct Pattern: Type-Safe Error Handling

```typescript
// Client component can now handle specific types
"use client";

export function EpisodeTracker({ episodeId }: Props) {
  const handleTrack = async (rating: number) => {
    try {
      await trackEpisode(episodeId, rating);
      toast.success("Episode tracked!");
    } catch (error) {
      // ✅ Type-safe error handling
      if (error instanceof ValidationException) {
        toast.error(`${error.field}: ${error.message}`);
      } else if (error instanceof NotFoundException) {
        toast.error(`${error.entityType} not found`);
      } else {
        toast.error("Something went wrong");
      }
    }
  };

  return <button onClick={() => handleTrack(5)}>Track</button>;
}
```

### Exception Flow Through Layers

```
┌─────────────────────────────────────────────────────────────┐
│ CLIENT (Presentation)                                       │
│ ✅ Catch specific exception types                           │
│ ✅ Access exception metadata (field, code, entityType)      │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ throw ValidationException
                            │ (preserved, not wrapped)
┌─────────────────────────────────────────────────────────────┐
│ DELIVERY LAYER (Server Actions)                            │
│ ✅ Preserve domain exceptions (DO NOT WRAP)                 │
│ ✅ Only wrap truly unexpected errors                        │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ throw ValidationException
                            │ (from use case)
┌─────────────────────────────────────────────────────────────┐
│ APPLICATION LAYER (Use Cases)                               │
│ ✅ Throw domain exceptions for business rules               │
│ ✅ Use specific exception types                             │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ uses
┌─────────────────────────────────────────────────────────────┐
│ DOMAIN LAYER (Entities, Value Objects, Exceptions)         │
│ ✅ Define domain exceptions                                 │
│ ✅ Encode business rules as exceptions                      │
└─────────────────────────────────────────────────────────────┘
```

### Benefits of Preserving Exception Types

1. **Type Safety** - Client code can catch specific types
2. **Rich Error Information** - Metadata preserved (field, code, entityId)
3. **Better UX** - Field-specific error messages
4. **Debugging** - Full stack traces maintained
5. **Testability** - Tests can verify specific exception types

### Lessons Learned (SonarLint PR #14)

**Files Fixed:**

- [app/\_actions/collections.ts](../../../app/_actions/collections.ts) - Preserved `ValidationException`, `DomainException`
- [app/\_actions/episodes.ts](../../../app/_actions/episodes.ts) - Preserved all domain exceptions
- [app/\_actions/diary.ts](../../../app/_actions/diary.ts) - Improved exception flow
- [app/\_actions/social.ts](../../../app/_actions/social.ts) - Unified error handling

**Impact:**

- Type-safe error handling across entire stack
- Better client-side error messages
- Zero SonarLint warnings
- Improved debugging in production

**Reference:** See [.traces/05-sonarlint-pr14-cleanup.md](../../../.traces/05-sonarlint-pr14-cleanup.md) for complete analysis.

---

## Value Objects and Entities

### Value Objects (Immutable, Identity-less)

Value Objects represent descriptive aspects of the domain with no conceptual identity.

```typescript
// core/domain/value-objects/Rating.ts
export class Rating {
  private readonly value: number;

  private constructor(value: number) {
    this.value = value;
  }

  static create(value: number): Rating {
    if (value < 1 || value > 5) {
      throw new InvalidRatingError("Rating must be between 1 and 5");
    }
    return new Rating(value);
  }

  getValue(): number {
    return this.value;
  }

  equals(other: Rating): boolean {
    return this.value === other.value;
  }

  isHighRating(): boolean {
    return this.value >= 4;
  }

  // Immutable - returns new instance
  increment(): Rating {
    return Rating.create(Math.min(this.value + 1, 5));
  }
}

// core/domain/value-objects/EmailAddress.ts
export class EmailAddress {
  private readonly value: string;

  private constructor(value: string) {
    this.value = value;
  }

  static create(email: string): EmailAddress {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      throw new InvalidEmailError(email);
    }
    return new EmailAddress(email.toLowerCase());
  }

  getValue(): string {
    return this.value;
  }

  getDomain(): string {
    return this.value.split("@")[1];
  }

  equals(other: EmailAddress): boolean {
    return this.value === other.value;
  }
}
```

### Entities (Identity-based)

Entities have a unique identity that runs through time and different representations.

```typescript
// core/domain/entities/User.ts
import { EmailAddress } from "@/core/domain/value-objects/EmailAddress";

export class User {
  private constructor(
    public readonly id: string,
    private _email: EmailAddress,
    private _name: string,
    private _isActive: boolean,
  ) {}

  static create(data: UserData): User {
    return new User(
      data.id,
      EmailAddress.create(data.email),
      data.name,
      data.isActive ?? true,
    );
  }

  updateEmail(newEmail: string): User {
    const email = EmailAddress.create(newEmail);
    return new User(this.id, email, this._name, this._isActive);
  }

  deactivate(): User {
    return new User(this.id, this._email, this._name, false);
  }

  get email(): string {
    return this._email.getValue();
  }

  get name(): string {
    return this._name;
  }

  get isActive(): boolean {
    return this._isActive;
  }

  // Entity equality is based on ID
  equals(other: User): boolean {
    return this.id === other.id;
  }
}
```

---

## Domain Services

When business logic doesn't naturally fit in an Entity or Value Object, use a Domain Service.

```typescript
// core/domain/services/EpisodeRecommendationService.ts
import { Episode } from "@/core/domain/entities/Episode";
import { User } from "@/core/domain/entities/User";

export class EpisodeRecommendationService {
  calculateRecommendationScore(
    episode: Episode,
    user: User,
    userHistory: Episode[],
  ): number {
    let score = 0;

    // Business rule: Prefer highly rated episodes
    if (episode.isHighlyRated) {
      score += 10;
    }

    // Business rule: Prefer similar seasons
    const watchedSeasons = userHistory.map((ep) => ep.season);
    if (watchedSeasons.includes(episode.season)) {
      score += 5;
    }

    // Business rule: Penalize already watched episodes
    const alreadyWatched = userHistory.some((ep) => ep.equals(episode));
    if (alreadyWatched) {
      score -= 20;
    }

    return score;
  }

  getTopRecommendations(
    availableEpisodes: Episode[],
    user: User,
    userHistory: Episode[],
    limit: number,
  ): Episode[] {
    const scored = availableEpisodes.map((episode) => ({
      episode,
      score: this.calculateRecommendationScore(episode, user, userHistory),
    }));

    return scored
      .sort((a, b) => b.score - a.score)
      .slice(0, limit)
      .map((item) => item.episode);
  }
}
```

---

## Dependency Injection in Next.js

### Manual DI (Simplest)

```typescript
// app/episodes/[id]/page.tsx
import { PrismaEpisodeRepository } from "@/infrastructure/prisma/repositories/PrismaEpisodeRepository";
import { GetEpisodeDetailsUseCase } from "@/core/application/use-cases/GetEpisodeDetailsUseCase";

export default async function EpisodePage({ params }: Props) {
  // Manual dependency injection
  const repository = new PrismaEpisodeRepository();
  const useCase = new GetEpisodeDetailsUseCase(repository);

  const episode = await useCase.execute({ id: params.id });

  return <EpisodeDetail episode={episode} />;
}
```

### Factory Pattern

```typescript
// infrastructure/factories/UseCaseFactory.ts
import { TrackEpisodeUseCase } from "@/core/application/use-cases/TrackEpisodeUseCase";
import { PrismaEpisodeRepository } from "@/infrastructure/prisma/repositories/PrismaEpisodeRepository";

export class UseCaseFactory {
  static createTrackEpisodeUseCase(): TrackEpisodeUseCase {
    const repository = new PrismaEpisodeRepository();
    return new TrackEpisodeUseCase(repository);
  }

  static createGetEpisodeDetailsUseCase(): GetEpisodeDetailsUseCase {
    const repository = new PrismaEpisodeRepository();
    return new GetEpisodeDetailsUseCase(repository);
  }
}

// Usage in Server Action
("use server");
import { UseCaseFactory } from "@/infrastructure/factories/UseCaseFactory";

export async function trackEpisode(episodeId: number, rating: number) {
  const useCase = UseCaseFactory.createTrackEpisodeUseCase();
  return useCase.execute({ episodeId, rating });
}
```

### DI Container (Advanced)

```typescript
// infrastructure/di/Container.ts
import { EpisodeRepository } from "@/core/application/ports/EpisodeRepository";
import { PrismaEpisodeRepository } from "@/infrastructure/prisma/repositories/PrismaEpisodeRepository";

class Container {
  private services = new Map<string, any>();

  register<T>(key: string, factory: () => T): void {
    this.services.set(key, factory);
  }

  resolve<T>(key: string): T {
    const factory = this.services.get(key);
    if (!factory) {
      throw new Error(`Service ${key} not registered`);
    }
    return factory();
  }
}

export const container = new Container();

// Register dependencies
container.register<EpisodeRepository>("EpisodeRepository", () => {
  return new PrismaEpisodeRepository();
});

// Usage
const repository = container.resolve<EpisodeRepository>("EpisodeRepository");
const useCase = new TrackEpisodeUseCase(repository);
```

---

## Testing Strategy by Layer

### Domain Layer Tests (Pure Unit Tests)

Domain tests are the easiest - no mocks, no database, pure logic.

```typescript
// core/domain/entities/Episode.test.ts
import { describe, it, expect } from "vitest";
import { Episode } from "./Episode";
import { InvalidRatingError } from "../exceptions/InvalidRatingError";

describe("Episode", () => {
  it("creates episode with valid data", () => {
    const episode = Episode.create({
      id: 1,
      title: "Simpsons Roasting on an Open Fire",
      season: 1,
      episodeNumber: 1,
      rating: 5,
    });

    expect(episode.title).toBe("Simpsons Roasting on an Open Fire");
    expect(episode.isHighlyRated).toBe(true);
  });

  it("throws error for invalid rating", () => {
    expect(() => {
      Episode.create({
        id: 1,
        title: "Test",
        season: 1,
        episodeNumber: 1,
        rating: 6, // Invalid!
      });
    }).toThrow(InvalidRatingError);
  });

  it("updates rating correctly", () => {
    const episode = Episode.create({
      id: 1,
      title: "Test",
      season: 1,
      episodeNumber: 1,
      rating: 3,
    });

    const updated = episode.updateRating(5);

    expect(updated.rating).toBe(5);
    expect(episode.rating).toBe(3); // Original unchanged (immutability)
  });
});
```

### Application Layer Tests (Use Cases with Mocks)

```typescript
// core/application/use-cases/TrackEpisodeUseCase.test.ts
import { describe, it, expect, vi } from "vitest";
import { TrackEpisodeUseCase } from "./TrackEpisodeUseCase";
import { EpisodeRepository } from "../ports/EpisodeRepository";
import { Episode } from "@/core/domain/entities/Episode";

describe("TrackEpisodeUseCase", () => {
  it("updates episode rating successfully", async () => {
    // Mock repository
    const mockRepository: EpisodeRepository = {
      findById: vi.fn().mockResolvedValue(
        Episode.create({
          id: 1,
          title: "Test",
          season: 1,
          episodeNumber: 1,
          rating: 3,
        }),
      ),
      save: vi.fn().mockResolvedValue(undefined),
      findTrending: vi.fn(),
    };

    const useCase = new TrackEpisodeUseCase(mockRepository);

    // Execute
    const result = await useCase.execute({
      episodeId: 1,
      rating: 5,
    });

    // Verify
    expect(result.newRating).toBe(5);
    expect(mockRepository.findById).toHaveBeenCalledWith(1);
    expect(mockRepository.save).toHaveBeenCalled();
  });

  it("throws error when episode not found", async () => {
    const mockRepository: EpisodeRepository = {
      findById: vi.fn().mockResolvedValue(null),
      save: vi.fn(),
      findTrending: vi.fn(),
    };

    const useCase = new TrackEpisodeUseCase(mockRepository);

    await expect(
      useCase.execute({ episodeId: 999, rating: 5 }),
    ).rejects.toThrow("Episode not found");
  });
});
```

### Infrastructure Layer Tests (Integration Tests)

```typescript
// infrastructure/prisma/repositories/PrismaEpisodeRepository.test.ts
import { describe, it, expect, beforeEach } from "vitest";
import { PrismaEpisodeRepository } from "./PrismaEpisodeRepository";
import { Episode } from "@/core/domain/entities/Episode";
import { prisma } from "@/app/_lib/prisma";

describe("PrismaEpisodeRepository", () => {
  let repository: PrismaEpisodeRepository;

  beforeEach(async () => {
    repository = new PrismaEpisodeRepository();
    // Clean database
    await prisma.episode.deleteMany();
  });

  it("saves and retrieves episode", async () => {
    // Create test data
    await prisma.episode.create({
      data: {
        id: 1,
        title: "Test Episode",
        season: 1,
        episode_number: 1,
        rating: 4,
      },
    });

    const episode = await repository.findById(1);

    expect(episode).not.toBeNull();
    expect(episode?.title).toBe("Test Episode");
    expect(episode?.rating).toBe(4);
  });

  it("returns null when episode not found", async () => {
    const episode = await repository.findById(999);
    expect(episode).toBeNull();
  });

  it("updates episode correctly", async () => {
    // Seed
    await prisma.episode.create({
      data: {
        id: 1,
        title: "Test",
        season: 1,
        episode_number: 1,
        rating: 3,
      },
    });

    // Update via repository
    const episode = Episode.create({
      id: 1,
      title: "Test",
      season: 1,
      episodeNumber: 1,
      rating: 5,
    });
    await repository.save(episode);

    // Verify
    const updated = await prisma.episode.findUnique({ where: { id: 1 } });
    expect(updated?.rating).toBe(5);
  });
});
```

---

## Migration Guide from Current Structure

### Step 1: Identify Domain Entities

**Current structure:**

```typescript
// app/_lib/repositories.ts
export async function findCharacterById(id: number) {
  return prisma.character.findUnique({ where: { id } });
}
```

**Target structure:**

```typescript
// 1. Create domain entity
// core/domain/entities/Character.ts
export class Character {
  private constructor(
    public readonly id: number,
    public readonly name: string,
    private _followersCount: number,
  ) {}

  static create(data: CharacterData): Character {
    return new Character(data.id, data.name, data.followersCount ?? 0);
  }

  incrementFollowers(): Character {
    return new Character(this.id, this.name, this._followersCount + 1);
  }

  get followersCount(): number {
    return this._followersCount;
  }
}

// 2. Define repository interface
// core/application/ports/CharacterRepository.ts
export interface CharacterRepository {
  findById(id: number): Promise<Character | null>;
  save(character: Character): Promise<void>;
}

// 3. Implement repository adapter
// infrastructure/prisma/repositories/PrismaCharacterRepository.ts
export class PrismaCharacterRepository implements CharacterRepository {
  async findById(id: number): Promise<Character | null> {
    const record = await prisma.character.findUnique({ where: { id } });
    return record ? CharacterMapper.toDomain(record) : null;
  }

  async save(character: Character): Promise<void> {
    await prisma.character.update({
      where: { id: character.id },
      data: { followers_count: character.followersCount },
    });
  }
}
```

### Step 2: Extract Use Cases from Server Actions

**Current structure:**

```typescript
// app/_actions/social.ts
"use server";
export async function followCharacter(characterId: number, userId: string) {
  const user = await getCurrentUser();
  if (!user) throw new Error("Not authenticated");

  await prisma.characterFollow.create({
    data: { userId: user.id, characterId },
  });

  revalidatePath(`/characters/${characterId}`);
}
```

**Target structure:**

```typescript
// 1. Create use case
// core/application/use-cases/FollowCharacterUseCase.ts
export class FollowCharacterUseCase {
  constructor(
    private characterRepository: CharacterRepository,
    private followRepository: FollowRepository,
  ) {}

  async execute(input: FollowCharacterInput): Promise<void> {
    // Business logic
    const character = await this.characterRepository.findById(
      input.characterId,
    );
    if (!character) {
      throw new CharacterNotFoundError(input.characterId);
    }

    const updatedCharacter = character.incrementFollowers();

    await this.followRepository.create(input.userId, input.characterId);
    await this.characterRepository.save(updatedCharacter);
  }
}

// 2. Server Action becomes thin controller
// app/_actions/social.ts
("use server");
export async function followCharacter(characterId: number) {
  const user = await getCurrentUser();
  if (!user) throw new Error("Not authenticated");

  const useCase = UseCaseFactory.createFollowCharacterUseCase();
  await useCase.execute({ characterId, userId: user.id });

  revalidatePath(`/characters/${characterId}`);
}
```

### Step 3: Progressive Migration Strategy

1. **Week 1-2:** Create core domain entities
   - Extract business rules from scattered code
   - Create entity classes with validation
   - Write domain tests

2. **Week 3-4:** Define application layer
   - Create use cases for critical flows
   - Define repository interfaces
   - Test use cases with mocks

3. **Week 5-6:** Implement infrastructure adapters
   - Create Prisma repository implementations
   - Create mappers for domain ↔ database
   - Write integration tests

4. **Week 7-8:** Refactor delivery layer
   - Update server actions to use use cases
   - Update pages to use repositories
   - Remove direct Prisma calls from app/

---

## Anti-Patterns to Avoid

### ❌ Anti-Pattern #1: Domain Depends on Framework

```typescript
// ❌ WRONG
// core/domain/entities/Episode.ts
import { prisma } from "@/app/_lib/prisma"; // NO!

export class Episode {
  async save() {
    await prisma.episode.update(...); // VIOLATION!
  }
}
```

**Why it's wrong:** Domain layer must be framework-agnostic.

**Solution:**

```typescript
// ✅ CORRECT
// core/domain/entities/Episode.ts - No imports!
export class Episode {
  // Pure business logic only
  updateRating(newRating: number): Episode {
    return new Episode(this.id, this.title, newRating);
  }
}

// infrastructure/prisma/repositories/PrismaEpisodeRepository.ts
export class PrismaEpisodeRepository {
  async save(episode: Episode) {
    await prisma.episode.update(...);
  }
}
```

### ❌ Anti-Pattern #2: Use Case Depends on Concrete Implementation

```typescript
// ❌ WRONG
import { PrismaEpisodeRepository } from "@/infrastructure/prisma";

export class TrackEpisodeUseCase {
  async execute(input: TrackEpisodeInput) {
    const repo = new PrismaEpisodeRepository(); // VIOLATION!
    await repo.save(...);
  }
}
```

**Why it's wrong:** Use case should depend on interface, not concrete class.

**Solution:**

```typescript
// ✅ CORRECT
import { EpisodeRepository } from "../ports/EpisodeRepository"; // Interface

export class TrackEpisodeUseCase {
  constructor(private repository: EpisodeRepository) {} // DI

  async execute(input: TrackEpisodeInput) {
    await this.repository.save(...);
  }
}
```

### ❌ Anti-Pattern #3: Anemic Domain Model

```typescript
// ❌ WRONG - Data structure, no behavior
export class Episode {
  id: number;
  title: string;
  rating: number;
}

// Business logic scattered in services
export class EpisodeService {
  updateRating(episode: Episode, newRating: number) {
    if (newRating < 1 || newRating > 5) {
      throw new Error("Invalid rating");
    }
    episode.rating = newRating;
  }
}
```

**Why it's wrong:** Business rules should live in domain entities.

**Solution:**

```typescript
// ✅ CORRECT - Rich domain model
export class Episode {
  private constructor(
    public readonly id: number,
    public readonly title: string,
    private _rating: number,
  ) {
    this.validateRating(_rating);
  }

  private validateRating(rating: number): void {
    if (rating < 1 || rating > 5) {
      throw new InvalidRatingError();
    }
  }

  updateRating(newRating: number): Episode {
    this.validateRating(newRating);
    return new Episode(this.id, this.title, newRating);
  }
}
```

### ❌ Anti-Pattern #4: Direct Database Calls in Pages

```typescript
// ❌ WRONG
import { prisma } from "@/app/_lib/prisma";

export default async function EpisodePage({ params }: Props) {
  const episode = await prisma.episode.findUnique({
    where: { id: params.id },
  });

  return <div>{episode.title}</div>;
}
```

**Why it's wrong:** Pages should orchestrate use cases, not access database directly.

**Solution:**

```typescript
// ✅ CORRECT
import { UseCaseFactory } from "@/infrastructure/factories/UseCaseFactory";

export default async function EpisodePage({ params }: Props) {
  const useCase = UseCaseFactory.createGetEpisodeDetailsUseCase();
  const episode = await useCase.execute({ id: params.id });

  return <div>{episode.title}</div>;
}
```

### ❌ Anti-Pattern #5: God Use Cases

```typescript
// ❌ WRONG - Too many responsibilities
export class EpisodeManagementUseCase {
  async createEpisode(data: EpisodeData) { ... }
  async updateEpisode(id: number, data: UpdateData) { ... }
  async deleteEpisode(id: number) { ... }
  async trackEpisode(id: number, rating: number) { ... }
  async shareEpisode(id: number, userId: string) { ... }
}
```

**Why it's wrong:** Use cases should represent single user intentions.

**Solution:**

```typescript
// ✅ CORRECT - One use case per user action
export class TrackEpisodeUseCase {
  async execute(input: TrackEpisodeInput) { ... }
}

export class ShareEpisodeUseCase {
  async execute(input: ShareEpisodeInput) { ... }
}

export class DeleteEpisodeUseCase {
  async execute(input: DeleteEpisodeInput) { ... }
}
```

---

## Real-World Example: Complete Feature

Let's implement "Track Episode with Rating" from scratch using Clean Architecture.

### 1. Domain Layer

```typescript
// core/domain/entities/Episode.ts
export class Episode {
  private constructor(
    public readonly id: number,
    public readonly title: string,
    private _rating: number,
    private _watchCount: number,
  ) {
    this.validateRating(_rating);
  }

  static create(data: EpisodeData): Episode {
    return new Episode(
      data.id,
      data.title,
      data.rating ?? 0,
      data.watchCount ?? 0,
    );
  }

  private validateRating(rating: number): void {
    if (rating < 0 || rating > 5) {
      throw new InvalidRatingError("Rating must be between 0 and 5");
    }
  }

  updateRating(newRating: number): Episode {
    this.validateRating(newRating);
    return new Episode(this.id, this.title, newRating, this._watchCount + 1);
  }

  get rating(): number {
    return this._rating;
  }

  get watchCount(): number {
    return this._watchCount;
  }

  get isHighlyRated(): boolean {
    return this._rating >= 4;
  }
}

// core/domain/value-objects/Rating.ts
export class Rating {
  private readonly value: number;

  private constructor(value: number) {
    this.value = value;
  }

  static create(value: number): Rating {
    if (value < 1 || value > 5) {
      throw new InvalidRatingError("Rating must be 1-5");
    }
    return new Rating(value);
  }

  getValue(): number {
    return this.value;
  }
}

// core/domain/exceptions/InvalidRatingError.ts
export class InvalidRatingError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "InvalidRatingError";
  }
}
```

### 2. Application Layer

```typescript
// core/application/ports/EpisodeRepository.ts
import { Episode } from "@/core/domain/entities/Episode";

export interface EpisodeRepository {
  findById(id: number): Promise<Episode | null>;
  save(episode: Episode): Promise<void>;
}

// core/application/ports/UserProgressRepository.ts
export interface UserProgressRepository {
  recordWatch(userId: string, episodeId: number, rating: number): Promise<void>;
}

// core/application/dtos/TrackEpisodeDTO.ts
export interface TrackEpisodeInput {
  userId: string;
  episodeId: number;
  rating: number;
}

export interface TrackEpisodeOutput {
  episodeId: number;
  newRating: number;
  watchCount: number;
}

// core/application/use-cases/TrackEpisodeUseCase.ts
import { Episode } from "@/core/domain/entities/Episode";
import { Rating } from "@/core/domain/value-objects/Rating";
import { EpisodeRepository } from "../ports/EpisodeRepository";
import { UserProgressRepository } from "../ports/UserProgressRepository";
import { TrackEpisodeInput, TrackEpisodeOutput } from "../dtos/TrackEpisodeDTO";

export class TrackEpisodeUseCase {
  constructor(
    private episodeRepository: EpisodeRepository,
    private progressRepository: UserProgressRepository,
  ) {}

  async execute(input: TrackEpisodeInput): Promise<TrackEpisodeOutput> {
    // 1. Validate rating using Value Object
    const rating = Rating.create(input.rating);

    // 2. Fetch episode
    const episode = await this.episodeRepository.findById(input.episodeId);
    if (!episode) {
      throw new EpisodeNotFoundError(input.episodeId);
    }

    // 3. Apply business logic (domain entity)
    const updatedEpisode = episode.updateRating(rating.getValue());

    // 4. Persist changes
    await this.episodeRepository.save(updatedEpisode);
    await this.progressRepository.recordWatch(
      input.userId,
      input.episodeId,
      rating.getValue(),
    );

    // 5. Return DTO
    return {
      episodeId: updatedEpisode.id,
      newRating: updatedEpisode.rating,
      watchCount: updatedEpisode.watchCount,
    };
  }
}
```

### 3. Infrastructure Layer

```typescript
// infrastructure/prisma/mappers/EpisodeMapper.ts
import { Episode } from "@/core/domain/entities/Episode";
import { Episode as PrismaEpisode } from "@prisma/client";

export class EpisodeMapper {
  static toDomain(prismaEpisode: PrismaEpisode): Episode {
    return Episode.create({
      id: prismaEpisode.id,
      title: prismaEpisode.title,
      rating: prismaEpisode.rating,
      watchCount: prismaEpisode.watch_count,
    });
  }

  static toPersistence(episode: Episode) {
    return {
      id: episode.id,
      title: episode.title,
      rating: episode.rating,
      watch_count: episode.watchCount,
    };
  }
}

// infrastructure/prisma/repositories/PrismaEpisodeRepository.ts
import { EpisodeRepository } from "@/core/application/ports/EpisodeRepository";
import { Episode } from "@/core/domain/entities/Episode";
import { prisma } from "@/app/_lib/prisma";
import { EpisodeMapper } from "../mappers/EpisodeMapper";

export class PrismaEpisodeRepository implements EpisodeRepository {
  async findById(id: number): Promise<Episode | null> {
    const record = await prisma.episode.findUnique({ where: { id } });
    return record ? EpisodeMapper.toDomain(record) : null;
  }

  async save(episode: Episode): Promise<void> {
    const data = EpisodeMapper.toPersistence(episode);
    await prisma.episode.update({
      where: { id: episode.id },
      data,
    });
  }
}

// infrastructure/prisma/repositories/PrismaUserProgressRepository.ts
import { UserProgressRepository } from "@/core/application/ports/UserProgressRepository";
import { prisma } from "@/app/_lib/prisma";

export class PrismaUserProgressRepository implements UserProgressRepository {
  async recordWatch(
    userId: string,
    episodeId: number,
    rating: number,
  ): Promise<void> {
    await prisma.userEpisodeProgress.upsert({
      where: {
        userId_episodeId: { userId, episodeId },
      },
      update: {
        rating,
        watchedAt: new Date(),
      },
      create: {
        userId,
        episodeId,
        rating,
        watchedAt: new Date(),
      },
    });
  }
}
```

### 4. Delivery Layer

```typescript
// infrastructure/factories/UseCaseFactory.ts
import { TrackEpisodeUseCase } from "@/core/application/use-cases/TrackEpisodeUseCase";
import { PrismaEpisodeRepository } from "@/infrastructure/prisma/repositories/PrismaEpisodeRepository";
import { PrismaUserProgressRepository } from "@/infrastructure/prisma/repositories/PrismaUserProgressRepository";

export class UseCaseFactory {
  static createTrackEpisodeUseCase(): TrackEpisodeUseCase {
    const episodeRepo = new PrismaEpisodeRepository();
    const progressRepo = new PrismaUserProgressRepository();
    return new TrackEpisodeUseCase(episodeRepo, progressRepo);
  }
}

// app/episodes/[id]/actions.ts
"use server";

import { getCurrentUser } from "@/app/_lib/auth";
import { UseCaseFactory } from "@/infrastructure/factories/UseCaseFactory";
import { revalidatePath } from "next/cache";

export async function trackEpisode(episodeId: number, rating: number) {
  const user = await getCurrentUser();
  if (!user) {
    throw new Error("Authentication required");
  }

  try {
    const useCase = UseCaseFactory.createTrackEpisodeUseCase();
    const result = await useCase.execute({
      userId: user.id,
      episodeId,
      rating,
    });

    revalidatePath(`/episodes/${episodeId}`);

    return { success: true, data: result };
  } catch (error) {
    return { success: false, error: (error as Error).message };
  }
}

// app/_components/EpisodeTracker.tsx
"use client";

import { trackEpisode } from "@/app/episodes/[id]/actions";
import { useFormAction } from "@/app/_lib/hooks";
import { Button } from "@/components/ui/button";

export function EpisodeTracker({ episodeId }: Props) {
  const { execute, isPending, error } = useFormAction(
    async (rating: number) => trackEpisode(episodeId, rating)
  );

  return (
    <div>
      {[1, 2, 3, 4, 5].map((rating) => (
        <Button
          key={rating}
          onClick={() => execute(rating)}
          disabled={isPending}
        >
          {rating} ⭐
        </Button>
      ))}
      {error && <p className="text-red-500">{error.message}</p>}
    </div>
  );
}
```

---

## Quick Reference

### Layer Checklist

| Layer              | Can Import From     | Cannot Import From       | Contains                                 |
| ------------------ | ------------------- | ------------------------ | ---------------------------------------- |
| **Domain**         | Nothing             | Everything               | Entities, Value Objects, Domain Services |
| **Application**    | Domain              | Infrastructure, Delivery | Use Cases, Ports (interfaces), DTOs      |
| **Infrastructure** | Domain, Application | Delivery                 | Repositories, Adapters, Mappers          |
| **Delivery**       | All layers          | Nothing (it's outermost) | Pages, Components, Server Actions        |

### When to Create What

- **Entity:** When object has unique identity and lifecycle
- **Value Object:** When object is immutable and compared by value
- **Domain Service:** When business logic doesn't fit in entity
- **Use Case:** For each user intention/action
- **Repository Interface:** For each aggregate root entity
- **Repository Implementation:** One per data source (Prisma, REST API, etc.)

### Dependency Rule Validation

```typescript
// ✅ ALLOWED
import { Episode } from "@/core/domain/entities/Episode"; // Any layer → Domain
import { TrackEpisodeUseCase } from "@/core/application/use-cases/TrackEpisodeUseCase"; // Infrastructure/Delivery → Application
import { PrismaEpisodeRepository } from "@/infrastructure/prisma/repositories/PrismaEpisodeRepository"; // Delivery → Infrastructure

// ❌ FORBIDDEN
import { prisma } from "@/app/_lib/prisma"; // Domain → Infrastructure
import { trackEpisode } from "@/app/episodes/actions"; // Domain/Application → Delivery
import { PrismaEpisodeRepository } from "@/infrastructure/prisma"; // Application → Infrastructure concrete class
```

### File Naming Conventions

- Entities: `Episode.ts`, `Character.ts` (PascalCase, singular)
- Value Objects: `Rating.ts`, `EmailAddress.ts` (PascalCase)
- Use Cases: `TrackEpisodeUseCase.ts`, `GetEpisodeDetailsUseCase.ts`
- Repositories: `EpisodeRepository.ts` (interface), `PrismaEpisodeRepository.ts` (implementation)
- DTOs: `TrackEpisodeDTO.ts`, `EpisodeDetailsDTO.ts`
- Mappers: `EpisodeMapper.ts`, `CharacterMapper.ts`

---

## Comparison: Clean Architecture vs DDD

| Aspect           | Clean Architecture                                                      | DDD (Domain-Driven Design)   |
| ---------------- | ----------------------------------------------------------------------- | ---------------------------- |
| **Focus**        | Layer separation, Dependency Rule                                       | Business domain modeling     |
| **Structure**    | Concentric circles (layers)                                             | Bounded contexts, aggregates |
| **Key Concept**  | Dependencies point inward                                               | Ubiquitous language          |
| **Entities**     | Objects with identity                                                   | Rich domain models           |
| **Use Cases**    | Application-specific business rules                                     | Domain services              |
| **Main Goal**    | Framework independence                                                  | Domain understanding         |
| **Can Combine?** | ✅ Yes - Clean Architecture defines layers, DDD organizes within layers |

**Recommendation:** Use both together:

- Clean Architecture for layer separation
- DDD for organizing domain logic within those layers

---

## Security with Clean Architecture: Row Level Security (RLS) Layer

Clean Architecture naturally accommodates security concerns through layered separation. Row Level Security (RLS) becomes the "security enforcement layer" sitting between application logic and database.

### Architecture with RLS Integration

```
┌──────────────────────────────────────────────────┐
│  Delivery Layer (Server Actions, API Routes)    │
│  • Validates input with Zod                      │
│  • Calls Application layer use cases             │
│  • Catches and returns errors cleanly            │
├──────────────────────────────────────────────────┤
│  Application Layer (Use Cases)                   │
│  • Implements business logic                     │
│  • Calls Infrastructure for data                 │
│  • Zero knowledge of RLS or database             │
├──────────────────────────────────────────────────┤
│  RLS Security Layer (Prisma Transactions)       │
│  • Sets app.current_user_id context             │
│  • Wraps all database transactions               │
│  • Enforces authentication checks                │
├──────────────────────────────────────────────────┤
│  Infrastructure Layer (Repositories)             │
│  • Executes queries via RLS context             │
│  • Cannot bypass security (DB enforced)         │
│  • Returns domain entities                       │
└──────────────────────────────────────────────────┘
```

### Why RLS Belongs in Clean Architecture

**RLS = Security Boundary:**

- Not application logic (doesn't belong in Application layer)
- Not delivery (doesn't belong in Server Actions)
- Is infrastructure concern (database access layer)
- Provides "policy enforcement" at Infrastructure level

**Clean Architecture + RLS Benefits:**

1. **Single Responsibility:** Each layer has one reason to change
   - Application: business rules change
   - RLS: security policies change
   - Infrastructure: query optimization changes

2. **Dependency Rule:** RLS respects inward dependencies
   - Domain ← Application ← Infrastructure (with RLS) ← Delivery
   - RLS policies never expose domain entities
   - Policies are implementation detail

3. **Testability:** Layered approach enables isolation
   - Unit test: Application logic without RLS (mock repo)
   - Integration test: RLS policies with real database
   - E2E test: Full flow through Delivery

4. **Flexibility:** Swap security layer without changing logic
   - Replace RLS with API key auth? Change Infrastructure only
   - Modify policies? Change database only
   - Application layer doesn't care

### Pattern: Use Cases with RLS

```typescript
// ✅ CORRECT - Clean Architecture + RLS

// core/domain/entities/DiaryEntry.ts
export class DiaryEntry {
  constructor(
    public id: string,
    public userId: string,
    public content: string,
    public createdAt: Date
  ) {}

  isOwnedBy(userId: string): boolean {
    return this.userId === userId;
  }
}

// core/application/use-cases/AddDiaryEntryUseCase.ts
import { DiaryEntryRepository } from "@/infrastructure/repositories/DiaryEntryRepository";

export class AddDiaryEntryUseCase {
  constructor(private repository: DiaryEntryRepository) {}

  async execute(input: {
    content: string;
    userId: string;
  }): Promise<DiaryEntry> {
    // Pure business logic - no RLS knowledge
    if (!input.content) {
      throw new InvalidInputError("Content required");
    }

    // Call repository to persist
    return this.repository.create({
      userId: input.userId,
      content: input.content,
    });
  }
}

// infrastructure/repositories/DiaryEntryRepository.ts
import { withAuthenticatedRLS } from "@/app/_lib/prisma-rls";

export class DiaryEntryRepository {
  async create(data: {
    userId: string;
    content: string;
  }): Promise<DiaryEntry> {
    // RLS enforcement happens HERE
    return withAuthenticatedRLS(async (tx) => {
      const created = await tx.diaryEntry.create({
        data: {
          userId: data.userId,
          content: data.content,
        },
      });

      return new DiaryEntry(
        created.id,
        created.userId,
        created.content,
        created.createdAt
      );
    });
  }

  async findById(id: string, userId: string): Promise<DiaryEntry | null> {
    // RLS ensures only user's own entries are returned
    return withAuthenticatedRLS(async (tx) => {
      const entry = await tx.diaryEntry.findUnique({
        where: { id },
      });

      if (!entry) return null;

      // Extra validation (defensive programming)
      if (!new DiaryEntry(...).isOwnedBy(userId)) {
        throw new UnauthorizedError();
      }

      return entry;
    });
  }
}

// app/_actions/diary.ts (Delivery Layer)
"use server";
import { z } from "zod";
import { AddDiaryEntryUseCase } from "@/core/application/use-cases/AddDiaryEntryUseCase";
import { DiaryEntryRepository } from "@/infrastructure/repositories/DiaryEntryRepository";

const AddEntrySchema = z.object({
  content: z.string().min(10).max(1000),
});

export async function addDiaryEntry(
  input: z.infer<typeof AddEntrySchema>
) {
  try {
    const { content } = AddEntrySchema.parse(input);
    const user = await getCurrentUser();

    if (!user) throw new Error("Unauthorized");

    // Instantiate use case
    const useCase = new AddDiaryEntryUseCase(
      new DiaryEntryRepository()
    );

    // Execute - RLS happens inside repository
    const entry = await useCase.execute({
      content,
      userId: user.id,
    });

    return { success: true, data: entry };
  } catch (error) {
    return { success: false, error: error.message };
  }
}
```

### RLS Testing in Clean Architecture

```typescript
// Unit test: Pure business logic (no RLS)
describe("AddDiaryEntryUseCase", () => {
  it("validates input", async () => {
    const mockRepo = {
      create: vi.fn(),
    };

    const useCase = new AddDiaryEntryUseCase(mockRepo);
    await expect(
      useCase.execute({ content: "", userId: "user1" }),
    ).rejects.toThrow("Content required");
  });
});

// Integration test: RLS enforcement
describe("DiaryEntryRepository with RLS", () => {
  it("prevents cross-user access", async () => {
    const userA = "user-a";
    const userB = "user-b";

    // User A creates entry
    const repo = new DiaryEntryRepository();
    await repo.create({
      userId: userA,
      content: "User A's secret",
    });

    // User B cannot read it (RLS enforced)
    const entry = await repo.findById(entryId, userB);
    expect(entry).toBeNull();
  });
});
```

### Lessons Learned: RLS + Clean Architecture

1. **RLS is Infrastructure Concern:** Belongs in the data layer, not business logic
2. **Policies are Implementation Details:** Use cases don't know about RLS
3. **Layering Enables Testing:** Unit test without DB, integration test with DB
4. **Single Responsibility:** Keep security logic separate from business logic
5. **Dependency Rule:** RLS layer sits between Application and Database

**Key Takeaway:** Clean Architecture + RLS = Maximum Security with Minimum Coupling

---

## Summary

Clean Architecture ensures:

1. **Business logic independence** - Domain is framework-agnostic
2. **Testability** - Each layer can be tested in isolation
3. **Flexibility** - Easy to swap frameworks, databases, UI
4. **Maintainability** - Clear boundaries reduce coupling
5. **Scalability** - Separation of concerns enables growth
6. **Security** - RLS sits naturally in Infrastructure layer

**Golden Rules:**

- Dependencies point inward only
- Domain has zero external dependencies
- Application defines interfaces, Infrastructure implements
- Delivery layer orchestrates, doesn't contain business logic
- Use cases represent single user intentions
- Entities contain business rules, not just data
- RLS policies enforce data isolation at Infrastructure boundary

Start small, migrate progressively, and prioritize critical flows first.
