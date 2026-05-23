---
name: us-govt-data
description: Access official US Government records. Currently supports SEC EDGAR (financial filings) and Federal Register (rule changes). Ensures data provenance from .gov domains.
---

# US Government & Legal Data Skill

This skill allows you to retrieve official documents from US government sources, essential for due diligence and regulatory research.

## Capabilities

1.  **SEC EDGAR**: Retrieve 10-K (Annual) and 10-Q (Quarterly) filings for public companies.
2.  **Federal Register**: (Future) Check for new agency rules.

## Usage

Run the python script `fetch_filing.py` to retrieve SEC documents.

### Arguments

*   `ticker` (required): The stock symbol (e.g., AAPL, MSFT).
*   `--type` (optional): Form type (default "10-K").
*   `--count` (optional): Number of filings to retrieve (default 1).

### Example

```bash
# Get the latest 10-K for Apple
python3 fetch_filing.py AAPL --type 10-K

# Get the last 3 quarterly reports for Tesla
python3 fetch_filing.py TSLA --type 10-Q --count 3
```

## Output Format

The script outputs a JSON object containing:
*   `cik`: Central Index Key
*   `company_name`
*   `filings`: List of filing objects:
    *   `accessionNumber`
    *   `filingDate`
    *   `reportDate`
    *   `primaryDocumentUrl`: Direct link to the HTML document on sec.gov
    *   `description`

## Tips for the Agent

*   **User-Agent**: The script automatically sets a compliant User-Agent.
*   **Direct Links**: Always provide the `primaryDocumentUrl` to the user so they can verify the source.
*   **Financials**: Use the link to read the full text if specific financial data extraction is needed (this basic skill finds the document).
