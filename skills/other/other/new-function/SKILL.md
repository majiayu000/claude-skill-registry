---
name: new-function
description: Add a new template function to jhelm (Helm or Sprig)
disable-model-invocation: true
argument-hint: [function-name]
---

## Add a new template function

Guided workflow for adding a new template function named `$ARGUMENTS`.

### Step 1: Determine the category

**Helm functions** (in `jhelm-gotemplate/src/main/java/.../helm/`):
- `conversion/ConversionFunctions.java` — YAML/JSON conversion (toYaml, fromJson, etc.)
- `template/TemplateFunctions.java` — Template inclusion (include, tpl, required)
- `kubernetes/KubernetesFunctions.java` — Kubernetes integration (lookup)
- `chart/ChartFunctions.java` — Chart utilities (semverCompare, certificate generation)

**Sprig functions** (in `jhelm-gotemplate/src/main/java/.../sprig/`):
- `strings/StringFunctions.java` — String manipulation
- `collections/CollectionFunctions.java` — List/dict operations
- `logic/LogicFunctions.java` — default, empty, coalesce, ternary
- `math/MathFunctions.java` — Arithmetic operations
- `encoding/EncodingFunctions.java` — Base64, SHA, etc.
- `crypto/CryptoFunctions.java` — UUID, random, encryption
- `date/DateFunctions.java` — Date formatting/manipulation
- `reflection/ReflectionFunctions.java` — Type checking
- `network/NetworkFunctions.java` — DNS lookup
- `semver/SemverFunctions.java` — Semantic versioning

### Step 2: Implement the function

1. Add the function to the appropriate category class
2. Follow existing patterns in that class (method signature, error handling)
3. Use `@Slf4j` for logging if needed
4. For strict variants, create a `must*` version that throws on error

### Step 3: Registration

The function auto-registers via the coordinator:
- Helm functions: `HelmFunctions.java` → `getFunctionCategories()`
- Sprig functions: `SprigFunctionsRegistry.java` → `getFunctionCategories()`

If adding a **new category**, update `getFunctionCategories()` in the appropriate coordinator.

### Step 4: Add tests

Add tests in the corresponding test class (e.g., `Helm4FunctionsTest.java`, or the test class for the Sprig category).

### Step 5: Verify

Run the relevant module tests:
```bash
./mvnw test -pl jhelm-gotemplate
```
