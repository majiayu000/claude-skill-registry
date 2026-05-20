---
name: perplexity-research
description: Use when conducting web research with Perplexity API - covers authentication, search strategies, structured output generation, and integration patterns for Claude-interpretable results
---

# Perplexity API Research Integration

## When to Use This Skill

Invoke this skill when you need to:
- Conduct comprehensive web research beyond Claude's knowledge cutoff
- Gather current market data, pricing, or competitive intelligence
- Find technical documentation or implementation examples
- Research industry trends, news, or recent developments
- Generate structured research reports with citations
- Build research workflows that feed into Claude's analysis

## Core Principles

1. **Structured Queries**: Design prompts that request specific, structured responses
2. **Citation Tracking**: Always capture and preserve source URLs for verification
3. **Iterative Refinement**: Start broad, then narrow based on initial results
4. **Claude Integration**: Format output for easy Claude interpretation and analysis
5. **API Efficiency**: Batch related queries to minimize API calls

## Authentication Setup

### Step 1: API Key Configuration

```python
from dotenv import load_dotenv
import os
import requests

load_dotenv('.env')

PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')
PERPLEXITY_API_URL = 'https://api.perplexity.ai/chat/completions'

headers = {
    'Authorization': f'Bearer {PERPLEXITY_API_KEY}',
    'Content-Type': 'application/json'
}
```

### Step 2: Environment Configuration

Create `.env` file:
```bash
PERPLEXITY_API_KEY=your_api_key_here
```

**CRITICAL**: Add `.env` to `.gitignore`

## Basic Research Pattern

### Pattern: Simple Query with Structured Output

```python
def perplexity_search(query, system_prompt=None):
    """Execute Perplexity search with optional system prompt for structure"""

    payload = {
        'model': 'llama-3.1-sonar-large-128k-online',  # Latest model
        'messages': [
            {'role': 'system', 'content': system_prompt or 'You are a helpful research assistant.'},
            {'role': 'user', 'content': query}
        ],
        'temperature': 0.2,  # Low temperature for factual research
        'return_citations': True,
        'return_images': False
    }

    response = requests.post(
        PERPLEXITY_API_URL,
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        data = response.json()
        return {
            'content': data['choices'][0]['message']['content'],
            'citations': data.get('citations', []),
            'model': data.get('model')
        }
    else:
        raise Exception(f"Perplexity API error: {response.status_code} - {response.text}")
```

## Structured Output Patterns

### Pattern: Market Research with JSON Output

```python
system_prompt = """
You are a market research analyst. For each query, respond with a JSON structure:
{
  "market_size": {"value": "number", "unit": "currency", "year": "YYYY"},
  "growth_rate": {"value": "percentage", "timeframe": "description"},
  "key_players": [{"name": "company", "market_share": "percentage"}],
  "trends": ["trend1", "trend2", "trend3"],
  "sources": ["url1", "url2"]
}
"""

query = "What is the current size and growth rate of the pharmaceutical drug discovery market?"

result = perplexity_search(query, system_prompt)

import json
market_data = json.loads(result['content'])
```

### Pattern: Competitive Intelligence

```python
system_prompt = """
You are a competitive intelligence analyst. Structure your response as:

## Competitor Overview
- Name:
- Founded:
- Headquarters:

## Product/Service
- Description:
- Key Features:
- Pricing:

## Market Position
- Target Customers:
- Competitive Advantages:
- Weaknesses:

## Recent News
- [Date] Event description
- [Date] Event description

## Sources
- [1] URL
- [2] URL
"""

query = "Analyze DeepMind's AlphaFold product for drug discovery market positioning"

result = perplexity_search(query, system_prompt)
# Result is markdown-formatted for easy Claude parsing
```

### Pattern: Technical Documentation Search

```python
system_prompt = """
You are a technical documentation expert. For API/library queries, respond with:

## Overview
Brief description of the technology

## Installation
Installation steps or package managers

## Basic Usage
Code example showing common use case

## Key Methods/Functions
- method_name: description
- method_name: description

## Common Patterns
Example code snippets

## Official Documentation
Links to official docs and tutorials
"""

query = "How do I use the gspread library for Google Sheets automation in Python?"

result = perplexity_search(query, system_prompt)
```

## Advanced Research Workflows

### Pattern: Multi-Stage Research Pipeline

```python
def research_pipeline(topic):
    """
    Execute multi-stage research:
    1. Broad overview
    2. Deep dive on key aspects
    3. Recent developments
    4. Synthesis
    """

    # Stage 1: Overview
    overview = perplexity_search(
        f"Provide a comprehensive overview of {topic}, including key technologies, major players, and market dynamics.",
        system_prompt="Provide a structured overview with sections: Technology, Market, Key Players, Challenges."
    )

    # Stage 2: Extract key players for deep dive
    key_players = extract_companies(overview['content'])  # Custom parsing

    # Stage 3: Deep dive on each player
    player_analysis = []
    for player in key_players[:3]:  # Top 3 only
        analysis = perplexity_search(
            f"Analyze {player}'s position in {topic}: products, market share, recent news, competitive advantages.",
            system_prompt="Structure as: Products, Market Position, Recent News (last 6 months), Advantages/Disadvantages."
        )
        player_analysis.append({
            'company': player,
            'analysis': analysis['content'],
            'citations': analysis['citations']
        })

    # Stage 4: Recent developments
    recent = perplexity_search(
        f"What are the most significant developments in {topic} in the last 6 months?",
        system_prompt="List chronologically with [Date] Event format, include citations."
    )

    return {
        'overview': overview,
        'deep_dives': player_analysis,
        'recent_developments': recent
    }
```

### Pattern: Citation-Rich Research Report

```python
def research_with_citations(query):
    """Generate research report with inline citation markers"""

    system_prompt = """
    You are a research analyst. Structure your response with inline citation markers [1], [2], etc.
    At the end, include a ## Citations section with:
    [1] Source Title - URL
    [2] Source Title - URL
    """

    result = perplexity_search(query, system_prompt)

    # Parse citations for verification
    citations = parse_citations(result['content'])

    return {
        'report': result['content'],
        'citation_urls': citations,
        'raw_citations': result.get('citations', [])
    }
```

## Claude Integration Patterns

### Pattern: Research → Claude Analysis

```python
def research_and_analyze(research_query, analysis_prompt):
    """
    Two-stage process:
    1. Perplexity gathers current data
    2. Claude analyzes and synthesizes
    """

    # Stage 1: Perplexity research
    research_result = perplexity_search(
        research_query,
        system_prompt="Provide factual, structured data with clear sections and citations."
    )

    # Save research results
    research_file = 'research_output.md'
    with open(research_file, 'w') as f:
        f.write(research_result['content'])
        f.write('\n\n## Citations\n')
        for i, citation in enumerate(research_result.get('citations', []), 1):
            f.write(f"[{i}] {citation}\n")

    # Stage 2: Claude analyzes (delegated via Task tool)
    # User (Claude): Now read research_output.md and apply analysis_prompt

    return research_file
```

### Pattern: Structured Data for Claude Processing

```python
import json

def research_to_json(query, schema_description):
    """
    Request JSON-formatted research that Claude can easily process
    """

    system_prompt = f"""
    You are a data structuring expert. Respond with ONLY valid JSON matching this schema:
    {schema_description}

    Include a 'sources' array with citation URLs.
    """

    result = perplexity_search(query, system_prompt)

    try:
        data = json.loads(result['content'])
        data['_citations'] = result.get('citations', [])
        return data
    except json.JSONDecodeError:
        # Fallback: return as text for Claude to parse
        return {
            'raw_content': result['content'],
            'citations': result.get('citations', []),
            'parse_error': True
        }
```

## Research Strategy Checklist

Before executing research with Perplexity:

- [ ] **Query Clarity**: Is the query specific enough to get actionable results?
- [ ] **Output Structure**: Have I specified the desired output format (JSON, markdown sections, list)?
- [ ] **Citation Requirements**: Am I requesting and capturing source URLs?
- [ ] **Temperature Setting**: Using low temperature (0.2) for factual research?
- [ ] **Model Selection**: Using appropriate model (sonar-large for comprehensive, sonar-small for quick checks)?
- [ ] **Iteration Plan**: Do I have a strategy if initial results are insufficient?
- [ ] **Claude Integration**: How will Claude consume and analyze these results?

## Common Use Cases

### Market Research
```python
query = "Analyze the protein-protein interaction prediction market: size, growth, key players, pricing models, and customer segments (pharmaceutical, agricultural, academic)."

system_prompt = """
Structure your response:
## Market Size and Growth
## Key Players (with product names and pricing)
## Customer Segments (needs and pain points)
## Technology Trends
## Competitive Landscape
## Sources
"""
```

### Technical Feasibility
```python
query = "What are the current approaches for deploying LLM-based agents in production? Include infrastructure options, cost estimates, and reliability patterns."

system_prompt = "Provide technical architecture patterns, vendor options with pricing, and code examples where applicable."
```

### Competitive Intelligence
```python
query = "Research Partner Project's competitors in protein interaction prediction: AlphaFold, RoseTTAFold, other commercial offerings. Compare accuracy, speed, and pricing."

system_prompt = """
For each competitor provide:
- Technology approach
- Reported accuracy metrics
- Processing speed
- Pricing model
- Target customers
- Recent updates
"""
```

### Industry Trends
```python
query = "What are the latest developments in AI-driven drug discovery from the last 3 months? Focus on protein interaction prediction and structure prediction advances."

system_prompt = "Chronological list with [Date] Event format, include company names, funding, and technical breakthroughs. Cite sources inline."
```

## Error Handling and Rate Limits

```python
import time
from functools import wraps

def retry_with_backoff(max_retries=3, base_delay=1):
    """Decorator for handling rate limits and transient errors"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 429:  # Rate limit
                        delay = base_delay * (2 ** attempt)
                        print(f"Rate limited. Retrying in {delay}s...")
                        time.sleep(delay)
                    else:
                        raise
                except requests.exceptions.RequestException as e:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(base_delay)
            raise Exception("Max retries exceeded")

        return wrapper
    return decorator

@retry_with_backoff(max_retries=3)
def robust_perplexity_search(query, system_prompt=None):
    return perplexity_search(query, system_prompt)
```

## Best Practices

1. **Query Design**: Be specific about desired format, timeframe, and depth
2. **Temperature Control**: Use 0.2 for factual research, 0.5-0.7 for creative synthesis
3. **Citation Verification**: Always capture and review source URLs
4. **Batch Operations**: Group related queries to minimize API calls
5. **Result Storage**: Save research outputs to files for Claude analysis
6. **Error Handling**: Implement retry logic for production workflows
7. **Cost Management**: Monitor API usage, use appropriate models for task complexity

## Model Selection Guide

- **llama-3.1-sonar-small-128k-online**: Quick lookups, simple queries (faster, cheaper)
- **llama-3.1-sonar-large-128k-online**: Comprehensive research, complex queries (recommended default)
- **llama-3.1-sonar-huge-128k-online**: Maximum quality for critical research (slower, expensive)

## Integration with user's Workflows

### Partner Project Market Research
```python
# Use Perplexity for current market data
market_research = research_pipeline("protein-protein interaction prediction market pharmaceutical agricultural applications")

# Save for Claude analysis
with open('partner_market_research.md', 'w') as f:
    f.write(json.dumps(market_research, indent=2))

# Claude reads and synthesizes for strategic recommendations
```

### Business Project Customer Research
```python
# Research potential customers for micro-application development
query = "Identify small to medium businesses in [industry] that need custom web applications but lack in-house development teams. Include typical pain points and budget ranges."

customer_intel = robust_perplexity_search(query, system_prompt="Structure as customer profiles with: Industry, Size, Pain Points, Budget, Decision Makers.")
```

## API Documentation

- **Perplexity API Docs**: https://docs.perplexity.ai/
- **Model Options**: https://docs.perplexity.ai/guides/model-cards
- **Pricing**: https://www.perplexity.ai/hub/pricing
