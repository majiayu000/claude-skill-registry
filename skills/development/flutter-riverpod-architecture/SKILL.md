---
name: flutter-riverpod-architecture
description: Clean Architecture patterns for Flutter with Riverpod state management. Use when building or reviewing Flutter apps with layered architecture (Domain, Data, Application, Presentation).
---

# Flutter + Riverpod Clean Architecture

## Overview

This skill provides architectural patterns and rules for building Flutter applications using Clean Architecture with Riverpod for state management. Follow these patterns to maintain clear layer boundaries, testability, and scalability.

## Architecture Layers

```
┌─────────────────────────────────────────┐
│           Presentation Layer            │  Flutter UI, Widgets, Routing
├─────────────────────────────────────────┤
│           Application Layer             │  Riverpod Providers, State Management
├─────────────────────────────────────────┤
│              Data Layer                 │  Repositories, External APIs
├─────────────────────────────────────────┤
│             Domain Layer                │  Entities, Value Objects, Business Rules
└─────────────────────────────────────────┘
```

## Layer Dependency Rules

| Layer | Can Depend On | Cannot Depend On |
|-------|---------------|------------------|
| **Domain** | Nothing (pure Dart) | Flutter, Riverpod, Firebase, any SDK |
| **Data** | Domain | Flutter, Riverpod, Presentation |
| **Application** | Domain, Data | Flutter UI classes |
| **Presentation** | Application, Domain | Data (direct access) |

## Quick Reference

| Layer | Primary Purpose | Key Technology |
|-------|-----------------|----------------|
| Domain | Business entities, Value Objects | Freezed, pure Dart |
| Data | Repository implementations, API calls | Firebase, HTTP clients |
| Application | State management, Provider definitions | Riverpod, AsyncNotifier |
| Presentation | UI components, routing | ConsumerWidget, go_router |

## Layer References

- `references/domain-layer.md` - Freezed entities, Value Objects, immutable data
- `references/data-layer.md` - Repository pattern, dependency injection
- `references/application-layer.md` - Riverpod providers, AsyncNotifier pattern
- `references/presentation-layer.md` - ConsumerWidget, type-safe routing
- `references/ui-patterns.md` - Widget composition, anti-patterns

## Core Principles

### 1. Dependency Inversion
- Inner layers don't know about outer layers
- Domain is completely independent
- Data depends only on Domain
- Dependencies flow inward

### 2. Single Responsibility
- Each layer has a clear purpose
- Repositories handle data access only
- Providers handle state management only
- Widgets handle UI rendering only

### 3. Testability
- Domain layer is easily unit-testable (no dependencies)
- Data layer can mock external services
- Application layer can mock repositories
- Presentation layer can mock providers

## Directory Structure (Recommended)

```
lib/
├── app/
│   ├── route/           # go_router configuration
│   └── providers/       # App-wide providers
├── features/
│   └── {feature}/
│       ├── domain/      # Entities, Value Objects
│       ├── data/        # Repositories
│       ├── application/ # Providers, Notifiers
│       └── presentation/# Screens, Widgets
└── shared/
    ├── domain/          # Shared entities
    ├── data/            # Shared repositories
    └── widgets/         # Shared UI components
```

## Getting Started

1. **New Entity?** -> See `references/domain-layer.md`
2. **API Integration?** -> See `references/data-layer.md`
3. **State Management?** -> See `references/application-layer.md`
4. **Building UI?** -> See `references/presentation-layer.md`
5. **Widget Patterns?** -> See `references/ui-patterns.md`

## Compliance Verification

```bash
# Verify Domain layer purity
grep -r "package:flutter" lib/features/*/domain/
grep -r "riverpod" lib/features/*/domain/

# Verify Data layer isolation
grep -r "package:flutter" lib/features/*/data/
grep -r "riverpod" lib/features/*/data/

# Verify Presentation doesn't access Data directly
grep -r "features/.*/data/.*_repository" lib/features/*/presentation/
```

All commands should return empty results if architecture is properly maintained.
