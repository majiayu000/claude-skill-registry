---
name: DDD Testing Standards
description: Standards de tests exhaustifs pour les bounded contexts DDD (Domain, Application, Integration). À utiliser lors de l'écriture de tests backend, tests unitaires, tests d'intégration, ou quand l'utilisateur mentionne "test", "TDD", "coverage", "unit test", "integration test", "test domain", "test handler".
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# DDD Testing Standards

## 🎯 Mission

Créer des tests exhaustifs pour les bounded contexts DDD suivant une approche TDD (Test-Driven Development) avec des standards de coverage stricts.

## 🏆 Philosophie Critique

**Dans DDD, les tests sont NON-NÉGOCIABLES.**

La logique métier dans le Domain Layer DOIT être testée à 100% avant toute autre implémentation. Les tests sont la **documentation vivante** de votre logique métier.

### Pourquoi TDD en DDD ?

1. **Logique métier fiable** : Le Domain contient les règles critiques de l'application
2. **Refactoring sécurisé** : Tests exhaustifs permettent de refactorer sans casser
3. **Documentation** : Tests décrivent le comportement attendu
4. **Confidence** : Déploiement en production sans peur
5. **Régression** : Prévenir la réintroduction de bugs

## 📁 Structure des Tests

```
bounded-context/
├── tests/
│   ├── unit/
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   ├── subscription.entity.spec.ts
│   │   │   │   └── club.entity.spec.ts
│   │   │   ├── value-objects/
│   │   │   │   ├── subscription-plan.vo.spec.ts
│   │   │   │   └── club-name.vo.spec.ts
│   │   │   └── services/
│   │   │       └── subscription-limit.service.spec.ts
│   │   └── application/
│   │       ├── commands/
│   │       │   ├── create-club.handler.spec.ts
│   │       │   └── subscribe-to-plan.handler.spec.ts
│   │       └── queries/
│   │           ├── get-club.handler.spec.ts
│   │           └── list-clubs.handler.spec.ts
│   └── integration/
│       └── handlers/
│           ├── create-club.integration.spec.ts
│           └── subscribe-to-plan.integration.spec.ts
```

## 🧪 1. Domain Layer Tests (MANDATORY - 100% Coverage)

### Entities Tests

**Objectif** : Tester TOUTE la logique métier encapsulée dans les entités

**Ce qui DOIT être testé** :
- ✅ Tous les business methods
- ✅ Toutes les validation rules
- ✅ Toutes les state transitions
- ✅ Tous les edge cases et boundary conditions
- ✅ Tous les invariants
- ✅ Tous les factory methods

#### Template Entity Test

```typescript
// tests/unit/domain/entities/subscription.entity.spec.ts

import { Subscription } from '../../../../domain/entities/subscription.entity';
import { SubscriptionPlan } from '../../../../domain/value-objects/subscription-plan.vo';
import { SubscriptionStatus } from '../../../../domain/value-objects/subscription-status.vo';

describe('Subscription Entity', () => {
  describe('Factory Method - create()', () => {
    it('should create a new subscription with default values', () => {
      // Arrange
      const clubId = 'club-123';
      const plan = SubscriptionPlan.FREE;

      // Act
      const subscription = Subscription.create(clubId, plan);

      // Assert
      expect(subscription.getClubId()).toBe(clubId);
      expect(subscription.getPlan()).toBe(plan);
      expect(subscription.isActive()).toBe(true);
      expect(subscription.getCurrentTeamsCount()).toBe(0);
    });

    it('should throw error when clubId is empty', () => {
      // Arrange
      const clubId = '';
      const plan = SubscriptionPlan.FREE;

      // Act & Assert
      expect(() => Subscription.create(clubId, plan)).toThrow('Club ID is required');
    });
  });

  describe('Business Method - canCreateTeam()', () => {
    it('should return true when subscription is active and limit not reached', () => {
      // Arrange
      const subscription = Subscription.create('club-123', SubscriptionPlan.FREE);

      // Act
      const result = subscription.canCreateTeam();

      // Assert
      expect(result).toBe(true);
    });

    it('should return false when subscription is inactive', () => {
      // Arrange
      const subscription = Subscription.create('club-123', SubscriptionPlan.FREE);
      subscription.deactivate(); // State transition

      // Act
      const result = subscription.canCreateTeam();

      // Assert
      expect(result).toBe(false);
    });

    it('should return false when team limit is reached', () => {
      // Arrange
      const subscription = Subscription.create('club-123', SubscriptionPlan.FREE);
      subscription.incrementTeamsCount(); // 1/1 team for FREE plan

      // Act
      const result = subscription.canCreateTeam();

      // Assert
      expect(result).toBe(false);
    });

    it('should return true when plan has unlimited teams', () => {
      // Arrange
      const subscription = Subscription.create('club-123', SubscriptionPlan.UNLIMITED);
      // Simulate many teams
      for (let i = 0; i < 100; i++) {
        subscription.incrementTeamsCount();
      }

      // Act
      const result = subscription.canCreateTeam();

      // Assert
      expect(result).toBe(true);
    });

    it('should handle null teams count gracefully', () => {
      // Arrange
      const subscription = Subscription.create('club-123', SubscriptionPlan.FREE);

      // Act
      const result = subscription.canCreateTeam();

      // Assert
      expect(result).toBe(true);
    });
  });

  describe('Business Method - upgrade()', () => {
    it('should upgrade from FREE to PRO successfully', () => {
      // Arrange
      const subscription = Subscription.create('club-123', SubscriptionPlan.FREE);

      // Act
      subscription.upgrade(SubscriptionPlan.PRO);

      // Assert
      expect(subscription.getPlan()).toBe(SubscriptionPlan.PRO);
    });

    it('should upgrade from PRO to UNLIMITED successfully', () => {
      // Arrange
      const subscription = Subscription.create('club-123', SubscriptionPlan.PRO);

      // Act
      subscription.upgrade(SubscriptionPlan.UNLIMITED);

      // Assert
      expect(subscription.getPlan()).toBe(SubscriptionPlan.UNLIMITED);
    });

    it('should throw error when trying to downgrade', () => {
      // Arrange
      const subscription = Subscription.create('club-123', SubscriptionPlan.PRO);

      // Act & Assert
      expect(() => subscription.upgrade(SubscriptionPlan.FREE))
        .toThrow('Cannot downgrade subscription');
    });

    it('should throw error when upgrading to same plan', () => {
      // Arrange
      const subscription = Subscription.create('club-123', SubscriptionPlan.PRO);

      // Act & Assert
      expect(() => subscription.upgrade(SubscriptionPlan.PRO))
        .toThrow('Already on this plan');
    });
  });

  describe('State Transition - incrementTeamsCount()', () => {
    it('should increment teams count when limit not reached', () => {
      // Arrange
      const subscription = Subscription.create('club-123', SubscriptionPlan.PRO);
      const initialCount = subscription.getCurrentTeamsCount();

      // Act
      subscription.incrementTeamsCount();

      // Assert
      expect(subscription.getCurrentTeamsCount()).toBe(initialCount + 1);
    });

    it('should throw error when limit is reached', () => {
      // Arrange
      const subscription = Subscription.create('club-123', SubscriptionPlan.FREE);
      subscription.incrementTeamsCount(); // Reach limit (1/1)

      // Act & Assert
      expect(() => subscription.incrementTeamsCount())
        .toThrow('Team limit reached for current plan');
    });

    it('should allow unlimited increments for UNLIMITED plan', () => {
      // Arrange
      const subscription = Subscription.create('club-123', SubscriptionPlan.UNLIMITED);

      // Act - Increment 1000 times
      for (let i = 0; i < 1000; i++) {
        subscription.incrementTeamsCount();
      }

      // Assert
      expect(subscription.getCurrentTeamsCount()).toBe(1000);
    });
  });

  describe('Edge Cases', () => {
    it('should handle negative teams count validation', () => {
      // Arrange & Act & Assert
      expect(() => new Subscription(
        'id-123',
        'club-123',
        SubscriptionPlan.FREE,
        SubscriptionStatus.ACTIVE,
        new Date(),
        null,
        -1, // Negative count
      )).toThrow('Teams count cannot be negative');
    });

    it('should handle null plan', () => {
      // Arrange & Act & Assert
      expect(() => new Subscription(
        'id-123',
        'club-123',
        null as any,
        SubscriptionStatus.ACTIVE,
        new Date(),
        null,
        0,
      )).toThrow('Plan is required');
    });
  });
});
```

### Value Objects Tests

```typescript
// tests/unit/domain/value-objects/subscription-plan.vo.spec.ts

import { SubscriptionPlan } from '../../../../domain/value-objects/subscription-plan.vo';

describe('SubscriptionPlan Value Object', () => {
  describe('Creation', () => {
    it('should create FREE plan', () => {
      // Act
      const plan = SubscriptionPlan.FREE;

      // Assert
      expect(plan.toString()).toBe('FREE');
      expect(plan.getMaxTeams()).toBe(1);
    });

    it('should throw error for invalid plan name', () => {
      // Act & Assert
      expect(() => SubscriptionPlan.fromString('INVALID'))
        .toThrow('Invalid plan: INVALID');
    });
  });

  describe('hasTeamLimit()', () => {
    it('should return true for FREE plan', () => {
      expect(SubscriptionPlan.FREE.hasTeamLimit()).toBe(true);
    });

    it('should return false for UNLIMITED plan', () => {
      expect(SubscriptionPlan.UNLIMITED.hasTeamLimit()).toBe(false);
    });
  });

  describe('isUpgradeFrom()', () => {
    it('should return true when upgrading from FREE to PRO', () => {
      expect(SubscriptionPlan.PRO.isUpgradeFrom(SubscriptionPlan.FREE)).toBe(true);
    });

    it('should return false when downgrading from PRO to FREE', () => {
      expect(SubscriptionPlan.FREE.isUpgradeFrom(SubscriptionPlan.PRO)).toBe(false);
    });

    it('should return false for same plan', () => {
      expect(SubscriptionPlan.PRO.isUpgradeFrom(SubscriptionPlan.PRO)).toBe(false);
    });
  });

  describe('Immutability', () => {
    it('should be immutable (same instance for same value)', () => {
      const plan1 = SubscriptionPlan.FREE;
      const plan2 = SubscriptionPlan.FREE;

      expect(plan1).toBe(plan2);
    });
  });
});
```

### Domain Services Tests

```typescript
// tests/unit/domain/services/subscription-limit.service.spec.ts

import { SubscriptionLimitService } from '../../../../domain/services/subscription-limit.service';
import { Subscription } from '../../../../domain/entities/subscription.entity';
import { SubscriptionPlan } from '../../../../domain/value-objects/subscription-plan.vo';

describe('SubscriptionLimitService', () => {
  let service: SubscriptionLimitService;

  beforeEach(() => {
    service = new SubscriptionLimitService();
  });

  describe('canAddTeam()', () => {
    it('should return true when subscription allows new team', () => {
      // Arrange
      const subscription = Subscription.create('club-123', SubscriptionPlan.FREE);

      // Act
      const result = service.canAddTeam(subscription);

      // Assert
      expect(result).toBe(true);
    });

    it('should return false when team limit is reached', () => {
      // Arrange
      const subscription = Subscription.create('club-123', SubscriptionPlan.FREE);
      subscription.incrementTeamsCount(); // Reach limit

      // Act
      const result = service.canAddTeam(subscription);

      // Assert
      expect(result).toBe(false);
    });
  });

  describe('getRemainingSlots()', () => {
    it('should return correct remaining slots for PRO plan', () => {
      // Arrange
      const subscription = Subscription.create('club-123', SubscriptionPlan.PRO);
      subscription.incrementTeamsCount(); // 1/3 teams

      // Act
      const remaining = service.getRemainingSlots(subscription);

      // Assert
      expect(remaining).toBe(2);
    });

    it('should return Infinity for UNLIMITED plan', () => {
      // Arrange
      const subscription = Subscription.create('club-123', SubscriptionPlan.UNLIMITED);

      // Act
      const remaining = service.getRemainingSlots(subscription);

      // Assert
      expect(remaining).toBe(Infinity);
    });
  });
});
```

## 🔧 2. Application Layer Tests (MANDATORY - 95%+ Coverage)

### Command Handler Tests

**Objectif** : Tester l'orchestration des entités domain par les handlers

**Ce qui DOIT être testé** :
- ✅ Successful execution path
- ✅ All validation errors
- ✅ Domain exceptions handling
- ✅ Repository methods are called correctly
- ✅ Return values (IDs)

#### Template Command Handler Test

```typescript
// tests/unit/application/commands/create-club.handler.spec.ts

import { CreateClubHandler } from '../../../../application/commands/create-club/create-club.handler';
import { CreateClubCommand } from '../../../../application/commands/create-club/create-club.command';
import { IClubRepository } from '../../../../domain/repositories/club.repository.interface';
import { Club } from '../../../../domain/entities/club.entity';

describe('CreateClubHandler', () => {
  let handler: CreateClubHandler;
  let mockClubRepository: jest.Mocked<IClubRepository>;

  beforeEach(() => {
    // Mock repository
    mockClubRepository = {
      create: jest.fn(),
      findById: jest.fn(),
      findByUserId: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
    } as jest.Mocked<IClubRepository>;

    handler = new CreateClubHandler(mockClubRepository);
  });

  describe('execute()', () => {
    it('should create club successfully with valid data', async () => {
      // Arrange
      const command = new CreateClubCommand(
        'Volley Club Paris',
        'Best club in Paris',
        'user-123',
      );

      const mockClub = Club.create(
        command.name,
        command.description,
        command.userId,
      );

      mockClubRepository.create.mockResolvedValue(mockClub);

      // Act
      const result = await handler.execute(command);

      // Assert
      expect(result).toBe(mockClub.getId());
      expect(mockClubRepository.create).toHaveBeenCalledTimes(1);
      expect(mockClubRepository.create).toHaveBeenCalledWith(
        expect.objectContaining({
          getName: expect.any(Function),
          getDescription: expect.any(Function),
        }),
      );
    });

    it('should throw error when name is empty', async () => {
      // Arrange
      const command = new CreateClubCommand(
        '', // Empty name
        'Description',
        'user-123',
      );

      // Act & Assert
      await expect(handler.execute(command))
        .rejects
        .toThrow('Club name cannot be empty');
    });

    it('should throw error when userId is missing', async () => {
      // Arrange
      const command = new CreateClubCommand(
        'Volley Club',
        'Description',
        '', // Empty userId
      );

      // Act & Assert
      await expect(handler.execute(command))
        .rejects
        .toThrow('User ID is required');
    });

    it('should call repository.create() with correct club entity', async () => {
      // Arrange
      const command = new CreateClubCommand(
        'Volley Club Paris',
        'Best club',
        'user-123',
      );

      const mockClub = Club.create(command.name, command.description, command.userId);
      mockClubRepository.create.mockResolvedValue(mockClub);

      // Act
      await handler.execute(command);

      // Assert
      expect(mockClubRepository.create).toHaveBeenCalledWith(
        expect.objectContaining({
          getName: expect.any(Function),
        }),
      );

      const callArg = mockClubRepository.create.mock.calls[0][0];
      expect(callArg.getName().getValue()).toBe('Volley Club Paris');
    });

    it('should propagate repository errors', async () => {
      // Arrange
      const command = new CreateClubCommand('Club', 'Desc', 'user-123');
      mockClubRepository.create.mockRejectedValue(new Error('Database error'));

      // Act & Assert
      await expect(handler.execute(command))
        .rejects
        .toThrow('Database error');
    });
  });
});
```

### Query Handler Tests

```typescript
// tests/unit/application/queries/get-club.handler.spec.ts

import { GetClubHandler } from '../../../../application/queries/get-club/get-club.handler';
import { GetClubQuery } from '../../../../application/queries/get-club/get-club.query';
import { IClubRepository } from '../../../../domain/repositories/club.repository.interface';
import { Club } from '../../../../domain/entities/club.entity';
import { ClubDetailReadModel } from '../../../../application/read-models/club-detail.read-model';

describe('GetClubHandler', () => {
  let handler: GetClubHandler;
  let mockClubRepository: jest.Mocked<IClubRepository>;

  beforeEach(() => {
    mockClubRepository = {
      create: jest.fn(),
      findById: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
    } as jest.Mocked<IClubRepository>;

    handler = new GetClubHandler(mockClubRepository);
  });

  describe('execute()', () => {
    it('should return club read model when club exists', async () => {
      // Arrange
      const query = new GetClubQuery('club-123');

      const mockClub = Club.create('Club Paris', 'Description', 'user-123');
      mockClubRepository.findById.mockResolvedValue(mockClub);

      // Act
      const result = await handler.execute(query);

      // Assert
      expect(result).toBeDefined();
      expect(result.id).toBe(mockClub.getId());
      expect(result.name).toBe('Club Paris');
      expect(mockClubRepository.findById).toHaveBeenCalledWith('club-123');
    });

    it('should throw NotFoundException when club does not exist', async () => {
      // Arrange
      const query = new GetClubQuery('non-existent-id');
      mockClubRepository.findById.mockResolvedValue(null);

      // Act & Assert
      await expect(handler.execute(query))
        .rejects
        .toThrow('Club with ID non-existent-id not found');
    });

    it('should transform domain entity to read model correctly', async () => {
      // Arrange
      const query = new GetClubQuery('club-123');
      const mockClub = Club.create('Club Paris', 'Best club', 'user-123');
      mockClubRepository.findById.mockResolvedValue(mockClub);

      // Act
      const result = await handler.execute(query);

      // Assert
      expect(result).toMatchObject({
        id: mockClub.getId(),
        name: 'Club Paris',
        description: 'Best club',
      });
    });
  });
});
```

## 🔗 3. Integration Tests (MANDATORY - Critical Workflows)

### Handler → Repository → Database Integration

**Objectif** : Tester le flux complet de bout en bout avec une vraie base de données

**Ce qui DOIT être testé** :
- ✅ Complete workflows: Handler → Repository → Database
- ✅ Transactions and rollbacks
- ✅ Concurrent operations
- ✅ Real database constraints

#### Template Integration Test

```typescript
// tests/integration/handlers/create-club.integration.spec.ts

import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication } from '@nestjs/common';
import { PrismaService } from '../../../src/prisma/prisma.service';
import { CreateClubHandler } from '../../../src/club-management/application/commands/create-club/create-club.handler';
import { CreateClubCommand } from '../../../src/club-management/application/commands/create-club/create-club.command';
import { ClubRepository } from '../../../src/club-management/infrastructure/persistence/repositories/club.repository';
import { CLUB_REPOSITORY } from '../../../src/club-management/domain/repositories/club.repository.interface';

describe('CreateClubHandler Integration', () => {
  let app: INestApplication;
  let prismaService: PrismaService;
  let handler: CreateClubHandler;

  beforeAll(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      providers: [
        PrismaService,
        CreateClubHandler,
        {
          provide: CLUB_REPOSITORY,
          useClass: ClubRepository,
        },
      ],
    }).compile();

    app = moduleFixture.createNestApplication();
    await app.init();

    prismaService = moduleFixture.get<PrismaService>(PrismaService);
    handler = moduleFixture.get<CreateClubHandler>(CreateClubHandler);
  });

  beforeEach(async () => {
    // Clean database before each test
    await prismaService.club.deleteMany({});
  });

  afterAll(async () => {
    await app.close();
  });

  it('should create club in database successfully', async () => {
    // Arrange
    const command = new CreateClubCommand(
      'Volley Club Integration',
      'Integration test club',
      'user-integration-123',
    );

    // Act
    const clubId = await handler.execute(command);

    // Assert
    const savedClub = await prismaService.club.findUnique({
      where: { id: clubId },
    });

    expect(savedClub).toBeDefined();
    expect(savedClub.name).toBe('Volley Club Integration');
    expect(savedClub.description).toBe('Integration test club');
    expect(savedClub.ownerId).toBe('user-integration-123');
  });

  it('should enforce database constraints (unique name per user)', async () => {
    // Arrange
    const command1 = new CreateClubCommand('Club Name', 'Desc', 'user-123');
    const command2 = new CreateClubCommand('Club Name', 'Desc 2', 'user-123');

    // Act
    await handler.execute(command1);

    // Assert
    await expect(handler.execute(command2))
      .rejects
      .toThrow(); // Database unique constraint
  });

  it('should rollback transaction on error', async () => {
    // Arrange
    const command = new CreateClubCommand(
      'Club Rollback',
      'Test rollback',
      'invalid-user-id', // Foreign key violation
    );

    // Act & Assert
    await expect(handler.execute(command)).rejects.toThrow();

    // Verify no club was created
    const clubs = await prismaService.club.findMany({});
    expect(clubs).toHaveLength(0);
  });
});
```

## 📊 Coverage Requirements

### Exigences STRICTES par couche

- **Domain Layer**: **100% coverage** (TOUS les methods, TOUTES les branches)
- **Application Layer**: **95%+ coverage**
- **Integration Tests**: **TOUS les workflows critiques**

### Commandes de coverage

```bash
# Run tests with coverage
cd volley-app-backend
yarn test:cov

# View coverage report
open coverage/lcov-report/index.html
```

### Vérification de la coverage

```json
// jest.config.js - Coverage thresholds
{
  "coverageThreshold": {
    "global": {
      "branches": 80,
      "functions": 80,
      "lines": 80,
      "statements": 80
    },
    "**/domain/**/*.ts": {
      "branches": 100,
      "functions": 100,
      "lines": 100,
      "statements": 100
    }
  }
}
```

## ✅ Test Naming Convention

### Règle de nommage

```typescript
describe('[Unit Under Test]', () => {
  describe('[Method/Feature]', () => {
    it('should [expected behavior] when [condition]', () => {
      // Test
    });
  });
});
```

### Exemples

```typescript
describe('Subscription Entity', () => {
  describe('canCreateTeam()', () => {
    it('should return true when subscription is active and limit not reached', () => {});
    it('should return false when subscription is inactive', () => {});
    it('should return false when team limit is reached', () => {});
  });
});

describe('CreateClubHandler', () => {
  describe('execute()', () => {
    it('should create club successfully with valid data', () => {});
    it('should throw ValidationException when name is missing', () => {});
  });
});
```

## 🔄 Test Execution Order (TDD Approach)

### 1. RED Phase (Write failing test)

```typescript
it('should return true when subscription allows team creation', () => {
  const subscription = Subscription.create('club-123', SubscriptionPlan.FREE);
  expect(subscription.canCreateTeam()).toBe(true); // FAILS (method doesn't exist)
});
```

### 2. GREEN Phase (Implement minimal code to pass)

```typescript
// domain/entities/subscription.entity.ts
canCreateTeam(): boolean {
  return true; // Minimal implementation
}
```

### 3. REFACTOR Phase (Improve code while keeping tests green)

```typescript
canCreateTeam(): boolean {
  if (!this.isActive()) return false;
  if (!this.plan.hasTeamLimit()) return true;
  return this.currentTeamsCount < this.plan.getMaxTeams();
}
```

### Workflow de Développement TDD

1. **Écrire les tests Domain Layer FIRST** (entities, value objects, services)
2. **Implémenter le Domain Layer** pour passer les tests (TDD)
3. **Écrire les tests Application Layer** (handlers)
4. **Implémenter l'Application Layer**
5. **Écrire les Integration tests**
6. **Implémenter Infrastructure et Presentation layers**

## 🛠️ Outils et Configuration

### Jest Configuration

```javascript
// jest.config.js
module.exports = {
  moduleFileExtensions: ['js', 'json', 'ts'],
  rootDir: 'src',
  testRegex: '.*\\.spec\\.ts$',
  transform: {
    '^.+\\.(t|j)s$': 'ts-jest',
  },
  collectCoverageFrom: [
    '**/*.(t|j)s',
    '!**/*.spec.ts',
    '!**/node_modules/**',
  ],
  coverageDirectory: '../coverage',
  testEnvironment: 'node',
};
```

### Running Tests

```bash
# Run all tests
yarn test

# Run tests in watch mode
yarn test:watch

# Run tests with coverage
yarn test:cov

# Run specific test file
yarn test create-club.handler.spec.ts

# Run integration tests only
yarn test:e2e
```

## 🎓 Exemples Concrets du Projet

### Bounded Context `club-management`

Tests existants à consulter :
- `tests/unit/domain/entities/subscription.entity.spec.ts`
- `tests/unit/application/commands/create-club.handler.spec.ts`
- `tests/integration/handlers/subscribe-to-plan.integration.spec.ts`

Référence : `volley-app-backend/src/club-management/tests/`

## 🚨 Erreurs Courantes à Éviter

1. ❌ **Ne pas tester les edge cases**
   - ✅ FAIRE : Tester null, undefined, limites, valeurs négatives
   - ❌ NE PAS FAIRE : Tester uniquement le happy path

2. ❌ **Tests qui testent l'implémentation au lieu du comportement**
   - ✅ FAIRE : Tester ce que fait la méthode (behavior)
   - ❌ NE PAS FAIRE : Tester comment elle le fait (implementation)

3. ❌ **Tests qui dépendent d'autres tests**
   - ✅ FAIRE : Chaque test est indépendant
   - ❌ NE PAS FAIRE : Tests qui s'exécutent dans un ordre spécifique

4. ❌ **Mocks dans les tests Domain Layer**
   - ✅ FAIRE : Tester les entités pures sans mocks
   - ❌ NE PAS FAIRE : Mocker des Value Objects ou Services dans les tests d'entités

5. ❌ **Ne pas nettoyer la DB dans les tests d'intégration**
   - ✅ FAIRE : `beforeEach(() => prisma.club.deleteMany())`
   - ❌ NE PAS FAIRE : Laisser les données s'accumuler

## 📚 Skills Complémentaires

Pour aller plus loin :
- **ddd-bounded-context** : Architecture DDD complète
- **cqrs-command-query** : Patterns CQRS pour Commands/Queries
- **testing** : Standards généraux de tests (unit, integration, frontend)

---

**Rappel** : Les tests sont la **documentation vivante** de votre logique métier. Un test bien écrit vaut mieux que 100 lignes de commentaires.
