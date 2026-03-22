---
name: mvn-build
description: Build the jhelm project with Maven
disable-model-invocation: true
allowed-tools: Bash(./mvnw *)
---

## Build the jhelm project

Run the Maven build for the project. If an argument is provided, build only that module.

### Full build
```bash
./mvnw clean install
```

### Module build (if argument provided)
```bash
./mvnw clean install -pl $ARGUMENTS
```

### Modules
- `jhelm-gotemplate` — Go template engine
- `jhelm-core` — Core Helm logic
- `jhelm-kube` — Kubernetes integration
- `jhelm-app` — CLI application

Run the appropriate build command. Report any compilation errors or test failures clearly.
