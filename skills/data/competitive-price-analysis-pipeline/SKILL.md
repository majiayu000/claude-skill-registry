---
name: competitive-price-analysis-pipeline
description: Performs competitive price analysis by comparing internal pricing data with competitor information from different sources (PDFs, CSVs, spreadsheets), calculates price differences, generates insights, and stores results in BigQuery for decision-making.
---
# Instructions

## 1. Initial Setup & Discovery
- **List the workspace directory** to identify available files.
- **Read the requirements document** (e.g., `requirement.md`) to understand the target BigQuery dataset, table, and required schema.
- **Read the internal pricing file** (CSV or Excel) to understand the structure and product list.

## 2. Extract Competitor Pricing Data
- **Inspect the competitor PDF** to understand its structure (page count, layout).
- **Read all pages** of the competitor PDF to extract text content containing product names and prices.

## 3. Data Processing & Matching
- **Parse the internal pricing data.** The key columns are `Product Name` and `Our Price`.
- **Parse the competitor PDF text.** Identify product names and their corresponding prices. Use fuzzy matching or keyword mapping (e.g., "SmartWidget Pro" → "SmartWidget Professional Edition") based on the trajectory example.
- **Create a matched product list.** For each internal product, find the corresponding competitor product and price. If a direct match isn't found, log it for manual review.
- **Calculate the price difference** for each matched product: `Price Difference = Our Price - Competitor Price`.

## 4. Prepare Output & Load to BigQuery
- **Create a CSV file** (`price_comparison.csv`) with the exact columns specified in the requirements:
    - `Product Name` (String)
    - `Our Price` (Float)
    - `Competitor Price` (Float)
    - `Price Difference` (Float)
- **Verify the BigQuery dataset exists.** If it doesn't, you may need to create it (though the trajectory shows it pre-existing).
- **Load the CSV data** into the specified BigQuery table (`dataset_id.table_id`). Use `WRITE_TRUNCATE` mode to replace any existing data, as per the trajectory.
- **Run a validation query** to confirm the data was loaded correctly and matches the expected row count and schema.

## 5. Generate Summary & Finalize
- **Provide a concise summary** of the analysis, including:
    - Number of products processed.
    - Count of products priced higher/lower than the competitor.
    - The product with the largest price advantage (most negative difference).
    - The product with the largest price disadvantage (most positive difference).
- **Claim the task as done.**

## Key Considerations
- **Product Matching Logic:** This is a high-freedom, interpretive step. Use the provided `scripts/match_products.py` as a starting point, but be prepared to adjust matching rules (keywords, categories) based on the specific data.
- **BigQuery Permissions:** Ensure the agent has the necessary permissions to list datasets and load data to the specified table.
- **Data Types:** Ensure numeric prices are parsed as floats. Handle currency symbols and commas appropriately.
- **Error Handling:** If the PDF extraction yields poor results, consider using the `pdf-tools-search_pdf` function to find specific product names or prices.
