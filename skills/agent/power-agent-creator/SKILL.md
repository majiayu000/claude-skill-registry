---
name: power-agent-creator
description: This skill should be used when users want to create powerful AI agents comparable to Claude Code or sonph-code. It provides battle-tested system prompts, masterfully-crafted tool implementations, and the simple but powerful agent loop pattern. Use this skill when users ask to build coding agents, AI assistants with tools, or any autonomous agent that needs file operations, code execution, search, and task management capabilities. The key insight is that customization requires only ONE HumanMessage after the SystemPrompt.
---

# Power Agent Creator

## Overview

This skill provides everything needed to create powerful AI agents comparable to Claude Code. It includes:

1. **Battle-tested System Prompt** - A masterpiece prompt refined through millions of dollars of evaluation
2. **Production-ready Tools** - Comprehensive toolset for file ops, search, execution, and task management
3. **The Agent Loop** - The same simple pattern used by the most powerful agents

## Core Philosophy

> "The main agent is just a loop. The session memory is just a list of messages. It is enough to build the most powerful agent in the world. PERIOD!"

**CRITICAL**: Do NOT modify the system prompts or tool descriptions. They are masterpieces refined through extensive evaluation.

## The Customization Secret

To create ANY kind of agent, you only need to add ONE `HumanMessage` after the `SystemMessage`:

```python
from langchain_core.messages import SystemMessage, HumanMessage
from prompts import coding_agent_prompt

messages = [
    SystemMessage(content=coding_agent_prompt()),
    HumanMessage(content="""You are now specialized as a [ROLE].

Your additional capabilities:
- [CAPABILITY 1]
- [CAPABILITY 2]

Your constraints:
- [CONSTRAINT 1]
- [CONSTRAINT 2]

Focus on: [SPECIFIC DOMAIN]"""),
]
```

## Quick Start: Create a Specialized Agent

### Step 1: Initialize with Base System Prompt

```python
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
load_dotenv()

# Import the masterpiece system prompt - DO NOT MODIFY
from references.prompts import coding_agent_prompt

# Initialize any LLM
llm = init_chat_model("grok-code-fast-1")  # or gpt-4.1, grok-code-fast-1

# Start with base system prompt
messages = [SystemMessage(content=coding_agent_prompt())]
```

### Step 2: Add Specialization Message

```python
# Add ONE HumanMessage to specialize the agent
specialization = HumanMessage(content="""You are now a specialized DevOps Agent.

Additional expertise:
- Docker and Kubernetes configurations
- CI/CD pipeline management
- Infrastructure as Code (Terraform, Ansible)
- Cloud platforms (AWS, GCP, Azure)

When working on tasks:
1. Always check existing infrastructure code first
2. Follow GitOps principles
3. Prefer declarative over imperative approaches
4. Document all changes in infrastructure comments""")

messages.append(specialization)
```

### Step 3: Bind Tools and Create Agent

```python
# Import production-ready tools - DO NOT MODIFY THEIR DOCSTRINGS
from references.tools import (
    read_file, write_file, edit_file, list_files,  # File operations
    glob_files, grep_files,                         # Search tools
    bash, get_bash_output, todo_write,              # Execution & task management
)

# Bind tools to LLM
tools = [read_file, write_file, edit_file, list_files,
         glob_files, grep_files, bash, get_bash_output, todo_write]
llm_with_tools = llm.bind_tools(tools)
```

### Step 4: Run the Agent Loop

```python
from langchain_core.messages import ToolMessage

def run_agent(user_input: str):
    messages.append(HumanMessage(content=user_input))

    response = llm_with_tools.invoke(messages)
    messages.append(response)

    # Tool execution loop
    while hasattr(response, "tool_calls") and response.tool_calls:
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_id = tool_call["id"]

            # Execute tool (map name to function)
            tools_map = {t.name: t for t in tools}
            result = tools_map[tool_name].invoke(tool_args)

            messages.append(ToolMessage(content=str(result), tool_call_id=tool_id))

        response = llm_with_tools.invoke(messages)
        messages.append(response)

    return response.content
```

## Specialization Examples

### Data Science Agent

```python
specialization = HumanMessage(content="""You are now a specialized Data Science Agent.

Additional expertise:
- Pandas, NumPy, and scikit-learn workflows
- Data cleaning, feature engineering, and EDA
- Statistical analysis and hypothesis testing
- Machine learning model development and evaluation

When working on tasks:
1. Always explore data before analysis (df.info(), df.describe())
2. Check for missing values and data quality issues
3. Document assumptions and methodology
4. Provide reproducible code with clear explanations""")
```

### Security Analyst Agent

```python
specialization = HumanMessage(content="""You are now a specialized Security Analyst Agent.

Additional expertise:
- Code vulnerability analysis (OWASP Top 10)
- Security best practices review
- Authentication and authorization patterns
- Secrets management and encryption

When working on tasks:
1. Always scan for hardcoded secrets first
2. Check for injection vulnerabilities
3. Review authentication flows
4. Document all findings with severity levels""")
```

### Full-Stack Developer Agent

```python
specialization = HumanMessage(content="""You are now a specialized Full-Stack Developer Agent.

Additional expertise:
- React/Vue/Next.js frontend development
- Node.js/Python backend APIs
- Database design and optimization
- API design and RESTful principles

When working on tasks:
1. Check existing patterns in the codebase
2. Follow the project's code style
3. Write tests for new functionality
4. Consider performance implications""")
```

### Documentation Agent

```python
specialization = HumanMessage(content="""You are now a specialized Documentation Agent.

Additional expertise:
- Technical writing and API documentation
- README creation and maintenance
- Code comment standards
- Architecture decision records (ADRs)

When working on tasks:
1. Read the code thoroughly before documenting
2. Use clear, concise language
3. Include examples for all features
4. Keep documentation close to the code""")
```

## Complete Agent Class

```python
from typing import List, Dict, Any, Optional
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_core.tools import BaseTool
from langchain.chat_models import init_chat_model

class PowerAgent:
    """A powerful agent comparable to Claude Code."""

    def __init__(
        self,
        specialization: str = None,
        tools: List[BaseTool] = None,
        model_name: str = "grok-code-fast-1",
        working_dir: str = None,
    ):
        from references.prompts import coding_agent_prompt
        from references.tools import (
            read_file, write_file, edit_file, list_files,
            glob_files, grep_files, bash, get_bash_output, todo_write,
        )

        # Use provided tools or defaults
        self.tools = tools or [
            read_file, write_file, edit_file, list_files,
            glob_files, grep_files, bash, get_bash_output, todo_write,
        ]
        self.tools_map: Dict[str, BaseTool] = {t.name: t for t in self.tools}

        # Initialize LLM with tools
        llm = init_chat_model(model_name)
        self.llm_with_tools = llm.bind_tools(self.tools)

        # Initialize messages with system prompt
        self.messages: List[Any] = [
            SystemMessage(content=coding_agent_prompt(working_dir))
        ]

        # Add specialization if provided
        if specialization:
            self.messages.append(HumanMessage(content=specialization))

    def chat(self, user_input: str) -> str:
        """Process user input and return response."""
        self.messages.append(HumanMessage(content=user_input))

        response = self.llm_with_tools.invoke(self.messages)
        self.messages.append(response)

        # Tool execution loop
        while hasattr(response, "tool_calls") and response.tool_calls:
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_id = tool_call["id"]

                if tool_name in self.tools_map:
                    result = self.tools_map[tool_name].invoke(tool_args)
                else:
                    result = f"Error: Unknown tool '{tool_name}'"

                self.messages.append(
                    ToolMessage(content=str(result), tool_call_id=tool_id)
                )

            response = self.llm_with_tools.invoke(self.messages)
            self.messages.append(response)

        return response.content

    def reset(self):
        """Reset conversation, keeping system prompt and specialization."""
        # Keep first 1-2 messages (system + optional specialization)
        keep_count = 2 if len(self.messages) > 1 and isinstance(self.messages[1], HumanMessage) else 1
        self.messages = self.messages[:keep_count]
```

## Usage Example

```python
# Create a DevOps agent
agent = PowerAgent(
    specialization="""You are now a specialized DevOps Agent.

    Focus on: Docker, Kubernetes, CI/CD, and infrastructure as code.
    Always check existing infrastructure patterns first.""",
    model_name="grok-code-fast-1",
)

# Use the agent
response = agent.chat("Set up a Dockerfile for a Python FastAPI application")
print(response)
```

## Available Tools Reference

The skill includes these production-ready tools (DO NOT modify their docstrings):

### File Operations
- **Read** - Read files with line numbers, supports images/PDFs/notebooks
- **Write** - Write files with overwrite protection
- **Edit** - Precise string replacement in files
- **LS** - List directory contents

### Search Tools
- **Glob** - Fast file pattern matching (`**/*.py`)
- **Grep** - Powerful ripgrep-based content search

### Execution Tools
- **Bash** - Execute shell commands with timeout and background support
- **BashOutput** - Monitor background processes
- **KillBash** - Terminate background processes

### Task Management
- **TodoWrite** - Create and manage structured task lists

### Web Tools (Optional)
- **web_fetch** - Fetch and analyze web content
- **web_search** - Search the web for information

## Resources

### references/

This skill includes complete, production-ready code:

- `prompts.py` - The battle-tested system prompt (DO NOT MODIFY)
- `base_n_powerful_agent.py` - The simple agent loop pattern
- `tools/` - All tool implementations:
  - `file_tools.py` - Read, Write, Edit, LS
  - `search_tools.py` - Glob, Grep
  - `execution_tools.py` - Bash, BashOutput, KillBash, TodoWrite
  - `task_tool.py` - Task delegation to sub-agents
  - `web_fetch_tool.py` - Web content fetching
  - `web_search_tool.py` - Web search

**IMPORTANT**: The tool docstrings are masterpieces of prompt engineering. They cost millions of dollars to refine. DO NOT modify them - they are the key to proper tool usage by the LLM.
