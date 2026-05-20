---
name: llmintegration
description: LLM integration patterns for Claude, GPT, Gemini, and Ollama. Activate for AI API integration, prompt engineering, token management, extended thinking, and multi-model orchestration.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
related-skills:
  - extended-thinking
  - complex-reasoning
  - deep-analysis
---

# LLM Integration Skill

Provides comprehensive LLM integration capabilities for the Golden Armada AI Agent Fleet Platform, including advanced features like extended thinking, sophisticated prompt engineering, and intelligent token budget management.

## When to Use This Skill

Activate this skill when working with:
- Claude/Anthropic API integration
- OpenAI GPT integration
- Google Gemini integration
- Ollama local models
- Multi-model orchestration
- Prompt engineering

## Anthropic Claude Integration

\`\`\`python
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# Basic completion
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)
print(message.content[0].text)

# With system prompt
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="You are a helpful coding assistant.",
    messages=[
        {"role": "user", "content": "Write a Python function to sort a list."}
    ]
)

# Streaming
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Tell me a story."}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

# Tool use
tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather in a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "The city and state"}
            },
            "required": ["location"]
        }
    }
]

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in San Francisco?"}]
)
\`\`\`

## OpenAI GPT Integration

\`\`\`python
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Basic completion
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)
print(response.choices[0].message.content)

# Streaming
stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Write a poem."}],
    stream=True
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")

# Function calling
functions = [
    {
        "name": "get_weather",
        "description": "Get the current weather",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            },
            "required": ["location"]
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Weather in NYC?"}],
    functions=functions,
    function_call="auto"
)
\`\`\`

## Google Gemini Integration

\`\`\`python
import google.generativeai as genai

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel('gemini-pro')

# Basic generation
response = model.generate_content("Explain quantum computing")
print(response.text)

# Chat
chat = model.start_chat(history=[])
response = chat.send_message("Hello!")
print(response.text)

# Streaming
response = model.generate_content("Tell me a story", stream=True)
for chunk in response:
    print(chunk.text, end="")
\`\`\`

## Ollama Local Models

\`\`\`python
import ollama

# Basic completion
response = ollama.chat(
    model='llama2',
    messages=[
        {'role': 'user', 'content': 'Hello!'}
    ]
)
print(response['message']['content'])

# Streaming
stream = ollama.chat(
    model='llama2',
    messages=[{'role': 'user', 'content': 'Tell me a story.'}],
    stream=True
)
for chunk in stream:
    print(chunk['message']['content'], end='')

# Pull model
ollama.pull('llama2')

# List models
models = ollama.list()
\`\`\`

## Multi-Model Abstraction

\`\`\`python
from abc import ABC, abstractmethod
from typing import Generator

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        pass

    @abstractmethod
    def stream(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        pass

class ClaudeProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def generate(self, prompt: str, **kwargs) -> str:
        message = self.client.messages.create(
            model=self.model,
            max_tokens=kwargs.get('max_tokens', 1024),
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text

    def stream(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        with self.client.messages.stream(
            model=self.model,
            max_tokens=kwargs.get('max_tokens', 1024),
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            for text in stream.text_stream:
                yield text

class LLMFactory:
    @staticmethod
    def create(provider: str, **kwargs) -> LLMProvider:
        providers = {
            'claude': ClaudeProvider,
            'gpt': GPTProvider,
            'gemini': GeminiProvider,
            'ollama': OllamaProvider
        }
        return providers[provider](**kwargs)
\`\`\`

## Prompt Engineering Best Practices

\`\`\`python
# Structured prompts
SYSTEM_PROMPT = """You are a helpful coding assistant.

Guidelines:
1. Write clean, well-documented code
2. Follow best practices
3. Explain your reasoning
"""

# Few-shot examples
FEW_SHOT_PROMPT = """Convert natural language to SQL.

Example 1:
Input: Get all users
Output: SELECT * FROM users;

Example 2:
Input: Count active orders
Output: SELECT COUNT(*) FROM orders WHERE status = 'active';

Input: {user_input}
Output:"""

# Chain of thought
COT_PROMPT = """Solve this step by step:
{problem}

Let's think through this:
1."""
\`\`\`

## Extended Thinking Integration

Extended thinking enables Claude models to "think" before responding, improving accuracy on complex tasks like coding, math, and scientific reasoning.

### When to Use Extended Thinking

- Complex multi-step reasoning tasks
- Code architecture and system design
- Mathematical problem-solving
- Scientific analysis and research
- Strategic planning and decision-making

**Cross-reference:** See `.claude/skills/extended-thinking/SKILL.md` for detailed guidance.

### Basic Extended Thinking

\`\`\`python
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# Enable extended thinking (Claude Sonnet 4 and Opus 4)
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000  # Reserve tokens for thinking
    },
    messages=[
        {
            "role": "user",
            "content": "Design a scalable microservices architecture for a multi-tenant SaaS platform"
        }
    ]
)

# Response includes thinking and final text
for block in response.content:
    if block.type == "thinking":
        print(f"Thinking: {block.thinking}")
    elif block.type == "text":
        print(f"Response: {block.text}")
\`\`\`

### Extended Thinking with Streaming

\`\`\`python
# Stream thinking process in real-time
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000
    },
    messages=[
        {"role": "user", "content": "Analyze the time complexity of this sorting algorithm..."}
    ]
) as stream:
    for event in stream:
        if event.type == "content_block_start":
            if event.content_block.type == "thinking":
                print("\n[Thinking Process]")
            elif event.content_block.type == "text":
                print("\n[Final Answer]")
        elif event.type == "content_block_delta":
            if event.delta.type == "thinking_delta":
                print(event.delta.thinking, end="", flush=True)
            elif event.delta.type == "text_delta":
                print(event.delta.text, end="", flush=True)
\`\`\`

### Multi-Provider Extended Thinking Abstraction

\`\`\`python
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class ThinkingConfig:
    enabled: bool = False
    budget_tokens: Optional[int] = None
    show_thinking: bool = True

class ExtendedThinkingProvider:
    """Abstract extended thinking across providers"""

    def __init__(self, provider: str, config: ThinkingConfig):
        self.provider = provider
        self.config = config

    def generate_with_thinking(self, prompt: str, **kwargs) -> Dict[str, Any]:
        if self.provider == "claude":
            return self._claude_thinking(prompt, **kwargs)
        elif self.provider == "gpt":
            # Simulate thinking with chain-of-thought
            return self._gpt_cot_thinking(prompt, **kwargs)
        else:
            raise ValueError(f"Provider {self.provider} doesn't support extended thinking")

    def _claude_thinking(self, prompt: str, **kwargs) -> Dict[str, Any]:
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

        thinking_params = {}
        if self.config.enabled:
            thinking_params["thinking"] = {
                "type": "enabled",
                "budget_tokens": self.config.budget_tokens or 10000
            }

        response = client.messages.create(
            model=kwargs.get("model", "claude-sonnet-4-20250514"),
            max_tokens=kwargs.get("max_tokens", 16000),
            messages=[{"role": "user", "content": prompt}],
            **thinking_params
        )

        result = {"thinking": None, "response": None}
        for block in response.content:
            if block.type == "thinking":
                result["thinking"] = block.thinking
            elif block.type == "text":
                result["response"] = block.text

        return result

    def _gpt_cot_thinking(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Use chain-of-thought prompting for GPT models"""
        from openai import OpenAI
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

        cot_prompt = f"""Let's approach this step-by-step:

{prompt}

First, think through the problem systematically, then provide your final answer."""

        response = client.chat.completions.create(
            model=kwargs.get("model", "gpt-4"),
            messages=[{"role": "user", "content": cot_prompt}]
        )

        # Parse thinking from response (heuristic-based)
        content = response.choices[0].message.content
        parts = content.split("\n\n")

        return {
            "thinking": "\n\n".join(parts[:-1]) if len(parts) > 1 else None,
            "response": parts[-1] if parts else content
        }

# Usage
thinking_provider = ExtendedThinkingProvider(
    provider="claude",
    config=ThinkingConfig(enabled=True, budget_tokens=8000)
)

result = thinking_provider.generate_with_thinking(
    "Design a distributed caching strategy for a multi-tenant system"
)

if result["thinking"]:
    print(f"Thinking Process:\n{result['thinking']}\n")
print(f"Final Answer:\n{result['response']}")
\`\`\`

## Claude Prompt Engineering Best Practices

Based on Anthropic's official guidelines for optimal performance.

### 1. Clear and Direct Instructions

\`\`\`python
# BAD: Vague request
prompt = "Make this code better"

# GOOD: Specific instructions
prompt = """Refactor this Python function to:
1. Use type hints
2. Add comprehensive docstrings
3. Handle edge cases (empty input, None values)
4. Improve variable naming for clarity
5. Add input validation

Code:
{code}
"""
\`\`\`

### 2. Use XML Tags for Structure

\`\`\`python
# XML tags help Claude parse complex inputs
prompt = """Analyze this codebase and identify security vulnerabilities.

<codebase>
<file path="auth.py">
{auth_code}
</file>
<file path="api.py">
{api_code}
</file>
</codebase>

<requirements>
- Focus on authentication and authorization issues
- Check for SQL injection vulnerabilities
- Identify improper input validation
- Flag missing rate limiting
</requirements>

Provide output in this format:
<vulnerability>
<severity>High|Medium|Low</severity>
<file>path/to/file.py</file>
<line>123</line>
<description>Clear description</description>
<recommendation>How to fix</recommendation>
</vulnerability>
"""
\`\`\`

### 3. Provide Examples (Few-Shot Prompting)

\`\`\`python
FEW_SHOT_TEMPLATE = """Convert user stories to acceptance criteria.

<example>
<user_story>
As a user, I want to reset my password so that I can regain access to my account.
</user_story>
<acceptance_criteria>
- Given I'm on the login page
- When I click "Forgot Password"
- Then I should see a password reset form
- And I should receive a reset link via email
- And the link should expire after 1 hour
- And I can set a new password using the link
</acceptance_criteria>
</example>

<example>
<user_story>
As an admin, I want to export user data so that I can generate reports.
</user_story>
<acceptance_criteria>
- Given I'm logged in as admin
- When I navigate to Users > Export
- Then I should see export format options (CSV, JSON, Excel)
- And I should be able to filter by date range
- And the export should include all user fields
- And I should receive a download link within 5 minutes
</acceptance_criteria>
</example>

Now convert this user story:
<user_story>
{user_input}
</user_story>
"""
\`\`\`

### 4. Assign Roles for Context

\`\`\`python
ROLE_BASED_SYSTEM_PROMPTS = {
    "code_reviewer": """You are an expert code reviewer with 15 years of experience.
Your expertise includes:
- Software architecture and design patterns
- Security best practices (OWASP Top 10)
- Performance optimization
- Code maintainability and readability

When reviewing code:
1. Identify bugs and potential issues
2. Suggest improvements for clarity and performance
3. Check for security vulnerabilities
4. Recommend design pattern improvements
5. Ensure code follows language best practices

Be constructive and specific in your feedback.""",

    "architect": """You are a senior software architect specializing in:
- Microservices and distributed systems
- Cloud-native architecture (AWS, GCP, Azure)
- Database design and optimization
- API design (REST, GraphQL, gRPC)
- Security and compliance

When designing systems:
1. Consider scalability and performance
2. Ensure fault tolerance and resilience
3. Design for observability (logging, metrics, tracing)
4. Follow cloud-native best practices
5. Consider cost optimization""",

    "security_expert": """You are a security specialist focused on:
- OWASP Top 10 vulnerabilities
- Authentication and authorization (OAuth, OIDC, JWT)
- Data encryption and privacy
- Secure coding practices
- Compliance (GDPR, HIPAA, SOC2)

When analyzing security:
1. Identify vulnerabilities with severity ratings
2. Provide specific remediation steps
3. Reference security standards and best practices
4. Consider both code-level and architectural security"""
}

# Usage
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    system=ROLE_BASED_SYSTEM_PROMPTS["code_reviewer"],
    messages=[
        {"role": "user", "content": f"Review this code:\n\n{code}"}
    ]
)
\`\`\`

### 5. Chain of Thought Prompting

\`\`\`python
COT_PROMPT = """Solve this problem step by step, showing your reasoning at each stage.

Problem: {problem}

Think through this by:
1. Understanding what's being asked
2. Identifying relevant information
3. Breaking down the problem into steps
4. Solving each step
5. Verifying the solution

Show your work for each step."""

# For complex reasoning, combine with extended thinking
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    messages=[
        {"role": "user", "content": COT_PROMPT.format(problem=complex_problem)}
    ]
)
\`\`\`

### 6. Prefill Responses for Format Control

\`\`\`python
# Force JSON output by prefilling assistant response
messages = [
    {"role": "user", "content": "Extract entities from: 'Apple Inc. hired John Smith as CEO in 2023.'"},
    {"role": "assistant", "content": "{"}  # Prefill to force JSON
]

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=messages
)

# Claude will complete the JSON starting with "{"
json_output = "{" + response.content[0].text
\`\`\`

### 7. Long Context Best Practices

\`\`\`python
# For Claude's 200k token context window
LONG_CONTEXT_TEMPLATE = """I'm providing a large codebase for analysis.
The most important files for this task are at the END of this message.

<codebase>
{less_important_files}
</codebase>

<critical_files>
{important_files}
</critical_files>

<task>
{specific_question}
</task>

Focus primarily on the critical files when answering the task."""
\`\`\`

## Token Budget Management

### Anthropic Token Counting

\`\`\`python
import anthropic

def count_tokens_anthropic(text: str, model: str = "claude-sonnet-4-20250514") -> int:
    """Count tokens using Anthropic's API"""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    # Use count_tokens endpoint
    result = client.messages.count_tokens(
        model=model,
        messages=[{"role": "user", "content": text}]
    )

    return result.input_tokens

def count_tokens_with_system(messages: list, system: str = None, model: str = "claude-sonnet-4-20250514") -> dict:
    """Count tokens including system prompt and messages"""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    params = {
        "model": model,
        "messages": messages
    }
    if system:
        params["system"] = system

    result = client.messages.count_tokens(**params)

    return {
        "input_tokens": result.input_tokens,
        "system_tokens": getattr(result, "system_tokens", 0)
    }
\`\`\`

### Smart Token Budget Management

\`\`\`python
from typing import List, Dict
import anthropic

class TokenBudgetManager:
    """Intelligent token budget management for LLM calls"""

    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        self.model = model
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

        # Model-specific limits
        self.limits = {
            "claude-opus-4-20250514": {"context": 200000, "output": 16384},
            "claude-sonnet-4-20250514": {"context": 200000, "output": 16384},
            "claude-haiku-3-5-20250514": {"context": 200000, "output": 8192},
        }

    def get_budget(self, model: str = None) -> Dict[str, int]:
        """Get token limits for model"""
        model = model or self.model
        return self.limits.get(model, {"context": 200000, "output": 16384})

    def check_budget(
        self,
        messages: List[Dict],
        system: str = None,
        max_tokens: int = 4096,
        thinking_tokens: int = 0
    ) -> Dict[str, any]:
        """Check if request fits within budget"""

        # Count input tokens
        token_count = self.client.messages.count_tokens(
            model=self.model,
            messages=messages,
            system=system
        )

        input_tokens = token_count.input_tokens
        budget = self.get_budget()

        # Calculate total required tokens
        total_required = input_tokens + max_tokens + thinking_tokens

        return {
            "fits_budget": total_required <= budget["context"],
            "input_tokens": input_tokens,
            "requested_output": max_tokens,
            "thinking_budget": thinking_tokens,
            "total_required": total_required,
            "context_limit": budget["context"],
            "remaining": budget["context"] - total_required,
            "utilization_pct": (total_required / budget["context"]) * 100
        }

    def optimize_for_budget(
        self,
        messages: List[Dict],
        system: str = None,
        target_output: int = 4096,
        thinking_tokens: int = 0,
        priority_last_n: int = 3
    ) -> List[Dict]:
        """Truncate messages to fit budget, preserving recent context"""

        budget = self.get_budget()
        available = budget["context"] - target_output - thinking_tokens

        # Always keep system prompt and last N messages
        preserved_messages = messages[-priority_last_n:]

        # Count tokens for preserved content
        preserved_count = self.client.messages.count_tokens(
            model=self.model,
            messages=preserved_messages,
            system=system
        ).input_tokens

        if preserved_count <= available:
            # Try to include earlier messages
            remaining = available - preserved_count
            earlier_messages = messages[:-priority_last_n]

            # Binary search to find how many earlier messages fit
            left, right = 0, len(earlier_messages)
            best_fit = 0

            while left <= right:
                mid = (left + right) // 2
                test_messages = earlier_messages[-mid:] + preserved_messages

                test_count = self.client.messages.count_tokens(
                    model=self.model,
                    messages=test_messages,
                    system=system
                ).input_tokens

                if test_count <= available:
                    best_fit = mid
                    left = mid + 1
                else:
                    right = mid - 1

            return earlier_messages[-best_fit:] + preserved_messages if best_fit > 0 else preserved_messages
        else:
            # Even preserved messages exceed budget, truncate them
            return preserved_messages[-1:]  # Keep at least the last message

    def get_recommendations(self, budget_check: Dict) -> List[str]:
        """Get recommendations based on budget utilization"""
        recommendations = []

        util = budget_check["utilization_pct"]

        if util > 90:
            recommendations.append("CRITICAL: Token usage >90%. Consider reducing context or output length.")
            recommendations.append("Enable extended thinking only if necessary for task complexity.")
        elif util > 75:
            recommendations.append("WARNING: Token usage >75%. Monitor context size.")
            recommendations.append("Consider summarizing earlier conversation turns.")
        elif util > 50:
            recommendations.append("Moderate token usage. Budget healthy.")
        else:
            recommendations.append("Low token usage. Budget has plenty of headroom.")

        if budget_check["thinking_budget"] > budget_check["requested_output"]:
            recommendations.append("Thinking budget exceeds output budget. Ensure this is intentional.")

        return recommendations

# Usage example
manager = TokenBudgetManager(model="claude-sonnet-4-20250514")

messages = [
    {"role": "user", "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a high-level programming language..."},
    {"role": "user", "content": "Write a complex microservices architecture"}
]

system = "You are an expert software architect."

# Check budget
budget_check = manager.check_budget(
    messages=messages,
    system=system,
    max_tokens=8192,
    thinking_tokens=10000
)

print(f"Fits budget: {budget_check['fits_budget']}")
print(f"Utilization: {budget_check['utilization_pct']:.1f}%")
print(f"Remaining tokens: {budget_check['remaining']}")

# Get recommendations
for rec in manager.get_recommendations(budget_check):
    print(f"- {rec}")

# Optimize if needed
if not budget_check["fits_budget"]:
    optimized_messages = manager.optimize_for_budget(
        messages=messages,
        system=system,
        target_output=8192,
        thinking_tokens=10000
    )
    print(f"Reduced from {len(messages)} to {len(optimized_messages)} messages")
\`\`\`

### OpenAI Token Counting

\`\`\`python
import tiktoken

def count_tokens_openai(text: str, model: str = "gpt-4") -> int:
    """Count tokens for OpenAI models"""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def truncate_to_token_limit(text: str, max_tokens: int, model: str = "gpt-4") -> str:
    """Truncate text to fit token limit"""
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    if len(tokens) <= max_tokens:
        return text
    return encoding.decode(tokens[:max_tokens])

def split_by_tokens(text: str, chunk_size: int, model: str = "gpt-4") -> List[str]:
    """Split text into chunks of specific token size"""
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)

    chunks = []
    for i in range(0, len(tokens), chunk_size):
        chunk_tokens = tokens[i:i + chunk_size]
        chunks.append(encoding.decode(chunk_tokens))

    return chunks
\`\`\`

## Cross-References and Related Skills

### Extended Thinking
For complex reasoning tasks requiring deep analysis:
- **Skill:** `.claude/skills/extended-thinking/SKILL.md`
- **Use when:** Multi-step reasoning, architecture design, mathematical proofs

### Complex Reasoning
For advanced problem-solving and analysis:
- **Skill:** `.claude/skills/complex-reasoning/SKILL.md`
- **Use when:** System design, optimization problems, strategic planning

### Deep Analysis
For comprehensive codebase and system analysis:
- **Skill:** `.claude/skills/deep-analysis/SKILL.md`
- **Use when:** Code review, security audits, performance analysis

### Orchestration Integration

When using LLM integration within the Golden Armada orchestration system:

\`\`\`python
from orchestration.agent_activity_logger import AgentActivityLogger

# Log LLM API calls for tracking
logger = AgentActivityLogger()

logger.log_activity(
    agent_name="code-reviewer",
    activity_type="llm_api_call",
    details={
        "provider": "anthropic",
        "model": "claude-sonnet-4-20250514",
        "input_tokens": 1500,
        "output_tokens": 800,
        "thinking_tokens": 3000,
        "extended_thinking": True,
        "task": "security_audit"
    }
)
\`\`\`

## Model Selection Guide

### Claude Models

| Model | Best For | Context | Output | Cost |
|-------|----------|---------|--------|------|
| **Opus 4** | Complex reasoning, architecture design | 200K | 16K | Highest |
| **Sonnet 4** | General development, balanced performance | 200K | 16K | Medium |
| **Haiku 3.5** | Fast tasks, simple queries, high throughput | 200K | 8K | Lowest |

**Extended Thinking:** Only available on Sonnet 4 and Opus 4

### When to Use Each Model

\`\`\`python
MODEL_SELECTION = {
    "strategic_planning": "claude-opus-4-20250514",
    "system_architecture": "claude-opus-4-20250514",
    "complex_debugging": "claude-sonnet-4-20250514",
    "code_review": "claude-sonnet-4-20250514",
    "code_generation": "claude-sonnet-4-20250514",
    "documentation": "claude-haiku-3-5-20250514",
    "simple_queries": "claude-haiku-3-5-20250514",
    "batch_processing": "claude-haiku-3-5-20250514"
}

def select_model(task_type: str, use_thinking: bool = False) -> str:
    """Select appropriate model based on task"""
    model = MODEL_SELECTION.get(task_type, "claude-sonnet-4-20250514")

    # Ensure model supports extended thinking if requested
    if use_thinking and "haiku" in model:
        model = "claude-sonnet-4-20250514"

    return model
\`\`\`

## Performance Optimization Tips

### 1. Prompt Caching (Reduce Costs)

\`\`\`python
# Cache large system prompts or context
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    system=[
        {
            "type": "text",
            "text": large_system_prompt,
            "cache_control": {"type": "ephemeral"}  # Cache this
        }
    ],
    messages=[
        {"role": "user", "content": "Question about the system"}
    ]
)
\`\`\`

### 2. Batch Processing

\`\`\`python
async def process_batch(items: List[str], batch_size: int = 10):
    """Process items in batches to avoid rate limits"""
    import asyncio

    async def process_item(item: str):
        # Async LLM call
        return await async_llm_call(item)

    results = []
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        batch_results = await asyncio.gather(*[process_item(item) for item in batch])
        results.extend(batch_results)

        # Rate limiting
        if i + batch_size < len(items):
            await asyncio.sleep(1)

    return results
\`\`\`

### 3. Streaming for Responsiveness

\`\`\`python
# Always use streaming for long-running tasks
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=8192,
    messages=[{"role": "user", "content": complex_task}]
) as stream:
    for text in stream.text_stream:
        yield text  # Stream to UI or process incrementally
\`\`\`
