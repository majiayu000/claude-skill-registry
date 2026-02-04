---
name: amazon-product-search-recommender
description: When the user wants to search for specific products on Amazon within budget constraints and generate structured recommendations. This skill navigates to Amazon.com, performs targeted searches using specific criteria (price range, material, color), browses search results, extracts product details (title, price, store/brand, URL), and compiles recommendations into a structured JSON format. Triggers include requests for product recommendations, shopping assistance, budget-constrained searches, or when users need to find specific items on Amazon with detailed specifications.
---
# Skill: Amazon Product Search & Recommender

## Purpose
Search Amazon for products matching user criteria (budget, material, color, etc.), extract detailed product information, and output structured recommendations in JSON format.

## Core Workflow
1.  **Parse Request:** Identify the product category, budget, material, color, and any other specific constraints from the user's request.
2.  **Navigate & Search:** Go to `https://www.amazon.com`, locate the main search box, and perform a search using a constructed query (e.g., "black leather sofa under 400").
3.  **Browse Results:** Navigate through the search results page to find relevant product listings.
4.  **Extract Details:** For each selected product, click into its detail page to gather accurate information:
    *   **Canonical URL:** The full product page URL.
    *   **Title:** The complete product title.
    *   **Price:** The current selling price (prioritize Prime/sale price if shown).
    *   **Store/Brand Name:** The brand or store name (e.g., from "Visit the [Brand] Store" link).
5.  **Compile & Output:** Format the extracted data into a JSON array matching the required schema and write it to the specified output file (e.g., `recommend.json`).

## Key Instructions & Best Practices
*   **Search Query:** Construct the search query by combining key attributes from the user request (color, material, product type, budget hint).
*   **Element Identification:** Use the `browser_snapshot_search` tool with patterns like `"searchbox"` or `"Search Amazon"` to reliably locate the search input field. Avoid interacting with dropdowns or other elements near the search bar.
*   **Result Navigation:** Use `browser_snapshot_navigate_to_span` and `browser_snapshot_search` (e.g., for `"price"`, `"$"`, product brand names) to move through the search results and identify product links and their details.
*   **Data Accuracy:** Always navigate to the product detail page (`browser_click` on product link) to capture the definitive `canonical_url`, `title`, `price`, and `store_name`. Do not rely solely on snippet data from search results.
*   **Price Extraction:** On the product page, search for price-related patterns (`"\\$"`, `"price"`). The price is often found near elements like "Prime Member Price" or within the buy box. Extract only the numerical price (e.g., "287.99"), not currency symbols or additional text.
*   **Store/Brand Extraction:** Look for a link containing "Visit the ... Store" on the product page. The text between "Visit the " and " Store" is typically the `store_name`.
*   **Error Handling:** If an action fails (e.g., clicking an element), use snapshot search and navigation tools to re-orient and find the correct element reference.
*   **Task Completion:** After writing the final JSON file, read it back to verify its contents and call `local-claim_done`.

## Output Schema
The final output must be a JSON file (e.g., `recommend.json`) containing an array of objects. Each object must have a `product_info` key containing:
