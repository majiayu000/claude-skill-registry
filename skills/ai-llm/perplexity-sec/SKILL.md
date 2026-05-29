---
name: perplexity-sec
description: SEC EDGAR filings search. Use for official regulatory documents.
---

# Perplexity SEC

## Supported Filings

10-K (annual), 10-Q (quarterly), 8-K (current), S-1/S-4 (IPO/M&A)

## Command

```bash
cd /home/faisal/EventMarketDB && python3 -c "
from utils.perplexity_search import perplexity_sec_search
print(perplexity_sec_search('AAPL 10-K risk factors', search_after_date='01/01/2024'))
"
```

Date format: MM/DD/YYYY
