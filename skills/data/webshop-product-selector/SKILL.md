---
name: webshop-product-selector
description: Selects the most promising product candidate from a filtered shortlist for detailed inspection. Use this skill when multiple items seem viable; it makes a final selection based on a heuristic (e.g., best feature match, lowest price) and triggers the action to navigate to that product's detail page (click[product_id]).
---
# Instructions
Use this skill when you are on a search results page with multiple product options that appear to meet the user's core requirements.

## Decision Process
1.  **Assess the List:** Review the provided observation, which contains a list of products. Each product entry typically includes a Product ID (e.g., `B093C1THVP`), a title, and a price.
2.  **Apply Selection Heuristic:** Use the bundled `selector.py` script to programmatically identify the best candidate. The script implements the following logic:
    *   Filters products strictly under the user's specified maximum price.
    *   Scores remaining products based on keyword matching in the title against the user's core requirements (e.g., "portable", "easy to carry", "double horn").
    *   Selects the product with the highest score. In case of a tie, it chooses the lowest-priced item.
3.  **Execute Action:** The final action is always to click on the selected product's ID to navigate to its detail page for final verification and purchase. The action format is `click[product_id]`.

## Thought Process Template
Structure your reasoning before acting using this template:
