---
name: deep-research
description: Run OpenAI deep research to analyze and synthesize web sources into a comprehensive report. Invoked with a research query as argument.
user_invocable: true
---

# Deep Research

Use OpenAI's `o4-mini-deep-research` model to perform deep web research and return a comprehensive report with citations.

## Requirements

- `OPENAI_API_KEY` must be set in the environment
- `openai` Python package must be installed

## Procedure

1. Receive the user's research query from `$ARGUMENTS`
2. Ensure the `openai` package is available: run `pip install -q openai` via Bash
3. Run the research script via Bash in background mode (it may take several minutes):
   ```
   python skills/deep-research/scripts/deep_research.py "$ARGUMENTS"
   ```
4. Wait for the script to complete
5. Present the returned markdown report to the user as-is (it includes inline citations and a sources list)
6. If the script fails, show the error output and suggest:
   - Check that `OPENAI_API_KEY` is set and valid
   - Check that the `openai` package is installed (`pip install openai`)
   - Check OpenAI API status at https://status.openai.com
