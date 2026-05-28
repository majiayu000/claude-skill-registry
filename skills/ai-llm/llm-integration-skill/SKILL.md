---
name: llm-integration
version: 1.0
triggers: ["LLM", "provider", "fallback", "streaming"]
---

# LLM Integration SKILL

## Provider Abstraction

```python
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

llm = ChatOpenAI(model="gpt-4")
# or
llm = ChatAnthropic(model="claude-3-sonnet-20240229")
```

## Fallback Chain

```python
from langchain.chat_models import init_chat_model

llm = init_chat_model(
    "gpt-4",
    fallbacks=["claude-3-sonnet-20240229", "ollama/llama2"]
)
```

## Streaming

```python
for chunk in llm.stream("What is RAG?"):
    print(chunk.content, end="", flush=True)
```
