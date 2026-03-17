---
name: DDD Bounded Context Generator
description: Génère des bounded contexts DDD complets avec architecture en couches (Domain, Application, Infrastructure, Presentation). À utiliser lors de la création de nouvelles features backend, bounded contexts, domain entities, ou quand l'utilisateur mentionne "DDD", "bounded context", "domain model", "clean architecture", "layered architecture".
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# DDD Bounded Context Generator

## 🎯 Mission

Créer des bounded contexts backend suivant rigoureusement les principes DDD (Domain-Driven Design) avec une architecture en couches propre et maintenable.

## 🏗️ Architecture DDD du Projet

### Philosophie DDD

Le backend suit les principes DDD avec une séparation stricte des responsabilités :
- **Bounded Contexts** : Chaque feature majeure est un bounded context isolé
- **Layered Architecture** : 4 couches avec dépendances unidirectionnelles vers l'intérieur
- **Rich Domain Models** : Les entités contiennent la logique métier
- **Framework-Agnostic Domain** : Le domain ne dépend d'aucun framework

### Structure d'un Bounded Context

```
volley-app-backend/src/[bounded-context]/
├── domain/
│   ├── entities/           # Entités riches avec logique métier
│   ├── value-objects/      # Value Objects immuables
│   ├── repositories/       # Interfaces de repositories (PAS d'implémentation)
│   ├── services/           # Domain Services pour logique complexe
│   └── exceptions/         # Exceptions métier custom
├── application/
│   ├── commands/           # Opérations d'écriture (CQRS)
│   │   └── create-foo/
│   │       ├── create-foo.command.ts
│   │       └── create-foo.handler.ts
│   ├── queries/            # Opérations de lecture (CQRS)
│   │   └── get-foo/
│   │       ├── get-foo.query.ts
│   │       └── get-foo.handler.ts
│   └── read-models/        # DTOs optimisés pour l'UI
├── infrastructure/
│   ├── persistence/
│   │   ├── repositories/   # Implémentations des repositories
│   │   └── mappers/        # Mappers Domain ↔ Prisma
│   └── [external-services]/
├── presentation/
│   └── controllers/        # Controllers HTTP (NestJS)
├── tests/
│   ├── unit/
│   │   ├── domain/         # Tests des entités et services
│   │   └── application/    # Tests des handlers
│   └── integration/        # Tests Handler → Repository → DB
└── [bounded-context].module.ts
```

## 📐 Layered Architecture - Règles Strictes

### Flow de Dépendances (CRITIQUE)

```
Presentation → Application → Domain ← Infrastructure
```

- ✅ **Autorisé** : Les couches externes dépendent des couches internes
- ❌ **INTERDIT** : Le Domain ne doit JAMAIS dépendre des couches externes

### 1. Domain Layer (Cœur Métier)

**Responsabilité** : Contenir toute la logique métier de l'application

**Contenu** :
- **Entities** : Modèles riches avec méthodes métier
- **Value Objects** : Objets immuables représentant des concepts métier
- **Repository Interfaces** : Contrats pour la persistence (PAS d'implémentation)
- **Domain Services** : Logique métier complexe impliquant plusieurs entités
- **Domain Exceptions** : Exceptions métier custom

**Règles STRICTES** :
- ✅ Pure TypeScript (aucune dépendance externe)
- ✅ Logique métier encapsulée dans les entités
- ✅ Value Objects immuables et validés
- ✅ Interfaces de repositories uniquement
- ❌ **JAMAIS** de dépendances vers NestJS
- ❌ **JAMAIS** de dépendances vers Prisma
- ❌ **JAMAIS** de dépendances vers les couches externes
- ❌ **JAMAIS** de code infrastructure (DB, HTTP, etc.)

**Template d'Entité Domain** :

```typescript
// domain/entities/subscription.entity.ts

import { SubscriptionPlan } from '../value-objects/subscription-plan.vo';
import { SubscriptionStatus } from '../value-objects/subscription-status.vo';

export class Subscription {
  constructor(
    private readonly id: string,
    private readonly clubId: string,
    private plan: SubscriptionPlan,
    private status: SubscriptionStatus,
    private readonly startDate: Date,
    private endDate: Date | null,
    private currentTeamsCount: number,
  ) {
    this.validate();
  }

  // Factory method pour création
  static create(clubId: string, plan: SubscriptionPlan): Subscription {
    return new Subscription(
      crypto.randomUUID(),
      clubId,
      plan,
      SubscriptionStatus.ACTIVE,
      new Date(),
      null,
      0,
    );
  }

  // Validation des invariants
  private validate(): void {
    if (!this.id) throw new Error('Subscription ID is required');
    if (!this.clubId) throw new Error('Club ID is required');
    if (this.currentTeamsCount < 0) {
      throw new Error('Teams count cannot be negative');
    }
  }

  // Logique métier : Peut-on créer une nouvelle équipe ?
  canCreateTeam(): boolean {
    if (!this.isActive()) return false;
    if (!this.plan.hasTeamLimit()) return true; // Unlimited
    return this.currentTeamsCount < this.plan.getMaxTeams();
  }

  // Logique métier : Upgrade du plan
  upgrade(newPlan: SubscriptionPlan): void {
    if (!newPlan.isUpgradeFrom(this.plan)) {
      throw new Error('Cannot downgrade subscription');
    }
    this.plan = newPlan;
  }

  // Getters (pas de setters !)
  getId(): string {
    return this.id;
  }

  getClubId(): string {
    return this.clubId;
  }

  getPlan(): SubscriptionPlan {
    return this.plan;
  }

  isActive(): boolean {
    return this.status.isActive();
  }

  // Méthodes de modification retournent une nouvelle instance (immutabilité)
  incrementTeamsCount(): void {
    if (!this.canCreateTeam()) {
      throw new Error('Team limit reached for current plan');
    }
    this.currentTeamsCount++;
  }
}
```

**Template Value Object** :

```typescript
// domain/value-objects/subscription-plan.vo.ts

export class SubscriptionPlan {
  private static readonly PLANS = {
    FREE: { name: 'Free', maxTeams: 1, price: 0 },
    PRO: { name: 'Pro', maxTeams: 3, price: 9.99 },
    UNLIMITED: { name: 'Unlimited', maxTeams: -1, price: 29.99 },
  };

  private constructor(private readonly planName: string) {
    if (!Object.keys(SubscriptionPlan.PLANS).includes(planName)) {
      throw new Error(`Invalid plan: ${planName}`);
    }
  }

  static FREE = new SubscriptionPlan('FREE');
  static PRO = new SubscriptionPlan('PRO');
  static UNLIMITED = new SubscriptionPlan('UNLIMITED');

  static fromString(planName: string): SubscriptionPlan {
    return new SubscriptionPlan(planName);
  }

  hasTeamLimit(): boolean {
    return this.getMaxTeams() !== -1;
  }

  getMaxTeams(): number {
    return SubscriptionPlan.PLANS[this.planName].maxTeams;
  }

  isUpgradeFrom(otherPlan: SubscriptionPlan): boolean {
    const currentPrice = SubscriptionPlan.PLANS[this.planName].price;
    const otherPrice = SubscriptionPlan.PLANS[otherPlan.planName].price;
    return currentPrice > otherPrice;
  }

  toString(): string {
    return this.planName;
  }
}
```

**Template Repository Interface** :

```typescript
// domain/repositories/subscription.repository.interface.ts

import { Subscription } from '../entities/subscription.entity';

export interface ISubscriptionRepository {
  create(subscription: Subscription): Promise<Subscription>;
  findById(id: string): Promise<Subscription | null>;
  findByClubId(clubId: string): Promise<Subscription | null>;
  update(subscription: Subscription): Promise<Subscription>;
  delete(id: string): Promise<void>;
}

// Token pour injection de dépendances
export const SUBSCRIPTION_REPOSITORY = Symbol('ISubscriptionRepository');
```

### 2. Application Layer (Orchestration)

**Responsabilité** : Orchestrer la logique métier via des use cases (Commands/Queries)

**Contenu** :
- **Commands** : Opérations d'écriture (Create, Update, Delete)
- **Queries** : Opérations de lecture (Get, List, Search)
- **Handlers** : Exécutent les commands/queries
- **Read Models** : DTOs optimisés pour l'UI

**Règles** :
- ✅ Utiliser CQRS (Command Query Responsibility Segregation)
- ✅ Un handler par command/query
- ✅ Valider les inputs avec class-validator
- ✅ Orchestrer les entités domain (pas de logique métier ici)
- ✅ Retourner des IDs pour les commands, Read Models pour les queries
- ✅ Dépendre uniquement du Domain Layer
- ❌ **JAMAIS** de logique métier (celle-ci est dans le Domain)
- ❌ **JAMAIS** d'accès direct à Prisma (utiliser les repositories)

**Voir la Skill `cqrs-command-query` pour plus de détails sur les Commands/Queries**

### 3. Infrastructure Layer (Implémentation Technique)

**Responsabilité** : Implémenter les interfaces du Domain Layer

**Contenu** :
- **Repository Implementations** : Implémentent les interfaces du domain
- **Mappers** : Convertissent Domain Entities ↔ Prisma Models
- **External Services** : Intégrations externes (APIs, files, etc.)

**Règles** :
- ✅ Implémenter les interfaces du domain
- ✅ Utiliser Prisma ici (et UNIQUEMENT ici)
- ✅ Créer des mappers pour Domain ↔ Prisma
- ✅ Gérer les erreurs de persistence
- ❌ **JAMAIS** de logique métier
- ❌ **JAMAIS** exposer Prisma en dehors de cette couche

**Template Repository Implementation** :

```typescript
// infrastructure/persistence/repositories/subscription.repository.ts

import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../../prisma/prisma.service';
import { ISubscriptionRepository } from '../../../domain/repositories/subscription.repository.interface';
import { Subscription } from '../../../domain/entities/subscription.entity';
import { SubscriptionMapper } from '../mappers/subscription.mapper';

@Injectable()
export class SubscriptionRepository implements ISubscriptionRepository {
  constructor(private readonly prisma: PrismaService) {}

  async create(subscription: Subscription): Promise<Subscription> {
    const prismaData = SubscriptionMapper.toPrisma(subscription);

    const created = await this.prisma.subscription.create({
      data: prismaData,
    });

    return SubscriptionMapper.toDomain(created);
  }

  async findById(id: string): Promise<Subscription | null> {
    const subscription = await this.prisma.subscription.findUnique({
      where: { id },
    });

    return subscription ? SubscriptionMapper.toDomain(subscription) : null;
  }

  async findByClubId(clubId: string): Promise<Subscription | null> {
    const subscription = await this.prisma.subscription.findFirst({
      where: { clubId },
    });

    return subscription ? SubscriptionMapper.toDomain(subscription) : null;
  }

  async update(subscription: Subscription): Promise<Subscription> {
    const prismaData = SubscriptionMapper.toPrisma(subscription);

    const updated = await this.prisma.subscription.update({
      where: { id: subscription.getId() },
      data: prismaData,
    });

    return SubscriptionMapper.toDomain(updated);
  }

  async delete(id: string): Promise<void> {
    await this.prisma.subscription.delete({
      where: { id },
    });
  }
}
```

**Voir la Skill `prisma-mapper` pour plus de détails sur les Mappers**

### 4. Presentation Layer (HTTP/API)

**Responsabilité** : Gérer les requêtes/réponses HTTP

**Contenu** :
- **Controllers** : Endpoints HTTP avec NestJS
- **DTOs** : Validation des inputs HTTP (class-validator)
- **Guards** : Authentification et autorisation

**Règles** :
- ✅ Controllers TRÈS fins (HTTP uniquement)
- ✅ Déléguer immédiatement aux Handlers (Application Layer)
- ✅ Valider les inputs avec class-validator
- ✅ Transformer les outputs en JSON
- ✅ Gérer les erreurs HTTP
- ❌ **JAMAIS** de logique métier
- ❌ **JAMAIS** d'accès direct aux repositories
- ❌ **JAMAIS** d'accès direct à `DatabaseService` ou Prisma
- ❌ **JAMAIS** d'accès direct à la base de données
- ✅ **TOUJOURS** passer par une Query/Command → Handler → Repository

**Template Controller** :

```typescript
// presentation/controllers/subscriptions.controller.ts

import { Controller, Post, Body, Get, Param, Put, Delete, UseGuards } from '@nestjs/common';
import { JwtAuthGuard } from '../../auth/guards/jwt-auth.guard';
import { CreateSubscriptionCommand } from '../../application/commands/create-subscription/create-subscription.command';
import { CreateSubscriptionHandler } from '../../application/commands/create-subscription/create-subscription.handler';
import { GetSubscriptionQuery } from '../../application/queries/get-subscription/get-subscription.query';
import { GetSubscriptionHandler } from '../../application/queries/get-subscription/get-subscription.handler';

@Controller('subscriptions')
@UseGuards(JwtAuthGuard)
export class SubscriptionsController {
  constructor(
    private readonly createHandler: CreateSubscriptionHandler,
    private readonly getHandler: GetSubscriptionHandler,
  ) {}

  @Post()
  async create(@Body() command: CreateSubscriptionCommand) {
    const id = await this.createHandler.execute(command);
    return { id };
  }

  @Get(':id')
  async findOne(@Param('id') id: string) {
    const query = new GetSubscriptionQuery(id);
    return this.getHandler.execute(query);
  }
}
```

## 🔧 Module Configuration (NestJS)

**Template Module** :

```typescript
// [bounded-context].module.ts

import { Module } from '@nestjs/common';
import { PrismaModule } from '../prisma/prisma.module';

// Presentation
import { SubscriptionsController } from './presentation/controllers/subscriptions.controller';

// Application - Commands
import { CreateSubscriptionHandler } from './application/commands/create-subscription/create-subscription.handler';

// Application - Queries
import { GetSubscriptionHandler } from './application/queries/get-subscription/get-subscription.handler';

// Infrastructure
import { SubscriptionRepository } from './infrastructure/persistence/repositories/subscription.repository';
import { SUBSCRIPTION_REPOSITORY } from './domain/repositories/subscription.repository.interface';

@Module({
  imports: [PrismaModule],
  controllers: [SubscriptionsController],
  providers: [
    // Repository binding
    {
      provide: SUBSCRIPTION_REPOSITORY,
      useClass: SubscriptionRepository,
    },
    // Handlers
    CreateSubscriptionHandler,
    GetSubscriptionHandler,
  ],
  exports: [
    SUBSCRIPTION_REPOSITORY,
  ],
})
export class ClubManagementModule {}
```

## ✅ Checklist de Validation

Avant de finaliser un bounded context, vérifier :

### Domain Layer
- [ ] Entities contiennent la logique métier
- [ ] Value Objects sont immuables
- [ ] Pas d'imports NestJS ou Prisma
- [ ] Repository interfaces uniquement (pas d'implémentations)
- [ ] Validation des invariants dans les constructeurs
- [ ] Factory methods pour la création d'entités

### Application Layer
- [ ] Commands pour les écritures, Queries pour les lectures
- [ ] Handlers bien séparés (un handler par command/query)
- [ ] Pas de logique métier (délégation au domain)
- [ ] Validation avec class-validator
- [ ] Read Models séparés des entités domain

### Infrastructure Layer
- [ ] Repository implementations utilisent Prisma
- [ ] Mappers pour Domain ↔ Prisma
- [ ] Aucune logique métier
- [ ] Prisma confiné à cette couche

### Presentation Layer
- [ ] Controllers très fins (HTTP uniquement)
- [ ] Délégation immédiate aux handlers
- [ ] DTOs pour validation des inputs
- [ ] Gestion des erreurs HTTP

### Module
- [ ] Repositories injectés via DI (useClass)
- [ ] Handlers enregistrés comme providers
- [ ] Exports pour réutilisation dans d'autres modules

## 🎓 Exemples Concrets du Projet

### Bounded Context Existant : `club-management`

Structure complète :
- **Domain** : Club, Subscription, Invitation entities
- **Application** : create-club, subscribe-to-plan, get-club, etc.
- **Infrastructure** : ClubRepository, SubscriptionRepository, Mappers
- **Presentation** : ClubsController, SubscriptionsController

Référence : `volley-app-backend/src/club-management/`

### Bounded Context Existant : `training-management`

Structure complète avec CQRS avancé
Référence : `volley-app-backend/src/training-management/`

## 🚨 Erreurs Courantes à Éviter

1. ❌ **Entités anémiques** : Ne pas mettre la logique métier dans les entités
   - ✅ FAIRE : `subscription.canCreateTeam()`
   - ❌ NE PAS FAIRE : `if (subscription.currentTeams < subscription.maxTeams)`

2. ❌ **Domain qui dépend de Prisma** : Jamais d'import Prisma dans le domain
   - ✅ FAIRE : Repository interface dans domain
   - ❌ NE PAS FAIRE : `import { PrismaClient } from '@prisma/client'` dans domain

3. ❌ **Logique métier dans les Controllers** : Controllers doivent être fins
   - ✅ FAIRE : `await this.createHandler.execute(command)`
   - ❌ NE PAS FAIRE : Validation métier dans le controller

4. ❌ **Accès direct à DatabaseService dans les Controllers** : VIOLATION GRAVE!
   - ❌ NE PAS FAIRE :
     ```typescript
     constructor(private readonly database: DatabaseService) {}

     async method() {
       const user = await this.database.user.findUnique(...); // ❌ INTERDIT!
     }
     ```
   - ✅ FAIRE : Créer une Query + QueryHandler
     ```typescript
     constructor(private readonly queryBus: QueryBus) {}

     async method() {
       const query = new GetUserQuery(userId);
       const user = await this.queryBus.execute(query); // ✅ Correct
     }
     ```
   - **Pourquoi ?** : Le controller ne doit JAMAIS connaître la DB. Toute lecture/écriture passe par CQRS (Query/Command → Handler → Repository)

5. ❌ **Handlers qui contiennent de la logique métier** : Les handlers orchestrent
   - ✅ FAIRE : `subscription.upgrade(newPlan)` (logique dans l'entité)
   - ❌ NE PAS FAIRE : Logique d'upgrade dans le handler

## 📚 Skills Complémentaires

Pour aller plus loin :
- **cqrs-command-query** : Détails sur les Commands/Queries/Handlers
- **ddd-testing** : Standards de tests pour DDD
- **prisma-mapper** : Patterns de mappers Domain ↔ Prisma

---

**Rappel** : L'objectif de DDD est de créer un **code maintenable** où la **logique métier est centralisée** dans le **Domain Layer**, isolée de toute infrastructure technique.
