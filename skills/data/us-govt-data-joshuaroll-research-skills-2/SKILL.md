---
name: us-govt-data
description: Access official US Government records. Currently supports SEC EDGAR (financial filings) and Federal Register (rule changes). Ensures data provenance from .gov domains.
---

# US Government & Legal Data Skill

This skill allows you to retrieve official documents from US government sources, essential for due diligence and regulatory research.

## Capabilities

1.  **SEC EDGAR**: Retrieve 10-K (Annual) and 10-Q (Quarterly) filings for public companies.
2.  **Federal Register**: (Future) Check for new agency rules.
3.  **Text Extraction**: Convert HTML filings to raw text for analysis.
4.  **Section Targeting**: Extract specific sections like "Risk Factors" automatically.
5.  **Company Search**: Query by name (e.g., "Google" for Alphabet Inc.) if ticker is unknown.

## Usage

Run the python script [fetch_filing.py](file:///C:/Users/Joshua/.gemini/antigravity/brain/126df87b-03b8-439b-8a30-d59c16e53143/skills/us-govt-data/fetch_filing.py) to retrieve SEC documents.

### Arguments

*   `ticker` (required): The stock symbol (e.g., AAPL) or partial company name.
*   `--type` (optional): Form type (default "10-K").
*   `--count` (optional): Number of filings to retrieve (default 1).
*   `--clean-text` (optional): Set this flag to download and strip HTML tags.
*   `--section` (optional): "risk" (Risk Factors) or "mda" (Management Discussion). Implies `--clean-text`.

### Example

```bash
# Get the text of "Risk Factors" for Google
python3 fetch_filing.py "Google" --type 10-K --section risk

# Get text for Tesla 10-Q
python3 fetch_filing.py TSLA --type 10-Q --clean-text
```

## Output Format

The script outputs a JSON object containing:
*   [cik](file:///C:/Users/Joshua/.gemini/antigravity/brain/126df87b-03b8-439b-8a30-d59c16e53143/skills/us-govt-data/fetch_filing.py#25-48): Central Index Key
*   `company_name`
*   [filings](file:///C:/Users/Joshua/.gemini/antigravity/brain/126df87b-03b8-439b-8a30-d59c16e53143/skills/us-govt-data/fetch_filing.py#75-149):
    *   `primaryDocumentUrl`: Direct link to the HTML document.
    *   `content`: The extracted text (truncated or fully extracted section).

## Tips for the Agent

*   **HTML takes space**: Only use `--clean-text` if you plan to read the content. It makes the requested slower (extra HTTP call).
*   **Name Search**: You can now pass "Microsoft" instead of "MSFT".
