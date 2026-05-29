---
name: prd-clean
description: "Archive merged and invalid stories from prd.json to prd.archived.json, keeping only active work in the main PRD. Triggers on: clean prd, archive merged stories, clean up prd, move merged stories."
---

# PRD Clean - Archive Completed Stories

Run the following command and display its output to the user:

```bash
python3 .claude/skills/prd-clean/clean_prd.py ./prd.json
```

The script handles everything: reading prd.json, archiving merged/invalid stories to prd.archived.json, updating prd.json in-place, and printing a full recap. If there are errors they will be printed to stderr.
