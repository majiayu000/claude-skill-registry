---
name: architecture
description: jhelm project architecture and module structure for a Java Helm implementation
user-invocable: false
---

## jhelm Architecture

**Java 21 | Spring Boot 4.0.2 | Kubernetes Client 25.0.0 | Picocli 4.7.6**

### Module Dependency Graph
```
jhelm (parent)
├── jhelm-gotemplate  — Go template engine (standalone, no Spring)
├── jhelm-core        — Helm logic, charts, actions (depends on: gotemplate)
├── jhelm-kube        — Kubernetes client integration (depends on: core)
└── jhelm-app         — CLI, Spring Boot + Picocli (depends on: core, kube)
```

### Template Engine (`jhelm-gotemplate`)
- Pipeline: Lexer → Parser → AST → Executor
- Key classes: `GoTemplate`, `GoTemplateFactory`, `Functions`
- Functions by category: Sprig (strings, collections, logic, math, encoding, crypto, date, reflection, network, semver) and Helm (conversion, template, kubernetes, chart)
- No Spring dependency — pure Java library

### Core Engine (`jhelm-core`)
- `Engine.java` — Orchestrates template processing
- `Chart.java` — Represents Helm charts with metadata and templates
- `RepoManager.java` — Manages chart repositories
- Creates new `GoTemplateFactory` per render to avoid template accumulation
- Stack depth tracking prevents infinite template recursion

### Kubernetes Integration (`jhelm-kube`)
- `HelmKubeService` — Kubernetes resource deployment
- Uses official Kubernetes Java Client 25.0.0

### CLI Application (`jhelm-app`)
- Spring Boot 4.0.2 application
- Picocli-based command structure
- Entry point for user-facing commands
