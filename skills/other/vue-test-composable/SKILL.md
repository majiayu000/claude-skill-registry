---
name: test-vue-composable
description: Guide for unit testing Vue 3 Composables using Vitest. Use this skill when writing tests for Vue logic to determine the correct testing strategy based on whether the composable is independent, relies on lifecycle hooks (onMounted), or uses dependency injection (provide/inject).
---

# Vue Composable Testing Guide (Vitest)

## 1. Determine Composable Type

Analyze the source code of the composable to determine the testing strategy:

1.  **Independent**: Uses only Reactivity APIs (`ref`, `computed`, `watch`). Does not use Lifecycle hooks or `inject`.
2.  **Dependent (Lifecycle)**: Uses Lifecycle hooks (e.g., `onMounted`, `onUnmounted`).
3.  **Dependent (Injection)**: Uses `inject` to retrieve dependencies.

## 2. Select Testing Strategy

### A. Independent Composables
Test directly by invoking the function and asserting the returned state. No mocking of the Vue instance is required.

* **Pattern**: Import composable -> Call it -> Assert `result.value`.
* **Reference**: See `references/examples.md` (Section: Independent)

### B. Dependent Composables (Lifecycle)
Requires a component context to trigger hooks like `onMounted`. Use the `withSetup` helper function.

1.  **Prerequisite**: Ensure `test-utils.ts` (or similar) exists containing the `withSetup` helper.
    * *Action*: If the helper is missing, generate it using `references/helpers.md`.
2.  **Pattern**: Import `withSetup` -> Call `withSetup(() => useComposable())` -> Destructure result -> Assert.
3.  **Reference**: See `references/examples.md` (Section: Lifecycle Dependent)

### C. Dependent Composables (Injection)
Requires a provider context. Use the `useInjectedSetup` helper function.

1.  **Prerequisite**: Ensure `test-utils.ts` contains the `useInjectedSetup` helper.
    * *Action*: If the helper is missing, generate it using `references/helpers.md`.
2.  **Pattern**: Define injection config array -> Call `useInjectedSetup` -> Assert -> **Call unmount()**.
3.  **Reference**: See `references/examples.md` (Section: Injection Dependent)