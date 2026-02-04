---
name: webshop-price-checker
description: This skill scans product listings or detail pages to verify if an item's price meets a specified budget constraint. It is triggered when evaluating a potential product for purchase. It extracts the price from the displayed information (e.g., '$164.95') and compares it against the maximum allowed budget, outputting a boolean decision on whether the item is within budget.
---
# Instructions
When evaluating a product for purchase, use this skill to check if its price is within the specified budget.

## Process
1.  **Identify the Budget:** Extract the maximum allowed price from the user's instruction or the current context. The budget is typically expressed as a dollar amount (e.g., "lower than 200.00 dollars").
2.  **Locate the Price:** On the current web page (search results or product detail page), find the price string. It is usually prefixed with a `$` symbol and may be labeled "Price:".
3.  **Execute Check:** Run the `check_price.py` script, providing it with the extracted price string and the budget.
4.  **Make Decision:** Based on the script's boolean output (`True`/`False`):
    *   If `True`: The item is within budget. You may proceed with further evaluation or purchase.
    *   If `False`: The item exceeds the budget. You should continue searching or select a different item.

## Notes
*   The primary action for this skill is to call the bundled script. Do not perform manual price parsing or comparison in your main reasoning.
*   If the price cannot be found on the page, assume the item is not suitable and continue your search.
