---
name: product-recall-manager
description: Manages a complete product recall workflow in WooCommerce. Identifies products by model/metadata, deactivates them (draft/private/hidden), creates a Google Forms recall form, finds affected customers from orders, and sends personalized notification emails with the form link.
---
# Product Recall Manager

Execute a complete product recall process for a specified product model in WooCommerce.

## Core Workflow
1.  **Identify Target Products**: Search for products matching the specified model or containing recall metadata (`recall_status: need_recall`).
2.  **Deactivate Products**: Set identified products to `draft` status and `hidden` catalog visibility. Do NOT delete them.
3.  **Create Recall Form**: Generate a Google Form using the provided template (`recall_form_template.json`). The form must collect customer and product details for the recall process.
4.  **Find Affected Customers**: Query all historical WooCommerce orders that contain the recalled product(s).
5.  **Notify Customers**: Send a personalized recall email to each unique customer using the template (`recall_email_template.md`), inserting their specific details and the Google Form link.
6.  **Generate Report**: Create a `recall_report.json` file containing the generated Google Form's ID and URL.

## Required Input from User
You must ask the user to specify the **product model** or **identification criteria** to initiate the recall. If not provided, examine existing products for metadata clues (e.g., `recall_status: need_recall`).

## Key Instructions & Logic

### 1. Product Identification & Deactivation
- Use `woocommerce-woo_products_list` to browse store products.
- Filter products by:
    - **Name/SKU** containing the target model string (e.g., "X1").
    - **Metadata** containing `recall_status: need_recall` or `recall_reason`.
- Once identified, use `woocommerce-woo_products_batch_update` to set `status: "draft"` and `catalog_visibility: "hidden"` for all target products. Provide a summary of affected products (IDs, Names, SKUs).

### 2. Google Forms Creation
- **Create Form**: Use `google_forms-create_form` with only the `title` parameter. The description cannot be set during creation.
- **Add Questions**: Use the `recall_form_template.json` as a reference. Add questions sequentially using the appropriate `google_forms-add_*_question` functions:
    - `google_forms-add_text_question` for text, email, date fields.
    - `google_forms-add_multiple_choice_question` for choice fields.
    - Ensure `required` field settings from the template are applied.
- **Form URL**: The `responderUri` from the creation response is the public form link to include in emails.

### 3. Customer Identification & Notification
- For each recalled product ID, use `woocommerce-woo_orders_list` with the `product` filter to find all containing orders.
- **Deduplicate Customers**: Compile a unique list of customers by their email address (`billing.email`). Aggregate their order numbers and purchased product details.
- **Personalize & Send Email**:
    - Load the `recall_email_template.md`.
    - For each customer, populate the template placeholders (`[Customer Name]`, `[Product Model]`, `[Product ID]`, `[Order Number]`, `[Purchase Date]`, `[Google Forms Link]`).
    - Use `emails-send_email` to send. The subject should be clear, e.g., "Product Recall Notice - [Product Model]".

### 4. Final Reporting
- Use `filesystem-write_file` to create `recall_report.json` with the structure:
    