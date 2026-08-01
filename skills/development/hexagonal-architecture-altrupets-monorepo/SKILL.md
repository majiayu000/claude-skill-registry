---
name: hexagonal-architecture
description: '| ID | backend-hexagonal-architecture |'
---

# 🗄️ Skill: Arquitectura Hexagonal (Backend)

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `backend-hexagonal-architecture` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `hexagonal`, `hexagonal-architecture`, `ports-and-adapters`, `ddd`, `domain-driven-design` |
| **Referencia** | [Alistair Cockburn - Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) |

## 🔑 Keywords para Invocación

Usa cualquiera de estos keywords en tus prompts para invocar este skill:

- `hexagonal`
- `hexagonal-architecture`
- `ports-and-adapters`
- `backend-hexagonal`
- `@skill:hexagonal`

### Ejemplos de Prompts

```
Crea un microservicio usando arquitectura hexagonal
```

```
Implementa un caso de uso siguiendo el patrón ports and adapters
```

```
@skill:hexagonal - Estructura el módulo de usuarios con arquitectura hexagonal en NestJS
```

## 📖 Descripción

La **Arquitectura Hexagonal**, también conocida como **Ports and Adapters**, es un patrón de diseño que tiene como objetivo crear sistemas desacoplados, donde la lógica de negocio central (el Dominio) esté aislada de las tecnologías externas (Bases de datos, Frameworks, APIs externas, UIs).

Esta arquitectura permite que una aplicación sea igualmente dirigida por usuarios, programas, tests automatizados o scripts, y sea desarrollada y testead aislada de sus dispositivos de runtime y bases de datos eventuales.

### ✅ Cuándo Usar Este Skill

- Aplicaciones empresariales complejas.
- Cuando la lógica de negocio es el activo más valioso y debe protegerse de cambios tecnológicos.
- Proyectos que requieren alta testabilidad (Unit Testing sin mocks complejos de frameworks).
- Sistemas que podrían cambiar de base de datos o framework en el futuro.
- Microservicios que deben ser mantenibles a largo plazo.

### ❌ Cuándo NO Usar Este Skill

- Prototipos o MVPs rápidos donde la velocidad de entrega prima sobre la arquitectura.
- Aplicaciones CRUD extremadamente simples.
- Scripts pequeños o herramientas de línea de comandos simples.

## 🏗️ Estructura del Proyecto (NestJS)

```
src/
├── modules/
│   └── users/
│       ├── domain/                 # 1. Capa de Dominio (El Corazón)
│       │   ├── entities/           # Entidades de dominio (Reglas de negocio)
│       │   ├── value-objects/      # Objetos de valor (Email, Password, etc.)
│       │   ├── repositories/       # INTERFACES de repositorios (Ports de salida)
│       │   ├── services/           # Servicios de dominio (Opcional)
│       │   └── events/             # Eventos de dominio
│       │
│       ├── application/            # 2. Capa de Aplicación (Casos de Uso)
│       │   ├── use-cases/          # Casos de uso (Orquestación)
│       │   ├── dtos/               # Objetos de transferencia de datos (Entrada/Salida)
│       │   ├── mappers/            # Transformadores entre Dominio y DTOs
│       │   └── ports/              # INTERFACES de entrada (Ports de entrada)
│       │
│       ├── infrastructure/         # 3. Capa de Infraestructura (Detalles)
│       │   ├── persistence/        # Implementación de repositorios (TypeORM, Prisma, etc.)
│       │   │   ├── entities/       # Entidades de base de datos (Opcional si usas mappers)
│       │   │   └── repositories/   # Implementación real (Adapters de salida)
│       │   ├── http/               # Controladores o Resolvers (Adapters de entrada)
│       │   │   ├── controllers/
│       │   │   └── resolvers/
│       │   ├── external-services/  # Clientes para APIs externas, SendGrid, etc.
│       │   └── modules/            # NestJS Modules para inyección de dependencias
│       │
│       └── users.module.ts         # Punto de entrada de NestJS
```

## 💻 Implementación

### 1. Capa de Dominio (Sin dependencias externas)

Las entidades de dominio no deben depender de TypeORM, Sequelize o cualquier otro framework.

```typescript
// src/modules/users/domain/entities/user.entity.ts
export class User {
  constructor(
    private readonly id: string,
    private name: string,
    private email: string,
    private isActive: boolean,
  ) {}

  public static create(id: string, name: string, email: string): User {
    // Validaciones de negocio aquí
    return new User(id, name, email, true);
  }

  public deactivate(): void {
    this.isActive = false;
  }

  // Getters
  getId(): string { return this.id; }
  getName(): string { return this.name; }
  getEmail(): string { return this.email; }
  getIsActive(): boolean { return this.isActive; }
}

// src/modules/users/domain/repositories/user.repository.interface.ts
// Port de Salida
export interface IUserRepository {
  save(user: User): Promise<void>;
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
}
```

### 2. Capa de Aplicación (Casos de Uso)

Orquesta el flujo de datos desde y hacia las entidades de dominio.

```typescript
// src/modules/users/application/use-cases/create-user.use-case.ts
import { Inject, Injectable } from '@nestjs/common';
import { User } from '../../domain/entities/user.entity';
import { IUserRepository } from '../../domain/repositories/user.repository.interface';
import { CreateUserDto } from '../dtos/create-user.dto';

@Injectable()
export class CreateUserUseCase {
  constructor(
    @Inject('IUserRepository')
    private readonly userRepository: IUserRepository,
  ) {}

  async execute(dto: CreateUserDto): Promise<void> {
    const existingUser = await this.userRepository.findByEmail(dto.email);
    if (existingUser) {
      throw new Error('User already exists');
    }

    const user = User.create(
      crypto.randomUUID(),
      dto.name,
      dto.email
    );

    await this.userRepository.save(user);
  }
}
```

### 3. Capa de Infraestructura (Detalles tecnológicos)

Implementa las interfaces (Adapters) y expone la aplicación al exterior.

```typescript
// src/modules/users/infrastructure/persistence/repositories/typeorm-user.repository.ts
// Adapter de Salida
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { User } from '../../../domain/entities/user.entity';
import { IUserRepository } from '../../../domain/repositories/user.repository.interface';
import { UserEntity } from '../entities/user.entity'; // Entidad de DB

@Injectable()
export class TypeOrmUserRepository implements IUserRepository {
  constructor(
    @InjectRepository(UserEntity)
    private readonly repository: Repository<UserEntity>,
  ) {}

  async save(user: User): Promise<void> {
    const dbUser = new UserEntity();
    dbUser.id = user.getId();
    dbUser.name = user.getName();
    dbUser.email = user.getEmail();
    dbUser.isActive = user.getIsActive();

    await this.repository.save(dbUser);
  }

  async findByEmail(email: string): Promise<User | null> {
    const dbUser = await this.repository.findOneBy({ email });
    if (!dbUser) return null;

    return new User(dbUser.id, dbUser.name, dbUser.email, dbUser.isActive);
  }

  // ... rest of methods
}
```

```typescript
// src/modules/users/infrastructure/http/controllers/user.controller.ts
// Adapter de Entrada
import { Controller, Post, Body } from '@nestjs/common';
import { CreateUserUseCase } from '../../../application/use-cases/create-user.use-case';
import { CreateUserDto } from '../../../application/dtos/create-user.dto';

@Controller('users')
export class UserController {
  constructor(private readonly createUserUseCase: CreateUserUseCase) {}

  @Post()
  async create(@Body() dto: CreateUserDto) {
    return await this.createUserUseCase.execute(dto);
  }
}
```

### 4. Inyección de Dependencias (NestJS Module)

Es crucial vincular la interfaz (Port) con la implementación (Adapter).

```typescript
// src/modules/users/users.module.ts
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { CreateUserUseCase } from './application/use-cases/create-user.use-case';
import { UserController } from './infrastructure/http/controllers/user.controller';
import { UserEntity } from './infrastructure/persistence/entities/user.entity';
import { TypeOrmUserRepository } from './infrastructure/persistence/repositories/typeorm-user.repository';

@Module({
  imports: [TypeOrmModule.forFeature([UserEntity])],
  controllers: [UserController],
  providers: [
    CreateUserUseCase,
    {
      provide: 'IUserRepository',
      useClass: TypeOrmUserRepository,
    },
  ],
})
export class UsersModule {}
```

## 🧪 Testing Strategy

La Arquitectura Hexagonal facilita enormemente los tests, especialmente los unitarios de lógica de negocio.

### Unit Testing (Domain/Application)
No requieren base de datos, solo mocks de las interfaces.

```typescript
// test/users/application/create-user.use-case.spec.ts
describe('CreateUserUseCase', () => {
  it('should create a user successfully', async () => {
    const mockRepo: IUserRepository = {
      save: jest.fn(),
      findByEmail: jest.fn().mockResolvedValue(null),
      findById: jest.fn()
    };

    const useCase = new CreateUserUseCase(mockRepo);
    await useCase.execute({ name: 'John', email: 'john@example.com' });

    expect(mockRepo.save).toHaveBeenCalled();
  });
});
```

## 🏆 Mejores Prácticas

1. **Dependencias hacia adentro:** La capa de infraestructura puede conocer a la de aplicación y dominio. La de aplicación solo al dominio. El dominio no conoce a nadie.
2. **Sin Miedo a los Mappers:** Aunque parezca repetitivo, mapear de `UserEntity` (DB) a `User` (Dominio) asegura que un cambio en la base de datos no rompa el negocio.
3. **Usa Interfaces para Todo lo Externo:** Bases de datos, APIs de terceros, Sistemas de archivos, etc.
4. **Validaciones en el Dominio:** La entidad de dominio debe ser responsable de su propia integridad.
5. **DIP (Dependency Inversion Principle):** Siempre inyecta interfaces, no clases concretas de infraestructura en tus casos de uso.

---
**💡 Tip:** Si usas GraphQL, los `Resolvers` van en `infrastructure/http/resolvers/` de la misma manera que los controladores REST.
