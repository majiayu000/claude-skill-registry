---
description: "Symfony hexagonal architecture setup — project structure, module scaffolding, layer responsibilities, dependency rules. Triggers on: architecture, module, layer, hexagonal, scaffold, project structure, directory structure, new project, new module"
---

# Symfony Hexagonal Architecture

You are an expert in Symfony hexagonal architecture (ports & adapters). Use this skill when users need to set up project structure, create new modules, or understand layer responsibilities.

## When to Activate

- User wants to create a new Symfony project with hexagonal architecture
- User asks about project structure or directory layout
- User wants to scaffold a new module/bounded context
- User asks about layer responsibilities or dependency rules
- User mentions "hexagonal", "ports and adapters", "clean architecture" in Symfony context

## Core Principles

### Layer Direction (STRICT)
```
Presentation → Application → Domain ← Infrastructure
```

Infrastructure depends on Domain (implements ports), but Domain NEVER depends on Infrastructure.

### Module Structure

Every module follows this structure under `src/`:

```
Domain/{Module}/
├── Entity/          # Aggregates and entities (pure PHP)
├── ValueObject/     # Immutable value objects
├── Event/           # Domain events (past-tense)
├── Exception/       # Domain-specific exceptions
└── Port/            # Interfaces for external dependencies

Application/{Module}/
├── Command/         # Write operations (final readonly)
├── Query/           # Read operations (final readonly)
├── DTO/             # Data transfer objects
└── EventHandler/    # Domain event handlers

Infrastructure/{Module}/
├── Persistence/     # Doctrine repositories, mappings
├── Messaging/       # Messenger handlers, transports
└── ExternalService/ # HTTP clients, third-party APIs

Presentation/{Module}/
├── API/             # REST controllers
├── CLI/             # Console commands
└── GraphQL/         # GraphQL resolvers/types
```

## Progressive Refactoring (Existing Projects)

When working on an existing project that doesn't follow hexagonal architecture:

### Step 1: Detect Current Structure
Before writing any code, check:
```
- Is src/ organized by layer (Domain/, Application/, etc.) or by traditional Symfony (Controller/, Entity/, Repository/)?
- Does the module the user is working on already follow hexagonal patterns?
- Are there Doctrine annotations directly on entities?
```

### Step 2: Ask the User
When the user requests a feature/change in a non-hexagonal module, ALWAYS ask:

> "Bu modül (`{Module}`) şu anda hexagonal yapıda değil. Şu seçeneklerden birini tercih edebilirsiniz:
> 1. **Önce refactor**: `{Module}` modülünü hexagonal mimariye taşıyıp, sonra yeni özelliği ekleyeyim
> 2. **Sadece yeni kodu hexagonal yap**: Mevcut koda dokunmadan, yeni eklenen kısımları hexagonal yapıda oluşturayım
> 3. **Mevcut yapıda devam et**: Bu sefer hexagonal yapıyı atlayalım
>
> Hangisini tercih edersiniz?"

### Step 3: Incremental Migration (if user chooses refactor)
Migrate one layer at a time, in this order:

1. **Domain first**: Extract entities to `Domain/{Module}/Entity/`, create value objects, define port interfaces
2. **Application second**: Create Commands/Queries/Handlers, move business logic out of controllers/services
3. **Infrastructure third**: Move Doctrine repositories to `Infrastructure/{Module}/Persistence/`, extract mappings
4. **Presentation last**: Thin out controllers, add `ApiResponseTrait`, apply `#[IsGranted]`

After each layer, verify the code still works before moving to the next.

### Key Principles
- **Never touch modules the user isn't working on** — only refactor what's in scope
- **One module at a time** — don't try to migrate the whole project
- **Keep the app working** — each step should be a working state
- **Respect user's pace** — some teams prefer gradual migration over months

## Scaffolding a New Module

When user asks to create a new module, generate ALL directories and base files:

1. Create directory structure (all 4 layers)
2. Create a sample port interface in `Domain/{Module}/Port/`
3. Create a sample repository adapter in `Infrastructure/{Module}/Persistence/`
4. Bind the port to adapter in `services.yaml`
5. Suggest initial entities, commands, and queries based on the module purpose

## Key Rules

1. **Domain purity**: No `use Symfony\...` or `use Doctrine\...` in any Domain file
2. **Port-first**: Define the interface before the implementation
3. **One module = one bounded context**: Modules communicate via events, not direct calls
4. **Namespace convention**: `App\Domain\{Module}\...`, `App\Application\{Module}\...`, etc.

## References

See `references/` for detailed guides:
- `directory-structure.md` — Full directory layout with file examples
- `layer-responsibilities.md` — What belongs in each layer
- `dependency-rules.md` — Import rules and PHPStan enforcement
