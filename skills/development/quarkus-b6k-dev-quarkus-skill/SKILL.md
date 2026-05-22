---
name: quarkus
description: Guides Quarkus development across REST APIs, CDI dependency injection, Hibernate ORM, Panache, configuration, OpenAPI, templates, messaging, security, observability, packaging, and tooling. Use when building Quarkus applications, adding endpoints or clients, configuring datasources or OIDC, debugging build or runtime issues, or choosing extensions.
license: MIT
metadata:
  author: b6k-dev
  version: "0.1.0"
---

# Quarkus

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
│  ├─ Need asynchronous delivery, replay, or broker-managed fan-out
│  │  └─ messaging
│  ├─ Need synchronous request/response calls
│  │  └─ service-communication
│  │     ├─ Shared protobuf contract and HTTP/2 streaming fit well
│  │     │  └─ service-communication-grpc
│  │     └─ Standard HTTP/JSON or simpler interoperability matters more
│  │        └─ service-communication-rest
├─ Authentication, authorization, identity providers
│  ├─ Need core Quarkus security concepts, RBAC, built-in auth mechanisms, or custom policies
│  │  └─ security-core
│  ├─ Protect endpoints with OpenID Connect
│  │  ├─ Inbound bearer tokens, browser login redirects, or hybrid OIDC apps
│  │  │  └─ security-oidc
│  │  └─ Outbound token acquisition, refresh, exchange, or propagation to downstream services
│  │     └─ security-oidc-client
│  ├─ Need JWT verification or token building without full OIDC integration
│  │  └─ security-jwt
│  ├─ Need username/password identity stores backed by JPA, JDBC, or LDAP
│  │  └─ security-identity-providers
│  ├─ Need passkeys or WebAuthn flows
│  │  └─ security-webauthn
│  └─ Need to test secured applications
│     └─ security-testing
├─ Logging, health, metrics, traces
│  ├─ Need help choosing signals, management exposure, or local observability stack
│  │  └─ observability
│  ├─ Logging configuration, JSON logs, MDC, and log shipping
│  │  └─ observability-logging
│  ├─ Liveness/readiness/startup probes and Health UI
│  │  └─ observability-health
│  ├─ Metrics, Micrometer registries, and Prometheus/OTLP export
│  │  └─ observability-metrics
│  └─ Distributed tracing, propagation, and OpenTelemetry
│     └─ observability-tracing
├─ Native image, jars, and container packaging
│  └─ native-and-packaging
│     ├─ Need a native build, closed-world metadata, native SSL, or native-only runtime behavior
│     │  └─ native-image
│     ├─ Need JVM artifact shape decisions: `fast-jar`, `uber-jar`, `mutable-jar`, layout, or re-augmentation
│     │  └─ packaging-jars
│     └─ Need container image packaging: Jib, Docker, Podman, OpenShift, Buildpacks, tags, push, or base images
│        └─ packaging-containers
├─ Testing 
│  └─ Start with the feature module you are testing (for example `security-testing` or `native-image`)
└─ Dev mode, CLI, build plugins
   └─ tooling
```

## General guidelines 

- Quarkus resolves much of its framework wiring at build time, so expect many integration mistakes to fail during build or startup rather than deep at runtime.
- Align all extension versions through the Quarkus platform BOM.
- Start with the smallest extension set, then add only what the feature needs.
- Never skip writing high-level integration tests and prefer them opposed to unit testing individual components. Only write unit tests when they are actually beneficial, e.g. implementing methods with complex logic
