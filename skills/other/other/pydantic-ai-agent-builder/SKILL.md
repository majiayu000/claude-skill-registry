---
name: Pydantic AI Agent Builder
description: Expert guidance for building AI agents with Pydantic AI framework. Use when creating multi-agent systems, AI orchestration workflows, or structured LLM applications with type safety and validation.
version: 1.0.0
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Pydantic AI Agent Builder

Comprehensive system for building production-grade AI agents using Pydantic AI with type safety, structured outputs, and enterprise patterns.

## Core Concepts

Pydantic AI is a Python agent framework designed to make it less painful to build production-grade applications with Generative AI.

### Key Features

- **Type-safe**: Built on Pydantic for runtime validation
- **Model-agnostic**: Works with OpenAI, Anthropic, Gemini, Ollama
- **Structured outputs**: Guaranteed valid responses
- **Dependency injection**: Clean testing and modularity
- **Streaming support**: Real-time responses
- **Tool/function calling**: External integrations

## Basic Agent Patterns

### 1. Simple Agent

```python
from pydantic_ai import Agent
from pydantic import BaseModel

# Define response model
class MovieRecommendation(BaseModel):
    title: str
    year: int
    genre: str
    reason: str

# Create agent
agent = Agent(
    'openai:gpt-4o',
    result_type=MovieRecommendation,
    system_prompt='You are a movie recommendation expert.',
)

# Run agent
async def get_recommendation(preferences: str):
    result = await agent.run(preferences)
    return result.data

# Usage
recommendation = await get_recommendation("sci-fi with time travel")
print(f"{recommendation.title} ({recommendation.year})")
```

### 2. Agent with Tools

```python
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass

@dataclass
class SearchDeps:
    """Dependencies for search tools."""
    api_key: str
    database_url: str

agent = Agent(
    'anthropic:claude-3-5-sonnet-20241022',
    deps_type=SearchDeps,
    system_prompt='You are a research assistant with web search capabilities.',
)

@agent.tool
async def search_web(ctx: RunContext[SearchDeps], query: str) -> str:
    """Search the web for information."""
    # Use ctx.deps.api_key for API access
    results = await perform_search(query, ctx.deps.api_key)
    return f"Found {len(results)} results for '{query}'"

@agent.tool
async def search_database(ctx: RunContext[SearchDeps], query: str) -> list[dict]:
    """Search internal database."""
    # Use ctx.deps.database_url for DB access
    return await db_query(ctx.deps.database_url, query)

# Run with dependencies
deps = SearchDeps(
    api_key=os.getenv("SEARCH_API_KEY"),
    database_url=os.getenv("DATABASE_URL"),
)

result = await agent.run("Find information about quantum computing", deps=deps)
```

### 3. Multi-Step Agent with State

```python
from pydantic_ai import Agent
from pydantic import BaseModel, Field

class ResearchState(BaseModel):
    """Track research progress."""
    query: str
    sources_found: list[str] = Field(default_factory=list)
    summary: str = ""
    confidence: float = 0.0

class ResearchResult(BaseModel):
    """Final research output."""
    answer: str
    sources: list[str]
    confidence_score: float

agent = Agent(
    'openai:gpt-4o',
    result_type=ResearchResult,
    system_prompt='''You are a thorough researcher.
    First search for sources, then analyze them, then provide a summary.''',
)

@agent.tool
async def search_sources(ctx: RunContext[ResearchState], topic: str) -> list[str]:
    """Find relevant sources."""
    sources = await find_sources(topic)
    ctx.deps.sources_found.extend(sources)
    return sources

@agent.tool
async def analyze_source(ctx: RunContext[ResearchState], source_url: str) -> str:
    """Analyze a specific source."""
    content = await fetch_content(source_url)
    analysis = await analyze_content(content)
    return analysis

# Run research agent
state = ResearchState(query="What is quantum entanglement?")
result = await agent.run(state.query, deps=state)
```

### 4. Agent with Structured Output

```python
from pydantic_ai import Agent
from pydantic import BaseModel, Field
from typing import Literal

class CodeReview(BaseModel):
    """Structured code review output."""
    overall_quality: Literal["excellent", "good", "needs_improvement", "poor"]
    issues: list[str] = Field(description="List of identified issues")
    suggestions: list[str] = Field(description="Improvement suggestions")
    security_concerns: list[str] = Field(default_factory=list)
    performance_notes: list[str] = Field(default_factory=list)
    score: int = Field(ge=0, le=100, description="Overall score")

agent = Agent(
    'anthropic:claude-3-5-sonnet-20241022',
    result_type=CodeReview,
    system_prompt='''You are an expert code reviewer.
    Analyze code for quality, security, performance, and best practices.
    Provide actionable feedback.''',
)

async def review_code(code: str, language: str) -> CodeReview:
    prompt = f"Review this {language} code:\n\n```{language}\n{code}\n```"
    result = await agent.run(prompt)
    return result.data

# Usage
review = await review_code(open("app.py").read(), "python")
print(f"Quality: {review.overall_quality}, Score: {review.score}/100")
for issue in review.issues:
    print(f"- {issue}")
```

## Advanced Patterns

### 5. Multi-Agent System

```python
from pydantic_ai import Agent
from pydantic import BaseModel

class Task(BaseModel):
    description: str
    assigned_to: str
    status: str = "pending"

class ProjectPlan(BaseModel):
    tasks: list[Task]
    timeline: str
    risks: list[str]

# Specialized agents
architect_agent = Agent(
    'openai:gpt-4o',
    result_type=ProjectPlan,
    system_prompt='You are a technical architect. Design robust systems.',
)

developer_agent = Agent(
    'anthropic:claude-3-5-sonnet-20241022',
    result_type=str,
    system_prompt='You are a senior developer. Write clean, tested code.',
)

qa_agent = Agent(
    'openai:gpt-4o',
    result_type=list[str],
    system_prompt='You are a QA engineer. Find bugs and edge cases.',
)

# Orchestrator
class ProjectOrchestrator:
    def __init__(self):
        self.architect = architect_agent
        self.developer = developer_agent
        self.qa = qa_agent

    async def execute_project(self, requirements: str):
        # Step 1: Design
        plan_result = await self.architect.run(
            f"Create a project plan for: {requirements}"
        )
        plan = plan_result.data

        # Step 2: Implement each task
        implementations = []
        for task in plan.tasks:
            code_result = await self.developer.run(
                f"Implement: {task.description}"
            )
            implementations.append(code_result.data)

        # Step 3: QA Review
        combined_code = "\n\n".join(implementations)
        qa_result = await self.qa.run(
            f"Review this implementation:\n{combined_code}"
        )

        return {
            "plan": plan,
            "code": implementations,
            "qa_feedback": qa_result.data,
        }

# Usage
orchestrator = ProjectOrchestrator()
result = await orchestrator.execute_project(
    "Build a REST API for user management with authentication"
)
```

### 6. Agent with Streaming

```python
from pydantic_ai import Agent
import asyncio

agent = Agent('openai:gpt-4o')

async def stream_response(prompt: str):
    """Stream agent response in real-time."""
    async with agent.run_stream(prompt) as response:
        async for chunk in response.stream_text():
            print(chunk, end='', flush=True)

        # Get final result
        final = await response.get_data()
        return final

# Usage
await stream_response("Explain quantum computing in simple terms")
```

### 7. Agent with Retry Logic

```python
from pydantic_ai import Agent, ModelRetry
from pydantic import BaseModel, Field, field_validator

class ParsedData(BaseModel):
    name: str = Field(min_length=1)
    age: int = Field(ge=0, le=150)
    email: str

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v

agent = Agent(
    'openai:gpt-4o',
    result_type=ParsedData,
    retries=3,  # Retry up to 3 times on validation errors
)

@agent.result_validator
async def validate_result(ctx: RunContext, result: ParsedData) -> ParsedData:
    """Custom validation with retry."""
    if result.age < 18:
        raise ModelRetry('Age must be 18 or older. Please try again.')
    return result

# If validation fails, agent automatically retries with feedback
result = await agent.run("Extract person info: John Doe, 25, john@example.com")
```

### 8. Agent with RAG (Retrieval Augmented Generation)

```python
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
import chromadb

@dataclass
class RAGDeps:
    vector_db: chromadb.Client
    collection_name: str

agent = Agent(
    'anthropic:claude-3-5-sonnet-20241022',
    deps_type=RAGDeps,
    system_prompt='''You are a helpful assistant with access to a knowledge base.
    Always search the knowledge base before answering questions.''',
)

@agent.tool
async def search_knowledge_base(
    ctx: RunContext[RAGDeps],
    query: str,
    limit: int = 5
) -> list[str]:
    """Search vector database for relevant documents."""
    collection = ctx.deps.vector_db.get_collection(ctx.deps.collection_name)
    results = collection.query(
        query_texts=[query],
        n_results=limit,
    )
    return results['documents'][0]

# Initialize vector DB
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("knowledge_base")

# Add documents
collection.add(
    documents=["Document 1 content...", "Document 2 content..."],
    ids=["doc1", "doc2"],
)

# Run RAG agent
deps = RAGDeps(vector_db=chroma_client, collection_name="knowledge_base")
result = await agent.run("What does the documentation say about X?", deps=deps)
```

### 9. Agent with Custom Model

```python
from pydantic_ai import Agent
from pydantic_ai.models import Model, infer_model
from openai import AsyncOpenAI

# Use custom model configuration
custom_model = infer_model('openai:gpt-4o', openai_client=AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    timeout=60.0,
    max_retries=3,
))

agent = Agent(
    custom_model,
    system_prompt='You are a helpful assistant.',
)

# Or use model-specific parameters
result = await agent.run(
    "Generate a story",
    model_settings={
        'temperature': 0.9,
        'max_tokens': 2000,
        'top_p': 0.95,
    }
)
```

### 10. Agent Testing

```python
import pytest
from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel

@pytest.mark.asyncio
async def test_agent():
    """Test agent with mock model."""
    # Create test model with predefined responses
    test_model = TestModel()

    agent = Agent(test_model, result_type=str)

    # Set expected response
    test_model.agent_model_function_return = "Test response"

    result = await agent.run("Test prompt")
    assert result.data == "Test response"

    # Verify calls
    assert len(test_model.agent_model_function_calls) == 1

@pytest.mark.asyncio
async def test_agent_with_tools():
    """Test agent with mocked dependencies."""

    @dataclass
    class MockDeps:
        api_called: bool = False

    agent = Agent('test', deps_type=MockDeps)

    @agent.tool
    async def mock_api_call(ctx: RunContext[MockDeps]) -> str:
        ctx.deps.api_called = True
        return "API response"

    deps = MockDeps()
    result = await agent.run("Call the API", deps=deps)

    assert deps.api_called is True
```

## Production Patterns

### 11. Error Handling & Logging

```python
from pydantic_ai import Agent, UnexpectedModelBehavior
from pydantic import BaseModel
import logging
import structlog

# Configure structured logging
logger = structlog.get_logger()

class SafeAgent:
    def __init__(self, model: str):
        self.agent = Agent(model)

    async def run_safe(self, prompt: str) -> dict:
        """Run agent with comprehensive error handling."""
        try:
            logger.info("agent.run.start", prompt=prompt)

            result = await self.agent.run(prompt)

            logger.info(
                "agent.run.success",
                prompt=prompt,
                usage=result.usage(),
            )

            return {
                "success": True,
                "data": result.data,
                "cost": result.cost(),
            }

        except UnexpectedModelBehavior as e:
            logger.error(
                "agent.run.model_error",
                prompt=prompt,
                error=str(e),
            )
            return {"success": False, "error": "Model behavior error"}

        except Exception as e:
            logger.exception(
                "agent.run.unexpected_error",
                prompt=prompt,
            )
            return {"success": False, "error": str(e)}

# Usage
safe_agent = SafeAgent('openai:gpt-4o')
result = await safe_agent.run_safe("Complex prompt...")
```

### 12. Rate Limiting & Cost Control

```python
from pydantic_ai import Agent
import asyncio
from datetime import datetime, timedelta

class RateLimitedAgent:
    def __init__(self, model: str, max_requests_per_minute: int = 60):
        self.agent = Agent(model)
        self.max_rpm = max_requests_per_minute
        self.requests = []
        self.total_cost = 0.0
        self.max_cost = 10.0  # $10 limit

    async def run_with_limits(self, prompt: str):
        """Run agent with rate limiting and cost control."""
        # Check rate limit
        now = datetime.now()
        self.requests = [r for r in self.requests if r > now - timedelta(minutes=1)]

        if len(self.requests) >= self.max_rpm:
            wait_time = (self.requests[0] - (now - timedelta(minutes=1))).total_seconds()
            await asyncio.sleep(wait_time)

        # Check cost limit
        if self.total_cost >= self.max_cost:
            raise Exception(f"Cost limit reached: ${self.total_cost:.2f}")

        # Run agent
        result = await self.agent.run(prompt)

        # Track request and cost
        self.requests.append(datetime.now())
        cost = result.cost()
        self.total_cost += cost

        return result.data

# Usage
agent = RateLimitedAgent('openai:gpt-4o', max_requests_per_minute=50)
result = await agent.run_with_limits("Analyze this data...")
```

### 13. Agent Caching

```python
from pydantic_ai import Agent
from functools import lru_cache
import hashlib
import json

class CachedAgent:
    def __init__(self, model: str, cache_size: int = 128):
        self.agent = Agent(model)
        self.cache_size = cache_size

    @lru_cache(maxsize=128)
    async def _run_cached(self, prompt_hash: str, prompt: str):
        """Internal cached run."""
        result = await self.agent.run(prompt)
        return result.data

    async def run(self, prompt: str, use_cache: bool = True):
        """Run with optional caching."""
        if use_cache:
            prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
            return await self._run_cached(prompt_hash, prompt)
        else:
            result = await self.agent.run(prompt)
            return result.data

# Usage
cached_agent = CachedAgent('openai:gpt-4o')
result1 = await cached_agent.run("What is Python?")  # API call
result2 = await cached_agent.run("What is Python?")  # From cache
```

### 14. Prompt Management

```python
from pydantic_ai import Agent
from jinja2 import Template

class PromptLibrary:
    """Centralized prompt management."""

    PROMPTS = {
        "code_review": Template('''
            Review this {{ language }} code for:
            - Code quality and best practices
            - Security vulnerabilities
            - Performance issues
            - Maintainability

            Code:
            ```{{ language }}
            {{ code }}
            ```
        '''),

        "data_analysis": Template('''
            Analyze this dataset and provide:
            - Summary statistics
            - Key insights
            - Anomalies or patterns
            - Recommendations

            Data: {{ data }}
        '''),
    }

    @classmethod
    def render(cls, template_name: str, **kwargs) -> str:
        """Render prompt template with variables."""
        template = cls.PROMPTS.get(template_name)
        if not template:
            raise ValueError(f"Template '{template_name}' not found")
        return template.render(**kwargs)

# Usage
agent = Agent('anthropic:claude-3-5-sonnet-20241022')

prompt = PromptLibrary.render(
    "code_review",
    language="python",
    code=open("app.py").read(),
)

result = await agent.run(prompt)
```

### 15. Agent Composition

```python
from pydantic_ai import Agent
from pydantic import BaseModel

class ComposableAgent:
    """Compose multiple specialized agents."""

    def __init__(self):
        self.summarizer = Agent(
            'openai:gpt-4o',
            system_prompt='Summarize text concisely.',
        )

        self.analyzer = Agent(
            'anthropic:claude-3-5-sonnet-20241022',
            system_prompt='Analyze sentiment and key themes.',
        )

        self.translator = Agent(
            'openai:gpt-4o',
            system_prompt='Translate text accurately.',
        )

    async def process_document(self, text: str, target_language: str = None):
        """Process document through multiple agents."""
        # Step 1: Summarize
        summary_result = await self.summarizer.run(
            f"Summarize this text:\n{text}"
        )
        summary = summary_result.data

        # Step 2: Analyze
        analysis_result = await self.analyzer.run(
            f"Analyze this summary:\n{summary}"
        )
        analysis = analysis_result.data

        # Step 3: Translate if requested
        if target_language:
            translation_result = await self.translator.run(
                f"Translate to {target_language}:\n{summary}"
            )
            summary = translation_result.data

        return {
            "summary": summary,
            "analysis": analysis,
        }

# Usage
composer = ComposableAgent()
result = await composer.process_document(
    text=long_document,
    target_language="Spanish",
)
```

## Best Practices

### Type Safety
✅ Always define `result_type` for structured outputs
✅ Use Pydantic models for complex types
✅ Validate inputs with field validators
✅ Use `deps_type` for dependency injection

### Performance
✅ Implement caching for repeated queries
✅ Use streaming for long responses
✅ Set appropriate timeouts
✅ Monitor token usage and costs

### Error Handling
✅ Use `retries` parameter for transient failures
✅ Implement custom validators with `ModelRetry`
✅ Log all agent interactions
✅ Handle `UnexpectedModelBehavior` exceptions

### Testing
✅ Use `TestModel` for unit tests
✅ Mock dependencies with dataclasses
✅ Test validation logic separately
✅ Verify tool calls and responses

### Production
✅ Implement rate limiting
✅ Set cost limits and monitoring
✅ Use structured logging
✅ Version your prompts
✅ Monitor model performance

## Quick Reference

```python
# Basic agent
agent = Agent('openai:gpt-4o', result_type=MyModel)
result = await agent.run("prompt")

# Agent with tools
@agent.tool
async def my_tool(ctx: RunContext[Deps], arg: str) -> str:
    return "result"

# Agent with validation
@agent.result_validator
async def validate(ctx: RunContext, result: Model) -> Model:
    if not valid(result):
        raise ModelRetry("Try again")
    return result

# Streaming
async with agent.run_stream("prompt") as response:
    async for chunk in response.stream_text():
        print(chunk, end='')

# Custom settings
result = await agent.run(
    "prompt",
    model_settings={'temperature': 0.7},
)
```

---

**When to Use This Skill:**

Invoke when building AI agents, multi-agent systems, structured LLM applications, or when implementing type-safe AI workflows with Pydantic AI.
