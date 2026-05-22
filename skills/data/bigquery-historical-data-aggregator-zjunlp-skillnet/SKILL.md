---
name: bigquery-historical-data-aggregator
description: Aggregates and analyzes historical data from multiple BigQuery tables with similar schemas. Queries multiple tables using UNION ALL, calculates aggregate metrics (averages, sums, counts), handles table discovery via INFORMATION_SCHEMA, and processes large datasets efficiently with batch queries.
---
# Instructions

## Core Workflow
1.  **Discover Tables:** First, query `INFORMATION_SCHEMA.TABLES` to identify all available tables within the target dataset. This ensures the skill adapts to the actual table names present.
2.  **Aggregate Historical Data:** Construct a SQL query that uses `UNION ALL` to combine data from all identified tables. Calculate the required aggregate metric (e.g., `AVG(score)`) grouped by the relevant key (e.g., `student_id`, `name`).
3.  **Handle Large Results:** For datasets returning many rows (>50), use a batched querying strategy (e.g., `LIMIT` and `OFFSET` or filtering by key ranges) to retrieve the complete result set without truncation.
4.  **Join with Latest Data:** Read the latest data from the provided source (e.g., a local CSV file). Perform a join between the aggregated historical data and the latest data to enable comparative analysis.
5.  **Calculate Deltas & Filter:** Compute the percentage change or difference between historical and latest values. Apply the user-specified threshold filter (e.g., `drop_percentage > 0.25`).
6.  **Output Results:** Write the filtered results to the specified output file (e.g., `bad_student.csv`).
7.  **Trigger Critical Actions:** For records exceeding a higher, critical threshold (e.g., `drop_percentage > 0.45`), execute immediate actions such as writing critical log entries to a designated logging service.

## Key Techniques
*   **Dynamic Table Inclusion:** Use the list from `INFORMATION_SCHEMA` to build the `UNION ALL` query dynamically. Do not hardcode table names.
*   **Efficient Batch Retrieval:** When the final aggregated list or intermediate results are large, retrieve data in manageable chunks using `WHERE` clauses on sequential keys or `LIMIT/OFFSET`.
*   **Precise Percentage Calculation:** Ensure the percentage change formula is correct: `(historical_value - latest_value) / historical_value`.
*   **Logging for Notification:** When writing critical logs, include all necessary identifiers (e.g., name, ID) and context so downstream systems can trigger alerts or notifications.

## Error Handling & Validation
*   Confirm the target dataset exists before querying.
*   Verify that source files (e.g., CSV) exist and are readable.
*   Validate that the log bucket or destination for critical alerts exists and is accessible.

## Bundled Resources
*   `scripts/aggregate_query_template.sql`: A parameterized SQL template for the core aggregation logic.
*   `references/schema_example.md`: An example schema to illustrate the expected table structure.

---
