---
name: langchain
cluster: aimlops
description: "Framework for building applications with large language models and chains."
tags: ["langchain","llm","ai-framework"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "langchain ai ml framework llm chains"
---

# langchain

## Purpose
LangChain is a Python framework for developing applications that integrate large language models (LLMs) into workflows, enabling the creation of chains that combine multiple LLMs or tools for tasks like question answering or data processing.

## When to Use
Use LangChain when building AI-powered apps that require chaining LLMs, such as integrating multiple models for complex queries, or when you need to handle external data sources with LLMs. Apply it for rapid prototyping of AI agents, like chatbots that fetch real-time data, or for ML operations in aimlops clusters where scalable LLM workflows are needed.

## Key Capabilities
- **Chain Building**: Create sequences of LLMs using classes like `LLMChain`; for example, combine a prompt template with an LLM call.
- **Tool Integration**: Supports integrations with APIs like OpenAI via `OpenAI` class; handle vector stores with `FAISS` for semantic search.
- **Prompt Management**: Use `PromptTemplate` to define and render prompts dynamically, e.g., with variables for user input.
- **Agent Frameworks**: Build agents with tools using `AgentType.ZERO_SHOT_REACT`, allowing dynamic tool selection based on LLM output.
- **Async Support**: Leverage asynchronous chains for scalable applications, such as processing multiple queries concurrently.

## Usage Patterns
To use LangChain, install it via `pip install langchain`, then import and configure components. For basic chains, create an LLM instance and link it to prompts or tools. Pattern: Initialize an LLM with an API key, build a chain, and run it in a loop for iterative tasks. For agents, define tools and let the agent decide actions based on input.

## Common Commands/API
- **Installation and Setup**: Run `pip install langchain[all]` to include extras; set environment variables like `export OPENAI_API_KEY=your_key` for authentication.
- **Basic Chain Example**: 
  ```python
  from langchain.llms import OpenAI
  from langchain.chains import LLMChain
  llm = OpenAI(model_name="gpt-3.5-turbo")
  chain = LLMChain(llm=llm, prompt="What is {topic}?")
  result = chain.run(topic="LangChain")
  ```
- **API Endpoints**: When using LangChain with external services, call endpoints like `https://api.openai.com/v1/chat/completions` via LangChain wrappers; pass headers with auth tokens.
- **Config Formats**: Use YAML for chain configurations, e.g., in a file:
  ```
  chains:
    - name: simple_chain
      llm: OpenAI
      prompt: "Summarize {text}"
  ```
  Load with `from langchain.utilities import load_config`.
- **CLI Commands**: For LangChain CLI (if extended), use `langchain serve` to run chains as services, or debug with `langchain debug --chain my_chain` to trace executions.

## Integration Notes
Integrate LangChain with other tools by wrapping them as callable functions. For example, to add a database query tool, use `Tool.from_function` and pass it to an agent. Set env vars for keys, e.g., `$OPENAI_API_KEY` for OpenAI models or `$SERPAPI_API_KEY` for search integrations. When combining with aimlops cluster tools, ensure compatibility by using LangChain's callback system for logging; import `from langchain.callbacks import get_openai_callback` to track token usage. For vector databases, integrate with Pinecone by initializing `from langchain.vectorstores import Pinecone` and providing your API key via env var.

## Error Handling
Handle errors by wrapping chain runs in try-except blocks, e.g.:
```python
try:
    result = chain.run(input_data)
except ValueError as e:
    print(f"Invalid input: {e}")
except Exception as e:
    print(f"General error: {e} - Check API key or network")
```
Common issues include API rate limits (check with `if e.status_code == 429: retry()`), invalid API keys (verify `$OPENAI_API_KEY` is set), or chain misconfigurations (use `chain.validate()` if available). Log errors using LangChain's handlers for debugging in production.

## Concrete Usage Examples
1. **Simple Question-Answering Chain**: Build a chain to answer questions using an LLM and a vector store. First, set `export OPENAI_API_KEY=your_key`. Then:
   ```python
   from langchain.chains import RetrievalQA
   from langchain.llms import OpenAI
   qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff")
   answer = qa_chain.run({"query": "What is LangChain?"})
   ```
   This fetches relevant documents and generates a response.

2. **Agent for Web Search**: Create an agent that uses tools for web searches. Set `export SERPAPI_API_KEY=your_key`. Code:
   ```python
   from langchain.agents import AgentType, load_tools, initialize_agent
   from langchain.llms import OpenAI
   tools = load_tools(["serpapi"])
   agent = initialize_agent(tools, OpenAI(), agent=AgentType.ZERO_SHOT_REACT)
   response = agent.run("Search for latest AI news")
   ```
   The agent dynamically queries the web and returns results.

## Graph Relationships
- Related to cluster: aimlops (e.g., shares tools for ML operations).
- Connected via tags: langchain (self), llm (links to other LLM tools), ai-framework (connects to frameworks like Hugging Face).
- Dependencies: Requires OpenAI or similar APIs, integrates with vector stores like FAISS or Pinecone.
