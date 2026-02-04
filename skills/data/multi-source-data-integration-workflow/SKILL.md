---
name: multi-source-data-integration-workflow
description: When the user requires an end-to-end workflow that integrates data from multiple sources (financial APIs, local files) and outputs to collaboration tools (Google Sheets, Notion), this skill orchestrates the complete pipeline reading template formats, fetching external data, processing and transforming data, writing to cloud spreadsheets, and updating project management tools. Triggers include complex requests involving 'retrieve data and record in', 'create sheet with data from', or workflows that span multiple platforms with specific formatting requirements.
---
# Instructions

## 1. Understand the Request & Parse Requirements
- Identify the target stocks/tickers, date range, and required data fields (e.g., Open, High, Low, Close, Volume).
- Confirm the user wants **original prices** (`auto_adjust: false`), not adjusted prices.
- Identify the target output Google Sheet name and specific worksheet name.
- Identify the target Notion page and the exact notification message/comment to add.

## 2. Read the Format Template
- Locate and read the example file (e.g., `example.csv`) provided by the user to understand the required column order and data format.
- The standard format is: `Ticker,Date,Open,High,Low,Close,Volume`.

## 3. Create and Prepare the Google Sheet
- Create a new Google Spreadsheet with the requested title.
- Rename the default first worksheet to the requested name (e.g., "Jun-Jul_2025").

## 4. Fetch Historical Stock Data
- For each ticker, use the Yahoo Finance tool (`yahoo-finance-get_historical_stock_prices`) to fetch daily data for the specified date range.
- **CRITICAL:** Set `auto_adjust` to `false` to get original prices.
- The API automatically excludes non-trading days.

## 5. Process and Transform the Data
- Consolidate data from all tickers into a single list.
- Transform each data point to match the template format: `[Ticker, Date (YYYY-MM-DD), Open, High, Low, Close, Volume]`.
- Sort the consolidated list primarily by Date, then by Ticker to maintain a clean, chronological order grouped by ticker for each day.

## 6. Write Data to Google Sheet
- Write the header row (`Ticker,Date,Open,High,Low,Close,Volume`) to cell A1 of the target worksheet.
- Write the consolidated, sorted data rows starting from cell A2.
- Obtain the final URL of the Google Sheet.

## 7. Update the Notion Page
- Search for the target Notion page (e.g., "Quant Research") using the Notion API.
- Once the correct page ID is found, append a new line containing the Google Sheet URL in the format: `Google Sheet : {url}`.
- Add a comment to the top of that page with the exact text: "Monthly market data is ready. The reporting team can view it directly".

## 8. Final Verification
- Confirm the data has been written to the Google Sheet correctly.
- Confirm the Notion page has been updated with the URL and the top comment.
- Inform the user that the workflow is complete.
