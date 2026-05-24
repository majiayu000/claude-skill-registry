---
name: langchain-deep-research
description: Run LangChain Open Deep Research agent for iterative web research and comprehensive reports. Requires LLM API keys and search API (e.g., OPENAI_API_KEY, TAVILY_API_KEY).
---

# LangChain Open Deep Research Skill

This skill utilizes the LangChain Open Deep Research framework to perform iterative web research with reflection and knowledge gap identification, producing comprehensive reports with citations.

## Setup

1. **Dependencies:** Requires the `open-deep-research` package and LangGraph.

    ```bash
    pip install open-deep-research langgraph-cli python-dotenv
    ```

2. **API Key Configuration:** Requires API keys for an LLM and a search provider.

    ```bash
    # Set up your API keys
    echo "# LLM Configuration" >> .env
    echo "OPENAI_API_KEY=your_openai_key" >> .env
    echo "# Search Configuration" >> .env
    echo "TAVILY_API_KEY=your_tavily_key" >> .env
    if [ -f .gitignore ] && ! grep -q ".env" .gitignore; then echo ".env" >> .gitignore; fi
    echo "API keys saved to .env."
    ```

## Usage

Use the `scripts/research.py` script to run a research task.

### Command

```bash
python3 scripts/research.py --query "<research_query>" [--max-iterations <N>]
```

### Parameters

* `--query` (Required): The research question or topic.
* `--max-iterations` (Optional): Maximum number of research iterations (default: 3).
* `--output` (Optional): Output file path for the final report (default: stdout).

### Example

```bash
python3 scripts/research.py --query "What are the latest developments in quantum computing error correction?" --max-iterations 4 --output report.md
```

## Output

The script outputs a comprehensive research report with:

* Iterative search findings
* Knowledge gap analysis
* Final synthesized report with citations
* Source list

## Features

* **Iterative Research**: Performs multiple search cycles, reflecting on gaps
* **Configurable Models**: Supports OpenAI, Anthropic, Ollama, and other LLM providers
* **Multiple Search Engines**: Tavily (default), Brave, DuckDuckGo, SerpAPI
* **Citation Tracking**: All findings include source references
