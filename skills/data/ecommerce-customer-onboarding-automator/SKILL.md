---
name: ecommerce-customer-onboarding-automator
description: Automates customer onboarding workflows for e-commerce platforms. Fetches recent WooCommerce orders, identifies first-time customers within a specified timeframe, syncs their information to a BigQuery CRM database, and sends personalized welcome emails using a template.
---
# Instructions

## Objective
Automate the onboarding process for new e-commerce customers by:
1.  Identifying customers who completed their **first order** within the **past 7 days**.
2.  Syncing their core information (name, email, order details) from WooCommerce to a BigQuery CRM table.
3.  Sending a personalized welcome email to each identified customer.

## Prerequisites & Setup
*   **WooCommerce Connection:** Ensure access to the WooCommerce store's API (`woocommerce-woo_orders_list`).
*   **BigQuery Dataset:** Confirm the target BigQuery dataset (e.g., `woocommerce_crm`) and table (e.g., `new_customers`) exist. The table should have at least these columns: `customer_name` (STRING), `email` (STRING), `order_id` (INT64), `order_date` (TIMESTAMP), `order_total` (FLOAT64).
*   **Email Template:** Locate or create the `welcome_email_template.md` file. The skill expects to find it at `/workspace/dumps/workspace/` by default.

## Execution Steps

### 1. Fetch and Analyze Recent Orders
*   Use `woocommerce-woo_orders_list` to retrieve completed orders. Start with parameters: `{"status": ["completed"], "perPage": 100, "order": "desc", "orderby": "date"}`.
*   **Critical Logic:** Analyze the order metadata. In the provided trajectory, orders from first-time customers within the past 7 days were tagged with `"period": "recent_7_days"` in their `meta_data`. You must implement a similar filtering logic based on your store's data structure.
    *   **First-Time Customer Check:** Ensure a customer's email appears only once in the filtered set (or check against a historical customer list in BigQuery if available).
    *   **Date Filtering:** Use the `date_completed` field and calculate if it falls within the last 7 days from the current date.

### 2. Locate and Read the Email Template
*   Use `filesystem-search_files` to find `welcome_email_template.md`.
*   Use `filesystem-read_file` to load its content. The template should contain placeholders like `{{customer_name}}`, `{{order_id}}`, `{{order_total}}`, and `{{order_date}}`.

### 3. Prepare BigQuery Environment
*   Use `google-cloud-bigquery_list_datasets` and `google-cloud-bigquery_get_dataset_info` to verify the target dataset exists.
*   Use `google-cloud-bigquery_run_query` to inspect the `INFORMATION_SCHEMA` and confirm the schema of the target table (e.g., `new_customers`) matches the data you will insert.

### 4. Transform and Sync Customer Data
*   For each identified first-time customer, extract:
    *   `customer_name`: Combine `billing.first_name` and `billing.last_name`.
    *   `email`: From `billing.email`.
    *   `order_id`: The order's `id`.
    *   `order_date`: Convert `date_completed` to a TIMESTAMP.
    *   `order_total`: The order's `total` (as a float).
*   Construct a single `INSERT` query for BigQuery with all customer values. Use parameterized values or explicit casting (e.g., `TIMESTAMP('...')`) to ensure data type compatibility.
*   Execute the insert query using `google-cloud-bigquery_run_query`.
*   **Verification:** Run a `SELECT` query to confirm all records were inserted correctly.

### 5. Generate and Send Welcome Emails
*   For each customer, personalize the email template by replacing the placeholders with their specific data.
*   Use `emails-send_email` to send the email.
    *   **Subject:** Follow the template's subject line.
    *   **Body:** Use the fully personalized email body.
    *   **To:** The customer's email address.
*   Send emails sequentially or in small batches to avoid rate limits.

## Key Decisions & Error Handling
*   **Pagination:** If you have more than 100 recent orders, implement pagination using the `page` parameter in `woocommerce-woo_orders_list`.
*   **Duplicate Prevention:** Before inserting into BigQuery, consider checking if the `email` or `order_id` already exists in the target table to prevent duplicates if the skill runs multiple times.
*   **Template Flexibility:** The skill is designed to use an external template file. If the file is not found, you may need to create a default template or ask the user for its location.
*   **Email Send Errors:** Log or note if any email fails to send, but proceed with the remaining customers.

## Completion
After all emails are sent, provide a summary report including:
*   The number of first-time customers identified.
*   Confirmation of data sync to BigQuery.
*   Confirmation of emails sent.
*   Use `local-claim_done` to mark the task as complete.
