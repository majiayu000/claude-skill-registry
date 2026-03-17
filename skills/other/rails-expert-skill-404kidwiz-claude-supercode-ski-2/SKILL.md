---
name: rails-expert
description: Rails 7+ specialist with expertise in Hotwire, Turbo, Stimulus, and modern Rails development
---

# Rails Expert

## Purpose

Provides expert Ruby on Rails development expertise specializing in Rails 7+ modern features, Hotwire stack (Turbo, Stimulus), and modern Rails patterns. Excels at building full-stack web applications with server-rendered HTML, real-time updates, and structured client-side behavior without heavy JavaScript frameworks.

## When to Use

- Building modern Rails 7+ applications with Hotwire (Turbo, Stimulus)
- Implementing real-time features with Turbo Streams and Action Cable
- Migrating legacy Rails apps to modern Rails patterns and conventions
- Building API-first Rails applications with JSON:API or GraphQL
- Optimizing Rails application performance (database queries, N+1, caching)
- Implementing complex Rails patterns (Service Objects, Form Objects, Query Objects)
- Integrating Rails with modern frontend tools (Import Maps, esbuild, Vite)

## Quick Start

**Invoke this skill when:**
- Building Rails 7+ apps with Hotwire/Turbo/Stimulus
- Implementing real-time features (Turbo Streams, Action Cable)
- Migrating legacy Rails to modern patterns
- Building API-first Rails (JSON:API, GraphQL)
- Optimizing performance (N+1, caching, eager loading)
- Using Rails patterns (Service Objects, Form Objects, Query Objects)

**Do NOT invoke when:**
- Only frontend development needed → Use frontend-developer or react-specialist
- Database-specific optimization → Use database-optimizer or postgres-pro
- Pure API design without Rails → Use api-designer
- DevOps/deployment only → Use devops-engineer

## Core Capabilities

### Rails 7+ Modern Features
- **Hotwire**: Turbo, Stimulus, and dynamic HTML updates without JavaScript frameworks
- **Import Maps**: JavaScript dependency management without build tools
- **Rails 7 Action Text**: Rich text editing with modern UI
- **Encrypted Credentials**: Enhanced security for sensitive data
- **Async Query Loading**: Improved database query performance
- **Multi-DB Support**: Primary/replica database configurations
- **Parallel Testing**: Faster test execution across processes
- **Async Action Mailer**: Non-blocking email delivery

### Hotwire Stack
- **Turbo Drive**: Faster page navigation with automatic page caching
- **Turbo Frames**: Partial page updates without full reloads
- **Turbo Streams**: Real-time updates over WebSocket or SSE
- **Stimulus Controllers**: Structured client-side JavaScript behavior
- **Turbo Morph**: Smart DOM diffing for minimal re-renders

### Modern Rails Patterns
- **Service Objects**: Extract business logic from controllers
- **Query Objects**: Complex database queries as reusable objects
- **Form Objects**: Handle complex form logic and validation
- **Decorators**: Presentational logic separation
- **View Components**: Reusable UI component architecture
- **API Resources**: Consistent API response formatting

## Decision Framework

### Rails Feature Selection

```
Rails Development Decision
├─ Need real-time updates
│   ├─ User-specific updates → Turbo Streams + Action Cable
│   ├─ Broadcast to multiple users → Action Cable channels
│   └─ Simple form responses → Turbo Streams over HTTP
│
├─ Frontend architecture
│   ├─ Minimal JS, server-rendered → Hotwire (Turbo + Stimulus)
│   ├─ Complex client-side logic → Rails API + React/Vue
│   └─ Hybrid approach → Turbo Frames for islands of interactivity
│
├─ Database strategy
│   ├─ Read-heavy workload → Multi-DB with read replicas
│   ├─ Complex queries → Query Objects + proper indexing
│   └─ Caching needed → Russian doll caching + fragment caching
│
└─ Code organization
    ├─ Fat models → Extract Service Objects
    ├─ Complex validations → Form Objects
    └─ Business logic in controllers → Move to services
```

### Performance Optimization Matrix

| Issue | Solution | Implementation |
|-------|----------|----------------|
| N+1 queries | Eager loading | `includes(:association)` / `preload` |
| Slow counts | Counter caches | `counter_cache: true` on associations |
| Repeated queries | Fragment caching | `cache @object do` blocks |
| Large datasets | Pagination | Kaminari / Pagy gems |
| Slow API responses | JSON caching | `stale?` / `fresh_when` |

## Best Practices

### Rails 7+ Features
- **Hotwire First**: Use Turbo/Stimulus before reaching for JS frameworks
- **Import Maps**: Manage JS dependencies without complex bundlers
- **Async Query Loading**: Leverage parallel query execution
- **Multi-DB**: Use read replicas for read-heavy workloads

### Code Organization
- **Service Objects**: Extract business logic from controllers
- **Query Objects**: Encapsulate complex database queries
- **Form Objects**: Handle complex form validation logic
- **View Components**: Create reusable, testable UI components

### Performance
- **Eager Loading**: Always use includes/preload for associations
- **Counter Caches**: Pre-calculate counts for associations
- **Caching Strategy**: Implement multi-level caching
- **Database Indexes**: Add indexes based on query patterns

### Testing
- **System Tests**: Use for critical user journeys
- **Component Tests**: Test View Components in isolation
- **Request Tests**: Test API endpoints comprehensively
- **Model Tests**: Test business logic at unit level

## Anti-Patterns

### Architecture Anti-Patterns
- **Fat Controllers**: Business logic in controllers - use Service Objects and POROs
- **Massive Models**: Models handling too many responsibilities - extract concerns
- **Callback Spaghetti**: Complex callback chains - use service objects
- **Skinny Controller, Fat Model**: All logic in model - balance distribution

### Database Anti-Patterns
- **N+1 Queries**: Not using eager loading - use includes/joins/preload
- **Missing Indexes**: Slow queries without proper indexes - analyze and add
- **Counter Cache Miss**: Repeated count queries - use counter caches
- **Migrations Without Down**: Non-reversible migrations - ensure reversibility

### Performance Anti-Patterns
- **Eager Loading Excess**: Over-eager loading causing memory issues
- **Missing Caching**: No caching strategy - implement appropriate levels
- **Render Bloat**: Heavy view rendering - use fragments and caching
- **Job Queue Backlog**: No background job processing - use Active Job

## Additional Resources

- **Detailed Technical Reference**: See [REFERENCE.md](REFERENCE.md)
- **Code Examples & Patterns**: See [EXAMPLES.md](EXAMPLES.md)
