---
name: fraud-investigation-data-consolidator
description: Investigates a suspicious transaction by gathering all related data from a BigQuery analytics dataset, consolidating it into a structured JSON format, and triggering alert workflows.
---
# Instructions

Execute the following steps to investigate a suspicious transaction. The primary goal is to create a comprehensive data snapshot for a given `transaction_id` and trigger the required alerting and archiving workflows.

## 1. Initial Setup & Discovery
*   **Input:** You will be given a specific `transaction_id` (e.g., `T8492XJ3`).
*   **First, confirm the target dataset and storage buckets exist.**
    *   Use `google-cloud-bigquery_get_dataset_info` to verify the `transactions_analytics` dataset is accessible.
    *   Use `google-cloud-storage_list_buckets` to locate the archive bucket (name prefixed by `mcp-fraud-investigation-archive-`) and the log bucket (name prefixed by `Trading_Logging-`). Note their exact names.

## 2. Schema Exploration & Data Querying
*   **Discover all tables** in the `transactions_analytics` dataset using `google-cloud-bigquery_run_query` on the `INFORMATION_SCHEMA.TABLES` view.
*   **For the target transaction, query data from two primary sources:**
    1.  `live_transactions` table: Get the full record for the given `transaction_id`. This record contains key foreign IDs (`user_id`, `account_id`, `merchant_id`, `card_id`, `device_id`, `location_id`).
    2.  `fraud_alerts` table: Check for any existing alerts for this `transaction_id`.
*   **Using the IDs from the `live_transactions` record, query all related dimension tables:**
    *   `users` (by `user_id`)
    *   `accounts` (by `account_id`)
    *   `merchants` (by `merchant_id`)
    *   `cards` (by `card_id`)
    *   `devices` (by `device_id`)
    *   `locations` (by `location_id`)
    *   `risk_scores` (by `user_id`)
    *   `blacklist` (Check if any of the IDs `user_id`, `account_id`, `card_id`, `device_id`, or `merchant_id` appear in the `value` column. Note: The `blacklist` table schema uses `entity_id`, `entity_type`, `value`).
*   **Find related transactions:** Query the `live_transactions` table for all other transactions by the same `user_id`, excluding the target `transaction_id`. Order by `timestamp DESC` and limit results appropriately (e.g., 1000).

## 3. Data Consolidation & JSON Creation
*   **Structure the final JSON object** with the following keys. Convert Python objects (like `datetime`, `list`, `dict`) to JSON-serializable strings (ISO format for dates, proper JSON arrays/objects).
    *   `live_transactions`: The main transaction record.
    *   `fraud_alerts`: The associated alert record (if any).
    *   `users`, `accounts`, `merchants`, `cards`, `devices`, `locations`, `risk_scores`, `blacklist`: The related dimension data.
    *   `related_transactions`: An **array** containing the other transactions for the user.
*   **Save the JSON file** locally to the workspace using `filesystem-write_file`. Name the file `<transaction_id>.json` (e.g., `T8492XJ3.json`).

## 4. Archiving & Alerting
*   **Upload the JSON file** to the identified archive storage bucket using `google-cloud-storage_upload_file`. Use the `transaction_id` as the blob name.
*   **Write a CRITICAL log entry** to the identified logging bucket using `google-cloud-logging_write_log`.
    *   **Log Name:** Use the full name of the log bucket (e.g., `Trading_Logging-e877351c7447`).
    *   **Severity:** `CRITICAL`
    *   **Message/Payload:** A JSON string with the exact structure: `{"alert_type": "Fraud", "transaction_id": "<TRANSACTION_ID>", "status": "Pending_Investigation"}`

## Key Considerations
*   **Error Handling:** If a query for a specific table returns no data, include an empty object `{}` for that key in the final JSON.
*   **Data Types:** Pay special attention to serializing complex fields (flags, velocity_checks, etc.) from the `live_transactions` table from stringified JSON to proper JSON objects/arrays in the output.
*   **Bucket Names:** The archive and log bucket names are dynamic (with unique suffixes). Always list buckets first to confirm their exact names.
*   **Logging:** The log write must happen *after* successful archiving. The log entry is new and independent of any existing logs in the bucket.
