---
name: "arkts-coding-standard"
description: "Enforces ArkTS strict typing rules and coding standards. Invoke when writing, analyzing, or correcting ArkTS code for HarmonyOS to ensure compliance."
---

# ArkTS Coding Standards

This skill provides guidelines and validation for writing correct ArkTS code, focusing on strict typing and performance optimizations required for HarmonyOS development.

## ❌ Illegal / Discouraged Practices

The following patterns are **forbidden** or highly discouraged in ArkTS:

1.  **Any/Unknown Types**:
    ```typescript
    let x: any = 1; // ❌ Not allowed: `any` and `unknown` are forbidden.
    ```

2.  **Object Literal Types**:
    ```typescript
    type Inline = { value: number }; // ❌ Don't declare object-literal-based types.
    ```

3.  **Fresh Object Literals (Untyped)**:
    ```typescript
    const bad: Inline = { value: 1 }; // ❌ Fresh object literal without declared class/interface instance.
    ```

4.  **Runtime Shape Changes**:
    ```typescript
    bad.newProp = "later"; // ❌ Changing object shape (adding properties) at runtime is forbidden.
    ```

5.  **Implicit Object Shapes**:
    ```typescript
    const obj = {
      value: 1,
      double() {
        return this.value + this.value; // ❌ `this` in a non-method context is disallowed.
      }
    }; // ❌ Even with an object literal, it must match an explicit class/interface.
    ```

6.  **Type Mismatches**:
    ```typescript
    bad.value = "7"; // ❌ Assigning string to a number-typed field fails.
    ```

7.  **Implicit Coercion**:
    ```typescript
    console.info(String(+bad.value)); // ❌ Unary `+` on a string for coercion is not permitted.
    ```

## ✅ Correct Practices

Use explicit types, classes, and safe conversions:

1.  **Explicit Numeric Parsing**:
    ```typescript
    const s: string = "7";
    // Use explicit parsing methods instead of unary +
    const n: number = Number.parseInt(s); 
    ```

2.  **Classes and Interfaces**:
    Always define explicit classes or interfaces for your data structures.

    ```typescript
    class Doubler {
      value: number;
      constructor(value: number) {
        this.value = value;
      }
    }
    
    let obj = new Doubler(n);
    ```

## Summary of Rules

*   **Static Typing**: ArkTS is statically typed. Avoid dynamic features like `any`.
*   **Fixed Layout**: Object layout is fixed at compile time. You cannot add/remove properties at runtime.
*   **Explicit Types**: Define types explicitly using `class` or `interface`. Avoid anonymous object types.
*   **Strict Safety**: No implicit type coercion. Use standard library functions (e.g., `Number.parseInt`) for conversions.
