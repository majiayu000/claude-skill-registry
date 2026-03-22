---
name: browser-use
description: >-
  You are an expert in Browser Use, the Python library that lets AI agents
  control a web browser. You help developers build agents that can navigate
  websites, fill forms, click buttons, extract data, and complete multi-step
  web tasks — using vision and DOM understanding to interact with any website
  like a human would.
license: Apache-2.0
compatibility: ''
metadata:
  author: terminal-skills
  version: 1.0.0
  category: AI & Machine Learning
  tags:
    - browser
    - automation
    - agent
    - web
    - scraping
    - ai
    - playwright
---

# Browser Use — AI Browser Automation Agent

You are an expert in Browser Use, the Python library that lets AI agents control a web browser. You help developers build agents that can navigate websites, fill forms, click buttons, extract data, and complete multi-step web tasks — using vision and DOM understanding to interact with any website like a human would.

## Core Capabilities

```python
from browser_use import Agent
from langchain_openai import ChatOpenAI

agent = Agent(
    task="Go to amazon.com, search for 'mechanical keyboard', and find the best-rated one under $100",
    llm=ChatOpenAI(model="gpt-4o"),
)
result = await agent.run()
print(result)  # "The best-rated mechanical keyboard under $100 is..."

# Multi-step tasks
agent = Agent(
    task="""
    1. Go to github.com/myorg/myrepo
    2. Click on Issues tab
    3. Create a new issue with title 'Update dependencies' and body 'Run npm audit fix'
    4. Add the label 'maintenance'
    """,
    llm=ChatOpenAI(model="gpt-4o"),
)
await agent.run()

# With custom browser config
from browser_use import BrowserConfig

config = BrowserConfig(
    headless=True,
    proxy="http://proxy:8080",
    cookies=[{"name": "session", "value": "abc123", "domain": ".example.com"}],
)
agent = Agent(task="...", llm=llm, browser_config=config)

# Extract structured data
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    rating: float

agent = Agent(
    task="Go to bestbuy.com and find the top 5 laptops. Return structured data.",
    llm=ChatOpenAI(model="gpt-4o"),
    output_model=list[Product],
)
result = await agent.run()
# result is list[Product] — validated Pydantic objects
```

## Installation

```bash
pip install browser-use
playwright install
```

## Best Practices

1. **Vision model** — Use GPT-4o or Claude for best browser understanding; sees screenshots + DOM
2. **Structured output** — Pass `output_model` for typed extraction; Pydantic validation on results
3. **Headless mode** — Use `headless=True` for server/CI; `False` for debugging to watch the agent
4. **Cookies/auth** — Pre-set cookies for authenticated sessions; agent operates as logged-in user
5. **Task decomposition** — Write tasks as numbered steps for complex flows; agent follows the sequence
6. **Proxy support** — Use proxies for scraping at scale; rotate IPs to avoid blocks
7. **Retry on failure** — Browser Use auto-retries failed interactions; configure max attempts
8. **Combine with APIs** — Use browser for sites without APIs; prefer APIs when available (faster, cheaper)
