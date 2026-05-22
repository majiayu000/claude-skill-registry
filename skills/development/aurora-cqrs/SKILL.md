---
name: aurora-cqrs
description: >
    Aurora CQRS Architecture Reference - Understanding the CQRS structure,
    component relationships, editable zones, and data flow in Aurora/NestJS
    projects. Trigger: When needing to understand CQRS architecture, component
    structure, or editable zones.
license: MIT
metadata:
    author: aurora
    version: '1.1'
    auto_invoke:
        'Understanding CQRS architecture, component structure, editable zones'
---

## When to Use

Use this skill as a **REFERENCE** when:

- Understanding CQRS architecture and component relationships
- Learning what Commands, Queries, Handlers, Events, Sagas are
- Identifying which zones in generated files are editable
- Understanding the data flow between layers
- Learning the structure of Services, Repositories, Aggregates, Mappers

**⚠️ For IMPLEMENTING business logic in handlers, use `aurora-development` skill
instead.**

This skill is for UNDERSTANDING the architecture. The `aurora-development` skill
is for WRITING code.

## What is CQRS in Aurora?

**CQRS** (Command Query Responsibility Segregation) separates read operations
(Queries) from write operations (Commands).

Aurora implements CQRS using NestJS CQRS module with:

- **Commands** → Change state (Create, Update, Delete)
- **Queries** → Read state (Find, Get, Paginate, Count, etc.)
- **Handlers** → Execute commands/queries
- **Events** → Domain events triggered by aggregates
- **Sagas** → Coordinate complex workflows

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    @api Layer (REST/GraphQL)                 │
│  Controllers/Resolvers → Handlers → dispatch Commands/Queries│
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   @app/application Layer                     │
│  Commands → CommandHandlers → Services                       │
│  Queries  → QueryHandlers   → Services                       │
│  Events   → EventHandlers                                    │
│  Sagas    → React to events                                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    @app/domain Layer                         │
│  Aggregates (Entities with events)                           │
│  Value Objects (Immutable types)                             │
│  Repository Interfaces                                       │
│  Mappers (Domain ↔ Response)                                 │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                @app/infrastructure Layer                     │
│  Repository Implementations (Sequelize/TypeORM)              │
│  Seeders, Models                                             │
└─────────────────────────────────────────────────────────────┘
```

## Critical Patterns

### ⚠️ EDITABLE ZONES (CRITICAL!)

**In Aurora-generated files, you can ONLY edit these zones:**

```typescript
// ✅ Command Handler - ONLY the execute() method body
@CommandHandler(CreateTeslaModelCommand)
export class CreateTeslaModelCommandHandler {
    async execute(command: CreateTeslaModelCommand): Promise<void> {
        // ✅ ADD YOUR CUSTOM LOGIC HERE
        // Example: validations, business rules, external calls

        if (command.payload.year < 2008) {
            throw new TeslaYearInvalidException('Tesla first car was in 2008');
        }

        // The rest is generated code (don't modify)
        await this.service.main(payload, command.cQMetadata);
    }
}
```

**DO NOT modify:**

- ❌ Command/Query class definitions
- ❌ Service main() methods (unless custom service)
- ❌ Repository interfaces
- ❌ Aggregates (entities)
- ❌ Value Objects
- ❌ Mappers

### Marking Custom Code

**Always mark custom code with AI-generated comments:**

```typescript
async execute(command: CreateTeslaModelCommand): Promise<void> {
    /* #region AI-generated code */
    // Custom validation
    if (command.payload.year < 2008) {
        throw new TeslaYearInvalidException('Tesla first car was in 2008');
    }

    // Custom business logic
    const isValidPrice = await this.priceValidator.validate(command.payload.price);
    if (!isValidPrice) {
        throw new TeslaPriceInvalidException();
    }
    /* #endregion AI-generated code */

    // Generated code continues...
    await this.service.main(payload, command.cQMetadata);
}
```

## Commands

### Command Structure

```typescript
export class CreateTeslaModelCommand {
    constructor(
        public readonly payload: {
            id: string;
            name: string;
            status: string;
            year: number;
            isActive: boolean;
        },
        public readonly cQMetadata?: CQMetadata,
    ) {}
}
```

**Characteristics:**

- Immutable (readonly)
- Contains payload (data to create/update)
- Contains cQMetadata (context: timezone, user, tenant, etc.)
- Represents an intention to change state

### Command Types

```typescript
// Create single record
CreateTeslaModelCommand;

// Create multiple records
CreateTeslaModelsCommand;

// Update by ID
UpdateTeslaModelByIdCommand;

// Update multiple (by query)
UpdateTeslaModelsCommand;

// Delete by ID
DeleteTeslaModelByIdCommand;

// Delete multiple (by query)
DeleteTeslaModelsCommand;

// Upsert (insert or update)
UpsertTeslaModelCommand;

// Custom command with increment
UpdateAndIncrementTeslaModelsCommand;
```

## Command Handlers

### Basic Structure

```typescript
@CommandHandler(CreateTeslaModelCommand)
export class CreateTeslaModelCommandHandler implements ICommandHandler<CreateTeslaModelCommand> {
    constructor(private readonly service: CreateTeslaModelService) {}

    async execute(command: CreateTeslaModelCommand): Promise<void> {
        // ✅ EDITABLE ZONE - Add custom logic here

        // Call the service (generated)
        await this.service.main(
            {
                id: new TeslaModelId(command.payload.id),
                name: new TeslaModelName(command.payload.name),
                status: new TeslaModelStatus(command.payload.status),
                year: new TeslaModelYear(command.payload.year),
                isActive: new TeslaModelIsActive(command.payload.isActive),
            },
            command.cQMetadata,
        );
    }
}
```

### Handler with Custom Logic

```typescript
@CommandHandler(CreateTeslaModelCommand)
export class CreateTeslaModelCommandHandler implements ICommandHandler<CreateTeslaModelCommand> {
    constructor(
        private readonly service: CreateTeslaModelService,
        private readonly validator: TeslaModelValidator, // Custom service
        private readonly notifier: NotificationService, // Custom service
    ) {}

    async execute(command: CreateTeslaModelCommand): Promise<void> {
        /* #region AI-generated code */
        // Step 1: Custom validation
        await this.validator.validate(command.payload);

        // Step 2: Business rule
        if (command.payload.year < 2008) {
            throw new TeslaYearInvalidException(
                'Tesla first production car (Roadster) was in 2008',
            );
        }

        // Step 3: Check duplicates (custom logic)
        const exists = await this.service.repository.find({
            queryStatement: {
                where: { name: command.payload.name },
            },
        });

        if (exists) {
            throw new TeslaModelAlreadyExistsException();
        }
        /* #endregion AI-generated code */

        // Step 4: Execute service (generated)
        await this.service.main(
            {
                id: new TeslaModelId(command.payload.id),
                name: new TeslaModelName(command.payload.name),
                status: new TeslaModelStatus(command.payload.status),
                year: new TeslaModelYear(command.payload.year),
                isActive: new TeslaModelIsActive(command.payload.isActive),
            },
            command.cQMetadata,
        );

        /* #region AI-generated code */
        // Step 5: Post-creation actions
        await this.notifier.notifyNewModel(command.payload);
        /* #endregion AI-generated code */
    }
}
```

### Handler with Return Value

```typescript
// Some handlers return data (like upsert, update)
@CommandHandler(UpsertTeslaModelCommand)
export class UpsertTeslaModelCommandHandler implements ICommandHandler<UpsertTeslaModelCommand> {
    async execute(
        command: UpsertTeslaModelCommand,
    ): Promise<TeslaModelResponse> {
        const model = await this.service.main(payload, command.cQMetadata);

        return this.mapper.mapAggregateToResponse(model);
    }
}
```

## Queries

### Query Structure

```typescript
export class GetTeslaModelsQuery {
    constructor(
        public readonly queryStatement?: QueryStatement,
        public readonly constraint?: QueryStatement,
        public readonly cQMetadata?: CQMetadata,
    ) {}
}
```

**Characteristics:**

- Contains queryStatement (user filters, pagination, sorting)
- Contains constraint (system/security filters)
- Contains cQMetadata (context)
- Used for read operations

### Query Types

```typescript
// Find single record
FindTeslaModelQuery;

// Find by ID
FindTeslaModelByIdQuery;

// Get multiple records
GetTeslaModelsQuery;

// Paginate records
PaginateTeslaModelsQuery;

// Count records
CountTeslaModelQuery;

// Max value
MaxTeslaModelQuery;

// Min value
MinTeslaModelQuery;

// Sum values
SumTeslaModelQuery;

// Raw SQL
RawSQLTeslaModelsQuery;
```

## Query Handlers

### Basic Structure

```typescript
@QueryHandler(GetTeslaModelsQuery)
export class GetTeslaModelsQueryHandler implements IQueryHandler<GetTeslaModelsQuery> {
    private readonly mapper: TeslaModelMapper = new TeslaModelMapper();

    constructor(private readonly service: GetTeslaModelsService) {}

    async execute(query: GetTeslaModelsQuery): Promise<TeslaModelResponse[]> {
        // Get models from service
        const models = await this.service.main(
            query.queryStatement,
            query.constraint,
            query.cQMetadata,
        );

        // Skip mapping if requested
        if (query.cQMetadata?.excludeMapModelToAggregate) {
            return models;
        }

        // Map aggregates to responses
        return this.mapper.mapAggregatesToResponses(models);
    }
}
```

### Handler with Custom Logic

```typescript
@QueryHandler(GetTeslaModelsQuery)
export class GetTeslaModelsQueryHandler implements IQueryHandler<GetTeslaModelsQuery> {
    private readonly mapper: TeslaModelMapper = new TeslaModelMapper();

    constructor(
        private readonly service: GetTeslaModelsService,
        private readonly cache: CacheService, // Custom service
    ) {}

    async execute(query: GetTeslaModelsQuery): Promise<TeslaModelResponse[]> {
        /* #region AI-generated code */
        // Try cache first
        const cacheKey = this.buildCacheKey(query);
        const cached = await this.cache.get(cacheKey);
        if (cached) return cached;
        /* #endregion AI-generated code */

        // Get from database
        const models = await this.service.main(
            query.queryStatement,
            query.constraint,
            query.cQMetadata,
        );

        if (query.cQMetadata?.excludeMapModelToAggregate) {
            return models;
        }

        const responses = this.mapper.mapAggregatesToResponses(models);

        /* #region AI-generated code */
        // Cache results
        await this.cache.set(cacheKey, responses, 3600);
        /* #endregion AI-generated code */

        return responses;
    }
}
```

## Services

### Command Service Structure

```typescript
@Injectable()
export class CreateTeslaModelService {
    constructor(
        private readonly publisher: EventPublisher,
        private readonly repository: TeslaIModelRepository,
    ) {}

    async main(
        payload: {
            id: TeslaModelId;
            name: TeslaModelName;
            status: TeslaModelStatus;
            year: TeslaModelYear;
            isActive: TeslaModelIsActive;
        },
        cQMetadata?: CQMetadata,
    ): Promise<void> {
        // 1. Create aggregate with factory pattern
        const model = TeslaModel.register(
            payload.id,
            payload.name,
            payload.status,
            payload.year,
            payload.isActive,
            new TeslaModelCreatedAt({ currentTimestamp: true }),
            new TeslaModelUpdatedAt({ currentTimestamp: true }),
            null, // deletedAt
        );

        // 2. Persist to database
        await this.repository.create(model, {
            createOptions: cQMetadata?.repositoryOptions,
        });

        // 3. Merge EventBus with aggregate
        const modelRegister = this.publisher.mergeObjectContext(model);

        // 4. Apply and commit events
        modelRegister.created({
            payload: model,
            cQMetadata,
        });
        modelRegister.commit();
    }
}
```

### Query Service Structure

```typescript
@Injectable()
export class GetTeslaModelsService {
    constructor(private readonly repository: TeslaIModelRepository) {}

    async main(
        queryStatement?: QueryStatement,
        constraint?: QueryStatement,
        cQMetadata?: CQMetadata,
    ): Promise<TeslaModel[]> {
        return await this.repository.get({
            queryStatement,
            constraint,
            cQMetadata,
        });
    }
}
```

### Custom Service (Not Generated)

```typescript
@Injectable()
export class TeslaModelValidator {
    constructor(private readonly repository: TeslaIModelRepository) {}

    async validate(payload: any): Promise<void> {
        // Custom validation logic
        if (!payload.name || payload.name.length < 3) {
            throw new TeslaModelNameInvalidException();
        }

        // Check unique constraints
        const exists = await this.repository.find({
            queryStatement: {
                where: { name: payload.name },
            },
        });

        if (exists) {
            throw new TeslaModelAlreadyExistsException();
        }
    }
}
```

## Events

### Event Structure

```typescript
export class CreatedTeslaModelEvent {
    constructor(
        public readonly event: {
            payload: {
                id: string;
                name: string;
                status: string;
                year: number;
                isActive: boolean;
                createdAt?: string;
                updatedAt?: string;
                deletedAt?: string;
            };
            cQMetadata?: CQMetadata;
        },
    ) {}
}
```

### Aggregate Event Methods

```typescript
export class TeslaModel extends AggregateRoot {
    // Apply created event
    created(event: { payload: TeslaModel; cQMetadata?: CQMetadata }): void {
        this.apply(
            new CreatedTeslaModelEvent({
                payload: {
                    id: event.payload.id.value,
                    name: event.payload.name.value,
                    status: event.payload.status.value,
                    year: event.payload.year.value,
                    isActive: event.payload.isActive.value,
                    createdAt: event.payload.createdAt?.value,
                    updatedAt: event.payload.updatedAt?.value,
                    deletedAt: event.payload.deletedAt?.value,
                },
                cQMetadata: event.cQMetadata,
            }),
        );
    }

    // Apply updated event
    updated(event: { payload: TeslaModel; cQMetadata?: CQMetadata }): void {
        this.apply(new UpdatedTeslaModelEvent({...}));
    }

    // Apply deleted event
    deleted(event: { payload: TeslaModel; cQMetadata?: CQMetadata }): void {
        this.apply(new DeletedTeslaModelEvent({...}));
    }
}
```

## Event Handlers

### Basic Structure

```typescript
@EventsHandler(CreatedTeslaModelEvent)
export class CreatedTeslaModelEventHandler implements IEventHandler<CreatedTeslaModelEvent> {
    handle(event: CreatedTeslaModelEvent): void {
        // ✅ EDITABLE ZONE - Implement event reaction here
        console.log('Tesla model created:', event.event.payload.id);
    }
}
```

### Handler with Custom Logic

```typescript
@EventsHandler(CreatedTeslaModelEvent)
export class CreatedTeslaModelEventHandler implements IEventHandler<CreatedTeslaModelEvent> {
    constructor(
        private readonly notifier: NotificationService,
        private readonly analytics: AnalyticsService,
    ) {}

    async handle(event: CreatedTeslaModelEvent): Promise<void> {
        /* #region AI-generated code */
        // Send notification
        await this.notifier.notify({
            type: 'MODEL_CREATED',
            data: event.event.payload,
        });

        // Track analytics
        await this.analytics.track('model.created', {
            modelId: event.event.payload.id,
            modelName: event.event.payload.name,
        });

        // Log to audit system
        console.log('New Tesla model created:', {
            id: event.event.payload.id,
            name: event.event.payload.name,
            timestamp: new Date().toISOString(),
        });
        /* #endregion AI-generated code */
    }
}
```

## Sagas

### Saga Structure

```typescript
@Injectable()
export class TeslaModelSagas {
    // Example saga: When model is created, create initial inventory
    @Saga()
    modelCreated = (events$: Observable<any>): Observable<ICommand> => {
        return events$.pipe(
            ofType(CreatedTeslaModelEvent),
            delay(1000),
            map((event) => {
                // Return command to execute
                return new CreateInitialInventoryCommand({
                    modelId: event.event.payload.id,
                    quantity: 0,
                });
            }),
        );
    };

    // Example saga: When model is deleted, delete related records
    @Saga()
    modelDeleted = (events$: Observable<any>): Observable<ICommand> => {
        return events$.pipe(
            ofType(DeletedTeslaModelEvent),
            map((event) => {
                return new DeleteUnitsCommand({
                    modelId: event.event.payload.id,
                });
            }),
        );
    };
}
```

## Aggregates

### Aggregate Structure

```typescript
export class TeslaModel extends AggregateRoot {
    // Properties (Value Objects)
    id: TeslaModelId;
    name: TeslaModelName;
    status: TeslaModelStatus;
    year: TeslaModelYear;
    isActive: TeslaModelIsActive;
    createdAt: TeslaModelCreatedAt;
    updatedAt: TeslaModelUpdatedAt;
    deletedAt: TeslaModelDeletedAt;

    constructor(...) {
        super();
        // Assign properties
    }

    // Factory method
    static register(...): TeslaModel {
        return new TeslaModel(...);
    }

    // Event methods
    created(event: {...}): void { this.apply(new CreatedEvent(...)); }
    updated(event: {...}): void { this.apply(new UpdatedEvent(...)); }
    deleted(event: {...}): void { this.apply(new DeletedEvent(...)); }
}
```

## Repositories

### Repository Interface

```typescript
export abstract class TeslaIModelRepository implements IRepository<TeslaModel> {
    abstract readonly repository: any;

    // Query methods
    abstract paginate(options?: {...}): Promise<Pagination<TeslaModel>>;
    abstract find(options?: {...}): Promise<TeslaModel | null>;
    abstract findById(id: TeslaModelId, options?: {...}): Promise<TeslaModel | null>;
    abstract get(options?: {...}): Promise<TeslaModel[]>;
    abstract count(options?: {...}): Promise<number>;
    abstract max(column: string, options?: {...}): Promise<number>;
    abstract min(column: string, options?: {...}): Promise<number>;
    abstract sum(column: string, options?: {...}): Promise<number>;

    // Command methods
    abstract create(model: TeslaModel, options?: {...}): Promise<void>;
    abstract insert(models: TeslaModel[], options?: {...}): Promise<void>;
    abstract updateById(model: TeslaModel, options?: {...}): Promise<void>;
    abstract update(model: TeslaModel, options?: {...}): Promise<void>;
    abstract upsert(model: TeslaModel, options?: {...}): Promise<void>;
    abstract deleteById(id: TeslaModelId, options?: {...}): Promise<void>;
    abstract delete(options?: {...}): Promise<void>;
}
```

## Mappers

### Mapper Structure

```typescript
export class TeslaModelMapper implements IMapper {
    constructor(public options: MapperOptions = { eagerLoading: true }) {}

    // Model (DB) → Aggregate (Domain)
    mapModelToAggregate(
        model: LiteralObject,
        cQMetadata?: CQMetadata,
    ): TeslaModel {
        return TeslaModel.register(
            new TeslaModelId(model.id),
            new TeslaModelName(model.name),
            new TeslaModelStatus(model.status),
            new TeslaModelYear(model.year),
            new TeslaModelIsActive(model.isActive),
            new TeslaModelCreatedAt(model.createdAt),
            new TeslaModelUpdatedAt(model.updatedAt),
            new TeslaModelDeletedAt(model.deletedAt),
        );
    }

    // Aggregate (Domain) → Response (DTO)
    mapAggregateToResponse(model: TeslaModel): TeslaModelResponse {
        return {
            id: model.id.value,
            name: model.name.value,
            status: model.status.value,
            year: model.year.value,
            isActive: model.isActive.value,
            createdAt: model.createdAt?.value,
            updatedAt: model.updatedAt?.value,
            deletedAt: model.deletedAt?.value,
        };
    }
}
```

## Decision Trees

### When to use Command vs Query?

```
Operation changes state?
├─ YES → Use Command
│  ├─ Create → CreateXCommand + CreateXCommandHandler
│  ├─ Update → UpdateXCommand + UpdateXCommandHandler
│  ├─ Delete → DeleteXCommand + DeleteXCommandHandler
│  └─ Upsert → UpsertXCommand + UpsertXCommandHandler
│
└─ NO → Use Query
   ├─ Single record → FindXQuery + FindXQueryHandler
   ├─ Multiple records → GetXQuery + GetXQueryHandler
   ├─ Paginated → PaginateXQuery + PaginateXQueryHandler
   └─ Aggregate → CountXQuery / MaxXQuery / MinXQuery / SumXQuery
```

### Where to add custom logic?

```
Need validation before save?
└─ Add in CommandHandler.execute() before service call

Need to react to events?
└─ Create EventHandler

Need to coordinate multiple operations?
└─ Create Saga

Need to transform data?
└─ Use Mapper

Need custom query logic?
└─ Add in QueryHandler.execute() before/after service call

Need reusable business logic?
└─ Create custom Service and inject in Handler
```

## Best Practices

### ✅ DO

- Mark all custom code with `/* #region AI-generated code */` comments
- Only edit `execute()` method body in handlers
- Create custom services for reusable logic
- Use dependency injection for custom services
- Validate data in command handlers before calling service
- Use QueryStatement for complex filters
- Map aggregates to responses in query handlers
- Apply events in services (created, updated, deleted)
- Use sagas for cross-aggregate coordination
- Inject EventPublisher in command services
- Use Value Objects for type safety

### ❌ DON'T

- Don't modify generated Command/Query classes
- Don't modify Service main() methods (create custom services instead)
- Don't modify Repository interfaces
- Don't modify Aggregates or Value Objects
- Don't modify Mappers
- Don't put business logic in services (put in handlers or custom services)
- Don't bypass repository (always use repository interface)
- Don't create commands/queries manually (use Aurora CLI to regenerate)
- Don't forget to commit events (call `aggregate.commit()`)
- Don't use direct database access (use repository)

## Common Patterns

### Pattern 1: Command with Validation

```typescript
@CommandHandler(CreateTeslaModelCommand)
export class CreateTeslaModelCommandHandler {
    constructor(
        private readonly service: CreateTeslaModelService,
        private readonly validator: TeslaValidator,
    ) {}

    async execute(command: CreateTeslaModelCommand): Promise<void> {
        /* #region AI-generated code */
        // Pre-validation
        await this.validator.validate(command.payload);
        /* #endregion AI-generated code */

        // Execute service
        await this.service.main(payload, command.cQMetadata);
    }
}
```

### Pattern 2: Query with Cache

```typescript
@QueryHandler(GetTeslaModelsQuery)
export class GetTeslaModelsQueryHandler {
    constructor(
        private readonly service: GetTeslaModelsService,
        private readonly cache: CacheService,
    ) {}

    async execute(query: GetTeslaModelsQuery): Promise<TeslaModelResponse[]> {
        /* #region AI-generated code */
        const cached = await this.cache.get(key);
        if (cached) return cached;
        /* #endregion AI-generated code */

        const models = await this.service.main(...);
        const responses = this.mapper.mapAggregatesToResponses(models);

        /* #region AI-generated code */
        await this.cache.set(key, responses);
        /* #endregion AI-generated code */

        return responses;
    }
}
```

### Pattern 3: Event Handler with Side Effects

```typescript
@EventsHandler(CreatedTeslaModelEvent)
export class CreatedTeslaModelEventHandler {
    constructor(private readonly notifier: NotificationService) {}

    async handle(event: CreatedTeslaModelEvent): Promise<void> {
        /* #region AI-generated code */
        await this.notifier.sendEmail({
            to: 'admin@tesla.com',
            subject: 'New Model Created',
            body: `Model ${event.event.payload.name} created`,
        });
        /* #endregion AI-generated code */
    }
}
```

### Pattern 4: Saga Coordination

```typescript
@Injectable()
export class TeslaModelSagas {
    @Saga()
    createRelatedRecords = (events$: Observable<any>): Observable<ICommand> => {
        return events$.pipe(
            ofType(CreatedTeslaModelEvent),
            mergeMap((event) => [
                new CreateInventoryCommand({ modelId: event.event.payload.id }),
                new CreatePricingCommand({ modelId: event.event.payload.id }),
            ]),
        );
    };
}
```

## Resources

- **NestJS CQRS**: https://docs.nestjs.com/recipes/cqrs
- **Aurora Core**: `@aurorajs.dev/core` exports CQMetadata, IRepository, etc.
- **Project Structure**: `.claude/skills/aurora-project-structure/SKILL.md`
- **Aurora CLI**: `.claude/skills/aurora-cli/SKILL.md`

## Related Skills

- `aurora-development` - **USE THIS** for implementing business logic in
  handlers
- `aurora-project-structure` - Understand where CQRS components live
- `aurora-criteria` - Build complex QueryStatements for queries
- `typescript` - Type-safe implementation
- `aurora-cli` - Regenerate CQRS structure after YAML changes
