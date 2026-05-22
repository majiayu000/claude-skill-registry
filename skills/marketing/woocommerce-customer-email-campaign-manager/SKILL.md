---
name: woocommerce-customer-email-campaign-manager
description: Executes targeted email campaigns for a WooCommerce store, specifically for sending notifications about upcoming product releases or discount promotions. This skill retrieves and filters customers, queries products, identifies scheduled releases, and determines appropriate recipients for different campaign types.
---
# Instructions

## 1. Assess Store State
First, determine if the store has the necessary data to run a campaign.
- Use `woocommerce-woo_customers_list` to check for existing customers.
- Use `woocommerce-woo_products_list` with various statuses (`publish`, `draft`, `pending`, `private`) and the `onSale` parameter to check for existing products.

**Decision Logic:**
- If **no customers exist**, the campaign cannot proceed. Inform the user and claim the task as done.
- If **no products exist** (across all checked statuses), the campaign cannot proceed. Inform the user and claim the task as done.
- If both customers and relevant products exist, proceed to Step 2.

## 2. Filter Customers & Products for Campaigns
Based on the user's request, determine the target audience and the products to promote.

### For "New Product Reservation" Campaigns
*   **Target Customers:** Filter the customer list to only those whose `meta_data` includes `subscription_preferences` with `new_product_alerts` set to `True`. (Note: This filtering logic must be applied manually to the customer data returned by the API, as the provided tool may not support this filter directly).
*   **Target Products:** Identify products scheduled for release within the next 30 days. This typically involves checking products with a `draft` or `pending` status and analyzing their `meta_data` for a scheduled release date. (Note: The provided `woocommerce-woo_products_list` tool does not filter by date; you must retrieve all products and manually filter them based on their metadata or scheduled date field).

### For "Discount Reminder" Campaigns
*   **Target Customers:** All customers.
*   **Target Products:** All products where `onSale` is `true` (use the `woocommerce-woo_products_list` tool with `onSale: true`).

## 3. Execute or Report
- If valid customer-product pairs are found for either campaign type, proceed to compose and send the appropriate emails. (Note: The trajectory does not include an email sending tool; assume this is a subsequent step handled by another skill or manual process).
- If no valid pairs are found (e.g., customers exist but none are subscribed to alerts, or products exist but none are scheduled for release or on sale), inform the user of this specific outcome.
- Use `local-claim_done` to finalize the skill's execution once the assessment and filtering are complete, providing a clear summary of findings.

## Key Constraints & Notes
- The provided WooCommerce tools are for data retrieval only. Advanced filtering (by date, by specific meta field) must be done manually on the returned data.
- This skill is for **planning and identifying** the campaign audience and content. The actual email dispatch mechanism is out of scope.
- Always handle pagination (`perPage` parameter) appropriately if the store has more than 100 customers or products.
