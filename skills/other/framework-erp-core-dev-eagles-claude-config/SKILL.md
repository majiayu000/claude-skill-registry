---
name: framework
description: Display Claude Code Optimization Framework status and available configurations. Shows all DSL shortcuts, loaded configs, and project detection.
---

# Framework Status Skill

When this skill is invoked, perform the following:

## 1. Load Framework Manifest
Read `C:\.claude\FRAMEWORK-MANIFEST.yaml` and display:
- Framework version
- Total configuration files
- Last updated date

## 2. Display DSL Shortcuts
Show all available shortcuts in organized tables:

### Architecture Patterns (@arch:*)
| Shortcut | Description |
|----------|-------------|
| `@arch:hybrid` | Multi-tier hybrid architecture |
| `@arch:mono` | Monolithic (5 variants) |
| `@arch:ms` | Microservices |
| `@arch:sls` | Serverless |

### Workflows
| Shortcut | Description |
|----------|-------------|
| `@agile` | Agile/Scrum methodology |
| `@devops` | DevOps/CI-CD patterns |
| `@vmodel` | Waterfall/V-Model |
| `@kanban` | Kanban flow |

### Technology Stacks
| Shortcut | Description |
|----------|-------------|
| `@dotnet` | .NET 8 / ASP.NET Core |
| `@node` | Node.js 20.x / TypeScript |
| `@python` | Python 3.11+ / FastAPI |
| `@java` | Java 21 / Spring Boot 3.x |
| `@go` | Go 1.22+ / Gin |

### Deployment Strategies
| Shortcut | Description |
|----------|-------------|
| `@deploy:k8s` | Kubernetes / AKS |
| `@deploy:docker` | Docker Compose |
| `@deploy:sls` | Serverless |
| `@deploy:vm` | Virtual Machine |

### Testing Frameworks
| Shortcut | Description |
|----------|-------------|
| `@test:unit` | Unit testing |
| `@test:int` | Integration testing |
| `@test:e2e` | End-to-end testing |
| `@test:bdd` | BDD with SpecFlow/Cucumber |
| `@test:perf` | Performance testing |

## 3. Auto-Detect Project Type
Scan current directory for:
- `*.csproj` → Suggest `@dotnet`
- `package.json` → Suggest `@node`
- `pyproject.toml` → Suggest `@python`
- `pom.xml`/`build.gradle` → Suggest `@java`
- `go.mod` → Suggest `@go`
- `Dockerfile` → Suggest `@deploy:docker`
- `k8s/` or `helm/` → Suggest `@deploy:k8s`

## 4. Show Recommended Configuration
Based on detection, suggest a combined configuration:
```
@arch:ms @dotnet @agile @deploy:k8s @test:unit
```

## Usage
Simply type `/framework` to see the full status and recommendations.
