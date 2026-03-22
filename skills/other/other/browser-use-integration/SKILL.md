---
name: browser-use-integration
description: Self-hosted AI browser automation using Browser Use with any LLM (Claude, GPT, Ollama). Use when building web scraping agents, data extraction pipelines, self-hosted automation, or when you need flexibility without API rate limits.
---

# Browser Use Integration

## Overview

Browser Use is an open-source AI browser automation framework that works with any LLM. Unlike cloud-dependent solutions, you can self-host for unlimited usage with local models.

**Key Advantages**:
- **Open Source**: No API rate limits or vendor lock-in
- **Any LLM**: Claude, GPT-4, Ollama (local), and more
- **Self-Hosted**: Run on your infrastructure
- **3-5x Faster**: Optimized for browser tasks

---

## Quick Start (10 Minutes)

### 1. Install Browser Use

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Browser Use
pip install browser-use

# Install LLM provider (choose one)
pip install langchain-anthropic  # For Claude
pip install langchain-openai     # For GPT-4
pip install langchain-ollama     # For local models
```

### 2. Configure API Key

```bash
# For Claude
export ANTHROPIC_API_KEY=your_key_here

# For OpenAI
export OPENAI_API_KEY=your_key_here

# For Ollama (no key needed, just run Ollama locally)
ollama serve
```

### 3. Write First Agent

```python
# agent.py
import asyncio
from browser_use import Agent
from langchain_anthropic import ChatAnthropic

async def main():
    agent = Agent(
        task="Go to google.com and search for 'Browser Use AI automation'",
        llm=ChatAnthropic(model="claude-sonnet-4-20250514"),
    )

    result = await agent.run()
    print(result)

asyncio.run(main())
```

### 4. Run

```bash
python agent.py
```

---

## LLM Configuration

### Claude (Recommended)

```python
from langchain_anthropic import ChatAnthropic

# Claude Sonnet (best balance)
llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

# Claude Opus (highest quality)
llm = ChatAnthropic(model="claude-opus-4-20250514")

# Claude Haiku (fastest, cheapest)
llm = ChatAnthropic(model="claude-3-5-haiku-20241022")
```

### OpenAI

```python
from langchain_openai import ChatOpenAI

# GPT-4o
llm = ChatOpenAI(
    model="gpt-4o",
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# GPT-4 Turbo
llm = ChatOpenAI(model="gpt-4-turbo-preview")
```

### Ollama (Free, Local)

```bash
# First, install and run Ollama
ollama serve

# Pull a model
ollama pull llama3.2
```

```python
from langchain_ollama import ChatOllama

# Local Llama 3.2
llm = ChatOllama(
    model="llama3.2",
    base_url="http://localhost:11434",
)

# Local Mistral
llm = ChatOllama(model="mistral")

# Local Code Llama
llm = ChatOllama(model="codellama")
```

### Cost Comparison

| LLM | Cost per 1M tokens | Best For |
|-----|-------------------|----------|
| Claude Haiku | ~$0.25 | Simple tasks |
| Claude Sonnet | ~$3.00 | Complex tasks |
| GPT-4o | ~$5.00 | General use |
| Ollama | **Free** | Unlimited local |

---

## Agent Patterns

### Simple Task

```python
agent = Agent(
    task="Search for 'Python tutorials' on YouTube and get the top 5 video titles",
    llm=llm,
)
result = await agent.run()
```

### Multi-Step Task

```python
agent = Agent(
    task="""
    1. Go to amazon.com
    2. Search for 'wireless mouse'
    3. Filter by 4+ star rating
    4. Extract the top 5 products with name, price, and rating
    5. Return as JSON
    """,
    llm=llm,
)
result = await agent.run()
```

### Task with Extraction Schema

```python
from pydantic import BaseModel
from typing import List

class Product(BaseModel):
    name: str
    price: float
    rating: float
    url: str

class ProductList(BaseModel):
    products: List[Product]

agent = Agent(
    task="Find the top 5 laptops on BestBuy under $1000",
    llm=llm,
    output_schema=ProductList,  # Structured output
)
result = await agent.run()
# result.products is List[Product]
```

### With Custom Browser Settings

```python
from browser_use import Agent, Browser

browser = Browser(
    headless=False,  # Show browser
    proxy="http://proxy.example.com:8080",  # Use proxy
)

agent = Agent(
    task="Navigate to example.com",
    llm=llm,
    browser=browser,
)
```

---

## Error Handling

```python
import asyncio
from browser_use import Agent, AgentError

async def run_with_retry(task: str, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            agent = Agent(task=task, llm=llm)
            result = await agent.run()
            return result
        except AgentError as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)  # Exponential backoff

# Usage
result = await run_with_retry("Search Google for 'AI news'")
```

### Timeout Handling

```python
async def run_with_timeout(task: str, timeout: int = 60):
    agent = Agent(task=task, llm=llm)
    try:
        result = await asyncio.wait_for(agent.run(), timeout=timeout)
        return result
    except asyncio.TimeoutError:
        print(f"Task timed out after {timeout}s")
        return None
```

---

## Self-Hosting

### Docker Setup

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Install Chrome
RUN apt-get update && apt-get install -y \
    wget gnupg \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "agent.py"]
```

```text
# requirements.txt
browser-use
langchain-anthropic
langchain-ollama
```

### Docker Compose with Ollama

```yaml
# docker-compose.yml
version: '3.8'
services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama-data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]  # If GPU available

  browser-agent:
    build: .
    environment:
      - OLLAMA_HOST=http://ollama:11434
    depends_on:
      - ollama

volumes:
  ollama-data:
```

### Run

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f browser-agent
```

---

## Use Cases

### 1. Web Scraping

```python
agent = Agent(
    task="""
    Go to news.ycombinator.com
    Extract the top 30 stories with: title, points, comments, and URL
    Return as JSON array
    """,
    llm=llm,
)
```

### 2. Form Automation

```python
agent = Agent(
    task="""
    Go to example.com/contact
    Fill the form:
    - Name: John Doe
    - Email: john@example.com
    - Message: I'm interested in your services
    Submit the form
    """,
    llm=llm,
)
```

### 3. Price Monitoring

```python
agent = Agent(
    task="""
    Check the price of 'Sony WH-1000XM5' on:
    1. Amazon
    2. BestBuy
    3. Walmart
    Return prices from each site
    """,
    llm=llm,
)
```

### 4. Competitor Research

```python
agent = Agent(
    task="""
    Visit competitor.com
    Extract:
    - Pricing tiers
    - Feature list
    - Customer testimonials
    Format as structured report
    """,
    llm=llm,
)
```

### 5. Data Entry

```python
# Batch process data entry
data_entries = [
    {"name": "Product A", "price": 99.99},
    {"name": "Product B", "price": 149.99},
]

for entry in data_entries:
    agent = Agent(
        task=f"""
        Go to admin.example.com/products/new
        Add product: {entry['name']} with price ${entry['price']}
        Save and confirm
        """,
        llm=llm,
    )
    await agent.run()
```

---

## Best Practices

### 1. Be Specific

```python
# BAD - vague
agent = Agent(task="Find products", llm=llm)

# GOOD - specific
agent = Agent(
    task="Go to amazon.com, search for 'mechanical keyboard', filter by 4+ stars, extract top 5 with name and price",
    llm=llm,
)
```

### 2. Use Structured Output

```python
from pydantic import BaseModel

class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str

agent = Agent(
    task="Search Google for 'AI news' and get top 5 results",
    llm=llm,
    output_schema=SearchResult,  # Type-safe output
)
```

### 3. Handle Authentication

```python
# Option 1: Include credentials in task
agent = Agent(
    task="""
    Go to app.example.com/login
    Login with email 'user@example.com' and password 'secure123'
    Navigate to dashboard
    """,
    llm=llm,
)

# Option 2: Use cookies/session (more secure)
browser = Browser()
await browser.load_cookies("session_cookies.json")
agent = Agent(task="...", llm=llm, browser=browser)
```

### 4. Rate Limiting

```python
import asyncio

async def run_with_rate_limit(tasks: list, rate_per_minute: int = 10):
    delay = 60 / rate_per_minute
    results = []

    for task in tasks:
        agent = Agent(task=task, llm=llm)
        result = await agent.run()
        results.append(result)
        await asyncio.sleep(delay)

    return results
```

---

## Comparison: Browser Use vs Stagehand

| Feature | Browser Use | Stagehand |
|---------|-------------|-----------|
| **Language** | Python | TypeScript |
| **Self-Hosted** | Yes | Yes |
| **Local LLM** | Yes (Ollama) | Limited |
| **Speed** | 3-5x optimized | 44% faster (v3) |
| **Best For** | Python scraping | TypeScript testing |
| **Learning Curve** | Easy | Medium |

**When to use Browser Use**:
- Python projects
- Need local LLM (Ollama)
- Web scraping focus
- Cost optimization (free with Ollama)

**When to use Stagehand**:
- TypeScript/Node.js projects
- Testing focus
- Claude integration priority
- Self-healing tests

---

## References

- `references/browser-use-setup.md` - Complete installation guide
- `references/llm-configuration.md` - LLM setup for all providers

---

**Browser Use gives you AI browser automation with full control - self-host with any LLM, no rate limits, no vendor lock-in.**
