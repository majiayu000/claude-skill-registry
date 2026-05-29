---
name: webshop-result-filter
description: This skill filters search results by evaluating product listings against specific user constraints like price, features, or ratings. It should be triggered when reviewing a page of search results to identify items that match all given criteria. The skill takes a list of products with their details and outputs a subset that meets the defined requirements for closer inspection.
---
# Skill: webshop-result-filter

## When to Use
Activate this skill when you are on a search results page in a web shopping environment and need to systematically evaluate which products meet a user's specific, multi-faceted requirements (e.g., "price lower than 40.00 dollars" AND "natural looking").

## Core Instruction
1.  **Parse the Instruction:** Extract the user's constraints from the instruction. Common constraints include:
    *   **Price:** A maximum or target price (e.g., `price lower than 40.00 dollars`).
    *   **Features:** Specific attributes or keywords (e.g., `natural looking`, `long`, `clip-in`).
    *   **Ratings:** A minimum rating threshold (if available in the observation).

2.  **Parse the Observation:** Extract the list of products from the search results page. Each product listing typically contains:
    *   A Product ID/ASIN (e.g., `B09C337K8S`).
    *   A Title/Description.
    *   A Price.
    *   A Rating (if available).

3.  **Apply Filters:** For each product in the list, check it against **all** extracted user constraints.
    *   **Price Filter:** Compare the product's price to the user's maximum price. Convert prices to numerical values for comparison.
    *   **Keyword/Feature Filter:** Check if the product's title/description contains keywords related to the required features (e.g., "natural").
    *   **Rating Filter:** If a rating constraint exists and the product has a rating, ensure it meets the minimum.

4.  **Output Decision:** Identify the **first product** in the filtered list that passes all criteria. This becomes the primary candidate for the next action (`click[product_id]`). If no product passes all filters, you may need to refine the search.

## Example from Trajectory
*   **User Instruction:** `i need a long clip-in hair extension which is natural looking, and price lower than 40.00 dollars`
*   **Extracted Constraints:**
    *   `price < 40.00`
    *   Keywords: `natural` (implied from "natural looking")
*   **Observation (First Page):** Contains ~10 products with IDs, titles, and prices.
*   **Filtering Process:**
    1.  `B09C337K8S`: Price $29.99 (< $40.00). Title contains "Natural Looking". **PASSES**.
    2.  `B093BKWHFK`: Price $63.99 (> $40.00). **FAILS** on price.
    3.  `B099K9Z9L2`: Price $43.99 (> $40.00). **FAILS** on price.
*   **Result:** `B09C337K8S` is selected as the top matching candidate.

## Next Action
After identifying a matching product, the recommended action is to click on it for more details: `click[<matching_product_id>]`.

For complex filtering logic or to process large result sets, use the bundled script.
