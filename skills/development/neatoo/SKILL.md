---
name: neatoo
description: Neatoo DDD framework for .NET with Blazor WebAssembly. Use when building domain entities with EntityBase, implementing business rules and validation, creating factories with [Factory] attribute, setting up client-server communication with RemoteFactory, working with aggregates and parent-child relationships, or troubleshooting source generator issues.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(dotnet:*), WebFetch, WebSearch
---

# Neatoo Framework Skill

## Description

Neatoo is a Domain-Driven Design (DDD) framework for .NET that simplifies building business applications with Blazor WebAssembly and WPF. It combines two core repositories:

- **Neatoo Core**: DDD framework with entities, rules, validation, and Roslyn source generators
- **Neatoo.RemoteFactory**: Client-server communication layer enabling shared domain models

## When to Use This Skill

Use this skill when:

- Building domain entities with EntityBase or ValidateBase classes
- Implementing business rules and validation logic
- Creating factory classes with [Factory] attribute
- Setting up client-server communication with RemoteFactory
- Working with aggregates and parent-child entity relationships
- Implementing data mapping between domain and persistence entities
- Building Blazor UI components with MudNeatoo
- Configuring authorization for factory operations
- Troubleshooting Neatoo source generator issues

## Reference Files

| File | Topics |
|------|--------|
| **entities.md** | EntityBase, ValidateBase, Value Objects, property patterns |
| **aggregates.md** | Aggregate roots, entity graphs, parent-child, complete examples |
| **rules.md** | Rules engine, data annotations, custom rules, async validation |
| **factories.md** | Create/Fetch/Save operations, Commands & Queries |
| **client-server.md** | RemoteFactory setup, server/client configuration |
| **properties.md** | Meta-properties, INotifyPropertyChanged, dirty tracking |
| **data-mapping.md** | MapFrom, MapTo, MapModifiedTo patterns |
| **testing.md** | Unit testing patterns for rules |
| **authorization.md** | [Authorize] attribute, role-based access |
| **blazor-integration.md** | MudBlazor binding, validation display |
| **source-generators.md** | What gets generated, troubleshooting |
| **migration.md** | Version upgrade patterns |
| **pitfalls.md** | Common mistakes and quick checklist |

## Repository References

| Repository | Purpose |
|------------|---------|
| [NeatooDotNet/Neatoo](https://github.com/NeatooDotNet/Neatoo) | Core DDD framework |
| [NeatooDotNet/RemoteFactory](https://github.com/NeatooDotNet/RemoteFactory) | Client-server communication |
