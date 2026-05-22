---
name: framework-conventions-guide
description: This skill should be used when writing code in any opinionated framework's distinctive style. It applies when writing framework-based applications, creating models/controllers/views, or any framework code. Triggers on code generation, refactoring requests, code review, or when the user mentions framework conventions. Embodies the philosophy of embracing framework conventions, fighting complexity, and choosing simplicity over cleverness.
user-invocable: false
---

<objective>
Apply framework-native conventions to code in ANY opinionated framework. This skill teaches the universal principles that framework creators follow, regardless of language or framework.
</objective>

<essential_principles>
## Core Philosophy

"The best code is the code you don't write. The second best is the code that's obviously correct."

**Embrace the framework:**
- Rich domain models over service layers
- Framework routing over custom routing
- Built-in patterns over imported patterns
- Framework's database tools, not external ORMs
- Build solutions before reaching for packages
- Trust the framework's opinions - they exist for good reasons

**What to avoid (universal anti-patterns):**
- External auth libraries when framework auth exists
- Complex permission systems over simple role checks
- External job queues when framework has one
- External caching when framework provides it
- Component libraries when templates work
- GraphQL when REST is sufficient
- Factory patterns in tests when fixtures/seeds work
- Microservices when a monolith suffices

**Development Philosophy:**
- Ship, Validate, Refine - get to production to learn
- Fix root causes, not symptoms
- Write-time operations over read-time computations
- Database constraints over application validations
- Simple code that works > clever code that impresses
</essential_principles>

<intake>
What are you working on?

1. **Controllers/Views** - Request handling, routing, responses
2. **Models/Data** - Domain logic, state management, queries
3. **Frontend** - Templates, components, interactivity
4. **Architecture** - Routing, auth, jobs, caching
5. **Testing** - Unit tests, integration tests, fixtures
6. **Dependencies** - What to use vs avoid
7. **Code Review** - Review against framework conventions
8. **General Guidance** - Philosophy and conventions

**Specify a number or describe your task and your framework (Django, Laravel, Next.js, etc.)**
</intake>

<routing>
| Response | Reference to Read |
|----------|-------------------|
| 1, "controller", "view", "route" | [universal-patterns.md](./references/universal-patterns.md) - REST patterns section |
| 2, "model", "data", "query", "orm" | [universal-patterns.md](./references/universal-patterns.md) - State and models section |
| 3, "frontend", "template", "component" | [universal-patterns.md](./references/universal-patterns.md) - Frontend section |
| 4, "architecture", "auth", "job", "cache" | [universal-patterns.md](./references/universal-patterns.md) |
| 5, "test", "testing" | [universal-patterns.md](./references/universal-patterns.md) - Testing section |
| 6, "dependency", "package", "library" | [anti-patterns.md](./references/anti-patterns.md) |
| 7, "review" | Read all references, then review code |
| 8, general task | Read relevant references based on context |

**After reading relevant references, apply patterns to the user's code.**
</routing>

<framework_detection>
Before providing guidance, identify the framework and load its specific conventions:

| Framework | Core Conventions | What to Embrace |
|-----------|------------------|-----------------|
| **Django** | Fat models, thin views, ORM queries | Admin, class-based views, forms, signals |
| **Laravel** | Eloquent, Blade, Facades, Artisan | Resource controllers, form requests, events |
| **Next.js** | Server components, file routing, API routes | App router, server actions, middleware |
| **Spring Boot** | Auto-config, dependency injection, JPA | Starters, repositories, @Transactional |
| **Phoenix** | Contexts, Ecto, LiveView, channels | Generators, PubSub, presence |
| **FastAPI** | Pydantic, async, dependency injection | OpenAPI, background tasks, middleware |
| **Rails** | Fat models, thin controllers, conventions | Hotwire, concerns, Active* libraries |
| **Remix** | Loaders, actions, nested routes | Form handling, progressive enhancement |
| **NestJS** | Decorators, modules, providers | Guards, interceptors, pipes |
</framework_detection>

<quick_reference>
## Universal Naming Conventions

**Actions:** Domain verbs that describe what happens
- Good: `card.close()`, `order.ship()`, `user.activate()`
- Bad: `card.setStatus('closed')`, `order.updateShipped(true)`

**Predicates:** Boolean queries derived from state
- Good: `card.closed?`, `order.shipped?`, `user.active?`
- Bad: `card.isClosed`, `order.getIsShipped()`

**Collections:** Descriptive scope names
- Good: `chronologically`, `alphabetically`, `recent`, `active`, `pending`
- Bad: `sortByDate`, `filterActive`, `getRecent`

## REST Mapping (Universal)

Instead of custom actions, create new resources:

```
Custom Action          →  RESTful Resource
POST /cards/:id/close  →  POST /cards/:id/closure
DELETE /cards/:id/close → DELETE /cards/:id/closure
POST /orders/:id/ship  →  POST /orders/:id/shipment
POST /users/:id/ban    →  POST /users/:id/ban
```

## State as Data (Universal)

Instead of boolean flags, use related records or enums:

```
Boolean Flag           →  State Record/Enum
card.closed = true     →  card.closure (record exists)
order.shipped = true   →  order.shipment (record exists)
user.status = 'banned' →  user.ban (record exists)

Query with joins/relations, not boolean comparisons:
- Cards with closures = closed cards
- Cards without closures = open cards
```

## The Framework Way

Before writing custom code, ask:
1. Does the framework have a built-in way to do this?
2. Is there a convention I should follow?
3. Will this surprise other developers familiar with the framework?
4. Am I fighting the framework or working with it?
</quick_reference>

<reference_index>
## Domain Knowledge

All detailed patterns in `references/`:

| File | Topics |
|------|--------|
| [universal-patterns.md](./references/universal-patterns.md) | REST mapping, state as data, naming, testing, frontend |
| [anti-patterns.md](./references/anti-patterns.md) | What to avoid, complexity traps, over-engineering signs |
</reference_index>

<success_criteria>
Code follows framework conventions when:
- Routes map to CRUD verbs on resources
- Models use framework's built-in composition patterns
- State is tracked via records/relations, not booleans
- No unnecessary service objects or abstractions
- Framework solutions preferred over external packages
- Tests use framework's built-in test utilities
- Interactivity uses framework's frontend solution
- Authorization logic lives close to domain
- Jobs are shallow wrappers calling domain methods
- Configuration uses framework patterns, not custom solutions
</success_criteria>

<philosophy>
## Why Convention Over Configuration?

1. **Shared vocabulary** - Everyone knows what to expect
2. **Faster onboarding** - New devs understand the codebase immediately
3. **Less decision fatigue** - Spend energy on business logic, not architecture
4. **Community support** - Problems are already solved and documented
5. **Upgrades are easier** - Framework updates don't break custom patterns

## The 90/10 Rule

The framework solves 90% of your problems elegantly. The remaining 10% often feels like it needs custom solutions, but usually:
- You're overcomplicating the requirement
- There's a framework pattern you haven't discovered
- The "limitation" is actually protecting you from a bad idea

When you truly need to go custom, document why and keep it isolated.
</philosophy>
