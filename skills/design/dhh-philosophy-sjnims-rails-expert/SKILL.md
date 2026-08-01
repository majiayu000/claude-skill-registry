---
name: dhh-philosophy
description: This skill should be used when the user asks about Rails philosophy,
  DHH's principles, the Rails way, "convention over configuration", "majestic monolith",
  "omakase", "sharp knives", NO BUILD, integra
---

---
name: dhh-philosophy
description: This skill should be used when the user asks about Rails philosophy, DHH's principles, the Rails way, "convention over configuration", "majestic monolith", "omakase", "sharp knives", NO BUILD, integrated systems, programmer happiness, or general Rails 8 design principles. Also use when discussing why Rails makes certain architectural decisions or when comparing Rails approaches to alternatives. Examples:

<example>
Context: User is considering microservices architecture
user: "Should I split my Rails app into microservices?"
assistant: "I'll consult the DHH Philosophy skill to provide guidance on Rails architectural principles."
<commentary>
This question relates to the "majestic monolith" philosophy and integrated systems principle.
</commentary>
</example>

<example>
Context: User is frustrated by Rails conventions
user: "Why does Rails force me to put controllers in app/controllers?"
assistant: "Let me explain the Convention over Configuration philosophy and how it benefits development."
<commentary>
This relates to core Rails philosophy and the omakase principle.
</commentary>
</example>

<example>
Context: User is setting up build tooling
user: "What build tool should I use for my Rails 8 app?"
assistant: "Rails 8 embraces the NO BUILD philosophy. Let me explain how this works."
<commentary>
This directly relates to Rails 8's NO BUILD principle and Propshaft.
</commentary>
</example>
---

# DHH Philosophy & Rails 8 Principles

## Overview

Rails is opinionated software, and that opinion comes from creator David Heinemeier Hansson (DHH) and the Rails core team. Understanding Rails philosophy is essential to working effectively with the framework. Rails 8 doubles down on these principles while introducing new ones that reflect modern web development realities.

Rails is designed to make programming web applications easier by making assumptions about what every developer needs to get started. It allows writing less code while accomplishing more than many other languages and frameworks. Experienced Rails developers report that it makes web application development more fun.

The framework makes the assumption that there is a "best" way to do things, and it's designed to encourage that way—and in some cases to discourage alternatives. If you learn "The Rails Way," you'll discover a tremendous increase in productivity. If you persist in bringing old habits from other languages to Rails development, and trying to use patterns learned elsewhere, you may have a less happy experience.

## Core Rails Principles

### Don't Repeat Yourself (DRY)

DRY is a principle of software development stating that "Every piece of knowledge must have a single, unambiguous, authoritative representation within a system." By not writing the same information over and over again, code is more maintainable, more extensible, and less buggy.

In practice, DRY means:
- Database schema drives model attributes (no need to declare them)
- Conventions eliminate configuration files
- Shared partials avoid duplicate views
- Helpers and concerns extract common patterns
- Generators create consistent boilerplate

### Convention Over Configuration

Rails has opinions about the best way to do many things in a web application, and defaults to this set of conventions rather than requiring endless configuration files.

Key conventions:
- File structure matches URL structure
- Model names are singular, table names are plural
- Controllers are plural, resources are plural
- Database columns follow naming patterns (`user_id`, `created_at`)
- Standard CRUD actions (`index`, `show`, `new`, `create`, `edit`, `update`, `destroy`)

This means a `Product` model automatically:
- Maps to a `products` table
- Uses `ProductsController` for web requests
- Finds views in `app/views/products/`
- Routes via `resources :products`

No configuration files needed—it just works.

## DHH's Philosophical Principles

### The Menu is Omakase

Omakase (Japanese for "I'll leave it up to you") means trusting the chef to serve what's best. Rails is omakase software. DHH and the Rails team curate a full-stack experience with carefully chosen defaults.

This means:
- Rails bundles everything needed (ORM, testing, mailers, jobs, etc.)
- Default choices are carefully considered
- Removing defaults requires opt-out, not opt-in
- The "happy path" is well-lit and smooth

Fight this and you'll struggle. Embrace it and you'll fly.

### Optimize for Programmer Happiness

Rails prioritizes developer joy and productivity over other concerns. This manifests in:
- Beautiful, readable code
- Minimal boilerplate
- Helpful error messages
- Automatic code reloading in development
- Sensible naming that reads like English
- Tools that feel good to use

Code should be a joy to write and maintain. If it's painful, Rails wants to fix it.

### Exalt Beautiful Code

Rails values code aesthetics. Beautiful code is:
- Readable and expressive
- Concise without being cryptic
- Consistent in style
- Self-documenting through good naming
- Free of unnecessary abstractions

This isn't vanity—beautiful code is easier to understand, modify, and debug.

### Provide Sharp Knives

Rails gives you powerful tools and trusts you to use them responsibly. It doesn't infantilize developers with excessive safety rails.

Examples:
- Direct SQL when needed (`find_by_sql`)
- `eval` and metaprogramming available
- Callbacks with full power
- Database-level features accessible
- Strong parameters, not whitelist-by-default

With power comes responsibility. Rails assumes you're a professional.

### Value Integrated Systems (The Majestic Monolith)

Rails champions the integrated monolith over distributed microservices for most applications. Benefits:
- Simpler deployment
- Easier debugging
- Shared code and database
- Transactions that work
- No network latency between components
- One codebase to understand

Microservices have their place, but most applications don't need that complexity. Start with a monolith, extract services only when truly necessary.

See `references/majestic-monolith.md` for detailed discussion.

### Progress Over Stability (With Nuance)

Rails values moving forward over maintaining perfect backward compatibility. But this doesn't mean breaking changes without reason:
- Deprecation cycles warn before removal
- Upgrade guides detail changes
- LTS versions available for stability
- Breaking changes bring real improvements

Rails 8 removed deprecated features from Rails 7, ensuring the codebase stays clean and modern.

### Fat Models, Skinny Controllers

Business logic belongs in models, not controllers. Controllers should:
- Parse requests
- Delegate to models
- Render responses

They should not:
- Contain business logic
- Make multiple database queries
- Perform calculations
- Handle complex workflows

Models encapsulate domain logic. Controllers coordinate HTTP concerns.

### The One-Person Framework

Rails empowers small teams to build big things. A single developer can:
- Build full-stack applications
- Deploy to production
- Handle millions of requests
- Maintain the codebase over years

This doesn't mean you must work alone—it means you can if you want to.

## Rails 8-Specific Principles

Rails 8 introduces new philosophical directions while maintaining core principles.

### NO BUILD

Rails 8 eliminates complex JavaScript build toolchains for most applications. No webpack, no esbuild, no complex configurations.

Instead:
- **Propshaft** replaces Sprockets (simpler asset pipeline)
- **Import maps** for JavaScript modules (browser-native)
- **Turbo** and **Stimulus** for interactivity (minimal JS)
- CSS and JS served directly to browsers

Build tools add complexity, slow development, and break frequently. Modern browsers support ES modules natively. Most apps don't need a build step.

See `references/no-build.md` for implementation details.

### Database-Backed Everything (Solid*)

Rails 8 replaces external dependencies with database-backed solutions:

- **Solid Cache**: Replace Redis/Memcached for fragment caching
- **Solid Queue**: Replace Sidekiq/Resque for background jobs
- **Solid Cable**: Replace Redis for Action Cable pub/sub

Benefits:
- Fewer moving parts
- Simpler deployment
- One database to backup
- Familiar query tools
- Lower hosting costs
- Built on modern SQL features (`FOR UPDATE SKIP LOCKED`)

This is the integrated systems philosophy applied to infrastructure.

See `references/solid-suite.md` for technical details.

### Deploy Anywhere with Kamal 2

Rails 8 includes **Kamal 2** for zero-downtime deployments to any Linux server. No PaaS lock-in, no Kubernetes complexity.

Philosophy:
- Own your infrastructure
- Simple Docker-based deploys
- No vendor lock-in
- One command deploys (`kamal deploy`)
- **Kamal Proxy** replaces Traefik
- Registry-free deploys possible (8.1+)

This embodies self-sufficiency and simplicity.

See `references/kamal-philosophy.md` for deployment approach.

### Authentication, Not Authorization

Rails 8 includes a session-based authentication generator—but not authorization (roles, permissions).

Philosophy:
- Every app needs auth
- Every app's permissions differ
- Provide starting point, not framework
- Simple beats complex
- Code over gems when possible

The generator creates:
- Session-based authentication
- Password reset flow
- Metadata tracking (sign-in count, etc.)
- Tested, production-ready code

You customize from there.

### Thruster for Production Performance

Rails 8's Dockerfile includes **Thruster**, a Rust-based proxy that:
- Handles X-Sendfile acceleration
- Caches assets efficiently
- Compresses responses
- Sits in front of Puma

Philosophy: Production should be fast by default, without complex reverse proxy setup.

## How Philosophy Manifests in Practice

### Conventions Eliminate Decisions

With conventions, you don't decide:
- Where files go
- How URLs map to code
- How database tables relate
- What CRUD actions to implement
- How forms submit data

You follow the convention and move on to actual problems.

### Generators Encode Best Practices

Running `rails generate scaffold Product name:string price:decimal` creates:
- Migration
- Model with validations
- Controller with all CRUD actions
- Views for all actions
- Routes
- Tests

Everything follows conventions. You customize what you need, delete what you don't.

### Rails is a Framework, Not a Library

Rails is opinionated and integrated. You work within its structure, not alongside it. This trade-off gives:
- Faster development
- Shared understanding across teams
- Easier onboarding
- Better documentation
- Ecosystem consistency

You sacrifice some flexibility for massive productivity gains.

### Configuration is Available When Needed

While conventions dominate, Rails is configurable when necessary:
- `config/application.rb` for app-wide settings
- `config/routes.rb` for custom routing
- `config/database.yml` for database config
- Initializers for gem configuration
- ENV vars for secrets

Convention first, configuration when needed.

## Common Philosophical Questions

**Q: Why not microservices?**
A: Most apps don't have the scale or team size that justifies microservices complexity. Start with a monolith, extract services only when truly necessary. See `references/majestic-monolith.md`.

**Q: Why not TypeScript?**
A: TypeScript adds build complexity and ceremony. Ruby is dynamically typed and that's intentional. Tests provide safety. See `references/no-build.md`.

**Q: Why include so much in the framework?**
A: Integration is a feature. Curated defaults reduce decision fatigue. Everything works together smoothly. See `references/integrated-systems.md`.

**Q: Why the strong opinions?**
A: Opinions enable conventions. Conventions eliminate configuration. Less configuration means more time solving actual problems.

**Q: What if I disagree with Rails opinions?**
A: You can configure around them, but you'll fight the framework. Better to find a framework aligned with your preferences or embrace "The Rails Way."

## Rails 8 in Action: Philosophy to Code

Rails 8's major features demonstrate philosophy in practice:

**Kamal 2**: Deploy anywhere simply (self-sufficiency, simplicity)
**Thruster**: Fast by default (performance without complexity)
**Solid Cache/Queue/Cable**: Database-backed infrastructure (integrated systems)
**Propshaft**: No build needed (NO BUILD, simplicity)
**Authentication Generator**: Code over frameworks (sharp knives, pragmatism)
**Local CI**: Run tests locally (developer productivity, fast feedback)
**Markdown Rendering**: Modern needs met simply (pragmatic evolution)

Every feature reflects philosophical principles.

## Embracing the Philosophy

To work effectively with Rails:

1. **Trust the defaults** until you have specific reasons not to
2. **Follow conventions** even if they seem arbitrary at first
3. **Read the guides** to understand the "Rails Way"
4. **Resist over-engineering** early
5. **Start with the monolith** before distributing
6. **Use Rails tools** (generators, rake tasks, console)
7. **Embrace productivity** over architectural purity
8. **Value shipping** over perfect code

Rails optimizes for building and shipping. Let it.

## Further Reading

For deeper exploration of Rails philosophy:

- **`references/core-principles.md`**: Detailed examination of DRY and Convention over Configuration
- **`references/majestic-monolith.md`**: Why monoliths beat microservices for most apps
- **`references/no-build.md`**: Rails 8's NO BUILD philosophy and implementation
- **`references/solid-suite.md`**: Database-backed infrastructure (Solid Cache/Queue/Cable)
- **`references/integrated-systems.md`**: The value of integration over distribution
- **`references/kamal-philosophy.md`**: Deployment philosophy and Kamal 2

For code examples demonstrating principles:

- **`examples/convention-over-configuration.rb`**: How conventions eliminate code
- **`examples/dry-in-practice.rb`**: DRY principle in action
- **`examples/fat-models-skinny-controllers.rb`**: Proper logic placement

## Summary

Rails philosophy is about:
- **Programmer happiness** through beautiful, productive code
- **Convention over configuration** to eliminate decision fatigue
- **Integrated systems** (the majestic monolith) for simplicity
- **Progress** through continuous improvement
- **Sharp knives** that trust developers
- **NO BUILD** for faster development
- **Database-backed infrastructure** for fewer dependencies
- **Deploy anywhere** with simple tools

These aren't arbitrary opinions—they're battle-tested principles from building thousands of successful applications.

Embrace the philosophy, trust the framework, and ship amazing software.
