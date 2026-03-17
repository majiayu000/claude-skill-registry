---
name: google-web-search
description: Enables grounded question answering by automatically executing the Google Search tool within Gemini models. Use when the required information is recent (post knowledge cutoff) or requires verifiable citation.
---

# Google Web Search

## Overview

This skill provides the capability to perform real-time web searches via the Gemini API's `google_search` grounding tool. It is designed to fetch the most current information available on the web to provide grounded, citable answers to user queries.

**Key Features:**
- Real-time web search via Gemini API
- Grounded responses with verifiable citations
- Configurable model selection
- Simple Python API

## Usage

This skill exposes the Gemini API's `google_search` tool. It should be used when the user asks for **real-time information**, **recent events**, or requests **verifiable citations**.

### Execution Context

The core logic is in `scripts/example.py`. This script requires the following environment variables:

- **GEMINI_API_KEY** (required): Your Gemini API key
- **GEMINI_MODEL** (optional): Model to use (default: `gemini-2.5-flash-lite`)

**Supported Models:**
- `gemini-2.5-flash-lite` (default) - Fast and cost-effective
- `gemini-3-flash-preview` - Latest flash model
- `gemini-3-pro-preview` - More capable, slower
- `gemini-2.5-flash-lite-preview-09-2025` - Specific version

### Python Tool Implementation Pattern

When integrating this skill into a larger workflow, the helper script should be executed in an environment where the `google-genai` library is available and the `GEMINI_API_KEY` is exposed.

Example Python invocation structure:
```python
from skills.google-web-search.scripts.example import get_grounded_response

# Basic usage (uses default model):
prompt = "What is the latest market trend?"
response_text = get_grounded_response(prompt)
print(response_text)

# Using a specific model:
response_text = get_grounded_response(prompt, model="gemini-3-pro-preview")
print(response_text)

# Or set via environment variable:
import os
os.environ["GEMINI_MODEL"] = "gemini-3-flash-preview"
response_text = get_grounded_response(prompt)
print(response_text)
```

### Troubleshooting

If the script fails:
1. **Missing API Key**: Ensure `GEMINI_API_KEY` is set in the execution environment.
2. **Library Missing**: Verify that the `google-genai` library is installed (`pip install google-generativeai`).
3. **API Limits**: Check the API usage limits on the Google AI Studio dashboard.
4. **Invalid Model**: If you set `GEMINI_MODEL`, ensure it's a valid Gemini model name.
5. **Model Not Supporting Grounding**: Some models may not support the `google_search` tool. Use flash or pro variants.