---
name: xai-grok
description: Use xAI Grok API with Agent Tools for real-time web and X (Twitter) search and synthesis. Requires XAI_API_KEY.
---

# xAI Grok Research Skill

This skill utilizes the xAI Grok API and its Agent Tools for autonomous research, including real-time web and X platform search.

## Setup

1.  **Dependencies:** Requires the `xai-sdk`.
    ```bash
    pip install xai-sdk python-dotenv
    ```

2.  **API Key Configuration:** The skill requires the `XAI_API_KEY`.

    ```bash
    # If the script fails due to a missing key, run the following:
    echo "It seems the xAI API key is not set up."
    read -p "Enter your xAI API key: " GROK_KEY
    echo "XAI_API_KEY=$GROK_KEY" >> .env
    if [ -f .gitignore ] && ! grep -q ".env" .gitignore; then echo ".env" >> .gitignore; fi
    echo "API key saved to .env."
    ```

## Usage

Use the `scripts/grok_research.py` script. Grok will autonomously use the enabled tools.

### Command

```bash
python3 scripts/grok_research.py --query "<query>" [--model <model_name>] [--web-search] [--x-search]
```

### Parameters

* `--query` (Required): The research query.
* `--model` (Optional): Defaults to `grok-4.1-fast-reasoning` (optimized for tools).
* `--web-search` (Optional): Enable web search tool.
* `--x-search` (Optional): Enable X (Twitter) search tool.

### Example

```bash
python3 scripts/grok_research.py --query "What is the current public sentiment and news coverage on the latest AI regulations?" --web-search --x-search
```

## Output

The script streams the agent's thought process (to stderr) for visibility and outputs the final synthesized answer (to stdout) with citations.
