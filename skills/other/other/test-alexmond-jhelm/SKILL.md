---
name: test
description: Run tests for the jhelm project
disable-model-invocation: true
argument-hint: [module] [TestClass#method]
allowed-tools: Bash(./mvnw *)
---

## Run jhelm tests

Run tests based on the provided arguments.

### No arguments — run all tests
```bash
./mvnw test
```

### Module only (e.g., `/test jhelm-core`)
```bash
./mvnw test -pl $0
```

### Specific test class (e.g., `/test jhelm-core KpsComparisonTest`)
```bash
./mvnw test -Dtest=$1 -pl $0
```

### Specific test method (e.g., `/test jhelm-core KpsComparisonTest#testSimpleRendering`)
```bash
./mvnw test -Dtest=$1 -pl $0
```

### Key test classes
- `GoTemplateStandardTest` — Template engine behavior (jhelm-gotemplate)
- `TemplateTest` — Template rendering (jhelm-gotemplate)
- `KpsComparisonTest` — Comparison with native Helm output (jhelm-core)
- `Helm4FunctionsTest` — Helm 4 function support (jhelm-gotemplate)

Report test results clearly. On failure, show the failing test name, assertion message, and relevant stack trace.
