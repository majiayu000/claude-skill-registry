---
name: aios-cerebrum
description: AIOS Agent Operating System and Cerebrum SDK for building, deploying, and orchestrating AI agents
icon: 🧠
category: agent-orchestration
tools:
  - aios
  - cerebrum
  - run-agent
  - list-agents
  - download-agent
  - upload-agent
---

# AIOS & Cerebrum: Agent Operating System

## Overview

**AIOS** (AI Agent Operating System) is a user-space agent kernel that provides syscall-like abstractions for AI agents. **Cerebrum** is the SDK that enables developers to build and deploy agents on AIOS.

Together, they form an **agent substrate layer** in the FlexStack architecture, complementing AGiXT for orchestration and LocalAI for inference.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          AGENT STACK                                     │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                   │
│  │  Your Agent  │  │  Your Agent  │  │  Your Agent  │   <- Cerebrum SDK │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘                   │
│         │                 │                 │                           │
│  ┌──────┴─────────────────┴─────────────────┴───────┐                   │
│  │              AIOS Kernel (Port 8000)             │   <- Agent Syscalls│
│  │   Scheduler | Memory | Storage | Tools | LLM    │                    │
│  └──────────────────────┬───────────────────────────┘                   │
│                         │                                               │
│  ┌──────────────────────┴───────────────────────────┐                   │
│  │              LocalAI (Port 8080)                 │   <- LLM Inference │
│  │   OpenAI-compatible API | Local Models          │                    │
│  └──────────────────────────────────────────────────┘                   │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────┐                   │
│  │              AGiXT (Port 7437)                   │   <- Orchestration │
│  │   Chains | Extensions | Memory | Multi-Agent    │                    │
│  └──────────────────────────────────────────────────┘                   │
└─────────────────────────────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites

```bash
# Enter full development shell
nom develop .#full

# Or use direnv
direnv allow
```

### Installation

```bash
# Install AIOS Kernel
aios install

# Install Cerebrum SDK (in AIOS pixi environment)
pixi run -e aios pip install aios-agent-sdk

# Verify installation
pixi run -e aios python -c "import cerebrum; print('Cerebrum SDK ready')"
```

### Starting Services

```bash
# 1. Start LocalAI (inference backend)
localai start

# 2. Start AIOS Kernel (agent syscalls)
aios start

# 3. (Optional) Start AGiXT (orchestration)
agixt up
```

### Running Your First Agent

```bash
# List available agents
pixi run -e aios list-agenthub-agents

# Run an agent from AgentHub
pixi run -e aios run-agent \
  --mode remote \
  --agent_author example \
  --agent_name test_agent \
  --task "What is the capital of France?"

# Run a local agent
pixi run -e aios run-agent \
  --mode local \
  --agent_path ./my_agent \
  --task "Your task here"
```

## AIOS Kernel Management

### Commands

| Command | Description |
|---------|-------------|
| `aios install` | Clone AIOS repository and setup |
| `aios start` | Start AIOS Kernel server (port 8000) |
| `aios stop` | Stop AIOS Kernel server |
| `aios status` | Check if AIOS is running |
| `aios config` | Show AIOS configuration |

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `AIOS_DIR` | `~/.local/share/aios` | Installation directory |
| `AIOS_PORT` | `8000` | Kernel server port |
| `AIOS_URL` | `http://localhost:8000` | Kernel API URL |
| `AIOS_VECTOR_DB` | `chroma` | Vector database (chroma/qdrant) |

### Configuration

Edit `~/.local/share/aios/AIOS/aios/config/config.yaml`:

```yaml
api_keys:
  openai: "sk-..."        # OpenAI API key
  anthropic: "sk-..."     # Claude API key
  gemini: "..."           # Google Gemini key
  groq: "..."             # Groq fast inference
  huggingface_token: ""   # HuggingFace access

llm_models:
  - name: "gpt-4"
    backend: "openai"
  - name: "claude-3-opus"
    backend: "anthropic"
  - name: "local-model"
    backend: "ollama"     # For LocalAI models

storage:
  vector_db:
    type: "chroma"        # or "qdrant"

server:
  host: "localhost"
  port: 8000
```

## Cerebrum SDK

### Agent Structure

```
my_agent/
├── entry.py              # Main agent implementation
├── config.json           # Agent metadata
└── meta_requirements.txt # Additional dependencies (optional)
```

### Agent Configuration (config.json)

```json
{
  "name": "ros2_controller",
  "description": [
    "ROS2-aware agent that can control robot systems"
  ],
  "tools": [
    "my_org/ros2_topic_tool",
    "my_org/ros2_service_tool"
  ],
  "meta": {
    "author": "my_org",
    "version": "0.0.1",
    "license": "MIT"
  },
  "build": {
    "entry": "entry.py",
    "module": "ROS2ControllerAgent"
  }
}
```

### Basic Agent Implementation

```python
# entry.py
from cerebrum.llm.apis import llm_chat
from cerebrum.memory.apis import memory_read, memory_write
from cerebrum.storage.apis import storage_read, storage_write
from cerebrum.tool.apis import tool_call

class ROS2ControllerAgent:
    def __init__(self):
        self.name = "ROS2 Controller"

    def run(self, task: str) -> str:
        # Use LLM to understand the task
        response = llm_chat(
            messages=[
                {"role": "system", "content": "You are a ROS2 robot controller."},
                {"role": "user", "content": task}
            ],
            model="gpt-4"
        )

        # Use tools to interact with ROS2
        if "topic" in task.lower():
            result = tool_call("ros2_topic_tool", {"action": "list"})

        # Store context in memory
        memory_write("last_task", task)

        return response
```

### Tool Development

```python
# tools/ros2_topic_tool/entry.py
class ROS2TopicTool:
    def __init__(self):
        self.name = "ros2_topic_tool"

    def run(self, params: dict) -> str:
        action = params.get("action", "list")
        topic = params.get("topic", "")

        if action == "list":
            import subprocess
            result = subprocess.run(
                ["ros2", "topic", "list"],
                capture_output=True,
                text=True
            )
            return result.stdout
        elif action == "echo":
            # Echo topic messages
            pass

        return "Unknown action"

    def get_tool_call_format(self):
        return {
            "type": "function",
            "function": {
                "name": "ros2_topic_tool",
                "description": "Interact with ROS2 topics",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["list", "echo", "pub"],
                            "description": "Action to perform"
                        },
                        "topic": {
                            "type": "string",
                            "description": "Topic name"
                        }
                    },
                    "required": ["action"]
                }
            }
        }
```

## CLI Commands

### Agent Management

```bash
# List available agents
pixi run -e aios list-agenthub-agents
pixi run -e aios list-local-agents

# Download agent from AgentHub
pixi run -e aios download-agent \
  --agent_author example \
  --agent_name demo_agent \
  --agent_version 0.0.1

# Upload agent to AgentHub
pixi run -e aios upload-agents \
  --agent_path ./my_agent \
  --agenthub_url https://app.aios.foundation
```

### Tool Management

```bash
# List available tools
pixi run -e aios list-toolhub-tools
pixi run -e aios list-local-tools

# Download tool
pixi run -e aios download-tool \
  --tool_author example \
  --tool_name arxiv \
  --tool_version 0.0.1
```

### LLM Management

```bash
# List available LLMs
pixi run -e aios list-available-llms
```

## Integration with FlexStack

### LocalAI Integration

AIOS uses LocalAI as an inference backend through the `ollama` provider:

```yaml
# In AIOS config.yaml
llm_models:
  - name: "gemma-3n-E2B"
    backend: "ollama"
  - name: "phi-4-mini"
    backend: "ollama"
```

LocalAI provides OpenAI-compatible endpoints on port 8080.

### AGiXT Integration

AIOS and AGiXT can work together:

- **AGiXT**: High-level orchestration, chains, extensions, multi-agent coordination
- **AIOS**: Low-level agent kernel, syscalls, resource management

```python
# Use AGiXT for orchestration
import requests

# Use AIOS for agent execution
from cerebrum.client import Cerebrum

# Example: AGiXT triggers AIOS agent
agixt_response = requests.post(
    "http://localhost:7437/api/v1/run_chain",
    json={"chain_name": "ros2_task", "input": "Navigate to waypoint"}
)

# AIOS handles the actual agent execution
cerebrum = Cerebrum()
result = cerebrum.run_agent("ros2_controller", "Move to position (1, 2, 0)")
```

### ROS2 Integration

Build ROS2-aware agents using Cerebrum:

```python
# ros2_agent/entry.py
import rclpy
from rclpy.node import Node
from cerebrum.tool.apis import tool_call

class ROS2AgentNode(Node):
    def __init__(self):
        super().__init__('aios_agent')
        # ROS2 node with AIOS agent capabilities

    def process_task(self, task: str):
        # Use AIOS tools within ROS2 context
        result = tool_call("llm_reasoning", {"prompt": task})
        return result
```

## Pixi Environments

### Default Environment

```bash
# Standard ROS2 development (no AIOS)
pixi run python your_script.py
```

### AIOS Environment

```bash
# AIOS with strict dependency pins
pixi run -e aios python your_script.py

# Run AIOS agent
pixi run -e aios run-agent --mode local --agent_path ./my_agent --task "Hello"
```

### AIOS + CUDA Environment

```bash
# AIOS with GPU support (vLLM backend)
pixi run -e aios-cuda python your_script.py
```

## Troubleshooting

### AIOS Kernel Not Starting

```bash
# Check if port 8000 is in use
lsof -i :8000

# Check AIOS installation
ls -la ~/.local/share/aios/AIOS

# Reinstall if needed
rm -rf ~/.local/share/aios/AIOS
aios install
```

### Dependency Conflicts

AIOS requires strict dependency versions. Use the dedicated pixi environment:

```bash
# Wrong: mixing environments
pip install aios-agent-sdk  # May conflict with ROS2

# Correct: use AIOS environment
pixi run -e aios pip install aios-agent-sdk
```

### LLM Connection Issues

```bash
# Check LocalAI is running
localai status

# Verify API endpoint
curl http://localhost:8080/v1/models

# Check AIOS config points to LocalAI
cat ~/.local/share/aios/AIOS/aios/config/config.yaml | grep -A5 "ollama"
```

## Resources

- **AIOS GitHub**: [agiresearch/AIOS](https://github.com/agiresearch/AIOS)
- **Cerebrum GitHub**: [agiresearch/Cerebrum](https://github.com/agiresearch/Cerebrum)
- **AIOS Documentation**: [docs.aios.foundation](https://docs.aios.foundation/)
- **AgentHub**: [app.aios.foundation](https://app.aios.foundation)
- **PyPI**: [aios-agent-sdk](https://pypi.org/project/aios-agent-sdk/)

## Related Skills

- [AI Assistants](../ai-assistants/SKILL.md) - LocalAI, AGiXT, aichat, aider
- [Rust Tooling](../rust-tooling/SKILL.md) - AGiXT Rust SDK
- [Distributed Systems](../distributed-systems/SKILL.md) - NATS, Temporal
- [ROS2 Development](../ros2-development/SKILL.md) - ROS2 integration patterns
