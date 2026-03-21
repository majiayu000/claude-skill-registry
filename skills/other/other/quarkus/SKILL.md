---
name: quarkus-platform
description: Guides implementation, debugging, and architecture decisions across the Quarkus platform and extension ecosystem. Use when building or maintaining Quarkus applications, selecting extensions, or troubleshooting build and runtime behavior.
---

# Quarkus Platform

Use this as the entrypoint skill for Quarkus work in any kind of project.
Use decision tree below to find the right domain, then load detailed references.

## Decision Tree

```
What do you need?
├─ Dependency injection (CDI / ArC)
│  └─ dependency-injection
├─ Application configuration (.properties, profiles, config mapping)
│  └─ configuration
├─ REST and HTTP APIs
│  └─ web-rest
├─ Templates and server-side rendering (Qute)
│  └─ templates
├─ OpenAPI and API contract documentation
│  └─ openapi
├─ Databases, ORM, migrations, data access
│  ├─ Standard JPA / Hibernate ORM usage
│  │  └─ data-orm
│  ├─ Panache entities and repositories for simpler CRUD/data access
│  │  └─ data-panache
│  ├─ Schema migrations and database evolution with Flyway
│  │  └─ data-migrations
│  └─ Advanced Hibernate ORM features: multiple persistence units, multitenancy, caching, extension points
│     └─ data-orm-advanced
├─ Event streaming and asynchronous messaging channels
│  ├─ Is the event crossing a service/process boundary?
│  │  └─ YES -> messaging
│  └─ NO (in-process only)
│     ├─ Need clustering or non-blocking event loop behavior
│     │  └─ YES -> vertx-event-bus
│     └─ Want portability and type safety
│        └─ YES -> cdi-events
├─ Communicating with external APIs, communication between services
│  └─ service-communication
├─ Authentication, authorization, identity providers
│  └─ security
├─ Logging, health, metrics, traces, 
│  └─ observability
├─ Native image, jars, and container packaging
│  └─ native-and-packaging
├─ Testing 
│  └─ testing 
└─ Dev mode, CLI, build plugins
   └─ tooling
```

## General guidelines 

- Align all extension versions through the Quarkus platform BOM.
- Start with the smallest extension set, then add only what the feature needs.
- Never skip writing high-level integration tests and prefer them opposed to unit testing individual components. Only write unit tests when they are actually beneficial, e.g. implementing methods with complex logic
