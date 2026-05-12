# Dependency Boundary Rules

<!-- SCOPE: Architecture presets, rule types, hybrid composition, auto-detection heuristics. -->
<!-- Sources: dependency-cruiser rules-reference, ArchUnit layeredArchitecture/onionArchitecture, Clean Architecture Ch14 -->

## 3-Tier Priority Chain

| Priority | Source | When |
|----------|--------|------|
| **1. Custom** | `docs/project/dependency_rules.yaml` | Project team defined own boundaries |
| **2. Documented** | `docs/architecture.md` Section 4.2 + 6.4 | Architecture documented but no custom rules |
| **3. Auto-detected** | Directory structure heuristics | No docs, infer from project layout |

## Rule Types

Inspired by [dependency-cruiser](https://github.com/sverweij/dependency-cruiser/blob/main/doc/rules-reference.md):

| Type | Semantics | Violation severity |
|------|-----------|-------------------|
| **forbidden** | This dependency MUST NOT exist | Per rule (CRITICAL/HIGH/MEDIUM) |
| **allowed** | ONLY listed dependencies are permitted (whitelist) | MEDIUM for unlisted deps |
| **required** | This dependency MUST exist | MEDIUM for missing deps |

## Auto-Detection Heuristics

| Directory signals | Detected style | Confidence |
|-------------------|---------------|------------|
| `domain/` + `infrastructure/` + `application/` | Clean/Onion | HIGH |
| `controllers/` + `services/` + `repositories/` | Layered | HIGH |
| `features/{name}/` or `modules/{name}/` with internal layers | Vertical Slices | HIGH |
| `views/` + `controllers/` + `models/` | MVC | HIGH |
| `adapters/` + `ports/` + `core/` | Hexagonal | HIGH |
| Multiple patterns from above | **Hybrid** | MEDIUM |
| No clear pattern | **Custom** (cycles + metrics only) | LOW |

## Architecture Presets

### Clean Architecture

Per [ArchUnit onionArchitecture](https://www.archunit.org/userguide/html/000_Index.html#_onion_architecture):

```yaml
preset: clean
layers:
  - {name: domain, path: "**/domain/**", rank: 0}
  - {name: application, path: "**/application/**|**/use_cases/**", rank: 1}
  - {name: infrastructure, path: "**/infrastructure/**|**/adapters/**", rank: 2}
  - {name: api, path: "**/api/**|**/controllers/**|**/routes/**", rank: 2}
rule: "Dependencies MUST point inward (higher rank -> lower rank only)"
forbidden:
  - {from: domain, to: infrastructure, severity: CRITICAL, reason: "Domain must not depend on infrastructure"}
  - {from: domain, to: api, severity: CRITICAL, reason: "Domain must not depend on API layer"}
  - {from: domain, to: application, severity: HIGH, reason: "Domain must not depend on application layer"}
  - {from: application, to: api, severity: HIGH, reason: "Application must not depend on API layer"}
```

### Hexagonal (Ports & Adapters)

```yaml
preset: hexagonal
layers:
  - {name: core, path: "**/core/**|**/domain/**", rank: 0}
  - {name: ports, path: "**/ports/**", rank: 1}
  - {name: adapters, path: "**/adapters/**", rank: 2}
forbidden:
  - {from: core, to: adapters, severity: CRITICAL, reason: "Core must not know about adapters"}
  - {from: ports, to: adapters, severity: HIGH, reason: "Ports define interfaces, not implementations"}
  - {from: "adapters/*/", to: "adapters/*/", cross: true, severity: HIGH, reason: "Adapters must not depend on each other"}
```

### Layered

Per [ArchUnit layeredArchitecture](https://www.archunit.org/userguide/html/000_Index.html#_layered_architecture):

```yaml
preset: layered
layers:
  - {name: controllers, path: "**/controllers/**|**/routes/**|**/views/**"}
  - {name: services, path: "**/services/**|**/use_cases/**"}
  - {name: repositories, path: "**/repositories/**|**/dal/**|**/data/**"}
forbidden:
  - {from: controllers, to: repositories, severity: HIGH, reason: "Layer skipping: use services"}
  - {from: repositories, to: services, severity: HIGH, reason: "Upward dependency"}
  - {from: repositories, to: controllers, severity: CRITICAL, reason: "Upward dependency"}
allowed:
  - {from: controllers, to: services}
  - {from: services, to: repositories}
```

### Vertical Slices

Per [ArchUnit slices().notDependOnEachOther()](https://www.archunit.org/userguide/html/000_Index.html#_slices):

```yaml
preset: vertical
layers:
  - {name: features, path: "**/features/*/|**/modules/*/"}
  - {name: shared, path: "references/**|references/scripts/**|references/templates/**|references/agents/**"}
forbidden:
  - {from: "features/*/", to: "features/*/", cross: true, severity: HIGH, reason: "Features must not cross-reference"}
allowed:
  - {from: "features/*", to: shared}
```

### MVC

```yaml
preset: mvc
layers:
  - {name: views, path: "**/views/**|**/templates/**"}
  - {name: controllers, path: "**/controllers/**"}
  - {name: models, path: "**/models/**"}
forbidden:
  - {from: views, to: models, severity: MEDIUM, reason: "Views should use controllers, not models directly"}
  - {from: models, to: views, severity: HIGH, reason: "Models must not know about views"}
  - {from: models, to: controllers, severity: HIGH, reason: "Models must not know about controllers"}
```

## Hybrid Composition

For projects mixing styles (e.g., Layered backend + Vertical Slices for features):

```yaml
zones:
  - {path: "src/core/", preset: layered}
  - {path: "src/features/", preset: vertical}
  - {path: "src/infrastructure/", preset: clean}

cross_zone_rules:
  - {from: "src/features/*", to: "src/core/*", allowed: true}
  - {from: "src/core/*", to: "src/features/*", allowed: false, severity: HIGH, reason: "Core must not depend on features"}
  - {from: "src/features/*", to: "src/infrastructure/*", allowed: true}
  - {from: "src/infrastructure/*", to: "src/features/*", allowed: false, severity: HIGH}
```

## Custom Project Rules Format

Projects define their own boundaries in `docs/project/dependency_rules.yaml`:

```yaml
modules:
  - {name: auth, path: "src/auth/**"}
  - {name: billing, path: "src/billing/**"}
  - {name: shared, path: "references/**|references/scripts/**|references/templates/**|references/agents/**"}
  - {name: legacy, path: "src/legacy/**"}

forbidden:
  - {from: billing, to: auth, severity: HIGH, reason: "Billing must not know about auth internals"}
  - {from: "src/*/internal/**", to: "src/*/internal/**", cross: true, severity: MEDIUM, reason: "Internal packages are private"}
  - {from: "*", to: legacy, severity: LOW, reason: "Avoid new dependencies on legacy code"}

allowed:
  - {from: "*", to: shared, reason: "Shared module is accessible by all"}

required:
  - {module: "src/*/", must_depend_on: "src/references/logging", reason: "All modules must use centralized logging"}
```

## Pattern Matching

- `*` — matches any single module name
- `**/` — matches any number of directory levels
- `features/*/` — matches any direct child of features/
- `cross: true` — only flag violations BETWEEN different groups (not within same module)

---

**Version:** 1.0.0
**Last Updated:** 2026-02-11
