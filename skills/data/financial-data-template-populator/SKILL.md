---
name: financial-data-template-populator
description: Populates an Excel template with financial data (stock prices, market trends, ownership) for a specified company. Reads requirement files, fetches data from Yahoo Finance, analyzes template structure, formats data, writes to Excel, and renames the output file.
---
# Instructions

## 1. Understand the Request & Locate Files
The user will request to populate an Excel template with financial data for a specific company (e.g., NVIDIA/NVDA). They will provide:
*   An Excel template file (e.g., `results_template.xlsx`).
*   A data requirements file (e.g., `data.txt`).
*   A formatting instructions file (e.g., `tips.txt`).
*   A final output filename (e.g., `results.xlsx`).

First, read the requirement files to understand the exact data needed and formatting rules.

**Tool Calls:**
*   Use `filesystem-read_multiple_files` to read `data.txt` and `tips.txt`.

## 2. Analyze the Excel Template Structure
Examine the provided Excel template to understand its sheets, headers, and data ranges.

**Tool Calls:**
1.  Use `excel-get_workbook_metadata` on the template file to list its sheets.
2.  Use `excel-read_data_from_excel` on each sheet to see the column headers and empty data cells.

## 3. Fetch Required Financial Data
Based on the requirements (`data.txt`), fetch the necessary data. Common requirements include:
*   **Stock Info & Fundamentals:** Use `yahoo-finance-get_stock_info`.
*   **Major Holders Summary:** Use `yahoo-finance-get_holder_info` with `holder_type: "major_holders"`.
*   **Institutional Holders Details:** Use `yahoo-finance-get_holder_info` with `holder_type: "institutional_holders"`.
*   **Historical Stock Prices:** Use `yahoo-finance-get_historical_stock_prices` for a date range, or `yahoo-finance-get_stock_price_by_date` for specific quarter-end dates.

**Key Data Processing:**
*   Identify quarter-end dates (e.g., 2024-09-30 for Q3 2024).
*   Calculate Market Cap = `Stock Price * Shares Outstanding`.
*   Convert units as required (e.g., shares to millions, value to billions).

## 4. Format Data According to Rules
Strictly apply the formatting rules from `tips.txt` (e.g., "Round all numbers to two decimal places", "If the data is unavailable, fill in NaN").

## 5. Populate the Excel Template
Write the formatted data into the correct cells of the template.

**Tool Calls:**
*   Use `excel-write_data_to_excel` for each sheet, specifying the `start_cell` (e.g., "B2" for data below headers).

## 6. Finalize and Rename the File
After populating all sheets, rename the file to the user's requested output name (e.g., from `results_template.xlsx` to `results.xlsx`).

**Tool Calls:**
*   Use `filesystem-move_file`.

## 7. Verify Completion
Optionally, list the directory contents to confirm the final file exists and read back a sample of the data to ensure correctness.

**Tool Calls:**
*   Use `filesystem-list_directory`.
*   Use `excel-read_data_from_excel` on the final file.
