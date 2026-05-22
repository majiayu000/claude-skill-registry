---
name: chainlit
description: Expert guidance for building conversational AI applications with Chainlit framework in Python. Use when (1) creating chat interfaces for LLM applications, (2) building apps with OpenAI, LangChain, LlamaIndex, or Mistral AI, (3) implementing streaming responses, (4) adding UI elements like images, files, charts, (5) handling user file uploads, (6) implementing authentication (OAuth, password), (7) creating multi-step workflows with visible steps, (8) building RAG applications with document upload, or (9) deploying chat apps to web, Slack, Discord, or Teams.
---

# Chainlit

Build production-ready conversational AI applications in Python with rich UI.

## Installation

```bash
pip install chainlit
```

## Quick Start

```python
import chainlit as cl

@cl.on_message
async def on_message(message: cl.Message):
    await cl.Message(content=f"You said: {message.content}").send()
```

Run with:
```bash
chainlit run app.py -w
```

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Messages** | Text communication between user and assistant |
| **Steps** | Visible processing stages (LLM calls, tool use) |
| **Elements** | Rich UI (images, files, charts, dataframes) |
| **Actions** | Interactive buttons with callbacks |
| **Sessions** | Per-user state management |

## Lifecycle Hooks

```python
import chainlit as cl

@cl.on_chat_start
async def start():
    cl.user_session.set("history", [])
    await cl.Message(content="Hello!").send()

@cl.on_message
async def on_message(message: cl.Message):
    await cl.Message(content="Got it!").send()

@cl.on_chat_end
async def end():
    print("Session ended")
```

## Streaming Responses

```python
from openai import AsyncOpenAI
import chainlit as cl

client = AsyncOpenAI()
cl.instrument_openai()

@cl.on_message
async def on_message(message: cl.Message):
    msg = cl.Message(content="")
    await msg.send()

    stream = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": message.content}],
        stream=True
    )

    async for chunk in stream:
        if token := chunk.choices[0].delta.content:
            await msg.stream_token(token)

    await msg.update()
```

## Steps (Chain of Thought)

```python
@cl.step(type="tool")
async def search(query: str):
    return f"Results for: {query}"

@cl.step(type="llm")
async def generate(context: str):
    return await llm_call(context)

@cl.on_message
async def on_message(message: cl.Message):
    results = await search(message.content)
    answer = await generate(results)
    await cl.Message(content=answer).send()
```

## User Session

```python
@cl.on_chat_start
async def start():
    cl.user_session.set("counter", 0)

@cl.on_message
async def on_message(message: cl.Message):
    count = cl.user_session.get("counter")
    count += 1
    cl.user_session.set("counter", count)
```

## Ask User for Input

```python
# Text input
response = await cl.AskUserMessage(content="What's your name?").send()
name = response.get("output") if response else "Anonymous"

# File upload
files = await cl.AskFileMessage(
    content="Upload a file",
    accept=["text/plain", "application/pdf"]
).send()

# Action selection
response = await cl.AskActionMessage(
    content="Choose:",
    actions=[
        cl.Action(name="yes", label="Yes"),
        cl.Action(name="no", label="No"),
    ]
).send()
```

## UI Elements

```python
@cl.on_message
async def on_message(message: cl.Message):
    elements = [
        cl.Text(name="code.py", content="print('hello')", language="python"),
        cl.Image(name="chart", path="./chart.png", display="inline"),
        cl.File(name="report.pdf", path="./report.pdf"),
    ]

    await cl.Message(content="Results:", elements=elements).send()
```

## Actions (Buttons)

```python
@cl.action_callback("approve")
async def on_approve(action: cl.Action):
    await action.remove()
    await cl.Message(content="Approved!").send()

@cl.on_message
async def on_message(message: cl.Message):
    actions = [cl.Action(name="approve", label="Approve")]
    await cl.Message(content="Review:", actions=actions).send()
```

## Reference Documentation

For detailed guidance:

- **[lifecycle.md](references/lifecycle.md)** - on_chat_start, on_message, on_chat_end hooks
- **[messages.md](references/messages.md)** - Message class, streaming, chat_context
- **[steps.md](references/steps.md)** - Step decorator, context manager, nested steps
- **[elements.md](references/elements.md)** - Text, Image, File, PDF, Audio, Video, Plotly
- **[actions.md](references/actions.md)** - Action buttons, callbacks, payloads
- **[ask-user.md](references/ask-user.md)** - AskUserMessage, AskFileMessage, AskActionMessage
- **[session.md](references/session.md)** - User session, reserved keys, state management
- **[auth.md](references/auth.md)** - Password, OAuth, header authentication
- **[integrations.md](references/integrations.md)** - OpenAI, LangChain, LlamaIndex, Mistral
- **[patterns.md](references/patterns.md)** - RAG, document Q&A, multi-agent, feedback

## Integrations

```python
# OpenAI
cl.instrument_openai()

# LangChain
config = RunnableConfig(callbacks=[cl.LangchainCallbackHandler()])

# LlamaIndex
callback_manager = CallbackManager([cl.LlamaIndexCallbackHandler()])
```

## Configuration

`.chainlit/config.toml`:
```toml
[project]
name = "My App"

[UI]
cot = "full"  # Show chain of thought: full, hidden, tool_call
```

## Run Commands

```bash
# Development with auto-reload
chainlit run app.py -w

# Production
chainlit run app.py --host 0.0.0.0 --port 8000

# Generate auth secret
chainlit create-secret
```

## Key Imports

```python
import chainlit as cl

# Core
cl.Message, cl.Step, cl.Action

# Elements
cl.Text, cl.Image, cl.File, cl.Pdf, cl.Audio, cl.Video
cl.Plotly, cl.Dataframe, cl.TaskList

# Ask User
cl.AskUserMessage, cl.AskFileMessage, cl.AskActionMessage

# Decorators
@cl.on_chat_start, @cl.on_message, @cl.on_chat_end
@cl.step, @cl.action_callback
@cl.password_auth_callback, @cl.oauth_callback
```
