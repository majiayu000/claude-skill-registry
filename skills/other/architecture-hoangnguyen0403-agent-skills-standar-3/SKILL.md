---
name: Architecture
description: Standards for structural design, Clean Architecture, and project layout in Golang.
metadata:
  labels: [golang, architecture, clean-arch, project-layout, ddd]
  triggers:
    files: ['go.mod', 'internal/**']
    keywords:
      [architecture, structure, folder layout, clean arch, dependency injection]
---

# Golang Architecture Standards

## **Priority: P0 (CRITICAL)**

## Principles

- **Clean Architecture**: Separate concerns. Inner layers (Domain) rely on nothing. Outer layers (Adapters) rely on Inner.
- **Project Layout**: Follow standard Go project layout (`cmd`, `internal`, `pkg`).
- **Dependency Injection**: Explicitly pass dependencies via constructors. Avoid global singletons.
- **Package Oriented Design**: Organize by feature/domain, not by layer (avoid `controllers/`, `services/` at root).
- **Interface Segregation**: Define interfaces where they are _used_ (Consumer implementation).

## Standard Project Layout

See [Standard Project Layout](references/project-layout.md) for directory tree.

### Layer Rules

- **Domain**: Inner-most. No deps.
- **UseCase**: Depends on Domain.
- **Adapter**: Outer-most. Depends on UseCase/Domain.

## Guidelines

- **Use Constructors**: `NewService(repo Repository) *Service`.
- **Inversion of Control**: Service depends on `Repository` interface, not `SQLRepository` struct.
- **Wire up in Main**: Main function composes the dependency graph.

## References

- [Standard Project Layout](references/project-layout.md)
- [Clean Architecture Layers](references/clean-arch.md)
