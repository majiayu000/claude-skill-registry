---
name: clojure-testing
description: ALWAYS use when writing, modifying, or reviewing Clojure test code (deftest, clojure.test). Covers property-based testing with Malli generators and test.check, integration test patterns with cleanup, and test organization conventions. Also applies when running tests (bb test, lein test, clojure -X:test) or debugging test failures.
---

# Clojure Testing

## Test Types

Clojure projects typically use three complementary testing approaches:

### 1. Unit Tests (Minimal)
Simple function behavior tests with known inputs/outputs. Used sparingly — only when property-based tests would be overly complex.

```clojure
(deftest test-classify-route
  (testing "Static route classification"
    (let [route {:uri "/api/users"}
          result (classify-route route)]
      (is (= :static (:route-type result))))))
```

### 2. Property-Based Tests (Primary)
Schema-driven generative tests that validate function properties across many generated inputs. This is the **preferred** testing approach because it catches edge cases that hand-written tests miss.

#### Using test.check (Recommended)

```clojure
(require '[clojure.test.check.clojure-test :refer [defspec]]
         '[clojure.test.check.generators :as gen]
         '[clojure.test.check.properties :as prop])

(defspec my-function-roundtrip 100
  (prop/for-all [x gen/int
                 y gen/int]
    (let [result (my-function x y)]
      ;; Test properties, not specific values
      (or (nil? result) (int? result)))))
```

`defspec` provides shrinking (finds minimal failing case), seed reporting (reproducible failures), and proper test integration.

#### Using Malli Generators (Lightweight Alternative)

When you want to generate from Malli schemas directly:

```clojure
(deftest my-function-test
  (testing "my-function properties"
    (let [args-schema (-> #'my-function meta :malli/schema second)
          args-gen (mg/generator args-schema)]
      (dotimes [_ 100]
        (let [[arg1 arg2] (gen/generate args-gen)
              result (my-function arg1 arg2)]
          ;; Test properties, not specific values
          (is (or (nil? result) (string? result))))))))
```

### 3. Integration Tests
End-to-end flows testing compilation, file I/O, and runtime behavior with proper cleanup.

```clojure
(deftest test-full-flow
  (testing "Complete processing flow"
    (let [result (process-input test-input)]
      (is (map? result))
      (is (contains? result :expected-key)))))
```

## Malli Registry Setup Pattern

**CRITICAL:** All test namespaces that use Malli schemas MUST include a registry setup fixture. The **clojure-malli-schema** skill is the canonical source for the fixture pattern, registry configuration, and best practices for Malli in tests. Consult it when setting up or modifying Malli test fixtures.

**Important:** Include ONLY the schema registries needed for the test namespace. This keeps the registry lean.

## Property-Based Testing Workflow

### Step 1: Extract Schema from Function Metadata

```clojure
(let [args-schema (-> #'function-name meta :malli/schema second)
      args-gen (mg/generator args-schema)]
  ...)
```

### Step 2: Generate Test Cases

```clojure
(dotimes [_ 100]
  (let [[arg1 arg2] (gen/generate args-gen)
        result (function-name arg1 arg2)]
    ...))
```

### Step 3: Test Properties, Not Values

Focus on invariants and properties:
- Type properties: "Result is always a string or nil"
- Structural properties: "Result never contains X"
- Relationship properties: "Output length <= input length"

```clojure
;; Good: Tests properties
(is (or (nil? result) (string? result)))

;; Avoid: Tests specific values (use unit tests for this)
(is (= "expected-string" result))
```

### Custom Generators for Domain Objects

When function schemas aren't sufficient, create custom generators:

```clojure
(let [custom-gen (gen/one-of
                   [gen/string-alphanumeric
                    (gen/fmap #(str "prefix_" %) gen/string-alphanumeric)])]
  (dotimes [_ 100]
    (let [input (gen/generate custom-gen)]
      ...)))
```

## Integration Test Patterns

### Temp Directory Management

Use `java.nio.file.Files/createTempDirectory` for thread-safe temp dirs in parallel test runs:

```clojure
(import '[java.nio.file Files]
        '[java.nio.file.attribute FileAttribute])

(def temp-output-dir
  (str (Files/createTempDirectory "test-" (into-array FileAttribute []))))

(defn cleanup-fixture [f]
  "Clean up temp directory after tests"
  (try
    (f)
    (finally
      (when (.exists (io/file temp-output-dir))
        (doseq [file (reverse (file-seq (io/file temp-output-dir)))]
          (.delete file))))))

(use-fixtures :once cleanup-fixture)
```

### Setup-Process-Verify Flow

Standard pattern for testing processing pipelines:

```clojure
(testing "Process and verify output"
  (let [input {:data "test"}
        output-file (str temp-output-dir "/output.edn")]

    ;; Process
    (process-and-write input output-file)

    ;; Verify file created
    (is (.exists (io/file output-file)))

    ;; Load and verify
    (let [loaded (read-output output-file)]
      (is (= (:data input) (:data loaded))))))
```

### State/Cache Testing Pattern

For tests involving mutable state, always clear before each test:

```clojure
(deftest cache-scenario-test
  (testing "cache behavior"
    ;; Clear state to start fresh
    (reset-state!)

    ;; Test logic...
    ))
```

## Failure Modes and Troubleshooting

- **Generator fails with complex schemas** — Simplify the schema or provide a custom generator. Deeply nested schemas with many constraints can be unsatisfiable.
- **Reproducing property test failures** — When using `defspec`, the failure output includes the seed. Re-run with `(defspec ... {:seed <seed>})` to reproduce.
- **Flaky property tests** — Usually caused by side effects or shared state. Ensure tests are pure or properly isolated.
- **"Schema not found" in test fixtures** — Verify the registry function includes the schema and `(mdev/start!)` is called after registry setup.
- **Tests pass individually but fail together** — State leaking between tests. Add `(reset-state!)` in fixtures or use `:each` fixtures.

## Test Organization and Documentation

### Namespace Docstrings

Include clear namespace-level documentation:

```clojure
(ns my-app.integration-test
  "End-to-end integration tests.

   Tests the complete flow:
   1. Process input
   2. Write output
   3. Load and verify"
  (:require ...))
```

### Testing Blocks

Use nested `testing` blocks for clarity:

```clojure
(deftest feature-test
  (testing "happy path"
    ;; Test logic...
    )

  (testing "edge cases"
    ;; Test logic...
    ))
```

## Running Tests

```bash
# For devbox projects, prefix with: devbox run --
bb test
clojure -X:test
lein test

# Run specific test namespace
clojure -M:test -n my-app.core-test
```

## Checklist for New Tests

Before committing test code:

- [ ] Use `testing` blocks with descriptive strings
- [ ] Set up Malli registry fixture if using schemas
- [ ] Prefer property-based tests over unit tests
- [ ] Generate 100+ samples for property-based tests
- [ ] Test properties/invariants, not specific values
- [ ] Clean up temp files/directories in integration tests
- [ ] Include namespace docstring explaining test purpose
- [ ] Clear mutable state before state-dependent tests
- [ ] Run full test suite to verify all tests pass

For a complete annotated example showing all patterns together, see `references/test-template.clj`.
