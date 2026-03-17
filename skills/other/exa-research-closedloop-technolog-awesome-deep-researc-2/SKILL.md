---
name: exa-research
description: Use Exa AI for neural search, content retrieval, and automated deep research. Requires EXA_API_KEY.
---

# Exa Research Skill

This skill leverages the Exa AI API for neural search, finding similar content, and autonomous research via their Research endpoint.

## Setup

1.  **Dependencies:** Requires `exa-py` and `openai` (for research endpoint compatibility).
    ```bash
    pip install exa-py openai python-dotenv
    ```

2.  **API Key Configuration:** Requires `EXA_API_KEY`.

    ```bash
    # If the script fails due to a missing key, run the following:
    echo "It seems the Exa API key is not set up."
    read -p "Enter your Exa API key: " EXA_KEY
    echo "EXA_API_KEY=$EXA_KEY" >> .env
    if [ -f .gitignore ] && ! grep -q ".env" .gitignore; then echo ".env" >> .gitignore; fi
    echo "API key saved to .env."
    ```

## Usage

The script `scripts/exa_tools.py` supports multiple operations.

### 1. Search and Contents

Perform a neural search and retrieve content or highlights.

```bash
python3 scripts/exa_tools.py search "<query>" [--num-results <N>] [--highlights]
```

**Example:**

```bash
python3 scripts/exa_tools.py search "innovative sustainable urban planning" --num-results 5 --highlights
```

### 2. Research (Automated)

Automate in-depth research and receive a structured report.

```bash
python3 scripts/exa_tools.py research "<query>" [--model <exa-research|exa-research-pro>]
```

**Example:**

```bash
python3 scripts/exa_tools.py research "Analyze the impact of quantum computing on cryptography" --model exa-research-pro
```

### 3. Find Similar

Find pages similar to a given URL.

```bash
python3 scripts/exa_tools.py find_similar "<url>"
```

**Example:**

```bash
python3 scripts/exa_tools.py find_similar "https://arxiv.org/abs/1706.03762"
```

## Output

The script outputs results in JSON format.
