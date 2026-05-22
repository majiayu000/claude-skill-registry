---
name: CQRS Command Query Generator
description: Génère des Commands, Queries et Handlers suivant le pattern CQRS (Command Query Responsibility Segregation). À utiliser lors de la création de use cases, commands, queries, handlers, read models, ou quand l'utilisateur mentionne "CQRS", "command", "query", "handler", "use case", "read model".
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# CQRS Command Query Generator

## 🎯 Mission

Créer des Commands et Queries suivant le pattern CQRS pour séparer les opérations d'écriture (commands) des opérations de lecture (queries) dans l'Application Layer.

## 📚 Philosophie CQRS (Command Query Responsibility Segregation)

### Principe Fondamental

**CQRS** sépare les responsabilités en deux types d'opérations :

1. **Commands** (Écritures) : Modifient l'état du système
   - Create, Update, Delete
   - Retournent un ID ou un booléen de succès
   - Peuvent échouer (validation, business rules)

2. **Queries** (Lectures) : Lisent l'état du système
   - Get, List, Search
   - Retournent des Read Models (DTOs optimisés)
   - Ne modifient JAMAIS l'état

### Avantages

- ✅ **Séparation claire** : Écritures vs Lectures
- ✅ **Optimisation indépendante** : Read Models optimisés pour l'UI
- ✅ **Scalabilité** : Possibilité de scaler reads et writes séparément
- ✅ **Payloads minimaux** : Commands retournent juste un ID
- ✅ **Maintenabilité** : Ajout de nouvelles opérations sans affecter l'existant

### Architecture CQRS dans le Projet

```
application/
├── commands/               # Write operations
│   └── create-club/
│       ├── create-club.command.ts        # Command DTO
│       ├── create-club.handler.ts        # Command Handler
│       └── create-club.spec.ts           # Tests
├── queries/                # Read operations
│   └── get-club/
│       ├── get-club.query.ts             # Query DTO
│       ├── get-club.handler.ts           # Query Handler
│       └── get-club.spec.ts              # Tests
└── read-models/            # Optimized DTOs for UI
    ├── club-detail.read-model.ts
    ├── club-list.read-model.ts
    └── index.ts
```

## 🖊️ Commands (Write Operations)

### Qu'est-ce qu'un Command ?

Un **Command** représente l'intention de l'utilisateur de **modifier l'état** du système.

**Caractéristiques** :
- Nommé avec un **verbe d'action** : `CreateClub`, `UpdateSubscription`, `DeleteMember`
- Contient **toutes les données** nécessaires à l'opération
- **Validé** avec class-validator
- **Immuable** (DTO, pas de setters)
- **Co-localisé** avec son handler dans le même dossier

### Template Command

```typescript
// application/commands/create-club/create-club.command.ts

import { IsString, IsNotEmpty, IsOptional, MaxLength } from 'class-validator';

export class CreateClubCommand {
  @IsString()
  @IsNotEmpty()
  @MaxLength(100)
  readonly name: string;

  @IsString()
  @IsOptional()
  @MaxLength(500)
  readonly description?: string;

  @IsString()
  @IsNotEmpty()
  readonly userId: string; // ID de l'utilisateur qui crée le club

  constructor(name: string, description: string | undefined, userId: string) {
    this.name = name;
    this.description = description;
    this.userId = userId;
  }
}
```

### Template Command Handler

```typescript
// application/commands/create-club/create-club.handler.ts

import { Injectable, Inject } from '@nestjs/common';
import { CreateClubCommand } from './create-club.command';
import { IClubRepository, CLUB_REPOSITORY } from '../../domain/repositories/club.repository.interface';
import { Club } from '../../domain/entities/club.entity';
import { ClubName } from '../../domain/value-objects/club-name.vo';

@Injectable()
export class CreateClubHandler {
  constructor(
    @Inject(CLUB_REPOSITORY)
    private readonly clubRepository: IClubRepository,
  ) {}

  async execute(command: CreateClubCommand): Promise<string> {
    // 1. Créer l'entité domain avec la logique métier
    const clubName = ClubName.create(command.name);
    const club = Club.create(
      clubName,
      command.description,
      command.userId,
    );

    // 2. Persister via le repository
    const savedClub = await this.clubRepository.create(club);

    // 3. Retourner UNIQUEMENT l'ID (payload minimal)
    return savedClub.getId();
  }
}
```

### Règles pour les Commands

- ✅ Un Command = Une responsabilité unique
- ✅ Validation avec class-validator
- ✅ Retourne un ID (string) ou void
- ✅ Orchestre les entités domain (pas de logique métier)
- ✅ Gère les erreurs métier (throw domain exceptions)
- ❌ **JAMAIS** de logique métier (celle-ci est dans le Domain)
- ❌ **JAMAIS** de retour de Read Model (utiliser une Query après)
- ❌ **JAMAIS** d'accès direct à Prisma (utiliser le repository)

### Exemples de Commands

```typescript
// Write operations (modifient l'état)
CreateClubCommand
UpdateClubCommand
DeleteClubCommand
SubscribeToPlanCommand
UpgradeSubscriptionCommand
GenerateInvitationCommand
AcceptInvitationCommand
RemoveMemberCommand
ChangeClubCommand
```

## 📖 Queries (Read Operations)

### Qu'est-ce qu'une Query ?

Une **Query** représente l'intention de l'utilisateur de **lire des données** sans modifier l'état.

**Caractéristiques** :
- Nommée avec l'intention de lecture : `GetClub`, `ListClubs`, `SearchMembers`
- Contient les **paramètres de filtrage** (pagination, sorting, filtering)
- **Validée** avec class-validator
- **Immuable** (DTO)
- **Co-localisée** avec son handler

### Template Query

```typescript
// application/queries/list-clubs/list-clubs.query.ts

import { IsOptional, IsNumber, Min, Max, IsString } from 'class-validator';

export class ListClubsQuery {
  @IsOptional()
  @IsNumber()
  @Min(1)
  readonly page?: number = 1;

  @IsOptional()
  @IsNumber()
  @Min(1)
  @Max(100)
  readonly limit?: number = 10;

  @IsOptional()
  @IsString()
  readonly search?: string;

  @IsOptional()
  @IsString()
  readonly userId?: string; // Filtrer par utilisateur

  constructor(page?: number, limit?: number, search?: string, userId?: string) {
    this.page = page ?? 1;
    this.limit = limit ?? 10;
    this.search = search;
    this.userId = userId;
  }
}
```

### Template Query Handler

```typescript
// application/queries/list-clubs/list-clubs.handler.ts

import { Injectable, Inject } from '@nestjs/common';
import { ListClubsQuery } from './list-clubs.query';
import { IClubRepository, CLUB_REPOSITORY } from '../../domain/repositories/club.repository.interface';
import { ClubListReadModel } from '../../read-models/club-list.read-model';
import { PaginatedResult } from '../../../shared/types/paginated-result';

@Injectable()
export class ListClubsHandler {
  constructor(
    @Inject(CLUB_REPOSITORY)
    private readonly clubRepository: IClubRepository,
  ) {}

  async execute(query: ListClubsQuery): Promise<PaginatedResult<ClubListReadModel>> {
    // 1. Récupérer les entités domain via le repository
    const result = await this.clubRepository.findAll({
      page: query.page,
      limit: query.limit,
      search: query.search,
      userId: query.userId,
    });

    // 2. Transformer les entités en Read Models (optimisés pour l'UI)
    const data = result.data.map(club => this.toReadModel(club));

    // 3. Retourner les Read Models avec métadonnées de pagination
    return {
      data,
      meta: {
        page: query.page,
        limit: query.limit,
        total: result.total,
        totalPages: Math.ceil(result.total / query.limit),
      },
    };
  }

  private toReadModel(club: Club): ClubListReadModel {
    return {
      id: club.getId(),
      name: club.getName().getValue(),
      description: club.getDescription(),
      membersCount: club.getMembersCount(),
      createdAt: club.getCreatedAt(),
    };
  }
}
```

### Règles pour les Queries

- ✅ Une Query = Une intention de lecture
- ✅ Retourne des Read Models (JAMAIS les entités domain)
- ✅ Transforme Domain Entities → Read Models
- ✅ Optimise pour l'UI (sélection des champs pertinents)
- ✅ Supporte pagination, filtrage, sorting
- ❌ **JAMAIS** de modification d'état
- ❌ **JAMAIS** de retour des entités domain brutes
- ❌ **JAMAIS** de logique métier

### Exemples de Queries

```typescript
// Read operations (ne modifient PAS l'état)
GetClubQuery
ListClubsQuery
GetSubscriptionQuery
ValidateInvitationQuery
ListMembersQuery
SearchClubsQuery
```

## 📊 Read Models (Optimized DTOs)

### Qu'est-ce qu'un Read Model ?

Un **Read Model** est un **DTO optimisé** pour une vue spécifique de l'UI.

**Caractéristiques** :
- Séparé des entités domain
- Optimisé pour une utilisation spécifique (liste, détail, card, etc.)
- Peut agréger des données de plusieurs entités
- Plain TypeScript interface (pas de validation)
- Nommé avec le suffixe `ReadModel`

### Template Read Model

```typescript
// application/read-models/club-detail.read-model.ts

export interface ClubDetailReadModel {
  id: string;
  name: string;
  description: string | null;
  createdAt: Date;

  // Owner info
  owner: {
    id: string;
    name: string;
    email: string;
  };

  // Subscription info (agrégation)
  subscription: {
    plan: string;
    status: string;
    maxTeams: number;
    currentTeamsCount: number;
  };

  // Members count
  membersCount: number;

  // Teams info
  teams: {
    id: string;
    name: string;
    category: string;
  }[];
}
```

```typescript
// application/read-models/club-list.read-model.ts

export interface ClubListReadModel {
  id: string;
  name: string;
  description: string | null;
  membersCount: number;
  createdAt: Date;
}
```

```typescript
// application/read-models/index.ts

export * from './club-detail.read-model';
export * from './club-list.read-model';
export * from './subscription-status.read-model';
export * from './member-list.read-model';
```

### Règles pour les Read Models

- ✅ Une Read Model par vue UI spécifique
- ✅ Sélection des champs pertinents uniquement
- ✅ Agrégation de données de plusieurs entités si nécessaire
- ✅ Types primitifs (string, number, boolean, Date)
- ✅ Nested objects si nécessaire pour l'UI
- ❌ **JAMAIS** de méthodes (pure data)
- ❌ **JAMAIS** de validation decorators (class-validator)
- ❌ **JAMAIS** de logique métier

## 🔗 Intégration avec les Controllers

### Comment utiliser Commands et Queries dans les Controllers

```typescript
// presentation/controllers/clubs.controller.ts

import { Controller, Post, Get, Put, Delete, Body, Param, Query, UseGuards } from '@nestjs/common';
import { JwtAuthGuard } from '../../auth/guards/jwt-auth.guard';
import { CreateClubCommand } from '../../application/commands/create-club/create-club.command';
import { CreateClubHandler } from '../../application/commands/create-club/create-club.handler';
import { UpdateClubCommand } from '../../application/commands/update-club/update-club.command';
import { UpdateClubHandler } from '../../application/commands/update-club/update-club.handler';
import { GetClubQuery } from '../../application/queries/get-club/get-club.query';
import { GetClubHandler } from '../../application/queries/get-club/get-club.handler';
import { ListClubsQuery } from '../../application/queries/list-clubs/list-clubs.query';
import { ListClubsHandler } from '../../application/queries/list-clubs/list-clubs.handler';

@Controller('clubs')
@UseGuards(JwtAuthGuard)
export class ClubsController {
  constructor(
    // Inject handlers (NOT use cases)
    private readonly createClubHandler: CreateClubHandler,
    private readonly updateClubHandler: UpdateClubHandler,
    private readonly getClubHandler: GetClubHandler,
    private readonly listClubsHandler: ListClubsHandler,
  ) {}

  // Command - Retourne un ID uniquement
  @Post()
  async create(@Body() command: CreateClubCommand) {
    const id = await this.createClubHandler.execute(command);
    return { id }; // Payload minimal
  }

  // Command - Retourne un ID uniquement
  @Put(':id')
  async update(@Param('id') id: string, @Body() command: UpdateClubCommand) {
    const updatedId = await this.updateClubHandler.execute(command);
    return { id: updatedId };
  }

  // Query - Retourne un Read Model
  @Get(':id')
  async findOne(@Param('id') id: string) {
    const query = new GetClubQuery(id);
    return this.getClubHandler.execute(query); // Read Model
  }

  // Query - Retourne une liste de Read Models avec pagination
  @Get()
  async findAll(@Query() params: any) {
    const query = new ListClubsQuery(
      params.page,
      params.limit,
      params.search,
      params.userId,
    );
    return this.listClubsHandler.execute(query); // PaginatedResult<ReadModel>
  }
}
```

### Règles pour l'intégration Controller

- ✅ Injecter les Handlers (pas les use cases)
- ✅ Commands retournent `{ id: string }`
- ✅ Queries retournent Read Models directement
- ✅ Validation automatique via class-validator (NestJS)
- ❌ **JAMAIS** de logique métier dans le controller
- ❌ **JAMAIS** de mapping manuel (le handler s'en charge)

## 🔧 Module Configuration

### Enregistrer les Handlers comme Providers

```typescript
// club-management.module.ts

import { Module } from '@nestjs/common';
import { PrismaModule } from '../prisma/prisma.module';

// Controllers
import { ClubsController } from './presentation/controllers/clubs.controller';

// Command Handlers
import { CreateClubHandler } from './application/commands/create-club/create-club.handler';
import { UpdateClubHandler } from './application/commands/update-club/update-club.handler';
import { DeleteClubHandler } from './application/commands/delete-club/delete-club.handler';

// Query Handlers
import { GetClubHandler } from './application/queries/get-club/get-club.handler';
import { ListClubsHandler } from './application/queries/list-clubs/list-clubs.handler';

// Repositories
import { ClubRepository } from './infrastructure/persistence/repositories/club.repository';
import { CLUB_REPOSITORY } from './domain/repositories/club.repository.interface';

@Module({
  imports: [PrismaModule],
  controllers: [ClubsController],
  providers: [
    // Repository binding
    {
      provide: CLUB_REPOSITORY,
      useClass: ClubRepository,
    },

    // Command Handlers
    CreateClubHandler,
    UpdateClubHandler,
    DeleteClubHandler,

    // Query Handlers
    GetClubHandler,
    ListClubsHandler,
  ],
  exports: [
    CLUB_REPOSITORY,
  ],
})
export class ClubManagementModule {}
```

## ✅ Checklist CQRS

### Commands
- [ ] Command nommé avec un verbe d'action (CreateX, UpdateX, DeleteX)
- [ ] DTO validé avec class-validator
- [ ] Handler orchestre les entités domain
- [ ] Retourne un ID (string) ou void
- [ ] Pas de logique métier dans le handler
- [ ] Co-localisé avec son handler

### Queries
- [ ] Query nommée avec intention de lecture (GetX, ListX, SearchX)
- [ ] Supporte pagination/filtrage si liste
- [ ] Handler transforme Domain Entities → Read Models
- [ ] Retourne Read Models (pas les entités brutes)
- [ ] Pas de modification d'état
- [ ] Co-localisée avec son handler

### Read Models
- [ ] Interface TypeScript (pas de class)
- [ ] Optimisé pour une vue UI spécifique
- [ ] Champs pertinents uniquement
- [ ] Peut agréger plusieurs entités
- [ ] Pas de validation decorators
- [ ] Exporté via barrel (index.ts)

### Handlers
- [ ] Injectent les repository interfaces (pas les implémentations)
- [ ] Gèrent les erreurs métier
- [ ] Tests unitaires présents
- [ ] Un handler par command/query

## 🎓 Exemples Concrets du Projet

### Bounded Context `club-management`

**Commands** :
- `create-club` : Créer un nouveau club
- `update-club` : Mettre à jour les informations d'un club
- `delete-club` : Supprimer un club
- `subscribe-to-plan` : Souscrire à un plan d'abonnement
- `upgrade-subscription` : Upgrader un plan d'abonnement
- `generate-invitation` : Générer une invitation
- `accept-invitation` : Accepter une invitation
- `remove-member` : Retirer un membre
- `change-club` : Changer de club

**Queries** :
- `get-club` : Récupérer les détails d'un club
- `list-clubs` : Lister les clubs (avec pagination)
- `get-subscription` : Récupérer le statut d'abonnement
- `list-subscription-plans` : Lister les plans disponibles
- `validate-invitation` : Valider une invitation
- `list-members` : Lister les membres d'un club

**Read Models** :
- `ClubDetailReadModel` : Vue détaillée d'un club
- `ClubListReadModel` : Vue liste des clubs
- `SubscriptionStatusReadModel` : Statut d'abonnement
- `MemberListReadModel` : Liste des membres

Référence : `volley-app-backend/src/club-management/application/`

## 🚨 Erreurs Courantes à Éviter

1. ❌ **Command qui retourne un Read Model**
   - ✅ FAIRE : Command retourne `{ id: string }`, puis Query séparée pour récupérer le Read Model
   - ❌ NE PAS FAIRE : Command retourne l'entité complète ou le Read Model

2. ❌ **Query qui modifie l'état**
   - ✅ FAIRE : Query lit uniquement, jamais de modification
   - ❌ NE PAS FAIRE : `GetAndMarkAsReadQuery` (séparé en Query + Command)

3. ❌ **Logique métier dans le Handler**
   - ✅ FAIRE : `club.upgrade(newPlan)` (logique dans l'entité)
   - ❌ NE PAS FAIRE : Validation métier dans le handler

4. ❌ **Handler qui appelle Prisma directement**
   - ✅ FAIRE : `await this.clubRepository.create(club)`
   - ❌ NE PAS FAIRE : `await this.prisma.club.create(...)`

5. ❌ **Read Model = Domain Entity**
   - ✅ FAIRE : Read Model optimisé pour l'UI, différent de l'entité
   - ❌ NE PAS FAIRE : Retourner l'entité domain brute au client

## 📚 Skills Complémentaires

Pour aller plus loin :
- **ddd-bounded-context** : Architecture DDD complète avec bounded contexts
- **ddd-testing** : Standards de tests pour Commands/Queries/Handlers
- **prisma-mapper** : Patterns de mappers Domain ↔ Prisma

---

**Rappel** : CQRS sépare les **Écritures** (Commands) des **Lectures** (Queries) pour une architecture plus claire, scalable et maintenable.
