---
name: learning-sdk-integration
description: Integration patterns and best practices for adding persistent memory to LLM agents using the Letta Learning SDK
---

# Learning SDK Integration

## Overview
This skill provides universal patterns for adding persistent memory to LLM agents using the Learning SDK through a 3-line integration pattern that works with OpenAI, Anthropic, Gemini, and other LLM providers.

## When to Use
Use this skill when:
- Building LLM agents that need memory across sessions
- Implementing conversation history persistence
- Adding context-aware capabilities to existing agents
- Creating multi-agent systems with shared memory
- Working with any LLM provider (OpenAI, Anthropic, Gemini, etc.)

## Core Integration Pattern

### Basic 3-Line Integration
```python
from agentic_learning import learning

# Wrap LLM SDK calls to enable memory
with learning(agent="my-agent"):
    response = openai.chat.completions.create(...)
```

### Async Integration
```python
from agentic_learning import learning_async

# For async LLM SDK usage
async with learning_async(agent="my-agent"):
    response = await claude.messages.create(...)
```

## Provider-Specific Examples

### OpenAI Integration
```python
from openai import OpenAI
from agentic_learning import learning_async

class MemoryEnhancedOpenAIAgent:
    def __init__(self, api_key: str, agent_name: str):
        self.client = OpenAI(api_key=api_key)
        self.agent_name = agent_name
    
    async def chat(self, message: str, model: str = "gpt-4"):
        async with learning_async(agent=self.agent_name):
            response = await self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": message}]
            )
            return response.choices[0].message.content
```

### Claude Integration
```python
from anthropic import Anthropic
from agentic_learning import learning_async

class MemoryEnhancedClaudeAgent:
    def __init__(self, api_key: str, agent_name: str):
        self.client = Anthropic(api_key=api_key)
        self.agent_name = agent_name
    
    async def chat(self, message: str, model: str = "claude-3-5-sonnet-20241022"):
        async with learning_async(agent=self.agent_name):
            response = await self.client.messages.create(
                model=model,
                max_tokens=1000,
                messages=[{"role": "user", "content": message}]
            )
            return response.content[0].text
```

### Gemini Integration
```python
import google.generativeai as genai
from agentic_learning import learning_async

class MemoryEnhancedGeminiAgent:
    def __init__(self, api_key: str, agent_name: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.agent_name = agent_name
    
    async def chat(self, message: str):
        async with learning_async(agent=self.agent_name):
            response = await self.model.generate_content_async(message)
            return response.text
```

### PydanticAI Integration

```python
from pydantic_ai import Agent
from agentic_learning import learning

agent = Agent('anthropic:claude-sonnet-4-20250514')

with learning(agent="pydantic-demo"):
    result = agent.run_sync("Hello!")
```

For detailed patterns including structured output, tool usage, and async examples, see `references/pydantic-ai.md`.

## Advanced Patterns

### Memory-Only Mode (Capture Without Injection)
```python
# Use capture_only=True to save conversations without memory injection
async with learning_async(agent="research-agent", capture_only=True):
    # Conversation will be saved but no memory will be retrieved/injected
    response = await llm_call(...)
```

### Custom Memory Blocks
```python
# Define custom memory blocks for specific context
custom_memory = [
    {"label": "project_context", "description": "Current project details"},
    {"label": "user_preferences", "description": "User's working preferences"}
]

async with learning_async(agent="my-agent", memory=custom_memory):
    response = await llm_call(...)
```

### Multi-Agent Memory Sharing
```python
# Multiple agents can share memory by using the same agent name
agent1 = MemoryEnhancedOpenAIAgent(api_key, "shared-agent")
agent2 = MemoryEnhancedClaudeAgent(api_key, "shared-agent")

# Both agents will access the same memory context
response1 = await agent1.chat("Research topic X")
response2 = await agent2.chat("Summarize our research")
```

### Context-Aware Tool Selection
```python
async def context_aware_tool_use():
    async with learning_async(agent="tool-selector"):
        # Memory will help agent choose appropriate tools
        memories = await get_memories("tool-selector")
        
        if "web_search_needed" in str(memories):
            return use_web_search()
        elif "data_analysis" in str(memories):
            return use_data_tools()
        else:
            return use_default_tools()
```

## Best Practices

### 1. Agent Naming
- Use descriptive agent names that reflect their purpose
- For related functionality, use consistent naming patterns
- Example: `email-processor`, `research-assistant`, `code-reviewer`

### 2. Memory Structure
```python
# Good: Specific, purposeful memory blocks
memory_blocks = [
    {"label": "conversation_history", "description": "Recent conversation context"},
    {"label": "task_context", "description": "Current task and goals"},
    {"label": "user_preferences", "description": "User interaction preferences"}
]
```

### 3. Error Handling
```python
async def robust_llm_call(message: str):
    try:
        async with learning_async(agent="my-agent"):
            return await llm_sdk_call(...)
    except Exception as e:
        # Fallback without memory if learning fails
        return await llm_sdk_call(...)
```

### 4. Provider Selection Patterns
```python
def choose_provider(task_type: str, budget: str, latency_requirement: str):
    """Select LLM provider based on task requirements"""
    
    if task_type == "code_generation" and budget == "high":
        return "claude-3-5-sonnet"  # Best for code
    elif task_type == "general_chat" and budget == "low":
        return "gpt-3.5-turbo"  # Cost-effective
    elif latency_requirement == "ultra_low":
        return "gemini-1.5-flash"  # Fastest
    else:
        return "gpt-4"  # Good all-rounder
```

## Memory Management

### Retrieving Conversation History
```python
from agentic_learning import AsyncAgenticLearning

async def get_conversation_context(agent_name: str):
    client = AsyncAgenticLearning()
    memories = await client.get_memories(agent_name)
    return memories
```

### Clearing Memory
```python
# When starting fresh contexts
client = AsyncAgenticLearning()
await client.clear_memory(agent_name)
```

## Integration Examples

### Universal Research Agent
```python
class UniversalResearchAgent:
    def __init__(self, provider: str, api_key: str):
        self.provider = provider
        self.client = self._initialize_client(provider, api_key)
    
    def _initialize_client(self, provider: str, api_key: str):
        if provider == "openai":
            from openai import OpenAI
            return OpenAI(api_key=api_key)
        elif provider == "claude":
            from anthropic import Anthropic
            return Anthropic(api_key=api_key)
        elif provider == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            return genai.GenerativeModel('gemini-pro')
    
    async def research(self, topic: str):
        async with learning_async(
            agent="universal-researcher",
            memory=[
                {"label": "research_history", "description": "Previous research topics"},
                {"label": "current_session", "description": "Current research session"}
            ]
        ):
            prompt = f"Research the topic: {topic}. Consider previous research context."
            response = await self._make_llm_call(prompt)
            return response
```

### Multi-Provider Code Review Assistant
```python
class CodeReviewAssistant:
    def __init__(self, providers: dict):
        self.providers = providers
        self.clients = {name: self._init_client(name, key) 
                       for name, key in providers.items()}
    
    async def review_with_multiple_perspectives(self, code: str):
        reviews = {}
        
        for provider_name, client in self.clients.items():
            async with learning_async(
                agent=f"code-reviewer-{provider_name}",
                memory=[
                    {"label": "review_history", "description": "Past code reviews"},
                    {"label": "coding_standards", "description": "Project standards"}
                ]
            ):
                prompt = f"Review this code from {provider_name} perspective: {code}"
                reviews[provider_name] = await self._make_llm_call(client, prompt)
        
        # Synthesize multiple perspectives
        return await self._synthesize_reviews(reviews)
```

## Testing Integration

### Unit Test Pattern
```python
import pytest
from agentic_learning import learning_async

async def test_memory_integration():
    async with learning_async(agent="test-agent"):
        # Test that memory is working
        response = await llm_sdk_call("Remember this test")
        
        # Verify memory was captured
        client = AsyncAgenticLearning()
        memories = await client.get_memories("test-agent")
        assert len(memories) > 0

@pytest.mark.parametrize("provider", ["openai", "claude", "gemini"])
async def test_provider_memory_integration(provider):
    # Test memory works with each provider
    agent = create_agent(provider, api_key)
    response = await agent.chat("Test message")
    assert response is not None
```

## Troubleshooting

### Common Issues
1. **Memory not appearing**: Ensure agent name is consistent across calls
2. **Performance issues**: Use `capture_only=True` for logging-only scenarios
3. **Context overflow**: Regularly clear memory for long-running sessions
4. **Async conflicts**: Always use `learning_async` with async SDK calls
5. **Provider compatibility**: Check SDK version compatibility with Agentic Learning SDK

### Debug Mode
```python
# Enable debug logging to see memory operations
import logging
logging.basicConfig(level=logging.DEBUG)

async with learning_async(agent="debug-agent"):
    # Memory operations will be logged
    response = await llm_sdk_call(...)
```

## Provider-Specific Considerations

### OpenAI
- Works best with `chat.completions` endpoint
- Supports both sync and async clients
- Token counting available for cost tracking

### Claude
- Use `messages` endpoint for conversation
- Handles long context well
- Good for code and analysis tasks

### Gemini
- Use `generate_content_async` for async
- Supports multimodal inputs
- Fast response times

## References

- [Learning SDK Documentation](https://github.com/letta-ai/learning-sdk)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python)
- [Google AI Python SDK](https://github.com/google/generative-ai-python)

### Skill References

- `references/pydantic-ai.md` - PydanticAI integration patterns
- `references/mem0-migration.md` - Migrating from mem0 to Learning SDK