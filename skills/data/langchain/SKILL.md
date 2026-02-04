---
name: langchain
description: LangChain skill for building LLM orchestration, agents, RAG pipelines, tools, memory, callbacks, and deployment.
---

# LangChain - Skill

Purpose

This skill teaches the agent project specific conventions and concise patterns for building AI agent workflows with LangChain in Python. Use this when implementing chatbots, RAG pipelines, tool-enabled agents, multi-agent flows, or deploying runnables.

When an AI assistant should apply this skill

- Editing Python code that imports langchain or langchain_core
- Adding or changing agents, tools, retrievers, memory, or chains
- Writing pipeline glue code for RAG and vector stores
- Creating deployable runnables or LangServe endpoints

Quick start

1. Keep imports explicit and small. Prefer the Runnable interfaces for consistency. 2. Use typed small functions for tools. 3. Attach memory to chains or agents when conversation state is required. 4. Wrap external I/O behind tools to make tests deterministic.

Core concepts and cheat sheet

- LLMs and Runnables
  - Treat LLMs, chains, and tools as Runnable objects with invoke, batch, and stream methods.
  - Prefer explicit invocation: `result = llm.invoke("prompt")`.

- Prompts
  - Use ChatPromptTemplate for chat style flows and Template for single prompt flows.

- Tools
  - Define minimal pure functions and annotate with @tool where useful.
  - Keep tool side effects explicit and isolated.

- Agents
  - Create agents with the agent factory. Give the agent a short system style prompt and a curated tool list.

- Memory
  - Use ConversationBufferMemory for simple chat history. Use summarized or vectorized memory for long lived contexts.

- Retrievers and RAG
  - Index documents offline. At query time, call retriever.as_retriever or use RetrievalQA chain.

- Callbacks and middleware
  - Use callbacks for logging, telemetry, and custom token handling. Use middleware to enforce policies or rate limits.

- Deployment
  - Export runnables with LangServe or wrap them with FastAPI for custom routing.

Examples

1) Minimal chat chain with memory

```python
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory

prompt = ChatPromptTemplate.from_messages([
    {"role": "system", "content": "You are a concise helpful assistant."},
    {"role": "user", "content": "{question}"},
])

llm = ChatOpenAI(model="gpt-4o", temperature=0)
chain = LLMChain(llm=llm, prompt=prompt)
chain.memory = ConversationBufferMemory()

resp = chain.invoke({"question": "Explain RLHF in one paragraph."})
print(resp)
```

2) Define a deterministic tool and register it with an agent

```python
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

@tool
def calc(expression: str) -> str:
    """Evaluate a math expression safely."""
    # implement a safe eval or call a math microservice
    return str(eval(expression))

llm = ChatOpenAI(model="gpt-4o", temperature=0)
agent = create_agent(llm, tools=[calc])

result = agent.invoke({"input": "What is 12 * 7?"})
print(result)
```

3) RAG pipeline pattern

```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

# indexing (offline)
emb = OpenAIEmbeddings()
vect = Chroma.from_documents(docs, embedding=emb)
retriever = vect.as_retriever(search_kwargs={"k": 4})

qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4o"),
    retriever=retriever,
    chain_type="stuff",
)
answer = qa.invoke({"query": "How does caching in our app work?"})
print(answer)
```

4) Runnable batch and streaming

```python
# invoke in batch
questions = ["A?", "B?", "C?"]
for out in llm.batch_as_completed(questions):
    print(out)

# streaming
for token in llm.stream("Explain X step by step"):
    print(token, end="")
```

Middleware and callbacks pattern

- Implement a BaseCallbackHandler for custom logging or metrics.
- Create middleware to run before agent decision, for example to check quotas or to insert a human approval step.

Example callback handler

```python
from langchain_core.callbacks import BaseCallbackHandler

class SimpleLogger(BaseCallbackHandler):
    def on_llm_start(self, prompts, **kwargs):
        print("LLM start", len(prompts))

    def on_llm_end(self, response, **kwargs):
        print("LLM end")
```

Deployment snippet

```bash
# basic serve example
langserve serve my_chain.py --host 0.0.0.0 --port 8000
```

Guidelines and best practices

- Keep prompts short and test them with the same LLM configuration you will use in production.
- Unit test tools by mocking external calls. Keep side effects outside of agents when possible.
- Use retrievers with chunk overlap tuned to your retrieval needs.
- Prefer deterministic tool implementations for agent decisions that rely on exact operations.


---

