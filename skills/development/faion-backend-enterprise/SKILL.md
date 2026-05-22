---
name: faion-backend-enterprise
description: "Enterprise backends: Java, C#, PHP, Ruby."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Backend Developer: Enterprise

Enterprise web backend development in Java, C#, PHP, and Ruby.

## Purpose

Handles enterprise-grade web applications using Spring Boot, ASP.NET Core, Laravel, and Rails frameworks.

---

## Context Discovery

### Auto-Investigation

| Signal | How to Check | What It Tells Us |
|--------|--------------|------------------|
| `pom.xml` | `Glob("**/pom.xml")` | Java Maven |
| `build.gradle` | `Glob("**/build.gradle*")` | Java Gradle |
| Spring Boot | `Grep("spring-boot", "**/pom.xml")` | Spring Boot project |
| `*.csproj` | `Glob("**/*.csproj")` | .NET project |
| `Program.cs` | `Glob("**/Program.cs")` | .NET entry point |
| `composer.json` | `Read("composer.json")` | PHP dependencies |
| Laravel | `Grep("laravel", "composer.json")` | Laravel framework |
| `Gemfile` | `Read("Gemfile")` | Ruby dependencies |
| Rails | `Grep("rails", "Gemfile")` | Rails framework |

### Discovery Questions

#### Q1: Enterprise Framework (if not detected)

```yaml
question: "Which enterprise framework?"
header: "Framework"
multiSelect: false
options:
  - label: "Java Spring Boot"
    description: "Enterprise Java, microservices"
  - label: "C# ASP.NET Core"
    description: "Microsoft .NET ecosystem"
  - label: "PHP Laravel"
    description: "Elegant PHP web framework"
  - label: "Ruby on Rails"
    description: "Convention over configuration"
```

#### Q2: Application Type

```yaml
question: "What type of application?"
header: "Type"
multiSelect: false
options:
  - label: "REST API"
    description: "Backend API service"
  - label: "Full-stack web app"
    description: "Server-rendered + API"
  - label: "Microservice"
    description: "Part of larger system"
  - label: "Background jobs"
    description: "Async processing, queues"
```

#### Q3: ORM/Data Access

```yaml
question: "How do you access data?"
header: "ORM"
multiSelect: false
options:
  - label: "Framework ORM (JPA/EF/Eloquent/ActiveRecord)"
    description: "Standard ORM patterns"
  - label: "Raw SQL / Query builder"
    description: "Direct database access"
  - label: "Mix of both"
    description: "ORM for simple, SQL for complex"
```

---

## When to Use

- Java Spring Boot applications
- C# ASP.NET Core services
- PHP Laravel projects
- Ruby Rails applications
- Enterprise patterns and testing

## Methodologies (25 files)

**Java (6):** java-jpa-hibernate, java-junit-testing, java-spring, java-spring-async, java-spring-boot, java-spring-boot-patterns

**C# (6):** csharp-aspnet-core, csharp-background-services, csharp-dotnet, csharp-dotnet-patterns, csharp-entity-framework, csharp-xunit-testing

**PHP (7):** decomposition-laravel, laravel-patterns, php-eloquent, php-laravel, php-laravel-patterns, php-laravel-queues, php-phpunit-testing

**Ruby (6):** decomposition-rails, ruby-activerecord, ruby-rails, ruby-rails-patterns, ruby-rspec-testing, ruby-sidekiq-jobs

## Tools

**Java:** Spring Boot 3.x, Hibernate, JUnit 5, Maven/Gradle
**C#:** .NET 8+, ASP.NET Core, Entity Framework Core, xUnit
**PHP:** Laravel 11, Eloquent, PHPUnit, Composer
**Ruby:** Rails 7+, ActiveRecord, RSpec, Sidekiq, Bundler

## Related Sub-Skills

| Sub-skill | Relationship |
|-----------|--------------|
| faion-backend-developer:systems | Systems-level backends (Go, Rust, databases) |
| faion-python-developer | Python backends (Django, FastAPI) |
| faion-javascript-developer | Node.js backends |
| faion-api-developer | API design patterns |

## Integration

Invoked by parent skill `faion-backend-developer` for Java/C#/PHP/Ruby work.

---

*faion-backend-developer:enterprise v1.0 | 25 methodologies*
