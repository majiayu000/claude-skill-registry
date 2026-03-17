---
name: hello-demo
description: Delivers a static Hello World HTML demo page with bookmarklet. Use when user requests the hello demo, hello world demo, or demo page.
metadata:
  version: 1.0.4
---

## Delivery Instructions

When triggered:

1. Copy the asset to outputs:
```bash
cp assets/hello-demo.html /mnt/user-data/outputs/
```

2. Provide the computer link:
```
[View hello-demo.html](computer:///mnt/user-data/outputs/hello-demo.html)
```

3. Add one-line description: "Interactive HTML demo with bookmarklet showing token-efficient artifact delivery."

**DO NOT**:
- Generate HTML from scratch
- Explain the file contents in detail
- Add verbose commentary

The asset contains a complete, styled HTML page with:
- Bookmarklet demonstration
- Usage instructions
- Token efficiency explanation

**Token efficiency**: This pattern saves ~500 tokens vs. generating explanatory text each time.
