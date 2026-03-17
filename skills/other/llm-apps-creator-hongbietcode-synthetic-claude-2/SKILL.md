---
name: llm-apps-creator
description: This skill should be used when users want to build LLM-powered applications using LangChain. It provides patterns for initializing any LLM provider (OpenAI, Anthropic, Google, xAI), building agent loops with tools, and implementing structured output. Use this skill when users ask to create chatbots, AI agents, or applications that need LLM integration with tool calling or structured responses.
---

# LLM Apps Creator

## Overview

This skill provides essential patterns for building LLM-powered applications using LangChain. It covers three core concepts:

1. **Universal LLM Initialization** - Initialize any LLM provider with a single function
2. **Agent Loop Pattern** - The simple but powerful pattern used by top AI agents
3. **Structured Output** - Get predictable, validated responses from LLMs

## Core Philosophy

> "The main agent is just a loop. The session memory is just a list of messages. It is enough to build the most powerful agent in the world."

Forget complex frameworks like ReAct/Reflection agents. The same simple agent-loop pattern is used in one of the most powerful agents: Claude Code.

## Quick Start

### Initialize Any LLM

Use `init_chat_model` to initialize any LLM provider with automatic detection:

```python
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
load_dotenv()

# Auto-detects provider from model name
llm = init_chat_model("gpt-4.1")                    # OpenAI (needs OPENAI_API_KEY)
llm = init_chat_model("claude-sonnet-4-5-20250929") # Anthropic (needs ANTHROPIC_API_KEY)
llm = init_chat_model("grok-code-fast-1")           # xAI (needs XAI_API_KEY)

# Explicit provider specification
llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")  # Google
llm = init_chat_model("my-model", model_provider="openai")                # Custom
```

### Create Tools with DETAILED Docstrings

> **CRITICAL**: The docstring IS the prompt that tells the LLM how to use the tool. Poor docstrings = poor tool usage = broken agent.

```python
from langchain_core.tools import tool

# BAD - minimal docstring, LLM won't know how to use properly
@tool
def read_file(file_path: str) -> str:
    """Read a file."""  # DON'T DO THIS!
    ...

# GOOD - detailed docstring with usage guidelines
@tool("Read")  # Named tool for clarity
def read_file(file_path: str) -> str:
    """Reads a file from the local filesystem and returns its contents.

    ## Usage Guidelines
    - **file_path must be ABSOLUTE** (e.g., /Users/name/project/file.py), NOT relative
    - Returns file contents with line numbers in `cat -n` format
    - If file doesn't exist, returns an error message (this is OK, don't panic)

    ## When to Use
    - Reading source code to understand implementation
    - Checking configuration files
    - ALWAYS read a file BEFORE trying to edit or write to it

    ## Performance Tips
    - You can call this tool multiple times in parallel for different files

    Args:
        file_path: The ABSOLUTE path to the file (e.g., /Users/name/project/src/main.py)

    Returns:
        File contents with line numbers, or error message if file not found
    """
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        # Format with line numbers like cat -n
        result = []
        for i, line in enumerate(lines, 1):
            result.append(f"{i:6d}\t{line.rstrip()}")
        return "\n".join(result)
    except FileNotFoundError:
        return f"Error: File not found: {file_path}"
    except Exception as e:
        return f"Error reading file: {e}"
```

### More Tool Examples

```python
@tool("Write")
def write_file(file_path: str, content: str) -> str:
    """Writes content to a file, creating it if it doesn't exist or OVERWRITING if it does.

    ## Usage Guidelines
    - **file_path must be ABSOLUTE**, NOT relative
    - This will OVERWRITE the entire file - use Edit tool for partial modifications
    - **CRITICAL**: ALWAYS use Read tool first to check existing content!

    ## When to Use
    - Creating NEW files that don't exist yet
    - Completely replacing file contents

    ## When NOT to Use
    - Modifying existing files (use Edit tool instead)
    - If you haven't read the file first

    Args:
        file_path: The ABSOLUTE path to write to
        content: The complete content to write to the file

    Returns:
        Success message with file path, or error message
    """
    import os
    try:
        dir_path = os.path.dirname(file_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
        return f"Successfully wrote {len(content)} characters to {file_path}"
    except Exception as e:
        return f"Error writing file: {e}"

@tool("Bash")
def run_command(command: str, working_dir: str = None) -> str:
    """Executes a bash/shell command and returns the output (stdout + stderr).

    ## Usage Guidelines
    - Use for running scripts, builds, tests, git commands, etc.
    - Commands timeout after 30 seconds
    - Use absolute paths in commands to avoid directory confusion

    ## When to Use
    - Running build tools (npm, pip, cargo, make, etc.)
    - Git operations (git status, git diff, git commit, etc.)
    - Running tests (pytest, jest, cargo test, etc.)

    ## When NOT to Use
    - Reading files (use Read tool instead of cat/head/tail)
    - Searching files (use dedicated search tools instead of grep/find)

    Args:
        command: The shell command to execute
        working_dir: Optional working directory (absolute path)

    Returns:
        Command output (stdout + stderr combined), or error/timeout message
    """
    import subprocess
    import os
    try:
        cwd = working_dir if working_dir else os.getcwd()
        result = subprocess.run(
            command, shell=True, capture_output=True,
            text=True, timeout=30, cwd=cwd
        )
        output = result.stdout
        if result.stderr:
            output += f"\nSTDERR:\n{result.stderr}"
        if result.returncode != 0:
            output += f"\n[Exit code: {result.returncode}]"
        return output if output.strip() else "(Command completed with no output)"
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds"
    except Exception as e:
        return f"Error executing command: {e}"
```

### Initialize Agent with Tools

```python
from langchain.chat_models import init_chat_model

# Initialize LLM with tools
llm = init_chat_model("gpt-4.1")
llm_with_tools = llm.bind_tools([read_file, write_file, run_command])
```

### Get Structured Output

```python
from pydantic import BaseModel, Field
from langchain.agents import create_agent

class ContactInfo(BaseModel):
    """Contact information for a person."""
    name: str = Field(description="The name of the person")
    email: str = Field(description="The email address")
    phone: str = Field(description="The phone number")

agent = create_agent(
    model="gpt-4.1",
    response_format=ContactInfo  # Auto-selects best strategy
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract: John Doe, john@example.com, 555-1234"}]
})
print(result["structured_response"])
# ContactInfo(name='John Doe', email='john@example.com', phone='555-1234')
```

## The Agent Loop Pattern

The core pattern is deceptively simple:

```
1. User sends a message
2. LLM responds (possibly with tool calls)
3. If tool calls exist, execute them and feed results back
4. Repeat until LLM responds without tool calls
```

### Complete Agent Implementation

```python
from typing import List, Dict, Any, Optional
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_core.tools import BaseTool
from langchain.chat_models import init_chat_model

class SimpleAgent:
    """A minimal agent that uses tools to accomplish tasks."""

    def __init__(
        self,
        system_prompt: str,
        tools: List[BaseTool],
        model_name: str = "gpt-4.1",
        model_provider: Optional[str] = None,
    ):
        # Store tools in a map for quick lookup
        self.tools_map: Dict[str, BaseTool] = {tool.name: tool for tool in tools}

        # Create LLM with tools bound
        llm = init_chat_model(model_name, model_provider=model_provider)
        self.llm_with_tools = llm.bind_tools(tools)

        # Initialize conversation with system prompt
        self.messages: List[Any] = [SystemMessage(content=system_prompt)]

    def chat(self, user_input: str) -> str:
        """Process a user message and return the agent's response."""
        # Add user message to history
        self.messages.append(HumanMessage(content=user_input))

        # Get LLM response
        response = self.llm_with_tools.invoke(self.messages)
        self.messages.append(response)

        # Tool execution loop
        while hasattr(response, "tool_calls") and response.tool_calls:
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_id = tool_call["id"]

                # Execute the tool
                if tool_name in self.tools_map:
                    result = self.tools_map[tool_name].invoke(tool_args)
                else:
                    result = f"Error: Unknown tool '{tool_name}'"

                # Add tool result to conversation
                self.messages.append(
                    ToolMessage(content=str(result), tool_call_id=tool_id)
                )

            # Get next response (sees tool results)
            response = self.llm_with_tools.invoke(self.messages)
            self.messages.append(response)

        return response.content

    def reset(self):
        """Clear conversation history, keeping only system prompt."""
        self.messages = [self.messages[0]]
```

### Usage Example

```python
# Using the well-documented tools from above
agent = SimpleAgent(
    system_prompt="""You are a helpful coding assistant.
You can read files, write files, and run commands.
Always explain what you're doing before taking action.""",
    tools=[read_file, write_file, run_command],
    model_name="claude-sonnet-4-5-20250929",
)

response = agent.chat("List all Python files in the current directory")
print(response)
```

## Structured Output Patterns

### Strategy Selection

LangChain automatically selects the best strategy:

| Strategy | When Used | Reliability |
|----------|-----------|-------------|
| `ProviderStrategy` | Model supports native structured output (OpenAI, Anthropic, xAI) | Highest |
| `ToolStrategy` | All other models with tool calling | High |

### Schema Types Supported

1. **Pydantic Models** (recommended)
```python
from pydantic import BaseModel, Field

class ProductReview(BaseModel):
    """Analysis of a product review."""
    rating: int = Field(description="Rating 1-5", ge=1, le=5)
    sentiment: Literal["positive", "negative"]
    key_points: list[str]
```

2. **Dataclasses**
```python
from dataclasses import dataclass

@dataclass
class ContactInfo:
    name: str
    email: str
    phone: str
```

3. **TypedDict**
```python
from typing_extensions import TypedDict

class ContactInfo(TypedDict):
    name: str
    email: str
    phone: str
```

4. **JSON Schema**
```python
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"}
    },
    "required": ["name", "email"]
}
```

### Using ToolStrategy (Explicit)

For models without native structured output:

```python
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

agent = create_agent(
    model="gpt-4.1",
    tools=my_tools,
    response_format=ToolStrategy(ProductReview)
)
```

### Union Types for Multiple Schemas

```python
from typing import Union

class ProductReview(BaseModel):
    rating: int
    sentiment: str

class CustomerComplaint(BaseModel):
    issue_type: Literal["product", "service", "shipping"]
    severity: Literal["low", "medium", "high"]
    description: str

agent = create_agent(
    model="gpt-4.1",
    response_format=ToolStrategy(Union[ProductReview, CustomerComplaint])
)
```

### Error Handling

```python
# Custom error message
ToolStrategy(schema=MySchema, handle_errors="Please provide valid data.")

# Handle specific exceptions
ToolStrategy(schema=MySchema, handle_errors=ValueError)

# Custom handler function
def handle_error(e: Exception) -> str:
    return f"Error: {str(e)}. Please try again."

ToolStrategy(schema=MySchema, handle_errors=handle_error)

# Disable error handling (exceptions propagate)
ToolStrategy(schema=MySchema, handle_errors=False)
```

## Environment Setup

Required environment variables (set in `.env` file):

```bash
# OpenAI
OPENAI_API_KEY=sk-...

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Google
GOOGLE_API_KEY=...

# xAI (Grok)
XAI_API_KEY=...
```

## Best Practices

### Tool Design (MOST IMPORTANT)

> **The docstring IS the prompt.** Poor docstrings = poor tool usage = broken agent.

1. **Use named tools** - `@tool("Read")` not just `@tool` for clarity
2. **Write comprehensive docstrings** with:
   - **Usage Guidelines** - Requirements, constraints, formats
   - **When to Use** - Specific scenarios
   - **When NOT to Use** - Common mistakes to avoid
   - **Args** - Detailed parameter descriptions with examples
   - **Returns** - What the tool returns
3. **Include examples** in docstrings (e.g., "file_path must be ABSOLUTE like /Users/name/file.py")
4. **Document error behavior** - Tell LLM what errors look like and that they're OK

### Agent Design

1. **Keep it simple** - The basic loop pattern handles most use cases
2. **Handle errors gracefully** - Wrap tool execution in try/except
3. **Limit tool scope** - Give agent only tools it needs
4. **Use absolute paths** - Avoid confusion with relative paths

### Structured Output

1. **Use Pydantic for validation** - Built-in type checking and constraints
2. **Add Field descriptions** - Helps LLM understand expected format
3. **Use Literal for enums** - Constrains values to specific options
4. **Enable error handling** - Let LangChain retry on validation failures

### Model Selection

| Use Case | Recommended Model |
|----------|------------------|
| General tasks | `gpt-4.1` or `claude-sonnet-4-5-20250929` |
| Fast responses | `grok-code-fast-1` or `gemini-2.5-flash` |
| Complex reasoning | `claude-sonnet-4-5-20250929` or `gpt-4.1` |
| Cost-sensitive | `gpt-4.1-mini` or smaller models |

## Resources

### references/

This skill includes complete reference documentation:

- `base_n_powerful_agent.py` - Complete working agent implementation with tools
- `langchain_structured_output.md` - Comprehensive structured output documentation with all strategies and error handling patterns

Read these files for detailed examples and advanced patterns.
