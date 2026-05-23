---
name: claude-agent-sdk
version: 1.0.0
description: Build custom AI agents using Anthropic Claude API and agent SDK patterns. Create tool-using agents, multi-turn conversations, agent loops, streaming responses, and production-ready agent architectures. Use when building Claude-powered applications, implementing agentic AI features, or developing autonomous task completion systems.
---

# Claude Agent SDK: Building AI Agents with Claude

Build production-ready AI agents using Claude API patterns for tool use, multi-turn conversations, and autonomous task completion.

## Triggers

Use this skill when:
- Building Claude-powered AI applications
- Implementing tool-using agents
- Creating multi-turn conversation systems
- Developing autonomous task completion
- Building agentic features with Claude
- Keywords: claude api, anthropic, agent sdk, tool use, function calling, claude agent, ai agent, autonomous

## Core Concepts

### Claude API Fundamentals

```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

# Basic message
response = client.messages.create(
    model="claude-opus-4-5-20251101",
    max_tokens=4096,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)
```

### Model Selection

| Model | Use Case | Context | Speed |
|-------|----------|---------|-------|
| claude-opus-4-5-20251101 | Complex reasoning, coding | 200K | Slower |
| claude-sonnet-4-20250514 | Balanced performance | 200K | Medium |
| claude-haiku-3-5-20241022 | Fast responses, simple tasks | 200K | Fast |

---

## Pattern 1: Tool-Using Agent

### Define Tools

```python
tools = [
    {
        "name": "search_codebase",
        "description": "Search the codebase for files matching a pattern or containing specific text",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query (file pattern or text to find)"
                },
                "search_type": {
                    "type": "string",
                    "enum": ["filename", "content"],
                    "description": "Type of search to perform"
                }
            },
            "required": ["query", "search_type"]
        }
    },
    {
        "name": "read_file",
        "description": "Read the contents of a file",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to the file to read"
                }
            },
            "required": ["path"]
        }
    },
    {
        "name": "write_file",
        "description": "Write content to a file",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to write to"
                },
                "content": {
                    "type": "string",
                    "description": "Content to write"
                }
            },
            "required": ["path", "content"]
        }
    }
]
```

### Agent Loop

```python
def agent_loop(task: str, tools: list, max_iterations: int = 10):
    messages = [{"role": "user", "content": task}]

    for _ in range(max_iterations):
        response = client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )

        # Check if done
        if response.stop_reason == "end_turn":
            return extract_text_response(response)

        # Process tool calls
        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = execute_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            # Add assistant response and tool results
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

    return "Max iterations reached"
```

### Tool Execution

```python
def execute_tool(name: str, inputs: dict) -> str:
    if name == "search_codebase":
        return search_codebase(inputs["query"], inputs["search_type"])
    elif name == "read_file":
        return read_file(inputs["path"])
    elif name == "write_file":
        write_file(inputs["path"], inputs["content"])
        return f"Successfully wrote to {inputs['path']}"
    else:
        return f"Unknown tool: {name}"
```

---

## Pattern 2: Streaming Agent

### Stream Responses

```python
def streaming_agent(task: str, tools: list):
    messages = [{"role": "user", "content": task}]

    while True:
        with client.messages.stream(
            model="claude-opus-4-5-20251101",
            max_tokens=4096,
            tools=tools,
            messages=messages
        ) as stream:
            response = None
            for event in stream:
                if event.type == "content_block_delta":
                    if event.delta.type == "text_delta":
                        print(event.delta.text, end="", flush=True)

            response = stream.get_final_message()

        if response.stop_reason == "end_turn":
            break

        if response.stop_reason == "tool_use":
            # Process tools (same as above)
            tool_results = process_tool_calls(response)
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
```

### Event Types

| Event Type | Description |
|------------|-------------|
| `message_start` | Message begins |
| `content_block_start` | New content block |
| `content_block_delta` | Content chunk |
| `content_block_stop` | Block complete |
| `message_delta` | Message metadata |
| `message_stop` | Message complete |

---

## Pattern 3: Multi-Turn Conversation

### Conversation Manager

```python
class ConversationManager:
    def __init__(self, system_prompt: str = None):
        self.messages = []
        self.system_prompt = system_prompt

    def add_user_message(self, content: str):
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str):
        self.messages.append({"role": "assistant", "content": content})

    def get_response(self, user_input: str) -> str:
        self.add_user_message(user_input)

        kwargs = {
            "model": "claude-opus-4-5-20251101",
            "max_tokens": 4096,
            "messages": self.messages
        }

        if self.system_prompt:
            kwargs["system"] = self.system_prompt

        response = client.messages.create(**kwargs)

        assistant_text = extract_text(response)
        self.add_assistant_message(assistant_text)

        return assistant_text

    def reset(self):
        self.messages = []
```

### With Memory Summarization

```python
class ConversationWithMemory(ConversationManager):
    def __init__(self, max_messages: int = 20):
        super().__init__()
        self.max_messages = max_messages

    def get_response(self, user_input: str) -> str:
        # Summarize if too long
        if len(self.messages) > self.max_messages:
            self._summarize_history()

        return super().get_response(user_input)

    def _summarize_history(self):
        # Keep last few messages
        recent = self.messages[-4:]

        # Summarize older messages
        older = self.messages[:-4]
        summary = self._create_summary(older)

        # Replace with summary + recent
        self.messages = [
            {"role": "user", "content": f"[Previous conversation summary: {summary}]"},
            {"role": "assistant", "content": "I understand the context from our previous discussion."}
        ] + recent
```

---

## Pattern 4: Structured Output

### JSON Mode with Schema

```python
from pydantic import BaseModel
from typing import List

class TaskAnalysis(BaseModel):
    summary: str
    complexity: str  # "simple", "moderate", "complex"
    steps: List[str]
    estimated_time: str
    dependencies: List[str]

def analyze_task(task: str) -> TaskAnalysis:
    response = client.messages.create(
        model="claude-opus-4-5-20251101",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": f"""Analyze this task and respond with JSON matching this schema:
{{
    "summary": "brief summary",
    "complexity": "simple|moderate|complex",
    "steps": ["step 1", "step 2"],
    "estimated_time": "time estimate",
    "dependencies": ["dep 1", "dep 2"]
}}

Task: {task}"""
        }]
    )

    # Parse JSON from response
    json_str = extract_json(response.content[0].text)
    return TaskAnalysis.model_validate_json(json_str)
```

### With Tool for Structured Output

```python
analysis_tool = {
    "name": "submit_analysis",
    "description": "Submit the task analysis",
    "input_schema": {
        "type": "object",
        "properties": {
            "summary": {"type": "string"},
            "complexity": {"type": "string", "enum": ["simple", "moderate", "complex"]},
            "steps": {"type": "array", "items": {"type": "string"}},
            "estimated_time": {"type": "string"},
            "dependencies": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["summary", "complexity", "steps", "estimated_time"]
    }
}

response = client.messages.create(
    model="claude-opus-4-5-20251101",
    max_tokens=4096,
    tools=[analysis_tool],
    tool_choice={"type": "tool", "name": "submit_analysis"},
    messages=[{"role": "user", "content": f"Analyze: {task}"}]
)

# Extract structured data from tool call
tool_input = response.content[0].input
```

---

## Pattern 5: Agentic System Prompt

### System Prompt Template

```python
AGENT_SYSTEM_PROMPT = """You are an autonomous coding agent with access to tools for:
- Searching and reading code
- Writing and modifying files
- Running commands
- Managing tasks

## Behavior Guidelines

1. **Think Step by Step**: Before acting, reason about what needs to be done
2. **Verify Changes**: After modifications, verify they work
3. **Handle Errors**: If something fails, analyze why and try alternatives
4. **Stay Focused**: Complete the current task before moving on
5. **Ask When Stuck**: If blocked, explain what you need

## Tool Usage

- Use search before assuming file locations
- Read files before modifying them
- Make incremental changes and test
- Commit logical units of work

## Output Format

When you complete a task or need to report:
- Summarize what was done
- List files changed
- Note any issues or concerns
- Suggest next steps if applicable

## Constraints

- Do not modify files outside the project directory
- Do not execute potentially dangerous commands
- Do not expose sensitive information
- Ask for confirmation before destructive actions
"""
```

---

## Pattern 6: Error Handling & Retry

### Robust API Calls

```python
import time
from anthropic import APIError, RateLimitError

def robust_api_call(func, max_retries: int = 3, base_delay: float = 1.0):
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            delay = base_delay * (2 ** attempt)
            print(f"Rate limited. Waiting {delay}s...")
            time.sleep(delay)
        except APIError as e:
            if attempt == max_retries - 1:
                raise
            print(f"API error: {e}. Retrying...")
            time.sleep(base_delay)

    raise Exception("Max retries exceeded")

# Usage
response = robust_api_call(
    lambda: client.messages.create(
        model="claude-opus-4-5-20251101",
        max_tokens=4096,
        messages=messages
    )
)
```

### Tool Error Handling

```python
def execute_tool_safely(name: str, inputs: dict) -> str:
    try:
        result = execute_tool(name, inputs)
        return json.dumps({"success": True, "result": result})
    except FileNotFoundError as e:
        return json.dumps({
            "success": False,
            "error": "file_not_found",
            "message": str(e)
        })
    except PermissionError as e:
        return json.dumps({
            "success": False,
            "error": "permission_denied",
            "message": str(e)
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": "unknown",
            "message": str(e)
        })
```

---

## Production Checklist

### Security

- [ ] API keys in environment variables
- [ ] Input validation on all tool inputs
- [ ] Sandboxed file operations
- [ ] Rate limiting on API calls
- [ ] Audit logging for tool executions

### Reliability

- [ ] Retry logic with exponential backoff
- [ ] Graceful degradation on failures
- [ ] Timeout handling
- [ ] Checkpointing for long operations
- [ ] Health monitoring

### Performance

- [ ] Response streaming for UX
- [ ] Conversation summarization for long sessions
- [ ] Caching for repeated queries
- [ ] Async operations where possible
- [ ] Resource cleanup

### Observability

- [ ] Request/response logging
- [ ] Tool execution tracing
- [ ] Error tracking
- [ ] Usage metrics
- [ ] Cost monitoring

---

## Quick Reference

### API Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `model` | Model to use | Required |
| `max_tokens` | Max output tokens | Required |
| `messages` | Conversation history | Required |
| `system` | System prompt | None |
| `tools` | Available tools | None |
| `tool_choice` | Force tool use | auto |
| `temperature` | Randomness (0-1) | 1.0 |
| `stop_sequences` | Stop generation | None |

### Stop Reasons

| Reason | Meaning |
|--------|---------|
| `end_turn` | Natural completion |
| `max_tokens` | Hit token limit |
| `stop_sequence` | Hit stop sequence |
| `tool_use` | Wants to use tool |

---

## Notes

- Always handle tool results before continuing
- Stream for better UX in interactive apps
- Use appropriate model for task complexity
- Monitor token usage for cost control
- Test agents thoroughly before production
