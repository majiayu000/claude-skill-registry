---
name: webshop-product-evaluator
description: This skill evaluates product listings against user requirements, such as price limits and feature matches, to identify viable options. It should be triggered when presented with a search results page containing multiple products. The skill analyzes product titles, prices, and brief descriptions to select the most promising candidate for detailed inspection.
---
# Instructions

## When to Use
Activate this skill when you are on a **search results page** in a web shopping environment and need to evaluate multiple products against specific user requirements (e.g., price limits, feature keywords).

## Core Process
1.  **Parse the Observation:** Identify the user's instruction, the list of available products, and their associated details (Title, Price, ASIN/Product ID).
2.  **Extract Requirements:** From the user instruction, identify:
    *   **Price Limit:** The maximum acceptable price (e.g., "lower than 40.00 dollars").
    *   **Feature Keywords:** Key product attributes (e.g., "teeth whitening", "freshens breath").
3.  **Evaluate Products:** For each product listing on the current page:
    *   Check if the price is below the user's limit.
    *   Check if the product title contains the required feature keywords.
    *   Prioritize products that meet all criteria. If multiple products qualify, choose the one that appears most relevant or cost-effective.
4.  **Take Action:**
    *   If a suitable product is found, click on its product ID (e.g., `click[B09NYFDNVX]`) to view its details.
    *   If no suitable product is found on the current page, consider using the `search` action with refined keywords or clicking `Next >` to browse more results.

## Thought Process Format
Always structure your internal reasoning and final action using this format:
