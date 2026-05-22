---
name: Prisma Domain Mapper Generator
description: Génère des mappers bidirectionnels entre Domain Entities et Prisma Models pour l'isolation de la couche persistence. À utiliser lors de la création de mappers, repositories, ou quand l'utilisateur mentionne "mapper", "Prisma", "persistence", "toPrisma", "toDomain", "repository implementation".
allowed-tools: [Read, Write, Edit, Glob, Grep]
---

# Prisma Domain Mapper Generator

## 🎯 Mission

Créer des mappers bidirectionnels robustes pour convertir les Domain Entities en Prisma Models et vice-versa, en maintenant une stricte séparation entre le Domain Layer et la couche de persistence.

## 🏗️ Philosophie des Mappers

### Pourquoi des Mappers ?

En DDD, le **Domain Layer doit être totalement isolé** de toute infrastructure technique, y compris la base de données.

**Problème sans mappers** :
```typescript
// ❌ BAD - Domain entity dépend de Prisma
import { Club as PrismaClub } from '@prisma/client';

export class Club extends PrismaClub { // VIOLATION DDD
  // Domain logic here
}
```

**Solution avec mappers** :
```typescript
// ✅ GOOD - Domain entity est pure
export class Club {
  // Pure TypeScript, aucune dépendance Prisma
  private constructor(
    private readonly id: string,
    private name: ClubName, // Value Object
    // ...
  ) {}
}

// Mapper dans l'Infrastructure Layer
export class ClubMapper {
  static toDomain(prismaClub: PrismaClub): Club { /* ... */ }
  static toPrisma(club: Club): PrismaClubCreateInput { /* ... */ }
}
```

### Avantages des Mappers

- ✅ **Domain pur** : Aucune dépendance vers Prisma dans le domain
- ✅ **Flexibilité** : Changer de DB sans toucher au domain
- ✅ **Testabilité** : Tester le domain sans DB
- ✅ **Évolutivité** : Adapter le modèle de données sans casser le domain
- ✅ **Clarté** : Séparation explicite des responsabilités

## 📁 Organisation des Mappers

```
bounded-context/
└── infrastructure/
    └── persistence/
        ├── repositories/
        │   └── club.repository.ts          # Uses mappers
        └── mappers/
            ├── club.mapper.ts               # Club entity mapper
            ├── subscription.mapper.ts       # Subscription entity mapper
            ├── invitation.mapper.ts         # Invitation entity mapper
            └── index.ts                     # Barrel export
```

## 🔄 Mapper Bidirectionnel

### Structure d'un Mapper

Un mapper contient **deux méthodes statiques** :
1. `toDomain()` : Prisma Model → Domain Entity
2. `toPrisma()` : Domain Entity → Prisma Model (pour create/update)

### Template Mapper Simple

```typescript
// infrastructure/persistence/mappers/club.mapper.ts

import { Club as PrismaClub } from '@prisma/client';
import { Club } from '../../../domain/entities/club.entity';
import { ClubName } from '../../../domain/value-objects/club-name.vo';

export class ClubMapper {
  /**
   * Convertit un Prisma Model en Domain Entity
   */
  static toDomain(prismaClub: PrismaClub): Club {
    // Reconstruct Value Objects from primitive values
    const name = ClubName.create(prismaClub.name);

    // Reconstruct Entity using all-args constructor or factory method
    return new Club(
      prismaClub.id,
      name,
      prismaClub.description,
      prismaClub.ownerId,
      prismaClub.createdAt,
      prismaClub.updatedAt,
    );
  }

  /**
   * Convertit une Domain Entity en Prisma Create/Update Input
   */
  static toPrisma(club: Club): Prisma.ClubCreateInput {
    return {
      id: club.getId(),
      name: club.getName().getValue(), // Extract primitive from Value Object
      description: club.getDescription(),
      ownerId: club.getOwnerId(),
      createdAt: club.getCreatedAt(),
      updatedAt: new Date(),
    };
  }

  /**
   * Optionnel : Méthode spécifique pour les updates
   */
  static toUpdateInput(club: Club): Prisma.ClubUpdateInput {
    return {
      name: club.getName().getValue(),
      description: club.getDescription(),
      updatedAt: new Date(),
      // Exclude id, ownerId, createdAt (immutables)
    };
  }
}
```

## 🎨 Patterns de Mapping

### 1. Mapping avec Value Objects

```typescript
// Domain Entity avec Value Objects
export class Subscription {
  constructor(
    private readonly id: string,
    private plan: SubscriptionPlan, // Value Object
    private status: SubscriptionStatus, // Value Object
    private readonly startDate: Date,
  ) {}
}

// Mapper
export class SubscriptionMapper {
  static toDomain(prismaSubscription: PrismaSubscription): Subscription {
    // Reconstruct Value Objects from string primitives
    const plan = SubscriptionPlan.fromString(prismaSubscription.plan);
    const status = SubscriptionStatus.fromString(prismaSubscription.status);

    return new Subscription(
      prismaSubscription.id,
      plan,
      status,
      prismaSubscription.startDate,
    );
  }

  static toPrisma(subscription: Subscription): Prisma.SubscriptionCreateInput {
    return {
      id: subscription.getId(),
      plan: subscription.getPlan().toString(), // Extract primitive
      status: subscription.getStatus().toString(), // Extract primitive
      startDate: subscription.getStartDate(),
    };
  }
}
```

### 2. Mapping avec Relations (1-to-1, 1-to-many)

```typescript
// Prisma Schema
// model Club {
//   id            String         @id
//   name          String
//   subscription  Subscription?  @relation(...)
//   members       Member[]
// }

export class ClubMapper {
  /**
   * Mapping simple sans relations
   */
  static toDomain(prismaClub: PrismaClub): Club {
    return new Club(
      prismaClub.id,
      ClubName.create(prismaClub.name),
      prismaClub.description,
      prismaClub.ownerId,
      prismaClub.createdAt,
    );
  }

  /**
   * Mapping avec relations (requires Prisma includes)
   */
  static toDomainWithRelations(
    prismaClub: PrismaClub & {
      subscription?: PrismaSubscription;
      members?: PrismaMember[];
    },
  ): Club {
    const club = new Club(
      prismaClub.id,
      ClubName.create(prismaClub.name),
      prismaClub.description,
      prismaClub.ownerId,
      prismaClub.createdAt,
    );

    // Map 1-to-1 relation (subscription)
    if (prismaClub.subscription) {
      const subscription = SubscriptionMapper.toDomain(prismaClub.subscription);
      club.setSubscription(subscription);
    }

    // Map 1-to-many relation (members)
    if (prismaClub.members) {
      const members = prismaClub.members.map(m => MemberMapper.toDomain(m));
      club.setMembers(members);
    }

    return club;
  }

  /**
   * Mapping to Prisma (create)
   */
  static toPrisma(club: Club): Prisma.ClubCreateInput {
    return {
      id: club.getId(),
      name: club.getName().getValue(),
      description: club.getDescription(),
      owner: {
        connect: { id: club.getOwnerId() }, // Relation via connect
      },
      // Don't include subscription or members here
      // They are created separately via their own repositories
    };
  }

  /**
   * Mapping to Prisma avec nested create (optionnel)
   */
  static toPrismaWithSubscription(
    club: Club,
    subscription: Subscription,
  ): Prisma.ClubCreateInput {
    return {
      id: club.getId(),
      name: club.getName().getValue(),
      description: club.getDescription(),
      owner: {
        connect: { id: club.getOwnerId() },
      },
      subscription: {
        create: SubscriptionMapper.toPrisma(subscription), // Nested create
      },
    };
  }
}
```

### 3. Mapping avec Dates et Types Complexes

```typescript
export class InvitationMapper {
  static toDomain(prismaInvitation: PrismaInvitation): Invitation {
    // Convert Prisma Date to Domain Date
    const createdAt = new Date(prismaInvitation.createdAt);
    const expiresAt = new Date(prismaInvitation.expiresAt);

    // Handle nullable dates
    const usedAt = prismaInvitation.usedAt
      ? new Date(prismaInvitation.usedAt)
      : null;

    return new Invitation(
      prismaInvitation.id,
      prismaInvitation.clubId,
      InvitationType.fromString(prismaInvitation.type),
      prismaInvitation.email,
      createdAt,
      expiresAt,
      usedAt,
    );
  }

  static toPrisma(invitation: Invitation): Prisma.InvitationCreateInput {
    return {
      id: invitation.getId(),
      clubId: invitation.getClubId(),
      type: invitation.getType().toString(),
      email: invitation.getEmail(),
      createdAt: invitation.getCreatedAt(),
      expiresAt: invitation.getExpiresAt(),
      usedAt: invitation.getUsedAt(), // Can be null
    };
  }
}
```

### 4. Mapping avec Enums

```typescript
// Prisma Schema
// enum SubscriptionPlanEnum {
//   FREE
//   PRO
//   UNLIMITED
// }

export class SubscriptionMapper {
  static toDomain(prismaSubscription: PrismaSubscription): Subscription {
    // Convert Prisma enum to Domain Value Object
    const plan = SubscriptionPlan.fromString(prismaSubscription.plan);

    return new Subscription(
      prismaSubscription.id,
      plan,
      // ...
    );
  }

  static toPrisma(subscription: Subscription): Prisma.SubscriptionCreateInput {
    return {
      id: subscription.getId(),
      plan: subscription.getPlan().toString() as SubscriptionPlanEnum, // Type assertion
      // ...
    };
  }
}
```

### 5. Mapping avec JSON Fields

```typescript
// Prisma Schema
// model Training {
//   id       String  @id
//   name     String
//   metadata Json?   // Flexible JSON field
// }

interface TrainingMetadata {
  difficulty: string;
  duration: number;
  tags: string[];
}

export class TrainingMapper {
  static toDomain(prismaTraining: PrismaTraining): Training {
    // Parse JSON field
    const metadata = prismaTraining.metadata as TrainingMetadata | null;

    return new Training(
      prismaTraining.id,
      prismaTraining.name,
      metadata,
    );
  }

  static toPrisma(training: Training): Prisma.TrainingCreateInput {
    return {
      id: training.getId(),
      name: training.getName(),
      metadata: training.getMetadata(), // Prisma handles JSON serialization
    };
  }
}
```

## 🔗 Utilisation dans les Repositories

### Repository Implementation avec Mapper

```typescript
// infrastructure/persistence/repositories/club.repository.ts

import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../../prisma/prisma.service';
import { IClubRepository } from '../../../domain/repositories/club.repository.interface';
import { Club } from '../../../domain/entities/club.entity';
import { ClubMapper } from '../mappers/club.mapper';

@Injectable()
export class ClubRepository implements IClubRepository {
  constructor(private readonly prisma: PrismaService) {}

  async create(club: Club): Promise<Club> {
    // 1. Convert Domain Entity → Prisma Input
    const prismaData = ClubMapper.toPrisma(club);

    // 2. Save to database
    const created = await this.prisma.club.create({
      data: prismaData,
    });

    // 3. Convert Prisma Model → Domain Entity
    return ClubMapper.toDomain(created);
  }

  async findById(id: string): Promise<Club | null> {
    const prismaClub = await this.prisma.club.findUnique({
      where: { id },
    });

    if (!prismaClub) return null;

    // Convert Prisma Model → Domain Entity
    return ClubMapper.toDomain(prismaClub);
  }

  async findByIdWithRelations(id: string): Promise<Club | null> {
    const prismaClub = await this.prisma.club.findUnique({
      where: { id },
      include: {
        subscription: true,
        members: true,
      },
    });

    if (!prismaClub) return null;

    // Use specialized mapper method for relations
    return ClubMapper.toDomainWithRelations(prismaClub);
  }

  async update(club: Club): Promise<Club> {
    // 1. Convert to update input
    const updateData = ClubMapper.toUpdateInput(club);

    // 2. Update in database
    const updated = await this.prisma.club.update({
      where: { id: club.getId() },
      data: updateData,
    });

    // 3. Convert back to domain
    return ClubMapper.toDomain(updated);
  }

  async delete(id: string): Promise<void> {
    await this.prisma.club.delete({
      where: { id },
    });
  }

  async findAll(options: {
    page: number;
    limit: number;
    search?: string;
  }): Promise<{ data: Club[]; total: number }> {
    const skip = (options.page - 1) * options.limit;

    const where = options.search
      ? {
          name: {
            contains: options.search,
            mode: 'insensitive' as const,
          },
        }
      : {};

    const [prismaClubs, total] = await Promise.all([
      this.prisma.club.findMany({
        where,
        skip,
        take: options.limit,
        orderBy: { createdAt: 'desc' },
      }),
      this.prisma.club.count({ where }),
    ]);

    // Convert array of Prisma Models → Domain Entities
    const clubs = prismaClubs.map(pc => ClubMapper.toDomain(pc));

    return { data: clubs, total };
  }
}
```

## ✅ Checklist pour les Mappers

### Responsabilités du Mapper
- [ ] Deux méthodes statiques : `toDomain()` et `toPrisma()`
- [ ] Reconstruit les Value Objects dans `toDomain()`
- [ ] Extrait les primitives des Value Objects dans `toPrisma()`
- [ ] Gère les relations si nécessaire
- [ ] Gère les types complexes (dates, JSON, enums)
- [ ] Gère les valeurs nullables correctement
- [ ] Pas de logique métier (seulement transformation)

### Règles Strictes
- ✅ Mappers dans `infrastructure/persistence/mappers/`
- ✅ Un mapper par entité domain
- ✅ Méthodes statiques uniquement (pas d'état)
- ✅ Pas de logique métier dans les mappers
- ✅ Toujours reconstruire les Value Objects
- ❌ **JAMAIS** de références Prisma dans le domain
- ❌ **JAMAIS** de logique métier dans le mapper
- ❌ **JAMAIS** d'appels à la DB dans le mapper

## 🎓 Exemples Concrets du Projet

### Bounded Context `club-management`

Mappers existants à consulter :
- `infrastructure/persistence/mappers/club.mapper.ts`
- `infrastructure/persistence/mappers/subscription.mapper.ts`
- `infrastructure/persistence/mappers/invitation.mapper.ts`
- `infrastructure/persistence/mappers/member.mapper.ts`

Référence : `volley-app-backend/src/club-management/infrastructure/persistence/mappers/`

## 🚨 Erreurs Courantes à Éviter

1. ❌ **Mapper avec logique métier**
   - ✅ FAIRE : Transformer uniquement les données
   - ❌ NE PAS FAIRE : Valider ou calculer dans le mapper

2. ❌ **Exposer Prisma Types dans le Domain**
   - ✅ FAIRE : Domain Entity pure TypeScript
   - ❌ NE PAS FAIRE : `import { Club as PrismaClub }` dans domain

3. ❌ **Ne pas reconstruire les Value Objects**
   - ✅ FAIRE : `ClubName.create(prismaClub.name)`
   - ❌ NE PAS FAIRE : Passer directement la string

4. ❌ **Mapper qui appelle la DB**
   - ✅ FAIRE : Mapper transforme les données seulement
   - ❌ NE PAS FAIRE : `await this.prisma.club.findMany()` dans mapper

5. ❌ **Oublier de gérer les relations**
   - ✅ FAIRE : Créer une méthode séparée `toDomainWithRelations()`
   - ❌ NE PAS FAIRE : Ignorer les relations ou les gérer de manière incohérente

## 🧪 Tester les Mappers

### Template de Test

```typescript
// infrastructure/persistence/mappers/club.mapper.spec.ts

import { ClubMapper } from './club.mapper';
import { Club } from '../../../domain/entities/club.entity';
import { ClubName } from '../../../domain/value-objects/club-name.vo';

describe('ClubMapper', () => {
  describe('toDomain()', () => {
    it('should convert Prisma model to Domain entity', () => {
      // Arrange
      const prismaClub = {
        id: 'club-123',
        name: 'Volley Club Paris',
        description: 'Best club',
        ownerId: 'user-123',
        createdAt: new Date('2024-01-01'),
        updatedAt: new Date('2024-01-02'),
      };

      // Act
      const club = ClubMapper.toDomain(prismaClub);

      // Assert
      expect(club).toBeInstanceOf(Club);
      expect(club.getId()).toBe('club-123');
      expect(club.getName().getValue()).toBe('Volley Club Paris');
      expect(club.getDescription()).toBe('Best club');
    });

    it('should reconstruct Value Objects correctly', () => {
      const prismaClub = {
        id: 'club-123',
        name: 'Volley Club',
        description: null,
        ownerId: 'user-123',
        createdAt: new Date(),
        updatedAt: new Date(),
      };

      const club = ClubMapper.toDomain(prismaClub);

      expect(club.getName()).toBeInstanceOf(ClubName);
    });
  });

  describe('toPrisma()', () => {
    it('should convert Domain entity to Prisma input', () => {
      // Arrange
      const club = Club.create('Volley Club', 'Description', 'user-123');

      // Act
      const prismaInput = ClubMapper.toPrisma(club);

      // Assert
      expect(prismaInput).toMatchObject({
        id: club.getId(),
        name: 'Volley Club',
        description: 'Description',
        ownerId: 'user-123',
      });
    });

    it('should extract primitives from Value Objects', () => {
      const club = Club.create('Club Name', 'Desc', 'user-123');

      const prismaInput = ClubMapper.toPrisma(club);

      expect(typeof prismaInput.name).toBe('string');
    });
  });

  describe('Bidirectional mapping', () => {
    it('should maintain data integrity in round-trip', () => {
      // Domain → Prisma → Domain
      const originalClub = Club.create('Volley Club', 'Description', 'user-123');

      const prismaInput = ClubMapper.toPrisma(originalClub);
      const reconstructedClub = ClubMapper.toDomain({
        ...prismaInput,
        createdAt: new Date(),
        updatedAt: new Date(),
      } as any);

      expect(reconstructedClub.getName().getValue()).toBe(originalClub.getName().getValue());
      expect(reconstructedClub.getDescription()).toBe(originalClub.getDescription());
    });
  });
});
```

## 📚 Skills Complémentaires

Pour aller plus loin :
- **ddd-bounded-context** : Architecture DDD complète avec bounded contexts
- **cqrs-command-query** : Commands/Queries qui utilisent les repositories
- **ddd-testing** : Tests des repositories et mappers

---

**Rappel** : Les mappers sont la **frontière** entre votre Domain Layer pur et l'infrastructure de persistence. Ils garantissent que votre logique métier reste **indépendante** de la technologie de base de données.
