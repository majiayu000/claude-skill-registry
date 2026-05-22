---
name: shopify-functions
description: Guide for creating backend logic using Shopify Functions (Discounts, Shipping, Payment, etc.). Covers WASM, Rust/JavaScript (Javy) implementation, and input queries.
---

# Shopify Functions

Shopify Functions differ from traditional backend apps. They are compiled to **WASM** and run on Shopify's infrastructure with extremely low latency. They are the successor to Shopify Scripts (Plus).

## 1. Concepts

-   **Deterministic**: Same input always equals same output. No random numbers, no network calls.
-   **Execution Time**: Strict limits (e.g., 5ms for logic).
-   **Languages**: Rust (First-class) or JavaScript (via Javy).

## 2. Structure

A function consists of:
1.  **`shopify.extension.toml`**: Configuration.
2.  **`input.graphql`**: Defines data sent *to* the function.
3.  **`src/run.rs` (or `.js`)**: The logic that returns an `Output`.

## 3. Workflow

1.  **Generate**: `shopify app generate extension --template product_discounts --name my-discount`
2.  **Input Query**: Modify `input.graphql` to request necessary data (Cart, Customer, etc.).
3.  **CodeGen**: Run `shopify app function typegen` to generate types from your GraphQL query.
4.  **Logic**: Implement the `run` function.
5.  **Build**: `npm run build` (compiles to `.wasm`).
6.  **Deploy**: `shopify app deploy`.

## 4. JS Example (Product Discount)

```javascript
// src/run.js
// @ts-check

/**
 * @typedef {import("../generated/api").RunInput} RunInput
 * @typedef {import("../generated/api").FunctionRunResult} FunctionRunResult
 */

/**
 * @param {RunInput} input
 * @returns {FunctionRunResult}
 */
export function run(input) {
  const targets = input.cart.lines
    .filter(line => line.merchandise.product.hasAnyTag)
    .map(line => ({
      cartLine: {
        id: line.id
      }
    }));

  if (!targets.length) {
    return {
      discounts: [],
      discountApplicationStrategy: "FIRST",
    };
  }

  return {
    discounts: [
      {
        targets,
        value: {
          percentage: {
            value: "10.0"
          }
        },
        message: "VIP Discount"
      }
    ],
    discountApplicationStrategy: "FIRST",
  };
}
```

## 5. Configuration (GraphiQL)

You can't console.log in WASM. Use the **Shopify App Bridge** helper or the locally served **GraphiQL explorer** to debug inputs/outputs.

Run `npm run dev`, then open the highlighted GraphiQL URL in the terminal.
